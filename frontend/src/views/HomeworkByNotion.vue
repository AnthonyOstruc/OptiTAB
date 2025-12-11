<template>
  <DashboardLayout>
    <section class="quiz-section">
      <div class="nav-header-base">
        <BackButton
          text="Retour aux chapitres"
          title="Retour aux chapitres"
          :customAction="goBack"
          position="top-left-dashboard"
        />
      </div>

      <div class="quiz-container">
        <!-- Loading state -->
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Chargement des quiz...</p>
        </div>

        <!-- Empty state -->
        <div v-else-if="!loading && quizList.length === 0" class="empty-state">
          <div class="empty-icon">📝</div>
          <h3>Aucun quiz disponible</h3>
          <p>Il n'y a pas encore de quiz pour cette notion.</p>
        </div>

        <!-- Quiz list -->
        <div v-else class="quiz-list">
          <ExerciceQCM
            v-for="quiz in quizList"
            :key="quiz.id"
            :eid="quiz.id"
            :titre="quiz.titre"
            :exercices-list="quiz.questions_data"
            :difficulty="quiz.difficulty"
            :readonly="false"
            :best-score="quiz.bestScore"
            :attempt-count="quiz.attemptCount"
          />
        </div>
      </div>
    </section>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import BackButton from '@/components/common/BackButton.vue'
import ExerciceQCM from '@/components/UI/ExerciceQCM.vue'
import { getQuizByNotion, getQuizAttempts } from '@/api/quiz'
import { getQuizSubmissions } from '@/api/quizSubmissions'

const route = useRoute()
const router = useRouter()
const notionId = route.params.notionId

const loading = ref(true)
const quizList = ref([])

async function loadQuiz() {
  loading.value = true
  try {
    const response = await getQuizByNotion(notionId)
    const quizData = response.data || response || []
    
    console.log(`[HomeworkByNotion] Quiz chargés:`, quizData.length)
    
    // Charger les tentatives pour chaque quiz en parallèle
    const quizWithAttempts = await Promise.all(
      quizData.map(async (quiz) => {
        try {
          const attemptsResponse = await getQuizAttempts(quiz.id)
          // Gérer différentes structures de réponse
          let attempts = attemptsResponse
          if (attemptsResponse?.data) {
            attempts = Array.isArray(attemptsResponse.data) 
              ? attemptsResponse.data 
              : (attemptsResponse.data?.data || attemptsResponse.data?.results || [])
          }
          attempts = Array.isArray(attempts) ? attempts : []
          
          console.log(`[Quiz ${quiz.id}] Tentatives trouvées:`, attempts.length)
          
          // Charger aussi les soumissions manuelles (notes données par l'admin)
          let manualSubmissions = []
          try {
            const submissionsResponse = await getQuizSubmissions({ quiz: quiz.id })
            manualSubmissions = Array.isArray(submissionsResponse) ? submissionsResponse : []
            console.log(`[Quiz ${quiz.id}] Soumissions manuelles trouvées:`, manualSubmissions.length)
          } catch (error) {
            console.log(`[Quiz ${quiz.id}] Pas de soumissions manuelles ou erreur:`, error.message)
          }
          
          // Trouver la meilleure note
          let bestScore = null
          
          // 1. Notes des tentatives automatiques
          if (attempts.length > 0) {
            const scores = attempts
              .filter(a => a.score != null && a.total_points != null && a.total_points > 0)
              .map(a => (a.score / a.total_points) * 20)
            
            if (scores.length > 0) {
              bestScore = Math.max(...scores)
              console.log(`[Quiz ${quiz.id}] Meilleure note (tentatives): ${bestScore.toFixed(2)}/20`)
            }
          }
          
          // 2. Notes des soumissions manuelles (notées par l'admin)
          if (manualSubmissions.length > 0) {
            const manualScores = manualSubmissions
              .filter(s => s.status === 'graded' && s.note != null)
              .map(s => s.note)
            
            if (manualScores.length > 0) {
              const bestManualScore = Math.max(...manualScores)
              console.log(`[Quiz ${quiz.id}] Meilleure note (manuel): ${bestManualScore.toFixed(2)}/20`)
              
              // Prendre la meilleure entre les deux
              bestScore = bestScore !== null 
                ? Math.max(bestScore, bestManualScore)
                : bestManualScore
            }
          }
          
          if (bestScore !== null) {
            console.log(`[Quiz ${quiz.id}] Note finale affichée: ${bestScore.toFixed(2)}/20`)
          }
          
          return {
            ...quiz,
            questions_data: Array.isArray(quiz.questions_data) ? quiz.questions_data : [],
            bestScore: bestScore,
            attemptCount: attempts.length
          }
        } catch (error) {
          console.error(`[Quiz ${quiz.id}] Erreur chargement tentatives:`, error)
          return {
            ...quiz,
            questions_data: Array.isArray(quiz.questions_data) ? quiz.questions_data : [],
            bestScore: null,
            attemptCount: 0
          }
        }
      })
    )
    
    quizList.value = quizWithAttempts
    console.log('[HomeworkByNotion] Quiz avec notes:', quizList.value.map(q => ({
      id: q.id,
      titre: q.titre,
      bestScore: q.bestScore,
      attemptCount: q.attemptCount
    })))
  } catch (error) {
    console.error('[HomeworkByNotion] Erreur lors du chargement des quiz:', error)
    quizList.value = []
  } finally {
    loading.value = false
  }
}

function goBack() {
  router.back()
}

onMounted(() => {
  loadQuiz()
})
</script>

<style scoped>
.quiz-section {
  padding: 1rem 0 2rem;
  min-height: 100vh;
}

.quiz-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem 2rem;
}

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
  margin: 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
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

.quiz-list {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
</style>
