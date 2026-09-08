import json
import subprocess
import sys
import os
import re
import threading
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

meta_path = Path(sys.argv[1])
raw_dir = Path(sys.argv[2])
log_path = Path(sys.argv[3])

with open(meta_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

docs = data['documents']
print(f'{len(docs)} documents à télécharger')

file_lock = threading.Lock()
downloading = set()

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
    temp_dest = dest.with_suffix('.tmp')
    taille_attendue = parse_size(taille)
    
    with file_lock:
        if dest.exists() and taille_attendue > 0:
            taille_reelle = dest.stat().st_size
            diff = abs(taille_reelle - taille_attendue)
            marge = taille_attendue // 100
            if diff <= marge:
                msg = f"SKIP - {filename} ({taille}) - déjà présent"
                return ('skip', msg)
        
        if filename in downloading:
            msg = f"SKIP - {filename} - déjà en cours"
            return ('skip', msg)
        
        downloading.add(filename)
    
    try:
        result = subprocess.run([
            'curl', '-sL', url_pdf,
            '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            '-o', str(temp_dest)
        ], capture_output=True, timeout=120)
        
        with file_lock:
            if result.returncode == 0 and temp_dest.exists() and temp_dest.stat().st_size > 0:
                if dest.exists():
                    dest.unlink()
                temp_dest.rename(dest)
                
                size_mb = dest.stat().st_size / (1024*1024)
                msg = f"OK - {filename} ({taille}) - téléchargé ({size_mb:.1f} Mo)"
                downloading.discard(filename)
                return ('ok', msg)
            else:
                msg = f"ERROR - {filename} ({taille}) - échec (code: {result.returncode})"
                if temp_dest.exists():
                    temp_dest.unlink()
                downloading.discard(filename)
                return ('error', msg)
    except Exception as e:
        with file_lock:
            msg = f"ERROR - {filename} ({taille}) - exception: {str(e)[:50]}"
            if temp_dest.exists():
                temp_dest.unlink()
            downloading.discard(filename)
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
        if total % 50 == 0:
            print(f"--- Progression: {total}/{len(docs)} ({success} OK, {errors} ERR, {skipped} SKIP) ---")
            sys.stdout.flush()

summary = f"Résumé final: {success} OK, {errors} ERROR, {skipped} SKIP sur {len(docs)} total"
print(summary)
with open(log_path, 'a') as log:
    log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {summary}\n")
