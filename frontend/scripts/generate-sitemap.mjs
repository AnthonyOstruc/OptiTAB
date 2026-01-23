import fs from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

function normalizeSiteUrl(raw) {
  const value = String(raw || '').trim()
  if (!value) return ''
  return value.replace(/\/+$/, '')
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
  const p = String(pathname || '').trim()
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

function routeForResource(resource) {
  const slug = resource?.slug
  const type = resource?.resource_type || resource?.type || resource?.resourceType
  if (!slug || !type) return null

  if (type === 'course') return `/ressources-gratuites/cours/${slug}`
  if (type === 'exercise') return `/ressources-gratuites/exercices/${slug}`
  if (type === 'summary') return `/ressources-gratuites/syntheses/${slug}`

  return null
}

async function buildSitemap() {
  const siteUrl = normalizeSiteUrl(
    process.env.VITE_SITE_URL ||
    process.env.SITE_URL ||
    process.env.PUBLIC_SITE_URL ||
    'https://www.optitab.net'
  )

  const apiBase = normalizeSiteUrl(
    process.env.VITE_API_BASE_URL ||
    process.env.VITE_API_URL ||
    'https://optitab-backend.onrender.com'
  )

  const urls = new Map()
  const addUrl = (pathname, lastmod = '') => {
    if (!pathname) return
    const loc = joinUrl(siteUrl, pathname)
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

  // Static public pages
  addUrl('/', '')
  addUrl('/cours-particuliers', '')
  addUrl('/about', '')
  addUrl('/contact', '')
  addUrl('/conditions', '')
  addUrl('/cgv', '')
  addUrl('/cgu', '')
  addUrl('/confidentialite', '')
  addUrl('/legal', '')
  addUrl('/cookies', '')

  // Free content entry points
  addUrl('/ressources-gratuites/cours', '')
  addUrl('/ressources-gratuites/exercices', '')
  addUrl('/ressources-gratuites/syntheses', '')

  try {
    const baseEndpoint = `${apiBase}/api/free/learning-resources/`

    // 1) Custom FreeLearningResource items (curated content)
    const generic = await fetchAllPages(`${baseEndpoint}?page_size=500`)
    for (const item of generic) {
      const path = routeForResource(item)
      if (!path) continue
      addUrl(path, toLastMod(item?.date_modification))
    }

    // 2) Courses/Exercises/Summaries from existing models (filter locked)
    for (const type of ['course', 'exercise', 'summary']) {
      const items = await fetchAllPages(`${baseEndpoint}?type=${encodeURIComponent(type)}&page_size=500`)
      for (const item of items) {
        if (item?.is_locked === true) continue
        const path = routeForResource({ ...item, resource_type: type })
        if (!path) continue
        addUrl(path, toLastMod(item?.date_modification))
      }
    }
  } catch (err) {
    // Never fail the build if the API is unreachable.
    // We keep at least the static URLs above.
    console.warn('[sitemap] API fetch failed, generating a minimal sitemap:', err?.message || err)
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

  const outPath = path.resolve(__dirname, '..', 'public', 'sitemap.xml')
  await fs.writeFile(outPath, `${lines.join('\n')}\n`, 'utf8')
  console.log(`[sitemap] wrote ${entries.length} urls to ${outPath}`)
}

await buildSitemap()

