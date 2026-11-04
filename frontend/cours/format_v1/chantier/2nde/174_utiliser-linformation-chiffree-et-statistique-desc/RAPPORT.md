# Rapport : notion 174 (Seconde) : information chiffrée et statistique descriptive

## État
Prêt. `verifier_notion.py --navigateur` : 0 problème. Tous les résultats ont été vérifiés en Python dans `verif_174.py` (85 contrôles, journal : `verification_maths.txt`).

## Programme (Seconde, 2019)
Le programme demande : proportions et proportion de proportion ; variation absolue, taux d’évolution, coefficient multiplicateur, évolutions successives et réciproques ; moyenne pondérée et linéarité, médiane, écart interquartile, écart type ; comparer deux séries ; lire une fonction Python qui renvoie la moyenne, l’écart type et la proportion des valeurs dans [m − 2s ; m + 2s]. Toutes ces compétences sont maintenant travaillées. Les fréquences cumulées décroissantes et l’ogive (courbe des effectifs cumulés) ne sont plus au programme : je les ai retirées.

## Texte
- **Cours** (219) : remis à niveau. Ajout de la variation absolue, d’une méthode « proportion ↔ effectif », de la démonstration des évolutions successives et réciproques, de la méthode médiane et quartiles (N pair ou impair), d’une remarque sur la sensibilité de la moyenne aux valeurs extrêmes, de la méthode « comparer deux séries » et d’une remarque calculatrice et Python ([x̄ − 2σ ; x̄ + 2σ]).
- **Fiche** (144) : formules clés et tableau natif des indicateurs (position et dispersion).
- **Erreurs de maths corrigées** :
  - 1990 : la borne m − 2s était fausse (−4,12 au lieu de −5,79).
  - 1979 : avec 60 appels, les effectifs n’étaient pas entiers (7,2 ; 16,8…). L’énoncé passe à 50 appels (effectifs 6 ; 14 ; 15 ; 10 ; 5).
- **Exercices remplacés dans leur bloc** (Id inchangés) :
  - 1991 : le code est réécrit avec des lignes de 30 caractères au plus. La question 4, qui renvoyait à « la question précédente », est entièrement rédigée.
  - 1977 : ajout de la médiane, des quartiles et de la moyenne par linéarité (250,14 g) ; les fréquences cumulées décroissantes sont retirées ; nouveau titre.
  - 1978 : l’ogive est remplacée par « classe de la médiane » ; ajout d’un pourcentage.
  - 1979 : ajout d’une moyenne approchée.
  - 1980 : le tableau d’effectifs et les rangs sont détaillés (le corrigé ne justifiait rien) ; ajout d’une comparaison.
  - 1981 et 1982 : structure cassée par la conversion (titres coincés dans des encadrés « résultat »), réécrits en « Question N ». En 1982, les justifications sont rigoureuses, avec un dénombrement pour l’affirmation 4.
  - 1989 : retrait de la notation « partie entière supérieure » (⌈ ⌉), qui n’est pas vue en Seconde, et d’une question triviale.
  - 1990 : nouveau titre (il contenait une formule).
- **Retouches** : 1983 (tableau des effectifs cumulés et rangs justifiés, calcul de la moyenne découpé pour le téléphone) ; 1984 et 1992 (puces « • » remplacées par de vraies listes).
- **Ajouts** :
  - `nouveau-1` « Problème - Salaires d’une entreprise - Moyenne ou médiane ? » : valeur extrême, taux d’évolution, choix de l’indicateur.
  - `nouveau-2` « Entraînement - Comparer deux séries - Position et dispersion » : même moyenne, écarts types de 2,05 et 4, rédaction d’une comparaison.

## Figures
- **9 figures refaites** au style des livres, toutes générées en Python à partir des données exactes des énoncés : evolutions, boite_cours, dispersion_cours, hist_appels, hist_sport, batons_masses, boites_3series, boites_AB, groupes_AB.
- Les 11 images en ligne étaient de style ancien (matplotlib) ; toutes sont remplacées. L’ogive de l’exercice 1978 (position 2) n’est plus appelée et sera supprimée à l’import.
- **Ajout** : groupes_AB (exercice nouveau-2).
- **Conservées** : 0.

## Contrôles
- `verifier_notion.py --navigateur` : 0 problème.
- Captures regardées : le cours et la fiche en téléphone, ainsi que les exercices 1991, 1977 et nouveau-2 (énoncé et étapes).

## Remarques pour l’orchestrateur
- Les diagrammes en boîte ne figurent pas explicitement au programme de Seconde (2019). Ils sont utilisés comme illustration, avec une explication, dans 1980, 1981 et le cours.

## Finition 2026-11-02

**État : prêt** (agent-finition-S4). 20 exercices (aucun ajout : nombre suffisant).

### Titres
- Cours et fiche : intitulé officiel « Utiliser l’information chiffrée et statistique descriptive » (le « la » ajouté est retiré).
- 19 titres « Type - Chapitre - Sujet » → « Type - Sujet » ; types « Algorithmique » et « Maîtrise » remplacés (Entraînement / Type examen). Exemples : « Découverte - Calculer une proportion de proportion », « Entraînement - Enchaîner des évolutions successives », « Type examen - Notes d’un contrôle : pourcentages, quartiles et moyennes ».

### Exercices réécrits
- **1990 réécrit de zéro** : il reprenait exactement les séries de 1991 (9 ; 9 ; 11 ; 11 et 0 ; 0 ; 0 ; 0 ; 0 ; 10). Nouveau sujet « Type examen - Comparer les températures de deux villes avec l’écart type » : moyennes égales (24 °C), σ = √1,5 ≈ 1,22 et √14 ≈ 3,74, puis valeur record 42 °C (moyenne 25,5, médiane inchangée 24, σ ≈ 6,91) et proportion 7/8 dans [x̄ − 2σ ; x̄ + 2σ].
- **1983 Q5–Q6 refaites** : Q6 redemandait la moyenne déjà calculée en Q4 (question circulaire) → moyenne des deux classes réunies (11,25) et piège « moyenne des moyennes » (11,2625) ; notation ⌈ ⌉ (hors programme) retirée ; tableau sans ligne de séparation réparé.
- **1987** : rappel sans le symbole Σ, énoncés rédigés, erreur fréquente (prix moyen non pondéré 2,17 €) et vérification de Q4 ajoutées.
- 1976, 1986 (sous-questions a/b), points finaux des questions (1975, 1984, 1985, 1986, 1987, 1992) ; tous les `\displaystyle` retirés.

### Figures
- **Revérifiées une par une (11)** : détecteur 0 erreur, mais 4 refaites : `hist_appels`, `hist_sport`, `batons_masses` (effectifs écrits sur les lignes du quadrillage → étiquettes sur fond blanc), `boites_3series` et `boites_AB` (nom de la série B écrit sous la boîte A, ambigu → noms à gauche de chaque boîte, vide réduit). `evolutions` et `boite_cours` régénérées par les nouveaux générateurs (même dessin). Conservées : `dispersion_cours`, `groupes_AB` (justes, lisibles).
- **15 ajoutées** : cours `proportion_cours` (aires proportionnelles, 30 % de 40 % = 12 %) et `axe_cm_cours` (coefficients sur un axe) ; exercices 1976 (ensembles emboîtés), 1984 (axe des coefficients), 1985 (deux chaînes d’évolutions), 1986 (réciproque), 1989 (série + boîte), 1990 (deux villes, valeur record hors de l’intervalle), 1991 (intervalle [m − 2s ; m + 2s]), 1982 (boîte + moyenne + rangs 7 à 21), 1983 (32 notes + boîte), 1992 (arbre des effectifs), 3758 (salaires : moyenne tirée par la dirigeante, médiane stable).
- 17 exercices sur 20 ont une figure ; sans figure : 1975, 1987, 1988 (calculs purs).

### Contrôles
- `verif_174.py` : **114 contrôles** (fractions, sympy ; le code Python de 1991 est extrait de l’énoncé et exécuté), tout juste.
- Téléphone : figures `proportion_cours`, `e1976_emboites`, `axe_cm_cours`, `e1984_axe` et `e3758_salaires` agrandies (texte trop petit une fois la figure réduite à la largeur de l’écran) : largeur réduite, étiquettes en taille normale. Notation `C` (et non `CM`) dans la figure de 1984, comme dans son énoncé.
- `figures_livre.py` : 0 erreur (aucun texte sur un trait, aucune figure > 1 100 px) ; chaque PNG regardé.
- `verifier_notion.py` : 0 problème de contenu ; seuls signalés : les Id 3758 et 3759, créés en base le 29/10 mais absents de `source_en_ligne/` (export du 29/10 antérieur à leur création) → **ré-export nécessaire avant import** (outil réservé à l’orchestrateur).
- Contrôle navigateur (`controle_apercu.mjs`, téléphone + ordinateur) : 124 vues, 0 problème. Chrome restant parfois bloqué à la fermeture (défaut connu), seul mon processus a été arrêté et son verrou libéré.
- Captures téléphone regardées : cours, fiche et exercices à nouvelles figures.
