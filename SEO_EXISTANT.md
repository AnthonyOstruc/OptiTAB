# SEO existant dans le code (ordre + synthese)

Ce document liste les mecanismes SEO deja en place dans le projet, dans l'ordre de fonctionnement.

## 1) Build: generation du sitemap

- `frontend/package.json:8-10`
  - `prebuild` lance `node ./scripts/generate-sitemap.mjs`.
- `frontend/scripts/generate-sitemap.mjs:280-383`
  - Construit `frontend/public/sitemap.xml`.
  - Ajoute des pages statiques SEO (`/`, `/tarifs`, `/cours-particuliers`, `/about`, `/contact`, `/ressources-gratuites`).
  - Ajoute le contenu gratuit dynamique depuis l'API (cours/syntheses + chapitres d'exercices).
  - En cas d'echec API, garde un sitemap minimal et tente de merger l'existant.

## 2) Edge/serveur: redirections et domaine canonique

- `frontend/public/_redirects:1-12`
  - Redirection de domaine vers `https://www.optitab.net` (301).
  - Redirections legacy SEO:
    - `/cours-en-ligne` -> `/cours-particuliers`
    - `/soutien-scolaire` -> `/cours-particuliers`
    - `/aide-aux-devoirs` -> `/cours-particuliers`
    - `/ressources-gratuites` -> `/ressources-gratuites/cours`
  - Expose `/robots.txt` et `/sitemap.xml`.
- `frontend/public/netlify.toml:1-56`
  - Meme logique pour Netlify (domaine + redirects + fallback SPA).
- `frontend/nginx.conf:12-16`
  - Ajoute `X-Robots-Tag: noindex, follow` sur pages legales.

## 3) Robots et directives d'indexation serveur

- `frontend/public/robots.txt:1-69`
  - Autorise globalement le public.
  - Bloque les zones privees/app (`/dashboard`, `/account`, `/admin`, etc.).
  - Bloque les pages legales pour `User-agent: *`.
  - Cas special Googlebot: pages legales non bloquees pour laisser lire `meta robots noindex`.
  - Pointe vers `Sitemap: https://www.optitab.net/sitemap.xml`.
- `frontend/public/_headers:1-12`
  - Double securite noindex via `X-Robots-Tag` pour pages legales:
    - `/cgv`, `/cgu`, `/confidentialite`, `/legal`, `/cookies`, `/conditions`.

## 4) Meta SEO de base dans le HTML initial

- `frontend/index.html:87-102`
  - Meta par defaut:
    - `description`
    - `robots`
    - Open Graph (`og:*`)
    - Twitter cards (`twitter:*`)
  - Sert de fallback avant que Vue Router applique le SEO dynamique.

## 5) Moteur SEO central cote frontend (SPA)

- `frontend/src/services/seo.js:75-80`
  - `getRobotsForRoute()`:
    - `noindex,follow` si route forcee en noindex.
    - `noindex,follow` aussi si query params non tracking (anti-duplication URL).
- `frontend/src/services/seo.js:239-342`
  - `setPageSeo()` met a jour dynamiquement:
    - `document.title`
    - `meta description`, `meta robots`
    - `link rel=canonical`
    - OG + Twitter tags
    - JSON-LD global (`Organization`, `WebSite`, `WebPage`) + graph additionnel.
- `frontend/src/services/seo.js:344-441`
  - `ROUTE_SEO` mappe les routes publiques principales (home, cours particuliers, ressources gratuites, tarifs, about, contact, etc.).
  - Pages legales en `noindex`.
- `frontend/src/services/seo.js:443-448`
  - Routes systeme forcees noindex:
    - `PasswordReset`, `NotFound`, `Calculator`, `TestFiltrageStrict`.
- `frontend/src/services/seo.js:450-495`
  - `applyRouteSeo(route)` applique automatiquement le SEO route par route.

## 6) Point d'entree routeur: application automatique du SEO

- `frontend/src/router/index.js:6`
  - Import de `applyRouteSeo`.
- `frontend/src/router/index.js:275-294`
  - Normalisation des trailing slashes (evite variantes d'URL).
- `frontend/src/router/index.js:296-299`
  - `router.afterEach(...)` appelle `applyRouteSeo(to)` a chaque navigation.
- `frontend/src/router/index.js:126-213`
  - Beaucoup de routes privees ont `meta.requiresAuth`/`requiresSubscription`:
    - elles passent automatiquement en noindex via `applyRouteSeo`.
  - Exemple de ta vue active:
    - `ExercicesByNotion` -> `frontend/src/views/ChapterExercises.vue` est une route privee (`requiresAuth + requiresSubscription`) donc noindex systeme.

## 7) Surcouches SEO specifiques dans certaines vues

- `frontend/src/views/TarifsPage.vue:112-119`
  - Re-definit explicitement title/description/canonical.
  - Ajoute JSON-LD breadcrumb + FAQ.
- `frontend/src/views/FreeCourseDetail.vue:447-487, 489-647`
  - Calcule canonical dynamique (cours/synthese/exercice).
  - Redirige vers URL canonique si params non canoniques.
  - Genere title/description adaptes au contenu.
  - Ajoute JSON-LD `BreadcrumbList` + `Article`.
  - Force `noindex,follow` pour `resourceType === 'exercise'`.
  - En erreur: page introuvable en noindex.
- `frontend/src/views/FreeExerciseChapter.vue:319-403, 437-447`
  - Recalcule URL canonique du chapitre et redirige si besoin.
  - Set SEO dynamique (title/description/canonical/OG).
  - Ajoute JSON-LD `BreadcrumbList` + `ItemList`.
  - En erreur: noindex.
- `frontend/src/views/FreeExerciseSlug.vue:36-180`
  - Resolution de slug legacy -> redirection vers URL canonique de chapitre.

## 8) Markup semantique dans le contenu

- `frontend/src/components/home/HomeSeoSection.vue:2-37`
  - Microdata Schema.org dans le DOM (`WebPage`, `Product`, `Service`).
  - Liens internes vers pages SEO strategiques.

## 9) Cote backend (page API)

- `backend/core/templates/core/index.html:69`
  - `meta name="robots" content="noindex"` pour la page d'entree API.

---

## Synthese rapide: comment ca fonctionne globalement

1. Au build, le sitemap est regenere automatiquement.
2. En prod, les redirects imposent le domaine canonique et des URLs propres.
3. `robots.txt` + headers noindex filtrent ce qui doit etre crawlable.
4. Le HTML de base fournit des metas SEO par defaut.
5. A chaque navigation SPA, `applyRouteSeo()` met a jour title/meta/canonical/JSON-LD.
6. Certaines vues (tarifs, details ressources gratuites) raffinent encore le SEO et corrigent l'URL canonique en live.

## Point d'attention a verifier

- `ROUTE_SEO` met `FreeResourcesHome` en canonical `/ressources-gratuites` (`frontend/src/services/seo.js:429-433`), alors que les redirects envoient `/ressources-gratuites` vers `/ressources-gratuites/cours` (`frontend/public/_redirects:8`, `frontend/public/netlify.toml:35-37`).  
  Ce n'est pas forcement bloquant, mais c'est une incoherence de canonique a trancher.
