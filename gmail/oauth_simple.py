#!/usr/bin/env python3
"""
Script simplificado para OAuth - usa redirect de n8n
"""
import json
from google_auth_oauthlib.flow import Flow

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/drive',
]

def main():
    creds_file = '/home/adminbot/.config/opencode/secrets/vault/credentials.json'
    
    with open(creds_file, 'r') as f:
        creds_data = json.load(f)
    
    # Usar el redirect de n8n que ya tienes configurado
    redirect_uri = "http://172.17.0.1:5678/rest/oauth2-credential/callback"
    
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": creds_data['google_oauth']['client_id'],
                "client_secret": creds_data['google_oauth']['client_secret'],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [redirect_uri]
            }
        },
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    
    auth_url, _ = flow.authorization_url(
        access_type='offline',
        prompt='consent'
    )
    
    print("=" * 70)
    print("COPIA Y PEGA ESTA URL EN TU NAVEGADOR:")
    print("=" * 70)
    print()
    print(auth_url)
    print()
    print("=" * 70)
    print("Luego avísame para el siguiente paso")

if __name__ == '__main__':
    main()
