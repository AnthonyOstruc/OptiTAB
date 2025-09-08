<template>
  <div class="daily-objectives-card">
    <div class="objective-header">
      <div class="objective-title">🎯 Défi du jour</div>
      <button class="see-more-btn" @click="showAllObjectives">
        Voir tous les défis
      </button>
    </div>

    <!-- Affichage de l'objectif actuel seulement -->
    <div v-if="currentObjective" class="current-objective" :key="forceUpdate">
      <div class="objective-icon">{{ currentObjective.icon }}</div>
      <div class="objective-content">
        <div class="objective-text">{{ currentObjective.text }}</div>
        <div class="objective-progress">
          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: currentObjectivePercentage + '%' }"
              :class="getProgressBarClass(currentObjectivePercentage)"
            ></div>
          </div>
          <div class="progress-text">
            {{ currentObjective.progress }} / {{ currentObjective.target }}
          </div>
        </div>
      </div>
    </div>
    
    <!-- Message si aucun objectif disponible -->
    <div v-else class="no-objective">
      🎉 Tous les défis du jour sont terminés ! Revenez demain pour de nouveaux défis.
    </div>

    <!-- Badge de complétion si terminé -->
    <div v-if="currentObjective && currentObjective.isCompleted" class="completion-badge">
      ✅ Défi complété ! +{{ currentObjective.xpReward }} XP
    </div>
  </div>

  <!-- Modal pour tous les défis -->
  <div v-if="showModal" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>🎯 Vos défis journaliers</h3>
        <button class="close-btn" @click="closeModal">×</button>
      </div>
      
      <div class="objectives-list">
        <div 
          v-for="(objective, index) in allObjectives" 
          :key="index"
          class="objective-item"
          :class="{
            'completed': objective.isCompleted,
            'locked': !objective.isUnlocked
          }"
        >
          <div class="objective-info">
            <div class="objective-icon-small">{{ objective.icon }}</div>
            <div class="objective-details">
              <div class="objective-text-small">{{ objective.name }}</div>
              <div class="objective-description">{{ objective.text }}</div>
              <div class="objective-reward">+{{ objective.xpReward }} XP</div>
            </div>
          </div>
          <div class="objective-status">
            <div class="progress-info">
              {{ objective.progress }} / {{ objective.target }}
            </div>
            <div class="progress-bar-modal">
              <div 
                class="progress-fill-modal" 
                :style="{ width: objective.percentage + '%' }"
                :class="{ 'completed': objective.isCompleted }"
              ></div>
            </div>
            <div v-if="objective.isCompleted" class="status-completed">
              ✅ Terminé
            </div>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <div class="daily-summary">
          <div class="summary-stat">
            <span class="stat-label">Défis complétés :</span>
            <span class="stat-value">{{ completedObjectivesCount }} / {{ allObjectives.length }}</span>
          </div>
          <div class="summary-stat">
            <span class="stat-label">XP gagnés aujourd'hui :</span>
            <span class="stat-value">+{{ totalXPEarned }}</span>
          </div>
        </div>
        <p class="modal-note">
          Tous les défis se réinitialisent chaque jour à minuit. Bonne chance !
        </p>
      </div>
    </div>
  </div>

  <!-- Notification de récompense XP -->
  <XPRewardNotification />
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useDailyObjectives } from '@/composables/useDailyObjectives'
import XPRewardNotification from '@/components/notifications/XPRewardNotification.vue'

const showModal = ref(false)

// Utiliser le composable pour les objectifs journaliers
const {
  currentObjective,
  unlockedObjectivesList,
  unlockedObjectives,
  allObjectives,
  userStats,
  loadTodayStats,
  // Fonctions de simulation pour les tests
  simulateQuizEasy,
  simulateQuizMedium,
  simulateQuizHard,
  simulateQuizPerfect,
  simulateExerciseCompleted,
  simulateQuizStreak
} = useDailyObjectives()

// Force de mise à jour pour la réactivité
const forceUpdate = ref(0)

// Calculer le nombre de défis complétés
const completedObjectivesCount = computed(() => {
  forceUpdate.value // Forcer la re-évaluation
  return unlockedObjectivesList.value.filter(obj => obj.isCompleted).length
})

// Calculer le total des XP gagnés aujourd'hui
const totalXPEarned = computed(() => {
  forceUpdate.value // Forcer la re-évaluation
  return unlockedObjectivesList.value
    .filter(obj => obj.isCompleted)
    .reduce((total, obj) => total + obj.xpReward, 0)
})

// Fonctions pour le modal
const showAllObjectives = () => {
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

// Vérifier si un objectif est complété (pour la liste dans le modal)
const isObjectiveCompleted = (objective) => {
  return objective.isCompleted
}

// Obtenir la progression d'un objectif (pour la liste dans le modal)
const getObjectiveProgress = (objective) => {
  return objective.progress
}

// Computed pour le pourcentage de l'objectif actuel (réactif)
const currentObjectivePercentage = computed(() => {
  forceUpdate.value // Forcer la re-évaluation
  
  if (!currentObjective.value) {
    console.log(`🎯 [DailyObjectives] Aucun objectif actuel`)
    return 0
  }
  
  const progress = currentObjective.value.progress
  const target = currentObjective.value.target
  const percentage = Math.min((progress / target) * 100, 100)
  
  console.log(`🎯 [DailyObjectives] Calcul pourcentage réactif: ${progress}/${target} = ${percentage}%`)
  console.log(`🎯 [DailyObjectives] Objectif actuel:`, currentObjective.value)
  console.log(`🎯 [DailyObjectives] forceUpdate:`, forceUpdate.value)
  
  return percentage
})

// Calculer le pourcentage de l'objectif actuel avec logs (fonction de fallback)
const getCurrentObjectivePercentage = () => {
  return currentObjectivePercentage.value
}

// Obtenir la classe CSS pour la barre de progression selon le pourcentage
const getProgressBarClass = (percentage) => {
  if (percentage >= 100) {
    return 'completed'
  } else if (percentage >= 75) {
    return 'almost-done'
  } else if (percentage >= 25) {
    return 'half-way'
  } else if (percentage > 0) {
    return 'starting'
  }
  return ''
}

// Fonctions de test (à supprimer en production)
const testQuizEasy = () => simulateQuizEasy()
const testQuizMedium = () => simulateQuizMedium()
const testQuizHard = () => simulateQuizHard()
const testQuizPerfect = () => simulateQuizPerfect()
const testExerciseCompleted = () => simulateExerciseCompleted()
const testQuizStreak = () => simulateQuizStreak(Math.floor(Math.random() * 8) + 1)

// Mise à jour en temps réel des objectifs
const handleObjectiveProgress = (event) => {
  console.log('🎯 [DailyObjectives] Progression mise à jour:', event.detail)
  // Forcer la mise à jour de l'interface
  forceUpdate.value++
  // Recharger les stats pour s'assurer de la synchronisation
  loadTodayStats()
  
  // Log du pourcentage après mise à jour
  setTimeout(() => {
    if (currentObjective.value) {
      console.log('🎯 [DailyObjectives] Objectif après mise à jour:', {
        progress: currentObjective.value.progress,
        target: currentObjective.value.target,
        percentage: currentObjective.value.percentage,
        calculatedPercentage: getCurrentObjectivePercentage()
      })
    }
  }, 100)
}

// Gérer les objectifs débloqués
const handleObjectiveUnlocked = (event) => {
  console.log('🎯 [DailyObjectives] Nouvel objectif débloqué:', event.detail)
  // Forcer la mise à jour de l'interface
  forceUpdate.value++
}

// Gérer les objectifs complétés
const handleObjectiveCompleted = (event) => {
  console.log('🎯 [DailyObjectives] Objectif complété:', event.detail)
  // Forcer la mise à jour de l'interface
  forceUpdate.value++
}

// Watcher pour détecter les changements dans userStats
watch(userStats, (newStats, oldStats) => {
  console.log('🎯 [DailyObjectives] userStats changé:', { newStats, oldStats })
  forceUpdate.value++
}, { deep: true })

// Watcher pour détecter les changements dans unlockedObjectives
watch(unlockedObjectives, (newUnlocked, oldUnlocked) => {
  console.log('🎯 [DailyObjectives] unlockedObjectives changé:', { newUnlocked, oldUnlocked })
  forceUpdate.value++
}, { deep: true })

// Polling pour s'assurer de la synchronisation
let pollInterval = null

const startPolling = () => {
  pollInterval = setInterval(() => {
    loadTodayStats()
    forceUpdate.value++
  }, 2000) // Toutes les 2 secondes
}

const stopPolling = () => {
  if (pollInterval) {
    clearInterval(pollInterval)
    pollInterval = null
  }
}

// Écouter les mises à jour de progression
onMounted(() => {
  window.addEventListener('dailyObjectiveProgress', handleObjectiveProgress)
  window.addEventListener('objectiveUnlocked', handleObjectiveUnlocked)
  window.addEventListener('dailyObjectiveCompleted', handleObjectiveCompleted)
  
  // Log de debug au montage
  console.log('🎯 [DailyObjectives] Composant monté:', {
    userStats: userStats.value,
    currentObjective: currentObjective.value,
    unlockedObjectives: unlockedObjectives.value
  })
  
  // Démarrer le polling pour la synchronisation
  startPolling()
})

onUnmounted(() => {
  window.removeEventListener('dailyObjectiveProgress', handleObjectiveProgress)
  window.removeEventListener('objectiveUnlocked', handleObjectiveUnlocked)
  window.removeEventListener('dailyObjectiveCompleted', handleObjectiveCompleted)
  
  // Arrêter le polling
  stopPolling()
})

// Exposer les fonctions de test pour le développement
window.testDailyObjectives = {
  quizEasy: testQuizEasy,
  quizMedium: testQuizMedium,
  quizHard: testQuizHard,
  quizPerfect: testQuizPerfect,
  exerciseCompleted: testExerciseCompleted,
  quizStreak: testQuizStreak
}
</script>

<style scoped>
.daily-objectives-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: 0 2px 6px rgba(30, 41, 59, 0.06);
  min-width: 320px;
}

.objective-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.objective-title {
  font-weight: 800;
  color: #1f2937;
  font-size: 1rem;
}

.see-more-btn {
  background: #f3f4f6;
  color: #6b7280;
  border: none;
  border-radius: 6px;
  padding: 0.375rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.see-more-btn:hover {
  background: #e5e7eb;
  color: #374151;
}

.current-objective {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.objective-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.objective-content {
  flex: 1;
}

.objective-text {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.75rem;
}

.objective-progress {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: #f1f5f9;
  border-radius: 999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 999px;
  transition: all 0.3s ease;
  background: linear-gradient(90deg, #d1d5db, #9ca3af); /* Couleur par défaut grise */
}

.progress-fill.starting {
  background: linear-gradient(90deg, #f59e0b, #f97316);
}

.progress-fill.half-way {
  background: linear-gradient(90deg, #3b82f6, #2563eb);
}

.progress-fill.almost-done {
  background: linear-gradient(90deg, #8b5cf6, #7c3aed);
}

.progress-fill.completed {
  background: linear-gradient(90deg, #10b981, #059669);
}

.progress-text {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  min-width: 3rem;
  text-align: right;
}

/* Styles pour l'affichage compact des objectifs */
.objectives-compact {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.objective-compact {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  transition: all 0.2s;
}

.objective-compact.completed {
  border-color: #10b981;
  background: #f0fdf4;
}

.objective-icon-compact {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.objective-info-compact {
  flex: 1;
}

.objective-name {
  font-weight: 600;
  color: #1f2937;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.objective-progress-compact {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.progress-bar-compact {
  flex: 1;
  height: 6px;
  background: #f1f5f9;
  border-radius: 999px;
  overflow: hidden;
}

.progress-fill-compact {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #2563eb);
  border-radius: 999px;
  transition: all 0.3s ease;
}

.progress-fill-compact.completed {
  background: linear-gradient(90deg, #10b981, #059669);
}

.progress-text-compact {
  font-size: 0.75rem;
  font-weight: 500;
  color: #6b7280;
  min-width: 2.5rem;
  text-align: right;
}

.completion-check {
  font-size: 1rem;
  flex-shrink: 0;
}

.completion-summary {
  margin-top: 1rem;
  padding: 0.75rem;
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  text-align: center;
}

.completed-count {
  font-weight: 700;
  color: #1f2937;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.total-xp {
  font-weight: 600;
  color: #10b981;
  font-size: 0.75rem;
}

/* Modal styles */
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
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  max-width: 500px;
  width: 90vw;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 1.25rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6b7280;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
}

.close-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.objectives-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.objective-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  transition: all 0.2s;
}

.objective-item.current {
  border-color: #3b82f6;
  background: #eff6ff;
}

.objective-item.completed {
  border-color: #10b981;
  background: #f0fdf4;
}

.objective-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.objective-icon-small {
  font-size: 1.5rem;
}

.objective-details {
  flex: 1;
}

.objective-text-small {
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.25rem;
  font-size: 0.875rem;
}

.objective-description {
  font-size: 0.75rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.objective-reward {
  font-size: 0.75rem;
  color: #10b981;
  font-weight: 600;
}

.objective-status {
  text-align: right;
  min-width: 6rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.progress-info {
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

.progress-bar-modal {
  width: 100%;
  height: 6px;
  background: #f1f5f9;
  border-radius: 999px;
  overflow: hidden;
}

.progress-fill-modal {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #2563eb);
  border-radius: 999px;
  transition: all 0.3s ease;
}

.progress-fill-modal.completed {
  background: linear-gradient(90deg, #10b981, #059669);
}

.status-completed {
  color: #10b981;
  font-weight: 600;
  font-size: 0.75rem;
}

.modal-footer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.daily-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 8px;
}

.summary-stat {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  text-align: center;
}

.stat-label {
  font-size: 0.75rem;
  color: #6b7280;
  font-weight: 500;
}

.stat-value {
  font-size: 1rem;
  color: #1f2937;
  font-weight: 700;
}

.modal-note {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
  text-align: center;
  font-style: italic;
}

.no-objective {
  text-align: center;
  padding: 24px;
  color: #6b7280;
  font-size: 1rem;
  background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
  border-radius: 12px;
  border: 2px dashed #d1d5db;
}

.completion-badge {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  text-align: center;
  margin-top: 12px;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

@media (max-width: 768px) {
  .modal-content {
    width: 95vw;
    padding: 1rem;
  }
  
  .objective-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .objective-info {
    width: 100%;
  }
  
  .objective-status {
    align-self: flex-end;
  }
}
</style>
