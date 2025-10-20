<template>
  <Modal 
    :is-open="isOpen" 
    :can-close="true" 
    :show-header="false"
    @close="handleModalClose"
  >
    <div class="auto-niveau-modal">
      <!-- Header -->
      <div class="modal-header">
        <h2>🎓 Bienvenue sur OptiTAB !</h2>
        <p class="modal-subtitle">Pour commencer votre apprentissage, veuillez d'abord sélectionner votre pays, puis votre niveau scolaire</p>
      </div>
      
      <!-- Sélection du pays -->
      <div class="selection-section">
        <h3 class="section-title">📍 Sélectionnez votre pays</h3>
        <div v-if="loadingPays" class="loading-section">
          <div class="spinner"></div>
          <p>Chargement des pays...</p>
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
              <p>{{ pays.nombre_niveaux }} niveaux disponibles</p>
            </div>
            <div v-if="selectedPaysId === pays.id" class="selected-indicator">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Sélection du niveau -->
      <div class="selection-section" v-if="selectedPaysId">
        <h3 class="section-title">🎯 Sélectionnez votre niveau scolaire</h3>
        <div v-if="loadingNiveaux" class="loading-section">
          <div class="spinner"></div>
          <p>Chargement des niveaux...</p>
        </div>
        <div v-else-if="niveaux.length === 0" class="no-niveaux">
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
            <div class="niveau-color" :style="{ backgroundColor: niveau.couleur }"></div>
            <div class="niveau-info">
              <h4>{{ niveau.nom }}</h4>
              <p>Niveau scolaire</p>
              <div class="niveau-stats">
                <span v-if="niveau.nombre_cours">{{ niveau.nombre_cours }} cours</span>
                <span v-if="niveau.nombre_exercices">{{ niveau.nombre_exercices }} exercices</span>
              </div>
            </div>
            <div v-if="selectedNiveauId === niveau.id" class="selected-indicator">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Footer -->
      <div class="modal-footer">
        <button 
          @click="saveSelection" 
          class="btn-primary"
          :disabled="!selectedPaysId || !selectedNiveauId || saving"
        >
          <span v-if="saving" class="loading-spinner"></span>
          <span v-else>Commencer avec cette configuration</span>
        </button>
      </div>
    </div>
  </Modal>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToast } from '@/composables/useToast'
import Modal from '@/components/common/Modal.vue'
import { getPaysActifs, getPaysNiveaux } from '@/api/pays.js'
import { updateUserPaysNiveau } from '@/api/users.js'

export default {
  name: 'AutoNiveauModal',
  components: {
    Modal
  },
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  emits: ['niveau-selected', 'close'],
  setup(props, { emit }) {
    const userStore = useUserStore()
    const { showToast } = useToast()
    
    // États réactifs
    const paysDisponibles = ref([])
    const niveaux = ref([])
    const selectedPaysId = ref(null)
    const selectedNiveauId = ref(null)
    const loadingPays = ref(false)
    const loadingNiveaux = ref(false)
    const saving = ref(false)

    // Méthodes
    const loadPays = async () => {
      try {
        loadingPays.value = true
        const data = await getPaysActifs()
        paysDisponibles.value = data
      } catch (error) {
        console.error('Error loading pays:', error)
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
        const data = await getPaysNiveaux(paysId)
        niveaux.value = data
        // Réinitialiser la sélection de niveau si elle n'est plus valide
        if (selectedNiveauId.value && !data.some(n => n.id === selectedNiveauId.value)) {
          selectedNiveauId.value = null
        }
      } catch (error) {
        console.error('Error loading niveaux for pays:', error)
        showToast('Erreur lors du chargement des niveaux', 'error')
        niveaux.value = []
      } finally {
        loadingNiveaux.value = false
      }
    }

    const selectPays = (pays) => {
      selectedPaysId.value = pays.id
      selectedNiveauId.value = null // Réinitialiser le niveau
      loadNiveauxPourPays(pays.id)
    }

    const selectNiveau = (niveau) => {
      selectedNiveauId.value = niveau.id
    }

    const saveSelection = async () => {
      if (!selectedPaysId.value || !selectedNiveauId.value) return
      
      try {
        saving.value = true
        
        console.log('🔄 Sauvegarde de la configuration...', {
          paysId: selectedPaysId.value,
          niveauId: selectedNiveauId.value
        })
        
        await updateUserPaysNiveau(selectedPaysId.value, selectedNiveauId.value)
        
        console.log('✅ Configuration sauvegardée, mise à jour du store...')
        
        // Marquer la configuration comme terminée
        localStorage.setItem('configurationCompleted', 'true')
        localStorage.setItem('userConfiguration', JSON.stringify({
          pays_id: selectedPaysId.value,
          niveau_id: selectedNiveauId.value,
          timestamp: new Date().toISOString()
        }))
        
        // Mettre à jour le store
        await userStore.fetchUser()
        
        console.log('📊 Store mis à jour:', {
          pays: userStore.pays,
          niveau_pays: userStore.niveau_pays,
          isAuthenticated: userStore.isAuthenticated
        })
        
        showToast('Configuration enregistrée avec succès !', 'success')
        emit('niveau-selected')
        
        // Fermer le modal immédiatement
        console.log('🚪 Fermeture immédiate du modal...')
        emit('close')
        
      } catch (error) {
        console.error('❌ Error saving user configuration:', error)
        showToast('Erreur lors de l\'enregistrement de la configuration', 'error')
      } finally {
        saving.value = false
      }
    }

    // Surveiller l'ouverture du modal pour charger les pays
    watch(() => props.isOpen, (isOpen) => {
      if (isOpen && paysDisponibles.value.length === 0) {
        loadPays()
      }
    })

    // Surveiller le changement de pays pour charger les niveaux
    watch(selectedPaysId, (newPaysId) => {
      if (newPaysId) {
        loadNiveauxPourPays(newPaysId)
      }
    })

    onMounted(() => {
      if (props.isOpen) {
        loadPays()
      }
    })

    const handleModalClose = () => {
      emit('close')
    }

    return {
      paysDisponibles,
      niveaux,
      selectedPaysId,
      selectedNiveauId,
      loadingPays,
      loadingNiveaux,
      saving,
      selectPays,
      selectNiveau,
      saveSelection,
      handleModalClose
    }
  }
}
</script>

<style scoped>
.auto-niveau-modal {
  display: flex;
  flex-direction: column;
  height: 100%;
  max-width: 800px;
  width: 100%;
  margin: 0 auto;
}

.modal-header {
  text-align: center;
  margin-bottom: 2rem;
}

.modal-header h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.75rem;
  font-weight: 700;
  color: #1f2937;
}

.modal-subtitle {
  margin: 0;
  font-size: 1rem;
  color: #6b7280;
  line-height: 1.5;
}

.selection-section {
  margin-bottom: 2rem;
}

.section-title {
  margin: 0 0 1rem 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.loading-section {
  text-align: center;
  padding: 1.5rem;
  color: #6b7280;
}

.no-niveaux {
  text-align: center;
  padding: 1.5rem;
  color: #6b7280;
  font-style: italic;
}

/* Styles pour les pays */
.pays-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.pays-card {
  position: relative;
  background: #fff;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.pays-card:hover {
  border-color: #3b82f6;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.pays-card.selected {
  border-color: #3b82f6;
  background: #eff6ff;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}

.pays-flag {
  font-size: 2rem;
  line-height: 1;
}

.pays-info {
  flex: 1;
}

.pays-info h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.pays-info p {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.niveaux-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}

.niveau-card {
  position: relative;
  background: #fff;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
}

.niveau-card:hover {
  border-color: #3b82f6;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
}

.niveau-card.selected {
  border-color: #3b82f6;
  background: #eff6ff;
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2);
}

.niveau-card .niveau-color {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  margin: 0 auto 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.niveau-info h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  text-align: center;
}

.niveau-card p {
  margin: 0 0 1rem 0;
  color: #6b7280;
  font-size: 0.9rem;
  text-align: center;
  line-height: 1.4;
}

.niveau-stats {
  display: flex;
  justify-content: center;
  gap: 1rem;
  font-size: 0.8rem;
  color: #9ca3af;
}

.selected-indicator {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: #3b82f6;
  color: white;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: popIn 0.3s ease;
}

@keyframes popIn {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

.modal-footer {
  display: flex;
  justify-content: center;
  padding-top: 1rem;
  margin-top: auto;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.875rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 200px;
  justify-content: center;
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Responsive */
@media (max-width: 768px) {
  .niveaux-grid {
    grid-template-columns: 1fr;
  }
  
  .niveau-card {
    padding: 1.25rem;
  }
  
  .modal-header h2 {
    font-size: 1.5rem;
  }
}
</style> 