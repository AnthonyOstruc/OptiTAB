// Joue un quiz dans l'aperçu local (/apercu/quiz/<id>, serveur « npm run dev »)
// et photographie chaque écran sur téléphone (390 px) : accueil, chaque question
// avant et après correction, résultat. Répond juste une fois sur deux pour voir
// les deux corrections. Contrôle aussi : débordement horizontal, erreurs MathJax,
// erreurs de la console.
//   node captures_quiz.mjs <id> [dossier_captures] [--large]
import path from 'node:path'
import fs from 'node:fs'
import { createRequire } from 'node:module'
import { fileURLToPath } from 'node:url'

const here = path.dirname(fileURLToPath(import.meta.url))
const require = createRequire(path.resolve(here, '../../../package.json'))
const { chromium } = require('playwright-core')

const args = process.argv.slice(2).filter((a) => !a.startsWith('--'))
const [id, dossier = `captures_quiz_${args[0]}`] = args
const LARGE = process.argv.includes('--large')
const BASE = process.env.QUIZ_URL || 'http://localhost:5173'
fs.mkdirSync(dossier, { recursive: true })

const browser = await chromium.launch({ channel: 'chrome', headless: true })
const viewport = LARGE ? { width: 1280, height: 900 } : { width: 390, height: 844 }
const page = await browser.newPage({ viewport, deviceScaleFactor: 2 })
const erreurs = []
page.on('console', (m) => { if (m.type() === 'error') erreurs.push(m.text().slice(0, 200)) })
page.on('pageerror', (e) => erreurs.push(String(e).slice(0, 200)))

let n = 0
const problemes = []
async function photo(nom) {
  await page.waitForTimeout(500)
  await page.evaluate(async () => { if (window.MathJax?.startup?.promise) await window.MathJax.startup.promise })
  await page.waitForTimeout(300)
  const audit = await page.evaluate(() => ({
    deborde: document.documentElement.scrollWidth > window.innerWidth + 1,
    merr: [...document.querySelectorAll('mjx-merror')].map((e) => e.getAttribute('data-mjx-error') || e.textContent),
    brut: [...document.querySelectorAll('.qq, .cq-card')].some((el) => /\$[^$\s][^$]*\$/.test(el.innerText))
  }))
  if (audit.deborde) problemes.push(`${nom} : la page déborde en largeur`)
  if (audit.merr.length) problemes.push(`${nom} : erreur MathJax ${audit.merr.join(' | ')}`)
  if (audit.brut) problemes.push(`${nom} : formule non composée ($…$ visible)`)
  n += 1
  await page.screenshot({ path: path.join(dossier, `${String(n).padStart(2, '0')}_${nom}.png`), fullPage: true })
}

await page.goto(`${BASE}/apercu/quiz/${id}`, { waitUntil: 'domcontentloaded' })
await page.waitForSelector('.cq-accueil', { timeout: 60000 })
// Le bandeau des cookies n'appartient pas au quiz : masqué pour les captures
await page.addStyleTag({ content: '.cookie-consent-root{display:none!important}' })
await photo('accueil')
await page.click('.cq-go')

for (let k = 1; k <= 60; k += 1) {
  const q = await page.$('.qq')
  if (!q) break
  const bien = k % 2 === 1
  await photo(`q${k}_enonce`)
  // Une question sur cinq : bouton « Je ne sais pas »
  if (k % 5 === 0) {
    await page.click('.qq-actions .es-btn--ghost')
    await photo(`q${k}_je_ne_sais_pas`)
    await page.click('.qq-actions .es-btn')
    continue
  }
  // Répondre selon le type présent à l'écran
  if (await page.$('.qq-choix')) {
    const opts = await page.$$('.qq-choix .qq-option')
    await opts[bien ? 0 : opts.length - 1].click()
  } else if (await page.$('.qq-vf')) {
    await (await page.$$('.qq-vf .qq-option'))[bien ? 0 : 1].click()
  } else if (await page.$('.qq-saisie')) {
    const expression = /calculatrice/.test(await page.innerText('.qq-consigne'))
    await page.fill('.qq-champ input', expression ? (bien ? 'xe^x' : 'e^2x') : (bien ? '3' : '1/2'))
    await page.waitForTimeout(400)
    await photo(`q${k}_saisie`)
  } else if (await page.$('.qq-assoc')) {
    const lignes = await page.$$('.qq-ligne')
    for (const [i, l] of lignes.entries()) {
      const b = await l.$$('.qq-lettre-btn')
      await b[i % b.length].click()
    }
  }
  const valider = await page.$('.qq-actions .es-btn:not(.es-btn--ghost):not([disabled])')
  if (!valider) { problemes.push(`q${k} : impossible de valider`); break }
  await valider.click()
  await photo(`q${k}_correction`)
  await page.click('.qq-actions .es-btn')
}
await page.waitForSelector('.cq-fin', { timeout: 10000 })
await photo('resultat')
await browser.close()

for (const e of erreurs) problemes.push(`console : ${e}`)
console.log(`${n} captures dans ${dossier}`)
console.log(problemes.length ? problemes.map((p) => '✗ ' + p).join('\n') : '✓ aucun problème détecté')
