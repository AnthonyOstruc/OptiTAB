# 🔧 Guide de dépannage - OptiTAB sur Render

## Problèmes courants et solutions

### 1. Erreur "invalid runtime python3"

**Erreur :**
```
services[0].runtime
invalid runtime python3
```

**Solution :**
✅ **Corrigée automatiquement** - Le runtime doit être `python` au lieu de `python3`

```yaml
# ❌ Incorrect
runtime: python3

# ✅ Correct
runtime: python
```

### 2. Erreur de chemin dans les commandes

**Erreur :**
```
ModuleNotFoundError: No module named 'django'
```

**Solution :**
✅ **Corrigée automatiquement** - Ajouter `cd backend` avant les commandes

```yaml
# ❌ Incorrect
buildCommand: "pip install -r requirements.txt"

# ✅ Correct
buildCommand: "cd backend && pip install -r requirements.txt"
```

### 3. Erreur avec le serveur frontend

**Erreur :**
```
Command failed: npm run start
```

**Solution :**
✅ **Corrigée automatiquement** - Utiliser `serve` au lieu de `vite preview`

```json
{
  "scripts": {
    "start": "serve -s dist -l $PORT"
  },
  "dependencies": {
    "serve": "^14.2.1"
  }
}
```

### 4. Erreur de base de données

**Erreur :**
```
django.db.utils.OperationalError: could not connect to server
```

**Solutions :**
1. Vérifier que `DATABASE_URL` est correctement configurée
2. S'assurer que la base de données PostgreSQL est créée
3. Vérifier les permissions utilisateur

### 5. Erreur CORS

**Erreur :**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solutions :**
1. Vérifier `CORS_ALLOWED_ORIGINS` dans les variables d'environnement
2. S'assurer que l'URL du frontend est dans la liste des origines autorisées
3. Vérifier `VITE_API_BASE_URL` dans le frontend

### 6. Erreur de fichiers statiques

**Erreur :**
```
404 Not Found: /static/admin/css/base.css
```

**Solutions :**
1. Vérifier que `collectstatic` s'exécute correctement
2. S'assurer que `STATIC_ROOT` est configuré dans settings.py
3. Vérifier les permissions d'écriture

## 🔍 Diagnostic rapide

### Vérifier la configuration :
```bash
./validate-config.sh
```

### Vérifier les logs Render :
1. Aller dans le dashboard Render
2. Sélectionner le service
3. Onglet "Logs"
4. Chercher les erreurs

### Tester les endpoints :
```bash
# Health check
curl https://optitab-backend.onrender.com/api/health/

# API racine
curl https://optitab-backend.onrender.com/api/

# Frontend
curl https://optitab.net
```

## 🚀 Déploiement en production

### Étapes de déploiement :
1. **Préparation** :
   ```bash
   git add .
   git commit -m "fix: Corrections pour Render"
   git push origin main
   ```

2. **Sur Render** :
   - Créer un Blueprint avec votre repository
   - Attendre que Render détecte `render.yaml`
   - Configurer les variables d'environnement

3. **Configuration domaine** :
   - Ajouter `optitab.net` dans le service frontend
   - Configurer les DNS chez votre registrar

4. **Migration base de données** :
   ```bash
   # Via Render Shell
   python backend/manage.py migrate
   python backend/manage.py createsuperuser
   ```

## 📊 Variables d'environnement critiques

### Backend (optitab-backend) :
```env
SECRET_KEY=votre-secret-key-super-securisee
DEBUG=False
DATABASE_URL=postgresql://...
OPENAI_API_KEY=votre-cle-openai
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=mot-de-passe-app
GOOGLE_OAUTH_CLIENT_ID=votre-client-id
GOOGLE_OAUTH_CLIENT_SECRET=votre-client-secret
```

### Frontend (optitab-frontend) :
```env
NODE_ENV=production
VITE_API_BASE_URL=https://optitab-backend.onrender.com/api
```

## 💡 Conseils de performance

1. **Cache** : Activer le cache Redis si nécessaire
2. **CDN** : Utiliser Cloudflare pour les fichiers statiques
3. **Monitoring** : Configurer les alertes Render
4. **Logs** : Surveiller les erreurs régulièrement

## 📞 Support

Si vous rencontrez un problème non listé ici :
1. Vérifiez les logs détaillés
2. Testez localement avec `DEBUG=True`
3. Consultez la documentation Render
4. Ouvrez une issue sur GitHub

---

🎯 **Rappel** : La plupart des erreurs sont dues à des variables d'environnement manquantes ou incorrectes.
