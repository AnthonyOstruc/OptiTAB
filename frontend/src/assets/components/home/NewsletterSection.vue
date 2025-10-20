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
      <button type="submit">{{ bouton }}</button>
    </form>
    <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
  </section>
</template>

<script setup>
import { ref } from 'vue'
const props = defineProps({
  titre: { type: String, default: 'Recevez nos nouveautés' },
  description: { type: String, default: 'Inscrivez-vous à notre newsletter.' },
  placeholder: { type: String, default: 'Votre email' },
  bouton: { type: String, default: 'S\'inscrire' }
})

const email = ref('')
const successMessage = ref('')

function onSubmit() {
  // Ici, tu pourrais émettre un événement ou appeler une API
  email.value = ''
  successMessage.value = 'Merci pour votre inscription !'
  setTimeout(() => (successMessage.value = ''), 3000)
}
</script>

<style scoped>
.newsletter {
  max-width: 680px;
  margin: 0 auto;
  padding: 24px 20px;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 12px rgba(30,41,59,0.06);
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.content h3 {
  color: #4f46e5;
  font-size: 1.25rem;
  font-weight: 800;
  margin-bottom: 6px;
}
.content p {
  color: #52525b;
  font-size: 1rem;
  margin: 0;
}
.form {
  display: flex;
  flex-direction: row;
  gap: 10px;
  flex-wrap: wrap;
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
@media (max-width: 600px) {
  .form {
    flex-direction: column;
    gap: 10px;
  }
  button {
    width: 100%;
  }
}
</style>
