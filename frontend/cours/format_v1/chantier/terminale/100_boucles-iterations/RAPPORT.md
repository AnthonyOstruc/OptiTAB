# Rapport : Terminale, notion 100, ex « Boucles / Itérations »

## Finition 2026-11-02

**État : prêt.** Le cours 104, la fiche 36 et **12 exercices** (les 5 existants réécrits de zéro, 7 ajoutés) sont au format v1. La notion est réorientée vers les **algorithmes cités par le programme de Terminale spécialité** (BO spécial n° 8 du 25 juillet 2019).

**Titre proposé pour la notion (à renommer en base) : « Algorithmes du programme de Terminale »**. C'est le titre du cours ; la fiche s'intitule « Résumé : Algorithmes du programme de Terminale ». L'aperçu affiche encore « Boucles / Itérations », qui est le nom en base.

L'ancien rapport (version du 28/10) est conservé dans `sauvegardes/finition_20261102/RAPPORT_ancien.md`.

### Programme vérifié sur le texte officiel

J'ai téléchargé l'annexe du BO et relu chaque rubrique « Exemples d'algorithme ».

- **La méthode de Newton est citée** dans la partie « Continuité des fonctions d'une variable réelle » : « Méthode de dichotomie. Méthode de Newton, méthode de la sécante. » Elle est donc **traitée** : cours et exercice nouveau-1.
- Les autres exemples sont cités dans une remarque du bilan : méthode de la sécante, algorithme de Briggs, méthode d'Euler pour y′ = ay + b, méthodes des milieux et des trapèzes, Monte-Carlo, planche de Galton. La marche aléatoire est traitée dans la notion 99.

| Partie | Ce qui est traité |
|---|---|
| Suites | terme u_n, somme, seuil (`while`), suite majorée dont le seuil n'est jamais dépassé (démonstration par récurrence, garde-fou) |
| Continuité (TVI) | dichotomie, avec le nombre de tours en fonction de la précision ; méthode de Newton, avec la démonstration de la formule par la tangente |
| Calcul intégral | rectangles à gauche et à droite, encadrement, et S − s = (b − a)(f(a) − f(b))/n |
| Exp et ln | seuils obtenus par l'algorithme puis démontrés par le calcul |
| Probabilités | schéma de Bernoulli, loi binomiale, fréquences comparées à P(X = k), plus petit k tel que P(X ≤ k) ≥ a, surréservation, échantillons et loi des grands nombres, σ/√n, Bienaymé-Tchebychev |
| Dénombrement | triangle de Pascal (génération de listes), parties à 2 et 3 éléments |

Les boucles et les conditions ne sont plus que des outils, avec un rappel bref. Les listes renvoient à la notion 99. **Retirés** car purement informatiques : `break`, `continue`, l'organigramme, les boucles imbriquées « gratuites » et le parcours de chaînes.

### Texte
- **Cours réécrit de zéro** en 8 parties. Chaque algorithme est accompagné de sa méthode, du programme, de l'affichage réel, de la vérification mathématique et des erreurs fréquentes. Le cours se termine par un bilan, les pièges et un « À retenir ».
- **Fiche réécrite** : des tableaux et listes courts, un programme de seuil, la formule de Newton, les sommes des rectangles et 5 pièges.
- **Exercices existants réécrits** (Id conservés, titres changés) :
  - 832 : « Découverte - Terme et somme d'une suite récurrente »
  - 831 : « Entraînement - Algorithme de seuil et logarithme »
  - 835 : « Problème - Une suite majorée qui ne dépasse jamais un seuil »
  - 833 : « Entraînement - Méthode de dichotomie »
  - 834 : « Entraînement - Simuler un schéma de Bernoulli et une loi binomiale »
- **Exercices ajoutés** :
  - nouveau-1 : « Entraînement - Méthode de Newton » (√2)
  - nouveau-2 : « Entraînement - Méthode des rectangles » (∫x², valeur exacte 1/3)
  - nouveau-3 : « Découverte - Seuils avec l'exponentielle et le logarithme »
  - nouveau-4 : « Problème - Surréservation et loi binomiale »
  - nouveau-5 : « Entraînement - Simuler des échantillons et leurs moyennes »
  - nouveau-6 : « Entraînement - Triangle de Pascal et parties d'un ensemble »
  - nouveau-7 : « Type examen - Suite récurrente, fonction et algorithme »
- Les niveaux sont répartis ainsi : 2 Découverte, 7 Entraînement, 2 Problème, 1 Type examen. Chaque corrigé suit le modèle méthode, étapes, résultat encadré, avec une erreur fréquente quand elle est utile.
- **Erreurs repérées par relecture et corrigées** :
  - le texte disait « les dix premières décimales ne bougent plus » au 4e tour de Newton ; seules les neuf premières sont exactes ;
  - ln(149 995)/ln 4 ≈ 8,60 (et non 8,59) ;
  - u₉ ≈ 76,89 (et non 76,88), dans la notion 99.

### Code exécuté (`verif_algorithmes.py`, moteur commun `moteur_verif.py`, journal `verif_log.txt`)
- **46 programmes exécutés pour de vrai et 36 affichages identiques à l'exécution.** Les 6 programmes à compléter (« … ») ne sont pas exécutés ; leur version complète, dans le corrigé, l'est.
- Les affichages ont été écrits par l'exécution elle-même (option `--remplir`), puis relus. Le texte qui les commente a été accordé aux valeurs réelles.
- **Graine fixe** : chaque simulation contient `seed(2026)`, et le texte explique son rôle aux élèves. Le script **refuse** tout programme qui consomme du hasard sans graine.
- Le script vérifie aussi les largeurs sur téléphone : au plus 35 caractères par ligne au premier niveau, 31 dans un encadré et 29 dans une étape. Il détecte aussi les boucles sans fin.
- **80 contrôles mathématiques** avec sympy et en valeurs exactes : termes, formes explicites, seuils, ln, signes de la dichotomie, itérés de Newton, sommes des rectangles exactes, loi binomiale, surréservation (211 billets ; k = 199), Bienaymé-Tchebychev, Pascal, suite u_{n+1} = 4u_n/(u_n + 1).
- Les boucles annoncées comme infinies (seuil(10), seuil(7)) ont été rejouées en flottants au-delà de 10⁶ tours.

### Figures (29 neuves, 31 emplacements)
- Les 4 anciennes figures sont supprimées : organigramme, seuil des puissances, grille de dés et ancienne dichotomie. La notion n'avait aucune image en ligne : rien n'est conservé.
- **Cours (6)** :
  - termes et seuil, avec la limite jamais atteinte ;
  - dichotomie sur la courbe, avec les intervalles des tours 0 à 4 ;
  - Newton, avec les tangentes en x₀ et x₁ ;
  - rectangles sous 1/x ;
  - histogramme de la simulation binomiale, lu dans l'affichage réel du cours ;
  - triangle de Pascal.
- **Fiche (2)** : seuil et rectangles.
- **Exercices** : une figure dans l'énoncé et sa version complétée en vert dans le corrigé pour 831, 835, 833, 834, nouveau-1 à nouveau-7. 832 a une figure dans le corrigé seulement : la limite.
- **Simulations** : les figures 834, nouveau-5 et cours exécutent le programme imprimé, avec la même graine. La figure ne peut donc pas diverger du texte.
- Le détecteur ne signale aucun texte sur un trait. Toutes les figures font au plus 900 px.
- **Chaque PNG a été regardé.** 9 figures ont été refaites après relecture :
  - dichotomie : axes en bas, car les graduations étaient sur la courbe ;
  - Newton : vues zoomées ;
  - seuil 1 : zoom ;
  - suite majorée : étiquettes ;
  - Pascal : flèches visibles ;
  - histogramme des moyennes : intervalle sous l'axe.

### Contrôles
- `verifier_notion.py --navigateur` : **OK, 0 problème** (`verif_navigateur_log.txt`).
- `controle_apercu.mjs` avec captures : aucun problème (`captures_log.txt`). Les deux outils se sont terminés normalement.
- **Captures téléphone regardées** : le cours en entier (9 écrans), la fiche, et les étapes de 835, nouveau-5 et nouveau-7.
- **Corrections faites après relecture, non détectées par l'outil** :
  - chaînes d'équivalences en ligne coupées (capital à 3 %, décroissance exponentielle) : passées en `aligned` ;
  - sommes des rectangles et forme explicite passées en formules centrées ;
  - tableau bilan à 3 colonnes tronqué : 2 colonnes ;
  - tableau de la fiche avec du code coupé : liste ;
  - 6 formules longues des exercices passées en formules centrées.

### Remarques pour l'orchestrateur
- **À renommer en base** : la notion 100 devient « Algorithmes du programme de Terminale ».
- **7 exercices à créer** à l'import (`nouveau-1` à `nouveau-7`) ; leurs figures sont dans `correspondance.json`.
- **Défaut du contrôleur**, déjà signalé pour 161 et 163 :
  - une formule en ligne trop large (chaîne de ⟺) est coupée sur téléphone sans alerte ;
  - un tableau dont les cellules contiennent du code non sécable (`white-space: nowrap`) est tronqué sans alerte dans le cours.
- Fichiers ajoutés dans le dossier : `moteur_verif.py`, partagé par copie avec la notion 99, et `verif_algorithmes.py`, qui remplace `verif_boucles.py`, obsolète et supprimé.
