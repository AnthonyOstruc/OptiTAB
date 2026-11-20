// Gabarits HTML des ressources gratuites. Pages statiques complètes : texte,
// formules et figures sont dans le HTML (lisibles par Google et les IA).
import { CYCLES, CLASSES } from './classes.mjs'
import { titreDePage } from './titres.mjs'

export const SITE = 'https://www.optitab.net'
export const RACINE = '/ressources-gratuites/'

const ESC = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }
export const e = (t) => String(t ?? '').replace(/[&<>"']/g, (c) => ESC[c])

// ---------- Adresses ----------
export const urlClasse = (classe) => `${RACINE}maths/${classe.slug}/`
export const urlCours = (ch) => `${urlClasse(ch.classe)}${ch.slug}/`
export const urlFiche = (ch) => `${urlCours(ch)}fiche/`
export const urlExercices = (ch) => `${urlCours(ch)}exercices/`
export const urlMarkdown = (ch) => `${urlCours(ch)}index.md`
export const absolu = (chemin) => SITE + chemin

const DIFFICULTE = { easy: 'Facile', medium: 'Intermédiaire', hard: 'Difficile' }
const PREFIXE = /^(Découverte|Entraînement|Problème|Approfondissement|Synthèse|Bilan|Type examen|Type brevet|Type bac)\s*[-–:]\s*/i
export const titreExercice = (ex) => String(ex.titre || 'Exercice').replace(PREFIXE, '').trim()
export const typeExercice = (ex) => (String(ex.titre || '').match(PREFIXE) || [])[1] || ''

const pluriel = (n, un, plusieurs) => `${n} ${n > 1 ? plusieurs : un}`

// ---------- Icônes (traits, 24 px) ----------
const ICONES = {
  cours: '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>',
  fiche: '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/>',
  exercices: '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
  fleche: '<path d="M5 12h14M13 6l6 6-6 6"/>',
  retour: '<path d="M19 12H5M11 6l-6 6 6 6"/>',
  prof: '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>',
  check: '<path d="m5 12 5 5L20 7"/>',
  imprimer: '<path d="M6 9V3h12v6M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><path d="M6 14h12v7H6z"/>',
  menu: '<path d="M4 7h16M4 12h16M4 17h16"/>',
  // Rubriques de l'accueil des ressources
  formule: '<path d="M18 4H6l6 8-6 8h12"/>',
  table: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9.5h18M3 14.5h18M9 4v16M15 4v16"/>',
  calcul: '<rect x="5" y="2.5" width="14" height="19" rx="2"/><path d="M8.5 6.5h7v3h-7z"/><path d="M8.5 13.5h.01M12 13.5h.01M15.5 13.5h.01M8.5 17.5h.01M12 17.5h.01M15.5 17.5h.01"/>',
  operation: '<path d="M7 3.5v7M3.5 7h7M14 7h6.5M4.5 15.5l5 5M9.5 15.5l-5 5M14 18h6.5"/><path d="M17.25 15.25h.01M17.25 20.75h.01"/>',
  physique: '<path d="M9 3h6M10 3v6.5L4.6 18.4A1.7 1.7 0 0 0 6 21h12a1.7 1.7 0 0 0 1.4-2.6L14 9.5V3"/><path d="M7.5 15h9"/>'
}
const icone = (nom, cls = 'rg-ico') => `<svg class="${cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">${ICONES[nom]}</svg>`

// ---------- En-tête et pied de page ----------
function entete(actif = RACINE) {
  const liens = [
    ['/#methode', 'La méthode', 'method'],
    [RACINE, 'Ressources gratuites', 'free_resources'],
    ['/cours-particuliers', 'Cours particuliers', 'tutoring'],
    ['/tarifs', 'Tarifs', 'pricing']
  ]
  return `<header class="rg-header">
  <div class="rg-wrap rg-header__inner">
    <a href="/" class="rg-brand" aria-label="OptiTAB, cours de maths en ligne — accueil" data-track="nav" data-nav-name="home" data-nav-location="header_ressources"><img src="/logo-optitab.png" alt="OptiTAB" width="132" height="43"></a>
    <nav class="rg-nav" id="rg-nav" aria-label="Navigation principale">
      ${liens.map(([href, texte, nom]) => `<a href="${href}"${href === actif ? ' class="is-active"' : ''} data-track="nav" data-nav-name="${nom}" data-nav-location="header_ressources">${texte}</a>`).join('\n      ')}
      <a href="/?compte=connexion" class="rg-nav__login" data-cta-name="login" data-cta-location="header_ressources">Se connecter</a>
    </nav>
    <div class="rg-header__actions">
      <a href="/?compte=connexion" class="rg-login" data-cta-name="login" data-cta-location="header_ressources">Se connecter</a>
      <a href="/tarifs" class="rg-btn rg-btn--primary rg-btn--sm" data-cta-name="pricing" data-cta-location="header_ressources">S’abonner</a>
      <button type="button" class="rg-menu" aria-expanded="false" aria-controls="rg-nav" aria-label="Ouvrir le menu">${icone('menu')}</button>
    </div>
  </div>
</header>`
}

function pied(catalogue) {
  const colonnes = CYCLES.map((cy) => {
    const classes = catalogue.classes.filter((c) => c.cycle === cy.cle)
    return `<div class="rg-footer__col"><p class="rg-footer__title">${e(cy.titre)}</p><ul>${classes.map((c) => `<li><a href="${urlClasse(c)}">Maths ${e(c.court)}</a></li>`).join('')}</ul></div>`
  }).join('')
  return `<footer class="rg-footer">
  <div class="rg-wrap rg-footer__grid">
    <div class="rg-footer__brand">
      <img src="/logo-optitab.png" alt="OptiTAB" width="132" height="43" loading="lazy">
      <p>Cours de maths clairs, fiches de révision et exercices corrigés pas à pas, du CP à la Terminale. Et des profs disponibles en cours particuliers.</p>
      <p class="rg-footer__contact"><a href="mailto:contact@optitab.net">contact@optitab.net</a> · <a href="https://wa.me/33764040251" rel="noopener">WhatsApp 07 64 04 02 51</a></p>
    </div>
    ${colonnes}
    <div class="rg-footer__col"><p class="rg-footer__title">OptiTAB</p><ul>
      <li><a href="/cours-particuliers">Cours particuliers</a></li>
      <li><a href="/tarifs">Tarifs</a></li>
      <li><a href="${RACINE}maternelle/">Maths en maternelle</a></li>
      <li><a href="${RACINE}operations/">Poser les opérations</a></li>
      <li><a href="${RACINE}methodes/">Méthodes de calcul</a></li>
      <li><a href="${RACINE}fiches-a-imprimer/">Fiches à imprimer</a></li>
      <li><a href="${RACINE}formulaires/">Formulaires de maths</a></li>
      <li><a href="${RACINE}tables/">Tables de maths</a></li>
      <li><a href="${RACINE}physique-chimie/">Physique-chimie</a></li>
      <li><a href="/about">À propos</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="/contact">Contact</a></li>
    </ul></div>
  </div>
  <div class="rg-wrap rg-footer__legal">
    <span>© ${new Date().getFullYear()} OptiTAB</span>
    <a href="/legal">Mentions légales</a><a href="/confidentialite">Confidentialité</a><a href="/cookies">Cookies</a><a href="/cgu">CGU</a><a href="/cgv">CGV</a>
  </div>
</footer>`
}

// ---------- Squelette ----------
export function gabarit({ titre, description, chemin, contenu, catalogue, ctx, jsonld = [], image, type = 'website', markdown, motsCles, actif = RACINE, meta = '' }) {
  const canonique = absolu(chemin)
  const titrePage = titreDePage(titre)
  // Image de partage 1200 × 630 (la même que la vitrine) quand la page n'en a pas.
  const img = image || `${SITE}/og/optitab.png`
  return `<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>${e(titrePage)}</title>
<meta name="description" content="${e(description)}">
<link rel="canonical" href="${canonique}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1">
${motsCles ? `<meta name="keywords" content="${e(motsCles)}">\n` : ''}<meta name="theme-color" content="#1b3c8e">
<meta name="color-scheme" content="light">
<meta property="og:site_name" content="OptiTAB">
<meta property="og:locale" content="fr_FR">
<meta property="og:type" content="${type}">
<meta property="og:title" content="${e(titre)}">
<meta property="og:description" content="${e(description)}">
<meta property="og:url" content="${canonique}">
<meta property="og:image" content="${e(img)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${e(titre)}">
<meta name="twitter:description" content="${e(description)}">
<meta name="twitter:image" content="${e(img)}">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png">
<link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png">
<link rel="apple-touch-icon" href="/favicon-192.png">
${markdown ? `<link rel="alternate" type="text/markdown" href="${markdown}" title="Version texte (Markdown)">\n` : ''}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700&amp;display=swap">
<link rel="stylesheet" href="${ctx.css}">
${meta}${ctx.suivi || ''}
${jsonld.map((j) => `<script type="application/ld+json">${JSON.stringify(j).replace(/</g, '\\u003c')}</script>`).join('\n')}
</head>
<body class="rg">
${ctx.suiviCorps || ''}
<a class="rg-skip" href="#contenu">Aller au contenu</a>
${entete(actif)}
<main id="contenu">
${contenu}
</main>
${pied(catalogue)}
${BANDEAU_COOKIES}
<script>${SCRIPT}${SCRIPT_COOKIES}</script>
</body>
</html>
`
}

// Bandeau des cookies : même texte, même enregistrement (clé, durée de 6 mois,
// cookie + stockage local) et mêmes événements que le bandeau de l'application
// (components/common/CookieConsent.vue). Un choix fait ici vaut pour tout le site.
const BANDEAU_COOKIES = `<section class="rg-cookies" id="rg-cookies" role="dialog" aria-label="Gestion des cookies" hidden>
  <div class="rg-cookies__text"><strong>Votre vie privée compte.</strong>
    <p>OptiTAB utilise des cookies essentiels pour le fonctionnement du site et des cookies de statistiques et marketing/publicité pour mesurer l’audience et personnaliser nos campagnes. Vous pouvez accepter, refuser ou personnaliser votre choix. <a href="/cookies">En savoir plus</a>.</p>
    <div class="rg-cookies__choix" hidden>
      <label><input type="checkbox" data-consent="analytics"> Statistiques (Google Analytics, Microsoft Clarity)</label>
      <label><input type="checkbox" data-consent="marketing"> Marketing / Publicité (Meta Pixel)</label>
    </div>
  </div>
  <div class="rg-cookies__actions">
    <button type="button" class="rg-btn rg-btn--primary rg-btn--sm" data-cookies="tout">Tout accepter</button>
    <button type="button" class="rg-btn rg-btn--ghost rg-btn--sm" data-cookies="rien">Tout refuser</button>
    <button type="button" class="rg-btn rg-btn--ghost rg-btn--sm" data-cookies="choix">Personnaliser</button>
  </div>
</section>`

const SCRIPT_COOKIES = `(function(){var K='optitab_cookie_consent_v1',b=document.getElementById('rg-cookies');if(!b)return;
function lire(){var s=null;try{s=JSON.parse(localStorage.getItem(K))}catch(e){}if(!s){var m=document.cookie.match(/(?:^|; )optitab_cookie_consent_v1=([^;]*)/);if(m){try{s=JSON.parse(decodeURIComponent(m[1]))}catch(e){}}}return s&&s.expiresAt&&s.expiresAt>Date.now()?s:null}
if(lire())return;b.hidden=false;
function enregistrer(a,m){var d=new Date(),f=new Date(d);f.setMonth(f.getMonth()+6);var p={analytics:a?'granted':'denied',marketing:m?'granted':'denied',updatedAt:d.toISOString(),expiresAt:f.getTime()},t=JSON.stringify(p);try{localStorage.setItem(K,t)}catch(e){}
document.cookie=K+'='+encodeURIComponent(t)+'; expires='+f.toUTCString()+'; path=/; SameSite=Lax'+(location.protocol==='https:'?'; Secure':'');
window.dataLayer=window.dataLayer||[];var g=window.gtag||function(){dataLayer.push(arguments)};window.gtag=g;
g('consent','update',{analytics_storage:p.analytics,ad_storage:p.marketing,ad_user_data:p.marketing,ad_personalization:p.marketing});
dataLayer.push({event:'optitab_consent_updated',analytics_consent:p.analytics,marketing_consent:p.marketing});if(m)dataLayer.push({event:'optitab_marketing_consent_granted',marketing_consent:p.marketing});b.hidden=true}
var choix=b.querySelector('.rg-cookies__choix'),perso=b.querySelector('[data-cookies="choix"]');
b.querySelector('[data-cookies="tout"]').addEventListener('click',function(){enregistrer(true,true)});
b.querySelector('[data-cookies="rien"]').addEventListener('click',function(){enregistrer(false,false)});
perso.addEventListener('click',function(){if(choix.hidden){choix.hidden=false;perso.textContent='Enregistrer'}else{enregistrer(b.querySelector('[data-consent="analytics"]').checked,b.querySelector('[data-consent="marketing"]').checked)}})})();`

// Menu sur téléphone, impression avec les corrections ouvertes.
const SCRIPT = `(function(){var b=document.querySelector('.rg-menu'),n=document.getElementById('rg-nav');if(b&&n){b.addEventListener('click',function(){var o=n.classList.toggle('is-open');b.setAttribute('aria-expanded',o?'true':'false')})}var p=document.querySelector('[data-imprimer]');if(p){p.addEventListener('click',function(){window.print()})}window.addEventListener('beforeprint',function(){document.querySelectorAll('details').forEach(function(d){d.setAttribute('data-ferme',d.open?'':'1');d.open=true})});window.addEventListener('afterprint',function(){document.querySelectorAll('details[data-ferme="1"]').forEach(function(d){d.open=false})})})();`

// ---------- Recherche (accueil des ressources) ----------
// L'index (recherche.json : chapitres, formulaires, tables, méthodes…) n'est
// chargé qu'au premier usage de la case. Sans JavaScript, la case est masquée.
const SCRIPT_RECHERCHE = `(function(){var z=document.querySelector('[data-recherche]');if(!z)return;z.hidden=false;
var i=z.querySelector('input'),r=z.querySelector('.rg-search__res'),et=document.getElementById('rg-search-etat'),idx=null,att=null;
function n(t){return ' '+String(t||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim()+' '}
function charger(){if(!att){att=fetch('/ressources-gratuites/recherche.json').then(function(x){return x.json()}).then(function(d){idx=d.map(function(e){return {t:e[0],s:e[1],u:e[2],k:n(e[0]+' '+e[1]+' '+(e[3]||''))}});return idx}).catch(function(){att=null;return []})}return att}
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function montrer(){var q=n(i.value).trim();if(q.length<2){r.hidden=true;r.innerHTML='';et.textContent='';return}
charger().then(function(d){var m=q.split(' ').filter(function(w){return w.length>1}).map(function(w){return w.length>5?w.slice(0,5):w});if(!m.length)m=[q];var s=function(e){var t=n(e.t);return (t.indexOf(' '+q)>-1?6:0)+(e.k.indexOf(' '+q)>-1?3:0)+m.filter(function(w){return t.indexOf(' '+w)>-1}).length},res=d.filter(function(e){return m.every(function(w){return e.k.indexOf(' '+w)>-1})});res.sort(function(a,b){return s(b)-s(a)});res=res.slice(0,8);
r.innerHTML=res.length?res.map(function(e){return '<li><a href="'+e.u+'"><strong>'+esc(e.t)+'</strong><span>'+esc(e.s)+'</span></a></li>'}).join(''):'<li class="rg-search__vide">Aucun résultat. Essaie un autre mot, ou choisis ta classe ci-dessous.</li>';
r.hidden=false;et.textContent=res.length?res.length+' résultat'+(res.length>1?'s':''):'Aucun résultat'})}
var tm;i.addEventListener('focus',charger);i.addEventListener('input',function(){clearTimeout(tm);tm=setTimeout(montrer,120)});
i.addEventListener('keydown',function(ev){if(ev.key==='Escape'){i.value='';montrer()}if(ev.key==='Enter'){var a=r.querySelector('a');if(a){ev.preventDefault();location.href=a.href}}})})();`

const RECHERCHE = `<div class="rg-search" data-recherche hidden>
        <label class="rg-search__box">
          <span class="rg-visually-hidden">Rechercher une leçon, un chapitre ou une formule</span>
          <svg class="rg-ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="11" cy="11" r="7"></circle><path d="m20 20-3.5-3.5"></path></svg>
          <input type="search" placeholder="Fractions, Pythagore, dérivée…" autocomplete="off" enterkeyhint="search" aria-controls="rg-search-res" aria-describedby="rg-search-etat">
        </label>
        <p class="rg-visually-hidden" id="rg-search-etat" aria-live="polite"></p>
        <ul class="rg-search__res" id="rg-search-res" hidden></ul>
      </div>
      <script>${SCRIPT_RECHERCHE}</script>`

// ---------- Blocs communs ----------
export function filAriane(etapes) {
  return `<nav class="rg-crumbs" aria-label="Fil d’Ariane"><ol>${etapes.map(([texte, href], i) => (
    i === etapes.length - 1 ? `<li aria-current="page">${e(texte)}</li>` : `<li><a href="${href}">${e(texte)}</a></li>`
  )).join('')}</ol></nav>`
}

// Étapes du fil d'Ariane (la dernière est la page affichée).
export function etapesAriane(classe, ch, page) {
  const etapes = [['Accueil', '/'], ['Ressources gratuites', RACINE]]
  if (classe) etapes.push([`Maths ${classe.court}`, urlClasse(classe)])
  if (ch) etapes.push([ch.titre, urlCours(ch)])
  if (page === 'fiche') etapes.push(['Fiche de révision', urlFiche(ch)])
  if (page === 'exercices') etapes.push(['Exercices corrigés', urlExercices(ch)])
  return etapes
}

function onglets(ch, actif) {
  // Libellé complet sur ordinateur, court sur téléphone (trois onglets sur une ligne).
  const items = [
    ['cours', 'Cours', 'Cours', urlCours(ch), true],
    ['fiche', 'Fiche de révision', 'Fiche', urlFiche(ch), Boolean(ch.fiche)],
    ['exercices', 'Exercices corrigés', 'Exercices', urlExercices(ch), ch.exercices.length > 0]
  ].filter((x) => x[4])
  return `<nav class="rg-tabs" aria-label="Contenu du chapitre">${items.map(([cle, long, court, href]) => (
    `<a href="${href}" class="rg-tab${cle === actif ? ' is-active' : ''}"${cle === actif ? ' aria-current="page"' : ''}>${icone(cle)}<span class="rg-tab__long">${long}</span><span class="rg-tab__court" aria-hidden="true">${court}</span>${cle === 'exercices' ? `<span class="rg-tab__n">${ch.exercices.length}</span>` : ''}</a>`
  )).join('')}</nav>`
}

function enTeteChapitre(ch, page, chapeau, infos) {
  const libelle = { cours: 'Cours', fiche: 'Fiche de révision', exercices: 'Exercices corrigés' }[page]
  const separateur = ch.titre.includes(':') ? ' –' : ' :'
  const h1 = page === 'cours' ? `${e(ch.titre)}` : `${e(ch.titre)}<span class="rg-h1__suite">${separateur} ${libelle.toLowerCase()}</span>`
  return `<header class="rg-chap">
  <div class="rg-wrap">
    ${filAriane(etapesAriane(ch.classe, ch, page))}
    <p class="rg-kicker">Maths ${e(ch.classe.court)} · Chapitre ${ch.numero} · ${e(ch.theme)}</p>
    <h1 class="rg-h1">${h1}</h1>
    ${chapeau ? `<p class="rg-lead">${chapeau}</p>` : ''}
    ${infos && infos.length ? `<ul class="rg-infos">${infos.map((i) => `<li>${e(i)}</li>`).join('')}</ul>` : ''}
    ${onglets(ch, page)}
  </div>
</header>`
}

function voisins(ch) {
  if (!ch.precedent && !ch.suivant) return ''
  const lien = (c, sens) => c ? `<a class="rg-neighbour rg-neighbour--${sens}" href="${urlCours(c)}">${sens === 'prev' ? icone('retour') : ''}<span><small>${sens === 'prev' ? 'Chapitre précédent' : 'Chapitre suivant'}</small><strong>${e(c.titre)}</strong></span>${sens === 'next' ? icone('fleche') : ''}</a>` : '<span></span>'
  return `<nav class="rg-neighbours" aria-label="Chapitres voisins">${lien(ch.precedent, 'prev')}${lien(ch.suivant, 'next')}</nav>`
}

const examen = (classe) => {
  if (!classe) return ''
  if (classe.slug === '3e') return ' et le brevet'
  if (classe.slug === 'premiere' || classe.slug === 'terminale') return ' et le bac'
  return ''
}

// Les cours particuliers sont proposés du collège à la prépa (pas en primaire).
const avecProf = (classe) => !classe || classe.cycle !== 'primaire'

// Ligne d'aide (cours particuliers) à gauche du bouton Imprimer : visible dès
// l'arrivée, sans gêner la lecture. Cours et fiches de maths, pages de physique-chimie.
export function ligneAide(question, lieu) {
  return `<a class="rg-aide" href="/cours-particuliers" data-cta-name="tutoring" data-cta-location="${lieu}">${icone('prof')}<span>${question} <strong>Un prof t’explique en cours particulier</strong></span>${icone('fleche')}</a>`
}

function lienAide(classe, lieu) {
  if (!avecProf(classe)) return ''
  return ligneAide('Besoin d’aide sur ce chapitre\u00a0?', lieu)
}

// Encadré « cours particuliers » placé au milieu d'une longue page (physique-chimie).
export function encartProf({ titre, texte, lieu }) {
  return `<aside class="rg-encart" aria-label="Cours particuliers">
  <span class="rg-encart__ico">${icone('prof')}</span>
  <div class="rg-encart__texte"><p class="rg-encart__titre">${e(titre).replace(/(\S+-\S+)/g, '<span class="rg-insecable">$1</span>')}</p><p>${e(texte)}</p></div>
  <a class="rg-btn rg-btn--green rg-btn--sm" href="/cours-particuliers" data-cta-name="tutoring" data-cta-location="${lieu}">Réserver un cours ${icone('fleche')}</a>
</aside>`
}

export function appelsAction(classe, ch, lieu) {
  const totalChapitre = ch && ch.totalExercices > ch.exercices.length
    ? `Les ${ch.totalExercices} exercices corrigés de ce chapitre, le suivi de tes progrès et des révisions guidées.`
    : 'Tous les exercices corrigés pas à pas, le suivi de tes progrès et des révisions guidées.'
  const prof = avecProf(classe)
  return `<section class="rg-ctas${prof ? '' : ' rg-ctas--seul'}" aria-label="Aller plus loin">
  <div class="rg-cta rg-cta--plateforme">
    <p class="rg-cta__kicker">Plateforme OptiTAB</p>
    <h2 class="rg-cta__title">S’entraîner jusqu’à maîtriser${classe ? ` le programme de ${e(classe.court)}` : ''}</h2>
    <p>${totalChapitre}</p>
    <a class="rg-btn rg-btn--primary" href="/tarifs" data-cta-name="pricing" data-cta-location="${lieu}">Découvrir l’abonnement ${icone('fleche')}</a>
  </div>
  ${prof ? `<div class="rg-cta rg-cta--prof">
    <p class="rg-cta__kicker">${icone('prof')} Cours particuliers</p>
    <h2 class="rg-cta__title">Un prof de maths${classe ? ` en ${e(classe.court)}` : ''}, en ligne</h2>
    <p>${classe ? 'Des séances individuelles avec un professeur, à distance, pour comprendre, combler ses lacunes et préparer les contrôles' + examen(classe) + '.' : 'Des séances individuelles en ligne en maths, physique-chimie et informatique, du collège à la prépa, avec un professeur expérimenté.'}</p>
    <a class="rg-btn rg-btn--green" href="/cours-particuliers" data-cta-name="tutoring" data-cta-location="${lieu}">Réserver un cours particulier ${icone('fleche')}</a>
  </div>` : ''}
</section>`
}

// Formulaires et tables liés au chapitre (ch.formulaires, rempli par generer.mjs) :
// une carte « Le formulaire … » ou « La table … » dans « Pour continuer » (maillage interne).
function cartesFormulaires(ch) {
  return (ch.formulaires || []).map((f) => `<a class="rg-next__card" href="${f.url}">${icone('fiche')}<span><strong>${e(f.titre)}</strong><small>${e(f.article)} : ${e(f.resume || 'à consulter ou imprimer')}</small></span></a>`).join('')
}

// ---------- Pages ----------
export function pageCours(ch, rendu) {
  // Titres du sommaire : HTML du titre de partie (ses formules sont composées avec la page).
  const sommaire = rendu.titres.length > 2 ? `<aside class="rg-toc" aria-label="Sommaire du cours">
      <details class="rg-toc__box" open><summary>Sommaire</summary><ol>${rendu.titres.map((t) => `<li><a href="#${t.id}">${t.num ? `<span class="rg-toc__num">${e(t.num)}</span>` : ''}<span>${t.html}</span></a></li>`).join('')}</ol></details>
    </aside>` : ''
  return `${enTeteChapitre(ch, 'cours', null, rendu.infos)}
<div class="rg-wrap rg-reading${sommaire ? ' rg-reading--toc' : ''}">
  ${sommaire}
  <article class="rg-doc">
    <div class="rg-doc__tools">${lienAide(ch.classe, 'ressources_cours_haut')}<button type="button" class="rg-btn rg-btn--ghost rg-btn--sm" data-imprimer>${icone('imprimer')} Imprimer le cours</button></div>
    <div class="sci-doc rg-sci">${rendu.html}</div>
    <section class="rg-next" aria-label="Pour continuer">
      <p class="rg-next__title">${icone('check')} Cours lu ? Continue avec :</p>
      <div class="rg-next__grid">
        ${ch.fiche ? `<a class="rg-next__card" href="${urlFiche(ch)}">${icone('fiche')}<span><strong>La fiche de révision</strong><small>L’essentiel du chapitre, à relire avant un contrôle</small></span></a>` : ''}
        ${ch.exercices.length ? `<a class="rg-next__card" href="${urlExercices(ch)}">${icone('exercices')}<span><strong>${pluriel(ch.exercices.length, 'exercice corrigé', 'exercices corrigés')}</strong><small>Du plus simple au plus complet, corrigés pas à pas</small></span></a>` : ''}
        ${cartesFormulaires(ch)}
      </div>
    </section>
  </article>
</div>
<div class="rg-wrap">${voisins(ch)}${appelsAction(ch.classe, ch, 'ressources_cours')}</div>`
}

export function pageFiche(ch, rendu) {
  return `${enTeteChapitre(ch, 'fiche', `L’essentiel du chapitre « ${e(ch.titre)} » en une page : définitions, propriétés et méthodes à connaître en ${e(ch.classe.court)}.`)}
<div class="rg-wrap rg-reading">
  <article class="rg-doc rg-doc--fiche">
    <div class="rg-doc__tools">${lienAide(ch.classe, 'ressources_fiche_haut')}<button type="button" class="rg-btn rg-btn--ghost rg-btn--sm" data-imprimer>${icone('imprimer')} Imprimer la fiche</button></div>
    <div class="sci-doc rg-sci">${rendu.html}</div>
    <section class="rg-next" aria-label="Pour continuer">
      <p class="rg-next__title">${icone('check')} Fiche relue ? Vérifie que tu sais l’appliquer :</p>
      <div class="rg-next__grid">
        ${ch.exercices.length ? `<a class="rg-next__card" href="${urlExercices(ch)}">${icone('exercices')}<span><strong>${pluriel(ch.exercices.length, 'exercice corrigé', 'exercices corrigés')}</strong><small>Cherche, puis compare avec la correction détaillée</small></span></a>` : ''}
        <a class="rg-next__card" href="${urlCours(ch)}">${icone('cours')}<span><strong>Le cours complet</strong><small>Les explications, exemples et démonstrations</small></span></a>
        ${cartesFormulaires(ch)}
      </div>
    </section>
  </article>
</div>
<div class="rg-wrap">${voisins(ch)}${appelsAction(ch.classe, ch, 'ressources_fiche')}</div>`
}

export function pageExercices(ch, exercicesRendus) {
  const n = ch.exercices.length
  const blocs = exercicesRendus.map((x, i) => `<section class="rg-exo" id="exercice-${x.ex.id}" aria-labelledby="exo-titre-${x.ex.id}">
    <header class="rg-exo__head">
      <span class="rg-exo__num">Exercice ${i + 1}</span>
      <span class="rg-pill rg-pill--${x.ex.difficulty || 'medium'}">${DIFFICULTE[x.ex.difficulty] || 'Intermédiaire'}</span>
      ${typeExercice(x.ex) ? `<span class="rg-exo__type">${e(typeExercice(x.ex))}</span>` : ''}
    </header>
    <h2 class="rg-exo__title" id="exo-titre-${x.ex.id}">${e(titreExercice(x.ex))}</h2>
    <div class="sci-doc rg-sci rg-exo__enonce">${x.enonce}</div>
    ${x.etapes || x.solution ? `<details class="rg-correction">
      <summary><span>Voir la correction détaillée</span></summary>
      <div class="rg-correction__body">
        ${x.etapes ? `<div class="sci-doc rg-sci">${x.etapes}</div>` : ''}
        ${x.solution ? `<div class="rg-reponses"><p class="rg-reponses__title">${icone('check')} Les réponses</p><div class="sci-doc rg-sci">${x.solution}</div></div>` : ''}
      </div>
    </details>` : ''}
  </section>`).join('\n')
  // Après les exercices gratuits, le moment où l'élève sait s'il a besoin de
  // plus : d'autres exercices (abonnement) ou l'aide d'un prof (collège et plus).
  const autres = ch.totalExercices > n ? `<div class="rg-more__ligne">
      <p><strong>${ch.totalExercices - n} autres exercices corrigés</strong> t’attendent sur ce chapitre dans la plateforme OptiTAB, avec le suivi de tes réussites.</p>
      <a class="rg-btn rg-btn--primary rg-btn--sm" href="/tarifs" data-cta-name="pricing" data-cta-location="ressources_exercices">Voir les formules</a>
    </div>` : ''
  const aide = avecProf(ch.classe) ? `<div class="rg-more__ligne">
      <p><strong>Tu bloques sur un exercice\u00a0?</strong> Un prof de maths le reprend avec toi, pas à pas, en cours particulier en ligne.</p>
      <a class="rg-btn rg-btn--green rg-btn--sm" href="/cours-particuliers" data-cta-name="tutoring" data-cta-location="ressources_exercices_aide">Réserver un cours</a>
    </div>` : ''
  const reste = autres || aide ? `<aside class="rg-more" aria-label="Aller plus loin">
    ${[autres, aide].filter(Boolean).join('\n    ')}
  </aside>` : ''
  return `${enTeteChapitre(ch, 'exercices', `${pluriel(n, 'exercice corrigé', 'exercices corrigés')} sur « ${e(ch.titre)} » (${e(ch.classe.court)}), du plus simple au plus complet. Cherche d’abord sur ton brouillon, puis ouvre la correction détaillée.`)}
<div class="rg-wrap rg-reading">
  <div class="rg-exos">
    <div class="rg-doc__tools"><button type="button" class="rg-btn rg-btn--ghost rg-btn--sm" data-imprimer>${icone('imprimer')} Imprimer les exercices et leurs corrigés</button></div>
    ${blocs}
    ${reste}
    <section class="rg-next" aria-label="Pour continuer">
      <p class="rg-next__title">${icone('check')} Besoin de revoir une notion ?</p>
      <div class="rg-next__grid">
        <a class="rg-next__card" href="${urlCours(ch)}">${icone('cours')}<span><strong>Le cours complet</strong><small>Explications, exemples et méthodes</small></span></a>
        ${ch.fiche ? `<a class="rg-next__card" href="${urlFiche(ch)}">${icone('fiche')}<span><strong>La fiche de révision</strong><small>L’essentiel à retenir</small></span></a>` : ''}
      </div>
    </section>
  </div>
</div>
<div class="rg-wrap">${voisins(ch)}${appelsAction(ch.classe, ch, 'ressources_exercices')}</div>`
}

// Articles du blog proposés sur la page de chaque classe.
const BLOG_PAR_CLASSE = {
  cp: ['comment-aider-son-enfant-en-maths', 'astuces-calcul-mental'],
  ce1: ['comment-aider-son-enfant-en-maths', 'astuces-calcul-mental'],
  ce2: ['apprendre-les-tables-de-multiplication', 'astuces-calcul-mental'],
  cm1: ['apprendre-les-tables-de-multiplication', 'comment-aider-son-enfant-en-maths'],
  cm2: ['apprendre-les-tables-de-multiplication', 'reviser-un-controle-de-maths'],
  '6e': ['reviser-un-controle-de-maths', 'comment-progresser-en-maths'],
  '5e': ['reviser-un-controle-de-maths', 'comment-progresser-en-maths'],
  '4e': ['reviser-un-controle-de-maths', 'calculatrice-college-lycee'],
  '3e': ['reviser-le-brevet-de-maths', 'calculatrice-college-lycee'],
  seconde: ['comment-progresser-en-maths', 'calculatrice-college-lycee'],
  premiere: ['specialite-maths-premiere-terminale', 'epreuve-anticipee-de-maths-premiere'],
  terminale: ['specialite-maths-premiere-terminale', 'reviser-les-maths-pendant-les-vacances']
}

// Outils et rubriques gratuites utiles à chaque classe : liens depuis les pages
// de classe, parmi les plus fortes du site, vers les pages d'outils (maillage interne).
const OUTIL = {
  maternelle: ['maternelle/', 'cours', 'Avant le CP : la maternelle', 'Compter, les formes, se repérer : pour revoir les bases'],
  operations: ['operations/', 'operation', 'Poser les opérations', 'Addition, soustraction, multiplication et division posées'],
  fiches: ['fiches-a-imprimer/', 'imprimer', 'Fiches à imprimer', 'Des opérations à poser, avec leurs corrigés'],
  heure: ['methodes/lire-l-heure/', 'calcul', 'Lire l’heure', 'Une horloge interactive pour s’entraîner'],
  multiplication: ['tables/table-de-multiplication/', 'table', 'Table de multiplication', 'De 1 à 20, avec des astuces pour la retenir'],
  conversion: ['tables/tableau-de-conversion/', 'table', 'Tableau de conversion', 'Longueurs, masses, contenances, aires et volumes'],
  methodes: ['methodes/', 'calcul', 'Méthodes de calcul', 'Pourcentages, fractions, moyennes, durées, avec calculateurs'],
  formulaires: ['formulaires/', 'formule', 'Formulaires de maths', 'Toutes les formules expliquées, avec des exemples'],
  convertisseur: ['methodes/convertisseur-d-unites/', 'calcul', 'Convertisseur d’unités', 'Longueurs, masses, vitesses, pressions, températures'],
  brevet: ['methodes/simulateur-brevet/', 'calcul', 'Simulateur du brevet', 'Calculer sa note et sa mention au brevet'],
  physiqueBrevet: ['physique-chimie/formules-physique-chimie-brevet/', 'physique', 'Physique-chimie du brevet', 'Toutes les formules de 3e, avec exemples'],
  physique: ['physique-chimie/', 'physique', 'Physique-chimie', 'Formules, tableau périodique et unités, du collège à la prépa'],
  mecanique: ['physique-chimie/formules-de-mecanique/', 'physique', 'Formules de mécanique', 'Vitesse, forces, lois de Newton, chute libre'],
  periodique: ['physique-chimie/tableau-periodique/', 'physique', 'Tableau périodique', 'Interactif et à imprimer'],
  tables: ['tables/', 'table', 'Tables de maths', 'Carrés, puissances de 10, fractions, trigonométrie']
}
const OUTILS_PAR_CLASSE = {
  cp: ['maternelle', 'heure', 'operations'],
  ce1: ['operations', 'multiplication', 'heure', 'fiches'],
  ce2: ['operations', 'multiplication', 'heure', 'fiches'],
  cm1: ['operations', 'multiplication', 'methodes', 'fiches'],
  cm2: ['operations', 'multiplication', 'conversion', 'methodes'],
  '6e': ['formulaires', 'methodes', 'conversion', 'operations'],
  '5e': ['formulaires', 'methodes', 'tables', 'convertisseur'],
  '4e': ['formulaires', 'methodes', 'tables', 'physiqueBrevet'],
  '3e': ['brevet', 'formulaires', 'physiqueBrevet', 'methodes'],
  seconde: ['formulaires', 'mecanique', 'periodique', 'convertisseur'],
  premiere: ['formulaires', 'mecanique', 'periodique', 'tables'],
  terminale: ['formulaires', 'mecanique', 'physique', 'tables']
}

function outilsClasse(classe) {
  const liste = (OUTILS_PAR_CLASSE[classe.slug] || []).map((k) => OUTIL[k])
  if (!liste.length) return ''
  return `<section class="rg-next rg-outils" aria-labelledby="outils-${classe.slug}">
    <p class="rg-next__title" id="outils-${classe.slug}">${icone('check')} Outils et fiches gratuits utiles en ${e(classe.court)}</p>
    <div class="rg-next__grid">${liste.map(([chemin, ico, titre, texte]) => `<a class="rg-next__card" href="${RACINE}${chemin}">${icone(ico)}<span><strong>${e(titre)}</strong><small>${e(texte)}</small></span></a>`).join('')}</div>
  </section>`
}

function conseilsBlog(classe, articles) {
  const liste = (BLOG_PAR_CLASSE[classe.slug] || []).map((s) => articles.find((a) => a.slug === s)).filter(Boolean)
  if (!liste.length) return ''
  return `<section class="rg-next rg-conseils" aria-labelledby="conseils-${classe.slug}">
    <p class="rg-next__title" id="conseils-${classe.slug}">${icone('check')} Conseils pour réussir en maths ${e(classe.court)}</p>
    <div class="rg-next__grid">${liste.map((a) => `<a class="rg-next__card" href="/blog/${a.slug}/">${icone('cours')}<span><strong>${e(a.titre)}</strong><small>${e(a.description)}</small></span></a>`).join('')}</div>
  </section>`
}

export function pageClasse(classe, catalogue, articles = []) {
  const nb = classe.chapitres.length
  const nbExos = classe.chapitres.reduce((s, ch) => s + ch.exercices.length, 0)
  const themes = classe.themes.map((t) => `<section class="rg-theme" aria-labelledby="theme-${t.id}">
    <h2 class="rg-theme__title" id="theme-${t.id}">${e(t.titre)}</h2>
    <ul class="rg-chapters">${t.chapitres.map((ch) => `<li class="rg-chapter">
      <a class="rg-chapter__main" href="${urlCours(ch)}"><span class="rg-chapter__num">${ch.numero}</span><span class="rg-chapter__title">${e(ch.titre)}</span></a>
      <span class="rg-chapter__links">
        <a href="${urlCours(ch)}" title="Cours : ${e(ch.titre)}">${icone('cours')}<span>Cours</span></a>
        ${ch.fiche ? `<a href="${urlFiche(ch)}" title="Fiche de révision : ${e(ch.titre)}">${icone('fiche')}<span>Fiche</span></a>` : ''}
        ${ch.exercices.length ? `<a href="${urlExercices(ch)}" title="Exercices corrigés : ${e(ch.titre)}">${icone('exercices')}<span>${ch.exercices.length} exercices</span></a>` : ''}
      </span>
    </li>`).join('')}</ul>
  </section>`).join('\n')
  const memeCycle = catalogue.classes.filter((c) => c.cycle === classe.cycle)
  return `<header class="rg-chap rg-chap--classe">
  <div class="rg-wrap">
    ${filAriane(etapesAriane(classe))}
    <p class="rg-kicker">Ressources gratuites · ${e(CYCLES.find((c) => c.cle === classe.cycle).titre)}</p>
    <h1 class="rg-h1">Maths ${e(classe.court)} : cours, fiches et exercices corrigés</h1>
    <p class="rg-lead">${e(classe.intro)}</p>
    <ul class="rg-stats">
      <li><strong>${nb}</strong> chapitres</li>
      <li><strong>${nb}</strong> cours complets</li>
      <li><strong>${nb}</strong> fiches de révision</li>
      <li><strong>${nbExos}</strong> exercices corrigés</li>
    </ul>
    <nav class="rg-pills" aria-label="Autres classes">${memeCycle.map((c) => `<a href="${urlClasse(c)}"${c.slug === classe.slug ? ' aria-current="page" class="is-active"' : ''}>${e(c.court)}</a>`).join('')}</nav>
  </div>
</header>
<div class="rg-wrap rg-classe">
  ${themes}
  ${outilsClasse(classe)}
  ${conseilsBlog(classe, articles)}
  ${appelsAction(classe, null, 'ressources_classe')}
</div>`
}

// Accueil des ressources : une seule question par bloc, dans l'ordre où le
// visiteur se la pose. Chercher une notion (en-tête), choisir sa classe,
// aller droit aux pages les plus demandées, ou ouvrir une rubrique d'outils.
// blocs = donneesAccueil() de formulaires.mjs : { acces, rubriques, maternelle }.
export function pageAccueil(catalogue, faq, blocs) {
  const t = catalogue.totaux
  const ligne = (id, titre, liens) => `<div class="rg-choix__ligne">
      <h3 class="rg-choix__cycle" id="choix-${id}">${e(titre)}</h3>
      <ul class="rg-choix__classes" aria-labelledby="choix-${id}">${liens.map((l) => `<li><a href="${l.url}"><strong>${e(l.titre)}</strong><span>${e(l.meta)}</span></a></li>`).join('')}</ul>
    </div>`
  const { maternelle } = blocs
  const lignes = [
    maternelle.sections.length ? ligne('maternelle', 'Maternelle', maternelle.sections) : '',
    ...CYCLES.map((cy) => {
      const classes = catalogue.classes.filter((c) => c.cycle === cy.cle)
      return classes.length ? ligne(cy.cle, cy.titre, classes.map((c) => ({
        titre: `Maths ${c.court}`, meta: pluriel(c.chapitres.length, 'chapitre', 'chapitres'), url: urlClasse(c)
      }))) : ''
    })
  ].filter(Boolean).join('\n    ')
  return `<header class="rg-hero">
  <div class="rg-wrap rg-hero__inner">
    ${filAriane([['Accueil', '/'], ['Ressources gratuites', RACINE]])}
    <h1 class="rg-h1 rg-h1--hero">Cours de maths gratuits, du CP à la Terminale</h1>
    <p class="rg-lead">Des cours complets et illustrés, des fiches de révision et des exercices corrigés pas à pas, conformes au programme de l’Éducation nationale. Choisis ta classe ou cherche une notion.</p>
    ${RECHERCHE}
    <ul class="rg-garanties">
      <li>${icone('check')}<span><strong>${t.cours}</strong> cours et <strong>${t.fiches}</strong> fiches</span></li>
      <li>${icone('check')}<span><strong>${t.exercicesGratuits}</strong> exercices corrigés</span></li>
      <li>${icone('check')}<span>Sans inscription</span></li>
    </ul>
  </div>
</header>
<div class="rg-wrap rg-home">
  <section class="rg-bloc" aria-labelledby="choix-titre">
    <h2 class="rg-bloc__titre" id="choix-titre">Choisis ta classe</h2>
    <div class="rg-choix">
    ${lignes}
    </div>
  </section>
  <section class="rg-bloc" aria-labelledby="acces-titre">
    <h2 class="rg-bloc__titre" id="acces-titre">Accès rapide</h2>
    <ul class="rg-acces">${blocs.acces.map((a) => `<li><a href="${a.url}">${e(a.titre)}</a></li>`).join('')}</ul>
  </section>
  <section class="rg-bloc" aria-labelledby="outils-titre">
    <h2 class="rg-bloc__titre" id="outils-titre">Formulaires, tables et outils</h2>
    <ul class="rg-rubs">${blocs.rubriques.map((r) => `<li><a class="rg-rub rg-rub--${r.cle}" href="${r.url}">
      <span class="rg-rub__ico">${icone(r.icone)}</span>
      <span class="rg-rub__corps"><h3 class="rg-rub__titre">${e(r.titre)}</h3><span class="rg-rub__texte">${e(r.texte)}</span><span class="rg-rub__compte">${e(r.compte)} ${icone('fleche')}</span></span>
    </a></li>`).join('')}</ul>
  </section>
  ${appelsAction(null, null, 'ressources_accueil')}
  <section class="rg-faq" aria-labelledby="faq-title">
    <h2 id="faq-title">Questions fréquentes</h2>
    ${faq.map(([q, r]) => `<details class="rg-faq__item"><summary>${e(insecables(q))}</summary><p>${insecables(r)}</p></details>`).join('\n    ')}
  </section>
</div>`
}

// Espace insécable avant « ? ! : ; » (pas de ponctuation seule en début de ligne).
const insecables = (texte) => String(texte).replace(/ ([?!:;])/g, '\u00a0$1')

export function pageRedirection(cible, nom = 'Ressources gratuites') {
  const url = absolu(cible)
  return `<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><title>${nom} | OptiTAB</title>
<meta name="robots" content="noindex,follow"><link rel="canonical" href="${url}">
<meta http-equiv="refresh" content="0; url=${cible}"><script>location.replace(${JSON.stringify(cible)})</script></head>
<body><p><a href="${cible}">${nom} OptiTAB</a></p></body></html>
`
}

export { CLASSES }
