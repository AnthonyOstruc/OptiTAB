# SEO Canonical Policy

This document defines the canonical URL policy used by the frontend SEO layer.

## Canonical URL formats

- Hub: `/ressources-gratuites`
- Lists:
  - `/ressources-gratuites/cours`
  - `/ressources-gratuites/exercices`
  - `/ressources-gratuites/syntheses`
- Course detail (canonical): `/ressources-gratuites/cours/:pays/:niveauGroup/:matiere/:slug-:id`
- Summary detail (canonical): `/ressources-gratuites/syntheses/:pays/:niveauGroup/:matiere/:slug-:id`
- Exercise chapter (canonical): `/ressources-gratuites/exercices/:pays/:niveauGroup/:matiere/:slug-:id`
- Exercise detail (canonical): `/ressources-gratuites/exercices/:slug`

## Indexing gate for dynamic pages

- A dynamic page is indexable only when `route.path` matches its computed canonical path.
- If the current URL is non-canonical:
  - set `robots` to `noindex,follow`
  - set `<link rel="canonical">` to the computed canonical URL
  - keep `router.replace(...)` to the canonical route
- If the current URL is canonical:
  - use indexable robots (`index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1`)
  - keep canonical link as self
