#!/bin/bash

# Script de démarrage simple pour Render
echo "=== Démarrage OptiTAB Backend ==="

# Run gunicorn from the backend directory
exec gunicorn backendAPI.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 30
