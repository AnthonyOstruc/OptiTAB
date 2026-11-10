// Couvertures des articles du blog (1200 × 630, partages et Google Discover).
// Outil local, à lancer quand un article est ajouté ou que sa couverture change :
//   node scripts/ressources/couvertures.mjs [slug]
// Lit le champ « couverture » de chaque article (contenu/blog/*.md) et écrit
// public/blog/images/<slug>.png. Les images produites sont versionnées.
//
// Principe : peu d'éléments, mais grands, pour rester lisibles quand l'image
// est réduite sur les cartes du blog (environ 330 px de large) :
// - à gauche, la rubrique, le titre en grand et une phrase ;
// - à droite, un panneau à la couleur de la rubrique avec une grande icône
//   et un chiffre clé (champ « visuel » : icone, chiffre, legende).
// Les tailles de texte s'ajustent seules ; un contrôle refuse toute couverture
// dont un texte déborde de sa zone.
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'
import { chromium } from 'playwright'

const ICI = path.dirname(fileURLToPath(import.meta.url))
const FRONT = path.resolve(ICI, '..', '..')
const ARTICLES = path.join(FRONT, 'contenu', 'blog')
const SORTIE = path.join(FRONT, 'public', 'blog', 'images')
const LOGO = pathToFileURL(path.join(FRONT, 'public', 'Logo_bg.png')).href
const seul = process.argv[2]

const esc = (t) => String(t ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]))

// Couleur de chaque rubrique : [couleur principale, couleur foncée].
const THEMES = {
  'Méthode': ['#2f7a3a', '#1c4f24'],
  'Brevet': ['#1b3c8e', '#0e2461'],
  'Bac': ['#b86e12', '#7f4a08'],
  'Parents': ['#0f766e', '#0a4f4a'],
  'Orientation': ['#3557b7', '#1b3c8e'],
  'Primaire': ['#c2620c', '#8a4306']
}

// Icônes au trait (grille 24 × 24).
const ICONES = {
  ordinateur: '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>',
  progression: '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
  visio: '<rect x="2" y="6" width="14" height="12" rx="2"/><path d="m16 10 6-4v12l-6-4z"/>',
  horloge: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  calendrier: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
  famille: '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.4"/><path d="M15.5 14.2c3 .2 5.5 2.6 5.5 5.8"/>',
  liste: '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1"/><path d="m8.5 13 2.5 2.5 4.5-5"/>',
  boussole: '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/>',
  tableau: '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/>',
  eclair: '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>'
}

function page(info) {
  const c = info.couverture
  const v = c.visuel
  if (!v || !ICONES[v.icone]) throw new Error(`${info.slug} : couverture.visuel.icone inconnue (${v && v.icone})`)
  const [coul, fonce] = THEMES[info.rubrique] || THEMES.Brevet
  return `<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&display=swap">
<style>
*{box-sizing:border-box;margin:0}html,body{width:1200px;height:630px}
body{position:relative;overflow:hidden;font-family:'Montserrat',sans-serif;color:#0d1f4f;background:#f7f9fc}
body::before{content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(27,60,142,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(27,60,142,.05) 1px,transparent 1px);background-size:32px 32px;-webkit-mask-image:linear-gradient(90deg,#000 0%,transparent 60%)}
.g{position:absolute;left:68px;top:58px;width:600px;height:514px;display:flex;flex-direction:column}
.logo{height:44px;width:auto;align-self:flex-start}
.k{align-self:flex-start;margin-top:auto;padding:9px 18px;border-radius:999px;background:${coul}1c;color:${coul};font-size:19px;font-weight:800;letter-spacing:.07em;text-transform:uppercase}
.zt{margin-top:20px;height:250px;display:flex;flex-direction:column;justify-content:flex-start}
h1{font-size:76px;line-height:1.04;font-weight:800;letter-spacing:-.025em}
h1 span{display:block;color:${coul}}
.s{margin-top:18px;color:#3a4560;font-size:25px;line-height:1.38;font-weight:600;text-wrap:balance}
h1,.le{text-wrap:balance}
.pied{margin-top:auto;color:#5d667d;font-size:18px;font-weight:700}
.pied b{color:#1b3c8e}
.p{position:absolute;top:0;right:0;bottom:0;width:470px;background:linear-gradient(155deg,${coul} 0%,${fonce} 100%);clip-path:polygon(64px 0,100% 0,100% 100%,0 100%)}
.p::before{content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.07) 1px,transparent 1px);background-size:32px 32px}
.p::after{content:'';position:absolute;width:520px;height:520px;right:-230px;top:-250px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.16),transparent 70%)}
.v{position:absolute;left:96px;right:40px;top:0;bottom:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:#fff}
.rond{width:188px;height:188px;border-radius:50%;background:#fff;display:grid;place-items:center;box-shadow:0 18px 40px rgba(0,0,0,.18)}
.rond svg{width:104px;height:104px;fill:none;stroke:${coul};stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round}
.ch{margin-top:30px;font-size:84px;line-height:1;font-weight:800;letter-spacing:-.02em;white-space:nowrap}
.le{margin-top:14px;max-width:310px;font-size:24px;line-height:1.3;font-weight:600;opacity:.9}
</style></head><body>
<div class="g"><img class="logo" src="${LOGO}" alt="">
<p class="k">${esc(info.rubrique || 'Conseils')}</p>
<div class="zt"><h1>${esc(c.titre)}<span>${esc(c.accent)}</span></h1>
<p class="s">${esc(c.sous)}</p></div>
<p class="pied"><b>optitab.net</b> · Cours de maths en ligne</p></div>
<div class="p"><div class="v"><div class="rond"><svg viewBox="0 0 24 24">${ICONES[v.icone]}</svg></div>
<p class="ch">${esc(v.chiffre)}</p><p class="le">${esc(v.legende)}</p></div></div>
<script>
// Ajuste les tailles (appelée une fois les polices chargées) : le titre et la
// phrase tiennent dans leur zone, le chiffre clé tient dans le panneau.
function ajuster() {
  const zt = document.querySelector('.zt'), h1 = document.querySelector('h1'), ch = document.querySelector('.ch')
  let t = 76
  while (t > 44 && (zt.scrollHeight > zt.clientHeight || h1.scrollWidth > h1.clientWidth)) { t -= 2; h1.style.fontSize = t + 'px' }
  let n = 84
  while (n > 40 && ch.scrollWidth > 330) { n -= 2; ch.style.fontSize = n + 'px' }
}
</script>
</body></html>`
}

const fichiers = fs.readdirSync(ARTICLES).filter((f) => f.endsWith('.md'))
const navigateur = await chromium.launch({ channel: 'chrome' })
const onglet = await navigateur.newPage({ viewport: { width: 1200, height: 630 } })
const temporaire = path.join(SORTIE, '.couverture.html')
fs.mkdirSync(SORTIE, { recursive: true })
for (const f of fichiers) {
  const source = fs.readFileSync(path.join(ARTICLES, f), 'utf8').replace(/\r\n/g, '\n')
  const info = JSON.parse(source.match(/^---\n([\s\S]*?)\n---\n/)[1])
  if (!info.couverture || (seul && info.slug !== seul)) continue
  fs.writeFileSync(temporaire, page(info))
  await onglet.goto(pathToFileURL(temporaire).href, { waitUntil: 'networkidle' })
  await onglet.evaluate(async () => { await document.fonts.ready; ajuster() })
  // Contrôle : aucun texte ne déborde de sa zone ni ne touche le panneau.
  const pb = await onglet.evaluate(() => {
    const zt = document.querySelector('.zt'), h1 = document.querySelector('h1'), ch = document.querySelector('.ch')
    const panneau = document.querySelector('.p').getBoundingClientRect().left + 64
    const droite = Math.max(...[...document.querySelectorAll('.g *')].map((n) => n.getBoundingClientRect().right))
    const out = []
    if (zt.scrollHeight > zt.clientHeight + 1) out.push('titre et phrase trop longs')
    if (h1.scrollWidth > h1.clientWidth + 1) out.push('mot du titre trop long')
    if (droite > panneau - 24) out.push('texte trop près du panneau')
    if (ch.scrollWidth > 332) out.push('chiffre clé trop long')
    if (document.querySelector('.le').getBoundingClientRect().bottom > 600) out.push('légende trop longue')
    return out
  })
  if (pb.length) throw new Error(`${info.slug} : ${pb.join(', ')}`)
  await onglet.screenshot({ path: path.join(SORTIE, `${info.slug}.png`) })
  console.log('couverture :', `public/blog/images/${info.slug}.png`)
}
fs.rmSync(temporaire, { force: true })
await navigateur.close()
