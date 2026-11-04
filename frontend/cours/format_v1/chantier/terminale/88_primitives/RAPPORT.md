# Rapport — Terminale, notion 88 « Primitives »

## État
Prêt (cours 93, fiche 33, 10 exercices 1221 à 1230). Aucun point en suspens.

## Texte
Les résultats en ligne n'avaient pas d'erreur de calcul, mais **une grande partie des méthodes étaient hors programme**. Tout a été réécrit au format v1, dans le style du pilote et du livre de Terminale (chapitre 7) :
- notation $\int f(x)\,dx$ (intégrale indéfinie) et « $+C$ » dans les réponses → « déterminer une primitive de $f$ sur $I$ » ;
- changement de variable avec $du$ (exercice 1225, pas au programme) → reconnaissance des formes $u'u^n$, $\frac{u'}{u}$, $u'e^u$, $\frac{u'}{\sqrt u}$, $\frac{u'}{u^2}$ (le titre est conservé, une remarque fait le lien avec le « changement de variable ») ;
- $\ln|x|$ (hors programme) → intervalles précisés partout ; $\frac1x$ sur $]-\infty\,;0[$ donne $\ln(-x)$ (forme $\frac{u'}{u}$) ;
- règle anglo-saxonne « ILATE » (avec arctan, arcsin) supprimée ; intégration par parties présentée sous forme « primitives » ($uv-G$ primitive de $uv'$ si $G$ primitive de $u'v$), démontrée par la dérivée d'un produit, avec renvoi au chapitre Calcul intégral ;
- exposants fractionnaires $x^{3/2}$, $x^{-1/2}$ (hors programme) → dérivation de $x\sqrt x$, $x^2\sqrt x$, $(x+1)\sqrt{x+1}$ ;
- intervalles manquants ajoutés à chaque question ; chaque question a méthode / étapes / vérification par dérivation / résultat ; notes « attention » sur les erreurs classiques ($e^0=1$, facteur $\frac1a$, signe de $-\cos$).
- Cours : intervalle de $x^n$ corrigé ($n$ entier naturel, et non $n\ge1$), ajout de $\frac1{x^n}$ et $\frac{u'}{u^n}$, du cas $f(ax+b)$, de la primitive d'un produit (identification, intégration par parties), d'un tableau de variations natif (signe de $f$ / variations de $F$) ; démonstration de « deux primitives diffèrent d'une constante » et de l'unicité.
- Fiche restructurée (tableaux natifs des primitives usuelles et composées, lecture graphique, 5 pièges).

Vérification : `verif_primitives.py` (sympy, gardé dans le dossier) dérive chacune des 50 réponses d'exercices et tous les exemples du cours et de la fiche (dérivée symbolique + contrôle numérique sur l'intervalle, conditions $F(x_0)=y_0$) : tout est juste.

## Figures
- 2 refaites (cours et fiche, mêmes fichiers) : `famille.png` (primitives $x^2+C$, celle qui passe par $(1\,;3)$) et `lien.png` (signe de $f(x)=x^2-1$ / variations de $F(x)=\frac{x^3}{3}-x$, deux panneaux alignés) — les anciennes étaient en style matplotlib.
- 1 ajoutée : `ex_famille_cubique.png` dans le corrigé de l'exercice 1221 (question 1), réponse en vert.
- 0 conservée ; les 4 images en ligne (2 du cours, 2 de la fiche) sont remplacées.
- Contrôle des chevauchements texte/trait de `figures_livre.py` : aucune erreur ; chaque PNG regardé.

## Contrôles
`verifier_notion.py --navigateur` : OK, 0 problème (téléphone + ordinateur) ; `controle_apercu.mjs` : aucun problème. Captures téléphone regardées : cours (toutes les parties), fiche, exercices 1221, 1226, 1229 (énoncé et étapes).

## Remarques pour l'orchestrateur
- Les exercices 1226, 1227 et 1230 (intégration par parties) recoupent la notion 89 « Calcul intégral » ; ici la formule est utilisée sous forme « primitives », sans intégrale, pour rester cohérente avec la place du chapitre.
- Les questions 1224-2 et 1225-2 sont identiques ($\frac{2x}{x^2+1}$), de même que 1229-4 et 1225-5 à une translation près : à varier un jour si l'on veut (non fait : contenu de l'exercice conservé).

## Finition 2026-11-02

**État : prêt** (agent-finition-T3). 12 exercices (10 existants + 2 ajoutés).

### Titres
- Cours « Les primitives » → **« Primitives »** (intitulé de la notion) ; fiche « Résumé : Primitives ».
- 10 titres d'exercices « Type - Primitives - … » (nom du chapitre répété, majuscules abusives) → « Type - sujet » : « Découverte - Primitive vérifiant une condition », « Découverte - Linéarité et primitives usuelles », « Entraînement - Exponentielles et fonctions trigonométriques », « Entraînement - Fonctions rationnelles simples », « Entraînement - Fonctions de la forme f(ax + b) », « Entraînement - Intégration par parties », « Entraînement - Intégrations par parties successives », « Entraînement - Choisir la bonne méthode », « Entraînement - Racines, puissances et inverses », « Entraînement - Reconnaître une forme composée » (l'ancien « Substitution (Changement de variable) » nommait une méthode hors programme).

### Exercices
- Les 10 existants relus : justes ; aucun à réécrire. Tous étaient des listes de calculs : rien sur la lecture graphique ni sur une situation concrète.
- **2 ajoutés** :
  - `nouveau-1` « Découverte - Reconnaître la courbe d'une primitive » : deux courbes, laquelle est f, laquelle est F (signe de f / variations de F, et contre-argument) ; toutes les primitives ; F(0) lu sur le graphique ; primitive G passant par B(3 ; 2) = F + 1 (courbe décalée) ; aucune primitive par A et B à la fois ;
  - `nouveau-2` « Problème - Remplissage d'une cuve : du débit au volume » : V' = q, V(0) = 100 → V(t) = 500 − 400e^(−0,1t), croissance, limite et non-débordement, 400 L à t = 10 ln 4 ≈ 13 min 52 s, volume entré entre 5 et 10 min ≈ 95,5 L (lien annoncé avec le calcul intégral).
- 1223 (Q3) et 1224 (Q1) : un bloc « Lecture graphique » / « Contrôle graphique » ajouté autour de la nouvelle figure.

### Figures (10 fichiers, 12 emplacements)
- **Revérifiées** : les 3 existantes (détecteur 0 erreur + œil). **Retouchée (1)** : `lien` — « max 2/3 » et « min −2/3 » écrits en fractions minuscules → fractions lisibles.
- **Ajoutées (7)** :
  - `ex1223_cos` : −½cos(2x) passe par (0 ; −½), F décalée de ½ vers le haut passe par O (la constante non nulle expliquée) ;
  - `ex1224_ln` : ln(−x) décroissante sur ]−∞ ; 0[ car 1/x < 0, symétrique de ln ;
  - `n1_courbes` (énoncé, courbes C1 et C2 sans indication), `n1_lecture` (corrigé : signe de f / variations de F), `n1_famille` (corrigé : famille F + C, F par A, G par B, décalage +1) ;
  - `n2_debit` (énoncé : débit), `n2_volume` (corrigé : V avec asymptote V = 500 et le point (10 ln 4 ; 400)).
- Exercices sans figure (7) : 1222, 1228, 1226, 1227, 1230, 1229, 1225 — listes de calculs de primitives, où une figure serait décorative.
- `figures_livre.py` : 10/10, 0 erreur, 0 avertissement.

### Contrôles
- `verif_primitives.py` : TOUT EST JUSTE (100 contrôles, dont nouveaux exercices et valeurs des figures).
- `verifier_notion.py --navigateur` : OK, 0 problème ; `controle_apercu.mjs` avec captures : 0 défaut sur toutes les vues (téléphone et ordinateur) — Chrome est resté bloqué à la fermeture après la dernière capture (défaut connu) : seul mon processus a été arrêté et son verrou libéré.
- À l'import : 2 exercices `nouveau-N` à relier (relier_nouveaux) ; le titre du cours change (« Primitives »).
