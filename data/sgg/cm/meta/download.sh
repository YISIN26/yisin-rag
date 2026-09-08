#!/bin/bash
# Script de téléchargement PARALLÈLE des PDFs - Conseil des Ministres
# Utilise Python avec ThreadPoolExecutor (20 threads)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAW_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$SCRIPT_DIR/download.log"
META_FILE="$SCRIPT_DIR/metadata.json"

mkdir -p "$RAW_DIR"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] INFO - Début du téléchargement PARALLÈLE (20 threads Python)" >> "$LOG_FILE"

# Exporter les variables pour Python
export RAW_DIR LOG_FILE META_FILE

python -u << 'PYEOF'
import json
import subprocess
import sys
import os
import re
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

meta_path = Path(os.environ['META_FILE'])
raw_dir = Path(os.environ['RAW_DIR'])
log_path = Path(os.environ['LOG_FILE'])

with open(meta_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

docs = data['documents']

def parse_size(size_str):
    match = re.match(r'([\d.]+)\s*(Ko|Mo|Go)', size_str)
    if not match:
        return 0
    value = float(match.group(1))
    unit = match.group(2)
    if unit == 'Ko':
        return int(value * 1024)
    elif unit == 'Mo':
        return int(value * 1024 * 1024)
    elif unit == 'Go':
        return int(value * 1024 * 1024 * 1024)
    return 0

def download_one(doc):
    doc_id = doc['id']
    url_pdf = doc['url_pdf']
    taille = doc['taille']
    filename = f'{doc_id}.pdf'
    dest = raw_dir / filename
    taille_attendue = parse_size(taille)
    
    if dest.exists() and taille_attendue > 0:
        taille_reelle = dest.stat().st_size
        diff = abs(taille_reelle - taille_attendue)
        marge = taille_attendue // 100
        if diff <= marge:
            msg = f"SKIP - {filename} ({taille}) - déjà présent"
            return ('skip', msg)
        else:
            msg = f"INCOMPLET - {filename} (attendu: {taille}, réel: {taille_reelle} octets)"
            dest.unlink()
    
    try:
        result = subprocess.run([
            'curl', '-sL', url_pdf,
            '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            '-o', str(dest)
        ], capture_output=True, timeout=120)
        
        if result.returncode == 0 and dest.exists() and dest.stat().st_size > 0:
            size_mb = dest.stat().st_size / (1024*1024)
            msg = f"OK - {filename} ({taille}) - téléchargé ({size_mb:.1f} Mo)"
            return ('ok', msg)
        else:
            msg = f"ERROR - {filename} ({taille}) - échec (code: {result.returncode})"
            if dest.exists():
                dest.unlink()
            return ('error', msg)
    except Exception as e:
        msg = f"ERROR - {filename} ({taille}) - exception: {str(e)[:50]}"
        if dest.exists():
            dest.unlink()
        return ('error', msg)

success = 0
errors = 0
skipped = 0

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(download_one, doc): doc for doc in docs}
    
    for future in as_completed(futures):
        status, msg = future.result()
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(log_path, 'a') as log:
            log.write(f"[{timestamp}] {msg}\n")
        
        print(msg)
        sys.stdout.flush()
        
        if status == 'ok':
            success += 1
        elif status == 'error':
            errors += 1
        else:
            skipped += 1
        
        total = success + errors + skipped
        if total % 10 == 0:
            print(f"--- Progression: {total}/{len(docs)} ({success} OK, {errors} ERR, {skipped} SKIP) ---")
            sys.stdout.flush()

summary = f"Résumé final: {success} OK, {errors} ERROR, {skipped} SKIP sur {len(docs)} total"
print(summary)
with open(log_path, 'a') as log:
    log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {summary}\n")

PYEOF

echo "[$(date '+%Y-%m-%d %H:%M:%S')] INFO - Fin du téléchargement" >> "$LOG_FILE"
