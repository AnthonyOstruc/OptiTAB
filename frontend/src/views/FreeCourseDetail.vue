<script setup>
import { ref, onMounted, nextTick, watch, computed, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import BackButton from '@/components/common/BackButton.vue'
import ExerciceQCM from '@/components/UI/ExerciceQCM.vue'
import { getFreeResource } from '@/api/free-content'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { renderContentWithImages, renderMath } from '@/utils/scientificRenderer'

const props = defineProps({
  resourceType: {
    type: String,
    default: 'course'
  }
})

const route = useRoute()
const router = useRouter()
const { openModal } = useModalManager()

const resource = ref(null)
const loading = ref(false)
const error = ref(null)
const tableOfContents = ref([])
const isTocExpanded = ref(false)
const contentRef = ref(null)
const viewportWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1920)
const contentHeight = ref(0)
const renderedContent = computed(() => {
  if (!resource.value) return ''
  if (resource.value.contenu) {
    return renderContentWithImages(resource.value.contenu, resource.value.images || [])
  }
  return resource.value.contenu_html || ''
})
const isExerciseResource = computed(() => props.resourceType === 'exercise')
const exerciseInstruction = computed(() => {
  if (!resource.value) return ''
  return resource.value.question || resource.value.contenu || resource.value.accroche || ''
})
const exerciseSteps = computed(() => (resource.value?.etapes ? resource.value.etapes : ''))
const exerciseSolution = computed(() => {
  if (!resource.value) return ''
  return resource.value.solution || resource.value.reponse_correcte || ''
})
const exerciseDifficulty = computed(() => resource.value?.difficulty || 'medium')
const exerciseImages = computed(() => resource.value?.images || [])

const safeRenderMath = async () => {
  try {
    await renderMath()
  } catch (_) {
    // Ignore MathJax failures (e.g., when the content is empty or MathJax is busy)
  }
}
const showScrollTopButton = ref(false)
const backButtonLabel = computed(() => {
  if (props.resourceType === 'exercise') {
    return 'Retour aux exercices gratuits'
  }
  if (props.resourceType === 'summary') {
    return 'Retour aux fiches gratuites'
  }
  return 'Retour aux chapitres gratuits'
})

function computeAutoZoom(width) {
  let base
  if (width >= 1400) base = 1
  else if (width >= 1200) base = 0.95
  else if (width >= 1024) base = 0.9
  else if (width >= 900) base = 0.85
  else if (width >= 768) base = 0.8
  else if (width >= 640) base = 0.78
  else if (width >= 520) base = 0.76
  else if (width >= 420) base = 0.74
  else base = 0.72

  if (width < 1024) {
    const extra = width < 768 ? 0.1 : 0.07
    return Math.max(0.6, base - extra)
  }
  return base
}

const zoomLevel = computed(() => computeAutoZoom(viewportWidth.value))

const zoomStyle = computed(() => {
  const z = zoomLevel.value || 1
  const widthPercent = (100 / z).toFixed(3)
  return {
    '--course-zoom': z,
    '--course-content-height': `${contentHeight.value}px`,
    transform: `scale(${z})`,
    transformOrigin: 'top left',
    width: `${widthPercent}%`
  }
})

const fetchResource = async () => {
  loading.value = true
  error.value = null
  try {
    resource.value = await getFreeResource(route.params.slug)
  } catch (err) {
    console.error('Erreur chargement de la ressource gratuite', err)
    error.value = err?.message || "Impossible de charger cette ressource gratuite."
  } finally {
    loading.value = false
  }
}

const buildTableOfContents = () => {
  tableOfContents.value = []
  const root = contentRef.value
  if (!root) return
  const selectors = root.querySelectorAll('h1, h2, h3')
  const toc = []
  selectors.forEach((heading, index) => {
    const level = Number(heading.tagName.replace('H', ''))
    const text = heading.textContent?.trim()
    if (!text) return
    const id = heading.id || `free-course-heading-${index}`
    heading.id = id
    toc.push({ id, text, level })
  })
  tableOfContents.value = toc
}

const measureContentHeight = () => {
  if (!contentRef.value) {
    contentHeight.value = 0
    return
  }
  contentHeight.value = contentRef.value.scrollHeight || contentRef.value.offsetHeight || 0
}

const updateViewportWidth = () => {
  if (typeof window === 'undefined') return
  viewportWidth.value = window.innerWidth
  nextTick(() => measureContentHeight())
}

const handleScroll = () => {
  const threshold = 300
  showScrollTopButton.value = (window.scrollY || document.documentElement.scrollTop || 0) > threshold
}

const scrollToTop = () => {
  if (typeof window === 'undefined') return
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const scrollToSection = (id) => {
  const el = document.getElementById(id)
  if (!el) return
  el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const goBack = () => {
  let routeName = 'FreeCourses'
  if (props.resourceType === 'exercise') {
    routeName = 'FreeExercises'
  } else if (props.resourceType === 'summary') {
    routeName = 'FreeSummaries'
  }
  router.push({ name: routeName })
}

const openSignup = () => {
  openModal(MODAL_IDS.REGISTER)
}

watch(
  () => route.params.slug,
  () => {
    resource.value = null
    fetchResource()
  }
)

watch(
  renderedContent,
  async (html) => {
    if (!html) {
      tableOfContents.value = []
      return
    }
    await nextTick()
    buildTableOfContents()
    await safeRenderMath()
    measureContentHeight()
  },
  { immediate: true }
)

watch(zoomLevel, () => {
  nextTick(() => measureContentHeight())
})

onMounted(() => {
  fetchResource()
  if (typeof window !== 'undefined') {
    window.addEventListener('resize', updateViewportWidth, { passive: true })
    window.addEventListener('scroll', handleScroll, { passive: true })
  }
})

onBeforeUnmount(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', updateViewportWidth)
    window.removeEventListener('scroll', handleScroll)
  }
})
</script>

<template>
  <MainLayout>
    <section class="cours-section">
      <div class="nav-header-base">
        <BackButton 
          :text="backButtonLabel" 
          :custom-action="goBack"
        />
      </div>

      <div class="cours-body">
        <div v-if="loading" class="loading-container">
        Chargement de la ressource...
        </div>

        <div v-else-if="error" class="error-state">
          <p>{{ error }}</p>
          <button @click="fetchResource">Réessayer</button>
        </div>

        <div v-else-if="resource" class="cours-container">
          <header class="cours-header">
            <div class="cours-title-row">
              <h1 class="cours-title">{{ resource.titre }}</h1>
              <div class="cours-badges">
                <span v-if="resource.badge" class="cours-badge">{{ resource.badge }}</span>
                <span v-if="resource.type_label" class="cours-type-pill">{{ resource.type_label }}</span>
              </div>
            </div>
            <p class="cours-context">
              <span v-if="resource.notion_nom">Chapitre : {{ resource.notion_nom }}</span>
              <span v-if="resource.matiere_nom">• {{ resource.matiere_nom }}</span>
              <span v-if="resource.niveau_nom">• {{ resource.niveau_nom }}</span>
            </p>
          </header>

          <div v-if="isExerciseResource" class="exercise-detail-body">
            <ExerciceQCM
              :eid="resource.id"
              :titre="resource.titre"
              :instruction="exerciseInstruction"
              :etapes="exerciseSteps"
              :solution="exerciseSolution"
              :difficulty="exerciseDifficulty"
              :preview-images="exerciseImages"
              :readonly="true"
            />
          </div>

          <nav v-if="tableOfContents.length && !isExerciseResource" class="toc-container">
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
              <svg class="toc-toggle-icon" :class="{ expanded: isTocExpanded }" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9" />
              </svg>
          </div>
          <transition name="toc-expand">
              <div v-show="isTocExpanded" class="toc-body">
                <ul class="toc-list">
                  <li 
                    v-for="(item, index) in tableOfContents" 
                    :key="item.id || index"
                    :class="['toc-item', `toc-level-${item.level}`]"
                  >
                    <a class="toc-link" href="#" @click.prevent="scrollToSection(item.id)">
                      {{ item.text }}
                    </a>
                  </li>
                </ul>
              </div>
            </transition>
          </nav>

          <div v-if="!isExerciseResource" class="cours-content-outer" :style="zoomStyle">
            <div class="cours-content" ref="contentRef" v-html="renderedContent" />
          </div>

          <transition name="scroll-top-fade">
            <button
              v-show="showScrollTopButton && !isExerciseResource"
              class="scroll-top-btn"
              @click="scrollToTop"
              aria-label="Retour en haut"
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="18 15 12 9 6 15" />
              </svg>
            </button>
          </transition>
        </div>
      </div>
    </section>
  </MainLayout>
</template>

<style scoped>
.cours-section {
  padding: 110px 2vw 60px;
  background: #fff;
  min-height: 100vh;
  position: relative;
}

.nav-header-base {
  margin: 0 0 1rem 0;
  padding: 0;
  display: flex;
}

.cours-body {
  width: 100%;
}

@media (max-width: 768px) {
  .cours-section {
    padding-top: 90px;
  }

  .cours-header {
    margin-bottom: 0;
  }
}

.cours-header {
  text-align: center;
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.cours-title-row {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.cours-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.cours-badge,
.cours-type-pill {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 999px;
  border: 1px solid transparent;
}

.cours-badge {
  background: #e0f2fe;
  color: #0f172a;
  border-color: rgba(37, 99, 235, 0.4);
}

.cours-type-pill {
  background: #f1f5f9;
  color: #1d3557;
  border-color: rgba(148, 163, 184, 0.5);
}

.cours-context {
  margin: 0;
  color: #475569;
  font-weight: 600;
  font-size: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: center;
}

.exercise-detail-body {
  margin: 20px 0 0;
  width: 100%;
  padding: 0 0 24px;
}

.exercise-intro {
  font-size: 16px;
  color: #1f2937;
  margin: 0 0 16px;
}

.exercise-section {
  margin-bottom: 24px;
  padding: 18px;
  border-radius: 20px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
}

.exercise-section h3 {
  margin: 0 0 12px;
  font-size: 18px;
  color: #0f172a;
}

.exercise-card {
  background: #fff;
  border-radius: 24px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 20px 45px rgba(15, 23, 42, 0.08);
  padding: 20px 22px;
  margin: 18px 0 16px;
}

.exercise-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 12px;
}

.exercise-card-title {
  margin: 0;
  font-size: clamp(20px, 2vw, 26px);
  font-weight: 700;
  color: #0f172a;
}

.exercise-card-subtitle {
  margin: 4px 0 0;
  color: #475569;
  font-size: 15px;
}

.exercise-card-star {
  border-radius: 999px;
  border: 1px solid #d1d5db;
  background: #fefefe;
  width: 42px;
  height: 42px;
  font-size: 18px;
  cursor: pointer;
}

.exercise-card-tabs {
  display: flex;
  justify-content: flex-start;
  gap: 8px;
  margin-top: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e2e8f0;
}

.exercise-card-panel {
  margin-top: 10px;
  padding: 0;
}

.exercise-section-card {
  background: #f9fafb;
  border-radius: 18px;
  border: 1px solid #e2e8f0;
  padding: 16px 18px;
  min-height: 190px;
  font-size: 16px;
  line-height: 1.4;
}

.exercise-section-card :deep(*) {
  margin: 0;
  line-height: inherit;
}

.exercise-section-card :deep(p + p),
.exercise-section-card :deep(p + ul),
.exercise-section-card :deep(p + ol),
.exercise-section-card :deep(ul + p),
.exercise-section-card :deep(ol + p),
.exercise-section-card :deep(li + li) {
  margin-top: 4px;
}

.exercise-section-card :deep(ul),
.exercise-section-card :deep(ol) {
  padding-left: 18px;
}

.exercise-section-card :deep(li) {
  padding: 0;
}

.exercise-tabs {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 18px;
  padding-bottom: 4px;
  border-bottom: 1px solid #dbeafe;
}

.exercise-tab {
  border: none;
  background: transparent;
  padding: 8px 20px;
  font-weight: 600;
  color: #64748b;
  border-radius: 999px;
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease;
}

.exercise-tab.active {
  color: #0f172a;
  background: #e0f2fe;
  box-shadow: inset 0 -3px 0 0 #2563eb;
}

.cours-title {
  font-size: clamp(24px, 3vw, 30px);
  color: #193e8e;
  margin: 0 0 8px;
  font-weight: 800;
}

.detail-meta {
  color: #475569;
  font-weight: 600;
  margin: 8px 0 0;
}

.inline-back {
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 999px;
  border: 1px solid rgba(25, 62, 142, 0.3);
  background: #f5f8ff;
  color: #193e8e;
  font-weight: 600;
  cursor: pointer;
  transition: border-color 0.2s ease, color 0.2s ease;
}

.inline-back:hover {
  border-color: #193e8e;
}

.toc-container {
  margin: 12px 0 18px;
  width: 100%;
  border-radius: 24px;
  background: #f5f8ff;
  border: 1px solid rgba(25, 62, 142, 0.12);
  overflow: hidden;
  transform-origin: top left;
}

@media (max-width: 1024px) {
  .toc-container {
    transform: scale(0.96);
  }
}

@media (max-width: 768px) {
  .toc-container {
    transform: scale(0.92);
    margin: 0 auto;
  }
}

.toc-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 18px;
  cursor: pointer;
  color: #1d3b8b;
  font-weight: 600;
  font-size: 16px;
}

.toc-header-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.toc-body {
  border-top: 1px solid rgba(25, 62, 142, 0.12);
  padding: 10px 22px 16px;
}

.toc-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.toc-item {
  font-size: 16px;
  color: #0f172a;
}

.toc-link {
  text-decoration: none;
  color: #193e8e;
  font-weight: 600;
}

.toc-level-3 .toc-link {
  font-weight: 400;
  color: #1d4ed8;
  padding-left: 24px;
}

.cours-content-outer {
  width: 100%;
  transform-origin: top left;
  transition: transform 0.2s ease;
  overflow-x: hidden;
  height: calc(var(--course-content-height, 0px) * var(--course-zoom, 1));
  margin-top: -8px;
}

@supports (zoom: 1) {
  .cours-content-outer {
    zoom: var(--course-zoom, 1);
    transform: none !important;
    width: 100% !important;
    height: auto !important;
  }
}

.cours-content {
  width: 100%;
  padding: 0 0 40px;
  line-height: 1.75;
  color: #1f2937;
  font-size: 17px;
}

.cours-content :deep(h1),
.cours-content :deep(h2),
.cours-content :deep(h3) {
  color: #0f172a;
  margin-top: 32px;
  border-bottom: 2px solid #3b82f6;
  padding-bottom: 8px;
}

.scroll-top-btn {
  position: fixed;
  bottom: 28px;
  left: 24px;
  width: 50px;
  height: 50px;
  border: none;
  border-radius: 50%;
  background: #1d3b8b;
  color: #fff;
  box-shadow: 0 15px 30px rgba(29, 59, 139, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 1200;
}

.scroll-top-fade-enter-active,
.scroll-top-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.scroll-top-fade-enter-from,
.scroll-top-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
