<template>
  <div class="admin-quiz-submissions">
    <h2 class="admin-title">📝 Notation des Quiz (WhatsApp)</h2>
    
    <!-- Statistiques -->
    <div class="stats-cards">
      <div class="stat-card total">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.total || 0 }}</div>
          <div class="stat-label">Total</div>
        </div>
      </div>
      <div class="stat-card pending">
        <div class="stat-icon">⏳</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.pending || 0 }}</div>
          <div class="stat-label">En attente</div>
        </div>
      </div>
      <div class="stat-card graded">
        <div class="stat-icon">✅</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.graded || 0 }}</div>
          <div class="stat-label">Notés</div>
        </div>
      </div>
    </div>

    <!-- Formulaire rapide d'enregistrement -->
    <QuickSubmissionForm 
      v-if="showQuickForm" 
      @submitted="onSubmissionCreated" 
      class="quick-form"
    />

    <button @click="showQuickForm = !showQuickForm" class="btn-toggle-form">
      {{ showQuickForm ? '➖ Masquer le formulaire' : '➕ Enregistrer une nouvelle réception' }}
    </button>

    <!-- Filtres -->
    <div class="filters">
      <select v-model="filterStatus" class="filter-select">
        <option value="">Tous les statuts</option>
        <option value="pending">En attente</option>
        <option value="graded">Notés</option>
      </select>
      
      <button @click="loadSubmissions" class="btn-refresh">
        🔄 Actualiser
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>Chargement...</p>
    </div>

    <!-- Liste des soumissions -->
    <div v-else-if="submissions.length === 0" class="empty-state">
      <div class="empty-icon">📭</div>
      <h3>Aucune soumission</h3>
      <p>{{ filterStatus === 'pending' ? 'Aucune soumission en attente' : 'Aucune soumission trouvée' }}</p>
    </div>

    <div v-else class="submissions-list">
      <div 
        v-for="submission in submissions" 
        :key="submission.id" 
        class="submission-card"
        :class="{ 'pending': submission.status === 'pending', 'graded': submission.status === 'graded' }"
      >
        <div class="submission-header">
          <div class="submission-info">
            <h3>{{ submission.user_name || submission.user_email }}</h3>
            <p class="quiz-title">{{ submission.quiz_titre }}</p>
            <p class="notion-title">📚 {{ submission.quiz_notion_titre }}</p>
          </div>
          <div class="submission-status">
            <span class="status-badge" :class="submission.status">
              {{ submission.status === 'pending' ? '⏳ En attente' : '✅ Noté' }}
            </span>
          </div>
        </div>

        <div class="submission-details">
          <div class="detail-row">
            <span class="label">Date de soumission:</span>
            <span class="value">{{ formatDate(submission.date_creation) }}</span>
          </div>
          
          <div v-if="submission.status === 'graded'" class="graded-info">
            <div class="detail-row">
              <span class="label">Note:</span>
              <span class="value note-value">{{ submission.note }}/20</span>
            </div>
            <div v-if="submission.commentaire" class="detail-row">
              <span class="label">Commentaire:</span>
              <span class="value">{{ submission.commentaire }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Corrigé le:</span>
              <span class="value">{{ formatDate(submission.date_correction) }}</span>
            </div>
          </div>

          <div v-if="submission.notes_admin" class="admin-notes">
            <span class="label">Notes admin:</span>
            <p>{{ submission.notes_admin }}</p>
          </div>
        </div>

        <div class="submission-actions">
          <button 
            v-if="submission.status === 'pending'" 
            @click="openGradeModal(submission)"
            class="btn-grade"
          >
            ✏️ Noter
          </button>
          <button 
            v-else
            @click="openGradeModal(submission)"
            class="btn-edit-grade"
          >
            📝 Modifier la note
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de notation -->
    <div v-if="showGradeModal" class="modal-overlay" @click.self="closeGradeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ currentSubmission?.status === 'pending' ? 'Noter' : 'Modifier la note' }}</h3>
          <button @click="closeGradeModal" class="btn-close">×</button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label>Élève:</label>
            <p class="student-name">{{ currentSubmission?.user_name || currentSubmission?.user_email }}</p>
          </div>

          <div class="form-group">
            <label>Quiz:</label>
            <p>{{ currentSubmission?.quiz_titre }}</p>
          </div>

          <div class="form-group">
            <label for="note">Note sur 20: *</label>
            <input 
              id="note"
              v-model.number="gradeForm.note" 
              type="number" 
              min="0" 
              max="20" 
              step="0.25"
              class="form-input"
              placeholder="Ex: 15.5"
            />
          </div>

          <div class="form-group">
            <label for="commentaire">Commentaire de correction:</label>
            <textarea 
              id="commentaire"
              v-model="gradeForm.commentaire" 
              rows="4"
              class="form-textarea"
              placeholder="Ajoutez vos commentaires pour l'élève..."
            ></textarea>
          </div>

          <div v-if="gradeError" class="error-message">
            {{ gradeError }}
          </div>
        </div>

        <div class="modal-footer">
          <button @click="closeGradeModal" class="btn-cancel">Annuler</button>
          <button @click="submitGrade" class="btn-submit" :disabled="grading">
            {{ grading ? 'Enregistrement...' : 'Enregistrer' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { 
  getQuizSubmissions, 
  gradeQuizSubmission, 
  getQuizSubmissionStats 
} from '@/api/quizSubmissions'
import QuickSubmissionForm from '@/components/admin/QuickSubmissionForm.vue'

const submissions = ref([])
const stats = ref({ total: 0, pending: 0, graded: 0 })
const loading = ref(false)
const filterStatus = ref('pending') // Par défaut, afficher les en attente
const showQuickForm = ref(false)

const showGradeModal = ref(false)
const currentSubmission = ref(null)
const gradeForm = ref({
  note: null,
  commentaire: ''
})
const grading = ref(false)
const gradeError = ref('')

onMounted(() => {
  loadSubmissions()
  loadStats()
})

watch(filterStatus, () => {
  loadSubmissions()
})

async function loadSubmissions() {
  loading.value = true
  try {
    const filters = {}
    if (filterStatus.value) {
      filters.status = filterStatus.value
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
.admin-quiz-submissions {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.admin-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 2rem;
}

/* Stats Cards */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-card.total {
  border-left: 4px solid #3b82f6;
}

.stat-card.pending {
  border-left: 4px solid #f59e0b;
}

.stat-card.graded {
  border-left: 4px solid #10b981;
}

.stat-icon {
  font-size: 2.5rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Quick Form */
.quick-form {
  margin-bottom: 1.5rem;
}

.btn-toggle-form {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 1.5rem;
}

.btn-toggle-form:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

/* Filtres */
.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.filter-select {
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-select:hover {
  border-color: #3b82f6;
}

.btn-refresh {
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-refresh:hover {
  background: #2563eb;
  transform: translateY(-2px);
}

/* Loading & Empty States */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  gap: 1rem;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.6;
}

.empty-state h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.empty-state p {
  color: #64748b;
  font-size: 1rem;
}

/* Submissions List */
.submissions-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.submission-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #e2e8f0;
  transition: all 0.2s;
}

.submission-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.submission-card.pending {
  border-left-color: #f59e0b;
}

.submission-card.graded {
  border-left-color: #10b981;
}

.submission-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.submission-info h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.quiz-title {
  font-size: 1rem;
  font-weight: 600;
  color: #3b82f6;
  margin: 0 0 0.25rem 0;
}

.notion-title {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
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

.submission-details {
  margin-bottom: 1rem;
}

.detail-row {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.detail-row .label {
  font-weight: 600;
  color: #64748b;
  min-width: 180px;
}

.detail-row .value {
  color: #1e293b;
}

.note-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #3b82f6;
}

.graded-info {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
}

.admin-notes {
  background: #fef3c7;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
}

.admin-notes .label {
  font-weight: 600;
  color: #92400e;
  display: block;
  margin-bottom: 0.5rem;
}

.admin-notes p {
  margin: 0;
  color: #78350f;
}

.submission-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.btn-grade,
.btn-edit-grade {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-grade {
  background: #3b82f6;
  color: white;
}

.btn-grade:hover {
  background: #2563eb;
  transform: translateY(-2px);
}

.btn-edit-grade {
  background: #64748b;
  color: white;
}

.btn-edit-grade:hover {
  background: #475569;
  transform: translateY(-2px);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  font-size: 2rem;
  color: #64748b;
  cursor: pointer;
  padding: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.2s;
}

.btn-close:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.modal-body {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.student-name {
  font-size: 1.125rem;
  color: #3b82f6;
  margin: 0;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-textarea {
  resize: vertical;
  font-family: inherit;
}

.error-message {
  padding: 0.75rem;
  background: #fee2e2;
  color: #991b1b;
  border-radius: 8px;
  margin-top: 1rem;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.btn-cancel,
.btn-submit {
  flex: 1;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel {
  background: #f1f5f9;
  color: #64748b;
}

.btn-cancel:hover {
  background: #e2e8f0;
}

.btn-submit {
  background: #3b82f6;
  color: white;
}

.btn-submit:hover:not(:disabled) {
  background: #2563eb;
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .admin-quiz-submissions {
    padding: 1rem;
  }

  .admin-title {
    font-size: 1.5rem;
  }

  .stats-cards {
    grid-template-columns: 1fr;
  }

  .filters {
    flex-direction: column;
  }

  .submission-header {
    flex-direction: column;
    gap: 1rem;
  }

  .detail-row {
    flex-direction: column;
    gap: 0.25rem;
  }

  .detail-row .label {
    min-width: auto;
  }
}
</style>

