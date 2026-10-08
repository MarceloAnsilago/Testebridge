from datetime import date
from uuid import UUID, uuid4
import streamlit as st
from bridge_client import BridgeError, call, validated_url

PERIODS = ('M1','M2','M3','M4','M5','M6','M10','M12','M15','M20','M30','H1','H2','H3','H4','H6','H8','H12','D1','W1','MN1')
st.set_page_config(page_title='MT5 Optimization Bridge', page_icon='📊', layout='wide')
st.title('MT5 Optimization Bridge')
st.caption('Streamlit Cloud → seu PC → Strategy Tester do MT5')

try:
    saved_bridge = dict(st.secrets.get('bridge', {}))
except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
    saved_bridge = {}

with st.sidebar:
    st.header('Conectar ao seu PC')
    st.caption('Inicie a API e o túnel no Windows. A chave autoriza somente os testes desta bridge.')
    with st.form('connection_form'):
        url = st.text_input('URL da bridge', value=saved_bridge.get('url', ''), placeholder='https://nome-do-tunel.trycloudflare.com')
        if saved_bridge.get('token'):
            token = saved_bridge['token']
            st.caption('Chave salva nos Secrets do aplicativo.')
        else:
            token = st.text_input('Chave de acesso', type='password')
        connect = st.form_submit_button('Conectar')
    if connect:
        for key in ('connection','job_id','pending_request','pending_payload','result','health'):
            st.session_state.pop(key,None)
        try:
            health = call(url,token,'/v1/health')
            if health.get('service') != 'mt5-optimization-bridge' or health.get('version') != 1:
                raise BridgeError('Serviço incompatível.')
            st.session_state.connection = (validated_url(url),token)
            st.session_state.health = health
        except BridgeError as exc:
            st.error(str(exc))
    if 'connection' in st.session_state:
        st.success('Bridge conectada')
        if st.button('Desconectar'):
            st.session_state.clear()
            st.rerun()
    else:
        st.info('Aguardando conexão com a bridge local.')

connection = st.session_state.get('connection')
health = st.session_state.get('health',{})
if connection:
    st.info(health.get('message','Conectado.'))
    if st.button('Verificar conexão / disponibilidade'):
        try:
            st.session_state.health = call(*connection,'/v1/health')
            st.rerun()
        except BridgeError as exc:
            st.error(str(exc))
else:
    st.info('Conecte sua bridge na barra lateral para habilitar as otimizações.')

def heavy_preset():
    st.session_state.update(test_start=date(2025,1,1), test_end=date(2026,1,1),
                            test_period='H1', test_ma_start=5, test_ma_step=1, test_ma_stop=1004)

st.button('Carregar teste pesado — 1.000 passes / 2025 inteiro', on_click=heavy_preset)

with st.form('optimization'):
    st.subheader('Parâmetros do teste')
    a,b,c=st.columns(3)
    symbol=a.text_input('Símbolo exato','EURUSD')
    period=b.selectbox('Período',PERIODS,index=PERIODS.index('H1'),key='test_period')
    currency=c.text_input('Moeda','USD')
    a,b,c=st.columns(3)
    start=a.date_input('Data inicial',date(2025,1,1),key='test_start')
    end=b.date_input('Data final (limite do teste)',date(2025,2,1),key='test_end')
    deposit=c.number_input('Depósito',min_value=1.0,max_value=100000000.0,value=10000.0)
    st.subheader('Intervalo da média móvel')
    a,b,c=st.columns(3)
    ma_start=a.number_input('MA inicial',min_value=1,max_value=10000,value=5,step=1,key='test_ma_start')
    ma_step=b.number_input('Passo',min_value=1,max_value=10000,value=5,step=1,key='test_ma_step')
    ma_stop=c.number_input('MA final',min_value=1,max_value=10000,value=20,step=1,key='test_ma_stop')
    st.caption('EA de teste • SL 400 pontos • TP 800 pontos • lote mínimo. Feche o MT5 antes de iniciar. Prazo máximo: 10 minutos; no timeout o terminal é preservado.')
    submit=st.form_submit_button('OTIMIZAR NO MT5',type='primary',disabled=not connection)

if submit and connection:
    payload=dict(symbol=symbol,period=period,start=start.isoformat(),end=end.isoformat(),
                 deposit=deposit,currency=currency,ma_start=ma_start,ma_step=ma_step,ma_stop=ma_stop)
    if start>=end or ma_stop<=ma_start or (ma_stop-ma_start)%ma_step or (ma_stop-ma_start)//ma_step+1>1000:
        st.error('Confira as datas e o intervalo MA (2 a 1.000 passes, final alcançável pelo passo).')
    else:
        # Reutiliza o ID em caso de resposta perdida, evitando otimização duplicada.
        if payload != st.session_state.get('pending_payload'):
            st.session_state.pending_payload=payload
            st.session_state.pending_request=str(uuid4())
        try:
            job=call(*connection,'/v1/jobs',dict(payload,request_id=st.session_state.pending_request))
            st.session_state.job_id=job['id']
            st.session_state.pop('result',None)
            st.session_state.pop('pending_payload',None)
            st.session_state.pop('pending_request',None)
        except BridgeError as exc:
            st.error(str(exc))

st.subheader('Resultados')
if connection:
    with st.expander('Retomar acompanhamento por ID'):
        resume=st.text_input('ID do trabalho')
        if st.button('Acompanhar trabalho'):
            try:
                st.session_state.job_id=str(UUID(resume))
                st.session_state.pop('result',None)
            except ValueError:
                st.error('ID inválido.')

@st.fragment(run_every='5s')
def progress():
    identifier=st.session_state.get('job_id')
    if not identifier or not connection:
        st.write('Nenhuma otimização em acompanhamento.')
        return
    st.caption(f'ID do trabalho: {identifier}')
    try:
        saved=st.session_state.get('result')
        job=saved if saved and saved.get('id')==identifier else call(*connection,f'/v1/jobs/{identifier}')
        if job['status'] in ('queued','running'):
            st.info('Na fila local.' if job['status']=='queued' else 'MT5 executando a otimização…')
        elif job['status']=='failed':
            st.session_state.result=job
            st.error(job['error'])
        elif job['status']=='completed':
            if 'csv_bytes' not in job:
                job['csv_bytes']=call(*connection,f'/v1/jobs/{identifier}/csv')
            st.session_state.result=job
            st.success(f'{len(job["rows"])} passes confirmados no relatório nativo.')
            if job['missing']: st.warning('Campos ausentes: '+', '.join(job['missing']))
            st.dataframe(job['rows'],hide_index=True,use_container_width=True)
            st.download_button('Baixar CSV',job['csv_bytes'],file_name=f'{identifier}.csv',mime='text/csv')
            with st.expander('Tabela original — conferir campos e unidades'):
                st.dataframe(job['original'],hide_index=True,use_container_width=True)
    except BridgeError as exc:
        st.error(str(exc))
progress()
