#!/bin/bash

# Script de démarrage pour Render avec collecte des fichiers statiques
echo "=== Démarrage OptiTAB Backend ==="

# Répertoire du projet (compatible exécution depuis n'importe où)
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

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
if [ "${SKIP_COLLECTSTATIC:-0}" = "1" ]; then
  echo "Skipping collectstatic (SKIP_COLLECTSTATIC=1)"
else
  if [ -n "$(find backend/staticfiles -type f -print -quit 2>/dev/null)" ]; then
    echo "Static files already present; skipping collectstatic."
  else
    echo "Collecting static files..."
    (cd backend && python manage.py collectstatic --noinput --clear)
  fi
fi

# Run gunicorn with correct module path
echo "Starting Gunicorn..."
WORKERS=${GUNICORN_WORKERS:-${WEB_CONCURRENCY:-1}}
THREADS=${GUNICORN_THREADS:-1}
TIMEOUT=${GUNICORN_TIMEOUT:-120}
MAX_REQUESTS=${GUNICORN_MAX_REQUESTS:-1000}
MAX_REQUESTS_JITTER=${GUNICORN_MAX_REQUESTS_JITTER:-100}

echo "Gunicorn config: workers=$WORKERS threads=$THREADS timeout=$TIMEOUT"
cd backend
exec gunicorn backendAPI.wsgi:application \
  --bind 0.0.0.0:${PORT:-10000} \
  --worker-class gthread \
  --workers "$WORKERS" \
  --threads "$THREADS" \
  --timeout "$TIMEOUT" \
  --max-requests "$MAX_REQUESTS" \
  --max-requests-jitter "$MAX_REQUESTS_JITTER"
