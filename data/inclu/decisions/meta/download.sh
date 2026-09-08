#!/bin/bash
# Script de téléchargement des PDFs - Décisions
# Appelle download.py avec les bons chemins

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAW_DIR="$(dirname "$SCRIPT_DIR")"

# Convertir les chemins en format Windows pour Python
SCRIPT_DIR_WIN=$(cygpath -w "$SCRIPT_DIR")
RAW_DIR_WIN=$(cygpath -w "$RAW_DIR")

# Lancer le script Python
python -u "$SCRIPT_DIR_WIN\\download.py" "$SCRIPT_DIR_WIN\\metadata.json" "$RAW_DIR_WIN" "$SCRIPT_DIR_WIN\\download.log"
