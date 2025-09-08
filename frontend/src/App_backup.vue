<template>
  <FullPageSpinner v-if="userStore.isLoading" />
  <div v-else id="app">
    <!-- Debug button (dev only) -->
    <div v-if="isDevelopment" style="position: fixed; top: 10px; right: 10px; z-index: 10000;">
      <button 
        @click="forceShowModal"
        style="background: #ff4444; color: white; border: none; padding: 10px; border-radius: 5px; font-size: 12px; cursor: pointer;"
      >
        🐛 Force Modal
      </button>
      <button 
        @click="debugUserState"
        style="background: #4444ff; color: white; border: none; padding: 10px; border-radius: 5px; font-size: 12px; cursor: pointer; margin-left: 5px;"
      >
        🔍 Debug User
      </button>
      <button 
        @click="clearConfigForUser"
        style="background: #44ff44; color: white; border: none; padding: 10px; border-radius: 5px; font-size: 12px; cursor: pointer; margin-left: 5px;"
      >
        🧹 Clear Config
      </button>
      <button 
        @click="fullReset"
        style="background: #ff8800; color: white; border: none; padding: 10px; border-radius: 5px; font-size: 12px; cursor: pointer; margin-left: 5px;"
      >
        🔥 Full Reset
      </button>
    </div>
    
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
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { useConfigurationModal } from '@/composables/useConfigurationModal'
import LoginModal from '@/components/modals/LoginModal.vue'
import RegisterModal from '@/components/modals/RegisterModal.vue'
import ForgotPasswordModal from '@/components/modals/ForgotPasswordModal.vue'
import VerifyCodeModal from '@/components/modals/VerifyCodeModal.vue'
import PaysNiveauSelector from '@/components/modals/PaysNiveauSelector.vue'
import Toast from '@/components/common/Toast.vue'
import { registerUser } from '@/api'
import { useUserStore } from '@/stores/user'
import { useSubjectsStore } from '@/stores/subjects/index'
import FullPageSpinner from '@/components/common/FullPageSpinner.vue'

const userStore = useUserStore()
const subjectsStore = useSubjectsStore()
const router = useRouter()
const { isModalOpen, closeModal, openModal } = useModalManager()

// Configuration modal pays/niveau
const { 
  isModalOpen: isConfigurationModalOpen, 
  closeModal: closeConfigurationModal, 
  handleConfigurationConfirmed 
} = useConfigurationModal()

// Computed pour le mode développement
const isDevelopment = computed(() => import.meta.env.DEV)

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
    console.log('🎯 Initialisation du store des matières avec utilisateur configuré')
    try {
      await subjectsStore.initialize()
      console.log('✅ Store des matières initialisé avec succès')
    } catch (error) {
      console.error('❌ Erreur lors de l\'initialisation du store des matières:', error)
    }
  }
}

const handleConfigurationComplete = () => {
  console.log('✅ Configuration pays/niveau terminée')
  
  // Marquer la configuration comme terminée pour cet utilisateur spécifique
  if (userStore.id) {
    const userConfigKey = `configurationCompleted_${userStore.id}`
    localStorage.setItem(userConfigKey, 'true')
  }
  
  closePaysNiveauModal()
  
  // Recharger les données utilisateur pour avoir les nouvelles infos
  userStore.fetchUser().then(() => {
    console.log('🔄 Données utilisateur rechargées après configuration')
    // Maintenant initialiser le store des matières avec les bonnes données
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
  console.log('🔍 Vérification modal pays/niveau:', {
    isAuthenticated: userStore.isAuthenticated,
    pays: userStore.pays,
    pays_type: typeof userStore.pays,
    niveau_pays: userStore.niveau_pays,
    niveau_pays_type: typeof userStore.niveau_pays,
    userId: userStore.id,
    isLoading: userStore.isLoading,
    isPaysNiveauModalOpen: isPaysNiveauModalOpen.value
  })
  
  // Attendre que les données utilisateur soient chargées
  if (userStore.isLoading) {
    console.log('⏳ Données utilisateur en cours de chargement...')
    return
  }
  
  // Vérifier si l'utilisateur est connecté
  if (!userStore.isAuthenticated || !userStore.id) {
    console.log('❌ Utilisateur non authentifié ou sans ID')
    return
  }
  
  // Vérifier si l'utilisateur n'a pas de pays ou niveau
  const hasPays = userStore.pays !== null && userStore.pays !== undefined
  const hasNiveau = userStore.niveau_pays !== null && userStore.niveau_pays !== undefined
  
  console.log('📊 Vérification configuration:', {
    hasPays,
    hasNiveau,
    paysValue: userStore.pays,
    niveauValue: userStore.niveau_pays
  })
  
  if (!hasPays || !hasNiveau) {
    // Vérifier si on n'a pas déjà montré le modal pour cet utilisateur
    const userConfigKey = `configurationCompleted_${userStore.id}`
    const configCompleted = localStorage.getItem(userConfigKey) === 'true'
    
    console.log('🔍 Vérification localStorage:', {
      userConfigKey,
      configCompleted,
      modalAlreadyOpen: isPaysNiveauModalOpen.value
    })
    
    // Si le localStorage dit "terminé" mais l'utilisateur n'a pas de pays/niveau
    // C'est une incohérence, on nettoie
    if (configCompleted && (!hasPays || !hasNiveau)) {
      console.log('🧹 Incohérence détectée - Nettoyage localStorage')
      localStorage.removeItem(userConfigKey)
    }
    
    // TEMPORAIRE : Ignorer la configuration localStorage pour tester
    const forceShowForTesting = isDevelopment.value && false // Changez à true pour forcer
    
    if ((!localStorage.getItem(userConfigKey) || forceShowForTesting) && !isPaysNiveauModalOpen.value) {
      console.log('🎯 OUVERTURE DU MODAL - Utilisateur sans configuration complète')
      isPaysNiveauModalOpen.value = true
    } else {
      console.log('⚠️ Modal non ouvert:', {
        reasonConfigCompleted: localStorage.getItem(userConfigKey),
        reasonModalOpen: isPaysNiveauModalOpen.value,
        forceShowForTesting
      })
    }
  } else {
    console.log('✅ Utilisateur déjà configuré avec pays et niveau')
  }
}

// Watcher pour vérifier quand l'utilisateur se connecte
watch(() => userStore.isAuthenticated, (isAuthenticated) => {
  if (isAuthenticated) {
    console.log('👤 Utilisateur authentifié, vérification modal...')
    // Attendre que les données utilisateur soient chargées
    setTimeout(() => {
      checkAndShowPaysNiveauModal()
    }, 200)
  }
}, { immediate: true })

// Watcher pour vérifier quand les données utilisateur changent
watch([() => userStore.pays, () => userStore.niveau_pays, () => userStore.isLoading], ([pays, niveau_pays, isLoading]) => {
  console.log('🔄 Changement données utilisateur:', { 
    pays, 
    niveau_pays, 
    isLoading,
    paysType: typeof pays,
    niveauType: typeof niveau_pays,
    isAuthenticated: userStore.isAuthenticated,
    userId: userStore.id
  })
  
  // Si les données sont chargées et l'utilisateur est authentifié
  if (!isLoading && userStore.isAuthenticated && userStore.id) {
    const hasPays = pays !== null && pays !== undefined
    const hasNiveau = niveau_pays !== null && niveau_pays !== undefined
    
    if (hasPays && hasNiveau) {
      // L'utilisateur a maintenant un pays et un niveau, fermer le modal
      console.log('✅ Utilisateur configuré, fermeture du modal')
      isPaysNiveauModalOpen.value = false
      
      // Marquer comme configuré pour cet utilisateur
      const userConfigKey = `configurationCompleted_${userStore.id}`
      localStorage.setItem(userConfigKey, 'true')
      
      // Initialiser le store des matières maintenant que l'utilisateur est configuré
      initializeSubjectsStoreWhenReady()
    } else {
      // Vérifier si on doit afficher le modal
      console.log('⚠️ Utilisateur incomplet, vérification modal...')
      checkAndShowPaysNiveauModal()
    }
  } else {
    console.log('⏳ En attente de l\'authentification ou du chargement complet')
  }
})

// Vérifier au montage de l'application
onMounted(() => {
  console.log('🚀 Application montée, vérification modal...')
  if (userStore.isAuthenticated) {
    checkAndShowPaysNiveauModal()
    
    // Si l'utilisateur est déjà configuré, initialiser le store des matières
    if (userStore.pays && userStore.niveau_pays) {
      initializeSubjectsStoreWhenReady()
    }
  }
})

// Méthodes de debug (dev only)
const forceShowModal = () => {
  console.log('🐛 Force ouverture du modal')
  isPaysNiveauModalOpen.value = true
}

const debugUserState = () => {
  console.log('🔍 État utilisateur détaillé:', {
    userStore: { ...userStore.$state },
    localStorage: {
      configKey: `configurationCompleted_${userStore.id}`,
      configValue: localStorage.getItem(`configurationCompleted_${userStore.id}`)
    },
    modal: {
      isPaysNiveauModalOpen: isPaysNiveauModalOpen.value
    }
  })
}

const clearConfigForUser = () => {
  if (userStore.id) {
    const userConfigKey = `configurationCompleted_${userStore.id}`
    localStorage.removeItem(userConfigKey)
    console.log('🧹 Configuration utilisateur supprimée pour:', userConfigKey)
    checkAndShowPaysNiveauModal()
  }
}

const fullReset = () => {
  console.log('🔥 Reset complet de toutes les données localStorage')
  
  // Nettoyer toutes les clés possibles
  const allKeys = [
    'access_token',
    'refresh_token',
    'selectedMatieres',
    'favoriteMatieresIds',
    'activeMatiereId', 
    'selectedMatieresIds'
  ]
  
  // Nettoyer aussi toutes les clés de configuration utilisateur
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i)
    if (key && key.startsWith('configurationCompleted_')) {
      allKeys.push(key)
    }
  }
  
  allKeys.forEach(key => {
    localStorage.removeItem(key)
    console.log('🗑️ Supprimé:', key)
  })
  
  // Recharger la page pour un état propre
  setTimeout(() => {
    window.location.reload()
  }, 1000)
}
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
