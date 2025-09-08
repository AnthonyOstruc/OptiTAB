<template>
  <Modal
    :is-open="isOpen"
    title="Mot de passe oublié"
    size="small"
    @close="handleClose"
  >
    <!-- Success State -->
    <div v-if="isSuccess" class="success-state">
      <div class="success-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
          <polyline points="22,4 12,14.01 9,11.01"/>
        </svg>
      </div>
      
      <h3 class="success-title">Email envoyé !</h3>
      <p class="success-message">
        Nous avons envoyé un lien de réinitialisation à <strong>{{ formData.email }}</strong>
      </p>
      
      <div class="success-actions">
        <button 
          type="button"
          class="btn btn-primary"
          @click="handleClose"
        >
          Fermer
        </button>
        <button 
          type="button"
          class="btn btn-secondary"
          @click="handleResend"
        >
          Renvoyer l'email
        </button>
      </div>
    </div>

    <!-- Form State -->
    <div v-else>
      <!-- Instructions -->
      <div class="instructions">
        <p class="instruction-text">
          Entrez votre adresse email et nous vous enverrons un lien pour réinitialiser votre mot de passe.
        </p>
      </div>

      <!-- Forgot Password Form -->
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
      />

      <!-- Back to Login -->
      <div class="back-to-login">
        <p>
          <button
            type="button"
            class="back-btn"
            @click="handleBackToLogin"
          >
            ← Retour à la connexion
          </button>
        </p>
      </div>
    </div>
  </Modal>
</template>

<script>
import { ref } from 'vue'
import { useAuthForm } from '@/composables/useAuthForms'
import Modal from '@/components/common/Modal.vue'
import DynamicForm from '@/components/forms/DynamicForm.vue'

export default {
  name: 'ForgotPasswordModal',
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
  emits: ['close', 'forgot-password', 'login'],
  setup(props, { emit }) {
    // Success state
    const isSuccess = ref(false)

    // Use the auth form composable
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
      resetForm
    } = useAuthForm('FORGOT_PASSWORD')

    // Get field names for the form
    const fieldNames = getFieldNames()

    // Methods
    const handleClose = () => {
      emit('close')
      // Reset form when closing
      resetForm()
      isSuccess.value = false
    }

    const handleFormSubmit = async () => {
      const success = await submitForm(
        async (data) => {
          // Simulate API call
          await new Promise(resolve => setTimeout(resolve, 1500))
          
          // Emit forgot password event with form data
          emit('forgot-password', { ...data })
          
          // Show success state
          isSuccess.value = true
        },
        (error) => {
          console.error('Forgot password error:', error)
        }
      )

      if (!success) {
        console.log('Form validation failed')
      }
    }

    const handleBackToLogin = () => {
      emit('login')
    }

    const handleResend = async () => {
      isSuccess.value = false
      // Trigger form submission again
      await handleFormSubmit()
    }

    return {
      // State
      isSuccess,
      
      // Form configuration
      config,
      fieldNames,
      
      // Form data
      formData,
      isSubmitting,
      isValid,
      
      // Methods
      getFieldError,
      setFieldTouched,
      getFieldConfig,
      handleClose,
      handleFormSubmit,
      handleBackToLogin,
      handleResend
    }
  }
}
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;

// Instructions
.instructions {
  margin-bottom: 24px;
  text-align: center;
}

.instruction-text {
  color: #6b7280;
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
}

// Success state
.success-state {
  text-align: center;
  padding: 20px 0;
}

.success-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  background: #10b981;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  
  svg {
    width: 32px;
    height: 32px;
  }
}

.success-title {
  font-size: 24px;
  font-weight: 700;
  color: $text-color;
  margin: 0 0 12px;
}

.success-message {
  color: #6b7280;
  font-size: 16px;
  line-height: 1.5;
  margin: 0 0 32px;
  
  strong {
    color: $text-color;
    font-weight: 600;
  }
}

.success-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  
  .btn {
    min-width: 120px;
  }
}

// Back to login
.back-to-login {
  margin-top: 24px;
  text-align: center;
  
  p {
    margin: 0;
  }
}

.back-btn {
  background: none;
  border: none;
  color: $primary-color;
  text-decoration: none;
  font-weight: 500;
  cursor: pointer;
  font-size: 14px;
  display: inline-flex;
  align-items: center;
  gap: 4px;

  &:hover {
    text-decoration: underline;
  }
}

// Responsive
@media (max-width: 480px) {
  .success-actions {
    flex-direction: column;
    
    .btn {
      width: 100%;
    }
  }
  
  .success-icon {
    width: 56px;
    height: 56px;
    
    svg {
      width: 28px;
      height: 28px;
    }
  }
  
  .success-title {
    font-size: 20px;
  }
}
</style> 