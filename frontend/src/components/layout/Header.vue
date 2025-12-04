<template>
  <header :class="['header', { 'header--no-shadow': isFreeResourcePage }]" ref="headerRef">
    <div class="header-desktop">
      <Logo />
      <Navigation @open-login="handleLogin" />
    </div>
    <div class="header-mobile">
      <div class="header-mobile-top">
        <Logo />
      </div>
      <div v-if="isFreeResourcePage" class="mobile-free-tabs">
        <FreeResourceTabs />
      </div>
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
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'

export default {
  name: 'Header',
  components: {
    Logo,
    Navigation,
    MobileMenu,
    FreeResourceTabs
  },
  setup() {
    const { openModal } = useModalManager()
    const headerRef = ref(null)
    const route = useRoute()

    const handleLogin = () => {
      openModal(MODAL_IDS.LOGIN)
    }

    const isFreeResourcePage = computed(() => route.path?.startsWith('/ressources-gratuites'))

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
      isFreeResourcePage
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
  /* Empêcher le zoom et les gestes indésirables sur le header */
  touch-action: pan-y;
  -webkit-tap-highlight-color: transparent;
  /* Empêcher le zoom automatique sur iOS */
  -webkit-user-select: none;
  user-select: none;
  /* S'assurer que le header reste visible */
  transform: translateZ(0);
  -webkit-transform: translateZ(0);
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
  padding: 0 20px;
  box-sizing: border-box;
  gap: 12px;
}

.header-mobile-top {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.mobile-free-tabs {
  display: none;
  flex: 1;
  min-width: 0;
  pointer-events: auto;
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
  .header-desktop {
    display: none;
  }
  .header-mobile {
    display: flex;
  }

  .mobile-free-tabs {
    display: flex;
    justify-content: center;
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
        .header { padding-top: env(safe-area-inset-top); }
      }

      /* Ensure header never scrolls, and allow page scroll to start from it */
      .header { pointer-events: none; }
      .header-mobile, .header-desktop { pointer-events: auto; touch-action: pan-y; }
      .mobile-free-tabs { pointer-events: auto; }
</style> 
