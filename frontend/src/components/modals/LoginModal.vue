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
          class="signup-btn"
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
      @input="handleInput"
    >
      <!-- Custom Form Content -->
      <template #form-content>
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
    <div v-if="loginError" class="login-error">{{ loginError }}</div>
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
      getFieldNames
    } = useAuthForm('LOGIN')

    // Get field names for the form
    const fieldNames = getFieldNames()

    const loginError = ref('')
    const isLoggingIn = ref(false) // Contrôle du spinner global pendant toute l'opération

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
      emit('close')
    }

    const handleInput = () => {
      loginError.value = ''
    }

    const handleFormSubmit = async () => {
      // Activer les spinners (local + global App.vue)
      isLoggingIn.value = true
      userStore.isLoading = true

      try {
        const success = await submitForm(processLogin)
        if (!success) {
          // Validation échouée ou erreur déjà gérée
          isLoggingIn.value = false
          userStore.isLoading = false
          return
        }
        // isLoggingIn et userStore.isLoading seront désactivés dans processLogin après redirection
      } catch (error) {
        isLoggingIn.value = false
        userStore.isLoading = false
      }
    }

    const processLogin = async (data) => {
      const payload = mapLoginFormToPayload(data)
      try {
        const response = await loginUser(payload)
        
        console.log('🔑 Réponse login complète:', response.data) // Debug
        
        // Vérifier la structure de la réponse - les tokens sont dans response.data.data
        const responseData = response.data.data || response.data
        const accessToken = responseData.access
        const refreshToken = responseData.refresh
        
        if (!accessToken || !refreshToken) {
          console.error('❌ Tokens manquants dans la réponse:', response.data)
          throw new Error('Tokens d\'authentification manquants')
        }
        
        // Stocker le token JWT dans localStorage
        localStorage.setItem('access_token', accessToken)
        localStorage.setItem('refresh_token', refreshToken)

        console.log('💾 Tokens sauvegardés:', {
          access: accessToken.substring(0, 20) + '...',
          refresh: refreshToken.substring(0, 20) + '...'
        }) // Debug

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
        
        console.log('✅ Utilisateur chargé, état authentifié:', userStore.isAuthenticated)

        // Fermer le modal AVANT la redirection
        emit('login', { email: data.email })
        handleClose()
        closeModal(MODAL_IDS.LOGIN)
        
        // Attendre que tout soit synchronisé
        await nextTick()
        
        // Double vérification de l'état d'authentification
        const finalAuthState = userStore.isAuthenticated
        console.log('🔍 État final avant redirection:', { isAuthenticated: finalAuthState })
        
        if (finalAuthState) {
          console.log('🚀 Redirection vers le dashboard...')

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
          console.error('❌ Erreur: isAuthenticated est false après fetchUser')
          // Fallback: recharger la page
          window.location.href = '/dashboard'
        }
      } catch (error) {
        console.error('Erreur lors de la connexion:', error)
        // Gestion de l'erreur backend : DRF renvoie généralement 'detail'
        const backendMessage = error.response?.data?.detail || error.response?.data?.error
        loginError.value = backendMessage || "Erreur lors de la connexion"
        isLoggingIn.value = false
        userStore.isLoading = false
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

.login-error {
  color: #ef4444;
  margin-top: 10px;
  text-align: center;
  font-weight: 600;
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
