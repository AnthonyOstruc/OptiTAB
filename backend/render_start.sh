#!/bin/bash

# Script de démarrage pour Render - Solution ultime
echo "=== Démarrage de l'application OptiTAB ==="

# Change vers le répertoire backend
cd /opt/render/project/src/backend

# Démarre Gunicorn avec le fichier de configuration
PYTHONPATH=/opt/render/project/src/backend gunicorn --config gunicorn.conf.py backendAPI.wsgi:application --bind 0.0.0.0:$PORT
