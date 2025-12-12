<template>
  <div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
      <h2 class="admin-title" style="margin-bottom: 0;">Notation des Quiz</h2>
      <div style="display: flex; gap: 0.5rem; font-size: 0.875rem; color: #6b7280;">
        <span>Total: <strong>{{ stats.total || 0 }}</strong></span>
        <span>•</span>
        <span style="color: #f59e0b;">En attente: <strong>{{ stats.pending || 0 }}</strong></span>
        <span>•</span>
        <span style="color: #10b981;">Notés: <strong>{{ stats.graded || 0 }}</strong></span>
      </div>
    </div>

    <div v-if="showQuickForm" class="admin-form" style="margin-bottom: 1rem;">
      <QuickSubmissionForm @submitted="onSubmissionCreated" />
    </div>

    <div class="filters">
      <button @click="showQuickForm = !showQuickForm" class="btn-secondary">
        {{ showQuickForm ? 'Masquer' : 'Nouvelle réception' }}
      </button>
      
      <div class="filter-group">
        <select v-model="filterStatus">
          <option value="">Tous statuts</option>
          <option value="pending">En attente</option>
          <option value="graded">Notés</option>
        </select>
      </div>

      <div class="filter-group">
        <select v-model="filterPays">
          <option value="">Tous pays</option>
          <option v-for="pays in paysList" :key="pays.id" :value="pays.id">
            {{ pays.nom }}
          </option>
        </select>
      </div>

      <div class="filter-group">
        <select v-model="filterNiveau">
          <option value="">Tous niveaux</option>
          <option v-for="niveau in niveauxList" :key="niveau.id" :value="niveau.id">
            {{ niveau.nom }}
          </option>
        </select>
      </div>

      <div class="filter-group">
        <input 
          v-model="filterStudent" 
          type="text" 
          placeholder="Rechercher un élève (nom ou email)..."
          style="padding: 0.5rem 0.75rem; border: 1px solid #d1d5db; border-radius: 0.375rem; font-size: 0.875rem; min-width: 250px;"
        />
      </div>
      
      <button @click="loadSubmissions" class="btn-primary">
        Actualiser
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" style="text-align: center; padding: 2rem; color: #6b7280;">
      <p>Chargement...</p>
    </div>

    <!-- Liste des soumissions -->
    <div v-else-if="filteredSubmissions.length === 0" style="text-align: center; padding: 2rem; color: #6b7280;">
      <p>{{ filterStatus === 'pending' ? 'Aucune soumission en attente' : 'Aucune soumission trouvée' }}</p>
    </div>

    <table v-else class="admin-table">
      <thead>
        <tr>
          <th>Nom</th>
          <th>Email</th>
          <th>Pays</th>
          <th>Niveau</th>
          <th>Notion</th>
          <th>Date soumission</th>
          <th>Statut</th>
          <th>Note</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="submission in filteredSubmissions" :key="submission.id">
          <td>{{ submission.user_name || '—' }}</td>
          <td>{{ submission.user_email }}</td>
          <td>{{ submission.user_pays_nom || '—' }}</td>
          <td>{{ submission.user_niveau_nom || '—' }}</td>
          <td>{{ submission.quiz_notion_titre }}</td>
          <td>{{ formatDate(submission.date_creation) }}</td>
          <td>
            <span 
              class="status-badge" 
              :class="submission.status"
            >
              {{ submission.status === 'pending' ? 'En attente' : 'Noté' }}
            </span>
          </td>
          <td>
            <span v-if="submission.status === 'graded'" style="font-weight: 600;">
              {{ submission.note }}/20
            </span>
            <span v-else style="color: #9ca3af;">—</span>
          </td>
          <td>
            <div style="display: flex; gap: 0.5rem;">
              <button 
                @click="openGradeModal(submission)"
                :class="submission.status === 'pending' ? 'btn-primary' : 'btn-secondary'"
                style="padding: 0.5rem 0.75rem; font-size: 0.875rem;"
              >
                {{ submission.status === 'pending' ? 'Noter' : 'Modifier' }}
              </button>
              <button 
                @click="deleteSubmission(submission)"
                class="btn-danger"
                style="padding: 0.5rem 0.75rem; font-size: 0.875rem;"
              >
                Supprimer
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal de notation -->
    <div v-if="showGradeModal" class="modal-overlay" @click.self="closeGradeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ currentSubmission?.status === 'pending' ? 'Noter le quiz' : 'Modifier la note' }}</h3>
          <button @click="closeGradeModal" class="modal-close">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="info-row">
            <span class="info-label">Élève</span>
            <span class="info-value">{{ currentSubmission?.user_name || currentSubmission?.user_email }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Notion</span>
            <span class="info-value">{{ currentSubmission?.quiz_notion_titre }}</span>
          </div>

          <div class="form-group">
            <label for="note">Note sur 20 *</label>
            <input 
              id="note"
              v-model.number="gradeForm.note" 
              type="number" 
              min="0" 
              max="20" 
              step="0.25"
              placeholder="15.5"
              class="input-note"
            />
          </div>

          <div class="form-group">
            <label for="commentaire">Commentaire</label>
            <textarea 
              id="commentaire"
              v-model="gradeForm.commentaire" 
              rows="4"
              placeholder="Ajoutez vos commentaires..."
            ></textarea>
          </div>

          <div v-if="gradeError" class="error-box">
            {{ gradeError }}
          </div>
        </div>

        <div class="modal-footer">
          <button @click="closeGradeModal" class="btn-secondary">Annuler</button>
          <button @click="submitGrade" class="btn-primary" :disabled="grading">
            {{ grading ? 'Enregistrement...' : 'Enregistrer' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { 
  getQuizSubmissions, 
  gradeQuizSubmission, 
  getQuizSubmissionStats,
  deleteQuizSubmission
} from '@/api/quizSubmissions'
import { getPays } from '@/api/pays'
import { getNiveaux } from '@/api/niveaux'
import QuickSubmissionForm from '@/components/admin/QuickSubmissionForm.vue'

const submissions = ref([])
const stats = ref({ total: 0, pending: 0, graded: 0 })
const loading = ref(false)
const filterStatus = ref('pending') // Par défaut, afficher les en attente
const filterPays = ref('')
const filterNiveau = ref('')
const filterStudent = ref('')
const paysList = ref([])
const niveauxList = ref([])
const showQuickForm = ref(false)

// Filtrer les soumissions par nom ou email d'élève
const filteredSubmissions = computed(() => {
  if (!filterStudent.value) {
    return submissions.value
  }
  
  const searchTerm = filterStudent.value.toLowerCase().trim()
  return submissions.value.filter(submission => {
    const name = (submission.user_name || '').toLowerCase()
    const email = (submission.user_email || '').toLowerCase()
    return name.includes(searchTerm) || email.includes(searchTerm)
  })
})

const showGradeModal = ref(false)
const currentSubmission = ref(null)
const gradeForm = ref({
  note: null,
  commentaire: ''
})
const grading = ref(false)
const gradeError = ref('')

onMounted(async () => {
  await loadPaysList()
  await loadNiveauxList()
  loadSubmissions()
  loadStats()
})

watch([filterStatus, filterPays, filterNiveau, filterStudent], () => {
  loadSubmissions()
})

async function loadPaysList() {
  try {
    const response = await getPays()
    paysList.value = response?.data || response || []
  } catch (error) {
    console.error('Erreur chargement pays:', error)
  }
}

async function loadNiveauxList() {
  try {
    const response = await getNiveaux()
    niveauxList.value = response?.data || response || []
  } catch (error) {
    console.error('Erreur chargement niveaux:', error)
  }
}

async function loadSubmissions() {
  loading.value = true
  try {
    const filters = {}
    if (filterStatus.value) {
      filters.status = filterStatus.value
    }
    if (filterPays.value) {
      filters.pays = filterPays.value
    }
    if (filterNiveau.value) {
      filters.niveau = filterNiveau.value
    }
    submissions.value = await getQuizSubmissions(filters)
  } catch (error) {
    console.error('Erreur chargement soumissions:', error)
  } finally {
    loading.value = false
  }
}

async function loadStats() {
  try {
    stats.value = await getQuizSubmissionStats()
  } catch (error) {
    console.error('Erreur chargement stats:', error)
  }
}

function openGradeModal(submission) {
  currentSubmission.value = submission
  gradeForm.value = {
    note: submission.note || null,
    commentaire: submission.commentaire || ''
  }
  gradeError.value = ''
  showGradeModal.value = true
}

function closeGradeModal() {
  showGradeModal.value = false
  currentSubmission.value = null
  gradeForm.value = { note: null, commentaire: '' }
  gradeError.value = ''
}

async function submitGrade() {
  gradeError.value = ''
  
  // Validation
  if (gradeForm.value.note === null || gradeForm.value.note === '') {
    gradeError.value = 'La note est requise'
    return
  }
  
  if (gradeForm.value.note < 0 || gradeForm.value.note > 20) {
    gradeError.value = 'La note doit être entre 0 et 20'
    return
  }

  grading.value = true
  try {
    await gradeQuizSubmission(currentSubmission.value.id, {
      note: gradeForm.value.note,
      commentaire: gradeForm.value.commentaire
    })
    
    // Recharger les données
    await loadSubmissions()
    await loadStats()
    
    closeGradeModal()
  } catch (error) {
    console.error('Erreur notation:', error)
    gradeError.value = error.response?.data?.error || 'Erreur lors de la notation'
  } finally {
    grading.value = false
  }
}

function onSubmissionCreated() {
  // Recharger les données après création d'une soumission
  loadSubmissions()
  loadStats()
  // Masquer le formulaire
  showQuickForm.value = false
}

async function deleteSubmission(submission) {
  if (!confirm(`Voulez-vous vraiment supprimer la soumission de ${submission.user_name || submission.user_email} ?`)) {
    return
  }

  try {
    await deleteQuizSubmission(submission.id)
    await loadSubmissions()
    await loadStats()
  } catch (error) {
    console.error('Erreur suppression:', error)
    alert('Erreur lors de la suppression')
  }
}

function formatDate(dateString) {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.admin-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
}

.admin-form {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.filters {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  align-items: center;
}

.filter-group select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  background: white;
}

.btn-primary,
.btn-secondary {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: #6b7280;
  color: white;
}

.btn-secondary:hover {
  background: #4b5563;
}

.btn-danger {
  background: #ef4444;
  color: white;
}

.btn-danger:hover {
  background: #dc2626;
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
  padding: 0.75rem 0.5rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
  font-size: 0.875rem;
}

.admin-table th {
  background: #f9fafb;
  font-weight: 600;
  color: #374151;
  font-size: 0.8rem;
  white-space: nowrap;
}

.admin-table tbody tr:hover {
  background: #f9fafb;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-badge.pending {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.graded {
  background: #d1fae5;
  color: #065f46;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
  backdrop-filter: blur(2px);
}

.modal-content {
  background: white;
  border-radius: 0.75rem;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.75rem;
  color: #9ca3af;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.375rem;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #f3f4f6;
  color: #1f2937;
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem;
  background: #f9fafb;
  border-radius: 0.375rem;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.info-row:last-of-type {
  margin-bottom: 1.5rem;
}

.info-label {
  font-weight: 600;
  color: #6b7280;
}

.info-value {
  color: #1f2937;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: #374151;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.625rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.input-note {
  max-width: 150px;
  font-size: 1rem;
  font-weight: 600;
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
}

.error-box {
  background: #fee2e2;
  color: #991b1b;
  padding: 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  margin-top: 1rem;
}

.modal-footer {
  display: flex;
  gap: 0.75rem;
  padding: 1.25rem 1.5rem;
  border-top: 1px solid #e5e7eb;
  justify-content: flex-end;
}
</style>

