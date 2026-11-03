// Enregistre la démo vidéo de la vitrine avec le compte démo.
// usage (depuis frontend/) :
//   DEMO_EMAIL=demo@optitab.net DEMO_PASSWORD=... node scripts/demo-video/record.mjs desktop|mobile
// Prérequis : site local (npm run dev, port 3000) et API locale (port 8000).
// Sortie : scripts/demo-video/.work/rec-<mode>/ (images + timeline.json), puis build.py.
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { chromium } from 'playwright'

const HERE = path.dirname(fileURLToPath(import.meta.url))
const WORK = path.join(HERE, '.work')
const API = process.env.API_URL || 'http://localhost:8000'
const EMAIL = process.env.DEMO_EMAIL || 'demo@optitab.net'
const PASSWORD = process.env.DEMO_PASSWORD
if (!PASSWORD) {
  console.error('DEMO_PASSWORD manquant (mot de passe du compte démo).')
  process.exit(1)
}
const MODE = process.argv[2] || 'desktop'
const MOBILE = MODE === 'mobile'
// Ordinateur filmé en 1024 × 640 (format 16:10, dernière largeur où la plateforme
// garde sa mise en page « ordinateur ») : le texte est 40 % plus gros qu'en 1440.
const W = MOBILE ? 390 : 1024
const H = MOBILE ? 844 : 640
// Ordinateur en ×1,5 : au-delà, la capture ralentit et le défilement saccade.
const DPR = Number(process.env.DPR || (MOBILE ? 2 : 1.5))
const BASE = process.env.BASE_URL || 'http://localhost:3000'
const NOTION = MOBILE ? 179 : 89
const OUT = path.join(WORK, `rec-${MODE}`)
fs.rmSync(OUT, { recursive: true, force: true })
fs.mkdirSync(`${OUT}/frames`, { recursive: true })
fs.mkdirSync(`${OUT}/checks`, { recursive: true })

// Sans ce drapeau, le screencast livre des images en pixels CSS (390 px de large) même avec deviceScaleFactor 2.
const browser = await chromium.launch({ channel: 'chrome', args: DPR > 1 ? [`--force-device-scale-factor=${DPR}`] : [] })
// Connexion par l'API : les jetons sont posés dans le localStorage avant le chargement.
const login = await fetch(`${API}/api/users/login/`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
  body: JSON.stringify({ email: EMAIL, password: PASSWORD })
}).then((r) => r.json())
const tokens = login.data || login
const access = tokens.access || tokens.access_token || tokens.tokens?.access
const refresh = tokens.refresh || tokens.refresh_token || tokens.tokens?.refresh
if (!access) {
  console.error('Connexion du compte démo impossible :', JSON.stringify(login).slice(0, 300))
  process.exit(1)
}

const ctx = await browser.newContext({
  viewport: { width: W, height: H },
  deviceScaleFactor: DPR,
  isMobile: MOBILE,
  hasTouch: MOBILE
})
await ctx.addInitScript(([a, r]) => {
  try {
    localStorage.setItem('access_token', a)
    if (r) localStorage.setItem('refresh_token', r)
    localStorage.setItem('optitab_cookie_consent_v1', JSON.stringify({ analytics: 'denied', marketing: 'denied', expiresAt: Date.now() + 1e10 }))
  } catch (e) {}
}, [access, refresh])
const page = await ctx.newPage()
const wait = (ms) => page.waitForTimeout(ms)

// ---------- Aides dans la page ----------

const DEMO_CSS = `
  .dashboard-main { scrollbar-width: none !important; }
  .dashboard-main::-webkit-scrollbar, html::-webkit-scrollbar, body::-webkit-scrollbar { display: none !important; }
  .scroll-top-btn, [class*="scroll-top"], [class*="back-to-top"] { display: none !important; }
  #demo-cursor { position: fixed; left: 0; top: 0; z-index: 2147483647; pointer-events: none;
    width: 26px; height: 26px; transform: translate(-100px, -100px); will-change: transform;
    filter: drop-shadow(0 2px 3px rgba(0,0,0,.35)); }
  .demo-ripple { position: fixed; z-index: 2147483646; pointer-events: none; border-radius: 50%;
    width: 44px; height: 44px; margin: -22px 0 0 -22px; border: 3px solid rgba(37, 99, 235, .75);
    background: rgba(37, 99, 235, .12); animation: demo-ripple .55s ease-out forwards; }
  @keyframes demo-ripple { from { transform: scale(.35); opacity: 1 } to { transform: scale(1.25); opacity: 0 } }
  .demo-touch { position: fixed; z-index: 2147483646; pointer-events: none; border-radius: 50%;
    width: 46px; height: 46px; margin: -23px 0 0 -23px; background: rgba(60, 60, 67, .28);
    border: 2px solid rgba(255,255,255,.85); box-shadow: 0 2px 10px rgba(0,0,0,.18);
    animation: demo-touch .6s ease-out forwards; }
  @keyframes demo-touch { 0% { transform: scale(.6); opacity: 0 } 25% { transform: scale(1); opacity: 1 }
    70% { opacity: 1 } 100% { transform: scale(1.15); opacity: 0 } }
  #demo-kick { position: fixed; right: 0; bottom: 0; width: 1px; height: 1px; z-index: 2147483647; pointer-events: none; }
`

const installHelpers = async () => {
  await page.addStyleTag({ content: DEMO_CSS })
  await page.evaluate((mobile) => {
    if (!document.getElementById('demo-kick')) {
      const k = document.createElement('div'); k.id = 'demo-kick'; document.body.appendChild(k)
    }
    if (!mobile && !document.getElementById('demo-cursor')) {
      const c = document.createElement('div'); c.id = 'demo-cursor'
      c.innerHTML = '<svg viewBox="0 0 26 26" width="26" height="26"><path d="M5 2.5 L5 21 L9.6 16.6 L12.6 23.4 L15.6 22.1 L12.7 15.4 L19 15.4 Z" fill="#111" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>'
      document.body.appendChild(c)
    }
  }, MOBILE)
}

// Le curseur se range dans la marge grise à droite du contenu.
const PARK = { x: W - 30, y: Math.round(H * 0.5) }
let cursor = { ...PARK }

// Déplacement du curseur avec une courbe douce, animé dans la page (60 i/s).
const cursorTo = async (x, y, ms = 900) => {
  await page.evaluate(({ from, to, ms }) => new Promise((resolve) => {
    const el = document.getElementById('demo-cursor')
    const t0 = performance.now()
    const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2)
    const step = (now) => {
      const p = Math.min(1, (now - t0) / ms)
      const e = ease(p)
      // Légère courbe pour un geste naturel.
      const bx = from.x + (to.x - from.x) * e
      const by = from.y + (to.y - from.y) * e - Math.sin(Math.PI * e) * 18
      el.style.transform = `translate(${bx - 5}px, ${by - 2.5}px)`
      if (p < 1) requestAnimationFrame(step); else resolve()
    }
    requestAnimationFrame(step)
  }), { from: cursor, to: { x, y }, ms })
  cursor = { x, y }
  await page.mouse.move(x, y)
}

const ripple = async (x, y, cls) => {
  await page.evaluate(({ x, y, cls }) => {
    const r = document.createElement('div'); r.className = cls
    r.style.left = x + 'px'; r.style.top = y + 'px'
    document.body.appendChild(r); setTimeout(() => r.remove(), 900)
  }, { x, y, cls })
}

const centerOf = async (locator) => {
  const b = await locator.boundingBox()
  return { x: b.x + b.width / 2, y: b.y + b.height / 2 }
}

// Clic visible : le curseur rejoint la cible, effet d'onde, vrai clic.
const clickOn = async (locator, travel = 950) => {
  const c = await centerOf(locator)
  if (MOBILE) {
    await ripple(c.x, c.y, 'demo-touch')
    await wait(140)
    await locator.tap({ force: true })
  } else {
    await cursorTo(c.x, c.y, travel)
    await wait(160)
    await ripple(c.x, c.y, 'demo-ripple')
    await locator.click({ force: true })
  }
}

const scroller = () => page.evaluate(() => {
  const sc = document.querySelector('.dashboard-main')
  return sc && sc.scrollHeight > sc.clientHeight + 10 ? 'main' : 'window'
})

const setScroll = async (y) => {
  await page.evaluate((y) => {
    const sc = document.querySelector('.dashboard-main')
    if (sc && sc.scrollHeight > sc.clientHeight + 10) sc.scrollTop = y; else window.scrollTo(0, y)
  }, y)
}

// Défilement doux (ease-in-out) sur la durée demandée.
const scrollTo = async (y, ms = 1600) => {
  await page.evaluate(({ y, ms }) => new Promise((resolve) => {
    const sc = document.querySelector('.dashboard-main')
    const useMain = sc && sc.scrollHeight > sc.clientHeight + 10
    const get = () => (useMain ? sc.scrollTop : window.scrollY)
    const set = (v) => (useMain ? (sc.scrollTop = v) : window.scrollTo(0, v))
    const from = get(); const t0 = performance.now()
    const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2)
    const step = (now) => {
      const p = Math.min(1, (now - t0) / ms)
      set(from + (y - from) * ease(p))
      if (p < 1) requestAnimationFrame(step); else resolve()
    }
    requestAnimationFrame(step)
  }), { y, ms })
}

// Position (dans le conteneur qui défile) du haut d'un élément.
const topOf = (selectorOrText, byText = false) => page.evaluate(({ s, byText }) => {
  const sc = document.querySelector('.dashboard-main')
  const useMain = sc && sc.scrollHeight > sc.clientHeight + 10
  let el
  if (byText) {
    el = [...document.querySelectorAll('.exercice-card')].find((c) => c.textContent.includes(s))
  } else {
    el = document.querySelector(s)
  }
  if (!el) return null
  const r = el.getBoundingClientRect()
  return Math.round(r.top + (useMain ? sc.scrollTop : window.scrollY))
}, { s: selectorOrText, byText })

// Position d'un élément dans le conteneur qui défile : le plus profond contenant
// `text`, ou la première figure d'une carte d'exercice (`img: true`).
const posOf = (text, { inCard = null, img = false } = {}) => page.evaluate(({ text, inCard, img }) => {
  const sc = document.querySelector('.dashboard-main')
  const root = inCard
    ? [...document.querySelectorAll('.exercice-card')].find((c) => c.textContent.includes(inCard))
    : (sc || document.body)
  if (!root) return null
  let el
  if (img) {
    el = [...root.querySelectorAll('img')].find((i) => i.naturalWidth > 80 && i.offsetParent !== null)
  } else {
    const all = [...root.querySelectorAll('*')].filter((e) => e.offsetParent !== null && e.textContent.includes(text))
    el = all.find((e) => ![...e.children].some((c) => c.textContent.includes(text)))
  }
  if (!el) return null
  const r = el.getBoundingClientRect()
  const base = sc ? sc.getBoundingClientRect().top : 0
  return { top: Math.round(r.top - base + (sc ? sc.scrollTop : window.scrollY)), height: Math.round(r.height), view: sc ? sc.clientHeight : window.innerHeight }
}, { text, inCard, img })

// Cible de défilement : l'élément `marge` px sous le haut de la zone visible.
const topTarget = async (text, marge = 24, opts = {}) => {
  const p = await posOf(text, opts)
  if (!p) throw new Error(`Élément introuvable : ${text || 'figure'}`)
  return Math.max(0, p.top - marge)
}

// Cible de défilement : le bas de l'élément `marge` px au-dessus du bas de la zone visible.
const bottomTarget = async (text, marge = 24, opts = {}) => {
  const p = await posOf(text, opts)
  if (!p) throw new Error(`Élément introuvable : ${text || 'figure'}`)
  return Math.max(0, p.top + p.height - p.view + marge)
}

const waitForImages = () => page.evaluate(() => Promise.all(
  [...document.images].filter((i) => !i.complete).map((i) => new Promise((r) => { i.onload = i.onerror = r; setTimeout(r, 4000) }))
))

const check = async (name) => {
  await page.screenshot({ path: `${OUT}/checks/${name}.png` })
}

// ---------- Capture image par image (CDP screencast) ----------

const cdp = await ctx.newCDPSession(page)
const frames = []
let recording = false
let offset = 0
let pausedAt = 0
let lastStamp = 0
cdp.on('Page.screencastFrame', ({ data, metadata, sessionId }) => {
  cdp.send('Page.screencastFrameAck', { sessionId }).catch(() => {})
  lastStamp = metadata.timestamp
  if (!recording) return
  const file = `f${String(frames.length).padStart(5, '0')}.jpg`
  fs.writeFileSync(`${OUT}/frames/${file}`, Buffer.from(data, 'base64'))
  frames.push({ file, t: metadata.timestamp - offset })
})

const kick = async () => {
  await page.evaluate(() => {
    const k = document.getElementById('demo-kick')
    if (k) k.style.background = k.style.background === 'rgba(0, 0, 0, 0.01)' ? 'rgba(0, 0, 0, 0.02)' : 'rgba(0, 0, 0, 0.01)'
  })
}

const nowSec = () => Date.now() / 1000
const cutStart = async () => { recording = false; pausedAt = nowSec() }
const cutEnd = async () => {
  offset += nowSec() - pausedAt
  recording = true
  await kick()
  await wait(60)
  await kick()
}

// ---------- Scénarios ----------

const tab = (label) => MOBILE
  ? page.locator('[aria-label="Onglet suivant"]').first()
  : page.getByText(label, { exact: true }).first()

const goTab = async (label) => {
  // Clic visible, puis on coupe le temps de bascule de page.
  await clickOn(tab(label))
  await wait(MOBILE ? 380 : 260)
  await cutStart()
  await page.waitForLoadState('networkidle').catch(() => {})
  await wait(700)
  await waitForImages()
}

// Clic sur un onglet d'exercice : le temps où la carte est vide (formules en cours
// de mise en page) est coupé au montage.
const clickTabThenCut = async (card, label, travel) => {
  const target = exerciseTab(card, label)
  const c = await centerOf(target)
  if (MOBILE) {
    await ripple(c.x, c.y, 'demo-touch')
    await wait(160)
    await target.tap({ force: true })
  } else {
    await cursorTo(c.x, c.y, travel)
    await wait(160)
    await ripple(c.x, c.y, 'demo-ripple')
    await wait(120)
    await target.click({ force: true })
  }
  await cutStart()
  await page.waitForFunction((cardText) => {
    const el = [...document.querySelectorAll('.exercice-card')].find((x) => x.textContent.includes(cardText))
    if (!el) return false
    const imgsOk = [...el.querySelectorAll('img')].every((i) => i.complete)
    return el.querySelectorAll('mjx-container').length > 3 && imgsOk
  }, card, { timeout: 8000 }).catch(() => {})
  await wait(400)
}

const exerciseTab = (card, label) => page.locator('.exercice-card', { hasText: card }).first().locator('button, [role=tab]', { hasText: label }).first()

const CARD = MOBILE ? 'Formule des Probabilités Totales' : 'Aires sous la Courbe'

// 1) Préchauffage : chaque page est ouverte une fois (gardée en mémoire par l'application).
await page.goto(`${BASE}/course-notion/${NOTION}`, { waitUntil: 'networkidle', timeout: 90000 })
await wait(2500)
for (const label of ['Synthèse', 'Exercices']) {
  await tab(label).click({ force: true })
  await page.waitForLoadState('networkidle').catch(() => {})
  await wait(2500)
}
// L'onglet Étapes de l'exercice choisi : on charge ses figures puis on revient à l'énoncé.
await exerciseTab(CARD, 'Étapes').scrollIntoViewIfNeeded()
await exerciseTab(CARD, 'Étapes').click({ force: true })
await wait(1500)
await waitForImages()
await exerciseTab(CARD, 'Énoncé').click({ force: true })
await wait(600)
const cardTop = await topOf(CARD, true)
console.log('carte exercice à', cardTop)

// Retour au cours dans l'application (sans recharger : les pages restent en mémoire).
if (MOBILE) {
  for (let i = 0; i < 2; i++) {
    await page.locator('[aria-label="Onglet précédent"]').first().click({ force: true })
    await wait(1500)
  }
} else {
  await tab('Cours').click({ force: true })
  await wait(2000)
}
await page.waitForLoadState('networkidle').catch(() => {})
console.log('retour au cours :', new URL(page.url()).pathname)
await waitForImages()
await installHelpers()
await setScroll(0)
await wait(500)
if (!MOBILE) {
  await page.evaluate(({ x, y }) => { document.getElementById('demo-cursor').style.transform = `translate(${x - 5}px, ${y - 2.5}px)` }, cursor)
  await page.mouse.move(cursor.x, cursor.y)
}
await check('00-depart')

// 2) Tournage
await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 93, everyNthFrame: 1, maxWidth: W * DPR, maxHeight: H * DPR })
await wait(300)
recording = true
const tStart = nowSec()
await kick()

if (!MOBILE) {
  // Cours : la définition de l'intégrale et sa figure.
  await wait(1300)
  await scrollTo(await topTarget('Intégrale et aire', 72), 1900)
  await wait(2400)
  await check('01-cours')

  // Fiche de synthèse : l'aire entre deux courbes.
  await goTab('Synthèse')
  await setScroll(0)
  await cutEnd()
  await wait(700)
  await Promise.all([scrollTo(await topTarget('Aires et valeur moyenne', 72), 2000), cursorTo(PARK.x, PARK.y, 1500)])
  await wait(2400)
  await check('02-fiche')

  // Exercices : un exercice d'aire sous la courbe, puis ses étapes.
  await goTab('Exercices')
  // La page restaure sa propre position en se réactivant : on attend, on vise le
  // titre de la carte (sous le bouton « Retour aux chapitres »), puis on confirme.
  await wait(600)
  const exoTop = await topTarget(CARD, 84)
  await setScroll(exoTop)
  await wait(500)
  await setScroll(exoTop)
  await wait(250)
  console.log('défilement exercice', exoTop, await page.evaluate(() => document.querySelector('.dashboard-main')?.scrollTop))
  await cutEnd()
  await Promise.all([wait(1500), cursorTo(PARK.x, PARK.y, 1100)])
  await check('03-exo-enonce')
  await clickTabThenCut(CARD, 'Étapes', 900)
  await cutEnd()
  await wait(900)
  await Promise.all([scrollTo(await bottomTarget('', 20, { inCard: CARD, img: true }), 2000), cursorTo(PARK.x, PARK.y, 1500)])
  await wait(2800)
  await check('04-exo-etapes')
} else {
  // Cours : les arbres pondérés.
  await wait(1300)
  await scrollTo(await topTarget('', 90, { img: true }), 1800)
  await wait(1800)
  await scrollTo(await topTarget('Test de dépistage', 64), 2100)
  await wait(2300)
  await check('01-cours')

  // Fiche de synthèse.
  await goTab('Synthèse')
  await setScroll(0)
  await cutEnd()
  await wait(1100)
  await scrollTo(260, 1300)
  await wait(2000)
  await check('02-fiche')

  // Exercices : énoncé puis étapes.
  await goTab('Exercices')
  await setScroll(Math.max(0, cardTop - 70))
  await wait(300)
  await cutEnd()
  await wait(1500)
  await check('03-exo-enonce')
  await clickTabThenCut(CARD, 'Étapes')
  await cutEnd()
  await wait(1000)
  await scrollTo(await topTarget('Arbre pondéré', 64, { inCard: CARD }), 2100)
  await wait(2700)
  await check('04-exo-etapes')
}

await kick()
await wait(200)
const tEnd = nowSec() - offset
recording = false
await cdp.send('Page.stopScreencast')
await cdp.detach().catch(() => {})

// Durée de chaque image = écart avec la suivante.
const timeline = frames.map((f, i) => ({
  file: f.file,
  d: Math.max(0.001, (i + 1 < frames.length ? frames[i + 1].t : tEnd) - f.t)
}))
const total = timeline.reduce((a, f) => a + f.d, 0)
fs.writeFileSync(`${OUT}/timeline.json`, JSON.stringify({ W: W * DPR, H: H * DPR, total, timeline }, null, 1))
console.log(JSON.stringify({ mode: MODE, images: frames.length, duree: total.toFixed(2), reel: (nowSec() - tStart).toFixed(1) }))
await browser.close().catch(() => {})
process.exit(0)
