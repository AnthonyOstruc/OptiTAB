<template>
  <DashboardLayout>
    <section class="cours-detail-section">
      <!-- Bouton de retour -->
      <BackButton 
        text="Retour aux cours" 
        :customAction="goBackToCours"
        position="top-left"
      />
      
      <div v-if="loading" class="loading-container">
        <LoadingSpinner />
      </div>
      
      <div v-else-if="cours" class="cours-container">
        <!-- En-tête du cours -->
        <header class="cours-header">
          <h1 class="cours-title">{{ cours.titre }}</h1>
          <div class="cours-meta">
            <span class="cours-difficulty" :class="cours.difficulty">
              {{ getDifficultyLabel(cours.difficulty) }}
            </span>
            <span class="cours-date">
              {{ formatDate(cours.date_creation) }}
            </span>
          </div>
          <p v-if="cours.description" class="cours-description">
            {{ cours.description }}
          </p>
        </header>
        
        <!-- Contenu du cours -->
        <div class="cours-content" v-html="renderedContent"></div>
        
        <!-- Vidéo du cours si disponible -->
        <div v-if="cours.video_url" class="cours-video">
          <h3>Vidéo explicative</h3>
          <div class="video-container">
            <iframe
              :src="cours.video_url"
              title="Vidéo du cours"
              frameborder="0"
              allowfullscreen
            ></iframe>
          </div>
        </div>
      </div>
      
      <div v-else class="no-cours">
        <p>Cours non trouvé.</p>
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
import { renderContentWithImages, renderMath } from '@/utils/scientificRenderer'

const route = useRoute()
const router = useRouter()

const cours = ref(null)
const loading = ref(true)

// Récupérer les paramètres de la route
const coursId = computed(() => route.params.coursId)
const currentMatiereId = computed(() => route.params.matiereId)
const currentNotionId = computed(() => route.params.notionId)
const currentChapitreId = computed(() => route.params.chapitreId)

// Contenu rendu avec images et formules
const renderedContent = computed(() => {
  if (!cours.value?.contenu) return ''
  
  // Récupérer les images du cours
  const images = cours.value.images || []
  
  // Rendre le contenu avec les images intégrées
  return renderContentWithImages(cours.value.contenu, images)
})

// Fonction pour revenir aux cours
function goBackToCours() {
  if (currentChapitreId.value) {
    router.push({ 
      name: 'Cours', 
      params: { 
        matiereId: currentMatiereId.value,
        notionId: currentNotionId.value,
        chapitreId: currentChapitreId.value
      } 
    })
  } else {
    router.back()
  }
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
    
    // Récupérer les cours du chapitre
    const { data } = await getCours(
      currentMatiereId.value,
      currentNotionId.value,
      currentChapitreId.value
    )
    
    // Trouver le cours correspondant à l'ID
    if (Array.isArray(data)) {
      cours.value = data.find(c => c.id == coursId.value)
    } else if (data && data.id == coursId.value) {
      // Si c'est un seul cours et qu'il correspond
      cours.value = data
    } else if (data) {
      // S'il n'y a qu'un cours dans le chapitre, le prendre
      cours.value = data
    }
    
    // Rendre le contenu MathJax après le chargement
    nextTick(() => {
      renderMath()
    })
  } catch (error) {
    console.error('Erreur lors du chargement du cours:', error)
    cours.value = null
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.cours-detail-section {
  background: #fff;
  padding: 0 5vw 40px 5vw;
  position: relative;
  min-height: 100vh;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.no-cours {
  text-align: center;
  padding: 40px;
  color: #666;
}

.cours-container {
  max-width: 800px;
  margin: 0 auto;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.cours-header {
  background: linear-gradient(135deg, #193e8e, #2563eb);
  color: white;
  padding: 2rem;
  text-align: center;
}

.cours-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin: 0 0 1rem 0;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.cours-meta {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.cours-difficulty {
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-size: 0.875rem;
  font-weight: 600;
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

.cours-date {
  font-size: 0.875rem;
  opacity: 0.9;
  font-style: italic;
}

.cours-description {
  font-size: 1.1rem;
  line-height: 1.6;
  margin: 0;
  opacity: 0.95;
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
  max-width: 100%;
}

.cours-content {
  padding: 2rem;
  line-height: 1.8;
  color: #333;
  font-size: 1rem;
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
  max-width: 100%;
}

.cours-content :deep(h1),
.cours-content :deep(h2),
.cours-content :deep(h3),
.cours-content :deep(h4),
.cours-content :deep(h5),
.cours-content :deep(h6) {
  color: #193e8e;
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.cours-content :deep(h1) {
  font-size: 2rem;
}

.cours-content :deep(h2) {
  font-size: 1.75rem;
}

.cours-content :deep(h3) {
  font-size: 1.5rem;
}

.cours-content :deep(h4) {
  font-size: 1.25rem;
}

.cours-content :deep(p) {
  margin-bottom: 1rem;
}

.cours-content :deep(ul),
.cours-content :deep(ol) {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}

.cours-content :deep(li) {
  margin-bottom: 0.5rem;
}

.cours-content :deep(strong) {
  color: #193e8e;
  font-weight: 600;
}

.cours-content :deep(em) {
  color: #666;
  font-style: italic;
}

.cours-content :deep(code) {
  background: #f8f9fa;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
  color: #e91e63;
}

.cours-content :deep(pre) {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1rem 0;
  border-left: 4px solid #193e8e;
}

.cours-content :deep(blockquote) {
  border-left: 4px solid #193e8e;
  background: #f8f9fa;
  padding: 1rem;
  margin: 1rem 0;
  font-style: italic;
}

.cours-content :deep(.cours-image) {
  text-align: center;
  margin: 2rem 0;
}

.cours-content :deep(.cours-image img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.cours-content :deep(.cours-image .image-caption) {
  margin-top: 0.5rem;
  font-style: italic;
  color: #666;
  font-size: 0.875rem;
}

.cours-video {
  padding: 2rem;
  border-top: 1px solid #e0e0e0;
}

.cours-video h3 {
  color: #193e8e;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.video-container {
  position: relative;
  width: 100%;
  height: 0;
  padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
}

.video-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 8px;
}

/* MathJax Styles */
.cours-content :deep(.MathJax) {
  font-size: 1.1em !important;
  margin: 0.5em 0 !important;
}

.cours-content :deep(.MathJax_Display) {
  margin: 1.5em 0 !important;
  text-align: center !important;
}

.cours-content :deep(.MathJax_SVG_Display) {
  margin: 1.5em 0 !important;
  text-align: center !important;
}

.cours-content :deep(.MathJax_SVG) {
  font-size: 1.1em !important;
}

/* Responsive */
@media (max-width: 768px) {
  .cours-detail-section {
    padding: 0 3vw 40px 3vw;
  }
  
  .cours-header {
    padding: 1.5rem;
  }
  
  .cours-title {
    font-size: 2rem;
  }
  
  .cours-content {
    padding: 1.5rem;
  }
  
  .cours-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
}

@media (max-width: 480px) {
  .cours-title {
    font-size: 1.75rem;
  }
  
  .cours-content {
    padding: 1rem;
    font-size: 0.95rem;
  }
  
  .cours-content :deep(h1) {
    font-size: 1.5rem;
  }
  
  .cours-content :deep(h2) {
    font-size: 1.375rem;
  }
  
  .cours-content :deep(h3) {
    font-size: 1.25rem;
  }
}
</style>
