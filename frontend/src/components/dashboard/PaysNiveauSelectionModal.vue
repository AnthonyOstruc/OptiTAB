<template>
  <Teleport to="body">
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
        <div v-if="selectionRestricted" class="lock-banner">
          <svg class="lock-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="11" width="18" height="10" rx="2"/>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
          </svg>
          <div class="lock-texts">
            <p class="lock-title">Niveau verrouillé</p>
            <p class="lock-text">
              Niveaux disponibles avec votre abonnement : {{ restrictedLabels }}. Contactez l'équipe OptiTAB pour en ajouter d'autres.
            </p>
          </div>
        </div>
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
            <button 
              type="button" 
              class="role-btn" 
              :class="{ active: selectedRole === 'parent' }" 
              @click="selectRole('parent')"
            >
              Parent
            </button>
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
  </Teleport>
</template>

<script setup>
import { watch, onMounted, onUnmounted, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { lockBodyScroll, unlockBodyScroll } from '@/utils/bodyScrollLock'
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
  },
  selectionRestricted: {
    type: Boolean,
    default: false
  },
  restrictedLevels: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue', 'select-pays', 'select-niveau', 'select-role', 'save', 'prefetch-niveaux'])

// Store utilisateur pour vérifier les permissions admin
const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin)

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

const restrictedLevels = computed(() => props.restrictedLevels || [])
const selectionRestricted = computed(() => props.selectionRestricted && restrictedLevels.value.length > 0)
const restrictedLabels = computed(() => {
  if (!restrictedLevels.value.length) return 'actuel'
  return restrictedLevels.value.map(level => level.label).join(', ')
})

const prefetchNiveaux = (pays) => {
  emit('prefetch-niveaux', pays?.id || pays)
}

const selectedRole = computed(() => props.selectedRole)
const selectRole = (role) => emit('select-role', role)

// Empêcher le scroll de l'arrière-plan quand le modal est ouvert
watch(() => props.modelValue, (isOpen) => {
  if (isOpen) {
    lockBodyScroll('pays-niveau-selection-modal', { mode: 'fixed' })
  } else {
    unlockBodyScroll('pays-niveau-selection-modal')
  }
}, { immediate: false })

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
  unlockBodyScroll('pays-niveau-selection-modal')
})
</script>

<style scoped>
.config-modal-overlay {
  position: fixed;
  inset: 0;
  width: 100%;
  min-height: 100vh;
  min-height: 100dvh;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  z-index: 99999;
  padding: clamp(0.75rem, 2vh, 2.5rem) clamp(0.75rem, 4vw, 2rem) calc(env(safe-area-inset-bottom) + 1.5rem);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  animation: fadeIn 0.3s ease-out;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior: contain;
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
  width: min(680px, 100%);
  max-height: min(90vh, calc(100dvh - 3rem));
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: slideIn 0.3s ease-out;
  transform-origin: center;
  position: relative;
  z-index: 100000;
  display: flex;
  flex-direction: column;
  -webkit-overflow-scrolling: touch;
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
  gap: 1rem;
}

.title-wrap {
  flex: 1;
  min-width: 0;
}

.config-modal-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.title-wrap .subtitle {
  margin: 6px 0 0 0;
  color: #6b7280;
  font-size: 14px;
  line-height: 1.5;
  word-wrap: break-word;
  overflow-wrap: break-word;
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
  padding: 0 24px 24px;
  flex: 1 1 auto;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.lock-banner {
  display: flex;
  gap: 1rem;
  padding: 1rem 1.25rem;
  margin-bottom: 1.5rem;
  border: 1px solid #c7d2fe;
  border-radius: 12px;
  background: #eef2ff;
  color: #1e1b4b;
}

.lock-icon {
  width: 32px;
  height: 32px;
  color: #4c1d95;
  flex-shrink: 0;
}

.lock-texts {
  flex: 1;
}

.lock-title {
  margin: 0;
  font-weight: 600;
  font-size: 0.95rem;
  color: #312e81;
}

.lock-text {
  margin: 0.15rem 0 0;
  font-size: 0.9rem;
  color: #4338ca;
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
  padding: 12px 24px 18px;
}

.progress-step {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #9ca3af;
}

.progress-step .circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  font-weight: 600;
  font-size: 0.95rem;
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
      padding: 0.75rem clamp(0.75rem, 6vw, 1.25rem) calc(env(safe-area-inset-bottom) + 1.25rem);
    }
    
    .config-modal-content {
      margin: 0.5rem auto;
      max-height: calc(100dvh - 2.75rem);
      border-radius: 12px;
    }
    
    .config-modal-header {
      padding: 1.125rem 1.125rem 0;
      margin-bottom: 0.75rem;
    }

    .config-modal-header h3 {
      font-size: 1.125rem;
      line-height: 1.3;
    }

    .title-wrap .subtitle {
      font-size: 0.8125rem;
      margin-top: 0.375rem;
    }

    .close-btn {
      width: 28px;
      height: 28px;
      font-size: 1.125rem;
    }

    .progress {
      padding: 0.75rem 1.125rem 1rem;
      gap: 0.5rem;
    }

    .progress-step .label {
      font-size: 0.75rem;
    }

    .progress-step .circle {
      width: 28px;
      height: 28px;
      font-size: 0.9rem;
    }

    .line {
      width: 40px;
    }
    
    .config-modal-body {
      padding: 0 1.125rem;
    }

    .config-step {
      margin-bottom: 1.5rem;
    }

    .config-step h4 {
      font-size: 1rem;
      gap: 0.625rem;
    }

    .step-number {
      width: 24px;
      height: 24px;
      font-size: 0.8125rem;
    }

    .config-step p {
      font-size: 0.875rem;
      margin-bottom: 1rem;
    }
    
    .config-modal-footer {
      padding: 1.125rem;
      gap: 0.625rem;
    }

    .btn-secondary,
    .btn-primary {
      padding: 0.625rem 1.125rem;
      font-size: 0.875rem;
    }
    
    .options-grid {
      grid-template-columns: 1fr;
      gap: 0.75rem;
    }

    .role-options {
      gap: 0.625rem;
    }

    .role-btn {
      font-size: 0.875rem;
      padding: 0.625rem 1rem;
    }

    /* Optimisation de la bannière de verrouillage pour mobile */
    .lock-banner {
      flex-direction: row;
      align-items: flex-start;
      gap: 0.625rem;
      padding: 0.75rem;
      margin-bottom: 1rem;
      border-radius: 0.625rem;
    }

    .lock-icon {
      width: 22px;
      height: 22px;
      flex-shrink: 0;
      margin-top: 0.125rem;
    }

    .lock-texts {
      flex: 1;
      min-width: 0;
      overflow-wrap: break-word;
      word-wrap: break-word;
    }

    .lock-title {
      font-size: 0.875rem;
      line-height: 1.3;
      margin-bottom: 0.25rem;
      font-weight: 600;
    }

    .lock-text {
      font-size: 0.8125rem;
      line-height: 1.4;
      margin: 0;
      overflow-wrap: break-word;
      word-wrap: break-word;
    }
  }

  @media (max-width: 640px) {
    .config-modal-overlay {
      padding: 0.5rem clamp(0.75rem, 8vw, 1.25rem) calc(env(safe-area-inset-bottom) + 1rem);
    }

    .config-modal-content {
      max-height: calc(100dvh - 2.5rem);
      margin: 0.4rem auto;
    }
  }

  @media (max-width: 480px) {
    .config-modal-overlay {
      padding: 0.5rem clamp(0.5rem, 8vw, 1rem) calc(env(safe-area-inset-bottom) + 0.875rem);
    }

    .config-modal-content {
      border-radius: 10px;
      max-height: calc(100dvh - 2.25rem);
      margin: 0.375rem auto;
    }

    .config-modal-header {
      padding: 1rem 1rem 0;
      margin-bottom: 0.625rem;
    }

    .config-modal-header h3 {
      font-size: 1.0625rem;
    }

    .title-wrap .subtitle {
      font-size: 0.75rem;
      margin-top: 0.3rem;
      line-height: 1.4;
    }

    .close-btn {
      width: 26px;
      height: 26px;
      font-size: 1rem;
    }

    .progress {
      padding: 0.75rem 1rem 0.9rem;
      gap: 0.375rem;
      flex-wrap: nowrap;
      overflow-x: auto;
    }

    .progress-step {
      gap: 0.375rem;
      white-space: nowrap;
    }

    .progress-step .label {
      font-size: 0.6875rem;
    }

    .progress-step .circle {
      width: 26px;
      height: 26px;
      font-size: 0.85rem;
    }

    .line {
      width: 30px;
      min-width: 30px;
    }

    .config-modal-body {
      padding: 0 1rem;
    }

    .config-step {
      margin-bottom: 1.25rem;
    }

    .config-step h4 {
      font-size: 0.9375rem;
      gap: 0.5rem;
    }

    .step-number {
      width: 22px;
      height: 22px;
      font-size: 0.75rem;
    }

    .config-step p {
      font-size: 0.8125rem;
      margin-bottom: 0.875rem;
      line-height: 1.4;
    }

    .config-modal-footer {
      padding: 1rem;
      gap: 0.5rem;
      flex-wrap: wrap;
    }

    .btn-secondary,
    .btn-primary {
      padding: 0.5625rem 1rem;
      font-size: 0.8125rem;
      flex: 1;
      min-width: calc(50% - 0.25rem);
    }

    .options-grid {
      gap: 0.625rem;
    }

    .role-options {
      gap: 0.5rem;
      flex-wrap: wrap;
    }

    .role-btn {
      font-size: 0.8125rem;
      padding: 0.5625rem 0.875rem;
      flex: 1;
    }

    /* Optimisation supplémentaire pour très petits écrans */
    .lock-banner {
      gap: 0.5rem;
      padding: 0.625rem;
      border-radius: 0.5rem;
    }

    .lock-icon {
      width: 20px;
      height: 20px;
    }

    .lock-title {
      font-size: 0.8125rem;
      margin-bottom: 0.1875rem;
      font-weight: 600;
    }

    .lock-text {
      font-size: 0.75rem;
      line-height: 1.35;
      overflow-wrap: break-word;
      word-wrap: break-word;
    }

    .empty-state {
      padding: 1.25rem;
      font-size: 0.875rem;
    }
  }

  @media (max-width: 380px) {
    .config-modal-overlay {
      padding: 0.375rem;
      padding-bottom: 115px;
    }

    .config-modal-content {
      max-height: calc(100vh - 150px);
      margin: 0.25rem auto;
    }

    .config-modal-header {
      padding: 0.875rem 0.875rem 0;
      gap: 0.625rem;
    }

    .config-modal-header h3 {
      font-size: 1rem;
    }

    .title-wrap .subtitle {
      font-size: 0.6875rem;
      margin-top: 0.25rem;
    }

    .close-btn {
      width: 24px;
      height: 24px;
      font-size: 0.9375rem;
      flex-shrink: 0;
    }

    .progress {
      padding: 0 0.875rem 0.625rem;
      gap: 0.3rem;
    }

    .progress-step .label {
      font-size: 0.625rem;
    }

    .progress-step .circle {
      width: 20px;
      height: 20px;
      font-size: 0.6875rem;
    }

    .line {
      width: 24px;
      min-width: 24px;
    }

    .config-modal-body {
      padding: 0 0.875rem;
    }

    .config-step h4 {
      font-size: 0.875rem;
      gap: 0.4rem;
    }

    .step-number {
      width: 20px;
      height: 20px;
      font-size: 0.6875rem;
    }

    .config-step p {
      font-size: 0.75rem;
      margin-bottom: 0.75rem;
    }

    .config-modal-footer {
      padding: 0.875rem;
    }

    .btn-secondary,
    .btn-primary {
      padding: 0.5rem 0.875rem;
      font-size: 0.75rem;
    }

    .role-btn {
      font-size: 0.75rem;
      padding: 0.5rem 0.75rem;
    }

    .lock-banner {
      padding: 0.5rem;
    }

    .lock-icon {
      width: 18px;
      height: 18px;
    }

    .lock-title {
      font-size: 0.75rem;
    }

    .lock-text {
      font-size: 0.6875rem;
    }

    .empty-state {
      padding: 1rem;
      font-size: 0.8125rem;
    }
  }

  /* S'assurer que le modal est en premier plan */
  .config-modal-overlay {
    pointer-events: auto;
    touch-action: none;
    overscroll-behavior: contain;
    -webkit-overflow-scrolling: touch;
  }

  .config-modal-overlay * {
    pointer-events: auto;
  }

  /* Améliorer l'accessibilité */
  .config-modal-overlay:focus {
    outline: none;
  }

  .config-modal-content {
    pointer-events: auto;
    touch-action: auto;
    overscroll-behavior: contain;
  }

  .config-modal-content:focus {
    outline: none;
  }

  /* Empêcher les interactions avec l'arrière-plan */
  .config-modal-overlay {
    isolation: isolate;
    -webkit-tap-highlight-color: transparent;
  }

  /* Empêcher le zoom sur mobile */
  .config-modal-content input,
  .config-modal-content select,
  .config-modal-content textarea {
    touch-action: manipulation;
  }
</style>
