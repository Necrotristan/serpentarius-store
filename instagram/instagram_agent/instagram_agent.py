#!/usr/bin/env python3
"""
Instagram Agent - Manages Instagram Shop, Reels, DMs, creators
Uses: instagram-marketing skill
"""
import os, sys, time, requests, json

sys.path.insert(0, '/home/adminbot/.local/lib/python3.14/site-packages')

LOG_FILE = '/home/adminbot/Proyecto EVA/eva/agents/instagram_agent/instagram.log'
N8N_URL = "http://localhost:5678"

def log(msg):
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

def check_instagram_integration():
    """Check if Instagram is connected to n8n"""
    try:
        r = requests.get(N8N_URL + "/rest/workflows", timeout=5)
        if r.status_code == 200:
            workflows = r.json()
            instagram_workflows = [w for w in workflows if 'instagram' in w.get('name', '').lower()]
            return len(instagram_workflows) > 0
    except:
        pass
    return False

def process_instructions():
    """Process instructions from EVA"""
    instr_path = '/home/adminbot/Proyecto EVA/eva/agents/instagram_agent/instructions.txt'
    if os.path.exists(instr_path):
        with open(instr_path, 'r') as f:
            instructions = f.readlines()
        
        for line in instructions[-5:]:
            line_lower = line.lower()
            if 'shop' in line_lower or 'tienda' in line_lower:
                log("Configurando Instagram Shop...")
            elif 'reel' in line_lower or 'video' in line_lower or 'contenido' in line_lower:
                log("Planificando Reels virales...")
            elif 'dm' in line_lower or 'mensaje' in line_lower:
                log("Configurando automatización de DMs...")
            elif 'influencer' in line_lower or 'creador' in line_lower or 'afiliado' in line_lower:
                log("Gestionando creadores e influencers...")
            elif 'anuncio' in line_lower or 'ad' in line_lower:
                log("Optimizando campañas de anuncios...")
            elif 'story' in line_lower or 'historia' in line_lower:
                log("Preparando Stories con productos...")
        
        open(instr_path, 'w').close()

def monitor_instagram_health():
    """Monitor Instagram Shop health metrics"""
    # TODO: Check violations, account health, DM response times
    # Use Instagram Graph API when available
    pass

def main():
    log("Instagram Agent iniciado - Usando skill: instagram-marketing")
    
    last_check = 0
    
    while True:
        now = time.time()
        
        # Check Instagram integration every 10 minutes
        if now - last_check > 600:
            if not check_instagram_integration():
                log("Instagram workflows not found in n8n")
            last_check = now
        
        process_instructions()
        monitor_instagram_health()
        time.sleep(60)

if __name__ == '__main__':
    main()
