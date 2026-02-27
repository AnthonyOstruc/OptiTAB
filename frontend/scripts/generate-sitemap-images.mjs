import fs from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const CANONICAL_SITE_ORIGIN = 'https://www.optitab.net'

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

function normalizePathname(pathname) {
  const raw = String(pathname || '').trim()
  if (!raw) return ''
  let resolved = raw
  try {
    const parsed = new URL(raw, CANONICAL_SITE_ORIGIN)
    resolved = parsed.pathname || '/'
  } catch {
    resolved = raw
  }
  if (!resolved.startsWith('/')) resolved = `/${resolved}`
  const normalized = resolved.replace(/\/+$/, '')
  return normalized || '/'
}

function joinUrl(base, pathname) {
  const b = normalizeSiteUrl(base)
  const p = normalizePathname(pathname)
  if (!b) return p
  return `${b}${p}`
}

function escapeXml(value) {
  return String(value || '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&apos;')
}

function stripUrlTracking(value) {
  const raw = String(value || '').trim()
  if (!raw) return ''
  try {
    const parsed = new URL(raw, CANONICAL_SITE_ORIGIN)
    parsed.hash = ''
    parsed.search = ''
    return parsed.toString()
  } catch {
    return raw
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
    normalized.includes('bac') ||
    normalized.includes('bases-methodes')
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
    normalized.includes('mp')
  ) {
    return 'prepa'
  }
  return ''
}

function formatNiveauSlug(value) {
  const normalized = slugifyText(value || '')
  if (!normalized) return ''
  if (normalized.includes('terminale') || normalized.includes('terminal')) return 'terminal-bac'
  if (normalized.includes('premiere') || normalized.includes('1ere') || normalized.includes('1re')) return 'premiere-1er'
  if (normalized.includes('seconde') || normalized.includes('2nde') || normalized.includes('2de')) return 'seconde'
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

function buildCourseRoutePath(resource) {
  const pays = formatPaysSlug(resource?.pays_nom)
  const matiere = formatMatiereSlug(resource?.matiere_nom || resource?.matiere)
  const niveauGroup = formatNiveauGroupSlug(resource?.niveau_nom)
  const slug = buildCoursePathSlug({
    niveauNom: resource?.niveau_nom,
    titre: resource?.titre
  })
  const id = resource?.id != null ? String(resource.id) : ''

  if (!pays || !matiere || !slug || !id || !niveauGroup) return ''
  return `/ressources-gratuites/cours/${pays}/${niveauGroup}/${matiere}/${slug}-${id}`
}

function buildExerciseRoutePath(resource) {
  const slug = normalizeText(resource?.slug)
  if (!slug) return ''
  return `/ressources-gratuites/exercices/${slug}`
}

function buildSummaryRoutePath(resource) {
  const pays = formatPaysSlug(resource?.pays_nom)
  const matiere = formatMatiereSlug(resource?.matiere_nom || resource?.matiere)
  const niveauGroup = formatNiveauGroupSlug(resource?.niveau_nom)
  const slug = buildCoursePathSlug({
    niveauNom: resource?.niveau_nom,
    titre: resource?.titre
  })
  const id = resource?.id != null ? String(resource.id) : ''

  if (!pays || !matiere || !slug || !id) return ''
  if (niveauGroup) {
    return `/ressources-gratuites/syntheses/${pays}/${niveauGroup}/${matiere}/${slug}-${id}`
  }
  return `/ressources-gratuites/syntheses/${pays}/${matiere}/${slug}-${id}`
}

function normalizeText(value) {
  return String(value || '').replace(/\s+/g, ' ').trim()
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

function resolveImageUrl(rawImageUrl, { apiBase, mediaBase } = {}) {
  const raw = String(rawImageUrl || '').trim()
  if (!raw) return ''

  if (/^https?:\/\//i.test(raw)) {
    return stripUrlTracking(raw)
  }
  if (raw.startsWith('//')) {
    return stripUrlTracking(`https:${raw}`)
  }

  const safeApiBase = normalizeSiteUrl(apiBase)
  const safeMediaBase = normalizeSiteUrl(mediaBase)

  if (raw.startsWith('/media/')) {
    if (safeMediaBase) {
      return stripUrlTracking(`${safeMediaBase}/${raw.replace(/^\/media\//, '')}`)
    }
    return stripUrlTracking(`${safeApiBase}${raw}`)
  }

  if (raw.startsWith('media/')) {
    if (safeMediaBase) {
      return stripUrlTracking(`${safeMediaBase}/${raw.replace(/^media\//, '')}`)
    }
    return stripUrlTracking(`${safeApiBase}/${raw}`)
  }

  if (raw.startsWith('/')) {
    if (safeMediaBase) {
      return stripUrlTracking(`${safeMediaBase}/${raw.replace(/^\/+/, '')}`)
    }
    return stripUrlTracking(`${safeApiBase}${raw}`)
  }

  if (safeMediaBase) {
    return stripUrlTracking(`${safeMediaBase}/${raw}`)
  }

  return stripUrlTracking(`${safeApiBase}/media/${raw}`)
}

function collectImageNodes(resource, { apiBase, mediaBase } = {}) {
  const images = Array.isArray(resource?.images) ? resource.images : []
  return images
    .map((img, index) => {
      const loc = resolveImageUrl(img?.image, { apiBase, mediaBase })
      if (!loc) return null

      const caption = normalizeText(img?.legende || img?.caption || '')
      const title = normalizeText(
        img?.title_text_resolved || img?.title_text || img?.alt_text_resolved || img?.alt_text || caption || `Image ${index + 1}`
      )

      return {
        loc,
        caption: caption || '',
        title: title || ''
      }
    })
    .filter(Boolean)
}

function mergePageImages(entries, pageUrl, imageNodes, lastmod) {
  if (!imageNodes.length) return

  const existing = entries.get(pageUrl)
  if (!existing) {
    entries.set(pageUrl, {
      loc: pageUrl,
      lastmod: lastmod || '',
      images: imageNodes
    })
    return
  }

  const knownLocs = new Set(existing.images.map((img) => img.loc))
  for (const node of imageNodes) {
    if (!knownLocs.has(node.loc)) {
      existing.images.push(node)
    }
  }
  if (lastmod && (!existing.lastmod || lastmod > existing.lastmod)) {
    existing.lastmod = lastmod
  }
}

async function fetchAllPages(url) {
  const items = []
  let nextUrl = url
  let guard = 0

  while (nextUrl && guard < 50) {
    guard += 1
    const res = await fetch(nextUrl, { headers: { Accept: 'application/json' } })
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

async function fetchAllPagesSafe(url, label = 'resource') {
  try {
    return await fetchAllPages(url)
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error)
    console.warn(`[sitemap-images] warning: failed to fetch ${label}: ${message}`)
    return []
  }
}

async function buildImageSitemap() {
  const siteUrl = normalizeSiteUrl(
    process.env.VITE_SITE_URL ||
    process.env.SITE_URL ||
    process.env.PUBLIC_SITE_URL ||
    CANONICAL_SITE_ORIGIN
  ) || CANONICAL_SITE_ORIGIN

  const apiBase = normalizeSiteUrl(
    process.env.VITE_API_BASE_URL ||
    process.env.VITE_API_URL ||
    'https://optitab-backend.onrender.com'
  )

  const mediaBase = normalizeSiteUrl(
    process.env.VITE_S3_MEDIA_URL ||
    process.env.VITE_MEDIA_BASE_URL ||
    ''
  )

  const outPath = path.resolve(__dirname, '..', 'public', 'sitemap-images.xml')
  const [courseResources, exerciseResources, summaryResources, tableResources] = await Promise.all([
    fetchAllPagesSafe(`${apiBase}/api/free/learning-resources/?type=course&page_size=500&include_images=1`, 'courses'),
    fetchAllPagesSafe(`${apiBase}/api/free/learning-resources/?type=exercise&page_size=500&include_images=1`, 'exercises'),
    fetchAllPagesSafe(`${apiBase}/api/free/learning-resources/?type=summary&page_size=500&include_images=1`, 'summaries'),
    fetchAllPagesSafe(`${apiBase}/api/free/learning-resources/?type=table&page_size=500&include_images=1`, 'tables')
  ])

  const entries = new Map()

  for (const resource of courseResources) {
    if (resource?.is_locked === true) continue

    const routePath = buildCourseRoutePath(resource)
    if (!routePath) continue
    const pageUrl = joinUrl(siteUrl, routePath)
    const imageNodes = collectImageNodes(resource, { apiBase, mediaBase })
    const lastmod = toLastMod(resource?.date_modification)
    mergePageImages(entries, pageUrl, imageNodes, lastmod)
  }

  for (const resource of exerciseResources) {
    if (resource?.is_locked === true) continue

    const routePath = buildExerciseRoutePath(resource)
    if (!routePath) continue
    const pageUrl = joinUrl(siteUrl, routePath)
    const imageNodes = collectImageNodes(resource, { apiBase, mediaBase })
    const lastmod = toLastMod(resource?.date_modification)
    mergePageImages(entries, pageUrl, imageNodes, lastmod)
  }

  for (const resource of [...summaryResources, ...tableResources]) {
    if (resource?.is_locked === true) continue

    const routePath = buildSummaryRoutePath(resource)
    if (!routePath) continue
    const pageUrl = joinUrl(siteUrl, routePath)
    const imageNodes = collectImageNodes(resource, { apiBase, mediaBase })
    const lastmod = toLastMod(resource?.date_modification)
    mergePageImages(entries, pageUrl, imageNodes, lastmod)
  }

  const orderedEntries = [...entries.values()].sort((a, b) => a.loc.localeCompare(b.loc, 'fr'))
  if (!orderedEntries.length) {
    try {
      await fs.access(outPath)
      console.warn('[sitemap-images] no entries generated, keeping existing sitemap-images.xml')
      return
    } catch {
      throw new Error('No image sitemap entries could be generated and no previous sitemap exists.')
    }
  }
  const lines = []
  lines.push('<?xml version=\"1.0\" encoding=\"UTF-8\"?>')
  lines.push('<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\" xmlns:image=\"http://www.google.com/schemas/sitemap-image/1.1\">')

  for (const entry of orderedEntries) {
    lines.push('  <url>')
    lines.push(`    <loc>${escapeXml(entry.loc)}</loc>`)
    if (entry.lastmod) {
      lines.push(`    <lastmod>${escapeXml(entry.lastmod)}</lastmod>`)
    }
    for (const image of entry.images) {
      lines.push('    <image:image>')
      lines.push(`      <image:loc>${escapeXml(image.loc)}</image:loc>`)
      if (image.caption) {
        lines.push(`      <image:caption>${escapeXml(image.caption)}</image:caption>`)
      }
      if (image.title) {
        lines.push(`      <image:title>${escapeXml(image.title)}</image:title>`)
      }
      lines.push('    </image:image>')
    }
    lines.push('  </url>')
  }

  lines.push('</urlset>')
  await fs.writeFile(outPath, `${lines.join('\n')}\n`, 'utf8')
  console.log(`[sitemap-images] wrote ${orderedEntries.length} urls to ${outPath}`)
}

await buildImageSitemap()
