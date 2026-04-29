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
  return ['left', 'right', 'center', 'full'].includes(value) ? value : 'center'
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

function isExternalHref(href) {
  return /^https?:\/\//i.test(href || '')
}

function resolveCtaImage(rawValue, images = []) {
  const value = String(rawValue ?? '').trim()
  if (!value) return null

  const markerMatch = value.match(/^\[?\s*IMAGE\s*_?\s*(\d+)\s*\]?$/i)
  if (!markerMatch) {
    return { src: value, alt: '' }
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
  const content = String(source ?? '')
  if (!content) return content

  return content.replace(/\[\s*CTA\s*\]([\s\S]*?)\[\s*\/\s*CTA\s*\]/gi, (_match, rawBlock) => {
    const fields = parseCtaFields(rawBlock)
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
    const image = resolveCtaImage(imageField, images)
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
  })
}

export function renderBlogImageMarkers(source, images = [], options = {}) {
  const content = String(source ?? '')
  if (!content) return content

  const { byPosition, sortedImages } = buildImagePositionMap(images)

  let replacedAnyMarker = false
  const withMarkers = content.replace(/\[\s*IMAGE\s*_?\s*(\d+)\s*\]/gi, (_match, rawPosition) => {
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
    }
  }
})

export function renderBlogMarkdown(source, options = {}) {
  const { title = '', stripTitleHeading = true, images = [], preview = false } = options
  if (!source) return ''

  const articleContent = stripTitleHeading
    ? removeDuplicateTitleHeading(source, title)
    : String(source ?? '')
  const hasExplicitMediaBlock = /\[\s*IMAGE\s*_?\s*\d+\s*\]|\[\s*CTA\s*\]/i.test(articleContent)
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
