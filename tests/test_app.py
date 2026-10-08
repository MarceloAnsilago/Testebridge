"""Teste de interface com respostas sintéticas; não são resultados de trading."""
from pathlib import Path
import unittest
from unittest.mock import patch
from streamlit.testing.v1 import AppTest

class AppTests(unittest.TestCase):
    def test_connection_gates_optimization(self):
        app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run()
        self.assertFalse(app.exception)
        self.assertTrue(next(b for b in app.button if b.label=='OTIMIZAR NO MT5').disabled)
        next(f for f in app.text_input if f.label=='URL da bridge').set_value('https://test-only.trycloudflare.com')
        next(f for f in app.text_input if f.label=='Chave de acesso').set_value('test-only-token')
        with patch('bridge_client.call',return_value={'service':'mt5-optimization-bridge','version':1,'ready':True,'message':'Teste de interface'}):
            next(b for b in app.button if b.label=='Conectar').click().run()
        self.assertFalse(app.exception)
        self.assertFalse(next(b for b in app.button if b.label=='OTIMIZAR NO MT5').disabled)
        next(b for b in app.button if b.label=='Desconectar').click().run()
        self.assertFalse(app.exception)
        self.assertTrue(next(b for b in app.button if b.label=='OTIMIZAR NO MT5').disabled)

if __name__=='__main__': unittest.main()
