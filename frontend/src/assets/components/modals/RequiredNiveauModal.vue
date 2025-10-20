<template>
  <Modal :is-open="isOpen" :can-close="false">
    <template #header>
      <div class="modal-header">
        <h2>🎓 Bienvenue sur OptiTAB !</h2>
        <p class="modal-subtitle">Pour commencer votre apprentissage, veuillez sélectionner votre niveau scolaire</p>
      </div>
    </template>
    
    <template #body>
      <div class="niveaux-selection">

        
        <div v-if="niveaux.length === 0" class="loading-niveaux">
          <p>Chargement des niveaux...</p>
        </div>
        <div v-else class="niveaux-grid">
          <div class="debug-info">
            <p>Niveaux disponibles: {{ niveaux.length }}</p>
          </div>
          <div 
            v-for="niveau in niveaux" 
            :key="niveau.id"
            class="niveau-card"
            :class="{ selected: selectedNiveauId === niveau.id }"
            @click="selectNiveau(niveau)"
          >
            <div class="niveau-color" :style="{ backgroundColor: niveau.couleur }"></div>
            <div class="niveau-info">
              <h3>{{ niveau.nom }}</h3>
              <p>Niveau scolaire</p>
              <div class="niveau-stats">
                <span>Contenu adapté</span>
                <span>Exercices personnalisés</span>
              </div>
            </div>
            <div v-if="selectedNiveauId === niveau.id" class="selected-indicator">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </template>
    
    <template #footer>
      <div class="modal-footer">
        <button 
          @click="saveNiveau" 
          class="btn-primary"
          :disabled="!selectedNiveauId || saving"
        >
          <span v-if="saving" class="loading-spinner"></span>
          <span v-else>Commencer avec ce niveau</span>
        </button>
      </div>
    </template>
  </Modal>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToast } from '@/composables/useToast'
import Modal from '@/components/common/Modal.vue'
import { getNiveaux } from '@/api/niveaux.js'
import { updateUserNiveau } from '@/api/users.js'

export default {
  name: 'RequiredNiveauModal',
  components: {
    Modal
  },
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  emits: ['niveau-selected'],
  setup(props, { emit }) {
    const userStore = useUserStore()
    const { showToast } = useToast()
    
    const niveaux = ref([])
    const selectedNiveauId = ref(null)
    const saving = ref(false)

    // Computed
    const userNiveau = computed(() => userStore.niveau_pays)

    // Methods
    const loadNiveaux = async () => {
      try {
        console.log('🔄 Chargement des niveaux...')
        const data = await getNiveaux()
        console.log('✅ Niveaux chargés:', data)
        niveaux.value = data
      } catch (error) {
        console.error('❌ Error loading niveaux:', error)
        showToast('Erreur lors du chargement des niveaux', 'error')
      }
    }

    const selectNiveau = (niveau) => {
      selectedNiveauId.value = niveau.id
    }

    const saveNiveau = async () => {
      if (!selectedNiveauId.value) return
      
      try {
        saving.value = true
        await updateUserNiveau(selectedNiveauId.value)
        
        // Mettre à jour le store
        await userStore.fetchUser()
        
        showToast('Niveau enregistré avec succès !', 'success')
        emit('niveau-selected')
      } catch (error) {
        console.error('Error saving niveau:', error)
        showToast('Erreur lors de l\'enregistrement du niveau', 'error')
      } finally {
        saving.value = false
      }
    }

    onMounted(() => {
      console.log('🎯 RequiredNiveauModal mounted, isOpen:', props.isOpen)
      console.log('🎯 Niveaux au montage:', niveaux.value)
      loadNiveaux()
    })
    
    // Surveiller les changements de props
    watch(() => props.isOpen, (newValue) => {
      console.log('👀 Modal isOpen changé:', newValue)
    })

    return {
      niveaux,
      selectedNiveauId,
      saving,
      userNiveau,
      selectNiveau,
      saveNiveau
    }
  }
}
</script>

<style scoped>
.required-niveau-modal {
  max-width: 800px;
}

.modal-header {
  text-align: center;
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

.niveaux-selection {
  padding: 1rem 0;
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

.niveau-card h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
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
  top: 0.75rem;
  right: 0.75rem;
  background: #3b82f6;
  color: white;
  width: 32px;
  height: 32px;
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

@keyframes spin {
  to { transform: rotate(360deg); }
}



.loading-niveaux {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

.debug-info {
  background: #f3f4f6;
  padding: 0.5rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  text-align: center;
  font-size: 0.875rem;
  color: #6b7280;
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