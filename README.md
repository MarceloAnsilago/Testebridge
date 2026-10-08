# Testebridge

Interface Streamlit Cloud para otimizações no MT5 instalado no Windows.

## Conectar

1. No PC Windows, execute o iniciador `iniciar_conexao.ps1` da bridge local.
2. Na barra lateral do aplicativo, informe a URL HTTPS `*.trycloudflare.com` exibida pelo iniciador e sua chave privada.
3. Clique **Conectar**, feche os terminais MT5 e envie os parâmetros em **OTIMIZAR NO MT5**.
4. Acompanhe o trabalho; os resultados nativos confirmados ficam disponíveis para download CSV.

A chave é informada por sessão, em campo de senha, e não fica no repositório. Sem uma chave válida, visitantes não conseguem iniciar trabalhos nem consultar resultados. Não informe senhas da corretora neste aplicativo.

Este repositório continua contendo somente a interface e seu cliente HTTPS. O EA, a API, o executável do túnel, as chaves e os logs ficam no Windows. A API suporta exclusivamente o EA fixo da POC; não recebe caminhos de executáveis nem comandos arbitrários.

## Executar localmente

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Streamlit Community Cloud

Repositório: `MarceloAnsilago/Testebridge`; branch: `main`; entrada: `app.py`; Python 3.11. Esta versão não precisa de Secrets no Cloud: URL e chave são fornecidas pelo operador em sua sessão. A conexão HTTPS leva a chave ao servidor do aplicativo e à bridge; ela não é exibida para outros visitantes.

O túnel temporário muda de endereço quando reinicia. O PC deve permanecer ligado. A bridge executa um trabalho por vez, preserva o MT5 em timeout e conserva até cem trabalhos em memória. Reiniciar o serviço perde o acompanhamento na API, mas preserva os relatórios locais. Não reenvie trabalhos automaticamente depois de reiniciar a API: confira primeiro o MT5 e os relatórios.

## Contrato da API

Todas as rotas usam `Authorization: Bearer <chave>`:

- `GET /v1/health`: conexão e disponibilidade.
- `POST /v1/jobs`: parâmetros e `request_id` UUID, com reenvio idempotente na sessão do serviço.
- `GET /v1/jobs/{id}`: estado, erro ou resultados normalizados e originais.
- `GET /v1/jobs/{id}/csv`: CSV somente após conclusão validada.

A interface atual aceita apenas URLs HTTPS do Quick Tunnel da Cloudflare. Não segue redirects nem permite endereços de rede local fornecidos pelo visitante.

## Testes

```powershell
python -m unittest discover -s tests -v
```
