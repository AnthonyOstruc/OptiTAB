# Classe de 5e — Mathématiques OptiTAB

Création du 27 octobre 2026, sur le modèle des contenus de 3e du site.

20 cours, 20 fiches de synthèse et 420 exercices, répartis en 7 Découvertes,
7 Entraînements et 7 Problèmes par chapitre. Chaque exercice comporte six
questions reliées, leur démarche expliquée, leur résultat et une note pédagogique.
Les 2 520 questions traitent des situations complètes : budgets, partages,
recettes, températures, constructions, surfaces, volumes, données et programmes.

Les scénarios ont plusieurs jeux de données, avec calcul exact et figures
reproductibles. Les paramètres sont conservés dans les sources Python ; les
fichiers `.txt` sont les livrables importables dans le site.

## Programme et progression

Les cours sont adaptés du livre OptiTAB de Cinquième existant, édition revue
le 23 octobre 2026, et de ses figures TikZ. Le programme de référence est
l'annexe 2 du [BO du 5 mars 2026](https://www.education.gouv.fr/bo/2026/Hebdo10/MENE2602912A),
applicable en 5e depuis la rentrée 2026.

| N° | Fichier / slug | Chapitre |
|---|---|---|
| 1 | operations | Opérations et priorités |
| 2 | divisibilite | Multiples, diviseurs et partages |
| 3 | relatifs | Découvrir les nombres relatifs |
| 4 | sommes-relatifs | Additionner et soustraire des relatifs |
| 5 | fractions | Fractions, quotients et comparaisons |
| 6 | additions-fractions | Additionner et soustraire des fractions |
| 7 | carres-cubes | Carrés et cubes |
| 8 | formules | Lettres, formules et motifs |
| 9 | distributivite | Développer, réduire et démontrer |
| 10 | equations | Inconnues et équations simples |
| 11 | proportionnalite | Proportionnalité et pourcentages |
| 12 | reperage | Repérage et grandeurs en fonction d’une autre |
| 13 | angles | Angles et droites parallèles |
| 14 | triangles | Construire et comprendre les triangles |
| 15 | symetries | Symétries et demi-tour |
| 16 | parallelogrammes | Parallélogrammes et aires |
| 17 | espace | Solides, disques et volumes |
| 18 | statistiques | Organiser et interpréter des données |
| 19 | probabilites | Hasard et probabilités |
| 20 | programmation | Penser et programmer par blocs |

La programmation reste dans le périmètre de 5e : lecture d'une donnée saisie,
expression d'une formule, séquence d'instructions et boucle inconditionnelle.
Les propriétés de géométrie précisent les données utilisées ; les cours du livre
distinguent les propriétés démontrées et les propriétés admises.

## Fichiers et reconstruction

- Cours : `cours_<slug>_5e.txt`, avec les figures dans `images/`.
- Fiches : `frontend/cours/resume/5e/resume_<slug>_5e.txt`.
- Exercices : `frontend/exercices/5e/exercice_<slug>_5e.txt`, figures dans `images/`.
- Scénarios : `sources/nombres.py`, `algebre.py`, `geometrie.py`, `donnees.py`, `variantes.py`.
- Construction, images et import : `outils/`.
- Rapports de calcul, manifeste et contrôle visuel : `verifications/`.

Depuis la racine du dépôt, avec Python, SymPy, Matplotlib, Pillow, PyMuPDF,
LuaLaTeX et les dépendances Node déjà utilisées par la collection :

```powershell
python -X utf8 frontend/cours/cours_optitab/5e/outils/construire_5e.py all
python -X utf8 frontend/cours/cours_optitab/5e/verifications/verifier_calculs.py
python -X utf8 frontend/cours/cours_optitab/5e/outils/valider_5e.py all
node frontend/cours/cours_optitab/5e/outils/verifier_rendu.cjs
```

Le vérificateur MathJax `outils/verifier_mathjax.cjs` accepte la liste des
fichiers `.txt`. Le contrôle visuel réutilise les formateurs du site et produit
80 vues : cours et dernier problème de chaque chapitre, sur ordinateur et mobile.
Les captures servent à la relecture ; elles ne remplacent pas la vérification
mathématique des sources.

## Intégration au site

Le script `outils/integrer_5e.py` retrouve le niveau France / 5ème, crée les cinq
thèmes, les 20 notions, leurs cours, exercices, fiches et images, puis active le
niveau seulement après contrôle des totaux. Il utilise le même rattachement à
la matière Mathématiques que la 3e. Les cartes affichent le titre de la notion.

L'intégration est idempotente et ne supprime aucun contenu existant. Un nom de
figure contient un SHA-256 partiel : une image modifiée ne réutilise pas un ancien
fichier en cache. Le cours Opérations, sa fiche et les deux premiers exercices
servent de découverte gratuite, comme le chapitre de démonstration en 3e.

Depuis `backend/` :

```powershell
$env:PYTHONUTF8='1'
.\venv\Scripts\python.exe manage.py shell -c "import runpy; m=runpy.run_path(r'../frontend/cours/cours_optitab/5e/outils/integrer_5e.py'); m['main']()"
```

La configuration locale Django utilise la base et le stockage du site en
production. Le rapport `verifications/integration.json` est écrit après une
intégration terminée et indique les identifiants effectivement créés.
