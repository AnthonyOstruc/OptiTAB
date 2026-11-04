<template>
  <!-- Spinner global pour la création de compte (mobile: écran figé) -->
  <Teleport to="body">
    <FullPageSpinner v-if="isSubmitting || isGoogleLoading" />
  </Teleport>

  <Modal
    :is-open="isOpen"
    title="Créer un compte"
    subtitle="Gratuit, sans carte bancaire."
    :icon="UserPlusIcon"
    size="medium"
    @close="handleClose"
  >
    <!-- Inscription avec Google -->
    <div class="social-btn-group">
      <button
        v-for="provider in socialProviders"
        :key="provider.key"
        type="button"
        :class="['om-btn om-btn--ghost om-btn--block social-btn', provider.btnClass]"
        @click="() => handleSocialRegister(provider.key)"
        :disabled="isSubmitting || (provider.key === 'google' && isGoogleLoading)"
      >
        <img :src="provider.icon" alt="" class="social-icon" />
        {{ provider.label }}
      </button>
    </div>

    <p class="om-divider">ou avec ton e-mail</p>

    <!-- Prénom, Nom -->
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

    <!-- Formulaire d'inscription -->
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
        <!-- Robustesse du mot de passe -->
        <PasswordStrength v-if="mainFieldNames.includes('password') && formData.password" :password="formData.password" />
        <!-- Conditions et lettre d'information -->
        <div class="consents">
          <FormField
            field-name="acceptTerms"
            :field-config="getFieldConfig('acceptTerms')"
            v-model="formData.acceptTerms"
            :disabled="isSubmitting"
            :get-field-error="getFieldError"
            @blur="handleFieldBlur"
          />
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

    <!-- Message de retour -->
    <p
      v-if="feedbackMessage"
      :class="['om-alert register-feedback', feedbackType === 'success' ? 'om-alert--success' : 'om-alert--error']"
      role="status"
    >
      {{ feedbackMessage }}
    </p>

    <p class="switch-account">
      Déjà un compte ?
      <button type="button" class="om-link" @click="handleLogin">Se connecter</button>
    </p>
  </Modal>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useAuthForm } from '@/composables/useAuthForms'
import { registerUser, mapRegisterFormToPayload } from '@/api'
import Modal from '@/components/common/Modal.vue'
import DynamicForm from '@/components/forms/DynamicForm.vue'
import FormField from '@/components/forms/FormField.vue'
import { socialProviders } from '@/config/socialProviders'
import PasswordStrength from '@/components/forms/PasswordStrength.vue'
import { useUserStore } from '@/stores/user'
import { useGoogleAuth } from '@/composables/useGoogleAuth'
import FullPageSpinner from '@/components/common/FullPageSpinner.vue'
import { UserPlusIcon } from '@heroicons/vue/24/outline'
import * as analytics from '@/services/analytics'

export default {
  name: 'RegisterModal',
  components: {
    Modal,
    DynamicForm,
    FormField,
    PasswordStrength,
    FullPageSpinner
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
    const { setupGoogleSignIn, signInWithGoogle, isGoogleLoading } = useGoogleAuth()

    // Name fields for the top section
    const nameFields = ['firstName', 'lastName']
    // Main fields for DynamicForm (excluding custom layout fields).
    // Un seul champ mot de passe (avec l'œil pour l'afficher) : la confirmation
    // attendue par le serveur est recopiée automatiquement.
    const mainFieldNames = getFieldNames().filter(name =>
      !['firstName', 'lastName', 'confirmPassword', 'acceptTerms', 'newsletter'].includes(name)
    )
    watch(() => formData.password, (motDePasse) => {
      formData.confirmPassword = motDePasse
    })

    // Feedback message state
    const feedbackMessage = ref('')
    const feedbackType = ref('') // 'success' ou 'error'

    // Initialiser Google Sign-In
    onMounted(async () => {
      await setupGoogleSignIn()
    })

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
        // Sauvegarder les tokens si présents, puis mettre à jour le store
        if (response && response.data) {
          const data = response.data?.data || response.data
          const access = data.access
          const refresh = data.refresh
          const registrationEventId = data?.tiktok_event_ids?.complete_registration || ''
          const appUserId = data?.id || data?.user_id || null
          if (access && refresh) {
            localStorage.setItem('access_token', access)
            localStorage.setItem('refresh_token', refresh)
          }
          userStore.setUser(data)
          analytics.completeRegistration('email_password', {
            appUserId,
            eventId: registrationEventId,
          })
        }
        showFeedback('Compte créé avec succès!', 'success')
        emit('register', { ...payload })
        // Ferme la modale après un court délai pour laisser le message s’afficher
        setTimeout(handleClose, 1200)
      } catch (error) {
        const apiData = error.response?.data
        let serverMsg = ''
        if (apiData?.errors && typeof apiData.errors === 'object') {
          const parts = Object.entries(apiData.errors).map(([field, msgs]) => {
            if (Array.isArray(msgs)) return `${field}: ${msgs.join(', ')}`
            if (typeof msgs === 'object' && msgs !== null) {
              const flat = Object.values(msgs).flat()
              return `${field}: ${flat.join(', ')}`
            }
            return `${field}: ${String(msgs)}`
          })
          serverMsg = parts.join(' | ') || apiData.message
        } else if (apiData?.message) {
          serverMsg = apiData.message
        } else {
          serverMsg = error.message
        }
        console.error('Registration error:', serverMsg, apiData?.errors || apiData)
        showFeedback(serverMsg || 'Erreur lors de la création du compte', 'error')
      }
    }





    const handleFieldBlur = ({ fieldName, event }) => {
      setFieldTouched(fieldName)
    }
    const handleSocialRegister = (providerKey) => {
      if (providerKey === 'google') {
        signInWithGoogle()
      } else {
        emit('register', { provider: providerKey })
      }
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
      isGoogleLoading,
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
      UserPlusIcon
    }
  }
}
</script>

<style scoped>
/* Éléments communs (.om-btn, .om-link, .om-divider, .om-alert) : components/common/Modal.vue */
.social-btn-group {
  display: grid;
  gap: 10px;
}

.social-icon {
  width: 20px;
  height: 20px;
}

.name-fields {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-bottom: 18px;
}

.consents {
  display: grid;
  gap: 10px;
  margin: 4px 0 6px;
}

.register-feedback {
  margin-top: 16px;
}

.switch-account {
  margin: 22px 0 0;
  color: var(--om-muted);
  font-size: 14.5px;
  text-align: center;
}

/* Téléphone : fenêtre compacte (prénom et nom restent côte à côte). */
@media (max-width: 640px) {
  .name-fields {
    gap: 10px;
    margin-bottom: 14px;
  }

  .consents {
    gap: 6px;
    margin: 2px 0 4px;
  }

  .switch-account {
    margin-top: 16px;
    font-size: 14px;
  }
}
</style>
