# OptiTAB - Mathématiques CP

Livre pédagogique original pour la France, édition 2026-2027. Créé à la
demande de l’utilisateur après consultation des livres OptiTAB existants.
Les CE1 et CE2 ne font pas partie de cette livraison.

## Contenu

- 30 chapitres, avec manipulation, leçon, exemple et entraînement.
- 270 exercices numérotés, avec leurs corrigés expliqués.
- Une méthode supplémentaire pour chercher la moitié d’un nombre pair.
- 5 bilans comprenant 30 questions et leurs corrigés.
- 360 problèmes oraux répartis sur 36 semaines, réservés à l’adulte.
- Fiches outils, monnaie de jeu, horloges, formes, faces de cube et quadrillage.
- Sommaire cliquable, signets et liens entre exercices et corrigés.
- Références officielles et correspondances avec les domaines du CP.

Les exercices, les bilans et les schémas sont des créations originales.
Ils ne sont pas présentés comme des sujets officiels ou validés par le
ministère. Le texte officiel du cycle 2 publié le 31 octobre 2024 et les
ressources Éduscol ont été consultés le 23 octobre 2026. Les liens sont
dans `modele.py` et à la fin du livre.

## Construction

Python 3 avec `reportlab`, `pymupdf` et `pillow` ; polices Arial présentes
dans `C:/Windows/Fonts`. Les logos de la collection sont inclus dans
`images`. Aucun autre livre n’est nécessaire dès que ce dossier est
copié avec ses images.

```powershell
python construire.py
python verifier.py
```

Le PDF construit est `build/optitab-cp-complet.pdf`. La construction en
deux passes stabilise le sommaire. Les dessins sont vectoriels et les
polices sont incorporées. Aucune connexion n’est requise pour reconstruire.

Le vérificateur contrôle les calculs explicitement déclarés, les égalités
numériques détectées, les renvois, les caractères, les blocs de texte et
le cadre réel de chaque figure. Il rend toutes les pages et crée des
planches de contrôle dans `build/qa`. Il ne prétend pas démontrer
automatiquement toutes les réponses graphiques ou toutes les décisions
pédagogiques. Une relecture visuelle reste nécessaire après une modification.

## Impression

Format A4, taille réelle à 100 %, sans ajustement à la page. Un repère
de 5 cm permet de vérifier l’échelle. Les pages de matériel sont à
photocopier pour conserver le livre. Les résultats des problèmes oraux
sont imprimés sur les pages de l’adulte : ces pages ne sont pas destinées
à être distribuées comme fiches d’évaluation.

Les nombres et résultats du parcours restent entre 0 et 100. Les problèmes
en deux étapes ainsi que les problèmes multiplicatifs ou de partage
restent dans le champ jusqu’à 30. Les heures sont entières et la monnaie
est exprimée en euros entiers. Les repères de période sont à utiliser
avec l’enseignant et en fonction des acquis de l’enfant.
