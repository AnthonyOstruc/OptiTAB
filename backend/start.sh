#!/bin/bash

# Script de démarrage pour Render avec collecte des fichiers statiques
echo "=== Démarrage OptiTAB Backend ==="

# Répertoire du projet (backend)
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

# Créer les répertoires médias si manquants (Render persistent disk)
# Utiliser MEDIA_ROOT si défini (Render) sinon ./media
MEDIA_DIR=${MEDIA_ROOT:-media}
mkdir -p "$MEDIA_DIR/exercice_images"
mkdir -p "$MEDIA_DIR/cours_images"
mkdir -p "$MEDIA_DIR/quiz_images"

# Si MEDIA_DIR différent de ./media et que ./media contient des fichiers seed,
# copier tout fichier manquant (sans écraser ceux déjà présents)
if [ "$MEDIA_DIR" != "media" ] && [ -d "media" ]; then
  echo "Syncing seed media into $MEDIA_DIR (no overwrite)..."
  cp -rn media/* "$MEDIA_DIR" 2>/dev/null || true
  # Copier aussi récursivement l'intérieur des sous-dossiers si absents
  for sub in exercice_images cours_images quiz_images; do
    if [ -d "media/$sub" ]; then
      mkdir -p "$MEDIA_DIR/$sub"
      cp -rn media/$sub/* "$MEDIA_DIR/$sub" 2>/dev/null || true
    fi
  done
fi

# Collecte des fichiers statiques
if [ "${SKIP_COLLECTSTATIC:-0}" = "1" ]; then
  echo "Skipping collectstatic (SKIP_COLLECTSTATIC=1)"
else
  if [ -n "$(find staticfiles -type f -print -quit 2>/dev/null)" ]; then
    echo "Static files already present; skipping collectstatic."
  else
    echo "Collecting static files..."
    python manage.py collectstatic --noinput --clear
  fi
fi

# Run gunicorn with correct module path
echo "Starting Gunicorn..."
WORKERS=${GUNICORN_WORKERS:-${WEB_CONCURRENCY:-2}}
THREADS=${GUNICORN_THREADS:-2}
TIMEOUT=${GUNICORN_TIMEOUT:-120}
MAX_REQUESTS=${GUNICORN_MAX_REQUESTS:-1000}
MAX_REQUESTS_JITTER=${GUNICORN_MAX_REQUESTS_JITTER:-100}

# Vérifier que Django se charge correctement avant de lancer Gunicorn
echo "Checking Django configuration..."
python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendAPI.settings')
django.setup()
print('Django setup OK')
" || {
  echo "ERREUR: Django ne peut pas démarrer. Vérifier les variables d'environnement et la base de données."
  exit 1
}

echo "Gunicorn config: workers=$WORKERS threads=$THREADS timeout=$TIMEOUT"
exec gunicorn backendAPI.wsgi:application \
  --bind 0.0.0.0:${PORT:-10000} \
  --worker-class gthread \
  --workers "$WORKERS" \
  --threads "$THREADS" \
  --timeout "$TIMEOUT" \
  --max-requests "$MAX_REQUESTS" \
  --max-requests-jitter "$MAX_REQUESTS_JITTER" \
  --graceful-timeout 30 \
  --keep-alive 5 \
  --preload
