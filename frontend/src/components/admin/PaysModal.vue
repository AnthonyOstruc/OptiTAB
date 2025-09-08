<template>
  <div v-if="visible" class="modal-overlay" @click="handleOverlayClick">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <h2>
          <i class="fas fa-globe"></i>
          {{ mode === 'create' ? 'Nouveau Pays' : 'Modifier le Pays' }}
        </h2>
        <button @click="$emit('cancel')" class="modal-close">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="modal-body">
        <!-- Informations principales -->
        <div class="form-section">
          <h3><i class="fas fa-info-circle"></i> Informations générales</h3>
          
          <div class="form-group">
            <label for="nom" class="required">Nom du pays</label>
            <input
              id="nom"
              v-model="form.nom"
              type="text"
              class="form-control"
              :class="{ error: errors.nom }"
              placeholder="France, Canada, Allemagne..."
              required
            >
            <span v-if="errors.nom" class="error-message">{{ errors.nom }}</span>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="code_iso" class="required">Code ISO</label>
              <input
                id="code_iso"
                v-model="form.code_iso"
                type="text"
                class="form-control"
                :class="{ error: errors.code_iso }"
                placeholder="FR, CA, DE..."
                maxlength="3"
                style="text-transform: uppercase"
                required
              >
              <span v-if="errors.code_iso" class="error-message">{{ errors.code_iso }}</span>
            </div>

            <div class="form-group">
              <label for="drapeau_emoji">Drapeau (emoji)</label>
              <input
                id="drapeau_emoji"
                v-model="form.drapeau_emoji"
                type="text"
                class="form-control emoji-input"
                placeholder="🇫🇷"
                maxlength="4"
              >
              <small class="form-help">Utilisez l'emoji du drapeau du pays</small>
            </div>
          </div>

          <div class="form-group">
            <label for="description">Description</label>
            <textarea
              id="description"
              v-model="form.description"
              class="form-control"
              rows="3"
              placeholder="Description optionnelle du système éducatif ou autres informations..."
            ></textarea>
          </div>
        </div>

        <!-- Configuration -->
        <div class="form-section">
          <h3><i class="fas fa-cog"></i> Configuration</h3>
          
          <div class="form-row">
            <div class="form-group">
              <label for="ordre">Ordre d'affichage</label>
              <input
                id="ordre"
                v-model.number="form.ordre"
                type="number"
                class="form-control"
                min="0"
                placeholder="0"
              >
              <small class="form-help">Plus le nombre est petit, plus le pays apparaît en premier</small>
            </div>

            <div class="form-group">
              <div class="checkbox-group">
                <label class="checkbox-label">
                  <input
                    v-model="form.est_actif"
                    type="checkbox"
                    class="checkbox-input"
                  >
                  <span class="checkbox-custom"></span>
                  Pays actif
                </label>
                <small class="form-help">Les pays inactifs ne sont pas visibles aux utilisateurs</small>
              </div>
            </div>
          </div>
        </div>

        <!-- Prévisualisation -->
        <div v-if="form.nom || form.drapeau_emoji" class="form-section preview-section">
          <h3><i class="fas fa-eye"></i> Aperçu</h3>
          <div class="pays-preview">
            <span class="preview-flag">{{ form.drapeau_emoji || '🏳️' }}</span>
            <div class="preview-info">
              <strong>{{ form.nom || 'Nom du pays' }}</strong>
              <small v-if="form.code_iso">[{{ form.code_iso }}]</small>
              <p v-if="form.description">{{ form.description }}</p>
            </div>
            <span v-if="!form.est_actif" class="preview-status inactive">Inactif</span>
            <span v-else class="preview-status active">Actif</span>
          </div>
        </div>
      </form>

      <div class="modal-footer">
        <button @click="$emit('cancel')" type="button" class="btn btn-secondary">
          <i class="fas fa-times"></i>
          Annuler
        </button>
        <button @click="handleSubmit" type="submit" class="btn btn-primary" :disabled="!isFormValid">
          <i class="fas fa-save"></i>
          {{ mode === 'create' ? 'Créer le pays' : 'Sauvegarder' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue'

export default {
  name: 'PaysModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    pays: {
      type: Object,
      default: null
    },
    mode: {
      type: String,
      default: 'create', // 'create' or 'edit'
      validator: value => ['create', 'edit'].includes(value)
    }
  },
  emits: ['save', 'cancel'],
  setup(props, { emit }) {
    const form = ref({
      nom: '',
      code_iso: '',
      drapeau_emoji: '',
      description: '',
      ordre: 0,
      est_actif: true
    })

    const errors = ref({})

    // Initialiser le formulaire avec les données du pays (en mode édition)
    const initializeForm = () => {
      if (props.mode === 'edit' && props.pays) {
        form.value = {
          nom: props.pays.nom || '',
          code_iso: props.pays.code_iso || '',
          drapeau_emoji: props.pays.drapeau_emoji || '',
          description: props.pays.description || '',
          ordre: props.pays.ordre || 0,
          est_actif: props.pays.est_actif !== undefined ? props.pays.est_actif : true
        }
      } else {
        // Mode création - réinitialiser le formulaire
        form.value = {
          nom: '',
          code_iso: '',
          drapeau_emoji: '',
          description: '',
          ordre: 0,
          est_actif: true
        }
      }
      errors.value = {}
    }

    // Validation du formulaire
    const validateForm = () => {
      const newErrors = {}

      if (!form.value.nom.trim()) {
        newErrors.nom = 'Le nom du pays est requis'
      } else if (form.value.nom.length < 2) {
        newErrors.nom = 'Le nom doit contenir au moins 2 caractères'
      }

      if (!form.value.code_iso.trim()) {
        newErrors.code_iso = 'Le code ISO est requis'
      } else if (!/^[A-Z]{2,3}$/.test(form.value.code_iso)) {
        newErrors.code_iso = 'Le code ISO doit contenir 2-3 lettres majuscules'
      }

      errors.value = newErrors
      return Object.keys(newErrors).length === 0
    }

    const isFormValid = computed(() => {
      return form.value.nom.trim() && 
             form.value.code_iso.trim() && 
             /^[A-Z]{2,3}$/.test(form.value.code_iso)
    })

    // Soumettre le formulaire
    const handleSubmit = () => {
      if (!validateForm()) {
        return
      }

      const formData = {
        nom: form.value.nom.trim(),
        code_iso: form.value.code_iso.trim().toUpperCase(),
        drapeau_emoji: form.value.drapeau_emoji.trim(),
        description: form.value.description.trim(),
        ordre: form.value.ordre || 0,
        est_actif: form.value.est_actif
      }

      emit('save', formData)
    }

    // Gérer le clic sur l'overlay
    const handleOverlayClick = () => {
      emit('cancel')
    }

    // Auto-majuscules pour le code ISO
    watch(() => form.value.code_iso, (newValue) => {
      form.value.code_iso = newValue.toUpperCase()
    })

    // Réinitialiser quand les props changent
    watch([() => props.visible, () => props.pays, () => props.mode], () => {
      if (props.visible) {
        initializeForm()
      }
    })

    onMounted(() => {
      if (props.visible) {
        initializeForm()
      }
    })

    return {
      form,
      errors,
      isFormValid,
      handleSubmit,
      handleOverlayClick,
      validateForm
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-50px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25px 30px;
  border-bottom: 2px solid #f1f3f4;
  background: #f8f9fa;
  border-radius: 12px 12px 0 0;
}

.modal-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.25rem;
  color: #6c757d;
  cursor: pointer;
  padding: 5px;
  border-radius: 4px;
  transition: all 0.3s;
}

.modal-close:hover {
  background: #e9ecef;
  color: #495057;
}

.modal-body {
  padding: 30px;
}

.form-section {
  margin-bottom: 30px;
}

.form-section:last-child {
  margin-bottom: 0;
}

.form-section h3 {
  margin: 0 0 20px 0;
  color: #495057;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  padding-bottom: 10px;
  border-bottom: 2px solid #f1f3f4;
}

.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #495057;
}

.form-group label.required::after {
  content: ' *';
  color: #dc3545;
}

.form-control {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
  box-sizing: border-box;
}

.form-control:focus {
  outline: none;
  border-color: #007cba;
  box-shadow: 0 0 0 3px rgba(0, 124, 186, 0.1);
}

.form-control.error {
  border-color: #dc3545;
}

.form-control.error:focus {
  box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.1);
}

.emoji-input {
  text-align: center;
  font-size: 1.5rem;
}

.error-message {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 5px;
  display: block;
}

.form-help {
  color: #6c757d;
  font-size: 0.875rem;
  margin-top: 5px;
  display: block;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  font-weight: 600;
}

.checkbox-input {
  display: none;
}

.checkbox-custom {
  width: 20px;
  height: 20px;
  border: 2px solid #e9ecef;
  border-radius: 4px;
  position: relative;
  transition: all 0.3s;
}

.checkbox-input:checked + .checkbox-custom {
  background: #007cba;
  border-color: #007cba;
}

.checkbox-input:checked + .checkbox-custom::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-weight: bold;
  font-size: 0.875rem;
}

.preview-section {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
}

.pays-preview {
  display: flex;
  align-items: center;
  gap: 15px;
  background: white;
  padding: 15px 20px;
  border-radius: 8px;
  border: 2px solid #e9ecef;
}

.preview-flag {
  font-size: 2rem;
}

.preview-info {
  flex: 1;
}

.preview-info strong {
  display: block;
  color: #2c3e50;
  font-size: 1.1rem;
}

.preview-info small {
  color: #6c757d;
  margin-left: 8px;
}

.preview-info p {
  margin: 5px 0 0 0;
  color: #6c757d;
  font-size: 0.9rem;
}

.preview-status {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.preview-status.active {
  background: #d4edda;
  color: #155724;
}

.preview-status.inactive {
  background: #f8d7da;
  color: #721c24;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  padding: 25px 30px;
  border-top: 2px solid #f1f3f4;
  background: #f8f9fa;
  border-radius: 0 0 12px 12px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
  font-size: 1rem;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #007cba;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #005a87;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
}

@media (max-width: 768px) {
  .modal-container {
    margin: 10px;
    max-height: calc(100vh - 20px);
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .modal-header,
  .modal-body,
  .modal-footer {
    padding: 20px;
  }
  
  .modal-footer {
    flex-direction: column;
  }
  
  .btn {
    justify-content: center;
  }
}
</style>
