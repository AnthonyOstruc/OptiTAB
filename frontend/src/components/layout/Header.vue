<template>
  <header :class="['header', { 'header--no-shadow': isFreeResourcePage }]" ref="headerRef">
    <div class="header-desktop">
      <Logo data-track="nav" data-nav-name="home" data-nav-location="header_public" />
      <Navigation @open-login="handleLogin" />
    </div>
    <div class="header-mobile">
      <div class="header-mobile-top">
        <Logo data-track="nav" data-nav-name="home" data-nav-location="header_public" />
      </div>
      <div v-if="isFreeResourcePage" class="mobile-free-tabs">
        <FreeResourceTabs />
      </div>
      <div v-else-if="isCalculatorPage" class="mobile-calculator-tabs">
        <CalculatorTabs />
      </div>
      <!-- Cours Particuliers à gauche -->
      <router-link v-if="!isFreeResourcePage && !isCalculatorPage" to="/cours-particuliers" class="mobile-quick-link mobile-quick-link--left" data-track="nav" data-nav-name="tutoring" data-nav-location="header_public">
        <UserGroupIcon class="mobile-quick-icon" />
        <span>Cours Particuliers</span>
      </router-link>
      <!-- Nous contacter -->
      <router-link v-if="!isFreeResourcePage && !isCalculatorPage" to="/contact" class="mobile-quick-link mobile-quick-link--contact" data-track="nav" data-nav-name="contact" data-nav-location="header_public">
        <EnvelopeIcon class="mobile-quick-icon" />
        <span>Nous contacter</span>
      </router-link>
      <!-- Spacer pour pousser Connexion à droite -->
      <div v-if="!isFreeResourcePage && !isCalculatorPage" class="mobile-spacer"></div>
      <!-- Connexion à droite -->
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
    </div>
  </header>
</template>

<script>
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import Logo from '@/components/common/Logo.vue'
import Navigation from '@/components/layout/Navigation.vue'
import MobileMenu from '@/components/layout/MobileMenu.vue'
import FreeResourceTabs from '@/components/free-content/FreeResourceTabs.vue'
import CalculatorTabs from '@/components/calculator/CalculatorTabs.vue'
import { UserGroupIcon, UserIcon, EnvelopeIcon } from '@heroicons/vue/24/outline'
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'

export default {
  name: 'Header',
  components: {
    Logo,
    Navigation,
    MobileMenu,
    FreeResourceTabs,
    CalculatorTabs,
    UserGroupIcon,
    UserIcon,
    EnvelopeIcon
  },
  setup() {
    const { openModal } = useModalManager()
    const headerRef = ref(null)
    const route = useRoute()

    const handleLogin = () => {
      openModal(MODAL_IDS.LOGIN)
    }

    const isFreeResourcePage = computed(() => {
      const path = route.path
      // Exclure la page d'accueil des ressources gratuites, ne montrer les tabs que sur les sous-pages
      return path?.startsWith('/ressources-gratuites/') && path !== '/ressources-gratuites'
    })
    const isCalculatorPage = computed(() => route.path === '/calculator')

    // Empêcher le zoom et les gestes indésirables sur le header
    const handleTouchStart = (e) => {
      // Si c'est un multi-touch (pinch zoom), empêcher
      if (e.touches.length > 1) {
        e.preventDefault()
        e.stopPropagation()
      }
    }

    const handleTouchMove = (e) => {
      // Empêcher le pinch zoom sur le header
      if (e.touches.length > 1) {
        e.preventDefault()
        e.stopPropagation()
      }
    }

    // Empêcher le zoom lors du double-tap sur le header
    let lastTap = 0
    const handleDoubleTap = (e) => {
      const currentTime = Date.now()
      const tapLength = currentTime - lastTap
      if (tapLength < 300 && tapLength > 0) {
        e.preventDefault()
        return false
      }
      lastTap = currentTime
    }

    onMounted(() => {
      const header = headerRef.value
      if (header) {
        // Ajouter les listeners avec passive: false pour permettre preventDefault()
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
      headerRef,
      isFreeResourcePage,
      isCalculatorPage
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
  /* Empêcher le zoom et les gestes indésirables */
  touch-action: pan-y;
  -webkit-tap-highlight-color: transparent;
  -webkit-user-select: none;
  user-select: none;
  /* Forcer le header à rester fixe (GPU layer) */
  will-change: transform;
  transform: translateZ(0);
  -webkit-transform: translateZ(0);
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
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

.header-desktop {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  min-height: $header-height;
  padding: 0 20px;
  box-sizing: border-box;
}

// Responsive breakpoints
@media (max-width: #{$max-width-media}) {
  .header {
    /* Bloquer le scroll sur le header lui-même - empêche tout mouvement */
    touch-action: none;
    overscroll-behavior: contain;
  }

  .header-desktop {
    display: none;
  }
  .header-mobile {
    display: flex;
    /* Permettre les clics sur les éléments du header */
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

// Écrans < 530px - masquer "Nous contacter"
@media (max-width: 530px) {
  .mobile-quick-link--contact {
    display: none !important;
  }
}

// Très petits écrans (< 400px)
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

/* iOS safe area at top */
@supports (padding: env(safe-area-inset-top)) {
  .header {
    padding-top: env(safe-area-inset-top);
  }
}
</style> 
