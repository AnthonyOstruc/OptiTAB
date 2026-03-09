import fs from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const CANONICAL_SITE_ORIGIN = 'https://www.optitab.net'
const DEFAULT_API_BASE = 'https://optitab-backend.onrender.com'
const RENDER_YAML_PATH = path.resolve(__dirname, '..', '..', 'render.yaml')
const OUTPUT_JSON_PATH = path.resolve(__dirname, '..', 'generated', 'render-legacy-redirects.json')
const START_MARKER = '      # BEGIN GENERATED LEGACY REDIRECTS'
const END_MARKER = '      # END GENERATED LEGACY REDIRECTS'
const STRICT_MODE = String(process.env.RENDER_ROUTES_STRICT || '').trim() === '1'
const API_FETCH_TIMEOUT_MS = Number.parseInt(
  String(process.env.RENDER_ROUTES_API_TIMEOUT_MS || '15000'),
  10
)
const API_PAGE_SIZE = Number.parseInt(
  String(process.env.RENDER_ROUTES_API_PAGE_SIZE || '100'),
  10
)
const KNOWN_404_POPULAR_LINK_PATHS = [
  '/ressources-gratuites/exercices/exercice-gratuit-1058-france-1ere-mathematiques-boucles-for-avec-range-exercices-de-base'
]

function slugifyText(value) {
  return String(value || '')
    .normalize('NFD')
    .replace(/\p{Diacritic}/gu, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
}

function formatNiveauSlug(value) {
  if (!value) return ''
  const normalized = slugifyText(value)
  if (!normalized) return ''
  if (normalized.includes('terminale') || normalized.includes('terminal')) return 'terminal-bac'
  if (normalized.includes('premiere') || normalized.includes('1ere') || normalized.includes('1re')) return 'premiere-1er'
  if (normalized.includes('seconde') || normalized.includes('2nde') || normalized.includes('2de')) return 'seconde'
  return normalized
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
  if (normalized.includes('bases-methodes')) return 'lycee'
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

function buildExerciseChapterRouteParams({ paysNom, matiereNom, niveauNom, niveauGroup, name, title, notionNom, id } = {}) {
  const paysSlug = formatPaysSlug(paysNom || '') || 'france'
  const matiereSlug = formatMatiereSlug(matiereNom || '') || 'maths'
  const niveauGroupSlug = formatNiveauGroupSlug(niveauGroup || niveauNom || '')
  const slug = buildExerciseChapterSlug({ niveauNom, name, title, notionNom })
  const safeId = id != null ? String(id) : ''
  if (!slug || !safeId) return null
  return { pays: paysSlug, niveauGroup: niveauGroupSlug, matiere: matiereSlug, slug, id: safeId }
}

function normalizeSiteUrl(raw) {
  const value = String(raw || '').trim()
  if (!value) return ''
  try {
    const url = new URL(value)
    return String(url.origin || '').replace(/\/+$/, '')
  } catch {
    return value.replace(/\/+$/, '')
  }
}

function normalizePath(pathLike) {
  const raw = String(pathLike || '').trim()
  if (!raw) return '/'

  try {
    const url = new URL(raw, CANONICAL_SITE_ORIGIN)
    let pathname = url.pathname || '/'
    if (!pathname.startsWith('/')) pathname = `/${pathname}`
    if (pathname.length > 1) pathname = pathname.replace(/\/+$/, '')
    return pathname || '/'
  } catch {
    let pathname = raw
    if (!pathname.startsWith('/')) pathname = `/${pathname}`
    if (pathname.length > 1) pathname = pathname.replace(/\/+$/, '')
    return pathname || '/'
  }
}

function sanitizeSlug(value) {
  const slug = String(value || '').trim().replace(/^\/+|\/+$/g, '')
  if (!slug) return ''
  if (slug.includes('/')) return ''
  return slug
}

function buildCourseCanonicalPath(item) {
  const params = buildCourseRouteParams({
    paysNom: item?.pays_nom,
    matiereNom: item?.matiere_nom || item?.matiere,
    niveauNom: item?.niveau_nom,
    titre: item?.titre,
    id: item?.id
  })
  if (!params?.pays || !params?.matiere || !params?.slug || !params?.id || !params?.niveauGroup) return null
  return {
    canonicalPath: `/ressources-gratuites/cours/${params.pays}/${params.niveauGroup}/${params.matiere}/${params.slug}-${params.id}`,
    ungroupedPath: `/ressources-gratuites/cours/${params.pays}/${params.matiere}/${params.slug}-${params.id}`
  }
}

function buildSummaryCanonicalPath(item) {
  const params = buildSummaryRouteParams({
    paysNom: item?.pays_nom,
    matiereNom: item?.matiere_nom || item?.matiere,
    niveauNom: item?.niveau_nom,
    titre: item?.titre,
    id: item?.id
  })
  if (!params?.pays || !params?.matiere || !params?.slug || !params?.id || !params?.niveauGroup) return null
  return {
    canonicalPath: `/ressources-gratuites/syntheses/${params.pays}/${params.niveauGroup}/${params.matiere}/${params.slug}-${params.id}`,
    ungroupedPath: `/ressources-gratuites/syntheses/${params.pays}/${params.matiere}/${params.slug}-${params.id}`
  }
}

function buildExerciseChapterCanonicalPath(item) {
  const params = buildExerciseChapterRouteParams({
    paysNom: item?.pays_nom,
    matiereNom: item?.matiere_nom || item?.matiere,
    niveauNom: item?.niveau_nom,
    niveauGroup: item?.niveau_group || item?.niveauGroup || item?.niveau_nom,
    name: item?.notion_nom || item?.name || item?.titre,
    id: item?.notion || item?.id
  })
  if (!params?.pays || !params?.matiere || !params?.slug || !params?.id || !params?.niveauGroup) return null
  return {
    canonicalPath: `/ressources-gratuites/exercices/${params.pays}/${params.niveauGroup}/${params.matiere}/${params.slug}-${params.id}`,
    slugOnlyPath: `/ressources-gratuites/exercices/${params.slug}`,
    paysOnlyPath: `/ressources-gratuites/exercices/${params.pays}/${params.slug}-${params.id}`,
    paysMatierePath: `/ressources-gratuites/exercices/${params.pays}/${params.matiere}/${params.slug}-${params.id}`,
    params
  }
}

function toLegacyExerciseSlugVariant(slug) {
  const value = sanitizeSlug(slug)
  if (!value) return ''
  if (value === 'terminal-bac') return 'terminale-bac'
  if (value.startsWith('terminal-bac-')) {
    return value.replace(/^terminal-bac-/, 'terminale-bac-')
  }
  if (value === 'premiere-1er') return 'premiere-bac'
  if (value.startsWith('premiere-1er-')) {
    return value.replace(/^premiere-1er-/, 'premiere-bac-')
  }
  return ''
}

async function fetchAllPages(url) {
  const items = []
  let nextUrl = url
  let guard = 0

  while (nextUrl && guard < 100) {
    guard += 1
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), Number.isFinite(API_FETCH_TIMEOUT_MS) ? API_FETCH_TIMEOUT_MS : 15000)
    let response
    try {
      response = await fetch(nextUrl, {
        headers: { Accept: 'application/json' },
        signal: controller.signal
      })
    } finally {
      clearTimeout(timeout)
    }
    if (!response.ok) {
      throw new Error(`HTTP ${response.status} while fetching ${nextUrl}`)
    }
    const data = await response.json()
    const pageItems = Array.isArray(data?.results) ? data.results : (Array.isArray(data) ? data : [])
    items.push(...pageItems)
    nextUrl = data?.next || null
  }

  return items
}

function renderYamlRedirectEntry({ source, destination }) {
  return [
    '      - type: redirect',
    `        source: ${source}`,
    `        destination: ${destination}`,
    '        status: 301'
  ].join('\n')
}

function applyGeneratedBlock(renderYamlContent, redirectEntries) {
  const startIndex = renderYamlContent.indexOf(START_MARKER)
  const endIndex = renderYamlContent.indexOf(END_MARKER)
  if (startIndex === -1 || endIndex === -1 || endIndex <= startIndex) {
    throw new Error(`Unable to find route markers in ${RENDER_YAML_PATH}`)
  }

  const eol = renderYamlContent.includes('\r\n') ? '\r\n' : '\n'
  const before = renderYamlContent.slice(0, startIndex + START_MARKER.length)
  const after = renderYamlContent.slice(endIndex)

  const blockLines = []
  if (redirectEntries.length === 0) {
    blockLines.push('      # (no generated redirects)')
  } else {
    for (const entry of redirectEntries) {
      blockLines.push(renderYamlRedirectEntry(entry))
    }
  }

  return `${before}${eol}${blockLines.join(eol)}${eol}${after}`
}

async function main() {
  const apiBase = normalizeSiteUrl(process.env.VITE_API_BASE_URL || process.env.API_BASE_URL || DEFAULT_API_BASE)
  if (!apiBase) {
    throw new Error('Missing API base URL for redirect generation')
  }
  const pageSize = Number.isFinite(API_PAGE_SIZE) && API_PAGE_SIZE > 0 ? API_PAGE_SIZE : 100

  const redirectsBySource = new Map()
  const addRedirect = (source, destination, reason) => {
    const normalizedSource = normalizePath(source)
    const normalizedDestination = normalizePath(destination)
    if (!normalizedSource || !normalizedDestination) return
    if (normalizedSource === normalizedDestination) return

    const key = normalizedSource.toLowerCase()
    const existing = redirectsBySource.get(key)
    if (!existing) {
      redirectsBySource.set(key, {
        source: normalizedSource,
        destination: normalizedDestination,
        reason
      })
      return
    }

    if (existing.destination !== normalizedDestination) {
      console.warn(
        `[render-routes] conflicting destination for ${normalizedSource}: ` +
          `${existing.destination} vs ${normalizedDestination} (keeping first)`
      )
    }
  }

  const baseEndpoint = `${apiBase}/api/free/learning-resources/`
  const [courses, summaries, exerciseChapters, exercises] = await Promise.all([
    fetchAllPages(`${baseEndpoint}?type=course&page_size=${pageSize}&light=1`),
    fetchAllPages(`${baseEndpoint}?type=summary&page_size=${pageSize}&light=1`),
    fetchAllPages(`${baseEndpoint}?type=exercise&group_by=notion&page_size=${pageSize}&light=1`),
    fetchAllPages(`${baseEndpoint}?type=exercise&page_size=${pageSize}&light=1`)
  ])

  for (const item of courses) {
    const canonical = buildCourseCanonicalPath(item)
    if (!canonical) continue
    const sourceSlug = sanitizeSlug(item?.slug)
    if (sourceSlug) {
      addRedirect(`/ressources-gratuites/cours/${sourceSlug}`, canonical.canonicalPath, 'course_slug_legacy')
    }
    addRedirect(canonical.ungroupedPath, canonical.canonicalPath, 'course_ungrouped_legacy')
  }

  for (const item of summaries) {
    const canonical = buildSummaryCanonicalPath(item)
    if (!canonical) continue
    const sourceSlug = sanitizeSlug(item?.slug)
    if (sourceSlug) {
      addRedirect(`/ressources-gratuites/syntheses/${sourceSlug}`, canonical.canonicalPath, 'summary_slug_legacy')
    }
    addRedirect(canonical.ungroupedPath, canonical.canonicalPath, 'summary_ungrouped_legacy')
  }

  for (const item of exerciseChapters) {
    const canonical = buildExerciseChapterCanonicalPath(item)
    if (!canonical) continue

    addRedirect(canonical.slugOnlyPath, canonical.canonicalPath, 'exercise_chapter_slug_legacy')
    addRedirect(canonical.paysOnlyPath, canonical.canonicalPath, 'exercise_chapter_pays_legacy')
    addRedirect(canonical.paysMatierePath, canonical.canonicalPath, 'exercise_chapter_pays_matiere_legacy')

    const legacySlug = toLegacyExerciseSlugVariant(canonical.params.slug)
    if (legacySlug && legacySlug !== canonical.params.slug) {
      addRedirect(`/ressources-gratuites/exercices/${legacySlug}`, canonical.canonicalPath, 'exercise_chapter_legacy_slug_variant')
      addRedirect(
        `/ressources-gratuites/exercices/${canonical.params.pays}/${legacySlug}-${canonical.params.id}`,
        canonical.canonicalPath,
        'exercise_chapter_legacy_slug_variant'
      )
      addRedirect(
        `/ressources-gratuites/exercices/${canonical.params.pays}/${canonical.params.matiere}/${legacySlug}-${canonical.params.id}`,
        canonical.canonicalPath,
        'exercise_chapter_legacy_slug_variant'
      )
    }
  }

  const exerciseById = new Map()
  for (const item of exercises) {
    const id = String(item?.id || '').trim()
    const slug = sanitizeSlug(item?.slug)
    if (!id || !slug) continue
    exerciseById.set(id, slug)
  }

  for (const rawPath of KNOWN_404_POPULAR_LINK_PATHS) {
    const sourcePath = normalizePath(rawPath)
    const idMatch = sourcePath.match(/exercice-gratuit-(\d+)/i)
    if (!idMatch) continue
    const canonicalSlug = exerciseById.get(String(idMatch[1]))
    if (!canonicalSlug) continue
    addRedirect(sourcePath, `/ressources-gratuites/exercices/${canonicalSlug}`, 'known_broken_popular_link')
  }

  const redirects = [...redirectsBySource.values()]
    .sort((a, b) => a.source.localeCompare(b.source, 'fr'))
    .map(({ source, destination, reason }) => ({ source, destination, reason }))

  await fs.mkdir(path.dirname(OUTPUT_JSON_PATH), { recursive: true })
  await fs.writeFile(
    OUTPUT_JSON_PATH,
    `${JSON.stringify(
      {
        generatedAt: new Date().toISOString(),
        apiBase,
        count: redirects.length,
        redirects
      },
      null,
      2
    )}\n`,
    'utf8'
  )

  const renderYaml = await fs.readFile(RENDER_YAML_PATH, 'utf8')
  const updatedRenderYaml = applyGeneratedBlock(renderYaml, redirects)
  if (updatedRenderYaml !== renderYaml) {
    await fs.writeFile(RENDER_YAML_PATH, updatedRenderYaml, 'utf8')
  }

  console.log(`[render-routes] wrote ${redirects.length} generated legacy redirects`)
  console.log(`[render-routes] updated ${RENDER_YAML_PATH}`)
  console.log(`[render-routes] wrote ${OUTPUT_JSON_PATH}`)
}

main().catch((error) => {
  const message = error?.message || String(error)
  if (STRICT_MODE) {
    console.error('[render-routes] fatal:', message)
    process.exitCode = 1
    return
  }
  console.warn('[render-routes] warning:', message)
  console.warn('[render-routes] keeping existing render.yaml generated block (set RENDER_ROUTES_STRICT=1 to fail on error)')
})
