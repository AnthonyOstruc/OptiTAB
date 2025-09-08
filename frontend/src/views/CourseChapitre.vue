<template>
  <DashboardLayout>
    <section class="course-chapitre-section">
      <!-- Bouton de retour -->
      <BackButton 
        text="Retour aux chapitres" 
        :customAction="goBackToChapitres"
        position="top-left"
      />
      

      
      <h2 class="course-chapitre-title">{{ chapitre?.nom || 'Cours en ligne' }}</h2>
      
      <!-- Boutons d'affichage et PDF -->
      <div class="display-toggle-container">
        <button 
          class="display-toggle-btn" 
          @click="toggleDisplayMode"
          :class="{ 'active': isWideDisplay }"
        >
          <span class="toggle-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 3h18v18H3z"/>
              <path d="M3 9h18"/>
              <path d="M9 21V9"/>
            </svg>
          </span>
          <span class="toggle-text">{{ isWideDisplay ? 'Normal' : 'Large' }}</span>
        </button>

        <!-- Boutons PDF -->
        <div v-if="!loading && cours.length > 0" class="pdf-buttons-group">
          <PDFDownloadButton
            type="cours"
            :data="cours"
            :title="`Cours_${chapitre?.nom || 'Chapitre'}`"
            text="📄 PDF"
            :useMathJax="true"
            :includeSolution="false"
            class="pdf-btn-compact"
            title="Télécharger le cours en PDF"
          />
        </div>
      </div>
      
      <div v-if="chapitre" class="course-content" :class="{ 'wide-display': isWideDisplay }">
        <div class="course-header">
          <p class="course-description">{{ chapitre.description }}</p>
        </div>
        
        <!-- Contenu du cours -->
        <div class="course-body">
          <div v-if="loading" class="loading-state">
            <div class="loading-spinner"></div>
            <span>Chargement des cours...</span>
          </div>
          
          <div v-else-if="cours.length === 0" class="coming-soon">
            <div class="coming-soon-icon">📚</div>
            <h3>Aucun cours disponible</h3>
            <p>Il n'y a pas encore de cours pour ce chapitre.</p>
            <p>Les cours seront bientôt disponibles.</p>
          </div>
          
          <div v-else class="cours-list">
            <div v-for="coursItem in cours" :key="coursItem.id" class="cours-item">
              <div class="cours-header">
                <h3 class="cours-title">{{ coursItem.titre }}</h3>
                <span class="cours-difficulty" :class="coursItem.difficulty">
                  {{ getDifficultyLabel(coursItem.difficulty) }}
                </span>
              </div>
              
              <div v-if="coursItem.description" class="cours-description">
                {{ coursItem.description }}
              </div>
              
              <div class="cours-content" v-html="renderContentWithImages(coursItem.contenu, coursItem.images)" @click="handleImageClick"></div>
              
              <!-- Images du cours -->
              <div v-if="coursItem.images && coursItem.images.length > 0" class="cours-images">
                <div v-for="image in coursItem.images" :key="image.id" class="cours-image">
                  <img :src="getImageUrl(image.image)" :alt="image.legende || image.image_type" />
                  <div v-if="image.legende" class="image-legende">{{ image.legende }}</div>
                </div>
              </div>
              
              <div class="cours-meta">
                <span class="cours-date">Créé le {{ formatDate(coursItem.date_creation) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else class="loading-state">
        <div class="loading-spinner"></div>
        <span>Chargement du cours...</span>
      </div>
    </section>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, computed, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import BackButton from '@/components/common/BackButton.vue'
import PDFDownloadButton from '@/components/common/PDFDownloadButton.vue'

import { getChapitres, getChapitreDetail } from '@/api'
import { getCours } from '@/api/cours'
import { useSubjectsStore } from '@/stores/subjects/index'
import { useUserStore } from '@/stores/user'
import { renderContentWithImages, renderMath, getImageUrl } from '@/utils/scientificRenderer'

const route = useRoute()
const router = useRouter()
const subjectsStore = useSubjectsStore()
const userStore = useUserStore()

const chapitre = ref(null)
const chapitres = ref([])
const cours = ref([])
const loading = ref(true)
const isWideDisplay = ref(false)

// Fonction pour revenir aux chapitres
async function goBackToChapitres() {
  try {
    const chapitreId = route.params.chapitreId
    if (!chapitreId) {
      router.back()
      return
    }
    // Utiliser le détail du chapitre pour récupérer la notion
    const ch = chapitre.value || await getChapitreDetail(chapitreId)
    const notionId = ch?.notion
    if (notionId) {
      router.push({ name: 'CourseChapitres', params: { notionId } })
    } else {
      router.back()
    }
  } catch (error) {
    console.error('Erreur lors de la navigation:', error)
    router.back()
  }
}

// Fonctions utilitaires
function getDifficultyLabel(difficulty) {
  const labels = {
    'easy': 'Facile',
    'medium': 'Moyen',
    'hard': 'Difficile'
  }
  return labels[difficulty] || difficulty
}

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

function handleImageClick(event) {
  // Gérer le clic sur les images si nécessaire
  if (event.target.tagName === 'IMG') {
    console.log('Image cliquée:', event.target.src)
  }
}

function toggleDisplayMode() {
  isWideDisplay.value = !isWideDisplay.value
}

// Cache simple pour les cours d'un chapitre (localStorage)
const COURSE_CACHE_TTL_MS = 120000
function courseCacheKey(chapitreId) { return `course_chapitre:${chapitreId}` }
function readCourseCache(chapitreId) {
  try {
    const raw = localStorage.getItem(courseCacheKey(chapitreId))
    if (!raw) return null
    const parsed = JSON.parse(raw)
    if (!parsed?.t || !parsed?.v) return null
    if (Date.now() - parsed.t > COURSE_CACHE_TTL_MS) return null
    return parsed.v
  } catch (_) { return null }
}
function writeCourseCache(chapitreId, value) {
  try { localStorage.setItem(courseCacheKey(chapitreId), JSON.stringify({ t: Date.now(), v: value })) } catch (_) {}
}

onMounted(async () => {
  loading.value = true
  try {
    const chapitreId = route.params.chapitreId
    if (!chapitreId) return

    // Cache d'abord
    const cached = readCourseCache(chapitreId)
    if (cached) {
      chapitre.value = cached.chapitre || null
      cours.value = Array.isArray(cached.cours) ? cached.cours : []
      loading.value = false
      // refresh en arrière-plan
      getChapitreDetail(chapitreId).then(async ch => {
        const { data: cData } = await getCours(null, null, chapitreId)
        writeCourseCache(chapitreId, { chapitre: ch, cours: cData || [] })
      }).catch(()=>{})
      return
    }

    // Charger le chapitre (détail direct)
    const ch = await getChapitreDetail(chapitreId)
    chapitre.value = ch

    // Charger les cours du chapitre
    const { data: coursData } = await getCours(null, null, chapitreId)
    cours.value = coursData || []
    writeCourseCache(chapitreId, { chapitre: ch, cours: cours.value })

    nextTick(() => { renderMath() })
  } catch (error) {
    console.error('Erreur lors du chargement du cours:', error)
    chapitre.value = null
    cours.value = []
  } finally {
    loading.value = false
  }
})

// Watcher pour re-rendre MathJax quand le contenu change
watch(cours, () => {
  nextTick(() => {
    renderMath()
  })
}, { deep: true })
</script>

<style scoped>
.course-chapitre-section {
  background: #fff;
  padding: 0 5vw 40px 5vw;
  position: relative;
  min-height: 60vh;
}

.course-chapitre-title {
  font-size: 2rem;
  color: #193e8e;
  margin-bottom: 30px;
  font-weight: 800;
  text-align: center;
}

.course-content {
  max-width: 800px;
  margin: 0 auto;
  overflow: visible;
  transition: max-width 0.3s ease;
}

.course-content.wide-display {
  max-width: 1200px;
}

.display-toggle-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.pdf-buttons-group {
  display: flex;
  gap: 0.5rem;
}

/* Styles pour les boutons PDF compacts */
.pdf-btn-compact {
  background: #10b981 !important;
  border: 1px solid #10b981 !important;
  border-radius: 8px !important;
  padding: 0.75rem 1rem !important;
  color: white !important;
  font-size: 0.875rem !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
}

.pdf-btn-compact:hover {
  background: #059669 !important;
  border-color: #059669 !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
}

.display-toggle-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #ffffff;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  color: #374151;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.display-toggle-btn:hover {
  border-color: #3b82f6;
  background: #eff6ff;
  color: #1d4ed8;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.display-toggle-btn.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: #ffffff;
}

.toggle-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggle-text {
  font-size: 0.875rem;
  font-weight: 600;
}

.course-header {
  margin-bottom: 40px;
  text-align: center;
}

.course-description {
  font-size: 1.1rem;
  color: #666;
  line-height: 1.6;
}

.course-body {
  background: #f8fafc;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
}

.coming-soon {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.coming-soon-icon {
  font-size: 4rem;
  margin-bottom: 10px;
}

.coming-soon h3 {
  font-size: 1.5rem;
  color: #193e8e;
  margin: 0;
}

.coming-soon p {
  font-size: 1rem;
  color: #666;
  margin: 0;
  line-height: 1.6;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  text-align: center;
  margin-top: 60px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f4f6;
  border-top: 4px solid #193e8e;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Styles pour les cours */
.cours-list {
  text-align: left;
}

.cours-item {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: visible;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.cours-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.cours-title {
  font-size: 1.5rem;
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
  margin-bottom: 1.5rem;
  line-height: 1.6;
  font-size: 1.1rem;
}

.cours-content {
  margin-bottom: 2rem;
  line-height: 1.8;
  color: #333;
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
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
  max-width: 100%;
}

.cours-content :deep(p) {
  margin-bottom: 1rem;
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
  max-width: 100%;
}

.cours-content :deep(ul),
.cours-content :deep(ol) {
  margin-bottom: 1rem;
  padding-left: 2rem;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.cours-content :deep(li) {
  margin-bottom: 0.5rem;
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
}

.cours-content :deep(.content-image-container) {
  margin: 1rem 0;
  text-align: center;
}

.cours-content :deep(.content-image) {
  display: block;
  margin: 0 auto;
  max-width: 100%;
  max-height: 80vh;
  width: auto;
  height: auto;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.cours-content :deep(.content-image:hover) {
  transform: scale(1.02);
}

.cours-content :deep(.image-legende) {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #666;
  font-style: italic;
  text-align: center;
}

.cours-images {
  margin: 2rem 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.cours-image {
  text-align: center;
}

.cours-image img {
  max-width: 100%;
  max-height: 85vh;
  width: auto;
  height: auto;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.image-legende {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #666;
  font-style: italic;
}

.cours-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
  color: #999;
  border-top: 1px solid #eee;
  padding-top: 1rem;
  margin-top: 1rem;
}

.cours-date {
  font-style: italic;
}

@media (max-width: 768px) {
  .cours-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .cours-title {
    font-size: 1.25rem;
  }
  
  .cours-images {
    grid-template-columns: 1fr;
  }

  /* Sur petits écrans, éviter que l'image dépasse la hauteur visible */
  .cours-image img,
  .cours-content :deep(.content-image) {
    max-height: 60vh;
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

/* MathJax responsive */
@media (max-width: 768px) {
  .cours-content :deep(.MathJax_Display) {
    font-size: 0.9em !important;
    overflow-x: auto !important;
  }
  
  .cours-content :deep(.MathJax_SVG_Display) {
    font-size: 0.9em !important;
    overflow-x: auto !important;
  }
  
  .cours-content :deep(.MathJax_SVG) {
    font-size: 0.9em !important;
  }
}

@media (max-width: 480px) {
  .cours-content :deep(.MathJax_Display) {
    font-size: 0.8em !important;
  }
  
  .cours-content :deep(.MathJax_SVG_Display) {
    font-size: 0.8em !important;
  }
  
  .cours-content :deep(.MathJax_SVG) {
    font-size: 0.8em !important;
  }
}

@media (max-width: 640px) {
  .course-chapitre-title {
    font-size: 1.5rem;
    margin-bottom: 20px;
  }
  
  .course-body {
    padding: 30px 20px;
  }
  
  .coming-soon-icon {
    font-size: 3rem;
  }
  
  .coming-soon h3 {
    font-size: 1.3rem;
  }
  
  .course-chapitre-section {
    padding: 0 4vw 30px 4vw;
  }
  
  .display-toggle-container {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .display-toggle-btn {
    padding: 0.625rem 1.25rem;
    font-size: 0.875rem;
  }
  
  .pdf-btn-compact {
    padding: 0.625rem 1rem !important;
    font-size: 0.8rem !important;
  }
  
  .course-content.wide-display {
    max-width: 100%;
  }
}
</style> 