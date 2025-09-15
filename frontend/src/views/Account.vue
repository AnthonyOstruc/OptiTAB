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
              <button v-if="!userStoreIsActive" type="button" class="verify-btn" @click="openVerificationModal">
                Vérifier
              </button>
              <span v-else class="verified-badge">✔️ Vérifié</span>
            </div>
            <p v-if="!userStoreIsActive" class="verify-hint">Votre email n'est pas encore vérifié.</p>
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
    </div>
  </DashboardLayout>

  <!-- Modal de vérification email -->
  <div v-if="showVerifyModal" class="modal-overlay" @click="closeVerificationModal">
    <div class="modal-card" @click.stop>
      <div class="modal-header">
        <h3>Vérification de l'email</h3>
        <button class="modal-close" @click="closeVerificationModal">×</button>
      </div>
      <div class="modal-body">
        <p>Un code a été envoyé à <strong>{{ form.email }}</strong> depuis <strong>contact@optitab.net</strong>. Veuillez le saisir ci-dessous.</p>
        <div class="code-inputs">
          <input v-for="(d, idx) in 6" :key="idx" maxlength="1" inputmode="numeric" pattern="[0-9]*" class="code-input" v-model="codeDigits[idx]" @input="focusNext(idx, $event)" />
        </div>
        <p v-if="verifyError" class="verify-error">{{ verifyError }}</p>
        <p v-if="verifySuccess" class="verify-success">Email vérifié avec succès.</p>
      </div>
      <div class="modal-actions">
        <button class="resend-btn" :disabled="isSending || resendCooldown>0" @click="sendCode">
          {{ resendCooldown>0 ? `Renvoyer (${resendCooldown}s)` : (isSending ? 'Envoi...' : 'Renvoyer le code') }}
        </button>
        <button class="confirm-btn" :disabled="isVerifying" @click="confirmCode">
          {{ isVerifying ? 'Vérification...' : 'Confirmer' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { updateUserProfile, fetchUserProfile, sendEmailVerificationCode, verifyEmailCode } from '@/api'
import FormInput from '@/components/forms/FormInput.vue'
import FormSelect from '@/components/forms/FormSelect.vue'
import { UserCircleIcon } from '@heroicons/vue/24/outline'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import UserPaysNiveauConfig from '@/components/dashboard/UserPaysNiveauConfig.vue'
import VueDatePicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'

const icon = UserCircleIcon
const userStore = useUserStore()

const form = ref({
  civilite: '',
  firstName: '',
  lastName: '',
  email: '',
  telephone: '',
  date_naissance: ''
})

const isSaving = ref(false)
const successMsg = ref('')
const errorMsg = ref('')

// Email verification state
const showVerifyModal = ref(false)
const isSending = ref(false)
const isVerifying = ref(false)
const verifyError = ref('')
const verifySuccess = ref('')
const resendCooldown = ref(0)
const codeDigits = ref(['', '', '', '', '', ''])
const userStoreIsActive = computed(() => !!userStore && userStore.id && (userStore.isActive || userStore.is_active || false) || (userStore?.isAuthenticated && userStore?.id && userStore?.level >= 0 && userStore?.email))

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

function openVerificationModal() {
  verifyError.value = ''
  verifySuccess.value = ''
  codeDigits.value = ['','','','','','']
  showVerifyModal.value = true
  // Envoyer le code immédiatement
  sendCode()
}

function closeVerificationModal() {
  showVerifyModal.value = false
}

async function sendCode() {
  try {
    if (resendCooldown.value > 0) return
    isSending.value = true
    await sendEmailVerificationCode()
    verifyError.value = ''
    verifySuccess.value = 'Code envoyé. Vérifiez votre boîte mail.'
    // Cooldown 60s
    resendCooldown.value = 60
    const timer = setInterval(() => {
      resendCooldown.value--
      if (resendCooldown.value <= 0) clearInterval(timer)
    }, 1000)
  } catch (e) {
    verifyError.value = e?.response?.data?.message || 'Impossible d\'envoyer le code. Réessayez plus tard.'
    verifySuccess.value = ''
  } finally {
    isSending.value = false
  }
}

function focusNext(idx, evt) {
  const val = evt.target.value.replace(/[^0-9]/g, '')
  codeDigits.value[idx] = val
  if (val && idx < 5) {
    const inputs = evt.target.parentElement.querySelectorAll('.code-input')
    inputs[idx + 1]?.focus()
  }
}

async function confirmCode() {
  try {
    isVerifying.value = true
    verifyError.value = ''
    verifySuccess.value = ''
    const code = codeDigits.value.join('')
    const res = await verifyEmailCode(code)
    verifySuccess.value = 'Email vérifié avec succès.'
    // Rafraîchir le profil pour mettre à jour is_active
    await userStore.fetchUser()
    showVerifyModal.value = false
  } catch (e) {
    verifyError.value = e?.response?.data?.message || 'Code invalide. Réessayez.'
  } finally {
    isVerifying.value = false
  }
}
</script>

<style scoped>
.account-page {
  max-width: 950px;
  margin: 2.5rem auto 0 auto;
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

/* Modal */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.5);
  display: flex; align-items: center; justify-content: center; z-index: 9999;
}
.modal-card { background: #fff; border-radius: 12px; width: 90%; max-width: 460px; padding: 1rem; }
.modal-header { display:flex; align-items:center; justify-content: space-between; margin-bottom: .5rem; }
.modal-header h3 { margin: 0; color: #193e8e; }
.modal-close { background:none; border:none; font-size:1.5rem; cursor:pointer; }
.modal-body { padding: .5rem 0 1rem 0; }
.code-inputs { display:flex; gap:.5rem; justify-content:center; margin-top:.5rem; }
.code-input { width: 46px; height: 50px; text-align:center; font-size: 1.25rem; border:2px solid #e5e7eb; border-radius:8px; }
.modal-actions { display:flex; justify-content: space-between; gap:.75rem; }
.confirm-btn { background:#16a34a; color:#fff; border:none; border-radius:8px; padding:.6rem 1.1rem; font-weight:700; cursor:pointer; }
.resend-btn { background:#f3f4f6; color:#111827; border:none; border-radius:8px; padding:.6rem 1.1rem; font-weight:700; cursor:pointer; }
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
@media (max-width: 900px) {
  .account-page {
    padding: 1.2rem 0.7rem 1.5rem 0.7rem;
  }
  .account-fields-row {
    flex-direction: column;
    gap: 0.7rem;
  }
}
.dark-blue-icon {
  color: #193e8e !important;
}
</style> 