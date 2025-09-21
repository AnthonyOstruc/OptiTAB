#!/bin/bash

# Script de démarrage pour Render avec collecte des fichiers statiques
 echo "=== Démarrage OptiTAB Backend ==="

# Créer les répertoires médias si manquants (Render persistent disk)
# Utiliser MEDIA_ROOT si défini (Render) sinon ./media
MEDIA_DIR=${MEDIA_ROOT:-media}
mkdir -p "$MEDIA_DIR/exercice_images"
mkdir -p "$MEDIA_DIR/cours_images"
mkdir -p "$MEDIA_DIR/quiz_images"

# Si MEDIA_DIR différent de ./media et que ./media contient des fichiers seed, les copier une fois
if [ "$MEDIA_DIR" != "media" ] && [ -d "media" ] && [ -z "$(ls -A "$MEDIA_DIR" 2>/dev/null)" ]; then
  echo "Seeding media folder from repo to $MEDIA_DIR..."
  cp -r media/* "$MEDIA_DIR" || true
fi

# Collecte des fichiers statiques
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run gunicorn with correct module path
echo "Starting Gunicorn..."
exec gunicorn backendAPI.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 30
