#!/usr/bin/env python3
"""
Script para obtener token de Google Drive sin problemas de URI
"""
import urllib.parse
import urllib.request
import json

# Credenciales desde vault de serpentarius
import json, os
VAULT_PATH = "/home/adminbot/Proyecto EVA/empresas/serpentarius/vault/credentials.json"
try:
    with open(VAULT_PATH) as f:
        vault = json.load(f)
    CLIENT_ID = vault.get('google', {}).get('client_id', '')
    CLIENT_SECRET = vault.get('google', {}).get('client_secret', '')
except:
    CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')
    CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '')

def generar_url():
    redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
    scope = "https://www.googleapis.com/auth/drive"
    url = (f"https://accounts.google.com/o/oauth2/v2/auth?"
           f"client_id={CLIENT_ID}&"
           f"redirect_uri={urllib.parse.quote(redirect_uri)}&"
           f"response_type=code&"
           f"scope={urllib.parse.quote(scope)}&"
           f"access_type=offline&"
           f"prompt=consent")
    return url

def intercambiar_codigo(code):
    token_url = "https://oauth2.googleapis.com/token"
    data = urllib.parse.urlencode({
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
        'grant_type': 'authorization_code'
    }).encode()
    
    req = urllib.request.Request(token_url, data=data)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

print("=" * 60)
print("OBTENER TOKEN DE GOOGLE DRIVE (MÉTODO OOB)")
print("=" * 60)
print()
print("PASO 1: Abre esta URL en tu navegador:")
print()
url = generar_url()
print(url)
print()
print("PASO 2: Autoriza con la cuenta: Serpentariusrockstore@gmail.com")
print()
print("PASO 3: Google mostrará un código en pantalla.")
print("         Cópialo y pégalo aquí cuando te lo pida.")
print()
print("=" * 60)
print()
code = input("Pega el código aquí: ").strip()

if code:
    print("\nObteniendo tokens...")
    try:
        tokens = intercambiar_codigo(code)
        print("\n✓ TOKENS OBTENIDOS EXITOSAMENTE")
        print(f"Access Token: {tokens.get('access_token', 'N/A')[:40]}...")
        print(f"Refresh Token: {'SÍ' if 'refresh_token' in tokens else 'NO'}")
        
        # Guardar tokens
        token_file = '/home/adminbot/Proyecto EVA/empresas/serpentarius/vault/google_tokens.json'
        with open(token_file, 'w') as f:
            json.dump(tokens, f, indent=2)
        print(f"\n✓ Tokens guardados en: {token_file}")
        print("\nEVA AHORA TIENE ACCESO COMPLETO A GOOGLE DRIVE")
    except Exception as e:
        print(f"\n✗ Error: {e}")
else:
    print("No se ingresó ningún código")
