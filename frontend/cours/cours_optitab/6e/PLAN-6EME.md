# Classe de 6e — Mathématiques OptiTAB

Mise à jour du 27 octobre 2026, suivant l'organisation des classes de 3e et 5e du site.

21 cours, 21 fiches de synthèse et 441 exercices paramétrés à partir de scénarios
pédagogiques, soit 2 646 questions. Chaque chapitre comprend sept Découvertes,
sept Entraînements et sept Problèmes ; chaque exercice possède six questions
reliées, une méthode expliquée pour chaque réponse, un résultat et une note à
retenir. Les figures d'énoncé sont bleues ; des corrections annotées sont ajoutées
lorsqu'elles aident à comprendre la démarche.

## Programme de référence

Les cours et leurs figures sont adaptés du livre OptiTAB de Sixième existant
(`livre/livre-maths/livre-sixieme`). Le programme est celui du cycle 3 publié au
[BO du 17 avril 2025](https://www.education.gouv.fr/bo/2025/Hebdo16/MENE2504620A),
applicable en Sixième depuis la rentrée 2025.

La progression respecte notamment les limites suivantes : division décimale par
un entier inférieur à 10, recherche d'inconnues avec des schémas et des calculs
à trous, proportionnalité par passage à l'unité sans produit en croix, volume
en cm³ par dénombrement de cubes, instructions et répétitions simples.

| N° | Slug | Chapitre |
|---|---|---|
| 1 | numeration | Entiers et décimaux |
| 2 | reperage | Repérer, comparer et arrondir |
| 3 | calcul-decimal | Calculer avec les décimaux |
| 4 | division | Diviser et interpréter un partage |
| 5 | fraction-quotient | Les fractions comme nombres |
| 6 | calcul-fractions | Comparer et calculer des fractions |
| 7 | pourcentages | Proportions et pourcentages |
| 8 | prealgebre | Chercher des inconnues et des régularités |
| 9 | proportionnalite | Proportionnalité et échelles |
| 10 | longueurs | Longueurs et périmètres |
| 11 | aires | Comparer et mesurer des aires |
| 12 | durees | Horaires et durées |
| 13 | distances-cercles | Droites, distances et cercles |
| 14 | mediatrice | Médiatrice et équidistance |
| 15 | angles | Angles et bissectrices |
| 16 | triangles | Triangles et cercle circonscrit |
| 17 | symetrie-axiale | Symétrie axiale |
| 18 | solides-volumes | Solides, assemblages et volumes |
| 19 | donnees | Données et enquêtes |
| 20 | probabilites | Comprendre le hasard |
| 21 | instructions | Instructions, répétitions et chemins |

## Fichiers

- Cours : `cours_<slug>_6e.txt`, avec les figures dans `images/`.
- Fiches : `frontend/cours/resume/6e/resume_<slug>_6e.txt`.
- Exercices : `frontend/exercices/6e/exercice_<slug>_6e.txt` et leurs `images/`.
- Sources des scénarios : `sources/` ; figures et composition : `outils/`.
- Contrôles, empreintes des fichiers et rapports : `verifications/`.

Le **manifeste** `verifications/manifeste.json` définit les 21 chapitres de cette
édition. Les anciens cours non réutilisés restent présents dans le dépôt ; les
quatre fichiers remplacés sont conservés dans `archives/`. Ils ne font pas partie
du manifeste et ne sont pas importés avec l'édition actuelle.

## Construire et vérifier

Depuis la racine du dépôt :

```powershell
python -u -X utf8 frontend/cours/cours_optitab/6e/outils/construire_6e.py all
python -X utf8 frontend/cours/cours_optitab/6e/verifications/verifier_calculs.py
python -X utf8 frontend/cours/cours_optitab/6e/outils/valider_6e.py all
node frontend/cours/cours_optitab/6e/outils/verifier_mathjax.cjs all
node frontend/cours/cours_optitab/6e/outils/verifier_rendu.cjs
python -X utf8 frontend/cours/cours_optitab/6e/verifications/planches.py
```

Le rendu utilise les formateurs du site et MathJax. Il contrôle 84 vues : cours
et dernier problème de chaque chapitre sur ordinateur et sur téléphone, ainsi
que des captures supplémentaires de corrigés pour la relecture. Les contrôles
de calcul et de structure soutiennent la relecture sans prétendre prouver toutes
les explications en langage naturel.

## Intégrer au site

Le niveau France / 6ème utilise l'identifiant 14. Les identifiants des anciennes
notions sont réutilisés quand leur contenu correspond à la nouvelle progression.
Les anciennes notions regroupées sont désactivées après l'import complet ; leurs
données sont conservées. `verifications/avant-integration.json` conserve l'état
des notions, cours et thèmes antérieur à cette mise à jour.

Le chapitre Entiers et décimaux, sa fiche et les deux premiers exercices forment
la découverte gratuite du niveau. Les autres contenus suivent l'accès habituel
du site. Le niveau est actif dès l'intégration du premier chapitre.

Depuis `backend/` :

```powershell
$env:PYTHONUTF8='1'
.\venv\Scripts\python.exe manage.py shell -c "import runpy; m=runpy.run_path(r'../frontend/cours/cours_optitab/6e/outils/integrer_6e.py'); m['main']()"
```

La configuration Django locale utilise la base et le stockage du site en
production. L'import est idempotent ; les noms des images incluent leur empreinte.
Le rapport `verifications/integration.json` consigne les identifiants effectivement
créés ou mis à jour après un import complet.
