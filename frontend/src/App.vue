<template>
  <FullPageSpinner v-if="userStore.isLoading" />
  <div v-else id="app">
    <router-view v-slot="{ Component, route }">
      <keep-alive include="ExercisesByNotion,ExerciceDetail,CourseByNotion,ChapterQuiz,Themes,QuizNotions,CourseNotions,SynthesisNotions,SynthesisByNotion">
        <component :is="Component" :key="getComponentKey(route)" />
      </keep-alive>
    </router-view>
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
import LoginModal from '@/components/modals/LoginModal.vue'
import RegisterModal from '@/components/modals/RegisterModal.vue'
import ForgotPasswordModal from '@/components/modals/ForgotPasswordModal.vue'
import PaysNiveauSelector from '@/components/modals/PaysNiveauSelector.vue'
import Toast from '@/components/common/Toast.vue'
import { registerUser } from '@/api'
import { triggerDailyLogin } from '@/api/users'
import { useUserStore } from '@/stores/user'
import { useSubjectsStore } from '@/stores/subjects/index'
import FullPageSpinner from '@/components/common/FullPageSpinner.vue'
import { useNotificationStore } from '@/stores/notifications'
import { useCheckoutIntentStore } from '@/stores/checkoutIntent'
import { useToast } from '@/composables/useToast'
import { useSidebarStore } from '@/stores/sidebar'

const userStore = useUserStore()
const subjectsStore = useSubjectsStore()
const router = useRouter()
const { isModalOpen, closeModal, openModal } = useModalManager()
const notificationStore = useNotificationStore()
const checkoutIntentStore = useCheckoutIntentStore()
const { info: toastInfo, error: toastError } = useToast()
const sidebarStore = useSidebarStore()

if (typeof window !== 'undefined') {
  checkoutIntentStore.initFromStorage()
}

// Fonction pour générer une clé unique pour KeepAlive
// Utilise les params de la route au lieu du path complet pour préserver l'état
function getComponentKey(route) {
  const name = route.name
  
  // Pour les vues qui doivent être mises en cache par notion
  // IMPORTANT : utiliser route.name (pas de variation) pour maintenir le même composant
  if (name === 'ExercicesByNotion' || name === 'CourseByNotion' || name === 'SynthesisByNotion') {
    // Utiliser le name uniquement pour garder l'instance active
    // Le composant gère lui-même le changement de notionId via watch
    return name
  }
  
  if (name === 'Themes' || name === 'CourseNotions' || name === 'QuizNotions' || name === 'SynthesisNotions') {
    // Pour ces vues, utiliser matiereId
    return `${name}-${route.params.matiereId || 'default'}`
  }
  
  // Pour les autres vues, utiliser le path complet
  return route.path
}

// Verification flow removed

// State for pays/niveau modal
const isPaysNiveauModalOpen = ref(false)

const canProcessCheckout = computed(() => userStore.isAuthenticated && !userStore.isLoading)

const attemptPendingCheckout = async () => {
  if (!checkoutIntentStore.hasIntent) return
  const planLabel = checkoutIntentStore.planName || 'OptiTAB'
  toastInfo(`Redirection vers le paiement ${planLabel}…`, 4000)
  try {
    const result = await checkoutIntentStore.processIntent()
    if (!result?.redirected) {
      toastError('Impossible d’ouvrir la page de paiement. Réessaie depuis la section Tarifs.')
    }
  } catch (error) {
    console.error('Erreur redirection paiement:', error)
    toastError('Impossible d’ouvrir la page de paiement. Réessaie depuis la section Tarifs.')
  }
}

watch(canProcessCheckout, (ready) => {
  if (ready) {
    attemptPendingCheckout()
  }
}, { immediate: true })

watch(
  () => checkoutIntentStore.hasIntent,
  (hasIntent) => {
    if (hasIntent && canProcessCheckout.value) {
      attemptPendingCheckout()
    }
  }
)

onMounted(() => {
  if (typeof window !== 'undefined') {
    sidebarStore.init()
  }
})

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

// Verification flow removed

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
    // Inscription classique: fermer la modale et aller au dashboard
    closeRegisterModal()
    router.push('/dashboard')
  }
}
const handleSwitchToLogin = () => {
  closeRegisterModal()
  closeForgotPasswordModal()
  openModal(MODAL_IDS.LOGIN)
}
const handleTerms = () => {}
const handlePrivacy = () => {}
const handleForgotPasswordSubmit = (forgotPasswordData) => {}

// Déclenche la récompense quotidienne de connexion (+1 XP)
const handleDailyLoginReward = async () => {
  try {
    if (!userStore.isAuthenticated || !userStore.id) return
    const todayKey = `daily_login_rewarded_${userStore.id}_${new Date().toDateString()}`
    if (localStorage.getItem(todayKey)) {
      return
    }
    const res = await triggerDailyLogin()
    const payload = res?.data?.data || res?.data || {}
    if (payload && payload.xp_awarded > 0) {
      // Mettre à jour le store XP/niveau immédiatement depuis la réponse
      const newXp = Number(payload.new_xp ?? (userStore.xp + payload.xp_awarded))
      userStore.xp = newXp
      userStore.level = Number(payload.level ?? userStore.level)
      userStore.xp_to_next = Number(payload.xp_to_next ?? userStore.xp_to_next)
      userStore.loginStreakCount = Number(payload.streak_count ?? (userStore.loginStreakCount || 1))
    } else if (payload && payload.streak_count !== undefined) {
      userStore.loginStreakCount = Number(payload.streak_count)
    }
    localStorage.setItem(todayKey, 'true')
  } catch (e) {
    // Silencieux en cas d'erreur
    console.warn('⚠️ Daily login reward failed:', e?.response?.status || e?.message)
  }
}

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
watch(() => userStore.isAuthenticated, async (isAuthenticated) => {
  if (isAuthenticated) {
    // Récompense de connexion quotidienne (+1 XP) avant de charger les notifications
    await handleDailyLoginReward()
    checkAndShowPaysNiveauModal()
    // Charger les notifications persistées localement puis fusionner celles du serveur
    try { await notificationStore.loadFromServer() } catch (_) {}
    try { await notificationStore.loadFromLocal() } catch (_) {}
    // Initialiser le store des matières si l'utilisateur est déjà configuré
    if (userStore.pays && userStore.niveau_pays) {
      initializeSubjectsStoreWhenReady()
    }
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
  if (userStore.isAuthenticated) {
    await handleDailyLoginReward()
    checkAndShowPaysNiveauModal()
    
    // Si l'utilisateur est déjà configuré, initialiser le store des matières
    if (userStore.pays && userStore.niveau_pays) {
      initializeSubjectsStoreWhenReady()
    }

    // Charger d'abord les notifications locales persistées, puis fusionner celles du serveur
    try { await notificationStore.loadFromServer() } catch (_) {}
    try { await notificationStore.loadFromLocal() } catch (_) {}
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

html {
  /* Empêcher le zoom automatique sur iOS */
  -webkit-text-size-adjust: 100%;
  text-size-adjust: 100%;
  /* Empêcher le sélection de texte qui peut causer du zoom */
  -webkit-tap-highlight-color: transparent;
    overscroll-behavior: none;
  }

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: #333;
  /* Empêcher le zoom lors de double-tap */
  touch-action: manipulation;
  /* Assurer que le body utilise toute la largeur */
  width: 100%;
  overflow-x: hidden;
  /* Empêcher le zoom sur certains éléments */
  -webkit-text-size-adjust: 100%;
  text-size-adjust: 100%;
}

#app {
  min-height: 100vh;
  /* S'assurer que l'app prend toute la largeur */
  width: 100%;
  overflow-x: hidden;
}

/* Empêcher le zoom automatique sur les inputs en iOS */
input,
textarea,
select {
  font-size: 16px !important;
  /* iOS ne zoom pas si la taille de police est >= 16px */
}

/* Pour les petits écrans */
@media screen and (max-width: 768px) {
  html {
    /* S'assurer que la largeur est correcte */
    width: 100%;
    overflow-x: hidden;
    /* Empêcher le zoom lors du scroll depuis le haut */
    touch-action: pan-y;
    overscroll-behavior: none;
  }
  
  body {
    /* Empêcher le zoom indésirable */
    position: relative;
    width: 100%;
    min-width: 100%;
    max-width: 100vw;
    /* Empêcher le zoom lors du scroll */
    touch-action: pan-y;
    /* Empêcher le zoom lors du scroll depuis le header */
    overscroll-behavior: none;
  }
  
  /* Empêcher le zoom lors du scroll en haut de page sur mobile */
  body:not(.no-scroll) {
    overflow-x: hidden;
    overflow-y: auto;
    /* Empêcher le bounce scroll qui peut causer des problèmes de zoom */
    -webkit-overflow-scrolling: touch;
  }
}

/* Neutraliser uniquement les grands wrappers (1er niveau) dans cours/synthèse */
:where(.sheet-content, .cours-content) > :is(
  [style*="background:#ffffff;"],
  [style*="background: #ffffff;"],
  [style$="background:#ffffff"],
  [style$="background: #ffffff"],
  [style*="background:#fff;"],
  [style*="background: #fff;"],
  [style$="background:#fff"],
  [style$="background: #fff"],
  [style*="background:#f9f9f9;"],
  [style*="background: #f9f9f9;"],
  [style$="background:#f9f9f9"],
  [style$="background: #f9f9f9"]
) {
  background: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
}

/* Supprimer la box blanche juste après un titre (h1/h2/h3) */
:where(.sheet-content, .cours-content) :is(h1, h2, h3) + :is(
  [style*="background:#fff;"],
  [style*="background: #fff;"],
  [style$="background:#fff"],
  [style$="background: #fff"],
  [style*="background:#ffffff;"],
  [style*="background: #ffffff;"],
  [style$="background:#ffffff"],
  [style$="background: #ffffff"]
) {
  background: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
}

/* Supprimer aussi les boîtes blanches qui CONTIENNENT un sous-titre (h2–h6) */
:where(.sheet-content, .cours-content) :is(
  [style*="background:#fff;"],
  [style*="background: #fff;"],
  [style$="background:#fff"],
  [style$="background: #fff"],
  [style*="background:#ffffff;"],
  [style*="background: #ffffff;"],
  [style$="background:#ffffff"],
  [style$="background: #ffffff"]
):has(:is(h2, h3, h4, h5, h6)) {
  background: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
}

/* Cas imbriqué courant: sous-titre -> conteneur gris -> boîte blanche */
:where(.sheet-content, .cours-content) :is(h2, h3, h4, h5, h6) + [style*="background:#f8f9fa"] > :is(
  [style*="background:#fff;"],
  [style*="background: #fff;"],
  [style$="background:#fff"],
  [style$="background: #fff"],
  [style*="background:#ffffff;"],
  [style*="background: #ffffff;"],
  [style$="background:#ffffff"],
  [style$="background: #ffffff"]
) {
  background: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
}
</style>
