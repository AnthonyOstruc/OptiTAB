<template>
  <header class="header">
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

    return {
      handleLogin
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
</style> 