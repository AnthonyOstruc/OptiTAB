<template>
  <div class="user-menu-container" ref="menuContainer">
    <!-- Bouton utilisateur déclencheur du menu -->
    <button 
      class="user-menu-trigger" 
      @click="toggleMenu"
      :aria-expanded="isOpen"
      aria-label="Menu utilisateur"
    >
      <div class="user-info">
        <div 
          class="avatar-progress" 
          :style="{ '--progress': xpProgress + '%' }" 
          role="img" 
          :aria-label="`Progression de niveau: ${xpProgress}%`"
          title="Progression vers le prochain niveau"
        >
          <span class="user-avatar">{{ userInitials }}</span>
        </div>
        <div class="user-details">
          <span class="user-name">{{ userName }}</span>
          <span class="user-title">{{ userTitle }}</span>
          <div v-if="showXp" class="user-xp-bar">
            <div class="user-xp-fill" :style="{ width: xpProgress + '%' }"></div>
          </div>
        </div>
      </div>
      <!-- Suppression de la flèche du menu déroulant -->
    </button>

    <!-- Menu déroulant -->
    <Transition name="menu-dropdown">
      <div v-if="isOpen" class="user-menu-dropdown">
        <!-- En-tête du menu avec infos utilisateur -->
        <button 
          class="menu-header"
          @click="handleProfile"
        >
          <span class="menu-avatar">{{ userInitials }}</span>
          <div class="menu-user-info">
            <div class="menu-full-name">{{ userName }}</div>
            <div class="menu-email">{{ userEmail }}</div>
          </div>
        </button>



        <!-- Options du menu -->
        <div class="menu-options">
          <button 
            class="menu-option"
            @click="handleAccount"
          >
            <span class="option-icon"><Cog6ToothIcon class="user-menu-heroicon" /></span>
            <span class="option-label">Mon compte</span>
          </button>

          <button 
            class="menu-option"
            @click="handleSubscription"
          >
            <span class="option-icon"><CreditCardIcon class="user-menu-heroicon" /></span>
            <span class="option-label">Abonnement</span>
          </button>

          <!-- Option de déconnexion -->
          <button 
            class="menu-option logout-option"
            @click="handleLogout"
          >
            <span class="option-icon"><ArrowRightOnRectangleIcon class="user-menu-heroicon" /></span>
            <span class="option-label">Déconnexion</span>
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { logoutUser } from '@/api'
import { getInitials } from '@/utils'
import { Cog6ToothIcon, CreditCardIcon, ArrowRightOnRectangleIcon } from '@heroicons/vue/24/outline'


// Props et émissions d'événements
const emit = defineEmits(['logout'])

// Stores et router
const userStore = useUserStore()
const router = useRouter()

// Références réactives
const isOpen = ref(false)
const menuContainer = ref(null)

// Computed properties pour les données utilisateur
const userName = computed(() => {
  const fullName = `${userStore.firstName} ${userStore.lastName}`.trim()
  return fullName || 'Utilisateur'
})

const userInitials = computed(() => {
  return getInitials(userStore.firstName, userStore.lastName)
})

const userTitle = computed(() => {
  if (!userStore.isAuthenticated) return ''
  const level = userStore.level ?? 0
  const xp = userStore.xp ?? 0
  return `Niveau ${level} · ${xp} XP`
})

const showXp = computed(() => userStore.isAuthenticated)

const xpProgress = computed(() => {
  const level = Number(userStore.level || 0)
  const totalXp = Number(userStore.xp || 0)

  // Seuils exponentiels: niveau n atteint à n^2 * 10 XP
  const currentLevelThreshold = level * level * 10
  const nextLevelThreshold = (level + 1) * (level + 1) * 10

  const clampedTotal = Math.max(totalXp, currentLevelThreshold)
  const currentInLevel = clampedTotal - currentLevelThreshold
  const span = Math.max(1, nextLevelThreshold - currentLevelThreshold)

  return Math.min(100, Math.round((currentInLevel / span) * 100))
})

const userEmail = computed(() => {
  return userStore.email || 'email@exemple.com'
})

// Méthodes pour gérer le menu
const toggleMenu = () => {
  isOpen.value = !isOpen.value
}

const closeMenu = () => {
  isOpen.value = false
}

// Gestionnaires d'événements pour les options du menu
const handleAccount = () => {
  closeMenu()
  router.push('/account')
}

const handleSubscription = () => {
  closeMenu()
  router.push('/pricing')
}

const handleProfile = () => {
  closeMenu()
  router.push('/account')
}

const handleLogout = async () => {
  closeMenu()
  
  try {
    // Récupération du refresh token
    const refresh = localStorage.getItem('refresh_token')
    
    // Tentative de blacklist du token côté backend
    if (refresh && refresh !== 'null' && refresh !== 'undefined' && refresh.trim() !== '') {
      try {
        await logoutUser({ refresh })
      } catch (error) {
        // Ignore les erreurs de déconnexion (le backend gère déjà les erreurs)
        console.log('Erreur lors de la déconnexion backend:', error.message)
      }
    }
    
    // Nettoyage local
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    userStore.clearUser()
    
    // Émission de l'événement de déconnexion
    emit('logout')
    
    // Redirection vers la page d'accueil
    router.push('/')
    
  } catch (error) {
    console.error('Erreur lors de la déconnexion:', error)
    // En cas d'erreur, on force quand même la déconnexion locale
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    userStore.clearUser()
    router.push('/')
  }
}

// Gestion du clic en dehors du menu pour le fermer
const handleClickOutside = (event) => {
  if (menuContainer.value && !menuContainer.value.contains(event.target)) {
    closeMenu()
  }
}

// Gestion de la touche Escape pour fermer le menu
const handleEscapeKey = (event) => {
  if (event.key === 'Escape' && isOpen.value) {
    closeMenu()
  }
}

// Watch pour déboguer les changements XP/Level
watch(
  () => [userStore.xp, userStore.level, userStore.xp_to_next],
  (newVals, oldVals) => {
    console.log('🏪 UserMenu - Changement détecté dans le store:', {
      old: { xp: oldVals[0], level: oldVals[1], xp_to_next: oldVals[2] },
      new: { xp: newVals[0], level: newVals[1], xp_to_next: newVals[2] },
      progress: xpProgress.value
    })
  },
  { deep: true }
)

// Lifecycle hooks
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleEscapeKey)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleEscapeKey)
})
</script>

<style scoped>
/* Container principal du menu utilisateur */
.user-menu-container {
  position: relative;
  display: inline-block;
}

/* Bouton déclencheur du menu */
.user-menu-trigger {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: none;
  border: none;
  padding: 0.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  color: inherit;
  text-decoration: none;
}

.user-menu-trigger:hover {
  background-color: #f8fafc;
}

.user-menu-trigger:focus {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}

/* Informations utilisateur */
.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* Avatar utilisateur */
.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #60a5fa;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  font-weight: bold;
  border: 2px solid #60a5fa;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}

/* Anneau de progression (conic-gradient) autour de l'avatar */
.avatar-progress {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: conic-gradient(#22c55e var(--progress), #e5e7eb 0);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 2px; /* épaisseur de l'anneau */
}

/* Détails utilisateur */
.user-details {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  min-width: 0;
}

.user-xp-bar {
  width: clamp(80px, 18vw, 140px);
  height: 6px;
  background: #eef2ff;
  border-radius: 999px;
  overflow: hidden;
  margin-top: 4px;
}

.user-xp-fill {
  height: 100%;
  background: linear-gradient(90deg, #6366f1, #22c55e);
  width: 0;
  transition: width .3s ease;
}

@media (max-width: 768px) {
  .user-xp-bar { height: 4px; }
  .avatar-progress { width: 38px; height: 38px; }
}

@media (max-width: 480px) {
  .user-xp-bar { width: clamp(64px, 24vw, 100px); }
  .avatar-progress { width: 34px; height: 34px; }
}

.user-name {
  font-weight: 600;
  font-size: 1rem;
  color: #1f2937;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.2;
}

.user-title {
  display: block;
  font-size: 0.8rem;
  color: #64748b;
  font-weight: 600;
}

/* Réduction d'empreinte pour éviter le chevauchement sur petites largeurs */
@media (max-width: 770px) {
  .user-title { display: none; }
}

@media (max-width: 770px) {
  .user-xp-bar { display: none; }
}

/* Menu déroulant */
.user-menu-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  min-width: 280px;
  z-index: 15000;
  overflow: hidden;
}

/* En-tête du menu */
.menu-header {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 1.25rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 1px solid #e5e7eb;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  text-align: left;
}

.menu-header:hover {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
}

.menu-header:focus {
  outline: none;
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
}

.menu-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #60a5fa;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  font-weight: bold;
  border: 2px solid #60a5fa;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  flex-shrink: 0;
}

.menu-user-info {
  flex: 1;
  min-width: 0;
}

.menu-full-name {
  font-weight: 700;
  font-size: 1.125rem;
  color: #1f2937;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.2;
}

.menu-title {
  display: none;
}

.menu-email {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Séparateur */
.menu-divider {
  height: 1px;
  background: #e5e7eb;
  margin: 0.5rem 0;
}

/* Options du menu */
.menu-options {
  padding: 0;
}

.menu-option {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  width: 100%;
  padding: 0.875rem 1.25rem;
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #374151;
  font-size: 0.95rem;
  text-align: left;
  font-weight: 500;
}

.menu-option:hover {
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  color: #1f2937;
  transform: translateX(2px);
}

.menu-option:focus {
  outline: none;
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  color: #1f2937;
}

.option-icon {
  font-size: 1.25rem;
  width: 24px;
  text-align: center;
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.menu-option:hover .option-icon {
  transform: scale(1.1);
}

.option-label {
  flex: 1;
  font-weight: 500;
}

/* Option de déconnexion spéciale */
.logout-option {
  color: #dc2626;
  font-weight: 600;
}

.logout-option:hover {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  color: #b91c1c;
}

.logout-option .option-icon {
  color: #dc2626;
}

.logout-option:hover .option-icon {
  color: #b91c1c;
}

/* Animations de transition */
.menu-dropdown-enter-active,
.menu-dropdown-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.menu-dropdown-enter-from,
.menu-dropdown-leave-to {
  opacity: 0;
  transform: translateY(-12px) scale(0.95);
}

/* Responsive design */
@media (max-width: 768px) {
  .user-name {
    display: none;
  }
  
  .user-menu-dropdown {
    right: -0.5rem;
    min-width: 240px;
  }
  
  .menu-header {
    padding: 1rem;
  }
  
  .menu-option {
    padding: 0.75rem 1rem;
  }
  
  .user-avatar {
    width: 32px;
    height: 32px;
    font-size: 0.85rem;
  }
  
  .menu-avatar {
    width: 36px;
    height: 36px;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .user-menu-dropdown {
    min-width: 200px;
  }
  
  .menu-option {
    padding: 0.625rem 0.875rem;
    font-size: 0.9rem;
  }
  
  .option-icon {
    font-size: 1.1rem;
    width: 20px;
  }
}

.user-menu-heroicon {
  width: 1.4em;
  height: 1.4em;
  color: #193e8e;
  vertical-align: middle;
}
</style> 