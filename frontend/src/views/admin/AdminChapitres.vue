<template>
  <div>
    <h2 class="admin-title">Gestion des Chapitres</h2>
    <form class="admin-form" @submit.prevent="handleSave">
      <div class="form-group">
        <label>Notion (hérite du contexte via Thème):</label>
        <input v-model="notionFormFilter" type="text" placeholder="Filtrer les notions..." class="filter-input" />
        <select v-model="form.notion" required>
          <option value="">Choisir une notion</option>
          <option v-for="notion in filteredNotionsForForm" :key="notion.id" :value="notion.id">
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
        <input v-model="notionFilter" type="text" placeholder="Filtrer les notions..." class="filter-input" />
        <select v-model="filters.notion">
          <option value="">Toutes les notions</option>
          <option v-for="notion in filteredNotions" :key="notion.id" :value="notion.id">
            {{ formatNotionOption(notion) }}
          </option>
        </select>
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
        <tr v-for="chapitre in paginatedChapitres" :key="chapitre.id">
          <td>{{ chapitre.id }}</td>
          <td>{{ chapitre.nom }}</td>
          <td>{{ getNotionLabelById(chapitre.notion) }}</td>
          <td>{{ chapitre.ordre || 0 }}</td>
          <td>
            <AdminActionsButtons
              :item="chapitre"
              :actions="['edit', 'duplicate', 'delete']"
              edit-label="Éditer"
              duplicate-label="Dupliquer"
              confirm-message="Êtes-vous sûr de vouloir supprimer ce chapitre ?"
              @edit="editChapitre"
              @duplicate="openDuplicateModal(chapitre)"
              @delete="handleDeleteChapitre"
            />
          </td>
        </tr>
        <tr v-if="paginatedChapitres.length === 0">
          <td colspan="5" style="text-align:center; font-style: italic;">Aucun chapitre trouvé.</td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="pagination">
      <button 
        class="pagination-btn" 
        @click="currentPage--" 
        :disabled="currentPage === 1"
      >
        Précédent
      </button>
      
      <div class="pagination-numbers">
        <button
          v-for="page in displayedPages"
          :key="page"
          class="pagination-number"
          :class="{ active: page === currentPage }"
          @click="currentPage = page"
        >
          {{ page }}
        </button>
      </div>
      
      <button 
        class="pagination-btn" 
        @click="currentPage++" 
        :disabled="currentPage === totalPages"
      >
        Suivant
      </button>
    </div>
    
    <div v-if="totalPages > 1" class="pagination-info">
      Page {{ currentPage }} sur {{ totalPages }} ({{ filteredChapitres.length }} chapitre(s) au total)
    </div>
  </div>
  <!-- Duplication Modal -->
  <SimpleModal :isOpen="duplicateState.open" title="Dupliquer le chapitre" @close="closeDuplicateModal">
    <div>
      <div class="form-group">
        <label>Notion cible</label>
        <input v-model="notionFilter" type="text" placeholder="Rechercher une notion..." class="filter-input" />
        <select v-model="duplicateState.targetNotion" required>
          <option value="">Choisir une notion cible</option>
          <option
            v-for="n in filteredNotions"
            :key="n.id"
            :value="n.id"
          >
            {{ formatNotionOption(n) }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label>Nouveau nom (optionnel)</label>
        <input v-model="duplicateState.newTitle" placeholder="Nom de la copie (laisser vide pour suffixe (Copie))" />
      </div>
    </div>
    <template #footer>
      <button class="btn-secondary" @click="closeDuplicateModal">Annuler</button>
      <button class="btn-primary" :disabled="!duplicateState.targetNotion" @click="confirmDuplicate">Dupliquer</button>
    </template>
  </SimpleModal>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { createChapitre, updateChapitre, deleteChapitre } from '@/api'
import { getNotions } from '@/api'
import { apiClient } from '@/api'
import SimpleModal from '@/components/debug/SimpleModal.vue'
import { AdminActionsButtons } from '@/components/admin'

const chapitres = ref([])
const notions = ref([])
const notionFormFilter = ref('')
const notionFilter = ref('')
const form = ref({
  id: null,
  nom: '',
  notion: '',
  description: '',
  ordre: 0,
})
const filters = ref({
  notion: ''
})

// Pagination
const currentPage = ref(1)
const itemsPerPage = 5

// UI state for duplication modal
const duplicateState = ref({
  open: false,
  sourceChapitre: null,
  targetNotion: '',
  newTitle: ''
})

// Computed properties
const filteredChapitres = computed(() => {
  let filtered = chapitres.value
  
  if (filters.value.notion) {
    filtered = filtered.filter(c => c.notion == filters.value.notion)
  }

  return filtered.sort((a, b) => (a.ordre || 0) - (b.ordre || 0))
})

// Notions filtrées pour le formulaire (par texte seulement)
const filteredNotionsForForm = computed(() => {
  if (!notionFormFilter.value) {
    return notions.value
  }
  const filter = notionFormFilter.value.toLowerCase()
  return notions.value.filter(notion =>
    formatNotionOption(notion).toLowerCase().includes(filter)
  )
})

// Notions filtrées pour les filtres (par texte seulement)
const filteredNotions = computed(() => {
  if (!notionFilter.value) {
    return notions.value
  }
  const filter = notionFilter.value.toLowerCase()
  return notions.value.filter(notion =>
    formatNotionOption(notion).toLowerCase().includes(filter)
  )
})

// Computed properties pour la pagination
const totalPages = computed(() => {
  const total = filteredChapitres.value.length
  return Math.ceil(total / itemsPerPage)
})

const paginatedChapitres = computed(() => {
  const allFiltered = filteredChapitres.value
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return allFiltered.slice(start, end)
})

const displayedPages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value
  
  // Afficher au maximum 5 numéros de page
  let startPage = Math.max(1, current - 2)
  let endPage = Math.min(total, current + 2)
  
  // Ajuster si on est proche du début ou de la fin
  if (current <= 3) {
    endPage = Math.min(5, total)
  }
  if (current >= total - 2) {
    startPage = Math.max(1, total - 4)
  }
  
  for (let i = startPage; i <= endPage; i++) {
    pages.push(i)
  }
  
  return pages
})

async function load() {
  try {
    const [nData] = await Promise.all([
      getNotions()
    ])
    chapitres.value = []
    notions.value = nData || []
  } catch (error) {
    console.error('[AdminChapitres] Erreur lors du chargement:', error)
    chapitres.value = []
    notions.value = []
  }
}

onMounted(load)

// Watcher pour réinitialiser la page courante quand les filtres changent
watch(() => filters.value.notion, () => {
  currentPage.value = 1
})

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

    // Sauvegarder la notion actuelle avant de reset le formulaire
    const currentNotion = form.value.notion

    resetForm()

    // Remettre la notion sélectionnée pour permettre d'ajouter un autre chapitre dans la même notion
    form.value.notion = currentNotion

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

function openDuplicateModal(chapitre) {
  duplicateState.value = {
    open: true,
    sourceChapitre: chapitre,
    targetNotion: chapitre.notion || '',
    newTitle: chapitre.nom || ''
  }
}

function closeDuplicateModal() {
  duplicateState.value.open = false
}

async function confirmDuplicate() {
  const src = duplicateState.value.sourceChapitre
  const targetNotionId = Number(duplicateState.value.targetNotion)
  const newTitle = (duplicateState.value.newTitle || '').trim()
  if (!src || !targetNotionId) return
  try {
    await apiClient.post(`/api/chapitres/${src.id}/duplicate/`, { notion: targetNotionId, titre: newTitle })
    closeDuplicateModal()
    await load()
  } catch (e) {
    console.error('[AdminChapitres] Erreur de duplication:', e)
    alert('Erreur lors de la duplication du chapitre')
  }
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

.filter-input {
  margin-bottom: 0.5rem;
  width: 100%;
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

/* Pagination */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 2rem;
  padding: 1rem 0;
}

.pagination-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  transition: all 0.2s;
}

.pagination-btn:hover:not(:disabled) {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-numbers {
  display: flex;
  gap: 0.25rem;
}

.pagination-number {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  transition: all 0.2s;
  min-width: 2.5rem;
}

.pagination-number:hover {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.pagination-number.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

.pagination-info {
  text-align: center;
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.5rem;
  margin-bottom: 2rem;
}
</style> 