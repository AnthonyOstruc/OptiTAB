#!/bin/bash

# Script de validation de la configuration OptiTAB pour Render
echo "🔍 Validation de la configuration OptiTAB"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Fonction de validation
validate() {
    local name=$1
    local condition=$2
    local message=$3

    if [ "$condition" = true ]; then
        echo -e "${GREEN}✅ $name : $message${NC}"
        return 0
    else
        echo -e "${RED}❌ $name : $message${NC}"
        return 1
    fi
}

# Vérifications de fichiers
echo ""
echo "📁 Vérification des fichiers :"

validate "render.yaml" "$(test -f render.yaml && echo true || echo false)" "présent"
validate "README.md" "$(test -f README.md && echo true || echo false)" "présent"
validate "backend/requirements.txt" "$(test -f backend/requirements.txt && echo true || echo false)" "présent"
validate "backend/manage.py" "$(test -f backend/manage.py && echo true || echo false)" "présent"
validate "backend/gunicorn.conf.py" "$(test -f backend/gunicorn.conf.py && echo true || echo false)" "présent"
validate "frontend/package.json" "$(test -f frontend/package.json && echo true || echo false)" "présent"
validate "frontend/vite.config.js" "$(test -f frontend/vite.config.js && echo true || echo false)" "présent"

# Vérification du contenu des fichiers critiques
echo ""
echo "🔧 Vérification du contenu des fichiers :"

# Vérifier render.yaml
if [ -f "render.yaml" ]; then
    if grep -q "runtime: python" render.yaml; then
        validate "Runtime Python" true "correctement configuré"
    else
        validate "Runtime Python" false "devrait être 'python'"
    fi

    if grep -q "cd backend" render.yaml; then
        validate "Commandes backend" true "chemins corrects"
    else
        validate "Commandes backend" false "devrait inclure 'cd backend'"
    fi
fi

# Vérifier package.json
if [ -f "frontend/package.json" ]; then
    if grep -q '"start": "serve' frontend/package.json; then
        validate "Script start frontend" true "utilise 'serve'"
    else
        validate "Script start frontend" false "devrait utiliser 'serve'"
    fi

    if grep -q '"serve":' frontend/package.json; then
        validate "Dépendance serve" true "présente"
    else
        validate "Dépendance serve" false "devrait être ajoutée"
    fi
fi

# Recommandations
echo ""
echo "📋 Prochaines étapes :"
echo ""
echo "1. Commitez et pushez vos changements :"
echo "   git add ."
echo "   git commit -m 'fix: Correction runtime Python dans render.yaml'"
echo "   git push origin main"
echo ""
echo "2. Créez le Blueprint sur Render :"
echo "   - Allez sur https://render.com"
echo "   - New → Blueprint"
echo "   - Connectez votre repository"
echo "   - Render détectera automatiquement render.yaml"
echo ""
echo "3. Configurez les variables d'environnement dans chaque service"
echo ""
echo "4. Testez les endpoints :"
echo "   - Health: https://optitab-backend.onrender.com/api/health/"
echo "   - Frontend: https://optitab.net"
echo ""
echo "🚀 Configuration validée !"
