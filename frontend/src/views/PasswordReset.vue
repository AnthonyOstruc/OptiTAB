<template>
  <div class="page auth-page">
    <div class="auth-card">
      <h1 class="title">Réinitialiser le mot de passe</h1>
      <p class="subtitle" v-if="!isSuccess">
        Entrez votre nouveau mot de passe. Le lien est valable une seule fois.
      </p>

      <div v-if="isSuccess" class="success">
        <p>✅ Votre mot de passe a été mis à jour.</p>
        <router-link class="btn" :to="{ name: 'Home' }">Se connecter</router-link>
      </div>

      <form v-else @submit.prevent="onSubmit" class="form">
        <div class="field">
          <label>Nouveau mot de passe</label>
          <input type="password" v-model="password" required minlength="6" autocomplete="new-password" />
        </div>
        <div class="field">
          <label>Confirmer le mot de passe</label>
          <input type="password" v-model="password2" required minlength="6" autocomplete="new-password" />
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

export default {
  name: 'PasswordReset',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const token = ref('')
    const password = ref('')
    const password2 = ref('')
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

    return { token, password, password2, loading, error, isSuccess, onSubmit }
  }
}
</script>

<style scoped>
.page { display:flex; justify-content:center; padding:40px 16px; }
.auth-card { max-width:420px; width:100%; background:#fff; border-radius:12px; padding:24px; box-shadow:0 10px 30px rgba(0,0,0,0.08); }
.title { margin:0 0 8px; font-size:24px; font-weight:700; }
.subtitle { margin:0 0 16px; color:#6b7280; }
.field { display:flex; flex-direction:column; gap:6px; margin-bottom:14px; }
.field input { padding:10px 12px; border:1px solid #e5e7eb; border-radius:8px; font-size:14px; }
.actions { margin-top:10px; }
.btn { display:inline-block; padding:10px 14px; border-radius:8px; text-decoration:none; border:none; cursor:pointer; }
.btn.primary { background:#6366f1; color:#fff; }
.error { color:#ef4444; margin-top:10px; }
.success { text-align:center; display:flex; gap:10px; flex-direction:column; }
</style>


