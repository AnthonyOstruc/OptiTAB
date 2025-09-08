#!/bin/bash

# Script de déploiement OptiTAB sur Render
# Usage: ./deploy.sh [backend|frontend|both]

set -e

echo "🚀 Déploiement OptiTAB sur Render"

# Fonction pour déployer le backend
deploy_backend() {
    echo "📦 Déploiement du backend Django..."

    cd backend

    # Vérification des dépendances
    if [ ! -f "requirements.txt" ]; then
        echo "❌ Fichier requirements.txt manquant"
        exit 1
    fi

    # Installation des dépendances
    echo "📦 Installation des dépendances..."
    pip install -r requirements.txt

    # Collecte des fichiers statiques
    echo "📂 Collecte des fichiers statiques..."
    python manage.py collectstatic --noinput --clear

    # Test des migrations
    echo "🗄️ Vérification des migrations..."
    python manage.py check

    cd ..
    echo "✅ Backend prêt pour le déploiement"
}

# Fonction pour déployer le frontend
deploy_frontend() {
    echo "🎨 Déploiement du frontend Vue.js..."

    cd frontend

    # Vérification des dépendances
    if [ ! -f "package.json" ]; then
        echo "❌ Fichier package.json manquant"
        exit 1
    fi

    # Installation des dépendances
    echo "📦 Installation des dépendances..."
    npm install

    # Build de production
    echo "🔨 Build de production..."
    npm run build

    # Vérification du build
    if [ ! -d "dist" ]; then
        echo "❌ Dossier dist non créé"
        exit 1
    fi

    cd ..
    echo "✅ Frontend prêt pour le déploiement"
}

# Fonction pour vérifier la configuration
check_config() {
    echo "🔍 Vérification de la configuration..."

    # Vérification render.yaml
    if [ ! -f "render.yaml" ]; then
        echo "❌ Fichier render.yaml manquant"
        exit 1
    fi

    # Vérification des variables d'environnement
    if [ ! -f "backend/env.example" ]; then
        echo "⚠️ Fichier env.example manquant (documentation des variables)"
    fi

    echo "✅ Configuration vérifiée"
}

# Fonction principale
main() {
    local target=${1:-both}

    check_config

    case $target in
        backend)
            deploy_backend
            ;;
        frontend)
            deploy_frontend
            ;;
        both)
            deploy_backend
            deploy_frontend
            ;;
        *)
            echo "❌ Usage: $0 [backend|frontend|both]"
            exit 1
            ;;
    esac

    echo ""
    echo "🎉 Préparation terminée !"
    echo ""
    echo "📋 Prochaines étapes :"
    echo "1. Commitez et pushez vos changements :"
    echo "   git add ."
    echo "   git commit -m 'feat: Configuration déploiement Render'"
    echo "   git push origin main"
    echo ""
    echo "2. Allez sur https://render.com"
    echo "3. Créez un nouveau Blueprint avec votre repository"
    echo "4. Configurez les variables d'environnement"
    echo "5. Déployez !"
    echo ""
    echo "📖 Consultez README.md pour les détails complets"
}

# Exécution du script
main "$@"
