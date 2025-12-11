<template>
  <DashboardLayout>
    <section class="quiz-submissions-student">
      <div class="nav-header-base">
        <BackButton
          text="Retour"
          title="Retour"
          :customAction="goBack"
          position="top-left-dashboard"
        />
      </div>

      <div class="content-container">
        <h1 class="page-title">📝 Mes Quiz Rendus</h1>
        <p class="page-subtitle">Consultez vos quiz envoyés par WhatsApp et vos notes</p>

        <!-- Statistiques -->
        <div v-if="stats" class="stats-cards">
          <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.total || 0 }}</div>
              <div class="stat-label">Quiz rendus</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">⏳</div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.pending || 0 }}</div>
              <div class="stat-label">En correction</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">✅</div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.graded || 0 }}</div>
              <div class="stat-label">Notés</div>
            </div>
          </div>
          <div v-if="stats.moyenne !== null" class="stat-card moyenne">
            <div class="stat-icon">🎯</div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.moyenne }}/20</div>
              <div class="stat-label">Moyenne</div>
            </div>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Chargement de vos quiz...</p>
        </div>

        <!-- Empty state -->
        <div v-else-if="submissions.length === 0" class="empty-state">
          <div class="empty-icon">📭</div>
          <h3>Aucun quiz rendu</h3>
          <p>Vous n'avez pas encore envoyé de quiz par WhatsApp</p>
        </div>

        <!-- Liste des soumissions -->
        <div v-else class="submissions-list">
          <div 
            v-for="submission in submissions" 
            :key="submission.id" 
            class="submission-card"
            :class="{ 'graded': submission.status === 'graded', 'pending': submission.status === 'pending' }"
          >
            <div class="card-header">
              <div class="quiz-info">
                <h3>{{ submission.quiz_titre }}</h3>
                <p class="notion-name">📚 {{ submission.quiz_notion_titre }}</p>
              </div>
              <div class="status-badge" :class="submission.status">
                {{ submission.status === 'pending' ? '⏳ En correction' : '✅ Noté' }}
              </div>
            </div>

            <div class="card-body">
              <div class="info-row">
                <span class="label">Date de soumission:</span>
                <span class="value">{{ formatDate(submission.date_creation) }}</span>
              </div>

              <div v-if="submission.status === 'graded'" class="graded-section">
                <div class="note-display">
                  <span class="note-label">Note obtenue:</span>
                  <span class="note-value">{{ submission.note }}/20</span>
                </div>

                <div v-if="submission.commentaire" class="commentaire-box">
                  <div class="commentaire-header">💬 Commentaire du professeur</div>
                  <p class="commentaire-text">{{ submission.commentaire }}</p>
                </div>

                <div class="info-row">
                  <span class="label">Corrigé le:</span>
                  <span class="value">{{ formatDate(submission.date_correction) }}</span>
                </div>

                <!-- Solution du quiz (visible uniquement après correction) -->
                <div v-if="submission.quiz_solution" class="solution-section">
                  <button 
                    class="solution-toggle" 
                    @click="toggleSolution(submission.id)"
                  >
                    <span>📝 {{ expandedSolutions.has(submission.id) ? 'Masquer' : 'Voir' }} la solution</span>
                    <span class="toggle-icon">{{ expandedSolutions.has(submission.id) ? '▲' : '▼' }}</span>
                  </button>
                  <div v-if="expandedSolutions.has(submission.id)" class="solution-content">
                    <div class="solution-header">📖 Solution du quiz</div>
                    <div class="solution-text" v-html="renderSolution(submission.quiz_solution)"></div>
                  </div>
                </div>
              </div>

              <div v-else class="pending-message">
                <p>⏳ Votre quiz est en cours de correction. Vous recevrez votre note bientôt.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import BackButton from '@/components/common/BackButton.vue'
import { getQuizSubmissions, getQuizSubmissionStats } from '@/api/quizSubmissions'

const router = useRouter()
const submissions = ref([])
const stats = ref(null)
const loading = ref(false)
const expandedSolutions = ref(new Set())

onMounted(() => {
  loadSubmissions()
  loadStats()
})

async function loadSubmissions() {
  loading.value = true
  try {
    submissions.value = await getQuizSubmissions()
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

function goBack() {
  router.back()
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

function toggleSolution(submissionId) {
  if (expandedSolutions.value.has(submissionId)) {
    expandedSolutions.value.delete(submissionId)
  } else {
    expandedSolutions.value.add(submissionId)
    // Render MathJax après l'affichage de la solution
    nextTick(() => {
      if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise()
      }
    })
  }
  // Forcer la réactivité du Set
  expandedSolutions.value = new Set(expandedSolutions.value)
}

function renderSolution(solution) {
  if (!solution) return ''
  // Convertir les retours à la ligne en <br> et traiter le Markdown basique
  let html = solution
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
  return html
}
</script>

<style scoped>
.quiz-submissions-student {
  padding: 1rem 0 2rem;
  min-height: 100vh;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin: 2rem 0 0.5rem;
}

.page-subtitle {
  font-size: 1rem;
  color: #64748b;
  margin-bottom: 2rem;
}

/* Stats Cards */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border-left: 4px solid #3b82f6;
}

.stat-card.moyenne {
  border-left-color: #8b5cf6;
}

.stat-icon {
  font-size: 2rem;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
  margin-top: 0.25rem;
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

.loading-state p {
  color: #64748b;
  font-size: 1rem;
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
  margin: 0;
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
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.2s;
}

.submission-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.submission-card.graded {
  border-left: 4px solid #10b981;
}

.submission-card.pending {
  border-left: 4px solid #f59e0b;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.quiz-info h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  color: white;
}

.notion-name {
  font-size: 0.875rem;
  margin: 0;
  opacity: 0.9;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  white-space: nowrap;
}

.status-badge.pending {
  background: rgba(251, 191, 36, 0.2);
  color: #fef3c7;
  border: 2px solid #fbbf24;
}

.status-badge.graded {
  background: rgba(16, 185, 129, 0.2);
  color: #d1fae5;
  border: 2px solid #10b981;
}

.card-body {
  padding: 1.5rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e2e8f0;
}

.info-row:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.info-row .label {
  font-weight: 600;
  color: #64748b;
  font-size: 0.875rem;
}

.info-row .value {
  color: #1e293b;
  font-size: 0.875rem;
}

.graded-section {
  margin-top: 1rem;
}

.note-display {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1rem;
}

.note-label {
  font-size: 1rem;
  font-weight: 600;
  color: white;
}

.note-value {
  font-size: 2rem;
  font-weight: 700;
  color: white;
}

.commentaire-box {
  background: #f8fafc;
  border-left: 4px solid #3b82f6;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.commentaire-header {
  font-weight: 600;
  color: #3b82f6;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.commentaire-text {
  color: #1e293b;
  margin: 0;
  line-height: 1.6;
  white-space: pre-wrap;
}

.pending-message {
  background: #fef3c7;
  border-left: 4px solid #f59e0b;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
}

.pending-message p {
  margin: 0;
  color: #92400e;
  font-size: 0.875rem;
}

/* Solution Section */
.solution-section {
  margin-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
  padding-top: 1rem;
}

.solution-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 0.875rem 1rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
}

.solution-toggle:hover {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  box-shadow: 0 4px 8px rgba(16, 185, 129, 0.4);
  transform: translateY(-1px);
}

.toggle-icon {
  font-size: 0.75rem;
  transition: transform 0.3s ease;
}

.solution-content {
  margin-top: 1rem;
  background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
  border: 2px solid #86efac;
  border-radius: 12px;
  overflow: hidden;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.solution-header {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
  padding: 0.75rem 1rem;
  font-weight: 600;
  font-size: 1rem;
}

.solution-text {
  padding: 1.25rem;
  color: #166534;
  font-size: 0.95rem;
  line-height: 1.8;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.solution-text strong {
  color: #14532d;
}

.solution-text em {
  font-style: italic;
}

@media (max-width: 768px) {
  .page-title {
    font-size: 1.5rem;
  }

  .stats-cards {
    grid-template-columns: 1fr;
  }

  .card-header {
    flex-direction: column;
    gap: 1rem;
  }

  .status-badge {
    align-self: flex-start;
  }

  .info-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }

  .note-display {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }

  .solution-toggle {
    font-size: 0.875rem;
    padding: 0.75rem 1rem;
  }

  .solution-text {
    padding: 1rem;
    font-size: 0.875rem;
  }
}
</style>

