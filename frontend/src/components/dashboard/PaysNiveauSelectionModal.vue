<template>
  <div v-if="modelValue" class="config-modal-overlay" @click="closeModal">
    <div class="config-modal-content" @click.stop>
      <div class="config-modal-header">
        <div class="title-wrap">
          <h3>Modifier votre configuration</h3>
          <p class="subtitle">Personnalisez votre pays et votre niveau pour adapter tout le contenu.</p>
        </div>
        <button @click="closeModal" class="close-btn" aria-label="Fermer">×</button>
      </div>

      <!-- Barre de progression -->
      <div class="progress">
        <div class="progress-step" :class="{ active: currentStep === 'pays' || currentStep === 'niveau', completed: currentStep === 'niveau' && !!selectedPaysId }">
          <span class="circle">1</span>
          <span class="label">Pays</span>
        </div>
        <div class="line" :class="{ completed: currentStep === 'niveau' && !!selectedPaysId }"></div>
        <div class="progress-step" :class="{ active: currentStep === 'niveau' }">
          <span class="circle">2</span>
          <span class="label">Niveau</span>
        </div>
        <div class="line"></div>
        <div class="progress-step">
          <span class="circle">3</span>
          <span class="label">Rôle</span>
        </div>
      </div>
      
      <div class="config-modal-body">
        <!-- Étape 1: Sélection du pays -->
        <div class="config-step" :class="{ active: currentStep === 'pays' }">
          <h4>
            <span class="step-number">1</span>
            Sélectionnez votre pays
          </h4>
          <p>Choisissez votre pays pour adapter le contenu à votre système éducatif</p>

          <div v-if="!paysList || paysList.length === 0" class="empty-state">
            <p>Aucun pays disponible pour le moment.</p>
          </div>
          
          <div v-else class="options-grid">
            <SelectionCard
              v-for="pays in paysList"
              :key="pays.id"
              :item="pays"
              type="pays"
              :is-selected="selectedPaysId === pays.id"
              :is-current="userPays?.id === pays.id"
              :is-disabled="pays.nombre_niveaux === 0"
              @select="selectPays"
              @hover="prefetchNiveaux"
            />
          </div>
        </div>

        <!-- Étape 2: Sélection du niveau -->
        <div class="config-step" :class="{ active: currentStep === 'niveau' }" v-if="selectedPaysId">
          <h4>
            <span class="step-number">2</span>
            Sélectionnez votre niveau
          </h4>
          <p>Choisissez votre niveau scolaire pour du contenu adapté</p>

          <div v-if="loadingNiveaux" class="empty-state">
            <p>Chargement des niveaux...</p>
          </div>
          <div v-else-if="!filteredNiveaux || filteredNiveaux.length === 0" class="empty-state">
            <p>Aucun niveau disponible pour ce pays.</p>
          </div>
          
          <div v-else class="options-grid">
            <SelectionCard
              v-for="niveau in filteredNiveaux"
              :key="niveau.id"
              :item="niveau"
              type="niveau"
              :is-selected="selectedNiveauId === niveau.id"
              :is-current="userNiveau?.id === niveau.id"
              @select="selectNiveau"
            />
          </div>
        </div>

        <!-- Étape 3: Sélection du rôle -->
        <div class="config-step role-step">
          <h4>
            <span class="step-number">3</span>
            Vous êtes ?
          </h4>
          <p>Choisissez le type de compte pour personnaliser l'expérience.</p>
          <div class="role-options">
            <button type="button" class="role-btn" :class="{ active: selectedRole === 'student' }" @click="selectRole('student')">Élève</button>
            <button type="button" class="role-btn" :class="{ active: selectedRole === 'parent' }" @click="selectRole('parent')">Parent</button>
          </div>
        </div>
      </div>
      
      <div class="config-modal-footer">
        <button @click="closeModal" class="btn-secondary">Annuler</button>
        <button 
          @click="saveConfiguration" 
          class="btn-primary"
          :disabled="!canSave || saving"
        >
          <span v-if="saving">Sauvegarde...</span>
          <span v-else>Sauvegarder</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { watch, onMounted, onUnmounted, computed } from 'vue'
import SelectionCard from '@/components/common/SelectionCard.vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  paysList: {
    type: Array,
    default: () => []
  },
  filteredNiveaux: {
    type: Array,
    default: () => []
  },
  loadingNiveaux: {
    type: Boolean,
    default: false
  },
  selectedPaysId: {
    type: Number,
    default: null
  },
  selectedNiveauId: {
    type: Number,
    default: null
  },
  userPays: {
    type: Object,
    default: null
  },
  userNiveau: {
    type: Object,
    default: null
  },
  currentStep: {
    type: String,
    default: 'pays'
  },
  canSave: {
    type: Boolean,
    default: false
  },
  saving: {
    type: Boolean,
    default: false
  },
  selectedRole: {
    type: String,
    default: 'student'
  }
})

const emit = defineEmits(['update:modelValue', 'select-pays', 'select-niveau', 'select-role', 'save', 'prefetch-niveaux'])

const closeModal = () => {
  emit('update:modelValue', false)
}

const selectPays = (pays) => {
  emit('select-pays', pays)
}

const selectNiveau = (niveau) => {
  emit('select-niveau', niveau)
}

const saveConfiguration = () => {
  emit('save')
}

const prefetchNiveaux = (pays) => {
  emit('prefetch-niveaux', pays?.id || pays)
}

const selectedRole = computed(() => props.selectedRole)
const selectRole = (role) => emit('select-role', role)

// Empêcher le scroll de l'arrière-plan quand le modal est ouvert
watch(() => props.modelValue, (isOpen) => {
  if (isOpen) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

// Gestion de la touche Échap
const handleEscape = (event) => {
  if (event.key === 'Escape' && props.modelValue) {
    closeModal()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleEscape)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape)
  document.body.style.overflow = ''
})
</script>

<style scoped>
.config-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
  padding: 20px;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.config-modal-content {
  background: white;
  border-radius: 16px;
  max-width: 680px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: slideIn 0.3s ease-out;
  transform-origin: center;
  position: relative;
  z-index: 100000;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.config-modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 24px 24px 0;
  margin-bottom: 12px;
}

.config-modal-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #111827;
}

.title-wrap .subtitle {
  margin: 6px 0 0 0;
  color: #6b7280;
  font-size: 14px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  color: #9ca3af;
  cursor: pointer;
  padding: 4px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: #f3f4f6;
  color: #6b7280;
}

.config-modal-body {
  padding: 0 24px;
}

.config-step {
  margin-bottom: 32px;
  transition: opacity 0.3s ease;
}

.config-step.active {
  opacity: 1;
}

.config-step h4 {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.step-number {
  background: #3b82f6;
  color: white;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
}

.config-step p {
  margin: 0 0 20px 0;
  color: #6b7280;
  line-height: 1.5;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 12px;
}

.empty-state {
  padding: 24px;
  text-align: center;
  color: #6b7280;
  background: #f9fafb;
  border: 1px dashed #e5e7eb;
  border-radius: 12px;
}

.config-modal-footer {
  display: flex;
  gap: 12px;
  padding: 24px;
  justify-content: flex-end;
  border-top: 1px solid #f3f4f6;
}

.btn-secondary {
  background: #f9fafb;
  color: #374151;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: #f3f4f6;
}

.btn-primary {
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Progress bar */
.progress {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 0 24px 16px 24px;
}

.progress-step {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #9ca3af;
}

.progress-step .circle {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  font-weight: 600;
  font-size: 14px;
}

.progress-step.active .circle {
  background: #667eea;
  color: white;
}

.progress-step.completed .circle {
  background: #10b981;
}

.progress-step .label {
  font-size: 13px;
  font-weight: 500;
}

.line {
  height: 2px;
  width: 60px;
  background: #e5e7eb;
}

.line.completed {
  background: #10b981;
}

/* Role step */
.role-options {
  display: flex;
  gap: 12px;
}
.role-btn {
  border: 1px solid #d1d5db;
  background: #f9fafb;
  color: #111827;
  border-radius: 9999px;
  padding: 10px 16px;
  font-weight: 600;
  cursor: pointer;
}
.role-btn.active {
  background: #e0e7ff;
  border-color: #6366f1;
  color: #3730a3;
}

  @media (max-width: 768px) {
    .config-modal-overlay {
      padding: 10px;
    }
    
    .config-modal-content {
      margin: 0;
      max-height: 95vh;
    }
    
    .config-modal-header,
    .config-modal-body,
    .config-modal-footer {
      padding-left: 20px;
      padding-right: 20px;
    }
    
    .options-grid {
      grid-template-columns: 1fr;
    }
  }

  /* S'assurer que le modal est en premier plan */
  .config-modal-overlay {
    pointer-events: auto;
  }

  .config-modal-overlay * {
    pointer-events: auto;
  }

  /* Améliorer l'accessibilité */
  .config-modal-overlay:focus {
    outline: none;
  }

  .config-modal-content:focus {
    outline: none;
  }

  /* Empêcher les interactions avec l'arrière-plan */
  .config-modal-overlay {
    isolation: isolate;
  }
</style>
