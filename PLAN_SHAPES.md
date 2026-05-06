# Plan — Formes annotées dans le Reel Studio

Ajouter des cercles, carrés et flèches superposés sur les slides en plein écran, pour annoter les formules.

---

## Objectif

Permettre à l'utilisateur de dessiner des formes (cercle, carré, flèche) par-dessus la slide en plein écran, de les positionner, les redimensionner, changer leur couleur, et les sauvegarder avec la slide.

---

## Architecture retenue

Les formes sont stockées en JSON sur le champ `annotations` de chaque `ReelSlide` (nouveau champ backend). Le rendu se fait en SVG superposé sur la slide (z-index au-dessus du contenu, transparent aux clics quand en mode lecture).

---

## 1. Backend

### 1.1 Modèle

Fichier : `backend/reel_studio/models.py`

```python
# Ajouter dans ReelSlide
annotations = models.JSONField(blank=True, default=list)
# Format : [{ id, type, x, y, width, height, color, strokeWidth, ...extras }]
```

### 1.2 Migration

```bash
python manage.py makemigrations reel_studio
python manage.py migrate
```

### 1.3 Sérialiseur

Fichier : `backend/reel_studio/serializers.py`

- Ajouter `annotations` dans les champs du `ReelSlideSerializer`

---

## 2. Frontend — Composant `AnnotationLayer.vue`

Nouveau fichier : `src/components/admin/reel-studio/AnnotationLayer.vue`

Composant SVG superposé sur la slide (position absolute, inset 0, pointer-events none en mode lecture, auto en mode édition).

### Formes supportées

| Type | Props SVG | Extras |
|------|-----------|--------|
| `circle` | `cx cy r` | - |
| `rect` | `x y width height` | `rx` pour coins arrondis |
| `arrow` | `x1 y1 x2 y2` | `markerEnd` SVG arrow |

### Props du composant

```js
props: {
  annotations: Array,   // liste des formes
  editable: Boolean,    // true = plein écran, false = thumbnail/export
  width: Number,        // largeur de la slide (pour normaliser coords en %)
  height: Number,
}
emits: ['update']       // émet la liste mise à jour
```

### Structure d'une annotation

```json
{
  "id": "uuid",
  "type": "circle",     // "circle" | "rect" | "arrow"
  "x": 42.5,            // % de la largeur slide
  "y": 30.0,            // % de la hauteur slide
  "width": 12.0,        // % largeur (rect) ou rayon (circle) ou longueur (arrow)
  "height": 8.0,        // % hauteur (rect uniquement)
  "color": "#e74c3c",
  "strokeWidth": 2,
  "filled": false       // true = rempli, false = contour uniquement
}
```

Coordonnées en **pourcentage** pour que les formes restent proportionnelles quelle que soit la résolution d'export.

---

## 3. Frontend — Panneau d'outils dans le plein écran

Dans `ReelPreview.vue`, onglet KaTeX du panneau gauche (ou nouvel onglet "Formes").

### Outils à ajouter

```
[ Cercle ]  [ Carré ]  [ Flèche ]
Couleur : [5 pastilles]
Épaisseur : [ - 2px + ]
[ Supprimer sélection ]
[ Effacer tout ]
```

### Interaction

1. Clic sur un outil → active le mode dessin
2. Click-drag sur la slide → crée la forme
3. Clic sur une forme existante → la sélectionne (poignées de redimensionnement)
4. Drag sur la forme → déplace
5. Escape → désélectionne

---

## 4. Intégration dans `ReelPreview.vue`

- Monter `AnnotationLayer` par-dessus `ReelSlidePreview` dans le stage plein écran
- Passer `editable=true` seulement en plein écran
- À chaque `update` de l'annotation layer → `emit('update-slide', { id, patch: { annotations } })`
- En export PNG : monter l'annotation layer dans le `png-export-frame` avec `editable=false`

---

## 5. Intégration dans `ReelSlidePreview.vue`

- Ajouter `AnnotationLayer` en overlay (non éditable) pour afficher les formes sur les thumbnails et en export
- Passer les `annotations` depuis le `slide`

---

## 6. Sauvegarde

Utiliser le flux `update-slide` existant — `handlePatchSlide` dans `ReelStudioAdminPage.vue` envoie déjà un PATCH avec n'importe quel champ. Aucun changement côté admin page nécessaire, juste ajouter `annotations` au PATCH.

---

## Ordre d'implémentation recommandé

1. **Backend** — migration + sérialiseur (15 min)
2. **`AnnotationLayer.vue`** — rendu SVG lecture seule d'abord (affiche les formes) (1h)
3. **Ajouter l'overlay sur les thumbnails et en export** (30 min)
4. **Mode édition dans le plein écran** — dessin + sélection + drag (2h)
5. **Panneau d'outils dans le plein écran** — boutons + couleurs + épaisseur (1h)
6. **Suppression + effacement** (30 min)

---

## Points d'attention

- Les coordonnées en `%` garantissent un rendu correct en export 1080×1920 ou 1920×1080 (YouTube)
- Ajouter `pointer-events: none` sur l'overlay en mode thumbnail pour ne pas casser les clics de sélection de slide
- En export PNG, `html2canvas` rend le SVG — tester que les `marker` (têtes de flèche) sont bien capturés
- `strokeWidth` en `%` de la largeur ou en px fixe à choisir (recommandé : px fixe, scalé par `cqw` comme les formules)
