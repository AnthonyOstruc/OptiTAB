<template>
  <div>
    <h2 class="admin-title">Gestion des Notions</h2>
    <form class="admin-form" @submit.prevent="handleSave">
      <div class="form-group">
        <label>Thème (lié à un contexte Matière + Niveau):</label>
        <select v-model="form.theme" required>
          <option value="">Choisir un thème</option>
          <option v-for="theme in themes" :key="theme.id" :value="theme.id">
            {{ theme.nom }} — {{ theme.contexte_detail?.matiere_nom }} — {{ theme.contexte_detail?.pays?.nom }} - {{ theme.contexte_detail?.niveau?.nom }}
          </option>
        </select>
      </div>
      
      <div class="form-group">
        <label>Nom de la notion:</label>
        <input v-model="form.nom" placeholder="Nom de la notion" required />
      </div>
      
      <!-- Plus besoin de choisir pays/niveau ici: le thème porte le contexte -->
      
      <button class="btn-primary" type="submit">{{ form.id ? 'Mettre à jour' : 'Créer' }}</button>
      <button v-if="form.id" class="btn-secondary" type="button" @click="resetForm">Annuler</button>
    </form>

    <!-- Filtres -->
    <div class="filters">
      <div class="filter-group">
        <label>Filtrer par thème:</label>
        <select v-model="filters.theme">
          <option value="">Tous les thèmes</option>
          <option v-for="theme in themes" :key="theme.id" :value="theme.id">
            {{ theme.nom }} — {{ theme.contexte_detail?.matiere_nom }} — {{ theme.contexte_detail?.pays?.nom }} - {{ theme.contexte_detail?.niveau?.nom }}
          </option>
        </select>
      </div>
      
      <div class="filter-group">
        <label>Rechercher:</label>
        <input v-model="filters.nom" type="text" placeholder="Nom de la notion..." />
      </div>
    </div>

    <!-- Tableau des notions -->
    <table class="admin-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nom de la notion</th>
          <th>Thème</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="notion in filteredNotions" :key="notion.id">
          <td>{{ notion.id }}</td>
          <td>{{ notion.nom }}</td>
          <td>
            <span v-if="notion.theme_nom" 
                  class="theme-badge" 
                  :style="{ backgroundColor: notion.theme_couleur, color: '#fff' }">
              {{ notion.theme_nom }}
            </span>
            <span v-else class="no-theme">Aucun thème</span>
          </td>
          
          <td>
            <AdminActionsButtons
              :item="notion"
              :actions="['edit', 'delete']"
              edit-label="Éditer"
              confirm-message="Êtes-vous sûr de vouloir supprimer cette notion ?"
              @edit="editNotion"
              @delete="handleDeleteNotion"
            />
          </td>
        </tr>
        <tr v-if="filteredNotions.length === 0">
          <td colspan="4" style="text-align:center; font-style: italic;">Aucune notion trouvée.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getNotions, createNotion, updateNotion, deleteNotion } from '@/api/notions'
import { getThemes } from '@/api/themes'
import PaysNiveauxSelector from '@/components/admin/PaysNiveauxSelector.vue'
import PaysNiveauxDisplay from '@/components/admin/PaysNiveauxDisplay.vue'
import { AdminActionsButtons } from '@/components/admin'

const notions = ref([])
const themes = ref([])
const form = ref({ 
  id: null, 
  nom: '', 
  theme: '', 
  niveaux: []
})
const filters = ref({
  theme: '',
  nom: ''
})

// Computed properties
// Plus de filtre par matière: le thème porte déjà le contexte complet

const filteredNotions = computed(() => {
  let filtered = notions.value
  
  // Filtrage par thème
  if (filters.value.theme) {
    filtered = filtered.filter(n => 
      String(n.theme) === String(filters.value.theme)
    )
  }
  
  if (filters.value.nom) {
    filtered = filtered.filter(n => 
      n.nom.toLowerCase().includes(filters.value.nom.toLowerCase())
    )
  }
  
  return filtered
})

async function load() {
  try {
    const [{ data: nData }, { data: tData }] = await Promise.all([
      getNotions(),
      getThemes()
    ])
    notions.value = nData || []
    themes.value = tData || []
  } catch (error) {
    console.error('[AdminNotions] Erreur lors du chargement:', error)
    notions.value = []
    themes.value = []
  }
}

onMounted(load)

function resetForm() {
  form.value = { 
    id: null, 
    nom: '', 
    theme: '', 
    niveaux: []
  }
}

async function handleSave() {
  if (!form.value.nom || !form.value.theme) return
  
  try {
    const payload = {
      nom: form.value.nom,
      theme: Number(form.value.theme),
      niveaux: []
    }
    
    if (form.value.id) {
      await updateNotion(form.value.id, payload)
    } else {
      await createNotion(payload)
    }
    resetForm()
    await load()
  } catch (e) {
    console.error('[AdminNotions] Erreur:', e)
  }
}

function editNotion(notion) {
  const niveauxIds = notion.niveaux ? notion.niveaux.map(n => n.id) : []
  
  form.value = { 
    id: notion.id,
    nom: notion.nom,
    theme: notion.theme || '',
    niveaux: []
  }
}

async function removeNotion(id) {
  try {
    await deleteNotion(id)
    await load()
  } catch (e) {
    console.error('Erreur:', e)
  }
}

// Nouvelle fonction qui utilise le composant AdminActionsButtons
function handleDeleteNotion(notion) {
  removeNotion(notion.id)
}
</script>

<style scoped>
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
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.btn-primary {
  background: #3b82f6;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  margin-right: 0.5rem;
}

.btn-secondary {
  background: #6b7280;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  margin-right: 0.5rem;
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

.admin-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.admin-table th,
.admin-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.admin-table th {
  background: #f9fafb;
  font-weight: 600;
  color: #374151;
}

.admin-table tr:hover {
  background: #f9fafb;
}

.theme-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.no-theme {
  color: #6b7280;
  font-style: italic;
  font-size: 0.875rem;
}
</style>
