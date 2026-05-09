# Google Drive Integration Setup - SerpentariuStore

## Pasos para configurar acceso gratuito

### Opción 1: API Key (Simpler, solo lectura básica)
1. Ir a https://console.cloud.google.com/apis/credentials
2. Crear proyecto (sin habilitar facturación)
3. Habilitar "Google Drive API"
4. Crear "API Key"
5. Configurar restricciones de API (opcional pero recomendado)

### Opción 2: OAuth 2.0 (Acceso completo - RECOMENDADO)
1. Ir a https://console.cloud.google.com/apis/credentials
2. Crear proyecto "SerpentariuStore" (sin facturación)
3. Habilitar "Google Drive API"
4. Crear "OAuth client ID" (tipo: Desktop/Native app)
5. Descargar archivo JSON de credenciales

### Compartir carpetas con EVA
Una vez configurado, las carpetas que debes compartir:
- **Facturas**: ID de carpeta de Google Drive con facturas
- **Photos**: ID de carpeta de Google Drive con fotos de productos
- **Catalog**: ID de carpeta con catálogo

### Verificar cuotas gratuitas
- Google Drive API tiene límites generosos sin costo
- 1,000,000,000 cuota de unidades por día
- No requiere facturación para uso básico

### URLs útiles
- Console: https://console.cloud.google.com/apis/library/drive.googleapis.com
- Docs: https://developers.google.com/drive/api/v3/about-sdk
- Quotas: https://console.cloud.google.com/apis/api/drive.googleapis.com/quotas

## Estado actual
- [x] Estructura local creada
- [x] Agentes asignados
- [ ] Google Cloud project creado
- [ ] Google Drive API habilitada
- [ ] Credenciales configuradas
- [ ] Carpetas compartidas
