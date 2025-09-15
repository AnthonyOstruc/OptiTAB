/**
 * Composable pour l'authentification Google One Tap
 * Simple, fluide et automatique
 */

import { ref } from 'vue'
import { googleLogin } from '@/api/auth'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { useToast } from '@/composables/useToast'

export function useGoogleAuth() {
  const router = useRouter()
  const userStore = useUserStore()
  const { closeModal } = useModalManager()
  const { showToast } = useToast()

  const isGoogleLoading = ref(false)
  const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID

  /**
   * Initialise Google Sign-In
   */
  const initializeGoogleSignIn = () => {
    if (!googleClientId) {
      console.warn('⚠️ VITE_GOOGLE_CLIENT_ID non configuré - Google Sign-In sera désactivé')
      console.warn('📝 Consultez ENV_SETUP.md pour configurer Google OAuth')
      return
    }

    // Vérifier si Google Identity Services est chargé
    if (typeof google !== 'undefined') {
      try {
        // Activer les logs détaillés côté GSI uniquement en développement
        if (import.meta?.env?.DEV && google?.accounts?.id?.setLogLevel) {
          google.accounts.id.setLogLevel('debug')
        }
      } catch (_) {}

      google.accounts.id.initialize({
        client_id: googleClientId,
        callback: handleGoogleCredentialResponse,
        context: 'signin',
        ux_mode: 'popup',
        auto_select: false,
        cancel_on_tap_outside: true,
        // Enable FedCM (mandatory from Oct 2024)
        use_fedcm_for_prompt: true
      })

      console.log('Google Sign-In initialisé (FedCM activé)')
      try {
        console.log('[GSI] Origin:', window.location.origin, '| Client ID:', googleClientId)
      } catch (_) {}
    } else {
      console.error('Google Identity Services non chargé')
    }
  }

  /**
   * Gère la connexion Google One Tap
   */
  const handleGoogleCredentialResponse = async (response) => {
    try {
      isGoogleLoading.value = true

      // Envoyer l'id_token Google au backend
      const result = await googleLogin({
        access_token: response.credential
      })

      // Récupérer les données de la réponse
      const { user, access, refresh } = result.data.data

      // Stocker nos tokens JWT
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)

      // Mettre à jour l'utilisateur
      userStore.setUser(user)
      await userStore.fetchUser()

      // Fermer et rediriger
      closeModal(MODAL_IDS.LOGIN)
      router.push('/dashboard')

      showToast('Connexion réussie !', 'success')

    } catch (error) {
      console.error('Erreur Google:', error)
      const errorMessage = error.response?.data?.message || 'Erreur de connexion'
      showToast(errorMessage, 'error')
    } finally {
      isGoogleLoading.value = false
    }
  }

  /**
   * Déclenche Google One Tap
   */
  const signInWithGoogle = () => {
    if (!googleClientId) {
      showToast('Google OAuth non configuré', 'warning')
      return
    }

    if (typeof google !== 'undefined') {
      // Appeler prompt sans callback pour éviter l'avertissement GSI lié aux méthodes de statut UI
      google.accounts.id.prompt()
    } else {
      showToast('Google Sign-In non disponible', 'error')
    }
  }

  /**
   * Charge le script Google Identity Services
   */
  const loadGoogleScript = () => {
    return new Promise((resolve, reject) => {
      // Vérifier si le script est déjà chargé
      if (typeof google !== 'undefined') {
        resolve()
        return
      }

      // Créer et charger le script
      const script = document.createElement('script')
      script.src = 'https://accounts.google.com/gsi/client'
      script.async = true
      script.defer = true

      script.onload = () => {
        console.log('Script Google Identity Services chargé')
        resolve()
      }

      script.onerror = () => {
        console.error('Erreur lors du chargement du script Google')
        reject(new Error('Failed to load Google script'))
      }

      document.head.appendChild(script)
    })
  }

  /**
   * Initialise complètement Google Sign-In
   */
  const setupGoogleSignIn = async () => {
    try {
      await loadGoogleScript()
      initializeGoogleSignIn()
    } catch (error) {
      console.error('Erreur lors de l\'initialisation Google Sign-In:', error)
    }
  }

  return {
    isGoogleLoading,
    signInWithGoogle,
    setupGoogleSignIn,
    loadGoogleScript,
    initializeGoogleSignIn
  }
}
