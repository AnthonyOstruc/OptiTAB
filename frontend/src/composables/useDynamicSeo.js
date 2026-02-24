const TITLE_SUFFIX = '| OptiTAB'
const TITLE_MAX_LENGTH = 70
const TITLE_TARGET_MIN_LENGTH = 45
const TITLE_TARGET_MAX_LENGTH = 65
const DESCRIPTION_MIN_LENGTH = 140
const DESCRIPTION_MAX_LENGTH = 160
const DEFAULT_LEVEL = 'Tous niveaux'
const PEDAGOGIC_LABEL_PREFIX = /^(résumé\s*[:\-]\s*|decouverte\s*[:\-]\s*|découverte\s*[:\-]\s*|entrainement\s*[:\-]\s*|entraînement\s*[:\-]\s*|ds\s*[:\-]\s*)/i

export const DYNAMIC_SEO_PAGE_TYPES = Object.freeze({
  EXERCISE_DETAIL: 'exercise-detail',
  COURSE_DETAIL: 'course-detail',
  SUMMARY_DETAIL: 'summary-detail',
  EXERCISE_CHAPTER: 'exercise-chapter'
})

const PAGE_SPEC = Object.freeze({
  [DYNAMIC_SEO_PAGE_TYPES.EXERCISE_DETAIL]: {
    descriptor: 'exercice corrigé',
    fallbackTopic: 'Exercice de maths',
    baseDescription: (topic, level) =>
      `Exercice corrigé pas-à-pas sur ${topic} (${level}) : méthode, étapes clés et correction détaillée.`,
    ogType: 'article'
  },
  [DYNAMIC_SEO_PAGE_TYPES.COURSE_DETAIL]: {
    descriptor: 'cours de maths',
    fallbackTopic: 'Cours de maths',
    baseDescription: (topic, level) =>
      `Cours sur ${topic} (${level}) : explications claires, méthode, exemples et exercices pour s’entraîner.`,
    ogType: 'article'
  },
  [DYNAMIC_SEO_PAGE_TYPES.SUMMARY_DETAIL]: {
    descriptor: 'fiche de révision',
    fallbackTopic: 'Fiche de révision',
    baseDescription: (topic, level) =>
      `Fiche de révision sur ${topic} (${level}) : formules, méthodes, exemples rapides et points à retenir.`,
    ogType: 'article'
  },
  [DYNAMIC_SEO_PAGE_TYPES.EXERCISE_CHAPTER]: {
    descriptor: 'exercices corrigés',
    fallbackTopic: 'Chapitre de maths',
    baseDescription: (topic, level) =>
      `Exercices corrigés sur ${topic} (${level}) : méthodes, explications et corrections détaillées. Entraînement gratuit.`,
    ogType: 'website'
  }
})

function normalizeWhitespace(value) {
  return String(value || '')
    .replace(/\s+/g, ' ')
    .trim()
}

function decodeHtmlEntities(value) {
  const raw = String(value || '')
  if (!raw.includes('&')) return raw
  if (typeof document === 'undefined') return raw
  const textarea = document.createElement('textarea')
  textarea.innerHTML = raw
  return textarea.value
}

export function stripHtmlForSeo(value) {
  return normalizeWhitespace(
    decodeHtmlEntities(String(value || '').replace(/<[^>]*>/g, ' '))
  )
}

export function normalizePathname(pathname) {
  const raw = normalizeWhitespace(pathname)
  if (!raw) return '/'
  const withSlash = raw.startsWith('/') ? raw : `/${raw}`
  if (withSlash.length === 1) return withSlash
  return withSlash.replace(/\/+$/, '')
}

function toSentenceCase(value) {
  const clean = normalizeWhitespace(value)
  if (!clean) return ''
  return `${clean.charAt(0).toUpperCase()}${clean.slice(1)}`
}

function truncateAtWord(value, maxLength, ellipsis = '') {
  const clean = normalizeWhitespace(value)
  if (!clean || clean.length <= maxLength) return clean
  const safeMax = Math.max(8, maxLength - ellipsis.length)
  const sliced = clean.slice(0, safeMax)
  const lastSpace = sliced.lastIndexOf(' ')
  const base = lastSpace > 12 ? sliced.slice(0, lastSpace) : sliced
  return `${base.trimEnd()}${ellipsis}`
}

function stripPedagogicPrefix(value) {
  let clean = normalizeWhitespace(value)
  let prev = ''
  while (clean && clean !== prev) {
    prev = clean
    clean = clean.replace(PEDAGOGIC_LABEL_PREFIX, '').trim()
  }
  return clean
}

function normalizeTopic(topic, fallbackTopic) {
  const raw = stripHtmlForSeo(topic)
  const clean = toSentenceCase(stripPedagogicPrefix(raw))
  return clean || fallbackTopic
}

function normalizeLevel(level) {
  const clean = toSentenceCase(stripHtmlForSeo(level))
  return clean || DEFAULT_LEVEL
}

function ensureTitleSuffix(title) {
  const clean = normalizeWhitespace(title).replace(/\s*\|\s*OptiTAB$/i, '')
  return `${clean} ${TITLE_SUFFIX}`
}

function buildTitle({ descriptor, topic, level }) {
  const fixedPart = ` — ${descriptor} (${level})`
  const suffixPart = ` ${TITLE_SUFFIX}`
  const rawBody = `${topic}${fixedPart}`
  let title = ensureTitleSuffix(rawBody)

  if (title.length < TITLE_TARGET_MIN_LENGTH) {
    const filler = title.includes('maths') ? '' : ' de maths'
    title = ensureTitleSuffix(`${topic}${filler}${fixedPart}`)
  }

  if (title.length > TITLE_TARGET_MAX_LENGTH) {
    const maxBodyLength = Math.max(20, TITLE_TARGET_MAX_LENGTH - suffixPart.length)
    const body = truncateAtWord(rawBody, maxBodyLength)
    title = ensureTitleSuffix(body)
  }

  if (title.length > TITLE_MAX_LENGTH) {
    const maxBodyLength = Math.max(20, TITLE_MAX_LENGTH - suffixPart.length)
    title = ensureTitleSuffix(truncateAtWord(title, maxBodyLength))
  }

  return title
}

function sentenceWithoutTrailingPeriod(value) {
  return normalizeWhitespace(value).replace(/[.。!?]+$/, '').trim()
}

function buildSecondSentence({ pageType }) {
  const defaultByType = {
    [DYNAMIC_SEO_PAGE_TYPES.EXERCISE_DETAIL]:
      "Repères fiables pour valider chaque raisonnement.",
    [DYNAMIC_SEO_PAGE_TYPES.COURSE_DETAIL]:
      "Méthode structurée pour appliquer les notions sans confusion.",
    [DYNAMIC_SEO_PAGE_TYPES.SUMMARY_DETAIL]:
      "Repères clairs pour mémoriser l'essentiel durablement.",
    [DYNAMIC_SEO_PAGE_TYPES.EXERCISE_CHAPTER]:
      "Progression guidée pour gagner en autonomie."
  }
  return defaultByType[pageType] || defaultByType[DYNAMIC_SEO_PAGE_TYPES.COURSE_DETAIL]
}

function countSentences(value) {
  return (String(value || '').match(/[.!?]+/g) || []).length
}

function expectedDescriptionPrefix(pageType) {
  const byType = {
    [DYNAMIC_SEO_PAGE_TYPES.COURSE_DETAIL]: 'Cours sur ',
    [DYNAMIC_SEO_PAGE_TYPES.SUMMARY_DETAIL]: 'Fiche de révision sur ',
    [DYNAMIC_SEO_PAGE_TYPES.EXERCISE_CHAPTER]: 'Exercices corrigés sur ',
    [DYNAMIC_SEO_PAGE_TYPES.EXERCISE_DETAIL]: 'Exercice corrigé pas-à-pas sur '
  }
  return byType[pageType] || byType[DYNAMIC_SEO_PAGE_TYPES.COURSE_DETAIL]
}

function startsWithExpectedPrefix(pageType, text) {
  const prefix = expectedDescriptionPrefix(pageType)
  return normalizeWhitespace(text).toLowerCase().startsWith(prefix.toLowerCase())
}

function buildDescriptionFromTemplate({ pageType, baseDescription, secondSentence }) {
  const template = `${sentenceWithoutTrailingPeriod(baseDescription)}.`
  if (countSentences(template) >= 2) return template
  const extra = sentenceWithoutTrailingPeriod(secondSentence)
  if (!extra) return template
  return `${template} ${extra}.`
}

function finalizeDescription(value) {
  let clean = normalizeWhitespace(value)
    .replace(/[.…]+$/, '')
    .replace(/[!?]+$/, '')
    .trim()
  if (!clean) return ''

  if (clean.length > DESCRIPTION_MAX_LENGTH - 1) {
    clean = truncateAtWord(clean, DESCRIPTION_MAX_LENGTH - 1)
      .replace(/[.…!?]+$/, '')
      .trim()
  }
  if (!clean) return ''
  return `${clean}.`
}

function buildDescription({ pageType, baseDescription, sourceText, topic }) {
  const secondSentence = buildSecondSentence({ pageType, sourceText, topic })
  let description = buildDescriptionFromTemplate({ pageType, baseDescription, secondSentence })

  if (description.length < DESCRIPTION_MIN_LENGTH) {
    const sentenceCount = countSentences(description)
    if (sentenceCount < 2) {
      description = normalizeWhitespace(
        `${description} Clair, concret et utile pour progresser.`
      )
    } else {
      description = normalizeWhitespace(
        `${description.replace(/[.!?]\s*$/, '')} pour progresser.`
      )
    }
  }

  if (description.length < DESCRIPTION_MIN_LENGTH) {
    description = normalizeWhitespace(
      `${description.replace(/[.…]+$/, '')} avec une méthode directement applicable.`
    )
  }

  if (!startsWithExpectedPrefix(pageType, description)) {
    description = buildDescriptionFromTemplate({ pageType, baseDescription, secondSentence })
  }

  description = finalizeDescription(description)
  if (!startsWithExpectedPrefix(pageType, description)) {
    description = finalizeDescription(
      buildDescriptionFromTemplate({ pageType, baseDescription, secondSentence })
    )
  }
  return description
}

export function buildDynamicSeo({
  pageType,
  topic,
  level,
  sourceText
} = {}) {
  const spec = PAGE_SPEC[pageType] || PAGE_SPEC[DYNAMIC_SEO_PAGE_TYPES.COURSE_DETAIL]
  const cleanTopic = normalizeTopic(topic, spec.fallbackTopic)
  const cleanLevel = normalizeLevel(level)
  const title = buildTitle({
    descriptor: spec.descriptor,
    topic: cleanTopic,
    level: cleanLevel
  })
  const description = buildDescription({
    pageType,
    baseDescription: spec.baseDescription(cleanTopic, cleanLevel),
    sourceText,
    topic: cleanTopic
  })

  return {
    title,
    description,
    topic: cleanTopic,
    level: cleanLevel,
    ogType: spec.ogType
  }
}

export function buildCanonicalSeoFields({
  routePath,
  canonicalPath,
  isCanonicalRoute,
  robotsWhenCanonical
} = {}) {
  const currentPath = normalizePathname(routePath)
  const targetPath = normalizePathname(canonicalPath || currentPath)
  return {
    canonicalPath: currentPath,
    canonicalUrl: isCanonicalRoute ? undefined : targetPath,
    robots: isCanonicalRoute ? String(robotsWhenCanonical || '') : 'noindex,follow'
  }
}

export function pageTypeFromResourceType(resourceType) {
  const type = String(resourceType || '').trim().toLowerCase()
  if (type === 'exercise') return DYNAMIC_SEO_PAGE_TYPES.EXERCISE_DETAIL
  if (type === 'summary') return DYNAMIC_SEO_PAGE_TYPES.SUMMARY_DETAIL
  return DYNAMIC_SEO_PAGE_TYPES.COURSE_DETAIL
}

export function topicFromSlug(slug) {
  const value = String(slug || '')
    .replace(/^exercice-gratuit-\d+-/i, '')
    .replace(/-\d+$/, '')
    .replace(/[-_]+/g, ' ')
  return toSentenceCase(value)
}
