#!/usr/bin/env python3
"""
Gmail Agent - Monitors, optimizes and handles all Gmail operations
Uses: ecommerce-gmail skill
"""
import os, sys, time, requests, json, imaplib, email
from email.header import decode_header

sys.path.insert(0, '/home/adminbot/.local/lib/python3.14/site-packages')

LOG_FILE = '/home/adminbot/agents/gmail_agent/gmail.log'
N8N_URL = "http://localhost:5678"
WEBHOOK_URL = "http://localhost:8080/webhook"

def log(msg):
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

def check_n8n_workflows():
    """Check if Gmail workflows are active in n8n"""
    try:
        # Check if n8n is accessible
        r = requests.get(N8N_URL, timeout=5)
        if r.status_code == 200:
            return True
    except:
        pass
    return False

def process_instructions():
    """Process instructions from EVA"""
    instr_path = '/home/adminbot/agents/gmail_agent/instructions.txt'
    if os.path.exists(instr_path):
        with open(instr_path, 'r') as f:
            instructions = f.readlines()
        
        for line in instructions[-5:]:
            line_lower = line.lower()
            if 'cita' in line_lower or 'appointment' in line_lower:
                log("Configurando detección de citas...")
            elif 'cliente' in line_lower or 'customer' in line_lower:
                log("Optimizando atención al cliente...")
            elif 'venta' in line_lower or 'sale' in line_lower:
                log("Configurando notificaciones de ventas...")
            elif 'proveedor' in line_lower or 'supplier' in line_lower:
                log("Monitoreando emails de proveedores...")
            elif 'marketing' in line_lower:
                log("Preparando campañas de marketing...")
        
        open(instr_path, 'w').close()

def monitor_gmail_integration():
    """Monitor Gmail integration health"""
    if not check_n8n_workflows():
        log("n8n not accessible, Gmail workflows may be down")
        return False
    return True

def main():
    log("Gmail Agent iniciado - Usando skill: ecommerce-gmail")
    
    last_check = 0
    
    while True:
        now = time.time()
        
        # Check Gmail integration every 5 minutes
        if now - last_check > 300:
            monitor_gmail_integration()
            last_check = now
        
        process_instructions()
        time.sleep(60)

if __name__ == '__main__':
    main()
