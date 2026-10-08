"""Cliente HTTPS; nunca executa programas ou acessa arquivos do MT5."""
import re
import requests

class BridgeError(Exception):
    pass

def validated_url(url):
    url = url.strip().rstrip('/')
    if not re.fullmatch(r'https://[a-z0-9]+(?:-[a-z0-9]+)*\.trycloudflare\.com', url):
        raise BridgeError('Informe a URL HTTPS do túnel, terminada em .trycloudflare.com.')
    return url

def call(url, token, path, payload=None):
    base = validated_url(url)
    try:
        response = requests.request('POST' if payload is not None else 'GET', base+path,
                                    headers={'Authorization':'Bearer '+token}, json=payload,
                                    timeout=(5,20), allow_redirects=False)
    except requests.RequestException:
        raise BridgeError('Não foi possível alcançar o PC. Confira se a API e o túnel estão ligados.') from None
    if response.status_code == 401:
        raise BridgeError('Chave de acesso inválida.')
    if response.status_code in (404,409,422):
        try:
            detail = response.json().get('detail')
        except ValueError:
            detail = None
        raise BridgeError(detail if isinstance(detail,str) else 'Solicitação inválida ou resultado indisponível.')
    if response.status_code not in (200,202):
        raise BridgeError(f'A bridge respondeu com erro HTTP {response.status_code}.')
    if path.endswith('/csv'):
        return response.content
    try:
        return response.json()
    except ValueError:
        raise BridgeError('Resposta incompatível com a bridge.') from None
