import { Marked } from 'marked'
import katex from 'katex'

function stripHtml(value) {
  return String(value ?? '').replace(/<[^>]*>/g, '')
}

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

function clampNumber(value, min, max, fallback) {
  const numeric = Number.parseInt(value, 10)
  if (!Number.isFinite(numeric)) return fallback
  return Math.min(max, Math.max(min, numeric))
}

function normalizeImageAlign(value) {
  const normalized = normalizeCtaKey(value)
  const compact = normalized.replace(/[\s_-]+/g, '')
  if (['left', 'gauche', 'agauche'].includes(compact)) return 'left'
  if (['right', 'droite', 'adroite'].includes(compact)) return 'right'
  if (['full', 'wide', 'pleinelargeur', 'pleinelargeur', 'largeurcomplete', '100'].includes(compact)) return 'full'
  return 'center'
}

function resolveImageUrl(image) {
  return image?.image_url || image?._preview || image?.preview_url || image?.image || ''
}

function renderBlogImageFigure(image, position, preview = false) {
  const src = resolveImageUrl(image)
  const align = normalizeImageAlign(image?.align)
  const width = align === 'full'
    ? 100
    : clampNumber(image?.width_percent, 20, 100, align === 'center' ? 100 : 45)
  const alt = escapeHtml(image?.alt_text || image?.caption || `Image ${position}`)
  const title = image?.title_text ? ` title="${escapeHtml(image.title_text)}"` : ''
  const caption = image?.caption
    ? `<figcaption class="blog-inline-image__caption">${escapeHtml(image.caption)}</figcaption>`
    : ''

  if (!src) {
    return preview
      ? `<div class="blog-image-placeholder">Image ${position} non disponible</div>`
      : ''
  }

  return `
<figure class="blog-inline-image blog-inline-image--${align}" style="--blog-image-width: ${width}%;">
  <img src="${escapeHtml(src)}" alt="${alt}"${title} loading="lazy" decoding="async" />
  ${caption}
</figure>`
}

function buildImagePositionMap(images = []) {
  const byPosition = new Map()
  const sortedImages = Array.isArray(images)
    ? [...images].sort((a, b) => {
      const posA = clampNumber(a?.position, 1, 999, 999)
      const posB = clampNumber(b?.position, 1, 999, 999)
      return posA - posB
    })
    : []

  sortedImages.forEach((image, index) => {
    const position = clampNumber(image?.position, 1, 999, index + 1)
    if (!byPosition.has(position)) {
      byPosition.set(position, image)
    }
  })

  return { byPosition, sortedImages }
}

function normalizeCtaKey(value) {
  return String(value ?? '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim()
}

function parseCtaFields(rawBlock) {
  const fields = {}
  String(rawBlock ?? '')
    .split(/\r?\n/)
    .map(line => line.trim())
    .filter(Boolean)
    .forEach((line) => {
      const separatorIndex = line.indexOf(':')
      if (separatorIndex === -1) return
      const key = normalizeCtaKey(line.slice(0, separatorIndex))
      const value = line.slice(separatorIndex + 1).trim()
      if (key) fields[key] = value
    })
  return fields
}

function ctaField(fields, keys, fallback = '') {
  for (const key of keys) {
    const value = fields[normalizeCtaKey(key)]
    if (value) return value
  }
  return fallback
}

const BLOG_CTA_PRESETS = {
  cours: {
    aliases: ['1', 'cours', 'cours particuliers', 'cours_particuliers', 'prof', 'professeur'],
    fields: {
      surtitre: 'Cours particuliers OptiTAB',
      titre: 'Progresser en maths avec un professeur',
      texte: 'Un accompagnement clair pour reprendre confiance, travailler les bonnes methodes et avancer plus vite.',
      bouton: 'Decouvrir les cours particuliers',
      url: '/cours-particuliers',
      image: '/cta-banner-cours-particuliers.png',
      image_alt: 'Cours particuliers de maths en ligne avec OptiTAB',
      image_position: 'droite',
      style: 'split',
      theme: 'optitab',
    },
  },
  abonnement: {
    aliases: ['2', 'abonnement', 'plateforme', 'premium', 'optitab'],
    fields: {
      surtitre: 'Plateforme de maths OptiTAB',
      titre: 'S entrainer avec des cours, fiches et exercices corriges',
      texte: 'Accede aux ressources de maths pour reviser, comprendre les notions et progresser regulierement.',
      bouton: 'Voir les abonnements',
      url: '/abonnement',
      image: '/cta-banner-plateforme.png',
      image_alt: 'Plateforme de maths OptiTAB avec cours et exercices corriges',
      image_position: 'gauche',
      style: 'split',
      theme: 'light',
    },
  },
}

const DEFAULT_BLOG_CTA_ORDER = ['cours', 'abonnement']
const CTA_PRESET_ALIAS_MAP = new Map(
  Object.entries(BLOG_CTA_PRESETS).flatMap(([key, preset]) => [
    [normalizeCtaKey(key).replace(/[\s_-]+/g, ''), key],
    ...preset.aliases.map(alias => [normalizeCtaKey(alias).replace(/[\s_-]+/g, ''), key]),
  ])
)

function ctaPresetKey(value) {
  const normalized = normalizeCtaKey(value).replace(/^(cta|cta defaut|cta default)\s*/i, '').replace(/[\s_-]+/g, '')
  return CTA_PRESET_ALIAS_MAP.get(normalized) || ''
}

function ctaFieldsObject(fields = {}) {
  return Object.fromEntries(
    Object.entries(fields).map(([key, value]) => [normalizeCtaKey(key), value])
  )
}

function parseImagePercent(value) {
  const match = String(value ?? '').match(/\d+/)
  if (!match) return ''
  return clampNumber(match[0], 20, 100, 100)
}

function imageWithInlineOptions(image, position, rawBlock) {
  const fields = parseCtaFields(rawBlock)
  const title = ctaField(fields, ['nom', 'nom image', 'nom de l image', 'titre', 'titre image', 'title'])
  const alt = ctaField(fields, ['alt', 'alt seo', 'texte alternatif', 'accessibilite', 'accessibilité'])
  const description = ctaField(fields, ['description', 'description seo', 'desc', 'seo description'])
  const caption = ctaField(fields, ['legende', 'légende', 'caption'])
  const align = ctaField(fields, ['alignement', 'align', 'position', 'placement'])
  const width = parseImagePercent(ctaField(fields, ['largeur', 'largeur %', 'width', 'width percent', 'width_percent']))

  return {
    ...(image || {}),
    position,
    title_text: description || title || image?.title_text || '',
    alt_text: alt || description || image?.alt_text || '',
    caption: caption || image?.caption || '',
    align: align ? normalizeImageAlign(align) : image?.align,
    width_percent: width || image?.width_percent,
  }
}

function normalizeCtaVariant(value) {
  const normalized = normalizeCtaKey(value)
  if (['solid', 'plein', 'bandeau', 'simple'].includes(normalized)) return 'solid'
  if (['split', 'image', 'visuel'].includes(normalized)) return 'split'
  return 'split'
}

function normalizeCtaTheme(value) {
  const normalized = normalizeCtaKey(value)
  if (['green', 'vert', 'lycee'].includes(normalized)) return 'green'
  if (['light', 'clair'].includes(normalized)) return 'light'
  if (['blue', 'bleu', 'optitab'].includes(normalized)) return 'optitab'
  return 'optitab'
}

function normalizeCtaImagePosition(value) {
  const normalized = normalizeCtaKey(value)
  const compact = normalized.replace(/[\s_-]+/g, '')
  if (['left', 'gauche', 'agauche'].includes(compact)) return 'left'
  if (['bottom', 'bas', 'dessous', 'endessous', 'sous'].includes(compact)) return 'bottom'
  return 'right'
}

function normalizeCtaHref(value) {
  const href = String(value ?? '').trim()
  if (!href) return '/cours-particuliers'
  if (/^(https?:\/\/|mailto:|tel:|\/(?!\/)|#)/i.test(href)) return href
  if (!href.includes(':') && /^[a-z0-9][a-z0-9/_?&=#.-]*$/i.test(href)) return `/${href}`
  return '/cours-particuliers'
}

function normalizeMarkdownHref(value) {
  const href = String(value ?? '').trim()
  if (!href) return ''
  if (/^(https?:\/\/|mailto:|tel:|\/(?!\/)|#)/i.test(href)) return href
  if (!href.includes(':') && /^[a-z0-9][a-z0-9/_?&=#.-]*$/i.test(href)) return `/${href}`
  return ''
}

function isExternalHref(href) {
  return /^https?:\/\//i.test(href || '')
}

function resolveCtaImage(rawValue, images = [], fallbackAlt = '') {
  const value = String(rawValue ?? '').trim()
  if (!value) return null

  const markerMatch = value.match(/^\[?\s*IMAGE\s*_?\s*(\d+)\s*\]?$/i)
  if (!markerMatch) {
    return { src: value, alt: fallbackAlt }
  }

  const position = Number.parseInt(markerMatch[1], 10)
  const { byPosition } = buildImagePositionMap(images)
  const image = byPosition.get(position)
  const src = resolveImageUrl(image)
  if (!src) return null

  return {
    src,
    alt: image?.alt_text || image?.caption || image?.title_text || `Image ${position}`,
    title: image?.title_text || '',
  }
}

export function renderBlogCtaBlocks(source, images = [], options = {}) {
  let content = String(source ?? '')
  if (!content) return content

  const usedPresets = new Set()
  const disableDefaultCtas = /\[\s*(?:CTA_AUCUN|CTA_NONE|NO_CTA|SANS_CTA)\s*\]/i.test(content)
  content = content.replace(/\[\s*(?:CTA_AUCUN|CTA_NONE|NO_CTA|SANS_CTA)\s*\]/gi, '')

  function renderCtaFromFields(fields) {
    const title = ctaField(fields, ['titre', 'title'])
    const text = ctaField(fields, ['texte', 'description', 'sous-titre', 'subtitle'])
    const eyebrow = ctaField(fields, ['surtitre', 'eyebrow'])
    const button = ctaField(fields, ['bouton', 'button', 'cta'], 'En savoir plus')
    const href = normalizeCtaHref(ctaField(fields, ['url', 'lien', 'link', 'href']))
    const variant = normalizeCtaVariant(ctaField(fields, ['style', 'variant', 'type']))
    const theme = normalizeCtaTheme(ctaField(fields, ['theme', 'couleur', 'color']))
    const imageField = ctaField(fields, ['image', 'img', 'visuel'])
    const imagePosition = normalizeCtaImagePosition(ctaField(fields, [
      'image_position',
      'position_image',
      'position image',
      'image-position',
      'placement image',
      'placement',
    ]))
    const imageAlt = ctaField(fields, ['image_alt', 'alt image', 'alt', 'alt seo'])
    const image = resolveCtaImage(imageField, images, imageAlt)
    const target = isExternalHref(href) ? ' target="_blank" rel="noopener noreferrer"' : ''
    const hasImage = Boolean(image?.src)
    const hasMedia = hasImage || (options.preview && imageField)

    if (!title && !text && !button) return ''

    const media = hasImage
      ? `<a class="blog-cta-card__media" href="${escapeHtml(href)}"${target} aria-label="${escapeHtml(button)}">
  <img src="${escapeHtml(image.src)}" alt="${escapeHtml(image.alt || title)}"${image.title ? ` title="${escapeHtml(image.title)}"` : ''} loading="lazy" decoding="async" />
</a>`
      : (options.preview && imageField
        ? '<div class="blog-cta-card__media blog-cta-card__media--empty">Image CTA non disponible</div>'
        : '')

    return `
<section class="blog-cta-card blog-cta-card--${variant} blog-cta-card--${theme} blog-cta-card--image-${imagePosition}${hasMedia ? ' blog-cta-card--has-image' : ''}">
  <div class="blog-cta-card__body">
    ${eyebrow ? `<p class="blog-cta-card__eyebrow">${escapeHtml(eyebrow)}</p>` : ''}
    ${title ? `<h3 class="blog-cta-card__title">${escapeHtml(title)}</h3>` : ''}
    ${text ? `<p class="blog-cta-card__text">${escapeHtml(text)}</p>` : ''}
    <a class="blog-cta-card__button" href="${escapeHtml(href)}"${target}>${escapeHtml(button)}</a>
  </div>
  ${media}
</section>`
  }

  content = content.replace(/\[\s*CTA\s*[_:-]?\s*([A-Z0-9_\-\s]+?)\s*\]/gi, (match, rawPreset) => {
    const key = ctaPresetKey(rawPreset)
    if (!key) return match
    usedPresets.add(key)
    return `\n\n${renderCtaFromFields(ctaFieldsObject(BLOG_CTA_PRESETS[key].fields))}\n\n`
  })

  content = content.replace(/\[\s*CTA_DEFAUTS?\s*\]|\[\s*CTA_DEFAULTS?\s*\]/gi, () => {
    DEFAULT_BLOG_CTA_ORDER.forEach(key => usedPresets.add(key))
    return DEFAULT_BLOG_CTA_ORDER
      .map(key => renderCtaFromFields(ctaFieldsObject(BLOG_CTA_PRESETS[key].fields)))
      .join('\n\n')
  })

  content = content.replace(/\[\s*CTA\s*\]([\s\S]*?)\[\s*\/\s*CTA\s*\]/gi, (_match, rawBlock) => {
    const fields = parseCtaFields(rawBlock)
    return renderCtaFromFields(fields)
  })

  if (!disableDefaultCtas && options.autoDefaultCtas !== false) {
    const missingDefaults = DEFAULT_BLOG_CTA_ORDER.filter(key => !usedPresets.has(key))
    if (missingDefaults.length) {
      const defaultCtas = missingDefaults
        .map(key => renderCtaFromFields(ctaFieldsObject(BLOG_CTA_PRESETS[key].fields)))
        .join('\n\n')
      content = `${content.trim()}\n\n${defaultCtas}`
    }
  }

  return content
}

export function renderBlogImageMarkers(source, images = [], options = {}) {
  const content = String(source ?? '')
    .replace(/\n?\[\s*IMAGE\s*_?\s*0\s*\][\s\S]*?\[\s*\/\s*IMAGE(?:\s*_?\s*0)?\s*\]\n?/gi, '\n\n')
    .replace(/^\s*\[\s*IMAGE\s*_?\s*0\s*\]\s*$/gmi, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim()
  if (!content) return content

  const { byPosition, sortedImages } = buildImagePositionMap(images)

  let replacedAnyMarker = false
  const withConfiguredMarkers = content.replace(
    /\[\s*IMAGE\s*_?\s*(\d+)\s*\]([\s\S]*?)\[\s*\/\s*IMAGE(?:\s*_?\s*\1)?\s*\]/gi,
    (_match, rawPosition, rawBlock) => {
      replacedAnyMarker = true
      const position = Number.parseInt(rawPosition, 10)
      const image = imageWithInlineOptions(byPosition.get(position), position, rawBlock)
      return `\n\n${renderBlogImageFigure(image, position, options.preview)}\n\n`
    }
  )

  const withMarkers = withConfiguredMarkers.replace(/\[\s*IMAGE\s*_?\s*(\d+)\s*\]/gi, (_match, rawPosition) => {
    replacedAnyMarker = true
    const position = Number.parseInt(rawPosition, 10)
    const image = byPosition.get(position)
    return `\n\n${renderBlogImageFigure(image, position, options.preview)}\n\n`
  })

  if (replacedAnyMarker || options.skipGallery || sortedImages.length === 0) {
    return withMarkers
  }

  const gallery = sortedImages
    .map((image, index) => {
      const position = clampNumber(image?.position, 1, 999, index + 1)
      return renderBlogImageFigure(image, position, options.preview)
    })
    .filter(Boolean)
    .join('\n\n')

  return gallery ? `${withMarkers}\n\n${gallery}` : withMarkers
}

export function slugifyHeading(value) {
  return stripHtml(value)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
}

export function plainHeadingText(value) {
  return stripHtml(String(value ?? ''))
    .replace(/!\[([^\]]*)\]\([^)]+\)/g, '$1')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/[*_`~#]/g, '')
    .trim()
}

function normalizeComparableText(value) {
  return plainHeadingText(value)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^\p{L}\p{N}\s]/gu, '')
    .replace(/\s+/g, ' ')
    .trim()
}

export function removeDuplicateTitleHeading(source, title) {
  const content = String(source ?? '')
  const match = content.match(/^\s*#\s+(.+?)(?:\r?\n|$)/)
  if (!match) return content

  const heading = normalizeComparableText(match[1])
  const pageTitle = normalizeComparableText(title)
  const looksLikeArticleTitle = !pageTitle
    || heading === pageTitle
    || pageTitle.startsWith(heading)
    || heading.startsWith(pageTitle)

  if (!looksLikeArticleTitle) {
    return content
  }

  return content.slice(match[0].length).replace(/^\s*\r?\n/, '')
}

function renderKatex(latex, displayMode = false) {
  const expression = String(latex ?? '').trim()
  if (!expression) return ''

  try {
    const html = katex.renderToString(expression, {
      throwOnError: false,
      displayMode,
      strict: 'ignore',
      trust: false,
    })

    if (displayMode) {
      return `<div class="blog-math blog-math--display">${html}</div>`
    }

    return `<span class="blog-math blog-math--inline">${html}</span>`
  } catch (_) {
    return `<code class="blog-math-error">${escapeHtml(expression)}</code>`
  }
}

function protectCodeBlocks(source) {
  const blocks = []
  const text = String(source ?? '').replace(/```[\s\S]*?```|`[^`\n]*`/g, (match) => {
    const key = `@@OPTITAB_CODE_${blocks.length}@@`
    blocks.push(match)
    return key
  })

  return { text, blocks }
}

function restoreCodeBlocks(source, blocks) {
  return blocks.reduce(
    (content, block, index) => content.replaceAll(`@@OPTITAB_CODE_${index}@@`, block),
    source
  )
}

export function renderLatexBeforeMarkdown(source) {
  const { text, blocks } = protectCodeBlocks(source)
  const withMath = text
    .replace(/\$\$([\s\S]+?)\$\$/g, (_match, math) => `\n\n${renderKatex(math, true)}\n\n`)
    .replace(/\\\[([\s\S]+?)\\\]/g, (_match, math) => `\n\n${renderKatex(math, true)}\n\n`)
    .replace(/\\\(([\s\S]+?)\\\)/g, (_match, math) => renderKatex(math, false))
    .replace(/(^|[^\\$])\$(?!\$)([^\n$]+?)\$(?!\$)/g, (_match, prefix, math) => {
      return `${prefix}${renderKatex(math, false)}`
    })

  return restoreCodeBlocks(withMath, blocks)
}

const blogMarked = new Marked({ breaks: true, gfm: true })

blogMarked.use({
  renderer: {
    heading(tokenOrText, level) {
      const isToken = typeof tokenOrText === 'object' && tokenOrText !== null
      const depth = Math.min(6, Math.max(1, Number(isToken ? tokenOrText.depth : level) || 2))
      const rawText = isToken ? tokenOrText.text : tokenOrText
      const html = isToken && tokenOrText.tokens
        ? this.parser.parseInline(tokenOrText.tokens)
        : String(tokenOrText ?? '')
      const id = slugifyHeading(rawText)

      return `<h${depth} id="${id}">${html}</h${depth}>\n`
    },
    link(tokenOrHref, title, text) {
      const isToken = typeof tokenOrHref === 'object' && tokenOrHref !== null
      const rawHref = isToken ? tokenOrHref.href : tokenOrHref
      const href = normalizeMarkdownHref(rawHref)
      const rawTitle = isToken ? tokenOrHref.title : title
      const html = isToken && tokenOrHref.tokens
        ? this.parser.parseInline(tokenOrHref.tokens)
        : String(text ?? '')

      if (!href) return html

      const titleAttr = rawTitle ? ` title="${escapeHtml(rawTitle)}"` : ''
      const targetAttr = isExternalHref(href) ? ' target="_blank" rel="noopener noreferrer"' : ''
      return `<a href="${escapeHtml(href)}"${titleAttr}${targetAttr}>${html}</a>`
    }
  }
})

export function renderBlogMarkdown(source, options = {}) {
  const { title = '', stripTitleHeading = true, images = [], preview = false } = options
  if (!source) return ''

  const articleContent = stripTitleHeading
    ? removeDuplicateTitleHeading(source, title)
    : String(source ?? '')
  const hasExplicitMediaBlock = /\[\s*IMAGE\s*_?\s*[1-9]\d*\s*\]|\[\s*CTA\s*\]/i.test(articleContent)
  const contentWithCtas = renderBlogCtaBlocks(articleContent, images, { preview })
  const contentWithImages = renderBlogImageMarkers(contentWithCtas, images, { preview, skipGallery: hasExplicitMediaBlock })
  const contentWithKatex = renderLatexBeforeMarkdown(contentWithImages)

  return blogMarked.parse(contentWithKatex)
}

export function extractBlogToc(source) {
  if (!source) return []

  const items = []
  const regex = /^(#{2,3})\s+(.+)$/gm
  let match
  while ((match = regex.exec(source)) !== null) {
    const level = match[1].length
    const text = plainHeadingText(match[2])
    const id = slugifyHeading(text)
    items.push({ level, text, id })
  }
  return items
}
