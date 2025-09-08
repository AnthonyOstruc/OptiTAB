# 🔐 Guide de Dépannage Authentification IA

## 🚨 Problème : "Pas de token d'authentification"

### 📋 Diagnostic Rapide

#### **1. Vérifier la Connexion**
1. **Êtes-vous connecté ?** Regardez en haut à droite de l'écran
2. **Le bouton "Se connecter" est-il visible ?** Si oui → vous n'êtes pas connecté

#### **2. Vérifier le Token dans la Console**
1. Ouvrez la **console** (F12)
2. Tapez : `localStorage.getItem('access_token')`
3. Résultat attendu : Votre token JWT ou `null`

#### **3. Test de l'API**
```javascript
// Dans la console, testez l'endpoint historique :
fetch('/api/ai/history/', {
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
  }
})
.then(r => r.json())
.then(console.log)
```

### ✅ Solutions

#### **Solution A : Se Connecter**
1. Cliquez sur **"Se connecter"** en haut à droite
2. Entrez vos identifiants
3. Actualisez la page

#### **Solution B : Vérifier le Token**
```javascript
// Dans la console :
console.log('Token:', localStorage.getItem('access_token'))
console.log('Token length:', localStorage.getItem('access_token')?.length)
```

#### **Solution C : Forcer la Reconnexion**
```javascript
// Supprimer l'ancien token et se reconnecter :
localStorage.removeItem('access_token')
localStorage.removeItem('refresh_token')
// Puis actualisez la page
```

### 🔍 Logs Attendus

**Après connexion réussie :**
```
Token d'authentification: Présent
Historique chargé: []
Status HTTP: 200
```

### 💡 Conseils

- **Actualisez toujours** la page après connexion
- **Vérifiez la console** pour les erreurs d'authentification
- **Le token expire** automatiquement après un certain temps

### 🚨 Si le Problème Persiste

1. **Videz le cache** du navigateur (Ctrl+F5)
2. **Essayez un autre navigateur**
3. **Vérifiez la configuration** du backend (OPENAI_API_KEY)

**Une fois connecté, l'assistant IA fonctionnera parfaitement !** 🔐✨
