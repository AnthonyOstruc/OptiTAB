// Construction (après scripts/ressources/generer.mjs) : livre les pages de la
// vitrine en HTML complet, lisible sans JavaScript.
//
// Pour chaque page de src/config/pagesStatiques.js, à partir du relevé
// contenu/vitrine/<nom>.json (scripts/vitrine/instantanes.mjs) :
// - balises de référencement et de partage, adresse canonique et données
//   structurées de la vraie page, dans le <head> ;
// - texte de la page dans <div id="app">, masqué dès que JavaScript tourne
//   (l'application affiche alors la page elle-même, à l'identique) ;
// - l'accueil va dans dist/index.html, les autres pages dans
//   dist/<page>/index.html (adresse officielle avec « / » final).
// Puis : plan du site des pages de la vitrine (sitemap.xml) et liens internes
// vers ces pages réécrits avec le « / » final dans les pages statiques.
//
// Un relevé manquant n'arrête pas la mise en ligne : la page garde alors
// l'ancienne coquille (message d'avertissement dans le journal).
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PAGES_STATIQUES, cheminCanonique } from '../../src/config/pagesStatiques.js'

const ICI = path.dirname(fileURLToPath(import.meta.url))
const FRONT = path.resolve(ICI, '..', '..')
const DIST = path.join(FRONT, process.argv[2] || 'dist')
const RELEVES = path.join(FRONT, 'contenu', 'vitrine')
const SITE = 'https://www.optitab.net'
const journal = (m) => console.log(`[vitrine] ${m}`)

const echapper = (t) => String(t).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
const AVEC_BARRE = PAGES_STATIQUES.map((p) => p.chemin).filter((c) => c !== '/')

// Liens internes : « /tarifs » → « /tarifs/ » (et les rubriques statiques).
function liensAvecBarre(texte) {
  let s = texte
  for (const c of [...AVEC_BARRE, '/ressources-gratuites', '/blog']) {
    const e = c.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    s = s.replace(new RegExp(`(href=")${e}(["#?])`, 'g'), (m, a, b) => `${a}${c}/${b === '"' ? '"' : b}`)
    s = s.replace(new RegExp(`(https://www\\.optitab\\.net)${e}(?=[\\s"'<)\\],]|$)`, 'gm'), `$1${c}/`)
  }
  return s
}

// Balises du <head> gérées par le relevé : retirées de la page de base.
function sansBalisesSeo(head) {
  return head
    .replace(/\s*<title>[\s\S]*?<\/title>/i, '')
    .replace(/\s*<meta\s+(?:name|property)="(?:description|robots|keywords|og:[^"]*|twitter:[^"]*)"[^>]*>/gi, '')
    .replace(/\s*<link\s+rel="canonical"[^>]*>/gi, '')
    .replace(/\s*<script type="application\/ld\+json"[^>]*>[\s\S]*?<\/script>/gi, '')
}

function page(base, r) {
  const [avant, apres] = base.split('</head>')
  const balises = [
    `<title>${echapper(r.titre)}</title>`,
    ...r.metas.map((m) => `<meta ${m.attr}="${echapper(m.cle)}" content="${echapper(m.valeur)}" />`),
    `<link rel="canonical" href="${echapper(r.canonique)}" />`,
    // Même identifiant que celui de l'application (services/seo.js) : elle met
    // ce bloc à jour au lieu d'en ajouter un second (pas de données en double).
    ...r.jsonld.map((j, i) => `<script type="application/ld+json"${i === 0 ? ' id="seo-jsonld"' : ''}>${j.replace(/<\//g, '<\\/')}</script>`),
    // Contenu lisible sans JavaScript ; masqué dès que JavaScript tourne.
    '<script>document.documentElement.classList.add(\'js\')</script>',
    '<style>.js [data-prerendu]{display:none!important}[data-prerendu]{max-width:1100px;margin:0 auto;padding:24px;font-family:system-ui,sans-serif;line-height:1.6}</style>'
  ]
  const corps = apres.replace('<div id="app"></div>', `<div id="app"><div data-prerendu>${liensAvecBarre(r.html)}</div></div>`)
  if (corps === apres) throw new Error('<div id="app"></div> introuvable dans dist/index.html')
  return `${sansBalisesSeo(avant)}\n    ${balises.join('\n    ')}\n  </head>${corps}`
}

const fichierBase = path.join(DIST, 'index.html')
if (!fs.existsSync(fichierBase)) throw new Error(`${fichierBase} introuvable : lancer la construction d'abord`)
// Rejouable : si dist/index.html a déjà été traité, on repart de la coquille.
const base = fs.readFileSync(fichierBase, 'utf8')
  .replace(/<div id="app"><div data-prerendu>[\s\S]*?<\/div><\/div>/, '<div id="app"></div>')
  .replace(/\s*<script>document\.documentElement\.classList\.add\('js'\)<\/script>/, '')
  .replace(/\s*<style>\.js \[data-prerendu\][^<]*<\/style>/, '')
const ecrites = []
for (const p of PAGES_STATIQUES) {
  const releve = path.join(RELEVES, `${p.nom}.json`)
  if (!fs.existsSync(releve)) { journal(`⚠ relevé manquant pour ${p.chemin} (contenu/vitrine/${p.nom}.json) : page laissée telle quelle`); continue }
  const r = JSON.parse(fs.readFileSync(releve, 'utf8'))
  const cible = p.chemin === '/' ? fichierBase : path.join(DIST, p.chemin.slice(1), 'index.html')
  fs.mkdirSync(path.dirname(cible), { recursive: true })
  fs.writeFileSync(cible, page(base, r))
  ecrites.push({ ...p, releve: r.releve })
}

// Plan du site des pages de la vitrine (les ressources et le blog ont le leur).
const sitemap = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  ...ecrites.map((p) => `  <url>\n    <loc>${SITE}${cheminCanonique(p.chemin)}</loc>\n    <lastmod>${p.releve}</lastmod>\n  </url>`),
  '</urlset>',
  ''
].join('\n')
fs.writeFileSync(path.join(DIST, 'sitemap.xml'), sitemap)

// Liens vers ces pages dans les pages statiques (ressources, blog), llms.txt…
let modifies = 0
const parcourir = (dossier) => {
  for (const e of fs.readdirSync(dossier, { withFileTypes: true })) {
    const f = path.join(dossier, e.name)
    if (e.isDirectory()) { if (e.name !== 'assets') parcourir(f); continue }
    if (!/\.(html|md|txt|xml)$/.test(e.name) || e.name === 'sitemap.xml') continue
    const avant = fs.readFileSync(f, 'utf8')
    const apres = liensAvecBarre(avant)
    if (apres !== avant) { fs.writeFileSync(f, apres); modifies++ }
  }
}
parcourir(DIST)

journal(`${ecrites.length}/${PAGES_STATIQUES.length} pages livrées en HTML complet (${ecrites.map((p) => cheminCanonique(p.chemin)).join(', ')}), relevés du ${[...new Set(ecrites.map((p) => p.releve))].join(', ')} ; liens réécrits dans ${modifies} fichier(s)`)
