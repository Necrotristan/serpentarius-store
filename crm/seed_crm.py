#!/usr/bin/env python3
"""Seed CRM database with realistic data for SerpentariuStore"""
import psycopg2
from uuid import uuid4

conn = psycopg2.connect(
    host='localhost', port=5432, user='postgres',
    password='bbL2Tdlq4lPFSbr4xUCu', dbname='serpentarius_crm'
)
conn.autocommit = False
cur = conn.cursor()

# Clean existing data
for t in ['lead_scores', 'interactions', 'shipping_guides', 'invoices', 'order_items', 'orders', 'deals', 'campaigns', 'auto_response_rules', 'audit_log', 'products', 'contacts']:
    cur.execute(f'DELETE FROM {t}')

def uid():
    return str(uuid4())

# Products
products = [
    ('IM-POM-001', 'Camiseta Iron Maiden - Piece of Mind', 'camisetas', 45000, 22000, ['S','M','L','XL'], ['Negro','Blanco','Gris'], 25),
    ('MT-MOP-002', 'Chaqueta Metallica - Master of Puppets', 'chaquetas', 120000, 65000, ['M','L','XL'], ['Negro'], 10),
    ('SL-RIB-003', 'Gorra Slayer - Reign in Blood', 'accesorios', 35000, 15000, ['Ajustable'], ['Negro','Rojo'], 30),
    ('TL-LAT-004', 'Camiseta Tool - Lateralus', 'camisetas', 55000, 25000, ['S','M','L','XL'], ['Negro','Violeta'], 20),
    ('PN-TIR-005', 'Jean Tiro', 'pantalones', 170000, 85000, ['30','32','34','36'], ['Negro','Azul oscuro'], 15),
    ('IM-FEAR-006', 'Camiseta Iron Maiden - Fear of the Dark', 'camisetas', 48000, 23000, ['S','M','L','XL'], ['Negro','Gris'], 18),
    ('SL-SHZ-007', 'Sudadera Slayer - Show No Mercy', 'hoodies', 95000, 48000, ['M','L','XL'], ['Negro'], 12),
    ('PT-CF-008', 'Camiseta Pantera - Cowboys from Hell', 'camisetas', 50000, 24000, ['S','M','L','XL'], ['Negro','Blanco'], 22),
    ('GJ-WAY-009', 'Camiseta Gojira - The Way of All Flesh', 'camisetas', 55000, 26000, ['M','L','XL'], ['Negro','Verde oscuro'], 14),
    ('AC-DC-010', 'Chaqueta AC/DC - Back in Black', 'chaquetas', 135000, 70000, ['M','L','XL'], ['Negro','Azul'], 8),
    ('SP-7TH-011', 'Camiseta Sepultura - Arise', 'camisetas', 42000, 20000, ['S','M','L','XL'], ['Negro','Verde'], 16),
    ('PRL-JAM-012', 'Parche AC/DC', 'accesorios', 12000, 5000, ['Unico'], ['Multicolor'], 50),
]
for p in products:
    cur.execute("""INSERT INTO products (sku, name, category, price, cost_price, sizes, colors, stock, tags, is_active)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,ARRAY['metal','camiseta'],true)""", p)
print(f"Inserted {len(products)} products")

# Contacts
contact_list = [
    ('Pedro López', '+573001234567', 'pedro.lopez@email.com', 'pedro_metal', 'instagram', 'lead'),
    ('Ana Gómez', '+573012345678', 'ana.gomez@email.com', 'ana_rockera', 'tiktok', 'lead'),
    ('Carlos Ruiz', '+573023456789', 'carlos.ruiz@email.com', 'carlos_headbang', 'web', 'lead'),
    ('Laura Mora', '+573034567890', 'laura.mora@email.com', 'laura_mosh', 'whatsapp', 'contacted'),
    ('Diego Rojas', '+573045678901', 'diego.rojas@email.com', 'diego_thrash', 'instagram', 'contacted'),
    ('Sofía Martínez', '+573056789012', 'sofia.mtz@email.com', 'sofia_metalera', 'referido', 'qualified'),
    ('Jorge Pérez', '+573067890123', 'jorge.perez@email.com', 'jorge_prog', 'telegram', 'qualified'),
    ('Valentina Ortiz', '+573078901234', 'valentina.ortiz@email.com', 'vale_slipknot', 'instagram', 'customer'),
    ('Ricardo Vega', '+573089012345', 'ricardo.vega@email.com', 'ricardo_metalhead', 'web', 'qualified'),
    ('Camila Torres', '+573090123456', 'camila.torres@email.com', 'camila_rock', 'whatsapp', 'qualified'),
    ('Andrea Mejía', '+573101234567', 'andrea.mejia@email.com', 'andy_metal', 'instagram', 'customer'),
    ('Miguel Ángel', '+573112345678', 'miguel.angel@email.com', 'mike_riff', 'instagram', 'lead'),
    ('Diana Vargas', '+573123456789', 'diana.vargas@email.com', 'diana_grunge', 'whatsapp', 'customer'),
    ('Pedro Sánchez', '+573134567890', 'pedro.sanchez@email.com', 'pedro_doom', 'referido', 'lost'),
    ('Camila Rincón', '+573145678901', 'camila.rincon@email.com', 'cami_rock', 'tiktok', 'lead'),
]
cid = {}
for c in contact_list:
    uuid = uid()
    cid[c[0]] = uuid
    cur.execute("""INSERT INTO contacts (id, full_name, phone, email, instagram_handle, source, status, whatsapp_phone)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""", (uuid, c[0], c[1], c[2], c[3], c[4], c[5], c[1]))
print(f"Inserted {len(contact_list)} contacts")

# Deals
deal_list = [
    (cid['Pedro López'], 'Camiseta Iron Maiden - Pedro', 'lead', 45000, 10, 'Instagram'),
    (cid['Ana Gómez'], 'Chaqueta Metallica - Ana', 'lead', 120000, 15, 'TikTok'),
    (cid['Carlos Ruiz'], 'Gorra Slayer - Carlos', 'lead', 35000, 10, 'Web'),
    (cid['Laura Mora'], 'Parche AC/DC - Laura', 'contacted', 15000, 30, 'WhatsApp'),
    (cid['Diego Rojas'], 'Camiseta Pantera - Diego', 'contacted', 55000, 25, 'Instagram'),
    (cid['Sofía Martínez'], 'Jean Tiro - Sofía', 'qualified', 180000, 50, 'Referido'),
    (cid['Jorge Pérez'], 'Camiseta Tool - Jorge', 'qualified', 65000, 60, 'Telegram'),
    (cid['Valentina Ortiz'], 'Conjunto Slipknot - Valentina', 'proposal', 210000, 70, 'Instagram'),
    (cid['Ricardo Vega'], 'Pedido Múltiple - Ricardo', 'negotiation', 350000, 85, 'Web'),
    (cid['Camila Torres'], 'Camiseta Gojira - Camila', 'negotiation', 75000, 80, 'WhatsApp'),
    (cid['Andrea Mejía'], 'Camiseta Pantera - Andrea', 'won', 55000, 100, 'Instagram'),
    (cid['Pedro Sánchez'], 'Consulta gorras - Pedro', 'lost', 0, 0, 'Referido'),
]
did = {}
for d in deal_list:
    uuid = uid()
    did[d[0]] = uuid
    cur.execute("""INSERT INTO deals (id, contact_id, title, stage, value, probability, source, assigned_agent)
    VALUES (%s,%s,%s,%s,%s,%s,%s,'Sales Agent')""", (uuid, d[0], d[1], d[2], d[3], d[4], d[5]))
print(f"Inserted {len(deal_list)} deals")

# Orders
order_list = [
    (did[cid['Andrea Mejía']], cid['Andrea Mejía'], 'ORD-2026-00001', 'delivered', 50000, 55000, 'nequi', 'Bogotá', '2026-04-28 10:30:00-05'),
    (did[cid['Diego Rojas']], cid['Diego Rojas'], 'ORD-2026-00002', 'delivered', 50000, 55000, 'bancolombia', 'Medellín', '2026-04-30 14:15:00-05'),
    (did[cid['Sofía Martínez']], cid['Sofía Martínez'], 'ORD-2026-00003', 'delivered', 170000, 180000, 'transferencia', 'Barranquilla', '2026-05-03 11:45:00-05'),
    (did[cid['Valentina Ortiz']], cid['Valentina Ortiz'], 'ORD-2026-00004', 'shipped', 200000, 210000, 'nequi', 'Cali', '2026-05-02 09:00:00-05'),
    (did[cid['Camila Torres']], cid['Camila Torres'], 'ORD-2026-00005', 'paid', 55000, 75000, 'nequi', 'Bogotá', '2026-05-05 13:20:00-05'),
    (did[cid['Jorge Pérez']], cid['Jorge Pérez'], 'ORD-2026-00006', 'shipped', 55000, 65000, 'transferencia', 'Pereira', '2026-05-08 10:00:00-05'),
    (did[cid['Ricardo Vega']], cid['Ricardo Vega'], 'ORD-2026-00007', 'paid', 320000, 350000, 'bancolombia', 'Bogotá', '2026-05-06 08:00:00-05'),
    (None, cid['Diana Vargas'], 'ORD-2026-00008', 'paid', 120000, 120000, 'nequi', 'Manizales', '2026-05-07 15:00:00-05'),
    (None, cid['Sofía Martínez'], 'ORD-2026-00009', 'delivered', 160000, 160000, 'efectivo', 'Barranquilla', '2026-04-20 16:30:00-05'),
    (None, cid['Andrea Mejía'], 'ORD-2026-00010', 'paid', 80000, 85000, 'nequi', 'Bogotá', '2026-05-11 09:15:00-05'),
]
oid = {}
for o in order_list:
    uuid = uid()
    oid[o[2]] = uuid
    cur.execute("""INSERT INTO orders (id, deal_id, contact_id, order_number, status, subtotal, total, payment_method, shipping_city, created_at)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::timestamptz)""", (uuid, o[0], o[1], o[2], o[3], o[4], o[5], o[6], o[7], o[8]))
print(f"Inserted {len(order_list)} orders")

# Order items
items = [
    ('ORD-2026-00001', 'PT-CF-008', 'Camiseta Pantera - Cowboys from Hell', 1, 50000, 50000, 'M', 'Negro'),
    ('ORD-2026-00002', 'PT-CF-008', 'Camiseta Pantera - Cowboys from Hell', 1, 50000, 50000, 'L', 'Negro'),
    ('ORD-2026-00003', 'PN-TIR-005', 'Jean Tiro', 1, 170000, 170000, '34', 'Negro'),
    ('ORD-2026-00004', 'SL-SHZ-007', 'Sudadera Slayer - Show No Mercy', 1, 95000, 95000, 'L', 'Negro'),
    ('ORD-2026-00004', 'IM-POM-001', 'Camiseta Iron Maiden - Piece of Mind', 1, 45000, 45000, 'M', 'Negro'),
    ('ORD-2026-00004', 'SL-RIB-003', 'Gorra Slayer - Reign in Blood', 1, 35000, 35000, 'Ajustable', 'Negro'),
    ('ORD-2026-00004', 'TL-LAT-004', 'Camiseta Tool - Lateralus', 1, 55000, 25000, 'S', 'Negro'),
    ('ORD-2026-00005', 'GJ-WAY-009', 'Camiseta Gojira - The Way of All Flesh', 1, 55000, 55000, 'M', 'Negro'),
    ('ORD-2026-00006', 'TL-LAT-004', 'Camiseta Tool - Lateralus', 1, 55000, 55000, 'L', 'Violeta'),
    ('ORD-2026-00007', 'IM-POM-001', 'Camiseta Iron Maiden - Piece of Mind', 2, 45000, 90000, 'L', 'Negro'),
    ('ORD-2026-00007', 'MT-MOP-002', 'Chaqueta Metallica - Master of Puppets', 1, 120000, 120000, 'L', 'Negro'),
    ('ORD-2026-00007', 'SL-RIB-003', 'Gorra Slayer - Reign in Blood', 2, 35000, 70000, 'Ajustable', 'Negro'),
    ('ORD-2026-00007', 'IM-FEAR-006', 'Camiseta Iron Maiden - Fear of the Dark', 1, 48000, 40000, 'M', 'Negro'),
    ('ORD-2026-00008', 'AC-DC-010', 'Chaqueta AC/DC - Back in Black', 1, 135000, 120000, 'M', 'Negro'),
    ('ORD-2026-00009', 'IM-POM-001', 'Camiseta Iron Maiden - Piece of Mind', 1, 45000, 45000, 'L', 'Negro'),
    ('ORD-2026-00009', 'PN-TIR-005', 'Jean Tiro', 1, 170000, 115000, '32', 'Azul oscuro'),
    ('ORD-2026-00010', 'SL-RIB-003', 'Gorra Slayer - Reign in Blood', 1, 35000, 35000, 'Ajustable', 'Rojo'),
    ('ORD-2026-00010', 'PRL-JAM-012', 'Parche AC/DC', 2, 12000, 24000, 'Unico', 'Multicolor'),
    ('ORD-2026-00010', 'IM-POM-001', 'Camiseta Iron Maiden - Piece of Mind', 1, 45000, 21000, 'M', 'Gris'),
]
for i in items:
    cur.execute("""INSERT INTO order_items (order_id, product_sku, product_name, quantity, unit_price, total_price, size, color)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""", (oid[i[0]], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
print(f"Inserted {len(items)} order items")

# Lead scores
scores = [
    (cid['Pedro López'], 15, 12, 1, 0),
    (cid['Ana Gómez'], 20, 8, 2, 0),
    (cid['Carlos Ruiz'], 10, 15, 0, 0),
    (cid['Laura Mora'], 45, 5, 4, 0),
    (cid['Diego Rojas'], 55, 3, 3, 55000),
    (cid['Sofía Martínez'], 85, 1, 6, 340000),
    (cid['Jorge Pérez'], 70, 2, 5, 65000),
    (cid['Valentina Ortiz'], 75, 2, 4, 210000),
    (cid['Ricardo Vega'], 90, 0, 8, 350000),
    (cid['Camila Torres'], 80, 1, 5, 75000),
    (cid['Andrea Mejía'], 65, 3, 2, 55000),
    (cid['Miguel Ángel'], 5, 20, 0, 0),
    (cid['Diana Vargas'], 60, 4, 3, 120000),
    (cid['Pedro Sánchez'], 10, 30, 0, 0),
    (cid['Camila Rincón'], 8, 18, 1, 0),
]
for s in scores:
    cur.execute("""INSERT INTO lead_scores (contact_id, score, recency_days, frequency_30d, monetary) VALUES (%s,%s,%s,%s,%s)""", s)
print(f"Inserted {len(scores)} lead scores")

# Interactions
interactions = [
    (cid['Pedro López'], 'instagram', 'inbound', 'dm', 'Hola, quería saber si tienen disponibles las camisetas de Iron Maiden', 'positive'),
    (cid['Ana Gómez'], 'tiktok', 'inbound', 'comment', 'Donde compro esa chaqueta?', 'positive'),
    (cid['Laura Mora'], 'whatsapp', 'inbound', 'message', 'Buenos días, me interesan los parches bordados', 'positive'),
    (cid['Diego Rojas'], 'instagram', 'outbound', 'dm', 'Hola Diego! Vimos que te gustó la camiseta de Pantera, la tenemos disponible', 'positive'),
    (cid['Sofía Martínez'], 'whatsapp', 'inbound', 'message', 'Excelente la calidad! Me interesa otro jean', 'positive'),
    (cid['Ricardo Vega'], 'web', 'inbound', 'message', 'Necesito hacer un pedido corporativo de 10 camisetas', 'positive'),
    (cid['Andrea Mejía'], 'instagram', 'inbound', 'dm', 'Ya recibí mi pedido! Excelente calidad', 'positive'),
    (cid['Pedro Sánchez'], 'whatsapp', 'outbound', 'message', 'Hola Pedro, aún te interesan las gorras?', 'neutral'),
    (cid['Carlos Ruiz'], 'web', 'inbound', 'message', 'Buenas, tienen gorras de Slayer?', 'positive'),
    (cid['Camila Torres'], 'whatsapp', 'inbound', 'message', 'Hola! Quiero la camiseta de Gojira, me la apartas?', 'positive'),
]
for i in interactions:
    cur.execute("""INSERT INTO interactions (contact_id, channel, direction, type, content, sentiment) VALUES (%s,%s,%s,%s,%s,%s)""", i)
print(f"Inserted {len(interactions)} interactions")

# Auto response rules
rules = [
    ('keyword', 'precio', 'send_whatsapp', '{"template": "precio_catalogo"}', 10, 'Enviar catálogo de precios'),
    ('keyword', 'catálogo', 'send_whatsapp', '{"template": "enviar_catalogo"}', 10, 'Solicitud de catálogo'),
    ('keyword', 'gracias', 'send_whatsapp', '{"template": "de_nada"}', 5, 'Agradecimiento automático'),
    ('stage_change', 'won', 'create_deal', '{"auto_create_invoice": true}', 100, 'Factura automática al ganar'),
    ('lead_source', 'instagram', 'add_tag', '{"tag": "instagram_lead"}', 20, 'Marcar leads de Instagram'),
    ('inactivity', '7_dias', 'send_whatsapp', '{"template": "reactivacion"}', 30, 'Reactivar leads inactivos'),
    ('payment', 'confirmed', 'update_stage', '{"new_stage": "paid"}', 90, 'Actualizar orden al pagar'),
]
for r in rules:
    cur.execute("""INSERT INTO auto_response_rules (trigger_type, trigger_value, action_type, action_config, priority, description) VALUES (%s,%s,%s,%s,%s,%s)""", r)
print(f"Inserted {len(rules)} auto response rules")

conn.commit()
cur.close()
conn.close()
print("\n✅ CRM seed complete!")
print("Tables: products, contacts, deals, orders, order_items, lead_scores, interactions, auto_response_rules")
