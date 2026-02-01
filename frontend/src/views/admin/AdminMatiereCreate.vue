<template>
  <div class="admin-matiere-create">
    <div class="page-header">
      <h1>📚 Créer une nouvelle matière</h1>
      <p>Sélectionnez d'abord le pays et le niveau, puis configurez la matière</p>
    </div>

    <div class="form-container">
      <!-- Sélecteur Pays/Niveau -->
      <div class="form-section">
        <h3>🌍 Localisation et niveau</h3>
        <PaysNiveauSelector 
          v-model="paysNiveauSelection"
          @selection-change="onPaysNiveauChange"
        />
      </div>

      <!-- Formulaire de la matière -->
      <div v-if="paysNiveauSelection.pays && paysNiveauSelection.niveau" class="form-section">
        <h3>📝 Informations de la matière</h3>
        
        <div class="form-group">
          <label for="matiere-nom">Nom de la matière</label>
          <input 
            id="matiere-nom"
            v-model="matiereForm.nom"
            type="text"
            placeholder="Ex: Mathématiques, Physique, Histoire..."
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="matiere-description">Description</label>
          <textarea 
            id="matiere-description"
            v-model="matiereForm.description"
            placeholder="Description de la matière..."
            rows="4"
            class="form-textarea"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="matiere-couleur">Couleur</label>
          <input 
            id="matiere-couleur"
            v-model="matiereForm.couleur"
            type="color"
            class="form-color-input"
          />
        </div>

        <div class="form-group">
          <label>
            <input 
              v-model="matiereForm.est_actif"
              type="checkbox"
              class="form-checkbox"
            />
            Matière active
          </label>
        </div>

        <!-- Bouton de création -->
        <div class="form-actions">
          <button 
            @click="createMatiere"
            :disabled="!canCreateMatiere || creating"
            class="btn-primary"
          >
            <span v-if="creating" class="loading-spinner"></span>
            <span v-else>✅ Créer la matière</span>
          </button>
        </div>
      </div>

      <!-- Message d'instruction -->
      <div v-else class="instruction-message">
        <div class="instruction-icon">🎯</div>
        <h3>Sélectionnez d'abord un pays et un niveau</h3>
        <p>Pour créer une matière, vous devez d'abord choisir le pays et le niveau scolaire auxquels elle sera associée.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import PaysNiveauSelector from '@/components/admin/PaysNiveauSelector.vue'

export default {
  name: 'AdminMatiereCreate',
  components: {
    PaysNiveauSelector
  },
  setup() {
    // États réactifs
    const paysNiveauSelection = ref({
      pays_id: null,
      niveau_id: null,
      pays: null,
      niveau: null
    })

    const matiereForm = ref({
      nom: '',
      description: '',
      couleur: '#3b82f6',
      est_actif: true
    })

    const creating = ref(false)

    // Computed
    const canCreateMatiere = computed(() => {
      return paysNiveauSelection.value.pays_id && 
             paysNiveauSelection.value.niveau_id && 
             matiereForm.value.nom.trim() !== ''
    })

    // Méthodes
    const onPaysNiveauChange = (selection) => {
      console.log('Sélection pays/niveau:', selection)
      // Ici vous pouvez ajouter de la logique supplémentaire
    }

    const createMatiere = async () => {
      if (!canCreateMatiere.value) return

      try {
        creating.value = true
        
        const matiereData = {
          ...matiereForm.value,
          pays_id: paysNiveauSelection.value.pays_id,
          niveau_pays_id: paysNiveauSelection.value.niveau_id
        }

        console.log('Création de la matière:', matiereData)
        
        // Ici vous appelleriez votre API pour créer la matière
        // await createMatiereAPI(matiereData)
        
        // Simulation d'un délai
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        alert(`✅ Matière "${matiereForm.value.nom}" créée avec succès pour ${paysNiveauSelection.value.pays.nom} - ${paysNiveauSelection.value.niveau.nom}`)
        
        // Reset du formulaire
        matiereForm.value = {
          nom: '',
          description: '',
          couleur: '#3b82f6',
          est_actif: true
        }
        
      } catch (error) {
        console.error('Erreur lors de la création:', error)
        alert('❌ Erreur lors de la création de la matière')
      } finally {
        creating.value = false
      }
    }

    return {
      paysNiveauSelection,
      matiereForm,
      creating,
      canCreateMatiere,
      onPaysNiveauChange,
      createMatiere
    }
  }
}
</script>

<style scoped>
.admin-matiere-create {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  margin: 0 0 0.5rem 0;
  color: #1f2937;
  font-size: 2rem;
}

.page-header p {
  margin: 0;
  color: #6b7280;
  font-size: 1rem;
}

.form-container {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.form-section {
  padding: 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.form-section:last-child {
  border-bottom: none;
}

.form-section h3 {
  margin: 0 0 1.5rem 0;
  color: #374151;
  font-size: 1.25rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition: border-color 0.2s;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.form-color-input {
  width: 60px;
  height: 40px;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  cursor: pointer;
}

.form-checkbox {
  margin-right: 0.5rem;
}

.form-actions {
  margin-top: 2rem;
  text-align: center;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary:hover:not(:disabled) {
  background-color: #2563eb;
}

.btn-primary:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.instruction-message {
  text-align: center;
  padding: 3rem 2rem;
  color: #6b7280;
}

.instruction-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.instruction-message h3 {
  margin: 0 0 0.5rem 0;
  color: #374151;
  font-size: 1.25rem;
}

.instruction-message p {
  margin: 0;
  font-size: 1rem;
  line-height: 1.5;
}
</style> 