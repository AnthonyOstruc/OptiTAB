# 📝 Guide d'utilisation - Système de notation des Quiz

## Vue d'ensemble

Ce système permet aux élèves d'envoyer leurs quiz par WhatsApp et aux administrateurs de les noter directement depuis l'interface d'administration.

## Pour les administrateurs

### Accéder à l'interface de notation

1. Connectez-vous à l'interface admin
2. Accédez à l'URL: `http://localhost:3000/admin/quiz-submissions`
3. Ou ajoutez un lien dans le menu admin

### Fonctionnalités disponibles

#### 📊 Tableau de bord
- **Total**: Nombre total de soumissions
- **En attente**: Soumissions non encore notées
- **Notés**: Soumissions déjà corrigées

#### 🔍 Filtres
- Filtrer par statut (Tous / En attente / Notés)
- Bouton d'actualisation pour rafraîchir les données

#### ✏️ Noter un quiz

1. Cliquez sur le bouton **"Noter"** sur une soumission en attente
2. Dans la fenêtre qui s'ouvre:
   - **Note sur 20**: Saisissez la note (peut être décimale, ex: 15.5)
   - **Commentaire**: Ajoutez vos remarques et corrections (optionnel)
3. Cliquez sur **"Enregistrer"**

#### 📝 Modifier une note

Pour les quiz déjà notés:
1. Cliquez sur **"Modifier la note"**
2. Modifiez la note et/ou le commentaire
3. Enregistrez

### Workflow recommandé

1. **Réception par WhatsApp**: L'élève vous envoie son quiz
2. **Enregistrement**: (Pour l'instant manuel - voir section Développement futur)
3. **Correction**: Notez le quiz dans l'interface
4. **Notification**: L'élève voit sa note apparaître automatiquement

## Pour les élèves

### Accéder à ses notes

1. Connectez-vous à votre compte
2. Accédez à: `http://localhost:3000/mes-quiz-rendus`

### Informations affichées

#### 📊 Statistiques personnelles
- Nombre de quiz rendus
- Nombre en correction
- Nombre notés
- Moyenne générale (si au moins un quiz noté)

#### 📝 Détails de chaque quiz
- **Quiz en correction**: Statut "⏳ En correction"
- **Quiz noté**: 
  - Note obtenue (sur 20)
  - Commentaire du professeur
  - Date de correction

## API Backend

### Endpoints disponibles

#### Liste des soumissions
```
GET /api/suivis/quiz-submissions/
```
- Élèves: Voient uniquement leurs soumissions
- Admins: Voient toutes les soumissions
- Filtres: `?status=pending` ou `?status=graded`

#### Créer une soumission
```
POST /api/suivis/quiz-submissions/
{
  "quiz": 1,  // ID du quiz
  "notes_admin": "Reçu par WhatsApp le 11/12/2025"
}
```

#### Noter une soumission (admin seulement)
```
POST /api/suivis/quiz-submissions/{id}/grade/
{
  "note": 15.5,
  "commentaire": "Très bon travail, quelques petites erreurs à corriger"
}
```

#### Statistiques
```
GET /api/suivis/quiz-submissions/stats/
```

## Structure de la base de données

### Modèle QuizSubmission

| Champ | Type | Description |
|-------|------|-------------|
| user | ForeignKey | L'élève qui a soumis le quiz |
| quiz | ForeignKey | Le quiz concerné |
| status | CharField | 'pending' ou 'graded' |
| note | DecimalField | Note sur 20 (nullable) |
| commentaire | TextField | Commentaire de correction |
| corrige_par | ForeignKey | Admin qui a corrigé |
| date_correction | DateTimeField | Date de correction |
| notes_admin | TextField | Notes privées de l'admin |
| date_creation | DateTimeField | Date de soumission |

## Développement futur (Suggestions)

### Automatisation de la création de soumissions

Pour faciliter l'enregistrement des quiz reçus par WhatsApp, vous pourriez:

1. **Option 1: Formulaire rapide pour l'admin**
   - Créer une page où l'admin sélectionne:
     - L'élève (liste déroulante)
     - Le quiz concerné
     - Clic sur "Enregistrer la réception"

2. **Option 2: Import en masse**
   - CSV avec: email_élève, id_quiz
   - Bouton d'import dans l'interface admin

3. **Option 3: Intégration WhatsApp API** (avancé)
   - Webhook pour recevoir automatiquement les messages
   - Reconnaissance du quiz envoyé
   - Création automatique de la soumission

### Gestion des fichiers

Ajouter un champ pour uploader les photos du quiz:
- Stockage des images dans le media folder
- Visualisation dans l'interface de notation
- Permet de voir le quiz pendant la correction

### Notifications

Ajouter des notifications pour:
- L'élève quand son quiz est noté
- L'admin quand un nouveau quiz arrive
- Email automatique avec la note

## Fichiers créés/modifiés

### Backend
- `backend/suivis/models.py` - Modèle QuizSubmission
- `backend/suivis/serializers.py` - QuizSubmissionSerializer
- `backend/suivis/views.py` - QuizSubmissionViewSet
- `backend/suivis/urls.py` - Routes API
- `backend/suivis/admin.py` - Interface Django admin
- `backend/suivis/migrations/0004_quizsubmission.py` - Migration

### Frontend
- `frontend/src/api/quizSubmissions.js` - API client
- `frontend/src/views/admin/AdminQuizSubmissions.vue` - Interface admin
- `frontend/src/views/QuizSubmissionsStudent.vue` - Interface élève
- `frontend/src/router/index.js` - Routes ajoutées

## Support

Pour toute question ou amélioration, consultez ce guide ou contactez l'équipe de développement.

---

**Date de création**: 11 Décembre 2025
**Version**: 1.0

