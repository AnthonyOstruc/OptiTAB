<template>
  <DashboardLayout>
    <div class="account-page">
      <!-- Header -->
      <div class="page-header">
        <div class="header-content">
          <div class="header-icon">
            <component :is="UserCircleIcon" />
          </div>
          <div class="header-text">
            <h1 class="page-title">Mon Compte</h1>
            <p class="page-subtitle">Gérez vos informations personnelles et paramètres de sécurité</p>
          </div>
        </div>
      </div>

      <!-- Configuration Pays/Niveau Card -->
      <section class="info-card">
        <div class="card-header">
          <div class="card-header-icon">
            <component :is="GlobeAltIcon" />
          </div>
          <div>
            <h2 class="card-title">Configuration</h2>
            <p class="card-description">Pays et niveau d'études</p>
          </div>
        </div>
        <div class="card-content">
          <UserPaysNiveauConfig />
        </div>
      </section>

      <!-- Informations personnelles Card -->
      <section class="info-card">
        <div class="card-header">
          <div class="card-header-icon">
            <component :is="UserIcon" />
          </div>
          <div>
            <h2 class="card-title">Informations personnelles</h2>
            <p class="card-description">Vos coordonnées et informations de profil</p>
          </div>
        </div>
        
        <form class="card-content" @submit.prevent="handleSubmit">
          <!-- Civilité, Prénom, Nom -->
          <div class="form-grid">
            <FormSelect
              label="Civilité"
              v-model="form.civilite"
              :options="[
                { value: '', label: '--' },
                { value: 'M', label: 'Monsieur' },
                { value: 'Mme', label: 'Madame' }
              ]"
              autocomplete="honorific-prefix"
              class="form-field"
            />
            <FormInput 
              label="Prénom" 
              v-model="form.firstName" 
              id="firstName" 
              required 
              autocomplete="given-name" 
              placeholder="Votre prénom"
              class="form-field"
            />
            <FormInput 
              label="Nom" 
              v-model="form.lastName" 
              id="lastName" 
              required 
              autocomplete="family-name" 
              placeholder="Votre nom"
              class="form-field"
            />
          </div>

          <!-- Email Section -->
          <div class="form-section">
            <label class="form-label" for="email">
              <component :is="EnvelopeIcon" class="label-icon" />
              Adresse email
            </label>
            <div class="email-container">
              <input 
                class="form-input email-input" 
                id="email" 
                type="email" 
                :value="form.email" 
                disabled 
                autocomplete="email" 
              />
              <button type="button" class="btn-secondary" @click="openEmailChangeModal">
                <component :is="PencilSquareIcon" class="btn-icon" />
                Modifier
              </button>
              <button
                v-if="!userStoreIsActive"
                type="button"
                class="btn-primary"
                :disabled="isSendingVerification || resendCooldown>0"
                @click="sendVerificationLink"
              >
                <component :is="ShieldCheckIcon" class="btn-icon" />
                {{ resendCooldown>0 ? `Lien envoyé (${resendCooldown}s)` : (isSendingVerification ? 'Envoi...' : 'Vérifier') }}
              </button>
              <span v-else class="status-badge verified">
                <component :is="CheckBadgeIcon" class="badge-icon" />
                Vérifié
              </span>
            </div>

            <!-- Email Status Messages -->
            <div v-if="!userStoreIsActive || pendingEmailActive || verificationSuccess || verificationError || emailChangeSuccess || emailChangeError" class="email-messages">
              <div v-if="!userStoreIsActive && !verificationSuccess && !verificationError" class="info-message">
                <component :is="InformationCircleIcon" class="message-icon" />
                <span>Cliquez sur « Vérifier » pour recevoir un email de vérification.</span>
              </div>
              <div v-if="pendingEmailActive" class="warning-message">
                <component :is="ExclamationTriangleIcon" class="message-icon" />
                <span>
                  Nouvelle adresse en attente : <strong>{{ userStore.pendingEmail }}</strong><br />
                  Le lien expire dans <strong>{{ pendingEmailCountdownLabel }}</strong>.
                </span>
              </div>
              <div v-if="verificationSuccess" class="success-message">
                <component :is="CheckCircleIcon" class="message-icon" />
                <span>{{ verificationSuccess }}</span>
              </div>
              <div v-if="verificationError" class="error-message">
                <component :is="XCircleIcon" class="message-icon" />
                <span>{{ verificationError }}</span>
              </div>
              <div v-if="emailChangeSuccess" class="success-message">
                <component :is="CheckCircleIcon" class="message-icon" />
                <span>{{ emailChangeSuccess }}</span>
              </div>
              <div v-if="emailChangeError" class="error-message">
                <component :is="XCircleIcon" class="message-icon" />
                <span>{{ emailChangeError }}</span>
              </div>
            </div>
          </div>

          <!-- Téléphone et Date de naissance -->
          <div class="form-grid-2">
            <div class="form-section">
              <label class="form-label" for="telephone">
                <component :is="PhoneIcon" class="label-icon" />
                Numéro de téléphone
              </label>
              <FormInput 
                v-model="form.telephone" 
                id="telephone" 
                type="tel" 
                autocomplete="tel" 
                placeholder="Votre numéro de téléphone"
              />
            </div>
            <div class="form-section">
              <label for="date_naissance" class="form-label">
                <component :is="CalendarIcon" class="label-icon" />
                Date de naissance
              </label>
              <VueDatePicker
                v-model="form.date_naissance"
                model-type="yyyy-MM-dd"
                format="dd/MM/yyyy"
                :enable-time-picker="false"
                :week-start="1"
                locale="fr"
                :max-date="new Date()"
                input-class-name="form-input"
                :clearable="false"
                :hide-input-icon="true"
                :teleport="true"
                autocomplete="bday"
                placeholder="jj/mm/aaaa"
              />
            </div>
          </div>

          <!-- Actions -->
          <div class="form-actions">
            <button class="btn-primary btn-large" type="submit" :disabled="isSaving">
              <component :is="isSaving ? null : CheckIcon" class="btn-icon" />
              {{ isSaving ? 'Sauvegarde en cours...' : 'Enregistrer les modifications' }}
            </button>
            <div v-if="successMsg || errorMsg" class="action-message">
              <span v-if="successMsg" class="success-text">{{ successMsg }}</span>
              <span v-if="errorMsg" class="error-text">{{ errorMsg }}</span>
            </div>
          </div>
        </form>
      </section>

      <!-- Sécurité Card -->
      <section class="info-card">
        <div class="card-header">
          <div class="card-header-icon">
            <component :is="LockClosedIcon" />
          </div>
          <div>
            <h2 class="card-title">Sécurité</h2>
            <p class="card-description">Mettez à jour votre mot de passe pour protéger votre compte</p>
          </div>
        </div>
        
        <form class="card-content" @submit.prevent="handlePasswordSubmit">
          <div class="form-grid-2">
            <div class="form-section">
              <FormInput
                label="Nouveau mot de passe"
                type="password"
                v-model="passwordForm.newPassword"
                autocomplete="new-password"
                required
                :error="passwordErrors.newPassword"
                placeholder="••••••••"
              />
              <PasswordStrength class="password-strength" :password="passwordForm.newPassword" />
            </div>
            <div class="form-section">
              <FormInput
                label="Confirmer le nouveau mot de passe"
                type="password"
                v-model="passwordForm.confirmPassword"
                autocomplete="new-password"
                required
                :error="passwordErrors.confirmPassword"
                placeholder="••••••••"
              />
            </div>
          </div>

          <div class="form-actions">
            <button class="btn-primary btn-large" type="submit" :disabled="isChangingPassword">
              <component :is="isChangingPassword ? null : KeyIcon" class="btn-icon" />
              {{ isChangingPassword ? 'Mise à jour en cours...' : 'Mettre à jour le mot de passe' }}
            </button>
            <div v-if="passwordSuccess || passwordError" class="action-message">
              <span v-if="passwordSuccess" class="success-text">{{ passwordSuccess }}</span>
              <span v-if="passwordError" class="error-text">{{ passwordError }}</span>
            </div>
          </div>
        </form>
      </section>
    </div>
  </DashboardLayout>


  <!-- Modal pour modifier l'email -->
  <div v-if="showEmailChangeModal" class="modal-overlay" @click="closeEmailChangeModal">
    <div class="modal-card" @click.stop>
      <div class="modal-header">
        <h3>Modifier mon email</h3>
        <button class="modal-close" @click="closeEmailChangeModal">×</button>
      </div>
      <div class="modal-body">
        <label class="form-label" for="newEmail">
          <component :is="EnvelopeIcon" class="label-icon" />
          Nouvelle adresse email
        </label>
        <input
          id="newEmail"
          v-model="emailChangeForm.email"
          type="email"
          class="form-input"
          placeholder="nouveau@mail.com"
          autocomplete="email"
        />
        <div v-if="emailChangeError" class="error-message" style="margin-top: 0.5rem;">
          <component :is="XCircleIcon" class="message-icon" />
          <span>{{ emailChangeError }}</span>
        </div>
        <div v-if="emailChangeSuccess" class="success-message" style="margin-top: 0.5rem;">
          <component :is="CheckCircleIcon" class="message-icon" />
          <span>{{ emailChangeSuccess }}</span>
        </div>
      </div>
      <div class="modal-actions">
        <button class="resend-btn" type="button" @click="closeEmailChangeModal">Annuler</button>
        <button class="confirm-btn" type="button" :disabled="isSubmittingEmailChange" @click="submitEmailChange">
          {{ isSubmittingEmailChange ? 'Envoi...' : 'Envoyer le lien' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onBeforeUnmount, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { updateUserProfile, fetchUserProfile, sendEmailVerificationLink, changeUserPassword, requestEmailChange } from '@/api'
import FormInput from '@/components/forms/FormInput.vue'
import FormSelect from '@/components/forms/FormSelect.vue'
import { 
  UserCircleIcon, 
  UserIcon,
  LockClosedIcon, 
  GlobeAltIcon,
  EnvelopeIcon,
  PhoneIcon,
  CalendarIcon,
  CheckIcon,
  KeyIcon,
  PencilSquareIcon,
  ShieldCheckIcon,
  CheckBadgeIcon,
  InformationCircleIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  XCircleIcon
} from '@heroicons/vue/24/outline'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import UserPaysNiveauConfig from '@/components/dashboard/UserPaysNiveauConfig.vue'
import VueDatePicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'
import PasswordStrength from '@/components/forms/PasswordStrength.vue'
import { useRoute, useRouter } from 'vue-router'
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
const pendingEmailActive = computed(() => Boolean(userStore.pendingEmail) && pendingEmailSecondsLeft.value > 0)
const pendingEmailCountdownLabel = computed(() => {
  const total = pendingEmailSecondsLeft.value
  const minutes = Math.floor(total / 60)
  const seconds = total % 60
  if (minutes > 0) {
    return `${minutes} min ${seconds.toString().padStart(2, '0')} s`
  }
  return `${seconds} s`
})
const showEmailChangeModal = ref(false)
const isSubmittingEmailChange = ref(false)
const emailChangeForm = ref({ email: '' })
const emailChangeError = ref('')
const emailChangeSuccess = ref('')
const pendingEmailSecondsLeft = ref(0)

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
  await handleEmailChangeQuery()
  refreshPendingEmailTimer()
})

watch(
  () => [userStore.pendingEmail, userStore.pendingEmailRequestedAt],
  () => {
    refreshPendingEmailTimer()
  }
)

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
let pendingEmailInterval = null

const sendVerificationLink = async () => {
  if (resendCooldown.value > 0 || isSendingVerification.value) return

  if (userStore.emailVerified) {
    userStore.emailVerified = false
  }
  verificationError.value = ''
  verificationSuccess.value = ''

  try {
    isSendingVerification.value = true
    const response = await sendEmailVerificationLink()
    const serverMessage = response?.data?.message
    const emailSent = response?.data?.data?.email_sent !== false
    startResendCooldown()

    if (emailSent) {
      verificationSuccess.value = serverMessage || 'Lien de vérification envoyé. Vérifiez votre boîte mail.'
    } else {
      verificationError.value = serverMessage || 'Impossible d\'envoyer le lien. Réessayez plus tard.'
    }
  } catch (e) {
    const status = e?.response?.status
    const serverMessage = e?.response?.data?.message
    if (status === 429) {
      verificationError.value = serverMessage || 'Veuillez patienter une minute avant de renvoyer un lien.'
      startResendCooldown()
    } else {
      verificationError.value = serverMessage || 'Impossible d\'envoyer le lien. Réessayez plus tard.'
    }
  } finally {
    isSendingVerification.value = false
  }
}

const openEmailChangeModal = () => {
  emailChangeForm.value.email = userStore.pendingEmail || ''
  emailChangeSuccess.value = ''
  emailChangeError.value = ''
  showEmailChangeModal.value = true
}

const closeEmailChangeModal = () => {
  showEmailChangeModal.value = false
}

const validateEmailFormat = (email) => {
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return pattern.test(email)
}

const submitEmailChange = async () => {
  emailChangeSuccess.value = ''
  emailChangeError.value = ''
  const newEmail = (emailChangeForm.value.email || '').trim().toLowerCase()

  if (!newEmail) {
    emailChangeError.value = 'Veuillez saisir une nouvelle adresse email.'
    return
  }

  if (!validateEmailFormat(newEmail)) {
    emailChangeError.value = 'Adresse email invalide.'
    return
  }

  if (newEmail === (userStore.email || '').toLowerCase()) {
    emailChangeError.value = 'Veuillez saisir une adresse différente de l\'actuelle.'
    return
  }

  try {
    isSubmittingEmailChange.value = true
    const response = await requestEmailChange(newEmail)
    const emailSent = response?.data?.data?.email_sent !== false
    if (emailSent) {
      emailChangeSuccess.value = 'Un lien de confirmation a été envoyé à votre nouvelle adresse. Vérifiez votre boîte mail.'
    } else {
      emailChangeError.value = response?.data?.message || 'Impossible d\'envoyer le lien. Réessayez plus tard.'
    }
    userStore.emailVerified = false
    userStore.pendingEmail = newEmail
    userStore.pendingEmailRequestedAt = new Date().toISOString()
    showEmailChangeModal.value = false
    verificationError.value = ''
    verificationSuccess.value = ''
    refreshPendingEmailTimer()
  } catch (e) {
    const errors = e?.response?.data?.errors
    const message = e?.response?.data?.message
    if (errors && typeof errors === 'object') {
      const firstKey = Object.keys(errors)[0]
      const val = Array.isArray(errors[firstKey]) ? errors[firstKey][0] : errors[firstKey]
      emailChangeError.value = val || 'Impossible de traiter votre demande.'
    } else {
      emailChangeError.value = message || 'Impossible de traiter votre demande.'
    }
  } finally {
    isSubmittingEmailChange.value = false
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

const stopPendingEmailTimer = () => {
  if (pendingEmailInterval) {
    clearInterval(pendingEmailInterval)
    pendingEmailInterval = null
  }
}

const refreshPendingEmailTimer = () => {
  stopPendingEmailTimer()
  const pendingEmail = userStore.pendingEmail
  const sentAtRaw = userStore.pendingEmailRequestedAt
  if (!pendingEmail || !sentAtRaw) {
    pendingEmailSecondsLeft.value = 0
    return
  }

  const sentAt = new Date(sentAtRaw).getTime()
  if (Number.isNaN(sentAt)) {
    pendingEmailSecondsLeft.value = 0
    return
  }

  const expiresAt = sentAt + 60 * 60 * 1000
  const diff = Math.floor((expiresAt - Date.now()) / 1000)

  if (diff <= 0) {
    pendingEmailSecondsLeft.value = 0
    return
  }

  pendingEmailSecondsLeft.value = diff
  pendingEmailInterval = setInterval(() => {
    pendingEmailSecondsLeft.value -= 1
    if (pendingEmailSecondsLeft.value <= 0) {
      pendingEmailSecondsLeft.value = 0
      stopPendingEmailTimer()
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
    router.push('/dashboard').catch(() => {})
  } else if (status === '0') {
    verificationError.value = 'Lien de vérification invalide ou expiré. Veuillez renvoyer un lien.'
  }

  const newQuery = { ...route.query }
  delete newQuery.email_verified
  router.replace({ query: newQuery }).catch(() => {})
}

const handleEmailChangeQuery = async () => {
  const rawStatus = route.query?.email_change
  const status = Array.isArray(rawStatus) ? rawStatus[0] : rawStatus
  if (status === undefined) return

  if (status === '1') {
    emailChangeSuccess.value = 'Votre adresse email a été mise à jour.'
    try {
      await userStore.fetchUser()
      refreshPendingEmailTimer()
    } catch (e) {
      console.error('Erreur lors du rafraîchissement du profil après changement email:', e)
    }
  } else {
    emailChangeError.value = 'Impossible de confirmer le changement d\'email.'
  }

  const newQuery = { ...route.query }
  delete newQuery.email_change
  router.replace({ query: newQuery }).catch(() => {})
}

onBeforeUnmount(() => {
  if (resendInterval) {
    clearInterval(resendInterval)
    resendInterval = null
  }
  stopPendingEmailTimer()
})
</script>

<style scoped>
/* ============================================
   LAYOUT & STRUCTURE
   ============================================ */

.account-page {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 1rem 4rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* ============================================
   PAGE HEADER
   ============================================ */

.page-header {
  margin-bottom: 1rem;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon {
  width: 3.5rem;
  height: 3.5rem;
  background: linear-gradient(135deg, #667eea 0%, #5a67d8 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  flex-shrink: 0;
  box-shadow: 0 4px 6px -1px rgba(102, 126, 234, 0.2);
}

.header-icon svg {
  width: 2rem;
  height: 2rem;
}

.header-text {
  flex: 1;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.25rem 0;
  line-height: 1.2;
}

.page-subtitle {
  font-size: 0.9375rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.4;
}

/* ============================================
   CARD STRUCTURE
   ============================================ */

.info-card {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: box-shadow 0.2s ease;
}

.info-card:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem 1.75rem;
  background: linear-gradient(to bottom, #f9fafb 0%, #ffffff 100%);
  border-bottom: 1px solid #e5e7eb;
}

.card-header-icon {
  width: 2.5rem;
  height: 2.5rem;
  background: linear-gradient(135deg, #667eea 0%, #5a67d8 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  flex-shrink: 0;
}

.card-header-icon svg {
  width: 1.25rem;
  height: 1.25rem;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.25rem 0;
  line-height: 1.3;
}

.card-description {
  font-size: 0.8125rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.3;
}

.card-content {
  padding: 1.75rem;
}

/* ============================================
   FORM STRUCTURE
   ============================================ */

.form-grid {
  display: grid;
  grid-template-columns: 120px 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.form-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  margin-bottom: 1.5rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.label-icon {
  width: 1.125rem;
  height: 1.125rem;
  color: #667eea;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 16px;
  background: #fff;
  color: #222;
  transition: border 0.2s;
  font-family: inherit;
  margin-bottom: 0;
  height: auto;
  min-height: 48px;
  line-height: 1.5;
  box-sizing: border-box;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}

.form-input:hover:not(:disabled) {
  border-color: #e5e7eb;
}

.form-input:focus {
  border-color: #667eea;
  outline: none;
  box-shadow: none;
}

.form-input:disabled {
  background: #f9fafb;
  color: #6b7280;
  cursor: not-allowed;
  border-color: #e5e7eb;
}

/* ============================================
   EMAIL SECTION
   ============================================ */

.email-container {
  display: flex;
  gap: 0.75rem;
  align-items: stretch;
  flex-wrap: wrap;
}

.email-input {
  flex: 1;
  min-width: 200px;
}

.email-messages {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 0.75rem;
}

.info-message,
.warning-message,
.success-message,
.error-message {
  display: flex;
  align-items: flex-start;
  gap: 0.625rem;
  padding: 0.875rem 1rem;
  border-radius: 10px;
  font-size: 0.875rem;
  line-height: 1.5;
}

.info-message {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  color: #1e40af;
}

.warning-message {
  background: #fef3c7;
  border: 1px solid #fde68a;
  color: #92400e;
}

.success-message {
  background: #ecfdf5;
  border: 1px solid #a7f3d0;
  color: #065f46;
}

.error-message {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
}

.message-icon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
  margin-top: 0.125rem;
}

/* ============================================
   BUTTONS
   ============================================ */

.btn-primary,
.btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  border: none;
  font-family: inherit;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #5a67d8 100%);
  color: #ffffff;
  box-shadow: 0 1px 2px 0 rgba(102, 126, 234, 0.2);
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #5a67d8 0%, #4c5bc4 100%);
  box-shadow: 0 4px 6px -1px rgba(102, 126, 234, 0.3);
  transform: translateY(-1px);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(0);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: #ffffff;
  color: #374151;
  border: 1.5px solid #d1d5db;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.btn-secondary:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #9ca3af;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.08);
}

.btn-large {
  padding: 0.875rem 2rem;
  font-size: 0.9375rem;
}

.btn-icon {
  width: 1.125rem;
  height: 1.125rem;
}

/* ============================================
   STATUS BADGE
   ============================================ */

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 600;
}

.status-badge.verified {
  background: #ecfdf5;
  color: #059669;
  border: 1.5px solid #a7f3d0;
}

.badge-icon {
  width: 1.125rem;
  height: 1.125rem;
}

/* ============================================
   FORM ACTIONS
   ============================================ */

.form-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding-top: 1.5rem;
  border-top: 1px solid #f3f4f6;
  margin-top: 0.5rem;
}

.action-message {
  flex: 1;
}

.success-text {
  color: #059669;
  font-size: 0.875rem;
  font-weight: 500;
}

.error-text {
  color: #dc2626;
  font-size: 0.875rem;
  font-weight: 500;
}

/* ============================================
   PASSWORD STRENGTH
   ============================================ */

.password-strength {
  margin-top: 0.5rem;
}

/* ============================================
   DATE PICKER CUSTOM STYLES
   ============================================ */

/* Wrapper du DatePicker */
:deep(.dp__main) {
  width: 100% !important;
}

:deep(.dp__input_wrap) {
  width: 100% !important;
}

/* Input du DatePicker - identique à .form-input */
:deep(.dp__input),
:deep(.dp__input:enabled),
:deep(.dp__input:not(:disabled)),
:deep(input.dp__input) {
  width: 100% !important;
  padding: 12px 16px !important;
  border: 2px solid #e5e7eb !important;
  border-radius: 8px !important;
  font-size: 16px !important;
  background: #fff !important;
  color: #222 !important;
  transition: border 0.2s !important;
  font-family: inherit !important;
  margin: 0 !important;
  margin-bottom: 0 !important;
  height: 48px !important;
  max-height: 48px !important;
  min-height: 48px !important;
  line-height: 1.5 !important;
  box-sizing: border-box !important;
  appearance: none !important;
  -webkit-appearance: none !important;
  -moz-appearance: none !important;
  vertical-align: middle !important;
}

:deep(.dp__input:hover:not(:disabled)) {
  border-color: #e5e7eb !important;
}

:deep(.dp__input:focus) {
  border-color: #667eea !important;
  outline: none !important;
  box-shadow: none !important;
}

:deep(.dp__input:disabled) {
  background: #f9fafb !important;
  color: #6b7280 !important;
  cursor: not-allowed !important;
  border-color: #e5e7eb !important;
}

/* Cacher les icônes */
:deep(.dp__input_icon),
:deep(.dp__input_icon_pad) {
  display: none !important;
}

:deep(.dp__clear_icon) {
  display: none !important;
}

/* ============================================
   MODAL
   ============================================ */

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(4px);
  animation: fadeIn 0.2s ease;
  overflow-y: auto;
  padding: 2rem 1rem;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-card {
  background: #ffffff;
  border-radius: 20px;
  width: min(90%, 480px);
  max-width: 480px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.15), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  animation: slideUp 0.3s ease;
  max-height: calc(100vh - 4rem);
  display: flex;
  flex-direction: column;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.75rem 1.75rem 1.25rem 1.75rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  color: #111827;
  font-size: 1.25rem;
  font-weight: 700;
}

.modal-close {
  background: #f3f4f6;
  border: none;
  font-size: 1.5rem;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
  line-height: 1;
  padding: 0;
  width: 2rem;
  height: 2rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close:hover {
  background: #e5e7eb;
  color: #374151;
}

.modal-body {
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  flex: 1 1 auto;
  overflow-y: auto;
}

.modal-body .form-label {
  margin-bottom: 0.5rem;
}

.modal-body .form-input {
  width: 100%;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1.25rem 1.75rem 1.75rem 1.75rem;
  border-top: 1px solid #f3f4f6;
}

.resend-btn {
  background: #ffffff;
  color: #374151;
  border: 1.5px solid #d1d5db;
  border-radius: 10px;
  padding: 0.625rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.resend-btn:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #9ca3af;
}

.confirm-btn {
  background: linear-gradient(135deg, #667eea 0%, #5a67d8 100%);
  color: #ffffff;
  border: none;
  border-radius: 10px;
  padding: 0.625rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px 0 rgba(102, 126, 234, 0.2);
}

.confirm-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #5a67d8 0%, #4c5bc4 100%);
  box-shadow: 0 4px 6px -1px rgba(102, 126, 234, 0.3);
}

.confirm-btn:disabled,
.resend-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ============================================
   RESPONSIVE DESIGN
   ============================================ */

@media (max-width: 768px) {
  .account-page {
    padding: 1.5rem 1rem 3rem;
    gap: 1.25rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .page-subtitle {
    font-size: 0.875rem;
  }

  .header-icon {
    width: 3rem;
    height: 3rem;
  }

  .header-icon svg {
    width: 1.75rem;
    height: 1.75rem;
  }

  .card-header {
    padding: 1.25rem 1.25rem;
  }

  .card-content {
    padding: 1.25rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-grid-2 {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .email-container {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
  }

  .email-input {
    min-width: auto;
  }

  .form-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .action-message {
    text-align: center;
  }

  .modal-card {
    border-radius: 16px;
  }

  .modal-header {
    padding: 1.5rem 1.5rem 1rem 1.5rem;
  }

  .modal-body {
    padding: 1.5rem;
  }

  .modal-actions {
    flex-direction: column-reverse;
    padding: 1rem 1.5rem 1.5rem 1.5rem;
  }

  .resend-btn,
  .confirm-btn {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .info-card {
    border-radius: 14px;
  }

  .card-title {
    font-size: 1.0625rem;
  }

  .card-description {
    font-size: 0.8rem;
  }

  .card-header-icon {
    width: 2.25rem;
    height: 2.25rem;
  }

  .card-header-icon svg {
    width: 1.125rem;
    height: 1.125rem;
  }

  .form-label {
    font-size: 0.8125rem;
  }

  .btn-primary,
  .btn-secondary {
    padding: 0.6875rem 1.125rem;
    font-size: 0.875rem;
  }

  .info-message,
  .warning-message,
  .success-message,
  .error-message {
    padding: 0.75rem 0.875rem;
    font-size: 0.8125rem;
  }
}

@media (max-width: 640px) {
  .account-page {
    padding: 1.25rem 0.875rem 2.5rem;
    gap: 1rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .page-subtitle {
    font-size: 0.8125rem;
  }

  .header-icon {
    width: 2.75rem;
    height: 2.75rem;
    border-radius: 14px;
  }

  .header-icon svg {
    width: 1.625rem;
    height: 1.625rem;
  }

  .info-card {
    border-radius: 12px;
  }

  .card-header {
    padding: 1.125rem 1.25rem;
    gap: 0.75rem;
  }

  .card-header-icon {
    width: 2rem;
    height: 2rem;
    border-radius: 10px;
  }

  .card-header-icon svg {
    width: 1rem;
    height: 1rem;
  }

  .card-title {
    font-size: 1rem;
  }

  .card-description {
    font-size: 0.75rem;
  }

  .card-content {
    padding: 1.25rem;
  }

  .form-label {
    font-size: 0.8rem;
  }

  .label-icon {
    width: 1rem;
    height: 1rem;
  }

  .form-input,
  :deep(.dp__input) {
    padding: 11px 14px !important;
    font-size: 15px !important;
    min-height: 46px !important;
    height: 46px !important;
  }

  .btn-primary,
  .btn-secondary {
    padding: 0.65rem 1rem;
    font-size: 0.8125rem;
  }

  .btn-icon {
    width: 1rem;
    height: 1rem;
  }

  .status-badge {
    padding: 0.4rem 0.875rem;
    font-size: 0.8125rem;
  }
}

@media (max-width: 480px) {
  .account-page {
    padding: 1rem 0.75rem 2rem;
    gap: 0.875rem;
  }

  .page-title {
    font-size: 1.375rem;
  }

  .page-subtitle {
    font-size: 0.75rem;
  }

  .header-icon {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 12px;
  }

  .header-icon svg {
    width: 1.5rem;
    height: 1.5rem;
  }

  .info-card {
    border-radius: 11px;
  }

  .card-header {
    padding: 1rem 1.125rem;
    gap: 0.625rem;
  }

  .card-header-icon {
    width: 1.875rem;
    height: 1.875rem;
    border-radius: 9px;
  }

  .card-header-icon svg {
    width: 0.9375rem;
    height: 0.9375rem;
  }

  .card-title {
    font-size: 0.9375rem;
  }

  .card-description {
    font-size: 0.7rem;
  }

  .card-content {
    padding: 1.125rem;
  }

  .form-label {
    font-size: 0.75rem;
  }

  .label-icon {
    width: 0.9375rem;
    height: 0.9375rem;
  }

  .form-input,
  :deep(.dp__input) {
    padding: 10px 13px !important;
    font-size: 14px !important;
    min-height: 44px !important;
    height: 44px !important;
    border-radius: 7px !important;
  }

  .btn-primary,
  .btn-secondary {
    padding: 0.6rem 0.9375rem;
    font-size: 0.8rem;
    border-radius: 8px;
  }

  .btn-icon {
    width: 0.9375rem;
    height: 0.9375rem;
  }

  .status-badge {
    padding: 0.375rem 0.8125rem;
    font-size: 0.8rem;
  }

  .info-message,
  .warning-message,
  .success-message,
  .error-message {
    padding: 0.625rem 0.75rem;
    font-size: 0.75rem;
  }

  .message-icon {
    width: 1rem;
    height: 1rem;
  }

  .modal-card {
    width: 95%;
  }

  .modal-header h3 {
    font-size: 1.0625rem;
  }

  .modal-body p {
    font-size: 0.8125rem;
  }
}

@media (max-width: 380px) {
  .account-page {
    padding: 0.875rem 0.625rem 1.75rem;
  }

  .page-title {
    font-size: 1.25rem;
  }

  .page-subtitle {
    font-size: 0.6875rem;
  }

  .header-icon {
    width: 2.25rem;
    height: 2.25rem;
  }

  .header-icon svg {
    width: 1.375rem;
    height: 1.375rem;
  }

  .card-header {
    padding: 0.9375rem 1rem;
  }

  .card-title {
    font-size: 0.875rem;
  }

  .card-description {
    font-size: 0.6875rem;
  }

  .card-content {
    padding: 1rem;
  }

  .form-label {
    font-size: 0.7rem;
  }

  .form-input,
  :deep(.dp__input) {
    padding: 9px 12px !important;
    font-size: 13.5px !important;
    min-height: 42px !important;
    height: 42px !important;
  }

  .btn-primary,
  .btn-secondary {
    padding: 0.5625rem 0.875rem;
    font-size: 0.75rem;
  }
}
</style> 
