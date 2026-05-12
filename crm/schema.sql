-- ============================================================
-- SERPENTARIUSTORE CRM - Esquema de Base de Datos
-- Motor: PostgreSQL 15+ (Supabase)
-- Fecha: Mayo 2026
-- ============================================================

-- Extensión para UUIDs (gen_random_uuid() built-in desde PG 13)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- 1. CONTACTOS (Clientes + Leads)
-- ============================================================
CREATE TABLE contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    whatsapp_phone TEXT UNIQUE,
    telegram_id TEXT UNIQUE,
    instagram_handle TEXT,
    facebook_id TEXT,
    tiktok_handle TEXT,
    shopee_id TEXT,
    tags TEXT[] DEFAULT '{}',
    source TEXT DEFAULT 'whatsapp' CHECK (source IN ('whatsapp','instagram','facebook','tiktok','shopee','referido','web','telegram','email','presencial')),
    status TEXT DEFAULT 'lead' CHECK (status IN ('lead','contacted','qualified','customer','inactive','lost','blocked')),
    lifetime_value DECIMAL(12,2) DEFAULT 0,
    total_orders INT DEFAULT 0,
    first_purchase_date TIMESTAMPTZ,
    last_purchase_date TIMESTAMPTZ,
    last_interaction_at TIMESTAMPTZ,
    notes TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 2. PIPELINE DE VENTAS (Oportunidades)
-- ============================================================
CREATE TABLE deals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    stage TEXT NOT NULL DEFAULT 'lead' CHECK (stage IN ('lead','contacted','qualified','proposal','negotiation','won','lost')),
    value DECIMAL(12,2) DEFAULT 0,
    probability INT DEFAULT 10 CHECK (probability >= 0 AND probability <= 100),
    source TEXT,
    assigned_agent TEXT,
    expected_close_date DATE,
    closed_date TIMESTAMPTZ,
    outcome TEXT CHECK (outcome IN ('won','lost','cancelled')),
    lost_reason TEXT,
    products JSONB[] DEFAULT '{}',
    activities JSONB[] DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 3. ÓRDENES (Ventas Completadas)
-- ============================================================
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deal_id UUID REFERENCES deals(id),
    contact_id UUID REFERENCES contacts(id) NOT NULL,
    order_number TEXT UNIQUE NOT NULL,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending','confirmed','paid','shipped','delivered','cancelled','refunded')),
    subtotal DECIMAL(12,2) NOT NULL DEFAULT 0,
    discount DECIMAL(12,2) DEFAULT 0,
    shipping_cost DECIMAL(12,2) DEFAULT 0,
    total DECIMAL(12,2) NOT NULL DEFAULT 0,
    payment_method TEXT CHECK (payment_method IN ('nequi','bancolombia','efectivo','shopee_pay','transferencia','otros')),
    payment_status TEXT DEFAULT 'pending' CHECK (payment_status IN ('pending','confirmed','failed','refunded')),
    shipping_address TEXT,
    shipping_city TEXT,
    shipping_guide TEXT,
    shipping_carrier TEXT CHECK (shipping_carrier IN ('servientrega','interrapidisimo','envia','coordinadora','otros')),
    invoice_drive_id TEXT,
    guide_drive_id TEXT,
    notes TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 4. ITEMS DE ÓRDENES
-- ============================================================
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    product_sku TEXT NOT NULL,
    product_name TEXT NOT NULL,
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    unit_price DECIMAL(12,2) NOT NULL,
    total_price DECIMAL(12,2) NOT NULL,
    size TEXT,
    color TEXT,
    metadata JSONB DEFAULT '{}'
);

-- ============================================================
-- 5. PRODUCTOS (Catálogo)
-- ============================================================
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    category TEXT CHECK (category IN ('camisetas','pantalones','chaquetas','accesorios','hoodies','zapatos','otros')),
    subcategory TEXT,
    price DECIMAL(12,2) NOT NULL,
    cost_price DECIMAL(12,2),
    sizes TEXT[] DEFAULT '{}',
    colors TEXT[] DEFAULT '{}',
    stock INT DEFAULT 0,
    min_stock INT DEFAULT 5,
    images TEXT[] DEFAULT '{}',
    tags TEXT[] DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    is_featured BOOLEAN DEFAULT false,
    shopee_id TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 6. INTERACCIONES (Historial multicanal)
-- ============================================================
CREATE TABLE interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
    deal_id UUID REFERENCES deals(id),
    channel TEXT NOT NULL CHECK (channel IN ('whatsapp','telegram','email','instagram','facebook','tiktok','shopee','web','presencial')),
    direction TEXT NOT NULL CHECK (direction IN ('inbound','outbound')),
    type TEXT NOT NULL CHECK (type IN ('message','call','email','comment','dm','order_note','system','payment_confirmation','shipping_update')),
    content TEXT,
    media_urls TEXT[] DEFAULT '{}',
    ai_agent TEXT,
    sentiment TEXT CHECK (sentiment IN ('positive','neutral','negative','angry')),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 7. CAMPAÑAS DE MARKETING
-- ============================================================
CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('email','whatsapp','instagram_ads','facebook_ads','tiktok','sms','multicanal')),
    status TEXT DEFAULT 'draft' CHECK (status IN ('draft','active','paused','completed','cancelled')),
    audience_tags TEXT[] DEFAULT '{}',
    audience_query TEXT,
    content JSONB DEFAULT '{}',
    scheduled_at TIMESTAMPTZ,
    started_at TIMESTAMPTZ,
    ended_at TIMESTAMPTZ,
    budget DECIMAL(12,2) DEFAULT 0,
    spent DECIMAL(12,2) DEFAULT 0,
    leads_generated INT DEFAULT 0,
    deals_closed INT DEFAULT 0,
    revenue_generated DECIMAL(12,2) DEFAULT 0,
    roi DECIMAL(5,2),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 8. LEAD SCORING
-- ============================================================
CREATE TABLE lead_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE UNIQUE,
    score INT DEFAULT 0 CHECK (score >= 0 AND score <= 100),
    recency_days INT,
    frequency_30d INT DEFAULT 0,
    monetary DECIMAL(12,2) DEFAULT 0,
    messages_sent INT DEFAULT 0,
    catalog_views INT DEFAULT 0,
    website_visits INT DEFAULT 0,
    cart_abandoned INT DEFAULT 0,
    social_engagement INT DEFAULT 0,
    email_opens INT DEFAULT 0,
    email_clicks INT DEFAULT 0,
    tier TEXT GENERATED ALWAYS AS (
        CASE
            WHEN score >= 80 THEN 'hot'
            WHEN score >= 40 THEN 'warm'
            WHEN score >= 10 THEN 'cold'
            ELSE 'dead'
        END
    ) STORED,
    last_calculated TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 9. FACTURAS (metadatos de Drive)
-- ============================================================
CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
    invoice_number TEXT UNIQUE NOT NULL,
    drive_file_id TEXT NOT NULL,
    drive_url TEXT,
    file_type TEXT DEFAULT 'pdf',
    total DECIMAL(12,2),
    tax DECIMAL(12,2) DEFAULT 0,
    status TEXT DEFAULT 'issued' CHECK (status IN ('issued','paid','cancelled','refunded')),
    sent_whatsapp BOOLEAN DEFAULT false,
    sent_email BOOLEAN DEFAULT false,
    paid_at TIMESTAMPTZ,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 10. GUÍAS DE ENVÍO
-- ============================================================
CREATE TABLE shipping_guides (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
    guide_number TEXT NOT NULL,
    carrier TEXT NOT NULL CHECK (carrier IN ('servientrega','interrapidisimo','envia','coordinadora','otros')),
    drive_file_id TEXT,
    drive_url TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending','in_transit','delivered','failed','returned')),
    tracking_url TEXT,
    sent_whatsapp BOOLEAN DEFAULT false,
    estimated_delivery DATE,
    delivered_at TIMESTAMPTZ,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 11. REGLAS DE AUTO-RESPUESTA
-- ============================================================
CREATE TABLE auto_response_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trigger_type TEXT NOT NULL CHECK (trigger_type IN ('keyword','stage_change','payment','lead_source','inactivity','campaign')),
    trigger_value TEXT NOT NULL,
    action_type TEXT NOT NULL CHECK (action_type IN ('send_whatsapp','send_email','assign_agent','create_deal','update_stage','add_tag','remove_tag','notify_team')),
    action_config JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    priority INT DEFAULT 0,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 12. AUDITORÍA (log de cambios)
-- ============================================================
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_name TEXT NOT NULL,
    record_id UUID NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('INSERT','UPDATE','DELETE')),
    old_data JSONB,
    new_data JSONB,
    changed_by TEXT DEFAULT 'system',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- VISTAS ÚTILES
-- ============================================================

-- Pipeline de ventas con valores agregados
CREATE VIEW vw_pipeline AS
SELECT
    stage,
    COUNT(*) AS deals_count,
    SUM(value) AS total_value,
    AVG(probability) AS avg_probability,
    SUM(value * probability / 100) AS weighted_value
FROM deals
WHERE outcome IS NULL OR outcome NOT IN ('won','lost')
GROUP BY stage
ORDER BY array_position(ARRAY['lead','contacted','qualified','proposal','negotiation'], stage);

-- Leads calientes (hot) para acción inmediata
CREATE VIEW vw_hot_leads AS
SELECT
    c.id,
    c.full_name,
    c.whatsapp_phone,
    c.source,
    ls.score,
    ls.tier,
    c.last_interaction_at,
    c.tags
FROM contacts c
JOIN lead_scores ls ON ls.contact_id = c.id
WHERE ls.score >= 80 AND c.status IN ('lead','contacted','qualified')
ORDER BY ls.score DESC, c.last_interaction_at DESC;

-- Resumen de ventas por día
CREATE VIEW vw_daily_sales AS
SELECT
    DATE(o.created_at) AS sale_date,
    COUNT(*) AS orders_count,
    SUM(o.total) AS total_revenue,
    AVG(o.total) AS avg_order_value,
    COUNT(DISTINCT o.contact_id) AS unique_customers
FROM orders o
WHERE o.status NOT IN ('cancelled','refunded')
GROUP BY DATE(o.created_at)
ORDER BY sale_date DESC;

-- Top productos vendidos
CREATE VIEW vw_top_products AS
SELECT
    oi.product_sku,
    oi.product_name,
    SUM(oi.quantity) AS total_sold,
    SUM(oi.total_price) AS total_revenue,
    COUNT(DISTINCT oi.order_id) AS order_count
FROM order_items oi
JOIN orders o ON o.id = oi.order_id
WHERE o.status NOT IN ('cancelled','refunded')
GROUP BY oi.product_sku, oi.product_name
ORDER BY total_sold DESC
LIMIT 50;

-- ============================================================
-- FUNCIONES ÚTILES
-- ============================================================

-- Calcular lead score para un contacto
CREATE OR REPLACE FUNCTION calculate_lead_score(p_contact_id UUID)
RETURNS INT AS $$
DECLARE
    v_score INT := 0;
    v_recency INT;
    v_frequency INT;
    v_monetary DECIMAL;
    v_engagement INT;
BEGIN
    -- Días desde última interacción (máx 30)
    SELECT COALESCE(
        EXTRACT(DAY FROM NOW() - last_interaction_at)::INT, 30
    ) INTO v_recency FROM contacts WHERE id = p_contact_id;

    -- Interacciones últimos 30 días
    SELECT COUNT(*) INTO v_frequency
    FROM interactions
    WHERE contact_id = p_contact_id
      AND created_at > NOW() - INTERVAL '30 days';

    -- Gasto total
    SELECT COALESCE(SUM(total), 0) INTO v_monetary
    FROM orders
    WHERE contact_id = p_contact_id AND status NOT IN ('cancelled','refunded');

    -- Engagement social
    SELECT COALESCE(SUM(social_engagement), 0) INTO v_engagement
    FROM lead_scores WHERE contact_id = p_contact_id;

    -- Cálculo
    v_score := v_score + GREATEST(30 - v_recency, 0);  -- hasta 30 pts por recencia
    v_score := v_score + LEAST(v_frequency * 5, 25);    -- hasta 25 pts por frecuencia
    v_score := v_score + LEAST(FLOOR(v_monetary / 50000)::INT * 5, 25); -- hasta 25 pts por monetary
    v_score := v_score + LEAST(v_engagement, 20);        -- hasta 20 pts por engagement

    -- Actualizar o insertar en lead_scores
    INSERT INTO lead_scores (contact_id, score, recency_days, frequency_30d, monetary, social_engagement, last_calculated)
    VALUES (p_contact_id, v_score, v_recency, v_frequency, v_monetary, v_engagement, NOW())
    ON CONFLICT (contact_id) DO UPDATE SET
        score = v_score,
        recency_days = v_recency,
        frequency_30d = v_frequency,
        monetary = v_monetary,
        last_calculated = NOW();

    RETURN v_score;
END;
$$ LANGUAGE plpgsql;

-- Generar número de factura
CREATE OR REPLACE FUNCTION generate_invoice_number()
RETURNS TEXT AS $$
DECLARE
    v_year TEXT := EXTRACT(YEAR FROM NOW())::TEXT;
    v_seq INT;
BEGIN
    SELECT COALESCE(MAX(SUBSTRING(invoice_number FROM '\d+$')::INT), 0) + 1
    INTO v_seq
    FROM invoices
    WHERE invoice_number LIKE 'FAC-' || v_year || '-%';

    RETURN 'FAC-' || v_year || '-' || LPAD(v_seq::TEXT, 5, '0');
END;
$$ LANGUAGE plpgsql;

-- Generar número de orden
CREATE OR REPLACE FUNCTION generate_order_number()
RETURNS TEXT AS $$
DECLARE
    v_year TEXT := EXTRACT(YEAR FROM NOW())::TEXT;
    v_seq INT;
BEGIN
    SELECT COALESCE(MAX(SUBSTRING(order_number FROM '\d+$')::INT), 0) + 1
    INTO v_seq
    FROM orders
    WHERE order_number LIKE 'ORD-' || v_year || '-%';

    RETURN 'ORD-' || v_year || '-' || LPAD(v_seq::TEXT, 5, '0');
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- TRIGGERS
-- ============================================================

-- Actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_contacts_updated_at
    BEFORE UPDATE ON contacts
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trg_deals_updated_at
    BEFORE UPDATE ON deals
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trg_orders_updated_at
    BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trg_products_updated_at
    BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- Actualizar last_interaction_at en contactos cuando hay nueva interacción
CREATE OR REPLACE FUNCTION update_contact_last_interaction()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE contacts
    SET last_interaction_at = NEW.created_at
    WHERE id = NEW.contact_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_interaction_contact_update
    AFTER INSERT ON interactions
    FOR EACH ROW EXECUTE FUNCTION update_contact_last_interaction();

-- Auditoría de cambios en deals
CREATE OR REPLACE FUNCTION audit_deal_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, record_id, action, old_data, new_data, changed_by)
        VALUES ('deals', NEW.id, 'UPDATE',
                row_to_json(OLD)::JSONB,
                row_to_json(NEW)::JSONB,
                current_setting('app.agent_name', true));
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_deals_audit
    AFTER UPDATE ON deals
    FOR EACH ROW
    WHEN (OLD.stage IS DISTINCT FROM NEW.stage OR OLD.value IS DISTINCT FROM NEW.value)
    EXECUTE FUNCTION audit_deal_changes();

-- ============================================================
-- ÍNDICES PARA RENDIMIENTO
-- ============================================================
CREATE INDEX idx_contacts_phone ON contacts(phone);
CREATE INDEX idx_contacts_whatsapp ON contacts(whatsapp_phone);
CREATE INDEX idx_contacts_status ON contacts(status);
CREATE INDEX idx_contacts_source ON contacts(source);
CREATE INDEX idx_contacts_tags ON contacts USING GIN(tags);
CREATE INDEX idx_deals_stage ON deals(stage);
CREATE INDEX idx_deals_contact ON deals(contact_id);
CREATE INDEX idx_deals_outcome ON deals(outcome);
CREATE INDEX idx_orders_number ON orders(order_number);
CREATE INDEX idx_orders_contact ON orders(contact_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_payment ON orders(payment_status);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_sku ON order_items(product_sku);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_active ON products(is_active);
CREATE INDEX idx_products_tags ON products USING GIN(tags);
CREATE INDEX idx_interactions_contact ON interactions(contact_id);
CREATE INDEX idx_interactions_channel ON interactions(channel);
CREATE INDEX idx_interactions_created ON interactions(created_at DESC);
CREATE INDEX idx_interactions_sentiment ON interactions(sentiment);
CREATE INDEX idx_campaigns_type ON campaigns(type);
CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_lead_scores_score ON lead_scores(score DESC);
CREATE INDEX idx_lead_scores_tier ON lead_scores(tier);
CREATE INDEX idx_invoices_number ON invoices(invoice_number);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_shipping_guides_status ON shipping_guides(status);
CREATE INDEX idx_audit_log_table ON audit_log(table_name, record_id);
CREATE INDEX idx_audit_log_created ON audit_log(created_at DESC);

-- ============================================================
-- DATOS INICIALES (Seed)
-- ============================================================

-- Reglas de auto-respuesta por defecto
INSERT INTO auto_response_rules (trigger_type, trigger_value, action_type, action_config, priority, description) VALUES
('keyword', 'precio', 'send_whatsapp', '{"template": "precio_catalogo"}', 10, 'Cuando preguntan precios, enviar catálogo'),
('keyword', 'catálogo', 'send_whatsapp', '{"template": "enviar_catalogo"}', 10, 'Solicitud de catálogo'),
('keyword', 'gracias', 'send_whatsapp', '{"template": "de_nada"}', 5, 'Agradecimiento automático'),
('stage_change', 'won', 'create_deal', '{"auto_create_invoice": true}', 100, 'Deal ganado → crear factura automáticamente'),
('stage_change', 'proposal', 'send_whatsapp', '{"template": "propuesta_enviada"}', 50, 'Propuesta enviada → notificar al cliente'),
('lead_source', 'instagram', 'add_tag', '{"tag": "instagram_lead"}', 20, 'Marcar leads de Instagram'),
('lead_source', 'whatsapp', 'add_tag', '{"tag": "whatsapp_lead"}', 20, 'Marcar leads de WhatsApp'),
('inactivity', '7_dias', 'send_whatsapp', '{"template": "reactivacion"}', 30, 'Lead inactivo 7 días → reactivar'),
('payment', 'confirmed', 'update_stage', '{"new_stage": "paid"}', 90, 'Pago confirmado → actualizar orden'),
('keyword', 'donde está mi pedido', 'send_whatsapp', '{"template": "tracking"}', 50, 'Cliente pregunta por su pedido');
