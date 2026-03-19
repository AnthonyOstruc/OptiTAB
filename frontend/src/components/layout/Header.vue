<template>
  <header :class="['header', { 'header--no-shadow': isFreeResourcePage, 'header--landing': isLandingVariant }]" ref="headerRef">
    <div class="header-desktop">
      <Logo data-track="nav" data-nav-name="home" data-nav-location="header_public" />
      <Navigation :variant="variant" @open-login="handleLogin" @open-contact="openLandingContactModal" />
    </div>

    <div class="header-mobile">
      <template v-if="isLandingVariant">
        <div class="header-mobile-top header-mobile-top--landing">
          <Logo data-track="nav" data-nav-name="home" data-nav-location="header_public" />
          <div class="landing-mobile-actions">
            <button
              type="button"
              class="mobile-quick-link mobile-quick-link--contact"
              data-track="nav"
              data-nav-name="contact"
              data-nav-location="header_public"
              @click="openLandingContactModal"
            >
              <EnvelopeIcon class="mobile-quick-icon" />
              <span>Nous contacter</span>
            </button>
            <button
              type="button"
              class="mobile-quick-link mobile-quick-link--login"
              :data-cta-name="landingPrimaryCtaName"
              data-cta-location="header_public"
              @click="handleLogin"
            >
              <span v-if="isPlateformeMathsLanding" class="mobile-quick-emoji" aria-hidden="true">✦</span>
              <UserIcon v-else class="mobile-quick-icon" />
              <span>{{ landingPrimaryCtaLabel }}</span>
            </button>
          </div>
        </div>
      </template>

      <template v-else>
        <div class="header-mobile-top">
          <Logo data-track="nav" data-nav-name="home" data-nav-location="header_public" />
        </div>
        <div v-if="isFreeResourcePage" class="mobile-free-tabs">
          <FreeResourceTabs />
        </div>
        <div v-else-if="isCalculatorPage" class="mobile-calculator-tabs">
          <CalculatorTabs />
        </div>

        <router-link
          v-if="!isFreeResourcePage && !isCalculatorPage"
          to="/cours-particuliers"
          class="mobile-quick-link mobile-quick-link--left"
          data-track="nav"
          data-nav-name="tutoring"
          data-nav-location="header_public"
        >
          <UserGroupIcon class="mobile-quick-icon" />
          <span>Cours Particuliers</span>
        </router-link>

        <router-link
          v-if="!isFreeResourcePage && !isCalculatorPage"
          to="/contact"
          class="mobile-quick-link mobile-quick-link--contact"
          data-track="nav"
          data-nav-name="contact"
          data-nav-location="header_public"
        >
          <EnvelopeIcon class="mobile-quick-icon" />
          <span>Nous contacter</span>
        </router-link>

        <div v-if="!isFreeResourcePage && !isCalculatorPage" class="mobile-spacer"></div>

        <button
          v-if="!isFreeResourcePage && !isCalculatorPage"
          class="mobile-quick-link mobile-quick-link--login"
          data-cta-name="login"
          data-cta-location="header_public"
          @click="handleLogin"
        >
          <UserIcon class="mobile-quick-icon" />
          <span>Connexion</span>
        </button>

        <MobileMenu @open-login="handleLogin" />
      </template>
    </div>
  </header>
  <ContactModal
    :isOpen="isContactModalOpen"
    :initialSubject="contactModalSubject"
    @close="closeContactModal"
    @success="handleContactSuccess"
  />
</template>

<script>
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import Logo from '@/components/common/Logo.vue'
import Navigation from '@/components/layout/Navigation.vue'
import MobileMenu from '@/components/layout/MobileMenu.vue'
import FreeResourceTabs from '@/components/free-content/FreeResourceTabs.vue'
import CalculatorTabs from '@/components/calculator/CalculatorTabs.vue'
import ContactModal from '@/components/common/ContactModal.vue'
import { UserGroupIcon, UserIcon, EnvelopeIcon } from '@heroicons/vue/24/outline'
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'Header',
  components: {
    Logo,
    Navigation,
    MobileMenu,
    FreeResourceTabs,
    CalculatorTabs,
    ContactModal,
    UserGroupIcon,
    UserIcon,
    EnvelopeIcon
  },
  props: {
    variant: {
      type: String,
      default: 'default'
    }
  },
  setup(props) {
    const { openModal } = useModalManager()
    const headerRef = ref(null)
    const route = useRoute()
    const router = useRouter()
    const isContactModalOpen = ref(false)
    const contactModalSubject = ref('')

    const isLandingVariant = computed(() => props.variant === 'landing')
    const isPlateformeMathsLanding = computed(
      () =>
        isLandingVariant.value &&
        ['/plateforme-maths', '/bases-methode'].includes(route.path)
    )
    const landingPrimaryCtaLabel = computed(() =>
      isPlateformeMathsLanding.value ? 'Choisir un abonnement' : 'Créer un compte'
    )
    const landingPrimaryCtaName = computed(() =>
      isPlateformeMathsLanding.value ? 'pricing' : 'signup'
    )

    const scrollToOffer = async () => {
      if (typeof document !== 'undefined') {
        const offer = document.getElementById('offre')
        if (offer) {
          offer.scrollIntoView({ behavior: 'smooth', block: 'start' })
          return
        }
      }

      if (!['/plateforme-maths', '/bases-methode'].includes(route.path)) {
        await router.push({ path: '/plateforme-maths', hash: '#offre' })
      } else if (typeof window !== 'undefined') {
        window.location.hash = 'offre'
      }
    }

    const handleLogin = async () => {
      if (isPlateformeMathsLanding.value) {
        await scrollToOffer()
        return
      }
      openModal(isLandingVariant.value ? MODAL_IDS.REGISTER : MODAL_IDS.LOGIN)
    }

    const openLandingContactModal = () => {
      if (!isLandingVariant.value) return
      contactModalSubject.value = "Demande d'information"
      isContactModalOpen.value = true
    }

    const closeContactModal = () => {
      isContactModalOpen.value = false
      contactModalSubject.value = ''
    }

    const handleContactSuccess = () => {
      // no-op: le ContactModal gère déjà son message de confirmation
    }

    const isFreeResourcePage = computed(() => {
      const path = route.path
      return path?.startsWith('/ressources-gratuites/') && path !== '/ressources-gratuites'
    })

    const isCalculatorPage = computed(() => route.path === '/calculator')

    const handleTouchStart = (e) => {
      if (e.touches.length > 1) {
        e.preventDefault()
        e.stopPropagation()
      }
    }

    const handleTouchMove = (e) => {
      if (e.touches.length > 1) {
        e.preventDefault()
        e.stopPropagation()
      }
    }

    let lastTap = 0
    const handleDoubleTap = (e) => {
      const currentTime = Date.now()
      const tapLength = currentTime - lastTap
      if (tapLength < 300 && tapLength > 0) {
        e.preventDefault()
        return false
      }
      lastTap = currentTime
      return true
    }

    onMounted(() => {
      const header = headerRef.value
      if (header) {
        header.addEventListener('touchstart', handleTouchStart, { passive: false })
        header.addEventListener('touchmove', handleTouchMove, { passive: false })
        header.addEventListener('touchend', handleDoubleTap, { passive: false })
      }
    })

    onUnmounted(() => {
      const header = headerRef.value
      if (header) {
        header.removeEventListener('touchstart', handleTouchStart)
        header.removeEventListener('touchmove', handleTouchMove)
        header.removeEventListener('touchend', handleDoubleTap)
      }
    })

    return {
      handleLogin,
      openLandingContactModal,
      closeContactModal,
      handleContactSuccess,
      isContactModalOpen,
      contactModalSubject,
      headerRef,
      isFreeResourcePage,
      isCalculatorPage,
      isLandingVariant,
      isPlateformeMathsLanding,
      landingPrimaryCtaLabel,
      landingPrimaryCtaName
    }
  }
}
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;

.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  margin: 0;
  padding: 0;
  z-index: 12000;
  background: #fff;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
  box-sizing: border-box;
  display: flex;
  align-items: center;
  min-height: $header-height;
  touch-action: pan-y;
  -webkit-tap-highlight-color: transparent;
  -webkit-user-select: none;
  user-select: none;
  will-change: transform;
  transform: translateZ(0);
  -webkit-transform: translateZ(0);
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
}

.header--landing {
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.1);
}

.header--no-shadow {
  box-shadow: none;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.header-mobile {
  display: none;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  height: $header-height;
  padding: 0 12px;
  box-sizing: border-box;
  gap: 6px;
}

.header-mobile-top {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  min-width: 0;
}

.header-mobile-top--landing {
  width: 100%;
  justify-content: space-between;
}

.landing-mobile-actions {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-left: auto;
}

.mobile-free-tabs {
  display: none;
  flex: 1;
  min-width: 0;
  pointer-events: auto;
}

.mobile-calculator-tabs {
  display: none;
  flex: 1;
  min-width: 0;
  pointer-events: auto;
}

.mobile-spacer {
  display: none;
  flex: 1;
}

.mobile-quick-link {
  display: none;
  align-items: center;
  gap: 5px;
  padding: 6px 10px;
  font-size: 12px;
  font-weight: 500;
  text-decoration: none;
  color: #10257f;
  border-radius: 6px;
  transition: all 0.2s ease;
  background: transparent;
  border: none;
  cursor: pointer;
  white-space: nowrap;
  flex-shrink: 0;

  &:hover {
    background: rgba(102, 126, 234, 0.1);
    color: #667eea;
  }

  &--left {
    margin-left: 4px;
    color: #10257f;
    border: 1px solid rgba(102, 126, 234, 0.3);

    &:hover {
      background: rgba(102, 126, 234, 0.1);
      color: #667eea;
      border-color: #667eea;
    }
  }

  &--contact {
    color: #10257f;
    border: 1px solid rgba(102, 126, 234, 0.3);

    &:hover {
      background: rgba(102, 126, 234, 0.1);
      color: #667eea;
      border-color: #667eea;
    }
  }

  &--login {
    background: #667eea;
    color: white;

    &:hover {
      background: #5a67d8;
    }
  }
}

.mobile-quick-icon {
  width: 16px;
  height: 16px;
}

.mobile-quick-emoji {
  font-size: 15px;
  line-height: 1;
  color: currentColor;
}

.header-desktop {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  min-height: $header-height;
  padding: 0 20px;
  box-sizing: border-box;
}

@media (max-width: #{$max-width-media}) {
  .header {
    touch-action: none;
    overscroll-behavior: contain;
  }

  .header-desktop {
    display: none;
  }

  .header-mobile {
    display: flex;
    touch-action: manipulation;
  }

  .mobile-free-tabs {
    display: flex;
    justify-content: center;
  }

  .mobile-calculator-tabs {
    display: flex;
    justify-content: center;
  }

  .mobile-quick-link {
    display: flex;
  }

  .mobile-spacer {
    display: block;
  }
}

@media (max-width: 530px) {
  .mobile-quick-link--contact {
    display: none !important;
  }

  .header--landing .mobile-quick-link--contact {
    display: flex !important;
  }
}

@media (max-width: 420px) {
  .header--landing .mobile-quick-link {
    min-width: 38px;
    padding: 6px 8px;
    justify-content: center;
  }

  .header--landing .mobile-quick-link span {
    display: none;
  }
}

@media (max-width: 400px) {
  .header-mobile {
    padding: 0 8px;
    gap: 4px;
  }

  .mobile-quick-link {
    padding: 5px 8px;
    font-size: 11px;
    gap: 4px;

    &--left {
      margin-left: 2px;
    }
  }

  .mobile-quick-icon {
    width: 14px;
    height: 14px;
  }
}

@media (min-width: #{$max-width-media + 1px}) {
  .header-mobile {
    display: none;
  }

  .header-desktop {
    display: flex;
  }
}

@supports (padding: env(safe-area-inset-top)) {
  .header {
    padding-top: env(safe-area-inset-top);
  }
}
</style>
