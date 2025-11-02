<template>
  <DashboardLayout>
    <div class="account-page">
      <h2 class="account-title">
        <span class="account-title-icon"> <component :is="icon" class="account-icon dark-blue-icon" /> </span>
        Mes Coordonnées
      </h2>

      <!-- Configuration Pays/Niveau -->
      <div class="config-section">
        <UserPaysNiveauConfig />
      </div>

      <form class="account-form" @submit.prevent="handleSubmit">
        <div class="account-fields-row">
          <FormSelect
            label="Civilité"
            v-model="form.civilite"
            :options="[
              { value: '', label: '--' },
              { value: 'M', label: 'Monsieur' },
              { value: 'Mme', label: 'Madame' }
            ]"
            autocomplete="honorific-prefix"
            class="account-input"
          />
          <FormInput label="Prénom" v-model="form.firstName" id="firstName" required autocomplete="given-name" class="account-input" placeholder="Prénom" />
          <FormInput label="Nom" v-model="form.lastName" id="lastName" required autocomplete="family-name" class="account-input" placeholder="Nom" />
        </div>
        <div class="account-fields-row">
          <div class="account-field field-wide">
            <label class="account-label" for="email">Email</label>
            <div class="email-row">
              <input class="account-input" id="email" type="email" :value="form.email" disabled autocomplete="email" placeholder="Email" />
              <button
                v-if="!userStoreIsActive"
                type="button"
                class="verify-btn"
                :disabled="isSendingVerification || resendCooldown>0"
                @click="sendVerificationLink"
              >
                {{ resendCooldown>0 ? `Lien envoyé (${resendCooldown}s)` : (isSendingVerification ? 'Envoi...' : 'Envoyer le lien') }}
              </button>
              <span v-else class="verified-badge">✔️ Vérifié</span>
            </div>
            <p v-if="!userStoreIsActive" class="verify-hint">
              Cliquez sur « Envoyer le lien » pour recevoir un email de vérification.
            </p>
            <p v-if="verificationSuccess" class="verify-success">{{ verificationSuccess }}</p>
            <p v-if="verificationError" class="verify-error">{{ verificationError }}</p>
          </div>
          <FormInput label="Numéro de téléphone" v-model="form.telephone" id="telephone" type="tel" autocomplete="tel" class="account-input field-narrow" placeholder="Numéro de téléphone" />
        </div>
        <div class="account-fields-row">
          <div class="account-field">
            <label for="date_naissance" class="account-label">Date de naissance</label>
            <VueDatePicker
              v-model="form.date_naissance"
              model-type="yyyy-MM-dd"
              format="dd/MM/yyyy"
              :enable-time-picker="false"
              :week-start="1"
              locale="fr"
              :max-date="new Date()"
              input-class-name="account-input"
              :clearable="false"
              :hide-input-icon="true"
              :teleport="true"
              autocomplete="bday"
              placeholder="jj/mm/aaaa"
            />
          </div>
        </div>
        <div class="account-actions">
          <button class="account-save-btn" type="submit" :disabled="isSaving">
            {{ isSaving ? 'Sauvegarde...' : 'Sauvegarder' }}
          </button>
          <span v-if="successMsg" class="account-success">{{ successMsg }}</span>
          <span v-if="errorMsg" class="account-error">{{ errorMsg }}</span>
        </div>
      </form>

      <section class="password-card">
        <h3 class="password-title">Sécurité</h3>
        <p class="password-subtitle">Mettez à jour votre mot de passe pour protéger votre compte.</p>
        <form class="password-form" @submit.prevent="handlePasswordSubmit">
          <div class="password-fields">
            <div class="password-field">
              <FormInput
                label="Nouveau mot de passe"
                type="password"
                v-model="passwordForm.newPassword"
                autocomplete="new-password"
                required
                :error="passwordErrors.newPassword"
                placeholder="Nouveau mot de passe"
              />
              <PasswordStrength class="password-strength-hints" :password="passwordForm.newPassword" />
            </div>
            <div class="password-field">
              <FormInput
                label="Confirmer le nouveau mot de passe"
                type="password"
                v-model="passwordForm.confirmPassword"
                autocomplete="new-password"
                required
                :error="passwordErrors.confirmPassword"
                placeholder="Confirmez le nouveau mot de passe"
              />
            </div>
          </div>
          <div class="password-actions">
            <button class="account-save-btn password-save-btn" type="submit" :disabled="isChangingPassword">
              {{ isChangingPassword ? 'Mise à jour...' : 'Mettre à jour le mot de passe' }}
            </button>
            <span v-if="passwordSuccess" class="account-success">{{ passwordSuccess }}</span>
            <span v-if="passwordError" class="account-error">{{ passwordError }}</span>
          </div>
        </form>
      </section>
    </div>
  </DashboardLayout>

</template>

<script setup>
import { ref, onMounted, computed, onBeforeUnmount } from 'vue'
import { useUserStore } from '@/stores/user'
import { updateUserProfile, fetchUserProfile, sendEmailVerificationLink, changeUserPassword } from '@/api'
import FormInput from '@/components/forms/FormInput.vue'
import FormSelect from '@/components/forms/FormSelect.vue'
import { UserCircleIcon } from '@heroicons/vue/24/outline'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import UserPaysNiveauConfig from '@/components/dashboard/UserPaysNiveauConfig.vue'
import VueDatePicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'
import PasswordStrength from '@/components/forms/PasswordStrength.vue'
import { useRoute, useRouter } from 'vue-router'

const icon = UserCircleIcon
const userStore = useUserStore()
const route = useRoute()
const router = useRouter()

const form = ref({
  civilite: '',
  firstName: '',
  lastName: '',
  email: '',
  telephone: '',
  date_naissance: ''
})

const defaultPasswordState = () => ({
  newPassword: '',
  confirmPassword: ''
})

const defaultPasswordErrorsState = () => ({
  newPassword: '',
  confirmPassword: ''
})

const passwordForm = ref(defaultPasswordState())
const passwordErrors = ref(defaultPasswordErrorsState())
const isChangingPassword = ref(false)
const passwordSuccess = ref('')
const passwordError = ref('')

const isSaving = ref(false)
const successMsg = ref('')
const errorMsg = ref('')

// Email verification state
const isSendingVerification = ref(false)
const verificationSuccess = ref('')
const verificationError = ref('')
const resendCooldown = ref(0)
const userStoreIsActive = computed(() => Boolean(userStore?.emailVerified))

const fillForm = (user) => {
  // Backend expects 'M' or 'Mme'. If older human-readable value slipped in, map it.
  const civ = user.civilite || ''
  form.value.civilite = civ === 'Monsieur' ? 'M' : civ === 'Madame' ? 'Mme' : civ
  form.value.firstName = user.firstName || user.first_name || ''
  form.value.lastName = user.lastName || user.last_name || ''
  form.value.email = user.email || ''
  form.value.telephone = user.telephone || ''
  form.value.date_naissance = user.date_naissance || ''
}

onMounted(async () => {
  if (!userStore.firstName || !userStore.lastName) {
    await userStore.fetchUser()
  }
  fillForm(userStore)
  try {
    const { data } = await fetchUserProfile()
    // API returns { success, message, data: { ...user } }
    fillForm((data && data.data) ? data.data : data)
  } catch {}
  await handleEmailVerifiedQuery()
})

const handleSubmit = async () => {
  isSaving.value = true
  successMsg.value = ''
  errorMsg.value = ''
  
  try {
    const payload = {
      civilite: form.value.civilite,
      first_name: form.value.firstName,
      last_name: form.value.lastName,
      telephone: form.value.telephone,
      date_naissance: form.value.date_naissance
    }
    
    // Nettoyer les champs vides
    Object.keys(payload).forEach(key => {
      if (payload[key] === '' || payload[key] === null || payload[key] === undefined) {
        payload[key] = null
      }
    })
    
    const response = await updateUserProfile(payload)
    successMsg.value = 'Profil mis à jour avec succès !'
    // Recharger depuis la réponse (plus rapide) puis synchroniser le store
    if (response && response.data) {
      const userPayload = response.data.data || response.data
      if (userPayload) fillForm(userPayload)
    }
    await userStore.fetchUser()
  } catch (e) {
    console.error('Erreur mise à jour profil:', e)
    
    // Gérer les erreurs de validation
    if (e.response && e.response.data && e.response.data.errors) {
      const errors = e.response.data.errors
      const errorMessages = Object.values(errors).join(', ')
      errorMsg.value = `Erreurs de validation: ${errorMessages}`
    } else if (e.response && e.response.data && e.response.data.error) {
      errorMsg.value = e.response.data.error
    } else {
      errorMsg.value = "Erreur lors de la sauvegarde. Veuillez réessayer."
    }
  } finally {
    isSaving.value = false
  }
}

const resetPasswordForm = () => {
  passwordForm.value = defaultPasswordState()
}

const clearPasswordErrors = () => {
  passwordErrors.value = defaultPasswordErrorsState()
}

const formatErrorMessages = (value) => {
  if (Array.isArray(value)) return value.join(', ')
  if (typeof value === 'string') return value
  return ''
}

const handlePasswordSubmit = async () => {
  passwordSuccess.value = ''
  passwordError.value = ''
  clearPasswordErrors()

  const localErrors = {}
  if (!passwordForm.value.newPassword) {
    localErrors.newPassword = 'Veuillez choisir un nouveau mot de passe.'
  }
  if (!passwordForm.value.confirmPassword) {
    localErrors.confirmPassword = 'Veuillez confirmer votre nouveau mot de passe.'
  }
  if (
    passwordForm.value.newPassword &&
    passwordForm.value.confirmPassword &&
    passwordForm.value.newPassword !== passwordForm.value.confirmPassword
  ) {
    localErrors.confirmPassword = 'La confirmation ne correspond pas au nouveau mot de passe.'
  }

  if (Object.keys(localErrors).length > 0) {
    passwordErrors.value = { ...defaultPasswordErrorsState(), ...localErrors }
    passwordError.value = 'Veuillez corriger les erreurs ci-dessus.'
    return
  }

  try {
    isChangingPassword.value = true
    await changeUserPassword({
      new_password: passwordForm.value.newPassword,
      confirm_password: passwordForm.value.confirmPassword
    })
    passwordSuccess.value = 'Mot de passe mis à jour avec succès.'
    resetPasswordForm()
  } catch (e) {
    console.error('Erreur changement mot de passe:', e)
    const responseData = e?.response?.data
    const responseErrors = responseData?.errors

    if (responseErrors && typeof responseErrors === 'object') {
      const fieldErrors = defaultPasswordErrorsState()
      if (responseErrors.new_password) {
        fieldErrors.newPassword = formatErrorMessages(responseErrors.new_password)
      }
      if (responseErrors.confirm_password) {
        fieldErrors.confirmPassword = formatErrorMessages(responseErrors.confirm_password)
      }
      passwordErrors.value = fieldErrors

      const nonFieldErrors = responseErrors.non_field_errors || responseErrors.detail
      if (nonFieldErrors) {
        passwordError.value = formatErrorMessages(nonFieldErrors)
      }
    }

    if (!passwordError.value) {
      passwordError.value = responseData?.message || "Erreur lors de la mise à jour du mot de passe. Veuillez réessayer."
    }
  } finally {
    isChangingPassword.value = false
  }
}

let resendInterval = null

const sendVerificationLink = async () => {
  if (resendCooldown.value > 0 || isSendingVerification.value) return

  verificationError.value = ''
  verificationSuccess.value = ''

  try {
    isSendingVerification.value = true
    const response = await sendEmailVerificationLink()
    verificationSuccess.value = response?.data?.message || 'Lien de vérification envoyé. Vérifiez votre boîte mail.'
    startResendCooldown()
  } catch (e) {
    verificationError.value = e?.response?.data?.message || 'Impossible d\'envoyer le lien. Réessayez plus tard.'
  } finally {
    isSendingVerification.value = false
  }
}

const startResendCooldown = () => {
  resendCooldown.value = 60
  if (resendInterval) clearInterval(resendInterval)
  resendInterval = setInterval(() => {
    resendCooldown.value -= 1
    if (resendCooldown.value <= 0) {
      resendCooldown.value = 0
      clearInterval(resendInterval)
      resendInterval = null
    }
  }, 1000)
}

const handleEmailVerifiedQuery = async () => {
  const rawStatus = route.query?.email_verified
  const status = Array.isArray(rawStatus) ? rawStatus[0] : rawStatus
  if (status === undefined) return

  if (status === '1') {
    verificationSuccess.value = 'Votre adresse email a été vérifiée avec succès.'
    try {
      await userStore.fetchUser()
    } catch (e) {
      console.error('Erreur lors de la mise à jour du profil après vérification email:', e)
    }
  } else if (status === '0') {
    verificationError.value = 'Lien de vérification invalide ou expiré. Veuillez renvoyer un lien.'
  }

  const newQuery = { ...route.query }
  delete newQuery.email_verified
  router.replace({ query: newQuery }).catch(() => {})
}

onBeforeUnmount(() => {
  if (resendInterval) {
    clearInterval(resendInterval)
    resendInterval = null
  }
})
</script>

<style scoped>
.account-page {
  width: 100%;
  max-width: none;
  margin: 2.5rem 0 0 0;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 16px rgba(30,41,59,0.06);
  padding: 2.2rem 2.5rem 2.5rem 2.5rem;
}
.account-title {
  display: flex;
  align-items: center;
  font-size: 1.35rem;
  font-weight: 700;
  color: #193e8e;
  margin-bottom: 2.2rem;
  gap: 0.7rem;
}
.account-title-icon .account-icon {
  width: 2.1rem;
  height: 2.1rem;
  color: #fbbf24;
}
.config-section {
  margin-bottom: 2rem;
}
.account-form {
  display: flex;
  flex-direction: column;
  gap: 2.2rem;
}
.account-fields-row {
  display: flex;
  gap: 1.2rem;
  margin-bottom: 0.5rem;
}
.account-field {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.account-label {
  font-weight: 900;
  color: #333;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 4px;
}
.account-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 16px;
  background: #fff;
  color: #222;
  transition: border 0.2s;
  margin-bottom: 0;
}
.account-input:focus {
  border-color: #2563eb;
  outline: none;
}
/* widths for email/phone */
.field-wide {
  flex: 2;
}
.field-narrow {
  flex: 1;
}
/* Agrandir le select de civilité */
#civilite.account-input {
  min-width: 160px;
  max-width: 220px;
  height: 48px;
  font-size: 16px;
  padding: 12px 20px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  background: #fff;
  color: #222;
  box-sizing: border-box;
  transition: border 0.2s;
  margin-bottom: 0;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  display: flex;
  align-items: center;
}
#civilite.account-input:focus {
  border-color: #2563eb;
  outline: none;
}
.account-actions {
  display: flex;
  align-items: center;
  gap: 1.2rem;
  margin-top: 1.2rem;
}

/* Email verify UI */
.email-row {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}
.verify-btn {
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 12px;
  font-weight: 700;
  cursor: pointer;
}
.verified-badge {
  color: #16a34a;
  font-weight: 800;
}
.verify-hint { color: #6b7280; font-size: 0.85rem; margin-top: 0.3rem; }
.verify-error { color: #dc2626; font-weight: 600; margin-top: 0.5rem; }
.verify-success { color: #16a34a; font-weight: 600; margin-top: 0.5rem; }
.account-save-btn {
  background: #6366f1;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 12px 32px;
  font-size: 1.08rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
}
.account-save-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
.account-save-btn:hover:not(:disabled) {
  background: #4f46e5;
}
.account-success {
  color: #22c55e;
  font-weight: 600;
}
.account-error {
  color: #ef4444;
  font-weight: 600;
}
.password-card {
  margin-top: 2.5rem;
  padding: 2rem;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  background: #f9fafb;
}
.password-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.4rem;
}
.password-subtitle {
  color: #6b7280;
  margin-bottom: 1.5rem;
}
.password-fields {
  display: flex;
  flex-wrap: wrap;
  gap: 1.2rem;
}
.password-field {
  flex: 1 1 240px;
  min-width: 220px;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}
.password-actions {
  display: flex;
  align-items: center;
  gap: 1.2rem;
  margin-top: 1.5rem;
}
.password-save-btn {
  min-width: 220px;
}
@media (max-width: 900px) {
  .account-page {
    padding: 1.2rem 0.7rem 1.5rem 0.7rem;
  }
  .account-fields-row {
    flex-direction: column;
    gap: 0.7rem;
  }
  .password-card {
    padding: 1.4rem;
  }
  .password-actions {
    flex-direction: column;
    align-items: stretch;
  }
  .password-save-btn {
    width: 100%;
  }
}
.password-strength-hints {
  margin-top: 0;
}
.dark-blue-icon {
  color: #193e8e !important;
}
</style> 
