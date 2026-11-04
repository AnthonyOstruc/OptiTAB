<template>
  <!-- Spinner global pour la connexion - persiste pendant la navigation -->
  <Teleport to="body">
    <FullPageSpinner v-if="isLoggingIn" />
  </Teleport>

  <Modal
    :is-open="isOpen"
    title="Connexion"
    subtitle="Content de te revoir ! Connecte-toi pour retrouver tes chapitres et tes progrès."
    :icon="ArrowRightOnRectangleIcon"
    size="small"
    @close="handleClose"
  >
    <!-- Login Form -->
    <DynamicForm
      :field-names="fieldNames"
      :get-field-config="getFieldConfig"
      :form-data="formData"
      :is-submitting="isSubmitting"
      :is-valid="isValid"
      :get-field-error="getFieldError"
      :set-field-touched="setFieldTouched"
      :submit-text="config.submitText"
      @submit="handleFormSubmit"
      @field-input="handleInput"
    >
      <!-- Custom Form Content -->
      <template #form-content>
        <div class="form-options">
          <button
            type="button"
            class="om-link forgot-password-btn"
            @click="handleForgotPassword"
          >
            Mot de passe oublié ?
          </button>
        </div>
        <p
          v-if="loginErrorMessage"
          class="om-alert om-alert--error"
          role="alert"
          aria-live="assertive"
        >
          {{ loginErrorMessage }}
        </p>
      </template>
    </DynamicForm>

    <p class="om-divider">ou</p>

    <!-- Social Login -->
    <div class="social-btn-group">
      <button
        v-for="provider in socialProviders"
        :key="provider.key"
        type="button"
        :class="['om-btn om-btn--ghost om-btn--block social-btn', provider.btnClass]"
        @click="() => handleSocialLogin(provider.key)"
        :disabled="isSubmitting || (provider.key === 'google' && isGoogleLoading)"
      >
        <img :src="provider.icon" alt="" class="social-icon" />
        {{ provider.label }}
      </button>
    </div>

    <p class="switch-account">
      Pas encore de compte ?
      <button
        type="button"
        class="om-link" data-cta-name="signup" data-cta-location="modal"
        @click="handleSignUp"
      >
        Créer un compte gratuit
      </button>
    </p>
  </Modal>
</template>

<script>
import { useAuthForm } from '@/composables/useAuthForms'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import Modal from '@/components/common/Modal.vue'
import DynamicForm from '@/components/forms/DynamicForm.vue'
import FullPageSpinner from '@/components/common/FullPageSpinner.vue'
import { socialProviders } from '@/config/socialProviders'
import { loginUser, mapLoginFormToPayload } from '@/api'
import { useRouter } from 'vue-router'
import { ref, onMounted, nextTick, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useGoogleAuth } from '@/composables/useGoogleAuth'
import { useToast } from '@/composables/useToast'
import * as analytics from '@/services/analytics'
import { ArrowRightOnRectangleIcon } from '@heroicons/vue/24/outline'

export default {
  name: 'LoginModal',
  components: {
    Modal,
    DynamicForm,
    FullPageSpinner
  },
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close', 'login', 'signup', 'forgot-password'],
  setup(props, { emit }) {
    const router = useRouter()
    const userStore = useUserStore()
    const { error: showErrorToast } = useToast()
    const { closeModal } = useModalManager()
    const { setupGoogleSignIn, signInWithGoogle, isGoogleLoading } = useGoogleAuth()

    const {
      config,
      formData,
      isSubmitting,
      isValid,
      getFieldError,
      setFieldTouched,
      submitForm,
      getFieldConfig,
      getFieldNames,
      setFieldError
    } = useAuthForm('LOGIN')

    // Get field names for the form
    const fieldNames = getFieldNames()

    const loginError = ref('')
    const loginErrorMessage = computed(() => (loginError.value || '').trim())
    const isLoggingIn = ref(false) // Contrôle du spinner global pendant toute l'opération

    const invalidCredentialsKeywords = [
      'mot de passe incorrect',
      'mot de passe incorect',
      'mot de passe invalide',
      'identifiant incorrect',
      'identifiants incorrects',
      'identifiants invalides',
      'email ou mot de passe',
      'wrong password',
      'invalid credentials',
      'unauthorized',
      'non autorise',
      'authentification invalide'
    ]

    const verificationKeywords = [
      'verification',
      'verifie',
      'unverified',
      'non verifie',
      'activate',
      'activation',
      'inactive',
      'non active',
      'desactive'
    ]

    const userNotFoundKeywords = [
      'utilisateur introuvable',
      'compte introuvable',
      'aucun compte',
      'no active account',
      'not found',
      'email introuvable'
    ]

    // Initialiser Google Sign-In et pré-remplir si "Se souvenir" est actif
    onMounted(async () => {
      await setupGoogleSignIn()

      try {
        const raw = localStorage.getItem('remember_me')
        if (raw) {
          const parsed = JSON.parse(raw)
          const now = Date.now()
          if (parsed?.expiresAt && now < parsed.expiresAt && parsed?.email && parsed?.password) {
            formData.email = parsed.email
            formData.password = parsed.password
            formData.rememberMe = true
          } else if (parsed?.expiresAt && now >= parsed.expiresAt) {
            localStorage.removeItem('remember_me')
          }
        }
      } catch (_) {
        // ignore parsing errors
      }
    })

    // Methods
    const handleClose = () => {
      loginError.value = ''
      setFieldError('password', '')
      setFieldError('email', '')
      emit('close')
    }

    const handleInput = ({ fieldName } = {}) => {
      loginError.value = ''
      if (fieldName === 'password') {
        setFieldError('password', '')
      } else if (fieldName === 'email') {
        setFieldError('email', '')
      }
    }

    const ensureCredentialsPresence = () => {
      const missing = []
      const emailEmpty = !formData.email || !formData.email.trim()
      const passwordEmpty = !formData.password || !formData.password.toString().trim()

      if (emailEmpty) {
        setFieldTouched('email')
        setFieldError('email', 'Veuillez renseigner votre email.')
        missing.push('email')
      }

      if (passwordEmpty) {
        setFieldTouched('password')
        setFieldError('password', 'Veuillez renseigner votre mot de passe.')
        missing.push('mot de passe')
      }

      if (missing.length) {
        loginError.value = missing.length === 2
          ? 'Veuillez renseigner votre email et votre mot de passe.'
          : `Veuillez renseigner votre ${missing[0]}.`
        return false
      }

      return true
    }

    const extractMessageFromData = (data) => {
      if (!data) return ''

      if (typeof data === 'string') {
        return data
      }

      if (Array.isArray(data)) {
        for (const item of data) {
          const nested = extractMessageFromData(item)
          if (nested) return nested
        }
        return ''
      }

      if (typeof data === 'object') {
        if (data.detail) return extractMessageFromData(data.detail)
        if (data.message) return extractMessageFromData(data.message)
        if (data.error) return extractMessageFromData(data.error)
        if (data.error_message) return extractMessageFromData(data.error_message)
        if (Array.isArray(data.non_field_errors)) {
          const msg = extractMessageFromData(data.non_field_errors[0])
          if (msg) return msg
        }
        if (Array.isArray(data.errors)) {
          const msg = extractMessageFromData(data.errors[0])
          if (msg) return msg
        }
        for (const value of Object.values(data)) {
          const nested = extractMessageFromData(value)
          if (nested) return nested
        }
      }

      return ''
    }

    const normalizeText = (text) => {
      if (!text) return ''
      try {
        return text
          .toString()
          .trim()
          .toLowerCase()
          .normalize('NFD')
          .replace(/[\u0300-\u036f]/g, '')
      } catch (_) {
        return text.toString().trim().toLowerCase()
      }
    }

    const containsAny = (value, keywords) =>
      !!value && keywords.some(keyword => value.includes(keyword))

    const mapLoginErrorMessage = (error) => {
      const status = error?.response?.status
      const messageFromPayload = extractMessageFromData(error?.response?.data)
      const primaryMessage = (typeof messageFromPayload === 'string' ? messageFromPayload.trim() : '') || ''
      const fallbackMessage = primaryMessage || error?.response?.statusText || error?.message || ''
      const normalized = normalizeText(fallbackMessage)

      if (status === 0 || error?.code === 'ERR_NETWORK') {
        return 'Connexion impossible. Vérifiez votre connexion internet et réessayez.'
      }

      if (primaryMessage) {
        return primaryMessage
      }

      if (status === 400 || status === 401) {
        if (containsAny(normalized, invalidCredentialsKeywords) || status === 401) {
          return 'Email ou mot de passe incorrect. Veuillez réessayer.'
        }

        if (containsAny(normalized, verificationKeywords)) {
          return 'Votre compte nécessite une vérification. Consultez vos emails ou contactez le support.'
        }

        if (normalized.includes('already') || normalized.includes('exists') || normalized.includes('registered')) {
          return 'Cet utilisateur existe déjà. Si vous ne connaissez pas votre mot de passe, utilisez "Mot de passe oublié ?".'
        }

        if (containsAny(normalized, userNotFoundKeywords)) {
          return 'Aucun compte ne correspond à cet email. Vérifiez l\'adresse ou créez un compte.'
        }
      }

      if (status === 404 || containsAny(normalized, userNotFoundKeywords)) {
        return 'Aucun compte ne correspond à cet email. Vérifiez l\'adresse ou créez un compte.'
      }

      if (containsAny(normalized, verificationKeywords)) {
        return 'Votre compte nécessite une vérification. Consultez vos emails ou contactez le support.'
      }

      if (containsAny(normalized, invalidCredentialsKeywords) && !primaryMessage) {
        return 'Email ou mot de passe incorrect. Veuillez réessayer.'
      }

      return primaryMessage || 'Impossible de vous connecter pour le moment. Veuillez réessayer dans quelques instants.'
    }

    const handleFormSubmit = async () => {
      loginError.value = ''

      // Vérifier d'abord que les identifiants sont renseignés avant d'appeler l'API
      if (!ensureCredentialsPresence()) {
        return
      }

      await submitForm(processLogin)
    }

    const processLogin = async (data) => {
      const payload = mapLoginFormToPayload(data)

      try {
        const response = await loginUser(payload)
        
        // Debug en dev uniquement
        if (import.meta.env.DEV) {
          console.debug('🔑 Réponse login complète:', response.data)
        }

        // Vérifier la structure de la réponse - les tokens sont dans response.data.data
        const responseData = response.data.data || response.data
        const accessToken = responseData.access
        const refreshToken = responseData.refresh

        if (!accessToken || !refreshToken) {
          if (import.meta.env.DEV) {
            console.debug('❌ Tokens manquants dans la réponse:', response.data)
          }
          throw new Error('Tokens d\'authentification manquants')
        }

        // Stocker le token JWT dans localStorage
        localStorage.setItem('access_token', accessToken)
        localStorage.setItem('refresh_token', refreshToken)

        if (import.meta.env.DEV) {
          console.debug('💾 Tokens sauvegardés:', {
            access: accessToken.substring(0, 20) + '...',
            refresh: refreshToken.substring(0, 20) + '...'
          })
        }

        // Enregistrer les identifiants si "Se souvenir de moi" est coché (30 jours)
        try {
          if (data.rememberMe) {
            const payloadToRemember = {
              email: data.email,
              password: data.password,
              expiresAt: Date.now() + 30 * 24 * 60 * 60 * 1000
            }
            localStorage.setItem('remember_me', JSON.stringify(payloadToRemember))
          } else {
            localStorage.removeItem('remember_me')
          }
        } catch (_) {}

        // IMPORTANT: Charger le profil pour mettre à jour isAuthenticated
        await userStore.fetchUser()

        analytics.login('email_password')
        if (userStore.id) analytics.setUserId(userStore.id)

        if (import.meta.env.DEV) {
          console.debug('✅ Utilisateur chargé, état authentifié:', userStore.isAuthenticated)
        }

        // Fermer le modal AVANT la redirection
        emit('login', { email: data.email })
        handleClose()
        closeModal(MODAL_IDS.LOGIN)

        await nextTick()

        // Double vérification de l'état d'authentification
        const finalAuthState = userStore.isAuthenticated
        if (import.meta.env.DEV) {
          console.debug('🔍 État final avant redirection:', { isAuthenticated: finalAuthState })
        }

        if (finalAuthState) {
          if (import.meta.env.DEV) {
            console.debug('🚀 Redirection vers le dashboard...')
          }

          // Activer les spinners (local + global App.vue) uniquement au moment de la redirection
          isLoggingIn.value = true
          // Assurer le spinner global pendant la transition
          userStore.isLoading = true

          // Redirection avec remplacements d'historique (évite l'état Home précédent)
          await router.replace('/dashboard')

          // S'assurer que la vue est montée
          await nextTick()

          // Attendre un court délai pour laisser les requêtes initiales se terminer
          // (peut être ajusté au besoin)
          await new Promise(resolve => setTimeout(resolve, 2000))

          // Désactiver les spinners (local + global App.vue)
          isLoggingIn.value = false
          userStore.isLoading = false
        } else {
          if (import.meta.env.DEV) {
            console.debug('❌ Erreur: isAuthenticated est false après fetchUser')
          }
          // Fallback: recharger la page
          window.location.href = '/dashboard'
        }
      } catch (error) {
        // Ne pas bruiter la console pour les erreurs d'auth attendues
        if (import.meta.env.DEV) {
          console.debug('Erreur lors de la connexion:', error)
        }
        // Gestion de l'erreur backend : DRF renvoie généralement 'detail'
        const friendlyMessage = mapLoginErrorMessage(error)
        const normalizedFriendly = normalizeText(friendlyMessage)
        const isInvalidCredentials =
          containsAny(normalizedFriendly, invalidCredentialsKeywords) || error?.response?.status === 401
        const isUserNotFound =
          containsAny(normalizedFriendly, userNotFoundKeywords) || error?.response?.status === 404

        if (isInvalidCredentials) {
          setFieldTouched('password')
          setFieldError('password', friendlyMessage)
          // Nettoyer une éventuelle erreur e-mail si posée précédemment
          setFieldError('email', '')
        } else if (isUserNotFound) {
          setFieldTouched('email')
          setFieldError('email', friendlyMessage)
          // Nettoyer une éventuelle erreur password si posée précédemment
          setFieldError('password', '')
        }

        loginError.value = friendlyMessage

        if (!isInvalidCredentials && !isUserNotFound) {
          showErrorToast(friendlyMessage)
        }

        return false
      }
    }

    const handleSocialLogin = (provider) => {
      if (provider === 'google') {
        signInWithGoogle()
      } else {
        emit('login', { provider })
      }
    }

    const handleSignUp = () => {
      emit('signup')
    }

    const handleForgotPassword = () => {
      emit('forgot-password')
    }

    return {
      ArrowRightOnRectangleIcon,
      // Form configuration
      config,
      fieldNames,
      socialProviders,

      // Form data
      formData,
      isSubmitting: computed(() => isSubmitting.value || isLoggingIn.value), // Combiner les deux spinners
      isValid,
      isGoogleLoading,
      isLoggingIn,

      // Methods
      getFieldError,
      setFieldTouched,
      getFieldConfig,
      handleClose,
      handleFormSubmit,
      handleSocialLogin,
      handleSignUp,
      handleForgotPassword,
      loginError,
      loginErrorMessage,
      handleInput
    }
  }
}
</script>

<style scoped>
/* Éléments communs (.om-btn, .om-link, .om-divider, .om-alert) : components/common/Modal.vue */
.form-options {
  display: flex;
  justify-content: flex-end;
  margin-top: -6px;
  font-size: 14px;
}

.social-btn-group {
  display: grid;
  gap: 10px;
}

.social-icon {
  width: 20px;
  height: 20px;
}

.switch-account {
  margin: 22px 0 0;
  color: var(--om-muted);
  font-size: 14.5px;
  text-align: center;
}
</style>
