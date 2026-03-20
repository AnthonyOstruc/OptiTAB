# Guide du Blog OptiTAB — Administration

## Architecture

Le blog fonctionne avec **3 entités** liées entre elles :

```
Catégorie (1) ──── contient ───→ (N) Articles
Tag (N) ←──── associé à ───→ (N) Articles
```

---

## 1. Catégories

**C'est quoi ?** Un dossier/thème principal pour regrouper les articles.  
Un article ne peut avoir **qu'une seule catégorie** (ou aucune).

**Exemples de catégories :**
- Méthodologie
- Mathématiques
- Orientation
- Conseils révisions
- Actualités OptiTAB

### Champs à remplir

| Champ | Obligatoire | Description |
|-------|:-----------:|-------------|
| **Nom** | ✅ | Nom affiché (ex: "Méthodologie") |
| **Slug** | ❌ | URL auto-générée depuis le nom (ex: "methodologie"). Laisser vide = auto. |
| **Description** | ❌ | Courte description de la catégorie (affiché sur la page catégorie du blog) |
| **Meta description** | ❌ | Description SEO (max 160 car.) utilisée par Google pour la page catégorie. Si vide, la description normale est utilisée. |
| **Meta robots** | ❌ | **Index** = visible Google (par défaut), **Noindex** = masqué de Google. Utile pour cacher les catégories avec peu d'articles. |
| **Ordre** | ❌ | Nombre pour trier l'affichage (0 = premier, 10 = après, etc.) |

---

## 2. Tags

**C'est quoi ?** Des étiquettes/mots-clés pour caractériser un article plus finement.  
Un article peut avoir **plusieurs tags** (ou aucun).

**Exemples de tags :**
- MPSI
- Terminale
- Algèbre
- Bac 2026
- Productivité
- Gratuit

### Champs à remplir

| Champ | Obligatoire | Description |
|-------|:-----------:|-------------|
| **Nom** | ✅ | Nom du tag (ex: "Algèbre") |
| **Slug** | ❌ | URL auto-générée. Laisser vide = auto. |
| **Meta description** | ❌ | Description SEO (max 160 car.) pour la page tag. Si vide, un texte par défaut est généré. |
| **Meta robots** | ❌ | **Index** = visible Google (par défaut), **Noindex** = masqué de Google. Utile pour cacher les tags avec peu d'articles. |

---

## 3. Articles

**C'est quoi ?** Le contenu principal du blog. Chaque article est une page avec un titre, du texte en Markdown, et optionnellement une catégorie + des tags.

### Champs à remplir

| Champ | Obligatoire | Description |
|-------|:-----------:|-------------|
| **Titre** | ✅ | Titre de l'article (ex: "5 astuces pour réussir sa prépa MPSI") |
| **Slug** | ❌ | URL de l'article. Auto-généré depuis le titre si vide. Ex: "5-astuces-reussir-prepa-mpsi" |
| **Extrait** | ❌ | Résumé court (max 400 car.) affiché dans la liste du blog et les cartes |
| **Catégorie** | ❌ | Sélectionner UNE catégorie dans la liste déroulante |
| **Statut** | ✅ | **Brouillon** = invisible au public, **Publié** = visible sur le blog |
| **Tags** | ❌ | Ajouter des tags via le sélecteur + bouton "+" |
| **Contenu** | ✅ | Corps de l'article écrit en **Markdown** (voir syntaxe ci-dessous) |
| **Image couverture** | ❌ | Upload d'image affichée en haut de l'article et dans les cartes |
| **Alt text image** | ❌ | Description textuelle de l'image pour l'accessibilité et le SEO (max 250 car.) |
| **SEO** | ❌ | Accordéon avec tous les champs SEO (voir section 5) |

### Statut : Brouillon vs Publié

- **Brouillon** : l'article est sauvegardé mais **invisible** sur le blog public. Utile pour rédiger en avance.
- **Publié** : l'article apparaît sur `/blog` et est indexable par Google. La date de publication est auto-remplie au premier passage en Publié.

### Bouton Prévisualiser

Avant de publier, cliquez sur **"Prévisualiser"** pour voir le rendu final de l'article (Markdown → HTML) directement dans l'admin.

---

## 4. Syntaxe Markdown pour le contenu

Le champ "Contenu" accepte du **Markdown**. Voici les éléments les plus utiles :

```markdown
## Titre de section (H2)
### Sous-section (H3)

Paragraphe normal. **Texte en gras**, *texte en italique*.

- Élément de liste
- Autre élément
  - Sous-élément

1. Liste numérotée
2. Deuxième point

> Citation ou remarque importante

[Texte du lien](https://example.com)

![Description de l'image](https://url-de-image.com/photo.jpg)

`code inline`

---  (ligne de séparation)
```

> **⚠️ Important** : ne PAS utiliser `# H1` dans le contenu. Le titre de l'article est déjà le seul H1 de la page. Commencez toujours par `## H2`.

### Formules mathématiques (LaTeX)

Si l'article contient des maths :

```markdown
Formule inline : $x^2 + y^2 = z^2$

Formule centrée :
$$\int_0^1 f(x)\,dx = F(1) - F(0)$$
```

---

## 5. Champs SEO (optionnel)

Ces champs sont dans l'accordéon **"SEO (optionnel)"** du formulaire article. Ils améliorent le référencement Google et l'aperçu sur les réseaux sociaux :

| Champ | Max | À quoi ça sert |
|-------|-----|----------------|
| **Titre SEO** | 70 car. | Titre affiché dans l'onglet Google (si différent du titre article) |
| **Meta description** | 160 car. | Description affichée sous le lien dans Google |
| **OG Title** | 100 car. | Titre affiché quand on partage sur Facebook/LinkedIn |
| **OG Description** | 200 car. | Description affichée quand on partage sur les réseaux |
| **Image OG** | — | Image dédiée pour les réseaux sociaux (si différente de l'image couverture). Format idéal : 1200×630 px. |
| **Meta robots** | — | **Index** (par défaut) = Google peut indexer. **Noindex** = masqué de Google. |

**Si laissés vides** :
- Le titre SEO = titre de l'article
- La meta description = l'extrait de l'article
- L'image OG = l'image de couverture
- Les brouillons sont **toujours en noindex** automatiquement, quel que soit le réglage

### Indexation et Google

| Situation | Indexable par Google ? |
|-----------|:----------------------:|
| Article **Publié** + Meta robots **Index** | ✅ Oui |
| Article **Publié** + Meta robots **Noindex** | ❌ Non |
| Article **Brouillon** (quel que soit le réglage) | ❌ Non (forcé noindex) |
| Catégorie avec Meta robots **Noindex** | ❌ Non |
| Tag avec Meta robots **Noindex** | ❌ Non |

---

## 6. Workflow recommandé

1. **Créer les catégories** d'abord (onglet Catégories) : Méthodologie, Maths, Orientation, etc.
   - Remplir la **description** et la **meta description** pour un bon SEO
   - Mettre en **Noindex** les catégories avec très peu d'articles
2. **Créer quelques tags** (onglet Tags) : MPSI, Terminale, Bac 2026, etc.
   - Mettre en **Noindex** les tags trop spécifiques ou avec peu d'articles
3. **Rédiger un article** (onglet Articles) :  
   - Remplir titre + contenu Markdown  
   - **Uploader une image de couverture** + remplir l'alt text
   - Choisir une catégorie + ajouter des tags  
   - Statut = **Brouillon**  
   - Ouvrir l'accordéon **SEO** et remplir titre SEO + meta description
   - Cliquer **Prévisualiser** pour vérifier le rendu  
   - Si OK → passer en **Publié** → cliquer **Créer**
4. L'article apparaît sur `/blog` du site
5. L'article est automatiquement ajouté au **sitemap XML** (sauf si noindex)

---

## 7. URLs publiques du blog

| Page | URL |
|------|-----|
| Liste des articles | `/blog` |
| Article individuel | `/blog/{slug-de-l-article}` |
| Articles d'une catégorie | `/blog/categorie/{slug-categorie}` |
| Articles d'un tag | `/blog/tag/{slug-tag}` |

---

## 8. Accès admin

- **URL admin blog** : `/admin/blog`
- **Onglet dans le header** : cliquer sur "📝 Blog" dans la barre admin
- **Bouton sidebar** : "Blog" dans la section Administration
- Seuls les **utilisateurs admin** (is_staff=True) peuvent accéder à cette page

---

## 9. SEO — Ce qui est automatique

Le blog gère automatiquement les éléments SEO suivants (pas besoin d'intervenir) :

| Élément | Détail |
|---------|--------|
| **Canonical URL** | Automatique sur chaque page (`/blog`, `/blog/{slug}`, `/blog/categorie/{slug}`, `/blog/tag/{slug}`) |
| **JSON-LD BlogPosting** | Données structurées schema.org sur chaque article (titre, description, image, dates, auteur) |
| **JSON-LD BreadcrumbList** | Fil d'Ariane structuré sur toutes les pages blog |
| **Open Graph** | Balises og:title, og:description, og:image, og:type automatiques |
| **Twitter Cards** | Balises twitter:card, twitter:title, twitter:description, twitter:image |
| **Meta robots** | Géré automatiquement : brouillons = noindex, publié = index (sauf si forcé noindex) |
| **Sitemap XML** | Auto-généré avec tous les articles publiés + indexables + catégories indexables |
| **Dates article:published_time / article:modified_time** | Injectées automatiquement dans les meta OG |
| **Sommaire (TOC)** | Généré automatiquement à partir des titres H2/H3 du contenu Markdown |
| **Temps de lecture** | Calculé automatiquement (nombre de mots / 200) |
| **Liens internes** | Section "Aller plus loin" en bas de chaque article vers cours, exercices, abonnements |
