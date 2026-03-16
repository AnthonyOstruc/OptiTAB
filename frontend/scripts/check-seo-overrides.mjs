import fs from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import {
  MANUAL_SEO_OVERRIDES_BY_PATH,
  listManualSeoOverridePaths
} from '../src/config/manualSeoOverrides.js'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const DEFAULT_SITEMAP_PATH = path.resolve(__dirname, '..', 'public', 'sitemap.xml')
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

const FORBIDDEN_GENERIC_TITLE_PATTERNS = [
  /^optitab\s*-\s*page$/i,
  /^cours\s*-\s*optitab$/i,
  /^exercices\s*-\s*optitab$/i,
  /^accueil$/i,
  /^connexion$/i,
  /^logo\s*optitab$/i
]

function parseCliArgs(argv) {
  const options = {
    sitemapPath: DEFAULT_SITEMAP_PATH,
    strictManual: false,
    showMissingLimit: 50
  }

  for (const arg of argv) {
    if (arg.startsWith('--sitemap=')) {
      const value = arg.slice('--sitemap='.length).trim()
      if (value) options.sitemapPath = path.resolve(process.cwd(), value)
      continue
    }
    if (arg === '--strict-manual' || arg === '--fail-on-missing') {
      options.strictManual = true
      continue
    }
    if (arg.startsWith('--missing-limit=')) {
      const raw = Number(arg.slice('--missing-limit='.length))
      if (Number.isFinite(raw) && raw > 0) options.showMissingLimit = Math.floor(raw)
    }
  }

  return options
}

function normalizePathname(pathname) {
  const raw = String(pathname || '').trim()
  if (!raw) return '/'
  try {
    const url = new URL(raw, 'https://www.optitab.net')
    const pathValue = String(url.pathname || '/').replace(/\/+$/, '')
    return pathValue || '/'
  } catch {
    const withSlash = raw.startsWith('/') ? raw : `/${raw}`
    const normalized = withSlash.replace(/\/+$/, '')
    return normalized || '/'
  }
}

function extractLocsFromSitemapXml(xml) {
  return [...String(xml || '').matchAll(/<loc>(.*?)<\/loc>/g)]
    .map((match) => String(match?.[1] || '').trim())
    .filter(Boolean)
}

function isGenericTitle(title) {
  const value = String(title || '').trim()
  if (!value) return true
  return FORBIDDEN_GENERIC_TITLE_PATTERNS.some((re) => re.test(value))
}

function isRoutedByAutomaticSeo(pathname) {
  const pathValue = normalizePathname(pathname)
  if (STATIC_INDEXABLE_PATHS.has(pathValue)) return true
  if (GROUPED_COURSE_PATH_RE.test(pathValue)) return true
  if (GROUPED_SUMMARY_PATH_RE.test(pathValue)) return true
  if (GROUPED_EXERCISE_CHAPTER_PATH_RE.test(pathValue)) return true
  return false
}

function inferPageType(pathname) {
  const pathValue = normalizePathname(pathname)
  if (pathValue.startsWith('/ressources-gratuites/cours/')) return 'cours'
  if (pathValue.startsWith('/ressources-gratuites/syntheses/')) return 'synthese'
  if (pathValue.startsWith('/ressources-gratuites/exercices/')) return 'exercice'
  if (pathValue === '/cours-particuliers' || pathValue === '/tarifs') return 'service'
  if (pathValue.startsWith('/ressources-gratuites')) return 'niveau'
  return 'service'
}

function findDuplicates(valuesByKey) {
  const seen = new Map()
  const duplicates = []

  for (const [key, value] of valuesByKey) {
    const normalized = String(value || '').trim().toLowerCase()
    if (!normalized) continue
    if (seen.has(normalized)) {
      duplicates.push({ key, duplicateOf: seen.get(normalized), value })
      continue
    }
    seen.set(normalized, key)
  }

  return duplicates
}

async function run() {
  const options = parseCliArgs(process.argv.slice(2))
  const sitemapXml = await fs.readFile(options.sitemapPath, 'utf8')
  const sitemapPaths = [
    ...new Set(extractLocsFromSitemapXml(sitemapXml).map((loc) => normalizePathname(loc)))
  ].sort((a, b) => a.localeCompare(b, 'fr'))

  const manualPaths = listManualSeoOverridePaths().map((entry) => normalizePathname(entry))
  const manualSet = new Set(manualPaths)

  const manualEntries = Object.entries(MANUAL_SEO_OVERRIDES_BY_PATH).map(([pathValue, entry]) => ({
    path: normalizePathname(pathValue),
    title: String(entry?.title || '').trim(),
    description: String(entry?.description || '').trim()
  }))

  const missingTitle = manualEntries.filter((entry) => !entry.title)
  const missingDescription = manualEntries.filter((entry) => !entry.description)
  const genericTitles = manualEntries.filter((entry) => isGenericTitle(entry.title))
  const duplicateTitles = findDuplicates(manualEntries.map((entry) => [entry.path, entry.title]))
  const duplicateDescriptions = findDuplicates(manualEntries.map((entry) => [entry.path, entry.description]))

  const coveredByManual = []
  const coveredByAutomatic = []
  const uncovered = []
  const manualMissing = []

  for (const pathValue of sitemapPaths) {
    if (manualSet.has(pathValue)) {
      coveredByManual.push(pathValue)
      continue
    }
    manualMissing.push(pathValue)
    if (isRoutedByAutomaticSeo(pathValue)) {
      coveredByAutomatic.push(pathValue)
    } else {
      uncovered.push(pathValue)
    }
  }

  const byType = sitemapPaths.reduce((acc, pathValue) => {
    const type = inferPageType(pathValue)
    acc[type] = (acc[type] || 0) + 1
    return acc
  }, {})

  console.log('[seo-overrides] Summary')
  console.log(
    JSON.stringify(
      {
        sitemapUrls: sitemapPaths.length,
        manualOverrides: manualEntries.length,
        coveredByManual: coveredByManual.length,
        coveredByAutomatic: coveredByAutomatic.length,
        uncovered: uncovered.length,
        byType
      },
      null,
      2
    )
  )

  if (manualMissing.length > 0) {
    console.log(`[seo-overrides] Missing manual entries: ${manualMissing.length}`)
    for (const pathValue of manualMissing.slice(0, options.showMissingLimit)) {
      console.log(`- ${pathValue}`)
    }
    if (manualMissing.length > options.showMissingLimit) {
      console.log(`... ${manualMissing.length - options.showMissingLimit} more`)
    }
  }

  const errors = []
  if (missingTitle.length > 0) {
    errors.push(`Missing title for ${missingTitle.length} manual entries`)
  }
  if (missingDescription.length > 0) {
    errors.push(`Missing description for ${missingDescription.length} manual entries`)
  }
  if (genericTitles.length > 0) {
    errors.push(`Generic/forbidden title detected on ${genericTitles.length} manual entries`)
  }
  if (duplicateTitles.length > 0) {
    errors.push(`Duplicate manual titles: ${duplicateTitles.length}`)
  }
  if (duplicateDescriptions.length > 0) {
    errors.push(`Duplicate manual descriptions: ${duplicateDescriptions.length}`)
  }
  if (uncovered.length > 0) {
    errors.push(`Sitemap URLs without manual or automatic SEO route: ${uncovered.length}`)
  }
  if (options.strictManual && manualMissing.length > 0) {
    errors.push(`Strict manual mode enabled: ${manualMissing.length} sitemap URLs without manual entry`)
  }

  if (errors.length > 0) {
    console.error('[seo-overrides] FAIL')
    for (const item of errors) {
      console.error(`- ${item}`)
    }
    process.exit(1)
  }

  console.log('[seo-overrides] PASS')
}

run().catch((error) => {
  console.error('[seo-overrides] fatal:', error instanceof Error ? error.message : String(error))
  process.exit(1)
})
