# Guide du chantier « format OptiTAB v1 »

Mission : faire passer chaque notion du site (cours, fiche de synthèse,
exercices) au format OptiTAB v1, avec des **figures impeccables au style des
livres**. Demande du propriétaire du site (non technicien, francophone) :
« ultra propre, impeccable, professionnel ». Le chapitre pilote
(`pilote_trigo_terminale/`) a été validé par lui : c'est le **modèle de qualité**.

Lire d'abord : `FORMAT.md` (syntaxe), puis le pilote :
`pilote_trigo_terminale/cours.txt`, `fiche.txt`, `exercices.txt`,
`figures/figures.py` et quelques `figures/images/*.png`.

**Modèles les plus récents (novembre 2026, à imiter en priorité)** : un chapitre
fini = son dossier complet (cours, fiche, exercices, `figures/figures.py`,
`RAPPORT.md`). Exemples : `chantier/1ere/161_variables-aleatoires-reelles`,
`chantier/terminale/96_sommes-de-variables-aleatoires` (enrichissement),
`chantier/terminale/89_calcul-integral`, `chantier/2nde/169_resoudre-des-problemes-de-geometrie`.

**Consignes du propriétaire, en résumé** (le détail est dans les § 1, 4 et 5) :
- programme officiel du niveau ; titres de cours et fiche = intitulé officiel ;
  hors programme, faux ou faible → réécrit (« même si nécessaire de refaire de zéro ») ;
  ce qui ne sert à rien est supprimé (décision de l'orchestrateur) ;
- exercices COMPLETS et pédagogiques : énoncé + questions numérotées ; corrigé
  (`Étapes:`) = méthode, étapes détaillées, résultat encadré, erreur fréquente ;
  progression Découverte → Entraînement → Problème → Type examen/brevet/bac ;
  au moins 10 exercices par notion (sinon en ajouter, `Id: nouveau-N`) ;
  titres « Type - Sujet » sans le nom du chapitre ;
- figures style livre partout où elles aident : cours, fiche, énoncé (sans donner
  la réponse) ET corrigé (complétée en vert) ; jamais de texte sur un trait,
  rien ne déborde, lisible sur téléphone ; toutes les anciennes images refaites ;
- calculs vérifiés avec sympy, programmes Python réellement exécutés ;
- captures téléphone regardées à l'œil (formules coupées ou réduites → découper).

Orchestration (import, files d'attente) : § 8.

---

## 1. Règles absolues

1. **Aucune écriture en base, aucun import.** `backend/.env` pointe sur la
   PRODUCTION. Seul l'orchestrateur importe, après validation. N'exécuter
   aucun script via `manage.py` (même l'export : déjà fait).
2. **Ne travailler que dans le(s) dossier(s) de notion attribué(s)**
   (`chantier/<niveau>/<id>_<slug>/`). Ne modifier ni `outils/`, ni
   `frontend/src/`, ni le pilote, ni une autre notion. Un défaut d'outil ou
   du moteur d'affichage → le décrire dans le rapport (§ 7), avec un exemple.
3. Pas de `git` (ni commit, ni checkout, ni stash). Rien sur le Bureau.
   Pas de suppression par motif (`rm *.png`) : supprimer fichier par fichier,
   et seulement dans son dossier de notion.
4. **Antislashs** : écrire et modifier les fichiers LaTeX/Python/texte avec les
   outils Write / Edit, jamais avec un heredoc Bash ni `sed` (les `\f`, `\b`,
   `\n` y sont corrompus). En Python, chaînes LaTeX toujours brutes `r"…"`.
5. Exercices (consigne du propriétaire, 2026-10-29 : « fais toujours le mieux ;
   si besoin supprime ou corrige ; vérifie le programme officiel ; si tu
   supprimes des exercices, ajoute des exercices pédagogiques complets ») :
   - ne jamais changer une ligne `Id:` existante ; ne jamais retirer un bloc
     (l'historique des élèves y est rattaché) ;
   - un exercice hors programme, faux ou faible est **remplacé** dans son bloc :
     nouveau contenu complet, nouveau titre si besoin (même type en tête :
     `Découverte - …`, `Entraînement - …`, `Problème - …`), `Difficulté:` cohérente ;
   - s'il manque des exercices (notion pauvre, compétence du programme non
     travaillée), **ajouter** un bloc avec `Id: nouveau-1`, `nouveau-2`… ;
     ses figures se déclarent dans `correspondance.json` sous la clé `"nouveau-1"` ;
   - titres uniques dans la notion ; le RAPPORT liste remplacements et ajouts.
6. `convertir_notion.py` n'est lancé **qu'une fois**, au début : ensuite
   `etat.json` (statut `en_cours`) protège vos corrections.

## 2. Dossier d'une notion

```
chantier/<niveau>/<id>_<slug>/
  source_en_ligne/        export de la base (LECTURE SEULE) : cours_<id>.txt,
                          fiche_<id>.txt, exercices.txt, meta.json (ids, images)
  cours_<id>.txt          version finale v1 (en-tête « Titre: », puis <!-- optitab:1 -->)
  fiche_<id>.txt          version finale v1
  exercices.txt           version finale v1 (=== titre / Id / Difficulté / Énoncé / Étapes / Solution)
  figures/figures.py      vos figures (TikZ), compilées par outils/figures_livre.py
  figures/images/*.png    figures produites (ne pas éditer à la main)
  figures/correspondance.json   quelle figure va à quelle place (§ 5)
  images_en_ligne/, planches/   images actuelles du site et leurs planches-contacts
  apercu.html             aperçu fidèle du rendu du site (généré)
  etat.json               {"statut": "a_faire" | "en_cours" | "pret", "agent": "…", "maj": "AAAA-MM-JJ"}
  RAPPORT.md              votre compte rendu (§ 7)
```

## 3. Déroulé pour une notion

Les commandes se lancent depuis `frontend/cours/format_v1/outils/`
(préfixer Python par `PYTHONIOENCODING=utf-8` dans Bash).

1. `etat.json` → `{"statut": "en_cours", …}` (si la conversion automatique
   n'a pas encore été faite : `python convertir_notion.py <dossier>` AVANT).
2. Lire la source (`source_en_ligne/`) et la conversion (fichiers finaux).
   Repérer ce qui est cassé, laid, faux, incomplet.
3. **Réécrire / corriger le texte** (§ 4) directement dans les fichiers finaux.
4. **Images** : `python planche.py <dossier>` puis lire chaque
   `planches/planche_NN.png` (outil Read). Décider pour chaque image (§ 5).
   Écrire `figures/figures.py`, compiler, **regarder chaque PNG** (Read),
   corriger jusqu'à perfection, remplir `figures/correspondance.json`.
5. `python verifier_notion.py <dossier> --navigateur` → **0 problème**.
   Puis `node controle_apercu.mjs <dossier>/apercu.html <dossier>/captures`
   (avec captures) et regarder au moins : le cours en téléphone (toutes les
   parties), la fiche, et 3 exercices (énoncé + étapes) en téléphone.
   Laisser le dossier `captures/` en place (l'orchestrateur le nettoie).
6. `RAPPORT.md` (§ 7), puis `etat.json` → `"pret"`.

## 4. Texte : niveau d'exigence

**Consigne du propriétaire (2026-11-02) : « même si nécessaire de refaire de
zéro, tu refais ».** Un cours, une fiche ou un exercice faible, mal structuré
ou indigne d'un manuel n'est pas retouché : il est réécrit entièrement, au
programme officiel.

**Titres (consigne du 2026-11-02).** Le titre du cours et de la fiche reprend
l'intitulé du programme officiel et correspond exactement au contenu. Un
chapitre dont le contenu relève d'un autre niveau (ex. « Conditions » en
Première = programme de Seconde) est signalé dans RAPPORT.md : le
propriétaire décide de le masquer ; son contenu utile est intégré ailleurs.

Tout doit être **juste, clair, structuré, au programme** (programme
officiel en vigueur du niveau ; rien de hors programme sans le signaler
comme « Pour aller plus loin »).

**Exactitude** : vérifier CHAQUE résultat numérique, chaque calcul, chaque
tableau de variations / de signes, chaque limite, avec Python (sympy, numpy)
dans un script de vérification (`verif_<notion>.py` dans le dossier de la
notion, à garder). Une erreur de maths en ligne est inacceptable.

**Cours** (modèle : `pilote_trigo_terminale/cours.txt`) :
- `::: objectifs` en tête ; parties `## I. …`, `### …` ;
- encadrés justes : `definition`, `theoreme`, `propriete`, `methode`,
  `exemple`, `demonstration` (démonstrations du programme), `attention`
  (erreurs fréquentes), `retenir` ; formules importantes centrées `$$…$$` ;
- calculs en chaîne alignés (`aligned`), pas de pavés de texte, pas d'emoji,
  pas de couleur ni de HTML ; typographie française (« … », virgule
  décimale `{,}` dans les formules : `2{,}5`).
- Les cours de lycée ont pour la plupart été réécrits récemment (contenu bon) :
  vérifier la conversion, la structure, les figures ; les autres (anciens)
  demandent une vraie remise à niveau.

**Fiche de synthèse** : l'essentiel en 1 à 2 écrans de téléphone :
définitions / formules clés, méthodes, erreurs classiques, tableaux.

**Exercices** (modèle : `pilote_trigo_terminale/exercices.txt`) :
- `Énoncé:` contexte court + questions numérotées `1.`, `2.` (sous-questions
  `a)` en liste) ; données lisibles (tableaux en `| … |`, pas en image) ;
- `Étapes:` pour chaque question `## Question N : …` puis `::: methode`
  (une ligne : l'idée), `::: etape Titre` (raisonnement détaillé, calculs
  alignés), `::: resultat` (conclusion encadrée) ; quand c'est utile :
  `::: attention` (erreur fréquente) ou `::: retenir` ;
- `Solution:` réponses courtes numérotées, cohérentes avec les étapes ;
- pédagogie : un élève seul doit pouvoir suivre ; pas de saut de calcul ;
- exercices avec « Partie A / Question A1 » en gras dans la conversion :
  restructurer en `## Partie A : …` + `## Question A1 : …`.
- Arbres de probabilités, schémas, tableaux de variations dessinés en tableau
  HTML (cellules fusionnées) : à remplacer par une **figure** (arbre TikZ) ou
  un `::: tableau` natif.
- Code Python : blocs ```` ```python ```` (jamais d'image de code).

## 5. Figures : exigences du propriétaire

Mots du propriétaire : « supprime lorsque nécessaire les anciens schémas et
refais des figures et schémas impeccables », « aucun débordement »,
« quand tu écris un truc, qu'il ne s'écrive pas au-dessus d'un trait ».

**Décision pour chaque image actuelle** (planches) :
- tableau de variations / de signes en image → `::: tableau` natif, image retirée ;
- tableau de données, texte, code en image → texte / tableau / code, image retirée ;
- image floue, texte minuscule, grands vides, style matplotlib par défaut
  (bleu/rouge criards, légende minuscule), étiquettes qui se chevauchent,
  erreur mathématique, valeurs différentes de l'énoncé → **refaire** ;
- figure récente propre, lisible, juste, cohérente avec le style des livres
  (palette bleu marine / vert / orange, texte net) → peut être conservée
  (elle sera listée « conservée » par le vérificateur : vous en répondez) ;
- dans une même notion, ne pas mélanger un style ancien et le style livre
  pour des figures du même type : en cas de doute, refaire ;
- figure inutile (décorative, doublon) → retirer l'appel `[IMAGE_N]`.
  Les images en ligne qui ne sont plus appelées seront **supprimées** à l'import.
- ajouter une figure là où elle aide vraiment (géométrie, courbe étudiée,
  arbre, situation concrète), y compris dans les corrigés (`Étapes:`), avec
  les éléments de réponse en vert (otGreenDark).
  **Obligatoire (consigne du 2026-11-02)** : chaque schéma nécessaire est
  présent partout où il aide — cours, fiche, énoncé ET corrigé. Un énoncé de
  géométrie, de courbe ou d'arbre sans figure, ou un corrigé qui raisonne sur
  une figure sans la montrer complétée, est un défaut à corriger.

**Fabrication** (`figures/figures.py`, compilé par `figures_livre.py`) :
- LuaLaTeX + TikZ/pgfplots avec le préambule commun (polices et palette des
  livres, styles `otWeb`, `otTrig`, `otBarres`, `courbe`, `geoTrait`,
  `cote`, `\angledroit`, `\codage`, `\cote`, `\pnt`… — voir le docstring et
  `PREAMBULE` de `outils/figures_livre.py`) ; modèle de courbes : `pilote_trigo_terminale/figures/figures.py` ;
- réutiliser les figures des livres : `livre/livre-maths/livre-<niveau>/figures/*.tex`
  (seconde, première, collège) et les `tikzpicture` des chapitres
  (`livre-terminale/chapitres/`, `livre-maths-expertes/`) ; générateurs Python
  du collège : `livre-sixieme/generer_figures.py` ;
- **taille** : largeur finale ≤ 900 px (≈ 9,5 cm ; refus au-delà de 1100 px) ;
  la figure est affichée à la moitié de ses pixels : son texte a alors la
  taille du texte du site. Jamais `transform shape`, `\resizebox`, ni `scale`
  sur un `axis` (régler `width`/`height`) ;
- **aucun texte sur un trait** : le compilateur compare la figure avec et sans
  texte et REFUSE toute étiquette posée sur un trait visible. Placer les
  étiquettes dans l'espace libre (`anchor=…`, petit décalage). Un fond blanc
  (`etiq`, `coteTexte`) est réservé aux cotes et graduations ; ailleurs,
  déplacer l'étiquette. `TOLERE = {"nom": "raison"}` seulement pour un faux
  positif avéré, raison écrite ;
- tout ce qui est écrit sur la figure correspond exactement au texte (noms
  des points, valeurs, unités) ; virgule décimale ; points en italique `$A$` ;
- courbes : graduations lisibles, pas de chevauchement graduation/courbe
  (graduations placées à la main avec `XLAB` si besoin, comme le pilote),
  repère et fenêtre choisis pour montrer ce qui compte, sans vide inutile ;
- regarder chaque PNG produit (Read) : alignements, lisibilité, équilibre.

**Correspondance** (`figures/correspondance.json`) — position N = `[IMAGE_N]` :

```json
{
  "cours":     {"<id_cours>":    {"1": {"fichier": "repere_exp.png", "alt": "Courbe de la fonction exponentielle et sa tangente en 0"}}},
  "fiches":    {"<id_fiche>":    {"1": {"fichier": "…png", "alt": "…"}}},
  "exercices": {"<id_exercice>": {"2": {"fichier": "…png", "alt": "…"}}}
}
```

- position existante → l'image en ligne est remplacée ; nouvelle position →
  image ajoutée. Une même figure peut servir à plusieurs places.
- Dans un exercice, la numérotation `[IMAGE_N]` est commune à Énoncé,
  Étapes et Solution.
- `alt` : phrase descriptive précise (≥ 15 caractères, ce que montre la figure).

## 6. Pièges connus

- `*texte*` = italique : un produit s'écrit `\times` ; une étoile seule `$\ast$`.
- `$` de prix : `\$`. Pas de HTML (sauf `<br>` dans une cellule de tableau).
- Dans un `axis` pgfplots, un `\foreach` s'évalue trop tard : dérouler.
  `\bf` existe déjà (ne pas redéfinir). Fonctions trigo : style `otTrig` (radians).
- Courbes au-dessus des graduations : `axis on top=false` (déjà dans `otWeb`).
- Le vérificateur liste les images en ligne **conservées** : chacune doit être
  un choix assumé.
- Un exercice identique peut exister dans une autre notion (parcours
  « Bases & Méthodes ») : ne s'occuper que de sa notion.

## 7. Rapport (`RAPPORT.md`) et fin

Court, en français :
- état : prêt / points en suspens ;
- texte : principales corrections (erreurs de maths corrigées : lesquelles) ;
- figures : n refaites, n ajoutées, n conservées (pourquoi), n retirées ;
- contrôles : verifier_notion OK, vues regardées ;
- remarques pour l'orchestrateur (défaut d'outil ou de moteur, doute sur le
  programme, exercice à revoir).

Message final à l'orchestrateur : 5 à 10 lignes (notion(s), statut, chiffres,
points d'attention).

## 8. Orchestration (réservé à l'orchestrateur, jamais aux agents de notion)

- **Files d'attente et statut** : `FILE_FINITION.md` (lycée, fini le 02/11),
  `FILE_3E.md` (3e en cours). Un nouveau niveau ne démarre que sur le GO du
  propriétaire ; il fixe aussi le nombre d'agents en parallèle et l'heure d'arrêt.
- **Préparer un niveau** : `exporter.py --contexte <id>` (via `manage.py shell`,
  lecture seule) puis `convertir_notion.py <dossiers>`.
- **Publier des notions « pret »** : `powershell -File outils/publier_lot.ps1 <niveau> <ids…>`.
  Il enchaîne : `relier_nouveaux.py` (nouveau-N → vrai Id), ré-export (sinon
  `meta.json` est périmé), simulation `importer_v1.py`, application seulement si
  rien n'est refusé (sauvegarde automatique, restauration `--restaurer`),
  `titres_docs.py` (titres de cours/fiche), `synchro_contenu.py` (la page des
  exercices lit le champ `contenu` avant `question` : ils doivent être égaux).
  Le .ps1 doit rester en UTF-8 AVEC BOM (PowerShell 5.1).
- **Autres outils** : `renommer_programme.py` (titres de notions/thèmes),
  `supprimer_notion.py` (suppression avec sauvegarde), `creer_sujets_bac.py`.
- `backend/.env` = PRODUCTION : toute écriture est en ligne immédiatement ;
  jamais de `git push` sans accord explicite du propriétaire.
