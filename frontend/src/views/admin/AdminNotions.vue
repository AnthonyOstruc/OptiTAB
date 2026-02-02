<template>
  <div>
    <h2 class="admin-title">Gestion des Notions</h2>
    <form class="admin-form" @submit.prevent="handleSave">
      <div class="form-group">
        <label>Thème (lié à un contexte Matière + Niveau):</label>
        <input v-model="themeFormFilter" type="text" placeholder="Filtrer les thèmes..." class="filter-input" />
        <select v-model="form.theme" required>
          <option value="">Choisir un thème</option>
          <option v-for="theme in filteredThemesForForm" :key="theme.id" :value="theme.id">
            {{ theme.nom }} — {{ theme.contexte_detail?.matiere_nom }} — {{ theme.contexte_detail?.pays?.nom }} - {{ theme.contexte_detail?.niveau?.nom }}
          </option>
        </select>
      </div>
      
      <div class="form-group">
        <label>Nom de la notion:</label>
        <input v-model="form.nom" placeholder="Nom de la notion" required />
      </div>
      
      <div class="form-group">
        <label>Ordre d'affichage:</label>
        <input v-model.number="form.ordre" type="number" min="0" />
      </div>

      <div class="form-group inline-field">
        <label class="checkbox-label">
          <input type="checkbox" v-model="form.est_actif" />
          Notion active (visible dans les ressources gratuites)
        </label>
      </div>
      
      <!-- Plus besoin de choisir pays/niveau ici: le thème porte le contexte -->
      
      <button class="btn-primary" type="submit">{{ form.id ? 'Mettre à jour' : 'Créer' }}</button>
      <button v-if="form.id" class="btn-secondary" type="button" @click="resetForm">Annuler</button>
    </form>

    <!-- Filtres -->
    <div class="filters">
      <div class="filter-group">
        <label>Filtrer par contexte:</label>
        <input v-model="contexteFilter" type="text" placeholder="Filtrer les contextes..." class="filter-input" />
        <select v-model="filters.contexte">
          <option value="">Tous les contextes</option>
          <option v-for="c in filteredContextes" :key="c.id" :value="c.id">
            {{ c.matiere_nom }} — {{ c.pays.nom }} - {{ c.niveau.nom }}
          </option>
        </select>
      </div>

      <div class="filter-group">
        <label>Filtrer par thème:</label>
        <input v-model="themeFilter" type="text" placeholder="Filtrer les thèmes..." class="filter-input" />
        <select v-model="filters.theme">
          <option value="">Tous les thèmes</option>
          <option v-for="theme in filteredThemes" :key="theme.id" :value="theme.id">
            {{ theme.nom }} — {{ theme.contexte_detail?.matiere_nom }} — {{ theme.contexte_detail?.pays?.nom }} - {{ theme.contexte_detail?.niveau?.nom }}
          </option>
        </select>
      </div>
      
    </div>

    <!-- Tableau des notions -->
    <table class="admin-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Ordre</th>
          <th>Nom de la notion</th>
          <th>Actif</th>
          <th>Thème</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="isLoadingNotions">
          <td colspan="6" class="loading-row">Chargement des notions...</td>
        </tr>
        <template v-else>
          <tr v-for="notion in paginatedNotions" :key="notion.id">
            <td>{{ notion.id }}</td>
            <td>{{ notion.ordre || 0 }}</td>
            <td>{{ notion.nom }}</td>
            <td>
              <label class="status-toggle">
                <input
                  type="checkbox"
                  :checked="notion.est_actif !== false"
                  :disabled="isLoadingNotions"
                  @change="toggleNotionActive(notion, $event.target.checked)"
                />
                <span :class="['status-pill', (notion.est_actif !== false) ? 'active' : 'inactive']">
                  {{ (notion.est_actif !== false) ? 'Actif' : 'Inactif' }}
                </span>
              </label>
            </td>
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
                :actions="['edit', 'duplicate', 'delete']"
                edit-label="Éditer"
                duplicate-label="Dupliquer"
                confirm-message="Êtes-vous sûr de vouloir supprimer cette notion ?"
                @edit="editNotion"
                @duplicate="handleDuplicateNotion"
                @delete="handleDeleteNotion"
              />
            </td>
          </tr>
          <tr v-if="paginatedNotions.length === 0">
            <td colspan="6" style="text-align:center; font-style: italic;">Aucune notion trouvée.</td>
          </tr>
        </template>
      </tbody>
    </table>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="pagination">
      <button 
        class="pagination-btn" 
        @click="prevPage" 
        :disabled="currentPage === 1 || isLoadingNotions"
      >
        Précédent
      </button>
      
      <div class="pagination-numbers">
        <button
          v-for="page in displayedPages"
          :key="page"
          class="pagination-number"
          :class="{ active: page === currentPage }"
          @click="goToPage(page)"
          :disabled="isLoadingNotions"
        >
          {{ page }}
        </button>
      </div>
      
      <button 
        class="pagination-btn" 
        @click="nextPage" 
        :disabled="currentPage >= totalPages || isLoadingNotions"
      >
        Suivant
      </button>
    </div>
    
    <div v-if="totalPages > 1" class="pagination-info">
      Page {{ currentPage }} sur {{ totalPages }} ({{ totalItems }} notion(s) au total)
    </div>

  <!-- Duplication Modal -->
  <SimpleModal :isOpen="duplicateState.open" title="Dupliquer la notion" @close="closeDuplicateModal">
    <div>
      <div class="form-group">
        <label>Thème cible</label>
        <input v-model="duplicateThemeFilter" type="text" placeholder="Rechercher un thème..." class="filter-input" />
        <select v-model="duplicateState.targetTheme" required>
          <option value="">Choisir un thème cible</option>
          <option
            v-for="theme in filteredThemesForModal"
            :key="theme.id"
            :value="theme.id"
          >
            {{ theme.nom }} — {{ theme.contexte_detail?.matiere_nom }} — {{ theme.contexte_detail?.pays?.nom }} - {{ theme.contexte_detail?.niveau?.nom }}
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
      <button class="btn-primary" :disabled="!duplicateState.targetTheme" @click="confirmDuplicate">Dupliquer</button>
    </template>
  </SimpleModal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { getNotions, createNotion, updateNotion, deleteNotion, duplicateNotion } from '@/api/notions'
import { getThemes } from '@/api/themes'
import { getContextes } from '@/api/matiere-contextes.js'
import PaysNiveauxSelector from '@/components/admin/PaysNiveauxSelector.vue'
import PaysNiveauxDisplay from '@/components/admin/PaysNiveauxDisplay.vue'
import { AdminActionsButtons } from '@/components/admin'
import SimpleModal from '@/components/debug/SimpleModal.vue'

const notions = ref([])
const themes = ref([])
const contextesOptions = ref([])
const contexteFilter = ref('')
const themeFilter = ref('')
const themeFormFilter = ref('')
const duplicateThemeFilter = ref('')
const form = ref({
  id: null,
  nom: '',
  theme: '',
  niveaux: [],
  ordre: 0,
  est_actif: true
})
const filters = ref({
  theme: '',
  contexte: ''
})

// Pagination
const currentPage = ref(1)
const itemsPerPage = 5
const totalNotions = ref(0)
const isLoadingNotions = ref(false)

// UI state for duplication modal
const duplicateState = ref({
  open: false,
  sourceNotion: null,
  targetTheme: '',
  newTitle: ''
})

// Computed properties
// Plus de filtre par matière: le thème porte déjà le contexte complet

// Contextes filtrés par texte
const filteredContextes = computed(() => {
  if (!contexteFilter.value) {
    return contextesOptions.value
  }
  const filter = contexteFilter.value.toLowerCase()
  return contextesOptions.value.filter(c =>
    c.matiere_nom.toLowerCase().includes(filter) ||
    c.pays?.nom.toLowerCase().includes(filter) ||
    c.niveau?.nom.toLowerCase().includes(filter) ||
    `${c.matiere_nom} — ${c.pays?.nom} - ${c.niveau?.nom}`.toLowerCase().includes(filter)
  )
})

// Thèmes filtrés par contexte sélectionné et par texte
const filteredThemes = computed(() => {
  let filtered = themes.value

  // Filtrage par contexte sélectionné
  if (filters.value.contexte) {
    filtered = filtered.filter(theme =>
      String(theme.contexte) === String(filters.value.contexte)
    )
  }

  // Filtrage par texte du thème
  if (themeFilter.value) {
    const filter = themeFilter.value.toLowerCase()
    filtered = filtered.filter(theme =>
      theme.nom.toLowerCase().includes(filter) ||
      theme.contexte_detail?.matiere_nom.toLowerCase().includes(filter) ||
      theme.contexte_detail?.pays?.nom.toLowerCase().includes(filter) ||
      theme.contexte_detail?.niveau?.nom.toLowerCase().includes(filter) ||
      `${theme.nom} — ${theme.contexte_detail?.matiere_nom} — ${theme.contexte_detail?.pays?.nom} - ${theme.contexte_detail?.niveau?.nom}`.toLowerCase().includes(filter)
    )
  }

  return filtered
})

// Thèmes filtrés pour le formulaire (par texte seulement)
const filteredThemesForForm = computed(() => {
  if (!themeFormFilter.value) {
    return themes.value
  }
  const filter = themeFormFilter.value.toLowerCase()
  return themes.value.filter(theme =>
    theme.nom.toLowerCase().includes(filter) ||
    theme.contexte_detail?.matiere_nom.toLowerCase().includes(filter) ||
    theme.contexte_detail?.pays?.nom.toLowerCase().includes(filter) ||
    theme.contexte_detail?.niveau?.nom.toLowerCase().includes(filter) ||
    `${theme.nom} — ${theme.contexte_detail?.matiere_nom} — ${theme.contexte_detail?.pays?.nom} - ${theme.contexte_detail?.niveau?.nom}`.toLowerCase().includes(filter)
  )
})

const filteredThemesForModal = computed(() => {
  if (!duplicateThemeFilter.value) {
    return themes.value
  }
  const filter = duplicateThemeFilter.value.toLowerCase()
  return themes.value.filter(theme =>
    theme.nom.toLowerCase().includes(filter) ||
    theme.contexte_detail?.matiere_nom.toLowerCase().includes(filter) ||
    theme.contexte_detail?.pays?.nom.toLowerCase().includes(filter) ||
    theme.contexte_detail?.niveau?.nom.toLowerCase().includes(filter) ||
    `${theme.nom} — ${theme.contexte_detail?.matiere_nom} — ${theme.contexte_detail?.pays?.nom} - ${theme.contexte_detail?.niveau?.nom}`.toLowerCase().includes(filter)
  )
})

const paginatedNotions = computed(() => notions.value)
const totalItems = computed(() => totalNotions.value || 0)

// Computed properties pour la pagination
const totalPages = computed(() => {
  const total = totalItems.value
  return Math.ceil(total / itemsPerPage)
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

async function loadNotions(options = {}) {
  const { skipPageGuard = false } = options
  isLoadingNotions.value = true
  try {
    const page = Math.max(currentPage.value || 1, 1)
    const response = await getNotions({
      limit: itemsPerPage,
      offset: (page - 1) * itemsPerPage,
      theme: filters.value.theme || undefined,
      contexte: filters.value.contexte || undefined
    })
    const data = response?.data ?? response
    const results = Array.isArray(data?.results) ? data.results : (Array.isArray(data) ? data : [])
    const orderedResults = [...results].sort((a, b) => {
      const ao = Number(a?.ordre ?? 0)
      const bo = Number(b?.ordre ?? 0)
      if (ao !== bo) return ao - bo
      return String(a?.nom || '').localeCompare(String(b?.nom || ''))
    })
    notions.value = orderedResults
    const total = Number(data?.count ?? results.length ?? 0)
    totalNotions.value = Number.isFinite(total) ? total : results.length
    const maxPage = Math.max(1, Math.ceil((totalNotions.value || 0) / itemsPerPage))
    if (!skipPageGuard && totalNotions.value > 0 && currentPage.value > maxPage) {
      currentPage.value = maxPage
      await loadNotions({ skipPageGuard: true })
      return
    }
  } catch (error) {
    console.error('[AdminNotions] Erreur lors du chargement des notions:', error)
    notions.value = []
    totalNotions.value = 0
  } finally {
    isLoadingNotions.value = false
  }
}

async function loadInitial() {
  try {
    const [{ data: tData }, contextesRes] = await Promise.all([
      getThemes(),
      getContextes()
    ])
    themes.value = tData || []
    contextesOptions.value = Array.isArray(contextesRes) ? contextesRes : (contextesRes?.data || [])
  } catch (error) {
    console.error('[AdminNotions] Erreur lors du chargement des métadonnées:', error)
    themes.value = []
    contextesOptions.value = []
  } finally {
    await loadNotions()
  }
}

onMounted(loadInitial)

// Watcher pour réinitialiser le filtre thème quand le contexte change
watch(() => filters.value.contexte, (newContexte, oldContexte) => {
  if (newContexte !== oldContexte) {
    // Réinitialiser le filtre thème quand le contexte change
    filters.value.theme = ''
    // Réinitialiser la page courante
    currentPage.value = 1
    loadNotions()
  }
})

// Watcher pour réinitialiser la page courante quand le filtre thème change
watch(() => filters.value.theme, () => {
  currentPage.value = 1
  loadNotions()
})

function goToPage(page) {
  const total = totalPages.value || 0
  const maxPage = total > 0 ? total : 1
  const targetPage = Math.min(Math.max(page, 1), maxPage)
  if (targetPage === currentPage.value) return
  currentPage.value = targetPage
  loadNotions()
}

function nextPage() {
  if (totalPages.value && currentPage.value < totalPages.value) {
    currentPage.value += 1
    loadNotions()
  }
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value -= 1
    loadNotions()
  }
}

function resetForm() {
  form.value = { 
    id: null, 
    nom: '', 
    theme: '', 
    niveaux: [],
    ordre: 0,
    est_actif: true
  }
}

async function handleSave() {
  if (!form.value.nom || !form.value.theme) return

  try {
    const payload = {
      nom: form.value.nom,
      theme: Number(form.value.theme),
      niveaux: [],
      ordre: form.value.ordre,
      est_actif: form.value.est_actif
    }

    if (form.value.id) {
      await updateNotion(form.value.id, payload)
    } else {
      await createNotion(payload)
    }

    // Sauvegarder le thème actuel avant de reset le formulaire
    const currentTheme = form.value.theme

    resetForm()

    // Remettre le thème sélectionné pour permettre d'ajouter une autre notion dans le même thème
    form.value.theme = currentTheme

    await loadNotions()
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
    niveaux: [],
    ordre: notion.ordre || 0,
    est_actif: notion.est_actif !== false
  }
}

async function toggleNotionActive(notion, value) {
  const prev = notion.est_actif
  notion.est_actif = value
  try {
    await updateNotion(notion.id, { est_actif: value })
  } catch (e) {
    console.error('[AdminNotions] Erreur de mise à jour du statut:', e)
    notion.est_actif = prev
    alert("Impossible de mettre à jour le statut de la notion.")
  }
}

async function removeNotion(id) {
  try {
    await deleteNotion(id)
    await loadNotions()
  } catch (e) {
    console.error('Erreur:', e)
  }
}

// Nouvelle fonction qui utilise le composant AdminActionsButtons
function handleDeleteNotion(notion) {
  removeNotion(notion.id)
}

async function handleDuplicateNotion(notion) {
  // Open modal pre-filled with same theme
  duplicateThemeFilter.value = ''
  duplicateState.value = {
    open: true,
    sourceNotion: notion,
    targetTheme: notion.theme || '',
    newTitle: notion.nom || ''
  }
}

function closeDuplicateModal() {
  duplicateState.value.open = false
}

async function confirmDuplicate() {
  const src = duplicateState.value.sourceNotion
  const targetThemeId = Number(duplicateState.value.targetTheme)
  const newTitle = (duplicateState.value.newTitle || '').trim()
  if (!src || !targetThemeId) return
  try {
    await duplicateNotion(src.id, { theme: targetThemeId, nom: newTitle })
    closeDuplicateModal()
    await loadNotions()
  } catch (e) {
    console.error('[AdminNotions] Erreur de duplication:', e)
    alert('Erreur lors de la duplication de la notion')
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
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.inline-field {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.checkbox-label {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  color: #374151;
  cursor: pointer;
}

.checkbox-label input[type='checkbox'] {
  width: 16px;
  height: 16px;
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

.status-toggle {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.status-toggle input[type='checkbox'] {
  width: 16px;
  height: 16px;
  accent-color: #10b981;
}

.status-pill {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.2rem 0.5rem;
  border-radius: 999px;
  border: 1px solid transparent;
}

.status-pill.active {
  background: #ecfdf5;
  color: #047857;
  border-color: rgba(16, 185, 129, 0.35);
}

.status-pill.inactive {
  background: #fef2f2;
  color: #b91c1c;
  border-color: rgba(239, 68, 68, 0.35);
}

.loading-row {
  text-align: center;
  color: #6b7280;
  font-style: italic;
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
