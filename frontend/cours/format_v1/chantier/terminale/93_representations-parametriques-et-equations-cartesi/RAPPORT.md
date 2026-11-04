# Notion 93 — Représentations paramétriques et équations cartésiennes (Terminale)

**État : prêt.** `verifier_notion.py --navigateur` : 0 problème. Calculs vérifiés en calcul exact : `verif_93.py` (« TOUT EST JUSTE »).

## Texte

- **Cours** (ancien, mince) : réécrit et complété selon le programme : théorème de la représentation paramétrique, lecture point / vecteur directeur, rappel de l'équation cartésienne d'un plan (la démonstration est dans la notion 92), position droite-plan **avec démonstration** (équation $(\vec u\cdot\vec n)t+e=0$, trois cas), tableau des 4 positions de deux droites, méthode à deux paramètres, deux plans, projeté orthogonal sur un plan et sur une droite (capacité du programme), exemples tous vérifiés. Systèmes et représentations paramétriques alignés (`\left\{\begin{aligned}…`), coordonnées en `(x\,;y\,;z)`.
- **Fiche** : remise en forme (formule encadrée, intersections, tableau des positions de deux droites, 4 erreurs classiques).
- **Exercices** (11) : corrigés restructurés (méthode / étapes / résultat), systèmes numérotés $(L_1)$, $(L_2)$, $(L_3)$, troisième équation toujours testée.
  Corrections de fond :
  - 986 Q2 : l'énoncé demandait de « vérifier que $B$ appartient au plan » alors que $B\notin\mathcal P$ → question reformulée ; Q5 reliée à Q4 (plans strictement parallèles).
  - 1109 : le même paramètre $t$ servait pour $d_1$ et $d_2$ → paramètres distincts $t$, $k$, $s$, $\lambda$ ; bloc de calcul cassé par la conversion (Q6) refait ; Q7 : troisième équation réellement vérifiée.
  - 1110 : « $ABCD$ parallélogramme (base de la pyramide) » était un argument circulaire → $\overrightarrow{AB}=\overrightarrow{DC}$ ; distance de $S$ au plan obtenue par le projeté $H$ (la formule de distance point-plan est hors programme) ; aire de $PBC$ par le projeté $K$ de $P$ sur $(BC)$ (question ajoutée dans l'énoncé, au programme) au lieu d'un long calcul cosinus/sinus ; « pyramide $SPBC$ » → tétraèdre.
  - 988 Q5 et 985 Q5 : distance par le projeté orthogonal (au programme) ; formule hors programme signalée « Pour aller plus loin » (988).
  - 989 Q5 / 990 Q5 : angle « des droites / des plans » → angle des vecteurs directeurs / normaux, virgule décimale ($19{,}47^\circ$, $61{,}87^\circ$) ; 990 : perpendicularité discutée.
  - 992 : non-alignement de $A$, $B$, $C$ justifié avant l'équation du plan ; paramètre $k$ pour $(AB)$.

## Figures (TikZ, style livre)

- **Refaites : 7 / 7** images en ligne (cours ×3, fiche ×2, exercice 1110 ×2). Défaut corrigé : sur l'ancienne pyramide l'arête cachée $[SD]$ était dessinée en trait plein.
- **Nouvelles : 15 figures** (12 fichiers) : cours ×5 (droite et paramètre $t$, 3 positions droite/plan, cube et droites non coplanaires, deux plans sécants, projeté orthogonal), fiche ×2 (reprises du cours), exercices 983, 985, 988, 990, 991, 1110 ×3 (pyramide, section $BCPQ$, projeté de $S$).
- Parties cachées calculées (rayon vers l'observateur, petite fonction dans `figures.py`) : arêtes cachées et portions de droite sous un plan en pointillés ; aucun texte sur un trait (contrôle automatique) ; largeurs ≤ 900 px.
- Conservées : 0. Retirées : 0.

## Contrôles

- `verif_93.py` : tous les résultats (cours + 11 exercices) en calcul exact sympy.
- `verifier_notion.py --navigateur` : OK. Captures téléphone dans `captures/` (cours, fiche, exercices).

## Remarques pour l'orchestrateur

- Exercices 983 et 985 portent sur des droites **du plan** (niveau Première) : conservés tels quels, utiles en découverte.
- La démonstration de l'équation cartésienne d'un plan est laissée à la notion 92 (Produit scalaire et orthogonalité) ; le cours 93 en fait un rappel.

## Finition 2026-11-02

**État : prêt** (agent-finition-T5). 11 exercices, dont 1 réécrit.

### Exercices
- **985 réécrit** (droite du plan, équation cartésienne de droite : niveau Première) → « Entraînement - Deux représentations d’une même droite » dans l’espace : vecteurs colinéaires $\vec{u}\,' = -2\vec{u}$, point commun $A'$ ($t = 2$) donc droites confondues, intersection avec le plan $z = 0$ en $R(7\,;2\,;0)$, droite $\Delta$ strictement parallèle (compétence « une droite a une infinité de représentations » jusque-là non travaillée).
- 983 conservé (découverte dans le plan, transition assumée vers l’espace) ; les 9 autres relus : justes, au programme.
- 1109 : remarque « Vue d’ensemble » ajoutée (plan $\mathcal{Q}$ contenant $d_1$ et $d_4$, explication géométrique de la non-coplanarité de $d_1$ et $d_2$).
- **Titres** (majuscules abusives) : 983 « Représentation paramétrique d’une droite du plan », 984 « … d’une droite de l’espace », 986 « Équation cartésienne d’un plan et plan parallèle », 989 « Deux droites sécantes de l’espace », 991 « Deux droites non coplanaires », 990 « Intersection de deux plans », 988 « Droite sécante à un plan et projeté orthogonal », 992 « Type bac - Plan défini par trois points et droite sécante », 1110 « Type bac - Pyramide et droites paramétriques ».

### Figures (outil commun `figures/espace.py`)
- **Revérifiées** : les 12 existantes.
- **Refaites (3)** : `cours_droite_plan` (nom du plan et « I » collés à la droite, nom du plan sur la droite incluse), `cours_deux_plans` et `ex990_deux_plans` (nom de la droite d’intersection collé aux bords des plans).
- **Retirée (1)** : `ex985_distance` (exercice réécrit).
- **Ajoutées (10)** : cours `cours_plan_normal` (II, plan et vecteur normal) ; exercices `n984_droite`, `n986_directeurs`, `n986_paralleles`, `n989_secantes`, `n985_confondues`, `n985_paralleles`, `n1109_bilan`, `n988_intersection` (Q3, droite qui perce le plan), `n992_bilan`. Plus aucun exercice sans figure.

### Contrôles
- `verif_93.py` : TOUT EST JUSTE (101 contrôles, 985 refait, valeurs des nouvelles figures ajoutées).
- `figures_livre.py` : 21/21 figures, 0 erreur, 0 avertissement ; chaque PNG regardé.
- `verifier_notion.py --navigateur` : OK, 0 problème ; `controle_apercu.mjs` avec captures : aucun problème ; captures téléphone de 985 (réécrit) regardées.
