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
          <th>Thème</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="notion in filteredNotions" :key="notion.id">
          <td>{{ notion.id }}</td>
          <td>{{ notion.ordre || 0 }}</td>
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
          <td colspan="5" style="text-align:center; font-style: italic;">Aucune notion trouvée.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { getNotions, createNotion, updateNotion, deleteNotion } from '@/api/notions'
import { getThemes } from '@/api/themes'
import { getContextes } from '@/api/matiere-contextes.js'
import PaysNiveauxSelector from '@/components/admin/PaysNiveauxSelector.vue'
import PaysNiveauxDisplay from '@/components/admin/PaysNiveauxDisplay.vue'
import { AdminActionsButtons } from '@/components/admin'

const notions = ref([])
const themes = ref([])
const contextesOptions = ref([])
const contexteFilter = ref('')
const themeFilter = ref('')
const themeFormFilter = ref('')
const form = ref({
  id: null,
  nom: '',
  theme: '',
  niveaux: [],
  ordre: 0
})
const filters = ref({
  theme: '',
  contexte: ''
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

const filteredNotions = computed(() => {
  let filtered = notions.value
  
  // Filtrage par contexte
  if (filters.value.contexte) {
    filtered = filtered.filter(n => {
      // Trouver le thème de la notion
      const theme = themes.value.find(t => t.id === n.theme)
      return theme && String(theme.contexte) === String(filters.value.contexte)
    })
  }
  
  // Filtrage par thème
  if (filters.value.theme) {
    filtered = filtered.filter(n =>
      String(n.theme) === String(filters.value.theme)
    )
  }

  // Tri par ordre puis par nom
  return [...filtered].sort((a, b) => {
    const ao = Number(a?.ordre ?? 0)
    const bo = Number(b?.ordre ?? 0)
    if (ao !== bo) return ao - bo
    return String(a?.nom || '').localeCompare(String(b?.nom || ''))
  })
})

async function load() {
  try {
    const [{ data: nData }, { data: tData }, contextesRes] = await Promise.all([
      getNotions(),
      getThemes(),
      getContextes()
    ])
    notions.value = nData || []
    themes.value = tData || []
    contextesOptions.value = Array.isArray(contextesRes) ? contextesRes : (contextesRes?.data || [])
  } catch (error) {
    console.error('[AdminNotions] Erreur lors du chargement:', error)
    notions.value = []
    themes.value = []
    contextesOptions.value = []
  }
}

onMounted(load)

// Watcher pour réinitialiser le filtre thème quand le contexte change
watch(() => filters.value.contexte, (newContexte, oldContexte) => {
  if (newContexte !== oldContexte) {
    // Réinitialiser le filtre thème quand le contexte change
    filters.value.theme = ''
  }
})

function resetForm() {
  form.value = { 
    id: null, 
    nom: '', 
    theme: '', 
    niveaux: [],
    ordre: 0
  }
}

async function handleSave() {
  if (!form.value.nom || !form.value.theme) return

  try {
    const payload = {
      nom: form.value.nom,
      theme: Number(form.value.theme),
      niveaux: [],
      ordre: form.value.ordre
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
    niveaux: [],
    ordre: notion.ordre || 0
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
</style>
