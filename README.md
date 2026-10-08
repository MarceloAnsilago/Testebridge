# Testebridge

Interface Streamlit para configurar otimizações do MetaTrader 5, preparada para publicação no Streamlit Community Cloud.

## Estado atual

O formulário permite ajustar símbolo, período, datas, depósito e intervalo da média móvel. O botão **OTIMIZAR NO MT5** permanece desabilitado enquanto a bridge local não estiver conectada. Não há resultados simulados ou execução de ordens nesta versão.

Este repositório contém somente a interface. O terminal MT5 e a bridge Python continuarão no computador Windows. A comunicação autenticada entre a interface e a bridge será implementada posteriormente.

## Executar localmente

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Publicar no Streamlit Community Cloud

Selecione o repositório `MarceloAnsilago/Testebridge`, a branch `main` e o arquivo de entrada `app.py`. Use Python 3.11 para reproduzir o ambiente de validação local.

Esta versão não exige credenciais ou secrets. O deploy no Cloud será feito em uma etapa posterior.
