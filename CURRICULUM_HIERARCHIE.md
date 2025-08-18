## Hiérarchie du curriculum et logique de filtrage

Cette documentation décrit la hiérarchie des contenus (côté backend Django) et la façon dont le frontend (Vue) interroge l’API pour afficher des données filtrées par utilisateur.

### Modèles et relations

- **Pays** → contient des **Niveaux**
- **Matiere** (globale)
- **MatiereContexte** = Matiere + Niveau
  - Porte implicitement le Pays via le Niveau
  - Sert à « contextualiser » toute la suite du contenu
- **Theme** appartient à une Matiere et fait référence à un **MatiereContexte** (donc Niveau/Pays)
- **Notion** appartient à un Theme
- **Chapitre** appartient à une Notion
- **Exercice** appartient à un Chapitre

Vue d’ensemble: Pays → Niveau → (MatiereContexte) → Matiere → Theme → Notion → Chapitre → Exercice

### Règles de filtrage côté API

- Tous les ViewSets respectent `est_actif=True` pour l’affichage « utilisateur ».
- Admin (staff/superuser) voit les données sans filtrage strict sur `est_actif` lorsque pertinent.

- Themes
  - `GET /api/themes/pour-utilisateur/` filtre par le `niveau_pays` de l’utilisateur, sinon par son `pays`.
  - Option `?matiere=<id>` pour restreindre à une matière.

- Notions
  - `GET /api/notions/pour-utilisateur/` filtre via le contexte du thème (niveau → pays).
  - Options `?theme=<id>` ou `?matiere=<id>`.

- Chapitres
  - `GET /api/chapitres/?notion=<id>` renvoie les chapitres actifs d’une notion.

- Exercices
  - `GET /api/exercices/?chapitre=<id>` renvoie les exercices actifs d’un chapitre.

Notes:
- Le contexte (Pays/Niveau) est porté par `Theme.contexte` via `MatiereContexte`. Comme `Notion` → `Theme` et `Chapitre` → `Notion`, le contexte est implicite en cascade.

### Endpoints hiérarchiques utiles

- `GET /api/matieres/<id>/themes/`
- `GET /api/themes/<id>/notions/`
- `GET /api/notions/<id>/chapitres/`
- `GET /api/chapitres/<id>/exercices/`

### Flux frontend (pages principales)

- Thèmes d’une matière: `/themes/:matiereId`
- Notions d’un thème: `/theme-notions/:themeId`
- Chapitres d’une notion: `/chapitres/:notionId`
- Exercices d’un chapitre: `/exercices/:chapitreId`

Chaque page appelle l’API la plus spécifique possible:
- Thèmes: `themes.pour-utilisateur?matiere=<id>` (filtrage par user)
- Notions: `notions.pour-utilisateur?theme=<id>` (filtrage par user)
- Chapitres: `chapitres?notion=<id>`
- Exercices: `exercices?chapitre=<id>`

### Administration – création simple d’un exercice

Page: `/admin/exercices`

- Sélection « Chapitre » (liste des chapitres). Le chapitre porte déjà Matière/Thème/Niveau/Pays via sa Notion → Theme → Contexte.
- Saisie minimale: Titre, Énoncé (contenu), Solution (optionnel), Difficulté.
- Le payload mappé côté frontend respecte le modèle `Exercice`:
  - `chapitre`, `titre`, `contenu`, `difficulty` (+ alias `question`, `reponse_correcte`, `points`, `type` si utilisés)

### Exemples de requêtes

```bash
# Chapitres d’une notion
GET /api/chapitres/?notion=12

# Exercices d’un chapitre
GET /api/exercices/?chapitre=34

# Notions filtrées par utilisateur pour un thème
GET /api/notions/pour-utilisateur/?theme=7
```

### Bonnes pratiques

- Pour l’UX, toujours remonter du plus spécifique au plus général (ex.: `chapitreId` → exercices) pour éviter les gros chargements.
- Côté admin, créer les exercices à partir d’un chapitre garantit que le contexte est correct sans ressaisir Matière/Thème/Niveau/Pays.


