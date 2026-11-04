// Copie locale du contrôle commun : mêmes audits ; fermeture bornée pour le défaut Windows de nettoyage Playwright.
// Contrôle automatique d'une page d'aperçu (générée par apercu.mjs).
//
// Usage : node controle_apercu.mjs <apercu.html> <dossier_captures>
//
// Ouvre la page dans Chrome (téléphone 390 px et ordinateur 1280 px),
// affiche chaque onglet (cours, fiche, chaque exercice × énoncé / étapes /
// solution) et vérifie : débordement horizontal de la page, erreurs MathJax,
// « $ » restés en texte brut, blocs .otm-error, images non résolues.
// Enregistre des captures pleine page de chaque vue.
import path from 'node:path'
import fs from 'node:fs'
import { createRequire } from 'node:module'
import { fileURLToPath } from 'node:url'

const here = path.dirname(fileURLToPath(import.meta.url))
const require = createRequire(path.resolve(here, '../../../../../package.json'))
const { chromium } = require('playwright-core')

// --rapide : contrôles seulement, sans captures d'écran
const RAPIDE = process.argv.includes('--rapide')
const [page_file, shots = 'captures'] = process.argv.slice(2).filter((a) => !a.startsWith('--'))
if (!RAPIDE) fs.mkdirSync(shots, { recursive: true })
const url = 'file:///' + path.resolve(page_file).replace(/\\/g, '/')

const AUDIT = `(() => {
  const doc = document.documentElement
  const visible = (el) => !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length)
  const panels = [...document.querySelectorAll('.sci-doc')].filter(visible)
  const merr = [...document.querySelectorAll('mjx-merror')].filter(visible).map((e) => (e.getAttribute('data-mjx-error') || e.textContent).slice(0, 120))
  const raw = []
  for (const p of panels) {
    const walker = document.createTreeWalker(p, NodeFilter.SHOW_TEXT)
    let n
    while ((n = walker.nextNode())) {
      if (n.parentElement.closest('mjx-container, script, style')) continue
      if (/\\$|\\\\(frac|sqrt|displaystyle|left|right)/.test(n.textContent)) raw.push(n.textContent.trim().slice(0, 100))
    }
  }
  const imgs = panels.flatMap((p) => (p.innerText.match(/\\[IMAGE_?\\d+\\]/gi) || []))
  const errs = [...document.querySelectorAll('.otm-error')].filter(visible).map((e) => e.textContent)
  const wide = []
  for (const p of panels) {
    const box = p.getBoundingClientRect()
    p.querySelectorAll('*').forEach((el) => {
      const r = el.getBoundingClientRect()
      if (!r.width) return
      if (r.right > box.right + 2 && !el.closest('.otm-scroll, mjx-container.mjx-scrollable, mjx-assistive-mml')) {
        const scroller = el.closest('[style*="overflow"], .otm-scroll')
        if (!scroller) wide.push(el.tagName.toLowerCase() + '.' + String(el.className).slice(0, 30))
      }
    })
  }
  return { overflowX: doc.scrollWidth - doc.clientWidth, merr, raw: raw.slice(0, 10), imgs, errs, wide: [...new Set(wide)].slice(0, 8) }
})()`

// Au plus 5 Chrome de contrôle à la fois sur la machine (agents en parallèle)
const VERROUS = path.resolve(here, '../../../outils/.verrous')
fs.mkdirSync(VERROUS, { recursive: true })
let slot = null
while (!slot) {
  for (let k = 0; k < 5 && !slot; k += 1) {
    const f = path.join(VERROUS, `chrome_${k}.lock`)
    try {
      if (fs.existsSync(f) && Date.now() - fs.statSync(f).mtimeMs > 15 * 60 * 1000) fs.unlinkSync(f)
      fs.closeSync(fs.openSync(f, 'wx'))
      slot = f
    } catch { /* place occupée */ }
  }
  if (!slot) await new Promise((r) => setTimeout(r, 1500))
}
const libere = () => { try { fs.unlinkSync(slot) } catch { /* déjà libéré */ } }
process.on('exit', libere)
process.on('SIGINT', () => { libere(); process.exit(130) })

const browser = await chromium.launch({ channel: 'chrome', headless: true })
let problems = 0
for (const [label, viewport] of [['mobile', { width: 390, height: 844 }], ['desktop', { width: 1280, height: 900 }]]) {
  const page = await browser.newPage({ viewport, deviceScaleFactor: 1 })
  const consoleErrors = []
  page.on('console', (m) => { if (m.type() === 'error') consoleErrors.push(m.text()) })
  page.on('pageerror', (e) => consoleErrors.push(String(e)))
  await page.goto(url)
  await page.waitForFunction('window.__ready !== undefined')
  await page.evaluate('window.__ready')
  await page.waitForTimeout(300)

  const report = async (name) => {
    const r = await page.evaluate(AUDIT)
    const bad = r.overflowX > 0 || r.merr.length || r.raw.length || r.imgs.length || r.errs.length || r.wide.length
    if (bad) problems += 1
    console.log(`[${label}] ${name} : débordement ${r.overflowX}px · erreurs formule ${r.merr.length} · $ bruts ${r.raw.length} · images manquantes ${r.imgs.length} · blocs en erreur ${r.errs.length} · éléments trop larges ${r.wide.length}`)
    if (r.merr.length) console.log('    formules :', r.merr)
    if (r.raw.length) console.log('    texte brut :', r.raw)
    if (r.errs.length) console.log('    blocs :', r.errs)
    if (r.wide.length) console.log('    trop larges :', r.wide)
  }

  const docTabs = await page.$$eval('.ap-tab', (bs) => bs.map((b) => b.dataset.tab).filter((t) => t !== 'exercices'))
  for (const tab of docTabs) {
    await page.click(`.ap-tab[data-tab="${tab}"]`)
    await page.waitForFunction((id) => document.getElementById(id).dataset.typeset === '1', tab)
    await page.evaluate('MathJax.startup.promise')
    await page.waitForTimeout(400)
    await report(tab)
    if (RAPIDE) continue
    const h = await page.evaluate('document.documentElement.scrollHeight')
    for (let y = 0, part = 1; y < h && part <= 12; y += 2400, part += 1) {
      await page.screenshot({ path: path.join(shots, `${label}-${tab}-${part}.png`), fullPage: true, clip: { x: 0, y, width: viewport.width, height: Math.min(2400, h - y) } })
    }
  }

  const hasEx = await page.$('.ap-tab[data-tab="exercices"]')
  if (hasEx) await page.click('.ap-tab[data-tab="exercices"]')
  const cards = hasEx ? await page.$$('.ex-card') : []
  for (let k = 0; k < cards.length; k += 1) {
    for (let i = 0; i < 3; i += 1) {
      await page.evaluate(([k, i]) => document.querySelectorAll('.ex-card')[k].querySelectorAll('.ex-tab')[i].click(), [k, i])
      await page.waitForFunction(([k, i]) => document.querySelectorAll('.ex-card')[k].querySelectorAll('.ex-panel')[i].dataset.typeset === '1', [k, i])
      await page.waitForTimeout(250)
    }
  }
  // Vérifie chaque onglet de chaque exercice, affiché à son tour
  for (let k = 0; k < cards.length; k += 1) {
    for (let i = 0; i < 3; i += 1) {
      await page.evaluate(([k, i]) => document.querySelectorAll('.ex-card')[k].querySelectorAll('.ex-tab')[i].click(), [k, i])
      await page.waitForTimeout(120)
      const exId = await page.evaluate((k) => document.querySelectorAll('.ex-card')[k].dataset.id || '', k)
      await report(`exercice ${k + 1}${exId ? ` (Id ${exId})` : ''} onglet ${['énoncé', 'étapes', 'solution'][i]}`)
      if (!RAPIDE && (i === 1 || (i === 0 && k < 2))) {
        const el = cards[k]
        await el.screenshot({ path: path.join(shots, `${label}-ex${String(k + 1).padStart(2, '0')}-${['enonce', 'etapes', 'solution'][i]}.png`) })
      }
    }
  }
  if (consoleErrors.length) {
    problems += 1
    console.log(`[${label}] erreurs console :`, consoleErrors.slice(0, 5))
  }
  await page.close()
}
await Promise.race([browser.close(), new Promise((resolve) => setTimeout(resolve, 2000))])
console.log(problems ? `\n${problems} vue(s) à corriger` : '\nAucun problème détecté')
await new Promise((resolve) => process.stdout.write('', resolve))
process.exit(problems ? 2 : 0)
