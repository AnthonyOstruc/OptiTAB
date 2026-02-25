import fs from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { spawn, spawnSync } from 'node:child_process'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
const DEFAULT_BASE_URL = process.env.STRUCTURED_DATA_BASE_URL || 'http://127.0.0.1:4173'
const DEFAULT_SNAPSHOT_PATH = path.resolve(__dirname, '..', 'test-results', 'structured-data-snapshot.json')
const NAVIGATION_TIMEOUT_MS = 25000
const SERVER_START_TIMEOUT_MS = 45000

const MOCK_FIXTURES = {
  courseSlug: 'cours-gratuit-101-france-terminale-mathematiques-derivees',
  summarySlug: 'synthese-gratuite-202-france-terminale-mathematiques-derivees',
  exerciseSlug: 'exercice-gratuit-303-derivees-regles-base',
  notionId: '9001'
}

const COURSE_RESOURCE = {
  id: 101,
  slug: MOCK_FIXTURES.courseSlug,
  titre: 'Derivees : cours complet',
  contenu: '<p>Apprendre les derivees et leurs regles de calcul.</p>',
  excerpt: 'Cours complet sur les derivees',
  pays_nom: 'France',
  matiere_nom: 'Mathematiques',
  niveau_nom: 'Terminale'
}

const SUMMARY_RESOURCE = {
  id: 202,
  slug: MOCK_FIXTURES.summarySlug,
  titre: 'Derivees : fiche de synthese',
  contenu: '<p>Formules et methodes essentielles sur les derivees.</p>',
  excerpt: 'Fiche de synthese sur les derivees',
  pays_nom: 'France',
  matiere_nom: 'Mathematiques',
  niveau_nom: 'Terminale'
}

const EXERCISE_RESOURCE = {
  id: 303,
  slug: MOCK_FIXTURES.exerciseSlug,
  titre: 'Exercice derivees : regles de base',
  question: '<p>Calculer la derivee de f(x)=x^3.</p>',
  solution: '<p>f\'(x)=3x^2.</p>',
  etapes: '<ol><li>Identifier la puissance.</li><li>Appliquer la regle n*x^(n-1).</li></ol>',
  pays_nom: 'France',
  matiere_nom: 'Mathematiques',
  niveau_nom: 'Terminale',
  notion_nom: 'Derivees'
}

const EXERCISE_CHAPTER_LIST = [
  {
    id: 401,
    notion: Number(MOCK_FIXTURES.notionId),
    notion_nom: 'Derivees',
    titre: 'Exercice derivees 1',
    slug: 'exercice-gratuit-401-derivees-1',
    question: '<p>Calculer la derivee de x^2.</p>',
    solution: '<p>2x</p>',
    etapes: '<p>Regle de la puissance.</p>',
    pays_nom: 'France',
    matiere_nom: 'Mathematiques',
    niveau_nom: 'Terminale',
    is_locked: false,
    count: 2
  },
  {
    id: 402,
    notion: Number(MOCK_FIXTURES.notionId),
    notion_nom: 'Derivees',
    titre: 'Exercice derivees 2',
    slug: 'exercice-gratuit-402-derivees-2',
    question: '<p>Calculer la derivee de 1/x.</p>',
    solution: '<p>-1/x^2</p>',
    etapes: '<p>Reecrire x^-1 puis derivation.</p>',
    pays_nom: 'France',
    matiere_nom: 'Mathematiques',
    niveau_nom: 'Terminale',
    is_locked: false,
    count: 2
  }
]

const CASES = [
  {
    label: 'cours-list',
    path: '/ressources-gratuites/cours',
    expectedTypes: ['BreadcrumbList', 'FAQPage']
  },
  {
    label: 'cours-detail',
    path: `/ressources-gratuites/cours/${MOCK_FIXTURES.courseSlug}`,
    expectedTypes: ['BreadcrumbList', 'Course']
  },
  {
    label: 'summary-detail',
    path: `/ressources-gratuites/syntheses/${MOCK_FIXTURES.summarySlug}`,
    expectedTypes: ['BreadcrumbList', 'CreativeWork']
  },
  {
    label: 'exercise-detail',
    path: `/ressources-gratuites/exercices/${MOCK_FIXTURES.exerciseSlug}`,
    expectedTypes: ['BreadcrumbList', 'CreativeWork']
  },
  {
    label: 'exercise-chapter',
    path: `/ressources-gratuites/exercices/notion/${MOCK_FIXTURES.notionId}`,
    expectedTypes: ['BreadcrumbList', 'CreativeWork', 'ItemList']
  }
]

function cleanPath(rawPath) {
  const value = String(rawPath || '').trim()
  if (!value) return '/'
  const withSlash = value.startsWith('/') ? value : `/${value}`
  if (withSlash.length === 1) return withSlash
  return withSlash.replace(/\/+$/, '')
}

function buildListPayload(type, queryParams) {
  if (type === 'exercise') {
    const notion = String(queryParams.get('notion') || '').trim()
    const results = notion ? EXERCISE_CHAPTER_LIST : [
      {
        notion: Number(MOCK_FIXTURES.notionId),
        notion_nom: 'Derivees',
        pays_nom: 'France',
        matiere_nom: 'Mathematiques',
        niveau_nom: 'Terminale',
        count: EXERCISE_CHAPTER_LIST.length,
        is_locked: false
      }
    ]
    return { count: results.length, results }
  }

  if (type === 'summary') {
    return { count: 1, results: [SUMMARY_RESOURCE] }
  }

  return { count: 1, results: [COURSE_RESOURCE] }
}

async function setupApiMocks(context) {
  await context.route('**/api/free/learning-resources/**', async (route) => {
    const requestUrl = new URL(route.request().url())
    const pathname = requestUrl.pathname
    const trimmedPath = pathname.endsWith('/') ? pathname : `${pathname}/`
    const basePath = '/api/free/learning-resources/'

    if (trimmedPath === basePath) {
      const type = String(requestUrl.searchParams.get('type') || 'course').trim().toLowerCase()
      const payload = buildListPayload(type, requestUrl.searchParams)
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(payload)
      })
    }

    const slug = trimmedPath.slice(basePath.length).replace(/\/+$/, '')
    if (slug === MOCK_FIXTURES.courseSlug || slug.startsWith('cours-gratuit-101')) {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(COURSE_RESOURCE)
      })
    }
    if (slug === MOCK_FIXTURES.summarySlug || slug.startsWith('synthese-gratuite-202')) {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(SUMMARY_RESOURCE)
      })
    }
    if (slug === MOCK_FIXTURES.exerciseSlug || slug.startsWith('exercice-gratuit-303')) {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(EXERCISE_RESOURCE)
      })
    }

    return route.fulfill({
      status: 404,
      contentType: 'application/json',
      body: JSON.stringify({ detail: 'not found' })
    })
  })

}

function collectTypesFromGraph(payload) {
  if (!payload || typeof payload !== 'object') return []
  const graph = Array.isArray(payload?.['@graph']) ? payload['@graph'] : [payload]
  const rawTypes = graph.flatMap((item) => item?.['@type'] || [])
  return rawTypes
    .flat()
    .map((value) => String(value || '').trim())
    .filter(Boolean)
}

async function run() {
  let previewProcess = null
  const shouldAutoStartPreview = !process.env.STRUCTURED_DATA_BASE_URL && process.env.STRUCTURED_DATA_AUTOSTART !== 'false'

  if (shouldAutoStartPreview) {
    previewProcess = startPreviewServer()
    await waitForServer(DEFAULT_BASE_URL, SERVER_START_TIMEOUT_MS)
  }

  let chromium
  try {
    const playwright = await import('playwright')
    chromium = playwright.chromium
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error)
    throw new Error(`Playwright is required. Install with: npm --prefix frontend i -D playwright. (${reason})`)
  }

  try {
    const browser = await chromium.launch({ headless: true })
    const context = await browser.newContext()
    await setupApiMocks(context)
    const page = await context.newPage()

    const snapshot = []
    const failures = []

    try {
      for (const entry of CASES) {
        const targetUrl = new URL(cleanPath(entry.path), DEFAULT_BASE_URL).toString()
        await page.goto(targetUrl, { waitUntil: 'domcontentloaded', timeout: NAVIGATION_TIMEOUT_MS })
        await page.waitForLoadState('networkidle', { timeout: NAVIGATION_TIMEOUT_MS })
        await page.waitForSelector('#seo-jsonld', { state: 'attached', timeout: NAVIGATION_TIMEOUT_MS })

        const jsonLdText = await page.locator('#seo-jsonld').first().textContent()
        let parsed = null
        try {
          parsed = JSON.parse(String(jsonLdText || '{}'))
        } catch {
          parsed = null
        }

        const foundTypes = collectTypesFromGraph(parsed)
        const missingTypes = entry.expectedTypes.filter((expected) => !foundTypes.includes(expected))
        if (missingTypes.length > 0) {
          failures.push({
            label: entry.label,
            url: targetUrl,
            expectedTypes: entry.expectedTypes,
            foundTypes,
            missingTypes
          })
        }

        const headSnapshot = await page.evaluate(() => {
          const title = document.title
          const canonical = document.querySelector('link[rel="canonical"]')?.getAttribute('href') || ''
          const robots = document.querySelector('meta[name="robots"]')?.getAttribute('content') || ''
          const ogUrl = document.querySelector('meta[property="og:url"]')?.getAttribute('content') || ''
          return { title, canonical, robots, ogUrl }
        })

        snapshot.push({
          label: entry.label,
          requestedUrl: targetUrl,
          finalUrl: page.url(),
          expectedTypes: entry.expectedTypes,
          foundTypes,
          head: headSnapshot
        })
      }
    } finally {
      await context.close()
      await browser.close()
    }

    await fs.mkdir(path.dirname(DEFAULT_SNAPSHOT_PATH), { recursive: true })
    await fs.writeFile(DEFAULT_SNAPSHOT_PATH, JSON.stringify(snapshot, null, 2), 'utf8')
    console.log(`[structured-data] snapshot written: ${DEFAULT_SNAPSHOT_PATH}`)

    if (failures.length > 0) {
      console.error(`[structured-data] FAILED ${failures.length}/${CASES.length}`)
      for (const failure of failures) {
        console.error(`- ${failure.label}`)
        console.error(`  url=${failure.url}`)
        console.error(`  missing=${failure.missingTypes.join(', ')}`)
        console.error(`  found=${failure.foundTypes.join(', ') || '(none)'}`)
      }
      process.exit(1)
    }

    console.log(`[structured-data] PASS ${CASES.length}/${CASES.length}`)
  } finally {
    stopPreviewServer(previewProcess)
  }
}

run().catch((error) => {
  console.error('[structured-data] fatal:', error instanceof Error ? error.message : String(error))
  process.exit(1)
})

function startPreviewServer() {
  const frontendDir = path.resolve(__dirname, '..')
  const child = process.platform === 'win32'
    ? spawn('cmd.exe', ['/c', 'npm run preview -- --host 127.0.0.1 --port 4173'], {
        cwd: frontendDir,
        stdio: 'pipe'
      })
    : spawn('npm', ['run', 'preview', '--', '--host', '127.0.0.1', '--port', '4173'], {
        cwd: frontendDir,
        stdio: 'pipe'
      })

  child.stdout?.on('data', (chunk) => {
    const text = String(chunk || '').trim()
    if (text) process.stdout.write(`[structured-data][preview] ${text}\n`)
  })

  child.stderr?.on('data', (chunk) => {
    const text = String(chunk || '').trim()
    if (text) process.stderr.write(`[structured-data][preview] ${text}\n`)
  })

  return child
}

async function waitForServer(url, timeoutMs) {
  const startedAt = Date.now()
  while (Date.now() - startedAt < timeoutMs) {
    try {
      const response = await fetch(url, { method: 'GET' })
      if (response.ok || (response.status >= 200 && response.status < 500)) {
        return
      }
    } catch {
      // keep polling until timeout
    }
    await new Promise((resolve) => setTimeout(resolve, 500))
  }
  throw new Error(`Preview server did not start in time (${timeoutMs}ms): ${url}`)
}

function stopPreviewServer(processRef) {
  if (!processRef || processRef.killed) return
  try {
    if (process.platform === 'win32') {
      spawnSync('taskkill', ['/PID', String(processRef.pid), '/T', '/F'], { stdio: 'ignore' })
      return
    }
    processRef.kill('SIGTERM')
  } catch {
    // no-op
  }
}
