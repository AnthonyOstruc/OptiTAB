# 🧪 Guide de Test - IA OptiTAB

## 🚀 Démarrage Rapide

### 1. Configuration
```bash
# Créer votre fichier .env avec votre clé API
cp CONFIG_ENV_EXAMPLE.txt .env
# Éditez .env et mettez votre clé OpenAI
```

### 2. Installation
```bash
cd BackendOptiTAB
python manage.py runserver
```

### 3. Frontend
```bash
cd websitecursor
npm run dev
```

## 🎯 Test de l'IA

### Via l'interface web
1. **Connectez-vous** à votre application
2. **Allez dans le dashboard** - vous verrez le bouton IA flottant (🤖) en bas à droite
3. **Cliquez sur le bouton IA** pour ouvrir l'assistant
4. **Posez une question** comme :
   - "Explique-moi les dérivées"
   - "Donne-moi des exercices sur les fonctions"
   - "Comment résoudre cette équation : 2x + 3 = 7"

### Via API directe (pour test)
```bash
curl -X POST http://localhost:8000/api/ai/ask/ \
  -H "Authorization: Bearer VOTRE_TOKEN_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explique-moi les mathématiques",
    "model": "gpt-3.5-turbo"
  }'
```

## 🔍 Fonctionnalités à Tester

### ✅ Recherche Contextuelle
- [ ] L'IA trouve-t-elle les exercices pertinents ?
- [ ] Intègre-t-elle les cours disponibles ?
- [ ] Les réponses sont-elles basées sur vos données ?

### ✅ Interface Utilisateur
- [ ] Le bouton flottant apparaît-il ?
- [ ] La modale s'ouvre-t-elle correctement ?
- [ ] L'historique des conversations fonctionne-t-il ?
- [ ] Les filtres par matière/chapitre marchent-ils ?

### ✅ Sécurité
- [ ] L'authentification JWT est-elle requise ?
- [ ] Les conversations sont-elles isolées par utilisateur ?

### ✅ Performance
- [ ] Les réponses sont-elles rapides ?
- [ ] L'interface reste-t-elle fluide ?

## 🐛 Dépannage

### Erreur "No module named 'openai'"
```bash
pip install openai==1.3.0
```

### Erreur "OPENAI_API_KEY non configurée"
- Vérifiez que votre `.env` existe
- Vérifiez que la clé API est correcte
- Redémarrez le serveur Django

### Erreur d'authentification
- Vérifiez que vous êtes connecté
- Vérifiez que votre token JWT est valide

### Le bouton IA n'apparaît pas
- Vérifiez que le composant est importé dans DashboardLayout.vue
- Vérifiez la console pour les erreurs JavaScript

## 📊 Test Automatisé

```bash
cd BackendOptiTAB
python test_ai_api.py
```

## 🎉 Prochaines Étapes

Une fois les tests réussis :

1. **Personnalisez les prompts** dans `ai/views.py`
2. **Ajoutez plus de contextes** (quiz, feuilles d'exercices)
3. **Intégrez l'IA** dans plus de pages
4. **Ajoutez des analytics** pour mesurer l'usage
5. **Optimisez les coûts** avec un système de cache

## 💡 Questions de Test Suggérées

- "Quels sont les prérequis pour étudier les intégrales ?"
- "Donne-moi un exercice sur les matrices"
- "Explique-moi la différence entre dérivée et primitive"
- "Comment résoudre un système d'équations à 2 inconnues ?"
- "Quels sont les théorèmes importants en géométrie ?"

---

**Prêt à tester ?** 🚀 Votre IA pédagogique est maintenant opérationnelle !
