# Classe de 4ème sur OptiTAB — Plan complet et suivi

> Objectif : ajouter la classe **4ème** (France) au site, sur le modèle de la 3ème :
> Pays → Niveau → Matière → Thème → Notion → Cours / Exercices / Fiches.
> Contenu adapté du livre OptiTAB de 4ème, édition 2026-2027 (`livre/livre-maths/livre-quatrieme/`),
> programme de cycle 4 en vigueur en 2026-2027 (le nouveau programme de 4ème n'entre en vigueur qu'en 2027-2028).

## Règles de qualité (demande du 2026-10-27)

- **21 exercices par chapitre** : 7 Découverte (easy), 7 Entraînement (medium), 7 Problème (hard).
- **Chaque exercice est un problème entier d'au moins 6 questions** qui s'enchaînent.
- **Corrigés pédagogiques** : pour chaque question, Méthode et/ou étapes expliquées en mots,
  Résultat, et selon les cas 🔎 Vérification, ✍️ Rédaction modèle, 💡 À retenir, ⚠️ Erreur fréquente
  (au moins une note pédagogique par exercice).
- **Schémas et figures** partout où ils aident : figures d'énoncé, figures de correction annotées
  en vert, tableaux de données dessinés (lisibles sur mobile), droites graduées, graphiques.
- **Zéro erreur** : chaque résultat numérique est recalculé (`verifications/check_chNN.py`),
  chaque formule est compilée avec MathJax 3 (`outils/verifier_mathjax.cjs`), le format est validé
  (`outils/valider_4e.py`).

## Les 5 thèmes et les 18 notions

| N° | slug | Notion (titre sur le site) | Thème |
|---|---|---|---|
| 1 | relatifs | Calculer avec les nombres relatifs | Nombres et calculs |
| 2 | fractions | Fractions et nombres premiers | Nombres et calculs |
| 3 | puissances | Puissances et notation scientifique | Nombres et calculs |
| 4 | racines | Carrés et racines carrées | Nombres et calculs |
| 5 | calcul-litteral | Calcul littéral et distributivité | Nombres et calculs |
| 6 | equations | Équations et résolution de problèmes | Nombres et calculs |
| 7 | proportionnalite | Proportionnalité et pourcentages | Organisation et gestion de données, fonctions |
| 8 | grandeurs | Grandeurs composées et unités | Grandeurs et mesures |
| 9 | graphiques | Relier des grandeurs et lire des graphiques | Organisation et gestion de données, fonctions |
| 10 | statistiques | Statistiques et diagrammes | Organisation et gestion de données, fonctions |
| 11 | probabilites | Probabilités | Organisation et gestion de données, fonctions |
| 12 | triangles | Construire et comparer des triangles | Espace et géométrie |
| 13 | pythagore | Théorème de Pythagore | Espace et géométrie |
| 14 | thales | Théorème de Thalès (triangles emboîtés) | Espace et géométrie |
| 15 | cosinus | Cosinus dans le triangle rectangle | Espace et géométrie |
| 16 | translations | Translations, agrandissements et réductions | Espace et géométrie |
| 17 | espace | Pyramides, cônes et volumes | Espace et géométrie |
| 18 | programmation | Algorithmique et programmation | Algorithmique et programmation |

## Fichiers

| Contenu | Emplacement |
|---|---|
| Cours | `frontend/cours/cours_optitab/4e/cours_<slug>_4e.txt` (+ `images/`) |
| Fiches de synthèse | `frontend/cours/resume/4e/resume_<slug>_4e.txt` (images du dossier cours) |
| Exercices (générés) | `frontend/exercices/4e/exercice_<slug>_4e.txt` (+ `images/`) |
| Sources des exercices | `4e/sources/exos_<slug>_4e.src` (format compact, voir `outils/construire_4e.py`) |
| Figures | `4e/graphe/fig4e.py` (module partagé) + `figures_chNN.py` |
| Contrôles de calcul | `4e/verifications/check_chNN.py` |

## Chaîne de production d'un chapitre

```
python graphe/figures_chNN.py                 # figures
python verifications/check_chNN.py            # tous les résultats recalculés
python outils/construire_4e.py <slug>         # source -> fichier d'exercices du site
python outils/valider_4e.py <slug>            # format, 6 questions, corrigés, images
node outils/verifier_mathjax.cjs <fichiers>   # chaque formule compilée par MathJax
```

## Suivi

| N° | slug | Figures | Cours | Fiche | Exercices | Contrôles | Validé |
|---|---|---|---|---|---|---|---|
| 1 | relatifs | ✅ 20 | ✅ | ✅ | ✅ 21 exos / 132 q. | ✅ | ✅ en ligne (notion 249) |
| 2 | fractions | ✅ 21 | ✅ | ✅ | ✅ 21 exos / 131 q. | ✅ | ✅ en ligne |
| 3 | puissances | ✅ 12 | ✅ | ✅ | ✅ 21 exos / 127 q. | ✅ | ✅ en ligne |
| 4 | racines | ✅ 15 | ✅ | ✅ | ✅ 21 exos / 128 q. | ✅ | ✅ en ligne |
| 5 | calcul-litteral | ✅ 14 | ✅ | ✅ | ✅ 21 exos / 127 q. | ✅ | ✅ en ligne |
| 6 | equations | ✅ 12 | ✅ | ✅ | ✅ 21 exos / 130 q. | ✅ | ✅ en ligne |
| 7 | proportionnalite | ✅ 10 | ✅ | ✅ | ✅ 21 exos / 129 q. | ✅ | ✅ en ligne |
| 8 | grandeurs | ✅ 11 | ✅ | ✅ | ✅ 21 exos / 127 q. | ✅ | ✅ en ligne |
| 9 | graphiques | ✅ 27 | ✅ | ✅ | ✅ 21 exos / 128 q. | ✅ | ✅ en ligne |
| 10 | statistiques | ✅ 18 | ✅ | ✅ | ✅ 21 exos / 126 q. | ✅ | ✅ en ligne |
| 11 | probabilites | ✅ 18 | ✅ | ✅ | ✅ 21 exos / 126 q. | ✅ | ✅ en ligne |
| 12 | triangles | ✅ 20 | ✅ | ✅ | ✅ 21 exos / 126 q. | ✅ | ✅ en ligne |
| 13 | pythagore | ✅ 23 | ✅ | ✅ | ✅ 21 exos / 126 q. | ✅ | ✅ en ligne |
| 14 | thales | ✅ 45 | ✅ | ✅ | ✅ 21 exos / 126 q. | ✅ | ✅ en ligne |
| 15 | cosinus | ✅ 43 | ✅ | ✅ | ✅ 21 exos / 126 q. | ✅ | ✅ en ligne |
| 16 | translations | ✅ 41 | ✅ | ✅ | ✅ 21 exos / 126 q. | ✅ | ✅ en ligne |
| 17 | espace | ✅ 38 | ✅ | ✅ | ✅ 21 exos / 126 q. | ✅ | ✅ en ligne |
| 18 | programmation | ✅ 36 | ✅ | ✅ | ✅ 21 exos / 126 q. | ✅ | ✅ en ligne |
