# Classe de 3ème sur OptiTAB — état et mode d'emploi

> Niveau **3ème** (France) en ligne depuis le 27/10/2026 : Pays → Niveau → Matière → Thème → Notion → Cours / Exercices / Fiches.
> Contenu adapté du livre OptiTAB de 3ème (`livre/livre-maths/livre-troisieme/`).

## 1. Ce qui est en ligne

| Thème (ordre) | Notions (slug) |
|---|---|
| 1. Nombres et calculs | fractions, puissances, arithmetique, calcul-litteral, equations |
| 2. Organisation et gestion de données, fonctions | proportionnalite, fonctions, affines, statistiques, probabilites |
| 3. Grandeurs et mesures | grandeurs |
| 4. Espace et géométrie | pythagore, thales, trigonometrie, transformations, espace |
| 5. Algorithmique et programmation | algorithmique, raisonner |
| 6. Préparation au brevet | brevet (10 sujets complets + cours de méthode + fiche automatismes) |

Chaque notion : 1 cours, 1 fiche de synthèse et **21 exercices** (7 Découverte, 7 Entraînement, 7 Problème),
chacun avec au moins 4 questions, des étapes détaillées et des figures.
La notion Thalès sert de démo gratuite (cours, fiche et 2 premiers exercices).

## 2. Fichiers

| Contenu | Emplacement |
|---|---|
| Cours | `cours_<slug>_3e.txt` (ce dossier) |
| Fiches | `frontend/cours/resume/3e/resume_<slug>_3e.txt` |
| Exercices | `frontend/exercices/3e/exercice_<slug>_3e.txt` |
| Figures | `images/` (cours et fiches), `frontend/exercices/3e/images/` (exercices) |
| Générateurs de figures | `graphe/figures_chNN.py`, `graphe/figures_brevet.py` |
| Contrôles numériques | `verifications/check_chNN.py` |
| Sujets brevet (source) | `outils/brevet_sujets_a.py`, `outils/brevet_sujets_b.py` |

## 3. Modifier puis republier un chapitre

1. Modifier le fichier `.txt` (ou le générateur de figures, puis le relancer avec `python graphe/figures_chNN.py`).
2. Contrôler : `python verifications/check_chNN.py` et `python outils/valider_3e.py <slug>`.
3. Importer (depuis `backend/`) :
   `./venv/Scripts/python.exe manage.py shell -c "import sys; sys.argv=['x','<slug>']; exec(open(r'<chemin>/outils/integrer_3e.py', encoding='utf-8').read())"`

Pour les sujets brevet : modifier `outils/brevet_sujets_*.py`, lancer `python outils/brevet_3e.py`
(contrôles + écriture du fichier), puis importer avec le slug `brevet`.

⚠️ La configuration locale du backend pointe sur la base et le stockage **de production** : un import est visible immédiatement sur www.optitab.net.

## 4. Règles de rédaction propres au site

- Formules : `$\displaystyle ... $` ; saut de ligne : `$\\$`.
- Pas d'astérisque isolé (le site le transforme en italique) : `\times` dans les formules, `&#42;` dans une formule de tableur.
- Références absolues de tableur : `\$D\$2`.
- Les exercices sont triés par titre : garder la numérotation `Catégorie - Chapitre - N. Titre`.

## 5. Qualité pédagogique et tableaux

- Chaque question corrigée explique la démarche (puce « Méthode » ou « Étape ») avant le « Résultat » ;
  chaque exercice se termine par une note « 💡 À retenir » ou « ⚠️ Erreur fréquente ».
  Pour compléter un chapitre : `python outils/enrichir_3e.py lister <slug>`, écrire les méthodes dans
  `outils/methodes/<slug>.py`, puis `python outils/enrichir_3e.py appliquer <slug>`.
- Tableaux des cours et fiches : `python outils/tableaux_3e.py` applique le gabarit bordé (et le défilement sur mobile).
- Tableaux des exercices : images générées par `graphe/tableaux_exos.py` (fonction `tableau` de `fig3e.py`),
  jamais de données alignées avec des espaces.
- Le validateur refuse tout écart à ces règles.
