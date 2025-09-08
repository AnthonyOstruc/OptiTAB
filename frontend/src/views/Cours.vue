<template>
  <DashboardLayout>
    <section class="cours-section">
      <!-- Bouton de retour -->
      <BackButton 
        text="Retour aux chapitres" 
        :customAction="goBackToChapitres"
        position="top-left"
      />
      
      <h2 class="cours-title">Cours disponibles</h2>
      
      <div v-if="loading" class="loading-container">
        <LoadingSpinner />
      </div>
      
      <div v-else-if="cours.length === 0" class="no-cours">
        <p>Aucun cours disponible pour le moment.</p>
      </div>
      
      <div v-else class="cours-grid">
        <div
          v-for="coursItem in cours"
          :key="coursItem.id"
          class="cours-card"
          @click="viewCours(coursItem)"
        >
          <div class="cours-card-header">
            <h3 class="cours-card-title">{{ coursItem.titre }}</h3>
            <span class="cours-difficulty" :class="coursItem.difficulty">
              {{ getDifficultyLabel(coursItem.difficulty) }}
            </span>
          </div>
          
          <p v-if="coursItem.description" class="cours-description">
            {{ coursItem.description }}
          </p>
          
          <div class="cours-meta">
            <span class="cours-date">
              Créé le {{ formatDate(coursItem.date_creation) }}
            </span>
          </div>
        </div>
      </div>
    </section>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import BackButton from '@/components/common/BackButton.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import { getCours } from '@/api/cours'
import { useSubjectsStore } from '@/stores/subjects/index'
import { renderContentWithImages, renderMath } from '@/utils/scientificRenderer'

const route = useRoute()
const router = useRouter()
const subjectsStore = useSubjectsStore()

const cours = ref([])
const loading = ref(true)

// Récupérer les paramètres de la route
const currentMatiereId = computed(() => {
  return subjectsStore.activeMatiereId || route.params.matiereId
})

const currentNotionId = computed(() => route.params.notionId)
const currentChapitreId = computed(() => route.params.chapitreId)

// Fonction pour revenir aux chapitres
function goBackToChapitres() {
  if (currentChapitreId.value) {
    router.push({ 
      name: 'CourseChapitres', 
      params: { 
        matiereId: currentMatiereId.value,
        notionId: currentNotionId.value 
      } 
    })
  } else {
    router.back()
  }
}

// Fonction pour afficher un cours
function viewCours(coursItem) {
  router.push({ 
    name: 'CoursDetail', 
    params: { 
      coursId: coursItem.id,
      matiereId: currentMatiereId.value,
      notionId: currentNotionId.value,
      chapitreId: currentChapitreId.value
    } 
  })
}

// Fonction pour obtenir le label de difficulté
function getDifficultyLabel(difficulty) {
  const labels = {
    'easy': 'Facile',
    'medium': 'Moyen',
    'hard': 'Difficile'
  }
  return labels[difficulty] || difficulty
}

// Fonction pour formater la date
function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(async () => {
  try {
    loading.value = true
    
    const { data } = await getCours(
      currentMatiereId.value,
      currentNotionId.value,
      currentChapitreId.value
    )
    
    cours.value = data
    
    // Rendre le contenu MathJax après le chargement
    nextTick(() => {
      renderMath()
    })
  } catch (error) {
    console.error('Erreur lors du chargement des cours:', error)
    cours.value = []
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.cours-section {
  background: #fff;
  padding: 0 5vw 40px 5vw;
  text-align: center;
  position: relative;
}

.cours-title {
  font-size: 2rem;
  color: #193e8e;
  margin-bottom: 40px;
  font-weight: 800;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.no-cours {
  text-align: center;
  padding: 40px;
  color: #666;
}

.cours-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.cours-card {
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.cours-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  border-color: #193e8e;
}

.cours-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.cours-card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #193e8e;
  margin: 0;
  flex: 1;
}

.cours-difficulty {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.cours-difficulty.easy {
  background: #e8f5e8;
  color: #2e7d32;
}

.cours-difficulty.medium {
  background: #fff3e0;
  color: #f57c00;
}

.cours-difficulty.hard {
  background: #ffebee;
  color: #c62828;
}

.cours-description {
  color: #666;
  margin-bottom: 1rem;
  line-height: 1.5;
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
  max-width: 100%;
}

.cours-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
  color: #999;
}

.cours-date {
  font-style: italic;
}

@media (max-width: 640px) {
  .cours-title {
    font-size: 1.5rem;
    margin-bottom: 30px;
  }
  
  .cours-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .cours-card {
    padding: 1rem;
  }
  
  .cours-card-title {
    font-size: 1.1rem;
  }
}

/* MathJax Styles pour les cours */
.cours-content :deep(.MathJax) {
  font-size: 1em !important;
  margin: 0.5em 0 !important;
}

.cours-content :deep(.MathJax_Display) {
  margin: 1em 0 !important;
  text-align: center !important;
}

.cours-content :deep(.MathJax_SVG_Display) {
  margin: 1em 0 !important;
  text-align: center !important;
}

.cours-content :deep(.MathJax_SVG) {
  font-size: 1em !important;
}
</style> 