/**
 * Composable pour l'authentification Google One Tap
 * Simple, fluide et automatique
 */

import { ref, nextTick } from 'vue'
import { googleLogin, googleOAuthExchange } from '@/api/auth'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { useToast } from '@/composables/useToast'

export function useGoogleAuth() {
  const router = useRouter()
  const userStore = useUserStore()
  const { openModal, closeModal, isModalOpen } = useModalManager()
  const { showToast } = useToast()

  const isGoogleLoading = ref(false)
  const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID
  // Permet de savoir si on doit réouvrir le modal login après l'interaction Google
  const shouldReopenLoginModal = ref(false)
  // Évite les boucles de fallback
  const didFallbackToNoFedCM = ref(false)
  const didFallbackToOAuth = ref(false)

  const isFedCMPreferred = () => {
    try {
      const disabledFlag = localStorage.getItem('gsi_disable_fedcm') === '1'
      if (disabledFlag) return false
      const envOverride = import.meta?.env?.VITE_GSI_ENABLE_FEDCM
      if (envOverride === 'true') return true
      if (envOverride === 'false') return false
      // Par défaut, on désactive FedCM en production pour éviter les warnings incognito
      return !import.meta?.env?.PROD
    } catch (_) {
      return !import.meta?.env?.PROD
    }
  }

  /**
   * Initialise Google Sign-In
   */
  const initializeGoogleSignIn = (options = {}) => {
    const { useFedCMForPrompt = isFedCMPreferred() } = options
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
        // FedCM peut échouer en navigation privée si l'utilisateur n'est pas connecté à l'IdP
        use_fedcm_for_prompt: !!useFedCMForPrompt
      })

      console.log(`Google Sign-In initialisé (FedCM=${!!useFedCMForPrompt})`)
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
      // Si l'utilisateur venait du modal Login, on le ré-ouvre en cas d'échec
      if (shouldReopenLoginModal.value) {
        openModal(MODAL_IDS.LOGIN)
        shouldReopenLoginModal.value = false
      }
    } finally {
      isGoogleLoading.value = false
    }
  }

  const startOAuthFallback = () => {
    return new Promise((resolve, reject) => {
      try {
        if (!google?.accounts?.oauth2?.initCodeClient) {
          reject(new Error('OAuth2 Code Client non disponible'))
          return
        }

        const codeClient = google.accounts.oauth2.initCodeClient({
          client_id: googleClientId,
          scope: 'openid email profile',
          ux_mode: 'popup',
          callback: async (resp) => {
            try {
              if (resp?.code) {
                // Envoyer le code au backend pour échange
                const result = await googleOAuthExchange({ code: resp.code })
                const { user, access, refresh } = result.data.data

                localStorage.setItem('access_token', access)
                localStorage.setItem('refresh_token', refresh)
                userStore.setUser(user)
                await userStore.fetchUser()
                closeModal(MODAL_IDS.LOGIN)
                router.push('/dashboard')
                showToast('Connexion réussie !', 'success')
                didFallbackToOAuth.value = true
                shouldReopenLoginModal.value = false
                resolve(true)
              } else {
                reject(new Error('Code OAuth non reçu'))
              }
            } catch (e) {
              reject(e)
            }
          },
        })

        codeClient.requestCode()
      } catch (e) {
        reject(e)
      }
    })
  }

  /**
   * Déclenche Google One Tap
   */
  const signInWithGoogle = async () => {
    if (!googleClientId) {
      showToast('Google OAuth non configuré', 'warning')
      return
    }

    if (typeof google !== 'undefined') {
      // Si FedCM n'est pas préféré, lancer directement le Code Flow en popup
      if (!isFedCMPreferred()) {
        try {
          await startOAuthFallback()
          return
        } catch (e) {
          // En cas d'échec, ouvrir/rouvrir le modal login
          if (shouldReopenLoginModal.value) {
            openModal(MODAL_IDS.LOGIN)
            shouldReopenLoginModal.value = false
          }
          showToast('Échec de la connexion Google', 'error')
          return
        }
      }
      // Si le modal Login est ouvert, on le ferme temporairement pour laisser Google au premier plan
      shouldReopenLoginModal.value = isModalOpen(MODAL_IDS.LOGIN)
      if (shouldReopenLoginModal.value) {
        closeModal(MODAL_IDS.LOGIN)
        await nextTick()
      }

      // Utiliser le callback de moment pour gérer l'affichage/fermeture du prompt
      try {
        didFallbackToNoFedCM.value = false
        const runPrompt = () => {
          google.accounts.id.prompt((notification) => {
            try {
              const isNotDisplayed = notification?.isNotDisplayed?.()
              const notDisplayedReason = notification?.getNotDisplayedReason?.()
              const isSkipped = notification?.isSkippedMoment?.()
              const skippedReason = notification?.getSkippedReason?.()
              const isDismissed = notification?.isDismissedMoment?.()
              const dismissedReason = notification?.getDismissedReason?.()

              const closedWithoutCredential = (
                (isDismissed && dismissedReason !== 'credential_returned') ||
                isNotDisplayed ||
                isSkipped
              )

              // Fallback: si le prompt FedCM n'est pas affiché en navigation privée, ré-essayer sans FedCM une seule fois
              const shouldFallbackNoFedCM = (
                !didFallbackToNoFedCM.value && (
                  isNotDisplayed ||
                  notDisplayedReason === 'opt_out_or_no_session' ||
                  notDisplayedReason === 'unknown_reason' ||
                  (isDismissed && dismissedReason === 'token_generation_failed') ||
                  (isDismissed && dismissedReason === 'network_error')
                )
              )

              if (shouldFallbackNoFedCM) {
                didFallbackToNoFedCM.value = true
                try {
                  initializeGoogleSignIn({ useFedCMForPrompt: false })
                  // Attendre le prochain tick pour s'assurer de l'init
                  nextTick().then(() => {
                    runPrompt()
                  })
                  return
                } catch (_) {}
              }

              // Si après le fallback no-FedCM, l'UI n'est toujours pas affichée ou a échoué,
              // tenter l'OAuth Code Flow en popup (comme le font d'autres sites)
              const shouldStartOAuth = (
                !didFallbackToOAuth.value && (
                  closedWithoutCredential || isNotDisplayed || isSkipped || isDismissed
                )
              )

              if (shouldStartOAuth) {
                startOAuthFallback().catch(() => {
                  if (shouldReopenLoginModal.value) {
                    openModal(MODAL_IDS.LOGIN)
                    shouldReopenLoginModal.value = false
                  }
                })
                return
              }

              if (closedWithoutCredential && shouldReopenLoginModal.value) {
                openModal(MODAL_IDS.LOGIN)
                shouldReopenLoginModal.value = false
              }
            } catch (_) {}
          })
        }
        runPrompt()
      } catch (_) {
        // En cas d'erreur imprévue, ré-ouvrir le modal si on l'avait fermé
        if (shouldReopenLoginModal.value) {
          openModal(MODAL_IDS.LOGIN)
          shouldReopenLoginModal.value = false
        }
      }
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
