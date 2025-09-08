#!/bin/bash

# Script de démarrage pour Render
echo "=== Démarrage de l'application OptiTAB ==="

# Vérifie si nous sommes dans le bon répertoire
if [ -d "backend" ]; then
    echo "Navigation vers le dossier backend..."
    cd backend
fi

# Vérifie que manage.py existe
if [ ! -f "manage.py" ]; then
    echo "Erreur: manage.py non trouvé!"
    exit 1
fi

# Collecte les fichiers statiques si nécessaire
echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear

# Applique les migrations de base de données
echo "Application des migrations..."
python manage.py migrate --noinput

# Démarre Gunicorn
echo "Démarrage de Gunicorn..."
exec gunicorn --config gunicorn.conf.py backendAPI.wsgi:application
