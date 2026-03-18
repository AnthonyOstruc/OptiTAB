<template>
  <div class="page auth-page">
    <div class="auth-card">
      <h1 class="title">Réinitialiser le mot de passe</h1>
      <p class="subtitle" v-if="!isSuccess">
        Entrez votre nouveau mot de passe. Le lien est valable une seule fois.
      </p>

      <div v-if="isSuccess" class="success">
        <p>✅ Votre mot de passe a été mis à jour.</p>
        <button class="btn primary" @click="goToLogin">Se connecter</button>
      </div>

      <form v-else @submit.prevent="onSubmit" class="form">
        <div class="field">
          <label>Nouveau mot de passe</label>
          <div class="input-wrapper">
            <input :type="showPassword ? 'text' : 'password'" v-model="password" required minlength="6" autocomplete="new-password" />
            <button type="button" class="toggle-eye" @click="showPassword = !showPassword" tabindex="-1" aria-label="Afficher le mot de passe">
              <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
            </button>
          </div>
        </div>
        <div class="field">
          <label>Confirmer le mot de passe</label>
          <div class="input-wrapper">
            <input :type="showPassword2 ? 'text' : 'password'" v-model="password2" required minlength="6" autocomplete="new-password" />
            <button type="button" class="toggle-eye" @click="showPassword2 = !showPassword2" tabindex="-1" aria-label="Afficher le mot de passe">
              <svg v-if="!showPassword2" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
            </button>
          </div>
        </div>
        <div class="actions">
          <button class="btn primary" :disabled="loading">{{ loading ? 'En cours...' : 'Valider' }}</button>
        </div>
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
  </div>
  
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { confirmPasswordReset } from '@/api/auth'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'

export default {
  name: 'PasswordReset',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const { openModal } = useModalManager()
    const token = ref('')
    const password = ref('')
    const password2 = ref('')
    const showPassword = ref(false)
    const showPassword2 = ref(false)
    const loading = ref(false)
    const error = ref('')
    const isSuccess = ref(false)

    onMounted(() => {
      token.value = (route.query.token || '').toString()
      if (!token.value) {
        error.value = 'Lien invalide ou expiré.'
      }
    })

    const onSubmit = async () => {
      error.value = ''
      if (!token.value) {
        error.value = 'Lien invalide ou expiré.'
        return
      }
      if (password.value !== password2.value) {
        error.value = 'Les mots de passe ne correspondent pas.'
        return
      }
      try {
        loading.value = true
        await confirmPasswordReset({ token: token.value, password: password.value })
        isSuccess.value = true
      } catch (e) {
        error.value = (e?.response?.data?.detail) || 'Impossible de réinitialiser le mot de passe.'
      } finally {
        loading.value = false
      }
    }

    const goToLogin = () => {
      router.push({ name: 'Home' }).then(() => {
        openModal(MODAL_IDS.LOGIN)
      })
    }

    return { token, password, password2, showPassword, showPassword2, loading, error, isSuccess, onSubmit, goToLogin }
  }
}
</script>

<style scoped>
.page { display:flex; justify-content:center; padding:40px 16px; }
.auth-card { max-width:420px; width:100%; background:#fff; border-radius:12px; padding:24px; box-shadow:0 10px 30px rgba(0,0,0,0.08); }
.title { margin:0 0 8px; font-size:24px; font-weight:700; }
.subtitle { margin:0 0 16px; color:#6b7280; }
.field { display:flex; flex-direction:column; gap:6px; margin-bottom:14px; }
.field input { padding:10px 12px; border:1px solid #e5e7eb; border-radius:8px; font-size:14px; width:100%; }
.input-wrapper { position:relative; display:flex; align-items:center; }
.input-wrapper input { padding-right:40px; }
.toggle-eye { position:absolute; right:10px; background:none; border:none; cursor:pointer; color:#9ca3af; padding:0; display:flex; align-items:center; }
.toggle-eye:hover { color:#6366f1; }
.actions { margin-top:10px; }
.btn { display:inline-block; padding:10px 14px; border-radius:8px; text-decoration:none; border:none; cursor:pointer; }
.btn.primary { background:#6366f1; color:#fff; }
.error { color:#ef4444; margin-top:10px; }
.success { text-align:center; display:flex; gap:10px; flex-direction:column; }
</style>


