# CRM PROFESIONAL - SERPENTARIUSTORE

## Modelo de Ventas Integral omnicanal

```
Arquitecto: EVA (COO)
Empresa: SerpentariuStore (Ropa)
Stack base: n8n + Supabase + PostgreSQL + AI Agents + Telegram + WhatsApp + Drive + Gmail
```

---

## 1. ARQUITECTURA GENERAL

```
┌──────────────────────────────────────────────────────────────────────┐
│                     INTERFACE LAYER (Canales de entrada)             │
├────────────┬───────────┬──────────┬─────────┬──────────┬────────────┤
│  Telegram  │ WhatsApp  │ Facebook │ Instagram│ TikTok   │   Shopee  │
│  (Bot EVA) │  (Ventas) │  (Ads)   │ (Shop)   │ (Viral)  │ (Market)  │
└─────┬──────┴─────┬─────┴────┬────┴────┬────┴─────┬────┴─────┬──────┘
      │            │          │         │          │          │
      ▼            ▼          ▼         ▼          ▼          ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    INTEGRATION LAYER (n8n Workflows)                 │
│  Webhooks  │  API Bridge  │  Message Router  │  File Handler        │
│  Lead Capture │ Auto-responder │ Invoice Gen │ Notification Engine  │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      AI AGENT LAYER                                  │
├──────────────┬───────────────┬──────────────┬───────────────────────┤
│ Sales Agent  │  CRM Speclst  │ Marketing Ag │  Support Agent        │
│ (up-sell,    │  (Nathan Park)│ (campañas,   │  (post-venta,        │
│  recovery)   │  segmentación │  leads)       │   tickets)            │
├──────────────┼───────────────┼──────────────┼───────────────────────┤
│ Catalog Ag   │ Inventory Ag  │ Gmail Agent  │  Instagram/TikTok Ag  │
│ (productos)  │ (stock)       │ (correos)    │  (social content)     │
└──────────────┴───────────────┴──────────────┴───────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                                    │
├──────────────────────────┬───────────────────────────────────────────┤
│   Supabase (PostgreSQL)  │     Google Drive (Almacenamiento)         │
│   - Contacts             │     - facturas/ (PDF)                     │
│   - Deals                │     - guias/ (PDF)                        │
│   - Orders               │     - catalog/ (JSON/CSV)                 │
│   - Products             │     - photos/ (JPEG/PNG)                  │
│   - Interactions         │     - backups/                            │
│   - Campaigns            │                                           │
│   - Analytics            │                                           │
└──────────────────────────┴───────────────────────────────────────────┘
```

---

## 2. PIPELINE DE VENTAS (Lead-to-Cash)

```
┌─────────┐   ┌──────────┐   ┌───────────┐   ┌──────────┐   ┌──────────┐   ┌───────────┐
│ LEAD    │──▶│ CONTACT │──▶│ QUALIFY  │──▶│ PROPOSAL│──▶│ NEGOTIATE│──▶│ CLOSED   │
│ (Raw)   │   │ (Contact)│   │ (Calif.) │   │ (Oferta) │   │ (Negoc.) │   │ (Cerrado) │
└─────────┘   └──────────┘   └───────────┘   └──────────┘   └──────────┘   └─────┬─────┘
      │                                                                           │
      ▼                                                                           ▼
┌──────────────┐                                                         ┌────────────────┐
│ Origen:      │                                                         │ WON → Invoice  │
│ - WhatsApp   │                                                         │ LOST → Nurture │
│ - Instagram  │                                                         │                │
│ - Facebook   │                                                         │                │
│ - TikTok     │                                                         │                │
│ - Shopee     │                                                         │                │
│ - Web        │                                                         │                │
│ - Referido   │                                                         │                │
└──────────────┘                                                         └────────────────┘
```

### 2.1 Etapas del Pipeline

| Etapa | Acción | Automatización | Tiempo Máx |
|-------|--------|----------------|------------|
| **Lead** | Captura automática desde canal | n8n detecta → crea contacto en Supabase | Instantáneo |
| **Contactado** | Bot envía primer mensaje (WhatsApp/Telegram) | n8n → AI Agent redacta → envía | < 5 min |
| **Calificado** | Agente CRM evalúa: interés + presupuesto + timing | Nathan Park agent clasifica (hot/warm/cold) | < 24 hrs |
| **Oferta** | Catálogo + precio + promoción personalizada | Sales Agent prepara propuesta | < 48 hrs |
| **Negociación** | Contra-ofertas, descuentos, envío | Bot negocia dentro de reglas | < 72 hrs |
| **Cerrado Ganado** | Factura → Drive → WhatsApp → Pago | Invoice Agent genera todo | < 1 hr post-acuerdo |
| **Cerrado Perdido** | Lead guardado para nurturing | Marketing Agent → secuencia email/WhatsApp | Automático |

---

## 3. MODELO DE DATOS (Supabase/PostgreSQL)

### 3.1 Entidades Principales

```sql
-- =====================================================
-- CORAZÓN DEL CRM: Contactos (Clientes + Leads)
-- =====================================================
CREATE TABLE contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    -- Canales
    whatsapp_phone TEXT UNIQUE,
    telegram_id TEXT UNIQUE,
    instagram_handle TEXT,
    facebook_id TEXT,
    tiktok_handle TEXT,
    shopee_id TEXT,
    -- Segmentación
    tags TEXT[],            -- {'vip', 'nuevo', 'mayorista', 'recurrente'}
    source TEXT,             -- 'whatsapp','instagram','facebook','tiktok','shopee','referido','web'
    status TEXT DEFAULT 'lead', -- 'lead','contacted','qualified','customer','inactive','lost'
    lifetime_value DECIMAL(12,2) DEFAULT 0,
    total_orders INT DEFAULT 0,
    last_purchase_date TIMESTAMPTZ,
    notes TEXT,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- PIPELINE DE VENTAS (Oportunidades)
-- =====================================================
CREATE TABLE deals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
    title TEXT NOT NULL,            -- 'Camiseta colección verano x2'
    stage TEXT NOT NULL DEFAULT 'lead',  -- pipeline stage
    value DECIMAL(12,2) DEFAULT 0,       -- valor estimado
    probability INT DEFAULT 10,          -- 10-100%
    source TEXT,                          -- canal de origen
    assigned_agent TEXT,                  -- qué agente AI maneja
    expected_close_date DATE,
    closed_date TIMESTAMPTZ,
    outcome TEXT,                         -- 'won','lost'
    lost_reason TEXT,
    products JSONB[],                    -- [{sku, name, qty, price}]
    activities JSONB[],                  -- [{type, date, note, agent}]
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- ÓRDENES (Ventas Completadas)
-- =====================================================
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deal_id UUID REFERENCES deals(id),
    contact_id UUID REFERENCES contacts(id) NOT NULL,
    order_number TEXT UNIQUE NOT NULL,     -- FACT-2026-00001
    status TEXT DEFAULT 'pending',         -- 'pending','paid','shipped','delivered','cancelled','refunded'
    subtotal DECIMAL(12,2),
    discount DECIMAL(12,2) DEFAULT 0,
    shipping_cost DECIMAL(12,2) DEFAULT 0,
    total DECIMAL(12,2),
    payment_method TEXT,                    -- 'nequi','bancolombia','efectivo','shopee_pay'
    payment_status TEXT DEFAULT 'pending',  -- 'pending','confirmed','failed'
    shipping_address TEXT,
    shipping_city TEXT,
    shipping_guide TEXT,                   -- número guía
    shipping_carrier TEXT,                 -- 'servientrega','interrapidisimo','envia'
    invoice_drive_id TEXT,                 -- ID archivo en Google Drive
    guide_drive_id TEXT,                   -- ID guía en Google Drive
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- ITEMS DE ÓRDENES
-- =====================================================
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    product_sku TEXT NOT NULL,
    product_name TEXT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(12,2) NOT NULL,
    total_price DECIMAL(12,2) NOT NULL,
    size TEXT,        -- 'S','M','L','XL'
    color TEXT,
    metadata JSONB
);

-- =====================================================
-- PRODUCTOS (Catálogo)
-- =====================================================
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    category TEXT,              -- 'camisetas','pantalones','accesorios','chaquetas'
    subcategory TEXT,
    price DECIMAL(12,2) NOT NULL,
    cost_price DECIMAL(12,2),
    sizes TEXT[],               -- {'S','M','L','XL','XXL'}
    colors TEXT[],
    stock INT DEFAULT 0,
    min_stock INT DEFAULT 5,    -- alerta cuando baja de aquí
    images TEXT[],              -- URLs / Drive IDs
    tags TEXT[],                -- {'verano','nuevo','descuento','top'}
    is_active BOOLEAN DEFAULT true,
    shopee_id TEXT,             -- ID en Shopee
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- INTERACCIONES (Historial completo de comunicación)
-- =====================================================
CREATE TABLE interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
    deal_id UUID REFERENCES deals(id),
    channel TEXT NOT NULL,       -- 'whatsapp','telegram','email','instagram','facebook','tiktok','shopee'
    direction TEXT NOT NULL,     -- 'inbound','outbound'
    type TEXT NOT NULL,          -- 'message','call','email','comment','dm','order_note'
    content TEXT,
    media_urls TEXT[],           -- URLs a Drive o CDN
    ai_agent TEXT,               -- qué agente manejó
    sentiment TEXT,              -- 'positive','neutral','negative'
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- CAMPAÑAS DE MARKETING
-- =====================================================
CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    type TEXT NOT NULL,          -- 'email','whatsapp','instagram_ads','facebook_ads','tiktok'
    status TEXT DEFAULT 'draft', -- 'draft','active','paused','completed'
    audience_segment TEXT[],     -- tags o filtros
    content JSONB,               -- mensajes, imágenes, CTAs
    schedule TIMESTAMPTZ,
    budget DECIMAL(12,2),
    spent DECIMAL(12,2) DEFAULT 0,
    leads_generated INT DEFAULT 0,
    deals_closed INT DEFAULT 0,
    revenue_generated DECIMAL(12,2) DEFAULT 0,
    rois DECIMAL(5,2),           -- retorno de inversión
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- LEAD SCORING (Puntuación de leads)
-- =====================================================
CREATE TABLE lead_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_id UUID REFERENCES contacts(id) UNIQUE,
    score INT DEFAULT 0,         -- 0-100
    -- Factores de scoring
    recency_days INT,            -- días desde última interacción
    frequency_30d INT,           -- interacciones últimos 30 días
    monetary DECIMAL(12,2),      -- gasto total
    page_visits INT,             -- visitas a catálogo/web
    cart_abandoned INT,          -- carritos abandonados
    social_engagement INT,       -- likes/compartidos
    -- Cálculos
    tier TEXT,                   -- 'hot','warm','cold','dead'
    last_calculated TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- FACTURAS Y GUÍAS (Metadatos de archivos en Drive)
-- =====================================================
CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id),
    invoice_number TEXT UNIQUE NOT NULL,  -- FAC-2026-NNNNN
    drive_file_id TEXT NOT NULL,           -- ID en Google Drive
    drive_url TEXT,
    file_type TEXT DEFAULT 'pdf',
    total DECIMAL(12,2),
    tax DECIMAL(12,2),
    status TEXT DEFAULT 'issued',         -- 'issued','paid','cancelled'
    sent_whatsapp BOOLEAN DEFAULT false,
    sent_email BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE shipping_guides (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id),
    guide_number TEXT NOT NULL,            -- número de guía real
    carrier TEXT NOT NULL,                 -- transportadora
    drive_file_id TEXT,                    -- PDF de guía en Drive
    drive_url TEXT,
    status TEXT DEFAULT 'pending',         -- 'pending','in_transit','delivered','failed'
    tracking_url TEXT,
    sent_whatsapp BOOLEAN DEFAULT false,
    estimated_delivery DATE,
    delivered_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- AUTO-RESPONSE RULES (Reglas de negocio para bots)
-- =====================================================
CREATE TABLE auto_response_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trigger_type TEXT NOT NULL,     -- 'keyword','stage_change','payment','lead_source'
    trigger_value TEXT NOT NULL,    -- 'gracias','pago_confirmado','instagram_lead'
    action_type TEXT NOT NULL,      -- 'send_whatsapp','send_email','assign_agent','create_deal'
    action_config JSONB,           -- configuración de la acción
    is_active BOOLEAN DEFAULT true,
    priority INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- ÍNDICES
-- =====================================================
CREATE INDEX idx_contacts_phone ON contacts(phone);
CREATE INDEX idx_contacts_status ON contacts(status);
CREATE INDEX idx_contacts_source ON contacts(source);
CREATE INDEX idx_deals_stage ON deals(stage);
CREATE INDEX idx_deals_contact ON deals(contact_id);
CREATE INDEX idx_orders_contact ON orders(contact_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_interactions_contact ON interactions(contact_id);
CREATE INDEX idx_interactions_channel ON interactions(channel);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_lead_scores_score ON lead_scores(score DESC);
```

---

## 4. FLUJOS n8n (Automatización)

### 4.1 Captura de Leads

```
[Trigger: WhatsApp Webhook]
       │
       ▼
[Analizar mensaje: ¿es lead nuevo?]
       │
       ├── Sí ──▶ [Crear contacto en Supabase]
       │              │
       │              ▼
       │         [Buscar en Drive: ¿cliente existente?]
       │              │
       │              ▼
       │         [Asignar score inicial]
       │              │
       │              ▼
       │         [Sales Agent: primer mensaje personalizado]
       │              │
       │              ▼
       │         [Enviar WhatsApp: "Hola {nombre}, gracias por escribir"]
       │
       └── No ──▶ [Registrar interacción]
                      │
                      ▼
                  [Actualizar lead_score]
```

### 4.2 Generación de Factura + Drive

```
[Trigger: Deal → Closed Won]
       │
       ▼
[Sales Agent: confirmar detalles orden]
       │
       ▼
[Generar factura PDF con datos de orden]
       │
       ▼
[Subir a Drive → /facturas/{order_number}.pdf]
       │
       ▼
[Registrar en tabla invoices con drive_file_id]
       │
       ▼
[Enviar WhatsApp al cliente: "🧾 Tu factura"]
       │
       ▼
[Enviar por Gmail: copia factura]
       │
       ▼
[Actualizar order: invoice_drive_id, status=paid]
```

### 4.3 Guía de Envío + Tracking

```
[Trigger: Order → status=paid]
       │
       ▼
[Generar guía (según transportadora)]
       │
       ▼
[Subir PDF guía a Drive → /guias/{guide_number}.pdf]
       │
       ▼
[Registrar en shipping_guides]
       │
       ▼
[Enviar WhatsApp: "📦 Tu pedido va en camino"]
       │
       ▼
[Enviar tracking_url por WhatsApp]
       │
       ▼
[n8n espera webhook de entregado → actualizar status]
```

### 4.4 Nurturing Automático

```
[Trigger: Lead status=lost o lead >7 días sin actividad]
       │
       ▼
[Marketing Agent: seleccionar campaña]
       │
       ├── Email ──▶ [Gmail Agent: enviar promocional]
       │
       ├── WhatsApp ──▶ [WhatsApp Bot: "Oye {nombre}, tenemos nuevos"]
       │
       ├── Instagram ──▶ [Instagram Agent: DM / mention]
       │
       └── SMS ──▶ [Mensaje de texto]
              │
              ▼
        [Registrar en interactions]
              │
              ▼
        [Actualizar lead_score]
```

### 4.5 Social Media → Lead Pipeline

```
[Trigger: Instagram comment / Facebook lead ad / TikTok DM]
       │
       ▼
[Social Media Agent: clasificar mensaje]
       │
       ├── Interés compra ──▶ [Crear lead/contact] ──▶ [Assign to Sales]
       │
       ├── Pregunta ──▶ [Responder automático + ofrecer catálogo]
       │
       └── Spam ──▶ [Ignorar / marcar]
```

---

## 5. AGENTES AI ASIGNADOS AL CRM

| Agente | Rol | Función en CRM |
|--------|-----|----------------|
| **Sales Agent** | Vendedor principal | Califica leads, envía catálogos, negocia, cierra ventas |
| **Nathan Park (CRM Specialist)** | Estrategia CRM | Segmentación RFM, campañas email, dashboard métricas |
| **Marketing Agent** | Campañas | Crea secuencias email/WhatsApp, promo social |
| **Gmail Agent** | Correos | Envía facturas, promociones, seguimiento |
| **Instagram Agent** | Social commerce | Detecta leads en comments/DM, publica promos |
| **TikTok Agent** | Viral sales | Captura leads de tendencias/videos |
| **Catalog Agent** | Productos | Mantiene precios, stock, imágenes |
| **Inventory Agent** | Stock | Alertas de stock bajo, sugiere reposición |
| **Support Agent** | Post-venta | Resuelve dudas de envío, cambios, devoluciones |
| **Bot Manager** | Infraestructura | Mantiene canales activos (Telegram/WhatsApp) |

---

## 6. LEAD GENERATION ENGINE

### 6.1 Fuentes de Leads

```
WhatsApp Business
  ├── Número directo (publicado en redes)
  ├── Catálogo compartido por clientes
  └── Campañas broadcast

Instagram
  ├── Comentarios en publicaciones → Bot detecta interés
  ├── DM automáticos por stories
  └── Instagram Shopping → lead directo

Facebook
  ├── Lead Ads (formulario automático)
  └── Comentarios en Marketplace / Grupo

TikTok
  ├── Comentarios en videos virales
  └── TikTok Shop → órdenes directas

Shopee
  ├── Preguntas en productos
  └── Órdenes directas en marketplace

Gmail
  ├── Campañas promocionales → reply → lead
  └── Firma automática con catálogo

Web (Próximamente)
  ├── Landing page con captura
  └── Chat widget con EVA
```

### 6.2 Lead Scoring (0-100)

```
PUNTOS POR ACCIÓN:
  +30  Mensaje directo WhatsApp preguntando precio
  +25  Click en catálogo compartido
  +20  Interacción en Instagram (comentario en producto)
  +15  Abre email promocional
  +10  Sigue cuenta de Instagram/TikTok
  +5   Like en publicación
  +5   Miembro del grupo de WhatsApp/Facebook
  -10  No responde en >7 días
  -20  Rechaza oferta explícitamente

SEGMENTOS:
  🔥 Hot  (80-100): Contactar inmediatamente, prioridad máxima
  💡 Warm (40-79):  Secuencia de nurturing activa
  ❄️ Cold (10-39):  Campaña de reactivación mensual
  💀 Dead (0-9):    Guardar para análisis, no contactar
```

### 6.3 Métricas Clave (KPIs)

| Métrica | Target | Frecuencia |
|---------|--------|------------|
| Leads capturados/día | >20 | Diario |
| Tasa de conversión lead→cliente | >15% | Semanal |
| Tiempo promedio lead→cierre | <72 hrs | Semanal |
| Valor promedio orden (AOV) | >$60,000 COP | Semanal |
| Tasa de recompra | >25% | Mensual |
| WhatsApp open rate | >90% | Diario |
| Email open rate | >30% | Por campaña |
| ROI social media | >4x | Mensual |
| Clientes nuevos/mes | >100 | Mensual |

---

## 7. DASHBOARD (Panel de Control)

### 7.1 Vistas del Dashboard

1. **Pipeline View** - Kanban con etapas, valor total, deals activos
2. **Sales Funnel** - Embudo de conversión lead→contact→qualify→proposal→close
3. **Lead Analytics** - Fuentes de leads, score distribution, tendencias
4. **Contact Timeline** - Historial completo por cliente (todos los canales)
5. **Campaign Performance** - ROI por campaña, open rates, conversiones
6. **Invoice/Guide Status** - Facturas pendientes, guías activas, entregas
7. **Product Analytics** - Top sellers, stock bajo, margen por producto
8. **Team Performance** - Deals por agente AI, tasa de cierre

### 7.2 Implementación

- **Flask Dashboard** existente en `http://localhost:5051` - extender con rutas CRM
- Datos en tiempo real vía Supabase REST API (PostgREST en puerto 3000)
- n8n para reportes programados (diarios/semanales por WhatsApp/Telegram)

---

## 8. INTEGRACIÓN CON GOOGLE DRIVE

### Estructura de Carpetas

```
SerpentariuStore/                    (Carpeta raíz compartida)
├── facturas/                         # Facturas PDF (FAC-2026-NNNNN.pdf)
│   ├── 2026/
│   │   ├── 01-enero/
│   │   ├── 02-febrero/
│   │   └── ...
│   └── pendientes/                   # Sin pagar aún
├── guias/                            # Guías de envío PDF
│   ├── servientrega/
│   ├── interrapidisimo/
│   └── envia/
├── catalog/                          # Catálogo de productos
│   ├── camisetas/
│   ├── pantalones/
│   └── accesorios/
├── photos/                           # Fotos de productos
│   ├── 2026/
│   └── campañas/
├── contracts/                        # Contratos partners
├── reports/                          # Reportes semanales/mensuales
│   ├── ventas/
│   └── marketing/
└── backups/                          # Backups de base de datos
```

### Flujo Factura → Drive → WhatsApp

```
1. Venta cerrada → n8n trigger
2. Sales Agent recolecta datos: productos, total, cliente
3. n8n genera PDF (template HTML → Puppeteer → PDF)
4. n8n sube a Drive: POST /upload → facturas/FAC-2026-NNNNN.pdf
5. n8n guarda drive_file_id en tabla invoices
6. n8n descarga URL pública temporal
7. WhatsApp Bot envía PDF + mensaje: "🧿 SerpentariuStore - Factura"
8. Gmail Agent envía copia por correo
```

---

## 9. PLAN DE IMPLEMENTACIÓN

### Fase 1: Fundación (Semana 1)
- [x] Supabase corriendo con PostgreSQL
- [x] n8n operativo con webhooks
- [ ] Ejecutar schema.sql en Supabase (crear tablas CRM)
- [ ] Configurar webhooks entrantes en n8n para leads
- [ ] Conectar Google Drive con n8n (OAuth ya funciona)

### Fase 2: Leads + WhatsApp (Semana 2)
- [ ] Workflow n8n: captura de lead WhatsApp → Supabase
- [ ] Workflow n8n: auto-respuesta inicial
- [ ] Sales Agent integrado con CRM
- [ ] Catálogo de productos cargado en products table

### Fase 3: Facturación + Drive (Semana 3)
- [ ] Workflow n8n: generar factura PDF
- [ ] Workflow n8n: subir factura a Drive
- [ ] Workflow n8n: enviar factura por WhatsApp
- [ ] Workflow n8n: guía de envío + tracking

### Fase 4: Social Media (Semana 4)
- [ ] Instagram Agent → detectar leads en comments/DM
- [ ] Facebook Lead Ads → webhook → CRM
- [ ] TikTok Agent → capturar leads
- [ ] Shopee → sincronizar órdenes

### Fase 5: Marketing + Nurturing (Semana 5)
- [ ] Gmail Agent → campañas promocionales
- [ ] WhatsApp broadcast → ofertas
- [ ] Lead scoring automático
- [ ] Secuencias de nurturing (abandonado, post-compra, reactivación)

### Fase 6: Dashboard + Optimización (Semana 6)
- [ ] Extender dashboard Flask con vistas CRM
- [ ] Reportes automáticos semanales a WhatsApp
- [ ] Ajustar scoring basado en datos reales
- [ ] Optimizar conversión por canal

---

## 10. TECNOLOGÍAS Y COSTOS

| Componente | Tecnología | Estado |
|------------|------------|--------|
| Base de datos | Supabase (PostgreSQL 15 + pgvector) | ✅ Listo |
| Automatización | n8n (Docker, self-hosted) | ✅ Listo |
| Bot Telegram | Python (eva_telegram_bot.py) | ✅ Listo |
| Bot WhatsApp | Meta Business API (vía n8n) | 🔧 Configurar |
| Almacenamiento | Google Drive API v3 | ✅ Listo |
| Email | Gmail API (IMAP/SMTP bridge) | ✅ Listo |
| AI Agents | 45+ agents (Python) | ✅ Listo |
| LLM | Gemini + big-pickle + Ollama | ✅ Listo |
| Dashboard | Flask + Supabase REST | ✅ Base lista |
| Social APIs | Instagram/Facebook/TikTok/Shopee | 🔧 Configurar |
| Lead Scoring | Algoritmo propio en SQL + Python | 📝 Por crear |
| Factura PDF | Plantilla HTML → Puppeteer (n8n) | 📝 Por crear |

---

## 11. ESQUEMA DE COMUNICACIÓN MULTICANAL

```
CLIENTE
    │
    ├── WhatsApp ────▶ n8n Webhook ────▶ Supabase (interactions)
    │                                        │
    ├── Instagram DM ─▶ n8n Webhook ────▶   │
    │                                        │
    ├── Email ────────▶ Gmail Bridge ────▶   │
    │                                        │
    └── Shopee ────────▶ API Webhook ────▶   │
                                             │
                                             ▼
                                AI Agent (decide acción)
                                             │
                          ┌──────────────────┼──────────────────┐
                          ▼                  ▼                  ▼
                    WhatsApp Bot       Gmail Agent       Social Agent
                    (respuesta)        (email auto)      (reply DM)
```

**Regla de oro**: Toda interacción con el cliente queda registrada en `interactions`, sin importar el canal. El historial del cliente es multicanal y completo.

---

## 12. PLANTILLAS DE MENSAJES

### WhatsApp - Primer Contacto
```
🧿 SerpentariuStore | Ropa con estilo

¡Hola {nombre}! Soy EVA, tu asesora de moda.

Gracias por escribirte. ¿Qué tipo de ropa buscas hoy?

🔥 Tenemos:
• Camisetas oversize desde $45,000
• Pantalones cargo desde $75,000  
• Chaquetas desde $95,000

📸 ¿Te envío nuestro catálogo completo?
```

### WhatsApp - Factura
```
🧿 SERPENTARIUSTORE - FACTURA

Hola {nombre}, aquí tienes tu factura:

━━━━━━━━━━━━━━━━
FACTURA: {invoice_number}
FECHA: {date}
TOTAL: ${total} COP
━━━━━━━━━━━━━━━━

📎 PDF adjunto

💳 Método de pago: Nequi
📱 {nequi_number}
Titular: SerpentariuStore

Por favor confirma el pago con el comprobante para procesar tu envío ✅
```

### WhatsApp - Guía de Envío
```
📦 SERPENTARIUSTORE - TU PEDIDO VA EN CAMINO

Hola {nombre}, tu pedido ya fue despachado:

• Guía: {guide_number}
• Transportadora: {carrier}
• Fecha estimada: {estimated_date}

🔗 Tracking: {tracking_url}

¡Gracias por comprar con nosotros! 🧿
```

### Email - Promocional
```
Subject: 🔥 {nombre}, nuevos diseños llegaron a SerpentariuStore

Hola {nombre},

Esta semana lanzamos:
✨ Colección Verano 2026
🔥 Descuentos hasta 30%
🚚 Envío gratis en compras > $150,000

Ver catálogo: {catalog_link}

¿Listo para renovar tu estilo?

🧿 SerpentariuStore
```

---

## RESUMEN

**Modelo elegido**: CRM Propio sobre Supabase + n8n + AI Agents

**Razones**:
1. Ya tienes toda la infraestructura (n8n, Supabase, PostgreSQL, 45+ agents)
2. Control total de datos (sin depender de SaaS externo)
3. Integración nativa con WhatsApp, Drive, Gmail
4. Los AI Agents existentes consumen directamente los datos del CRM
5. Cero costo adicional de licencias CRM
6. Escalable: de 1 a 10,000 clientes sin cambiar arquitectura
7. Optimizado para este equipo (todo corre local en Docker)

**Primer paso concreto**: Ejecutar el schema.sql en Supabase para crear las tablas.
