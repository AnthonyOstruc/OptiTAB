# OptiTAB - Mathématiques CE2

Livre original pour la France, édition 2026-2027, réalisé à la suite des
volumes de CP et de CE1 à la demande de l’utilisateur.

## Contenu

- 36 chapitres avec manipulation, objectif, leçon et exemple guidé.
- 324 exercices progressifs et leurs corrigés expliqués.
- 6 pages de méthode supplémentaires et une page de graphique à construire.
- 5 bilans : 30 questions avec corrigés.
- 360 problèmes oraux pour l’adulte, répartis sur 36 semaines.
- Tableaux de numération, cartes à découper, tables et faits utiles.
- Bandes de fractions, règles en fractions d’unité et monnaie de jeu.
- Horloges, quadrillage, papier pointé, axes de symétrie et matériel de solides.
- Sommaire cliquable, signets et allers-retours entre exercices et corrigés.

## Progression et sources

Les rubriques CE2 du programme du cycle 2 publié le 31 octobre 2024 ont
été relues. Elles s’appliquent depuis septembre 2025. Le livret
d’accompagnement CE2 et les supports Repères CE2 2026 ont aussi été consultés.
Les références sont dans `modele.py` et à la fin du livre.

Les exercices et les schémas sont originaux. Les ressources officielles
servent de référence pour les compétences et les familles de tâches ; les
énoncés ne sont pas présentés comme des sujets officiels. Le volume est
indépendant et ne porte aucun label ministériel.

Quelques repères de conception :

- Nombres supérieurs à 1 000 dès P1, jusqu’à 10 000 au plus tard en P2.
- Fractions d’un tout dès P1 et fractions d’unité de longueur à partir de P3.
- Fractions au plus égales à 1 et dénominateurs au plus égaux à 12.
- Comparaison à numérateur égal, dénominateur égal ou avec un dénominateur multiple de l’autre.
- Opérations sur des fractions avec mêmes dénominateurs ou dénominateurs liés par un multiple.
- Multiplication posée à un et deux chiffres introduite au plus tard en P4.
- Sens de la division et symbole ÷, sans division posée.
- Prix à virgule dès P1 ; addition posée des prix au plus tard en P2, soustraction au plus tard en P4.
- Mesures sans tableau de conversion et sans écriture à virgule des longueurs, masses ou contenances.
- Périmètre par le contour et les longueurs des côtés, sans formule à mémoriser.
- Heures à la minute et durées dans une même journée.
- Symétrie par pliage, calque et report sur quadrillage.
- Données qualitatives ou numériques, échelle adaptée et problèmes de données.

## Reconstruire et vérifier

Python 3 avec `reportlab`, `pymupdf` et `pillow` ; polices Arial dans
`C:/Windows/Fonts`. Le dossier inclut les logos et les dessins communs.
La reconstruction ne dépend pas d’un autre livre ni d’une connexion réseau.

```powershell
python construire.py
python verifier.py
```

Le PDF est construit dans `build/optitab-ce2-complet.pdf` en deux passes
pour stabiliser le sommaire. Les polices sont incorporées et les figures
sont vectorielles.

Le vérificateur contrôle les calculs déclarés, les égalités numériques
détectées avec calcul rationnel exact, les réponses de la banque orale,
les séries de fluence, les liens, les débordements et les chevauchements
de blocs de texte. Les figures sont rendues séparément pour vérifier leur
cadrage. Toutes les pages sont rendues et regroupées en planches.

La vérification automatique ne prouve pas les activités ouvertes ni
l’efficacité pédagogique. Une relecture visuelle reste nécessaire après
toute modification. `livrer.py` exige une relecture consignée avec la même
empreinte SHA-256 avant de copier le PDF dans `output/pdf/`.

## Impression

A4, 100 %, sans ajustement. Vérifier le repère de 5 cm avant de mesurer.
Photocopier le matériel. L’unité u des règles de fractions vaut 4 cm.
Les grandes constructions se réalisent sur une feuille séparée.
Les réponses de la banque orale sont réservées à l’adulte.

La soustraction emploie la méthode par échanges. L’enseignant adapte
l’utilisation du livre à l’algorithme commun retenu dans son école.
