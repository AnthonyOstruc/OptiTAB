# Rapport — 2nde, notion 170 « Représenter et caractériser les droites du plan »

**État : prêt.** Aucun point en suspens.

## Texte

- **Cours (226)** remis à niveau sur le programme 2019 : droite comme ensemble des
  points $M$ tels que $\det(\overrightarrow{AM}, \vec{u}) = 0$ (absent auparavant),
  théorème de l'équation cartésienne avec la **démonstration du programme
  complète** (sens direct et réciproque, encadré `demonstration`), méthodes
  (équation par le déterminant, lecture graphique de $p$ et $m$, tracé d'une
  droite), justification de $ab' - a'b$, alignement + algorithme Python (lignes
  ≤ 30 caractères), systèmes (interprétation graphique, substitution, combinaison).
- **Fiche (140)** : restructurée en 4 parties, erreurs classiques conservées.
- Aucune erreur de calcul dans l'existant ; défauts corrigés : `\displaystyle`
  partout, encadrés `resultat` en double, anglicisme « intercepts », tutoiement,
  puces « • (a) », couples écrits $(3;4)$, code Python trop long (lignes > 30 car.).
- `verif_170.py` : 56 contrôles sympy (cours, 12 exercices, figures) — tous justes.

## Exercices

- **Remplacé — 2046** « Droite perpendiculaire et distance » : **hors programme de
  Seconde** (orthogonalité par les pentes, distance point-droite = Première). Remplacé
  par « Découverte - Lire graphiquement pente et ordonnée à l'origine » (capacité du
  programme non travaillée : pente / vecteur directeur à partir d'une représentation
  graphique), avec figure d'énoncé et figure de corrigé.
- **Ajoutés** : `nouveau-1` « Problème - Tarifs d'un musée » (mise en système d'un
  problème concret, critère $ab' - a'b$, combinaison, interprétation graphique) ;
  `nouveau-2` « Problème - Location de vélos » (interprétation de la pente et de
  l'ordonnée à l'origine, intersection, comparaison de tarifs).
- **Améliorés** : 2049 (Q3 et Q5 par le déterminant, méthode du programme, au lieu
  d'une formule à apprendre par cœur ; titre raccourci) ; 2052 Q1 (justification
  « distinctes » par un point, au lieu d'un argument confus) ; 2048 Q5 (preuve que
  b) et d) ne sont pas des droites : trois points non alignés) ; 2054 (Q6 ajoutée :
  pourquoi la fonction est juste) ; 2045, 2051, 2047, 2050, 2053 : rédaction,
  contrôles, conclusions.

## Figures

- 29 figures neuves au style des livres (`figures/figures.py`, moteur générique
  repère + droites + étiquettes posées hors des traits) ; 31 emplacements.
- **Refaites** : 5 du cours, 2 de la fiche (réutilisent celles du cours), 21 des
  exercices (anciennes images matplotlib 4625 px, texte minuscule, légendes).
- **Ajoutées** : 2046 (énoncé + corrigé), `nouveau-1`, `nouveau-2`.
- **Conservées** : 0. **Retirées** : 0 appel supprimé (l'image en ligne de 2046 est
  remplacée à sa position).
- Contrôle de chevauchement de `figures_livre.py` : 0 erreur ; chaque PNG regardé.

## Contrôles

- `verifier_notion.py --navigateur` : OK, 0 problème.
- `controle_apercu.mjs` avec captures : cours (téléphone, 5 vues), fiche,
  exercices 2054 (étapes), 2046 (énoncé), nouveau-2 (étapes) regardés. Corrigé
  après lecture : deux formules centrées trop larges (réduites à l'écran) mises
  en `aligned`, la formule de la question 6 de 2054 réécrite en liste (elle était
  coupée), coefficients de 2054 en formules plutôt qu'en code, figure « trois
  cas » resserrée (727 px) pour que ses légendes restent lisibles sur téléphone.

## Remarques pour l'orchestrateur

- Aucune écriture en base, aucun `manage.py`, pas de git.

## Vérification des figures 2026-11-02

- **29 figures vues** (31 appels : 5 du cours, 2 de la fiche — reprises du cours —, 24 des exercices), à l'œil et avec le détecteur texte/trait de `figures_livre.py` : 29/29 sans chevauchement ni alerte.
- La session interrompue avait refait 3 figures (ex_lecture_enonce, ex_lecture_corrige, ex_pos_q3) : revérifiées.
- Contrôles mathématiques, contre les énoncés et les résultats des corrigés : u(3 ; 2) et A(2 ; 1) ; Δx = 3, Δy = 4 ; y = 2x − 1 et x + y = 5 sécantes en I(2 ; 3) ; d1 : y = 2x − 3, d2 : y = −2x/3 + 2, d3 : x = −3 (2046) ; A(−2 ; 3), B(4 ; −1), u(3 ; −2), x = 2 (2045) ; A, B, C sur y = 2x + 4, F hors de (DE), K(6 ; 3) (2051) ; (AB) : y = x/2 + 3/2, y = −3x − 8, x + 2y = 0, x = −5, x + y − 2 = 0 (2049) ; d′ : y = −3x + 5 par B(0 ; 5) et C(3 ; −4) (2047) ; d1 ∥ d2, d3 = d4, x = −3 et x = 1/2, 3x + y − 5 = 0 par P(2 ; −1), (2 ; 2) (2052) ; points de tracé des 5 droites de 2050 ; (9 ; 6) (3739) ; tarif A = 1,5x + 12 et tarif B = 3x sécants en (8 ; 24) (3740). Graduations omises seulement là où une droite passe (choix assumé, les valeurs utiles restent écrites), style des livres.
- **Défauts trouvés : aucun. Figures refaites dans cette reprise : aucune.**
- Contrôles finaux : `verifier_notion.py --navigateur` sur une copie de travail dont `meta.json` déclare les Id 3739 et 3740 (créés à l'import du 29/10, absents de l'export) : **OK, 0 problème**, contrôle Chrome compris. Captures téléphone des figures refaites regardées.

## Finition 2026-11-02

**État : prêt** (agent-finition-S2). 12 exercices, tous au programme de Seconde 2019 (pas d'ajout ni de remplacement).

### Titres
- Cours et fiche : « Droites du plan et systèmes » → **« Représenter et caractériser les droites du plan »**, l'intitulé officiel (les systèmes en font partie). **À renommer en base aussi** : c'est `titres_docs.py` qui s'en charge.
- Exercices : 5 titres retouchés (« Maîtrise » → Entraînement pour 2053, parenthèse et deux-points retirés, apostrophes typographiques).

### Figures (9 ajoutées, aucune refaite ni retirée)
- **Corrigés** : 2054 (3 figures : points alignés sur y = x + 1, point (4 ; 6) hors de la droite, droite x = 2) ; 2048 (les 4 droites, ordonnées à l'origine en vert) ; 2053 (3 figures : les trois cas, une solution (3 ; 2), aucune, une infinité).
- **Énoncés** : 2045 (les quatre points), 2047 (droite d, points B et C).
- Plus aucun exercice sans figure. Graduations coupées par une droite retirées. 2053 Q2 : les droites sont nommées d et d′ dans le texte, comme sur la figure. Chaque PNG regardé.

### Contrôles
- `verif_170.py` : 56 contrôles OK.
- `verifier_notion.py --navigateur` : **OK, 0 problème**. `controle_apercu.mjs` avec captures : 76 vues, aucun problème ; capture téléphone de 2053 (étapes, 3 nouvelles figures) regardée.
