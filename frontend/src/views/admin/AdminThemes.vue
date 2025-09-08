<template>
  <div class="admin-themes">
    <h1 class="admin-title">Gestion des Thèmes</h1>
    
    <!-- Formulaire -->
    <div class="admin-form">
      <h2>{{ form.id ? 'Modifier' : 'Ajouter' }} un thème</h2>
      <form @submit.prevent="handleSave">
        <div class="form-group">
          <label>Contexte (Matière + Niveau):</label>
          <select v-model="form.contexte" required>
            <option value="">Choisir un contexte</option>
            <option v-for="c in contextesOptions" :key="c.id" :value="c.id">
              {{ c.matiere_nom }} — {{ c.pays.nom }} - {{ c.niveau.nom }}
            </option>
          </select>
        </div>
        
        <div class="form-group">
          <label>Nom du thème:</label>
          <input v-model="form.nom" type="text" required />
        </div>
        
        <div class="form-group">
          <label>Description:</label>
          <textarea v-model="form.description" rows="3"></textarea>
        </div>
        
        <div class="form-group">
          <label>Couleur:</label>
          <div class="color-input-group">
            <input v-model="form.couleur" type="color" />
            <input v-model="form.couleur" type="text" placeholder="#3b82f6" />
          </div>
        </div>
        
        <div class="form-group">
          <label>Ordre d'affichage:</label>
          <input v-model.number="form.ordre" type="number" min="0" />
        </div>
        
        <!-- Niveaux spécifiques au thème (optionnel) -->
        <!-- Retiré: le contexte porte déjà le niveau. On garde simple et DRY. -->
        
        <div class="form-actions">
          <button type="submit" class="btn-primary">{{ form.id ? 'Modifier' : 'Ajouter' }}</button>
          <button type="button" @click="resetForm" class="btn-secondary">Annuler</button>
        </div>
      </form>
    </div>

    <!-- Liste des thèmes groupés par matière -->
    <div class="admin-list">
      <h2>Thèmes existants</h2>
      
      <!-- Filtres -->
      <div class="filters">
        <div class="filter-group">
          <label>Filtrer par contexte:</label>
          <select v-model="filters.contexte">
            <option value="">Tous les contextes</option>
            <option v-for="c in contextesOptions" :key="c.id" :value="c.id">
              {{ c.matiere_nom }} — {{ c.pays.nom }} - {{ c.niveau.nom }}
            </option>
          </select>
        </div>
        
        <div class="filter-group">
          <label>Rechercher:</label>
          <input v-model="filters.nom" type="text" placeholder="Nom du thème..." />
        </div>
      </div>

      <!-- Liste simple des thèmes (le contexte inclut déjà la matière/niveau) -->
      <div class="themes-grid">
        <div v-for="theme in filteredThemes()" :key="theme.id" class="theme-card">
            <div class="theme-header">
              <div class="theme-color" :style="{ backgroundColor: theme.couleur }"></div>
              <h4 class="theme-name">{{ theme.titre || theme.nom }}</h4>
            </div>
            <div class="context-chip" v-if="theme.contexte_detail">
              {{ theme.contexte_detail.matiere_nom }} — {{ theme.contexte_detail.pays?.nom }} - {{ theme.contexte_detail.niveau?.nom }}
            </div>
            
            <p v-if="theme.description" class="theme-description">{{ theme.description }}</p>
            
            <div class="theme-meta">
              <span class="theme-ordre">Ordre: {{ theme.ordre || 0 }}</span>
            </div>
            
            <div class="theme-actions">
              <AdminActionsButtons
                :item="theme"
                :actions="['edit', 'delete']"
                edit-label="Modifier"
                confirm-message="Êtes-vous sûr de vouloir supprimer ce thème ?"
                @edit="editTheme"
                @delete="handleDeleteTheme"
              />
            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getThemes, getThemesByContexte } from '@/api/themes.js'
import { getContextes } from '@/api/matiere-contextes.js'
import { createTheme, updateTheme, deleteTheme } from '@/api/themes.js'
import PaysNiveauxDisplay from '@/components/admin/PaysNiveauxDisplay.vue'
import { AdminActionsButtons } from '@/components/admin'

const contextesOptions = ref([])
const themes = ref([])
const form = ref({
  id: null,
  contexte: '',
  nom: '',
  description: '',
  couleur: '#3b82f6',
  ordre: 0
})

const filters = ref({
  contexte: '',
  nom: ''
})

// Computed properties
const filteredMatieres = computed(() => [])

const filteredThemes = () => {
  const list = Array.isArray(themes.value) ? themes.value : []
  let filtered = list
  if (filters.value.contexte) {
    filtered = filtered.filter(t => String(t.contexte) === String(filters.value.contexte))
  }
  
  if (filters.value.nom) {
    filtered = filtered.filter(t => 
      t.nom.toLowerCase().includes(filters.value.nom.toLowerCase())
    )
  }
  
  return filtered.sort((a, b) => (a.ordre || 0) - (b.ordre || 0))
}

// Methods
async function load() {
  try {
    const [contextesRes, themesRes] = await Promise.all([
      getContextes(),
      getThemes()
    ])
    contextesOptions.value = Array.isArray(contextesRes) ? contextesRes : (contextesRes?.data || [])
    themes.value = Array.isArray(themesRes) ? themesRes : (themesRes?.data || [])
  } catch (error) {
    console.error('Erreur lors du chargement:', error)
  }
}

function resetForm() {
  form.value = {
    id: null,
    contexte: '',
    nom: '',
    description: '',
    couleur: '#3b82f6',
    ordre: 0
  }
}

async function handleSave() {
  if (!form.value.contexte || !form.value.nom) return
  
  try {
    // Find the selected contexte to get the matiere
    const selectedContexte = contextesOptions.value.find(c => c.id === Number(form.value.contexte))
    if (!selectedContexte) {
      console.error('Contexte non trouvé')
      return
    }
    
    if (!selectedContexte.matiere) {
      console.error('Matière non trouvée dans le contexte')
      alert('Erreur: Impossible de récupérer la matière associée à ce contexte.')
      return
    }
    
    // Check for duplicate theme name in the same matiere
    const existingTheme = themes.value.find(t => 
      t.matiere === selectedContexte.matiere && 
      (t.nom === form.value.nom || t.titre === form.value.nom) && 
      t.id !== form.value.id
    )
    if (existingTheme) {
      alert('Un thème avec ce nom existe déjà dans cette matière.')
      return
    }
    
    const payload = {
      contexte: Number(form.value.contexte),
      matiere: selectedContexte.matiere, // Add the matiere field
      nom: form.value.nom,
      description: form.value.description,
      couleur: form.value.couleur,
      ordre: form.value.ordre
    }
    
    console.log('Payload being sent:', payload)
    console.log('Selected contexte:', selectedContexte)
    
    if (form.value.id) {
      await updateTheme(form.value.id, payload)
    } else {
      await createTheme(payload)
    }
    
    resetForm()
    await load()
  } catch (error) {
    console.error('Erreur lors de la sauvegarde:', error)
    // Show more specific error message
    if (error.response?.data) {
      const errorData = error.response.data
      if (errorData.non_field_errors) {
        alert(`Erreur: ${errorData.non_field_errors.join(', ')}`)
      } else if (errorData.titre) {
        alert(`Erreur sur le nom: ${errorData.titre.join(', ')}`)
      } else if (errorData.matiere) {
        alert(`Erreur sur la matière: ${errorData.matiere.join(', ')}`)
      } else {
        alert(`Erreur: ${JSON.stringify(errorData)}`)
      }
    } else {
      alert('Erreur lors de la sauvegarde. Vérifiez les données saisies.')
    }
  }
}

function editTheme(theme) {
  form.value = {
    id: theme.id,
    contexte: theme.contexte || '',
    nom: theme.nom || theme.titre || '',
    description: theme.description || '',
    couleur: theme.couleur || '#3b82f6',
    ordre: theme.ordre || 0
  }
}

async function removeTheme(id) {
  try {
    await deleteTheme(id)
    await load()
  } catch (error) {
    console.error('Erreur lors de la suppression:', error)
  }
}

// Nouvelle fonction qui utilise le composant AdminActionsButtons
function handleDeleteTheme(theme) {
  removeTheme(theme.id)
}

// Plus nécessaire: on affiche maintenant les niveaux propres au thème depuis l'API

onMounted(load)
</script>

<style scoped>
.admin-themes {
  padding: 1rem;
}

.admin-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #1f2937;
}

.admin-form {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.admin-form h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #374151;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #374151;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.color-input-group {
  display: flex;
  gap: 0.5rem;
}

.color-input-group input[type="color"] {
  width: 60px;
  padding: 0.25rem;
}

.color-input-group input[type="text"] {
  flex: 1;
}

.form-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1.5rem;
}

.btn-primary {
  background: #3b82f6;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
}

.btn-secondary {
  background: #6b7280;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
}

.btn-danger {
  background: #ef4444;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
}

.admin-list h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #374151;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.filter-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.filter-group input,
.filter-group select {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.matiere-group {
  margin-bottom: 2rem;
}

.matiere-header {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #374151;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.theme-count {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: normal;
}

.no-themes {
  padding: 1rem;
  background: #f9fafb;
  border-radius: 0.375rem;
  text-align: center;
  color: #6b7280;
}

.themes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.theme-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1rem;
  transition: all 0.2s ease;
}

.theme-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.theme-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.theme-color {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  flex-shrink: 0;
}

.theme-name {
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  margin: 0;
}

.theme-description {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.75rem;
  line-height: 1.4;
}

.theme-meta {
  margin-bottom: 0.75rem;
}

.theme-ordre {
  font-size: 0.75rem;
  color: #9ca3af;
  background: #f3f4f6;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
}

.theme-niveaux {
  margin-bottom: 1rem;
}

.theme-actions {
  display: flex;
  gap: 0.5rem;
}

.theme-actions button {
  flex: 1;
  padding: 0.5rem;
  font-size: 0.875rem;
}
</style>
