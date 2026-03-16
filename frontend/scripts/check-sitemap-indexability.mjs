import fs from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const DEFAULT_SITEMAP_PATH = path.resolve(__dirname, '..', 'public', 'sitemap.xml')
const DEFAULT_SAMPLE_SIZE = 30
const DEFAULT_CONCURRENCY = 5
const NAVIGATION_TIMEOUT_MS = 30000
const NETWORK_IDLE_TIMEOUT_MS = 15000
const MIN_DESCRIPTION_LENGTH = 90
const MAX_DESCRIPTION_LENGTH = 220
const GENERIC_DESCRIPTION_MARKERS = [
  'plateforme de maths',
  'cours particuliers',
  '6e, 5e, 4e, 3e',
  'prepa'
]

function parseCliArgs(argv) {
  const options = {
    sitemapPath: DEFAULT_SITEMAP_PATH,
    sampleSize: DEFAULT_SAMPLE_SIZE,
    concurrency: DEFAULT_CONCURRENCY,
    siteOrigin: ''
  }

  for (const arg of argv) {
    if (arg.startsWith('--sitemap=')) {
      const value = arg.slice('--sitemap='.length).trim()
      if (value) options.sitemapPath = path.resolve(process.cwd(), value)
      continue
    }

    if (arg.startsWith('--sample=')) {
      const raw = Number(arg.slice('--sample='.length))
      if (Number.isFinite(raw) && raw > 0) options.sampleSize = Math.floor(raw)
      continue
    }

    if (arg.startsWith('--concurrency=')) {
      const raw = Number(arg.slice('--concurrency='.length))
      if (Number.isFinite(raw) && raw > 0) options.concurrency = Math.max(1, Math.min(Math.floor(raw), 10))
      continue
    }

    if (arg.startsWith('--site=')) {
      const value = arg.slice('--site='.length).trim()
      if (value) {
        try {
          const url = new URL(value)
          options.siteOrigin = `${url.origin}`.replace(/\/+$/, '')
        } catch {
          // Ignore invalid site origin values.
        }
      }
    }
  }

  return options
}

function normalizePathname(pathname) {
  const raw = String(pathname || '').trim()
  if (!raw) return ''

  let resolvedPath = raw
  try {
    const parsed = new URL(raw, 'https://www.optitab.net')
    resolvedPath = parsed.pathname || '/'
  } catch {
    resolvedPath = raw
  }

  if (!resolvedPath.startsWith('/')) {
    resolvedPath = `/${resolvedPath}`
  }

  const normalized = resolvedPath.replace(/\/+$/, '')
  return normalized || '/'
}

function normalizeAbsoluteUrl(rawUrl, baseUrl) {
  try {
    const url = new URL(String(rawUrl || ''), String(baseUrl || 'https://www.optitab.net'))
    url.hash = ''
    url.search = ''
    url.pathname = normalizePathname(url.pathname)
    return `${url.origin}${url.pathname}`
  } catch {
    return ''
  }
}

function extractLocsFromSitemapXml(xml) {
  const matches = [...String(xml || '').matchAll(/<loc>(.*?)<\/loc>/g)]
  return matches
    .map((match) => String(match?.[1] || '').trim())
    .filter(Boolean)
}

function pickRandomItems(items, count) {
  const copy = [...items]
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1))
    const temp = copy[i]
    copy[i] = copy[j]
    copy[j] = temp
  }
  return copy.slice(0, Math.min(count, copy.length))
}

async function loadPlaywright() {
  try {
    const mod = await import('playwright')
    if (!mod?.chromium) {
      throw new Error('playwright module loaded without chromium export')
    }
    return mod
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error)
    throw new Error(`Playwright is required for SPA sitemap checks. Install with: npm --prefix frontend i -D playwright. (${reason})`)
  }
}

function toNavigationUrl(expectedUrl, siteOrigin) {
  const normalizedExpected = normalizeAbsoluteUrl(expectedUrl, expectedUrl)
  if (!normalizedExpected) return ''
  if (!siteOrigin) return normalizedExpected
  try {
    const expected = new URL(normalizedExpected)
    return `${siteOrigin}${normalizePathname(expected.pathname)}`
  } catch {
    return normalizedExpected
  }
}

function normalizeWhitespace(value) {
  return String(value || '')
    .replace(/\s+/g, ' ')
    .trim()
}

function normalizeHtmlEntities(value) {
  return normalizeWhitespace(
    String(value || '')
      .replace(/&amp;/gi, '&')
      .replace(/&lt;/gi, '<')
      .replace(/&gt;/gi, '>')
      .replace(/&quot;/gi, '"')
      .replace(/&#39;|&apos;/gi, "'")
  )
}

function looksGenericDescription(value) {
  const normalized = normalizeHtmlEntities(value).toLowerCase()
  if (!normalized) return false
  let score = 0
  for (const marker of GENERIC_DESCRIPTION_MARKERS) {
    if (normalized.includes(marker)) score += 1
  }
  return score >= 2
}

function isResourceDetailPath(urlLike) {
  const pathValue = normalizePathname(urlLike)
  return /^\/ressources-gratuites\/(cours|syntheses|exercices)\/[a-z0-9-]+\/(college|lycee|prepa)\/[a-z0-9-]+\/[a-z0-9-]+-\d+$/i.test(pathValue)
}

async function validateUrlWithPlaywright(browser, { expectedCanonicalUrl, navigationUrl }) {
  const expectedUrl = normalizeAbsoluteUrl(expectedCanonicalUrl, expectedCanonicalUrl)
  const targetUrl = normalizeAbsoluteUrl(navigationUrl || expectedCanonicalUrl, navigationUrl || expectedCanonicalUrl)
  if (!expectedUrl) {
    return {
      url: String(expectedCanonicalUrl || ''),
      ok: false,
      reason: 'invalid-url',
      status: null,
      canonical: '',
      robots: '',
      navigationUrl: targetUrl || String(navigationUrl || '')
    }
  }

  const context = await browser.newContext()
  const page = await context.newPage()

  try {
    const response = await page.goto(targetUrl, {
      waitUntil: 'domcontentloaded',
      timeout: NAVIGATION_TIMEOUT_MS
    })

    const status = response ? response.status() : null
    await page.waitForLoadState('networkidle', { timeout: NETWORK_IDLE_TIMEOUT_MS })

    const canonicalHref = await page.locator('link[rel="canonical"]').first().getAttribute('href')
    const canonicalUrl = normalizeAbsoluteUrl(canonicalHref, page.url())
    const robots = String(await page.locator('meta[name="robots"]').first().getAttribute('content') || '')
    const title = normalizeWhitespace(await page.title())
    const description = normalizeWhitespace(
      String(await page.locator('meta[name="description"]').first().getAttribute('content') || '')
    )

    if (status !== 200) {
      return {
        url: expectedUrl,
        ok: false,
        reason: 'status-not-200',
        status,
        canonical: canonicalUrl,
        robots,
        title,
        description,
        navigationUrl: targetUrl
      }
    }

    if (!canonicalUrl || canonicalUrl !== expectedUrl) {
      return {
        url: expectedUrl,
        ok: false,
        reason: 'canonical-mismatch',
        status,
        canonical: canonicalUrl,
        robots,
        title,
        description,
        navigationUrl: targetUrl
      }
    }

    if (/\bnoindex\b/i.test(robots)) {
      return {
        url: expectedUrl,
        ok: false,
        reason: 'robots-noindex',
        status,
        canonical: canonicalUrl,
        robots,
        title,
        description,
        navigationUrl: targetUrl
      }
    }

    if (!description) {
      return {
        url: expectedUrl,
        ok: false,
        reason: 'missing-description',
        status,
        canonical: canonicalUrl,
        robots,
        title,
        description,
        navigationUrl: targetUrl
      }
    }

    if (description.length < MIN_DESCRIPTION_LENGTH) {
      return {
        url: expectedUrl,
        ok: false,
        reason: 'description-too-short',
        status,
        canonical: canonicalUrl,
        robots,
        title,
        description,
        navigationUrl: targetUrl
      }
    }

    if (description.length > MAX_DESCRIPTION_LENGTH) {
      return {
        url: expectedUrl,
        ok: false,
        reason: 'description-too-long',
        status,
        canonical: canonicalUrl,
        robots,
        title,
        description,
        navigationUrl: targetUrl
      }
    }

    if (isResourceDetailPath(expectedUrl) && looksGenericDescription(description)) {
      return {
        url: expectedUrl,
        ok: false,
        reason: 'generic-description',
        status,
        canonical: canonicalUrl,
        robots,
        title,
        description,
        navigationUrl: targetUrl
      }
    }

    return {
      url: expectedUrl,
      ok: true,
      reason: '',
      status,
      canonical: canonicalUrl,
      robots,
      title,
      description,
      navigationUrl: targetUrl
    }
  } catch (error) {
    return {
      url: expectedUrl,
      ok: false,
      reason: 'playwright-error',
      status: null,
      canonical: '',
      robots: '',
      title: '',
      description: '',
      navigationUrl: targetUrl,
      error: error instanceof Error ? error.message : String(error)
    }
  } finally {
    await context.close()
  }
}

async function mapWithConcurrency(items, mapper, limit) {
  if (!Array.isArray(items) || items.length === 0) return []

  const results = new Array(items.length)
  let index = 0

  async function worker() {
    while (index < items.length) {
      const current = index
      index += 1
      results[current] = await mapper(items[current], current)
    }
  }

  const workerCount = Math.max(1, Math.min(limit, items.length))
  await Promise.all(Array.from({ length: workerCount }, () => worker()))
  return results
}

async function run() {
  const options = parseCliArgs(process.argv.slice(2))
  const xml = await fs.readFile(options.sitemapPath, 'utf8')
  const urls = extractLocsFromSitemapXml(xml)

  if (urls.length === 0) {
    throw new Error(`No <loc> entries found in ${options.sitemapPath}`)
  }

  const sample = pickRandomItems(urls, options.sampleSize)
  console.log(
    `[sitemap-check] urls=${urls.length} sample=${sample.length} concurrency=${options.concurrency} site=${options.siteOrigin || 'canonical'}`
  )

  const { chromium } = await loadPlaywright()
  const browser = await chromium.launch({ headless: true })

  try {
    const results = await mapWithConcurrency(
      sample,
      (entryUrl) =>
        validateUrlWithPlaywright(browser, {
          expectedCanonicalUrl: entryUrl,
          navigationUrl: toNavigationUrl(entryUrl, options.siteOrigin)
        }),
      options.concurrency
    )

    const failures = results.filter((entry) => !entry.ok)
    if (failures.length > 0) {
      console.error(`[sitemap-check] FAILED ${failures.length}/${sample.length}`)
      for (const failure of failures) {
        console.error(`- ${failure.url}`)
        console.error(`  navigated=${failure.navigationUrl || 'n/a'}`)
        console.error(`  reason=${failure.reason}`)
        console.error(`  status=${failure.status ?? 'n/a'}`)
        console.error(`  canonical=${failure.canonical || 'n/a'}`)
        console.error(`  robots=${failure.robots || 'n/a'}`)
        console.error(`  title=${failure.title || 'n/a'}`)
        console.error(`  description=${failure.description || 'n/a'}`)
        if (failure.error) {
          console.error(`  error=${failure.error}`)
        }
      }
      process.exit(1)
    }

    console.log(`[sitemap-check] PASS ${sample.length}/${sample.length}`)
  } finally {
    await browser.close()
  }
}

run().catch((error) => {
  console.error('[sitemap-check] fatal:', error instanceof Error ? error.message : String(error))
  process.exit(1)
})
