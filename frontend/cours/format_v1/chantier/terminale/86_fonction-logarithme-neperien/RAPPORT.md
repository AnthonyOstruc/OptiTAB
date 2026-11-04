# Rapport : notion 86, Fonction logarithme népérien (Terminale)

**État : prêt.** `verifier_notion.py --navigateur` : OK (0 problème). Les captures sont dans `captures/`. J'ai regardé le cours, la fiche et 3 exercices sur téléphone.

## Texte
- **Cours** restructuré :
  - définition et conséquences ;
  - théorème de la relation fonctionnelle, avec sa démonstration ;
  - tableau des règles de calcul ;
  - dérivée : démonstration au programme, dérivabilité admise ;
  - tableau de variations natif ;
  - théorème sur ln u ;
  - croissances comparées : démonstration de la limite de x ln x en 0⁺, qui est au programme ;
  - méthodes « équations et inéquations » et « seuil » ;
  - demi-vie.
- **Fiche** : tableau de variations natif, règles, seuils, pièges.
- **Exercices** (10, Id, titres et difficultés inchangés) : tous les corrigés sont réécrits en méthode / étapes / résultat. Le domaine est toujours traité en premier. Tous les tableaux de signes et de variations sont natifs, y compris les zones interdites hachurées.
- Erreurs ou défauts de fond corrigés :
  - Limites, Q3 : la règle de L'Hôpital (hors programme) est remplacée par un nombre dérivé. Q5 est traitée de la même façon.
  - Capital à 5 % : la réponse « 14,2 ans » devient **15 ans**, puisque les intérêts sont annuels.
  - Synthèse 1, Q3 : la limite en +∞ était justifiée par « +∞ − ln(+∞) = +∞ », ce qui est faux (forme indéterminée). Elle est désormais levée correctement.
  - Niveau sonore : la formule avec ln était présentée comme des « décibels », ce qui est physiquement faux. L'échelle devient abstraite, avec une remarque « Pour aller plus loin » sur log₁₀.
  - Textes tronqués par la conversion réparés (« x 2 », « h'(x) 0 », « Pour 0 0 », etc.).
  - Étude de m : limites et tableau ajoutés. Synthèse 2 : encadrements de α et β ajoutés.
- Tous les résultats sont vérifiés dans `verif_logarithme.py` (sympy, numpy, scipy) : 0 échec.

## Figures
- **Refaites : 24 sur 24** (cours 4, fiche 2 réutilisant celles du cours, exercices 18). Toutes les anciennes images étaient de style matplotlib : texte minuscule, grands vides, légendes illisibles.
- **Ajoutées : 0. Conservées : 0. Retirées : 0.**
- Les 24 figures font 26 emplacements, au style des livres, avec une largeur de 800 à 870 px.
- Aucun texte n'est posé sur un trait : le contrôle n'a signalé aucune erreur ni avertissement.
- Les éléments de réponse sont en vert : ensembles solutions sur l'axe, extremums, points d'intersection.

## Remarques pour l'orchestrateur
- J'ai ajouté deux macros locales, `\gradHD` et `\gradHG`, dans `PREAMBULE_EXTRA`. Elles placent une graduation au-dessus de l'axe, à droite ou à gauche du trait, car `XLAB` ne propose que la position centrée au-dessus. Cette option pourrait être ajoutée à l'outil.
- Sur téléphone, les longues chaînes `aligned` sont réduites, mais elles restent lisibles.

## Finition 2026-11-02

**État : prêt** (passe commencée par un premier agent, interrompue pendant la mise à jour de la correspondance des figures, reprise et terminée).

### Titres
- Cours « Fonction logarithme népérien » (était « La fonction logarithme népérien »), fiche « Résumé : Fonction logarithme népérien » : intitulé officiel.
- 10 titres d'exercices : « Type - Fonction Logarithme - … » → « Type - sujet » (ex. « Entraînement - Ensembles de définition et dérivées », « Problème - Synthèse en cinq questions indépendantes » (était « Problèmes de Synthèse 1 »), « Problème - Étude de ln x − x + 2 » (était « Problèmes de Synthèse 2 »)).

### Exercices réécrits
- 1250, question 5 : l'ancien « niveau sonore » L = 10 ln(I/I₀) n'avait pas de sens physique (les décibels utilisent log₁₀) → remplacé par un seuil de concentration d'un médicament : Cₙ = 50 × 0,8ⁿ < 5 ⇔ n > ln 0,1 / ln 0,8 ≈ 10,32, donc n = 11 (piège du signe de ln 0,8 signalé). Étapes, résultat et solution réécrits.

### Figures (30 fichiers, 32 emplacements)
- **Ajoutées (6)** : 1245 Q2 (ensemble de définition de ln(x² − 4) en vert), 1249 Q1, Q2, Q3 (x ln x en 0⁺, ln x / x en +∞, tangente y = x à ln(1 + x)), 1250 Q3 (refroidissement de Newton), 1250 Q5 (seuil de concentration).
- Correspondance des figures complétée (travail interrompu) : 32 emplacements, chacun avec son texte alternatif.
- **Revérification à l'œil des 30 figures (reprise) : 4 retouchées**
  - `ex1249_xlnx` : graduation 1 posée sur la courbe → placée du côté libre ;
  - `ex1249_lnx_x` : légende « tend vers 0 en +∞ » posée sur la courbe → remontée ; graduation 1/e agrandie ;
  - `ex1250_seuil` : graduations 10 et 12 sans valeur, point C₁₀ ≈ 5,37 confondu avec le seuil 5 à cette échelle → valeurs C₁₀ (bleu, au-dessus) et C₁₁ (vert, sous le seuil) écrites, graduation 11 en gras, grille allégée ;
  - `etude_k` : graduations 1, √e et 2 entassées → 2 retiré.
- Toutes les figures à graduations placées à la main : suppression des petits carrés blancs laissés par les graduations automatiques vides.
- `figures_livre.py` : 30/30, **0 erreur, 0 avertissement**.

### Contrôles
- `verif_logarithme.py` : 0 échec (contrôles sympy de la question réécrite et des figures ajoutés : seuil n = 11, C₁₀, C₁₁, T(10) = 60, domaine de ln(x² − 4), extremums des figures 1249, points des droites y = ax en 1251, zéros α et β en 1252).
- `verifier_notion.py --navigateur` : OK, 0 problème (32 nouvelles figures, 0 image en ligne conservée).
- `controle_apercu.mjs` avec captures : 64 vues sur 64 sans défaut (téléphone et ordinateur) ; au dernier passage, il est resté bloqué à la fermeture de Chrome (défaut connu) : seul mon processus a été arrêté et son verrou libéré. Captures regardées : cours (définition, propriétés), 1250 (étapes, avec la nouvelle question 5).
- **Formules au téléphone** (mesure dans Chrome à 390 px, script de travail hors du dépôt) :
  - cours : le tableau « Règle / Formule / Exemple » défilait → tableau « Règle / Formule » et exemples en liste juste après ;
  - 1251 Q2 (système) : chaîne qui défilait → redécoupée ;
  - chaînes réduites à 73-79 % (peu lisibles) → membre de gauche seul sur la première ligne : 1247 Q3 et Q5, 1248 Q5, 1250 Q1, Q2 et Q3, 1246 (dérivée de u).
  - Résultat : 0 formule qui défile, 0 formule réduite sous 80 %. Restent quelques tableaux de signes qui défilent de 12 à 58 px dans leur cadre (rendu normal du moteur).
