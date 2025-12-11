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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import BackButton from '@/components/common/BackButton.vue'
import { getQuizSubmissions, getQuizSubmissionStats } from '@/api/quizSubmissions'

const router = useRouter()
const submissions = ref([])
const stats = ref(null)
const loading = ref(false)

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
}
</style>

