#!/usr/bin/env python3
import os, sys, json, requests, urllib.parse, secrets, hashlib, base64, http.server, threading, time

BASE_DIR = '/home/adminbot/Proyecto EVA/empresas/serpentarius/tiktok'
CONFIG_PATH = f'{BASE_DIR}/config.json'
TOKEN_PATH = f'{BASE_DIR}/user_token.json'

SCOPES = ['user.info.basic', 'video.upload', 'video.publish', 'video.list', 'comment.list', 'comment.publish']
auth_code = None

def log(msg):
    print(f'[TikTok] {msg}')

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def save_token(data):
    with open(TOKEN_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    log(f'Token guardado en {TOKEN_PATH}')

def save_state(state, verifier):
    p = '/home/adminbot/Proyecto EVA/eva/state/tiktok_user_token.json'
    with open(p, 'w') as f:
        json.dump({'oauth_state': state, 'code_verifier': verifier}, f, indent=2)

def load_state():
    p = '/home/adminbot/Proyecto EVA/eva/state/tiktok_user_token.json'
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return {}

def pkce_verifier():
    return base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode()

def pkce_challenge(verifier):
    return base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()

class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        if 'code' in qs:
            auth_code = qs['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'<html><body style="font-family:sans-serif;text-align:center;padding:80px"><h2>OK</h2><p>Ya puedes cerrar.</p></body></html>')
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'waiting')
        threading.Thread(target=self.server.shutdown).start()
    def log_message(self, format, *args):
        pass

def start_callback_server(port):
    server = http.server.HTTPServer(('0.0.0.0', port), CallbackHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    log(f'Callback server on port {port}')
    return server

def exchange_code(code, redirect_uri):
    config = load_config()
    ck = config['api']['client_key']
    cs = config['api']['client_secret']
    state_data = load_state()
    verifier = state_data.get('code_verifier', '')
    r = requests.post('https://open-api.tiktok.com/v2/oauth/token/', json={
        'client_key': ck, 'client_secret': cs, 'code': code,
        'grant_type': 'authorization_code', 'redirect_uri': redirect_uri,
        'code_verifier': verifier,
    }, timeout=15)
    if r.status_code == 200:
        data = r.json()
        d = data.get('data', data)
        if d.get('access_token'):
            save_token(d)
            log('Token obtenido!')
            return d
        log(f'Exchange error: {json.dumps(data)}')
    else:
        log(f'HTTP {r.status_code}: {r.text[:300]}')
    return None

def test_token(token):
    r = requests.get('https://open-api.tiktok.com/v2/user/info/', headers={'Authorization': f'Bearer {token}'}, timeout=10)
    if r.status_code == 200:
        data = r.json()
        d = data.get('data', data)
        u = d.get('display_name') or d.get('user', {}).get('display_name', 'unknown')
        log(f'Token valido — user: {u}')
        return True
    log(f'Test: {r.status_code} {r.text[:150]}')
    return False

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('redirect_uri', nargs='?', help='Redirect URI (ej: https://xxx.lhr.life/callback)')
    args = parser.parse_args()

    if not args.redirect_uri:
        print("Modo manual — pega el codigo que aparece en la URL despues de autorizar")
        print("1. Abre el Developer Portal de TikTok")
        print("2. Agrega: http://localhost:8765/callback  (NO localhost? usa https://xxx.lhr.life/callback)")
        ru = input("Redirect URI: ").strip()
        if not ru:
            print("No ingresaste URI")
            sys.exit(1)
        args.redirect_uri = ru

    redirect_uri = args.redirect_uri
    log(f'Redirect URI: {redirect_uri}')

    config = load_config()
    ck = config['api']['client_key']
    state = secrets.token_hex(16)
    verifier = pkce_verifier()
    challenge = pkce_challenge(verifier)
    save_state(state, verifier)

    server = start_callback_server(8765)

    params = urllib.parse.urlencode({
        'client_key': ck, 'response_type': 'code',
        'scope': ','.join(SCOPES), 'redirect_uri': redirect_uri,
        'state': state, 'code_challenge': challenge,
        'code_challenge_method': 'S256',
    })
    url = f'https://www.tiktok.com/v2/auth/authorize/?{params}'

    print(f'\n{"="*55}')
    print(f'1. Si no lo has hecho, agrega en TikTok Developer Portal:')
    print(f'   {redirect_uri}')
    print(f'2. Abre esta URL en tu navegador:')
    print(f'\n{url}\n')
    print(f'3. Autoriza los permisos')
    print(f'4. TikTok redirige al callback — esperando...')
    print(f'{"="*55}\n')

    for _ in range(600):
        if auth_code:
            break
        time.sleep(1)

    if auth_code:
        log('Codigo recibido!')
        result = exchange_code(auth_code, redirect_uri)
        if result:
            print(f'\n Token obtenido!')
            test_token(result.get('access_token'))
    else:
        log('Timeout — no se recibio callback')

if __name__ == '__main__':
    main()
