#!/bin/bash

# Script de vérification pré-déploiement OptiTAB
echo "🔍 Vérification de la configuration OptiTAB"

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher le statut
check_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

# Vérifications générales
echo ""
echo "📁 Structure du projet :"
[ -f "render.yaml" ] && check_status 0 "render.yaml présent" || check_status 1 "render.yaml manquant"
[ -f "README.md" ] && check_status 0 "README.md présent" || check_status 1 "README.md manquant"
[ -f ".gitignore" ] && check_status 0 ".gitignore présent" || check_status 1 ".gitignore manquant"

# Vérifications backend
echo ""
echo "🐍 Backend Django :"
if [ -d "backend" ]; then
    cd backend
    [ -f "requirements.txt" ] && check_status 0 "requirements.txt présent" || check_status 1 "requirements.txt manquant"
    [ -f "manage.py" ] && check_status 0 "manage.py présent" || check_status 1 "manage.py manquant"
    [ -f "gunicorn.conf.py" ] && check_status 0 "gunicorn.conf.py présent" || check_status 1 "gunicorn.conf.py manquant"
    [ -f "backendAPI/settings.py" ] && check_status 0 "settings.py présent" || check_status 1 "settings.py manquant"
    [ -f "env.example" ] && echo -e "${YELLOW}⚠️ env.example présent (à configurer)${NC}" || check_status 1 "env.example manquant"
    cd ..
else
    echo -e "${RED}❌ Dossier backend manquant${NC}"
fi

# Vérifications frontend
echo ""
echo "🎨 Frontend Vue.js :"
if [ -d "frontend" ]; then
    cd frontend
    [ -f "package.json" ] && check_status 0 "package.json présent" || check_status 1 "package.json manquant"
    [ -f "vite.config.js" ] && check_status 0 "vite.config.js présent" || check_status 1 "vite.config.js manquant"
    cd ..
else
    echo -e "${RED}❌ Dossier frontend manquant${NC}"
fi

echo ""
echo "📋 Checklist pré-déploiement :"
echo ""
echo "🔐 Variables d'environnement à configurer dans Render :"
echo "  Backend (optitab-backend) :"
echo "  - SECRET_KEY: votre clé secrète Django"
echo "  - OPENAI_API_KEY: votre clé OpenAI"
echo "  - EMAIL_HOST_USER: votre email"
echo "  - EMAIL_HOST_PASSWORD: mot de passe app"
echo "  - GOOGLE_OAUTH_CLIENT_ID: client ID Google"
echo "  - GOOGLE_OAUTH_CLIENT_SECRET: client secret Google"
echo ""
echo "  Frontend (optitab-frontend) :"
echo "  - NODE_ENV: production"
echo "  - VITE_API_BASE_URL: https://optitab-backend.onrender.com/api"
echo ""
echo "🌐 Configuration domaine :"
echo "  1. Ajouter optitab.net dans Render"
echo "  2. Configurer DNS chez votre registrar"
echo "  3. Attendre 24-48h pour propagation"
echo ""
echo "🚀 Commandes pour déployer :"
echo "  ./deploy.sh both    # Préparer les deux services"
echo "  git add . && git commit -m 'feat: Config Render' && git push"
echo "  # Puis créer Blueprint sur Render.com"
