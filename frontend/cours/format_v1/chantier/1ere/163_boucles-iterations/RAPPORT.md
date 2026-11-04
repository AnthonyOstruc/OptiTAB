# Rapport : notion 163, ex « Boucles / Itérations » (Première spécialité)

**État : prêt.** Le cours, la fiche et les 11 exercices (5 existants réécrits, 6 ajoutés) sont au format OptiTAB v1. Le chapitre est réorienté vers les **algorithmes que le programme de Première (2019) demande d'écrire**.

**Titre proposé pour la notion (à renommer en base) : « Algorithmes du programme de Première »**. C'est aussi le titre du cours ; la fiche s'intitule « Résumé : Algorithmes du programme de Première ».

## Programme couvert (exemples d'algorithmes du programme 2019)

| Partie | Algorithmes traités |
|---|---|
| Suites | terme de rang n, somme de termes, factorielle, seuil (`while`), suite qui ne dépasse jamais un seuil (boucle infinie, avec garde-fou), Fibonacci |
| Second degré, fonctions | tableau de valeurs, balayage (encadrement d'une racine, comparé à la valeur exacte par le discriminant) |
| Dérivation | liste des coefficients directeurs des sécantes pour un pas donné ; sécantes de plus en plus proches de la tangente |
| Exponentielle | méthode d'Euler ; valeur approchée de e par (1 + 1/n)^n, avec un seuil |
| Trigonométrie | approximation de π par la méthode d'Archimède (polygones inscrits, formule de doublement démontrée par Pythagore) |
| Probabilités, VA | simulation (`random`, `randint`), fréquence, histogramme de simulation, moyenne d'un échantillon, succession de deux épreuves (urne sans remise ; dé puis urne, avec P_R(S)) |

Les boucles et les tests sont rappelés dans un encadré « Rappel de Seconde » (outils seulement). Les listes servent d'outil à deux endroits (histogramme, liste de valeurs `for h in [...]`) avec renvoi à la notion « Notion de liste ».

**Retiré (hors programme ou purement informatique)** : `break`, `continue`, boucles imbriquées « gratuites » (motifs, tables de multiplication), exercices de comptage sans lien avec les maths. **Non traités** : la méthode de Newton (hors programme selon votre consigne), Syracuse et la fréquence des lettres d'un texte (cités par le programme, mais ils relèvent surtout des listes et des chaînes : voir la notion 164).

## Texte

- **Cours réécrit de zéro** (8 parties) : objectifs, prérequis, rappel de Seconde, puis une partie par thème du programme. Chaque partie contient une méthode, des programmes avec l'affichage réel, des tableaux d'état et des erreurs fréquentes. Le cours se termine par un bilan sous forme de tableau, les pièges à éviter et un « À retenir ».
- **Fiche réécrite** : les quatre thèmes en tableaux et en listes courtes, un programme de seuil, 2 figures et 5 pièges.
- **Exercices existants (titres changés, Id conservés)** : tous étaient faibles ou hors sujet. Ils sont remplacés dans leur bloc par des exercices complets (méthode, étapes, résultat, erreur fréquente).
  - 1058 → « Découverte - Calculer les termes d'une suite » (fonction à compléter, tableau d'état, formule explicite par une suite géométrique auxiliaire).
  - 1059 → « Entraînement - Sommes de termes, factorielle et suite de Fibonacci » (seuil n! > 10^9, erreur d'affectation qui donne les puissances de 2).
  - 1060 → « Entraînement - Algorithme de seuil d'une suite » (population, résultats : 2034 et 2041).
  - 1061 → « Problème - Une suite qui ne dépasse jamais un seuil » (u_n = 15 − 14 × 0,8^n, boucle infinie, garde-fou qui renvoie `None`).
  - 1062 → « Entraînement - Simuler la succession de deux épreuves » (arbre, probabilités totales, P_R(S) estimée par simulation).
- **Exercices ajoutés** : nouveau-1 Tableau de valeurs et balayage ; nouveau-2 Coefficients directeurs des sécantes ; nouveau-3 Méthode d'Euler et fonction exponentielle ; nouveau-4 Valeur approchée du nombre e ; nouveau-5 Simuler un jeu : fréquence et moyenne d'un échantillon ; nouveau-6 Approximation de pi par la méthode d'Archimède.
- **Erreurs de l'ancienne version** : du code cassé par la conversion (`i $\ast$ i` dans les programmes), des affichages résumés par « … » au lieu de la sortie réelle, et 2 images de code (interdit).

## Vérification (`verif_algorithmes.py`, journal `verif_log.txt`)

- **46 programmes exécutés pour de vrai** et 42 affichages comparés **à l'identique** avec la sortie obtenue. Seuls 2 programmes « à compléter » (avec « … ») ne sont pas exécutés. Chaque document est exécuté bloc après bloc ; un compteur de lignes détecte une boucle qui ne s'arrête pas.
- **Simulations** : le générateur est initialisé (graine 2026) au début de chaque document. Les affichages imprimés sont donc ceux d'une exécution réelle, reproductible. Le texte précise que le résultat change à chaque exécution.
- **69 contrôles mathématiques (sympy)** : tous les termes, sommes, seuils (y compris e − u_n < 0,01 en précision 30 chiffres : n = 135), les racines, le discriminant, les taux de variation, Euler, la formule d'Archimède et les demi-périmètres, toutes les probabilités des arbres. Les boucles annoncées comme infinies sont rejouées au-delà de 10^6 tours.
- `controle_longueurs.py` : liste les lignes de code trop longues pour un téléphone.

## Figures

- **16 figures neuves** au style des livres, utilisées à **20 places**. **0 image en ligne conservée** : les 4 anciennes images (du code et un tableau en image) sont remplacées aux mêmes positions.
- **Cours (6)** : termes et seuil 50, suite bornée et seuil 5 jamais dépassé, Euler (pas 0,25) comparé à exp, hexagone d'Archimède, histogramme de 1000 lancers de deux dés comparé aux probabilités, arbre de l'urne. **Fiche (2)** : seuil et Euler.
- **Exercices** :
  - énoncé et corrigé distincts pour 1060 (population), 1061 (suite bornée), 1062 (arbre vide puis complété en vert) et nouveau-6 (figure d'Archimède annotée dans le corrigé) ;
  - nouveau-1 (parabole et intervalles des solutions), nouveau-2 (sécante, tangente, h et f(1 + h) − f(1)), nouveau-3 (Euler, pas 0,5).
- L'histogramme lit ses effectifs dans l'affichage du programme du cours, qui est lui-même vérifié : figure et texte ne peuvent pas diverger.
- Contrôle des chevauchements : 0 erreur. Largeurs de 538 à 895 px. Chaque PNG a été regardé.

## Contrôles

- `verifier_notion.py --navigateur` : **OK, 0 problème** (`verif_navigateur_log.txt`).
- `controle_apercu.mjs` avec captures : 70 vues, aucun problème (`captures_log.txt`). Les deux outils ont rendu la main normalement ; aucun processus n'est resté ouvert.
- **Captures téléphone regardées à l'œil** : le cours en entier, la fiche, et les étapes de 1058, 1059, 1062, nouveau-1 et nouveau-6. Corrections faites après relecture, **non détectées par l'outil** :
  - formules centrées coupées : OI² … donc OI (cours et nouveau-6), v_n … donc u_n (1058, 1061), somme arithmétique (1059), discriminant (nouveau-1), P_R(S) (1062), E(X) et la probabilité de l'urne (cours) ; elles sont passées en lignes alignées ;
  - ligne de code coupée dans un encadré d'étape (`c = sqrt(2 - sqrt(4 - c**2))` dans nouveau-6) : découpée en deux lignes ;
  - tableaux à 5 ou 6 colonnes transposés (nouveau-2, nouveau-6) ;
  - point-virgule orphelin, deux-points suivis d'un point dans un encadré.

## Remarques pour l'orchestrateur

- **Défaut d'outil (détection)** : déjà signalé pour la notion 161. Une formule centrée trop large est coupée sur téléphone sans être signalée, et une ligne de code qui défile dans un encadré d'étape n'est pas signalée non plus.
- **Titre** : l'en-tête de l'aperçu affiche encore « Boucles / Itérations » (nom de la notion en base). Il faut renommer la notion « Algorithmes du programme de Première ».
- **Programme** : le texte de 2019 cite, me semble-t-il, la méthode de Newton parmi les exemples d'algorithmes (partie « Variations et courbes représentatives des fonctions », « en se limitant à des cas favorables »). Elle est exclue ici selon votre consigne ; c'est à confirmer si vous voulez l'ajouter plus tard en « Pour aller plus loin ».
