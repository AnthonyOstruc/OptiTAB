// Image de partage par défaut du site (1200 × 630) : aperçus Google, WhatsApp,
// Facebook, LinkedIn… quand une page n'a pas d'image propre.
//   node scripts/vitrine/image-partage.mjs  →  public/og/optitab.png
// Même style que les couvertures du blog (scripts/ressources/couvertures.mjs).
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'
import { chromium } from 'playwright'

const ICI = path.dirname(fileURLToPath(import.meta.url))
const FRONT = path.resolve(ICI, '..', '..')
const SORTIE = path.join(FRONT, 'public', 'og')
const LOGO = pathToFileURL(path.join(FRONT, 'public', 'Logo_bg.png')).href
fs.mkdirSync(SORTIE, { recursive: true })

const html = `<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&display=swap">
<style>
*{box-sizing:border-box;margin:0}html,body{width:1200px;height:630px}
body{position:relative;overflow:hidden;font-family:'Montserrat',sans-serif;color:#0d1f4f;background:#f7f9fc}
body::before{content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(27,60,142,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(27,60,142,.05) 1px,transparent 1px);background-size:32px 32px;-webkit-mask-image:linear-gradient(90deg,#000 0%,transparent 60%)}
.g{position:absolute;left:68px;top:58px;width:610px;height:514px;display:flex;flex-direction:column}
.logo{height:52px;width:auto;align-self:flex-start}
.k{align-self:flex-start;margin-top:auto;padding:9px 18px;border-radius:999px;background:#2f7a3a1c;color:#2f7a3a;font-size:19px;font-weight:800;letter-spacing:.07em;text-transform:uppercase}
h1{margin-top:20px;font-size:80px;line-height:1.02;font-weight:800;letter-spacing:-.025em}
h1 span{display:block;color:#1b3c8e}
.s{margin-top:20px;color:#3a4560;font-size:26px;line-height:1.38;font-weight:600;text-wrap:balance}
.pied{margin-top:auto;color:#5d667d;font-size:18px;font-weight:700}.pied b{color:#1b3c8e}
.p{position:absolute;top:0;right:0;bottom:0;width:470px;background:linear-gradient(155deg,#1b3c8e 0%,#0e2461 100%);clip-path:polygon(64px 0,100% 0,100% 100%,0 100%)}
.p::before{content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.07) 1px,transparent 1px);background-size:32px 32px}
.v{position:absolute;left:96px;right:36px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;gap:16px;color:#fff}
.l{display:flex;align-items:center;gap:16px;padding:18px 20px;border-radius:18px;background:rgba(255,255,255,.1);font-size:20px;font-weight:700;white-space:nowrap}
.l b{flex-shrink:0;display:grid;place-items:center;width:42px;height:42px;border-radius:50%;background:#fff;color:#1b3c8e;font-size:20px}
</style></head><body>
<div class="g"><img class="logo" src="${LOGO}" alt="">
<p class="k">Cours de maths en ligne</p>
<h1>Les maths,<span>enfin claires.</span></h1>
<p class="s">Cours, fiches et exercices corrigés pas à pas, du CP à la Terminale.</p>
<p class="pied"><b>optitab.net</b> · Cours, fiches, exercices, professeurs</p></div>
<div class="p"><div class="v">
<p class="l"><b>1</b>Un cours limpide</p>
<p class="l"><b>2</b>Une fiche de synthèse</p>
<p class="l"><b>3</b>Des exercices corrigés</p>
<p class="l"><b>4</b>Un prof si besoin</p>
</div></div>
</body></html>`

const navigateur = await chromium.launch({ channel: 'chrome' })
const onglet = await navigateur.newPage({ viewport: { width: 1200, height: 630 } })
const temporaire = path.join(SORTIE, '.partage.html')
fs.writeFileSync(temporaire, html)
await onglet.goto(pathToFileURL(temporaire).href, { waitUntil: 'networkidle' })
await onglet.evaluate(() => document.fonts.ready)
const deborde = await onglet.evaluate(() =>
  [...document.querySelectorAll('.g > *')].some((n) => n.getBoundingClientRect().right > 740) ||
  [...document.querySelectorAll('.l')].some((n) => n.scrollWidth > n.clientWidth))
if (deborde) throw new Error('texte trop long pour l’image de partage')
await onglet.screenshot({ path: path.join(SORTIE, 'optitab.png') })
fs.rmSync(temporaire, { force: true })
await navigateur.close()
console.log('image de partage : public/og/optitab.png')
