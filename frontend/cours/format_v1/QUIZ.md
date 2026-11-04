# Quiz d'un chapitre (onglet « Quiz ») — format et méthode

Demande du propriétaire (2026-11-03) : en plus des exercices, des quiz de
plusieurs types, « simples, propres, impeccables, automatiques », avec des
schémas, pour donner envie d'apprendre. Pilote : Terminale 85 « Fonction
exponentielle ». Rien en base : le quiz est un fichier du site.

## Fichiers
```
chantier/<niveau>/<id>_<slug>/quiz/
  quiz.py                  QUIZ = {...}  (source, chaînes LaTeX en r"…")
  figures/figures.py       FIGURES = {...}  (même style que les figures du chapitre)
  figures/images/*.png     produit par : python outils/figures_livre.py <dossier>/quiz
  verif_quiz.py            vérifications sympy de chaque réponse
```
Construction (contrôle + publication dans le front) :
`python outils/construire_quiz.py <dossier_notion>` → `frontend/src/data/quiz/<id>.json`
et `frontend/public/quiz/<id>/*.png`. L'onglet Quiz apparaît seul dès que le
fichier JSON existe (en ligne après un déploiement du front).

## Structure
```python
QUIZ = {
  "notion": 85,
  "titre": "Fonction exponentielle",
  "intro": "12 questions pour vérifier que tu maîtrises le chapitre.",   # une phrase
  "duree": 10,                                                            # minutes, indicatif
  "parties": ["Rappels de Première", "Limites", ...],   # parties du cours, dans l'ordre du cours
  "questions": [ {...}, ... ],
}
```
Champs communs à toutes les questions :

| Champ | Rôle |
|---|---|
| `id` | court et unique (`q01`…) |
| `type` | `qcm`, `multi`, `vf`, `saisie`, `associer`, `ordre` |
| `niveau` | `Découverte`, `Entraînement`, `Approfondissement` |
| `theme` | petite étiquette (« Propriétés algébriques », « Lecture graphique »…) |
| `partie` | partie du cours (une des `parties`) : sert au bilan de fin « Acquis / En cours / À revoir ». Chaque partie du cours doit avoir au moins une question (contrôlé). |
| `enonce` | texte OptiTAB v1 (formules `$…$`, `**gras**`, listes, encadrés) — court |
| `figure` | facultatif : nom d'une figure d'énoncé (ne donne pas la réponse) |
| `explication` | correction affichée après la réponse, texte OptiTAB v1 : méthode en 1 phrase, étapes courtes, résultat encadré (`::: resultat`), `::: attention Erreur fréquente` si utile. Courte : on est dans un quiz, pas un corrigé d'exercice. |
| `figure_corrige` | facultatif : figure de la correction, complétée en vert |

Champs propres à chaque type :

| Type | Champs |
|---|---|
| `qcm` | `choix` (textes) **ou** `choix_figures` (noms de figures, ex. 4 courbes) ; `bonne` = indice |
| `multi` | `choix` ; `bonnes` = liste d'indices (l'élève coche tout ce qui est juste) |
| `vf` | `reponse` = `True` / `False` (l'énoncé est une affirmation) |
| `saisie` | `nature` = `nombre` ou `expression` ; `reponses` = réponses justes écrites comme sur une calculatrice (`ln(2)/3`, `2*exp(2*x)`) ; `tolerance` (nombre : `0.01` accepte un arrondi au centième ; absent = valeur exacte) ; `intervalle` (expression : intervalle de test, défaut `[0.3, 2.7]`) ; `variable` (défaut `x`) ; `placeholder` (exemple d'écriture) ; `unite` (affichée après la case) ; **`acceptees`** et **`refusees`** = exemples de saisies d'élèves, vérifiés automatiquement par le vrai correcteur du site |
| `associer` | `gauche` (textes) et `droite` (textes) ou `droite_figures` : `gauche[i]` va avec `droite[i]` (le site mélange) |
| `ordre` | `etapes` dans le bon ordre (le site mélange) ; 3 à 6 étapes |

Les choix, étapes et réponses sont mélangés à chaque passage : ne jamais écrire
« la réponse A » dans une explication.

## Correcteur des réponses écrites (`src/utils/quizMath.js`)
Comprend : virgule ou point décimal, `×` `*` `÷` `/` `^` `²`, `−`, multiplication
implicite (`2x`, `3e^x`, `2(x+1)`, `xe^x`), `e`, `pi`/`π`, `exp( )`, `ln( )`,
`sqrt( )`/`√`, `sin cos tan abs`. Un nombre est juste s'il a la même valeur (exacte
ou à la tolérance près) ; une expression est juste si elle prend les mêmes valeurs
en 7 points de l'intervalle : toutes les formes équivalentes sont acceptées
(`xe^x+e^x` = `(x+1)e^x`). L'élève voit en direct l'écriture mathématique de sa
saisie. Attention : `e^2x` se lit `e²·x` (l'aperçu le montre) — prévoir ce cas dans
`refusees` quand il est piégeant.

## Règles de qualité (consignes du propriétaire)
- 12 à 15 questions, tous les types représentés, progression Découverte →
  Approfondissement, tout le programme officiel du chapitre couvert.
- Questions courtes, une seule idée ; distracteurs = vraies erreurs d'élèves.
- Figures au style des livres (`figures_livre.py`), lisibles sur téléphone, jamais
  de texte sur un trait ; figure d'énoncé sans la réponse, figure de correction
  complétée en vert.
- Chaque réponse vérifiée avec sympy (`verif_quiz.py`).
- `construire_quiz.py` doit afficher ✓ ; regarder le rendu sur téléphone
  (aperçu sans connexion en local : `/apercu/quiz/<id>`, serveur `npx vite` lancé) :
  `node outils/captures_quiz.mjs <id> <dossier>` joue tout le quiz (une réponse juste
  sur deux), photographie chaque écran à 390 px et signale débordement, erreur
  MathJax, formule non composée, erreur console (`--large` : ordinateur).

## Interface (site)
`src/components/espace/ChapitreQuiz.vue` (accueil, déroulé, barre de progression,
série de bonnes réponses, résultat, « Refaire mes erreurs », meilleur score gardé
sur l'appareil), `QuizQuestion.vue` (les 6 types, correction immédiate, aperçu de la
saisie, touches x, e^, ln, √…), `QuizFigure.vue`, `src/utils/quizMath.js`
(correcteur), `src/data/quiz/` (contenus + `index.js`). Onglet ajouté dans
`views/espace/EspaceChapitre.vue` seulement si le fichier du chapitre existe.

## Fait
- 2026-11-03 : pilote Terminale 85 « Fonction exponentielle » — 16 questions,
  6 types, 19 figures, 119 vérifications sympy ; bouton « Je ne sais pas » (affiche
  la correction, compte comme à revoir) ; fin : note sur 20 + bilan par partie du
  cours + détail des questions. En local, à valider par le propriétaire (en ligne
  après déploiement du front).
