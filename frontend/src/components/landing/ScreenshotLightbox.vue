<script setup>
import { computed, nextTick, onBeforeUnmount, ref, watch } from 'vue'
import { lockBodyScroll, unlockBodyScroll } from '@/utils/bodyScrollLock'

const SCROLL_LOCK_KEY = 'screenshot-lightbox'

const props = defineProps({
  open: { type: Boolean, default: false },
  /** [{ src, alt, name, author, role, channel }] */
  items: { type: Array, default: () => [] },
  index: { type: Number, default: 0 }
})

const emit = defineEmits(['close', 'update:index'])

const dialogRef = ref(null)
const closeButtonRef = ref(null)
let lastFocusedElement = null

const total = computed(() => props.items.length)
const current = computed(() => props.items[props.index] || null)
const hasMultiple = computed(() => total.value > 1)

// Si un prénom est affiché, profil et niveau passent en sous-titre.
const lightboxSubtitle = computed(() => {
  const item = current.value
  if (!item) return ''
  if (item.name) return [item.author, item.role].filter(Boolean).join(' · ')
  return item.author ? item.role : ''
})

function close() {
  emit('close')
}

function go(step) {
  if (!hasMultiple.value) return
  const next = (props.index + step + total.value) % total.value
  emit('update:index', next)
}

function onKeydown(event) {
  if (event.key === 'Escape') {
    event.preventDefault()
    close()
    return
  }
  if (event.key === 'ArrowRight') {
    event.preventDefault()
    go(1)
    return
  }
  if (event.key === 'ArrowLeft') {
    event.preventDefault()
    go(-1)
    return
  }
  if (event.key !== 'Tab') return

  // Piège à focus : le clavier ne doit pas sortir de la visionneuse.
  const root = dialogRef.value
  if (!root) return
  const focusables = root.querySelectorAll(
    'button:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])'
  )
  if (!focusables.length) return
  const first = focusables[0]
  const last = focusables[focusables.length - 1]
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault()
    last.focus()
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault()
    first.focus()
  }
}

function onBackdropClick(event) {
  if (event.target === event.currentTarget) close()
}

watch(
  () => props.open,
  async (isOpen) => {
    if (typeof document === 'undefined') return
    if (isOpen) {
      lastFocusedElement = document.activeElement
      lockBodyScroll(SCROLL_LOCK_KEY, { mode: 'overflow' })
      document.addEventListener('keydown', onKeydown)
      await nextTick()
      closeButtonRef.value?.focus()
    } else {
      document.removeEventListener('keydown', onKeydown)
      unlockBodyScroll(SCROLL_LOCK_KEY)
      if (lastFocusedElement && typeof lastFocusedElement.focus === 'function') {
        lastFocusedElement.focus()
      }
      lastFocusedElement = null
    }
  }
)

onBeforeUnmount(() => {
  if (typeof document === 'undefined') return
  document.removeEventListener('keydown', onKeydown)
  if (props.open) unlockBodyScroll(SCROLL_LOCK_KEY)
})
</script>

<template>
  <Teleport to="body">
    <Transition name="lightbox-fade">
      <div
        v-if="open && current"
        ref="dialogRef"
        class="lightbox"
        role="dialog"
        aria-modal="true"
        aria-label="Capture originale du témoignage"
        @click="onBackdropClick"
      >
        <div class="lightbox__panel">
          <header class="lightbox__head">
            <div class="lightbox__identity">
              <p class="lightbox__title">
                {{ current.name || current.author || current.role || 'Capture originale' }}
              </p>
              <p v-if="lightboxSubtitle" class="lightbox__subtitle">{{ lightboxSubtitle }}</p>
            </div>
            <button
              ref="closeButtonRef"
              type="button"
              class="lightbox__close"
              aria-label="Fermer la capture"
              @click="close"
            >
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path
                  d="M6 6l12 12M18 6L6 18"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                />
              </svg>
            </button>
          </header>

          <div class="lightbox__stage">
            <button
              v-if="hasMultiple"
              type="button"
              class="lightbox__nav lightbox__nav--prev"
              aria-label="Capture précédente"
              @click="go(-1)"
            >
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path
                  d="M15 5l-7 7 7 7"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </button>

            <img
              :key="current.src"
              :src="current.src"
              :alt="current.alt || `Capture d'écran d'un message reçu — ${current.author || current.role || 'témoignage'}`"
              class="lightbox__image"
            />

            <button
              v-if="hasMultiple"
              type="button"
              class="lightbox__nav lightbox__nav--next"
              aria-label="Capture suivante"
              @click="go(1)"
            >
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path
                  d="M9 5l7 7-7 7"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </button>
          </div>

          <footer class="lightbox__foot">
            <p class="lightbox__note">
              Capture reproduite avec l'accord de la famille. Numéros et noms complets masqués.
            </p>
            <p v-if="hasMultiple" class="lightbox__counter">{{ index + 1 }} / {{ total }}</p>
          </footer>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped lang="scss">
.lightbox {
  position: fixed;
  inset: 0;
  z-index: 12050;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px 16px;
  background: rgba(8, 12, 24, 0.82);
  backdrop-filter: blur(4px);
}

.lightbox__panel {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 460px;
  max-height: 100%;
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.4);
}

.lightbox__head {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 13px 16px;
  border-bottom: 1px solid #e2e9fb;
}

.lightbox__identity {
  min-width: 0;
  flex: 1;
}

.lightbox__title {
  margin: 0;
  font-size: 0.98rem;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.25;
}

.lightbox__subtitle {
  margin: 2px 0 0;
  font-size: 0.8rem;
  color: #64748b;
  line-height: 1.3;
}

.lightbox__close {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e2e8f0;
  border-radius: 50%;
  background: #ffffff;
  color: #334155;
  cursor: pointer;
  transition: background 0.2s ease;
}

.lightbox__close:hover {
  background: #f1f5f9;
}

.lightbox__close:focus-visible,
.lightbox__nav:focus-visible {
  outline: 2px solid #2a38b7;
  outline-offset: 2px;
}

.lightbox__close svg {
  width: 18px;
  height: 18px;
}

.lightbox__stage {
  position: relative;
  flex: 1;
  min-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 14px;
  background: #f1f5f9;
}

.lightbox__image {
  display: block;
  max-width: 100%;
  max-height: 62vh;
  width: auto;
  height: auto;
  object-fit: contain;
  border-radius: 10px;
  background: #ffffff;
  box-shadow: 0 2px 12px rgba(15, 23, 42, 0.12);
}

.lightbox__nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 38px;
  height: 38px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.94);
  color: #0f172a;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.18);
  transition: background 0.2s ease;
}

.lightbox__nav:hover {
  background: #ffffff;
}

.lightbox__nav svg {
  width: 20px;
  height: 20px;
}

.lightbox__nav--prev {
  left: 10px;
}

.lightbox__nav--next {
  right: 10px;
}

.lightbox__foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 11px 16px;
  border-top: 1px solid #eef2f7;
}

.lightbox__note {
  margin: 0;
  font-size: 0.74rem;
  line-height: 1.4;
  color: #64748b;
}

.lightbox__counter {
  margin: 0;
  flex-shrink: 0;
  font-size: 0.78rem;
  font-weight: 700;
  color: #334155;
}

.lightbox-fade-enter-active,
.lightbox-fade-leave-active {
  transition: opacity 0.2s ease;
}

.lightbox-fade-enter-from,
.lightbox-fade-leave-to {
  opacity: 0;
}

@media (max-width: 600px) {
  .lightbox {
    padding: 12px;
  }

  .lightbox__image {
    max-height: 58vh;
  }
}

@media (prefers-reduced-motion: reduce) {
  .lightbox-fade-enter-active,
  .lightbox-fade-leave-active {
    transition: none;
  }
}
</style>
