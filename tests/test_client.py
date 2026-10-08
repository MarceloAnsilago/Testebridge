import unittest
from unittest.mock import patch, Mock
from bridge_client import call, validated_url, BridgeError

class ClientTests(unittest.TestCase):
    def test_url_restrictions(self):
        self.assertEqual(validated_url('https://example-test.trycloudflare.com/'),'https://example-test.trycloudflare.com')
        for url in ('http://localhost:8765','https://127.0.0.1','https://evil.example','https://x.trycloudflare.com@evil.example','https://x.trycloudflare.com/path'):
            with self.assertRaises(BridgeError): validated_url(url)

    def test_redirect_and_auth_handling(self):
        with patch('bridge_client.requests.request') as request:
            request.return_value=Mock(status_code=302)
            with self.assertRaises(BridgeError): call('https://test.trycloudflare.com','test','/v1/health')
            self.assertFalse(request.call_args.kwargs['allow_redirects'])
            request.return_value=Mock(status_code=401)
            with self.assertRaisesRegex(BridgeError,'Chave'): call('https://test.trycloudflare.com','test','/v1/health')

if __name__=='__main__': unittest.main()
