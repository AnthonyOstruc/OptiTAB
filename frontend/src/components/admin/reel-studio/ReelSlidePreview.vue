<template>
  <article
    class="slide-card"
    :class="{
      'slide-card--selected': isSelected,
      'slide-card--fullscreen': isLargeDisplayMode,
      'slide-card--clickable': clickable,
      'slide-card--youtube': isYoutubeFormat,
      'slide-card--carousel': isCarouselFormat,
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
        'reel-slide--generated': hasGeneratedImage,
      }"
    >
      <img
        v-if="hasGeneratedImage"
        class="reel-slide-generated-image"
        :src="safeSlide.generated_image_url"
        alt=""
        crossorigin="anonymous"
        decoding="async"
      />
      <div
        v-if="hasGeneratedImage && isCarouselFormat"
        class="reel-slide-generated-scrim"
        aria-hidden="true"
      ></div>

      <section v-if="isCarouselFormat" class="carousel-template" :class="{
        'carousel-template--cover': isCarouselCoverSlide,
        'carousel-template--content': isCarouselContentSlide,
        'carousel-template--cta': isCarouselCtaSlide,
        'carousel-template--on-image': hasGeneratedImage,
      }" :style="carouselTemplateStyle" ref="bodyRef">
        <header class="carousel-template__topbar">
          <span class="carousel-template__brand">
            <img
              src="/Logo_bg.png"
              alt="OptiTAB"
              class="carousel-template__brand-logo"
              draggable="false"
            />
          </span>
          <span v-if="carouselPageLabel" class="carousel-template__page">{{ carouselPageLabel }}</span>
        </header>

        <span
          v-if="hasGeneratedImage && isCarouselCoverSlide"
          class="carousel-template__floating-eyebrow carousel-template__floating-eyebrow--cover"
        >optitab.net</span>
        <span
          v-if="hasGeneratedImage && isCarouselCtaSlide"
          class="carousel-template__floating-eyebrow carousel-template__floating-eyebrow--cta"
        >À toi de jouer</span>

        <div class="carousel-template__main">
          <template v-if="isCarouselCoverSlide">
            <span class="carousel-template__eyebrow">optitab.net</span>
            <h1
              v-if="carouselTitleText"
              class="carousel-template__cover-title rich-text"
              v-html="renderRichText(carouselTitleText)"
            ></h1>
            <p
              v-if="carouselCoverSubtitle"
              class="carousel-template__cover-sub rich-text"
              v-html="renderRichText(carouselCoverSubtitle)"
            ></p>
            <div v-if="hasKatex" class="carousel-template__cover-katex" :style="carouselKatexInlineStyle" v-html="renderedKatex"></div>
            <span class="carousel-template__swipe" aria-hidden="true">
              <span class="carousel-template__swipe-text">Glisse</span>
              <span class="carousel-template__swipe-arrow">→</span>
            </span>
          </template>

          <template v-else-if="isCarouselCtaSlide">
            <span class="carousel-template__cta-eyebrow">À toi de jouer</span>
            <h2
              v-if="carouselTitleText"
              class="carousel-template__cta-title rich-text"
              v-html="renderRichText(carouselTitleText)"
            ></h2>
            <ul v-if="carouselTextLines.length" class="carousel-template__cta-list">
              <li
                v-for="(line, i) in carouselTextLines"
                :key="`cta-line-${i}-${line}`"
                class="carousel-template__cta-item rich-text"
                :style="lineInlineStyle(line)"
                v-html="renderRichTextLine(lineBody(line))"
              ></li>
            </ul>
            <div v-if="hasKatex" class="carousel-template__cta-katex" :style="carouselKatexInlineStyle" v-html="renderedKatex"></div>
            <div class="carousel-template__cta-url-wrap">
              <span class="carousel-template__cta-url">optitab.net</span>
              <span class="carousel-template__cta-underline" aria-hidden="true"></span>
            </div>
            <div class="carousel-template__cta-button">
              <span>Abonne-toi sans engagement</span>
              <span class="carousel-template__cta-button-arrow" aria-hidden="true">→</span>
            </div>
          </template>

          <template v-else>
            <span class="carousel-template__step" aria-hidden="true">{{ String(safeSlide.order || '').padStart(2, '0') }}</span>
            <h2
              v-if="carouselTitleText"
              class="carousel-template__title rich-text"
              v-html="renderRichText(carouselTitleText)"
            ></h2>
            <div class="carousel-template__accent" aria-hidden="true"></div>
            <ul
              v-if="carouselTextLines.length"
              class="carousel-template__text-list"
              :class="{
                'carousel-template__text-list--quiz': isQuizSlide,
                'carousel-template__text-list--reveal': isAnswerRevealSlide,
              }"
            >
              <li
                v-for="(line, i) in carouselTextLines"
                :key="`ct-line-${i}-${line}`"
                class="carousel-template__text-item rich-text"
                :class="{
                  'carousel-template__text-item--quiz-question': quizLineKind(line) === 'question',
                  'carousel-template__text-item--quiz-option': quizLineKind(line) === 'option',
                  'carousel-template__text-item--reveal': isAnswerRevealSlide,
                }"
                :style="lineInlineStyle(line)"
              >
                <template v-if="quizLineKind(line) === 'option'">
                  <span class="carousel-template__quiz-letter">{{ quizLetter(line) }}</span>
                  <span class="carousel-template__quiz-content" v-html="renderRichTextLine(quizContent(line))"></span>
                </template>
                <template v-else>
                  <span v-html="renderRichTextLine(lineBody(line))"></span>
                </template>
              </li>
            </ul>
            <div v-if="hasKatex" class="carousel-template__katex" :style="carouselKatexInlineStyle" v-html="renderedKatex"></div>
          </template>
        </div>

        <footer class="carousel-template__bottombar" v-if="!isCarouselCoverSlide">
          <span class="carousel-template__url">optitab.net</span>
        </footer>
      </section>

      <section v-if="!hasGeneratedImage && !isCarouselFormat" class="reel-slide-body" ref="bodyRef">
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
          <div v-if="splitMeta" class="reel-slide-split">
            <div class="reel-slide-split__left">
              <div
                v-if="hasNormalTitle"
                class="slide-title rich-text"
                v-html="renderRichText(normalTitleText)"
              ></div>

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
            </div>

            <aside class="reel-slide-split__right" aria-label="Méthode de référence">
              <p v-if="splitMeta.label" class="reel-slide-split__label">{{ splitMeta.label }}</p>
              <div
                v-if="renderedSplitRightKatex"
                class="reel-slide-split__katex"
                v-html="renderedSplitRightKatex"
              ></div>
            </aside>
          </div>

          <template v-else>
            <div
              v-if="hasNormalTitle"
              class="slide-title rich-text"
              v-html="renderRichText(normalTitleText)"
            ></div>

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
        </template>

        <p v-if="katexError" class="screen-text screen-text--error">Formule KaTeX invalide</p>

        <p v-if="!showHookTemplate && !hasNormalTitle && !hasScreenText && !hasKatex" class="screen-text screen-text--placeholder">
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

    <button
      v-if="showCarouselImageToggle"
      type="button"
      class="carousel-image-toggle"
      :class="{ 'carousel-image-toggle--off': carouselImageHidden }"
      :title="carouselImageHidden ? 'Afficher l image Gemini sur cette slide' : 'Masquer l image Gemini sur cette slide'"
      :aria-label="carouselImageHidden ? 'Afficher l image Gemini' : 'Masquer l image Gemini'"
      @click.stop="toggleCarouselImage"
      @dblclick.stop
    >
      <svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true">
        <path
          v-if="!carouselImageHidden"
          d="M4 5h16v14H4zM4 15l4.5-4.5L13 15l3-3 4 4"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linejoin="round"
          stroke-linecap="round"
        />
        <g v-else fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M4 5h16v14H4z" />
          <path d="M4 5l16 14" />
        </g>
      </svg>
      <span class="carousel-image-toggle__label">{{ carouselImageHidden ? 'Image OFF' : 'Image ON' }}</span>
    </button>
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
  splitRightScale: {
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
  totalSlides: {
    type: Number,
    default: 0,
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
  'toggle-carousel-image',
])

const screenTextRef = ref(null)
const katexZoneRef = ref(null)
const bodyRef = ref(null)
const thumbnailFitScale = ref(1)

const safeSlide = computed(() => props.slide || {})

const splitMeta = computed(() => {
  const raw = String(safeSlide.value.layout_notes || '').trim()
  if (!raw) return null
  let parsed = null
  try {
    parsed = JSON.parse(raw)
  } catch (_) {
    return null
  }
  const block = parsed && typeof parsed === 'object' ? parsed.split : null
  if (!block || typeof block !== 'object') return null
  const label = String(block.label || '').trim()
  const rightKatex = String(block.right_katex || '').trim()
  if (!label && !rightKatex) return null
  return { label, rightKatex }
})

const renderedSplitRightKatex = computed(() => {
  const meta = splitMeta.value
  if (!meta || !meta.rightKatex) return ''
  return splitKatexLines(meta.rightKatex)
    .map((line) => {
      try {
        return `<div class="reel-slide-split__katex-line">${katex.renderToString(line, { displayMode: true, throwOnError: false })}</div>`
      } catch (_) {
        return `<div class="reel-slide-split__katex-line">${escapeHtml(line)}</div>`
      }
    })
    .join('')
})

const isYoutubeFormat = computed(() => props.videoFormat === 'youtube')
const isCarouselFormat = computed(() => props.videoFormat === 'carousel')
const carouselImageHidden = computed(() => {
  const raw = String(safeSlide.value.layout_notes || '').trim()
  if (!raw) return false
  try {
    const parsed = JSON.parse(raw)
    return Boolean(parsed && parsed.hide_carousel_image)
  } catch (_) {
    return false
  }
})
const hasGeneratedImageRaw = computed(() => Boolean(safeSlide.value.generated_image_url))
const hasGeneratedImage = computed(() => (
  hasGeneratedImageRaw.value
  && !(isCarouselFormat.value && carouselImageHidden.value)
))
const isHookSlide = computed(() => safeSlide.value.slide_type === 'hook')
const isCtaSlide = computed(() => safeSlide.value.slide_type === 'cta')
const isCoverSlide = computed(() => Boolean(safeSlide.value.is_virtual_cover || safeSlide.value.slide_type === 'cover'))
const usesHookLayout = computed(() => isHookSlide.value || isCoverSlide.value)
const isLargeDisplayMode = computed(() => ['fullscreen', 'export'].includes(props.displayMode))
const isThumbnailMode = computed(() => !isLargeDisplayMode.value)
const shouldSkipLayoutEvaluation = computed(() => isCarouselFormat.value || hasGeneratedImage.value || (isYoutubeFormat.value && props.displayMode === 'fullscreen'))
const shouldAlignKatexLeft = computed(() => !usesHookLayout.value && !isCtaSlide.value && !isCarouselFormat.value)

function clampSlideScale(value) {
  return Math.min(2, Math.max(0.5, Number(value) || 1))
}

function clampCumulativeGap(value) {
  const numeric = Number(value)
  if (!Number.isFinite(numeric)) return 0.4
  return Number(numeric.toFixed(2))
}

const slideCardStyle = computed(() => {
  const numericScale = Number(props.mathScale)
  const requestedScale = Number.isFinite(numericScale) ? Math.max(0.05, numericScale) : 1
  const titleScale = clampSlideScale(safeSlide.value.title_scale)
  const screenTextScale = clampSlideScale(safeSlide.value.screen_text_scale)
  const katexScale = clampSlideScale(safeSlide.value.katex_scale)
  const rowGap = clampCumulativeGap(safeSlide.value.display_katex_row_gap_em ?? safeSlide.value.katex_cumulative_gap_em)
  const isYt = isYoutubeFormat.value
  const isCarousel = isCarouselFormat.value
  const numericSplitRightScale = Number(props.splitRightScale)
  const splitRightScale = Number.isFinite(numericSplitRightScale) ? Math.max(0.05, numericSplitRightScale) : 1
  const safeXScale = isYt
    ? Math.min(1.4, Math.max(0, Number(props.safeZoneXScale) || 0))
    : Math.min(1.4, Math.max(0.7, Number(props.safeZoneXScale) || 1))
  const safeYScale = isYt
    ? Math.min(1.4, Math.max(0, Number(props.safeZoneYScale) || 0))
    : Math.min(1.4, Math.max(0.7, Number(props.safeZoneYScale) || 1))
  const safeInlineUnit = isYt ? '3cqw' : isCarousel ? '6cqw' : '6.5cqw'
  const safeBlockUnit = isYt ? '2.5cqw' : isCarousel ? '5cqw' : '6.5cqw'
  const safeTopUnit = isYt ? '0cqw' : isCarousel ? '0.5cqw' : '16cqw'
  const carouselContentScale = isCarousel
    ? Math.min(1.6, Math.max(0.55, requestedScale / 0.9))
    : requestedScale

  return {
    '--reel-user-scale': requestedScale,
    '--reel-title-scale': titleScale,
    '--reel-screen-text-scale': screenTextScale,
    '--reel-math-scale': requestedScale * katexScale,
    '--reel-split-right-scale': splitRightScale,
    '--reel-carousel-scale': carouselContentScale,
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
  if (isYoutubeFormat.value) return 12
  if (isCarouselFormat.value) return 16
  return 20
})
const screenTextContent = computed(() => {
  const preferred = String(safeSlide.value.display_screen_text || '').trim()
  if (preferred) return preferred
  return String(safeSlide.value.screen_text || '').trim()
})

function normalizeTitleCompare(value) {
  return String(value || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '')
    .trim()
}

const normalTitleText = computed(() => {
  if (usesHookLayout.value || isCtaSlide.value) return ''
  const title = String(safeSlide.value.title || '').trim()
  if (!title) return ''
  const firstTextLine = screenTextContent.value
    .split(/\r?\n/)
    .map((line) => line.trim())
    .find(Boolean) || ''
  if (
    firstTextLine
    && normalizeTitleCompare(firstTextLine) === normalizeTitleCompare(title)
  ) {
    return ''
  }
  return title
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
  const raw = preferred || String(safeSlide.value.katex || '').trim()
  return parseLinePrefixes(raw).body.trim()
})
const carouselKatexMeta = computed(() => parseLinePrefixes(safeSlide.value.katex))
const carouselKatexInlineStyle = computed(() => {
  const { align, color } = carouselKatexMeta.value
  const parts = []
  if (align) parts.push(`text-align:${align}`)
  if (color) parts.push(`color:${color}`)
  return parts.join(';') || null
})
const katexRows = computed(() => {
  const rows = Array.isArray(safeSlide.value.display_katex_rows) ? safeSlide.value.display_katex_rows : []
  return rows
    .map((row) => {
      const parts = (Array.isArray(row?.parts) ? row.parts : [])
        .map((part) => stripKatexAlignmentMarkers(parseLinePrefixes(part).body))
        .filter(Boolean)
      const inlineCount = Math.max(parts.length - 1, 0)
      const fallbackOffset = clampInlineOffset(row?.inlineOffsetPercent)
      const fallbackVerticalOffset = clampInlineVerticalOffset(row?.inlineVerticalOffsetEm)
      const inlineOffsetPercents = Array.isArray(row?.inlineOffsetPercents)
        ? row.inlineOffsetPercents.slice(0, inlineCount).map((value) => clampInlineOffset(value))
        : []
      const inlineVerticalOffsetEms = Array.isArray(row?.inlineVerticalOffsetEms)
        ? row.inlineVerticalOffsetEms.slice(0, inlineCount).map((value) => clampInlineVerticalOffset(value))
        : []

      while (inlineOffsetPercents.length < inlineCount) {
        inlineOffsetPercents.push(fallbackOffset)
      }
      while (inlineVerticalOffsetEms.length < inlineCount) {
        inlineVerticalOffsetEms.push(fallbackVerticalOffset)
      }

      return {
        parts,
        inlineSeparators: Array.isArray(row?.inlineSeparators)
          ? row.inlineSeparators.map((value) => normalizeInlineSeparator(value))
          : [],
        inlineOffsetPercents,
        inlineVerticalOffsetEms,
        inlineOffsetPercent: inlineOffsetPercents.length
          ? inlineOffsetPercents[inlineOffsetPercents.length - 1]
          : fallbackOffset,
        inlineVerticalOffsetEm: inlineVerticalOffsetEms.length
          ? inlineVerticalOffsetEms[inlineVerticalOffsetEms.length - 1]
          : fallbackVerticalOffset,
      }
    })
    .filter((row) => row.parts.length)
})
const hasNormalTitle = computed(() => Boolean(normalTitleText.value))
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
  splitKatexLines(parseLinePrefixes(safeSlide.value.katex).body)
    .map((line) => normalizeKatexRevealKey(line))
    .filter(Boolean)
))
const hookTopText = computed(() => String(safeSlide.value.title || '').trim())
const hookBottomText = computed(() => screenTextContent.value)

const isCarouselCoverSlide = computed(() => (
  isCarouselFormat.value
  && (isHookSlide.value || isCoverSlide.value || Number(safeSlide.value.order || 0) === 1)
))
const isCarouselCtaSlide = computed(() => (
  isCarouselFormat.value
  && !isCarouselCoverSlide.value
  && (
    isCtaSlide.value
    || (props.totalSlides > 0 && Number(safeSlide.value.order || 0) === Number(props.totalSlides))
  )
))
const isCarouselContentSlide = computed(() => (
  isCarouselFormat.value && !isCarouselCoverSlide.value && !isCarouselCtaSlide.value
))
const carouselTitleText = computed(() => String(safeSlide.value.title || '').trim())
const carouselTextLines = computed(() => {
  const raw = screenTextContent.value || ''
  return raw
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
})
const QUIZ_OPTION_RE = /^[A-D]\s*[\)\.\-:]/i
function parseLinePrefixes(line) {
  let rest = String(line || '')
  const am = rest.match(ALIGN_PREFIX_RE)
  const align = am ? am[1].toLowerCase() : null
  if (align) rest = rest.slice(am[0].length)
  const cm = rest.match(COLOR_PREFIX_RE)
  const color = cm ? cm[1] : null
  if (color) rest = rest.slice(cm[0].length)
  return { body: rest, align, color }
}
function lineBody(line) {
  return parseLinePrefixes(line).body
}
function lineInlineStyle(line) {
  const { align, color } = parseLinePrefixes(line)
  const parts = []
  if (align) parts.push(`text-align:${align}`)
  if (color) parts.push(`color:${color}`)
  return parts.join(';')
}
const ANSWER_REVEAL_RE = /^\d+\s*[\)\.\-:]/
const isQuizSlide = computed(() => (
  isCarouselContentSlide.value
  && carouselTextLines.value.some((line) => QUIZ_OPTION_RE.test(lineBody(line)))
))
const isAnswerRevealSlide = computed(() => (
  isCarouselContentSlide.value
  && !isQuizSlide.value
  && carouselTextLines.value.length > 0
  && carouselTextLines.value.every((line) => ANSWER_REVEAL_RE.test(lineBody(line)))
))
const quizOptionGapEm = computed(() => {
  const value = Number(safeSlide.value?.quiz_option_gap_em)
  return Number.isFinite(value) ? value : 0.7
})
const carouselTemplateStyle = computed(() => ({
  '--quiz-option-gap': `${quizOptionGapEm.value}em`,
}))
function quizLineKind(line) {
  if (!isQuizSlide.value) return null
  return QUIZ_OPTION_RE.test(lineBody(line)) ? 'option' : 'question'
}
const QUIZ_OPTION_SPLIT_RE = /^([A-D])\s*[\)\.\-:]\s*(.*)$/i
function quizLetter(line) {
  const m = lineBody(line).match(QUIZ_OPTION_SPLIT_RE)
  return m ? m[1].toUpperCase() : ''
}
function quizContent(line) {
  const m = lineBody(line).match(QUIZ_OPTION_SPLIT_RE)
  return m ? m[2] : lineBody(line)
}
const carouselCoverSubtitle = computed(() => carouselTextLines.value.map(lineBody).join(' '))
const carouselPageLabel = computed(() => {
  const order = Number(safeSlide.value.order || 0)
  if (!order) return ''
  if (props.totalSlides && props.totalSlides > 0) {
    return `${String(order).padStart(2, '0')} / ${String(props.totalSlides).padStart(2, '0')}`
  }
  return String(order).padStart(2, '0')
})
const showCarouselImageToggle = computed(() => (
  isCarouselFormat.value
  && hasGeneratedImageRaw.value
  && props.displayMode !== 'export'
))
function toggleCarouselImage() {
  if (!showCarouselImageToggle.value) return
  emit('toggle-carousel-image', {
    id: safeSlide.value.id,
    hide: !carouselImageHidden.value,
  })
}
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

  if (isAlignedKatexBlock(raw)) {
    return unwrapAlignedBlock(raw)
      .split(/\\\\(?:\[[^\]]*\])?/)
      .map((line) => stripKatexAlignmentMarkers(line))
      .filter(Boolean)
  }

  return raw
    .replace(/\\\\(?:\[[^\]]*\])?/g, '\n')
    .replace(/\\\[[^\]]*\]/g, '\n')
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

const ALIGN_PREFIX_RE = /^\[(left|center|right)\]/i
const COLOR_PREFIX_RE = /^\{(#[0-9a-fA-F]{3,8})\}/

function renderRichText(value) {
  return String(value || '')
    .replace(/\r\n/g, '\n')
    .split('\n')
    .map((line) => {
      const alignMatch = line.match(ALIGN_PREFIX_RE)
      const align = alignMatch ? alignMatch[1].toLowerCase() : null
      let rest = align ? line.slice(alignMatch[0].length) : line
      const colorMatch = rest.match(COLOR_PREFIX_RE)
      const color = colorMatch ? colorMatch[1] : null
      if (color) rest = rest.slice(colorMatch[0].length)
      const styles = []
      if (align) styles.push(`text-align:${align}`)
      if (color) styles.push(`color:${color}`)
      const styleAttr = styles.length ? ` style="${styles.join(';')}"` : ''
      if (!rest.trim()) {
        return `<span class="rich-text-line rich-text-line--empty"${styleAttr}>&nbsp;</span>`
      }
      return `<span class="rich-text-line"${styleAttr}>${renderRichTextLine(rest)}</span>`
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
          const inlineOffsetPercents = Array.isArray(row.inlineOffsetPercents) ? row.inlineOffsetPercents : []
          const inlineVerticalOffsetEms = Array.isArray(row.inlineVerticalOffsetEms) ? row.inlineVerticalOffsetEms : []
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
          const inlineHtml = inlineParts
            .map((inlinePart, index) => {
              const offset = clampInlineOffset(inlineOffsetPercents[index] ?? row.inlineOffsetPercent)
              const verticalOffset = clampInlineVerticalOffset(inlineVerticalOffsetEms[index] ?? row.inlineVerticalOffsetEm)
              const baseTopEm = allNotTall
                ? -0.04
                : (baselineRef - inlinePart.metrics.aboveBaseline + inlinePart.visualNudge)
              const finalTopEm = baseTopEm + verticalOffset
              const topOffset = ` top:calc(${formatKatexEmMetric(finalTopEm)} * var(--reel-katex-inline-em));`
              if (useCompactInlineLayout) {
                const style = `position:relative; left:${formatKatexEmMetric(offset)}%;${topOffset}`
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
    props.splitRightScale,
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

.reel-slide--generated::before {
  display: none;
}

.reel-slide-generated-image {
  position: absolute;
  inset: 0;
  z-index: 1;
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.reel-slide-generated-scrim {
  position: absolute;
  inset: 0;
  z-index: 2;
  pointer-events: none;
  background:
    linear-gradient(180deg, rgba(8, 18, 48, 0.55) 0%, rgba(8, 18, 48, 0.10) 28%, rgba(8, 18, 48, 0.10) 58%, rgba(8, 18, 48, 0.78) 100%);
}

.slide-card--carousel .reel-slide--generated .reel-slide-body {
  z-index: 3;
  color: #ffffff;
  text-shadow: 0 2px 18px rgba(8, 18, 48, 0.55), 0 1px 2px rgba(8, 18, 48, 0.45);
}

.slide-card--carousel .reel-slide--generated .reel-slide-body :deep(.slide-title),
.slide-card--carousel .reel-slide--generated .reel-slide-body :deep(.screen-text),
.slide-card--carousel .reel-slide--generated .reel-slide-body :deep(.hook-top),
.slide-card--carousel .reel-slide--generated .reel-slide-body :deep(.hook-middle-text),
.slide-card--carousel .reel-slide--generated .reel-slide-body :deep(.hook-bottom),
.slide-card--carousel .reel-slide--generated .reel-slide-body :deep(.cta-top),
.slide-card--carousel .reel-slide--generated .reel-slide-body :deep(.cta-main),
.slide-card--carousel .reel-slide--generated .reel-slide-body :deep(.cta-line) {
  color: #ffffff;
}

.slide-card--carousel .reel-slide--generated .reel-slide-body :deep(.katex),
.slide-card--carousel .reel-slide--generated .reel-slide-body :deep(.katex .mord),
.slide-card--carousel .reel-slide--generated .reel-slide-body :deep(.katex .mbin),
.slide-card--carousel .reel-slide--generated .reel-slide-body :deep(.katex .mrel),
.slide-card--carousel .reel-slide--generated .reel-slide-body :deep(.katex .mop) {
  color: #ffffff;
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

.slide-title {
  margin: 0;
  width: 100%;
  max-width: 100%;
  color: #1e3a8a;
  font-family: Georgia, 'Times New Roman', serif;
  font-size: calc(18px * var(--reel-title-scale, 1) * var(--reel-thumb-fit-scale, 1));
  font-weight: 700;
  line-height: 1.12;
  text-align: left;
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

.slide-card--fullscreen .slide-title {
  font-size: clamp(24px, 2.5vw, 38px);
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

.slide-title,
.reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .slide-title,
.slide-card--fullscreen .slide-title {
  font-size: calc(5.4cqw * var(--reel-title-scale, 1) * var(--reel-thumb-fit-scale, 1));
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

.slide-card--youtube:not(.slide-card--fullscreen) .hook-top,
.slide-card--youtube:not(.slide-card--fullscreen) .hook-middle-text,
.slide-card--youtube:not(.slide-card--fullscreen) .hook-bottom,
.slide-card--youtube:not(.slide-card--fullscreen) .cta-top,
.slide-card--youtube:not(.slide-card--fullscreen) .cta-main,
.slide-card--youtube.slide-card--fullscreen .hook-top,
.slide-card--youtube.slide-card--fullscreen .hook-middle-text,
.slide-card--youtube.slide-card--fullscreen .hook-bottom,
.slide-card--youtube.slide-card--fullscreen .cta-top,
.slide-card--youtube.slide-card--fullscreen .cta-main {
  font-family: Georgia, 'Times New Roman', serif;
  color: #244b9f;
}

.slide-card--youtube:not(.slide-card--fullscreen) .hook-layout,
.slide-card--youtube.slide-card--fullscreen .hook-layout {
  box-sizing: border-box;
  gap: calc(3.4cqw * var(--reel-user-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.slide-card--youtube:not(.slide-card--fullscreen) .reel-slide--hook:not(.reel-slide--cover) .hook-layout,
.slide-card--youtube.slide-card--fullscreen .reel-slide--hook:not(.reel-slide--cover) .hook-layout {
  transform: translateY(-5cqw);
}

.slide-card--youtube:not(.slide-card--fullscreen) .reel-slide--subtitled.reel-slide--hook:not(.reel-slide--cover) .hook-layout,
.slide-card--youtube.slide-card--fullscreen .reel-slide--subtitled.reel-slide--hook:not(.reel-slide--cover) .hook-layout {
  transform: translateY(-7cqw);
  padding-bottom: 5cqw;
}

.slide-card--youtube:not(.slide-card--fullscreen) .hook-top,
.slide-card--youtube.slide-card--fullscreen .hook-top {
  font-size: calc(7.8cqw * var(--reel-title-scale, 1) * var(--reel-thumb-fit-scale, 1));
  line-height: 1.08;
  overflow-wrap: anywhere;
  white-space: normal;
}

.slide-card--youtube:not(.slide-card--fullscreen) .hook-bottom,
.slide-card--youtube.slide-card--fullscreen .hook-bottom {
  font-size: calc(5.2cqw * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
  line-height: 1.12;
  overflow-wrap: anywhere;
  white-space: normal;
}

.slide-card--youtube:not(.slide-card--fullscreen) .hook-middle-text,
.slide-card--youtube.slide-card--fullscreen .hook-middle-text {
  font-size: calc(5.8cqw * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
  line-height: 1.12;
}

.slide-card--youtube:not(.slide-card--fullscreen) .hook-katex :deep(.katex),
.slide-card--youtube.slide-card--fullscreen .hook-katex :deep(.katex) {
  font-size: calc(5cqw * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1)) !important;
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
  font-size: calc(6.2cqw * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1)) !important;
}

.slide-card--youtube .screen-text,
.slide-card--youtube .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .screen-text,
.slide-card--youtube.slide-card--fullscreen .screen-text {
  font-size: calc(3cqw * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
  line-height: 1.3;
}

.slide-card--youtube .slide-title,
.slide-card--youtube .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .slide-title,
.slide-card--youtube.slide-card--fullscreen .slide-title {
  font-size: calc(3.4cqw * var(--reel-title-scale, 1) * var(--reel-thumb-fit-scale, 1));
  line-height: 1.12;
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

.slide-card--carousel:not(.slide-card--fullscreen) {
  flex: 0 0 250px;
  width: 250px;
  min-width: 250px;
}

.slide-card--carousel .reel-slide {
  aspect-ratio: 4 / 5;
  border-color: #d7e4f8;
  background:
    radial-gradient(circle at 85% 12%, rgba(58, 91, 184, 0.10) 0%, transparent 38%),
    radial-gradient(circle at 12% 92%, rgba(41, 66, 142, 0.08) 0%, transparent 40%),
    linear-gradient(180deg, #ffffff 0%, #f4f8ff 100%);
}

.slide-card--carousel .reel-slide::before {
  background-image: url('/OptiTAB_bg.png');
  background-size: cover;
  background-position: center;
}

.slide-card--carousel.slide-card--fullscreen {
  width: min(82vw, calc((100dvh - 150px) * 4 / 5));
  max-width: 560px;
  min-width: min(72vw, 320px);
}

.slide-card--carousel .reel-slide-body,
.slide-card--carousel.slide-card--fullscreen .reel-slide-body {
  gap: calc(2.8cqw * var(--reel-thumb-fit-scale, 1));
}

.slide-card--carousel:not(.slide-card--fullscreen) .hook-layout,
.slide-card--carousel.slide-card--fullscreen .hook-layout,
.slide-card--carousel .cta-layout,
.slide-card--carousel.slide-card--fullscreen .cta-layout {
  gap: calc(4cqw * var(--reel-user-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.slide-card--carousel:not(.slide-card--fullscreen) .reel-slide--hook:not(.reel-slide--cover) .hook-layout,
.slide-card--carousel.slide-card--fullscreen .reel-slide--hook:not(.reel-slide--cover) .hook-layout {
  transform: translateY(-4cqw);
}

.slide-card--carousel:not(.slide-card--fullscreen) .hook-top,
.slide-card--carousel.slide-card--fullscreen .hook-top,
.slide-card--carousel .cta-top,
.slide-card--carousel.slide-card--fullscreen .cta-top {
  font-size: calc(8.4cqw * var(--reel-title-scale, 1) * var(--reel-thumb-fit-scale, 1));
  line-height: 1.08;
  overflow-wrap: anywhere;
  white-space: normal;
}

.slide-card--carousel:not(.slide-card--fullscreen) .hook-middle-text,
.slide-card--carousel.slide-card--fullscreen .hook-middle-text {
  font-size: calc(8.8cqw * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
  line-height: 1.1;
}

.slide-card--carousel:not(.slide-card--fullscreen) .hook-bottom,
.slide-card--carousel.slide-card--fullscreen .hook-bottom {
  font-size: calc(5.8cqw * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
  line-height: 1.14;
  overflow-wrap: anywhere;
  white-space: normal;
}

.slide-card--carousel:not(.slide-card--fullscreen) .hook-katex :deep(.katex),
.slide-card--carousel.slide-card--fullscreen .hook-katex :deep(.katex),
.slide-card--carousel .cta-katex :deep(.katex),
.slide-card--carousel.slide-card--fullscreen .cta-katex :deep(.katex) {
  font-size: calc(6.2cqw * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1)) !important;
}

.slide-card--carousel .cta-main,
.slide-card--carousel.slide-card--fullscreen .cta-main {
  font-size: calc(5cqw * var(--reel-title-scale, 1) * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
  line-height: 1.16;
}

.slide-card--carousel .screen-text,
.slide-card--carousel .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .screen-text,
.slide-card--carousel.slide-card--fullscreen .screen-text {
  font-size: calc(3.8cqw * var(--reel-screen-text-scale, 1) * var(--reel-thumb-fit-scale, 1));
  line-height: 1.28;
}

.slide-card--carousel .slide-title,
.slide-card--carousel .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .slide-title,
.slide-card--carousel.slide-card--fullscreen .slide-title {
  font-size: calc(4.2cqw * var(--reel-title-scale, 1) * var(--reel-thumb-fit-scale, 1));
  line-height: 1.1;
}

.slide-card--carousel .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone,
.slide-card--carousel.slide-card--fullscreen .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone {
  gap: calc(2.4cqw * var(--reel-thumb-fit-scale, 1));
}

.slide-card--carousel .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.katex),
.slide-card--carousel .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line .katex),
.slide-card--carousel.slide-card--fullscreen .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.katex) {
  font-size: calc(3.8cqw * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1)) !important;
}

.slide-card--carousel .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line),
.slide-card--carousel.slide-card--fullscreen .reel-slide:not(.reel-slide--hook):not(.reel-slide--cta) .katex-zone :deep(.reel-katex-line) {
  min-height: calc(6.4cqw * var(--reel-math-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

/* === Carousel per-slide image toggle =================================== */

.carousel-image-toggle {
  position: absolute;
  top: 8px;
  right: 8px;
  z-index: 12;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 9px;
  border-radius: 999px;
  border: 1px solid rgba(41, 66, 142, 0.35);
  background: rgba(255, 255, 255, 0.92);
  color: #1f4ed8;
  font: 600 10px/1 'Inter', system-ui, sans-serif;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  cursor: pointer;
  box-shadow: 0 6px 16px rgba(15, 23, 42, 0.18);
  transition: transform 0.15s ease, background 0.15s ease, color 0.15s ease;
  pointer-events: auto;
  opacity: 0;
}

.slide-card:hover .carousel-image-toggle,
.slide-card--selected .carousel-image-toggle,
.carousel-image-toggle:focus-visible {
  opacity: 1;
}

.carousel-image-toggle:hover {
  transform: translateY(-1px);
  background: #ffffff;
}

.carousel-image-toggle--off {
  background: rgba(15, 23, 42, 0.82);
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.4);
}

.carousel-image-toggle--off:hover {
  background: rgba(15, 23, 42, 0.95);
}

.carousel-image-toggle svg {
  flex: 0 0 auto;
}

.carousel-image-toggle__label {
  white-space: nowrap;
}

.slide-card--fullscreen .carousel-image-toggle {
  top: 18px;
  right: 18px;
  padding: 8px 14px;
  font-size: 12px;
  gap: 8px;
}

.slide-card--fullscreen .carousel-image-toggle svg {
  width: 16px;
  height: 16px;
}

/* === Carousel template (Instagram-ready) ============================== */

.slide-card--carousel .reel-slide {
  --ct-brand: #274ec3;
  --ct-brand-deep: #1c3070;
  --ct-brand-soft: #3a5bb8;
  --ct-brand-glow: rgba(41, 66, 142, 0.18);
  --ct-ink: #0b1733;
  --ct-ink-soft: #4a5d86;
  --ct-line: rgba(41, 66, 142, 0.18);
  --ct-bg: #f8fbff;
}

.carousel-template {
  position: absolute;
  inset: 0;
  z-index: 3;
  display: grid;
  grid-template-rows: auto 1fr auto;
  padding:
    calc(var(--reel-safe-block, 5cqw) + var(--reel-safe-top, 0.5cqw))
    var(--reel-safe-inline, 6cqw)
    var(--reel-safe-block, 5cqw);
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
  color: var(--ct-ink);
  gap: 3cqw;
}

.slide-card--carousel :deep(.annotation-layer) {
  z-index: 5;
}

.carousel-template__topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2cqw;
  font-size: 2.6cqw;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--ct-brand);
  font-weight: 700;
}

.carousel-template__brand {
  display: inline-flex;
  align-items: center;
  gap: 1.4cqw;
}

.carousel-template__brand-logo {
  height: 5.4cqw;
  width: auto;
  display: block;
  object-fit: contain;
  user-select: none;
  -webkit-user-drag: none;
  filter: drop-shadow(0 0.4cqw 0.8cqw rgba(41, 66, 142, 0.15));
}

.carousel-template__page {
  display: inline-flex;
  align-items: center;
  padding: 0.8cqw 2cqw;
  border-radius: 999px;
  background: rgba(41, 66, 142, 0.08);
  border: 0.18cqw solid rgba(41, 66, 142, 0.18);
  font-variant-numeric: tabular-nums;
  color: var(--ct-brand);
  font-weight: 700;
  font-size: 2.3cqw;
  letter-spacing: 0.22em;
}

.carousel-template__main {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  gap: 2.4cqw;
  min-height: 0;
  text-align: left;
  transform: scale(var(--reel-carousel-scale, 1));
  transform-origin: left center;
}

/* --- Cover slide --- */

.carousel-template--cover .carousel-template__main {
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 3cqw;
  transform-origin: center center;
}

.carousel-template__eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 1cqw;
  padding: 1.2cqw 3cqw;
  border-radius: 999px;
  background: rgba(41, 66, 142, 0.10);
  border: 0.18cqw solid rgba(41, 66, 142, 0.22);
  color: var(--ct-brand);
  font-size: 2.4cqw;
  font-weight: 800;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.carousel-template__eyebrow::before {
  content: '';
  width: 1.4cqw;
  height: 1.4cqw;
  border-radius: 999px;
  background: linear-gradient(135deg, var(--ct-brand) 0%, var(--ct-brand-soft) 100%);
}

.carousel-template__cover-title {
  margin: 0;
  font-size: calc(11cqw * var(--reel-title-scale, 1));
  line-height: 1.02;
  font-weight: 900;
  letter-spacing: -0.025em;
  color: var(--carousel-title-color, var(--ct-brand));
  max-width: 100%;
  overflow-wrap: anywhere;
  text-shadow: 0 0.6cqw 1.4cqw rgba(41, 66, 142, 0.08);
}

.carousel-template__cover-sub {
  margin: 0;
  font-size: calc(4.2cqw * var(--reel-screen-text-scale, 1));
  line-height: 1.32;
  color: var(--ct-ink-soft);
  font-weight: 500;
  max-width: 92%;
  overflow-wrap: anywhere;
}

.carousel-template__cover-katex {
  font-size: calc(4.2cqw * var(--reel-math-scale, 1));
  color: var(--carousel-text-color, var(--ct-ink));
}

.carousel-template__cover-katex :deep(.katex),
.carousel-template__cover-katex :deep(.katex .mord),
.carousel-template__cover-katex :deep(.katex .mbin),
.carousel-template__cover-katex :deep(.katex .mrel),
.carousel-template__cover-katex :deep(.katex .mop),
.carousel-template__cover-katex :deep(.katex .mopen),
.carousel-template__cover-katex :deep(.katex .mclose),
.carousel-template__cover-katex :deep(.katex .mpunct),
.carousel-template__cover-katex :deep(.katex .minner),
.carousel-template__cover-katex :deep(.katex .mathnormal),
.carousel-template__cover-katex :deep(.katex .mathit),
.carousel-template__cover-katex :deep(.katex .mathrm),
.carousel-template__cover-katex :deep(.katex .mfrac .frac-line) {
  color: inherit;
  border-color: inherit;
}

.carousel-template__swipe {
  margin-top: 2.4cqw;
  display: inline-flex;
  align-items: center;
  gap: 1.6cqw;
  padding: 1.8cqw 3.6cqw;
  border-radius: 999px;
  background: var(--ct-brand);
  color: #ffffff;
  font-weight: 800;
  font-size: 3.1cqw;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  box-shadow: 0 1.4cqw 2.8cqw rgba(41, 66, 142, 0.34);
}

.carousel-template__swipe-arrow {
  font-size: 3.6cqw;
  line-height: 1;
  transform: translateY(-0.05em);
}

/* --- Content slide --- */

.carousel-template--content .carousel-template__main {
  justify-content: flex-start;
  padding-top: 1.5cqw;
  transform-origin: left top;
}

.carousel-template__step {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 11.2cqw;
  min-width: 11.2cqw;
  height: 7.2cqw;
  padding: 0;
  border-radius: 999px;
  background: var(--ct-brand);
  color: #ffffff;
  font-weight: 800;
  font-size: 3.2cqw;
  font-variant-numeric: tabular-nums;
  letter-spacing: 0;
  line-height: 1;
  text-align: center;
  box-shadow: 0 1cqw 2.2cqw rgba(41, 66, 142, 0.30);
}

.carousel-template__title {
  margin: 1cqw 0 0;
  font-size: calc(7.8cqw * var(--reel-title-scale, 1));
  line-height: 1.04;
  font-weight: 900;
  letter-spacing: -0.02em;
  color: var(--carousel-title-color, var(--ct-brand));
  overflow-wrap: anywhere;
}

.carousel-template__accent {
  width: 16cqw;
  height: 1cqw;
  border-radius: 999px;
  background: linear-gradient(90deg, var(--ct-brand) 0%, var(--ct-brand-soft) 100%);
  margin: 1cqw 0 1.4cqw;
  box-shadow: 0 0.4cqw 1cqw rgba(41, 66, 142, 0.28);
}

.carousel-template__text-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 1.8cqw;
  width: 100%;
}

.carousel-template__text-item {
  position: relative;
  padding-left: 5cqw;
  font-size: calc(4.2cqw * var(--reel-screen-text-scale, 1));
  line-height: 1.34;
  color: var(--carousel-text-color, var(--ct-ink));
  font-weight: 600;
  overflow-wrap: anywhere;
}

.carousel-template__text-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.55em;
  width: 3cqw;
  height: 0.8cqw;
  border-radius: 999px;
  background: linear-gradient(90deg, var(--ct-brand) 0%, var(--ct-brand-soft) 100%);
  box-shadow: 0 0.3cqw 0.6cqw rgba(41, 66, 142, 0.28);
}

.carousel-template__text-list--quiz {
  gap: 0;
}

.carousel-template__text-list--quiz .carousel-template__text-item--quiz-option + .carousel-template__text-item--quiz-option {
  margin-top: var(--quiz-option-gap, 0.7em);
}

.carousel-template__text-item--quiz-question,
.carousel-template__text-item--quiz-option {
  padding-left: 0;
}

.carousel-template__text-item--quiz-question::before,
.carousel-template__text-item--quiz-option::before,
.carousel-template__text-item--reveal::before {
  content: none;
}

.carousel-template__text-item--reveal {
  padding-left: 0;
}

.carousel-template__text-item--quiz-question {
  font-size: calc(5.04cqw * var(--reel-screen-text-scale, 1));
  font-weight: 500;
  margin-bottom: 2.6cqw;
  color: var(--carousel-text-color, var(--ct-brand-deep));
  letter-spacing: -0.005em;
  line-height: 1.28;
  text-align: left !important;
}

.carousel-template__text-item--quiz-option {
  display: flex;
  align-items: baseline;
  gap: 2.4cqw;
  padding-left: 6cqw;
  font-size: calc(4.68cqw * var(--reel-screen-text-scale, 1));
  font-weight: 500;
  line-height: 1.3;
  color: var(--carousel-text-color, var(--ct-brand-deep));
}

.carousel-template__quiz-letter {
  flex: 0 0 auto;
  min-width: 1.2em;
  font-weight: 800;
  color: var(--carousel-text-color, var(--ct-brand-deep));
  letter-spacing: 0.01em;
}

.carousel-template__quiz-letter::after {
  content: '.';
  margin-left: 0.05em;
  color: var(--carousel-text-color, var(--ct-brand-deep));
}

.carousel-template__quiz-content {
  flex: 1 1 auto;
  min-width: 0;
  color: inherit;
}

.carousel-template__text-item--quiz-option .katex,
.carousel-template__text-item--quiz-question .katex {
  color: inherit;
}

.carousel-template__text-item--quiz-option .katex {
  font-size: 1.3em;
}

.carousel-template__katex {
  margin-top: 1cqw;
  font-size: calc(4.2cqw * var(--reel-math-scale, 1));
  color: var(--carousel-text-color, var(--ct-ink));
}

.carousel-template__katex :deep(.katex),
.carousel-template__katex :deep(.katex .mord),
.carousel-template__katex :deep(.katex .mbin),
.carousel-template__katex :deep(.katex .mrel),
.carousel-template__katex :deep(.katex .mop),
.carousel-template__katex :deep(.katex .mopen),
.carousel-template__katex :deep(.katex .mclose),
.carousel-template__katex :deep(.katex .mpunct),
.carousel-template__katex :deep(.katex .minner),
.carousel-template__katex :deep(.katex .mathnormal),
.carousel-template__katex :deep(.katex .mathit),
.carousel-template__katex :deep(.katex .mathrm),
.carousel-template__katex :deep(.katex .mfrac .frac-line) {
  color: inherit;
  border-color: inherit;
}

/* --- CTA slide --- */

.carousel-template--cta .carousel-template__main {
  align-items: flex-start;
  justify-content: center;
  text-align: left;
  gap: 2.4cqw;
  transform-origin: center center;
}

.carousel-template__cta-eyebrow {
  display: inline-block;
  padding: 1cqw 2.6cqw;
  border-radius: 999px;
  background: rgba(41, 66, 142, 0.12);
  color: var(--ct-brand);
  font-size: 2.4cqw;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.carousel-template__cta-title {
  margin: 0;
  font-size: calc(8.4cqw * var(--reel-title-scale, 1));
  line-height: 1.05;
  font-weight: 900;
  letter-spacing: -0.025em;
  color: var(--carousel-title-color, var(--ct-brand));
  text-align: left;
  overflow-wrap: anywhere;
  max-width: 100%;
}

.carousel-template__cta-url-wrap {
  position: relative;
  display: inline-block;
  padding: 0 1cqw;
  align-self: center;
}

.carousel-template__cta-url {
  position: relative;
  z-index: 1;
  font-size: 7cqw;
  font-weight: 900;
  line-height: 1;
  letter-spacing: -0.01em;
  color: var(--ct-brand);
}

.carousel-template__cta-underline {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0.6cqw;
  height: 2cqw;
  border-radius: 999px;
  background: linear-gradient(90deg, rgba(41, 66, 142, 0.18) 0%, rgba(58, 91, 184, 0.32) 100%);
  z-index: 0;
}

.carousel-template__cta-list {
  list-style: none;
  margin: 1cqw 0 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 1.4cqw;
  align-items: flex-start;
  width: 100%;
}

.carousel-template__cta-item {
  position: relative;
  font-size: calc(3.8cqw * var(--reel-screen-text-scale, 1));
  line-height: 1.32;
  color: var(--carousel-text-color, var(--ct-ink-soft));
  font-weight: 500;
  padding-left: 3.4cqw;
}

.carousel-template__cta-item::before {
  content: '✓';
  position: absolute;
  left: 0;
  top: 0;
  color: var(--ct-brand);
  font-weight: 800;
  font-size: 3.6cqw;
}

.carousel-template__cta-katex {
  font-size: calc(4cqw * var(--reel-math-scale, 1));
  color: var(--carousel-text-color, var(--ct-ink));
}

.carousel-template__cta-katex :deep(.katex),
.carousel-template__cta-katex :deep(.katex .mord),
.carousel-template__cta-katex :deep(.katex .mbin),
.carousel-template__cta-katex :deep(.katex .mrel),
.carousel-template__cta-katex :deep(.katex .mop),
.carousel-template__cta-katex :deep(.katex .mopen),
.carousel-template__cta-katex :deep(.katex .mclose),
.carousel-template__cta-katex :deep(.katex .mpunct),
.carousel-template__cta-katex :deep(.katex .minner),
.carousel-template__cta-katex :deep(.katex .mathnormal),
.carousel-template__cta-katex :deep(.katex .mathit),
.carousel-template__cta-katex :deep(.katex .mathrm),
.carousel-template__cta-katex :deep(.katex .mfrac .frac-line) {
  color: inherit;
  border-color: inherit;
}

.carousel-template__cta-button {
  position: relative;
  margin-top: 2.4cqw;
  align-self: center;
  display: inline-flex;
  align-items: center;
  gap: 1.6cqw;
  padding: 1.8cqw 3.6cqw;
  border-radius: 999px;
  background: var(--ct-brand);
  color: #ffffff;
  font-weight: 800;
  font-size: 3.1cqw;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  box-shadow: 0 1.4cqw 2.8cqw rgba(41, 66, 142, 0.34);
}

.carousel-template__cta-button-arrow {
  font-size: 3.6cqw;
  line-height: 1;
  transform: translateY(-0.05em);
}

/* --- Footer (all non-cover slides) --- */

.carousel-template__bottombar {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 1.6cqw;
  font-size: 2.5cqw;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--ct-brand);
  font-weight: 800;
  padding-top: 2cqw;
}

.carousel-template__bottombar::before {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  height: 0.18cqw;
  background: linear-gradient(90deg, transparent 0%, rgba(41, 66, 142, 0.22) 50%, transparent 100%);
}

.carousel-template__url {
  position: relative;
  padding-left: 3.6cqw;
}

.carousel-template__url::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 2.4cqw;
  height: 2.4cqw;
  border-radius: 999px;
  background: linear-gradient(135deg, var(--ct-brand) 0%, var(--ct-brand-soft) 100%);
  box-shadow: 0 0 0 0.5cqw rgba(41, 66, 142, 0.14);
}

/* --- Image hero variant: image as framed card on top, text in clean zone below --- */

/* Full-bleed background image with a strong premium overlay for legibility.
   This is the editorial pattern used by top brand carousels (Apple, Stripe,
   Notion): the image fills the slide, and the text sits in a dark gradient
   zone at the bottom that doubles as a brand-color tint. */
.slide-card--carousel .reel-slide--generated .reel-slide-generated-image {
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  border-radius: 0;
  box-shadow: none;
  object-fit: cover;
  object-position: center;
  background: #0b1733;
}

/* Premium scrim: subtle dark top (for topbar legibility) + strong OptiTAB blue
   gradient on the bottom 60% so the text zone is bulletproof regardless of
   what Gemini puts in the image. */
.slide-card--carousel .reel-slide--generated .reel-slide-generated-scrim {
  display: block;
  z-index: 2;
  background:
    linear-gradient(180deg,
      rgba(8, 18, 48, 0.55) 0%,
      rgba(8, 18, 48, 0.20) 18%,
      rgba(8, 18, 48, 0.00) 38%,
      rgba(8, 18, 48, 0.00) 48%,
      rgba(8, 18, 48, 0.55) 68%,
      rgba(11, 23, 51, 0.92) 100%);
}

.carousel-template--on-image {
  background: transparent;
  color: #ffffff;
}

/* Main content is anchored to the bottom 50% of the slide so it lives entirely
   inside the dark scrim zone -- guaranteed legibility. */
.carousel-template--on-image .carousel-template__main {
  position: absolute;
  top: auto;
  left: 6cqw;
  right: 6cqw;
  bottom: 9cqw;
  padding: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: flex-start;
  gap: 2.4cqw;
  z-index: 5;
  transform: none;
}

.carousel-template--on-image.carousel-template--cover .carousel-template__main,
.carousel-template--on-image.carousel-template--cta .carousel-template__main {
  align-items: center;
  text-align: center;
}

/* Topbar / brand: white on the image with a subtle dark drop-shadow */
.carousel-template--on-image .carousel-template__topbar,
.carousel-template--on-image .carousel-template__brand,
.carousel-template--on-image .carousel-template__bottombar,
.carousel-template--on-image .carousel-template__url {
  color: #ffffff;
}

.carousel-template--on-image .carousel-template__brand-logo {
  filter: brightness(0) invert(1) drop-shadow(0 0.4cqw 0.8cqw rgba(0, 0, 0, 0.45));
}

.carousel-template--on-image .carousel-template__page {
  background: rgba(255, 255, 255, 0.16);
  border-color: rgba(255, 255, 255, 0.30);
  color: #ffffff;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.carousel-template--on-image .carousel-template__brand-dot,
.carousel-template--on-image .carousel-template__url::before {
  background: #ffffff;
  box-shadow: 0 0 0 0.4cqw rgba(255, 255, 255, 0.20);
}

/* (CTA eyebrow on image is rendered via the floating-eyebrow element above.) */

/* When on image, hide the in-main eyebrows -- they are replaced by the
   floating eyebrows positioned at the top of the slide (siblings of main). */
.carousel-template--on-image .carousel-template__eyebrow,
.carousel-template--on-image .carousel-template__cta-eyebrow {
  display: none;
}

/* When on image, the bottombar (footer with "optitab.net") becomes duplicate:
   - the floating eyebrow at the top already carries the brand
   - the CTA slide already shows its own cta-url in the main content
   So we hide it to avoid overlap with the content. */
.carousel-template--on-image .carousel-template__bottombar {
  display: none;
}

/* Floating brand chip pinned to the top zone of the slide. As a direct child
   of .carousel-template (which is inset: 0 of the slide), it is positioned
   relative to the SLIDE, not relative to .main. */
.carousel-template__floating-eyebrow {
  position: absolute;
  top: 14cqw;
  left: 50%;
  transform: translateX(-50%);
  z-index: 6;
  display: inline-flex;
  align-items: center;
  gap: 1cqw;
  padding: 1.3cqw 3.4cqw;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.96);
  color: var(--ct-brand);
  font-size: 2.6cqw;
  font-weight: 800;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  white-space: nowrap;
  box-shadow:
    0 0.8cqw 2cqw rgba(8, 18, 48, 0.32),
    0 0.2cqw 0.6cqw rgba(8, 18, 48, 0.18);
}

.carousel-template__floating-eyebrow::before {
  content: '';
  width: 1.2cqw;
  height: 1.2cqw;
  border-radius: 999px;
  background: var(--ct-brand);
  box-shadow: 0 0 0 0.4cqw rgba(41, 66, 142, 0.14);
}

/* Titles: white with strong shadow for premium magazine feel */
.carousel-template--on-image .carousel-template__cover-title,
.carousel-template--on-image .carousel-template__title,
.carousel-template--on-image .carousel-template__cta-title {
  background: none;
  -webkit-background-clip: initial;
  background-clip: initial;
  color: #ffffff;
  text-shadow:
    0 0.6cqw 2cqw rgba(8, 18, 48, 0.55),
    0 0.2cqw 0.5cqw rgba(8, 18, 48, 0.55);
}

/* Sized slightly down so they fit in the bottom zone */
.carousel-template--on-image .carousel-template__cover-title {
  font-size: calc(9cqw * var(--reel-title-scale, 1));
  line-height: 1.04;
  font-weight: 900;
}

.carousel-template--on-image .carousel-template__cta-title {
  font-size: calc(7cqw * var(--reel-title-scale, 1));
  line-height: 1.06;
  font-weight: 900;
}

.carousel-template--on-image .carousel-template__cover-sub,
.carousel-template--on-image .carousel-template__text-item,
.carousel-template--on-image .carousel-template__cta-item,
.carousel-template--on-image .carousel-template__cta-url,
.carousel-template--on-image .carousel-template__katex,
.carousel-template--on-image .carousel-template__cta-katex,
.carousel-template--on-image .carousel-template__cover-katex {
  color: rgba(255, 255, 255, 0.94);
  text-shadow: 0 0.3cqw 1.2cqw rgba(8, 18, 48, 0.50);
  background: none;
  -webkit-background-clip: initial;
  background-clip: initial;
}

.carousel-template--on-image .carousel-template__cover-sub {
  font-size: calc(3.6cqw * var(--reel-screen-text-scale, 1));
  line-height: 1.34;
}

.carousel-template--on-image .carousel-template__cta-item {
  font-size: calc(3.4cqw * var(--reel-screen-text-scale, 1));
}

.carousel-template--on-image .carousel-template__text-item::before {
  background: #ffffff;
}

.carousel-template--on-image .carousel-template__cta-underline {
  background: rgba(255, 255, 255, 0.36);
}

.carousel-template--on-image .carousel-template__cta-item::before {
  color: #ffffff;
  background: transparent;
}

.carousel-template--on-image .carousel-template__accent {
  background: rgba(255, 255, 255, 0.95);
}

.carousel-template--on-image .carousel-template__step,
.carousel-template--on-image .carousel-template__swipe,
.carousel-template--on-image .carousel-template__cta-button {
  background: rgba(255, 255, 255, 0.96);
  color: var(--ct-brand);
  text-shadow: none;
  box-shadow:
    0 1cqw 2.4cqw rgba(8, 18, 48, 0.38),
    0 0.2cqw 0.6cqw rgba(8, 18, 48, 0.22);
  padding: 1.6cqw 3.4cqw;
  font-size: 2.9cqw;
}

@media (max-width: 768px) {
  .slide-card--carousel.slide-card--fullscreen {
    width: min(92vw, calc((100dvh - 190px) * 4 / 5));
    min-width: min(82vw, 320px);
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

.reel-slide-split {
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-columns: minmax(0, 60fr) minmax(0, 40fr);
  gap: 2.2cqw;
  align-items: stretch;
}

.reel-slide-split__left {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 12px;
  min-width: 0;
  min-height: 0;
}

.reel-slide-split__right {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: stretch;
  gap: calc(1.4cqw * var(--reel-split-right-scale, 1));
  padding: 1.8cqw 1.6cqw;
  background: linear-gradient(160deg, #f8fafc 0%, #eef2ff 55%, #e0e7ff 100%);
  border: 1px solid rgba(99, 102, 241, 0.22);
  border-radius: 1cqw;
  box-shadow:
    0 1.2cqw 2.4cqw rgba(30, 41, 59, 0.06),
    inset 0 0 0 1px rgba(255, 255, 255, 0.6);
  color: #1e293b;
  min-width: 0;
  min-height: 0;
  overflow: hidden;
}

.reel-slide-split__right::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: radial-gradient(140% 90% at 50% 0%, rgba(99, 102, 241, 0.08), transparent 60%);
  pointer-events: none;
}

.reel-slide-split__label {
  position: relative;
  margin: 0;
  padding-bottom: 1cqw;
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
  font-weight: 700;
  font-size: calc(1.45cqw * var(--reel-split-right-scale, 1));
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: #4f46e5;
  text-align: left;
  white-space: pre-line;
  border-bottom: 1px solid rgba(99, 102, 241, 0.18);
}

.reel-slide-split__katex {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  gap: calc(1.2cqw * var(--reel-split-right-scale, 1));
  flex: 1 1 auto;
  min-height: 0;
}

.reel-slide-split__katex :deep(.reel-slide-split__katex-line) {
  width: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  overflow: hidden;
  text-align: left;
}

.reel-slide-split__katex :deep(.reel-slide-split__katex-line .katex-display) {
  margin: 0;
  display: flex;
  justify-content: flex-start;
  width: 100%;
  max-width: 100%;
  overflow: hidden;
  text-align: left !important;
}

.reel-slide-split__katex :deep(.reel-slide-split__katex-line .katex-display > .katex) {
  margin-left: 0 !important;
  margin-right: auto !important;
  text-align: left !important;
}

.reel-slide-split__katex :deep(.reel-slide-split__katex-line .katex),
.reel-slide-split__katex :deep(.reel-slide-split__katex-line .katex .mord),
.reel-slide-split__katex :deep(.reel-slide-split__katex-line .katex .mop),
.reel-slide-split__katex :deep(.reel-slide-split__katex-line .katex .mbin),
.reel-slide-split__katex :deep(.reel-slide-split__katex-line .katex .mrel),
.reel-slide-split__katex :deep(.reel-slide-split__katex-line .katex .mopen),
.reel-slide-split__katex :deep(.reel-slide-split__katex-line .katex .mclose),
.reel-slide-split__katex :deep(.reel-slide-split__katex-line .katex .mpunct),
.reel-slide-split__katex :deep(.reel-slide-split__katex-line .katex .minner),
.reel-slide-split__katex :deep(.reel-slide-split__katex-line .katex .mathnormal),
.reel-slide-split__katex :deep(.reel-slide-split__katex-line .katex .mathit),
.reel-slide-split__katex :deep(.reel-slide-split__katex-line .katex .mathrm) {
  color: #1e293b;
}

.reel-slide-split__katex :deep(.reel-slide-split__katex-line .katex) {
  font-size: calc(1.85cqw * var(--reel-split-right-scale, 1)) !important;
  max-width: 100%;
}

.slide-card:not(.slide-card--fullscreen) .reel-slide-split__right {
  padding: calc(1.8cqw * var(--reel-thumb-fit-scale, 1))
    calc(1.6cqw * var(--reel-thumb-fit-scale, 1));
}

.slide-card:not(.slide-card--fullscreen) .reel-slide-split__label {
  font-size: calc(1.45cqw * var(--reel-split-right-scale, 1) * var(--reel-thumb-fit-scale, 1));
}

.slide-card:not(.slide-card--fullscreen) .reel-slide-split__katex :deep(.reel-slide-split__katex-line .katex) {
  font-size: calc(1.85cqw * var(--reel-split-right-scale, 1) * var(--reel-thumb-fit-scale, 1)) !important;
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
