<template>
  <section class="reel-preview-panel">
    <div class="preview-header">
      <h3>Aperçu des slides (9:16)</h3>
      <div class="preview-header-right">
        <button
          class="btn-fullscreen"
          type="button"
          :disabled="!slidesForRender.length"
          @click="openFromCurrent"
        >
          Plein écran
        </button>
        <button
          class="btn-fullscreen btn-png-export"
          type="button"
          :disabled="!slidesForRender.length || exportingPng || isVideoExportBusy"
          @click="exportAllSlidesPng"
        >
          {{ exportingPng ? `PNG ${pngExportProgress}/${slidesForRender.length}` : 'Exporter PNG' }}
        </button>
        <button
          class="btn-fullscreen btn-video-export btn-video-export-fast"
          type="button"
          :disabled="!slidesForRender.length || exportingPng || isVideoExportBusy"
          @click="exportAllSlidesVideo('fast')"
        >
          {{ videoFastExportButtonLabel }}
        </button>
        <button
          class="btn-fullscreen btn-video-export"
          type="button"
          :disabled="!slidesForRender.length || exportingPng || isVideoExportBusy"
          @click="exportAllSlidesVideo('hq')"
        >
          {{ videoHqExportButtonLabel }}
        </button>
        <div class="math-size-controls" aria-label="Taille des formules">
          <button class="size-button" type="button" @click="decreaseMathSize">A-</button>
          <span class="size-value">{{ mathSizePercent }}%</span>
          <button class="size-button" type="button" @click="increaseMathSize">A+</button>
          <button class="size-reset" type="button" @click="resetMathSize">Reset</button>
        </div>
        <span v-if="slidesForRender.length" class="preview-count">{{ slidesForRender.length }} slides</span>
      </div>
    </div>

    <p v-if="!slidesForRender.length" class="empty-state">Aucune slide à afficher.</p>

    <div v-else class="reel-preview-list">
      <ReelSlidePreview
        v-for="slide in slidesForRender"
        :key="slide.id"
        :slide="slide"
        :is-selected="Number(selectedSlideId) === Number(slide.id)"
        :math-scale="getMathScale(slide)"
        :safe-zone-x-scale="safeZoneXScale"
        :safe-zone-y-scale="getSafeZoneYScale(slide)"
        @select="handleSelectAndOpen(slide.id)"
        @diagnostic="$emit('diagnostic', $event)"
      />
    </div>

    <div v-if="pngExportMounted" class="png-export-area" :style="exportFrameStyle" aria-hidden="true">
      <div
        v-for="(slide, index) in slidesForRender"
        :key="`png-export-${slide.id || index}`"
        :ref="(el) => setExportSlideRef(el, index)"
        class="png-export-frame"
        :style="exportFrameStyle"
      >
        <ReelSlidePreview
          :slide="slide"
          :is-selected="false"
          display-mode="export"
          :clickable="false"
          :math-scale="getMathScale(slide)"
          :safe-zone-x-scale="safeZoneXScale"
          :safe-zone-y-scale="getSafeZoneYScale(slide)"
          @diagnostic="$emit('diagnostic', $event)"
        />
      </div>
    </div>

    <Teleport to="body">
      <div v-if="isFullscreen && activeSlide" class="fullscreen-backdrop" @click="closeFullscreen">
        <div class="fullscreen-content" @click.stop>
          <aside class="fullscreen-speech-panel" aria-label="Voix de la slide">
            <div class="speech-panel-header">
              <h4>Speech</h4>
              <span>{{ activeSlideIndexLabel }}</span>
            </div>

            <textarea
              class="speech-script"
              :value="activeSlideSpeechText"
              readonly
              rows="8"
            ></textarea>

            <audio
              v-if="activeSlideSpeechAudioUrl"
              :key="activeSlideSpeechAudioUrl"
              class="speech-player"
              :src="activeSlideSpeechAudioUrl"
              controls
              preload="metadata"
            ></audio>

            <p v-else class="speech-empty">{{ activeSlideSpeechStatusLabel }}</p>

            <button
              class="speech-generate-button"
              type="button"
              :disabled="isGeneratingActiveSpeech || !activeSlideSpeechText"
              @click="generateActiveSlideSpeech"
            >
              {{ isGeneratingActiveSpeech ? 'Generation...' : 'Generer cette slide' }}
            </button>
          </aside>

          <div class="fullscreen-toolbar">
            <div class="fullscreen-control-group" aria-label="Taille des formules">
              <span class="control-label">{{ mathSizeLabel }}</span>
              <button class="size-button" type="button" @click="decreaseMathSize">A-</button>
              <span class="size-value">{{ mathSizePercent }}%</span>
              <button class="size-button" type="button" @click="increaseMathSize">A+</button>
              <button class="size-reset" type="button" @click="resetMathSize">Reset</button>
            </div>

            <div
              v-if="activeSlide && isEdgeSlide(activeSlide)"
              class="fullscreen-control-group"
              aria-label="Taille du titre hook ou cta"
            >
              <span class="control-label">Titre</span>
              <button class="size-button" type="button" @click="decreaseActiveTitleSize">T-</button>
              <span class="size-value">{{ activeTitleSizePercent }}%</span>
              <button class="size-button" type="button" @click="increaseActiveTitleSize">T+</button>
              <button class="size-reset" type="button" @click="resetActiveTitleSize">Reset</button>
            </div>

            <div
              v-if="activeSlide && isEdgeSlide(activeSlide)"
              class="fullscreen-control-group"
              aria-label="Taille du texte hook ou cta"
            >
              <span class="control-label">Texte</span>
              <button class="size-button" type="button" @click="decreaseActiveTextSize">Txt-</button>
              <span class="size-value">{{ activeTextSizePercent }}%</span>
              <button class="size-button" type="button" @click="increaseActiveTextSize">Txt+</button>
              <button class="size-reset" type="button" @click="resetActiveTextSize">Reset</button>
            </div>

            <div class="fullscreen-control-group" aria-label="Safe zone horizontale">
              <span class="control-label">Safe H</span>
              <button class="size-button" type="button" @click="decreaseSafeZoneX">H-</button>
              <span class="size-value">{{ safeZoneXPercent }}%</span>
              <button class="size-button" type="button" @click="increaseSafeZoneX">H+</button>
              <button class="size-reset" type="button" @click="resetSafeZoneX">Reset</button>
            </div>

            <div class="fullscreen-control-group" aria-label="Safe zone verticale">
              <span class="control-label">{{ safeZoneYLabel }}</span>
              <button class="size-button" type="button" @click="decreaseSafeZoneY">V-</button>
              <span class="size-value">{{ safeZoneYPercent }}%</span>
              <button class="size-button" type="button" @click="increaseSafeZoneY">V+</button>
              <button class="size-reset" type="button" @click="resetSafeZoneY">Reset</button>
            </div>

            <div
              v-if="activeSlide && !isEdgeSlide(activeSlide)"
              class="fullscreen-control-group"
              aria-label="Disposition KaTeX"
            >
              <span class="control-label">KaTeX</span>
              <button
                class="size-reset line-mode-button"
                :class="{ 'line-mode-button--active': activeSlideInline }"
                type="button"
                :disabled="!canToggleKatexLineMode"
                @click="toggleActiveKatexLineMode"
              >
                {{ lineModeLabel }}
              </button>
            </div>

            <div
              v-if="activeSlide && !isEdgeSlide(activeSlide)"
              class="fullscreen-control-group"
              aria-label="Page de correction"
            >
              <span class="control-label">Cumul</span>
              <button
                class="size-reset line-mode-button"
                :class="{ 'line-mode-button--active': activeSlideResetsCumulative }"
                type="button"
                @click="toggleActiveResetCumulative"
              >
                {{ resetCumulativeLabel }}
              </button>
            </div>

          </div>

          <div class="fullscreen-stage">
            <button
              class="nav-arrow"
              type="button"
              aria-label="Slide précédente"
              @click="goPrev"
            >
              ‹
            </button>

            <ReelSlidePreview
              :key="activeSlide.id"
              :slide="activeSlide"
              :is-selected="true"
              display-mode="fullscreen"
              :clickable="false"
              :math-scale="getMathScale(activeSlide)"
              :safe-zone-x-scale="safeZoneXScale"
              :safe-zone-y-scale="getSafeZoneYScale(activeSlide)"
              @diagnostic="$emit('diagnostic', $event)"
            />

            <button
              class="nav-arrow"
              type="button"
              aria-label="Slide suivante"
              @click="goNext"
            >
              ›
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </section>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, ref, watch } from 'vue'
import html2canvas from 'html2canvas'
import ReelSlidePreview from './ReelSlidePreview.vue'

const props = defineProps({
  slides: {
    type: Array,
    default: () => [],
  },
  selectedSlideId: {
    type: [Number, String, null],
    default: null,
  },
  generatingSpeechSlideId: {
    type: [Number, String, null],
    default: null,
  },
  exportingVideo: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['select-slide', 'diagnostic', 'update-slide', 'generate-slide-speech', 'export-video'])

const isFullscreen = ref(false)
const fullscreenIndex = ref(0)
const previousBodyOverflow = ref('')
const mathScaleCalcul = ref(1)
const mathScaleHook = ref(1)
const mathScaleCta = ref(1)
const safeZoneXScale = ref(1)
const safeZoneMathYScale = ref(1)
const safeZoneHookYScale = ref(1)
const safeZoneCtaYScale = ref(1)
const exportingPng = ref(false)
const preparingVideoFrames = ref(false)
const pngExportMounted = ref(false)
const pngExportProgress = ref(0)
const videoFrameProgress = ref(0)
const videoExportMode = ref('fast')
const exportFrameWidth = ref(1080)
const exportFrameHeight = ref(1920)
const exportSlideRefs = ref([])

const slidesSafe = computed(() => (Array.isArray(props.slides) ? props.slides : []))
const NON_MATH_SLIDE_TYPES = new Set(['hook', 'cta'])
const PNG_EXPORT_WIDTH = 1080
const PNG_EXPORT_HEIGHT = 1920
const VIDEO_EXPORT_PRESETS = {
  fast: {
    width: 720,
    height: 1280,
    fps: 24,
    crf: 24,
    ffmpegPreset: 'ultrafast',
    imageType: 'image/jpeg',
    imageQuality: 0.9,
  },
  hq: {
    width: 1080,
    height: 1920,
    fps: 30,
    crf: 18,
    ffmpegPreset: 'veryfast',
    imageType: 'image/png',
    imageQuality: 1,
  },
}
const mathSizePercent = computed(() => Math.round(getMathScale(activeSlide.value) * 100))
const mathSizeLabel = computed(() => getActiveSlideTypeLabel('Taille'))
const safeZoneXPercent = computed(() => Math.round(safeZoneXScale.value * 100))
const safeZoneYPercent = computed(() => Math.round(getSafeZoneYScale(activeSlide.value) * 100))
const safeZoneYLabel = computed(() => getActiveSlideTypeLabel('Safe V'))
const activeTitleSizePercent = computed(() => Math.round(getSlideScale(activeSlide.value?.title_scale) * 100))
const activeTextSizePercent = computed(() => Math.round(getSlideScale(activeSlide.value?.screen_text_scale) * 100))
const activeSlideIndexLabel = computed(() => {
  if (!slidesForRender.value.length) return ''
  return `Slide ${fullscreenIndex.value + 1}/${slidesForRender.value.length}`
})
const activeSlideSpeechText = computed(() => slideSpeechText(activeSlide.value))
const activeSlideSpeechAudioUrl = computed(() => normalizeText(activeSlide.value?.speech_audio_url))
const isGeneratingActiveSpeech = computed(() => (
  activeSlide.value?.id &&
  Number(props.generatingSpeechSlideId) === Number(activeSlide.value.id)
))
const activeSlideSpeechStatusLabel = computed(() => {
  if (isGeneratingActiveSpeech.value) return 'Generation audio en cours.'
  if (activeSlide.value?.speech_status === 'error') return activeSlide.value.speech_error || 'Erreur audio.'
  if (!activeSlideSpeechText.value) return 'Aucun texte vocal pour cette slide.'
  return 'Aucun MP3 genere pour cette slide.'
})
const isVideoExportBusy = computed(() => Boolean(preparingVideoFrames.value || props.exportingVideo))
const exportFrameStyle = computed(() => ({
  '--export-width': `${exportFrameWidth.value}px`,
  '--export-height': `${exportFrameHeight.value}px`,
}))
const videoFastExportButtonLabel = computed(() => {
  if (props.exportingVideo && videoExportMode.value === 'fast') return 'Assemblage rapide...'
  if (preparingVideoFrames.value && videoExportMode.value === 'fast') return `Rapide ${videoFrameProgress.value}/${slidesForRender.value.length}`
  return 'MP4 rapide'
})
const videoHqExportButtonLabel = computed(() => {
  if (props.exportingVideo && videoExportMode.value === 'hq') return 'Assemblage HQ...'
  if (preparingVideoFrames.value && videoExportMode.value === 'hq') return `HQ ${videoFrameProgress.value}/${slidesForRender.value.length}`
  return 'MP4 HQ'
})

function normalizeText(value) {
  return String(value || '').trim()
}

function normalizeSpeechLine(value) {
  return String(value || '')
    .replace(/\r\n/g, '\n')
    .replace(/\r/g, '\n')
    .split('\n')
    .map((line) => line.replace(/\s+/g, ' ').trim())
    .filter(Boolean)
    .join(' ')
}

function slideSpeechText(slide) {
  const voice = normalizeSpeechLine(slide?.voice_script)
  if (voice) return voice

  return [slide?.title, slide?.screen_text]
    .map((part) => normalizeSpeechLine(part))
    .filter(Boolean)
    .join('. ')
}

function getSlideType(slide) {
  return normalizeText(slide?.slide_type).toLowerCase()
}

function isEdgeSlide(slide) {
  return NON_MATH_SLIDE_TYPES.has(getSlideType(slide))
}

function getActiveSlideTypeLabel(prefix) {
  const slideType = getSlideType(activeSlide.value)
  if (slideType === 'hook') return `${prefix} Hook`
  if (slideType === 'cta') return `${prefix} CTA`
  return `${prefix} Calcul`
}

function getSafeZoneYScale(slide) {
  const slideType = getSlideType(slide)
  if (slideType === 'hook') return safeZoneHookYScale.value
  if (slideType === 'cta') return safeZoneCtaYScale.value
  return safeZoneMathYScale.value
}

function getMathScale(slide) {
  const slideType = getSlideType(slide)
  if (slideType === 'hook') return mathScaleHook.value
  if (slideType === 'cta') return mathScaleCta.value
  return mathScaleCalcul.value
}

function getActiveSafeZoneYRef() {
  const slideType = getSlideType(activeSlide.value)
  if (slideType === 'hook') return safeZoneHookYScale
  if (slideType === 'cta') return safeZoneCtaYScale
  return safeZoneMathYScale
}

function getActiveMathScaleRef() {
  const slideType = getSlideType(activeSlide.value)
  if (slideType === 'hook') return mathScaleHook
  if (slideType === 'cta') return mathScaleCta
  return mathScaleCalcul
}

function getSlideScale(value) {
  const nextValue = Number(value) || 1
  return Math.min(2, Math.max(0.5, Number(nextValue.toFixed(2))))
}

function isAlignedKatexBlock(value) {
  return /^\\begin\{aligned\}[\s\S]*\\end\{aligned\}$/.test(normalizeText(value))
}

function unwrapAlignedBlock(value) {
  return normalizeText(value)
    .replace(/^\\begin\{aligned\}\s*/, '')
    .replace(/\s*\\end\{aligned\}$/, '')
    .trim()
}

function splitAlignedLines(innerBlock) {
  return String(innerBlock || '')
    .split(/\\\\(?:\[[^\]]*\])?/)
    .map((line) => line.trim())
    .filter(Boolean)
}

function splitKatexLines(block) {
  const raw = normalizeText(block)
  if (!raw) return []

  if (isAlignedKatexBlock(raw)) {
    return splitAlignedLines(unwrapAlignedBlock(raw))
  }

  return raw
    .split(/\\\\(?:\[[^\]]*\])?/)
    .map((line) => line.trim())
    .filter(Boolean)
}

function normalizeKatexLine(line) {
  return String(line || '')
    .replace(/^&\s*/, '')
    .replace(/\s+/g, ' ')
    .trim()
}

function toAlignedKatexRows(rows) {
  const prepared = (Array.isArray(rows) ? rows : [])
    .map((row) => {
      const rowLines = Array.isArray(row) ? row : [row]
      const rowContent = rowLines
        .map((line) => String(line || '').trim())
        .map((line) => line.replace(/^&+\s*/, ''))
        .filter(Boolean)
        .join('\\qquad ')
      return rowContent ? `&${rowContent}` : ''
    })
    .filter(Boolean)

  if (!prepared.length) return ''
  return `\\begin{aligned}\n${prepared.join('\\\\[0.4em]\n')}\n\\end{aligned}`
}

const slidesForRender = computed(() => {
  let cumulativeRows = []
  let cumulativeLineKeys = new Set()
  let carriedScreenText = ''

  return slidesSafe.value.map((slide) => {
    const safeSlide = slide && typeof slide === 'object' ? slide : {}
    const slideType = normalizeText(safeSlide.slide_type).toLowerCase()
    const baseText = normalizeText(safeSlide.screen_text)
    const baseKatex = normalizeText(safeSlide.katex)

    if (NON_MATH_SLIDE_TYPES.has(slideType)) {
      cumulativeRows = []
      cumulativeLineKeys = new Set()
      carriedScreenText = ''
      return {
        ...safeSlide,
        display_screen_text: baseText,
        display_katex: baseKatex,
      }
    }

    if (baseText) {
      carriedScreenText = baseText
    }
    const displayScreenText = baseText || carriedScreenText
    if (safeSlide.katex_reset_cumulative) {
      cumulativeRows = []
      cumulativeLineKeys = new Set()
    }

    if (slideType === 'katex') {
      const currentLines = splitKatexLines(baseKatex)
      const inlineWithPrevious = Boolean(safeSlide.katex_inline_with_previous) && cumulativeRows.length > 0
      for (const line of currentLines) {
        const key = normalizeKatexLine(line)
        if (!key || cumulativeLineKeys.has(key)) continue
        cumulativeLineKeys.add(key)
        if (inlineWithPrevious) {
          cumulativeRows[cumulativeRows.length - 1].push(line)
        } else {
          cumulativeRows.push([line])
        }
      }
      return {
        ...safeSlide,
        display_screen_text: displayScreenText,
        display_katex: toAlignedKatexRows(cumulativeRows) || baseKatex,
      }
    }

    if (slideType === 'cumulative_katex' || slideType === 'result') {
      const currentLines = splitKatexLines(baseKatex)
      const inlineWithPrevious = Boolean(safeSlide.katex_inline_with_previous) && cumulativeRows.length > 0
      for (const line of currentLines) {
        const key = normalizeKatexLine(line)
        if (!key || cumulativeLineKeys.has(key)) continue
        cumulativeLineKeys.add(key)
        if (inlineWithPrevious) {
          cumulativeRows[cumulativeRows.length - 1].push(line)
        } else {
          cumulativeRows.push([line])
        }
      }
      return {
        ...safeSlide,
        display_screen_text: displayScreenText,
        display_katex: toAlignedKatexRows(cumulativeRows),
      }
    }

    return {
      ...safeSlide,
      display_screen_text: displayScreenText,
      display_katex: baseKatex,
    }
  })
})

const activeSlide = computed(() => {
  if (!slidesForRender.value.length) return null
  const index = Math.min(Math.max(fullscreenIndex.value, 0), slidesForRender.value.length - 1)
  return slidesForRender.value[index] || null
})

const activeSlideInline = computed(() => Boolean(activeSlide.value?.katex_inline_with_previous))
const activeSlideResetsCumulative = computed(() => Boolean(activeSlide.value?.katex_reset_cumulative))
const canToggleKatexLineMode = computed(() => {
  if (!activeSlide.value || isEdgeSlide(activeSlide.value)) return false

  for (let index = fullscreenIndex.value - 1; index >= 0; index -= 1) {
    const previousSlide = slidesForRender.value[index]
    if (!previousSlide) return false
    if (isEdgeSlide(previousSlide)) return false
    return true
  }

  return false
})
const lineModeLabel = computed(() => (activeSlideInline.value ? 'Même ligne' : 'Nouvelle ligne'))
const resetCumulativeLabel = computed(() => (activeSlideResetsCumulative.value ? 'Nouvelle page' : 'Même page'))

function findIndexById(slideId) {
  return slidesForRender.value.findIndex((slide) => Number(slide.id) === Number(slideId))
}

function selectSlideByIndex(index) {
  const slide = slidesForRender.value[index]
  if (!slide?.id) return
  emit('select-slide', slide.id)
}

function openFullscreenAt(index) {
  if (!slidesForRender.value.length) return
  const maxIndex = slidesForRender.value.length - 1
  const normalizedIndex = Math.min(Math.max(index, 0), maxIndex)

  fullscreenIndex.value = normalizedIndex
  isFullscreen.value = true
  selectSlideByIndex(normalizedIndex)
}

function closeFullscreen() {
  isFullscreen.value = false
}

function clampMathScale(value) {
  return Math.min(1.3, Math.max(0.75, Number(value.toFixed(2))))
}

function decreaseMathSize() {
  const target = getActiveMathScaleRef()
  target.value = clampMathScale(target.value - 0.05)
}

function increaseMathSize() {
  const target = getActiveMathScaleRef()
  target.value = clampMathScale(target.value + 0.05)
}

function resetMathSize() {
  getActiveMathScaleRef().value = 1
}

function clampSafeZoneScale(value) {
  return Math.min(1.4, Math.max(0.7, Number(value.toFixed(2))))
}

function decreaseSafeZoneX() {
  safeZoneXScale.value = clampSafeZoneScale(safeZoneXScale.value - 0.05)
}

function increaseSafeZoneX() {
  safeZoneXScale.value = clampSafeZoneScale(safeZoneXScale.value + 0.05)
}

function resetSafeZoneX() {
  safeZoneXScale.value = 1
}

function decreaseSafeZoneY() {
  const target = getActiveSafeZoneYRef()
  target.value = clampSafeZoneScale(target.value - 0.05)
}

function increaseSafeZoneY() {
  const target = getActiveSafeZoneYRef()
  target.value = clampSafeZoneScale(target.value + 0.05)
}

function resetSafeZoneY() {
  getActiveSafeZoneYRef().value = 1
}

function patchActiveEdgeSlideScale(field, value) {
  if (!activeSlide.value?.id || !isEdgeSlide(activeSlide.value)) return

  emit('update-slide', {
    id: activeSlide.value.id,
    patch: {
      [field]: getSlideScale(value),
    },
  })
}

function decreaseActiveTitleSize() {
  patchActiveEdgeSlideScale('title_scale', getSlideScale(activeSlide.value?.title_scale) - 0.05)
}

function increaseActiveTitleSize() {
  patchActiveEdgeSlideScale('title_scale', getSlideScale(activeSlide.value?.title_scale) + 0.05)
}

function resetActiveTitleSize() {
  patchActiveEdgeSlideScale('title_scale', 1)
}

function decreaseActiveTextSize() {
  patchActiveEdgeSlideScale('screen_text_scale', getSlideScale(activeSlide.value?.screen_text_scale) - 0.05)
}

function increaseActiveTextSize() {
  patchActiveEdgeSlideScale('screen_text_scale', getSlideScale(activeSlide.value?.screen_text_scale) + 0.05)
}

function resetActiveTextSize() {
  patchActiveEdgeSlideScale('screen_text_scale', 1)
}

function toggleActiveKatexLineMode() {
  if (!canToggleKatexLineMode.value || !activeSlide.value?.id) return

  emit('update-slide', {
    id: activeSlide.value.id,
    patch: {
      katex_inline_with_previous: !activeSlideInline.value,
    },
  })
}

function toggleActiveResetCumulative() {
  if (!activeSlide.value?.id || isEdgeSlide(activeSlide.value)) return

  emit('update-slide', {
    id: activeSlide.value.id,
    patch: {
      katex_reset_cumulative: !activeSlideResetsCumulative.value,
    },
  })
}

function generateActiveSlideSpeech() {
  if (!activeSlide.value?.id || !activeSlideSpeechText.value || isGeneratingActiveSpeech.value) return
  emit('generate-slide-speech', activeSlide.value.id)
}

function setExportSlideRef(el, index) {
  if (el) {
    exportSlideRefs.value[index] = el
  }
}

function waitForNextPaint() {
  if (typeof window === 'undefined' || typeof window.requestAnimationFrame !== 'function') {
    return Promise.resolve()
  }

  return new Promise((resolve) => {
    window.requestAnimationFrame(() => {
      window.requestAnimationFrame(resolve)
    })
  })
}

async function waitForExportRender() {
  await nextTick()

  if (typeof document !== 'undefined' && document.fonts?.ready) {
    await document.fonts.ready.catch(() => {})
  }

  await waitForNextPaint()
}

async function downloadCanvasPng(canvas, filename) {
  const blob = await new Promise((resolve) => {
    canvas.toBlob((result) => resolve(result), 'image/png', 1)
  })
  const link = document.createElement('a')
  link.download = filename

  if (blob) {
    const url = URL.createObjectURL(blob)
    link.href = url
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.setTimeout(() => URL.revokeObjectURL(url), 1200)
    return
  }

  link.href = canvas.toDataURL('image/png')
  document.body.appendChild(link)
  link.click()
  link.remove()
}

function blobToDataUrl(blob) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result)
    reader.onerror = () => reject(reader.error)
    reader.readAsDataURL(blob)
  })
}

async function canvasToImageDataUrl(canvas, exportPreset) {
  const imageType = exportPreset?.imageType || 'image/png'
  const imageQuality = exportPreset?.imageQuality ?? 1
  const blob = await new Promise((resolve) => {
    canvas.toBlob((result) => resolve(result), imageType, imageQuality)
  })

  if (blob) {
    return blobToDataUrl(blob)
  }

  return canvas.toDataURL(imageType, imageQuality)
}

async function renderExportCanvas(index, dimensions = {}) {
  const frame = exportSlideRefs.value[index]
  const target = frame?.querySelector('.reel-slide') || frame
  if (!target) return null
  const width = dimensions.width || PNG_EXPORT_WIDTH
  const height = dimensions.height || PNG_EXPORT_HEIGHT

  return html2canvas(target, {
    backgroundColor: '#f8fbff',
    height,
    logging: false,
    scale: 1,
    scrollX: 0,
    scrollY: 0,
    useCORS: true,
    width,
    windowHeight: height,
    windowWidth: width,
  })
}

async function exportAllSlidesPng() {
  if (!slidesForRender.value.length || exportingPng.value) return

  exportFrameWidth.value = PNG_EXPORT_WIDTH
  exportFrameHeight.value = PNG_EXPORT_HEIGHT
  exportingPng.value = true
  pngExportMounted.value = true
  pngExportProgress.value = 0
  exportSlideRefs.value = []

  try {
    await waitForExportRender()

    for (const [index] of slidesForRender.value.entries()) {
      const canvas = await renderExportCanvas(index)
      if (!canvas) continue

      const filename = `optitab-reel-slide-${String(index + 1).padStart(2, '0')}.png`
      await downloadCanvasPng(canvas, filename)
      pngExportProgress.value = index + 1
      await new Promise((resolve) => window.setTimeout(resolve, 180))
    }
  } catch (error) {
    console.error('Erreur export PNG:', error)
    window.alert("Erreur lors de l'export PNG. Réessaie après avoir vérifié les slides.")
  } finally {
    pngExportMounted.value = false
    exportingPng.value = false
    exportSlideRefs.value = []
  }
}

async function exportAllSlidesVideo(mode = 'fast') {
  if (!slidesForRender.value.length || isVideoExportBusy.value || exportingPng.value) return
  const exportPreset = VIDEO_EXPORT_PRESETS[mode] || VIDEO_EXPORT_PRESETS.fast

  const slidesMissingAudio = slidesForRender.value.filter((slide) => (
    slideSpeechText(slide) && !normalizeText(slide?.speech_audio_url)
  ))
  if (
    slidesMissingAudio.length &&
    !window.confirm(`${slidesMissingAudio.length} slide(s) ont un script voix sans MP3. Exporter quand meme avec silence sur ces slides ?`)
  ) {
    return
  }

  videoExportMode.value = mode
  exportFrameWidth.value = exportPreset.width
  exportFrameHeight.value = exportPreset.height
  preparingVideoFrames.value = true
  pngExportMounted.value = true
  videoFrameProgress.value = 0
  exportSlideRefs.value = []

  try {
    await waitForExportRender()

    const frames = []
    for (const [index, slide] of slidesForRender.value.entries()) {
      const canvas = await renderExportCanvas(index, exportPreset)
      if (!canvas) continue

      frames.push({
        slide_id: slide.id,
        image: await canvasToImageDataUrl(canvas, exportPreset),
        duration_seconds: Number(slide.duration_seconds) || 4,
      })
      videoFrameProgress.value = index + 1
      await waitForNextPaint()
    }

    if (!frames.length) {
      window.alert("Aucune frame video n'a pu etre preparee.")
      return
    }

    emit('export-video', {
      frames,
      width: exportPreset.width,
      height: exportPreset.height,
      fps: exportPreset.fps,
      crf: exportPreset.crf,
      preset: exportPreset.ffmpegPreset,
    })
  } catch (error) {
    console.error('Erreur export video:', error)
    window.alert("Erreur lors de la preparation video. Reessaie apres avoir verifie les slides.")
  } finally {
    pngExportMounted.value = false
    preparingVideoFrames.value = false
    exportSlideRefs.value = []
  }
}

function handleSelectAndOpen(slideId) {
  const index = findIndexById(slideId)
  if (index === -1) return
  openFullscreenAt(index)
}

function openFromCurrent() {
  if (!slidesForRender.value.length) return
  const indexFromSelection = findIndexById(props.selectedSlideId)
  openFullscreenAt(indexFromSelection === -1 ? 0 : indexFromSelection)
}

function goNext() {
  if (!slidesForRender.value.length) return
  const nextIndex = (fullscreenIndex.value + 1) % slidesForRender.value.length
  fullscreenIndex.value = nextIndex
  selectSlideByIndex(nextIndex)
}

function goPrev() {
  if (!slidesForRender.value.length) return
  const prevIndex = (fullscreenIndex.value - 1 + slidesForRender.value.length) % slidesForRender.value.length
  fullscreenIndex.value = prevIndex
  selectSlideByIndex(prevIndex)
}

function handleKeydown(event) {
  if (!isFullscreen.value) return

  if (event.key === 'Escape') {
    event.preventDefault()
    closeFullscreen()
    return
  }

  if (event.key === 'ArrowRight') {
    event.preventDefault()
    goNext()
    return
  }

  if (event.key === 'ArrowLeft') {
    event.preventDefault()
    goPrev()
  }
}

watch(
  () => props.selectedSlideId,
  (slideId) => {
    if (!isFullscreen.value || slideId === null || slideId === undefined) return
    const index = findIndexById(slideId)
    if (index !== -1) {
      fullscreenIndex.value = index
    }
  }
)

watch(
  () => slidesForRender.value.length,
  (length) => {
    if (!length) {
      closeFullscreen()
      fullscreenIndex.value = 0
      return
    }

    if (fullscreenIndex.value > length - 1) {
      fullscreenIndex.value = length - 1
    }
  }
)

watch(isFullscreen, (open) => {
  if (typeof window === 'undefined' || typeof document === 'undefined') return

  if (open) {
    previousBodyOverflow.value = document.body.style.overflow || ''
    document.body.style.overflow = 'hidden'
    window.addEventListener('keydown', handleKeydown)
    return
  }

  document.body.style.overflow = previousBodyOverflow.value
  window.removeEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('keydown', handleKeydown)
  }

  if (typeof document !== 'undefined') {
    document.body.style.overflow = previousBodyOverflow.value
  }
})
</script>

<style scoped>
.reel-preview-panel {
  border: 1px solid #bfdbfe;
  border-radius: 12px;
  background: #f8fbff;
  padding: 16px;
}

.preview-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 12px;
}

.preview-header h3 {
  margin: 0;
  color: #1e40af;
  font-size: 18px;
}

.preview-header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.math-size-controls {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  background: #ffffff;
  padding: 4px;
}

.size-button,
.size-reset {
  border: 0;
  border-radius: 6px;
  background: #eff6ff;
  color: #1e40af;
  font-size: 12px;
  font-weight: 800;
  line-height: 1;
  padding: 7px 8px;
  cursor: pointer;
}

.size-button:hover,
.size-reset:hover {
  background: #dbeafe;
}

.line-mode-button {
  min-width: 104px;
}

.line-mode-button--active {
  background: #1d4ed8;
  color: #ffffff;
}

.line-mode-button--active:hover {
  background: #1e40af;
}

.line-mode-button:disabled {
  background: #e2e8f0;
  color: #64748b;
  cursor: not-allowed;
}

.size-value {
  min-width: 38px;
  color: #1e3a8a;
  font-size: 12px;
  font-weight: 800;
  text-align: center;
}

.btn-fullscreen {
  border: 0;
  border-radius: 8px;
  background: #1d4ed8;
  color: #ffffff;
  font-size: 12px;
  font-weight: 700;
  padding: 8px 12px;
  cursor: pointer;
}

.btn-fullscreen:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

.btn-png-export {
  background: #0f766e;
}

.btn-png-export:hover:not(:disabled) {
  background: #115e59;
}

.btn-video-export {
  background: #7c3aed;
}

.btn-video-export-fast {
  background: #2563eb;
}

.btn-video-export:hover:not(:disabled) {
  background: #6d28d9;
}

.btn-video-export-fast:hover:not(:disabled) {
  background: #1d4ed8;
}

.preview-count {
  font-size: 12px;
  font-weight: 700;
  color: #1d4ed8;
  background: #dbeafe;
  border-radius: 999px;
  padding: 4px 10px;
}

.empty-state {
  margin: 0;
  color: #1e3a8a;
  font-size: 14px;
}

.reel-preview-list {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.fullscreen-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.78);
  backdrop-filter: blur(2px);
  z-index: 26000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.fullscreen-content {
  width: min(1500px, 100%);
  max-height: calc(100dvh - 40px);
  display: grid;
  grid-template-columns: minmax(230px, 310px) minmax(0, auto) minmax(230px, 300px);
  gap: 20px;
  align-items: center;
  justify-content: center;
}

.fullscreen-speech-panel {
  grid-column: 1;
  grid-row: 1;
  width: 100%;
  max-height: calc(100dvh - 56px);
  border: 1px solid rgba(191, 219, 254, 0.72);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.96);
  padding: 12px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.22);
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow-y: auto;
}

.speech-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.speech-panel-header h4 {
  margin: 0;
  color: #0f172a;
  font-size: 15px;
}

.speech-panel-header span {
  border-radius: 999px;
  background: #dbeafe;
  color: #1d4ed8;
  font-size: 11px;
  font-weight: 800;
  padding: 4px 8px;
}

.speech-script {
  width: 100%;
  min-height: 132px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: #f8fafc;
  color: #0f172a;
  font: inherit;
  font-size: 13px;
  line-height: 1.45;
  padding: 10px;
  resize: vertical;
}

.speech-player {
  width: 100%;
}

.speech-empty {
  margin: 0;
  border: 1px dashed #bfdbfe;
  border-radius: 8px;
  background: #eff6ff;
  color: #1e3a8a;
  font-size: 12px;
  font-weight: 700;
  line-height: 1.4;
  padding: 10px;
}

.speech-generate-button {
  border: 0;
  border-radius: 8px;
  background: #1d4ed8;
  color: #ffffff;
  font-size: 13px;
  font-weight: 800;
  padding: 10px 12px;
  cursor: pointer;
}

.speech-generate-button:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

.fullscreen-toolbar {
  grid-column: 3;
  grid-row: 1;
  width: 100%;
  max-height: calc(100dvh - 56px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 10px;
  overflow-y: auto;
  padding-right: 2px;
}

.fullscreen-control-group {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 6px;
  flex-wrap: wrap;
  border: 1px solid rgba(191, 219, 254, 0.72);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.96);
  padding: 8px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.22);
}

.control-label {
  flex: 1 0 100%;
  color: #1e3a8a;
  font-size: 12px;
  font-weight: 800;
  padding: 0 2px;
}

.fullscreen-stage {
  grid-column: 2;
  grid-row: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  justify-items: center;
  gap: 14px;
}

.nav-arrow {
  width: 52px;
  height: 52px;
  border-radius: 999px;
  border: 1px solid rgba(59, 130, 246, 0.5);
  background: rgba(29, 78, 216, 0.38);
  color: #eff6ff;
  font-size: 36px;
  line-height: 1;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.nav-arrow:hover {
  background: rgba(37, 99, 235, 0.58);
}

.png-export-area {
  position: fixed;
  top: 0;
  left: -12000px;
  width: var(--export-width, 1080px);
  pointer-events: none;
  visibility: visible;
  z-index: 0;
}

.png-export-frame {
  width: var(--export-width, 1080px);
  height: var(--export-height, 1920px);
  overflow: hidden;
  background: #f8fbff;
}

.png-export-frame :deep(.slide-card) {
  width: var(--export-width, 1080px) !important;
  min-width: var(--export-width, 1080px) !important;
  max-width: var(--export-width, 1080px) !important;
  height: var(--export-height, 1920px) !important;
  padding: 0 !important;
  border: 0 !important;
  border-radius: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
}

.png-export-frame :deep(.reel-slide) {
  width: var(--export-width, 1080px) !important;
  height: var(--export-height, 1920px) !important;
  aspect-ratio: auto !important;
  border: 0 !important;
  border-radius: 0 !important;
}

@media (max-width: 980px) {
  .fullscreen-content {
    width: 100%;
    max-height: calc(100dvh - 40px);
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .fullscreen-toolbar {
    grid-column: 1;
    grid-row: 3;
    justify-self: center;
    width: min(640px, 100%);
    max-height: 28dvh;
    align-items: stretch;
  }

  .fullscreen-speech-panel {
    grid-column: 1;
    grid-row: 2;
    justify-self: center;
    width: min(640px, 100%);
    max-height: 28dvh;
  }

  .fullscreen-control-group {
    max-width: 100%;
    overflow-x: auto;
  }

  .fullscreen-stage {
    grid-column: 1;
    grid-row: 1;
    gap: 8px;
  }
}

@media (max-width: 680px) {
  .preview-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .preview-header-right {
    flex-wrap: wrap;
  }

  .fullscreen-backdrop {
    padding: 10px;
  }

  .fullscreen-content {
    max-height: calc(100dvh - 20px);
  }

  .fullscreen-toolbar {
    width: 100%;
  }

  .nav-arrow {
    width: 44px;
    height: 44px;
    font-size: 28px;
  }

  .fullscreen-stage {
    gap: 8px;
  }
}
</style>
