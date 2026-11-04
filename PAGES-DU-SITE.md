# Pages du site OptiTAB

Inventaire de toutes les pages du site (tiré du fichier des routes `frontend/src/router/index.js`), à jour au **3 novembre 2026**.

## Légende

| Pastille | Signification |
|:---:|---|
| 🟢 | **Refaite** : nouveau design (vitrine le 2 novembre, espace connecté le 3 novembre 2026), textes revus |
| 🟡 | Retouchée : nouveau cadre ou correction technique, contenu d'origine |
| ⚪ | Inchangée : ancien design |
| ↪ | Ancienne adresse : elle renvoie automatiquement vers la nouvelle page (liens et favoris toujours valables) |
| 🔒 | Abonnement ou pass requis (sinon l'élève est redirigé) |

## En résumé

| Espace | Pages | 🟢 Refaites | 🟡 Retouchées | ⚪ Inchangées | ↪ Anciennes adresses |
|---|:---:|:---:|:---:|:---:|:---:|
| Hors connexion | 36 | 18 | 17 | 1 | 4 |
| Avec connexion (élève ou parent) | 15 | 4 | 11 | 0 | 16 |
| Administration | 24 | 0 | 0 | 24 | – |
| **Total** | **75** | **22** | **28** | **25** | **20** |

Une même page peut avoir plusieurs adresses (anciens liens conservés) : elles sont regroupées sur une seule ligne.

---

## 1. Pages hors connexion

Depuis le 3 novembre 2026, toutes les pages publiques ont l'en-tête et le pied de page de la vitrine (version épurée « logo + contact + action » pour les pages publicitaires et de paiement). Les pages 🟡 ci-dessous gardent leur contenu d'origine.

### Vitrine et présentation

| État | Adresse | Page | Remarque |
|:---:|---|---|---|
| 🟢 | `/` | **Accueil** | Nouvelle vitrine : en-tête allégé orienté abonnement, 5 exemples de corrections qui défilent, chiffres réels, choix de la classe, vidéos de démonstration, formules, FAQ, référencement Google revu |
| 🟢 | `/apercu/accueil` | Ancienne adresse d'aperçu | Redirige vers l'accueil |
| 🟢 | `/tarifs` | **Tarifs** | Les 3 étapes (sans inscription, compte gratuit, abonnement), formules en direct, tableau comparatif, encart cours particuliers, FAQ paiement et résiliation |
| 🟢 | `/cours-particuliers` | **Cours particuliers** | Page écrite à la 1re personne : le professeur, le déroulé en 5 étapes, la méthode, tarifs par niveau (à l'heure, packs, suivi VIP), FAQ, formulaire « premier échange gratuit ». Section témoignages prête mais masquée pour l'instant. Une fois connecté, elle s'affiche dans l'espace élève |
| 🟢 | `/about` | **À propos** | L'histoire en frise (de l'ingénieur à la plateforme), chiffres réels, engagements, mot pour les parents, réseaux sociaux |
| 🟢 | `/contact` | **Contact** | WhatsApp, e-mail ou formulaire au choix, réponses rapides (tarifs, mot de passe oublié…), sujet pré-rempli possible (`/contact?sujet=Partenariat`) |
| 🟡 | `/calculator` | Outil de calcul | Accessible sans compte. Connecté : dans le nouvel espace. Graphique recentré sur téléphone et tablette (il débordait à 768 px) |
| 🟡 | `/aide-grapheur` | Aide du grapheur | |

### Ressources gratuites

| État | Adresse | Page | Remarque |
|:---:|---|---|---|
Refaites de zéro le 3 novembre 2026 en **pages statiques** (générées à chaque construction du site par `frontend/scripts/ressources/`) : tout le texte, les formules et les schémas sont dans la page, lisibles par Google et les assistants d'IA. Gratuit : tous les cours et toutes les fiches du CP à la Terminale, et au moins 3 exercices corrigés par chapitre (820). Voir aussi `/llms.txt` et `/sitemap-ressources.xml`.

| État | Adresse | Page | Remarque |
|:---:|---|---|---|
| 🟢 | `/ressources-gratuites/` | **Accueil des ressources gratuites** | Les 12 classes par cycle, mode d'emploi, abonnement et cours particuliers, FAQ |
| 🟢 | `/ressources-gratuites/maths/<classe>/` | **Une classe** (12 pages : `cp` … `terminale`) | Chapitres par thème avec liens Cours · Fiche · Exercices |
| 🟢 | `/ressources-gratuites/maths/<classe>/<chapitre>/` | **Cours d'un chapitre** (272 pages) | Sommaire, schémas décrits, chapitres voisins, version texte `index.md` |
| 🟢 | `…/<chapitre>/fiche/` | **Fiche de révision** (272 pages) | Bouton « Imprimer la fiche » |
| 🟢 | `…/<chapitre>/exercices/` | **Exercices corrigés** (272 pages) | Énoncés, corrections détaillées dépliables, réponses |
| ↪ | `/ressources-gratuites/cours`, `/exercices`, `/syntheses` | Anciens accueils | Vers l'accueil des ressources |
| ↪ | `/ressources-gratuites/cours/…` (3 formats d'adresse) | Ancien cours gratuit | Vers le cours du chapitre |
| ↪ | `/ressources-gratuites/exercices/notion/:id`, `/exercices/…` (4 formats) | Anciens exercices gratuits | Vers les exercices corrigés du chapitre |
| ↪ | `/ressources-gratuites/syntheses/…` (3 formats d'adresse) | Ancienne fiche gratuite | Vers la fiche du chapitre |

### Blog

| État | Adresse | Page |
|:---:|---|---|
| 🟡 | `/blog` | Liste des articles |
| 🟡 | `/blog/categorie/:slug` | Articles d'une catégorie |
| 🟡 | `/blog/tag/:slug` | Articles d'un mot-clé |
| 🟡 | `/blog/:slug` | Un article |

### Pages légales

| État | Adresse | Page | Remarque |
|:---:|---|---|---|
| 🟢 | `/legal` | **Mentions légales** | Nouveau design ; hébergeurs complétés (Render + Amazon Web Services) ; identité de l'entreprise à compléter |
| 🟢 | `/confidentialite` | **Politique de confidentialité** | Textes corrigés (cookies, prestataires, paiement Stripe, durées, droits) |
| 🟢 | `/cookies` | **Politique de cookies** | Tableau des cookies, bouton « Gérer mes cookies » |
| 🟢 | `/cgu` | **Conditions générales d'utilisation** | Suppression du compte « sur demande », services à jour |
| 🟢 | `/cgv` | **Conditions générales de vente** | Tarifs lus en direct, un niveau par abonnement, pass, cours particuliers, plateforme européenne des litiges retirée (fermée en 2025) |
| 🟢 | `/conditions` | **Conditions et informations légales** | Devenue le sommaire des 5 documents légaux, résumés en quelques lignes ; l'ancien texte, qui contredisait les CGU (13 ans au lieu de 15), est supprimé |

### Pages publicitaires et réseaux sociaux

| État | Adresse | Page |
|:---:|---|---|
| 🟡 | `/start` (aussi `/commencer`) | Page d'arrivée publicité |
| 🟡 | `/plateforme-maths` | Page d'arrivée « plateforme de maths » |
| 🟡 | `/bases-methode` | Page d'arrivée « bases et méthode » |
| 🟡 | `/exercices-corriges` (aussi `/exercices-corriges-pas-a-pas`) | Page d'arrivée « exercices corrigés » |
| 🟡 | `/diagnostic-maths-gratuit` | Diagnostic gratuit |
| 🟡 | `/diagnostic-merci` | Remerciement après le diagnostic |
| 🟡 | `/avis` (aussi `/optitab`, `/instagram`, `/facebook`, `/tiktok`, `/youtube`, `/snapchat`) | Page « lien en bio » (témoignages) |

### Paiement et compte

| État | Adresse | Page |
|:---:|---|---|
| 🟡 | `/paiement` | Régler un cours particulier |
| 🟡 | `/paiement/merci` | Confirmation de paiement d'un cours |
| 🟡 | `/billing/success` | Confirmation d'abonnement |
| 🟡 | `/billing/cancel` | Paiement d'abonnement annulé |
| ⚪ | `/password-reset` | Nouveau mot de passe |

### Divers

| État | Adresse | Page | Remarque |
|:---:|---|---|---|
| 🟢 | toute adresse inconnue | **Page introuvable (404)** | Refaite le 3 novembre 2026 : liens utiles (vitrine pour un visiteur, espace pour un élève connecté). Aussi affichée pour l'ancienne page de test `/test-filtrage-strict` |

---

## 2. Pages avec connexion (élève ou parent)

Depuis le 3 novembre 2026, toutes ces pages s'affichent dans le **nouvel espace** : menu latéral (ordinateur) ou barre d'onglets (téléphone), recherche de chapitres, carte « Anthony, ton prof ». L'administration garde son ancien cadre.

### Nouvel espace

| État | Adresse | Page | Remarque |
|:---:|---|---|---|
| 🟢 | `/dashboard` | **Tableau de bord élève ou parent** (selon le compte) | Élève : reprendre, semaine, à revoir, programme. Parent : une carte par enfant, ajout (invitation ou création du compte), demandes en attente. Démonstration réservée au compte démo et aux administrateurs : `?exemple=1`, `?vue=parent` |
| 🟢 | `/chapitres` | **Mes chapitres** | Tout le programme par thème, progression de chaque chapitre, filtres, recherche |
| 🟢 🔒 | `/chapitre/:id` | **Un chapitre** : onglets Cours, Fiche, Exercices | Remplace les anciennes pages de cours, de fiche et d'exercices |
| 🟢 | `/child/:childId` | **Suivi détaillé d'un enfant** (parent) | Semaine, résultats, progression par chapitre, points à revoir, activité récente, « Ne plus suivre » |

### Pages passées dans le nouvel espace (contenu d'origine)

| État | Adresse | Page | Remarque |
|:---:|---|---|---|
| 🟡 | `/account` | Mon compte | |
| 🟡 | `/billing` | Abonnement (formules) | Onglet « Gérer mon abonnement » conservé |
| 🟡 | `/subscription` | Mon abonnement (résiliation) | |
| 🟡 | `/historique-exercices` | Historique des exercices | Ajouté au menu (« Historique ») |
| 🟡 | `/historique-quiz` | Historique des quiz | |
| 🟡 | `/mes-quiz-rendus` | Mes quiz rendus | |
| 🟡 | `/quiz`, `/quiz/:matiereId` | Quiz | Dans le menu seulement si des quiz sont publiés pour la classe (aucun au 3 novembre 2026) |
| 🟡 🔒 | `/quiz-notion/:notionId` | Quiz d'un chapitre (dont le devoir `/quiz-notion/153`) | |
| 🟡 | `/quiz-coming-soon` | Quiz bientôt disponible | |
| 🟡 🔒 | `/exercice/:exerciceId` | Un exercice | Ouvre l'exercice dans son chapitre (son bouton retour menait à une adresse disparue) |

### Anciennes adresses (renvoyées vers le nouvel espace)

| État | Ancienne adresse | Arrive sur |
|:---:|---|---|
| ↪ | `/online-courses`, `/course-notions/:matiereId`, `/exercises`, `/exercicies/:matiereId`, `/notions/:matiereId`, `/theme-notions/:themeId`, `/sheets`, `/tables-formules`, `/progress` | `/chapitres` |
| ↪ | `/course-notion/:id`, `/cours/:matiere/:id/:chapitre`, `/cours/:matiere/:id/:chapitre/:cours` | `/chapitre/:id` (onglet Cours) |
| ↪ | `/sheets-notion/:id`, `/tables-formules-notion/:id` | `/chapitre/:id` (onglet Fiche) |
| ↪ | `/exercices-notion/:id` (avec `#ex-…`) | `/chapitre/:id` (onglet Exercices, sur l'exercice demandé) |
| ↪ | `/pricing` | `/billing` (l'ancienne page appelait une adresse serveur disparue) |
| ↪ | `/apercu/espace…` (adresses de l'aperçu) | adresses définitives |

---

## 3. Administration (compte administrateur)

| État | Adresse | Page |
|:---:|---|---|
| ⚪ | `/admin` | Accueil de l'administration |
| ⚪ | `/admin/newsletter` | Newsletter |
| ⚪ | `/admin/subscriptions` | Abonnements |
| ⚪ | `/admin/subscribers` | Abonnés |
| ⚪ | `/admin/passes` | Pass |
| ⚪ | `/admin/matieres` | Matières |
| ⚪ | `/admin/themes` | Thèmes |
| ⚪ | `/admin/notions` | Chapitres |
| ⚪ | `/admin/exercices` | Exercices |
| ⚪ | `/admin/exercices-plus` | Exercices (outil avancé) |
| ⚪ | `/admin/cours` | Cours |
| ⚪ | `/admin/cours-pdf` | Cours en PDF |
| ⚪ | `/admin/cours-plus` | Cours (outil avancé) |
| ⚪ | `/admin/sheets` | Fiches de synthèse |
| ⚪ | `/admin/quiz` | Quiz |
| ⚪ | `/admin/quiz-plus` | Quiz (outil avancé) |
| ⚪ | `/admin/quiz-submissions` | Quiz rendus |
| ⚪ | `/admin/niveaux` | Niveaux |
| ⚪ | `/admin/pays` | Pays |
| ⚪ | `/admin/reel-studio` | Studio de vidéos courtes |
| ⚪ | `/admin/reel-background` | Fonds des vidéos courtes |
| ⚪ | `/admin/blog` | Blog |
| ⚪ | `/admin/temoignages` | Témoignages (et mise en ligne de `/avis`) |
| ⚪ | `/jeux/math-run` | Jeu Math Run (réservé à l'administrateur) |

---

## Éléments communs à plusieurs pages

| État | Élément | Où il apparaît |
|:---:|---|---|
| 🟢 | En-tête allégé de la vitrine (logo, 4 liens, « Se connecter », « S'abonner » ; « Mon espace » si l'élève est connecté) | Accueil, Tarifs, Cours particuliers, À propos, Contact, Conditions et 5 pages légales |
| 🟢 | Pied de page de la vitrine (liens, contact, newsletter, avis Google, mentions) | Mêmes pages |
| 🟢 | Bloc des formules (étapes + cartes de prix, carrousel sur téléphone) | Accueil et Tarifs |
| 🟢 | Formulaire de contact (version « message » et version « demande de cours ») | Contact et Cours particuliers |
| 🟢 | Vidéos de démonstration (ordinateur et téléphone, compte démo « Lucas Martin ») | Accueil |
| 🟡 | Cartes de prix : majuscule ajoutée en début de chaque avantage | Partout où les formules s'affichent |
| 🟢 | Cadre du nouvel espace : menu latéral, recherche de chapitres (Ctrl K), barre d'onglets sur téléphone, carte « Anthony, ton prof » | Toutes les pages connectées (sauf administration) |
| 🟢 | Couleur et icône par thème (Analyse, Probabilités, Géométrie…) | Tableau de bord, chapitres, page chapitre, recherche |
| ⚪ | Ancien cadre de l'espace (menu, en-tête) | Administration uniquement |
| ⚪ | Ancien en-tête et ancien pied de page | Toutes les autres pages hors connexion |
| ⚪ | Bandeau des cookies | Tout le site |
| ⚪ | Fenêtres de connexion, d'inscription et de mot de passe oublié | Tout le site |
| ⚪ | Bouton WhatsApp flottant | Pages hors connexion |

## Prochaines étapes possibles

Tout le site a désormais le nouveau cadre et les couleurs OptiTAB. Pour aller plus loin, page par page :

1. Contenu des pages publicitaires (`/start`, `/plateforme-maths`, `/bases-methode`, `/exercices-corriges`, diagnostic) au style de l'accueil
2. Contenu des listes de ressources gratuites et du blog
3. Mise en page de Mon compte, Abonnement et Historique (couleurs déjà harmonisées)
4. Page `/password-reset` (nouveau mot de passe)
