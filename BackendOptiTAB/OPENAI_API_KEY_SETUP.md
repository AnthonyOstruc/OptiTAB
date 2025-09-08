# 🔑 Configuration de la Clé API OpenAI

## 🚨 Problème Identifié

```
The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable
```

## ✅ Solution : Configuration de l'API Key

### **Méthode 1 : Fichier .env (Recommandée)**

#### **Étape 1 : Créer/Remplir le fichier .env**
```bash
cd BackendOptiTAB

# Créer le fichier .env avec votre clé
OPENAI_API_KEY=sk-proj-votre-cle-api-openai-ici
DEBUG=True
SECRET_KEY=votre-secret-django
```

#### **Étape 2 : Vérifier la clé**
```bash
# Afficher la clé (masquée pour la sécurité)
echo "Clé API configurée: ${OPENAI_API_KEY:0:20}..."
```

### **Méthode 2 : Variable d'Environnement Système**

#### **Windows (PowerShell)**
```powershell
$env:OPENAI_API_KEY = "sk-proj-votre-cle-api-openai-ici"
python manage.py runserver
```

#### **Windows (CMD)**
```cmd
set OPENAI_API_KEY=sk-proj-votre-cle-api-openai-ici
python manage.py runserver
```

#### **Linux/Mac**
```bash
export OPENAI_API_KEY=sk-proj-votre-cle-api-openai-ici
python manage.py runserver
```

## 🔍 Test de Configuration

### **Script de Test**
```bash
cd BackendOptiTAB
python test_openai_api_key.py
```

### **Test Manuel**
```python
# Dans Python :
import os
api_key = os.getenv('OPENAI_API_KEY')
print("API Key trouvée:", "Oui" if api_key else "Non")
print("Longueur:", len(api_key) if api_key else 0)
```

## 📋 Comment Obtenir une Clé API OpenAI

### **Étape 1 : Créer un Compte**
1. Allez sur https://platform.openai.com/
2. Cliquez sur "Sign up"
3. Vérifiez votre email

### **Étape 2 : Générer une Clé**
1. Allez dans **API Keys** (menu gauche)
2. Cliquez sur **"Create new secret key"**
3. **Copiez la clé** (⚠️ Elle ne sera visible qu'une fois !)

### **Étape 3 : Activer la Facturation**
1. Allez dans **Billing** → **Payment methods**
2. Ajoutez une carte de crédit
3. Déposez au moins 5$ pour activer l'API

## 💰 Coûts OpenAI

### **Prix par Modèle**
- **GPT-3.5-turbo** : ~0.002$/1K tokens
- **GPT-4** : ~0.03$/1K tokens

### **Estimation d'Usage**
- **Question simple** : 100-500 tokens (~0.0002-0.001$)
- **Réponse détaillée** : 500-2000 tokens (~0.001-0.004$)

## 🧪 Test Final

Après configuration :
```bash
cd BackendOptiTAB
python test_openai_version.py
```

**Résultat attendu :**
```
✅ OpenAI importé avec succès
📦 Version OpenAI: 1.3.0
✅ Nouvelle API détectée (v1.x)
✅ Client OpenAI créé avec succès
```

## 🚨 Dépannage

### **Erreur "Invalid API Key"**
- Vérifiez que la clé est correcte
- Vérifiez qu'elle n'est pas expirée
- Vérifiez la facturation

### **Erreur "Rate Limit"**
- Vous avez dépassé la limite gratuite
- Ajoutez des crédits à votre compte OpenAI

### **Erreur "Model Not Found"**
- Vérifiez que vous utilisez un modèle valide
- `gpt-3.5-turbo` ou `gpt-4`

## 🎯 Prochaines Étapes

1. **Configurer l'API Key** avec une des méthodes ci-dessus
2. **Tester la configuration** avec le script de test
3. **Lancer le serveur** Django
4. **Tester l'IA** dans l'interface

**Votre IA sera alors pleinement fonctionnelle !** 🚀🤖

---

**Rappel de sécurité :**
- 🔒 Ne partagez jamais votre clé API
- 🔒 Ne la commitez jamais dans Git
- 🔒 Utilisez toujours des variables d'environnement
