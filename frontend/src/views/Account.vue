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
          <FormInput label="Email" v-model="form.email" id="email" type="email" :disabled="true" autocomplete="email" class="account-input field-wide" placeholder="Email" />
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
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { updateUserProfile, fetchUserProfile } from '@/api'
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