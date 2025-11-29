<template>
  <DashboardLayout>
    <div class="sheet-by-notion-page">
      <div class="nav-header-base">
        <BackButton text="Retour aux chapitres" :customAction="goBack" position="top-left-dashboard" />
      </div>

      <div class="sheet-content-wrapper" :class="{ 'sheet-loading': loading }">
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>Chargement...</p>
        </div>

        <div v-else>
          <div v-if="!sheet" class="empty-coming">
            <div class="empty-card">
            <div class="empty-icon">📘</div>
            <h2 class="empty-title">Fiche de synthèse — bientôt disponible</h2>
            <p class="empty-text">
              Cette fiche n'est pas encore publiée pour cette notion. Elle arrive très prochainement.
            </p>
            <div class="empty-actions">
              <button class="empty-btn" @click="goBack">Retour aux chapitres</button>
            </div>
          </div>
          </div>
          <div v-else class="sheet-container">
          <header class="sheet-header">
            <h1 class="sheet-title">{{ sheet.titre }}</h1>
          </header>

          <!-- Résultats de recherche (pilotés par la barre latérale) -->
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

          <div class="sheet-content-outer" :style="zoomStyle">
            <div class="sheet-content" ref="sheetContentRef" v-html="rendered"></div>
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
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted, onActivated, onBeforeUnmount, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import BackButton from '@/components/common/BackButton.vue'
import { getSynthesisSheets, getSynthesisSheet } from '@/api/synthesis'
import { useSubjectsStore } from '@/stores/subjects/index'
import { renderContentWithImages } from '@/utils/scientificRenderer'
import { useZoom } from '@/composables/useZoom'

const route = useRoute()
const router = useRouter()
const subjectsStore = useSubjectsStore()

defineOptions({ name: 'SynthesisByNotion' })

const notionId = computed(() => Number(route.params.notionId))
const loading = ref(true)
const sheet = ref(null)
const sheetContentRef = ref(null)
const tableOfContents = ref([])
const isTocExpanded = ref(false)
const showScrollTopButton = ref(false)
let tocObserver = null
let tocDebounce = null
let scrollCleanup = null

// Utiliser le composable de zoom
const {
  viewportWidth,
  contentHeight,
  detectMobileAndZoomSupport,
  createZoomStyle,
  updateViewportWidth,
  measureContentHeight,
  setupViewportListener,
  cleanupViewportListener
} = useZoom()

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
  const root = sheetContentRef.value
  if (!root) { searchIndex.value = list; return }
  let currentAnchor = null
  const nodes = root.querySelectorAll('h2, h3, p, li')
  nodes.forEach((el) => {
    const tag = el.tagName.toLowerCase()
    const text = (el.textContent || '').trim()
    if (!text) return
    if (tag === 'h2' || tag === 'h3') {
      currentAnchor = el.id || ''
      list.push({ type: tag, typeLabel: tag.toUpperCase(), text, anchor: currentAnchor, snippet: text })
    } else {
      if (!currentAnchor) return
      list.push({ type: 'p', typeLabel: '§', text, anchor: currentAnchor, snippet: text })
    }
  })
  searchIndex.value = list
}

function updateHeadingMatches() {
  const root = sheetContentRef.value
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

// Simple cache en mémoire pour accélérer les retours sur la même notion
const sheetCache = typeof window !== 'undefined' ? (window.__sheetCache ||= new Map()) : new Map()

const rendered = computed(() => {
  const html = (sheet.value?.summary || '')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
  const images = sheet.value?.images || []
  return renderContentWithImages(html, images)
})

const zoomStyle = createZoomStyle({
  cssVar: '--sheet-zoom',
  heightVar: '--sheet-content-height',
  mobileZoomAdjustment: (z) => Math.max(0.45, z * 0.75)
})

function measureContentHeightForSheets() {
  measureContentHeight(sheetContentRef)
}

function prepareTablesForScroll() {
  const root = sheetContentRef.value
  if (!root) return

  root.querySelectorAll('[data-table-scroll-wrapper]').forEach((wrapper) => {
    const parent = wrapper.parentElement
    if (!parent) return
    while (wrapper.firstChild) {
      parent.insertBefore(wrapper.firstChild, wrapper)
    }
    parent.removeChild(wrapper)
  })

  root.querySelectorAll('[data-table-scroll-target]').forEach((el) => {
    el.removeAttribute('data-table-scroll-target')
  })

  root.querySelectorAll('table').forEach((table) => {
    table.style.removeProperty('minWidth')
    table.style.removeProperty('whiteSpace')
  })

  // Mise à jour des mesures après normalisation des tableaux
  measureContentHeightForSheets()
}

function goBack() {
  // Rediriger vers sheets?matiereId=id (liste des notions de synthèse)
  const matiereId = route.params.matiereId || subjectsStore.activeMatiereId
  if (matiereId) {
    router.push({ 
      name: 'Sheets', 
      query: { 
        matiereId: matiereId
      } 
    })
  } else {
    router.back()
  }
}

async function fetchSheet(nId) {
  loading.value = true
  try {
    if (sheetCache.has(nId)) {
      sheet.value = sheetCache.get(nId)
    } else {
      const { data } = await getSynthesisSheets({ notion: nId })
      const result = Array.isArray(data) ? data[0] : (Array.isArray(data?.results) ? data.results[0] : null)
      let full = result
      if (result?.id) {
        try {
          const detail = await getSynthesisSheet(result.id)
          full = detail?.data || detail
        } catch (_) {
          full = result
        }
      }
      sheet.value = full
      sheetCache.set(nId, full)
    }
  } finally {
    loading.value = false
    await nextTick()
    scrollToTop({ behavior: 'auto' })
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise()
    }
    // Extraire le sommaire après le rendu
    setTimeout(() => {
      prepareTablesForScroll()
      extractTableOfContents()
      buildSearchIndex()
      updateHeadingMatches()
      setupTocObserver()
      setupScrollListener()
      measureContentHeightForSheets()
    }, 150)
  }
}

onMounted(() => {
  detectMobileAndZoomSupport()
  updateViewportWidth()
  setupViewportListener()
  if (route.query?.q) {
    try { searchQuery.value = String(route.query.q) } catch {}
  }
  fetchSheet(notionId.value)
})

// Hook onActivated - appelé quand le composant est réactivé depuis le cache KeepAlive
onActivated(() => {
  detectMobileAndZoomSupport()
  updateViewportWidth()
  // Forcer le rendu MathJax à chaque réactivation pour éviter les problèmes de cache
  nextTick(() => {
    prepareTablesForScroll()
    if (window.MathJax && window.MathJax.typesetPromise) {
      try {
        // Vider le cache de MathJax pour forcer un nouveau rendu
        if (window.MathJax.typesetClear) {
          window.MathJax.typesetClear()
        }
        window.MathJax.typesetPromise()
      } catch (error) {
        console.warn('[MathJax] Erreur:', error)
      }
    }
    // S'assurer que le rendu est bien appliqué avec un second appel après un délai
    setTimeout(() => {
      prepareTablesForScroll()
      if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise()
      }
      measureContentHeightForSheets()
    }, 100)
  })
})

// Extraire la table des matières depuis le contenu HTML
function extractTableOfContents() {
  tableOfContents.value = []
  
  if (!sheetContentRef.value) return
  
  const headings = sheetContentRef.value.querySelectorAll('h2, h3')
  
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
  if (!sheetContentRef.value || typeof MutationObserver === 'undefined') return
  if (tocObserver) {
    try { tocObserver.disconnect() } catch (e) {}
  }
  tocObserver = new MutationObserver(() => {
    if (tocDebounce) clearTimeout(tocDebounce)
    tocDebounce = setTimeout(() => {
      extractTableOfContents()
      buildSearchIndex()
      measureContentHeightForSheets()
    }, 200)
  })
  tocObserver.observe(sheetContentRef.value, {
    childList: true,
    subtree: true
  })
}

// Fonction pour scroller vers une section
function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId)
  if (!element) return

  const container = getScrollContainer(sheetContentRef.value)
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
  const container = getScrollContainer(sheetContentRef.value)

  const handleScroll = () => {
    const scrollTop = container === document.documentElement || container === document.body
      ? window.pageYOffset || document.documentElement.scrollTop
      : container.scrollTop

    showScrollTopButton.value = scrollTop > 300
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
function scrollToTop({ behavior = 'smooth', targetEl } = {}) {
  const container = getScrollContainer(targetEl ?? sheetContentRef.value)

  if (container === document.documentElement || container === document.body) {
    window.scrollTo({ top: 0, behavior })
  } else {
    container.scrollTo({ top: 0, behavior })
  }
}

// Si l'utilisateur change de notion, recharger intelligemment avec le cache
watch(() => route.params.notionId, (newId, oldId) => {
  const n = Number(newId)
  if (n && n !== Number(oldId)) {
    fetchSheet(n)
  }
})

watch(rendered, () => {
  nextTick(() => {
    prepareTablesForScroll()
    measureContentHeightForSheets()
  })
})

watch(viewportWidth, () => {
  nextTick(() => {
    prepareTablesForScroll()
    if (typeof window !== 'undefined' && window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise().catch(() => {})
    }
    measureContentHeightForSheets()
  })
}, { immediate: true })

// Nettoyer l'observer au démontage
onBeforeUnmount(() => {
  if (tocObserver) {
    try { tocObserver.disconnect() } catch (e) {}
  }
  if (tocDebounce) {
    try { clearTimeout(tocDebounce) } catch {}
  }
  if (scrollCleanup) {
    try { scrollCleanup() } catch {}
  }
  cleanupViewportListener()
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
.sheet-by-notion-page {
  background: #fff;
  min-height: 100vh;
  padding: 0;
  text-align: left;
  position: relative;
}

:deep(.dashboard-main) {
  padding-top: 0 !important;
  padding-left: 0 !important;
}

:deep(.dashboard-main.with-mobile-nav) {
  padding-top: 0 !important;
}

.nav-header-base {
  padding: 0;
  margin: 0 0 1rem 0;
  display: flex;
  background: white;
  padding-top: 1.5rem;
  padding-bottom: 1rem;
}

.nav-header-base .back-button--top-left-dashboard {
  top: 0;
  left: 0;
}

.sheet-content-wrapper {
  width: 100%;
  padding: 0 2rem 1.5rem 2rem;
}

@media (max-width: 1200px) {
  .sheet-content-wrapper {
    padding: 0 1.5rem 1.25rem 1.5rem;
  }
}

@media (max-width: 768px) {
  .sheet-content-wrapper {
    padding: 0 0.65rem 0.65rem 0.65rem;
  }
}

@media (max-width: 480px) {
.sheet-content-wrapper {
    padding: 0 0rem 0rem 0rem;
  }
}

/* Empêche la page de défiler pendant le chargement */
.sheet-content-wrapper.sheet-loading {
  box-sizing: border-box;
  max-height: calc(100vh - 4rem);
  min-height: calc(100vh - 4rem);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.sheet-content-wrapper.sheet-loading .loading {
  width: 100%;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

@media (max-width: 360px) {
  .sheet-content-wrapper {
    padding: 0 0.35rem 0.35rem 0.35rem;
  }
}

.loading { text-align:center; padding:2rem; }
.spinner { width:36px; height:36px; border:3px solid #e5e7eb; border-top:3px solid #2563eb; border-radius:50%; animation: spin 1s linear infinite; margin: 0 auto 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }
.sheet-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.sheet-title { font-size: clamp(1.3rem, 4vw, 2rem); font-weight: 800; margin: 0.25rem 0 0.5rem; color: #193e8e; text-align: center; }
.sheet-content { 
  text-align: left;
  max-width: 100%;
  overflow-x: visible; /* Les tableaux gèrent leur propre scroll */
  overflow-y: visible;
  -webkit-overflow-scrolling: touch; /* Smooth scroll sur iOS */
  overflow-wrap: break-word;
  word-wrap: break-word;
  hyphens: auto;
  line-height: 1.6;
  color: #333;
  padding: 1rem 0 100px 0; /* Espace en bas pour la barre d'outils mobile */
  background: transparent;
}

/* Sur mobile, augmenter le padding pour les barres d'outils */
@media (max-width: 768px) {
  .sheet-content {
    padding-bottom: 120px;
  }
}

.sheet-content-outer {
  width: 100%;
  transform-origin: top left;
  transition: transform 0.2s ease, zoom 0.2s ease;
  overflow: visible;
  /* Les styles (zoom ou transform) seront appliqués dynamiquement via JS selon le support du zoom */
}

/* Sur mobile, assurer que le conteneur ne crée pas de problèmes de scroll */
@media (max-width: 768px) {
  .sheet-content-outer {
    min-height: auto;
    overflow: visible;
  }
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
.sheet-content :deep(h2.search-hit),
.sheet-content :deep(h3.search-hit) {
  background: #fffbeb;
  box-shadow: inset 0 -2px 0 #fde68a;
}
/* Styles pour les titres dans le contenu */
.sheet-content :deep(h1),
.sheet-content :deep(h2),
.sheet-content :deep(h3),
.sheet-content :deep(h4),
.sheet-content :deep(h5),
.sheet-content :deep(h6) {
  color: #193e8e;
  margin-top: 0.25rem !important;
  margin-bottom: 0.5rem !important;
}

.sheet-content :deep(p) { margin-top: 0; margin-bottom: 0.5rem; }

/* Mise à l'échelle automatique du contenu */
.sheet-content :deep(table) {
  width: 100% !important;
  max-width: 100% !important;
  table-layout: auto !important;
  white-space: normal !important;
  margin: 1.25rem 0;
  border-collapse: collapse;
}

.sheet-content :deep(table th),
.sheet-content :deep(table td) {
  white-space: normal !important;
  word-break: break-word;
  padding: 8px 12px;
}

.sheet-content :deep(.MathJax),
.sheet-content :deep(mjx-container) {
  max-width: 100% !important;
  white-space: normal !important;
  display: inline-block !important;
  overflow: visible !important;
}

.sheet-content :deep(.MathJax_Display),
.sheet-content :deep(.MathJax_SVG_Display),
.sheet-content :deep(mjx-container[display="true"]) {
  max-width: 100% !important;
  white-space: normal !important;
  display: block !important;
  overflow: visible !important;
  margin: 1.25rem 0;
  text-align: center !important;
}

.sheet-content :deep(.MathJax_SVG) {
  max-width: 100% !important;
  min-width: auto !important;
}

@media (max-width: 768px) {
  .sheet-content :deep(table th),
  .sheet-content :deep(table td) {
    padding: 6px 10px;
  }
}

/* Harmoniser la taille du h1 avec la page Cours en mobile */
@media (max-width: 640px) {
  .sheet-title { font-size: 1.25rem; }
}

/* Styles du sommaire */
.toc-container {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 0.3rem 0.75rem;
  margin: 0.8rem auto;
  width: 100%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  text-align: left;
}
/* Aligner la position du sommaire avec la page Cours */
.sheet-by-notion-page .toc-container { margin: 0.5rem 0; width: 100%; }

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
  font-size: 0.88rem;
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
  padding-top: 0.6rem;
  border-top: 1px solid #cbd5e1;
  margin-top: 0.6rem;
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
  padding: 0.35rem 0.55rem;
  color: #2d3a61;
  background: transparent;
  border: none;
  border-radius: 6px;
  transition: all 0.2s ease;
  font-size: 0.76rem;
  line-height: 1.35;
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
  font-size: 0.82rem;
}

.toc-level-3 .toc-link {
  font-weight: 400;
  font-size: 0.7rem;
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

@media (max-width: 768px) {
  .toc-container {
    width: calc(100% - 0.35rem);
    margin-left: 0.35rem;
    margin-right: 0;
  }
}

@media (max-width: 640px) {
  .toc-container {
    padding: 0.12rem 0.3rem;
    margin: 0.5rem auto;
    width: calc(100% - 0.3rem);
    margin-left: 0.3rem;
    margin-right: 0;
    transform: none;
  }

  .toc-header {
    margin-bottom: 0.35rem;
  }

  .toc-title {
    font-size: 0.78rem;
  }

  .toc-level-3 {
    margin-left: 0.5rem;
  }

  .toc-link {
    font-size: 0.65rem;
    padding: 0.22rem 0.3rem;
  }

  .toc-level-2 .toc-link {
    font-size: 0.7rem;
  }

  .toc-level-3 .toc-link {
    font-size: 0.62rem;
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

<style scoped>
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
.empty-icon { font-size: 2.2rem; margin-bottom: .25rem; }
.empty-title { margin: 0 0 .5rem; color: #0f172a; font-size: 1.35rem; }
.empty-text { color: #475569; margin: 0; }
.empty-actions { margin-top: 1rem; }
.empty-btn {
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: .6rem 1rem;
  font-weight: 700;
  cursor: pointer;
}
.empty-btn:hover { filter: brightness(1.05); }
</style>
