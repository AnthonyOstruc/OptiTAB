<template>
  <div class="niveau-selector">
    <div v-if="!userNiveau" class="niveau-welcome">
      <div class="welcome-content">
        <h2>Bienvenue sur OptiTAB !</h2>
        <p>Pour vous proposer le contenu le plus adapté, veuillez sélectionner votre niveau scolaire :</p>
        
        <div class="niveaux-grid">
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
              <p>{{ niveau.description }}</p>
              <div class="niveau-stats">
                <span>{{ niveau.nombre_matieres }} matières</span>
                <span>{{ niveau.nombre_cours }} cours</span>
              </div>
            </div>
          </div>
        </div>

        <button 
          @click="saveNiveau" 
          class="btn-primary"
          :disabled="!selectedNiveauId || saving"
        >
          <span v-if="saving">Enregistrement...</span>
          <span v-else>Commencer avec ce niveau</span>
        </button>
      </div>
    </div>

    <div v-else class="niveau-current">
      <div class="current-niveau">
        <div class="niveau-badge" :style="{ backgroundColor: userNiveau.couleur }">
          {{ userNiveau.nom }}
        </div>
        <button @click="openChangeModal" class="btn-secondary">
          Changer de niveau
        </button>
      </div>
    </div>

    <!-- Modal de changement de niveau -->
    <Modal :is-open="showChangeModal" @close="showChangeModal = false">
      <template #header>
        <h2>Changer de Niveau</h2>
      </template>
      
      <template #body>
        <p>Voulez-vous changer votre niveau scolaire ? Cela modifiera les contenus qui vous sont proposés.</p>
        
        <div class="niveaux-list">
          <div 
            v-for="niveau in niveaux" 
            :key="niveau.id"
            class="niveau-option"
            :class="{ 
              selected: selectedNiveauId === niveau.id,
              current: userNiveau?.id === niveau.id 
            }"
            @click="selectNiveau(niveau)"
          >
            <div class="niveau-color" :style="{ backgroundColor: niveau.couleur }"></div>
            <div class="niveau-info">
              <h4>{{ niveau.nom }}</h4>
              <p>{{ niveau.description }}</p>
            </div>
            <div v-if="userNiveau?.id === niveau.id" class="current-indicator">
              Niveau actuel
            </div>
          </div>
        </div>
      </template>
      
      <template #footer>
        <button @click="showChangeModal = false" class="btn-secondary">Annuler</button>
        <button 
          @click="changeNiveau" 
          class="btn-primary"
          :disabled="!selectedNiveauId || selectedNiveauId === userNiveau?.id || saving"
        >
          <span v-if="saving">Changement...</span>
          <span v-else>Changer de niveau</span>
        </button>
      </template>
    </Modal>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToast } from '@/composables/useToast'
import Modal from '@/components/common/Modal.vue'
import { getNiveaux } from '@/api/niveaux.js'
import { updateUserNiveau } from '@/api/users.js'

export default {
  name: 'NiveauSelector',
  components: {
    Modal
  },
  setup() {
    const userStore = useUserStore()
    const { showToast } = useToast()
    
    const niveaux = ref([])
    const selectedNiveauId = ref(null)
    const saving = ref(false)
    const showChangeModal = ref(false)

    // Computed
    const userNiveau = computed(() => userStore.niveau_pays)

    // Methods
    const loadNiveaux = async () => {
      try {
        console.log('Loading niveaux...')
        const data = await getNiveaux()
        console.log('Niveaux loaded:', data)
        niveaux.value = data
      } catch (error) {
        console.error('Error loading niveaux:', error)
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
      } catch (error) {
        showToast('Erreur lors de l\'enregistrement du niveau', 'error')
      } finally {
        saving.value = false
      }
    }

    const openChangeModal = () => {
      console.log('Opening change modal...')
      showChangeModal.value = true
      // Si l'utilisateur a déjà un niveau, le sélectionner par défaut
      if (userNiveau.value) {
        selectedNiveauId.value = userNiveau.value.id
      }
    }

    const changeNiveau = async () => {
      if (!selectedNiveauId.value || selectedNiveauId.value === userNiveau.value?.id) return
      
      try {
        saving.value = true
        await updateUserNiveau(selectedNiveauId.value)
        
        // Mettre à jour le store
        await userStore.fetchUser()
        
        showToast('Niveau changé avec succès !', 'success')
        showChangeModal.value = false
      } catch (error) {
        showToast('Erreur lors du changement de niveau', 'error')
      } finally {
        saving.value = false
      }
    }

    onMounted(() => {
      loadNiveaux()
      // Si l'utilisateur a déjà un niveau, le sélectionner par défaut
      if (userNiveau.value) {
        selectedNiveauId.value = userNiveau.value.id
      }
    })

    return {
      niveaux,
      selectedNiveauId,
      saving,
      showChangeModal,
      userNiveau,
      selectNiveau,
      saveNiveau,
      openChangeModal,
      changeNiveau
    }
  }
}
</script>

<style scoped>
.niveau-selector {
  width: 100%;
}

.niveau-welcome {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 3rem 2rem;
  text-align: center;
  color: white;
}

.welcome-content h2 {
  margin: 0 0 1rem 0;
  font-size: 2rem;
  font-weight: 700;
}

.welcome-content p {
  margin: 0 0 2rem 0;
  font-size: 1.1rem;
  opacity: 0.9;
}

.niveaux-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.niveau-card {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid transparent;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.niveau-card:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.niveau-card.selected {
  border-color: #fbbf24;
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(251, 191, 36, 0.3);
}

.niveau-card .niveau-color {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin: 0 auto 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.niveau-card h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.niveau-card p {
  margin: 0 0 1rem 0;
  opacity: 0.8;
  font-size: 0.9rem;
}

.niveau-stats {
  display: flex;
  justify-content: center;
  gap: 1rem;
  font-size: 0.8rem;
  opacity: 0.7;
}

.niveau-current {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.current-niveau {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.niveau-badge {
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
}

.niveaux-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-height: 300px;
  overflow-y: auto;
}

.niveau-option {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.niveau-option:hover {
  border-color: #3b82f6;
  background: #f8fafc;
}

.niveau-option.selected {
  border-color: #3b82f6;
  background: #eff6ff;
}

.niveau-option.current {
  border-color: #10b981;
  background: #f0fdf4;
}

.niveau-option .niveau-color {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  flex-shrink: 0;
}

.niveau-option .niveau-info {
  flex: 1;
}

.niveau-option h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  font-weight: 600;
}

.niveau-option p {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
}

.current-indicator {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: #10b981;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1rem;
}

.btn-primary {
  background: #fbbf24;
  color: #1f2937;
}

.btn-primary:hover:not(:disabled) {
  background: #f59e0b;
  transform: translateY(-1px);
}

.btn-primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

@media (max-width: 768px) {
  .niveaux-grid {
    grid-template-columns: 1fr;
  }
  
  .welcome-content {
    padding: 2rem 1rem;
  }
  
  .welcome-content h2 {
    font-size: 1.5rem;
  }
}
</style> 