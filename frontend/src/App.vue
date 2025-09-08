<template>
  <FullPageSpinner v-if="userStore.isLoading" />
  <div v-else id="app">
    <router-view />
    <!-- Login Modal -->
    <LoginModal 
      :is-open="isLoginModalOpen"
      @close="closeLoginModal"
      @login="handleLogin"
      @signup="handleSignUp"
      @forgot-password="handleForgotPassword"
    />
    
    <!-- Register Modal -->
    <RegisterModal 
      :is-open="isRegisterModalOpen"
      @close="closeRegisterModal"
      @register="handleRegister"
      @login="handleSwitchToLogin"
      @terms="handleTerms"
      @privacy="handlePrivacy"
    />
    
    <!-- Forgot Password Modal -->
    <ForgotPasswordModal 
      :is-open="isForgotPasswordModalOpen"
      @close="closeForgotPasswordModal"
      @forgot-password="handleForgotPassword"
      @login="handleSwitchToLogin"
    />

    <!-- Verify Code Modal -->
    <VerifyCodeModal
      :is-open="isVerifyCodeModalOpen"
      :email="pendingVerifyEmail"
      @close="closeVerifyCodeModal"
      @verified="handleVerified"
    />

    <!-- Modal de sélection Pays/Niveau pour nouveaux utilisateurs -->
    <PaysNiveauSelector
      :is-open="isPaysNiveauModalOpen"
      @configuration-complete="handleConfigurationComplete"
      @close="closePaysNiveauModal"
    />

    <!-- Toast Notifications -->
    <Toast />
    
    <!-- XP Reward Notifications pour les objectifs journaliers -->
    <XPRewardNotification />
    
    <!-- Objective Unlocked Notifications -->
    <ObjectiveUnlockedNotification />
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import LoginModal from '@/components/modals/LoginModal.vue'
import RegisterModal from '@/components/modals/RegisterModal.vue'
import ForgotPasswordModal from '@/components/modals/ForgotPasswordModal.vue'
import VerifyCodeModal from '@/components/modals/VerifyCodeModal.vue'
import PaysNiveauSelector from '@/components/modals/PaysNiveauSelector.vue'
import Toast from '@/components/common/Toast.vue'
import XPRewardNotification from '@/components/notifications/XPRewardNotification.vue'
import ObjectiveUnlockedNotification from '@/components/notifications/ObjectiveUnlockedNotification.vue'
import { registerUser } from '@/api'
import { useUserStore } from '@/stores/user'
import { useSubjectsStore } from '@/stores/subjects/index'
import FullPageSpinner from '@/components/common/FullPageSpinner.vue'
import { useStreak } from '@/composables/useStreak'
import { useNotificationStore } from '@/stores/notifications'

const userStore = useUserStore()
const subjectsStore = useSubjectsStore()
const router = useRouter()
const { isModalOpen, closeModal, openModal } = useModalManager()
const { checkDailyStreak } = useStreak()
const notificationStore = useNotificationStore()

// State for verify code modal
const isVerifyCodeModalOpen = ref(false)
const pendingVerifyEmail = ref('')

// State for pays/niveau modal
const isPaysNiveauModalOpen = ref(false)

// Computed
const isLoginModalOpen = computed(() => isModalOpen(MODAL_IDS.LOGIN))
const isRegisterModalOpen = computed(() => isModalOpen(MODAL_IDS.REGISTER))
const isForgotPasswordModalOpen = computed(() => isModalOpen(MODAL_IDS.FORGOT_PASSWORD))

// Modal methods
const closeLoginModal = () => closeModal(MODAL_IDS.LOGIN)
const closeRegisterModal = () => closeModal(MODAL_IDS.REGISTER)
const closeForgotPasswordModal = () => closeModal(MODAL_IDS.FORGOT_PASSWORD)

// Pays/Niveau modal methods
const closePaysNiveauModal = () => {
  isPaysNiveauModalOpen.value = false
}

// Initialiser le store des matières seulement quand l'utilisateur est configuré
const initializeSubjectsStoreWhenReady = async () => {
  if (userStore.isAuthenticated && userStore.pays && userStore.niveau_pays) {
    try {
      await subjectsStore.initialize()
    } catch (error) {
      console.error('Erreur lors de l\'initialisation du store des matières:', error)
    }
  }
}

const handleConfigurationComplete = () => {
  // Marquer la configuration comme terminée pour cet utilisateur spécifique
  if (userStore.id) {
    const userConfigKey = `configurationCompleted_${userStore.id}`
    localStorage.setItem(userConfigKey, 'true')
  }
  
  closePaysNiveauModal()
  
  // Recharger les données utilisateur pour avoir les nouvelles infos
  userStore.fetchUser().then(() => {
    initializeSubjectsStoreWhenReady()
  })
}

// Verify code modal methods
const openVerifyCodeModal = (email) => {
  pendingVerifyEmail.value = email
  isVerifyCodeModalOpen.value = true
}
const closeVerifyCodeModal = () => {
  isVerifyCodeModalOpen.value = false
  pendingVerifyEmail.value = ''
}

// Login handlers
const handleLogin = (loginData) => {
  if (loginData.provider === 'google') {
    // Google login
  } else {
    // Email/password login - fermer le modal
    closeLoginModal()
  }
}
const handleSignUp = () => {
  closeLoginModal()
  openModal(MODAL_IDS.REGISTER)
}
const handleForgotPassword = () => {
  closeLoginModal()
  openModal(MODAL_IDS.FORGOT_PASSWORD)
}
// Register handlers
const handleRegister = async (registerData) => {
  if (registerData.provider === 'google') {
    // Google registration
  } else {
    closeRegisterModal()
    openVerifyCodeModal(registerData.email)
  }
}
const handleSwitchToLogin = () => {
  closeRegisterModal()
  closeForgotPasswordModal()
  openModal(MODAL_IDS.LOGIN)
}
const handleTerms = () => {}
const handlePrivacy = () => {}
const handleVerified = () => {
  closeVerifyCodeModal()
  router.push('/dashboard')
}
const handleForgotPasswordSubmit = (forgotPasswordData) => {}

// Logique pour afficher le modal pays/niveau pour les nouveaux utilisateurs
const checkAndShowPaysNiveauModal = () => {
  // Attendre que les données utilisateur soient chargées
  if (userStore.isLoading || !userStore.isAuthenticated || !userStore.id) {
    return
  }
  
  // Vérifier si l'utilisateur n'a pas de pays ou niveau
  const hasPays = userStore.pays !== null && userStore.pays !== undefined
  const hasNiveau = userStore.niveau_pays !== null && userStore.niveau_pays !== undefined
  
  if (!hasPays || !hasNiveau) {
    const userConfigKey = `configurationCompleted_${userStore.id}`
    const configCompleted = localStorage.getItem(userConfigKey) === 'true'
    
    // Si le localStorage dit "terminé" mais l'utilisateur n'a pas de pays/niveau
    // C'est une incohérence, on nettoie
    if (configCompleted && (!hasPays || !hasNiveau)) {
      localStorage.removeItem(userConfigKey)
    }
    
    if (!localStorage.getItem(userConfigKey) && !isPaysNiveauModalOpen.value) {
      isPaysNiveauModalOpen.value = true
    }
  }
}

// Watcher pour vérifier quand l'utilisateur se connecte
watch(() => userStore.isAuthenticated, (isAuthenticated) => {
  if (isAuthenticated) {
    // Vérifier/attribuer le streak dès que l'utilisateur est authentifié
    setTimeout(async () => {
      try {
        await checkDailyStreak()
      } catch (e) {
        console.warn('Erreur verification streak (auth watcher):', e)
      }
      checkAndShowPaysNiveauModal()
      // Charger notifications persistées à la connexion
      try { await notificationStore.loadFromServer() } catch (_) {}
    }, 200)
  }
}, { immediate: true })

// Watcher pour vérifier quand les données utilisateur changent
watch([() => userStore.pays, () => userStore.niveau_pays, () => userStore.isLoading], ([pays, niveau_pays, isLoading]) => {
  // Si les données sont chargées et l'utilisateur est authentifié
  if (!isLoading && userStore.isAuthenticated && userStore.id) {
    const hasPays = pays !== null && pays !== undefined
    const hasNiveau = niveau_pays !== null && niveau_pays !== undefined
    
    if (hasPays && hasNiveau) {
      // L'utilisateur a maintenant un pays et un niveau, fermer le modal
      isPaysNiveauModalOpen.value = false
      
      // Marquer comme configuré pour cet utilisateur
      const userConfigKey = `configurationCompleted_${userStore.id}`
      localStorage.setItem(userConfigKey, 'true')
      
      // Initialiser le store des matières maintenant que l'utilisateur est configuré
      initializeSubjectsStoreWhenReady()
    } else {
      // Vérifier si on doit afficher le modal
      checkAndShowPaysNiveauModal()
    }
  }
})

// Vérifier au montage de l'application
onMounted(async () => {
  // Vérifier le streak quotidien dès l'ouverture du site
  try {
    await checkDailyStreak()
  } catch (error) {
    console.warn('Erreur verification streak:', error)
  }

  if (userStore.isAuthenticated) {
    checkAndShowPaysNiveauModal()
    
    // Si l'utilisateur est déjà configuré, initialiser le store des matières
    if (userStore.pays && userStore.niveau_pays) {
      initializeSubjectsStoreWhenReady()
    }

    // Charger les notifications persistées
    try { await notificationStore.loadFromServer() } catch (_) {}
  }
})
</script>

<style>
/* Global styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: #333;
}

#app {
  min-height: 100vh;
}
</style>
