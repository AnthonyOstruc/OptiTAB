# Guide des ressources gratuites : référencement maximal (Google et IA)

À lire **avant** de créer ou de modifier une page de `/ressources-gratuites/`
(formulaires, tables, méthodes, outils, fiches à imprimer, physique-chimie…).

Le but de ces pages est d'**être trouvé** : premières positions sur Google et
sur Bing, et réponses reprises par les IA (ChatGPT, Claude, Perplexity, Gemini).
Le propriétaire veut un résultat **impeccable**. Mieux vaut une page parfaite
que trois pages moyennes. Ne rien inventer ; tout vérifier.

---

## 1. Règles du propriétaire (non négociables)

- **Aucun `git commit` ni `git push` sans son accord explicite.** Après un push,
  rien ne change en ligne tant qu'il n'a pas fait **Manual Deploy** sur Render.
- `backend/.env` pointe sur la base de **production** : ces pages n'en ont pas
  besoin. Ne jamais y écrire pour une ressource gratuite.
- Seule la marque **OptiTAB** apparaît : jamais « SWEELCO », jamais de nom de
  personne (signature : « l'équipe pédagogique OptiTAB »).
- Ne jamais copier de livre, de PDF ou d'audio sur le Bureau.
- Contenus conformes aux **programmes officiels français** de la classe visée.
- Comptes rendus au propriétaire : courts, en français, sans jargon.

## 2. Comment le site fabrique ces pages

- `npm run build` lance `scripts/ressources/generer.mjs` : chaque page devient
  une page **HTML statique complète**. Le texte, les formules (SVG + MathML) et
  les images sont lisibles sans JavaScript, donc par les robots et les IA.
- Une page = un dossier `frontend/contenu/<rubrique>/<slug>/` avec :
  - `formulaire.md` : bloc d'informations JSON entre `---`, puis le texte au
    format OptiTAB v1 (voir `frontend/cours/format_v1/FORMAT.md`) ;
  - `figures/figures.py` et `figures/images/*.png` (schémas) ;
  - `generer.py` quand le texte vient de données (tables, listes, fiches PDF).
    **Dans ce cas, ne jamais modifier `formulaire.md` à la main** : modifier
    `generer.py`, puis le relancer.
- Les rubriques (dossier, adresse, textes, référencement) sont définies dans
  `RUBRIQUES` (`scripts/ressources/formulaires.mjs`) : `formulaires`, `tables`,
  `methodes`, `operations`, `fiches`, `maternelle`, `physique-chimie`.
- L'adresse d'une page est `/ressources-gratuites/<racine>/<slug>/`, toujours avec
  « / » final. **Ne jamais changer l'adresse d'une page déjà en ligne.**
- Les outils interactifs (calculateurs, horloge, tableau périodique) sont dans
  `scripts/ressources/outils.mjs` et `scripts/ressources/outils/<nom>.js`. Un
  outil sur mesure a un champ `html` (exemples : `tableau-periodique.mjs`,
  `horloge.mjs`). Son HTML doit être **lisible sans JavaScript**.

## 3. Choisir le sujet : la demande réelle

1. Partir de ce que les gens tapent vraiment. Exemples : « tableau périodique »,
   « comment calculer un pourcentage » (26 000 recherches par mois),
   « lire l'heure », « formule concentration ».
2. **Pas de doublon.** Chercher d'abord si une page existante répond déjà à la
   question : `grep -ril "<mot>" frontend/contenu`, la recherche de l'accueil
   des ressources, les rubriques. Deux pages sur la même requête se font
   concurrence : il vaut mieux enrichir l'existante ou relier les deux.
3. Une page = une intention de recherche claire. Une page par chapitre, et non
   une page fourre-tout.

## 4. Le bloc d'informations (référencement)

| Champ | Règle |
|---|---|
| `slug` | nom du dossier, mots-clés de la requête, minuscules, tirets, sans accents (`tableau-periodique`). |
| `titre` | titre H1 de la page : la requête principale en tête (« Tableau périodique des éléments »). |
| `titreSeo` | titre pour Google : **≤ 65 caractères** (le build refuse au-delà), la requête exacte d'abord, puis le bénéfice (« interactif et à imprimer »). Unique sur le site. |
| `description` | **140 à 160 caractères** (refus au-delà de 160) : la requête, ce que la page contient, ce qu'on y gagne. Unique. |
| `chapo` | la réponse en deux phrases, en tête de page : c'est souvent ce que reprennent les IA. |
| `resume` | une ligne pour les cartes. |
| `motsCles` | les variantes réelles de la requête (orthographes, synonymes, questions). |
| `figures` | chaque figure avec un `alt` **descriptif et précis** (≥ 15 caractères) : ce que montre la figure, avec les valeurs. Exemple : « Tableau d'avancement de la réaction CH4 + 2 O2… ». |
| `vignette` | la figure la plus parlante : image de partage (og:image), image des cartes et première image pour Google. |
| `niveaux`, `ordre` | pastilles de niveau et place dans la rubrique (un nombre décimal est accepté, par exemple 3.5). |
| `publie`, `modifie` | dates ISO ; mettre à jour `modifie` à chaque vraie modification du contenu. |
| `faq` | 5 à 6 **vraies questions des gens** (« Comment… ? », « Quelle est la formule… ? »), réponses autonomes de 2 à 4 phrases, sans LaTeX, avec un exemple chiffré. |
| `liees` | 2 à 4 pages proches (`dossier/slug`), **dans les deux sens** : ajouter aussi le lien retour sur l'autre page. |
| `chapitresLies` | chapitres de cours correspondants (`classe/slug` existant) : relie la page aux cours. |
| `outil`, `telechargements` | outil interactif ; PDF à imprimer (`titre`, `libelle`, `pdf`, `corrige`). |

## 5. Rédaction

- Répondre à la question **dès le haut de la page** (chapo, outil, première partie).
- Parties `## I. …` numérotées, avec la pastille de niveau en fin de titre :
  `{Primaire}`, `{Collège}`, `{Lycée}`, `{Supérieur}`. Pour le lycée, ajouter
  sous le titre : `*Programme de Seconde.*` (ou Première, ou Terminale).
- En haut, un encadré `::: conseil Par où commencer ?` qui dit quelle partie
  lire selon la classe.
- Pour chaque formule : l'encadré `::: formule`, le tableau Lettre / Grandeur /
  Unité, un `::: exemple` **recalculé**, et un `::: attention` pour le piège classique.
- **Vérifier sur le programme officiel.** Les textes sont dans
  `livre/archives/programmes-officiels/` et
  `livre/livre-physique/livre-pc-*/recherche*/programme-*.txt`.
- **Valeurs générées et contrôlées par script** dès que c'est possible : données
  avec `assert`, recoupement de deux sources (exemple :
  `physique-chimie/tableau-periodique/construire_elements.py`), calcul automatique
  (exemple : les formules des composés de `physique-chimie/ions-courants/generer.py`).
- Typographie :
  - espace insécable entre un nombre et son unité (« 0,50 mol »), espace fine
    insécable pour les milliers ; le moteur ajoute l'espace avant « : ; ! ? » ;
  - pas de `\text{…}` avec accents ;
  - pas de formule dans un titre ;
  - formule longue en `aligned` sur deux lignes.

## 6. Téléphone d'abord (la majorité des visiteurs)

- Tableaux de 3 colonnes au plus, avec des cellules courtes. Quand les noms
  sont longs, passer à **2 colonnes**, qui s'empilent sur téléphone.
- Ne jamais mettre tout un texte dans une seule formule `$…$` : elle ne se coupe
  pas et déborde.
- Figures : **900 px de large au plus** (1 100 px est refusé). Pas de longue
  légende dans une figure : des numéros dans la figure, et le texte dans la page.
- Contrôle : captures à 390, 820 et 1 440 px, **0 débordement**, décalage
  d'affichage (CLS) inférieur à 0,1.
- Attention, faux débordement : `mjx-assistive-mml` est la copie des formules
  pour les lecteurs d'écran. Vérifier plutôt les SVG visibles.

## 7. Images : référencement maximal

- Schémas en TikZ avec `frontend/cours/format_v1/outils/figures_livre.py <dossier> --planche`.
  Le contrôle refuse tout texte posé sur un trait. Il prend aussi pour du texte
  sur un trait un **nœud rempli** ou du texte blanc sur fond foncé : dessiner les
  cadres en chemins (`\draw … rectangle`) et mettre le texte dans des nœuds sans fond.
- Relire **chaque figure en grand** avant de livrer (le propriétaire le fait).
- Le texte alternatif décrit l'image précisément, avec les mots que les gens cherchent.
- Une information importante ne doit jamais se trouver **seulement** dans une image :
  la redire dans le texte, que Google et les IA lisent.
- Automatique au build, ne rien casser :
  - les images de la page sont déclarées dans les données structurées (`image`) ;
  - elles figurent dans `sitemap-ressources.xml` (`image:image`) ;
  - la vignette sert d'image de partage ;
  - `max-image-preview:large` est déclaré.
- Pour un PDF à imprimer, faire aussi un aperçu en image (exemple :
  `tableau-periodique/generer.py`, avec `pdftoppm`).

## 8. Indexation et visibilité dans les IA

Ce que le build fait déjà, et qu'il ne faut **jamais casser** :

- HTML statique complet, adresse canonique avec « / » final,
  `index,follow,max-snippet:-1,max-image-preview:large` ;
- données structurées : `LearningResource`, `FAQPage`, `BreadcrumbList`, plus
  `ItemList` et `WebApplication` selon la page ; une seule organisation,
  `https://www.optitab.net/#organization` ;
- `sitemap-ressources.xml`, avec les images et les dates de modification ;
- `llms.txt`, plus une version Markdown `index.md` de chaque page, pour les IA ;
- `robots.txt` ouvert à tous les robots, IA comprises. Le 19/11/2026, GPTBot,
  OAI-SearchBot, ChatGPT-User, ClaudeBot, PerplexityBot, Googlebot et bingbot
  recevaient tous une réponse 200.

**Interdit :**
- mettre `noindex` sur une ressource ;
- bloquer un robot ;
- écrire un lien interne sans « / » final ;
- changer une adresse ;
- dupliquer une page ;
- publier une page vide ou « à venir ».

Maillage interne (les liens qui font monter une page) :
- `ACCES_RAPIDE` dans `formulaires.mjs` : les 12 pages les plus demandées, mises en avant sur l'accueil ;
- les liens `liees`, dans les deux sens ;
- les `chapitresLies` ;
- la rubrique ;
- le pied de page.

## 9. Contrôles obligatoires avant de livrer

Depuis `frontend/` :

```sh
PYTHONUTF8=1 python cours/format_v1/outils/figures_livre.py contenu/<rubrique>/<slug> --planche --jobs 1
python -X utf8 contenu/<rubrique>/<slug>/generer.py          # si la page en a un
node scripts/ressources/generer.mjs --sortie <dossier temporaire> --formulaires-seuls
node --test scripts/ressources/catalogue.test.mjs scripts/ressources/instantane.test.mjs
node scripts/ressources/generer.mjs --sortie <dossier temporaire>   # construction complète
```

Puis, sur la page générée (servie en local) :
- titre ≤ 65 caractères, description ≤ 160, un seul H1, JSON-LD valides, aucun
  lien interne cassé ;
- captures à 3 tailles, sans débordement ;
- test de chaque outil interactif avec Playwright (clics, résultats, aucune
  erreur JavaScript) ;
- ouvrir la page dans le navigateur du propriétaire et lui donner le lien.

Supprimer ensuite `figures/build`, `figures/__pycache__` et les planches.

## 10. Mise en ligne (seulement avec l'accord du propriétaire)

1. **Ne valider que ses propres fichiers** : `git commit --only -- <fichiers>`.
   D'autres sessions ont des travaux non enregistrés, dont **3 744 suppressions
   déjà préparées** qui ne doivent pas partir.
2. Vérifier d'abord dans une **copie propre** (worktree creux) :
   ```sh
   git worktree add --no-checkout --detach <dossier> HEAD
   cd <dossier>
   MSYS_NO_PATHCONV=1 git sparse-checkout set --no-cone /frontend/scripts/ /frontend/contenu/ /frontend/public/ /frontend/src/ /frontend/package.json
   git read-tree -mu HEAD
   ```
   Copier ses fichiers dedans, puis créer une jonction vers `frontend/node_modules`.
   Construire et comparer le HTML avec la version testée. Ensuite, **retirer la
   jonction avec `cmd /c rmdir` AVANT** `git worktree remove --force`.
3. `git push origin main`. Prévenir le propriétaire qu'il doit faire **Manual
   Deploy → Deploy latest commit** sur Render.
4. Après le déploiement :
   - dans Google Search Console, inspecter l'adresse et demander l'indexation ;
   - dans Bing Webmaster Tools, faire de même : ChatGPT et Copilot s'appuient
     en partie sur l'index de Bing.

## 11. Pièges déjà rencontrés

- L'outil Bash (heredoc, `python -c`, `sed`) mange les `\\`. Écrire le LaTeX avec
  les outils d'édition, ou construire les barres obliques avec `chr(92)`.
- Les séquences d'échappement Unicode (barre oblique + `u00a0`) sont converties
  en caractère réel par les outils d'édition. Dans le code JavaScript, construire
  la séquence avec `chr(92)` ou utiliser `String.fromCharCode(160)`.
- Dans le terminal Git Bash, les chemins qui commencent par « / » sont
  transformés : préfixer la commande par `MSYS_NO_PATHCONV=1`.
- PDF LuaLaTeX : Montserrat existe en `SemiBold` (pas de `Bold`).
- Render a des règles en boucle sur `/ressources-gratuites` (sans « / ») : seul
  le propriétaire peut les supprimer. Les liens du site ont toujours le « / » final.

## 12. Où en est le chantier (19/11/2026)

**En ligne ou poussé :**
- maths : formulaires, tables, méthodes de calcul (dont **lire l'heure**, avec
  horloge interactive et fiches CP, CE1, CE2), opérations posées, fiches à
  imprimer, maternelle ;
- **simulateur du brevet** (`methodes/simulateur-brevet`, poussé le 19/11) : calcul officiel depuis 2026 (40 % contrôle
  continu, 60 % épreuves), mention, note à viser. Le calcul existe en trois
  exemplaires qui doivent rester identiques : `scripts/ressources/brevet.mjs`
  (page), `scripts/ressources/outils/brevet.js` (saisie) et `generer.py` (texte) ;
  `generer.py` les compare sur 5 000 cas. Si les règles du brevet changent
  (nouvel arrêté, BO de rentrée), modifier les trois, relancer `generer.py`,
  puis mettre à jour `modifie` ;
- physique-chimie : formules du brevet, électricité, électrocinétique, quantité
  de matière et concentration, **tableau périodique** (interactif, PDF),
  **ions courants**, **formules de mécanique** (Seconde → Terminale :
  vitesse, forces, lois de Newton, chute libre, satellites ; `generer.py`
  recalcule chaque exemple) et **formulaire de mécanique du supérieur**
  (`formulaire-mecanique-prepa` : prépa 1re et 2e année, licence, Lagrange
  et Hamilton). Une page par public : lycée et supérieur sont séparés, et reliés.
- **unités SI et constantes physiques** (`physique-chimie/unites-si-constantes-physiques`) :
  `generer.py` compare chaque constante à CODATA 2022 (scipy.constants) ; à
  relancer après chaque nouvelle publication du CODATA (tous les 4 ans).
- **convertisseur d'unités** (`methodes/convertisseur-d-unites`, outil `convertisseur`) :
  15 grandeurs. Les unités sont dans `scripts/ressources/convertisseur.mjs`,
  SOURCE UNIQUE du convertisseur et des tableaux de la page ; pour ajouter une
  unité, l'ajouter là puis relancer `generer.py`, qui vérifie chaque facteur
  (scipy.constants) et que la page calcule comme le module. Lien direct vers une
  grandeur : `…/convertisseur-d-unites/#pression`.

**À faire ensuite, par demande décroissante :**
1. **Énergie** (Première) : énergie cinétique, travail d'une force, théorème de
   l'énergie cinétique, énergie potentielle et mécanique. Page à relier à
   `physique-chimie/formules-de-mecanique` dans les deux sens.
2. **Automatismes** : QCM de l'épreuve anticipée de Première, et calcul mental
   en CM1 et CM2.
3. Primaire : **problèmes** classés par type (CP au CE2), la **monnaie**.
4. Physique-chimie : couples acide-base (pKa) et indicateurs colorés, ondes,
   optique (réfraction, lentilles), thermodynamique, mécanique de prépa.
