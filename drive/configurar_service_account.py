#!/usr/bin/env python3
"""
Configurar Google Drive con Service Account
"""
import json
import os

SERVICE_ACCOUNT_PATH = '/home/adminbot/Proyecto EVA/empresas/serpentarius/vault/service_account.json'
# Fallback: SERVICE_ACCOUNT_PATH = '/home/adminbot/.config/opencode/secrets/vault/service_account.json'

print("=" * 60)
print("CONFIGURACIÓN DE SERVICE ACCOUNT PARA EVA")
print("=" * 60)
print()

if os.path.exists(SERVICE_ACCOUNT_PATH):
    print(f"✓ Service Account encontrado: {SERVICE_ACCOUNT_PATH}")
    with open(SERVICE_ACCOUNT_PATH) as f:
        sa_data = json.load(f)
    
    print(f"\nDetalles:")
    print(f"  Client Email: {sa_data.get('client_email', 'N/A')}")
    print(f"  Project ID: {sa_data.get('project_id', 'N/A')}")
    print(f"  Type: {sa_data.get('type', 'N/A')}")
    
    print("\n✓ EVA AHORA PUEDE USAR ESTE SERVICE ACCOUNT")
    print("\nAsegúrate de:")
    print(f"1. Compartir tus archivos de Drive con: {sa_data.get('client_email')}")
    print("2. Dar permisos de 'Editor' al menos")
else:
    print(f"✗ No se encontró Service Account en: {SERVICE_ACCOUNT_PATH}")
    print("\nPASOS PARA CREARLO:")
    print("1. Ve a: https://console.cloud.google.com/iam-admin/serviceaccounts")
    print("2. Crea una Service Account")
    print("3. Genera una clave JSON")
    print(f"4. Sube el archivo a: {SERVICE_ACCOUNT_PATH}")

print("\n" + "=" * 60)
