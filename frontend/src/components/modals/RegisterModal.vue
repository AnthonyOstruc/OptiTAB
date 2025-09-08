<template>
  <Modal
    :is-open="isOpen"
    title="Créer un compte"
    size="medium"
    @close="handleClose"
  >
    <!-- Login Link -->
    <div class="login-link login-link-top">
      <p>
        Déjà un compte ?
        <button
          type="button"
          class="login-btn"
          @click="handleLogin"
        >
          Se connecter
        </button>
      </p>
    </div>
    <!-- Top fields: Prénom, Nom -->
    <div class="top-fields">
      <div class="name-fields">
        <FormField
          :field-name="'firstName'"
          :field-config="getFieldConfig('firstName')"
          v-model="formData.firstName"
          :disabled="isSubmitting"
          :get-field-error="getFieldError"
          @blur="handleFieldBlur"
        />
        <FormField
          :field-name="'lastName'"
          :field-config="getFieldConfig('lastName')"
          v-model="formData.lastName"
          :disabled="isSubmitting"
          :get-field-error="getFieldError"
          @blur="handleFieldBlur"
        />
      </div>
    </div>
    <!-- Registration Form -->
    <DynamicForm
      class="register-dynamic-form"
      :field-names="mainFieldNames"
      :get-field-config="getFieldConfig"
      :form-data="formData"
      :is-submitting="isSubmitting"
      :is-valid="isValid"
      :get-field-error="getFieldError"
      :set-field-touched="setFieldTouched"
      :submit-text="config.submitText"
      @submit="handleFormSubmit"
    >
      <template #form-content>
        <!-- Password Strength Indicator -->
        <div v-if="mainFieldNames.includes('password')" class="password-strength-row">
          <PasswordStrength :password="formData.password" />
        </div>
        <!-- Terms and Conditions -->
        <div class="terms-section">
          <FormField
            field-name="acceptTerms"
            :field-config="getFieldConfig('acceptTerms')"
            v-model="formData.acceptTerms"
            :disabled="isSubmitting"
            :get-field-error="getFieldError"
            @blur="handleFieldBlur"
          />
        </div>
        <!-- Newsletter Subscription -->
        <div class="newsletter-section">
          <FormField
            field-name="newsletter"
            :field-config="getFieldConfig('newsletter')"
            v-model="formData.newsletter"
            :disabled="isSubmitting"
            :get-field-error="getFieldError"
            @blur="handleFieldBlur"
          />
        </div>
      </template>
    </DynamicForm>

    <!-- Feedback Message -->
    <div v-if="feedbackMessage" :class="['register-feedback', feedbackType]">
      {{ feedbackMessage }}
    </div>
    <!-- Divider -->
    <div class="divider">
      <span class="divider-line"></span>
      <span class="divider-text">ou</span>
      <span class="divider-line"></span>
    </div>
    <!-- Social Registration -->
    <div class="social-register">
      <div class="social-btn-group">
        <button 
          v-for="provider in socialProviders"
          :key="provider.key"
          :class="['social-btn', provider.btnClass]"
          @click="() => handleSocialRegister(provider.key)"
          :disabled="isSubmitting"
        >
          <img :src="provider.icon" :alt="provider.key" class="social-icon" />
          {{ provider.label }}
        </button>
      </div>
    </div>
  </Modal>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAuthForm } from '@/composables/useAuthForms'
import { registerUser, mapRegisterFormToPayload } from '@/api'
import Modal from '@/components/common/Modal.vue'
import DynamicForm from '@/components/forms/DynamicForm.vue'
import FormField from '@/components/forms/FormField.vue'
import { socialProviders } from '@/config/socialProviders'
import PasswordStrength from '@/components/forms/PasswordStrength.vue'
import { useUserStore } from '@/stores/user'

export default {
  name: 'RegisterModal',
  components: {
    Modal,
    DynamicForm,
    FormField,
    PasswordStrength,
  },
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close', 'register', 'login', 'terms', 'privacy'],
  setup(props, { emit }) {
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
    } = useAuthForm('REGISTER')

    const userStore = useUserStore()

    // Name fields for the top section
    const nameFields = ['firstName', 'lastName']
    // Main fields for DynamicForm (excluding custom layout fields)
    const mainFieldNames = getFieldNames().filter(name => 
      !['firstName', 'lastName', 'acceptTerms', 'newsletter'].includes(name)
    )

    // Feedback message state
    const feedbackMessage = ref('')
    const feedbackType = ref('') // 'success' ou 'error'

    // Méthode pour afficher un message
    function showFeedback(message, type = 'error') {
      feedbackMessage.value = message
      feedbackType.value = type
      setTimeout(() => {
        feedbackMessage.value = ''
        feedbackType.value = ''
      }, 4000)
    }

    // Methods
    const handleClose = () => {
      emit('close')
    }





    
    const handleFormSubmit = async () => {
      // `submitForm` effectue déjà la validation et gère `isSubmitting`.
      const success = await submitForm(processRegistration)

      if (!success) {
        console.log('Form validation failed')
      }
    }
    /**
     * Traite l’inscription après validation du formulaire
     * @param {Object} data - Données issues du composable useAuthForm
     */
    const processRegistration = async (data) => {
      const payload = mapRegisterFormToPayload(data)
      console.log("Payload envoyé au backend :", payload)

      try {
        const response = await registerUser(payload)
        // Si le backend renvoie les infos utilisateur, on les mémorise dans Pinia
        if (response && response.data) {
          userStore.setUser(response.data)
        }
        showFeedback('Compte créé avec succès!', 'success')
        emit('register', { ...payload })
        // Ferme la modale après un court délai pour laisser le message s’afficher
        setTimeout(handleClose, 1200)
      } catch (error) {
        const serverMsg = error.response?.data
          ? Object.entries(error.response.data)
              .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
              .join(' | ')
          : error.message
        console.error('Registration error:', serverMsg)
        showFeedback(serverMsg || 'Erreur lors de la création du compte', 'error')
      }
    }





    const handleFieldBlur = ({ fieldName, event }) => {
      setFieldTouched(fieldName)
    }
    const handleSocialRegister = (providerKey) => {
      emit('register', { provider: providerKey })
    }
    const handleLogin = () => {
      emit('login')
    }
    const handleTermsClick = () => {
      emit('terms')
    }
    const handlePrivacyClick = () => {
      emit('privacy')
    }

    return {
      config,
      formData,
      isSubmitting,
      isValid,
      getFieldError,
      setFieldTouched,
      submitForm,
      getFieldConfig,
      getFieldNames,
      nameFields,
      mainFieldNames,
      socialProviders,
      handleClose,
      handleFormSubmit,
      handleFieldBlur,
      handleSocialRegister,
      handleLogin,
      handleTermsClick,
      handlePrivacyClick,
      feedbackMessage,
      feedbackType,
      showFeedback,
    }
  }
}
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;

.top-fields {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 20px;
}
.name-fields {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.form-label {
  font-weight: 900;
  color: $text-color;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 4px;
}
.required-indicator {
  color: #ef4444 !important;
  font-weight: 700;
}
.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 16px;
  background: $white;
  color: $text-color;
  font-family: inherit;
  height: 48px;
  box-sizing: border-box;
  transition: all 0.2s ease;
}
.form-input::placeholder {
  color: #9ca3af;
  opacity: 1;
  font-size: 16px;
}
@media (max-width: 768px) {
  .name-fields {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
}
.register-dynamic-form {
  .form-fields {
    gap: 20px;
  }
}
// Terms section
.terms-section {
  margin-top: 8px;
}

.newsletter-section {
  margin-top: -8px;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  line-height: 1.5;
}

.checkbox-input {
  width: 16px;
  height: 16px;
  accent-color: $primary-color;
  margin-top: 2px;
  flex-shrink: 0;
}

.checkbox-text {
  color: $text-color;
}

.link-btn {
  background: none;
  border: none;
  color: $primary-color;
  text-decoration: none;
  font-weight: 500;
  cursor: pointer;
  font-size: 14px;
  padding: 0;

  &:hover {
    text-decoration: underline;
  }
}

// Submit button
.register-submit-btn {
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

// Social register
.social-register {
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

// Login link
.login-link {
  text-align: center;
  font-size: 14px;
  color: $text-color;

  p {
    margin: 0;
  }
}

.login-link-top {
  margin-bottom: 18px;
}

.login-btn {
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
@media (max-width: 768px) {
  .name-fields {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .checkbox-label {
    font-size: 13px;
  }
}
.password-strength-row {
  margin-bottom: 10px;
}
.phone-field-top {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}
.form-label {
  font-weight: 900;
  color: $text-color;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 4px;
}
.required-indicator {
  color: #ef4444 !important;
  font-weight: 700;
}
.phone-group {
  margin-top: 0;
}
#register-phone.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 16px;
  background: $white;
  color: $text-color;
  font-family: inherit;
  height: 48px;
  box-sizing: border-box;
  transition: all 0.2s ease;
}
#register-phone.form-input::placeholder {
  color: #9ca3af;
  opacity: 1;
  font-size: 16px;
}
.phone-input {
  max-width: 750px;
  min-width: 0;
  width: 100%;
}
@media (max-width: 768px) {
  .phone-input {
    max-width: 100%;
  }
}
.register-feedback {
  margin: 16px 0 0 0;
  padding: 12px 18px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 15px;
  text-align: center;
}
.register-feedback.error {
  background: #fee2e2;
  color: #b91c1c;
  border: 1px solid #fca5a5;
}
.register-feedback.success {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #86efac;
}
</style> 