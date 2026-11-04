<template>
  <Modal
    :is-open="isOpen"
    title="Poser une question"
    subtitle="Écris-nous : réponse sous 24 h par e-mail."
    :icon="ChatBubbleLeftRightIcon"
    :can-close="!isSubmitting"
    size="medium"
    @close="closeModal"
  >
    <form class="contact-form" novalidate @submit.prevent="handleSubmit">
      <p v-if="submitError" class="om-alert om-alert--error" role="alert">{{ submitError }}</p>

      <div class="contact-row">
        <div class="om-field">
          <label for="modal-firstName" class="om-label">Prénom</label>
          <input id="modal-firstName" v-model="form.firstName" type="text" class="om-input" :class="{ 'is-error': fieldErrors.firstName }" :aria-invalid="Boolean(fieldErrors.firstName)" placeholder="Ton prénom" autocomplete="given-name" required />
          <p v-if="fieldErrors.firstName" class="contact-error">{{ fieldErrors.firstName }}</p>
        </div>
        <div class="om-field">
          <label for="modal-lastName" class="om-label">Nom</label>
          <input id="modal-lastName" v-model="form.lastName" type="text" class="om-input" :class="{ 'is-error': fieldErrors.lastName }" :aria-invalid="Boolean(fieldErrors.lastName)" placeholder="Ton nom" autocomplete="family-name" required />
          <p v-if="fieldErrors.lastName" class="contact-error">{{ fieldErrors.lastName }}</p>
        </div>
      </div>

      <div class="om-field">
        <label for="modal-email" class="om-label">E-mail</label>
        <input id="modal-email" v-model="form.email" type="email" class="om-input" :class="{ 'is-error': fieldErrors.email }" :aria-invalid="Boolean(fieldErrors.email)" placeholder="ton@email.com" autocomplete="email" required />
        <p v-if="fieldErrors.email" class="contact-error">{{ fieldErrors.email }}</p>
      </div>

      <div class="om-field">
        <label for="modal-subject" class="om-label">Sujet</label>
        <select id="modal-subject" v-model="form.subject" class="om-input contact-select" :class="{ 'is-error': fieldErrors.subject }" :aria-invalid="Boolean(fieldErrors.subject)" required>
          <option value="">Je vous contacte à propos de…</option>
          <option value="Réserver un cours">Réserver un cours</option>
          <option value="Choisir un pack">Choisir un pack</option>
          <option value="Réserver un cours / pack">Réserver un cours / pack</option>
          <option value="Demande d'information">Demande d'information</option>
          <option value="Support technique">Support technique</option>
          <option value="Partenariat">Partenariat</option>
          <option value="Autre">Autre</option>
        </select>
        <p v-if="fieldErrors.subject" class="contact-error">{{ fieldErrors.subject }}</p>
      </div>

      <div class="om-field">
        <label for="modal-message" class="om-label">Message</label>
        <textarea id="modal-message" v-model="form.message" class="om-input" :class="{ 'is-error': fieldErrors.message }" :aria-invalid="Boolean(fieldErrors.message)" placeholder="Ta question, ta classe, tes disponibilités…" rows="4" minlength="5" required></textarea>
        <p v-if="fieldErrors.message" class="contact-error">{{ fieldErrors.message }}</p>
      </div>

      <div class="contact-actions">
        <button type="button" class="om-btn om-btn--ghost" :disabled="isSubmitting" @click="closeModal">Annuler</button>
        <button type="submit" class="om-btn om-btn--primary" :disabled="isSubmitting">
          {{ isSubmitting ? 'Envoi en cours…' : 'Envoyer le message' }}
        </button>
      </div>
    </form>

    <template #footer>
      <div class="contact-alternatives">
        <p>Ou directement :</p>
        <a
          href="https://wa.me/33764040251?text=Bonjour, j'aimerais poser une question sur les cours particuliers OptiTAB !"
          target="_blank"
          rel="noopener noreferrer"
          class="om-btn om-btn--green"
          data-cta-name="whatsapp"
          data-cta-location="modal"
          @click="closeModal"
        >
          <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.821 11.821 0 0020.885 3.488"/></svg>
          WhatsApp
        </a>
        <a href="mailto:contact@optitab.net?subject=Question sur les cours particuliers" class="om-btn om-btn--ghost" @click="closeModal">
          <EnvelopeIcon aria-hidden="true" />
          E-mail
        </a>
      </div>
    </template>
  </Modal>
</template>

	<script setup>
	import { ref, watch } from 'vue'
	import { sendContactMessage } from '@/api/contact'
	import { ChatBubbleLeftRightIcon, EnvelopeIcon } from '@heroicons/vue/24/outline'
	import Modal from '@/components/common/Modal.vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  initialSubject: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['close', 'success'])

	const isSubmitting = ref(false)
	const submitError = ref('')
	const fieldErrors = ref({})
	const form = ref({
	  firstName: '',
	  lastName: '',
	  email: '',
	  subject: '',
	  message: ''
	})
	
	const MIN_MESSAGE_LENGTH = 5
	const EMAIL_REGEX = /^[^@\s]+@[^@\s]+\.[^@\s]+$/

	const closeModal = () => {
	  if (!isSubmitting.value) {
	    emit('close')
	  }
	}
	
	const validate = () => {
	  const errors = {}
	  const first = (form.value.firstName || '').trim()
	  const last = (form.value.lastName || '').trim()
	  const email = (form.value.email || '').trim()
	  const subject = (form.value.subject || '').trim()
	  const message = (form.value.message || '').trim()
	
	  if (!first) errors.firstName = 'Champ requis'
	  if (!last) errors.lastName = 'Champ requis'
	  if (!email || !EMAIL_REGEX.test(email)) errors.email = 'Email invalide'
	  if (!subject) errors.subject = 'Champ requis'
	  if (!message || message.length < MIN_MESSAGE_LENGTH) {
	    errors.message = `Message trop court (min ${MIN_MESSAGE_LENGTH} caractères)`
	  }
	
	  return errors
	}

	const handleSubmit = async () => {
	  if (isSubmitting.value) return
	
	  submitError.value = ''
	  fieldErrors.value = {}
	
	  const clientErrors = validate()
	  if (Object.keys(clientErrors).length > 0) {
	    fieldErrors.value = clientErrors
	    submitError.value = 'Veuillez corriger les champs indiqués.'
	    return
	  }
	
	  isSubmitting.value = true
	  
	  try {
	    await sendContactMessage({
	      firstName: form.value.firstName,
      lastName: form.value.lastName,
      email: form.value.email,
      subject: form.value.subject,
      message: form.value.message,
    })
    
    // Réinitialiser le formulaire
    form.value = { firstName: '', lastName: '', email: '', subject: '', message: '' }
    
    // Émettre l'événement de succès
    emit('success', 'Votre message a été envoyé. Un email de confirmation vous a été adressé. Réponse sous 24h.')
    
	    // Fermer le modal après un court délai
	    setTimeout(() => {
	      emit('close')
	    }, 500)
	  } catch (e) {
	    console.error('Erreur envoi message de contact:', e)
	    const data = e?.response?.data
	    if (data && typeof data === 'object' && data.errors && typeof data.errors === 'object') {
	      fieldErrors.value = { ...data.errors }
	      submitError.value = 'Veuillez corriger les champs indiqués.'
	    } else if (data && typeof data === 'object' && typeof data.message === 'string') {
	      submitError.value = data.message
	    } else if (!e?.response) {
	      submitError.value = "Impossible de contacter le serveur. Vérifiez que le backend tourne sur http://localhost:8000."
	    } else {
	      submitError.value = "Désolé, l'envoi a échoué. Veuillez réessayer plus tard."
	    }
	  } finally {
	    isSubmitting.value = false
	  }
	}

	// Réinitialiser le formulaire quand le modal se ferme ou s'ouvre
	watch(() => props.isOpen, (newVal) => {
	  if (newVal) {
	    // Quand le modal s'ouvre, initialiser le sujet si fourni
	    form.value = { 
	      firstName: '', 
	      lastName: '', 
	      email: '', 
	      subject: props.initialSubject || '', 
	      message: '' 
	    }
	    submitError.value = ''
	    fieldErrors.value = {}
	  } else {
	    // Quand le modal se ferme, réinitialiser tout
	    form.value = { firstName: '', lastName: '', email: '', subject: '', message: '' }
	    submitError.value = ''
	    fieldErrors.value = {}
	  }
	})

// Mettre à jour le sujet quand initialSubject change
watch(() => props.initialSubject, (newSubject) => {
  if (props.isOpen && newSubject) {
    form.value.subject = newSubject
  }
})

</script>

<style scoped>
/* Éléments communs (.om-field, .om-input, .om-btn, .om-alert) : components/common/Modal.vue */
.contact-form {
  display: grid;
  gap: 16px;
}

.contact-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.contact-select {
  appearance: none;
  padding-right: 44px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%235d667d' stroke-width='2'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
  background-size: 18px;
  cursor: pointer;
}

.om-input.is-error {
  border-color: var(--om-red);
}

.contact-error {
  margin: 0;
  color: var(--om-red);
  font-size: 13.5px;
  font-weight: 500;
}

.contact-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 4px;
}

.contact-alternatives {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
}

.contact-alternatives p {
  margin: 0 6px 0 0;
  color: var(--om-muted);
  font-size: 14px;
}

.contact-alternatives .om-btn {
  min-height: 44px;
  padding: 0 18px;
  font-size: 14.5px;
}

@media (max-width: 520px) {
  .contact-row {
    grid-template-columns: 1fr;
  }

  .contact-actions {
    flex-direction: column-reverse;
  }

  .contact-actions .om-btn {
    width: 100%;
  }
}
</style>
