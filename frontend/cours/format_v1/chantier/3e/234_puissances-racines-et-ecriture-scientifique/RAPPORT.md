# Notion 234 (3e) : Puissances, racines et écriture scientifique

**État : prêt** (agent-3e-C2, 2026-11-03). 21 exercices (aucun ajout, 3 remplacés, 4 en partie réécrits).

## Texte
- **Cours 229** réécrit façon manuel : I. puissances (définition, $a^0$, $a^{-n}$, signes, tableau des règles en `propriete`, justification de $a^m \times a^n = a^{m+n}$) ; II. **puissances de 10, préfixes de nano à giga** (capacité du programme absente avant) et ordres de grandeur ; III. notation scientifique (définition, méthode pas à pas, calcul et normalisation) ; IV. racine carrée (définition, interprétation géométrique, **carrés parfaits de 1 à 144**, encadrement, **équation $x^2 = a$** en propriété).
- **Programme** : la simplification $\sqrt{72} = 6\sqrt{2}$ et la règle $\sqrt{ab} = \sqrt{a}\sqrt{b}$ relèvent de la Seconde ; elles ne sont plus enseignées comme exigibles (un encadré « Pour aller plus loin » les signale).
- **Fiche 149** : listes propres, préfixes, carrés parfaits, 4 pièges, réflexe brevet.
- **Exercices** : tous réécrits au format pilote (méthode / étapes / résultat encadré, au moins une erreur fréquente par exercice, titres « Type - Sujet »).
  - **Remplacés** : 2123 « Puissances de 10 » (doublon de 2118) → « Découverte - Puissances de 10 et ordres de grandeur » (axe) ; 2128 « Simplifier exactement » ($\sqrt{98}$, $\sqrt{75} - \sqrt{27}$ : hors programme) → « Entraînement - Utiliser les préfixes de nano à giga » ; 2133 « Une masse minuscule » (artificiel) → « Type brevet - Les globules rouges ».
  - **En partie réécrits** (questions hors programme en $a\sqrt{2}$) : 2131 Q4-Q5, 2135 Q4-Q5 (côté $\sqrt{8} = 2\sqrt{2}$ obtenu par $(2\sqrt{2})^2 = 8$), 2138 (côté $\sqrt{50}$, diagonale par Pythagore), 2189 (tests sur exemples, la règle du produit présentée comme admise).
  - 2188 : arrondis justifiés par $6{,}05^2$ et $9{,}45^2$ au lieu d’une valeur donnée.
  - Aucune erreur de maths dans l’ancien contenu ; `verif_234.py` : **58 contrôles** (sympy, Decimal), tout juste.

## Figures (style livre, `figures/figures.py`)
- 10 figures neuves, 13 emplacements : cours 3 (axe des ordres de grandeur, carrés et racines, encadrement de $\sqrt{37}$ par zooms), fiche 2 (reprises), exercices 8 (énoncé + corrigé en vert : 2123, 2131, 2135 ; corrigés : 2188, 2138 carré construit sur la diagonale).
- Les 2 images matplotlib en ligne (cours, fiche) sont remplacées : 0 conservée.
- Tolérances déclarées : aires écrites au centre des carrés colorés (faux positifs du détecteur). Avertissement admis : la cote « côté ? » coupe sa flèche grâce à son fond blanc (cote).

## Contrôles
- `verifier_notion.py --navigateur` : **OK, 0 problème**.
- `controle_apercu.mjs` avec captures : aucun problème détecté (téléphone et ordinateur). Vues regardées : cours en téléphone.
- Corrigé après relecture des captures : tableau des préfixes (4 colonnes, coupé) ramené à 3 colonnes, exemple de la règle $(ab)^n$ raccourci, axe des ordres de grandeur passé à la **verticale** (trop réduit en horizontal), formule de la notation scientifique isolée.

## Remarques pour l’orchestrateur
- 1 exercice « Type brevet » (2133, Id conservé, type changé dans le titre).
