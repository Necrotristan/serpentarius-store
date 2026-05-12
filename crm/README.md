# CRM SerpentariuStore

## Despliegue Rápido

### 1. Base de Datos

```bash
# Ejecutar schema en Supabase PostgreSQL
docker exec -i n8n-claw-db psql -U postgres -d n8n_claw < /path/to/schema.sql
```

O desde n8n-claw:
```bash
cd ~/Proyecto\ EVA/Projects/n8n-claw
docker compose exec -T db psql -U postgres -d n8n_claw < ~/Proyecto\ EVA/empresas/serpentarius/crm/schema.sql
```

### 2. n8n Workflows (Importar)

Los workflows se importan desde la UI de n8n en `http://localhost:5678`:
- Workflow → Import from JSON

Workflows disponibles en `crm/workflows/`:
- `crm-lead-capture.json` - Captura de leads
- `crm-invoice-generator.json` - Generación de facturas  
- `crm-shipping-guide.json` - Guías de envío
- `crm-nurturing.json` - Secuencias de nurturing

### 3. Verificar Conexiones

```bash
# Verificar Supabase
curl http://localhost:3000/contacts

# Verificar n8n health
curl http://localhost:5678/healthz

# Verificar Drive API
# (ya configurado en google_drive_config.json)
```

### 4. Dashboard

Extender el dashboard Flask existente en `http://localhost:5051` con las vistas CRM.
