#!/bin/bash
# Script de téléchargement des PDFs - LEGIS
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAW_DIR="$(dirname "$SCRIPT_DIR")"
SCRIPT_DIR_WIN=$(cygpath -w "$SCRIPT_DIR")
RAW_DIR_WIN=$(cygpath -w "$RAW_DIR")

python -u "$SCRIPT_DIR_WIN\\download.py" "$SCRIPT_DIR_WIN\\metadata.json" "$RAW_DIR_WIN" "$SCRIPT_DIR_WIN\\download.log"
