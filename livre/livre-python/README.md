# OptiTAB — Python · The Complete Method (5 volumes, in English)

Livre **rédigé en anglais** pour apprendre à programmer en Python de zéro jusqu'au niveau
professionnel. Collection : Volume 1 *First Steps* (Beginner) · Volume 2 *Solid Foundations*
(Elementary) · Volume 3 *Thinking in Objects* (Intermediate) · Volume 4 *Python at Work* (Advanced) ·
Volume 5 *Mastering Python* (Expert). Même charte que les autres livres OptiTAB.

## État (25/10/2026)

- [x] Gabarit `optitab-python.sty` + moteur de code `otpython.lua`, couvertures, page de titre
- [x] Liminaires : Welcome, How to use this book, Getting the code (+ programmer's alphabet),
      Contents, What you will learn, The collection
- [x] Plan complet du volume 1 (`tome-1/plan.tex`) : 5 parties, 20 chapitres, 5 projets, 5 checkpoints
- [x] Chapitres 1 à 3 + solutions + glossaire généré : **envoyés pour validation** (96 pages)
- [ ] Chapitres 4 à 20, projets 1 à 5, checkpoints 1 à 5 — après validation du propriétaire
- [ ] Mise en ligne du code (`tome-1/code/` → optitab.net/python/t1) et ISBN : décisions du propriétaire

## Structure

- `tome-1.tex` : fichier principal (ordre des pages) ; `tome-1/plan.tex` : plan (sommaire, tableau
  du programme, ouvertures de parties, en-têtes).
- `tome-1/chapitres/chNN-nom.tex`, `tome-1/annexes/solutions-chNN.tex`, `tome-1/annexes/glossaire.tex`
  (généré), `tome-1/liminaires/`, `tome-1/couverture/`, `tome-1/illustrations.tex` (bandeaux d'ouverture).
- `tome-1/code/` (généré) : `chapters/chapter-NN/*.py`, `solutions/chapter-NN/*.py`, `programmes.tex`
  (nombre de programmes par chapitre, affiché sur la page d'ouverture).
- `outils/` : `verifier_code.py` (vérification + export), `console_idle.py` et `execution_idle.py`
  (simulation exacte d'IDLE), `idle_commun.py`, `glossaire.py`.

## Un chapitre, toujours dans le même ordre

`\chapitre{n}{titre}{sous-titre}{\illusXxx}` puis `\histoire`, `objectifs`, `\auprogramme{concepts}{python}{outils}{habitudes}{réalisation}`,
`\seances[4]{icône/couleur/titre/contenu,...}` (pas de virgule dans les champs), puis les rubriques
`\rubrique{learn|hood|debug|pro|build|practice|review}{titre}` : plusieurs *learn*, un *hood*
(sous le capot), un *debug*, un *pro* (bonnes habitudes), un mini-projet *build*, 12 exercices
*practice*, puis *review* (`essentiel`, `quiz` de 10 `\qcm`/`qcmcode`, `jesais`).

Encadrés : `regle` (Key idea), `attention` (Watch out), `astuce` (Tip), `culture` (Did you know?),
`pratique` (Pro habit), `definition{terme}` (Key term → glossaire), `atoi` (Your turn, corrigé
`corrigeatoi`), `encadre`, `memoire` (schéma noms → objets : `\nomvar`, `\objet`, `\lien`),
`suivi` (tableau de suivi : `\nv`, `\av`), `calcul` (`\pas`, `\hlc`), `\cas{n}{titre}`,
`gauche`/`droite` (deux colonnes, accepte les blocs de code).
Exercices : `\exercice[type=predict|fix|complete|write|shell|read|explain|challenge,niveau=1..3]{titre}{consigne}`,
`questions`, `\trou`, `\ecranvide{n}`. Solutions : `\corrigesChapitre`, `corrige{n}`, `corrigeatoi{n}`,
`corrigequiz`, `\demarche`, `\pourquoi`, `\retiens`, `\piege`, `reponses`, `\rep`.

## Le code dans le livre

| Environnement | Rendu | Contrôle |
|---|---|---|
| `\begin{code}{file=x.py, marks={2,4-5}, first=1, nonum, mini}` | programme coloré, n° de ligne | exécuté si une sortie suit, sinon compilé |
| `\begin{sortie}` | écran sombre « Output » ; `«Ana»` = saisie de l'utilisateur | comparée à l'exécution réelle |
| `\begin{erreur}` | écran à bord rouge « Error message » | le programme doit échouer, message identique |
| `\begin{console}` | session du Shell (`>>>`, `...`) | rejouée dans un Shell IDLE simulé |
| `\begin{idleshell}{titre}` / `\begin{idleediteur}{titre}` | fenêtres d'IDLE dessinées (chapitre 1) | idem |

- Accolades obligatoires après `\begin{code}` (même vides `{}`) : la capture verbatim (Lua) ne doit pas
  lire la ligne suivante. `# <3>` en fin de ligne de code = pastille de renvoi ; `<<3>>` en fin de ligne
  d'écran = pastille ; `___` = trou à compléter.
- Options pour le vérificateur : `bug`, `trous`, `norun`, `nocheck`, `suite` (reprend le bloc précédent),
  `variante` + `first=n` (ne montre que les lignes modifiées d'un programme), `cible=clé`.
- Marques : `\cible{clé}` (sortie attendue d'un exercice, produite par la solution `cible=clé`),
  `\sortielibre`, `\rattacher` (sortie séparée de son code par du texte), `\suiteconsole`, `\titresortie{…}`.
- Code en ligne : `\py{print("Hi")}` (échapper `\# \% \_ \{ \}`, `\textbackslash`, `\textasciicircum{}`).
- Référence = **IDLE / Python 3.13** : tracebacks sans `^^^`, erreurs de syntaxe du Shell en une ligne,
  `<pyshell#N>` (un numéro par appui sur Entrée), chemins de fichiers raccourcis au nom du fichier.

## Commandes

```
python -X utf8 outils/verifier_code.py tome-1 --exporter   # tout le code + export de tome-1/code
python -X utf8 outils/glossaire.py tome-1                   # régénère le glossaire
"$LOCALAPPDATA/Programs/MiKTeX/miktex/bin/x64/lualatex.exe" -interaction=nonstopmode \
  -file-line-error -aux-directory=build tome-1.tex          # deux ou trois passes
```

Après chaque modification : vérificateur « Tout est conforme », compilation sans erreur ni
`Overfull` ni `Missing character`, puis contrôle des pages rendues (`pdftoppm`).

## Pièges connus

- Le paquet `piton` installé exige un LaTeX plus récent que celui du PC : d'où le moteur Lua maison.
- `\needspace` crée des coupures « préférées » avec `\raggedbottom` : utiliser `\Needspace`, et jamais
  à l'intérieur d'une boîte sécable (quiz, essentiel).
- Fira Mono n'a pas tous les symboles (✓, flèches…) : n'utiliser que l'ASCII et les lettres accentuées
  dans le code et les sorties.
- Une commande ne peut pas s'appeler `\code` (conflit avec l'environnement `code`).
- Éditer le LaTeX avec l'outil Edit ou des scripts Python écrits avec Write (les heredocs abîment les `\`).
