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
          :disabled="!slidesForRender.length || exportingPng"
          @click="exportAllSlidesPng"
        >
          {{ exportingPng ? `PNG ${pngExportProgress}/${slidesForRender.length}` : 'Exporter PNG' }}
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

    <div v-if="pngExportMounted" class="png-export-area" aria-hidden="true">
      <div
        v-for="(slide, index) in slidesForRender"
        :key="`png-export-${slide.id || index}`"
        :ref="(el) => setExportSlideRef(el, index)"
        class="png-export-frame"
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
          <div class="fullscreen-toolbar">
            <div class="fullscreen-control-group" aria-label="Taille des formules">
              <span class="control-label">{{ mathSizeLabel }}</span>
              <button class="size-button" type="button" @click="decreaseMathSize">A-</button>
              <span class="size-value">{{ mathSizePercent }}%</span>
              <button class="size-button" type="button" @click="increaseMathSize">A+</button>
              <button class="size-reset" type="button" @click="resetMathSize">Reset</button>
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

            <button class="fullscreen-close" type="button" @click="closeFullscreen">Fermer</button>
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
})

const emit = defineEmits(['select-slide', 'diagnostic', 'update-slide'])

const isFullscreen = ref(false)
const fullscreenIndex = ref(0)
const previousBodyOverflow = ref('')
const mathScaleCalcul = ref(1)
const mathScaleEdge = ref(1)
const safeZoneXScale = ref(1)
const safeZoneMathYScale = ref(1)
const safeZoneEdgeYScale = ref(1)
const exportingPng = ref(false)
const pngExportMounted = ref(false)
const pngExportProgress = ref(0)
const exportSlideRefs = ref([])

const slidesSafe = computed(() => (Array.isArray(props.slides) ? props.slides : []))
const NON_MATH_SLIDE_TYPES = new Set(['hook', 'cta'])
const PNG_EXPORT_WIDTH = 1080
const PNG_EXPORT_HEIGHT = 1920
const mathSizePercent = computed(() => Math.round(getMathScale(activeSlide.value) * 100))
const mathSizeLabel = computed(() => (isEdgeSlide(activeSlide.value) ? 'Taille Hook/CTA' : 'Taille Calcul'))
const safeZoneXPercent = computed(() => Math.round(safeZoneXScale.value * 100))
const safeZoneYPercent = computed(() => Math.round(getSafeZoneYScale(activeSlide.value) * 100))
const safeZoneYLabel = computed(() => (isEdgeSlide(activeSlide.value) ? 'Safe V Hook/CTA' : 'Safe V Calcul'))

function normalizeText(value) {
  return String(value || '').trim()
}

function isEdgeSlide(slide) {
  return NON_MATH_SLIDE_TYPES.has(normalizeText(slide?.slide_type).toLowerCase())
}

function getSafeZoneYScale(slide) {
  return isEdgeSlide(slide) ? safeZoneEdgeYScale.value : safeZoneMathYScale.value
}

function getMathScale(slide) {
  return isEdgeSlide(slide) ? mathScaleEdge.value : mathScaleCalcul.value
}

function getActiveSafeZoneYRef() {
  return isEdgeSlide(activeSlide.value) ? safeZoneEdgeYScale : safeZoneMathYScale
}

function getActiveMathScaleRef() {
  return isEdgeSlide(activeSlide.value) ? mathScaleEdge : mathScaleCalcul
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

async function exportAllSlidesPng() {
  if (!slidesForRender.value.length || exportingPng.value) return

  exportingPng.value = true
  pngExportMounted.value = true
  pngExportProgress.value = 0
  exportSlideRefs.value = []

  try {
    await waitForExportRender()

    for (const [index] of slidesForRender.value.entries()) {
      const frame = exportSlideRefs.value[index]
      const target = frame?.querySelector('.reel-slide') || frame
      if (!target) continue

      const canvas = await html2canvas(target, {
        backgroundColor: '#f8fbff',
        height: PNG_EXPORT_HEIGHT,
        logging: false,
        scale: 1,
        scrollX: 0,
        scrollY: 0,
        useCORS: true,
        width: PNG_EXPORT_WIDTH,
        windowHeight: PNG_EXPORT_HEIGHT,
        windowWidth: PNG_EXPORT_WIDTH,
      })

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
  width: min(1200px, 100%);
  max-height: 100dvh;
  display: flex;
  flex-direction: column;
  gap: 14px;
  align-items: center;
}

.fullscreen-toolbar {
  width: min(920px, 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
}

.fullscreen-control-group {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 1px solid rgba(191, 219, 254, 0.72);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.96);
  padding: 5px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.22);
}

.control-label {
  color: #1e3a8a;
  font-size: 12px;
  font-weight: 800;
  padding: 0 6px;
}

.fullscreen-close {
  border: 0;
  border-radius: 8px;
  background: #1d4ed8;
  color: #ffffff;
  font-size: 12px;
  font-weight: 800;
  padding: 10px 14px;
  cursor: pointer;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.22);
}

.fullscreen-close:hover {
  background: #1e40af;
}

.fullscreen-stage {
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
  width: 1080px;
  pointer-events: none;
  visibility: visible;
  z-index: 0;
}

.png-export-frame {
  width: 1080px;
  height: 1920px;
  overflow: hidden;
  background: #f8fbff;
}

.png-export-frame :deep(.slide-card) {
  width: 1080px !important;
  min-width: 1080px !important;
  max-width: 1080px !important;
  height: 1920px !important;
  padding: 0 !important;
  border: 0 !important;
  border-radius: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
}

.png-export-frame :deep(.reel-slide) {
  width: 1080px !important;
  height: 1920px !important;
  aspect-ratio: auto !important;
  border: 0 !important;
  border-radius: 0 !important;
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

  .fullscreen-toolbar {
    justify-content: flex-start;
  }

  .fullscreen-control-group {
    max-width: 100%;
    overflow-x: auto;
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
