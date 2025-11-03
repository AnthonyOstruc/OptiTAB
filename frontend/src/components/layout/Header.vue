<template>
  <header class="header" @touchstart="handleTouchStart" @touchmove="handleTouchMove">
    <div class="header-desktop">
      <Logo />
      <Navigation @open-login="handleLogin" />
    </div>
    <div class="header-mobile">
      <Logo />
      <MobileMenu @open-login="handleLogin" />
    </div>
  </header>
</template>

<script>
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import Logo from '@/components/common/Logo.vue'
import Navigation from '@/components/layout/Navigation.vue'
import MobileMenu from '@/components/layout/MobileMenu.vue'
import { onMounted, onUnmounted } from 'vue'

export default {
  name: 'Header',
  components: {
    Logo,
    Navigation,
    MobileMenu
  },
  setup() {
    const { openModal } = useModalManager()

    const handleLogin = () => {
      openModal(MODAL_IDS.LOGIN)
    }

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
      const header = document.querySelector('.header')
      if (header) {
        header.addEventListener('touchend', handleDoubleTap, { passive: false })
      }
    })

    onUnmounted(() => {
      const header = document.querySelector('.header')
      if (header) {
        header.removeEventListener('touchend', handleDoubleTap)
      }
    })

    return {
      handleLogin,
      handleTouchStart,
      handleTouchMove
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

.header-mobile {
  display: none;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  min-height: $header-height;
  padding: 0 20px;
  box-sizing: border-box;
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
</style> 
