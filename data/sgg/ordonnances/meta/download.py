import json
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

meta_path = Path(sys.argv[1])
raw_dir = Path(sys.argv[2])
log_path = Path(sys.argv[3])

with open(meta_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

docs = data['documents']
errors = 0
success = 0
skipped = 0

for doc in docs:
    doc_id = doc['id']
    url_pdf = doc['url_pdf']
    filename = f'{doc_id}.pdf'
    dest = raw_dir / filename
    
    # Vérifier si déjà téléchargé
    if dest.exists() and dest.stat().st_size > 0:
        msg = f"SKIP - {filename} - déjà présent"
        print(msg)
        with open(log_path, 'a') as log:
            log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
        skipped += 1
        continue
    
    print(f"DL - {filename}...")
    
    result = subprocess.run([
        'curl', '-sL', url_pdf,
        '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        '-o', str(dest)
    ], capture_output=True)
    
    if result.returncode == 0 and dest.exists() and dest.stat().st_size > 0:
        size_mb = dest.stat().st_size / (1024*1024)
        msg = f"OK - {filename} - téléchargé ({size_mb:.1f} Mo)"
        print(msg)
        with open(log_path, 'a') as log:
            log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
        success += 1
    else:
        msg = f"ERROR - {filename} - échec (code: {result.returncode})"
        print(msg)
        with open(log_path, 'a') as log:
            log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
        if dest.exists():
            dest.unlink()
        errors += 1

summary = f"Résumé: {success} OK, {errors} ERROR, {skipped} SKIP sur {len(docs)} total"
print(summary)
with open(log_path, 'a') as log:
    log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {summary}\n")
