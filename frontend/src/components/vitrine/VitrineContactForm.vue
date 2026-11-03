<template>
  <div class="cf">
    <div v-if="status === 'sent'" class="cf__done" role="status">
      <span class="cf__done-icon"><CheckIcon aria-hidden="true" /></span>
      <p class="cf__done-title">{{ mode === 'cours' ? 'Demande bien reçue !' : 'Message envoyé !' }}</p>
      <p class="cf__done-text">
        Un e-mail de confirmation vient de vous être envoyé.
        {{ mode === 'cours' ? 'Je vous recontacte sous 24 h pour fixer notre premier échange.' : 'Nous vous répondons sous 24 h.' }}
      </p>
      <button type="button" class="vt-btn vt-btn--ghost vt-btn--sm" @click="reset">Envoyer une autre demande</button>
    </div>

    <form v-else class="cf__form" novalidate @submit.prevent="submit">
      <div class="cf__row">
        <label class="cf__field">
          <span class="cf__label">Prénom</span>
          <input v-model.trim="form.firstName" type="text" autocomplete="given-name" :aria-invalid="!!errors.firstName" />
          <span v-if="errors.firstName" class="cf__error">{{ errors.firstName }}</span>
        </label>
        <label class="cf__field">
          <span class="cf__label">Nom</span>
          <input v-model.trim="form.lastName" type="text" autocomplete="family-name" :aria-invalid="!!errors.lastName" />
          <span v-if="errors.lastName" class="cf__error">{{ errors.lastName }}</span>
        </label>
      </div>

      <div class="cf__row">
        <label class="cf__field">
          <span class="cf__label">E-mail</span>
          <input v-model.trim="form.email" type="email" inputmode="email" autocomplete="email" :aria-invalid="!!errors.email" />
          <span v-if="errors.email" class="cf__error">{{ errors.email }}</span>
        </label>
        <label v-if="mode === 'cours'" class="cf__field">
          <span class="cf__label">Téléphone <em>facultatif</em></span>
          <input v-model.trim="form.phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="Pour être rappelé" />
        </label>
        <label v-else class="cf__field">
          <span class="cf__label">Sujet</span>
          <select v-model="form.subject" :aria-invalid="!!errors.subject">
            <option value="" disabled>Choisir un sujet</option>
            <option v-for="sujet in SUJETS" :key="sujet" :value="sujet">{{ sujet }}</option>
          </select>
          <span v-if="errors.subject" class="cf__error">{{ errors.subject }}</span>
        </label>
      </div>

      <template v-if="mode === 'cours'">
        <div class="cf__row">
          <label class="cf__field">
            <span class="cf__label">Vous êtes</span>
            <select v-model="form.profil">
              <option>Parent</option>
              <option>Élève ou étudiant</option>
            </select>
          </label>
          <label class="cf__field">
            <span class="cf__label">Niveau</span>
            <select v-model="form.niveau" @change="niveauChoisi = true">
              <option v-for="niveau in NIVEAUX" :key="niveau">{{ niveau }}</option>
            </select>
          </label>
        </div>
        <fieldset class="cf__field cf__choices">
          <legend class="cf__label">Matière</legend>
          <label v-for="matiere in MATIERES" :key="matiere" :class="['cf__choice', { 'is-checked': form.matiere === matiere }]">
            <input v-model="form.matiere" type="radio" name="cf-matiere" :value="matiere" />
            {{ matiere }}
          </label>
        </fieldset>
      </template>

      <label class="cf__field">
        <span class="cf__label">
          {{ mode === 'cours' ? 'Ce que vous aimeriez travailler' : 'Message' }}
          <em v-if="mode === 'cours'">facultatif</em>
        </span>
        <textarea
          v-model="form.message"
          rows="4"
          :placeholder="mode === 'cours' ? 'Ex. : remonter la moyenne en maths, préparer le bac, une notion qui bloque…' : 'Votre message…'"
          :aria-invalid="!!errors.message"
        ></textarea>
        <span v-if="errors.message" class="cf__error">{{ errors.message }}</span>
      </label>

      <p v-if="globalError" class="cf__alert" role="alert">{{ globalError }}</p>

      <div class="cf__footer">
        <button type="submit" class="vt-btn vt-btn--primary" :disabled="status === 'sending'">
          {{ status === 'sending' ? 'Envoi…' : (mode === 'cours' ? 'Demander mon premier échange' : 'Envoyer le message') }}
          <ArrowRightIcon v-if="status !== 'sending'" aria-hidden="true" />
        </button>
        <p class="cf__privacy">
          Vos informations servent uniquement à vous répondre.
          <router-link to="/confidentialite">Confidentialité</router-link>
        </p>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import { ArrowRightIcon, CheckIcon } from '@heroicons/vue/24/outline'
import { sendContactMessage } from '@/api/contact'

const props = defineProps({
  // 'contact' : formulaire général ; 'cours' : demande de cours particuliers.
  mode: { type: String, default: 'contact' },
  sujetInitial: { type: String, default: '' },
  // Niveau proposé par défaut (ex. celui consulté dans les tarifs).
  niveauInitial: { type: String, default: 'Lycée' }
})

const SUJETS = [
  'Cours particuliers',
  'Une question sur la plateforme',
  'Mon abonnement ou un paiement',
  'Un problème technique',
  'Partenariat',
  'Autre'
]
const NIVEAUX = ['Collège', 'Lycée', 'Prépa ou supérieur']
const MATIERES = ['Mathématiques', 'Physique-chimie', 'Informatique']

const blank = () => ({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  subject: SUJETS.includes(props.sujetInitial) ? props.sujetInitial : '',
  profil: 'Parent',
  niveau: NIVEAUX.includes(props.niveauInitial) ? props.niveauInitial : 'Lycée',
  matiere: 'Mathématiques',
  message: ''
})

const form = reactive(blank())
const errors = reactive({})
const status = ref('idle')
const globalError = ref('')

// Le niveau suit celui proposé par la page tant que l'utilisateur n'en a pas choisi un.
const niveauChoisi = ref(false)
watch(
  () => props.niveauInitial,
  (niveau) => {
    if (!niveauChoisi.value && NIVEAUX.includes(niveau)) form.niveau = niveau
  }
)

const validate = () => {
  Object.keys(errors).forEach((key) => delete errors[key])
  if (!form.firstName) errors.firstName = 'Indiquez votre prénom.'
  if (!form.lastName) errors.lastName = 'Indiquez votre nom.'
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) errors.email = 'Vérifiez votre adresse e-mail.'
  if (props.mode !== 'cours') {
    if (!form.subject) errors.subject = 'Choisissez un sujet.'
    if (form.message.trim().length < 5) errors.message = 'Votre message est un peu court.'
  }
  return Object.keys(errors).length === 0
}

// La demande de cours reprend profil, niveau et matière en tête du message.
const buildMessage = () => {
  if (props.mode !== 'cours') return form.message.trim()
  const lignes = [
    'Demande de cours particuliers',
    `Profil : ${form.profil}`,
    `Niveau : ${form.niveau}`,
    `Matière : ${form.matiere}`
  ]
  if (form.phone) lignes.push(`Téléphone : ${form.phone}`)
  if (form.message.trim()) lignes.push('', form.message.trim())
  return lignes.join('\n')
}

const submit = async () => {
  globalError.value = ''
  if (!validate()) return
  status.value = 'sending'
  try {
    await sendContactMessage({
      firstName: form.firstName,
      lastName: form.lastName,
      email: form.email,
      subject: props.mode === 'cours' ? 'Réserver un cours' : form.subject,
      message: buildMessage()
    })
    status.value = 'sent'
  } catch (error) {
    status.value = 'idle'
    const data = error?.response?.data
    if (data?.errors && typeof data.errors === 'object') {
      Object.assign(errors, data.errors)
      globalError.value = 'Merci de vérifier les champs indiqués.'
    } else if (!error?.response) {
      globalError.value = 'Connexion impossible. Vérifiez votre réseau, ou écrivez-nous sur WhatsApp.'
    } else {
      globalError.value = 'L’envoi n’a pas abouti. Réessayez dans un instant, ou écrivez-nous sur WhatsApp.'
    }
  }
}

const reset = () => {
  Object.assign(form, blank())
  niveauChoisi.value = false
  status.value = 'idle'
}
</script>

<style scoped>
.cf__form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cf__row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

/* Matière : trois boutons à cocher. */
.cf__field.cf__choices {
  flex-direction: row;
  flex-wrap: wrap;
  gap: 8px;
  margin: 0;
  padding: 0;
  border: 0;
}

.cf__choices legend {
  width: 100%;
  margin-bottom: 6px;
  padding: 0;
}

.cf__choice {
  position: relative;
  display: inline-flex;
  align-items: center;
  min-height: 44px;
  padding: 0 16px;
  border: 1px solid var(--vt-line-strong);
  border-radius: 999px;
  background: #fff;
  font-size: 15px;
  font-weight: 600;
  color: var(--vt-ink-soft);
  cursor: pointer;
  transition: border-color 0.15s ease, background-color 0.15s ease, color 0.15s ease;
}

.cf__choice:hover {
  border-color: var(--vt-navy);
}

.cf__choice input {
  position: absolute;
  inset: 0 auto auto 0;
  width: 1px;
  height: 1px;
  margin: 0;
  opacity: 0;
  pointer-events: none;
}

.cf__choice.is-checked {
  border-color: var(--vt-navy);
  background: var(--vt-navy);
  color: #fff;
}

.cf__choice:has(input:focus-visible) {
  outline: 3px solid rgba(95, 172, 96, 0.55);
  outline-offset: 2px;
}

.cf__field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.cf__label {
  font-size: 14px;
  font-weight: 700;
  color: var(--vt-ink);
}

.cf__label em {
  margin-left: 4px;
  font-style: normal;
  font-weight: 500;
  color: var(--vt-muted);
}

.cf__field input,
.cf__field select,
.cf__field textarea {
  width: 100%;
  min-height: 48px;
  padding: 11px 14px;
  border: 1px solid var(--vt-line-strong);
  border-radius: 12px;
  background: #fff;
  font-family: var(--vt-font);
  font-size: 16px;
  font-weight: 500;
  color: var(--vt-ink);
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.cf__field select {
  appearance: none;
  padding-right: 38px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='%235d667d'%3E%3Cpath d='M5.2 7.2a.75.75 0 0 1 1.06 0L10 10.94l3.74-3.74a.75.75 0 1 1 1.06 1.06l-4.27 4.27a.75.75 0 0 1-1.06 0L5.2 8.26a.75.75 0 0 1 0-1.06Z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 18px;
}

.cf__field textarea {
  min-height: 120px;
  resize: vertical;
  line-height: 1.55;
}

.cf__field input::placeholder,
.cf__field textarea::placeholder {
  color: #9aa3b5;
}

.cf__field input:focus,
.cf__field select:focus,
.cf__field textarea:focus {
  outline: none;
  border-color: var(--vt-navy);
  box-shadow: 0 0 0 3px rgba(27, 60, 142, 0.15);
}

.cf__field [aria-invalid='true'] {
  border-color: #d14343;
}

.cf__error {
  font-size: 13px;
  font-weight: 600;
  color: #b42318;
}

.cf__alert {
  margin: 0;
  padding: 12px 14px;
  border-radius: 12px;
  background: #fef3f2;
  font-size: 14px;
  font-weight: 600;
  color: #b42318;
}

.cf__footer {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px 20px;
  margin-top: 4px;
}

.cf__privacy {
  margin: 0;
  font-size: 13px;
  color: var(--vt-muted);
}

.cf__privacy a {
  color: var(--vt-navy);
  font-weight: 600;
}

/* ---------- Confirmation ---------- */

.cf__done {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 36px 20px;
  text-align: center;
}

.cf__done-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  margin-bottom: 6px;
  border-radius: 50%;
  background: var(--vt-green-50);
  color: var(--vt-green-700);
}

.cf__done-icon svg {
  width: 28px;
  height: 28px;
  stroke-width: 2.5;
}

.cf__done-title {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: var(--vt-ink);
}

.cf__done-text {
  max-width: 420px;
  margin: 0 0 12px;
  font-size: 15px;
  color: var(--vt-muted);
}

@media (max-width: 640px) {
  .cf__row {
    grid-template-columns: minmax(0, 1fr);
  }

  .cf__footer .vt-btn {
    width: 100%;
  }
}
</style>
