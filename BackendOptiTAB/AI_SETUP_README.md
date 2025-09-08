# Configuration de l'IA OptiTAB

## Prérequis

1. **Clé API OpenAI** : Vous devez avoir une clé API OpenAI valide
   - Allez sur https://platform.openai.com/api-keys
   - Créez une nouvelle clé API
   - Copiez la clé

## Configuration

### 1. Variables d'environnement

Ajoutez la variable suivante à votre fichier `.env` :

```env
OPENAI_API_KEY=votre-cle-api-openai-ici
```

### 2. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 3. Migration de la base de données

```bash
python manage.py makemigrations ai
python manage.py migrate
```

## Utilisation de l'API IA

### Endpoint principal

**POST** `/api/ai/ask/`

Headers:
```
Authorization: Bearer <votre-token-jwt>
Content-Type: application/json
```

Body:
```json
{
  "message": "Explique-moi comment résoudre cette équation",
  "matiere_contexte_id": 1,  // Optionnel - ID du contexte matière
  "chapitre_id": 2,          // Optionnel - ID du chapitre
  "model": "gpt-3.5-turbo"   // Optionnel - gpt-3.5-turbo ou gpt-4
}
```

### Historique des conversations

**GET** `/api/ai/history/`

Headers:
```
Authorization: Bearer <votre-token-jwt>
```

## Fonctionnement

1. **Recherche contextuelle** : L'IA recherche automatiquement les exercices et cours pertinents dans votre base de données
2. **Prompt intelligent** : Construit un prompt optimisé avec le contenu trouvé
3. **Réponse personnalisée** : ChatGPT répond en se basant sur vos données pédagogiques
4. **Sauvegarde** : Toutes les conversations sont sauvegardées pour l'historique

## Sécurité

- L'API nécessite une authentification JWT
- Les conversations sont liées à l'utilisateur connecté
- Les clés API sont stockées de manière sécurisée via les variables d'environnement

## Support des modèles

- **gpt-3.5-turbo** : Modèle par défaut, rapide et économique
- **gpt-4** : Modèle plus avancé pour des réponses plus précises (plus cher)
