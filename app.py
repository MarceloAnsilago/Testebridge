"""Interface independente; a conexão com a bridge será implementada depois."""
from datetime import date

import streamlit as st

PERIODS = ('M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M10', 'M12', 'M15',
           'M20', 'M30', 'H1', 'H2', 'H3', 'H4', 'H6', 'H8', 'H12', 'D1', 'W1', 'MN1')

st.set_page_config(page_title='MT5 Optimization Bridge', page_icon='📊', layout='wide')
st.title('MT5 Optimization Bridge')
st.caption('Configuração de otimizações • Strategy Tester')
st.info('Bridge local ainda não conectada. Você pode ajustar os parâmetros abaixo; '
        'a otimização ficará disponível após a conexão com o MT5 no seu computador.')

st.subheader('Parâmetros do teste')
a, b, c = st.columns(3)
symbol = a.text_input('Símbolo exato', 'EURUSD', help='Inclua o sufixo da corretora, quando houver.')
period = b.selectbox('Período', PERIODS, index=PERIODS.index('H1'))
currency = c.text_input('Moeda', 'USD')
a, b, c = st.columns(3)
start = a.date_input('Data inicial', date(2025, 1, 1))
end = b.date_input('Data final (limite do teste)', date(2025, 2, 1))
deposit = c.number_input('Depósito', min_value=1.0, value=10000.0)

st.subheader('Intervalo da média móvel')
a, b, c = st.columns(3)
ma_start = a.number_input('MA inicial', min_value=1, value=5, step=1)
ma_step = b.number_input('Passo', min_value=1, value=5, step=1)
ma_stop = c.number_input('MA final', min_value=1, value=20, step=1)

if start >= end:
    st.warning('A data final deve ser posterior à data inicial.')
if ma_stop <= ma_start or (ma_stop - ma_start) % ma_step:
    st.warning('Escolha um MA final maior que o inicial e alcançável pelo passo informado.')
else:
    count = (ma_stop - ma_start) // ma_step + 1
    if count > 1000:
        st.warning('Solicite no máximo 1.000 passes por otimização.')
    else:
        st.caption(f'{count} passes previstos na otimização completa.')

st.caption('EA de teste previsto: SMA do candle anterior • SL 400 pontos • '
           'TP 800 pontos • lote mínimo • uma posição por vez.')
st.button('OTIMIZAR NO MT5', type='primary', disabled=True,
          help='Disponível após a conexão com a bridge local.')
st.subheader('Resultados')
st.write('Nenhuma otimização executada. Os resultados aparecerão aqui após a integração com a bridge.')
