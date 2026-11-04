// Couvertures des articles du blog (1200 × 630, partages et Google Discover).
// Outil local, à lancer quand un article est ajouté ou que sa couverture change :
//   node scripts/ressources/couvertures.mjs [slug]
// Lit le champ « couverture » de chaque article (contenu/blog/*.md) et écrit
// public/blog/images/<slug>.png. Les images produites sont versionnées.
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
const COULEURS = ['#1b3c8e', '#1b3c8e', '#2f7a3a', '#f0a23b']

function page(info) {
  const c = info.couverture
  return `<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&display=swap">
<style>
*{box-sizing:border-box;margin:0}html,body{width:1200px;height:630px}
body{position:relative;overflow:hidden;font-family:'Montserrat',sans-serif;color:#0d1f4f;
background:radial-gradient(700px 420px at 100% 0%,rgba(95,172,96,.16),transparent 70%),radial-gradient(800px 500px at 0% 100%,rgba(27,60,142,.12),transparent 70%),#f6f8fc}
body::before{content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(27,60,142,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(27,60,142,.06) 1px,transparent 1px);background-size:30px 30px;-webkit-mask-image:radial-gradient(ellipse 80% 90% at 75% 40%,#000 20%,transparent 80%)}
.g{position:absolute;left:64px;top:56px;width:560px}
.logo{height:46px}
.k{margin-top:52px;color:#2f7a3a;font-size:18px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
h1{margin-top:14px;font-size:${c.titre.length > 16 ? 56 : 64}px;line-height:1.04;font-weight:800;letter-spacing:-.02em}
h1 span{display:block;color:#1b3c8e}
.s{margin-top:20px;color:#2c3550;font-size:24px;line-height:1.4;font-weight:600}
.pied{position:absolute;left:64px;bottom:52px;color:#5d667d;font-size:17px;font-weight:700}
.pied b{color:#1b3c8e}
.d{position:absolute;right:64px;top:92px;width:430px;display:grid;gap:16px}
.e{display:flex;align-items:center;gap:18px;padding:18px 22px;border:1px solid #e4e8f0;border-radius:20px;background:#fff;box-shadow:0 1px 2px rgba(16,32,79,.05),0 14px 30px rgba(16,32,79,.08)}
.e:nth-child(2),.e:nth-child(4){margin-left:28px}.e:nth-child(3){margin-left:56px}
.n{flex-shrink:0;width:46px;height:46px;border-radius:50%;display:grid;place-items:center;color:#fff;font-size:20px;font-weight:800}
.e b{display:block;font-size:22px}.e small{color:#5d667d;font-size:16px;font-weight:600}
</style></head><body>
<div class="g"><img class="logo" src="${LOGO}" alt="">
<p class="k">Le blog OptiTAB · ${esc(info.rubrique || 'Conseils')}</p>
<h1>${esc(c.titre)}<span>${esc(c.accent)}</span></h1>
<p class="s">${esc(c.sous)}</p></div>
<p class="pied"><b>optitab.net</b> · Cours de maths en ligne</p>
<div class="d">${c.points.map(([t, p], i) => `<div class="e"><span class="n" style="background:${COULEURS[i % 4]}">${i + 1}</span><span><b>${esc(t)}</b><small>${esc(p)}</small></span></div>`).join('')}</div>
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
  await onglet.evaluate(() => document.fonts.ready)
  // Contrôle : le texte de gauche ne doit ni déborder ni toucher les étapes.
  const { droiteTexte, gaucheEtapes, basTexte } = await onglet.evaluate(() => ({
    droiteTexte: Math.max(...[...document.querySelectorAll('.g > *')].map((n) => n.getBoundingClientRect().right)),
    gaucheEtapes: document.querySelector('.d').getBoundingClientRect().left,
    basTexte: document.querySelector('.g').getBoundingClientRect().bottom
  }))
  if (droiteTexte > gaucheEtapes - 24 || basTexte > 500) throw new Error(`${info.slug} : texte trop long pour la couverture`)
  await onglet.screenshot({ path: path.join(SORTIE, `${info.slug}.png`) })
  console.log('couverture :', `public/blog/images/${info.slug}.png`)
}
fs.rmSync(temporaire, { force: true })
await navigateur.close()
