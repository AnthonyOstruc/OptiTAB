<template>
  <DashboardLayout>
    <section class="cours-section">
      <!-- Bouton de retour -->
      <BackButton 
        text="Retour aux chapitres" 
        :customAction="goBackToNotions"
        position="top-left"
      />
      
      <div v-if="loading" class="loading-container">
        <SkeletonList :count="3" />
      </div>
      
      <div v-else-if="selectedCours" class="cours-container">
        <header class="cours-header">
          <h1 class="cours-title">{{ selectedCours.titre }}</h1>
          <template v-if="selectedCours.pdf_url">
            <a :href="selectedCours.pdf_url" class="btn-pdf" :download="`${selectedCours.titre}.pdf`">Télécharger PDF</a>
          </template>
          <p v-if="selectedCours.description" class="cours-description">
            {{ selectedCours.description }}
          </p>
        </header>

        <!-- Sommaire -->
        <nav v-if="tableOfContents.length > 0" class="toc-container">
          <div class="toc-header" @click="isTocExpanded = !isTocExpanded">
            <div class="toc-header-content">
              <svg class="toc-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="8" y1="6" x2="21" y2="6"/>
                <line x1="8" y1="12" x2="21" y2="12"/>
                <line x1="8" y1="18" x2="21" y2="18"/>
                <line x1="3" y1="6" x2="3.01" y2="6"/>
                <line x1="3" y1="12" x2="3.01" y2="12"/>
                <line x1="3" y1="18" x2="3.01" y2="18"/>
              </svg>
              <h3 class="toc-title">Sommaire</h3>
            </div>
            <svg 
              class="toc-toggle-icon" 
              :class="{ 'expanded': isTocExpanded }"
              width="20" 
              height="20" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              stroke-width="2"
            >
              <polyline points="6 9 12 15 18 9"/>
            </svg>
          </div>
          <transition name="toc-expand">
            <ul v-show="isTocExpanded" class="toc-list">
              <li 
                v-for="(item, index) in tableOfContents" 
                :key="index"
                :class="['toc-item', `toc-level-${item.level}`]"
              >
                <a 
                  class="toc-link"
                  :href="`#${item.id}`"
                  @click.prevent="scrollToSection(item.id)"
                >
                  {{ item.text }}
                </a>
              </li>
            </ul>
          </transition>
        </nav>

        <div class="cours-content" ref="coursContentRef" v-html="renderedContent"></div>
        <div v-if="selectedCours.video_url" class="cours-video">
          <h3>Vidéo explicative</h3>
          <div class="video-container">
            <iframe :src="selectedCours.video_url" title="Vidéo du cours" frameborder="0" allowfullscreen></iframe>
          </div>
        </div>

        <!-- Bouton retour en haut -->
        <transition name="scroll-top-fade">
          <button
            v-show="showScrollTopButton"
            class="scroll-top-btn"
            @click="scrollToTop"
            aria-label="Retour en haut"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="18 15 12 9 6 15"/>
            </svg>
          </button>
        </transition>
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
import { defineOptions } from 'vue'
// Nom explicite pour KeepAlive
defineOptions({ name: 'CourseByNotion' })
import { ref, onMounted, onActivated, onBeforeUnmount, computed, nextTick, watch } from 'vue'
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
const coursContentRef = ref(null)
const tableOfContents = ref([])
const isTocExpanded = ref(false)
const showScrollTopButton = ref(false)
let tocObserver = null
let tocDebounce = null
let scrollCleanup = null

// --- Persistence (sessionStorage) for keeping place between tabs ---
const pageStorageKey = computed(() => {
  const notionId = route.params.notionId
  return notionId ? `optitab_page_cours_${notionId}` : 'optitab_page_cours_generic'
})

function saveCoursViewState(extra = {}) {
  try {
    const state = {
      selectedCoursId: selectedCours.value?.id ?? null,
      scrollY: typeof window !== 'undefined' ? (window.scrollY || window.pageYOffset || 0) : 0,
      t: Date.now(),
      ...extra
    }
    sessionStorage.setItem(pageStorageKey.value, JSON.stringify(state))
  } catch (_) {}
}

function restoreCoursViewState() {
  try {
    const raw = sessionStorage.getItem(pageStorageKey.value)
    if (!raw) return null
    const s = JSON.parse(raw)
    return s && typeof s === 'object' ? s : null
  } catch (_) {
    return null
  }
}

// Récupérer les paramètres de la route
const currentMatiereId = computed(() => {
  return subjectsStore.activeMatiereId || route.params.matiereId
})

const currentNotionId = computed(() => route.params.notionId)
const currentChapitreId = computed(() => route.params.chapitreId)

// Fonction pour revenir aux chapitres
function goBackToNotions() {
  // Rediriger vers course-notions/id (liste des notions de cours)
  const matiereId = currentMatiereId.value
  if (matiereId) {
    router.push({ 
      name: 'CourseNotions', 
      params: { 
        matiereId: matiereId
      } 
    })
  } else {
    router.back()
  }
}

// Fonction pour afficher un cours
function viewCours(coursItem) {
  selectedCours.value = coursItem
  // Sauvegarder l'élément sélectionné pour reprise ultérieure
  saveCoursViewState()
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
  await loadCoursData()
})

// Hook onActivated - appelé quand le composant est réactivé depuis le cache KeepAlive
onActivated(() => {
  // Forcer le rendu MathJax à chaque réactivation pour éviter les problèmes de cache
  nextTick(() => {
    renderMath()
    // S'assurer que le rendu est bien appliqué avec un second appel après un délai
    setTimeout(() => {
      renderMath()
    }, 100)
  })
})

// Fonction de chargement (réutilisable au changement de notion)
async function loadCoursData() {
  try {
    loading.value = true
    tableOfContents.value = []
    selectedCours.value = null
    cours.value = []
    if (tocObserver) { try { tocObserver.disconnect() } catch (_) {} }
    
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

    // Restaurer l'état sauvegardé (cours sélectionné)
    const saved = restoreCoursViewState()
    if (saved && saved.selectedCoursId) {
      const found = cours.value.find(c => c.id === saved.selectedCoursId)
      if (found) selectedCours.value = found
    }

    // Rendre le contenu MathJax après le chargement
    nextTick(() => {
      renderMath()
      setTimeout(() => {
        extractTableOfContents()
        setupTocObserver()
        setupScrollListener()
        // Restaurer la position de scroll si disponible
        const s = restoreCoursViewState()
        if (s && typeof s.scrollY === 'number') {
          try { window.scrollTo({ top: s.scrollY, behavior: 'auto' }) } catch {}
        }
      }, 150)
    })
  } catch (error) {
    console.error('Erreur lors du chargement des cours:', error)
    cours.value = []
  } finally {
    loading.value = false
  }
}

// Recharger quand l'ID de notion change (navigation vers un nouveau chapitre/notion)
watch(() => route.params.notionId, async (newId, oldId) => {
  if (newId && newId !== oldId) {
    await loadCoursData()
  }
})

const renderedContent = computed(() => {
  if (!selectedCours.value?.contenu) return ''

  const content = selectedCours.value.contenu
  const images = selectedCours.value.images || []

  // Déléguer entièrement l'injection des images au renderer pour éviter que
  // le Markdown n'insère des balises <p> au milieu des balises <img>.
  return renderContentWithImages(content, images)
})

// Extraire la table des matières depuis le contenu HTML
function extractTableOfContents() {
  tableOfContents.value = []
  
  if (!coursContentRef.value) return
  
  const headings = coursContentRef.value.querySelectorAll('h2, h3')
  
  headings.forEach((heading, index) => {
    const level = parseInt(heading.tagName.substring(1)) // h2 -> 2, h3 -> 3
    const text = heading.textContent.trim()
    
    // Ignorer les titres vides ou trop courts
    if (!text || text.length < 2) return
    
    const id = `toc-section-${index}`
    
    // Ajouter l'ID à l'élément pour le scroll
    heading.id = id
    
    tableOfContents.value.push({
      id,
      text,
      level
    })
  })
}

// Observer pour ré-extraire le sommaire quand le DOM du contenu change
function setupTocObserver() {
  if (!coursContentRef.value || typeof MutationObserver === 'undefined') return
  if (tocObserver) {
    try { tocObserver.disconnect() } catch (e) {}
  }
  tocObserver = new MutationObserver(() => {
    if (tocDebounce) clearTimeout(tocDebounce)
    tocDebounce = setTimeout(() => {
      extractTableOfContents()
    }, 200)
  })
  tocObserver.observe(coursContentRef.value, {
    childList: true,
    subtree: true
  })
}

// Fonction pour scroller vers une section
function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId)
  if (!element) return

  const container = getScrollContainer(coursContentRef.value)
  const offset = 100 // Offset pour header fixe

  if (container && container !== document.body && container !== document.documentElement) {
    const rect = element.getBoundingClientRect()
    const containerRect = container.getBoundingClientRect()
    const targetTop = container.scrollTop + (rect.top - containerRect.top) - offset
    container.scrollTo({ top: targetTop, behavior: 'smooth' })
  } else {
    const currentScroll = window.pageYOffset || document.documentElement.scrollTop || 0
    const elementPosition = element.getBoundingClientRect().top + currentScroll
    const offsetPosition = elementPosition - offset
    window.scrollTo({ top: offsetPosition, behavior: 'smooth' })
  }
}

// Trouver le conteneur scrollable le plus proche
function getScrollContainer(el) {
  let parent = el ? el.parentElement : null
  while (parent) {
    const style = window.getComputedStyle(parent)
    const overflowY = style.overflowY
    const canScroll = (overflowY === 'auto' || overflowY === 'scroll') && parent.scrollHeight > parent.clientHeight
    if (canScroll) return parent
    parent = parent.parentElement
  }
  return document.scrollingElement || document.documentElement
}

// Gérer l'apparition du bouton retour en haut
function setupScrollListener() {
  const container = getScrollContainer(coursContentRef.value)

  const handleScroll = () => {
    const scrollTop = container === document.documentElement || container === document.body
      ? window.pageYOffset || document.documentElement.scrollTop
      : container.scrollTop

    showScrollTopButton.value = scrollTop > 300
    // Persister la position de scroll pour une reprise fluide entre onglets
    saveCoursViewState({ scrollY: scrollTop })
  }

  if (container === document.documentElement || container === document.body) {
    window.addEventListener('scroll', handleScroll, { passive: true })
  } else {
    container.addEventListener('scroll', handleScroll, { passive: true })
  }

  // Nettoyer l'écouteur au démontage
  scrollCleanup = () => {
    if (container === document.documentElement || container === document.body) {
      window.removeEventListener('scroll', handleScroll)
    } else {
      container.removeEventListener('scroll', handleScroll)
    }
  }
}

// Fonction pour remonter en haut
function scrollToTop() {
  const container = getScrollContainer(coursContentRef.value)

  if (container === document.documentElement || container === document.body) {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } else {
    container.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

// Relancer renderMath() et extraire le sommaire quand le contenu change
watch(selectedCours, () => {
  if (selectedCours.value) {
    nextTick(() => {
      renderMath()
      // Attendre que le DOM soit vraiment mis à jour
      setTimeout(() => {
        extractTableOfContents()
        setupTocObserver()
        // Réinitialiser l'écouteur de scroll pour le nouveau cours
        if (scrollCleanup) scrollCleanup()
        setupScrollListener()
      }, 100)
    })
  }
}, { deep: true })

onBeforeUnmount(() => {
  if (tocObserver) {
    try { tocObserver.disconnect() } catch (e) {}
  }
  if (tocDebounce) {
    try { clearTimeout(tocDebounce) } catch (e) {}
  }
  if (scrollCleanup) {
    try { scrollCleanup() } catch (e) {}
  }
  // Sauvegarder l'état courant (cours sélectionné + scroll)
  saveCoursViewState()
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
  margin: 0.25rem 0 0.5rem;
  font-weight: 800;
  text-align: center;
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
  text-align: center;
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
  margin: 1rem auto;
}

.btn-pdf:hover {
  background: #b91c1c;
}

.cours-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
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
  /* Réduire le padding global pour limiter les grands espaces verticaux */
  padding: 1rem 0;
  background: transparent;
}

/* Styles pour les titres dans le contenu */
.cours-content :deep(h1),
.cours-content :deep(h2),
.cours-content :deep(h3),
.cours-content :deep(h4),
.cours-content :deep(h5),
.cours-content :deep(h6) {
  color: #193e8e;
  /* Réduire l'espace vertical autour des titres pour éviter les grands blancs */
  margin-top: 0.25rem !important;
  margin-bottom: 0.5rem !important;
}

.cours-content :deep(p) { margin-top: 0; margin-bottom: 0.5rem; }

/* Limiter l'espace quand un titre suit un bloc */
.cours-content :deep(div) + :deep(h1),
.cours-content :deep(div) + :deep(h2),
.cours-content :deep(div) + :deep(h3),
.cours-content :deep(div) + :deep(h4),
.cours-content :deep(div) + :deep(h5),
.cours-content :deep(div) + :deep(h6) {
  margin-top: 0.4rem !important;
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

/* Styles du sommaire */
.toc-container {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1rem 1.5rem;
  margin: 2rem 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  text-align: left;
}

.toc-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0;
  border-bottom: none;
  cursor: pointer;
  user-select: none;
  transition: all 0.2s ease;
}

.toc-header:hover {
  opacity: 0.8;
}

.toc-header-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.toc-icon {
  color: #193e8e;
  flex-shrink: 0;
}

.toc-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #193e8e;
  margin: 0;
  letter-spacing: 0.025em;
}

.toc-toggle-icon {
  color: #193e8e;
  transition: transform 0.3s ease;
  flex-shrink: 0;
}

.toc-toggle-icon.expanded {
  transform: rotate(180deg);
}

.toc-list {
  list-style: none;
  padding: 0;
  margin: 0;
  padding-top: 1rem;
  border-top: 2px solid #cbd5e1;
  margin-top: 1rem;
}

.toc-item {
  margin: 0;
}

.toc-level-2 {
  margin-top: 0.5rem;
}

.toc-level-3 {
  margin-left: 1.5rem;
  margin-top: 0.25rem;
}

.toc-link {
  display: block;
  width: 100%;
  text-align: left;
  padding: 0.625rem 0.875rem;
  color: #334155;
  background: transparent;
  border: none;
  border-radius: 6px;
  transition: all 0.2s ease;
  font-size: 0.95rem;
  line-height: 1.5;
  cursor: pointer;
  word-wrap: break-word;
  overflow-wrap: break-word;
  font-family: inherit;
}

.toc-link:hover {
  background: #ffffff;
  color: #193e8e;
  transform: translateX(4px);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.toc-level-2 .toc-link {
  font-weight: 600;
  font-size: 1rem;
}

.toc-level-3 .toc-link {
  font-weight: 400;
  font-size: 0.9rem;
  color: #64748b;
}

.toc-level-3 .toc-link:hover {
  color: #193e8e;
}

/* Transition pour l'expansion/réduction */
.toc-expand-enter-active,
.toc-expand-leave-active {
  transition: all 0.3s ease;
  max-height: 1000px;
  overflow: hidden;
}

.toc-expand-enter-from,
.toc-expand-leave-to {
  max-height: 0;
  opacity: 0;
}

@media (max-width: 640px) {
  .toc-container {
    padding: 1rem;
    margin: 1.5rem 0;
  }

  .toc-header {
    margin-bottom: 0.75rem;
  }

  .toc-title {
    font-size: 1rem;
  }

  .toc-level-3 {
    margin-left: 1rem;
  }

  .toc-link {
    font-size: 0.875rem;
    padding: 0.4rem 0.5rem;
  }

  .toc-level-2 .toc-link {
    font-size: 0.95rem;
  }

  .toc-level-3 .toc-link {
    font-size: 0.85rem;
  }
}

/* Bouton retour en haut */
.scroll-top-btn {
  position: fixed;
  bottom: 2rem;
  left: 2rem;
  width: 50px;
  height: 50px;
  background: #193e8e;
  color: white;
  border: none;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(25, 62, 142, 0.3);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  transition: all 0.3s ease;
}

.scroll-top-btn:hover {
  background: #0f2866;
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(25, 62, 142, 0.4);
}

.scroll-top-btn:active {
  transform: translateY(-1px);
}

.scroll-top-btn svg {
  width: 24px;
  height: 24px;
}

/* Animation de transition pour le bouton */
.scroll-top-fade-enter-active,
.scroll-top-fade-leave-active {
  transition: all 0.3s ease;
}

.scroll-top-fade-enter-from,
.scroll-top-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

@media (max-width: 768px) {
  .scroll-top-btn {
    bottom: 1.5rem;
    left: 1.5rem;
    width: 45px;
    height: 45px;
  }
}

@media (max-width: 480px) {
  .scroll-top-btn {
    bottom: 1rem;
    left: 1rem;
    width: 40px;
    height: 40px;
  }

  .scroll-top-btn svg {
    width: 20px;
    height: 20px;
  }
}
</style> 
