<template>
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
import { socialProviders } from '@/config/socialProviders'
import { loginUser, mapLoginFormToPayload } from '@/api'
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useGoogleAuth } from '@/composables/useGoogleAuth'

export default {
  name: 'LoginModal',
  components: {
    Modal,
    DynamicForm
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

    // Initialiser Google Sign-In au montage du composant
    onMounted(async () => {
      await setupGoogleSignIn()
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
      const success = await submitForm(processLogin)
      if (!success) {
        return
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

        // Mémoriser les infos utilisateur de base dans Pinia (si disponibles)
        const userData = responseData || response.data
        if (userData.user_id || userData.id) {
          userStore.setUser(userData)
        }
        
        // Récupérer les données complètes de l'utilisateur (y compris le niveau)
        console.log('📡 Récupération du profil utilisateur...')
        await userStore.fetchUser()

        emit('login', { email: data.email })
        handleClose()
        closeModal(MODAL_IDS.LOGIN)
        router.push('/dashboard')
      } catch (error) {
        console.error('Erreur lors de la connexion:', error)
        // Gestion de l'erreur backend : DRF renvoie généralement 'detail'
        const backendMessage = error.response?.data?.detail || error.response?.data?.error
        loginError.value = backendMessage || "Erreur lors de la connexion"
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
      isSubmitting,
      isValid,
      isGoogleLoading,

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

.social-btn.facebook-btn {
  border-color: #1877f2;
  color: #1877f2;

  &:hover:not(:disabled) {
    background: #f0f6ff;
    border-color: #1877f2;
  }
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