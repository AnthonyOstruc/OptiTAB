<template>
  <div>
    <h2 class="admin-title">Gestion des Chapitres</h2>
    <form class="admin-form" @submit.prevent="handleSave">
      <div class="form-group">
        <label>Notion (hérite du contexte via Thème):</label>
        <select v-model="form.notion" required>
          <option value="">Choisir une notion</option>
          <option v-for="notion in notions" :key="notion.id" :value="notion.id">
            {{ formatNotionOption(notion) }}
          </option>
        </select>
      </div>
      
      <div class="form-group">
        <label>Nom du chapitre:</label>
        <input v-model="form.nom" placeholder="Nom du chapitre" required />
      </div>
      
      <div class="form-group">
        <label>Description:</label>
        <textarea v-model="form.description" rows="3"></textarea>
      </div>
      
      <div class="form-group">
        <label>Ordre d'affichage:</label>
        <input v-model.number="form.ordre" type="number" min="0" />
      </div>
      
      <!-- Plus besoin de pays/niveaux ici: la notion porte le contexte via le thème -->
      
      <button class="btn-primary" type="submit">{{ form.id ? 'Mettre à jour' : 'Créer' }}</button>
      <button v-if="form.id" class="btn-secondary" type="button" @click="resetForm">Annuler</button>
    </form>

    <!-- Filtres -->
    <div class="filters">
      <div class="filter-group">
        <label>Filtrer par notion:</label>
        <select v-model="filters.notion">
          <option value="">Toutes les notions</option>
          <option v-for="notion in notions" :key="notion.id" :value="notion.id">
            {{ formatNotionOption(notion) }}
          </option>
        </select>
      </div>
      
      <div class="filter-group">
        <label>Rechercher:</label>
        <input v-model="filters.nom" type="text" placeholder="Nom du chapitre..." />
      </div>
    </div>

    <!-- Tableau des chapitres -->
    <table class="admin-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nom du chapitre</th>
          <th>Notion</th>
          <th>Ordre</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="chapitre in filteredChapitres" :key="chapitre.id">
          <td>{{ chapitre.id }}</td>
          <td>{{ chapitre.nom }}</td>
          <td>{{ getNotionLabelById(chapitre.notion) }}</td>
          <td>{{ chapitre.ordre || 0 }}</td>
          <td>
            <AdminActionsButtons
              :item="chapitre"
              :actions="['edit', 'delete']"
              edit-label="Éditer"
              confirm-message="Êtes-vous sûr de vouloir supprimer ce chapitre ?"
              @edit="editChapitre"
              @delete="handleDeleteChapitre"
            />
          </td>
        </tr>
        <tr v-if="filteredChapitres.length === 0">
          <td colspan="5" style="text-align:center; font-style: italic;">Aucun chapitre trouvé.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getChapitres, createChapitre, updateChapitre, deleteChapitre } from '@/api'
import { getNotions } from '@/api'
import { AdminActionsButtons } from '@/components/admin'

const chapitres = ref([])
const notions = ref([])
const form = ref({ 
  id: null, 
  nom: '', 
  notion: '', 
  description: '', 
  ordre: 0,
})
const filters = ref({
  notion: '',
  nom: ''
})

// Computed properties
const filteredChapitres = computed(() => {
  let filtered = chapitres.value
  
  if (filters.value.notion) {
    filtered = filtered.filter(c => c.notion == filters.value.notion)
  }
  
  if (filters.value.nom) {
    filtered = filtered.filter(c => 
      c.nom.toLowerCase().includes(filters.value.nom.toLowerCase())
    )
  }
  
  return filtered.sort((a, b) => (a.ordre || 0) - (b.ordre || 0))
})

async function load() {
  try {
    const [cData, nData] = await Promise.all([
      getChapitres(),
      getNotions()
    ])
    chapitres.value = cData || []
    notions.value = nData || []
  } catch (error) {
    console.error('[AdminChapitres] Erreur lors du chargement:', error)
    chapitres.value = []
    notions.value = []
  }
}

onMounted(load)

function resetForm() {
  form.value = { 
    id: null, 
    nom: '', 
    notion: '', 
    description: '', 
    ordre: 0
  }
}

async function handleSave() {
  if (!form.value.nom || !form.value.notion) return
  
  try {
    const payload = {
      nom: form.value.nom,
      notion: Number(form.value.notion),
      description: form.value.description,
      ordre: form.value.ordre,
      contenu: ''
    }
    
    if (form.value.id) {
      await updateChapitre(form.value.id, payload)
    } else {
      await createChapitre(payload)
    }
    resetForm()
    await load()
  } catch (e) {
    console.error('[AdminChapitres] Erreur:', e)
  }
}

function editChapitre(chapitre) {
  form.value = { 
    ...chapitre, 
    notion: chapitre.notion
  }
}

// Helpers d'affichage
function formatNotionOption(n) {
  if (!n) return ''
  const matiere = n.matiere_nom || (n.contexte_detail && n.contexte_detail.matiere_nom) || ''
  const pays = n.contexte_detail && n.contexte_detail.pays ? n.contexte_detail.pays.nom : ''
  const niveau = n.contexte_detail && n.contexte_detail.niveau ? n.contexte_detail.niveau.nom : ''
  const theme = n.theme_nom || ''
  const parts = [n.nom, theme, matiere, [pays, niveau].filter(Boolean).join(' - ')].filter(Boolean)
  return parts.join(' — ')
}

function getNotionLabelById(id) {
  const n = notions.value.find(x => String(x.id) === String(id))
  return formatNotionOption(n)
}

async function removeChapitre(id) {
  try {
    await deleteChapitre(id)
    await load()
  } catch (e) {
    console.error('Erreur:', e)
  }
}

// Nouvelle fonction qui utilise le composant AdminActionsButtons
function handleDeleteChapitre(chapitre) {
  removeChapitre(chapitre.id)
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
</style> 