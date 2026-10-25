# OptiTAB — Anglais · Méthode complète en 5 tomes

Méthode d'anglais pour francophones qui partent de zéro, avec audio (QR code à côté de chaque
activité). Collection prévue : Tome 1 *Premiers pas* (A1) · Tome 2 *Les bases solides* (A2) ·
Tome 3 *Communiquer avec aisance* (B1) · Tome 4 *Parler couramment* (B2) · Tome 5 *Maîtriser
l'anglais* (C1). Fil rouge : Léa, graphiste lyonnaise installée à New York.

## État (25/10/2026)

- [x] Gabarit `optitab-anglais.sty`, couverture recto/verso, page de titre et mentions légales
- [x] Liminaires : Bienvenue, Mode d'emploi, Écouter les audios, Les sons de l'anglais
      (pistes 0.01–0.02), Les personnages, Sommaire, Programme du tome, La collection
- [x] Plan complet du tome 1 (`tome-1/plan.tex`) : 5 parties, 20 unités, 5 bilans
- [x] Unité 1 *Hello!* validée par le propriétaire (25/10/2026)
- [x] Unités 2 à 20, bilans 1 à 5 (barème sur 20), corrigés et transcriptions de tout le tome
- [x] Mémento de grammaire, 60 verbes irréguliers, lexique généré
- [x] Audio complet (272 pistes), vérifié par reconnaissance vocale
- [ ] Mise en ligne des audios (voir plus bas) et ISBN — décisions du propriétaire

## Structure

- `tome-1.tex` : fichier principal du tome 1 (informations du tome, ordre des pages).
- `optitab-anglais.sty` : le gabarit commun à tous les tomes.
- `tome-1/plan.tex` : le plan (titres et contenus des 20 unités) ; le sommaire, le tableau du
  programme et les ouvertures de parties sont générés à partir de lui.
- `tome-1/unites/uNN-titre.tex` : une unité ; `tome-1/annexes/` : corrigés, transcriptions,
  lexique (généré) ; `tome-1/liminaires/`, `tome-1/couverture/`.
- `tome-1/audio/` : `en-ligne/` (MP3 + pages d'écoute HTML, **à mettre en ligne**),
  `durees.tex` (durées imprimées), `manifeste.json`.
- `outils/` : chaîne audio et lexique ; `outils/modeles/` : modèle de voix (350 Mo, non versionné).
- `verifications/` : contrôles de contenu (`unite_NN.py`) et rapport audio.

## Une unité, toujours dans le même ordre

`\unite[Ligne 1\\Ligne 2]{n}{titre anglais}{sous-titre}{illustration}` (l'argument optionnel coupe
un titre long sur la page d'ouverture ; la taille s'ajuste seule pour ne jamais passer sous les
personnages) puis `\situation`, `objectifs`,
`\auprogramme`, `\semaine` (page d'ouverture), et les 7 rubriques
`\rubrique{ecouter|mots|grammaire|sons|culture|pratique|bilan}{titre}`.

Macros principales : `dialogue` + `\dit{perso}{anglais}{français}` + `\note{n}` /
`comprendre` + `\pointnote{n}` ; `vocabulaire` + `\categorie` + `\mot[texte dit]{anglais}{api}{français}` ;
`paires` + `\sonpaire` ; `\blocaudio` ; encadrés `regle`, `attention` (`\fauxjuste`),
`astuce`, `culture`, `paire` (deux encadrés côte à côte) ; `\exercice[ecouter,parler,lire,ecrire,
niveau=1..3,piste=1.10]{titre}{consigne}`, `questions`, `\trou{réponse}`, `\lignes{n}`,
`\choix`, `\etiq` ; bilan : `essentiel`, `testexpress` + `\qcm`, `jesais` ; corrigés :
`\corrigesUnite`, `corrige{n}`, `reponses`, `\rep`, `\pourquoi`, `\retiens`, `\piege`,
`corrigetest` ; transcriptions : `transcription` / `pisteaudio` avec `\dit`, `\dire`,
`\annonce`, `\repere`, `\numdire`, `\repete`, `\repetepaire`, `\silence{s}`.

Figures d'exercices : `\otCarteObjet{icône}{couleur}{n}{réponse}`, `\otCarteHeure`, `\otCartePrepo`,
`\otCarteAction{perso}{icône}{couleur}{indication}{réponse}` (avatar + action), `otTextos` +
`\otSms{g|d}{texte}` (écran de téléphone), `\otPrevision{jour/icône/couleur/°F/°C,…}` (météo),
`\otMonte` / `\otDescend` (flèches d'intonation, ignorées par la synthèse vocale). Icônes météo :
`soleil`, `nuage`, `pluie`, `neige`, `vent`, `brouillard`.

Règle typographique : tout texte anglais passe par `\en{…}` (en ligne, italique) ou `\enb{…}`
(bloc) — sinon la typographie française ajoute une espace avant `! ? : ;`.

## Audio

Le livre est la **source unique** : `outils/audio.py` lit les environnements qui impriment
chaque piste (dialogue, vocabulaire, paires, transcription, tableausons) et fabrique le MP3.

```
python -X utf8 outils/audio.py tome-1            # génère / met à jour toutes les pistes
python -X utf8 outils/verifier_audio.py tome-1   # réécoute tout (Whisper) et compare au livre
python -X utf8 outils/lexique.py tome-1          # régénère le lexique
python -X utf8 verifications/verifier_unite.py tout   # contrôle de contenu de tout le tome
```

- Voix : Kokoro 82M (poids sous licence Apache 2.0, usage commercial autorisé), en local.
  Accent de référence américain ; Emma (londonienne) a une voix britannique.
- Chaque énoncé est choisi parmi plusieurs « prises » : on garde la première que la
  reconnaissance vocale comprend exactement **après encodage MP3** (`build/prises.json`).
  Les mots isolés sont dits à vitesse naturelle : ralentie, la voix déforme les mots qui
  commencent par une voyelle. Les syllabes ouvertes en /ɔɪ/ (« boy », « toy ») sont mal
  rendues : choisir des exemples fermés (« voice »). Les interjections en début de réplique
  (« Wow! », « Hmm. », « Er… », « Brr! ») et un prénom seul (« Emma. ») sont mal rendus :
  les éviter. « Sixth. » isolé est déformé (« The sixth day. »).
- Formes faibles : `audio.py` fait dire /kən/, /wəz/, /wɚ/ à « can », « was », « were » quand ils ne
  sont pas en fin de phrase (espeak les prononce toujours en forme pleine).
- Les QR codes pointent vers `https://www.optitab.net/audio/anglais/t1/piste-1-05.mp3`
  (adresse réglée par `\otAudioBase` dans `tome-1.tex`). Pour les activer, copier le contenu de
  `tome-1/audio/en-ligne/` dans `frontend/public/audio/anglais/t1/` du site.

## Compilation

```
"$LOCALAPPDATA/Programs/MiKTeX/miktex/bin/x64/lualatex.exe" -interaction=nonstopmode \
  -file-line-error -aux-directory=build tome-1.tex      # deux passes
```

Après chaque modification : recompiler deux fois, vérifier 0 erreur, 0 `Overfull`,
0 `Missing character`, puis regarder les pages rendues (`pdftoppm`).
