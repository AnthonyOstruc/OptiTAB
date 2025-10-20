<template>
  <div class="pays-selector">
    <h3 class="selector-title">
      <span class="icon">🌍</span>
      Pays et système éducatif
    </h3>
    
    <div class="current-selection" v-if="userStore.user?.pays">
      <div class="current-pays">
        <span class="pays-flag">{{ userStore.user.pays.drapeau_emoji }}</span>
        <div class="pays-details">
          <h4>{{ userStore.user.pays.nom }}</h4>
          <p>Système éducatif actuel</p>
        </div>
        <button @click="showModal = true" class="btn-change">
          Changer
        </button>
      </div>
    </div>
    
    <div v-else class="no-selection">
      <p>Aucun pays sélectionné</p>
      <button @click="showModal = true" class="btn-primary">
        Sélectionner un pays
      </button>
    </div>

    <!-- Modal de sélection -->
    <Modal :is-open="showModal" @close="showModal = false">
      <div class="pays-modal">
        <h2>Sélectionnez votre pays</h2>
        <p class="modal-subtitle">
          Choisissez votre pays pour adapter le contenu à votre système éducatif
        </p>
        
        <div class="search-bar">
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Rechercher un pays..." 
            class="search-input"
          >
        </div>
        
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>Chargement des pays...</p>
        </div>
        
        <div v-else class="pays-list">
          <div 
            v-for="pays in filteredPays" 
            :key="pays.id"
            class="pays-item"
            :class="{ selected: selectedPaysId === pays.id }"
            @click="selectPays(pays)"
          >
            <span class="pays-flag">{{ pays.drapeau_emoji }}</span>
            <div class="pays-info">
              <h4>{{ pays.nom }}</h4>
              <p>{{ pays.nombre_niveaux }} niveaux disponibles</p>
            </div>
            <div v-if="selectedPaysId === pays.id" class="check-icon">
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
            @click="savePaysSelection" 
            :disabled="!selectedPaysId || saving"
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
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToast } from '@/composables/useToast'
import Modal from '@/components/common/Modal.vue'
import { getPaysActifs } from '@/api/pays.js'
import { updateUserPays } from '@/api/users.js'

export default {
  name: 'PaysSelector',
  components: {
    Modal
  },
  setup() {
    const userStore = useUserStore()
    const { showToast } = useToast()
    
    const showModal = ref(false)
    const loading = ref(false)
    const saving = ref(false)
    const searchQuery = ref('')
    const paysDisponibles = ref([])
    const selectedPaysId = ref(null)

    const filteredPays = computed(() => {
      if (!searchQuery.value) return paysDisponibles.value
      
      const query = searchQuery.value.toLowerCase()
      return paysDisponibles.value.filter(pays =>
        pays.nom.toLowerCase().includes(query) ||
        pays.code_iso.toLowerCase().includes(query)
      )
    })

    const loadPays = async () => {
      try {
        loading.value = true
        const data = await getPaysActifs()
        paysDisponibles.value = data
      } catch (error) {
        console.error('Error loading pays:', error)
        showToast('Erreur lors du chargement des pays', 'error')
      } finally {
        loading.value = false
      }
    }

    const selectPays = (pays) => {
      selectedPaysId.value = pays.id
    }

    const savePaysSelection = async () => {
      if (!selectedPaysId.value) return
      
      try {
        saving.value = true
        await updateUserPays(selectedPaysId.value)
        await userStore.fetchUser()
        
        showToast('Pays mis à jour avec succès', 'success')
        showModal.value = false
        selectedPaysId.value = null
        searchQuery.value = ''
      } catch (error) {
        console.error('Error updating user pays:', error)
        showToast('Erreur lors de la mise à jour du pays', 'error')
      } finally {
        saving.value = false
      }
    }

    // Charger les pays à l'ouverture de la modal
    watch(showModal, (isOpen) => {
      if (isOpen && paysDisponibles.value.length === 0) {
        loadPays()
      }
      if (!isOpen) {
        selectedPaysId.value = null
        searchQuery.value = ''
      }
    })

    onMounted(() => {
      // Précharger les pays si nécessaire
      if (userStore.user?.pays) {
        loadPays()
      }
    })

    return {
      userStore,
      showModal,
      loading,
      saving,
      searchQuery,
      paysDisponibles,
      selectedPaysId,
      filteredPays,
      selectPays,
      savePaysSelection
    }
  }
}
</script>

<style scoped>
.pays-selector {
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

.current-pays {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 8px;
}

.pays-flag {
  font-size: 2rem;
}

.pays-details {
  flex: 1;
}

.pays-details h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.pays-details p {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
}

.no-selection {
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

.pays-modal {
  max-width: 500px;
  width: 100%;
}

.pays-modal h2 {
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

.search-bar {
  margin-bottom: 1rem;
}

.search-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.pays-list {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.pays-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
  border-bottom: 1px solid #e5e7eb;
}

.pays-item:last-child {
  border-bottom: none;
}

.pays-item:hover {
  background: #f9fafb;
}

.pays-item.selected {
  background: #eff6ff;
  border-color: #3b82f6;
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

.check-icon {
  color: #3b82f6;
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
