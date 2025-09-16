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
        <!-- Bouton de connexion si non authentifié -->
        <button 
          v-if="!isAuthenticated" 
          class="login-button" 
          @click="handleLoginClick"
        >
          <UserIcon class="login-icon" />
          <span>Connexion</span>
        </button>
        
        <!-- Informations utilisateur si authentifié -->
        <div v-else class="user-info">
          <div class="user-details">
            <UserIcon class="user-avatar" />
            <div class="user-text">
              <div class="user-name">{{ userStore.user?.first_name || 'Utilisateur' }}</div>
              <div class="user-email">{{ userStore.user?.email }}</div>
            </div>
          </div>
          <button class="logout-button" @click="handleLogout">
            Déconnexion
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { menuItems } from '@/config/menuItems'
import { UserIcon } from '@heroicons/vue/24/outline'
import Logo from '@/components/common/Logo.vue'
import HamburgerIcon from '@/components/common/HamburgerIcon.vue'
import CloseIcon from '@/components/common/CloseIcon.vue'
import { useUserStore } from '@/stores/user'

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
    const userStore = useUserStore()

    // Computed
    const navigationItems = menuItems.filter(item =>
      ['calculator', 'cours-particuliers', 'about', 'contact'].includes(item.key)
    )
    const isAuthenticated = computed(() => userStore.isAuthenticated)

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

    const handleLogout = async () => {
      try {
        await userStore.logout()
        closeMenu()
      } catch (error) {
        console.error('Erreur lors de la déconnexion:', error)
      }
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
      userStore,
      
      // Computed
      navigationItems,
      isAuthenticated,
      
      // Methods
      toggleMenu,
      closeMenu,
      handleNavigationClick,
      handleLoginClick,
      handleLogout
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
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  
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
  height: 100dvh; // utiliser la hauteur dynamique pour iOS Safari
  background: $white;
  z-index: 12003;
  transition: right 0.3s ease;
  display: flex;
  flex-direction: column;
  box-shadow: -5px 0 15px rgba(0, 0, 0, 0.1);
  overflow: hidden; // Prévenir le débordement du contenu

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
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
  cursor: pointer;

  &:hover {
    background: $background-light;
  }
}

// Navigation List
.navigation-list {
  flex: 1;
  padding: 20px 0;
  overflow-y: auto;
  min-height: 0; // Important pour le flex scrolling
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
  cursor: pointer;

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
  flex-shrink: 0; // Empêcher le footer de se comprimer
  background: $white; // S'assurer que le background est visible
  // Laisser de l'espace pour la barre système (safe area) et les bulles flottantes
  padding-bottom: calc(20px + 12px);
  padding-bottom: calc(20px + constant(safe-area-inset-bottom) + 12px);
  padding-bottom: calc(20px + env(safe-area-inset-bottom) + 12px);
}

.login-button {
  @extend .btn;
  @extend .btn-primary;
  width: 100%;
  justify-content: center;
  padding: 14px 20px;
  font-size: 16px;
  font-weight: 600;
  min-height: 48px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  // Séparer visuellement du bord inférieur
  margin-bottom: max(4px, env(safe-area-inset-bottom));
  
  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  }
}

.login-icon {
  width: 20px;
  height: 20px;
}

// User Info Section
.user-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
  // Préserver un espace avec la zone sûre iOS
  padding-bottom: env(safe-area-inset-bottom);
}

.user-details {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  color: $primary-color;
  flex-shrink: 0;
}

.user-text {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-weight: 600;
  font-size: 14px;
  color: $text-color;
  margin-bottom: 2px;
}

.user-email {
  font-size: 12px;
  color: $text-light;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.logout-button {
  @extend .btn;
  width: 100%;
  justify-content: center;
  padding: 10px 16px;
  font-size: 14px;
  background: transparent;
  color: #ef4444;
  border: 1px solid #fecaca;
  border-radius: 6px;
  cursor: pointer;
  
  &:hover {
    background: #fef2f2;
    border-color: #fca5a5;
  }
}

// Responsive Design
@media (max-width: 480px) {
  .mobile-panel {
    width: 100%;
  }

  .user-details {
    padding: 10px;
  }

  .user-name, .user-email {
    font-size: 13px;
  }

  .panel-footer {
    padding: 16px;
    // Ajustement mobile: remonter encore un peu le bouton
    padding-bottom: calc(16px + 12px);
    padding-bottom: calc(16px + constant(safe-area-inset-bottom) + 12px);
    padding-bottom: calc(16px + env(safe-area-inset-bottom) + 12px);
  }
}
</style> 