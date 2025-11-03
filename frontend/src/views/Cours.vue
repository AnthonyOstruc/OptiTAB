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

        <!-- Résultats de recherche pilotés par la barre latérale -->
        <div class="page-search">
          <div v-if="searchQuery && filteredResults.length === 0" class="no-results">Aucun résultat pour « {{ searchQuery }} »</div>
          <div v-else-if="searchQuery && filteredResults.length > 0" class="results-info">{{ filteredResults.length }} résultat(s)</div>
          <ul v-if="searchQuery && filteredResults.length > 0" class="results-list">
            <li v-for="(r, i) in filteredResults" :key="i" class="result-item">
              <a href="#" @click.prevent="scrollToSection(r.anchor)">
                <span class="result-type">{{ r.typeLabel }}</span>
                <span class="result-text" v-html="highlightText(r.snippet)"></span>
              </a>
            </li>
          </ul>
        </div>

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
                  <span v-html="highlightText(item.text)"></span>
                </a>
              </li>
            </ul>
          </transition>
        </nav>

        <div class="cours-content-outer" :style="zoomStyle">
          <div class="cours-content" ref="coursContentRef" v-html="renderedContent"></div>
        </div>
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
      
      <div v-else-if="cours.length === 0" class="empty-coming">
        <div class="empty-card">
          <div class="empty-icon">📗</div>
          <h2 class="empty-title">Cours — bientôt disponible</h2>
          <p class="empty-text">
            Ce cours n'est pas encore publié pour cette notion. Il arrive très prochainement.
          </p>
          <div class="empty-actions">
            <button class="empty-btn" @click="goBackToNotions">Retour aux chapitres</button>
          </div>
        </div>
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
const viewportWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1920)

// Recherche dans la page
const searchQuery = ref('')
const searchIndex = ref([])

function normalize(str) {
  return (str || '').toString().normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase()
}

function escapeHtml(s) {
  return (s || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
}

function highlightText(text) {
  const q = normalize(searchQuery.value)
  if (!q) return escapeHtml(text)
  const source = text || ''
  const idx = normalize(source).indexOf(q)
  if (idx === -1) return escapeHtml(source)
  const before = escapeHtml(source.slice(0, idx))
  const match = escapeHtml(source.slice(idx, idx + q.length))
  const after = escapeHtml(source.slice(idx + q.length))
  return `${before}<mark class="hl">${match}</mark>${after}`
}

function buildSearchIndex() {
  const list = []
  const root = coursContentRef.value
  if (!root) { searchIndex.value = list; return }
  let currentAnchor = null
  let currentTitle = ''
  const nodes = root.querySelectorAll('h2, h3, p, li')
  nodes.forEach((el) => {
    const tag = el.tagName.toLowerCase()
    const text = (el.textContent || '').trim()
    if (!text) return
    if (tag === 'h2' || tag === 'h3') {
      currentAnchor = el.id || ''
      currentTitle = text
      list.push({ type: tag, typeLabel: tag.toUpperCase(), text, anchor: currentAnchor, snippet: text })
    } else {
      if (!currentAnchor) return
      // Créer un petit extrait autour du terme si possible (100 chars)
      list.push({ type: 'p', typeLabel: '§', text, anchor: currentAnchor, snippet: text })
    }
  })
  searchIndex.value = list
}

function updateHeadingMatches() {
  const root = coursContentRef.value
  if (!root) return
  const q = normalize(searchQuery.value)
  const heads = root.querySelectorAll('h2, h3')
  heads.forEach(h => {
    const txt = (h.textContent || '')
    const match = q && normalize(txt).includes(q)
    if (match) h.classList.add('search-hit')
    else h.classList.remove('search-hit')
  })
}

const filteredResults = computed(() => {
  const q = normalize(searchQuery.value)
  if (!q) return []
  return searchIndex.value.filter(e => normalize(e.text).includes(q)).slice(0, 50)
})

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
  updateViewportWidth()
  if (typeof window !== 'undefined') {
    window.addEventListener('resize', updateViewportWidth, { passive: true })
  }
  // Restaurer la requête depuis l'URL
  if (route.query?.q) {
    try { searchQuery.value = String(route.query.q) } catch {}
  }
  await loadCoursData()
})

// Hook onActivated - appelé quand le composant est réactivé depuis le cache KeepAlive
onActivated(() => {
  // Forcer le rendu MathJax à chaque réactivation pour éviter les problèmes de cache
  nextTick(() => {
    scheduleFormulaWrapRetry()
    renderMath()
    // S'assurer que le rendu est bien appliqué avec un second appel après un délai
    setTimeout(() => {
      scheduleFormulaWrapRetry()
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
      scheduleFormulaWrapRetry()
      renderMath()
      setTimeout(() => {
        scheduleFormulaWrapRetry()
        extractTableOfContents()
        buildSearchIndex()
        updateHeadingMatches()
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

function computeAutoZoom(width) {
  if (width >= 1400) return 1
  if (width >= 1200) return 0.95
  if (width >= 1024) return 0.9
  if (width >= 900) return 0.85
  if (width >= 768) return 0.8
  if (width >= 640) return 0.78
  if (width >= 520) return 0.76
  if (width >= 420) return 0.74
  return 0.72
}

const zoomLevel = computed(() => computeAutoZoom(viewportWidth.value))

const zoomStyle = computed(() => {
  const z = zoomLevel.value || 1
  const widthPercent = (100 / z).toFixed(3)
  return {
    '--course-zoom': z,
    transform: `scale(${z})`,
    transformOrigin: 'top left',
    width: `${widthPercent}%`
  }
})

function updateViewportWidth() {
  if (typeof window === 'undefined') return
  viewportWidth.value = window.innerWidth
}

function scheduleFormulaWrapRetry(attempt = 0) {
  const MAX_ATTEMPTS = 8
  if (!coursContentRef.value) return
  const hasScrollableContent = coursContentRef.value.querySelector('mjx-container, .MathJax_Display, .MathJax_SVG_Display, table')
  if (hasScrollableContent) {
    prepareScrollableContent()
    return
  }
  if (attempt < MAX_ATTEMPTS) {
    setTimeout(() => scheduleFormulaWrapRetry(attempt + 1), 120)
  }
}

function prepareScrollableContent() {
  const root = coursContentRef.value
  if (!root) return

  const wrapForScroll = (nodes, { wrapperTag = 'div', wrapperAttr, targetAttr, scrollType }) => {
    Array.from(nodes).forEach((node) => {
      node.setAttribute(targetAttr, 'true')

      const specificWrapper = node.closest(`[${wrapperAttr}]`)
      if (specificWrapper) {
        if (scrollType) {
          specificWrapper.setAttribute('data-scroll-type', scrollType)
        }
        return
      }

      const genericWrapper = node.closest('[data-horizontal-scroll-wrapper]')
      if (genericWrapper) {
        return
      }

      const wrapper = document.createElement(wrapperTag)
      wrapper.setAttribute('data-horizontal-scroll-wrapper', 'true')
      wrapper.setAttribute(wrapperAttr, 'true')
      if (scrollType) {
        wrapper.setAttribute('data-scroll-type', scrollType)
      }
      if (node.parentNode) {
        node.parentNode.insertBefore(wrapper, node)
        wrapper.appendChild(node)
      }
    })
  }

  const getOutermostNodes = (nodeList) => {
    const list = Array.from(nodeList)
    return list.filter((node) => !list.some((other) => other !== node && other.contains(node)))
  }

  wrapForScroll(root.querySelectorAll('table'), {
    wrapperAttr: 'data-table-scroll-wrapper',
    targetAttr: 'data-table-scroll-target',
    scrollType: 'table',
    wrapperTag: 'div'
  })

  const formulaNodes = getOutermostNodes(root.querySelectorAll('mjx-container[display="true"], .MathJax_Display, .MathJax_SVG_Display'))
  wrapForScroll(formulaNodes, {
    wrapperAttr: 'data-formula-scroll-wrapper',
    targetAttr: 'data-formula-scroll-target',
    scrollType: 'formula',
    wrapperTag: 'div'
  })

  const inlineFormulaNodes = getOutermostNodes(root.querySelectorAll('mjx-container:not([display="true"])'))
  wrapForScroll(inlineFormulaNodes, {
    wrapperAttr: 'data-formula-inline-scroll-wrapper',
    targetAttr: 'data-formula-inline-scroll-target',
    scrollType: 'formula-inline',
    wrapperTag: 'span'
  })

  const formulaTargets = root.querySelectorAll('[data-formula-inline-scroll-target], [data-formula-scroll-target]')
  formulaTargets.forEach((target) => {
    const blockParent = target.closest('p, li, div, section, article, blockquote, pre')
    if (blockParent) {
      blockParent.setAttribute('data-formula-line-block', 'true')
    }
  })
}

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
      buildSearchIndex()
      updateHeadingMatches()
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
      scheduleFormulaWrapRetry()
      renderMath()
      // Attendre que le DOM soit vraiment mis à jour
      setTimeout(() => {
        scheduleFormulaWrapRetry()
        extractTableOfContents()
        buildSearchIndex()
        updateHeadingMatches()
        setupTocObserver()
        // Réinitialiser l'écouteur de scroll pour le nouveau cours
        if (scrollCleanup) scrollCleanup()
        setupScrollListener()
      }, 100)
    })
  }
}, { deep: true })

watch(renderedContent, () => {
  nextTick(() => {
    scheduleFormulaWrapRetry()
  })
})

watch(zoomLevel, () => {
  nextTick(() => {
    scheduleFormulaWrapRetry()
    if (typeof window !== 'undefined' && window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise().catch(() => {})
    }
  })
}, { immediate: true })

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
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', updateViewportWidth)
  }
  // Sauvegarder l'état courant (cours sélectionné + scroll)
  saveCoursViewState()
})

// Garder la requête dans l'URL pour partage/retour
// Mettre à jour l'URL seulement si nécessaire
watch(searchQuery, (val) => {
  const q = (val || '').trim()
  const currentQ = route.query?.q ? String(route.query.q) : ''
  if (q !== currentQ) {
    const newQuery = { ...route.query }
    if (q) newQuery.q = q
    else delete newQuery.q
    router.replace({ query: newQuery }).catch(() => {})
  }
  updateHeadingMatches()
})

// Suivre la recherche globale depuis la sidebar (URL -> searchQuery)
watch(() => route.query.q, (val) => {
  const incoming = val ? String(val) : ''
  if (incoming !== (searchQuery.value || '')) {
    searchQuery.value = incoming
    updateHeadingMatches()
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
    /* Harmoniser avec la page Synthèse: même espace sous le titre */
    margin-bottom: 0.5rem;
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

/* Pleine largeur sur mobile (utiliser tout l'espace) */
@media (max-width: 768px) {
  .cours-section {
    padding-left: 0;
    padding-right: 0;
    margin-left: -1rem;   /* compense le padding du layout */
    margin-right: -1rem;
    width: calc(100% + 2rem);
  }
}

@media (max-width: 480px) {
  .cours-section {
    margin-left: -0.75rem;
    margin-right: -0.75rem;
    width: calc(100% + 1.5rem);
  }
}

/* Styles pour le contenu du cours */
.cours-content {
  text-align: left;
  max-width: 100%;
  overflow-x: visible;
  overflow-wrap: break-word;
  word-wrap: break-word;
  hyphens: auto;
  line-height: 1.6;
  color: #333;
  /* Réduire le padding global pour limiter les grands espaces verticaux */
  padding: 1rem 0;
  background: transparent;
}

.cours-content-outer {
  width: 100%;
  transform-origin: top left;
  transition: transform 0.2s ease;
}

/* Recherche dans la page */
.page-search { text-align: left; margin: 0.5rem 0; }
.page-search:empty { margin: 0; }
.page-search-inner { display:flex; align-items:center; gap:.5rem; border:1px solid #e5e7eb; border-radius:8px; padding:.5rem .75rem; background:#fff; }
.page-search .search-icon { color:#9ca3af; }
.page-search-input { flex:1; border:none; outline:none; font-size:.95rem; background:transparent; color:#111827; }
.no-results { color:#6b7280; margin-top:.5rem; }
.results-info { color:#6b7280; margin-top:.5rem; font-size:.9rem; }
.results-list { list-style:none; padding:0; margin:.5rem 0 0 0; display:flex; flex-direction:column; gap:.25rem; }
.result-item a { display:flex; gap:.5rem; align-items:flex-start; text-decoration:none; color:#1f2937; padding:.35rem .25rem; border-radius:6px; }
.result-item a:hover { background:#f9fafb; }
.result-type { font-size:.75rem; color:#6b7280; background:#f3f4f6; border-radius:4px; padding:.1rem .35rem; }
.result-text { font-size:.9rem; }
.hl { background: #fff3b0; padding: 0 .1rem; border-radius: 2px; }

/* Mise en évidence des titres correspondants */
.cours-content :deep(h2.search-hit),
.cours-content :deep(h3.search-hit) {
  background: #fffbeb;
  box-shadow: inset 0 -2px 0 #fde68a;
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
  padding: 0.6rem 1rem; /* compact height */
  margin: 1rem 0;      /* moins d'espace vertical */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  text-align: left;
}

/* Remonter un peu le sommaire dans les cours */
.cours-section .toc-container { margin: 0.5rem 0; }

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
    padding: 0.5rem 0.75rem; /* encore plus compact sur mobile */
    margin: 0.75rem 0;
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
  /* Au-dessus de la bottom-nav mobile */
  z-index: 12010;
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

.empty-coming {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
}

.empty-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 8px 24px rgba(2, 6, 23, 0.06);
  max-width: 720px;
}

.empty-icon {
  font-size: 2.2rem;
  margin-bottom: 0.25rem;
}

.empty-title {
  margin: 0 0 0.5rem;
  color: #0f172a;
  font-size: 1.35rem;
}

.empty-text {
  color: #475569;
  margin: 0;
}

.empty-actions {
  margin-top: 1rem;
}

.empty-btn {
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 0.6rem 1rem;
  font-weight: 700;
  cursor: pointer;
}

.empty-btn:hover {
  filter: brightness(1.05);
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
    /* Placer le bouton au-dessus de la barre de navigation mobile */
    bottom: calc(env(safe-area-inset-bottom) + 4.75rem);
    left: 1.25rem;
    width: 45px;
    height: 45px;
  }
}

@media (max-width: 480px) {
  .scroll-top-btn {
    /* Encore un peu plus haut sur très petits écrans */
    bottom: calc(env(safe-area-inset-bottom) + 4.25rem);
    left: 1rem;
    width: 42px;
    height: 42px;
  }

  .scroll-top-btn svg {
    width: 20px;
    height: 20px;
  }
}
</style>
