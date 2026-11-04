<template>
  <Modal
    :is-open="isOpen"
    :title="isSuccess ? 'E-mail envoyé' : 'Mot de passe oublié'"
    :subtitle="isSuccess ? '' : 'Indique ton adresse e-mail : tu recevras un lien pour choisir un nouveau mot de passe.'"
    :icon="isSuccess ? EnvelopeOpenIcon : KeyIcon"
    size="small"
    @close="handleClose"
  >
    <!-- E-mail envoyé -->
    <div v-if="isSuccess" class="success-state">
      <p class="om-alert om-alert--success">
        Nous avons envoyé un lien de réinitialisation à <strong>{{ formData.email }}</strong>.
        Pense à regarder dans les courriers indésirables.
      </p>
      <div class="success-actions">
        <button type="button" class="om-btn om-btn--primary" @click="handleClose">Fermer</button>
        <button type="button" class="om-btn om-btn--ghost" @click="handleResend">Renvoyer l’e-mail</button>
      </div>
    </div>

    <!-- Formulaire -->
    <div v-else>
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
      <p class="back-to-login">
        <button type="button" class="om-link" @click="handleBackToLogin">
          <ArrowLeftIcon aria-hidden="true" />
          Retour à la connexion
        </button>
      </p>
    </div>
  </Modal>
</template>

<script>
import { ref } from 'vue'
import { useAuthForm } from '@/composables/useAuthForms'
import Modal from '@/components/common/Modal.vue'
import DynamicForm from '@/components/forms/DynamicForm.vue'
import { requestPasswordReset } from '@/api/auth'
import { ArrowLeftIcon, EnvelopeOpenIcon, KeyIcon } from '@heroicons/vue/24/outline'

export default {
  name: 'ForgotPasswordModal',
  components: {
    Modal,
    DynamicForm,
    ArrowLeftIcon
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
          // Call backend to send reset email
          await requestPasswordReset({ email: data.email })
          
          // Emit forgot password event with form data
          emit('forgot-password', { ...data })
          
          // Show success state
          isSuccess.value = true
        },
        (error) => {
          console.error('Forgot password error:', error)
        }
      )

      if (!success) { /* handled in composable */ }
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
      EnvelopeOpenIcon,
      KeyIcon,
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

<style scoped>
/* Éléments communs (.om-btn, .om-link, .om-alert) : components/common/Modal.vue */
.success-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 20px;
}

.success-actions .om-btn {
  flex: 1 1 160px;
}

.back-to-login {
  margin: 20px 0 0;
  text-align: center;
  font-size: 14.5px;
}

.back-to-login .om-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.back-to-login svg {
  width: 18px;
  height: 18px;
}
</style>
