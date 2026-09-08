import json
import subprocess
import sys
import os
import re
import threading
import time
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import unescape

def clean_filename(title, doc_id):
    """Nettoie un titre pour en faire un nom de fichier valide avec ID unique"""
    title = unescape(title)
    title = re.sub(r'[<>:"/\\|?*]', '_', title)
    title = re.sub(r'\s+', ' ', title).strip().rstrip('.')
    if len(title) > 80:
        title = title[:80]
    short_id = doc_id.replace('legis-', '')[:8]
    return f'{title} [{short_id}]'

meta_path = Path(sys.argv[1])
raw_dir = Path(sys.argv[2])
log_path = Path(sys.argv[3])

with open(meta_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

docs = data['documents']
print(f'{len(docs)} documents à télécharger')

file_lock = threading.Lock()
downloading = set()

def download_one(doc):
    doc_id = doc['id']
    url_pdf = doc['url_pdf']
    title = doc['titre']
    
    base_filename = clean_filename(title, doc_id)
    temp_dest = raw_dir / f'.tmp_{doc_id}'
    
    with file_lock:
        if base_filename in downloading:
            return ('skip', f'SKIP - {base_filename} - déjà en cours')
        downloading.add(base_filename)
    
    try:
        result = subprocess.run([
            'curl', '-sL', url_pdf,
            '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            '-o', str(temp_dest)
        ], capture_output=True)
        
        with file_lock:
            if result.returncode == 0 and temp_dest.exists() and temp_dest.stat().st_size > 0:
                # Détecter le type de fichier
                file_type_result = subprocess.run(['file', '-b', '--mime-type', str(temp_dest)], capture_output=True, text=True)
                mime_type = file_type_result.stdout.strip() if file_type_result.returncode == 0 else 'application/octet-stream'
                
                # Déterminer l'extension
                ext_map = {
                    'application/pdf': '.pdf',
                    'image/jpeg': '.jpg',
                    'image/png': '.png',
                    'image/gif': '.gif',
                    'image/webp': '.webp',
                    'image/tiff': '.tiff',
                    'application/msword': '.doc',
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
                    'text/html': '.html',
                    'text/plain': '.txt',
                }
                ext = ext_map.get(mime_type, '.bin')
                
                dest = raw_dir / f'{base_filename}{ext}'
                
                # Gérer les conflits
                counter = 1
                while dest.exists():
                    dest = raw_dir / f'{base_filename} ({counter}){ext}'
                    counter += 1
                
                try:
                    temp_dest.rename(dest)
                except PermissionError:
                    time.sleep(1)
                    try:
                        temp_dest.rename(dest)
                    except:
                        pass
                
                size_mb = dest.stat().st_size / (1024*1024)
                msg = f'OK - {dest.name} ({size_mb:.1f} Mo, {mime_type})'
                downloading.discard(base_filename)
                return ('ok', msg)
            else:
                msg = f'ERROR - {base_filename} - échec'
                if temp_dest.exists():
                    try:
                        temp_dest.unlink()
                    except:
                        pass
                downloading.discard(base_filename)
                return ('error', msg)
    except Exception as e:
        with file_lock:
            msg = f'ERROR - {base_filename} - {str(e)[:50]}'
            if temp_dest.exists():
                try:
                    temp_dest.unlink()
                except:
                    pass
            downloading.discard(base_filename)
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
            log.write(f'[{timestamp}] {msg}\n')
        
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
            print(f'--- Progression: {total}/{len(docs)} ({success} OK, {errors} ERR, {skipped} SKIP) ---')
            sys.stdout.flush()

summary = f'Résumé: {success} OK, {errors} ERROR, {skipped} SKIP sur {len(docs)} total'
print(summary)
with open(log_path, 'a') as log:
    log.write(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {summary}\n')
