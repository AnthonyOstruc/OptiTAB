#!/bin/bash

# Script de démarrage pour Render avec collecte des fichiers statiques
echo "=== Démarrage OptiTAB Backend ==="

# Collecte des fichiers statiques
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run gunicorn with correct module path
echo "Starting Gunicorn..."
exec gunicorn backendAPI.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 30
