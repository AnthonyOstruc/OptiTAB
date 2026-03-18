<template>
  <Modal
    :is-open="isOpen"
    title=""
    :show-header="false"
    size="large"
    @close="handleClose"
  >
    <div class="sub-prompt-zoom-clip">
      <div class="sub-prompt-zoom-outer" :style="zoomStyle">
        <div ref="contentRef" class="sub-prompt-content">
          <!-- Header -->
          <div class="sub-prompt-header">
            <button class="sub-prompt-close-btn" @click="handleClose" aria-label="Fermer">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
            <div class="sub-prompt-icon">
              <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                <path d="M7 11V7a5 5 0 0 1 10 0v4" />
              </svg>
            </div>
            <h2 class="sub-prompt-title">Débloquez tout votre potentiel !</h2>
            <p class="sub-prompt-subtitle">
              Abonnez-vous pour accéder à tous les cours, exercices et quiz.
            </p>
          </div>

          <!-- PricingCards identique à Billing -->
          <div class="sub-prompt-cards">
            <PricingCards
              :submitting="submitting"
              cta-location="dashboard-modal"
              @select="handlePlanSelect"
            />
          </div>
        </div>
      </div>
    </div>
  </Modal>
</template>

<script setup>
import { ref, onBeforeUnmount, watch, nextTick } from 'vue'
import Modal from '@/components/common/Modal.vue'
import PricingCards from '@/components/shared/PricingCards.vue'
import { createCheckoutSession } from '@/api/subscriptions'
import { useUserStore } from '@/stores/user'
import { useZoom } from '@/composables/useZoom'

const props = defineProps({
  isOpen: { type: Boolean, default: false }
})

const emit = defineEmits(['close'])

const userStore = useUserStore()
const submitting = ref(false)

const handlePlanSelect = async (card) => {
  if (!card?.priceId || submitting.value) return
  const niveauId = userStore.niveau_pays?.id
  if (!niveauId) {
    alert('Sélectionnez votre niveau dans votre profil avant de vous abonner.')
    return
  }
  submitting.value = true
  try {
    const { data } = await createCheckoutSession(card.priceId, {
      niveau_pays_id: niveauId
    })
    if (data?.checkout_url) {
      window.location.assign(data.checkout_url)
    }
  } catch {
    alert('Erreur lors du processus de paiement. Veuillez réessayer.')
  } finally {
    submitting.value = false
  }
}

const handleClose = () => {
  emit('close')
}

// --- Dezoom mobile ---
const contentRef = ref(null)

function computeSubPromptZoom(width) {
  if (width >= 768) return 1
  if (width >= 520) return 0.92
  if (width >= 420) return 0.88
  if (width >= 360) return 0.84
  return 0.8
}

const {
  detectMobileAndZoomSupport,
  createZoomStyle,
  updateViewportWidth,
  measureContentHeight,
  setupViewportListener,
  cleanupViewportListener
} = useZoom({ computeAutoZoom: computeSubPromptZoom })

const zoomStyle = createZoomStyle({
  cssVar: '--sub-prompt-zoom',
  heightVar: '--sub-prompt-content-height',
  mobileZoomAdjustment: (z) => z
})

let zoomResizeObserver = null
let zoomSession = 0

const measureHeight = () => measureContentHeight(contentRef)

const onViewportChange = async () => {
  updateViewportWidth()
  await nextTick()
  measureHeight()
}

const startZoomTracking = async (sessionId) => {
  detectMobileAndZoomSupport()
  setupViewportListener()
  await nextTick()
  if (sessionId !== zoomSession || !props.isOpen) return
  measureHeight()

  if (typeof window !== 'undefined') {
    window.addEventListener('resize', onViewportChange, { passive: true })
    window.addEventListener('orientationchange', () => setTimeout(onViewportChange, 200), { passive: true })
    setTimeout(measureHeight, 250)
    if (window.ResizeObserver && contentRef.value) {
      zoomResizeObserver = new ResizeObserver(measureHeight)
      zoomResizeObserver.observe(contentRef.value)
    }
  }
}

const stopZoomTracking = () => {
  cleanupViewportListener()
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', onViewportChange)
  }
  zoomResizeObserver?.disconnect?.()
  zoomResizeObserver = null
}

watch(() => props.isOpen, async (open) => {
  zoomSession += 1
  const sid = zoomSession
  if (open) {
    await startZoomTracking(sid)
  } else {
    stopZoomTracking()
  }
}, { immediate: true })

onBeforeUnmount(() => {
  stopZoomTracking()
})
</script>

<style scoped>
.sub-prompt-zoom-clip {
  overflow: hidden;
}

.sub-prompt-zoom-outer {
  transition: transform 0.15s ease;
}

.sub-prompt-content {
  padding: 1.25rem 1.25rem 1rem;
  text-align: center;
}

/* Header */
.sub-prompt-header {
  margin-bottom: 0.75rem;
  position: relative;
}

.sub-prompt-close-btn {
  position: absolute;
  top: -0.5rem;
  right: -0.25rem;
  background: none;
  border: none;
  cursor: pointer;
  color: #9ca3af;
  padding: 4px;
  border-radius: 6px;
  transition: color 0.2s, background 0.2s;
}

.sub-prompt-close-btn:hover {
  color: #374151;
  background: #f3f4f6;
}

.sub-prompt-icon {
  margin-bottom: 0.5rem;
}

.sub-prompt-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: #1e3a8a;
  margin: 0 0 0.25rem;
}

.sub-prompt-subtitle {
  color: #6b7280;
  font-size: 0.9rem;
  line-height: 1.4;
  max-width: 500px;
  margin: 0 auto;
}

/* PricingCards wrapper — compact overrides */
.sub-prompt-cards {
  text-align: left;
}

.sub-prompt-cards :deep(.pricing-tabs) {
  margin-bottom: 1rem;
  padding: 0.25rem;
}

.sub-prompt-cards :deep(.pricing-tab) {
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
}

.sub-prompt-cards :deep(.pricing-grid) {
  align-items: stretch;
  min-height: 480px;
}

.sub-prompt-cards :deep(.pricing-card) {
  padding: 1.25rem 1rem;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.sub-prompt-cards :deep(.card-features) {
  margin: 0 0 0.75rem;
  flex-grow: 1;
}

.sub-prompt-cards :deep(.card-badge-area) {
  min-height: 24px;
  margin-bottom: 0.5rem;
}

.sub-prompt-cards :deep(.card-header) {
  margin-bottom: 0.75rem;
}

.sub-prompt-cards :deep(.card-title) {
  font-size: 1.2rem;
}

.sub-prompt-cards :deep(.card-price) {
  margin-bottom: 0.75rem;
}

.sub-prompt-cards :deep(.price-amount) {
  font-size: 2.25rem;
}

.sub-prompt-cards :deep(.card-features li) {
  padding: 0.25rem 0;
  font-size: 0.85rem;
}

.sub-prompt-cards :deep(.card-reviews) {
  margin-bottom: 0.75rem;
}

.sub-prompt-cards :deep(.card-button) {
  padding: 0.75rem 1rem;
  font-size: 0.9rem;
}

.sub-prompt-cards :deep(.card-note) {
  margin-top: 0.5rem;
  font-size: 0.75rem;
}

/* Mobile responsive */
@media (max-width: 767px) {
  .sub-prompt-content {
    padding: 1rem 0.75rem 0.75rem;
  }

  .sub-prompt-title {
    font-size: 1.15rem;
  }

  .sub-prompt-subtitle {
    font-size: 0.85rem;
  }
}

@media (max-width: 420px) {
  .sub-prompt-content {
    padding: 0.75rem 0.5rem;
  }

  .sub-prompt-title {
    font-size: 1.05rem;
  }
}
</style>
