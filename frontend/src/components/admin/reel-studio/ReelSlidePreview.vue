<template>
  <article
    class="slide-card"
    :class="{
      'slide-card--selected': isSelected,
      'slide-card--fullscreen': isLargeDisplayMode,
      'slide-card--clickable': clickable,
      'slide-card--youtube': isYoutubeFormat,
    }"
    :style="slideCardStyle"
    @click="handleSelect"
    @dblclick="handleOpen"
  >
    <div
      class="reel-slide"
      :class="{
        'reel-slide--hook': usesHookLayout,
        'reel-slide--cta': isCtaSlide,
        'reel-slide--cover': isCoverSlide,
        'reel-slide--subtitled': hasVisibleSubtitles,
      }"
    >
      <section class="reel-slide-body" ref="bodyRef">
        <template v-if="showHookTemplate">
          <div ref="screenTextRef" class="hook-layout">
            <p v-if="hookTopText" class="hook-top">{{ hookTopText }}</p>
            <div
              v-if="hasKatex"
              ref="katexZoneRef"
              class="katex-zone hook-katex"
              :class="katexZoneClass"
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
              :class="katexZoneClass"
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
            :class="katexZoneClass"
            v-html="renderedKatex"
          ></div>
        </template>

        <p v-if="katexError" class="screen-text screen-text--error">Formule KaTeX invalide</p>

        <p v-if="!showHookTemplate && !hasScreenText && !hasKatex" class="screen-text screen-text--placeholder">
          Slide vide
        </p>
      </section>

      <AnnotationLayer
        :annotations="safeSlide.annotations || []"
        :editable="annotationEditable"
        :active-tool="annotationActiveTool"
        :active-color="annotationActiveColor"
        :stroke-width="annotationStrokeWidth"
        :selected-id="annotationSelectedId"
        @add="$emit('annotation-add', $event)"
        @update="$emit('annotation-update', $event)"
        @update:selectedId="$emit('annotation-update-selected-id', $event)"
        @delete="$emit('annotation-delete', $event)"
      />

      <div v-if="hasVisibleSubtitles" class="reel-subtitles" aria-hidden="true">
        <template v-if="false">
          <span class="reel-subtitles-text">{{ subtitleText }}</span>
        </template>
        <template v-else>
          <Transition v-if="subtitleHasKaraokeData" name="subtitle-line" mode="out-in">
            <span v-if="subtitleCurrentLine" :key="subtitleCurrentLineIndex" class="reel-subtitles-text">
              <template v-for="(word, idx) in subtitleCurrentLine" :key="`sub-w-${word.globalIndex}`">
                <span
                  class="reel-subtitles-word"
                  :class="{
                    'reel-subtitles-word--active': word.globalIndex === subtitleActiveWordIndex,
                    'reel-subtitles-word--past': word.globalIndex < subtitleActiveWordIndex,
                  }"
                >{{ word.text }}</span>{{ idx < subtitleCurrentLine.length - 1 ? ' ' : '' }}
              </template>
            </span>
          </Transition>
          <span v-else class="reel-subtitles-text">{{ subtitleText }}</span>
        </template>
      </div>
    </div>
  </article>
</template>

<script setup>
import katex from 'katex'
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import AnnotationLayer from './AnnotationLayer.vue'

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
  videoFormat: {
    type: String,
    default: 'reel',
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
  annotationEditable: {
    type: Boolean,
    default: false,
  },
  annotationActiveTool: {
    type: String,
    default: 'select',
  },
  annotationActiveColor: {
    type: String,
    default: '#e74c3c',
  },
  annotationStrokeWidth: {
    type: Number,
    default: 3,
  },
  annotationSelectedId: {
    type: String,
    default: null,
  },
  showSubtitles: {
    type: Boolean,
    default: false,
  },
  subtitleOffsetPercent: {
    type: Number,
    default: null,
  },
  audioCurrentTime: {
    type: Number,
    default: 0,
  },
  audioPlaying: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits([
  'select',
  'diagnostic',
  'open',
  'annotation-add',
  'annotation-update',
  'annotation-update-selected-id',
  'annotation-delete',
])

const screenTextRef = ref(null)
const katexZoneRef = ref(null)
const bodyRef = ref(null)
const thumbnailFitScale = ref(1)

const safeSlide = computed(() => props.slide || {})

const isYoutubeFormat = computed(() => props.videoFormat === 'youtube')
const isHookSlide = computed(() => safeSlide.value.slide_type === 'hook')
const isCtaSlide = computed(() => safeSlide.value.slide_type === 'cta')
const isCoverSlide = computed(() => Boolean(safeSlide.value.is_virtual_cover || safeSlide.value.slide_type === 'cover'))
const usesHookLayout = computed(() => isHookSlide.value || isCoverSlide.value)
const isLargeDisplayMode = computed(() => ['fullscreen', 'export'].includes(props.displayMode))
const isThumbnailMode = computed(() => !isLargeDisplayMode.value)
const shouldSkipLayoutEvaluation = computed(() => isYoutubeFormat.value && props.displayMode === 'fullscreen')
const shouldAlignKatexLeft = computed(() => !usesHookLayout.value && !isCtaSlide.value)

function clampSlideScale(value) {
  return Math.min(2, Math.max(0.5, Number(value) || 1))
}

function clampCumulativeGap(value) {
  const numeric = Number(value)
  if (!Number.isFinite(numeric)) return 0.4
  return Math.min(1.5, Math.max(0, numeric))
}

const slideCardStyle = computed(() => {
  const requestedScale = Math.min(1.3, Math.max(0.75, Number(props.mathScale) || 1))
  const titleScale = clampSlideScale(safeSlide.value.title_scale)
  const screenTextScale = clampSlideScale(safeSlide.value.screen_text_scale)
  const katexScale = clampSlideScale(safeSlide.value.katex_scale)
  const rowGap = clampCumulativeGap(safeSlide.value.display_katex_row_gap_em ?? safeSlide.value.katex_cumulative_gap_em)
  const isYt = isYoutubeFormat.value
  const safeXScale = isYt
    ? Math.min(1.4, Math.max(0, Number(props.safeZoneXScale) || 0))
    : Math.min(1.4, Math.max(0.7, Number(props.safeZoneXScale) || 1))
  const safeYScale = isYt
    ? Math.min(1.4, Math.max(0, Number(props.safeZoneYScale) || 0))
    : Math.min(1.4, Math.max(0.7, Number(props.safeZoneYScale) || 1))
  const safeInlineUnit = isYt ? '3cqw' : '6.5cqw'
  const safeBlockUnit = isYt ? '2.5cqw' : '6.5cqw'
  const safeTopUnit = isYt ? '0cqw' : '16cqw'

  return {
    '--reel-user-scale': requestedScale,
    '--reel-title-scale': titleScale,
    '--reel-screen-text-scale': screenTextScale,
    '--reel-math-scale': requestedScale * katexScale,
    '--reel-katex-row-gap': `${rowGap.toFixed(2)}em`,
    '--reel-thumb-fit-scale': thumbnailFitScale.value,
    '--reel-safe-inline': `calc(${safeInlineUnit} * ${safeXScale.toFixed(3)})`,
    '--reel-safe-block': `calc(${safeBlockUnit} * ${safeYScale.toFixed(3)})`,
    '--reel-safe-top': `calc(${safeTopUnit} * ${safeYScale.toFixed(3)})`,
    '--reel-subtitle-offset': `${subtitleOffsetPercentResolved.value}%`,
  }
})

const subtitleOffsetPercentResolved = computed(() => {
  const v = Number(props.subtitleOffsetPercent)
  if (Number.isFinite(v)) return Math.max(0, Math.min(50, v))
  // Defaults: 20% from bottom for vertical (Reel/TikTok), 12% for horizontal (YouTube)
  return isYoutubeFormat.value ? 12 : 20
})
const screenTextContent = computed(() => {
  const preferred = String(safeSlide.value.display_screen_text || '').trim()
  if (preferred) return preferred
  return String(safeSlide.value.screen_text || '').trim()
})

function stripSubtitleControlTags(value) {
  return String(value || '')
    .replace(/\[[^\]\r\n]*[A-Za-zÀ-ÖØ-öø-ÿ][^\]\r\n]*\]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
}

const subtitleText = computed(() => {
  const candidates = [
    safeSlide.value.voice_script,
    safeSlide.value.speech_text,
  ]
  for (const candidate of candidates) {
    const cleaned = String(candidate || '')
      .replace(/\r\n/g, '\n')
      .replace(/\r/g, '\n')
      .split('\n')
      .map((line) => line.replace(/\s+/g, ' ').trim())
      .filter(Boolean)
      .join(' ')
    const subtitleCleaned = stripSubtitleControlTags(cleaned)
    if (subtitleCleaned) return subtitleCleaned
  }
  return ''
})

const hasVisibleSubtitles = computed(() => (
  props.showSubtitles
  && Boolean(subtitleText.value)
  && props.displayMode !== 'export'
))

const subtitleWordTimings = computed(() => {
  const raw = safeSlide.value.speech_word_timings
  if (!raw || typeof raw !== 'object') return []
  const words = Array.isArray(raw.words) ? raw.words : []
  return words
    .map((entry) => {
      if (!entry || typeof entry !== 'object') return null
      const text = stripSubtitleControlTags(entry.text)
      const start = Number(entry.start)
      const end = Number(entry.end)
      if (!text || !Number.isFinite(start) || !Number.isFinite(end)) return null
      return { text, start, end }
    })
    .filter(Boolean)
})

const subtitleHasKaraokeData = computed(() => subtitleWordTimings.value.length > 0)

const subtitleActiveWordIndex = computed(() => {
  const words = subtitleWordTimings.value
  if (!words.length) return -1
  const t = Number(props.audioCurrentTime) || 0
  if (!props.audioPlaying && t <= 0) return -1
  let activeIndex = -1
  for (let i = 0; i < words.length; i += 1) {
    const word = words[i]
    if (t >= word.start && t <= word.end + 0.05) {
      return i
    }
    if (t >= word.start) {
      activeIndex = i
    } else {
      break
    }
  }
  return activeIndex
})

const SUBTITLE_LINE_MAX_CHARS = 30

const subtitleLines = computed(() => {
  const words = subtitleWordTimings.value
  if (!words.length) return []
  const lines = []
  let line = []
  let chars = 0
  for (let i = 0; i < words.length; i++) {
    const w = words[i]
    const sep = line.length ? 1 : 0
    if (line.length > 0 && chars + sep + w.text.length > SUBTITLE_LINE_MAX_CHARS) {
      lines.push(line)
      line = [{ ...w, globalIndex: i }]
      chars = w.text.length
    } else {
      line.push({ ...w, globalIndex: i })
      chars += sep + w.text.length
    }
  }
  if (line.length) lines.push(line)
  return lines
})

const subtitleCurrentLineIndex = computed(() => {
  const lines = subtitleLines.value
  if (!lines.length) return -1
  const t = Number(props.audioCurrentTime) || 0
  if (!props.audioPlaying && t <= 0) return -1
  let found = -1
  for (let i = 0; i < lines.length; i++) {
    if (t >= lines[i][0].start - 0.05) found = i
    else break
  }
  return found
})

const subtitleCurrentLine = computed(() => {
  const idx = subtitleCurrentLineIndex.value
  return idx >= 0 ? subtitleLines.value[idx] : null
})
const katexContent = computed(() => {
  const preferred = String(safeSlide.value.display_katex || '').trim()
  if (preferred) return preferred
  return String(safeSlide.value.katex || '').trim()
})
const katexRows = computed(() => {
  const rows = Array.isArray(safeSlide.value.display_katex_rows) ? safeSlide.value.display_katex_rows : []
  return rows
    .map((row) => ({
      parts: (Array.isArray(row?.parts) ? row.parts : [])
        .map((part) => stripKatexAlignmentMarkers(part))
        .filter(Boolean),
      inlineSeparators: Array.isArray(row?.inlineSeparators)
        ? row.inlineSeparators.map((value) => normalizeInlineSeparator(value))
        : [],
      inlineOffsetPercent: clampInlineOffset(row?.inlineOffsetPercent),
      inlineVerticalOffsetEm: clampInlineVerticalOffset(row?.inlineVerticalOffsetEm),
    }))
    .filter((row) => row.parts.length)
})
const hasScreenText = computed(() => Boolean(screenTextContent.value))
const hasKatex = computed(() => Boolean(katexContent.value))
const katexRevealWithSpeech = computed(() => (
  Boolean(safeSlide.value.katex_reveal_with_speech)
  && props.displayMode === 'fullscreen'
  && hasKatex.value
))
const katexRevealActive = computed(() => (
  katexRevealWithSpeech.value
  && (props.audioPlaying || Number(props.audioCurrentTime) > 0.03)
))
const katexZoneClass = computed(() => ({
  'katex-zone--speech-reveal': katexRevealWithSpeech.value,
  'katex-zone--speech-reveal-active': katexRevealActive.value,
}))
const currentKatexRevealKeys = computed(() => new Set(
  splitKatexLines(safeSlide.value.katex)
    .map((line) => normalizeKatexRevealKey(line))
    .filter(Boolean)
))
const hookTopText = computed(() => String(safeSlide.value.title || '').trim())
const hookBottomText = computed(() => screenTextContent.value)
const showHookTemplate = computed(
  () => usesHookLayout.value && Boolean(hasKatex.value || hookTopText.value || hookBottomText.value)
)
const showCtaTemplate = computed(() => isCtaSlide.value)
const DEFAULT_CTA_TEXT = 'Abonne-toi à OptiTAB\nSauvegarde ce Reel\nCommente ton résultat'
const INLINE_RIGHT_FRACTION_ONLY_NUDGE_EM = 0.16
const INLINE_LEFT_FRACTION_ONLY_NUDGE_EM = -0.16
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

function stripKatexAlignmentMarkers(value) {
  return String(value || '')
    .trim()
    .replace(/(^|[^\\])&+/g, '$1')
    .replace(/\s+/g, ' ')
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
    .map((line) => stripKatexAlignmentMarkers(line))
    .filter(Boolean)
}

function normalizeKatexRevealKey(value) {
  return stripKatexAlignmentMarkers(value)
    .replace(/\\displaystyle/g, '')
    .replace(/\s+/g, ' ')
    .trim()
}

function isKatexRevealTargetPart(value) {
  if (!katexRevealWithSpeech.value) return false
  const key = normalizeKatexRevealKey(value)
  if (!key) return false
  const currentKeys = currentKatexRevealKeys.value
  if (!currentKeys.size) return true
  return currentKeys.has(key)
}

function katexRevealWeight(value) {
  const key = normalizeKatexRevealKey(value)
    .replace(/\\[a-zA-Z]+/g, 'x')
    .replace(/[{}_^]/g, '')
  return Math.max(1, key.length)
}

function clampInlineOffset(value) {
  const numeric = Number(value)
  if (!Number.isFinite(numeric)) return 0
  return Math.min(40, Math.max(-40, numeric))
}

function clampInlineVerticalOffset(value) {
  const numeric = Number(value)
  if (!Number.isFinite(numeric)) return 0
  return Math.min(1, Math.max(-1, Number(numeric.toFixed(3))))
}

function normalizeInlineSeparator(value) {
  const raw = String(value || '').trim()
  if (raw === 'arrow' || raw === 'none') return raw
  return 'semicolon'
}

function inlineSeparatorKatex(value) {
  const separator = normalizeInlineSeparator(value)
  if (separator === 'none') return ''
  return separator === 'arrow' ? '\\Rightarrow' : ';'
}

function parseKatexEmStyle(style, property) {
  const escapedProperty = property.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const match = String(style || '').match(new RegExp(`(?:^|;)\\s*${escapedProperty}\\s*:\\s*(-?\\d+(?:\\.\\d+)?)em`))
  return match ? Number(match[1]) : 0
}

function katexVerticalMetricsFromHtml(html) {
  let foundStrut = false
  let aboveBaseline = 0
  let belowBaseline = 0
  const strutRegex = /<span class="strut" style="([^"]*)"><\/span>/g

  for (const match of String(html || '').matchAll(strutRegex)) {
    foundStrut = true
    const style = match[1]
    const height = parseKatexEmStyle(style, 'height')
    const verticalAlign = parseKatexEmStyle(style, 'vertical-align')
    aboveBaseline = Math.max(aboveBaseline, height + verticalAlign)
    belowBaseline = Math.max(belowBaseline, -verticalAlign)
  }

  if (!foundStrut) {
    return { aboveBaseline: 0.6944, belowBaseline: 0 }
  }

  return {
    aboveBaseline: Math.max(0, aboveBaseline),
    belowBaseline: Math.max(0, belowBaseline),
  }
}

function formatKatexEmMetric(value) {
  const numeric = Number(value)
  if (!Number.isFinite(numeric) || Math.abs(numeric) < 0.0005) return '0'
  return String(Number(numeric.toFixed(4)))
}

function inlineKatexTopOffsetAttr(offsetEm) {
  const metric = formatKatexEmMetric(offsetEm)
  if (metric === '0') return ''
  return ` top:calc(${metric} * var(--reel-katex-inline-em));`
}

function isTallKatexPart(metrics) {
  const safeMetrics = metrics || {}
  return safeMetrics.belowBaseline > 0.5 || safeMetrics.aboveBaseline > 1.2
}

function inlineKatexVisualNudge(baseMetrics, inlineMetrics) {
  const baseIsTall = isTallKatexPart(baseMetrics)
  const inlineIsTall = isTallKatexPart(inlineMetrics)
  if (inlineIsTall && !baseIsTall) return INLINE_RIGHT_FRACTION_ONLY_NUDGE_EM
  if (baseIsTall && !inlineIsTall) return INLINE_LEFT_FRACTION_ONLY_NUDGE_EM
  return 0
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

function renderInlineKatexPart(expression, separator = 'semicolon', { compact = false } = {}) {
  const cleaned = String(expression || '').trim()
  if (!cleaned) return ''
  const alreadySeparated = /^(;|\\Rightarrow|\\to|\\rightarrow)/.test(cleaned)
  const separatorKatex = inlineSeparatorKatex(separator)
  const separatorSpacing = compact ? '\\;' : '\\quad '
  const separatedExpression = alreadySeparated
    ? cleaned
    : `${separatorKatex ? `${separatorKatex}${separatorSpacing}` : separatorSpacing}${cleaned}`
  return katex.renderToString(`\\displaystyle ${separatedExpression}`, { displayMode: false, throwOnError: false })
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
    let revealIndex = 0
    const revealTargetAttrs = (part) => {
      if (!isKatexRevealTargetPart(part)) return { className: '', attrs: '' }
      const attrs = [
        `data-reel-katex-reveal-index="${revealIndex}"`,
        `data-reel-katex-reveal-weight="${katexRevealWeight(part)}"`,
      ].join(' ')
      revealIndex += 1
      return {
        className: ' reel-katex-reveal-target',
        attrs: ` ${attrs}`,
      }
    }

    if (!shouldAlignKatexLeft.value) {
      const formulaHtml = katex.renderToString(raw, { displayMode: true, throwOnError: false })
      const revealAttrs = revealTargetAttrs(raw)
      return revealAttrs.attrs
        ? `<span class="reel-katex-reveal-target"${revealAttrs.attrs}>${formulaHtml}</span>`
        : formulaHtml
    }

    if (katexRows.value.length) {
      return katexRows.value
        .map((row) => {
          const parts = row.parts
          if (parts.length === 1) {
            const lineHtml = katex.renderToString(parts[0], { displayMode: true, throwOnError: false })
            const revealAttrs = revealTargetAttrs(parts[0])
            const lineContent = revealAttrs.attrs
              ? `<span class="reel-katex-reveal-target"${revealAttrs.attrs}>${lineHtml}</span>`
              : lineHtml
            return `<div class="reel-katex-line">${lineContent}</div>`
          }

          const basePart = parts[0]
          const baseHtml = katex.renderToString(`\\displaystyle ${basePart}`, { displayMode: false, throwOnError: false })
          const baseMetrics = katexVerticalMetricsFromHtml(baseHtml)
          const baseRevealAttrs = revealTargetAttrs(basePart)
          const inlineSeparators = Array.isArray(row.inlineSeparators) ? row.inlineSeparators : []
          const useCompactInlineLayout = isYoutubeFormat.value
          const inlineParts = parts
            .slice(1)
            .map((part, index) => {
              const partHtml = renderInlineKatexPart(part, inlineSeparators[index], { compact: useCompactInlineLayout })
              const revealAttrs = revealTargetAttrs(part)
              const metrics = katexVerticalMetricsFromHtml(partHtml)
              return {
                html: partHtml,
                metrics,
                visualNudge: inlineKatexVisualNudge(baseMetrics, metrics),
                revealAttrs,
              }
            })
          const maxAboveBaseline = Math.max(
            baseMetrics.aboveBaseline,
            ...inlineParts.map((part) => part.metrics.aboveBaseline)
          )
          const maxBelowBaseline = Math.max(
            baseMetrics.belowBaseline,
            ...inlineParts.map((part) => part.metrics.belowBaseline)
          )
          const maxVisualNudge = Math.max(0, ...inlineParts.map((part) => part.visualNudge))
          const rowHeight = maxAboveBaseline + maxBelowBaseline + maxVisualNudge
          const baseIsTall = isTallKatexPart(baseMetrics)
          const allNotTall = !baseIsTall && inlineParts.every((p) => !isTallKatexPart(p.metrics))
          const onlyInlineTall = !baseIsTall && inlineParts.some((p) => isTallKatexPart(p.metrics))
          const rowStyle = (rowHeight > 1.88 && !onlyInlineTall)
            ? ` style="min-height:calc(${formatKatexEmMetric(rowHeight)} * var(--reel-katex-inline-em));"`
            : ''
          const baselineRef = onlyInlineTall ? baseMetrics.aboveBaseline : maxAboveBaseline
          const lineExtraClass = `${allNotTall ? ' reel-katex-line--inline-centered' : ''}${useCompactInlineLayout ? ' reel-katex-line--inline-compact' : ''}`
          const baseStyle = (allNotTall || onlyInlineTall) ? '' : inlineKatexTopOffsetAttr(maxAboveBaseline - baseMetrics.aboveBaseline)
          const baseStyleAttr = baseStyle ? ` style="${baseStyle.trim()}"` : ''
          const offset = clampInlineOffset(row.inlineOffsetPercent)
          const verticalOffset = clampInlineVerticalOffset(row.inlineVerticalOffsetEm)
          const inlineHtml = inlineParts
            .map((inlinePart, index) => {
              const baseTopEm = allNotTall
                ? -0.04
                : (baselineRef - inlinePart.metrics.aboveBaseline + inlinePart.visualNudge)
              const finalTopEm = baseTopEm + verticalOffset
              const topOffset = ` top:calc(${formatKatexEmMetric(finalTopEm)} * var(--reel-katex-inline-em));`
              if (useCompactInlineLayout) {
                const style = `position:relative; left:auto;${topOffset}`
                return `<span class="reel-katex-part reel-katex-part--inline reel-katex-part--inline-compact${inlinePart.revealAttrs.className}" style="${style}"${inlinePart.revealAttrs.attrs}>${inlinePart.html}</span>`
              }
              const left = 50 + offset + index * 22
              const style = `left:${left}%;${topOffset}`
              return `<span class="reel-katex-part reel-katex-part--inline${inlinePart.revealAttrs.className}" style="${style}"${inlinePart.revealAttrs.attrs}>${inlinePart.html}</span>`
            })
            .join('')
          return `<div class="reel-katex-line reel-katex-line--inline${lineExtraClass}"${rowStyle}><span class="reel-katex-part reel-katex-part--base${baseRevealAttrs.className}"${baseStyleAttr}${baseRevealAttrs.attrs}>${baseHtml}</span>${inlineHtml}</div>`
        })
        .join('')
    }

    return splitKatexLines(raw)
      .map((line) => {
        const lineHtml = katex.renderToString(line, { displayMode: true, throwOnError: false })
        const revealAttrs = revealTargetAttrs(line)
        const lineContent = revealAttrs.attrs
          ? `<span class="reel-katex-reveal-target"${revealAttrs.attrs}>${lineHtml}</span>`
          : lineHtml
        return `<div class="reel-katex-line">${lineContent}</div>`
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

function handleOpen() {
  if (!props.clickable) return
  emit('open', safeSlide.value)
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
  const contentEl = (usesHookLayout.value || isCtaSlide.value) ? screenTextRef.value : bodyRef.value
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
  if (shouldSkipLayoutEvaluation.value) {
    thumbnailFitScale.value = 1
    return
  }

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

  const contentEl = (usesHookLayout.value || isCtaSlide.value) ? screenTextRef.value : bodyEl
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

function clamp01(value) {
  const numeric = Number(value)
  if (!Number.isFinite(numeric)) return 0
  return Math.min(1, Math.max(0, numeric))
}

function katexRevealTimelineDuration() {
  const words = subtitleWordTimings.value
  const lastWordEnd = words.reduce((maxEnd, word) => Math.max(maxEnd, Number(word.end) || 0), 0)
  const slideDuration = Number(safeSlide.value.duration_seconds) || 0
  return Math.max(0.5, lastWordEnd || slideDuration || 4)
}

function setKatexRevealProgress(target, progress) {
  const safeProgress = clamp01(progress)
  const clipPercent = Math.round((1 - safeProgress) * 1000) / 10
  target.style.setProperty('--reel-katex-reveal-clip', `${clipPercent}%`)
  target.classList.toggle('reel-katex-reveal-target--active', safeProgress > 0.01 && safeProgress < 0.99)
}

function updateKatexRevealProgress() {
  const zoneEl = katexZoneRef.value
  if (!zoneEl) return

  const targets = Array.from(zoneEl.querySelectorAll('.reel-katex-reveal-target'))
    .sort((a, b) => Number(a.dataset.reelKatexRevealIndex || 0) - Number(b.dataset.reelKatexRevealIndex || 0))
  if (!targets.length) return

  if (!katexRevealActive.value) {
    targets.forEach((target) => setKatexRevealProgress(target, 1))
    return
  }

  const weights = targets.map((target) => Math.max(1, Number(target.dataset.reelKatexRevealWeight) || 1))
  const totalWeight = weights.reduce((sum, weight) => sum + weight, 0) || 1
  const revealDuration = katexRevealTimelineDuration() * 0.94
  const elapsedWeight = clamp01((Number(props.audioCurrentTime) || 0) / Math.max(0.3, revealDuration)) * totalWeight

  let consumedWeight = 0
  targets.forEach((target, index) => {
    const weight = weights[index]
    const progress = (elapsedWeight - consumedWeight) / weight
    setKatexRevealProgress(target, progress)
    consumedWeight += weight
  })
}

watch(
  () => [
    safeSlide.value.title,
    safeSlide.value.screen_text,
    safeSlide.value.display_screen_text,
    safeSlide.value.katex,
    safeSlide.value.display_katex,
    JSON.stringify(safeSlide.value.display_katex_rows || []),
    safeSlide.value.display_katex_row_gap_em,
    safeSlide.value.katex_cumulative_gap_em,
    safeSlide.value.slide_type,
    safeSlide.value.title_scale,
    safeSlide.value.screen_text_scale,
    safeSlide.value.katex_scale,
    props.displayMode,
    props.videoFormat,
    props.mathScale,
    props.safeZoneXScale,
    props.safeZoneYScale,
  ],
  () => {
    evaluateLayout()
  },
  { immediate: true }
)

watch(
  () => [
    props.audioCurrentTime,
    props.audioPlaying,
    katexRevealWithSpeech.value,
    renderedKatex.value,
  ],
  () => {
    updateKatexRevealProgress()
  },
  { immediate: true, flush: 'post' }
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
.reel-slide--cta,
.reel-slide--cover {
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

.reel-slide--cover::before {
  background-image: url('/CoverReel.png');
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

.reel-slide--hook .reel-slide-body,
.reel-slide--cover .reel-slide-body {
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

.reel-slide--hook:not(.reel-slide--cover) .hook-layout {
  transform: translateY(-9cqw);
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
  font-size: calc(25.6px * var(--reel-title-scale, 1) * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
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
  flex: 0 0 auto;
  overflow: visible;
  padding-block: calc(0.4cqw * var(--reel-thumb-fit-scale, 1));
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
  overflow: visible;
  min-height: calc(1.8em * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1));
  padding-block: 0.08em;
}

.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line + .reel-katex-line) {
  margin-top: var(--reel-katex-row-gap, 0.4em);
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

.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line--inline) {
  --reel-katex-inline-em: calc(5cqw * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1));
  position: relative;
  overflow: visible;
}

.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-part) {
  display: inline-block;
  white-space: nowrap;
  top: 0;
  vertical-align: top;
}

.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-part--base) {
  position: relative;
}

.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-part--inline) {
  position: absolute;
}


.katex-zone--speech-reveal :deep(.reel-katex-reveal-target) {
  --reel-katex-reveal-clip: 0%;
  display: inline-block;
  max-width: 100%;
  vertical-align: top;
  clip-path: inset(0 var(--reel-katex-reveal-clip, 0%) 0 0);
  will-change: clip-path;
}

.katex-zone--speech-reveal :deep(.reel-katex-reveal-target > .katex-display) {
  width: auto !important;
  display: inline-block;
}

.katex-zone--speech-reveal-active :deep(.reel-katex-reveal-target) {
  transition: clip-path 0.08s linear;
}

.katex-zone--speech-reveal-active :deep(.reel-katex-reveal-target--active) {
  filter: drop-shadow(0 0 0.04em rgba(37, 99, 235, 0.28));
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
  min-height: calc(1.85em * var(--reel-math-scale, 1));
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
  font-size: calc(35.84px * var(--reel-title-scale, 1) * var(--reel-screen-text-scale, 1));
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
  font-size: calc(7.296cqw * var(--reel-title-scale, 1) * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
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
  min-height: calc(9.4cqw * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1));
  overflow: visible;
}

@media (max-width: 768px) {
  .slide-card--fullscreen {
    width: min(92vw, calc((100dvh - 190px) * 9 / 16));
    min-width: min(82vw, 340px);
  }
}

.slide-card--youtube:not(.slide-card--fullscreen) {
  flex: 0 0 min(680px, calc(100vw - 64px));
  width: min(680px, calc(100vw - 64px));
  min-width: min(680px, calc(100vw - 64px));
}

.slide-card--youtube .reel-slide {
  aspect-ratio: 16 / 9;
}

.slide-card--youtube .reel-slide-body,
.slide-card--youtube.slide-card--fullscreen .reel-slide-body {
  gap: calc(2.4cqw * var(--reel-thumb-fit-scale, 1));
}

.slide-card--youtube .hook-top,
.slide-card--youtube .hook-middle-text,
.slide-card--youtube .hook-bottom,
.slide-card--youtube .cta-top,
.slide-card--youtube .cta-main {
  font-family: Georgia, 'Times New Roman', serif;
  color: #244b9f;
}

.slide-card--youtube .hook-layout,
.slide-card--youtube.slide-card--fullscreen .hook-layout {
  box-sizing: border-box;
  gap: calc(3.4cqw * var(--reel-user-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.slide-card--youtube .reel-slide--hook:not(.reel-slide--cover) .hook-layout {
  transform: translateY(-5cqw);
}

.slide-card--youtube .reel-slide--subtitled.reel-slide--hook:not(.reel-slide--cover) .hook-layout {
  transform: translateY(-7cqw);
  padding-bottom: 5cqw;
}

.slide-card--youtube .hook-top,
.slide-card--youtube.slide-card--fullscreen .hook-top {
  font-size: calc(7.8cqw * var(--reel-title-scale, 1) * var(--reel-thumb-fit-scale, 1));
  line-height: 1.08;
  overflow-wrap: anywhere;
  white-space: normal;
}

.slide-card--youtube .hook-bottom,
.slide-card--youtube.slide-card--fullscreen .hook-bottom {
  font-size: calc(5.2cqw * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
  line-height: 1.12;
  overflow-wrap: anywhere;
  white-space: normal;
}

.slide-card--youtube .hook-middle-text,
.slide-card--youtube.slide-card--fullscreen .hook-middle-text {
  font-size: calc(5.8cqw * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
  line-height: 1.12;
}

.slide-card--youtube .hook-katex :deep(.katex),
.slide-card--youtube.slide-card--fullscreen .hook-katex :deep(.katex) {
  font-size: calc(2.5cqw * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1)) !important;
}

.slide-card--youtube .cta-layout,
.slide-card--youtube.slide-card--fullscreen .cta-layout {
  gap: calc(4.2cqw * var(--reel-user-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.slide-card--youtube .cta-top,
.slide-card--youtube.slide-card--fullscreen .cta-top {
  font-size: calc(7.6cqw * var(--reel-title-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.slide-card--youtube .cta-main,
.slide-card--youtube.slide-card--fullscreen .cta-main {
  font-size: calc(4.8cqw * var(--reel-title-scale, 1) * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.slide-card--youtube .cta-katex :deep(.katex),
.slide-card--youtube.slide-card--fullscreen .cta-katex :deep(.katex) {
  font-size: calc(3.1cqw * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1)) !important;
}

.slide-card--youtube .screen-text,
.slide-card--youtube .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .screen-text,
.slide-card--youtube.slide-card--fullscreen .screen-text {
  font-size: calc(3cqw * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
  line-height: 1.3;
}

.slide-card--youtube .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.katex),
.slide-card--youtube .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line .katex),
.slide-card--youtube.slide-card--fullscreen .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.katex) {
  font-size: calc(1.6cqw * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1)) !important;
}

.slide-card--youtube .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone,
.slide-card--youtube.slide-card--fullscreen .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone {
  gap: calc(2.2cqw * var(--reel-thumb-fit-scale, 1));
}

.slide-card--youtube .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line),
.slide-card--youtube.slide-card--fullscreen .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line) {
  min-height: calc(2.9cqw * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.slide-card--youtube .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line--inline),
.slide-card--youtube.slide-card--fullscreen .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line--inline) {
  --reel-katex-inline-em: calc(1.6cqw * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.slide-card--youtube .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line--inline-compact),
.slide-card--youtube.slide-card--fullscreen .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line--inline-compact) {
  white-space: nowrap;
}

.slide-card--youtube .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line--inline-compact .reel-katex-part--inline),
.slide-card--youtube.slide-card--fullscreen .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line--inline-compact .reel-katex-part--inline) {
  position: relative !important;
  left: auto !important;
}

.slide-card--youtube.slide-card--fullscreen {
  width: min(80vw, calc((100dvh - 180px) * 16 / 9));
  max-width: 860px;
  min-width: min(55vw, 440px);
}

@media (max-width: 768px) {
  .slide-card--youtube.slide-card--fullscreen {
    width: min(92vw, calc((100dvh - 220px) * 16 / 9));
    min-width: min(80vw, 320px);
  }
}

.reel-subtitles {
  position: absolute;
  left: 0;
  right: 0;
  bottom: var(--reel-subtitle-offset, 20%);
  padding: 1cqw 6cqw;
  background: none;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  pointer-events: none;
  z-index: 6;
}

.reel-subtitles-text {
  display: inline;
  max-width: 88%;
  background: none;
  color: #ffffff;
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
  font-weight: 700;
  font-size: calc(3.8cqw * var(--reel-thumb-fit-scale, 1));
  line-height: 1.4;
  letter-spacing: 0.01em;
  text-align: center;
  /* Multi-shadow trick = thick black outline so text stays readable on any slide */
  text-shadow:
    -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000,
    -2px 0 0 #000, 2px 0 0 #000, 0 -2px 0 #000, 0 2px 0 #000,
    0 0 8px rgba(0, 0, 0, 0.65);
  white-space: pre-wrap;
  word-break: break-word;
}

.slide-card--youtube .reel-subtitles {
  padding: 1cqw 7cqw;
}

.slide-card--youtube .reel-subtitles-text {
  max-width: 82%;
  font-size: calc(2.7cqw * var(--reel-thumb-fit-scale, 1));
  line-height: 1.25;
}

.reel-subtitles-word {
  display: inline;
  color: rgba(255, 255, 255, 0.72);
  transition: color 0.08s ease, text-shadow 0.08s ease;
  padding: 0;
}

.reel-subtitles-word--past {
  color: #ffffff;
}

.reel-subtitles-word--active {
  color: #ffffff;
  /* Thick blue halo replaces the black outline → clearly highlights the active word */
  text-shadow:
    -3px -3px 0 #2563eb, 3px -3px 0 #2563eb, -3px 3px 0 #2563eb, 3px 3px 0 #2563eb,
    -3px 0 0 #2563eb, 3px 0 0 #2563eb, 0 -3px 0 #2563eb, 0 3px 0 #2563eb,
    0 0 12px rgba(37, 99, 235, 0.7);
}

.subtitle-line-enter-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.subtitle-line-leave-active {
  transition: opacity 0.1s ease;
}
.subtitle-line-enter-from {
  opacity: 0;
  transform: translateY(4px);
}
.subtitle-line-leave-to {
  opacity: 0;
}
</style>
