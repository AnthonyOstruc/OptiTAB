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

export function renderBlogImageMarkers(source, images = [], options = {}) {
  const content = String(source ?? '')
  if (!content) return content

  const byPosition = new Map()
  ;(Array.isArray(images) ? images : []).forEach((image, index) => {
    const position = clampNumber(image?.position, 1, 999, index + 1)
    if (!byPosition.has(position)) {
      byPosition.set(position, image)
    }
  })

  return content.replace(/^\s*\[IMAGE_(\d+)\]\s*$/gm, (_match, rawPosition) => {
    const position = Number.parseInt(rawPosition, 10)
    const image = byPosition.get(position)
    return `\n\n${renderBlogImageFigure(image, position, options.preview)}\n\n`
  })
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
  const contentWithImages = renderBlogImageMarkers(articleContent, images, { preview })
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
