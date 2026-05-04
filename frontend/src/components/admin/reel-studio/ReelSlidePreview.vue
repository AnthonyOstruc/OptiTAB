<template>
  <article
    class="slide-card"
    :class="{
      'slide-card--selected': isSelected,
      'slide-card--fullscreen': isLargeDisplayMode,
      'slide-card--clickable': clickable,
    }"
    :style="slideCardStyle"
    @click="handleSelect"
  >
    <div class="reel-slide" :class="{ 'reel-slide--hook': isHookSlide, 'reel-slide--cta': isCtaSlide }">
      <section class="reel-slide-body" ref="bodyRef">
        <template v-if="showHookTemplate">
          <div ref="screenTextRef" class="hook-layout">
            <p v-if="hookTopText" class="hook-top">{{ hookTopText }}</p>
            <div
              v-if="hasKatex"
              ref="katexZoneRef"
              class="katex-zone hook-katex"
              v-html="renderedKatex"
            ></div>
            <div
              v-else-if="hookBottomText"
              class="hook-middle-text rich-text"
              v-html="renderRichText(hookBottomText)"
            ></div>
            <div
              v-if="hasKatex && hookBottomText"
              class="hook-bottom rich-text"
              v-html="renderRichText(hookBottomText)"
            ></div>
          </div>
        </template>

        <template v-else-if="showCtaTemplate">
          <div ref="screenTextRef" class="cta-layout">
            <p v-if="ctaTopText" class="cta-top">{{ ctaTopText }}</p>

            <div
              v-if="hasKatex"
              ref="katexZoneRef"
              class="katex-zone cta-katex"
              v-html="renderedKatex"
            ></div>

            <div v-if="ctaLines.length" class="cta-main">
              <span
                v-for="(line, index) in ctaLines"
                :key="`${index}-${line}`"
                class="cta-line"
                v-html="renderRichTextLine(line)"
              ></span>
            </div>
          </div>
        </template>

        <template v-else>
          <div
            v-if="hasScreenText"
            ref="screenTextRef"
            class="screen-text rich-text"
            v-html="renderRichText(screenTextContent)"
          ></div>

          <div
            v-if="hasKatex"
            ref="katexZoneRef"
            class="katex-zone"
            v-html="renderedKatex"
          ></div>
        </template>

        <p v-if="katexError" class="screen-text screen-text--error">Formule KaTeX invalide</p>

        <p v-if="!showHookTemplate && !hasScreenText && !hasKatex" class="screen-text screen-text--placeholder">
          Slide vide
        </p>
      </section>
    </div>
  </article>
</template>

<script setup>
import katex from 'katex'
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'

const props = defineProps({
  slide: {
    type: Object,
    required: true,
  },
  isSelected: {
    type: Boolean,
    default: false,
  },
  displayMode: {
    type: String,
    default: 'thumb',
  },
  clickable: {
    type: Boolean,
    default: true,
  },
  mathScale: {
    type: Number,
    default: 1,
  },
  safeZoneXScale: {
    type: Number,
    default: 1,
  },
  safeZoneYScale: {
    type: Number,
    default: 1,
  },
})

const emit = defineEmits(['select', 'diagnostic'])

const screenTextRef = ref(null)
const katexZoneRef = ref(null)
const bodyRef = ref(null)
const thumbnailFitScale = ref(1)

const safeSlide = computed(() => props.slide || {})

const isHookSlide = computed(() => safeSlide.value.slide_type === 'hook')
const isCtaSlide = computed(() => safeSlide.value.slide_type === 'cta')
const isLargeDisplayMode = computed(() => ['fullscreen', 'export'].includes(props.displayMode))
const isThumbnailMode = computed(() => !isLargeDisplayMode.value)
const shouldAlignKatexLeft = computed(() => !isHookSlide.value && !isCtaSlide.value)

function clampSlideScale(value) {
  return Math.min(2, Math.max(0.5, Number(value) || 1))
}

const slideCardStyle = computed(() => {
  const requestedScale = Math.min(1.3, Math.max(0.75, Number(props.mathScale) || 1))
  const titleScale = clampSlideScale(safeSlide.value.title_scale)
  const screenTextScale = clampSlideScale(safeSlide.value.screen_text_scale)
  const katexScale = clampSlideScale(safeSlide.value.katex_scale)
  const safeXScale = Math.min(1.4, Math.max(0.7, Number(props.safeZoneXScale) || 1))
  const safeYScale = Math.min(1.4, Math.max(0.7, Number(props.safeZoneYScale) || 1))

  return {
    '--reel-user-scale': requestedScale,
    '--reel-title-scale': titleScale,
    '--reel-screen-text-scale': screenTextScale,
    '--reel-math-scale': requestedScale * katexScale,
    '--reel-thumb-fit-scale': thumbnailFitScale.value,
    '--reel-safe-inline': `calc(6.5cqw * ${safeXScale.toFixed(3)})`,
    '--reel-safe-block': `calc(6.5cqw * ${safeYScale.toFixed(3)})`,
    '--reel-safe-top': `calc(16cqw * ${safeYScale.toFixed(3)})`,
  }
})
const screenTextContent = computed(() => {
  const preferred = String(safeSlide.value.display_screen_text || '').trim()
  if (preferred) return preferred
  return String(safeSlide.value.screen_text || '').trim()
})
const katexContent = computed(() => {
  const preferred = String(safeSlide.value.display_katex || '').trim()
  if (preferred) return preferred
  return String(safeSlide.value.katex || '').trim()
})
const hasScreenText = computed(() => Boolean(screenTextContent.value))
const hasKatex = computed(() => Boolean(katexContent.value))
const hookTopText = computed(() => String(safeSlide.value.title || '').trim())
const hookBottomText = computed(() => screenTextContent.value)
const showHookTemplate = computed(
  () => isHookSlide.value && Boolean(hasKatex.value || hookTopText.value || hookBottomText.value)
)
const showCtaTemplate = computed(() => isCtaSlide.value)
const DEFAULT_CTA_TEXT = 'Abonne-toi à OptiTAB\nSauvegarde ce Reel\nCommente ton résultat'
const LEGACY_CTA_TEXTS = new Set([
  "Abonne-toi à OptiTAB pour d'autres défis maths",
  "Abonne-toi à OptiTAB\npour d'autres défis maths",
  'Abonne-toi à OptiTAB | Sauvegarde ce Reel et commente ton résultat',
  'Abonne-toi à OptiTAB\nSauvegarde ce Reel et commente ton résultat',
  'Abonne-toi pour éviter les pièges',
])

const ctaTopText = computed(() => {
  const rawTitle = String(safeSlide.value.title || '').trim()
  if (rawTitle) return rawTitle
  if (hasKatex.value) return 'Résultat'
  return ''
})
const ctaText = computed(() => {
  const rawText = screenTextContent.value
  if (rawText) {
    return LEGACY_CTA_TEXTS.has(rawText) ? DEFAULT_CTA_TEXT : rawText
  }
  return DEFAULT_CTA_TEXT
})
const ctaLines = computed(() => {
  return ctaText.value
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
})

function isAlignedKatexBlock(value) {
  return /^\\begin\{aligned\}[\s\S]*\\end\{aligned\}$/.test(String(value || '').trim())
}

function unwrapAlignedBlock(value) {
  return String(value || '')
    .trim()
    .replace(/^\\begin\{aligned\}\s*/, '')
    .replace(/\s*\\end\{aligned\}$/, '')
    .trim()
}

function splitKatexLines(value) {
  const raw = String(value || '').trim()
  if (!raw) return []

  const source = (isAlignedKatexBlock(raw) ? unwrapAlignedBlock(raw) : raw)
    .replace(/\\\\(?:\[[^\]]*\])?/g, '\n')
    .replace(/\\\[[^\]]*\]/g, '\n')

  return source
    .split(/\n+/)
    .map((line) => line.trim().replace(/^&+\s*/, '').trim())
    .filter(Boolean)
}

function escapeHtml(value) {
  return String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

function renderTextKatex(expression, displayMode = false) {
  const cleaned = String(expression || '').trim()
  if (!cleaned) return ''

  try {
    return katex.renderToString(cleaned, {
      displayMode,
      throwOnError: false,
    })
  } catch (_) {
    return escapeHtml(expression)
  }
}

function renderRichMathToken(token) {
  const raw = String(token || '')
  if (raw.startsWith('$$') && raw.endsWith('$$')) {
    return renderTextKatex(raw.slice(2, -2), true)
  }
  if (raw.startsWith('\\[') && raw.endsWith('\\]')) {
    return renderTextKatex(raw.slice(2, -2), true)
  }
  if (raw.startsWith('\\(') && raw.endsWith('\\)')) {
    return renderTextKatex(raw.slice(2, -2), false)
  }
  if (raw.startsWith('$') && raw.endsWith('$')) {
    return renderTextKatex(raw.slice(1, -1), false)
  }
  return escapeHtml(raw)
}

function renderRichTextLine(line) {
  const raw = String(line || '')
  const katexDirective = raw.trim().match(/^KATEX\s*:\s*(.+)$/i)
  if (katexDirective) {
    return renderTextKatex(katexDirective[1], true)
  }

  const tokenPattern = /(\$\$[\s\S]+?\$\$|\\\[[\s\S]+?\\\]|\\\([\s\S]+?\\\)|\$[^$\n]+?\$)/g
  let html = ''
  let lastIndex = 0

  for (const match of raw.matchAll(tokenPattern)) {
    html += escapeHtml(raw.slice(lastIndex, match.index))
    html += renderRichMathToken(match[0])
    lastIndex = match.index + match[0].length
  }

  html += escapeHtml(raw.slice(lastIndex))
  return html
}

function renderRichText(value) {
  return String(value || '')
    .replace(/\r\n/g, '\n')
    .split('\n')
    .map((line) => {
      if (!line.trim()) {
        return '<span class="rich-text-line rich-text-line--empty">&nbsp;</span>'
      }
      return `<span class="rich-text-line">${renderRichTextLine(line)}</span>`
    })
    .join('')
}

const katexError = computed(() => {
  const raw = katexContent.value
  if (!raw) return ''
  try {
    if (shouldAlignKatexLeft.value) {
      for (const line of splitKatexLines(raw)) {
        katex.renderToString(line, { displayMode: true, throwOnError: true })
      }
    } else {
      katex.renderToString(raw, { displayMode: true, throwOnError: true })
    }
    return ''
  } catch (error) {
    return String(error?.message || 'KaTeX invalide')
  }
})

const renderedKatex = computed(() => {
  const raw = katexContent.value
  if (!raw) return ''
  try {
    if (!shouldAlignKatexLeft.value) {
      return katex.renderToString(raw, { displayMode: true, throwOnError: false })
    }

    return splitKatexLines(raw)
      .map((line) => {
        const lineHtml = katex.renderToString(line, { displayMode: true, throwOnError: false })
        return `<div class="reel-katex-line">${lineHtml}</div>`
      })
      .join('')
  } catch (_) {
    return ''
  }
})

const diagnostic = ref({
  status: 'unchecked',
  label: 'À vérifier',
  notes: '',
})

function handleSelect() {
  if (!props.clickable) return
  emit('select', safeSlide.value)
}

async function fitThumbnailContent() {
  const fitResult = { hasHardOverflow: false }

  // The preview must be a proportional reduction of fullscreen, not a reflowed layout.
  thumbnailFitScale.value = 1
  await nextTick()

  if (!isThumbnailMode.value) {
    return fitResult
  }

  const zoneEl = katexZoneRef.value
  const contentEl = (isHookSlide.value || isCtaSlide.value) ? screenTextRef.value : bodyRef.value
  if (!zoneEl && !contentEl) return fitResult

  const bodyEl = bodyRef.value
  const lineEls = zoneEl
    ? Array.from(zoneEl.querySelectorAll('.reel-katex-line .katex'))
    : []
  const katexEls = zoneEl && lineEls.length
    ? lineEls
    : Array.from(zoneEl?.querySelectorAll('.katex') || [])
  const availableWidth = Math.max((zoneEl || contentEl).clientWidth - 2, 1)
  const widestLine = katexEls.reduce((maxWidth, lineEl) => {
    const rect = lineEl.getBoundingClientRect()
    return Math.max(maxWidth, lineEl.scrollWidth || 0, rect.width || 0)
  }, 0)

  const heightTargetEl = contentEl || bodyEl

  fitResult.hasHardOverflow = Boolean(
    widestLine > availableWidth
      || (heightTargetEl && heightTargetEl.scrollHeight > heightTargetEl.clientHeight)
      || (contentEl && contentEl.scrollWidth > contentEl.clientWidth)
  )
  return fitResult
}

const evaluateLayout = async () => {
  await nextTick()
  const fitResult = await fitThumbnailContent()

  const notes = []
  const textEl = screenTextRef.value
  const katexEl = katexZoneRef.value
  const bodyEl = bodyRef.value

  if (katexEl) {
    katexEl.scrollLeft = 0
  }

  const textOverflowX = Boolean(
    textEl
      && textEl.scrollWidth > textEl.clientWidth
      && (!isThumbnailMode.value || fitResult.hasHardOverflow)
  )
  const formulaOverflowX = Boolean(
    katexEl
      && (
        fitResult.hasHardOverflow
        || (katexEl.scrollWidth > katexEl.clientWidth && !isThumbnailMode.value)
      )
  )

  if (textOverflowX) notes.push('Texte horizontalement trop long')
  if (formulaOverflowX) notes.push('Formule trop large')

  const contentEl = (isHookSlide.value || isCtaSlide.value) ? screenTextRef.value : bodyEl
  const bodyOverflow = Boolean(
    (
      (bodyEl && bodyEl.scrollHeight > bodyEl.clientHeight)
      || (contentEl && contentEl.scrollHeight > contentEl.clientHeight)
    )
    && (!isThumbnailMode.value || fitResult.hasHardOverflow)
  )
  if (bodyOverflow) notes.push('Contenu coupé en bas')

  let status = 'ok'
  let label = 'OK'

  if (katexError.value) {
    status = 'error'
    label = 'À vérifier'
    notes.push('KaTeX invalide')
  } else if (formulaOverflowX) {
    status = 'warning'
    label = 'Formule trop large'
  } else if (textOverflowX) {
    status = 'warning'
    label = 'Texte trop large'
  } else if (bodyOverflow) {
    status = 'warning'
    label = 'Bas coupé'
  }

  diagnostic.value = {
    status,
    label,
    notes: notes.join(' | '),
  }

  emit('diagnostic', {
    slideId: safeSlide.value.id,
    status,
    label,
    notes: diagnostic.value.notes,
  })
}

watch(
  () => [
    safeSlide.value.title,
    safeSlide.value.screen_text,
    safeSlide.value.display_screen_text,
    safeSlide.value.katex,
    safeSlide.value.display_katex,
    safeSlide.value.slide_type,
    safeSlide.value.title_scale,
    safeSlide.value.screen_text_scale,
    safeSlide.value.katex_scale,
    props.displayMode,
    props.mathScale,
    props.safeZoneXScale,
    props.safeZoneYScale,
  ],
  () => {
    evaluateLayout()
  },
  { immediate: true }
)

function handleResize() {
  evaluateLayout()
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
  evaluateLayout()

  if (typeof document !== 'undefined' && document.fonts?.ready) {
    document.fonts.ready.then(() => evaluateLayout()).catch(() => {})
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.slide-card {
  flex: 0 0 230px;
  width: 230px;
  min-width: 230px;
  border-radius: 14px;
  border: 1px solid #bfdbfe;
  background: #f8fbff;
  padding: 8px;
  transition: border-color 0.18s ease, box-shadow 0.18s ease;
}

.slide-card--clickable {
  cursor: pointer;
}

.slide-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.18);
}

.slide-card--selected {
  border-color: #1d4ed8;
  box-shadow: 0 0 0 3px rgba(29, 78, 216, 0.18);
}

.slide-card--fullscreen {
  width: min(88vw, calc((100dvh - 150px) * 9 / 16));
  max-width: 460px;
  min-width: min(72vw, 300px);
  padding: 10px;
  border-radius: 18px;
  border-color: #93c5fd;
  box-shadow: 0 20px 48px rgba(29, 78, 216, 0.28);
}

.slide-card--fullscreen:hover {
  transform: none;
  border-color: #93c5fd;
  box-shadow: 0 20px 48px rgba(29, 78, 216, 0.28);
}

.reel-slide {
  width: 100%;
  aspect-ratio: 9 / 16;
  display: block;
  border-radius: 12px;
  overflow: hidden;
  position: relative;
  background: #f8fbff;
  border: 1px solid #bfdbfe;
}

.reel-slide--hook,
.reel-slide--cta {
  display: block;
}

.reel-slide::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url('/CoverReelOptiTAB.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: 0;
}

.reel-slide-body {
  --reel-safe-padding: var(--reel-safe-inline, 16px);
  --reel-safe-block-padding: var(--reel-safe-block, 16px);
  --reel-top-safe-offset: var(--reel-safe-top, 42px);
  width: 100%;
  height: 100%;
  padding: calc(var(--reel-safe-block-padding) + var(--reel-top-safe-offset))
    var(--reel-safe-padding)
    var(--reel-safe-block-padding);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 12px;
  text-align: left;
  min-height: 0;
  overflow: hidden;
  position: relative;
  z-index: 1;
}

.reel-slide--hook .reel-slide-body {
  --reel-top-safe-offset: 0px;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.reel-slide--cta .reel-slide-body {
  --reel-top-safe-offset: 0px;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.hook-layout {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: calc(20px * var(--reel-user-scale, 1) * var(--reel-thumb-fit-scale, 1));
  padding: 0;
  color: #244b9f;
  text-align: center;
  overflow: hidden;
}

.hook-top,
.hook-middle-text,
.hook-bottom {
  margin: 0;
  font-family: Georgia, 'Times New Roman', serif;
  line-height: 1.12;
  letter-spacing: 0.01em;
  color: #244b9f;
}

.hook-top,
.hook-bottom {
  width: 100%;
  text-align: left;
  white-space: nowrap;
}

.hook-top {
  font-size: calc(36px * var(--reel-title-scale, 1) * var(--reel-thumb-fit-scale, 1));
  font-weight: 500;
}

.hook-middle-text {
  font-size: calc(40px * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
  font-weight: 500;
}

.hook-bottom {
  font-size: calc(34px * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
  font-weight: 500;
}

.hook-katex {
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
  overflow-y: hidden;
  text-align: left;
}

.hook-katex :deep(.katex-display) {
  width: 100%;
  display: block;
  margin: 0.1em 0;
  text-align: left !important;
}

.hook-katex :deep(.katex-display > .katex) {
  display: inline-block !important;
  margin-left: 0 !important;
  margin-right: auto !important;
  text-align: left !important;
}

.hook-katex :deep(.katex-display > .katex > .katex-html) {
  text-align: left !important;
}

.hook-katex :deep(.katex) {
  font-size: calc(2rem * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1));
  color: #244b9f;
}

.slide-card:not(.slide-card--fullscreen) .hook-layout {
  gap: calc(12px * var(--reel-user-scale, 1) * var(--reel-thumb-fit-scale, 1));
  padding: 0;
}

.slide-card:not(.slide-card--fullscreen) .hook-top,
.slide-card:not(.slide-card--fullscreen) .hook-bottom {
  font-size: calc(26px * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.slide-card:not(.slide-card--fullscreen) .hook-top {
  font-size: calc(26px * var(--reel-title-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.slide-card:not(.slide-card--fullscreen) .hook-middle-text {
  font-size: calc(24px * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.slide-card:not(.slide-card--fullscreen) .hook-katex :deep(.katex) {
  font-size: calc(2.15rem * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.cta-layout {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  gap: calc(22px * var(--reel-user-scale, 1) * var(--reel-thumb-fit-scale, 1));
  padding: 0;
  color: #244b9f;
  text-align: left;
  overflow: hidden;
}

.cta-top,
.cta-main {
  margin: 0;
  font-family: Georgia, 'Times New Roman', serif;
  line-height: 1.2;
  letter-spacing: 0.01em;
  color: #244b9f;
}

.cta-top {
  width: 100%;
  font-size: calc(40px * var(--reel-title-scale, 1) * var(--reel-thumb-fit-scale, 1));
  font-weight: 500;
  text-align: left;
}

.cta-katex {
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
  overflow-y: hidden;
  text-align: left;
}

.cta-katex :deep(.katex-display) {
  width: 100%;
  display: block;
  margin: 0.05em 0;
  text-align: left !important;
}

.cta-katex :deep(.katex-display > .katex) {
  display: inline-block !important;
  margin-left: 0 !important;
  margin-right: auto !important;
  text-align: left !important;
}

.cta-katex :deep(.katex-display > .katex > .katex-html) {
  text-align: left !important;
}

.cta-katex :deep(.katex) {
  font-size: calc(2rem * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1));
  color: #244b9f;
}

.cta-main {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: calc(1.6cqw * var(--reel-user-scale, 1) * var(--reel-thumb-fit-scale, 1));
  font-size: calc(32px * var(--reel-title-scale, 1) * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
  font-weight: 500;
  text-align: left;
}

.cta-line {
  display: block;
  max-width: 100%;
  white-space: nowrap;
}

.rich-text {
  white-space: normal;
}

.rich-text :deep(.rich-text-line) {
  display: block;
  max-width: 100%;
}

.rich-text :deep(.rich-text-line--empty) {
  min-height: 1em;
}

.rich-text :deep(.katex) {
  color: inherit;
  font-size: 0.98em;
}

.rich-text :deep(.katex-display) {
  width: 100%;
  display: block;
  margin: 0.08em 0;
  text-align: left !important;
}

.rich-text :deep(.katex-display > .katex) {
  display: inline-block !important;
  margin-left: 0 !important;
  margin-right: auto !important;
  text-align: left !important;
}

.rich-text :deep(.katex-display > .katex > .katex-html) {
  text-align: left !important;
}

.screen-text {
  margin: 0;
  color: #1e3a8a;
  font-size: 14px;
  font-weight: 700;
  line-height: 1.35;
  max-width: 100%;
  overflow-wrap: anywhere;
}

.screen-text--placeholder {
  color: #60a5fa;
  font-size: 13px;
  font-weight: 600;
}

.screen-text--error {
  color: #1d4ed8;
  font-size: 12px;
  font-weight: 700;
}

.katex-zone {
  width: 100%;
  max-width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
}

.katex-zone :deep(.katex-display) {
  margin: 0;
}

.katex-zone :deep(.katex) {
  font-size: calc(0.9rem * var(--reel-math-scale, 1));
  color: #1e3a8a;
}

.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.katex) {
  font-size: calc(0.9rem * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1)) !important;
}

.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .screen-text,
.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone {
  width: 100%;
  text-align: left;
}

.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .screen-text {
  font-size: calc(14px * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: clamp(7px, calc(12px * var(--reel-thumb-fit-scale, 1)), 12px);
  overflow-x: hidden;
}

.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.katex-display) {
  width: 100%;
  display: block;
  margin: 0 !important;
  text-align: left !important;
}

.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.katex-display > .katex) {
  display: inline-block !important;
  margin-left: 0 !important;
  margin-right: auto !important;
  text-align: left !important;
}

.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.katex-display > .katex > .katex-html) {
  text-align: left !important;
}

.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line) {
  width: 100%;
  max-width: 100%;
  display: block;
  text-align: left;
  overflow: hidden;
  min-height: 1.45em;
}

.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line .katex-display) {
  width: 100%;
  margin: 0 !important;
  text-align: left !important;
}

.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line .katex) {
  display: inline-block;
  max-width: none;
  text-align: left;
  white-space: nowrap;
  font-size: calc(0.9rem * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1)) !important;
}

.slide-card--fullscreen .reel-slide-body {
  --reel-safe-padding: var(--reel-safe-inline, 28px);
  --reel-safe-block-padding: var(--reel-safe-block, 28px);
  --reel-top-safe-offset: var(--reel-safe-top, 60px);
}

.slide-card--fullscreen .screen-text {
  font-size: clamp(22px, 2.2vw, 32px);
  line-height: 1.3;
}

.slide-card--fullscreen .screen-text--placeholder {
  font-size: clamp(16px, 1.7vw, 20px);
}

.slide-card--fullscreen .screen-text--error {
  font-size: 14px;
}

.slide-card--fullscreen .katex-zone :deep(.katex) {
  font-size: calc(1.35rem * var(--reel-math-scale, 1));
}

.slide-card--fullscreen .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.katex) {
  font-size: calc(1.35rem * var(--reel-math-scale, 1)) !important;
}

.slide-card--fullscreen .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone {
  gap: 16px;
}

.slide-card--fullscreen .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line) {
  min-height: 1.55em;
}

.slide-card--fullscreen .hook-layout {
  gap: calc(26px * var(--reel-user-scale, 1));
  padding: 0;
}

.slide-card--fullscreen .hook-top {
  font-size: calc(54px * var(--reel-title-scale, 1));
}

.slide-card--fullscreen .hook-bottom {
  font-size: calc(50px * var(--reel-screen-text-scale, 1));
}

.slide-card--fullscreen .hook-middle-text {
  font-size: calc(56px * var(--reel-screen-text-scale, 1));
}

.slide-card--fullscreen .hook-katex :deep(.katex) {
  font-size: calc(2.8rem * var(--reel-math-scale, 1));
}

.slide-card--fullscreen .cta-layout {
  gap: calc(28px * var(--reel-user-scale, 1));
  padding: 0;
}

.slide-card--fullscreen .cta-top {
  font-size: calc(56px * var(--reel-title-scale, 1));
}

.slide-card--fullscreen .cta-main {
  font-size: calc(44.8px * var(--reel-title-scale, 1) * var(--reel-screen-text-scale, 1));
}

.slide-card--fullscreen .cta-katex :deep(.katex) {
  font-size: calc(2.8rem * var(--reel-math-scale, 1));
}

.reel-slide {
  container-type: inline-size;
}

.reel-slide-body,
.slide-card--fullscreen .reel-slide-body {
  --reel-safe-padding: var(--reel-safe-inline, 6.5cqw);
  --reel-safe-block-padding: var(--reel-safe-block, 6.5cqw);
  --reel-top-safe-offset: var(--reel-safe-top, 13.5cqw);
  gap: calc(3.7cqw * var(--reel-thumb-fit-scale, 1));
}

.hook-layout,
.slide-card:not(.slide-card--fullscreen) .hook-layout,
.slide-card--fullscreen .hook-layout {
  gap: calc(6cqw * var(--reel-user-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.hook-top,
.slide-card:not(.slide-card--fullscreen) .hook-top,
.slide-card--fullscreen .hook-top {
  font-size: calc(11.4cqw * var(--reel-title-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.hook-bottom,
.slide-card:not(.slide-card--fullscreen) .hook-bottom,
.slide-card--fullscreen .hook-bottom {
  font-size: calc(8.4cqw * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
  white-space: nowrap;
}

.hook-middle-text,
.slide-card:not(.slide-card--fullscreen) .hook-middle-text,
.slide-card--fullscreen .hook-middle-text {
  font-size: calc(12cqw * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.hook-katex :deep(.katex),
.slide-card:not(.slide-card--fullscreen) .hook-katex :deep(.katex),
.slide-card--fullscreen .hook-katex :deep(.katex) {
  font-size: calc(7.4cqw * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1)) !important;
}

.cta-layout,
.slide-card--fullscreen .cta-layout {
  gap: calc(7cqw * var(--reel-user-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.cta-top,
.slide-card--fullscreen .cta-top {
  font-size: calc(8.4cqw * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.cta-top,
.slide-card--fullscreen .cta-top {
  font-size: calc(11.4cqw * var(--reel-title-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.cta-main,
.slide-card--fullscreen .cta-main {
  font-size: calc(9.12cqw * var(--reel-title-scale, 1) * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.cta-katex :deep(.katex),
.slide-card--fullscreen .cta-katex :deep(.katex) {
  font-size: calc(10.5cqw * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1)) !important;
}

.screen-text,
.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .screen-text,
.slide-card--fullscreen .screen-text {
  font-size: calc(4.8cqw * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.katex),
.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line .katex),
.slide-card--fullscreen .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.katex) {
  font-size: calc(5cqw * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1)) !important;
}

.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone,
.slide-card--fullscreen .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone {
  gap: calc(3.7cqw * var(--reel-thumb-fit-scale, 1));
}

.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line),
.slide-card--fullscreen .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line) {
  min-height: calc(7.7cqw * var(--reel-thumb-fit-scale, 1));
}

@media (max-width: 768px) {
  .slide-card--fullscreen {
    width: min(92vw, calc((100dvh - 190px) * 9 / 16));
    min-width: min(82vw, 340px);
  }
}
</style>
