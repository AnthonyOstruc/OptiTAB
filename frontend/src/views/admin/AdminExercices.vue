<template>
  <div>
    <h2 class="admin-title">Gestion des Exercices</h2>
    <form class="admin-form" @submit.prevent="handleSave">
      <!-- Sélecteur simple: on choisit uniquement le chapitre -->
      <div class="form-group">
        <label>Chapitre:</label>
        <input v-model="chapitreFormFilter" type="text" placeholder="Filtrer les chapitres..." class="filter-input" />
        <select v-model="form.chapitre" required>
          <option value="">Choisir un chapitre</option>
          <option value="all">✓ Tous les chapitres</option>
          <option v-for="c in filteredChapitresForForm" :key="c.id" :value="c.id">{{ formatChapitreOption(c) }}</option>
        </select>
      </div>
      <div v-if="currentContext" class="context-panel">
        <div v-if="currentContext.isAllChapters" class="context-header">
          <h4>📚 Vue d'ensemble - Tous les chapitres</h4>
        </div>
        <div class="context-row"><strong>Matière:</strong> <span>{{ currentContext.matiereNom || '—' }}</span></div>
        <div class="context-row"><strong>Thème:</strong> <span>{{ currentContext.themeNom || '—' }}</span></div>
        <div class="context-row"><strong>Pays:</strong> <span>{{ currentContext.paysNom || '—' }}</span></div>
        <div class="context-row"><strong>Niveau:</strong> <span>{{ currentContext.niveauNom || '—' }}</span></div>
        <div class="context-row"><strong>Chemin:</strong> <span>{{ getContextLabelByChapitre(form.chapitre) }}</span></div>
        <div class="context-row"><strong>Code:</strong> <code>{{ getContextCodeByChapitre(form.chapitre) }}</code></div>
        <div v-if="currentContext.isAllChapters" class="context-stats">
          <div class="stat-item">📖 {{ chapitres.length }} chapitre{{ chapitres.length > 1 ? 's' : '' }}</div>
          <div class="stat-item">📝 {{ exercices.length }} exercice{{ exercices.length > 1 ? 's' : '' }}</div>
        </div>
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
        <label>Méthode de résolution:</label>
        <textarea v-model="form.etapes" rows="4" placeholder="Décrivez les étapes de résolution..."></textarea>
      </div>
      
      <div class="form-group">
        <label>Solution:</label>
        <textarea v-model="form.solution" rows="4"></textarea>
      </div>
      
      <div class="form-group">
        <label>Difficulté:</label>
        <select v-model="form.difficulte" class="difficulty-select">
          <option value="facile">Facile</option>
          <option value="moyen">Moyen</option>
          <option value="difficile">Difficile</option>
        </select>
      </div>
      
      <div class="form-actions">
        <button class="btn-primary" type="submit">{{ form.id ? 'Mettre à jour' : 'Créer' }}</button>
        <button v-if="form.id" class="btn-secondary" type="button" @click="resetForm">Annuler</button>
        <button class="btn-preview" type="button" @click="handlePreview">Prévisualiser</button>
      </div>
    </form>

    <!-- Prévisualisation -->
    <div v-if="showPreview && previewData" class="preview-section">
      <div class="preview-header">
        <h3>Aperçu de l'exercice {{ form.id ? '(Mode édition)' : '(Mode création)' }}</h3>
        <button class="btn-close-preview" @click="closePreview" title="Fermer la prévisualisation">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 6L6 18"/>
            <path d="M6 6l12 12"/>
          </svg>
        </button>
      </div>
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
        <input v-model="chapitreFilter" type="text" placeholder="Filtrer les chapitres..." class="filter-input" />
        <select v-model="filters.chapitre" :disabled="filteredChapitres.length === 0">
          <option value="">Tous les chapitres</option>
          <option v-for="c in filteredChapitres" :key="c.id" :value="c.id">{{ c.nom }}</option>
        </select>
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
const chapitreFormFilter = ref('')
const chapitreFilter = ref('')
const selection = ref({})
const form = ref({ 
  id: null, 
  chapitre: '', 
  nom: '',
  enonce: '', 
  etapes: '', 
  solution: '', 
  difficulte: 'moyen',
  niveaux: []
})
const filters = ref({
  chapitre: ''
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

  return filtered
})

// Chapitres filtrés pour le formulaire (par texte seulement)
const filteredChapitresForForm = computed(() => {
  if (!chapitreFormFilter.value) {
    return chapitres.value
  }
  const filter = chapitreFormFilter.value.toLowerCase()
  return chapitres.value.filter(chapitre =>
    formatChapitreOption(chapitre).toLowerCase().includes(filter)
  )
})

// Chapitres filtrés pour les filtres (par texte seulement)
const filteredChapitres = computed(() => {
  if (!chapitreFilter.value) {
    return chapitres.value
  }
  const filter = chapitreFilter.value.toLowerCase()
  return chapitres.value.filter(chapitre =>
    formatChapitreOption(chapitre).toLowerCase().includes(filter)
  )
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
    // Ne pas filtrer quand "Tous les chapitres" est sélectionné
    if (form.value.chapitre && form.value.chapitre !== 'all') {
      params.chapitre = Number(form.value.chapitre)
    }
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
    etapes: '', 
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
      etapes: form.value.etapes || '',
      points: 1
    }

    if (form.value.id) {
      await updateExercice(form.value.id, payload)
    } else {
      await createExercice(payload)
    }

    // Sauvegarder le chapitre actuel avant de reset le formulaire
    const currentChapitre = form.value.chapitre

    resetForm()

    // Remettre le chapitre sélectionné pour permettre d'ajouter un autre exercice dans le même chapitre
    form.value.chapitre = currentChapitre

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
    etapes: exercice.etapes || '',
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
    etapes: form.value.etapes || '',
    solution: form.value.solution || '',
    difficulty: difficultyMap[form.value.difficulte] || 'medium'
  }
  
  showPreview.value = true
}

// Fonction pour fermer la prévisualisation
function closePreview() {
  showPreview.value = false
  previewData.value = null
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

// Fonction pour obtenir le contexte global de tous les chapitres
function getAllChaptersContext() {
  if (chapitres.value.length === 0) return null
  
  // Collecter toutes les matières, thèmes, pays et niveaux uniques
  const matieres = new Set()
  const themes = new Set()
  const pays = new Set()
  const niveaux = new Set()
  
  chapitres.value.forEach(chapitre => {
    const notion = getNotionById(chapitre.notion)
    if (notion) {
      if (notion.matiere_nom) matieres.add(notion.matiere_nom)
      if (notion.theme_nom) themes.add(notion.theme_nom)
      if (notion.contexte_detail?.pays?.nom) pays.add(notion.contexte_detail.pays.nom)
      if (notion.contexte_detail?.niveau?.nom) niveaux.add(notion.contexte_detail.niveau.nom)
    }
  })
  
  return {
    matiereNom: matieres.size > 0 ? Array.from(matieres).join(', ') : '—',
    themeNom: themes.size > 0 ? Array.from(themes).join(', ') : '—',
    paysNom: pays.size > 0 ? Array.from(pays).join(', ') : '—',
    niveauNom: niveaux.size > 0 ? Array.from(niveaux).join(', ') : '—',
    isAllChapters: true
  }
}

const currentContext = computed(() => {
  if (form.value.chapitre === 'all') {
    return getAllChaptersContext()
  }
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
  if (chapitreId === 'all') {
    return 'Tous les chapitres'
  }
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
  if (chapitreId === 'all') {
    return 'tous_les_chapitres'
  }
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

.filter-input {
  margin-bottom: 0.5rem;
  width: 100%;
  padding: 0.5rem;
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
}

.btn-preview {
  background: #6b7280;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  margin-right: 0.5rem;
  transition: all 0.2s ease;
}

.btn-preview:hover {
  background: #4b5563;
  transform: translateY(-1px);
}

.form-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.difficulty-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  background: white;
  cursor: pointer;
  transition: border-color 0.2s ease;
}

.difficulty-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.context-panel {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
}

.context-header {
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.context-header h4 {
  margin: 0;
  color: #1e293b;
  font-size: 1rem;
  font-weight: 600;
}

.context-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.25rem 0;
  border-bottom: 1px solid #f1f5f9;
}

.context-row:last-child {
  border-bottom: none;
}

.context-row strong {
  color: #374151;
  font-weight: 500;
  min-width: 80px;
}

.context-row span {
  color: #6b7280;
  text-align: right;
  flex: 1;
}

.context-row code {
  background: #f1f5f9;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.75rem;
  color: #475569;
}

.context-stats {
  display: flex;
  gap: 1rem;
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid #e2e8f0;
}

.stat-item {
  background: #e0f2fe;
  color: #0369a1;
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
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
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.preview-section h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: #1f2937;
}

.btn-close-preview {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.375rem;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close-preview:hover {
  background: #f3f4f6;
  color: #374151;
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

/* Responsive pour la prévisualisation */
@media (max-width: 768px) {
  .preview-section {
    margin: 1rem 0;
    padding: 1rem;
  }
  
  .preview-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .form-actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .form-actions button {
    width: 100%;
    margin-right: 0;
    margin-bottom: 0.5rem;
  }
  
  .form-actions button:last-child {
    margin-bottom: 0;
  }
}
</style> 