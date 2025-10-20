<template>
  <div class="niveau-assignment">
    <div class="assignment-header">
      <h3>🎯 Assignation des Niveaux</h3>
      <p>Sélectionnez les niveaux pour chaque élément</p>
    </div>

    <!-- Sélecteur de type d'élément -->
    <div class="element-selector">
      <label for="elementType">Type d'élément :</label>
      <select id="elementType" v-model="selectedType" @change="loadElements">
        <option value="">Choisir un type</option>
        <option value="matieres">Matières</option>
        <option value="exercices">Exercices</option>
        <option value="cours">Cours</option>
        <option value="quiz">Quiz</option>
        <!-- Temporairement désactivé jusqu'aux migrations -->
        <!-- <option value="themes">Thèmes</option> -->
        <!-- <option value="notions">Notions</option> -->
        <!-- <option value="chapitres">Chapitres</option> -->
      </select>
    </div>

    <!-- Sélecteur d'élément -->
    <div v-if="selectedType && elements.length > 0" class="element-selector">
      <label for="elementId">Élément :</label>
      <select id="elementId" v-model="selectedElementId" @change="loadElementNiveaux">
        <option value="">Choisir un élément</option>
        <option v-for="element in elements" :key="element.id" :value="element.id">
          {{ element.nom || element.titre }}
        </option>
      </select>
    </div>

    <!-- Sélecteur de niveaux -->
    <div v-if="selectedElementId && niveaux.length > 0" class="niveaux-selector">
      <h4>Niveaux assignés :</h4>
      <div class="niveaux-grid">
        <label v-for="niveau in niveaux" :key="niveau.id" class="niveau-checkbox">
          <input 
            type="checkbox" 
            :value="niveau.id" 
            v-model="selectedNiveaux"
            @change="updateNiveaux"
          />
          <span class="niveau-color" :style="{ backgroundColor: niveau.couleur }"></span>
          <span class="niveau-name">{{ niveau.nom }} ({{ niveau.pays_nom }})</span>
        </label>
      </div>
    </div>

    <!-- Actions en lot -->
    <div v-if="selectedType && elements.length > 0" class="bulk-actions">
      <h4>Actions en lot :</h4>
      <div class="bulk-controls">
        <select v-model="bulkNiveauId">
          <option value="">Choisir un niveau</option>
          <option v-for="niveau in niveaux" :key="niveau.id" :value="niveau.id">
            {{ niveau.nom }} ({{ niveau.pays_nom }})
          </option>
        </select>
        <button @click="assignNiveauToAll" class="btn-primary" :disabled="!bulkNiveauId">
          Assigner ce niveau à tous
        </button>
        <button @click="removeNiveauFromAll" class="btn-secondary" :disabled="!bulkNiveauId">
          Retirer ce niveau de tous
        </button>
      </div>
    </div>

    <!-- Statut -->
    <div v-if="status" class="status-message" :class="status.type">
      {{ status.message }}
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useToast } from '@/composables/useToast'
import apiClient from '@/api/client.js'
import { getNiveaux } from '@/api/niveaux.js'

export default {
  name: 'NiveauAssignment',
  setup() {
    const { showToast } = useToast()
    
    const selectedType = ref('')
    const selectedElementId = ref('')
    const selectedNiveaux = ref([])
    const bulkNiveauId = ref('')
    
    const elements = ref([])
    const niveaux = ref([])
    const status = ref(null)

    // Charger les niveaux
    const loadNiveaux = async () => {
      try {
        const data = await getNiveaux()
        niveaux.value = data
      } catch (error) {
        console.error('Erreur lors du chargement des niveaux:', error)
        showToast('Erreur lors du chargement des niveaux', 'error')
      }
    }

    // Charger les éléments selon le type
    const loadElements = async () => {
      if (!selectedType.value) {
        elements.value = []
        return
      }

      try {
        const response = await apiClient.get(`/api/${selectedType.value}/`)
        elements.value = response.data
      } catch (error) {
        console.error(`Erreur lors du chargement des ${selectedType.value}:`, error)
        showToast(`Erreur lors du chargement des ${selectedType.value}`, 'error')
      }
    }

    // Charger les niveaux d'un élément
    const loadElementNiveaux = async () => {
      if (!selectedElementId.value || !selectedType.value) {
        selectedNiveaux.value = []
        return
      }

      try {
        const response = await apiClient.get(`/api/${selectedType.value}/${selectedElementId.value}/`)
        selectedNiveaux.value = response.data.niveaux?.map(n => n.id) || []
      } catch (error) {
        console.error('Erreur lors du chargement des niveaux de l\'élément:', error)
        selectedNiveaux.value = []
      }
    }

    // Mettre à jour les niveaux d'un élément
    const updateNiveaux = async () => {
      if (!selectedElementId.value || !selectedType.value) return

      try {
        const response = await apiClient.patch(`/api/${selectedType.value}/${selectedElementId.value}/`, {
          niveaux: selectedNiveaux.value
        })

        if (response.status === 200) {
          showToast('Niveaux mis à jour avec succès', 'success')
        } else {
          throw new Error('Erreur lors de la mise à jour')
        }
      } catch (error) {
        console.error('Erreur lors de la mise à jour des niveaux:', error)
        showToast('Erreur lors de la mise à jour des niveaux', 'error')
      }
    }

    // Assigner un niveau à tous les éléments
    const assignNiveauToAll = async () => {
      if (!bulkNiveauId.value || !selectedType.value) return

      try {
        const promises = elements.value.map(element => 
          apiClient.patch(`/api/${selectedType.value}/${element.id}/`, {
            niveaux: [bulkNiveauId.value]
          })
        )

        await Promise.all(promises)
        showToast(`Niveau assigné à tous les ${selectedType.value}`, 'success')
        loadElements() // Recharger pour voir les changements
      } catch (error) {
        console.error('Erreur lors de l\'assignation en lot:', error)
        showToast('Erreur lors de l\'assignation en lot', 'error')
      }
    }

    // Retirer un niveau de tous les éléments
    const removeNiveauFromAll = async () => {
      if (!bulkNiveauId.value || !selectedType.value) return

      try {
        const promises = elements.value.map(element => 
          apiClient.patch(`/api/${selectedType.value}/${element.id}/`, {
            niveaux: []
          })
        )

        await Promise.all(promises)
        showToast(`Niveau retiré de tous les ${selectedType.value}`, 'success')
        loadElements() // Recharger pour voir les changements
      } catch (error) {
        console.error('Erreur lors du retrait en lot:', error)
        showToast('Erreur lors du retrait en lot', 'error')
      }
    }

    onMounted(() => {
      loadNiveaux()
    })

    return {
      selectedType,
      selectedElementId,
      selectedNiveaux,
      bulkNiveauId,
      elements,
      niveaux,
      status,
      loadElements,
      loadElementNiveaux,
      updateNiveaux,
      assignNiveauToAll,
      removeNiveauFromAll
    }
  }
}
</script>

<style scoped>
.niveau-assignment {
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.assignment-header {
  margin-bottom: 2rem;
  text-align: center;
}

.assignment-header h3 {
  margin: 0 0 0.5rem 0;
  color: #1f2937;
  font-size: 1.5rem;
}

.assignment-header p {
  margin: 0;
  color: #6b7280;
}

.element-selector {
  margin-bottom: 1.5rem;
}

.element-selector label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.element-selector select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.875rem;
}

.niveaux-selector {
  margin-bottom: 2rem;
}

.niveaux-selector h4 {
  margin: 0 0 1rem 0;
  color: #1f2937;
}

.niveaux-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.niveau-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.niveau-checkbox:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

.niveau-checkbox input[type="checkbox"] {
  margin: 0;
}

.niveau-color {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  flex-shrink: 0;
}

.niveau-name {
  font-size: 0.875rem;
  color: #374151;
}

.bulk-actions {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

.bulk-actions h4 {
  margin: 0 0 1rem 0;
  color: #1f2937;
}

.bulk-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.bulk-controls select {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
}

.btn-primary,
.btn-secondary {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-secondary:hover:not(:disabled) {
  background: #e5e7eb;
}

.btn-primary:disabled,
.btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.status-message {
  margin-top: 1rem;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.875rem;
}

.status-message.success {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.status-message.error {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}
</style> 