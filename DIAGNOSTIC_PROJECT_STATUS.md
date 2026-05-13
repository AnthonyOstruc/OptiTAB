# Projet Landing Diagnostic Maths Gratuit — État d'avancement

> **Objectif :** capturer des leads (élèves + parents) en échange d'un diagnostic
> personnalisé gratuit, puis convertir via une séquence email de 5 messages.

**URL publique :** `https://www.optitab.net/diagnostic-maths-gratuit`
**URL de remerciement :** `https://www.optitab.net/diagnostic-merci` *(noindex)*
**Endpoint API :** `POST /api/newsletter/diagnostic-lead/`

---

## ✅ Ce qui est livré

### 1. Frontend — Landing page complète

**Fichier :** [frontend/src/views/DiagnosticLanding.vue](frontend/src/views/DiagnosticLanding.vue)

- Design 100 % aligné sur la charte OptiTAB *(tokens repris de `GoogleAdsLanding.vue`)*
- 10 sections : hero · lead magnet · douleurs · solution · aperçu · formulaire principal · trust · comparaison · FAQ · CTA final
- Mobile-first avec sticky CTA mobile
- Formulaire 4 champs *(prénom, email, niveau, difficulté)* + opt-in RGPD *(non pré-coché)*
- Honeypot anti-bot caché
- Validation inline + IntersectionObserver pour tracker la visibilité des formulaires
- 3 formulaires sur la page *(hero, milieu, CTA final)*
- Tracking : `lead_form_viewed`, `level_selected`, `difficulty_selected`, `lead_submitted`
- SEO + canonical sur `/diagnostic-maths-gratuit`

### 2. Frontend — Page de remerciement `/diagnostic-merci`

**Fichier :** [frontend/src/views/DiagnosticMerci.vue](frontend/src/views/DiagnosticMerci.vue)

- Hero personnalisé `Merci {firstName} !` *(via sessionStorage)*
- Sections : "Ce qui se passe maintenant" *(3 étapes)* · aperçu plateforme · aide spam · CTA final
- `noindex,nofollow` *(double protection : meta tag + route meta)*
- Tracking : `diagnostic_lead_thank_you_viewed`, `thank_you_cta_clicked`
- Auto-clear de la session après affichage *(évite la réutilisation d'un ancien prénom)*

### 3. Frontend — API helper + routes

- [frontend/src/api/newsletter.js](frontend/src/api/newsletter.js) — fonction `submitDiagnosticLead(payload)`
- [frontend/src/router/index.js](frontend/src/router/index.js) — routes `/diagnostic-maths-gratuit` + `/diagnostic-merci`

### 4. Backend — Modèle, vue, URL, migration

| Fichier | Contenu |
|---|---|
| [backend/core/models.py](backend/core/models.py) | Modèle `DiagnosticLead` avec 25 champs *(form, RGPD, attribution, FK newsletter)* |
| [backend/core/migrations/0002_diagnosticlead.py](backend/core/migrations/0002_diagnosticlead.py) | Migration *(déjà appliquée sur la prod Render)* |
| [backend/core/newsletter_views.py](backend/core/newsletter_views.py) | Vue `diagnostic_lead()` avec honeypot, validation, RGPD, upsert newsletter |
| [backend/core/urls.py](backend/core/urls.py) | URL `POST /api/newsletter/diagnostic-lead/` |

**Comportement clé de l'endpoint :**
- Stocke le lead avec tout son contexte d'acquisition
- Si opt-in marketing coché → upsert `NewsletterSubscriber` avec `source='diagnostic_landing'`
- Envoie l'email de bienvenue *(template existant réutilisé)*
- Capture IP de consentement *(preuve RGPD)*
- Tronque les UTM trop longs

### 5. Backend — Admin Django

**Fichier :** [backend/core/admin.py](backend/core/admin.py)

- URL : `/admin/core/diagnosticlead/`
- Colonnes : email, prénom, niveau, difficulté, opt-in, date envoyé, utm_source, date création
- Filtres : niveau, difficulté, opt-in, emplacement formulaire, utm_source, utm_campaign, date
- Recherche : email, prénom, utm_campaign, utm_source, gclid, fbclid
- **Action export CSV** : UTF-8 BOM, séparateur `;`, 23 colonnes *(Excel-friendly)*
- **Action "marquer diagnostic envoyé"** : bulk update non destructif
- Fieldsets : Lead · RGPD · Newsletter · Attribution · Métadonnées
- Champs RGPD en lecture seule *(préservation de la preuve)*

### 6. Backend — Tests automatisés

**Fichier :** [backend/core/tests.py](backend/core/tests.py)

**25 tests, tous passants en 8 s** *(`python manage.py test core.tests --keepdb --noinput`)*

Couverture :
- Endpoint : cas nominal avec/sans opt-in · validation des 4 champs · 7 levels valides · 5 difficulties valides · honeypot · email lowercase · multi-submission · réactivation de désabonné · IP X-Forwarded-For · résilience SMTP · truncation UTM
- Modèle : `__str__` · `mark_diagnostic_sent` · defaults
- Admin : export CSV format · séparateur `;` · `oui/non` · `mark_diagnostic_sent` (action) · non-écrasement

### 7. Contenu — Séquence 5 emails

**Localisation :** dans la conversation initiale *(étape 2)*, à reporter dans Brevo/Mailjet.

| # | J+ | Sujet | Objectif |
|---|---|---|---|
| E1 | 0 h | `📋 {{firstName}}, ton diagnostic OptiTAB est arrivé` | Délivrer le PDF |
| E2 | +48 h | `Pourquoi tu bloques en maths (la vraie raison)` | Engagement |
| E3 | +96 h | `La méthode étape par étape (avec un exercice)` | Démontrer la valeur |
| E4 | +7 j | `Comment OptiTAB peut t'aider (sans cours particuliers)` | Soft pitch |
| E5 | +12 j | `[Dernier email] Es-tu prêt·e à progresser vraiment ?` | CTA abonnement |

Plein texte + variables `{{firstName}}`, `{{niveau}}`, `{{difficulte}}`, `{{diagnostic_url}}` + UTM-taggés dans le fil de conversation.

### 8. Contenu — Template PDF diagnostic

**Fichier :** [DIAGNOSTIC_PDF_TEMPLATE.md](DIAGNOSTIC_PDF_TEMPLATE.md)

- Structure 8 pages
- Variantes par `level` *(7 niveaux : Collège → BTS + Parent)*
- Variantes par `difficulty` *(5 difficultés)*
- Charte design *(couleurs, typo, mise en page)*
- Plan v1 → v2 → v3 *(du PDF unique au rendu HTML conditionnel)*

---

## ⏭️ Ce qui reste à faire pour la prochaine fois

### Priorité 1 — Mise en production

- [ ] **Vérifier le déploiement frontend** sur Render
  - `git add` + `git commit` + `git push` → Render redéploie automatiquement
  - Fichiers à committer : 4 nouveaux + 3 modifiés *(voir `git status`)*
- [ ] **Confirmer la migration `0002_diagnosticlead`** sur Render *(déjà appliquée pendant le debug, mais à confirmer après prochain déploiement)*
- [ ] **Tester l'endpoint en prod** : soumettre un formulaire de test depuis `optitab.net/diagnostic-maths-gratuit`, puis vérifier dans `/admin/core/diagnosticlead/`

### Priorité 2 — Faire fabriquer le PDF diagnostic v1

- [ ] Donner [DIAGNOSTIC_PDF_TEMPLATE.md](DIAGNOSTIC_PDF_TEMPLATE.md) à un designer *(ou faire soi-même sur Canva)*
- [ ] Version v1 minimale : **1 seul PDF** = la version `Terminale + cours_vs_exercices` *(~6 pages, 2-3 h de design)*
- [ ] Héberger le PDF *(S3 / Render static / Brevo media)*
- [ ] Récupérer l'URL publique du PDF pour la passer à Brevo

### Priorité 3 — Configurer Brevo (ou Mailjet)

- [ ] Créer un segment `diagnostic_leads` filtrant sur `source = diagnostic_landing`
- [ ] Vérifier authentification SPF + DKIM + DMARC sur `optitab.net`
- [ ] Créer une **automation 5 emails** déclenchée sur l'ajout dans le segment
- [ ] Coller le contenu des 5 emails depuis la conversation *(étape 2)*
- [ ] Attacher l'URL du PDF dans la variable `{{params.diagnostic_url}}` de l'E1
- [ ] Régler les délais : 0 h · 48 h · 96 h · 7 j · 12 j
- [ ] Activer les stop conditions : `unsubscribe`, achat abonnement *(via webhook Stripe)*
- [ ] Activer le tracking ouvertures + clics

### Priorité 4 — Configurer la conversion GA4

- [ ] Dans GA4, créer un événement de conversion :
  ```
  Event name: page_view
  Condition: page_path equals /diagnostic-merci
  Mark as conversion: "Diagnostic Lead Submitted"
  ```
- [ ] *(Optionnel)* Connecter Google Ads à GA4 pour importer la conversion
- [ ] *(Optionnel)* Configurer Meta CAPI / TikTok Events API côté serveur en se branchant sur `lead_submitted` dataLayer

### Priorité 5 — Optimisations *(quand tu auras du volume)*

- [ ] **Variante parent des 5 emails** *(vouvoiement, ton parent, segment `level=parent`)*
- [ ] **PDFs v2** : 7 versions par niveau *(Collège, Seconde, Première, Terminale, Prépa, BTS, Parent)*
- [ ] **PDFs v3** : 35 combinaisons level × difficulty rendues à la volée *(template HTML + Puppeteer)*
- [ ] **A/B test** sur les sujets d'email *(variantes proposées dans l'étape 2)*
- [ ] **Mockup hero** : remplacer le mockup CSS du hero par un vrai PNG/WebP designé

### Priorité 6 — Hygiène technique

- [ ] **Ajouter `/diagnostic-maths-gratuit` au sitemap** : `npm run generate:sitemap` côté frontend
- [ ] **Documenter la procédure de prod** dans `PRODUCTION_SETUP.md` *(migration + redémarrage)*
- [ ] **Brancher un monitoring** sur l'endpoint *(Sentry / Render logs alerts)* — alerter si > X erreurs 500/min
- [ ] **Rate limiter** l'endpoint au niveau infra *(5 req/IP/heure)* — actuellement seul le honeypot protège

---

## 🔧 Commandes utiles

### Frontend

```bash
cd frontend
npm run dev               # serveur dev
npm run build             # build prod
```

### Backend

```bash
cd backend
./venv/Scripts/python.exe manage.py check                                    # validation Django
./venv/Scripts/python.exe manage.py migrate core                             # appliquer la migration
./venv/Scripts/python.exe manage.py test core.tests --keepdb --noinput -v 2  # lancer les tests
./venv/Scripts/python.exe manage.py runserver                                # serveur local
```

### Vérifier que tout marche en local

```bash
# Terminal 1
cd backend && ./venv/Scripts/python.exe manage.py runserver

# Terminal 2
cd frontend && npm run dev

# Navigateur : http://localhost:5173/diagnostic-maths-gratuit
# Remplis le formulaire → tu dois être redirigé sur /diagnostic-merci
# Va dans /admin/core/diagnosticlead/ pour voir le lead créé
```

---

## 📚 Fichiers de référence

| Fichier | Rôle |
|---|---|
| [DIAGNOSTIC_PDF_TEMPLATE.md](DIAGNOSTIC_PDF_TEMPLATE.md) | Template complet pour fabriquer le PDF diagnostic |
| [DIAGNOSTIC_PROJECT_STATUS.md](DIAGNOSTIC_PROJECT_STATUS.md) | Ce document — état d'avancement |

---

## 🎯 État final

```
Frontend  ████████████████████ 100 %  (page + thank-you + API helper)
Backend   ████████████████████ 100 %  (modèle + vue + URL + admin)
Tests     ████████████████████ 100 %  (25/25 passants)
Contenu   ████████████░░░░░░░░  60 %  (emails OK, PDF à fabriquer)
Brevo     ░░░░░░░░░░░░░░░░░░░░   0 %  (à configurer)
Tracking  ██████████░░░░░░░░░░  50 %  (events posés, conversion GA4 à câbler)
```

**Le système est techniquement prêt à recevoir des leads.**
Il manque : le PDF v1, la config Brevo, et la conversion GA4 pour boucler la boucle.
