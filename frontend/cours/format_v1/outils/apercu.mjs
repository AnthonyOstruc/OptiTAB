// Génère une page d'aperçu autonome d'un chapitre au format OptiTAB v1.
//
// Usage :
//   node apercu.mjs <dossier_chapitre> <images.json> <dossier_images> <sortie.html> "<titre>" "<sous-titre>"
//
// La page embarque le vrai moteur (src/utils/optitabDoc.js), le réglage des
// formules (tuneMathOverflow de src/utils/scientificRenderer.js) et les
// vraies feuilles de style du site : ce que l'on voit est ce que verront les
// élèves. Les images sont intégrées en data URI.
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const here = path.dirname(fileURLToPath(import.meta.url))
const front = path.resolve(here, '../../..')
const args = process.argv.slice(2)
const ARTIFACT = args.includes('--artifact')
const [dir, imagesJson, imagesDir, out, titre = 'Chapitre', sousTitre = ''] = args.filter((a) => a !== '--artifact')
if (!out) {
  console.error('Usage : node apercu.mjs <dossier_chapitre> <images.json> <dossier_images> <sortie.html> "<titre>" "<sous-titre>"')
  process.exit(1)
}

const read = (p) => fs.readFileSync(p, 'utf8')

// --- moteur et styles du site -------------------------------------------
const engine = read(path.join(front, 'src/utils/optitabDoc.js')).replace(/^export /gm, '')
const sci = read(path.join(front, 'src/utils/scientificRenderer.js'))
const tuneStart = sci.indexOf('export function tuneMathOverflow')
const tuneEnd = sci.indexOf('\n}\n', tuneStart) + 3
const tune = sci.slice(tuneStart, tuneEnd).replace(/^export /, '')
const css = read(path.join(front, 'src/styles/scientific-content.css')) + '\n' + read(path.join(front, 'src/styles/optitab-doc.css'))

// --- contenu -------------------------------------------------------------
const stripHeader = (txt) => txt.slice(txt.indexOf('<!-- optitab:1 -->'))
const cours = stripHeader(read(path.join(dir, 'cours.txt')))
const fiche = stripHeader(read(path.join(dir, 'fiche.txt')))

function parseExercises(raw) {
  return raw
    .split(/^===[ \t]*$/m)
    .map((b) => b.trim())
    .filter(Boolean)
    .map((b) => {
      const titre = b.split('\n')[0].replace(/^===\s*/, '').trim()
      const diff = (b.match(/^Difficulté:\s*(\w+)/m) || [])[1] || 'medium'
      const field = (name, next) => {
        const s = b.indexOf(`${name}:`)
        const e = next ? b.indexOf(`${next}:`, s) : b.length
        return b.slice(s + name.length + 1, e).trim()
      }
      return {
        titre,
        difficulte: diff,
        enonce: field('Énoncé', 'Étapes'),
        etapes: field('Étapes', 'Solution'),
        solution: field('Solution', null)
      }
    })
}
const exercices = parseExercises(read(path.join(dir, 'exercices.txt')))

// --- images --------------------------------------------------------------
const db = JSON.parse(read(imagesJson))
const dataUri = (url) => {
  const name = url.split('/').pop().split('?')[0]
  const file = path.join(imagesDir, name)
  if (!fs.existsSync(file)) return ''
  const ext = path.extname(name).slice(1).toLowerCase()
  const mime = ext === 'jpg' || ext === 'jpeg' ? 'image/jpeg' : ext === 'svg' ? 'image/svg+xml' : 'image/png'
  return `data:${mime};base64,${fs.readFileSync(file).toString('base64')}`
}
// Dimensions d'affichage : moitié de la taille en pixels (figures en double résolution)
const pngSize = (url) => {
  const name = url.split('/').pop().split('?')[0]
  const file = path.join(imagesDir, name)
  if (!fs.existsSync(file) || !name.toLowerCase().endsWith('.png')) return null
  const b = fs.readFileSync(file)
  return { w: Math.round(b.readUInt32BE(16) / 2), h: Math.round(b.readUInt32BE(20) / 2) }
}
const imageMap = (list) =>
  Object.fromEntries((list || []).map(([pos, url]) => [pos, { src: dataUri(url), size: pngSize(url) }]))
const images = {
  cours: imageMap(db.cours_images),
  fiche: imageMap(db.fiche_images),
  exercices: Object.fromEntries(Object.entries(db.exercices || {}).map(([t, l]) => [t, imageMap(l)]))
}

const payload = { titre, sousTitre, cours, fiche, exercices, images }
const json = JSON.stringify(payload).replace(/</g, '\\u003c')

const html = `<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pilote trigonométrie Terminale</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700&display=swap">
<script>
window.MathJax = {
  loader: { load: ['[tex]/mhchem'] },
  tex: {
    packages: { '[+]': ['mhchem'] },
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
  },
  svg: { fontCache: 'none', scale: 1, minScale: 0.5, mtextInheritFont: true },
  options: { enableMenu: false },
  startup: { typeset: false }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js"></script>
<style>
:root {
  --page: #f4f6fb;
  --card: #ffffff;
  --line: #e3e9f4;
  --ink: #1c2130;
  --muted: #6b7385;
  --navy: #1b3c8e;
  color-scheme: light;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: var(--page); }
body { font-family: 'Segoe UI', system-ui, -apple-system, Roboto, sans-serif; color: var(--ink); -webkit-font-smoothing: antialiased; }
.ap-top { background: #fff; border-bottom: 1px solid var(--line); position: sticky; top: env(safe-area-inset-top, 0px); z-index: 10; }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: #fff; }
.ap-top-in { max-width: 1120px; margin: 0 auto; padding-block: 14px 0; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.ap-kicker { font: 700 11px/1.4 Montserrat, sans-serif; letter-spacing: .12em; text-transform: uppercase; color: #3b8544; }
.ap-title { font: 600 clamp(20px, 4.5vw, 26px)/1.25 Montserrat, sans-serif; margin: 4px 0 2px; }
.ap-sub { color: var(--muted); font-size: 14px; }
.ap-tabs { display: flex; gap: 4px; margin-top: 12px; overflow-x: auto; }
.ap-tab { appearance: none; border: 0; background: none; font: 600 14px/1 Montserrat, sans-serif; color: var(--muted); padding: 12px 14px 13px; border-bottom: 3px solid transparent; cursor: pointer; white-space: nowrap; }
.ap-tab[aria-selected="true"] { color: var(--navy); border-bottom-color: var(--navy); }
.ap-main { max-width: 1120px; margin: 0 auto; padding-block: 20px 64px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.ap-panel[hidden] { display: none; }
.ap-card { background: var(--card); border: 1px solid var(--line); border-radius: 18px; box-shadow: 0 10px 30px rgba(15,23,42,.05); padding: 28px 32px 34px; }
.ex-list { display: flex; flex-direction: column; gap: 22px; }
.ex-card { background: var(--card); border: 1px solid var(--line); border-radius: 18px; box-shadow: 0 10px 30px rgba(15,23,42,.05); overflow: hidden; }
.ex-head { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; padding: 16px 22px 12px; }
.ex-level { font: 700 10.5px/1 Montserrat, sans-serif; letter-spacing: .1em; text-transform: uppercase; padding: 6px 9px; border-radius: 999px; }
.ex-level--easy { background: #eaf4ea; color: #3b8544; }
.ex-level--medium { background: #f1f3f8; color: #1b3c8e; }
.ex-level--hard { background: #fef6eb; color: #a86a1c; }
.ex-stars { margin-left: auto; color: #f0a23b; letter-spacing: 2px; font-size: 14px; }
.ex-title { flex: 1 1 100%; order: 3; font: 600 17px/1.4 Montserrat, sans-serif; text-wrap: balance; }
.ex-tabs { display: flex; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); background: #fafbfd; }
.ex-tab { flex: 1; appearance: none; border: 0; background: none; padding: 13px 8px; font: 600 13.5px/1 Montserrat, sans-serif; color: var(--muted); border-bottom: 3px solid transparent; cursor: pointer; }
.ex-tab[aria-selected="true"] { color: var(--navy); border-bottom-color: var(--navy); background: #fff; }
.ex-panel { padding: 22px 24px 26px; }
.ex-panel[hidden] { display: none; }
figure.course-figure { margin: 1.2em 0; text-align: center; }
figure.course-figure img { max-width: 100%; height: auto; border-radius: 10px; }
@media (max-width: 640px) {
  .ap-main { padding-block: 14px 48px; }
  .ap-card { padding: 18px 14px 22px; border-radius: 14px; }
  .ex-head { padding: 14px 16px 10px; }
  .ex-panel { padding: 18px 14px 22px; }
  .ex-title { font-size: 15.5px; }
}
${css}
</style>
</head>
<body>
<header class="ap-top"><div class="ap-top-in">
  <div class="ap-kicker">Aperçu · nouveau format</div>
  <h1 class="ap-title" id="ap-title"></h1>
  <p class="ap-sub" id="ap-sub"></p>
  <nav class="ap-tabs" role="tablist">
    <button class="ap-tab" role="tab" data-tab="cours" aria-selected="true">Cours</button>
    <button class="ap-tab" role="tab" data-tab="fiche" aria-selected="false">Fiche de synthèse</button>
    <button class="ap-tab" role="tab" data-tab="exercices" aria-selected="false">Exercices</button>
  </nav>
</div></header>
<main class="ap-main">
  <section class="ap-panel" id="p-cours"><div class="ap-card"><div class="sci-doc" id="cours"></div></div></section>
  <section class="ap-panel" id="p-fiche" hidden><div class="ap-card"><div class="sci-doc" id="fiche"></div></div></section>
  <section class="ap-panel" id="p-exercices" hidden><div class="ex-list" id="exercices"></div></section>
</main>
<script id="data" type="application/json">${json}</script>
<script>
${engine}
${tune}

const DATA = JSON.parse(document.getElementById('data').textContent)
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;')

function withImages(html, map) {
  return html.replace(/\\[\\s*IMAGE\\s*_?\\s*(\\d+)\\s*\\]/gi, (m, pos) => {
    const img = map && map[pos]
    if (!img || !img.src) return m
    const dims = img.size ? ' width="' + img.size.w + '" height="' + img.size.h + '"' : ''
    return '<figure class="course-figure"><img alt="Illustration ' + pos + '"' + dims + ' src="' + img.src + '"></figure>'
  })
}

const typeset = async (el) => {
  if (!el || el.dataset.typeset) return
  el.dataset.typeset = '1'
  await MathJax.startup.promise
  await MathJax.typesetPromise([el])
  tuneMathOverflow(el)
}

document.getElementById('ap-title').textContent = DATA.titre
document.getElementById('ap-sub').textContent = DATA.sousTitre
document.getElementById('cours').innerHTML = withImages(renderOptitabDoc(DATA.cours, { context: 'course' }), DATA.images.cours)
document.getElementById('fiche').innerHTML = withImages(renderOptitabDoc(DATA.fiche, { context: 'sheet' }), DATA.images.fiche)

const LEVELS = { easy: 'Découverte', medium: 'Entraînement', hard: 'Approfondissement' }
const STARS = { easy: '★☆☆', medium: '★★☆', hard: '★★★' }
const list = document.getElementById('exercices')
DATA.exercices.forEach((ex, k) => {
  const imgs = DATA.images.exercices[ex.titre] || {}
  const card = document.createElement('article')
  card.className = 'ex-card'
  const tabs = [['enonce', 'Énoncé', ex.enonce], ['etapes', 'Étapes', ex.etapes], ['solution', 'Solution', ex.solution]]
  card.innerHTML =
    '<header class="ex-head"><span class="ex-level ex-level--' + ex.difficulte + '">' + (LEVELS[ex.difficulte] || '') + '</span>' +
    '<span class="ex-stars" aria-label="Difficulté">' + (STARS[ex.difficulte] || '') + '</span>' +
    '<h2 class="ex-title">' + esc(ex.titre) + '</h2></header>' +
    '<div class="ex-tabs" role="tablist">' + tabs.map((t, i) => '<button class="ex-tab" role="tab" data-i="' + i + '" aria-selected="' + (i === 0) + '">' + t[1] + '</button>').join('') + '</div>' +
    tabs.map((t, i) => '<div class="ex-panel sci-doc"' + (i ? ' hidden' : '') + '>' + withImages(renderOptitabDoc(t[2], { context: 'exercise' }), imgs) + '</div>').join('')
  card.querySelectorAll('.ex-tab').forEach((b) => b.addEventListener('click', () => {
    card.querySelectorAll('.ex-tab').forEach((x) => x.setAttribute('aria-selected', String(x === b)))
    card.querySelectorAll('.ex-panel').forEach((p, i) => { p.hidden = String(i) !== b.dataset.i })
    typeset(card.querySelectorAll('.ex-panel')[Number(b.dataset.i)])
  }))
  list.appendChild(card)
})

document.querySelectorAll('.ap-tab').forEach((b) => b.addEventListener('click', () => {
  document.querySelectorAll('.ap-tab').forEach((x) => x.setAttribute('aria-selected', String(x === b)))
  document.querySelectorAll('.ap-panel').forEach((p) => { p.hidden = p.id !== 'p-' + b.dataset.tab })
  if (b.dataset.tab === 'exercices') document.querySelectorAll('.ex-panel:not([hidden])').forEach(typeset)
  else typeset(document.getElementById(b.dataset.tab))
  window.scrollTo({ top: 0 })
}))

window.__ready = typeset(document.getElementById('cours'))
</script>
</body>
</html>
`

// Publication en artifact : le service ajoute lui-même doctype, head et body
const final = ARTIFACT
  ? html
      .replace(/^<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport"[^\n]*\n/, '')
      .replace('</head>\n<body>\n', '')
      .replace(/<\/body>\n<\/html>\n?$/, '')
  : html
fs.writeFileSync(out, final)
console.log('Aperçu :', out, `(${Math.round(html.length / 1024)} Ko)`)
