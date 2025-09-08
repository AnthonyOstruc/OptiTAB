<template>
  <div class="niveau-filter">
    <div class="filter-header">
      <h3 class="filter-title">Filtre par niveau</h3>
      <div v-if="selectedNiveau" class="selected-niveau">
        <span class="selected-label">Niveau sélectionné :</span>
        <span 
          class="niveau-badge"
          :style="{ backgroundColor: selectedNiveau.couleur }"
        >
          {{ selectedNiveau.nom }}
        </span>
      </div>
    </div>
    
    <div class="niveaux-grid">
      <button
        v-for="niveau in niveaux"
        :key="niveau.id"
        class="niveau-option"
        :class="{ active: selectedNiveauId === niveau.id }"
        :style="{ 
          borderColor: niveau.couleur,
          backgroundColor: selectedNiveauId === niveau.id ? niveau.couleur : 'transparent'
        }"
        @click="selectNiveau(niveau.id)"
      >
        <span class="niveau-color" :style="{ backgroundColor: niveau.couleur }"></span>
        <span class="niveau-name">{{ niveau.nom }}</span>
      </button>
    </div>
    
    <div class="filter-actions">
      <button 
        class="btn-apply"
        @click="applyFilter"
        :disabled="!selectedNiveauId"
      >
        Appliquer le filtre
      </button>
      <button 
        class="btn-clear"
        @click="clearFilter"
        :disabled="!selectedNiveauId"
      >
        Afficher tout
      </button>
    </div>
    
    <!-- Résultats du filtrage -->
    <div v-if="selectedNiveau" class="filter-results">
      <h4 class="results-title">Contenu disponible pour {{ selectedNiveau.nom }}</h4>
      
      <div class="results-grid">
        <div class="result-section">
          <h5>Matières ({{ matieres.length }})</h5>
          <div class="result-list">
            <div v-for="matiere in matieres" :key="matiere.id" class="result-item">
              {{ matiere.nom }}
            </div>
          </div>
        </div>
        
        <div class="result-section">
          <h5>Thèmes ({{ themes.length }})</h5>
          <div class="result-list">
            <div v-for="theme in themes" :key="theme.id" class="result-item">
              {{ theme.matiere?.nom }} > {{ theme.nom }}
            </div>
          </div>
        </div>
        
        <div class="result-section">
          <h5>Notions ({{ notions.length }})</h5>
          <div class="result-list">
            <div v-for="notion in notions" :key="notion.id" class="result-item">
              {{ notion.matiere?.nom }} > {{ notion.nom }}
            </div>
          </div>
        </div>
        
        <div class="result-section">
          <h5>Chapitres ({{ chapitres.length }})</h5>
          <div class="result-list">
            <div v-for="chapitre in chapitres" :key="chapitre.id" class="result-item">
              {{ chapitre.notion?.matiere?.nom }} > {{ chapitre.notion?.nom }} > {{ chapitre.nom }}
            </div>
          </div>
        </div>
        
        <div class="result-section">
          <h5>Exercices ({{ exercices.length }})</h5>
          <div class="result-list">
            <div v-for="exercice in exercices" :key="exercice.id" class="result-item">
              {{ exercice.chapitre?.notion?.matiere?.nom }} > {{ exercice.chapitre?.notion?.nom }} > {{ exercice.chapitre?.nom }} > {{ exercice.titre }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getNiveaux } from '@/api/niveaux'
import { getMatieres } from '@/api/matieres'
import { getThemes } from '@/api/themes'
import { getNotions } from '@/api/notions'
import { getChapitres } from '@/api/chapitres'
import { getExercices } from '@/api/exercices'

const emit = defineEmits(['filter-applied', 'filter-cleared'])

const niveaux = ref([])
const selectedNiveauId = ref(null)
const loading = ref(false)

// Données filtrées
const matieres = ref([])
const themes = ref([])
const notions = ref([])
const chapitres = ref([])
const exercices = ref([])

// Niveau sélectionné
const selectedNiveau = computed(() => {
  return niveaux.value.find(n => n.id === selectedNiveauId.value)
})

onMounted(async () => {
  try {
    const niveauxData = await getNiveaux()
    niveaux.value = niveauxData
  } catch (error) {
    console.error('Erreur lors du chargement des niveaux:', error)
  }
})

function selectNiveau(niveauId) {
  selectedNiveauId.value = niveauId
}

async function applyFilter() {
  if (!selectedNiveauId.value) return
  
  loading.value = true
  
  try {
    // Charger toutes les données filtrées par niveau
    const [matieresRes, themesRes, notionsRes, chapitresRes, exercicesRes] = await Promise.all([
      getMatieres(selectedNiveauId.value),
      getThemes(null, selectedNiveauId.value),
      getNotions(null, selectedNiveauId.value),
      getChapitres(null, selectedNiveauId.value),
      getExercices(null, selectedNiveauId.value)
    ])
    
    matieres.value = matieresRes.data || []
    themes.value = themesRes.data || []
    notions.value = notionsRes.data || []
    chapitres.value = chapitresRes.data || []
    exercices.value = exercicesRes.data || []
    
    emit('filter-applied', selectedNiveauId.value)
    
    console.log('Filtrage appliqué pour niveau', selectedNiveauId.value, {
      matieres: matieres.value.length,
      themes: themes.value.length,
      notions: notions.value.length,
      chapitres: chapitres.value.length,
      exercices: exercices.value.length
    })
  } catch (error) {
    console.error('Erreur lors du filtrage:', error)
  } finally {
    loading.value = false
  }
}

function clearFilter() {
  selectedNiveauId.value = null
  matieres.value = []
  themes.value = []
  notions.value = []
  chapitres.value = []
  exercices.value = []
  
  emit('filter-cleared')
}
</script>

<style scoped>
.niveau-filter {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.filter-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.selected-niveau {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.selected-label {
  font-size: 0.875rem;
  color: #6b7280;
}

.niveau-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
  color: white;
}

.niveaux-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.niveau-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  font-weight: 500;
}

.niveau-option:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.niveau-option.active {
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.niveau-color {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  flex-shrink: 0;
}

.niveau-name {
  flex: 1;
  text-align: left;
}

.filter-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 2rem;
}

.btn-apply, .btn-clear {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.btn-apply {
  background: #3b82f6;
  color: white;
}

.btn-apply:hover:not(:disabled) {
  background: #2563eb;
}

.btn-clear {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-clear:hover:not(:disabled) {
  background: #e5e7eb;
}

.btn-apply:disabled, .btn-clear:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.filter-results {
  border-top: 1px solid #e5e7eb;
  padding-top: 1.5rem;
}

.results-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 1rem 0;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.result-section {
  background: #f8fafc;
  border-radius: 8px;
  padding: 1rem;
}

.result-section h5 {
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 0.75rem 0;
}

.result-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.result-item {
  font-size: 0.875rem;
  color: #6b7280;
  padding: 0.5rem;
  background: white;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
}

@media (max-width: 768px) {
  .filter-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .niveaux-grid {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  }
  
  .filter-actions {
    flex-direction: column;
  }
  
  .results-grid {
    grid-template-columns: 1fr;
  }
}
</style> 