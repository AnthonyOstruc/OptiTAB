# 🚀 OptiTAB - Déploiement sur Render

Guide complet pour déployer votre plateforme de tutorat OptiTAB sur Render avec le domaine optitab.net.

## 📋 Prérequis

- Compte GitHub avec vos repositories `frontend` et `backend`
- Compte Render (https://render.com)
- Domaine `optitab.net` acheté et configuré
- Clés API nécessaires (OpenAI, Google OAuth, etc.)

## 🏗️ Structure du projet

```
├── backend/          # Django API
├── frontend/         # Vue.js Application
├── render.yaml       # Configuration Render
└── README.md         # Ce fichier
```

## 🚀 Déploiement rapide

### 1. Préparation des repositories

Assurez-vous que vos repositories GitHub sont à jour :

```bash
# Repository backend
cd backend
git add .
git commit -m "feat: Configuration déploiement Render"
git push origin main

# Repository frontend
cd ../frontend
git add .
git commit -m "feat: Configuration déploiement Render"
git push origin main
```

### 2. Déploiement sur Render

1. **Connectez-vous à Render** : https://render.com
2. **Créez un Blueprint** :
   - Cliquez sur "New" → "Blueprint"
   - Connectez votre repository principal (celui contenant render.yaml)
   - Render détectera automatiquement la configuration

### 3. Configuration des services

Render créera automatiquement :
- **optitab-backend** : Service web Python pour Django
- **optitab-frontend** : Service web Node.js pour Vue.js
- **optitab-db** : Base de données PostgreSQL

### 4. Variables d'environnement

Configurez ces variables dans chaque service Render :

#### Backend (optitab-backend) :
```env
SECRET_KEY=votre-secret-key-super-securisee
DEBUG=False
OPENAI_API_KEY=votre-cle-openai
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=mot-de-passe-app
GOOGLE_OAUTH_CLIENT_ID=votre-client-id
GOOGLE_OAUTH_CLIENT_SECRET=votre-client-secret
```

#### Frontend (optitab-frontend) :
```env
NODE_ENV=production
VITE_API_BASE_URL=https://optitab-backend.onrender.com/api
```

## 🌐 Configuration du domaine

### 1. Dans Render
- Allez dans votre service frontend (optitab-frontend)
- Onglet "Settings" → "Custom Domain"
- Ajoutez `optitab.net` et `www.optitab.net`

### 2. Chez votre registrar
Configurez les DNS pour pointer vers Render :
```
Type: CNAME
Name: @
Value: votre-app.onrender.com

Type: CNAME
Name: www
Value: votre-app.onrender.com
```

## 🔧 Migration de base de données

Après le premier déploiement :

```bash
# Via Render Shell ou commande
python backend/manage.py migrate
python backend/manage.py createsuperuser
```

## ✅ Vérifications post-déploiement

1. **Health Check** : `https://optitab-backend.onrender.com/api/health/`
2. **Frontend** : `https://optitab.net`
3. **API** : `https://optitab-backend.onrender.com/api/`
4. **Admin** : `https://optitab-backend.onrender.com/admin/`

## 🔒 Sécurité

- ✅ HTTPS forcé en production
- ✅ Headers de sécurité configurés
- ✅ Variables d'environnement chiffrées
- ✅ CORS configuré pour votre domaine
- ✅ Base de données avec SSL

## 🚨 Dépannage

### Problèmes courants :

1. **Erreur 500** : Vérifiez les logs du backend
2. **API non accessible** : Vérifiez `VITE_API_BASE_URL` dans le frontend
3. **Base de données** : Vérifiez la variable `DATABASE_URL`
4. **Domaines** : Vérifiez la propagation DNS (peut prendre 24-48h)

### Logs utiles :
- **Backend** : Render Dashboard → optitab-backend → Logs
- **Frontend** : Render Dashboard → optitab-frontend → Logs
- **Base de données** : Render Dashboard → optitab-db → Logs

## 📞 Support

Si vous rencontrez des problèmes :
1. Vérifiez les logs Render
2. Testez localement avec `DEBUG=True`
3. Consultez la documentation Render : https://docs.render.com

---

🎉 **Félicitations !** Votre plateforme OptiTAB est maintenant en ligne sur https://optitab.net
