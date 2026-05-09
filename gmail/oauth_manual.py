#!/usr/bin/env python3
"""
Script para generar URL de OAuth y pedir el código manualmente
"""
import json
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
]

def main():
    creds_file = '/home/adminbot/.config/opencode/secrets/vault/credentials.json'
    token_file = '/home/adminbot/.config/opencode/secrets/vault/token.json'
    
    with open(creds_file, 'r') as f:
        creds_data = json.load(f)
    
    oauth_config = {
        "installed": {
            "client_id": creds_data['google_oauth']['client_id'],
            "client_secret": creds_data['google_oauth']['client_secret'],
            "redirect_uris": ["http://localhost:8080/oauth/callback"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }
    
    flow = InstalledAppFlow.from_client_config(oauth_config, SCOPES)
    
    # Generar URL de autorización
    auth_url, _ = flow.authorization_url(prompt='consent')
    
    print("=" * 60)
    print("PASOS PARA AUTORIZAR:")
    print("1. Copia y pega esta URL en tu navegador:")
    print()
    print(auth_url)
    print()
    print("2. Acepta los permisos con tu cuenta Google")
    print("3. Te redirigirá a localhost (dará error en el navegador)")
    print("4. Copia el CÓDIGO de la URL del navegador")
    print("   (Lo que está después de 'code=')")
    print("=" * 60)
    
    auth_code = input("\nPega aquí el código de autorización: ").strip()
    
    flow.fetch_token(code=auth_code)
    creds = flow.credentials
    
    with open(token_file, 'w') as f:
        f.write(creds.to_json())
    
    print(f"\n✓ Token guardado en {token_file}")
    print("✓ Ya puedes usar Gmail y Drive!")

if __name__ == '__main__':
    main()
