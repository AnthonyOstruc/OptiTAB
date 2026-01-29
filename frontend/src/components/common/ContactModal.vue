<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
        <div class="modal-container">
          <div class="modal-header">
            <h2 class="modal-title">Poser une question</h2>
            <button class="modal-close" @click="closeModal" aria-label="Fermer">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
          
	          <form @submit.prevent="handleSubmit" class="contact-form-modal">
	            <p v-if="submitError" class="form-submit-error" role="alert">{{ submitError }}</p>
	            <div class="form-row">
	              <div class="form-group">
	                <label for="modal-firstName" class="form-label">Prénom *</label>
	                <input 
	                  type="text" 
	                  id="modal-firstName" 
	                  v-model="form.firstName"
	                  class="form-input"
	                  :class="{ 'form-control--error': fieldErrors.firstName }"
	                  :aria-invalid="Boolean(fieldErrors.firstName)"
	                  placeholder="Votre prénom"
	                  required
	                />
	                <p v-if="fieldErrors.firstName" class="form-field-error">{{ fieldErrors.firstName }}</p>
	              </div>
	              <div class="form-group">
	                <label for="modal-lastName" class="form-label">Nom *</label>
	                <input 
	                  type="text" 
	                  id="modal-lastName" 
	                  v-model="form.lastName"
	                  class="form-input"
	                  :class="{ 'form-control--error': fieldErrors.lastName }"
	                  :aria-invalid="Boolean(fieldErrors.lastName)"
	                  placeholder="Votre nom"
	                  required
	                />
	                <p v-if="fieldErrors.lastName" class="form-field-error">{{ fieldErrors.lastName }}</p>
	              </div>
	            </div>
	
	            <div class="form-group">
	              <label for="modal-email" class="form-label">Email *</label>
	              <input 
	                type="email" 
	                id="modal-email" 
	                v-model="form.email"
	                class="form-input"
	                :class="{ 'form-control--error': fieldErrors.email }"
	                :aria-invalid="Boolean(fieldErrors.email)"
	                placeholder="votre@email.com"
	                required
	              />
	              <p v-if="fieldErrors.email" class="form-field-error">{{ fieldErrors.email }}</p>
	            </div>
	
	            <div class="form-group">
	              <label for="modal-subject" class="form-label">Sujet *</label>
	              <select 
	                id="modal-subject" 
	                v-model="form.subject"
	                class="form-select"
	                :class="{ 'form-control--error': fieldErrors.subject }"
	                :aria-invalid="Boolean(fieldErrors.subject)"
	                required
	              >
	                <option value="">Je vous contacte à propos de...</option>
	                <option value="Réserver un cours">Réserver un cours</option>
	                <option value="Choisir un pack">Choisir un pack</option>
                <option value="Réserver un cours / pack">Réserver un cours / pack</option>
                <option value="Demande d'information">Demande d'information</option>
                <option value="Support technique">Support technique</option>
	                <option value="Partenariat">Partenariat</option>
	                <option value="Autre">Autre</option>
	              </select>
	              <p v-if="fieldErrors.subject" class="form-field-error">{{ fieldErrors.subject }}</p>
	            </div>
	
	            <div class="form-group">
	              <label for="modal-message" class="form-label">Message *</label>
	              <textarea 
	                id="modal-message" 
	                v-model="form.message"
	                class="form-textarea"
	                :class="{ 'form-control--error': fieldErrors.message }"
	                :aria-invalid="Boolean(fieldErrors.message)"
	                placeholder="Votre message..."
	                rows="4"
	                minlength="5"
	                required
	              ></textarea>
	              <p class="form-help">Minimum 5 caractères.</p>
	              <p v-if="fieldErrors.message" class="form-field-error">{{ fieldErrors.message }}</p>
	            </div>
	
	            <div class="form-actions">
	              <button type="button" class="btn-cancel" @click="closeModal" :disabled="isSubmitting">
	                Annuler
              </button>
              <button type="submit" class="btn-submit" :disabled="isSubmitting">
                <span v-if="!isSubmitting">Envoyer</span>
                <span v-else>Envoi en cours...</span>
              </button>
            </div>
          </form>
          
          <!-- Alternatives de contact -->
          <div class="contact-alternatives">
            <p class="alternatives-text">Ou contactez-nous directement :</p>
            <div class="alternatives-buttons">
              <a 
                href="https://wa.me/33764040251?text=Bonjour, j'aimerais poser une question sur les cours particuliers OptiTAB !" 
                target="_blank" 
                rel="noopener noreferrer"
                class="btn-whatsapp"
                data-cta-name="whatsapp"
                data-cta-location="modal"
                @click="closeModal"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" style="margin-right: 0.5rem;">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.821 11.821 0 0020.885 3.488"/>
                </svg>
                WhatsApp
              </a>
              <a 
                href="mailto:contact@optitab.net?subject=Question sur les cours particuliers" 
                class="btn-email"
                @click="closeModal"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                  <polyline points="22,6 12,13 2,6"/>
                </svg>
                Email
              </a>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
	</template>

	<script setup>
	import { ref, watch, onBeforeUnmount } from 'vue'
	import { sendContactMessage } from '@/api/contact'
	import { lockBodyScroll, unlockBodyScroll } from '@/utils/bodyScrollLock'

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
	const scrollPosition = ref(0)
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

// Fermer avec la touche Escape
const handleEscape = (e) => {
  if (e.key === 'Escape' && props.isOpen) {
    closeModal()
  }
}

const SCROLL_LOCK_KEY = 'contact-modal'

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    document.addEventListener('keydown', handleEscape)
    // Sauvegarder la position de scroll
    scrollPosition.value = window.pageYOffset || document.documentElement.scrollTop
    // Empêcher le scroll de l'arrière-plan
    lockBodyScroll(SCROLL_LOCK_KEY, { mode: 'fixed' })
  } else {
    document.removeEventListener('keydown', handleEscape)
    // Réactiver le scroll et restaurer la position
    unlockBodyScroll(SCROLL_LOCK_KEY)
  }
}, { immediate: true })

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleEscape)
  unlockBodyScroll(SCROLL_LOCK_KEY)
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 1rem;
  backdrop-filter: blur(4px);
}

.modal-container {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  background: white;
  z-index: 1;
  border-radius: 16px 16px 0 0;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.modal-close {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  color: #64748b;
  transition: all 0.2s ease;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.contact-form-modal {
  padding: 1.25rem 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 0.9rem;
}

	.form-label {
	  font-weight: 600;
	  color: #374151;
	  margin-bottom: 0.4rem;
	  font-size: 0.85rem;
	}
	
	.form-submit-error {
	  margin: 0 0 0.85rem 0;
	  padding: 0.75rem 0.9rem;
	  border-radius: 10px;
	  border: 1px solid #fecaca;
	  background: #fef2f2;
	  color: #991b1b;
	  font-size: 0.9rem;
	  font-weight: 600;
	}

	.form-input,
	.form-select,
	.form-textarea {
  padding: 0.6rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.9rem;
  transition: all 0.2s ease;
  background: white;
  font-family: inherit;
	  width: 100%;
	}
	
	.form-control--error {
	  border-color: #ef4444;
	}
	
	.form-control--error:focus {
	  border-color: #ef4444;
	  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.12);
	}
	
	.form-help {
	  margin-top: 0.35rem;
	  color: #6b7280;
	  font-size: 0.8rem;
	}
	
	.form-field-error {
	  margin-top: 0.35rem;
	  color: #b91c1c;
	  font-size: 0.82rem;
	  font-weight: 600;
	}

		.form-input:focus:not(.form-control--error),
		.form-select:focus:not(.form-control--error),
		.form-textarea:focus:not(.form-control--error) {
	  outline: none;
	  border-color: #2a38b7;
	  box-shadow: 0 0 0 3px rgba(42, 56, 183, 0.1);
	}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.btn-cancel {
  padding: 0.65rem 1.25rem;
  background: white;
  color: #64748b;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #9ca3af;
}

.btn-cancel:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-submit {
  padding: 0.65rem 1.25rem;
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(42, 56, 183, 0.3);
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(42, 56, 183, 0.4);
}

.btn-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

/* Alternatives de contact */
.contact-alternatives {
  padding: 1rem 1.5rem 1.25rem;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
  border-radius: 0 0 16px 16px;
}

.alternatives-text {
  text-align: center;
  color: #64748b;
  font-size: 0.85rem;
  margin: 0 0 0.75rem 0;
  font-weight: 500;
}

.alternatives-buttons {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
}

.btn-whatsapp,
.btn-email {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.65rem 1.25rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  cursor: pointer;
  border: none;
  font-family: inherit;
}

.btn-whatsapp {
  background: #25D366;
  color: white;
  box-shadow: 0 2px 8px rgba(37, 211, 102, 0.3);
}

.btn-whatsapp:hover {
  background: #20BA5A;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(37, 211, 102, 0.4);
}

.btn-email {
  background: white;
  color: #374151;
  border: 1px solid #d1d5db;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.btn-email:hover {
  background: #f9fafb;
  border-color: #9ca3af;
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

/* Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .modal-container {
    max-width: 100%;
    border-radius: 12px;
  }

  .modal-header {
    padding: 0.6rem 0.9rem;
  }

  .modal-title {
    font-size: 1rem;
  }

  .contact-form-modal {
    padding: 0.7rem 0.9rem;
  }

  .form-row {
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .form-group {
    margin-bottom: 0.6rem;
  }

  .form-label {
    font-size: 0.75rem;
    margin-bottom: 0.3rem;
  }

  .form-input,
  .form-select,
  .form-textarea {
    padding: 0.5rem;
    font-size: 0.8rem;
  }

  .form-textarea {
    min-height: 60px;
  }

  .form-actions {
    flex-direction: row;
    justify-content: flex-end;
    margin-top: 0.6rem;
    padding-top: 0.6rem;
    gap: 0.55rem;
  }

  .btn-cancel,
  .btn-submit {
    width: auto;
    padding: 0.55rem 0.9rem;
    font-size: 0.8rem;
  }

  .contact-alternatives {
    padding: 0.6rem 0.9rem 0.7rem;
  }

  .alternatives-text {
    font-size: 0.75rem;
    margin-bottom: 0.55rem;
  }

  .alternatives-buttons {
    flex-direction: row;
    gap: 0.55rem;
  }

  .btn-whatsapp,
  .btn-email {
    width: auto;
    flex: 1;
    padding: 0.55rem 0.9rem;
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .modal-overlay {
    padding: 0.4rem;
  }

  .modal-container {
    border-radius: 10px;
  }

  .modal-header {
    padding: 0.55rem 0.75rem;
  }

  .modal-title {
    font-size: 0.95rem;
  }

  .contact-form-modal {
    padding: 0.6rem 0.75rem;
  }

  .form-group {
    margin-bottom: 0.5rem;
  }

  .form-label {
    font-size: 0.7rem;
    margin-bottom: 0.25rem;
  }

  .form-input,
  .form-select,
  .form-textarea {
    padding: 0.45rem;
    font-size: 0.75rem;
  }

  .form-textarea {
    min-height: 50px;
  }

  .form-actions {
    flex-direction: row;
    justify-content: flex-end;
    margin-top: 0.5rem;
    padding-top: 0.5rem;
    gap: 0.5rem;
  }

  .btn-cancel,
  .btn-submit {
    padding: 0.5rem 0.8rem;
    font-size: 0.75rem;
    width: auto;
  }

  .contact-alternatives {
    padding: 0.55rem 0.75rem 0.65rem;
  }

  .alternatives-text {
    font-size: 0.7rem;
    margin-bottom: 0.5rem;
  }

  .alternatives-buttons {
    flex-direction: row;
    gap: 0.5rem;
  }

  .btn-whatsapp,
  .btn-email {
    padding: 0.5rem 0.8rem;
    font-size: 0.75rem;
    width: auto;
    flex: 1;
  }
}
</style>
