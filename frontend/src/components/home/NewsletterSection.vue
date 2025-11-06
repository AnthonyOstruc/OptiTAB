<template>
  <section class="newsletter">
    <div class="content">
      <h3>{{ titre }}</h3>
      <p>{{ description }}</p>
    </div>
    <form @submit.prevent="onSubmit" class="form">
      <div class="input-group">
        <label for="newsletter-email" class="sr-only">Email</label>
        <input
          id="newsletter-email"
          v-model="email"
          :placeholder="placeholder"
          type="email"
          required
          autocomplete="email"
        />
        <span class="icon" aria-hidden="true">
          <svg width="20" height="20" fill="none" stroke="#2a38b7" stroke-width="2" viewBox="0 0 24 24">
            <rect width="20" height="14" x="2" y="5" rx="3"/>
            <path d="M2 7l10 6 10-6"/>
          </svg>
        </span>
      </div>
      <button type="submit" :disabled="loading">{{ loading ? '...' : bouton }}</button>
    </form>
    <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { subscribeToNewsletter } from '@/api/newsletter'

const props = defineProps({
  titre: { type: String, default: 'Restez informé avec OptiTAB' },
  description: { type: String, default: 'Recevez les dernières actualités, mises à jour et conseils pour progresser en maths.' },
  placeholder: { type: String, default: 'Votre email' },
  bouton: { type: String, default: "S'abonner" }
})

const email = ref('')
const successMessage = ref('')
const errorMessage = ref('')
const loading = ref(false)

async function onSubmit() {
  errorMessage.value = ''
  successMessage.value = ''
  if (!email.value) return
  try {
    loading.value = true
    await subscribeToNewsletter(email.value)
    successMessage.value = 'Merci ! Votre inscription est confirmée.'
    email.value = ''
  } catch (e) {
    errorMessage.value = e?.response?.data?.message || 'Une erreur est survenue.'
  } finally {
    loading.value = false
    setTimeout(() => {
      successMessage.value = ''
      errorMessage.value = ''
    }, 4000)
  }
}
</script>

<style scoped>
.newsletter {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 2vw;
  background: #fff;
  display: flex;
  flex-direction: column;
  gap: 24px;
  align-items: center;
}
.content {
  text-align: center;
  max-width: 700px;
}

.content h3 {
  color: #2a38b7;
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 12px;
}
.content p {
  color: #52525b;
  font-size: 1.1rem;
  margin: 0;
  line-height: 1.6;
}
.form {
  display: flex;
  flex-direction: row;
  gap: 12px;
  flex-wrap: wrap;
  max-width: 600px;
  width: 100%;
  justify-content: center;
}
.input-group {
  position: relative;
  flex: 1;
  min-width: 220px;
}
.input-group input {
  width: 100%;
  padding: 14px 42px 14px 16px;
  font-size: 1rem;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  background: #f8fafc;
  transition: 0.2s;
}
.input-group input:focus {
  border-color: #2a38b7;
  background: #fff;
  outline: none;
}
.icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
}
button {
  padding: 14px 28px;
  background: #2a38b7;
  color: white;
  font-weight: 700;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
  min-width: 120px;
}
button:hover {
  background: #4f46e5;
}
.success-message {
  color: #22c55e;
  font-size: 0.98rem;
  text-align: center;
  margin-top: 8px;
}
.error-message {
  color: #ef4444;
  font-size: 0.98rem;
  text-align: center;
  margin-top: 8px;
}
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0,0,0,0);
  border: 0;
}
@media (max-width: 768px) {
  .newsletter {
    padding: 48px 4vw;
  }
  
  .content h3 {
    font-size: 1.35rem;
  }
  
  .content p {
    font-size: 1rem;
  }
}

@media (max-width: 600px) {
  .newsletter {
    padding: 40px 4vw;
  }
  
  .content h3 {
    font-size: 1.25rem;
  }
  
  .form {
    flex-direction: column;
    gap: 12px;
  }
  
  .input-group {
    min-width: 100%;
  }
  
  button {
    width: 100%;
  }
}
</style>

