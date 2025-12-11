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
import { getQuizByNotion } from '@/api/quiz'

const route = useRoute()
const router = useRouter()
const notionId = route.params.notionId

const loading = ref(true)
const quizList = ref([])

async function loadQuiz() {
  loading.value = true
  try {
    const response = await getQuizByNotion(notionId)
    // S'assurer que questions_data est bien un tableau
    quizList.value = (response.data || response || []).map(quiz => ({
      ...quiz,
      questions_data: Array.isArray(quiz.questions_data) ? quiz.questions_data : []
    }))
  } catch (error) {
    console.error('Erreur lors du chargement des quiz:', error)
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
