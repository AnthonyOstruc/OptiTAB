<template>
  <div class="niveau-selector">
    <h3 class="selector-title">
      <span class="icon">🎯</span>
      Niveau scolaire
    </h3>
    
    <div v-if="!userStore.user?.pays" class="no-pays">
      <p>⚠️ Veuillez d'abord sélectionner votre pays pour voir les niveaux disponibles</p>
    </div>
    
    <div v-else-if="userStore.user?.niveau" class="current-selection">
      <div class="current-niveau">
        <div class="niveau-color" :style="{ backgroundColor: userStore.user.niveau.couleur }"></div>
        <div class="niveau-details">
          <h4>{{ getNomLocalNiveau() }}</h4>
          <p>Niveau scolaire actuel</p>
        </div>
        <button @click="showModal = true" class="btn-change">
          Changer
        </button>
      </div>
    </div>
    
    <div v-else class="no-selection">
      <p>Aucun niveau sélectionné</p>
      <button @click="showModal = true" class="btn-primary">
        Sélectionner un niveau
      </button>
    </div>

    <!-- Modal de sélection -->
    <Modal :is-open="showModal" @close="showModal = false">
      <div class="niveau-modal">
        <h2>Sélectionnez votre niveau scolaire</h2>
        <p class="modal-subtitle">
          Choisissez votre niveau pour {{ userStore.user?.pays?.nom }}
        </p>
        
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>Chargement des niveaux...</p>
        </div>
        
        <div v-else-if="niveauxDisponibles.length === 0" class="no-niveaux">
          <p>Aucun niveau disponible pour votre pays</p>
        </div>
        
        <div v-else class="niveaux-grid">
          <div 
            v-for="niveau in niveauxDisponibles" 
            :key="niveau.id"
            class="niveau-card"
            :class="{ selected: selectedNiveauId === niveau.id }"
            @click="selectNiveau(niveau)"
          >
            <div class="niveau-color" :style="{ backgroundColor: niveau.couleur }"></div>
            <div class="niveau-info">
              <h4>{{ niveau.nom_local || niveau.nom }}</h4>
              <p>Niveau scolaire</p>
              <div class="niveau-stats">
                <span v-if="niveau.nombre_cours">{{ niveau.nombre_cours }} cours</span>
                <span v-if="niveau.nombre_exercices">{{ niveau.nombre_exercices }} exercices</span>
              </div>
            </div>
            <div v-if="selectedNiveauId === niveau.id" class="check-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
        </div>
        
        <div class="modal-actions">
          <button @click="showModal = false" class="btn-secondary">
            Annuler
          </button>
          <button 
            @click="saveNiveauSelection" 
            :disabled="!selectedNiveauId || saving"
            class="btn-primary"
          >
            <span v-if="saving">Enregistrement...</span>
            <span v-else>Confirmer</span>
          </button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script>
import { ref, watch, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToast } from '@/composables/useToast'
import Modal from '@/components/common/Modal.vue'
import { getPaysNiveaux } from '@/api/pays.js'
import { updateUserNiveau } from '@/api/users.js'

export default {
  name: 'NiveauSelector',
  components: {
    Modal
  },
  setup() {
    const userStore = useUserStore()
    const { showToast } = useToast()
    
    const showModal = ref(false)
    const loading = ref(false)
    const saving = ref(false)
    const niveauxDisponibles = ref([])
    const selectedNiveauId = ref(null)

    const getNomLocalNiveau = () => {
      if (!userStore.user?.niveau || !userStore.user?.pays) {
        return userStore.user?.niveau_pays?.nom || ''
      }
      
      // Essayer de récupérer le nom local depuis les niveaux disponibles
      const niveauLocal = niveauxDisponibles.value.find(n => n.id === userStore.user.niveau.id)
      return niveauLocal?.nom_local || userStore.user.niveau.nom
    }

    const loadNiveaux = async () => {
      if (!userStore.user?.pays?.id) {
        niveauxDisponibles.value = []
        return
      }

      try {
        loading.value = true
        const data = await getPaysNiveaux(userStore.user.pays.id)
        niveauxDisponibles.value = data
      } catch (error) {
        console.error('Error loading niveaux:', error)
        showToast('Erreur lors du chargement des niveaux', 'error')
        niveauxDisponibles.value = []
      } finally {
        loading.value = false
      }
    }

    const selectNiveau = (niveau) => {
      selectedNiveauId.value = niveau.id
    }

    const saveNiveauSelection = async () => {
      if (!selectedNiveauId.value) return
      
      try {
        saving.value = true
        await updateUserNiveau(selectedNiveauId.value)
        await userStore.fetchUser()
        
        showToast('Niveau mis à jour avec succès', 'success')
        showModal.value = false
        selectedNiveauId.value = null
      } catch (error) {
        console.error('Error updating user niveau:', error)
        showToast('Erreur lors de la mise à jour du niveau', 'error')
      } finally {
        saving.value = false
      }
    }

    // Charger les niveaux quand le pays change
    watch(() => userStore.user?.pays?.id, (newPaysId) => {
      if (newPaysId) {
        loadNiveaux()
      } else {
        niveauxDisponibles.value = []
      }
    }, { immediate: true })

    // Charger les niveaux à l'ouverture de la modal
    watch(showModal, (isOpen) => {
      if (isOpen && userStore.user?.pays?.id) {
        loadNiveaux()
      }
      if (!isOpen) {
        selectedNiveauId.value = null
      }
    })

    return {
      userStore,
      showModal,
      loading,
      saving,
      niveauxDisponibles,
      selectedNiveauId,
      getNomLocalNiveau,
      selectNiveau,
      saveNiveauSelection
    }
  }
}
</script>

<style scoped>
.niveau-selector {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.selector-title {
  margin: 0 0 1rem 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.icon {
  font-size: 1.25rem;
}

.current-niveau {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 8px;
}

.niveau-color {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.niveau-details {
  flex: 1;
}

.niveau-details h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.niveau-details p {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
}

.no-selection, .no-pays, .no-niveaux {
  text-align: center;
  padding: 1.5rem;
  color: #6b7280;
}

.btn-change {
  background: #e5e7eb;
  color: #374151;
  border: none;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-change:hover {
  background: #d1d5db;
}

.niveau-modal {
  max-width: 700px;
  width: 100%;
}

.niveau-modal h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
}

.modal-subtitle {
  margin: 0 0 1.5rem 0;
  color: #6b7280;
  line-height: 1.5;
}

.niveaux-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
  max-height: 400px;
  overflow-y: auto;
  padding: 0.5rem;
}

.niveau-card {
  position: relative;
  background: #fff;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.25rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.niveau-card:hover {
  border-color: #3b82f6;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.15);
}

.niveau-card.selected {
  border-color: #3b82f6;
  background: #eff6ff;
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.2);
}

.niveau-info {
  text-align: center;
}

.niveau-info h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

.niveau-info p {
  margin: 0 0 0.75rem 0;
  font-size: 0.875rem;
  color: #6b7280;
}

.niveau-stats {
  display: flex;
  justify-content: center;
  gap: 1rem;
  font-size: 0.8rem;
  color: #9ca3af;
}

.check-icon {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  color: #3b82f6;
  background: white;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn-primary, .btn-secondary {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #e5e7eb;
  color: #374151;
}

.btn-secondary:hover {
  background: #d1d5db;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e5e7eb;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
