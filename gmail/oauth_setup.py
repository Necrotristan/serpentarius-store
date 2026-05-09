#!/usr/bin/env python3
"""
Script para generar token.json usando OAuth2 (Google Gmail y Drive)
"""
import json
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
]

def main():
    # Intentar vault central primero, luego vault de serpentarius
    vault_paths = [
        '/home/adminbot/Proyecto EVA/empresas/serpentarius/vault/credentials.json',
        '/home/adminbot/.config/opencode/secrets/vault/credentials.json'
    ]
    creds_file = next((p for p in vault_paths if os.path.exists(p)), vault_paths[0])
    token_file = '/home/adminbot/Proyecto EVA/empresas/serpentarius/vault/token.json'
    
    # Cargar credenciales
    with open(creds_file, 'r') as f:
        creds_data = json.load(f)
    
    # Extraer client_id y client_secret de donde sea que estén
    if 'google' in creds_data:
        google = creds_data['google']
    elif 'empresas' in creds_data and 'serpentarius' in creds_data['empresas']:
        google = creds_data['empresas']['serpentarius']
    else:
        google = creds_data.get('google_oauth', {})
    
    oauth_config = {
        "installed": {
            "client_id": google.get('client_id', ''),
            "client_secret": google.get('client_secret', ''),
            "redirect_uris": ["http://localhost:8080/"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }
    
    flow = InstalledAppFlow.from_client_config(oauth_config, SCOPES)
    
    # Usar puerto 8080 como está en la configuración
    flow.run_local_server(port=8080)
    
    creds = flow.credentials
    
    # Guardar token
    with open(token_file, 'w') as f:
        f.write(creds.to_json())
    
    print(f"Token guardado en {token_file}")
    print("Listo para usar Gmail y Drive!")

if __name__ == '__main__':
    main()
