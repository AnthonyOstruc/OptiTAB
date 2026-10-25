# Livre OptiTAB - Physique-Chimie, Première spécialité

Livre de cours et d'exercices corrigés, dans la charte du livre de Terminale (`../livre-pc-terminale`),
dont il reprend les styles (`optitab-livre.sty`, `pc-livre.sty`) et les outils de compilation et de contrôle.

## Programme de référence

- Programme de spécialité physique-chimie de première générale, BO spécial n° 1 du 22 janvier 2019
  (arrêté du 17 janvier 2019, NOR MENE1901635A), toujours en vigueur : le BO n° 14 du 2 avril 2026 ne
  modifie que les programmes de mathématiques. Texte extrait dans `recherche/`.
- Une spécialité arrêtée en fin de première est évaluée en contrôle continu ; les notions de première
  restent mobilisables à l'épreuve de terminale.

## Plan (21 chapitres, 15 exercices chacun, un défi par chapitre)

1. Constitution et transformations de la matière : chapitres 1 à 10 (composition d'un système,
   absorbance et dosage par étalonnage, oxydoréduction, avancement, titrages colorimétriques, Lewis et
   polarité, cohésion et extraction, molécules organiques et IR, synthèses, combustions).
2. Mouvement et interactions : chapitres 11 à 13 (champs, fluides au repos, forces et variation de vitesse).
3. L'énergie : conversions et transferts : chapitres 14 à 16 (électricité, travail et énergie cinétique,
   énergie mécanique).
4. Ondes et signaux : chapitres 17 à 20 (ondes mécaniques, lentilles, couleurs, ondes et photons).
5. Outils transversaux : chapitre 21, Mesures et incertitudes.

Chaque chapitre : ouverture, L'essentiel (cours illustré, méthodes, programme Python, activité
expérimentale, encadré « Bien rédiger »), 5 exercices de Découverte, 6 d'Entraînement, 4 « Objectif DS »
avec documents, inspirés des devoirs surveillés, devoirs maison et contrôles de première (contextes
recherchés, énoncés originaux). Défis, indications et corrigés en fin d'ouvrage. Annexes :
six devoirs surveillés corrigés, méthode du devoir, fiches expérimentales, données utiles, repères du programme.

## État d'avancement

**Livre terminé et livré le 24 octobre 2026 (539 pages)** : PDF dans
`output/pdf/France/Physique-chimie/OptiTAB - Physique-chimie - Première spécialité - Manuel complet.pdf`
et sur le Bureau (`Livres OptiTAB - Lycée`).

- Couvertures, page de titre, mentions, avant-propos, mode d'emploi, parcours, sommaire, ressources, tableau de bord,
  références.
- 21 chapitres : cours illustré avec programme Python, 15 exercices (Découverte, Entraînement, Objectif DS), 15 corrigés
  avec figures annotées et notes « À retenir » / « Erreur fréquente », un défi avec indications et corrigé sur deux pages,
  un script `verifications/chapitre_NN.py` qui recalcule chaque valeur publiée.
  1. Composition d'un système chimique (D01 : le dernier souffle de César).
  2. Absorbance et dosage par étalonnage (D02 : deux colorants, une seule couleur).
  3. Réactions d'oxydoréduction (D03 : l'arbre de Diane prend du poids).
  4. Avancement et bilan de matière (D04 : la sonde lambda).
  5. Titrages colorimétriques (D05 : que vaut vraiment une eau de Javel ?).
  6. Schémas de Lewis, géométrie et polarité (D06 : la molécule d'eau en géométrie).
  7. Cohésion, dissolution et extraction (D07 : l'étiquette d'une eau minérale).
  8. Molécules organiques et spectroscopie infrarouge (D08 : l'odeur du chocolat).
  9. Synthèses organiques (D09 : deux procédés pour l'ibuprofène).
  10. Combustions et énergie chimique (D10 : le meilleur carburant ?).
  11. Interactions fondamentales et champs (D11 : ce qui tient le noyau).
  12. Description d'un fluide au repos (D12 : les hémisphères de Magdebourg).
  13. Forces et variation de la vitesse (D13 : freiner à temps).
  14. Énergie et puissance électriques (D14 : ne pas faire sauter les plombs).
  15. Travail et énergie cinétique (D15 : rouler moins vite pour consommer moins).
  16. Énergie potentielle et énergie mécanique (D16 : stocker l'électricité dans un lac).
  17. Ondes mécaniques (D17 : localiser l'épicentre d'un séisme).
  18. Lentilles minces et images (D18 : photographier la Lune).
  19. Couleurs et vision (D19 : pourquoi le ciel est-il bleu ?).
  20. Lumière : ondes et photons (D20 : de quoi les étoiles sont-elles faites ?).
  21. Mesures et incertitudes (D21 : combien de mesures faut-il ?).
- Devoirs surveillés : six devoirs de deux heures (`devoirs/ds-0N.tex`), trois exercices chacun, corrigés avec barèmes
  (`devoirs/corrige-0N.tex`), valeurs vérifiées par `verifications/devoirs.py` ; méthode du devoir, capacités
  expérimentales et quatre fiches expérimentales (`annexes/methodes-devoir.tex`).
- Annexes : données utiles (constantes, couples oxydant-réducteur, énergies de liaison du chapitre 10, tableau
  périodique, bandes infrarouges) et repères du programme (`annexes/donnees-programme.tex`).

Outils propres à ce livre : environnement `avancement` (tableaux d'avancement), décors d'ouverture
`mole`, `redox`, `avancement`, `colorimetrie`, `lewis`, `micelle`, `infrarouge`, `flamme` (`pc-livre.sty`) ;
les chapitres 11 et 12 réutilisent les décors `gravitation` et `gazparfait` du livre de Terminale.
Dans L'essentiel, `\schema` est collé au bloc qui le précède : `\par\penalty0` juste avant permet de
renvoyer la figure en haut de la page suivante plutôt que de laisser une demi-page vide.
La version installée de chemfig n'a plus `\lewis` : les doublets s'écrivent `\charge{90=\|}{O}`.

## Compiler et contrôler

    python compiler.py         # passes LuaLaTeX jusqu'à stabilisation, refuse les débordements
    python verifier_livre.py   # plan, comptes, titres énoncés/corrigés, défis, figures, calculs

Chaque valeur numérique publiée est recalculée dans `verifications/chapitre_NN.py`.
