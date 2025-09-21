#!/bin/bash

# Script de démarrage pour Render avec collecte des fichiers statiques
echo "=== Démarrage OptiTAB Backend ==="

# Créer les répertoires médias si manquants (Render persistent disk)
mkdir -p media/exercice_images media/cours_images media/quiz_images

# Collecte des fichiers statiques
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run gunicorn with correct module path
echo "Starting Gunicorn..."
exec gunicorn backendAPI.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 30
