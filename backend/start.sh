#!/bin/bash

# Script de démarrage simple pour Render
echo "=== Démarrage OptiTAB Backend ==="

# Aller dans le dossier backend et lancer gunicorn
cd /opt/render/project/src/backend && PYTHONPATH=/opt/render/project/src/backend gunicorn backendAPI.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 30
