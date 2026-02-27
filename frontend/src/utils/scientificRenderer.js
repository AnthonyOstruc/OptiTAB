/**
 * Utilitaire pour le rendu scientifique des contenus (cours, exercices, etc.)
 */

/**
 * Traite le texte LaTeX et HTML de base
 */
export function unescapeLatex(text) {
  if (!text) return ''

  let base = text
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;(?!nbsp;)/g, '&')
    .replace(/\\/g, '\\')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>')

  const escapeAngles = (s) => s.replace(/</g, '&lt;').replace(/>/g, '&gt;')

  base = base
    .replace(/\$\$([\s\S]*?)\$\$/g, (m, inner) => `$$${escapeAngles(inner)}$$`)
    .replace(/\\\[([\s\S]*?)\\\]/g, (m, inner) => `\\[${escapeAngles(inner)}\\]`)
    .replace(/\\\(([\s\S]*?)\\\)/g, (m, inner) => `\\(${escapeAngles(inner)}\\)`)

  base = base.replace(/(^|[^$])\$(?!\$)([^$\n]*?)\$(?!\$)/g, (m, prefix, inner) => {
    return `${prefix}$${escapeAngles(inner)}$`
  })

  return base
}

/**
 * Convertit le Markdown en HTML
 */
export function markdownToHtml(text) {
  if (!text) return ''

  let html = text

  html = html.replace(/^#### (.*$)/gm, '<h4 style="margin-top: 0.5em; margin-bottom: 0.5em; color: #193e8e; font-weight: 600;">$1</h4>')
  html = html.replace(/^### (.*$)/gm, '<h3 style="margin-top: 0.6em; margin-bottom: 0.5em; color: #193e8e; font-weight: 600;">$1</h3>')
  html = html.replace(/^## (.*$)/gm, '<h2 style="margin-top: 0.7em; margin-bottom: 0.5em; color: #193e8e; font-weight: 600; font-size: 1.5em;">$1</h2>')
  html = html.replace(/^# (.*$)/gm, '<h1 style="margin-top: 0.8em; margin-bottom: 0.6em; color: #193e8e; font-weight: 700; font-size: 1.8em;">$1</h1>')

  const lines = html.split('\n')
  const processedLines = []
  let inList = false

  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i]
    const trimmedLine = line.trim()

    if (trimmedLine.startsWith('- ')) {
      if (!inList) {
        processedLines.push('<ul style="margin: 1em 0; padding-left: 0;">')
        inList = true
      }
      processedLines.push(`<li style="margin-bottom: 0.5em;">${trimmedLine.substring(2)}</li>`)
    } else {
      if (inList) {
        processedLines.push('</ul>')
        inList = false
      }
      if (trimmedLine) {
        const processedLine = line
          .replace(/^ +/g, (match) => '&nbsp;'.repeat(match.length))
          .replace(/ +$/g, (match) => '&nbsp;'.repeat(match.length))
          .replace(/  +/g, (match) => '&nbsp;'.repeat(match.length))

        processedLines.push(`<p style="margin-bottom: 1em; line-height: 1.6;">${processedLine}</p>`)
      } else if (line === '') {
        processedLines.push('<p style="margin-bottom: 1em; line-height: 1.6;">&nbsp;</p>')
      }
    }
  }

  if (inList) {
    processedLines.push('</ul>')
  }

  html = processedLines.join('\n')
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong style="color: #193e8e;">$1</strong>')
  html = html.replace(/\*([^*]+)\*/g, '<em style="color: #666;">$1</em>')

  return html
}

function shiftHeadingLevels(html, offset) {
  if (!offset) return html
  return html.replace(/<(\/?)h([1-6])([^>]*)>/gi, (match, slash, level, rest) => {
    const current = Number(level)
    if (!Number.isFinite(current)) return match
    const next = Math.min(6, Math.max(1, current + offset))
    return `<${slash}h${next}${rest}>`
  })
}

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

function normalizeText(value) {
  return String(value ?? '').replace(/\s+/g, ' ').trim()
}

function resolveImageCaption(image) {
  return normalizeText(image?.caption || image?.legende || '')
}

function resolveImageAlt(image, position) {
  const resolvedAlt = normalizeText(
    image?.alt_text_resolved || image?.resolved_alt_text || image?.alt_text || image?.legende || image?.caption || ''
  )
  if (resolvedAlt) return resolvedAlt

  const resolvedTitle = normalizeText(image?.title_text_resolved || image?.resolved_title_text || image?.title_text || '')
  if (resolvedTitle) return resolvedTitle

  return `Illustration du cours ${position}`
}

function resolveImageTitle(image) {
  return normalizeText(image?.title_text_resolved || image?.resolved_title_text || image?.title_text || '')
}

function resolveImageDimensions(image) {
  const width = Number.parseInt(image?.width, 10)
  const height = Number.parseInt(image?.height, 10)
  const safeWidth = Number.isFinite(width) && width > 0 ? width : 1200
  const safeHeight = Number.isFinite(height) && height > 0 ? height : 675
  return { width: safeWidth, height: safeHeight }
}

function stripUrlQuery(value) {
  const raw = String(value || '').trim()
  if (!raw) return raw
  try {
    const base = typeof window !== 'undefined' && window.location?.origin
      ? window.location.origin
      : 'https://www.optitab.net'
    const parsed = new URL(raw, base)
    parsed.search = ''
    parsed.hash = ''
    return parsed.toString()
  } catch (_) {
    return raw.split('#')[0].split('?')[0]
  }
}

/**
 * Rendu du contenu avec images intégrées
 */
export function renderContentWithImages(content, images = [], options = {}) {
  if (!content) return ''

  const looksLikeHtml = /<\s*(h[1-6]|p|div|table|ul|ol|li|img|section|article|header|footer|span|br|hr)\b/i.test(content)
  let processedText = looksLikeHtml ? content : markdownToHtml(content)

  processedText = unescapeLatex(processedText)
  const { autoShiftHeadings = false, headingOffset = 0 } = options || {}
  if (autoShiftHeadings && /<h1/i.test(processedText)) {
    processedText = shiftHeadingLevels(processedText, 1)
  } else if (headingOffset) {
    processedText = shiftHeadingLevels(processedText, headingOffset)
  }

  if (!images || images.length === 0) {
    return processedText
  }

  const imagesByPosition = {}
  images.forEach((img) => {
    const position = Number.parseInt(img?.position, 10)
    if (Number.isFinite(position) && position > 0 && !imagesByPosition[position]) {
      imagesByPosition[position] = img
    }
  })

  processedText = processedText.replace(/\[\s*IMAGE\s*_?\s*(\d+)\s*\]/gi, (match, position) => {
    const numericPosition = Number.parseInt(position, 10)
    const image = imagesByPosition[numericPosition]
    if (!image) return match

    const src = escapeHtml(getImageUrl(image.image))
    const alt = escapeHtml(resolveImageAlt(image, numericPosition))
    const title = resolveImageTitle(image)
    const titleAttr = title ? ` title="${escapeHtml(title)}"` : ''
    const { width, height } = resolveImageDimensions(image)
    const caption = resolveImageCaption(image)
    const figcaption = caption
      ? `<figcaption class="image-legende" style="text-align: center; margin-top: 8px; font-style: italic; color: #666; font-size: 0.9em;">${escapeHtml(caption)}</figcaption>`
      : ''

    return `
      <figure class="course-figure content-image-container" data-image-position="${numericPosition}" style="text-align: center; margin: 2em 0;">
        <img
          src="${src}"
          loading="lazy"
          decoding="async"
          alt="${alt}"${titleAttr}
          width="${width}"
          height="${height}"
          class="content-image"
          style="max-width: 100%; height: auto;"
        />
        ${figcaption}
      </figure>
    `
  })

  processedText = processedText.replace(/<img(?![^>]*loading=)([^>]*?)>/gi, '<img loading="lazy"$1>')
  processedText = processedText.replace(/<img(?![^>]*decoding=)([^>]*?)>/gi, '<img decoding="async"$1>')

  return processedText
}

/**
 * Construit l'URL complète d'une image
 */
export function getImageUrl(imagePath, type = 'cours') {
  if (imagePath && (imagePath.startsWith('blob:') || imagePath.startsWith('data:'))) {
    return imagePath
  }
  if (imagePath && /^(https?:)?\/\//i.test(imagePath)) {
    return stripUrlQuery(imagePath)
  }

  const isProduction = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1'
  let prodMediaBase = null
  try {
    // eslint-disable-next-line no-undef
    prodMediaBase = (import.meta && import.meta.env)
      ? (import.meta.env.VITE_MEDIA_BASE_URL || import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_URL)
      : null
  } catch (_) {
    prodMediaBase = null
  }
  const baseUrl = isProduction
    ? (prodMediaBase || 'https://optitab-backend.onrender.com')
    : 'http://localhost:8000'

  if (imagePath && imagePath.startsWith('/media/')) {
    return stripUrlQuery(`${baseUrl}${imagePath}`)
  }
  if (imagePath && imagePath.startsWith('media/')) {
    return stripUrlQuery(`${baseUrl}/${imagePath}`)
  }
  if (imagePath && imagePath.includes('/')) {
    return stripUrlQuery(`${baseUrl}/media/${imagePath}`)
  }

  if (imagePath && !imagePath.startsWith('/')) {
    let folder = 'cours_images'
    if (type === 'exercice' || type === 'exercices') folder = 'exercice_images'
    else if (type === 'synthesis' || type === 'sheet' || type === 'sheets') folder = 'synthesis_images'
    else if (type === 'quiz') folder = 'quiz_images'
    return stripUrlQuery(`${baseUrl}/media/${folder}/${imagePath}`)
  }

  return stripUrlQuery(imagePath)
}

/**
 * Rend le contenu MathJax
 */
export function renderMath() {
  const forceRender = () => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      try {
        if (window.MathJax.typesetClear) {
          window.MathJax.typesetClear()
        }
        window.MathJax.typesetPromise().catch((err) => {
          console.warn('[MathJax] Erreur lors du rendu:', err)
        })
      } catch (error) {
        console.warn('[MathJax] Erreur:', error)
      }
    }
  }

  forceRender()
  setTimeout(forceRender, 50)

  let retryCount = 0
  const maxRetries = 8

  const tryRender = () => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      forceRender()
    } else if (retryCount < maxRetries) {
      retryCount += 1
      setTimeout(tryRender, 150)
    } else {
      console.warn('[MathJax] MathJax n\'est pas disponible apres plusieurs tentatives')
    }
  }

  setTimeout(tryRender, 100)
}

/**
 * Composable pour le rendu scientifique
 */
export function useScientificRenderer() {
  return {
    unescapeLatex,
    markdownToHtml,
    renderContentWithImages,
    getImageUrl,
    renderMath
  }
}
