<template>
  <div v-if="pendingSubmissions.length > 0" class="pending-section">
    <div class="pending-card">
      <div class="pending-header">
        <h3 class="pending-title">
          <span class="pending-icon">⏱️</span>
          Corrections en cours
        </h3>
        <span class="pending-count">{{ pendingSubmissions.length }}</span>
      </div>
      
      <div class="pending-list">
        <div 
          v-for="submission in pendingSubmissions" 
          :key="submission.id" 
          class="pending-item"
        >
          <div class="pending-item-content">
            <div class="pending-quiz-title">{{ submission.quiz_titre || 'Quiz' }}</div>
            <div class="pending-date">Envoyé {{ formatDate(submission.date_creation) }}</div>
          </div>
          <span class="status-badge">En attente</span>
        </div>
      </div>
      
      <div class="pending-info">
        Vous serez notifié dès que la correction sera disponible
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getQuizSubmissions } from '@/api/quizSubmissions'

const pendingSubmissions = ref([])
const loading = ref(true)

function formatDate(isoDate) {
  if (!isoDate) return ''
  const date = new Date(isoDate)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMins / 60)
  const diffDays = Math.floor(diffHours / 24)

  if (diffMins < 1) return "à l'instant"
  if (diffMins < 60) return `il y a ${diffMins} min`
  if (diffHours < 24) return `il y a ${diffHours}h`
  if (diffDays < 7) return `il y a ${diffDays}j`
  
  return date.toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'short'
  })
}

async function loadPendingSubmissions() {
  loading.value = true
  try {
    const response = await getQuizSubmissions({ status: 'pending' })
    // Gérer différentes structures de réponse
    let submissions = response
    if (response?.data) {
      submissions = Array.isArray(response.data) 
        ? response.data 
        : (response.data?.results || response.results || [])
    } else if (response?.results) {
      submissions = response.results
    }
    
    pendingSubmissions.value = Array.isArray(submissions) ? submissions : []
    console.log('[PendingCorrections] Soumissions en attente:', pendingSubmissions.value.length)
  } catch (error) {
    console.error('[PendingCorrections] Erreur lors du chargement:', error)
    pendingSubmissions.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadPendingSubmissions()
})

// Exposer la méthode de rechargement pour le parent si nécessaire
defineExpose({ loadPendingSubmissions })
</script>

<style scoped>
.pending-section {
  margin-top: 1.25rem;
  margin-bottom: 1.25rem;
}

.pending-card {
  background: #fff;
  border: 1px solid #f97316;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  box-shadow: 0 2px 6px rgba(249, 115, 22, 0.15);
}

.pending-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.pending-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 800;
  color: #1f2937;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.pending-icon {
  font-size: 1.2rem;
}

.pending-count {
  background: #ffedd5;
  color: #c2410c;
  font-weight: 700;
  font-size: 0.875rem;
  padding: 0.25rem 0.625rem;
  border-radius: 999px;
  border: 1px solid #f97316;
}

.pending-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.pending-item {
  background: #fff7ed;
  border: 1px solid #fed7aa;
  border-radius: 8px;
  padding: 0.75rem 0.875rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  transition: background 0.2s ease;
}

.pending-item:hover {
  background: #ffedd5;
}

.pending-item-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.pending-quiz-title {
  font-weight: 600;
  color: #1f2937;
  font-size: 0.9rem;
}

.pending-date {
  font-size: 0.8rem;
  color: #6b7280;
}

.status-badge {
  background: #f97316;
  color: #fff;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.3rem 0.7rem;
  border-radius: 6px;
  white-space: nowrap;
}

.pending-info {
  font-size: 0.85rem;
  color: #6b7280;
  border-top: 1px solid #fed7aa;
  padding-top: 0.75rem;
  text-align: center;
}

@media (max-width: 768px) {
  .pending-card {
    padding: 0.875rem 1rem;
  }
  
  .pending-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .status-badge {
    align-self: flex-start;
  }
}
</style>
