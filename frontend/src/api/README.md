# Structure API Modulaire

Cette structure modulaire sépare les responsabilités et améliore la maintenabilité du code.

## Structure des fichiers

```
src/api/
├── client.js          # Configuration Axios et intercepteurs
├── auth.js            # Authentification uniquement
├── users.js           # Gestion des utilisateurs et profils
├── matieres.js        # CRUD des matières
├── notions.js         # CRUD des notions
├── chapitres.js       # CRUD des chapitres
├── exercices.js       # CRUD des exercices et statuts
├── fiches.js          # CRUD des fiches de synthèse
├── quiz.js            # CRUD des quiz
├── calculator.js      # Fonctions de calcul (dérivées, intégrales, etc.)
├── preferences.js     # Gestion des préférences utilisateur
├── index.js           # Export centralisé
└── README.md          # Cette documentation
```

## Avantages de cette structure

### 1. **Séparation des responsabilités**
- Chaque fichier a une responsabilité unique et claire
- Plus facile de localiser et modifier une fonctionnalité spécifique

### 2. **Maintenabilité améliorée**
- Code plus lisible et organisé
- Moins de conflits lors du développement en équipe
- Tests plus faciles à écrire

### 3. **Réutilisabilité**
- Import sélectif possible : `import { loginUser } from '@/api/auth'`
- Import centralisé : `import { loginUser, getMatieres } from '@/api'`

### 4. **Évolutivité**
- Ajout de nouvelles fonctionnalités sans affecter les autres
- Refactoring plus simple

## Utilisation

### Import centralisé (recommandé)
```javascript
import { 
  loginUser, 
  getMatieres, 
  createExercice,
  deriveExpr 
} from '@/api'
```

### Import spécifique (si nécessaire)
```javascript
import { loginUser } from '@/api/auth'
import { getMatieres } from '@/api/matieres'
import { deriveExpr } from '@/api/calculator'
```

## Migration depuis l'ancien système

Tous les imports `from '@/api/auth'` ont été automatiquement mis à jour vers `from '@/api'`.

## Ajout de nouvelles fonctions

1. Identifier le domaine fonctionnel approprié
2. Ajouter la fonction dans le fichier correspondant
3. L'export sera automatiquement disponible via `@/api`

### Exemple d'ajout
```javascript
// Dans calculator.js
export const solveEquation = (payload) => apiClient.post('/api/calc/solve/', payload)

// Utilisation
import { solveEquation } from '@/api'
```

## Configuration

Le fichier `client.js` contient :
- Configuration Axios
- Intercepteurs de requête (ajout automatique du token)
- Intercepteurs de réponse (gestion du refresh token)
- Gestion des erreurs d'authentification

## Bonnes pratiques

1. **Nommage** : Utiliser des noms explicites pour les fonctions
2. **Documentation** : Ajouter des commentaires JSDoc pour les fonctions complexes
3. **Gestion d'erreurs** : Laisser les intercepteurs gérer les erreurs communes
4. **Types** : Utiliser TypeScript si possible pour une meilleure sécurité de type 