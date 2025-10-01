<template>
  <DashboardLayout>
    <section class="cours-section">
      <!-- Bouton de retour -->
      <BackButton 
        text="Retour aux notions" 
        :customAction="goBackToNotions"
        position="top-left"
      />
      
      <div v-if="loading" class="loading-container">
        <SkeletonList :count="3" />
      </div>
      
      <div v-else-if="selectedCours" class="cours-container">
        <header class="cours-header">
          <div class="cours-header-top">
            <h1 class="cours-title">{{ selectedCours.titre }}</h1>
            <template v-if="selectedCours.pdf_url">
              <a :href="selectedCours.pdf_url" class="btn-pdf" :download="`${selectedCours.titre}.pdf`">Télécharger PDF</a>
            </template>
          </div>
          <div class="cours-meta">
            <span class="cours-difficulty" :class="selectedCours.difficulty">
              {{ getDifficultyLabel(selectedCours.difficulty) }}
            </span>
            <span class="cours-date">
              {{ formatDate(selectedCours.date_creation) }}
            </span>
          </div>
          <p v-if="selectedCours.description" class="cours-description">
            {{ selectedCours.description }}
          </p>
        </header>
        <div class="cours-content" v-html="renderedContent"></div>
        <div v-if="selectedCours.video_url" class="cours-video">
          <h3>Vidéo explicative</h3>
          <div class="video-container">
            <iframe :src="selectedCours.video_url" title="Vidéo du cours" frameborder="0" allowfullscreen></iframe>
          </div>
        </div>
      </div>
      
      <div v-else-if="cours.length === 0" class="no-cours">
        <p>Aucun cours disponible pour le moment.</p>
      </div>
      
      <div v-else class="cours-grid">
        <div v-for="coursItem in cours" :key="coursItem.id" class="cours-card" @click="viewCours(coursItem)">
          <div class="cours-card-header">
            <h3 class="cours-card-title">{{ coursItem.titre }}</h3>
            <span class="cours-difficulty" :class="coursItem.difficulty">{{ getDifficultyLabel(coursItem.difficulty) }}</span>
          </div>
          <p v-if="coursItem.description" class="cours-description">{{ coursItem.description }}</p>
          <div class="cours-meta">
            <span class="cours-date">Créé le {{ formatDate(coursItem.date_creation) }}</span>
          </div>
        </div>
      </div>
    </section>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, computed, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import BackButton from '@/components/common/BackButton.vue'
import SkeletonList from '@/components/common/SkeletonList.vue'
import { getCours } from '@/api/cours'
import { useSubjectsStore } from '@/stores/subjects/index'
import { renderContentWithImages, renderMath } from '@/utils/scientificRenderer'

const route = useRoute()
const router = useRouter()
const subjectsStore = useSubjectsStore()

const cours = ref([])
const selectedCours = ref(null)
const loading = ref(true)

// Récupérer les paramètres de la route
const currentMatiereId = computed(() => {
  return subjectsStore.activeMatiereId || route.params.matiereId
})

const currentNotionId = computed(() => route.params.notionId)
const currentChapitreId = computed(() => route.params.chapitreId)

// Fonction pour revenir aux chapitres
function goBackToNotions() {
  if (currentChapitreId.value) {
    router.push({ 
      name: 'CourseByNotion', 
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
  selectedCours.value = coursItem
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
    if (Array.isArray(cours.value) && cours.value.length === 1) {
      selectedCours.value = cours.value[0]
    }
    // Si le backend renvoie directement un objet
    if (data && !Array.isArray(data)) {
      selectedCours.value = data
      cours.value = [data]
    }
    
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

const renderedContent = computed(() => {
  if (!selectedCours.value?.contenu) return ''
  
  let content = selectedCours.value.contenu
  const images = selectedCours.value.images || []
  
  // Remplacer les marqueurs [IMAGE_X] par les vraies images
  content = content.replace(/\[IMAGE_(\d+)\]/g, (match, position) => {
    const index = parseInt(position) - 1
    const image = images[index]
    
    if (image) {
      return `
        <div class="content-image-container" style="text-align: center; margin: 2em 0;">
          <img 
            src="${image.image}" 
            alt="${image.legende || `Image ${position}`}" 
            class="content-image"
            style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"
          />
          ${image.legende ? `<div class="image-caption" style="margin-top: 0.5rem; font-size: 0.875rem; color: #666; font-style: italic;">${image.legende}</div>` : ''}
        </div>
      `
    } else {
      return `
        <div class="image-placeholder" style="text-align: center; padding: 2em; background: #f5f5f5; border-radius: 8px; margin: 2em 0;">
          <div style="font-size: 2rem;">🖼️</div>
          <div style="color: #999; margin-top: 0.5rem;">Image ${position} non disponible</div>
        </div>
      `
    }
  })
  
  // Fallback: s'il n'y a PAS de marqueurs [IMAGE_X] mais qu'on a des images,
  // on les affiche automatiquement à la fin du contenu
  if (!/\[IMAGE_\d+\]/.test(selectedCours.value.contenu || '') && images.length > 0) {
    const autoGallery = images.map(img => `
      <div class="content-image-container" style="text-align: center; margin: 2em 0;">
        <img 
          src="${img.image}" 
          alt="${img.legende || ''}" 
          class="content-image"
          style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"
        />
        ${img.legende ? `<div class="image-caption" style="margin-top: 0.5rem; font-size: 0.875rem; color: #666; font-style: italic;">${img.legende}</div>` : ''}
      </div>
    `).join('\n')
    content = `${content}\n${autoGallery}`
  }
  
  // Utiliser le rendu Markdown/HTML
  return renderContentWithImages(content, images)
})

// Relancer renderMath() quand le contenu change
watch(selectedCours, () => {
  if (selectedCours.value) {
    nextTick(() => {
      renderMath()
    })
  }
}, { deep: true })
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

.cours-header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.btn-pdf {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  background: #dc2626;
  color: #fff;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.btn-pdf:hover {
  background: #b91c1c;
}

@media (max-width: 640px) {
  .cours-header-top {
    flex-direction: column;
    align-items: flex-start;
  }
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

/* Styles pour le contenu du cours */
.cours-content {
  text-align: left;
  max-width: 100%;
  overflow-wrap: break-word;
  word-wrap: break-word;
  hyphens: auto;
  line-height: 1.6;
  color: #333;
  padding: 2rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* Styles pour les titres dans le contenu */
.cours-content :deep(h1),
.cours-content :deep(h2),
.cours-content :deep(h3),
.cours-content :deep(h4),
.cours-content :deep(h5),
.cours-content :deep(h6) {
  color: #193e8e;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}

.cours-content :deep(p) {
  margin-bottom: 0.5rem;
}

.cours-content :deep(ul),
.cours-content :deep(ol) {
  margin-bottom: 0.5rem;
  padding-left: 1.5rem;
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