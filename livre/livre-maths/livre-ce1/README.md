# OptiTAB - Mathématiques CE1

Livre original pour la France, édition 2026-2027, réalisé après le livre
de CP à la demande de l’utilisateur. Le CE2 reste une étape ultérieure.

## Contenu

- 32 chapitres : découverte, manipulation, leçon, exemple et exercices.
- 288 exercices avec leurs corrigés expliqués.
- 5 bilans, soit 30 questions avec corrigés.
- 360 problèmes oraux pour l’adulte, répartis sur 36 semaines.
- Matériel à découper, fiches de référence et fiches d’observation de la fluence.
- Sommaire, signets et renvois entre les exercices et leurs corrigés.

La progression couvre les nombres jusqu’à 1 000, les opérations et tables,
les fractions d’un tout, les problèmes en une ou deux étapes, les mesures,
la monnaie, l’heure et les durées, la géométrie et les données.

Les fractions sont au plus égales à 1, avec les dénominateurs du CE1 :
2, 3, 4, 5, 6, 8 et 10. Les calculs de fractions utilisent un même
dénominateur. Les comparaisons portent sur des dénominateurs égaux ou
des numérateurs égaux à 1. L’écriture à virgule est employée pour les
prix ; les longueurs utilisent cm, m et km et les masses g et kg.

Le programme du cycle 2 publié le 31 octobre 2024, le livret
d’accompagnement CE1 et les supports Repères CE1 2026 ont été consultés.
Les ressources sont référencées dans `modele.py` et à la fin du livre.
Les cours, exercices et dessins sont originaux. Le livre ne présente
aucun exercice comme un sujet officiel et n’a pas de label ministériel.

## Reconstruire

Python 3 avec `reportlab`, `pymupdf` et `pillow` ; polices Arial dans
`C:/Windows/Fonts`. Le dossier inclut ses logos et les schémas communs
à la collection. Aucun autre livre ni connexion réseau ne sont nécessaires.

```powershell
python construire.py
python verifier.py
```

Le PDF est construit dans `build/optitab-ce1-complet.pdf`. Deux passes
stabilisent les numéros de page du sommaire. Les polices sont incorporées
et les schémas sont vectoriels.

`verifier.py` contrôle les calculs déclarés, les égalités détectées,
les réponses de la banque orale, les liens, les blocs de texte et le
cadrage réel des figures. Il rend toutes les pages et crée des planches
dans `build/qa`. Une relecture visuelle reste nécessaire après modification.
Les activités ouvertes et la pertinence pédagogique ne sont pas prouvées
formellement par le script.

## Impression et usage

Imprimer en A4 à 100 %, sans ajustement. Vérifier le repère de 5 cm.
Photocopier le matériel pour conserver le livre. Les problèmes oraux et
leurs réponses sont réservés à l’adulte. Les tracés qui demandent une
feuille personnelle peuvent être réalisés sur les annexes quadrillées,
pointées ou sur du papier uni.

La soustraction par échanges est utilisée dans ce volume. L’enseignant
adapte son utilisation à l’algorithme commun retenu dans son école.
