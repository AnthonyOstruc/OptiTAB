<template>
  <div>
    <h2 class="admin-title">Gestion des Exercices</h2>
    <form class="admin-form" @submit.prevent="handleSave">
      <!-- Sélecteur simple: on choisit uniquement le chapitre -->
      <div class="form-group">
        <label>Chapitre:</label>
        <select v-model="form.chapitre" required>
          <option value="">Choisir un chapitre</option>
          <option v-for="c in chapitres" :key="c.id" :value="c.id">{{ formatChapitreOption(c) }}</option>
        </select>
      </div>
      <div v-if="currentContext" class="context-panel">
        <div class="context-row"><strong>Matière:</strong> <span>{{ currentContext.matiereNom || '—' }}</span></div>
        <div class="context-row"><strong>Thème:</strong> <span>{{ currentContext.themeNom || '—' }}</span></div>
        <div class="context-row"><strong>Pays:</strong> <span>{{ currentContext.paysNom || '—' }}</span></div>
        <div class="context-row"><strong>Niveau:</strong> <span>{{ currentContext.niveauNom || '—' }}</span></div>
        <div class="context-row"><strong>Chemin:</strong> <span>{{ getContextLabelByChapitre(form.chapitre) }}</span></div>
        <div class="context-row"><strong>Code:</strong> <code>{{ getContextCodeByChapitre(form.chapitre) }}</code></div>
      </div>
      
      <div class="form-group">
        <label>Titre:</label>
        <input v-model="form.nom" placeholder="Titre de l'exercice" required />
      </div>

      
      
      <div class="form-group">
        <label>Énoncé:</label>
        <textarea v-model="form.enonce" rows="4" required></textarea>
      </div>
      
      <div class="form-group">
        <label>Solution:</label>
        <textarea v-model="form.solution" rows="4"></textarea>
      </div>
      
      <div class="form-group">
        <label>Difficulté:</label>
        <select v-model="form.difficulte">
          <option value="facile">Facile</option>
          <option value="moyen">Moyen</option>
          <option value="difficile">Difficile</option>
        </select>
      </div>
      
      
      
      <button class="btn-primary" type="submit">{{ form.id ? 'Mettre à jour' : 'Créer' }}</button>
      <button v-if="form.id" class="btn-secondary" type="button" @click="resetForm">Annuler</button>
      <button class="btn-secondary" type="button" @click="handlePreview">Prévisualiser</button>
    </form>

    <!-- Prévisualisation -->
    <div v-if="showPreview && previewData" class="preview-section">
      <h3>Aperçu de l'exercice {{ form.id ? '(Mode édition)' : '(Mode création)' }}</h3>
      <div class="preview-item">
        <ExerciceQCM 
          :eid="`preview-${form.id || 'new'}`" 
          :titre="previewData.titre" 
          :instruction="previewData.instruction" 
          :etapes="previewData.etapes" 
          :solution="previewData.solution" 
          :difficulty="previewData.difficulty" 
        />
      </div>
    </div>

    <!-- Filtres -->
    <div class="filters">
      <div class="filter-group">
        <label>Filtrer par chapitre:</label>
        <select v-model="filters.chapitre" :disabled="chapitres.length === 0">
          <option value="">Tous les chapitres</option>
          <option v-for="c in chapitres" :key="c.id" :value="c.id">{{ c.nom }}</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label>Filtrer par type:</label>
        <select v-model="filters.type">
          <option value="">Tous les types</option>
          <option value="qcm">QCM</option>
          <option value="calcul">Calcul</option>
          <option value="demonstration">Démonstration</option>
          <option value="probleme">Problème</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label>Rechercher:</label>
        <input v-model="filters.nom" type="text" placeholder="Rechercher dans l'énoncé..." />
      </div>
    </div>

    <!-- Tableau des exercices -->
    <table class="admin-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Titre</th>
          <th>Chapitre</th>
          <th>Contexte</th>
          <th>Difficulté</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="exercice in filteredExercices" :key="exercice.id">
          <td>{{ exercice.id }}</td>
          <td>{{ exercice.titre || exercice.nom }}</td>
          <td>{{ getChapitreName(exercice.chapitre) }}</td>
          <td class="ctx-cell">{{ getContextLabelByChapitre(exercice.chapitre) }}</td>
          <td>
            <span class="difficulte-badge" :class="`difficulte-${exercice.difficulte || exercice.difficulty}`">
              {{ exercice.difficulte || exercice.difficulty }}
            </span>
          </td>
          <td>
            <AdminActionsButtons
              :item="exercice"
              :actions="['edit', 'duplicate', 'delete']"
              edit-label="Éditer"
              duplicate-label="Dupliquer"
              confirm-message="Êtes-vous sûr de vouloir supprimer cet exercice ?"
              @edit="editExercice"
              @duplicate="handleDuplicateExercice"
              @delete="handleDeleteExercice"
            />
          </td>
        </tr>
        <tr v-if="filteredExercices.length === 0">
          <td colspan="6" style="text-align:center; font-style: italic;">Aucun exercice trouvé.</td>
        </tr>
      </tbody>
    </table>

    <!-- Modale de duplication -->
    <div v-if="showDuplicateModal" class="modal-overlay" @click="cancelDuplicate">
      <div class="modal-content" @click.stop>
        <h3>Dupliquer l'exercice</h3>
        <p class="modal-description">
          Créer une copie de "<strong>{{ duplicateForm.originalExercice?.titre || duplicateForm.originalExercice?.nom }}</strong>"
        </p>

        <div class="modal-form">
          <div class="form-group">
            <label>Nouveau chapitre:</label>
            <select v-model="duplicateForm.newChapitre" required>
              <option value="">Choisir un chapitre</option>
              <option v-for="c in chapitres" :key="c.id" :value="c.id">{{ formatChapitreOption(c) }}</option>
            </select>
          </div>

          <div class="form-group">
            <label>Nouveau titre:</label>
            <input v-model="duplicateForm.newTitre" placeholder="Titre de la copie" required />
          </div>
        </div>

        <div class="modal-actions">
          <button class="btn-secondary" @click="cancelDuplicate">Annuler</button>
          <button class="btn-primary" @click="confirmDuplicate" :disabled="!duplicateForm.newChapitre || !duplicateForm.newTitre.trim()">
            Dupliquer
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { getExercices, createExercice, updateExercice, deleteExercice, getChapitres, getNotions } from '@/api'
import PaysNiveauxSelector from '@/components/admin/PaysNiveauxSelector.vue'
import PaysNiveauxDisplay from '@/components/admin/PaysNiveauxDisplay.vue'
import { AdminActionsButtons } from '@/components/admin'
import ExerciceQCM from '@/components/UI/ExerciceQCM.vue'

const exercices = ref([])
const chapitres = ref([])
const notions = ref([])
const selection = ref({})
const form = ref({ 
  id: null, 
  chapitre: '', 
  nom: '',
  enonce: '', 
  solution: '', 
  difficulte: 'moyen',
  niveaux: []
})
const filters = ref({
  chapitre: '',
  type: '',
  nom: ''
})
const showPreview = ref(false)
const previewData = ref(null)
const showDuplicateModal = ref(false)
const duplicateForm = ref({
  originalExercice: null,
  newChapitre: '',
  newTitre: ''
})

// Computed properties
const filteredExercices = computed(() => {
  let filtered = exercices.value
  
  if (filters.value.chapitre) {
    filtered = filtered.filter(e => e.chapitre == filters.value.chapitre)
  }
  
  if (filters.value.type) {
    filtered = filtered.filter(e => e.type === filters.value.type)
  }
  
  if (filters.value.nom) {
    const needle = String(filters.value.nom).toLowerCase()
    filtered = filtered.filter(e => {
      const hay = String(e.titre || e.nom || e.question || e.contenu || '').toLowerCase()
      return hay.includes(needle)
    })
  }
  
  return filtered
})

async function loadInitial() {
  try {
    const [chs, nts] = await Promise.all([
      getChapitres(),
      getNotions()
    ])
    chapitres.value = chs || []
    notions.value = nts || []
    await reloadExercices()
  } catch (error) {
    console.error('[AdminExercices] Erreur chargement chapitres:', error)
  }
}

onMounted(loadInitial)

// Watchers simples

watch(() => form.value.chapitre, async () => {
  await reloadExercices()
})

async function reloadExercices() {
  try {
    const params = {}
    if (form.value.chapitre) params.chapitre = Number(form.value.chapitre)
    exercices.value = await getExercices(params)
  } catch (error) {
    console.error('[AdminExercices] Erreur lors du chargement exercices:', error)
    exercices.value = []
  }
}

function resetForm() {
  form.value = { 
    id: null, 
    chapitre: '', 
    nom: '',
    type: '', 
    enonce: '', 
    solution: '', 
    difficulte: 'moyen',
    niveaux: []
  }
  showPreview.value = false
  previewData.value = null
}

async function handleSave() {
  if (!form.value.chapitre || !form.value.enonce) return
  
  try {
    const difficultyMap = { 'facile': 'easy', 'moyen': 'medium', 'difficile': 'hard' }
    const payload = {
      chapitre: Number(form.value.chapitre),
      titre: form.value.nom || 'Exercice',
      contenu: form.value.enonce,
      difficulty: difficultyMap[form.value.difficulte] || 'medium',
      // Champs compatibles modèle Exercice
      question: form.value.enonce,
      reponse_correcte: form.value.solution || '',
      points: 1
    }
    
    if (form.value.id) {
      await updateExercice(form.value.id, payload)
    } else {
      await createExercice(payload)
    }
    resetForm()
    await reloadExercices()
  } catch (e) {
    console.error('[AdminExercices] Erreur:', e)
  }
}

function editExercice(exercice) {
  // Extraire les IDs des niveaux pour le composant PaysNiveauxSelector
  const niveauxIds = exercice.niveaux ? exercice.niveaux.map(n => n.id) : []
  
  // Mapper les champs de l'exercice vers le formulaire
  const difficultyMap = { 'easy': 'facile', 'medium': 'moyen', 'hard': 'difficile' }
  
  form.value = { 
    id: exercice.id,
    chapitre: exercice.chapitre,
    nom: exercice.titre || exercice.nom || '',
    enonce: exercice.contenu || exercice.question || exercice.enonce || '',
    solution: exercice.reponse_correcte || exercice.solution || '',
    difficulte: difficultyMap[exercice.difficulty] || exercice.difficulte || 'moyen',
    niveaux: niveauxIds
  }
  
  // Masquer la prévisualisation lors de l'édition
  showPreview.value = false
  previewData.value = null
  
  console.log('🔍 Exercice à éditer:', exercice)
  console.log('📝 Formulaire rempli:', form.value)
}

async function removeExercice(id) {
  try {
    await deleteExercice(id)
    await reloadExercices()
  } catch (e) {
    console.error('Erreur:', e)
  }
}

// Nouvelle fonction qui utilise le composant AdminActionsButtons
function handleDeleteExercice(exercice) {
  removeExercice(exercice.id)
}

// Fonction pour dupliquer un exercice
function handleDuplicateExercice(exercice) {
  duplicateForm.value = {
    originalExercice: exercice,
    newChapitre: '',
    newTitre: `${exercice.titre || exercice.nom}`
  }
  showDuplicateModal.value = true
}

// Fonction pour confirmer la duplication
async function confirmDuplicate() {
  if (!duplicateForm.value.newChapitre || !duplicateForm.value.newTitre.trim()) {
    alert('Veuillez sélectionner un chapitre et saisir un titre pour la copie.')
    return
  }

  try {
    const original = duplicateForm.value.originalExercice
    const difficultyMap = { 'easy': 'easy', 'medium': 'medium', 'hard': 'hard' }

    const payload = {
      chapitre: Number(duplicateForm.value.newChapitre),
      titre: duplicateForm.value.newTitre.trim(),
      contenu: original.contenu || original.question || original.enonce || '',
      difficulty: original.difficulty || difficultyMap[original.difficulte] || 'medium',
      question: original.contenu || original.question || original.enonce || '',
      reponse_correcte: original.reponse_correcte || original.solution || '',
      etapes: original.etapes || '',
      points: original.points || 1
    }

    await createExercice(payload)
    await reloadExercices()

    showDuplicateModal.value = false
    duplicateForm.value = {
      originalExercice: null,
      newChapitre: '',
      newTitre: ''
    }

    alert('Exercice dupliqué avec succès !')
  } catch (error) {
    console.error('Erreur lors de la duplication:', error)
    alert('Erreur lors de la duplication de l\'exercice.')
  }
}

// Fonction pour annuler la duplication
function cancelDuplicate() {
  showDuplicateModal.value = false
  duplicateForm.value = {
    originalExercice: null,
    newChapitre: '',
    newTitre: ''
  }
}

// Fonction de prévisualisation
function handlePreview() {
  if (!form.value.nom || !form.value.enonce) {
    alert('Veuillez remplir au moins le titre et l\'énoncé pour prévisualiser')
    return
  }
  
  const difficultyMap = { 'facile': 'easy', 'moyen': 'medium', 'difficile': 'hard' }
  
  previewData.value = {
    titre: form.value.nom,
    instruction: form.value.enonce,
    etapes: '', // Pas d'étapes dans ce formulaire simple
    solution: form.value.solution || '',
    difficulty: difficultyMap[form.value.difficulte] || 'medium'
  }
  
  showPreview.value = true
}

// Helpers d'affichage
function getChapitreName(id) {
  const c = chapitres.value.find(x => String(x.id) === String(id))
  return c ? c.nom : id
}

function getNotionById(id) {
  return notions.value.find(x => String(x.id) === String(id))
}

function chapterContext(chapitre) {
  if (!chapitre) return null
  const notion = getNotionById(chapitre.notion)
  if (!notion) return { themeNom: '', matiereNom: '', paysNom: '', niveauNom: '' }
  const matiereNom = notion.matiere_nom || (notion.contexte_detail && notion.contexte_detail.matiere_nom) || ''
  const themeNom = notion.theme_nom || ''
  const paysNom = notion.contexte_detail && notion.contexte_detail.pays ? notion.contexte_detail.pays.nom : ''
  const niveauNom = notion.contexte_detail && notion.contexte_detail.niveau ? notion.contexte_detail.niveau.nom : ''
  return { matiereNom, themeNom, paysNom, niveauNom }
}

const currentContext = computed(() => {
  const c = chapitres.value.find(x => String(x.id) === String(form.value.chapitre))
  return c ? chapterContext(c) : null
})

function formatChapitreOption(c) {
  const n = getNotionById(c.notion)
  const ctx = chapterContext(c)
  const parts = [
    c.nom,
    n ? `— ${n.nom}` : '',
    ctx && ctx.matiereNom ? `— ${ctx.matiereNom}` : '',
    ctx && (ctx.paysNom || ctx.niveauNom) ? `— ${[ctx.paysNom, ctx.niveauNom].filter(Boolean).join(' · ')}` : ''
  ].filter(Boolean)
  return parts.join(' ')
}

function slugify(text) {
  return String(text || '')
    .normalize('NFD').replace(/\p{Diacritic}/gu, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '')
}

function getContextLabelByChapitre(chapitreId) {
  const c = chapitres.value.find(x => String(x.id) === String(chapitreId))
  if (!c) return ''
  const n = getNotionById(c.notion)
  const ctx = chapterContext(c)
  const path = [
    ctx?.matiereNom,
    ctx?.themeNom,
    n?.nom,
    c.nom,
    ctx?.paysNom,
    ctx?.niveauNom
  ].filter(Boolean)
  return path.join(' › ')
}

function getContextCodeByChapitre(chapitreId) {
  const c = chapitres.value.find(x => String(x.id) === String(chapitreId))
  if (!c) return ''
  const n = getNotionById(c.notion)
  const ctx = chapterContext(c)
  const tokens = [
    slugify(n?.nom),
    slugify(ctx?.themeNom),
    slugify(ctx?.matiereNom),
    slugify(ctx?.paysNom),
    slugify(ctx?.niveauNom)
  ].filter(Boolean)
  return tokens.join('_')
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
  min-height: 100px;
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

.ctx-cell { color: #64748b; font-size: 0.8rem; max-width: 320px; }

.admin-table th {
  background: #f9fafb;
  font-weight: 600;
  color: #374151;
}

.admin-table tr:hover {
  background: #f9fafb;
}

.type-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
}

.type-qcm {
  background: #dbeafe;
  color: #1e40af;
}

.type-calcul {
  background: #dcfce7;
  color: #166534;
}

.type-demonstration {
  background: #fef3c7;
  color: #92400e;
}

.type-probleme {
  background: #fce7f3;
  color: #be185d;
}

.difficulte-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
}

.difficulte-facile {
  background: #dcfce7;
  color: #166534;
}

.difficulte-moyen {
  background: #fef3c7;
  color: #92400e;
}

.difficulte-difficile {
  background: #fee2e2;
  color: #991b1b;
}

.context-panel { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 1rem; }
.context-row { display: flex; gap: 0.5rem; font-size: 0.9rem; color: #334155; }

.preview-section {
  margin-top: 2rem;
  margin-bottom: 2rem;
}

.preview-section h3 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #1f2937;
}

.preview-item {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Styles pour la modale de duplication */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.modal-content h3 {
  margin: 0 0 1rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.modal-description {
  margin: 0 0 1.5rem 0;
  color: #6b7280;
  font-size: 0.9rem;
}

.modal-form {
  margin-bottom: 2rem;
}

.modal-form .form-group {
  margin-bottom: 1rem;
}

.modal-form .form-group:last-child {
  margin-bottom: 0;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.modal-actions .btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style> 