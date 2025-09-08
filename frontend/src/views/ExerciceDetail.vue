<template>
  <ExercisePageLayout>
    <section class="exercice-detail-section">
      <BackButton 
        text="Retour aux exercices" 
        :customAction="goBackToExercices"
        position="top-left"
      />
      
      <div v-if="loading" class="state-container">
        <div class="loading-spinner"></div>
        <p>Chargement de l'exercice...</p>
      </div>

      <div v-else-if="error" class="state-container">
        <div class="icon">❌</div>
        <h3>Erreur de chargement</h3>
        <p>{{ error }}</p>
        <button class="btn-primary" @click="loadExercice">Réessayer</button>
      </div>

      <div v-else-if="exercice" class="exercice-content">
        <!-- Boutons de téléchargement PDF -->
        <div class="exercice-actions">
          <PDFDownloadButton
            type="single"
            :data="exercice"
            :title="`Exercice_${exercice.id}_Enonce`"
            text="📄 Exercice (PDF serveur)"
            :useMathJax="true"
            :includeSolution="false"
            class="pdf-btn exercice-btn"
          />
          <PDFDownloadButton
            type="single"
            :data="exercice"
            :title="`Exercice_${exercice.id}_Corrige`"
            text="📝 Exercice + Corrigé (PDF serveur)"
            :useMathJax="true"
            :includeSolution="true"
            class="pdf-btn corrige-btn"
          />
        </div>
        
        <ExerciceQCM
          :eid="exercice.id"
          :titre="exercice.titre || exercice.nom"
          :instruction="exercice.instruction || exercice.contenu || exercice.question"
          :solution="exercice.solution || exercice.reponse_correcte || ''"
          :etapes="exercice.etapes || ''"
          :difficulty="exercice.difficulty || exercice.difficulte || 'medium'"
          :current="statusMap[exercice.id]?.status"
          @status-changed="handleStatus"
        />
      </div>

      <div v-else class="state-container">
        <div class="icon">📝</div>
        <h3>Exercice non trouvé</h3>
        <p>L'exercice demandé n'existe pas ou n'est plus disponible.</p>
        <button class="btn-primary" @click="goBackToExercices">Retour aux exercices</button>
      </div>
    </section>
  </ExercisePageLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getExerciceDetail } from '@/api'
import { useUserStore } from '@/stores/user'
import { useExerciseStatus } from '@/composables/useExerciseStatus'
import ExercisePageLayout from '@/components/common/ExercisePageLayout.vue'
import ExerciceQCM from '@/components/UI/ExerciceQCM.vue'
import BackButton from '@/components/common/BackButton.vue'
import PDFDownloadButton from '@/components/common/PDFDownloadButton.vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const { statusMap, loadStatuses, updateExerciseStatus } = useExerciseStatus()
const exerciceId = route.params.exerciceId

const exercice = ref(null)
const loading = ref(true)
const error = ref('')

const goBackToExercices = () => {
  const target = exercice.value?.chapitre 
    ? { name: 'Exercices', params: { chapitreId: String(exercice.value.chapitre) } }
    : { name: 'Dashboard' }
  router.push(target)
}

const loadExercice = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const exerciceResponse = await getExerciceDetail(exerciceId)
    exercice.value = exerciceResponse?.data || exerciceResponse
    
    if (!exercice.value) {
      error.value = 'Exercice non trouvé'
      return
    }
    
    // Charger les statuts via le composable
    await loadStatuses()
  } catch (err) {
    console.error('[ExerciceDetail] Erreur:', err)
    error.value = "Impossible de charger l'exercice. Veuillez réessayer."
  } finally {
    loading.value = false
  }
}

const handleStatus = async ({ exerciceId, status }) => {
  try {
    await updateExerciseStatus(exerciceId, status)
    
    // Intégration avec les objectifs journaliers
    if (status === 'acquired') {
      console.log(`[ExerciceDetail] Exercice réussi - intégration objectifs journaliers`)
      // Importer et utiliser l'intégration des objectifs journaliers
      const { useDailyObjectivesIntegration } = await import('@/composables/useDailyObjectives')
      const { onExerciseCompleted } = useDailyObjectivesIntegration()
      
      // Notifier le système d'objectifs
      onExerciseCompleted({
        exerciceId,
        isSuccess: true,
        status: 'acquired'
      })
    }
  } catch (err) {
    console.error('[ExerciceDetail] Erreur handleStatus:', err)
  }
}

onMounted(loadExercice)
</script>

<style scoped>
.exercice-detail-section {
  background: #fff;
  padding: 0 5vw 40px;
  text-align: center;
  min-height: 100vh;
}

.state-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #10b981;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

.icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.state-container h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 0.5rem 0;
}

.state-container p {
  color: #6b7280;
  margin: 0 0 1.5rem 0;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3);
}

.exercice-content {
  max-width: 800px;
  margin: 0 auto;
}

.exercice-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
}

.pdf-btn {
  margin-left: auto;
}

.exercice-btn {
  background: #3b82f6 !important;
  border-color: #3b82f6 !important;
}

.exercice-btn:hover {
  background: #2563eb !important;
  border-color: #2563eb !important;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.corrige-btn {
  background: #10b981 !important;
  border-color: #10b981 !important;
}

.corrige-btn:hover {
  background: #059669 !important;
  border-color: #059669 !important;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .exercice-detail-section { padding: 0 3vw 30px; }
  .state-container { padding: 3rem 1rem; }
}
</style>
