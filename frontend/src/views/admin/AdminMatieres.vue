<template>
  <div>
    <h2 class="admin-title">Gestion des Matières</h2>
    <form class="admin-form" @submit.prevent="handleSave">
      <input v-model="form.nom" placeholder="Nom de la matière" required />
      <textarea v-model="form.description" placeholder="Description"></textarea>
      <textarea v-model="form.svg_icon" placeholder="Code SVG"></textarea>
      
      <!-- Contextes (Matière + Niveau) -->
      <div class="contextes-panel">
        <h3>Contextes (Matière + Niveau)</h3>
        <div class="contextes-actions">
          <select v-model="contextForm.niveau" class="select">
            <option value="">Sélectionner un niveau</option>
            <optgroup v-for="g in niveauxByPays" :key="g.pays_id" :label="g.pays_nom">
              <option 
                v-for="n in g.niveaux"
                :key="n.id" 
                :value="n.id"
                :disabled="isContexteExisting(n.id)"
              >
                {{ n.nom }}
              </option>
            </optgroup>
          </select>
          <button class="btn-primary" type="button" @click="addContexte" :disabled="!form.id || !contextForm.niveau || addLoading">
            <span v-if="addLoading">Ajout...</span>
            <span v-else>Ajouter</span>
          </button>
        </div>

        <div class="chips" v-if="(contextesByMatiere[form.id] || []).length">
          <span class="chip" v-for="c in contextesByMatiere[form.id]" :key="c.id">
            {{ c.pays.nom }} - {{ c.niveau.nom }}
            <button class="chip-remove" title="Retirer" @click="removeContexte(c.id)" :disabled="removeLoadingId===c.id">×</button>
          </span>
        </div>
        <small class="hint">Créez des contextes pour lier cette matière à des niveaux/pays.</small>
      </div>
      
      <button class="btn-primary" type="submit">{{ form.id ? 'Mettre à jour' : 'Créer' }}</button>
      <button v-if="form.id" class="btn-secondary" type="button" @click="resetForm">Annuler</button>
    </form>

    <table class="admin-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nom</th>
          <th>Description</th>
          <th>Contextes (aperçu)</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="m in matieres" :key="m.id">
          <td>{{ m.id }}</td>
          <td>{{ m.nom }}</td>
          <td>{{ m.description }}</td>
          <td>
            <div class="pays-badges">
              <span
                v-for="c in (m.contextes || [])"
                :key="c.id"
                class="pays-badge"
                :title="(c.pays?.nom || '') + ' - ' + (c.niveau?.nom || '')"
              >
                <span class="pays-flag">{{ c.pays?.drapeau_emoji || '🏳️' }}</span>
                <span class="pays-name">{{ (c.pays?.nom || '') + ' - ' + (c.niveau?.nom || '') }}</span>
              </span>
              <span v-if="!(m.contextes && m.contextes.length)" class="pays-empty">Aucun</span>
            </div>
          </td>
          <td>
            <button class="btn-toggle-home" :class="{ active: !!m.show_on_home }" @click="toggleHome(m)" :disabled="togglingId===m.id" :title="m.show_on_home ? 'Cacher de l\'accueil' : 'Afficher sur l\'accueil'">
              <span v-if="togglingId===m.id" class="btn-toggle-loading">⋯</span>
              <template v-else>
                <span class="btn-toggle-icon">{{ m.show_on_home ? '🏠' : '🏡' }}</span>
                <span class="btn-toggle-text">{{ m.show_on_home ? 'Oui' : 'Non' }}</span>
              </template>
            </button>
            <AdminActionsButtons
              :item="m"
              :actions="['edit', 'delete']"
              edit-label="Éditer"
              confirm-message="Êtes-vous sûr de vouloir supprimer cette matière ?"
              @edit="editMatiere"
              @delete="handleDeleteMatiere"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getMatieresAdmin, createMatiere, updateMatiere, deleteMatiere } from '@/api/matieres'
import { getNiveaux } from '@/api/pays'
import { getContextes, createContexte, deleteContexte } from '@/api/matiere-contextes'
import { AdminActionsButtons } from '@/components/admin'

const matieres = ref([])
const niveauxOptions = ref([])
const contextesByMatiere = ref({})
const contextForm = ref({ niveau: '' })
const addLoading = ref(false)
const removeLoadingId = ref(null)
const togglingId = ref(null)

const niveauxByPays = computed(() => {
  const map = new Map()
  for (const n of niveauxOptions.value || []) {
    const key = n.pays || n.pays_id || n.pays_nom
    if (!map.has(key)) {
      map.set(key, { pays_id: key, pays_nom: n.pays_nom || 'Pays', niveaux: [] })
    }
    map.get(key).niveaux.push(n)
  }
  return Array.from(map.values()).sort((a,b)=>a.pays_nom.localeCompare(b.pays_nom))
})

function isContexteExisting(niveauId) {
  const list = contextesByMatiere.value[form.value.id] || []
  return list.some(c => c.niveau?.id === niveauId || c.niveau === niveauId)
}
const form = ref({ 
  id: null, 
  nom: '', 
  description: '', 
  svg_icon: ''
})

async function load() {
  try {
    const { data } = await getMatieresAdmin()
    matieres.value = data || []
    niveauxOptions.value = await getNiveaux({ est_actif: true })
    await refreshContextes()
  } catch (error) {
    console.error('Erreur lors du chargement des matières:', error)
    matieres.value = []
  }
}

async function toggleHome(m) {
  try {
    togglingId.value = m.id
    const next = !m.show_on_home
    await updateMatiere(m.id, { show_on_home: next })
    const idxLocal = matieres.value.findIndex(x => x.id === m.id)
    if (idxLocal !== -1) matieres.value[idxLocal] = { ...matieres.value[idxLocal], show_on_home: next }
  } catch (e) {
    console.error('Erreur lors du basculement accueil:', e)
  } finally {
    togglingId.value = null
  }
}

onMounted(load)

function resetForm() {
  form.value = { 
    id: null, 
    nom: '', 
    description: '', 
    svg_icon: ''
  }
  contextForm.value.niveau = ''
}

async function handleSave() {
  if (!form.value.nom) return
  
  try {
    if (form.value.id) {
      await updateMatiere(form.value.id, form.value)
    } else {
      await createMatiere(form.value)
    }
    resetForm()
    await load()
  } catch (e) {
    console.error('Erreur lors de la sauvegarde:', e)
  }
}

function editMatiere(matiere) {
  form.value = { 
    id: matiere.id, 
    nom: matiere.nom || matiere.titre || '', 
    description: matiere.description || '', 
    svg_icon: matiere.svg_icon || ''
  }
  contextForm.value.niveau = ''
}

async function handleDeleteMatiere(matiere) {
  try {
    await deleteMatiere(matiere.id)
    await load()
  } catch (e) {
    console.error('Erreur lors de la suppression:', e)
  }
}

// Contextes helpers
async function refreshContextes() {
  try {
    const list = await getContextes()
    const map = {}
    for (const c of list) {
      if (!map[c.matiere]) map[c.matiere] = []
      map[c.matiere].push(c)
    }
    contextesByMatiere.value = map
  } catch (e) {
    console.error('Erreur lors du chargement des contextes:', e)
  }
}

async function addContexte() {
  if (!form.value.id || !contextForm.value.niveau) return
  try {
    addLoading.value = true
    await createContexte({ matiere: form.value.id, niveau: contextForm.value.niveau })
    await refreshContextes()
    contextForm.value.niveau = ''
  } catch (e) {
    console.error('Erreur lors de l\'ajout du contexte:', e)
  } finally {
    addLoading.value = false
  }
}

async function removeContexte(contexteId) {
  try {
    removeLoadingId.value = contexteId
    await deleteContexte(contexteId)
    await refreshContextes()
  } catch (e) {
    console.error('Erreur lors de la suppression du contexte:', e)
  } finally {
    removeLoadingId.value = null
  }
}

// plus de calcul pays/niveaux ici
</script>

<style scoped>
.admin-title {
  margin-bottom: 20px;
  color: #333;
}

.admin-form {
  background: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.contextes-panel {
  margin-top: 16px;
  padding: 12px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}
.contextes-panel h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
}
.contextes-actions {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-bottom: 8px;
}
.contextes-actions .select {
  min-width: 280px;
  padding: 6px 8px;
}
.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 8px;
}
.chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #eef2ff;
  color: #3730a3;
  border: 1px solid #c7d2fe;
  padding: 4px 8px;
  border-radius: 9999px;
  font-size: 12px;
}
.chip-remove {
  border: none;
  background: transparent;
  color: #4f46e5;
  cursor: pointer;
  font-size: 14px;
}

.admin-form input,
.admin-form textarea {
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.admin-table th,
.admin-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.admin-table td:last-child {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.pays-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.pays-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 2px 8px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: #f8fafc;
  font-size: 12px;
  color: #374151;
}

.pays-flag {
  font-size: 14px;
}

.pays-name {
  line-height: 1;
}

.pays-empty {
  color: #6b7280;
  font-style: italic;
}

.admin-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.btn-primary {
  background: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
}

.btn-secondary {
  background: #6c757d;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}
</style> 




<style scoped>
.btn-toggle-home {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  background: #ffffff;
  color: #6b7280;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s ease;
  white-space: nowrap;
}
.btn-toggle-home:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #d1d5db;
  transform: translateY(-1px);
}
.btn-toggle-home:active:not(:disabled) {
  transform: translateY(0);
}
.btn-toggle-home:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.btn-toggle-home.active {
  background: #eff6ff;
  border-color: #3b82f6;
  color: #1e40af;
}
.btn-toggle-home.active:hover:not(:disabled) {
  background: #dbeafe;
  border-color: #2563eb;
}
.btn-toggle-icon {
  font-size: 16px;
  line-height: 1;
}
.btn-toggle-text {
  font-size: 13px;
  font-weight: 600;
}
.btn-toggle-loading {
  display: inline-block;
  font-size: 18px;
  line-height: 1;
  animation: pulse 1.5s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style>


