<template>
  <Modal :is-open="isOpen" :can-close="false" :show-header="false">
    <div class="pays-niveau-selector">
      <!-- Header avec progression -->
      <div class="modal-header">
        <div class="progress-bar">
          <div class="progress-step" :class="{ active: currentStep >= 1, completed: currentStep > 1 }">
            <span class="step-number">1</span>
            <span class="step-label">Pays</span>
          </div>
          <div class="progress-line" :class="{ completed: currentStep > 1 }"></div>
          <div class="progress-step" :class="{ active: currentStep >= 2, completed: currentStep > 2 }">
            <span class="step-number">2</span>
            <span class="step-label">Niveau</span>
          </div>
        </div>
        <h2>🎓 Configuration de votre profil d'apprentissage</h2>
        <p class="modal-subtitle">{{ getStepSubtitle() }}</p>
      </div>

      <!-- Étape 1: Sélection du pays -->
      <div v-if="currentStep === 1" class="step-content">
        <div class="section-header">
          <h3>📍 Sélectionnez votre pays</h3>
          <p>Choisissez votre pays pour personnaliser le contenu selon votre système éducatif</p>
        </div>

        <div v-if="loadingPays" class="loading-state">
          <div class="spinner"></div>
          <p>Chargement des pays disponibles...</p>
        </div>

        <div v-else-if="errorPays" class="error-state">
          <p>❌ Erreur lors du chargement des pays</p>
          <button @click="loadPays" class="btn-retry">Réessayer</button>
        </div>

        <div v-else class="pays-grid">
          <div 
            v-for="pays in paysDisponibles" 
            :key="pays.id"
            class="pays-card"
            :class="{ selected: selectedPaysId === pays.id }"
            @click="selectPays(pays)"
          >
            <div class="pays-flag">{{ pays.drapeau_emoji }}</div>
            <div class="pays-info">
              <h4>{{ pays.nom }}</h4>
              <p>{{ pays.nombre_niveaux || 0 }} niveaux disponibles</p>
            </div>
            <div v-if="selectedPaysId === pays.id" class="selected-indicator">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
        </div>

        <div class="step-actions">
          <button 
            @click="nextStep" 
            :disabled="!selectedPaysId || loadingNiveaux"
            class="btn-primary"
          >
            <span v-if="loadingNiveaux">Chargement...</span>
            <span v-else>Continuer</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Étape 2: Sélection du niveau -->
      <div v-if="currentStep === 2" class="step-content">
        <div class="section-header">
          <h3>📚 Sélectionnez votre niveau scolaire</h3>
          <p>Choisissez votre niveau pour {{ selectedPays?.nom }}</p>
        </div>

        <div v-if="loadingNiveaux" class="loading-state">
          <div class="spinner"></div>
          <p>Chargement des niveaux...</p>
        </div>

        <div v-else-if="niveaux.length === 0" class="empty-state">
          <p>Aucun niveau disponible pour ce pays</p>
        </div>

        <div v-else class="niveaux-grid">
          <div 
            v-for="niveau in niveaux" 
            :key="niveau.id"
            class="niveau-card"
            :class="{ selected: selectedNiveauId === niveau.id }"
            @click="selectNiveau(niveau)"
          >
            <div class="niveau-color" :style="{ backgroundColor: niveau.couleur || '#667eea' }"></div>
            <div class="niveau-info">
              <h4>{{ niveau.nom_local || niveau.nom }}</h4>
              <p>Niveau scolaire</p>
            </div>
            <div v-if="selectedNiveauId === niveau.id" class="selected-indicator">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
        </div>

        <div class="step-actions">
          <button @click="previousStep" class="btn-secondary">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Retour
          </button>
          <button 
            @click="saveConfiguration" 
            :disabled="!selectedNiveauId || saving"
            class="btn-primary"
          >
            <span v-if="saving">Enregistrement...</span>
            <span v-else>Terminer la configuration</span>
          </button>
        </div>
      </div>

      <!-- Étape 3: Confirmation -->
      <div v-if="currentStep === 3" class="step-content">
        <div class="confirmation-content">
          <div class="success-icon">✅</div>
          <h3>Configuration terminée !</h3>
          <p>Votre profil a été configuré avec succès.</p>
          <div class="configuration-summary">
            <div class="summary-item">
              <span class="label">Pays:</span>
              <span class="value">{{ selectedPays?.nom }}</span>
            </div>
            <div class="summary-item">
              <span class="label">Niveau:</span>
              <span class="value">{{ selectedNiveau?.nom_local || selectedNiveau?.nom }}</span>
            </div>
          </div>
          <p class="redirect-message">Vous allez être redirigé vers votre tableau de bord...</p>
        </div>
      </div>
    </div>
  </Modal>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToast } from '@/composables/useToast'
import Modal from '@/components/common/Modal.vue'
import { getPaysActifs, getPaysNiveaux } from '@/api/pays.js'
import { updateUserPaysNiveau } from '@/api/users.js'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['configuration-complete', 'close'])

const userStore = useUserStore()
const { showToast } = useToast()

// États réactifs
const currentStep = ref(1)
const paysDisponibles = ref([])
const niveaux = ref([])
const selectedPaysId = ref(null)
const selectedNiveauId = ref(null)
const loadingPays = ref(false)
const loadingNiveaux = ref(false)
const errorPays = ref(false)
const saving = ref(false)

// Computed
const selectedPays = computed(() => 
  paysDisponibles.value.find(p => p.id === selectedPaysId.value)
)

const selectedNiveau = computed(() => 
  niveaux.value.find(n => n.id === selectedNiveauId.value)
)

// Méthodes
const getStepSubtitle = () => {
  switch (currentStep.value) {
    case 1: return 'Étape 1 sur 2 - Choisissez votre pays'
    case 2: return 'Étape 2 sur 2 - Choisissez votre niveau'
    case 3: return 'Configuration terminée'
    default: return ''
  }
}

const loadPays = async () => {
  try {
    loadingPays.value = true
    errorPays.value = false
    
    const response = await getPaysActifs()
    paysDisponibles.value = response.data || response
    
  } catch (error) {
    console.error('Erreur lors du chargement des pays:', error)
    errorPays.value = true
    showToast('Erreur lors du chargement des pays', 'error')
  } finally {
    loadingPays.value = false
  }
}

const loadNiveauxPourPays = async (paysId) => {
  if (!paysId) {
    niveaux.value = []
    return
  }

  try {
    loadingNiveaux.value = true
    const response = await getPaysNiveaux(paysId)
    niveaux.value = response.data || response
  } catch (error) {
    console.error('Erreur lors du chargement des niveaux:', error)
    niveaux.value = []
    showToast('Erreur lors du chargement des niveaux', 'error')
  } finally {
    loadingNiveaux.value = false
  }
}

const selectPays = (pays) => {
  selectedPaysId.value = pays.id
  selectedNiveauId.value = null
}

const selectNiveau = (niveau) => {
  selectedNiveauId.value = niveau.id
}

const nextStep = () => {
  if (currentStep.value === 1 && selectedPaysId.value) {
    currentStep.value = 2
    loadNiveauxPourPays(selectedPaysId.value)
  }
}

const previousStep = () => {
  if (currentStep.value === 2) {
    currentStep.value = 1
    niveaux.value = []
    selectedNiveauId.value = null
  }
}

const saveConfiguration = async () => {
  if (!selectedPaysId.value || !selectedNiveauId.value) return
  
  try {
    saving.value = true
    
    await updateUserPaysNiveau(selectedPaysId.value, selectedNiveauId.value)
    
    // Mettre à jour le store utilisateur
    await userStore.fetchUser()
    
    // Passer à l'étape de confirmation
    currentStep.value = 3
    
    showToast('Configuration enregistrée avec succès !', 'success')
    
    // Attendre un peu puis émettre la fin
    setTimeout(() => {
      emit('configuration-complete')
    }, 2000)
    
  } catch (error) {
    console.error('Erreur lors de la sauvegarde:', error)
    showToast('Erreur lors de l\'enregistrement de la configuration', 'error')
  } finally {
    saving.value = false
  }
}

// Watchers
watch(() => props.isOpen, (isOpen) => {
  if (isOpen && paysDisponibles.value.length === 0) {
    loadPays()
  }
})

watch(selectedPaysId, (newPaysId) => {
  if (newPaysId && currentStep.value === 2) {
    loadNiveauxPourPays(newPaysId)
  }
})

// Lifecycle
onMounted(() => {
  if (props.isOpen) {
    loadPays()
  }
})
</script>

<style scoped>
.pays-niveau-selector {
  max-width: 800px;
  margin: 0 auto;
}

.modal-header {
  text-align: center;
  margin-bottom: 2rem;
}

.progress-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.step-number {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #e5e7eb;
  color: #6b7280;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.3s ease;
}

.progress-step.active .step-number {
  background-color: #667eea;
  color: white;
}

.progress-step.completed .step-number {
  background-color: #10b981;
  color: white;
}

.step-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

.progress-step.active .step-label {
  color: #667eea;
}

.progress-step.completed .step-label {
  color: #10b981;
}

.progress-line {
  width: 60px;
  height: 2px;
  background-color: #e5e7eb;
  margin: 0 1rem;
  transition: all 0.3s ease;
}

.progress-line.completed {
  background-color: #10b981;
}

.modal-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.modal-subtitle {
  color: #6b7280;
  font-size: 0.875rem;
}

.step-content {
  min-height: 400px;
}

.section-header {
  text-align: center;
  margin-bottom: 2rem;
}

.section-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.section-header p {
  color: #6b7280;
  font-size: 0.875rem;
}

.loading-state, .error-state, .empty-state {
  text-align: center;
  padding: 3rem 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top: 3px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.btn-retry {
  background-color: #667eea;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background-color 0.3s ease;
}

.btn-retry:hover {
  background-color: #5a67d8;
}

.pays-grid, .niveaux-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.pays-card, .niveau-card {
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.pays-card:hover, .niveau-card:hover {
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
}

.pays-card.selected, .niveau-card.selected {
  border-color: #667eea;
  background-color: #f8fafc;
}

.pays-flag {
  font-size: 2rem;
  flex-shrink: 0;
}

.niveau-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.pays-info, .niveau-info {
  flex: 1;
}

.pays-info h4, .niveau-info h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.pays-info p, .niveau-info p {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
}

.selected-indicator {
  color: #667eea;
  flex-shrink: 0;
}

.step-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-primary, .btn-secondary {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border: none;
}

.btn-primary {
  background-color: #667eea;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #5a67d8;
}

.btn-primary:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-secondary:hover {
  background-color: #e5e7eb;
}

.confirmation-content {
  text-align: center;
  padding: 3rem 1rem;
}

.success-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.confirmation-content h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.confirmation-content p {
  color: #6b7280;
  margin-bottom: 2rem;
}

.configuration-summary {
  background-color: #f8fafc;
  border-radius: 0.5rem;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.summary-item:not(:last-child) {
  border-bottom: 1px solid #e5e7eb;
}

.summary-item .label {
  font-weight: 500;
  color: #6b7280;
}

.summary-item .value {
  font-weight: 600;
  color: #1f2937;
}

.redirect-message {
  font-style: italic;
  color: #9ca3af;
}
</style>
