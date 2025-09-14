<template>
  <div>
    <h2 class="admin-title">Gestion des Quiz</h2>
    <form class="admin-form" @submit.prevent="handleSave">
      <div class="form-group">
        <label>Chapitre:</label>
        <input v-model="chapitreFormFilter" type="text" placeholder="Filtrer les chapitres..." class="filter-input" />
        <select v-model="form.chapitre" required>
          <option value="">Choisir un chapitre</option>
          <option v-for="c in filteredChapitresForForm" :key="c.id" :value="c.id">{{ formatChapitreOption(c) }}</option>
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
        <label>Titre du quiz:</label>
        <input v-model="form.titre" placeholder="Titre du quiz" required />
      </div>
      
      <div class="form-group">
        <label>Description:</label>
        <textarea v-model="form.description" rows="3"></textarea>
      </div>
      
      <div class="form-group">
        <label>Nombre de questions:</label>
        <input v-model.number="form.nombre_questions" type="number" min="1" max="50" />
      </div>
      
      <div class="form-group">
        <label>Temps limite (minutes):</label>
        <input v-model.number="form.temps_limite" type="number" min="1" max="120" />
      </div>

      <div class="form-group">
        <label>Questions (JSON) – optionnel</label>
        <textarea v-model="form.questions_json" rows="6" placeholder='Exemple:
[
  {
    "type": "qcm",
    "enonce": "1/2 + 1/3 = ?",
    "choix": ["5/6", "2/5", "3/5", "4/5"],
    "bonne_reponse_index": 0,
    "points": 1
  },
  {
    "type": "entree-libre",
    "enonce": "Simplifier 6/8",
    "reponse_attendue": "3/4",
    "points": 1
  }
]'></textarea>
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
    </form>

    <!-- Filtres -->
    <div class="filters">
      <div class="filter-group">
        <label>Filtrer par chapitre:</label>
        <input v-model="chapitreFilter" type="text" placeholder="Filtrer les chapitres..." class="filter-input" />
        <select v-model="filters.chapitre">
          <option value="">Tous les chapitres</option>
          <option v-for="chapitre in filteredChapitres" :key="chapitre.id" :value="chapitre.id">
            {{ chapitre.nom }} ({{ chapitre.notion_nom }})
          </option>
        </select>
      </div>
      
    </div>

    <!-- Tableau des quiz -->
    <table class="admin-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Titre</th>
          <th>Chapitre</th>
          <th>Contexte</th>
          <th>Questions</th>
          <th>Temps</th>
          <th>Difficulté</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="quiz in filteredQuiz" :key="quiz.id">
          <td>{{ quiz.id }}</td>
          <td>{{ quiz.titre }}</td>
          <td>{{ getChapitreName(quiz.chapitre) }}</td>
          <td class="ctx-cell">{{ getContextLabelByChapitre(quiz.chapitre) }}</td>
          <td>{{ (quiz.questions_data && quiz.questions_data.length) || quiz.nombre_questions || 0 }}</td>
          <td>{{ quiz.temps_limite || 0 }} min</td>
          <td><span class="difficulte-badge" :class="`difficulte-${quiz.difficulte || quiz.difficulty || 'moyen'}`">{{ quiz.difficulte || quiz.difficulty || 'moyen' }}</span></td>
          <td>
            <AdminActionsButtons
              :item="quiz"
              :actions="['edit', 'duplicate', 'delete']"
              edit-label="Éditer"
              duplicate-label="Dupliquer"
              confirm-message="Êtes-vous sûr de vouloir supprimer ce quiz ?"
              @edit="editQuiz"
              @duplicate="handleDuplicateQuiz"
              @delete="handleDeleteQuiz"
            />
          </td>
        </tr>
        <tr v-if="filteredQuiz.length === 0">
          <td colspan="8" style="text-align:center; font-style: italic;">Aucun quiz trouvé.</td>
        </tr>
      </tbody>
    </table>

    <!-- Modale de duplication -->
    <div v-if="showDuplicateModal" class="modal-overlay" @click="cancelDuplicate">
      <div class="modal-content" @click.stop>
        <h3>Dupliquer le quiz</h3>
        <p class="modal-description">
          Créer une copie de "<strong>{{ duplicateForm.originalQuiz?.titre }}</strong>"
        </p>

        <div class="modal-form">
          <div class="form-group">
            <label>Nouveau chapitre:</label>
            <select v-model="duplicateForm.newChapitre" required>
              <option value="">Choisir un chapitre</option>
              <option v-for="chapitre in chapitres" :key="chapitre.id" :value="chapitre.id">{{ formatChapitreOption(chapitre) }}</option>
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
import { ref, computed, onMounted } from 'vue'
import { getQuizAdmin, createQuiz, updateQuiz, deleteQuiz } from '@/api/quiz'
import { getChapitres, getNotions } from '@/api'
import { AdminActionsButtons } from '@/components/admin'

const quiz = ref([])
const chapitres = ref([])
const notions = ref([])
const chapitreFormFilter = ref('')
const chapitreFilter = ref('')
const form = ref({ 
  id: null, 
  chapitre: '', 
  titre: '', 
  description: '', 
  nombre_questions: 10,
  temps_limite: 30,
  difficulte: 'moyen',
  questions_json: ''
})
const filters = ref({
  chapitre: ''
})
const showDuplicateModal = ref(false)
const duplicateForm = ref({
  originalQuiz: null,
  newChapitre: '',
  newTitre: ''
})

// Computed properties
const filteredQuiz = computed(() => {
  let filtered = quiz.value
  
  if (filters.value.chapitre) {
    filtered = filtered.filter(q => q.chapitre == filters.value.chapitre)
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

async function load() {
  try {
    const [qRes, ch, nt] = await Promise.all([
      getQuizAdmin(),
      getChapitres(),
      getNotions()
    ])
    quiz.value = Array.isArray(qRes?.data) ? qRes.data : (Array.isArray(qRes) ? qRes : [])
    chapitres.value = Array.isArray(ch) ? ch : (ch?.data || [])
    notions.value = Array.isArray(nt) ? nt : (nt?.data || [])
  } catch (error) {
    console.error('[AdminQuiz] Erreur lors du chargement:', error)
    quiz.value = []
    chapitres.value = []
    notions.value = []
  }
}

onMounted(load)

function resetForm() {
  form.value = { 
    id: null, 
    chapitre: '', 
    titre: '', 
    description: '', 
    nombre_questions: 10,
    temps_limite: 30,
    difficulte: 'moyen',
    questions_json: ''
  }
}

async function handleSave() {
  if (!form.value.chapitre || !form.value.titre) return

  try {
    const difficultyMap = { 'facile': 'easy', 'moyen': 'medium', 'difficile': 'hard' }
    let questions = []
    if (form.value.questions_json && form.value.questions_json.trim()) {
      try { questions = JSON.parse(form.value.questions_json) } catch (_) { questions = [] }
    }
    const payload = {
      chapitre: Number(form.value.chapitre),
      titre: form.value.titre,
      contenu: form.value.description || form.value.titre,
      // aligné au modèle Quiz
      duree_minutes: Number(form.value.temps_limite) || 30,
      questions_data: Array.isArray(questions) ? questions : [],
      difficulty: difficultyMap[form.value.difficulte] || 'medium'
    }

    if (form.value.id) {
      await updateQuiz(form.value.id, payload)
    } else {
      await createQuiz(payload)
    }

    // Sauvegarder le chapitre actuel avant de reset le formulaire
    const currentChapitre = form.value.chapitre

    resetForm()

    // Remettre le chapitre sélectionné pour permettre d'ajouter un autre quiz dans le même chapitre
    form.value.chapitre = currentChapitre

    await load()
  } catch (e) {
    console.error('[AdminQuiz] Erreur:', e)
  }
}

function editQuiz(quiz) {
  // Mapping inverse pour la difficulté (anglais vers français)
  const difficultyMap = { 'easy': 'facile', 'medium': 'moyen', 'hard': 'difficile' }
  const difficulte = quiz.difficulte || quiz.difficulty || 'medium'
  const difficulteFr = difficultyMap[difficulte] || 'moyen'
  
  form.value = { 
    id: quiz.id,
    chapitre: quiz.chapitre,
    titre: quiz.titre || '',
    description: quiz.description || '',
    nombre_questions: quiz.nombre_questions || 10,
    temps_limite: quiz.temps_limite || 30,
    difficulte: difficulteFr,
    questions_json: quiz.questions_data ? JSON.stringify(quiz.questions_data, null, 2) : ''
  }
}

async function removeQuiz(id) {
  try {
    await deleteQuiz(id)
    await load()
  } catch (e) {
    console.error('Erreur:', e)
  }
}

// Nouvelle fonction qui utilise le composant AdminActionsButtons
function handleDeleteQuiz(quiz) {
  removeQuiz(quiz.id)
}

// Fonction pour dupliquer un quiz
function handleDuplicateQuiz(quiz) {
  duplicateForm.value = {
    originalQuiz: quiz,
    newChapitre: '',
    newTitre: `${quiz.titre}`
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
    const original = duplicateForm.value.originalQuiz
    const difficultyMap = { 'facile': 'easy', 'moyen': 'medium', 'difficile': 'hard' }

    const payload = {
      chapitre: Number(duplicateForm.value.newChapitre),
      titre: duplicateForm.value.newTitre.trim(),
      contenu: original.contenu || original.description || '',
      duree_minutes: original.duree_minutes || original.temps_limite || 30,
      questions_data: original.questions_data || [],
      difficulty: original.difficulty || difficultyMap[original.difficulte] || 'medium'
    }

    console.log('Payload envoyé pour duplication quiz:', payload)
    console.log('Original quiz:', original)

    await createQuiz(payload)
    await load()

    showDuplicateModal.value = false
    duplicateForm.value = {
      originalQuiz: null,
      newChapitre: '',
      newTitre: ''
    }

    alert('Quiz dupliqué avec succès !')
  } catch (error) {
    console.error('Erreur lors de la duplication:', error)
    alert('Erreur lors de la duplication du quiz.')
  }
}

// Fonction pour annuler la duplication
function cancelDuplicate() {
  showDuplicateModal.value = false
  duplicateForm.value = {
    originalQuiz: null,
    newChapitre: '',
    newTitre: ''
  }
}

// Helpers contextuels (alignés avec AdminExercices/AdminCours)
function getChapitreName(id) {
  const c = chapitres.value.find(x => String(x.id) === String(id))
  return c ? c.nom : id
}

function getNotionById(id) {
  return notions.value.find(x => String(x.id) === String(id))
}

function chapterContext(c) {
  if (!c) return null
  const notion = getNotionById(c.notion)
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