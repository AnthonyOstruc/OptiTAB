<template>
  <div class="mobile-menu">
    <!-- Hamburger Button -->
    <button 
      class="hamburger-button"
      @click="toggleMenu"
      aria-label="Toggle mobile menu"
    >
      <HamburgerIcon :is-active="isOpen" />
    </button>

    <!-- Mobile Menu Overlay -->
    <div 
      class="mobile-overlay"
      :class="{ 'is-open': isOpen }"
      @click="closeMenu"
    />

    <!-- Mobile Menu Panel -->
    <div class="mobile-panel" :class="{ 'is-open': isOpen }">
      <!-- Panel Header -->
      <div class="panel-header">
        <Logo />
        <button class="close-button" @click="closeMenu" aria-label="Close menu">
          <CloseIcon />
        </button>
      </div>

      <!-- Navigation List -->
      <nav class="navigation-list">
        <component
          v-for="item in navigationItems"
          :is="item.external ? 'a' : 'router-link'"
          :key="item.key"
          :href="item.external ? item.href : undefined"
          :to="!item.external ? item.href : undefined"
          :target="item.external ? '_blank' : undefined"
          :rel="item.external ? 'noopener noreferrer' : undefined"
          class="navigation-item"
          @click="handleNavigationClick(item)"
        >
          <component :is="item.icon" class="item-icon" />
          <span class="item-text">{{ item.text }}</span>
        </component>
      </nav>

      <!-- Panel Footer -->
      <div class="panel-footer">
        <button class="login-button" @click="handleLoginClick">
          <UserIcon class="login-icon" />
          <span>Connexion</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { menuItems } from '@/config/menuItems'
import { UserIcon } from '@heroicons/vue/24/outline'
import Logo from '@/components/common/Logo.vue'
import HamburgerIcon from '@/components/common/HamburgerIcon.vue'
import CloseIcon from '@/components/common/CloseIcon.vue'

export default {
  name: 'MobileMenu',
  components: {
    Logo,
    UserIcon,
    HamburgerIcon,
    CloseIcon
  },
  emits: ['open-login'],
  setup(props, { emit }) {
    // State
    const isOpen = ref(false)

    // Computed
    const navigationItems = menuItems.filter(item => item.key !== 'login')

    // Methods
    const toggleMenu = () => {
      isOpen.value = !isOpen.value
      updateBodyScroll()
    }

    const closeMenu = () => {
      isOpen.value = false
      updateBodyScroll()
    }

    const updateBodyScroll = () => {
      document.body.style.overflow = isOpen.value ? 'hidden' : 'auto'
    }

    const handleNavigationClick = (item) => {
      if (item.emit) {
        emit(item.emit)
      }
      closeMenu()
    }

    const handleLoginClick = () => {
      emit('open-login')
      closeMenu()
    }

    // ESC key handler
    const handleKeydown = (event) => {
      if (event.key === 'Escape' && isOpen.value) {
        closeMenu()
      }
    }

    // Lifecycle hooks
    onMounted(() => {
      document.addEventListener('keydown', handleKeydown)
    })

    onUnmounted(() => {
      document.removeEventListener('keydown', handleKeydown)
    })

    return {
      // State
      isOpen,
      
      // Computed
      navigationItems,
      
      // Methods
      toggleMenu,
      closeMenu,
      handleNavigationClick,
      handleLoginClick
    }
  }
}
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;

.mobile-menu {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

// Hamburger Button
.hamburger-button {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  
  &:hover {
    background: $background-light;
  }
}

// Mobile Menu Overlay
.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 12002;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;

  &.is-open {
    opacity: 1;
    visibility: visible;
  }
}

// Mobile Menu Panel
.mobile-panel {
  position: fixed;
  top: 0;
  right: -100%;
  width: 300px;
  height: 100vh;
  background: $white;
  z-index: 12003;
  transition: right 0.3s ease;
  display: flex;
  flex-direction: column;
  box-shadow: -5px 0 15px rgba(0, 0, 0, 0.1);

  &.is-open {
    right: 0;
  }
}

// Panel Header
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  border-bottom: 1px solid #e5e5e5;
}

.close-button {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s ease;

  &:hover {
    background: $background-light;
  }
}

// Navigation List
.navigation-list {
  flex: 1;
  padding: 20px 0;
  overflow-y: auto;
}

.navigation-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  text-decoration: none;
  color: $text-color;
  font-weight: 500;
  transition: all 0.2s ease;
  border-bottom: 1px solid #f5f5f5;

  &:hover {
    background: $background-light;
    color: $primary-color;
  }

  &:last-child {
    border-bottom: none;
  }
}

.item-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.item-text {
  font-size: 16px;
}

// Panel Footer
.panel-footer {
  padding: 20px;
  border-top: 1px solid #e5e5e5;
}

.login-button {
  @extend .btn;
  @extend .btn-primary;
  width: 100%;
  justify-content: center;
  padding: 12px 20px;
  font-size: 16px;
}

.login-icon {
  width: 20px;
  height: 20px;
}

// Responsive Design
@media (max-width: 480px) {
  .mobile-panel {
    width: 100%;
  }
}
</style> 