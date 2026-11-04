# Quiz pilote — Terminale 85 « Fonction exponentielle » (2026-11-03)

**État : prêt.** `src/data/quiz/85.json` et `public/quiz/85/` (19 PNG) sont écrits. Rien en base, aucun git.

## Contenu : 15 questions, 6 types, Découverte → Approfondissement
| # | Type | Niveau | Thème |
|---|---|---|---|
| q01 | vf | Découverte | Signe : $e^x=-2$ n'a pas de solution |
| q02 | qcm (4 courbes) | Découverte | Reconnaître la courbe de exp |
| q03 | saisie expression | Découverte | $(e^x)^3 e^{-x}=e^{2x}$ (piège `e^2x`) |
| q04 | qcm | Découverte | Tangente en 0 : $y=x+1$ |
| q05 | multi | Entraînement | Règles de calcul (6 égalités, 3 vraies) |
| q06 | vf | Entraînement | $e^{-2x+1}$ est décroissante |
| q07 | qcm | Entraînement | Dérivée de $e^{-3x+1}$ |
| q08 | saisie expression | Entraînement | Dérivée de $(x-1)e^x$ |
| q09 | saisie nombre | Entraînement | Équation $e^{2x-1}=e^{x+3}$ |
| q10 | ordre | Entraînement | Inéquation $e^{3x-2}<e^{x+4}$ |
| q11 | multi | Approfondissement | Limites et croissances comparées |
| q12 | associer (courbes) | Approfondissement | $e^{-x}$, $e^{-x^2}$, $e^{x^2}$, $xe^x$ |
| q13 | qcm | Approfondissement | Suite $e^{-0,5n}$ géométrique |
| q14 | saisie nombre exacte | Approfondissement | Maximum de $xe^{-x}$ : $1/e$ |
| q15 | saisie nombre (tolérance 0,005) | Approfondissement | Condensateur : $u(4)\approx4{,}32$ V |

Le logarithme n'est pas au cours de ce chapitre : aucune réponse en ln (valeur exacte en $e$, ou arrondie).

## Figures (19, `figures/figures.py`)
- 8 courbes « choix » (q02_a–d, q12_a–d) : même cadrage et même taille (226 × 214 et 226 × 204 px affichés), noms neutres.
- 3 figures d'énoncé sans la réponse (q04, q14, q15) ; 8 figures de correction en vert (q01, q02, q04, q06, q10, q13, q14, q15).
- Détecteur de chevauchements : 0 erreur, 0 avertissement. Chaque PNG regardé.

## Contrôles
- `verif_quiz.py` : 114 contrôles sympy justes, 0 erreur (bonnes réponses, distracteurs, clés, saisies, points des figures).
- `construire_quiz.py` : ✓ (toutes les `acceptees` / `refusees` bien jugées par quizMath.js).
- Rendu : moteur v1 et formules sans erreur ; parcours complet en téléphone (390 px) sur `/apercu/quiz/85`, aucune erreur console.

## Pour l'orchestrateur
1. **Défaut de `outils/construire_quiz.py`** : `RACINE = parents[3]` donne `frontend/`, donc il cherche `frontend/frontend/src/utils/quizMath.js` et échoue. Il faut `parents[4]`. Je ne l'ai pas modifié : je l'ai lancé avec un lanceur temporaire qui corrige seulement ce chemin.
2. **Saisies plausibles mal jugées par quizMath.js** (non modifié) :
   - `x.e^x` (point = multiplication, fréquent en France) : refusé, sans message clair (valeur NaN) ;
   - `x=4` : refusé avec le message « la réponse attendue est un nombre » (j'ai mis le placeholder « par exemple 2,5 » pour ne pas inviter à écrire `x=`) ;
   - `e^{2x}` (accolades) et `e⁻¹` (exposant Unicode) : « caractère inconnu » ;
   - `4,32 V` (unité tapée) : « symbole inconnu v ».
