// Relevé des pages de la vitrine pour les livrer en HTML complet (lisible sans
// JavaScript par Google, Bing, les assistants d'IA et les réseaux sociaux).
//
//   1. lancer le site en local (npm run dev → http://localhost:3000)
//   2. node scripts/vitrine/instantanes.mjs [http://localhost:3000]
//
// Pour chaque page de src/config/pagesStatiques.js, ouvre la vraie page comme
// un visiteur non connecté, relève le titre, les balises de référencement et
// de partage, les données structurées, puis le texte de la page réduit à des
// balises sémantiques (titres, paragraphes, listes, liens, tableaux).
// Écrit contenu/vitrine/<nom>.json, utilisé à la construction par prerendu.mjs.
// À relancer après toute modification d'une de ces pages.
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { chromium } from 'playwright'
import { PAGES_STATIQUES } from '../../src/config/pagesStatiques.js'

const ICI = path.dirname(fileURLToPath(import.meta.url))
const SORTIE = path.resolve(ICI, '..', '..', 'contenu', 'vitrine')
const BASE = (process.argv[2] || 'http://localhost:3000').replace(/\/$/, '')
fs.mkdirSync(SORTIE, { recursive: true })

// Exécuté dans la page : métadonnées + contenu nettoyé.
function releve() {
  const GARDER = new Set(['HEADER', 'NAV', 'MAIN', 'SECTION', 'ARTICLE', 'ASIDE', 'FOOTER', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6',
    'P', 'UL', 'OL', 'LI', 'A', 'STRONG', 'EM', 'B', 'I', 'TABLE', 'THEAD', 'TBODY', 'TR', 'TH', 'TD', 'DETAILS', 'SUMMARY',
    'FIGURE', 'FIGCAPTION', 'BLOCKQUOTE', 'DL', 'DT', 'DD', 'BR'])
  const BLOC = new Set(['DIV', 'SPAN', 'LABEL', 'BUTTON', 'SMALL', 'TIME', 'MARK', 'SUP', 'SUB', 'U', 'S', 'ABBR', 'CITE', 'Q'])
  const SUPPRIMER = 'script,style,svg,noscript,iframe,canvas,video,audio,img,picture,source,input,select,textarea,form,[role="dialog"],[aria-modal="true"],[hidden],template'

  // Éléments masqués à l'écran (menus mobiles, fenêtres…), sauf le contenu
  // replié des questions fréquentes, qui reste du vrai contenu.
  for (const el of document.querySelectorAll('#app *')) {
    const s = getComputedStyle(el)
    if ((s.display === 'none' || s.visibility === 'hidden') && !el.closest('details, [class*="faq" i], [class*="Faq"]')) el.setAttribute('data-pr-masque', '')
    if (el.getAttribute('aria-hidden') === 'true') el.setAttribute('data-pr-masque', '')
    // Élément affiché sur sa propre ligne : une espace avant et après, pour que
    // les mots de deux lignes voisines ne se collent pas une fois aplatis.
    if (!/^(inline|contents)$/.test(s.display)) el.setAttribute('data-pr-bloc', '')
  }
  const app = document.querySelector('#app').cloneNode(true)
  for (const el of app.querySelectorAll(`${SUPPRIMER},[data-pr-masque]`)) el.remove()
  for (const el of app.querySelectorAll('[class*="cookie" i]')) el.remove()

  // Balises non sémantiques : on garde leur contenu, pas la balise.
  const aplatir = (noeud) => {
    for (const enfant of [...noeud.children]) {
      aplatir(enfant)
      const bloc = enfant.hasAttribute('data-pr-bloc')
      if (GARDER.has(enfant.tagName)) {
        if (bloc && /^(A|STRONG|EM|B|I)$/.test(enfant.tagName)) {
          enfant.before(document.createTextNode(' '))
          enfant.after(document.createTextNode(' '))
        }
        for (const att of [...enfant.attributes]) if (!(enfant.tagName === 'A' && att.name === 'href')) enfant.removeAttribute(att.name)
        if (enfant.tagName === 'A') {
          const href = enfant.getAttribute('href') || ''
          if (!href || href.startsWith('javascript:') || href === '#') enfant.removeAttribute('href')
          else if (href.startsWith(location.origin)) enfant.setAttribute('href', href.slice(location.origin.length) || '/')
        }
      } else {
        // Un bloc devient une espace pour ne pas coller deux mots.
        const espace = bloc || (BLOC.has(enfant.tagName) && enfant.tagName !== 'SPAN') ? ' ' : ''
        enfant.replaceWith(document.createTextNode(espace), ...enfant.childNodes, document.createTextNode(espace))
      }
    }
  }
  aplatir(app)

  // Éléments vides (après nettoyage).
  let change = true
  while (change) {
    change = false
    for (const el of app.querySelectorAll('*')) {
      if (el.tagName !== 'BR' && !el.textContent.trim()) { el.remove(); change = true }
    }
  }

  const html = app.innerHTML
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/\s+/g, ' ')
    .replace(/>\s+</g, '><')
    .replace(/\s+(<\/(?:p|li|h[1-6]|td|th|a|strong|em|dt|dd|summary|figcaption)>)/g, '$1')
    .trim()

  const metas = [...document.head.querySelectorAll('meta[name], meta[property]')]
    .map((m) => ({ attr: m.hasAttribute('name') ? 'name' : 'property', cle: m.getAttribute('name') || m.getAttribute('property'), valeur: m.getAttribute('content') || '' }))
    .filter((m) => /^(description|robots|keywords|og:|twitter:)/.test(m.cle))
  return {
    titre: document.title,
    metas,
    canonique: document.querySelector('link[rel="canonical"]')?.getAttribute('href') || '',
    jsonld: [...document.querySelectorAll('script[type="application/ld+json"]')].map((s) => s.textContent.trim()).filter(Boolean),
    h1: app.querySelectorAll('h1').length,
    mots: app.textContent.trim().split(/\s+/).length,
    html
  }
}

const navigateur = await chromium.launch({ channel: 'chrome' })
const contexte = await navigateur.newContext({ viewport: { width: 1440, height: 900 } })
// Visiteur qui a refusé les cookies : aucune mesure d'audience pendant le relevé.
await contexte.addInitScript(() => {
  try { localStorage.setItem('optitab_cookie_consent_v1', JSON.stringify({ analytics: 'denied', marketing: 'denied', expiresAt: Date.now() + 1e9 })) } catch (e) {}
})
const onglet = await contexte.newPage()
let erreurs = 0
for (const page of PAGES_STATIQUES) {
  await onglet.goto(`${BASE}${page.chemin}`, { waitUntil: 'networkidle' })
  await onglet.waitForTimeout(1200)
  const r = await onglet.evaluate(releve)
  const pb = []
  if (r.h1 !== 1) pb.push(`${r.h1} titre(s) h1`)
  if (r.mots < 150) pb.push(`seulement ${r.mots} mots`)
  if (!r.canonique) pb.push('pas d’adresse canonique')
  if (!r.metas.some((m) => m.cle === 'description' && m.valeur)) pb.push('pas de description')
  if (pb.length) { erreurs++; console.log(`✗ ${page.chemin} : ${pb.join(', ')}`); continue }
  const donnees = { chemin: page.chemin, releve: new Date().toISOString().slice(0, 10), ...r }
  fs.writeFileSync(path.join(SORTIE, `${page.nom}.json`), `${JSON.stringify(donnees, null, 2)}\n`)
  console.log(`✓ ${page.chemin.padEnd(26)} ${String(r.mots).padStart(5)} mots, ${r.jsonld.length} bloc(s) de données structurées → contenu/vitrine/${page.nom}.json`)
}
await navigateur.close()
if (erreurs) process.exit(1)
