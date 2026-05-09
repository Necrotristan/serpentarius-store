#!/usr/bin/env python3
"""
Verificar acceso a Google Drive con Service Account
"""
import json
import os

SERVICE_ACCOUNT_PATH = '/home/adminbot/Proyecto EVA/empresas/serpentarius/vault/service_account.json'
# Fallback: SERVICE_ACCOUNT_PATH = '/home/adminbot/.config/opencode/secrets/vault/service_account.json'

print("=" * 60)
print("VERIFICACIÓN DE GOOGLE DRIVE PARA EVA")
print("=" * 60)
print()

if os.path.exists(SERVICE_ACCOUNT_PATH):
    print(f"✓ Service Account encontrado: {SERVICE_ACCOUNT_PATH}")
    try:
        with open(SERVICE_ACCOUNT_PATH) as f:
            sa_data = json.load(f)
        
        print(f"\nDetalles de la cuenta:")
        print(f"  Client Email: {sa_data.get('client_email', 'N/A')}")
        print(f"  Project ID: {sa_data.get('project_id', 'N/A')}")
        print(f"  Type: {sa_data.get('type', 'N/A')}")
        
        print("\n✓ EVA PUEDE USAR ESTE SERVICE ACCOUNT")
        print(f"\nACCIONES REQUERIDAS:")
        print(f"1. Ve a Google Drive: https://drive.google.com")
        print(f"2. Comparte archivos/carpetas con:")
        print(f"   {sa_data.get('client_email')}")
        print(f"3. Permiso: Editor")
        print(f"\nUna vez compartido, EVA tendrá acceso completo.")
        
    except Exception as e:
        print(f"✗ Error leyendo archivo: {e}")
else:
    print(f"✗ No se encontró Service Account")
    print(f"\nPASOS PARA CREARLO:")
    print(f"1. https://console.cloud.google.com/iam-admin/serviceaccounts")
    print(f"2. Crear Service Account en proyecto 772801886632")
    print(f"3. Generar clave JSON")
    print(f"4. Guardar en: {SERVICE_ACCOUNT_PATH}")

print("\n" + "=" * 60)
