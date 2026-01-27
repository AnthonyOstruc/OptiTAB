<template>
  <!-- Spinner global pour la connexion - persiste pendant la navigation -->
  <Teleport to="body">
    <FullPageSpinner v-if="isLoggingIn" />
  </Teleport>

  <Modal
    :is-open="isOpen"
    title="Connexion"
    size="small"
    @close="handleClose"
  >
    <!-- Sign Up Link moved here -->
    <div class="signup-link signup-link-top">
      <p>
        Pas encore de compte ?
        <button
          type="button"
          class="signup-btn" data-cta-name="signup" data-cta-location="modal"
          @click="handleSignUp"
        >
          Créer un compte
        </button>
      </p>
    </div>

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
        <div
          v-if="loginErrorMessage"
          class="login-error"
          role="alert"
          aria-live="assertive"
        >
          {{ loginErrorMessage }}
        </div>
        <div class="form-options">
          <button
            type="button"
            class="forgot-password-btn"
            @click="handleForgotPassword"
          >
            Mot de passe oublié ?
          </button>
        </div>
      </template>
    </DynamicForm>

    <!-- Divider -->
    <div class="divider">
      <span class="divider-line"></span>
      <span class="divider-text">ou</span>
      <span class="divider-line"></span>
    </div>

    <!-- Social Login -->
    <div class="social-login">
      <div class="social-btn-group">
        <button
          v-for="provider in socialProviders"
          :key="provider.key"
          :class="['social-btn', provider.btnClass]"
          @click="() => handleSocialLogin(provider.key)"
          :disabled="isSubmitting || (provider.key === 'google' && isGoogleLoading)"
        >
          <img :src="provider.icon" :alt="provider.key" class="social-icon" />
          {{ provider.label }}
        </button>
      </div>
    </div>
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

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;

// Form styles
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

// Form options
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
}

.login-error {
  margin: 16px 0 8px;
  padding: 12px 14px;
  border-radius: 10px;
  border: 1px solid #fecaca;
  background: #fef2f2;
  color: #b91c1c;
  font-size: 0.92rem;
  line-height: 1.4;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.checkbox-input {
  width: 16px;
  height: 16px;
  accent-color: $primary-color;
}

.checkbox-text {
  color: $text-color;
}

.forgot-password-btn {
  background: none;
  border: none;
  color: $primary-color;
  text-decoration: none;
  font-weight: 500;
  cursor: pointer;
  font-size: 14px;

  &:hover {
    text-decoration: underline;
  }
}

// Submit button
.login-submit-btn {
  @extend .btn;
  @extend .btn-primary;
  width: 100%;
  padding: 14px 20px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  position: relative;
  min-height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
}

// Divider
.divider {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  margin: 24px 0;
  position: relative;
}

.divider-line {
  flex: 1;
  height: 1px;
  background: #e5e7eb;
  margin: 0 12px;
}

.divider-text {
  background: $white;
  padding: 0 16px;
  color: #6b7280;
  font-size: 14px;
  font-weight: 500;
  z-index: 1;
  position: relative;
}

// Social login
.social-login {
  margin-bottom: 24px;
}

.social-btn-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.social-btn {
  @extend .btn;
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  background: $white;
  color: $text-color;
  border-radius: 8px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  transition: all 0.2s ease;

  &:hover:not(:disabled) {
    background: #f9fafb;
    border-color: #d1d5db;
  }

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
}

.social-btn.google-btn {
  border-color: #e5e7eb;
  color: $text-color;
}

.social-icon {
  width: 20px;
  height: 20px;
}

// Sign up link
.signup-link {
  text-align: center;
  font-size: 14px;
  color: $text-color;

  p {
    margin: 0;
  }
}

.signup-link-top {
  text-align: center;
  margin-bottom: 16px;
  font-size: 14px;
}

.signup-btn {
  background: none;
  border: none;
  color: $primary-color;
  text-decoration: none;
  font-weight: 600;
  cursor: pointer;
  font-size: 14px;

  &:hover {
    text-decoration: underline;
  }
}

// Responsive
@media (max-width: 480px) {
  .form-options {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  .social-btn-group {
    gap: 8px;
  }

  .social-btn {
    padding: 10px 12px;
    font-size: 14px;
  }

  .divider-text {
    font-size: 13px;
  }
}
</style>
