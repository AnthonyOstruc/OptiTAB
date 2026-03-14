import fs from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const STATIC_INDEXABLE_PATHS = new Set([
  '/',
  '/tarifs',
  '/cours-particuliers',
  '/about',
  '/contact',
  '/ressources-gratuites',
  '/ressources-gratuites/cours',
  '/ressources-gratuites/exercices',
  '/ressources-gratuites/syntheses'
])

const GROUPED_COURSE_PATH_RE = /^\/ressources-gratuites\/cours\/[a-z0-9-]+\/(college|lycee|prepa)\/[a-z0-9-]+\/[a-z0-9-]+-\d+$/i
const GROUPED_SUMMARY_PATH_RE = /^\/ressources-gratuites\/syntheses\/[a-z0-9-]+\/(college|lycee|prepa)\/[a-z0-9-]+\/[a-z0-9-]+-\d+$/i
const GROUPED_EXERCISE_CHAPTER_PATH_RE = /^\/ressources-gratuites\/exercices\/[a-z0-9-]+\/(college|lycee|prepa)\/[a-z0-9-]+\/[a-z0-9-]+-\d+$/i
const EXERCISE_DETAIL_PATH_RE = /^\/ressources-gratuites\/exercices\/exercice-gratuit-[a-z0-9-]+$/i

const HTML_FETCH_ACCEPT = 'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8'
const HTML_FETCH_TIMEOUT_MS = 15000
const API_FETCH_TIMEOUT_MS = Number.parseInt(
  String(process.env.SITEMAP_API_TIMEOUT_MS || '45000'),
  10
)
const API_PAGE_SIZE = Number.parseInt(
  String(process.env.SITEMAP_API_PAGE_SIZE || '100'),
  10
)
const API_FETCH_MAX_RETRIES = Number.parseInt(
  String(process.env.SITEMAP_API_RETRIES || '2'),
  10
)
const API_FETCH_RETRY_BASE_DELAY_MS = Number.parseInt(
  String(process.env.SITEMAP_API_RETRY_BASE_DELAY_MS || '500'),
  10
)
const SHOULD_VALIDATE_MERGE = String(process.env.VALIDATE_MERGE || '').trim() === '1'
const CANONICAL_SITE_ORIGIN = 'https://www.optitab.net'
const CANONICAL_SITE_HOSTS = new Set(['optitab.net', 'www.optitab.net'])

function normalizeSiteUrl(raw, { forceCanonicalHost = false } = {}) {
  const value = String(raw || '').trim()
  if (!value) return ''
  try {
    const url = new URL(value)
    const hostname = String(url.hostname || '').toLowerCase()
    if (forceCanonicalHost && CANONICAL_SITE_HOSTS.has(hostname)) {
      return CANONICAL_SITE_ORIGIN
    }
    const origin = String(url.origin || '').replace(/\/+$/, '')
    const pathname = String(url.pathname || '').replace(/\/+$/, '')
    if (!pathname || pathname === '/') return origin
    return `${origin}${pathname}`
  } catch {
    return value.replace(/\/+$/, '')
  }
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
    const url = new URL(String(rawUrl || ''), String(baseUrl || CANONICAL_SITE_ORIGIN))
    url.hash = ''
    url.search = ''
    url.pathname = normalizePathname(url.pathname)
    const hostname = String(url.hostname || '').toLowerCase()
    const origin = CANONICAL_SITE_HOSTS.has(hostname) ? CANONICAL_SITE_ORIGIN : url.origin
    return `${origin}${url.pathname}`
  } catch {
    return ''
  }
}

function isCanonicalIndexablePath(pathname) {
  const normalized = normalizePathname(pathname)
  if (!normalized) return false
  if (STATIC_INDEXABLE_PATHS.has(normalized)) return true
  if (GROUPED_COURSE_PATH_RE.test(normalized)) return true
  if (GROUPED_SUMMARY_PATH_RE.test(normalized)) return true
  if (GROUPED_EXERCISE_CHAPTER_PATH_RE.test(normalized)) return true
  if (EXERCISE_DETAIL_PATH_RE.test(normalized)) return true
  return false
}

function escapeXml(value) {
  return String(value || '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&apos;')
}

function joinUrl(base, pathname) {
  const b = normalizeSiteUrl(base)
  const p = normalizePathname(pathname)
  if (!b) return p
  if (!p) return b
  if (p.startsWith('/')) return `${b}${p}`
  return `${b}/${p}`
}

function toLastMod(value) {
  if (!value) return ''
  try {
    const date = new Date(value)
    if (Number.isNaN(date.getTime())) return ''
    return date.toISOString().slice(0, 10)
  } catch {
    return ''
  }
}

function slugifyText(value) {
  return String(value || '')
    .normalize('NFD')
    .replace(/\p{Diacritic}/gu, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
}

function formatPaysSlug(value) {
  return slugifyText(value || '')
}

function formatMatiereSlug(value) {
  const normalized = slugifyText(value || '')
  if (!normalized) return ''
  if (normalized.includes('math')) return 'maths'
  return normalized
}

function formatNiveauGroupSlug(value) {
  const normalized = slugifyText(value || '')
  if (!normalized) return ''
  if (normalized.includes('bases-methodes')) {
    return 'lycee'
  }
  if (
    normalized.includes('lycee') ||
    normalized.includes('terminale') ||
    normalized.includes('terminal') ||
    normalized.includes('premiere') ||
    normalized.includes('1ere') ||
    normalized.includes('1re') ||
    normalized.includes('seconde') ||
    normalized.includes('2nde') ||
    normalized.includes('2de') ||
    normalized.includes('bac')
  ) {
    return 'lycee'
  }
  if (
    normalized.includes('college') ||
    normalized.includes('3e') ||
    normalized.includes('4e') ||
    normalized.includes('5e') ||
    normalized.includes('6e') ||
    normalized.includes('brevet')
  ) {
    return 'college'
  }
  if (
    normalized.includes('prepa') ||
    normalized.includes('mpsi') ||
    normalized.includes('mp2i') ||
    normalized.includes('pcsi') ||
    normalized.includes('psi') ||
    normalized.includes('mp') ||
    normalized.includes('ecole') ||
    normalized.includes('grandes-ecoles')
  ) {
    return 'prepa'
  }
  return ''
}

function formatNiveauSlug(value) {
  if (!value) return ''
  const normalized = slugifyText(value)
  if (!normalized) return ''
  if (normalized.includes('terminale') || normalized.includes('terminal')) {
    return 'terminal-bac'
  }
  if (normalized.includes('premiere') || normalized.includes('1ere') || normalized.includes('1re')) {
    return 'premiere-1er'
  }
  if (normalized.includes('seconde') || normalized.includes('2nde') || normalized.includes('2de')) {
    return 'seconde'
  }
  return normalized
}

function buildCoursePathSlug({ niveauNom, titre } = {}) {
  const levelSlug = formatNiveauSlug(niveauNom || '')
  const titleSlug = slugifyText(titre || '')
  if (!levelSlug) return titleSlug
  if (!titleSlug) return levelSlug
  if (titleSlug === levelSlug || titleSlug.startsWith(`${levelSlug}-`)) return titleSlug
  return `${levelSlug}-${titleSlug}`
}

function buildCourseRouteParams({ paysNom, matiereNom, niveauNom, titre, id } = {}) {
  const paysSlug = formatPaysSlug(paysNom || '')
  const matiereSlug = formatMatiereSlug(matiereNom || '')
  const niveauGroupSlug = formatNiveauGroupSlug(niveauNom || '')
  const slug = buildCoursePathSlug({ niveauNom, titre })
  const safeId = id != null ? String(id) : ''
  if (!paysSlug || !matiereSlug || !slug || !safeId) return null
  return { pays: paysSlug, niveauGroup: niveauGroupSlug, matiere: matiereSlug, slug, id: safeId }
}

function buildSummaryRouteParams({ paysNom, matiereNom, niveauNom, titre, id } = {}) {
  return buildCourseRouteParams({ paysNom, matiereNom, niveauNom, titre, id })
}

function buildExerciseChapterSlug({ niveauNom, niveau, name, title, notionNom } = {}) {
  const levelSlug = formatNiveauSlug(niveauNom || niveau || '')
  const chapterSlug = slugifyText(name || title || notionNom || '')
  return [levelSlug, chapterSlug].filter(Boolean).join('-')
}

const DEFAULT_PAYS_SLUG = 'france'
const DEFAULT_MATIERE_SLUG = 'maths'

function buildExerciseChapterRouteParams({ paysNom, matiereNom, niveauNom, niveauGroup, name, title, notionNom, id } = {}) {
  const paysSlug = formatPaysSlug(paysNom || '') || DEFAULT_PAYS_SLUG
  const matiereSlug = formatMatiereSlug(matiereNom || '') || DEFAULT_MATIERE_SLUG
  const niveauGroupSlug = formatNiveauGroupSlug(niveauGroup || niveauNom || '')
  const slug = buildExerciseChapterSlug({ niveauNom, name, title, notionNom })
  const safeId = id != null ? String(id) : ''
  if (!slug || !safeId) return null
  return { pays: paysSlug, niveauGroup: niveauGroupSlug, matiere: matiereSlug, slug, id: safeId }
}

function throwMissingNiveauGroupError({ resourceType, resourceId, niveauNom, source, rawSlug } = {}) {
  const message = [
    '[sitemap] Missing canonical niveauGroup mapping.',
    `type=${String(resourceType || 'unknown')}`,
    `id=${String(resourceId || 'unknown')}`,
    `niveau="${String(niveauNom || '').trim()}"`,
    `source=${String(source || 'unknown')}`,
    `slug=${String(rawSlug || '').trim()}`
  ].join(' ')
  const error = new Error(message)
  error.code = 'MISSING_NIVEAU_GROUP'
  throw error
}

async function fetchAllPages(url) {
  const items = []
  let nextUrl = url
  let guard = 0
  const retryLimit = Number.isFinite(API_FETCH_MAX_RETRIES) && API_FETCH_MAX_RETRIES >= 0
    ? API_FETCH_MAX_RETRIES
    : 2
  const retryBaseDelayMs = Number.isFinite(API_FETCH_RETRY_BASE_DELAY_MS) && API_FETCH_RETRY_BASE_DELAY_MS > 0
    ? API_FETCH_RETRY_BASE_DELAY_MS
    : 500

  while (nextUrl && guard < 50) {
    guard += 1
    let res
    let attempt = 0

    while (true) {
      const controller = new AbortController()
      const timeout = setTimeout(() => controller.abort(), Number.isFinite(API_FETCH_TIMEOUT_MS) ? API_FETCH_TIMEOUT_MS : 45000)
      try {
        res = await fetch(nextUrl, {
          headers: { Accept: 'application/json' },
          signal: controller.signal
        })
      } catch (error) {
        if (attempt < retryLimit && isRetryableFetchError(error)) {
          attempt += 1
          await delay(retryBaseDelayMs * attempt)
          continue
        }
        throw error
      } finally {
        clearTimeout(timeout)
      }

      if (!res.ok && attempt < retryLimit && isRetryableStatus(res.status)) {
        attempt += 1
        await delay(retryBaseDelayMs * attempt)
        continue
      }

      break
    }

    if (!res.ok) {
      throw new Error(`HTTP ${res.status} for ${nextUrl}`)
    }
    const data = await res.json()
    const pageItems = Array.isArray(data?.results) ? data.results : (Array.isArray(data) ? data : [])
    items.push(...pageItems)
    nextUrl = data?.next || null
  }

  return items
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

function isRetryableStatus(status) {
  return status === 429 || status >= 500
}

function isRetryableFetchError(error) {
  if (!error) return false
  if (error?.name === 'AbortError') return true
  return error instanceof TypeError
}

function routeForResource(resource) {
  const type = String(resource?.resource_type || resource?.type || resource?.resourceType || '').toLowerCase()
  if (!type) return null

  if (type === 'course') {
    const params = buildCourseRouteParams({
      paysNom: resource?.pays_nom,
      matiereNom: resource?.matiere_nom || resource?.matiere,
      niveauNom: resource?.niveau_nom,
      titre: resource?.titre,
      id: resource?.id
    })
    if (!params?.slug || !params?.id) return null
    if (!params?.niveauGroup) {
      throwMissingNiveauGroupError({
        resourceType: 'course',
        resourceId: resource?.id,
        niveauNom: resource?.niveau_nom,
        source: 'routeForResource',
        rawSlug: resource?.slug
      })
    }
    return `/ressources-gratuites/cours/${params.pays}/${params.niveauGroup}/${params.matiere}/${params.slug}-${params.id}`
  }

  if (type === 'summary') {
    const params = buildSummaryRouteParams({
      paysNom: resource?.pays_nom,
      matiereNom: resource?.matiere_nom || resource?.matiere,
      niveauNom: resource?.niveau_nom,
      titre: resource?.titre,
      id: resource?.id
    })
    if (!params?.slug || !params?.id) return null
    if (!params?.niveauGroup) {
      throwMissingNiveauGroupError({
        resourceType: 'summary',
        resourceId: resource?.id,
        niveauNom: resource?.niveau_nom,
        source: 'routeForResource',
        rawSlug: resource?.slug
      })
    }
    return `/ressources-gratuites/syntheses/${params.pays}/${params.niveauGroup}/${params.matiere}/${params.slug}-${params.id}`
  }

  if (type === 'exercise') {
    const slug = String(resource?.slug || '').trim().replace(/^\/+|\/+$/g, '')
    if (!slug || slug.includes('/')) return null
    return `/ressources-gratuites/exercices/${slug}`
  }

  return null
}

function routeForExerciseChapter(resource) {
  const params = buildExerciseChapterRouteParams({
    paysNom: resource?.pays_nom,
    matiereNom: resource?.matiere_nom || resource?.matiere,
    niveauNom: resource?.niveau_nom,
    niveauGroup: resource?.niveau_group || resource?.niveauGroup,
    name: resource?.notion_nom || resource?.name || resource?.titre,
    id: resource?.notion || resource?.id
  })
  if (!params?.slug || !params?.id) return null
  if (!params?.niveauGroup) {
    throwMissingNiveauGroupError({
      resourceType: 'exercise_chapter',
      resourceId: resource?.notion || resource?.id,
      niveauNom: resource?.niveau_nom,
      source: 'routeForExerciseChapter',
      rawSlug: resource?.slug
    })
  }
  return `/ressources-gratuites/exercices/${params.pays}/${params.niveauGroup}/${params.matiere}/${params.slug}-${params.id}`
}

function extractPathname(loc) {
  try {
    const url = new URL(String(loc || ''), 'https://www.optitab.net')
    return normalizePathname(url.pathname || '/')
  } catch {
    return normalizePathname(loc)
  }
}

function extractCanonicalHrefFromHtml(html) {
  const source = String(html || '')
  const byRelThenHref = source.match(/<link\b[^>]*\brel=["'][^"']*\bcanonical\b[^"']*["'][^>]*\bhref=["']([^"']+)["'][^>]*>/i)
  if (byRelThenHref?.[1]) return byRelThenHref[1]
  const byHrefThenRel = source.match(/<link\b[^>]*\bhref=["']([^"']+)["'][^>]*\brel=["'][^"']*\bcanonical\b[^"']*["'][^>]*>/i)
  if (byHrefThenRel?.[1]) return byHrefThenRel[1]
  return ''
}

function extractRobotsContentFromHtml(html) {
  const source = String(html || '')
  const byNameThenContent = source.match(/<meta\b[^>]*\bname=["']robots["'][^>]*\bcontent=["']([^"']*)["'][^>]*>/i)
  if (byNameThenContent?.[1]) return byNameThenContent[1]
  const byContentThenName = source.match(/<meta\b[^>]*\bcontent=["']([^"']*)["'][^>]*\bname=["']robots["'][^>]*>/i)
  if (byContentThenName?.[1]) return byContentThenName[1]
  return ''
}

function hasNoIndexRobots(robotsContent) {
  return /\bnoindex\b/i.test(String(robotsContent || ''))
}

async function fetchHtml(url) {
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), HTML_FETCH_TIMEOUT_MS)
  try {
    return await fetch(url, {
      redirect: 'follow',
      signal: controller.signal,
      headers: { Accept: HTML_FETCH_ACCEPT }
    })
  } finally {
    clearTimeout(timeout)
  }
}

async function isIndexableSelfCanonicalUrl(url, siteUrl) {
  const expectedUrl = normalizeAbsoluteUrl(url, siteUrl)
  if (!expectedUrl) return false

  try {
    const response = await fetchHtml(expectedUrl)
    if (response.status !== 200) return false

    const html = await response.text()
    const canonicalHref = extractCanonicalHrefFromHtml(html)
    const canonicalUrl = normalizeAbsoluteUrl(canonicalHref, expectedUrl)
    if (!canonicalUrl || canonicalUrl !== expectedUrl) return false

    const robotsContent = extractRobotsContentFromHtml(html)
    if (hasNoIndexRobots(robotsContent)) return false

    return true
  } catch {
    return false
  }
}

async function mergeExistingSitemap(outPath, addUrl, { siteUrl } = {}) {
  try {
    const xml = await fs.readFile(outPath, 'utf8')
    const urlBlocks = xml.match(/<url>[\s\S]*?<\/url>/g) || []

    let kept = 0
    let skipped = 0

    for (const block of urlBlocks) {
      const locMatch = block.match(/<loc>(.*?)<\/loc>/)
      if (!locMatch) continue

      const pathname = extractPathname(locMatch[1])
      if (!isCanonicalIndexablePath(pathname)) continue

      if (SHOULD_VALIDATE_MERGE) {
        const url = joinUrl(siteUrl, pathname)
        const isValid = await isIndexableSelfCanonicalUrl(url, siteUrl)
        if (!isValid) {
          skipped += 1
          continue
        }
      }

      const lastmodMatch = block.match(/<lastmod>(.*?)<\/lastmod>/)
      const lastmod = lastmodMatch ? String(lastmodMatch[1]).trim() : ''
      addUrl(pathname, lastmod)
      kept += 1
    }

    if (SHOULD_VALIDATE_MERGE) {
      console.warn(`[sitemap] merged ${kept} validated URLs from previous sitemap (skipped ${skipped})`)
    } else {
      console.warn(`[sitemap] merged ${kept} canonical-pattern URLs from previous sitemap (VALIDATE_MERGE=0)`)
    }
    return true
  } catch {
    return false
  }
}

async function buildSitemap() {
  const siteUrl =
    normalizeSiteUrl(
      process.env.VITE_SITE_URL ||
      process.env.SITE_URL ||
      process.env.PUBLIC_SITE_URL ||
      'https://www.optitab.net',
      { forceCanonicalHost: true }
    ) || CANONICAL_SITE_ORIGIN

  const apiBase = normalizeSiteUrl(
    process.env.VITE_API_BASE_URL ||
    process.env.VITE_API_URL ||
    'https://optitab-backend.onrender.com'
  )
  const pageSize = Number.isFinite(API_PAGE_SIZE) && API_PAGE_SIZE > 0 ? API_PAGE_SIZE : 100

  const outPath = path.resolve(__dirname, '..', 'public', 'sitemap.xml')

  const urls = new Map()
  const addUrl = (pathname, lastmod = '') => {
    const normalizedPath = normalizePathname(pathname)
    if (!isCanonicalIndexablePath(normalizedPath)) return

    const loc = normalizeAbsoluteUrl(joinUrl(siteUrl, normalizedPath), siteUrl)
    if (!loc) return

    const key = loc.toLowerCase()
    const existing = urls.get(key)
    if (!existing) {
      urls.set(key, { loc, lastmod })
      return
    }
    if (lastmod && (!existing.lastmod || lastmod > existing.lastmod)) {
      urls.set(key, { loc, lastmod })
    }
  }

  for (const staticPath of STATIC_INDEXABLE_PATHS) {
    addUrl(staticPath, '')
  }

  try {
    const baseEndpoint = `${apiBase}/api/free/learning-resources/`

    // 1) Curated resources
    const generic = await fetchAllPages(`${baseEndpoint}?page_size=${pageSize}&light=1`)
    for (const item of generic) {
      if (item?.is_locked === true) continue
      const pathForItem = routeForResource(item)
      if (!pathForItem) continue
      addUrl(pathForItem, toLastMod(item?.date_modification))
    }

    // 2) Typed resources (course, summary, exercise detail)
    for (const type of ['course', 'summary', 'exercise']) {
      const items = await fetchAllPages(
        `${baseEndpoint}?type=${encodeURIComponent(type)}&page_size=${pageSize}&light=1`
      )
      for (const item of items) {
        if (item?.is_locked === true) continue
        const pathForItem = routeForResource({ ...item, resource_type: type })
        if (!pathForItem) continue
        addUrl(pathForItem, toLastMod(item?.date_modification))
      }
    }

    // 3) Exercise chapter pages (grouped canonical shape only)
    const chapterItems = await fetchAllPages(
      `${baseEndpoint}?type=exercise&group_by=notion&page_size=${pageSize}&light=1`
    )
    for (const item of chapterItems) {
      const pathForChapter = routeForExerciseChapter(item)
      if (!pathForChapter) continue
      addUrl(pathForChapter, toLastMod(item?.date_modification))
    }
  } catch (err) {
    if (err?.code === 'MISSING_NIVEAU_GROUP') {
      console.error('[sitemap] hard failure: unresolved niveauGroup mapping in canonical routes.')
      throw err
    }
    // Never fail the build if the API is unreachable.
    // Keep static URLs and only merge previous entries that are still indexable+self-canonical.
    console.warn('[sitemap] API fetch failed, attempting merge from existing sitemap:', err?.message || err)
    const merged = await mergeExistingSitemap(outPath, addUrl, { siteUrl })
    if (!merged) {
      console.warn('[sitemap] No existing sitemap to merge; generating static-only sitemap.')
    }
  }

  const entries = [...urls.values()].sort((a, b) => a.loc.localeCompare(b.loc, 'fr'))
  const lines = []
  lines.push('<?xml version="1.0" encoding="UTF-8"?>')
  lines.push('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
  for (const { loc, lastmod } of entries) {
    lines.push('  <url>')
    lines.push(`    <loc>${escapeXml(loc)}</loc>`)
    if (lastmod) {
      lines.push(`    <lastmod>${escapeXml(lastmod)}</lastmod>`)
    }
    lines.push('  </url>')
  }
  lines.push('</urlset>')

  await fs.writeFile(outPath, `${lines.join('\n')}\n`, 'utf8')
  console.log(`[sitemap] wrote ${entries.length} urls to ${outPath}`)
}

await buildSitemap()
