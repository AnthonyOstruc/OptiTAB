# Première : corrections à la suite de l’audit

Révision du 21 octobre 2026. Le livre corrigé conserve ses 317 pages.
Le classeur fourni est conservé sans modification.

## Neuf anomalies traitées

Les neuf observations ont été reproduites dans le PDF initial. Elles concernaient
douze signes moins mathématiques U+2212 dans des blocs de code. Les fichiers
sources contenaient déjà le signe Python ASCII U+002D. Le style du livre
transformait ce caractère pendant la composition ; il conserve désormais le
caractère ASCII dans les programmes et les sorties de console.

Les numéros ci-dessous désignent les pages physiques du PDF. La pagination du
livre est inférieure d’une unité.

| ID | Passage | PDF initial | PDF corrigé | Code corrigé |
| --- | --- | ---: | ---: | --- |
| 1 | Énoncé 12.1 | 123 | 123 | `b = a - b ; a = a - b` |
| 2 | Corrigé 5.12 | 207 | 207 | `exp(-0.1*t)` |
| 3 | Corrigé 11.12 | 257 | 257 | `return -1` |
| 4 | Corrigé 11.13 | 258 | 258 | `abs(m - 0.4)` |
| 5 | Corrigé 12.3 | 260 | 260 | `return x**2 - 3*x + 2` |
| 6 | Corrigé 12.11 | 264 | 264 | `return mu, carre - mu**2` |
| 7 | Corrigé 12.12 | 264 | 264 | `L.append(L[-1] + L[-2])` |
| 8 | Défi D05 D05 | 288 | 288 | `(1 - 1 / (2 * n)) ** (-n)` |
| 9 | Défi D12 D12 | 301 | 301 | `m ** 3 + m - 1 < 0` |

## Précision pédagogique

Dans le corrigé 12.11, les hypothèses de la fonction de calcul des moments sont
explicitées : listes non vides, même longueur, une probabilité par valeur,
probabilités positives ou nulles dont la somme vaut 1.

Les explications des huit autres passages ont été relues. Les seuils, cas limites,
résultats numériques et fonctions concernés par les neuf observations ont été
recontrôlés.

## Vérifications

- Les 27 programmes sont extraits du PDF compilé, et pas seulement des sources.
  Leur indentation est reconstruite depuis les positions des glyphes, sans
  remplacer aucun opérateur. Leur syntaxe est valide, leur structure syntaxique
  est identique à celle des sources et tous ont été exécutés.
- Les tests du code extrait couvrent notamment l’échange des variables, le
  refroidissement à la minute 13, les seuils de simulation, les 470 moyennes sur
  500 pour la graine 2026, les moments, Fibonacci, les bornes exponentielles et
  la dichotomie.
- Les 219 groupes de contrôles des 210 exercices, les 356 contrôles des
  compléments, les 85 contrôles de structure et de calcul, les 350 contrôles
  géométriques et les 2 799 contrôles de relecture passent.
- Les 317 pages sont rendues. La comparaison de tous les pixels à 80 dpi
  montre 309 pages identiques. Les huit pages modifiées sont relues ; la page
  264 est également contrôlée en grand avec Poppler. Aucun texte ne sort des
  pages et les renvois sont stabilisés.

Cette révision traite toutes les observations de l’audit fourni. Les contrôles
de résultats soutiennent la relecture ; ils ne constituent pas une certification
formelle de toutes les sous-questions du livre.

Empreinte SHA-256 du PDF corrigé : `709979da6b0219bfb068e55eb13dac906075a14dc09e57867229bc086412e0a4`.
