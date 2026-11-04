# Format OptiTAB v1 — contenus structurés

Format de rédaction des cours, fiches, énoncés, étapes et solutions du site.
Le contenu décrit la **structure** (une définition, une étape, un tableau de
variations…) ; le site décide de l'**affichage**, identique partout et calqué
sur les livres OptiTAB (mêmes encadrés, même palette, tableaux tkz-tab).

- Rendu : `frontend/src/utils/optitabDoc.js` (module sans dépendance)
- Styles : `frontend/src/styles/optitab-doc.css`
- Un contenu sans marqueur garde l'ancien rendu : la migration se fait
  chapitre par chapitre, sans rien casser.

## 1. Marqueur

Tout contenu au nouveau format commence par la ligne :

```
<!-- optitab:1 -->
```

Le HTML est interdit dans le contenu (il est affiché tel quel), sauf `<br>`
pour un retour à la ligne dans une cellule de tableau.

## 2. Texte

| Écriture | Résultat |
|---|---|
| `**gras**`, `*italique*` | gras, italique (formules comprises) |
| `$x^2$` | formule en ligne |
| `$$ … $$` (seule sur sa ligne, ou sur plusieurs lignes) | formule centrée |
| ligne vide | nouveau paragraphe |
| `- élément` / `  - sous-élément` | liste à puces |
| `1. élément` | liste numérotée |
| `[IMAGE_1]` (seul sur sa ligne) | image n° 1 du contenu |

Typographie automatique : espace insécable avant `: ; ! ?`, ponctuation
collée aux formules (jamais de « ) » seul en début de ligne).

Chaîne de calculs : une égalité par ligne, alignée sur le signe.

```
$$
\begin{aligned}
f'(x) &= \frac{\cos(x)(1 + \sin(x)) - \sin(x)\cos(x)}{(1 + \sin(x))^2} \\
&= \frac{\cos(x)}{(1 + \sin(x))^2}
\end{aligned}
$$
```

Une formule trop large pour l'écran se réduit (jusqu'à 70 %), puis défile
horizontalement : elle n'est jamais coupée.

## 3. Titres

```
## I. Titre de partie        (cours, fiche : numéro en bleu + filet)
### Sous-partie
## Question 2 : énoncé       (corrigé : pastille numérotée)
```

Dans un corrigé, les étapes sont renumérotées à chaque `## Question`.

## 4. Encadrés

```
::: definition Fonction sinus
Contenu (texte, formules, listes, tableaux…)
:::
```

Le mot après `:::` donne le type ; le reste de la ligne est le titre
(facultatif). Les encadrés peuvent s'imbriquer (fermeture dans l'ordre).

| Type | Affichage | Usage |
|---|---|---|
| `definition` | fond bleu pâle, barre bleue | définitions |
| `theoreme` | cadre bleu | théorèmes |
| `propriete` | cadre bleu clair | propriétés |
| `notation` | cadre bleu clair | notations |
| `methode` | fond vert, barre verte (cours) ; ligne « MÉTHODE … » (corrigé) | savoir-faire |
| `exemple` | filet gris à gauche | exemples |
| `demonstration` | cadre gris, carré final | preuves |
| `attention` | fond orangé, barre orange | erreurs fréquentes |
| `remarque` | fond gris pâle | remarques |
| `conseil` | fond gris pâle, barre verte | conseils |
| `retenir` | cadre vert | à retenir |
| `rappel` | fond bleu pâle | rappels dans un corrigé |
| `formule` | formule centrée encadrée | formule clé |
| `resultat` | fond vert pâle « RÉSULTAT » | conclusion d'une question |
| `etape` | « ÉTAPE n » + titre, trait de guidage | étapes d'un corrigé (numérotées seules) |
| `point` | comme une étape, étiquette = titre | « Vérification », « Tableau de variations »… |
| `objectifs`, `prerequis` | cadre fin, coches | en-tête de chapitre |

## 5. Tableaux de données

```
| Angle | $\sin$ | $\cos$ |
|---|---|---|
| $0$ | $0$ | $1$ |
| $\dfrac{\pi}{6}$ | $\dfrac{1}{2}$ | $\dfrac{\sqrt{3}}{2}$ |
```

Style des livres (filets horizontaux, première colonne en bleu). Un tableau
trop large défile dans son cadre.

## 6. Tableaux de variations et de signes (syntaxe tkz-tab)

Même syntaxe que `\tkzTabLine` / `\tkzTabVar` dans les livres. Les valeurs et
libellés sont du LaTeX **sans** `$`.

```
::: tableau
x : 0, \frac{\pi}{2}, \frac{3\pi}{2}, 2\pi
f'(x) : , +, z, -, d, +,
f(x) : -/0, +/\frac{1}{2}, -D-/-\infty/-\infty, +/0
:::
```

- Première ligne : `x : x1, x2, …, xn` (n valeurs).
- Ligne de **signes** : 2n − 1 éléments (valeur, intervalle, valeur…) :
  `+`, `-`, `z` (zéro et pointillés), `d` (double barre), `t` (pointillés),
  `h` (zone hachurée : fonction non définie), vide. Un intervalle peut aussi
  contenir un mot (`convexe`, `concave`) ou une formule LaTeX.
- Ligne de **variations** : n éléments.
  - `+/v` valeur en haut, `-/v` valeur en bas, `=/v` valeur au milieu
    (valeur intermédiaire, par exemple une image remarquable) ;
  - `D+/v`, `D-/v` : double barre puis valeur (borne exclue à gauche) ;
  - `+D/v`, `-D/v` : valeur puis double barre ;
  - `+D-/v1/v2` (et `-D+`, `+D+`, `-D-`) : limite à gauche, double barre,
    limite à droite ;
  - `R` : pas de valeur, la flèche traverse.
- Les flèches sont tracées automatiquement d'une valeur à la suivante.
- Libellé de ligne : formule (`f'(x)`) ou texte avec formules
  (`Signe de $x+2$`, `Convexité`).
- Toutes les valeurs doivent être renseignées (limites comprises) : une case
  vide `+/` n'est admise que si la valeur est réellement inconnue de l'élève.

## 6 bis. Code

Bloc de code (coloration Python, étiquette « Python » ; `console` pour un
affichage de programme) :

````
```python
def u(n):
    return 2 * n + 1
```
````

Code en ligne : `` `range(10)` ``. Jamais de code dans une image.

## 7. Exercices

Le fichier d'exercices garde ses rubriques (`=== titre`, `Difficulté:`,
`Image:`, `Énoncé:`, `Étapes:`, `Solution:`) ; chaque rubrique de contenu
commence par le marqueur.

```
Énoncé:
<!-- optitab:1 -->
Calculer les valeurs exactes suivantes.

1. $\sin\left(\frac{\pi}{6}\right) + \cos\left(\frac{\pi}{3}\right)$
2. …

Étapes:
<!-- optitab:1 -->
## Question 1 : Calculer $\sin\left(\frac{\pi}{6}\right) + \cos\left(\frac{\pi}{3}\right)$

::: methode
Utilisation des valeurs remarquables
:::

::: etape Valeurs remarquables
- $\sin\left(\frac{\pi}{6}\right) = \frac{1}{2}$
- $\cos\left(\frac{\pi}{3}\right) = \frac{1}{2}$
:::

::: resultat
$$\sin\left(\frac{\pi}{6}\right) + \cos\left(\frac{\pi}{3}\right) = 1$$
:::

Solution:
<!-- optitab:1 -->
1. $\sin\left(\frac{\pi}{6}\right) + \cos\left(\frac{\pi}{3}\right) = 1$
```

## 8. Outils (`frontend/cours/format_v1/outils/`)

| Outil | Rôle |
|---|---|
| `exporter.py` (via `manage.py shell`) | export LECTURE SEULE d'une notion → `chantier/<niveau>/<id>_<slug>/source_en_ligne/` |
| `convertir_notion.py <dossier>` | conversion automatique d'une notion (cours, fiche, exercices) |
| `convertir_exercices.py src dst` | ancien format d'exercices → v1 |
| `convertir_cours.py src dst` | cours / fiche HTML → v1 |
| `planche.py <dossier>` | planches-contacts des images en ligne (relecture) |
| `figures_livre.py <dossier>` | figures style livre (`figures/figures.py`), contrôle des chevauchements texte/trait |
| `verifier_notion.py <dossier> [--navigateur]` | contrôle complet avant import (syntaxe, images, aperçu, Chrome) |
| `apercu_notion.mjs <dossier>` | page d'aperçu autonome (vrai moteur, vraies feuilles de style) |
| `controle_apercu.mjs page.html [captures/] [--rapide]` | contrôle Chrome téléphone + ordinateur |
| `valider_v1.py fichiers…` | contrôle de syntaxe du format |
| `importer_v1.py` (via `manage.py shell`) | mise en ligne d'une notion (sauvegarde, contrôle de concurrence, restauration) |

Méthode de travail par notion : `GUIDE_CHANTIER.md`.
