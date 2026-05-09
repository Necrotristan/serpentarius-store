#!/usr/bin/env python3
"""
OAuth manual que funciona - copia el código de la URL
"""
import json
from google.oauth2 import credentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests

def main():
    creds_file = '/home/adminbot/.config/opencode/secrets/vault/credentials.json'
    token_file = '/home/adminbot/.config/opencode/secrets/vault/token.json'
    
    with open(creds_file, 'r') as f:
        creds_data = json.load(f)
    
    client_id = creds_data['google_oauth']['client_id']
    client_secret = creds_data['google_oauth']['client_secret']
    
    # URL de autorización manual
    scope = "https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/gmail.modify https://www.googleapis.com/auth/drive"
    
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&scope={scope.replace(' ', '%20')}&access_type=offline&prompt=consent"
    
    print("=" * 70)
    print("COPIA Y PEGA ESTA URL EN TU NAVEGADOR:")
    print("=" * 70)
    print()
    print(auth_url)
    print()
    print("=" * 70)
    print("INSTRUCCIONES:")
    print("1. Acepta los permisos en Google")
    print("2. Te redirigirá a una página de error (es normal)")
    print("3. Copia el CÓDIGO de la URL (lo que sigue a 'code=')")
    print("4. Pégalo aquí cuando te lo pida EVA")
    print("=" * 70)

if __name__ == '__main__':
    main()
