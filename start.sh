#!/bin/bash

# Script de démarrage pour Render avec collecte des fichiers statiques
echo "=== Démarrage OptiTAB Backend ==="

# Créer les répertoires médias si manquants (Render persistent disk)
# Utiliser MEDIA_ROOT si défini (Render) sinon ./media
MEDIA_DIR=${MEDIA_ROOT:-backend/media}
mkdir -p "$MEDIA_DIR/exercice_images"
mkdir -p "$MEDIA_DIR/cours_images"
mkdir -p "$MEDIA_DIR/quiz_images"

# Si MEDIA_DIR différent de ./media et que ./media contient des fichiers seed,
# copier tout fichier manquant (sans écraser ceux déjà présents)
if [ "$MEDIA_DIR" != "backend/media" ] && [ -d "backend/media" ]; then
  echo "Syncing seed media into $MEDIA_DIR (no overwrite)..."
  cp -rn backend/media/* "$MEDIA_DIR" 2>/dev/null || true
  # Copier aussi récursivement l'intérieur des sous-dossiers si absents
  for sub in exercice_images cours_images quiz_images; do
    if [ -d "backend/media/$sub" ]; then
      mkdir -p "$MEDIA_DIR/$sub"
      cp -rn backend/media/$sub/* "$MEDIA_DIR/$sub" 2>/dev/null || true
    fi
  done
fi

# Collecte des fichiers statiques
echo "Collecting static files..."
cd backend && python manage.py collectstatic --noinput --clear

# Run gunicorn with correct module path
echo "Starting Gunicorn..."
exec gunicorn backendAPI.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 30
