# Notion 233 (3e) : Nombres rationnels et fractions

**État : prêt** (agent-3e-C2, 2026-11-03). 21 exercices (aucun ajout, 4 remplacés).

## Texte
- **Cours 228** réécrit façon manuel : objectifs en liste ; I. rationnels (définition « $b \times \frac{a}{b} = a$ », représentations, écriture décimale finie ou périodique, fractions égales, fraction irréductible par décomposition en facteurs premiers — capacité de 3e absente avant) ; II. somme/différence ; III. produit, **inverse** (absent avant), quotient, simplification avant produit, priorités ; IV. fraction d’une quantité, fraction d’une fraction, tout de référence ; V. comparer, valeur exacte / approchée. Les « définition » qui contenaient des exemples sont devenues `exemple`, la « check-list » a été retirée (redite), le renvoi « onglet Fiches » supprimé.
- **Fiche 148** : listes propres (plus de puces « • »), tableau des 4 opérations sans `\displaystyle`, 4 pièges, réflexe brevet.
- **Exercices** : tous réécrits au format pilote (méthode / étapes détaillées / résultat encadré, au moins une erreur fréquente ou un « à retenir » par exercice, titres « Type - Sujet »).
  - **Remplacés** : 2181 « Des températures qui évoluent » (nombres relatifs, hors sujet) → « Découverte - Lire et représenter une fraction » (disques et barres) ; 2098 « Respecter les priorités » (entiers, niveau 5e) → « Découverte - Placer des fractions sur une droite graduée » ; 2115 « Un héritage partagé » (doublon de 2113) → « Type brevet - Vrai ou faux sur les fractions » ; 2116 « Un aquarium à remplir » (doublon de 2112) → « Problème - Remplir un bassin avec deux robinets ».
  - **Enrichis** : 2099 (question 1 avec barres 3/4 = 6/8 = 9/12), 2100 (décomposition en facteurs premiers), 2183 (modèle d’aire 2/3 × 3/4, inverses), 2104 (Q5 : ranger trois fractions au lieu d’un arrondi), 2110 (Q5 : 1/3 + 1/3 + 1/3 arrondi donne 0,99).
  - Aucune erreur de maths trouvée dans l’ancien contenu ; `verif_233.py` : **58 contrôles**, tout juste (fractions exactes, décompositions sympy, programme de calcul, problèmes rejoués).

## Figures (style livre, `figures/figures.py`)
- 19 figures neuves, 22 emplacements : cours 4 (représentations de 3/4, somme en barres, 3/5 de 40, droite en douzièmes), fiche 2 (reprises du cours), exercices 16 dans 13 exercices (énoncé + corrigé en vert pour 2181, 2098, 2183 ; corrigés 2099, 2182, 2103, 2104, 2111, 2112, 2113, 2114, 2116, 2117).
- Les 4 images matplotlib en ligne (cours ×2, fiche ×1, exercice 2111) sont remplacées : 0 conservée.
- Tolérances déclarées (`TOLERE`) : `quantite`, `ex_lecture`, `ex_votes` — nombres écrits au centre de parts coloriées (le détecteur prend le fond de couleur pour un trait). Toutes ≤ 900 px environ ; la droite du cours a été scindée en deux droites courtes après relecture sur téléphone (trop réduite).
- Pas de figure sur les calculs purs (2100, 2184, 2185, 2107, 2108, 2109, 2110, 2115).

## Contrôles
- `verifier_notion.py --navigateur` : **OK, 0 problème** (seules notes : titres changés).
- `controle_apercu.mjs` avec captures : aucun problème détecté (téléphone et ordinateur). Vues regardées : cours en téléphone, fiche, exercices 2183 et 2112 (étapes, figures corrigées).

## Remarques pour l’orchestrateur
- Type « Type brevet » : 1 exercice (2115, Id conservé, type changé dans le titre) pour suivre la progression demandée dans FILE_3E.
