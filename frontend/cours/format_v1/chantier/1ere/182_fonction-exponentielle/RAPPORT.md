# Rapport — notion 182 « Fonction exponentielle » (Première spécialité)

**État : prêt.** Le cours, la fiche et les 15 exercices (13 existants, tous réécrits, et 2 ajoutés) sont au format OptiTAB v1. Les 28 figures sont neuves, au style des livres ; aucune image en ligne n’est conservée. Les titres du cours et de la fiche reprennent l’intitulé du programme : « Fonction exponentielle ».

## Programme (2019, Première spécialité, partie « Fonction exponentielle »)

Couvert et vérifié :
- définition par $f' = f$ et $f(0) = 1$, existence et unicité admises ; nombre $e = \exp(1)$ ;
- $\exp(x)\exp(-x) = 1$ et non-annulation (démonstration) ; relation fonctionnelle (démonstration) ; $\exp(-a)$, $\exp(a - b)$, $\exp(na)$ ; notation $e^x$ ;
- signe (démonstration par $e^x = (e^{x/2})^2$), dérivée, variations, courbe, tangente $y = x + 1$ en $0$, approximation $e^h \approx 1 + h$ ;
- $e^a = e^b \iff a = b$, $e^a < e^b \iff a < b$, produits $A(x)e^{\ldots}$ ;
- fonctions $t \mapsto e^{kt}$ et $t \mapsto e^{-kt}$ ($k > 0$) : dérivée, variations, représentation, symétrie ;
- suites $(e^{na})$ géométriques ; modélisation d’une croissance / décroissance exponentielle (bactéries, radioactivité, médicament), taux $e^k - 1$ ;
- algorithmique : méthode d’Euler et approximation de $e$ par $(1 + 1/n)^n$, seuils par boucle `while`.

**Retiré (hors programme de Première, relève de la Terminale)** :
- toutes les limites (1290 Q1–Q3, 1298, 1294 Q4, 1292 Q6, 1301 Q5, 1295 Q4, 1296 Q4), dont $\lim (e^x - 1)/x$ ;
- les croissances comparées (1298, 1296) ;
- le logarithme (1293 Q2, Q3, Q5 ; 1297 Q1, Q3 ; tout l’exercice 1299 ; 1292 ; 1300 Q3, Q5) ;
- la dérivée de $e^{u(x)}$ pour $u$ non affine ($e^{x^2}$ dans 1291, $e^{-x^2}$ dans 1301, $e^{x^2 - 2x}$ dans 1295) et la convexité / dérivée seconde (1301).

Les seuils qui demandaient un logarithme sont désormais traités par un programme Python ou un tableau de valeurs, comme le prévoit le programme.

## Texte

- **Cours réécrit de zéro** (7 parties, objectifs, prérequis) : définition ; méthode d’Euler et approximation de $e$ (code `euler`) ; relation fonctionnelle et notation $e^x$ (avec démonstration, tableau des règles, erreurs fréquentes, suite $(e^{na})$) ; signe, variations (tableau natif), tangente en $0$ ; équations et inéquations ; fonctions $e^{kt}$ / $e^{-kt}$ et étude complète de $(2x - 1)e^x$ sur $[-2\,;\,1]$ ; modélisation (décroissance radioactive, programme de seuil) ; « L’essentiel ».
- **Fiche réécrite** : définition, règles, signe et variations, équations, dérivation et modélisation, Euler, 5 erreurs classiques, 2 figures.
- **Exercices** : les 13 exercices existants sont **remplacés dans leur bloc** (Id conservés, titres adaptés au nouveau contenu, même type en tête) ; chacun suit le modèle du pilote (méthode, étapes, résultat encadré, erreur fréquente) :
  - 1291 Dériver des fonctions exponentielles ($e^{x^2}$ remplacée par $(x + 1)e^x$) ;
  - 1290 Signe, variations et tangente en 0 (au lieu de limites) ;
  - 1289 Propriétés algébriques (ajout d’une identité $(e^x + e^{-x})^2 - (e^x - e^{-x})^2 = 4$) ;
  - 1293 Équations et inéquations (sans logarithme ; erreur de conversion « $-x -4$ » supprimée) ;
  - 1298 Comparer l’exponentielle et sa tangente : étude de $e^x - x$, inégalité $e^x \geqslant x + 1$, encadrement de $e^{0{,}1}$ ;
  - 1294 Étude de $xe^x$ (minimum, signe, tangente, position courbe/tangente) ;
  - 1297 Équations et inéquations avancées (changement de variable $X = e^x$ avec racines $1$ et $e$, condition $X > 0$) ;
  - 1299 Suites géométriques $(e^{-0{,}5n})$ et $(3e^{2n+1})$, somme, seuil Python (au lieu d’équations logarithmiques) ;
  - 1292 Étude complète de $(x^2 - 3)e^x$ sur $[-5\,;\,2]$ ;
  - 1301 Méthode d’Euler et approximation de $e$ (au lieu de la convexité) ;
  - 1295 Fonctions $e^{kt}$ et $e^{-kt}$ : associer quatre courbes (au lieu de $e^{x^2 - 2x}$) ;
  - 1300 Croissance de bactéries : seuils par programme Python (au lieu de $\ln$) ;
  - 1296 Optimisation : concentration $4te^{-0{,}5t}$ sur $[0\,;\,10]$, durée d’efficacité.
- **Exercices ajoutés** :
  - `nouveau-1` « Entraînement - Modélisation d'une décroissance radioactive » ($e^{-kt}$, taux $e^k - 1$, $A(t + 5) = e^{-1}A(t)$, seuils Python) ;
  - `nouveau-2` « Problème - Démontrer les propriétés de l'exponentielle » (non-annulation, relation fonctionnelle, signe, variations, à partir de la seule définition).
- **Erreurs de l’ancienne version** : solutions en $\ln$ hors programme, une inéquation tronquée par la conversion (« $-x -4$ » dans 1293), des corrigés de limites sans justification, des solutions courtes cassées (« $g'(x) 0$ pour $x > -1$ », « $0 \leq x 0$ »).
- **Vérification** : `verif_exponentielle.py` (sympy) fait **183 contrôles, 0 erreur** (`verif_log.txt`) : chaque dérivée, factorisation, équation, ensemble de solutions, valeur exacte et arrondi, tableau de variations, programme de seuil (rejoué) et valeur placée sur les figures. Le script a détecté 5 arrondis faux dans ma première rédaction, tous corrigés : $e^{0{,}1} \approx 1{,}105$, la somme $S \approx 2{,}524$, $v_5 \approx 179\,622$, $v_6 \approx 1\,327\,240$ et $C(0{,}8) \approx 2{,}15$.

## Figures

- **28 figures neuves** (`figures/figures.py`), 0 image en ligne conservée ; les 13 anciennes images (style matplotlib, contenu hors programme) ne sont plus appelées et seront supprimées à l’import.
- **Cours (5)** : méthode d’Euler, courbe et tangente en 0, quatre courbes $e^{\pm kt}$, étude de $(2x - 1)e^x$, modèle radioactif avec seuil. **Fiche (2)** : figures du cours réutilisées.
- **Exercices (23)** : figure dans l’énoncé et figure complétée en vert dans le corrigé pour 1290, 1298 (+ courbe au-dessus de la tangente), 1294, 1299, 1292, 1301, 1295, 1300, 1296, nouveau-1 ; figure de corrigé pour 1293 ($e^x = -3$) et 1297 (signe du trinôme). 1291, 1289 et nouveau-2 sont du calcul pur, sans figure.
- Contrôle des chevauchements : 0 erreur (graduations placées à la main là où une courbe ou un pointillé passait dessous) ; largeurs ≤ 900 px ; chaque PNG regardé.

## Contrôles

- `verifier_notion.py --navigateur` : **OK, 0 problème** au premier passage. Après les corrections de relecture, le passage `--navigateur` est resté bloqué à la fermeture de Chrome. J’ai donc appliqué la procédure de repli sur la version finale :
  - `verifier_notion.py` sans navigateur : **OK, 0 problème** (`verif_navigateur_log.txt`) ;
  - `controle_apercu.mjs` avec captures et délai maximal : **94 vues sur 94 à 0** (téléphone et ordinateur ; cours, fiche, 15 exercices × 3 onglets ; `captures_log.txt`).
- **Captures téléphone regardées à l’œil** : le cours entier (6 écrans), la fiche (2 écrans), et les étapes de 1290, 1298, 1297, 1299, 1292, 1296 et nouveau-2. Corrections faites après relecture, aucune n’étant signalée par l’outil :
  - formules centrées réduites : démonstrations et exemples d’équations découpés en lignes alignées ;
  - tableau `euler(n)` qui défilait : passé en deux colonnes ;
  - tableaux de signes à 4 valeurs coupés à droite quand ils sont dans une étape (1297 Q2 et Q6, 1292 Q2) : sortis de l’encadré, ils tiennent ;
  - lignes de code coupées dans une étape (1299 B3, nouveau-1 Q5) : code sorti de l’étape et raccourci (`1e6`, `2*n`) ;
  - ponctuation orpheline en début de ligne (« ; », « . », « g. ») et espacement de $]{-\infty}\,;\ldots[$.

## Remarques pour l’orchestrateur

- **Défaut d’outil (blocage)** : comme pour 159 et 161, `controle_apercu.mjs` ne rend pas la main après la dernière vue ; lancé avec `timeout`, puis arrêt de mon seul processus node.
- **Défaut d’outil (détection)** : une formule centrée trop large est réduite (police plus petite) sans être signalée.
- Programme : la démonstration de l’unicité n’est pas faite (unicité admise, consigne du propriétaire).
