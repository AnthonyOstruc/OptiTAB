<script setup>
import { ref, computed, onMounted, watch, nextTick, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import NotionCard from '@/components/UI/NotionCard.vue'
import BackButton from '@/components/common/BackButton.vue'
import { getFreeResources } from '@/api/free-content'
import { useUserStore } from '@/stores/user'
import { useSubscriptionStore } from '@/stores/subscription'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'

const props = defineProps({
  resourceType: {
    type: String,
    default: 'course'
  }
})

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const error = ref(null)
const resources = ref([])
const selectedLevels = ref([])
const showLevelFilter = ref(false)
const currentPage = ref(1)
const itemsPerPage = 12
const searchQuery = ref('')
const userStore = useUserStore()
const subscriptionStore = useSubscriptionStore()
const { openModal } = useModalManager()

// Zoom system for mobile
const viewportWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1920)
const contentHeight = ref(0)
const contentRef = ref(null)

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
    '--content-zoom': z,
    '--content-height': `${contentHeight.value}px`,
    transform: `scale(${z})`,
    transformOrigin: 'top left',
    width: `${widthPercent}%`
  }
})

function updateViewportWidth() {
  if (typeof window === 'undefined') return
  viewportWidth.value = window.innerWidth
  nextTick(() => measureContentHeight())
}

function measureContentHeight() {
  if (!contentRef.value) {
    contentHeight.value = 0
    return
  }
  contentHeight.value = contentRef.value.scrollHeight || contentRef.value.offsetHeight || 0
}

const typeConfig = computed(() => {
  if (props.resourceType === 'exercise') {
    return {
      slugRoute: 'FreeExerciseDetail',
      fallback: 'Exercices à découvrir',
      emptyLabel: 'Aucun exercice gratuit disponible pour le moment.',
      counterLabel: 'exercice',
      chapterLabel: 'Chapitre'
    }
  }
  if (props.resourceType === 'summary') {
    return {
      slugRoute: 'FreeSummaryDetail',
      fallback: 'Fiches à découvrir',
      emptyLabel: 'Aucune fiche de synthèse gratuite disponible pour le moment.',
      counterLabel: 'fiche',
      chapterLabel: 'Niveau'
    }
  }
  return {
    slugRoute: 'FreeCourseDetail',
    fallback: 'Chapitres à découvrir',
    emptyLabel: 'Aucun chapitre gratuit disponible pour le moment.',
    counterLabel: 'chapitre',
    chapterLabel: 'Chapitre'
  }
})

const isExerciseMode = computed(() => props.resourceType === 'exercise')
const isSummaryMode = computed(() => props.resourceType === 'summary')
const isCourseMode = computed(() => props.resourceType === 'course')

const getCardTitle = (resource) => {
  if (isExerciseMode.value && resource?.notion_nom) {
    return resource.notion_nom
  }
  return resource?.titre || resource?.notion_nom || 'Chapitre'
}

const getCardDescription = (resource) => {
  if (isExerciseMode.value) {
    return 'Cliquez pour explorer les exercices'
  }
  if (isSummaryMode.value) {
    return 'Cliquez pour explorer les chapitres'
  }
  if (isCourseMode.value) {
    return 'Cliquez pour explorer les exercices'
  }
  return resource?.accroche || resource?.excerpt || 'Cliquez pour explorer ce chapitre'
}

const getSummaryLevel = (resource) => {
  return resource?.niveau_nom || resource?.tag_secondaire || resource?.matiere_nom || ''
}

const fetchResources = async () => {
  loading.value = true
  error.value = null
  try {
    const data = await getFreeResources({ type: props.resourceType })
    resources.value = Array.isArray(data?.results) ? data.results : data
  } catch (err) {
    console.error('Erreur chargement ressources gratuites', err)
    error.value = err?.message || "Impossible de charger ces ressources gratuites."
  } finally {
    loading.value = false
  }
}

onMounted(fetchResources)
onMounted(() => {
  updateViewportWidth()
  if (typeof window !== 'undefined') {
    window.addEventListener('resize', updateViewportWidth, { passive: true })
  }
})

onBeforeUnmount(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', updateViewportWidth)
  }
})

watch(() => props.resourceType, () => {
  fetchResources()
  selectedLevels.value = []
  currentPage.value = 1
  searchQuery.value = ''
})

watch(() => selectedLevels.value.length, () => {
  currentPage.value = 1
  nextTick(() => measureContentHeight())
})

watch(() => searchQuery.value, () => {
  currentPage.value = 1
  nextTick(() => measureContentHeight())
})

watch(() => zoomLevel.value, () => {
  nextTick(() => measureContentHeight())
})

const availableLevels = computed(() => {
  const levels = new Set()
  resources.value.forEach((resource) => {
    const level = resource?.niveau_nom || resource?.tag_secondaire
    if (level) {
      levels.add(level)
    }
  })
  return Array.from(levels).sort()
})

const filteredResources = computed(() => {
  let filtered = resources.value

  // Filter by level
  if (selectedLevels.value.length > 0) {
    filtered = filtered.filter((resource) => {
      const level = resource?.niveau_nom || resource?.tag_secondaire
      return level && selectedLevels.value.includes(level)
    })
  }

  // Filter by search query and mark if match is in content
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    filtered = filtered.filter((resource) => {
      // Chercher dans le titre
      const title = (resource?.titre || resource?.notion_nom || '').toLowerCase()
      
      // Chercher dans le contenu texte (champ principal du cours)
      const content = (resource?.contenu || '').toLowerCase()
      
      // Chercher dans les autres champs textuels
      const accroche = (resource?.accroche || '').toLowerCase()
      const excerpt = (resource?.excerpt || '').toLowerCase()
      const question = (resource?.question || '').toLowerCase()
      
      // Enlever les balises HTML du contenu pour une meilleure recherche
      const cleanContent = content.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ')
      
      const titleMatch = title.includes(query)
      const contentMatch = cleanContent.includes(query)
      const otherMatch = accroche.includes(query) || excerpt.includes(query) || question.includes(query)
      
      // Marquer si le match provient du contenu
      resource._matchInContent = !titleMatch && (contentMatch || otherMatch)
      
      return titleMatch || contentMatch || otherMatch
    })
  } else {
    // Réinitialiser le marqueur si pas de recherche
    filtered.forEach(resource => {
      resource._matchInContent = false
    })
  }

  return filtered
})

const toggleLevel = (level) => {
  const index = selectedLevels.value.indexOf(level)
  if (index > -1) {
    selectedLevels.value.splice(index, 1)
  } else {
    selectedLevels.value.push(level)
  }
}

const clearFilters = () => {
  selectedLevels.value = []
}

const flatList = computed(() => {
  if (!filteredResources.value.length) {
    return []
  }

  if (isExerciseMode.value) {
    const chaptersMap = new Map()
    filteredResources.value.forEach((item, index) => {
      const chapterKey = item.notion || item.notion_nom || `chapitre-${index}`
      if (!chaptersMap.has(chapterKey)) {
        chaptersMap.set(chapterKey, {
          id: chapterKey,
          notionId: item.notion || chapterKey,
          name: item.notion_nom || 'Chapitre gratuit',
          description: item.notion_description || item.accroche || item.excerpt || '',
          exercises: [],
          displayTag: ''
        })
      }
      const chapterEntry = chaptersMap.get(chapterKey)
      chapterEntry.exercises.push(item)
      const tag = item.tag_secondaire || item.niveau_nom || item.matiere_nom || ''
      if (!chapterEntry.displayTag && tag) {
        chapterEntry.displayTag = tag
      }
    })
    return Array.from(chaptersMap.values())
      .map((chapter) => ({
        ...chapter,
        count: chapter.exercises.length,
        isLocked: chapter.exercises.length > 0 && chapter.exercises.every((exercise) => Boolean(exercise.is_locked))
      }))
      .sort((a, b) => {
        if (a.isLocked !== b.isLocked) {
          return a.isLocked ? 1 : -1
        }
        return a.name.localeCompare(b.name)
      })
  }

  const sorted = [...filteredResources.value].sort((a, b) => {
    const aLocked = Boolean(a.is_locked)
    const bLocked = Boolean(b.is_locked)
    if (aLocked === bLocked) return 0
    return aLocked ? 1 : -1
  })

  return sorted
})

const totalResourceCount = computed(() => {
  if (isExerciseMode.value) {
    // Pour les exercices, afficher "X exercices" et "Y chapitres"
    return {
      count: filteredResources.value.length,
      chapterCount: flatList.value.length
    }
  }
  return {
    count: flatList.value.length,
    chapterCount: 0
  }
})

const totalPages = computed(() => Math.ceil(flatList.value.length / itemsPerPage))

const paginatedList = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return flatList.value.slice(start, end)
})

const goToPage = (page) => {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const formatCount = (count, overrideLabel) => {
  const label = overrideLabel || typeConfig.value.counterLabel || 'ressource'
  return `${count} ${label}${count > 1 ? 's' : ''}`
}

const openResource = (resource) => {
  if (!resource) return
  if (resource.is_locked) {
    onLockedResource(resource)
    return
  }
  if (!resource.slug) return
  router.push({ name: typeConfig.value.slugRoute, params: { slug: resource.slug } })
}

const openExerciseChapter = (chapter) => {
  if (!chapter) return
  if (chapter.isLocked) {
    onLockedExercise(chapter)
    return
  }
  const notionId = chapter?.notionId || chapter?.id
  if (!notionId) return
  router.push({
    name: 'FreeExerciseChapter',
    params: { notionId },
    query: { title: chapter?.name || undefined }
  })
}

const premiumRoutes = {
  course: 'CourseByNotion',
  exercise: 'ExercicesByNotion',
  summary: 'SynthesisByNotion'
}

const handleLockedAccess = ({ resourceType, notionId }) => {
  if (subscriptionStore.hasAccess && notionId && premiumRoutes[resourceType]) {
    router.push({ name: premiumRoutes[resourceType], params: { notionId } })
    return
  }

  if (!userStore.isAuthenticated) {
    openModal(MODAL_IDS.LOGIN)
    return
  }

  router.push({
    name: 'Billing',
    query: {
      redirect: route.fullPath,
      reason: `${resourceType}_premium`
    }
  })
}

const onLockedResource = (resource) => {
  if (!resource?.notion) {
    handleLockedAccess({ resourceType: props.resourceType, notionId: null })
    return
  }
  handleLockedAccess({ resourceType: props.resourceType, notionId: resource.notion })
}

const onLockedExercise = (chapter) => {
  handleLockedAccess({ resourceType: 'exercise', notionId: chapter?.notionId })
}
</script>

<template>
  <MainLayout>
    <div class="free-course-page">
      <div class="header-row">
        <BackButton text="Retour à l'accueil" :custom-action="() => router.push({ name: 'Home' })" position="top-left" />
        <div v-if="!loading && totalResourceCount.count > 0" class="resource-count-badge">
          <template v-if="isExerciseMode && totalResourceCount.chapterCount > 0">
            {{ totalResourceCount.count }} {{ typeConfig.counterLabel }}{{ totalResourceCount.count > 1 ? 's' : '' }}
            <span class="badge-separator">+</span>
            {{ totalResourceCount.chapterCount }} chapitre{{ totalResourceCount.chapterCount > 1 ? 's' : '' }}
          </template>
          <template v-else>
            {{ totalResourceCount.count }} {{ typeConfig.counterLabel }}{{ totalResourceCount.count > 1 ? 's' : '' }}
          </template>
        </div>
      </div>

      <div v-if="availableLevels.length > 0" class="filter-section">
        <div class="filter-bar">
          <button class="filter-toggle" @click="showLevelFilter = !showLevelFilter">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="filter-icon">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 01-.659 1.591l-5.432 5.432a2.25 2.25 0 00-.659 1.591v2.927a2.25 2.25 0 01-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 00-.659-1.591L3.659 7.409A2.25 2.25 0 013 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0112 3z" />
            </svg>
            Filtrer par niveau
            <span v-if="selectedLevels.length > 0" class="filter-badge">{{ selectedLevels.length }}</span>
          </button>

          <div class="search-box">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="search-icon">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Rechercher un chapitre ou une méthode..."
              class="search-input"
            />
            <button
              v-if="searchQuery"
              class="clear-search-btn"
              @click="searchQuery = ''"
              aria-label="Effacer la recherche"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="clear-icon">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <div v-if="showLevelFilter" class="filter-dropdown">
          <div class="filter-header">
            <span class="filter-title">Niveaux</span>
            <button v-if="selectedLevels.length > 0" class="clear-btn" @click="clearFilters">Effacer</button>
          </div>
          <div class="filter-options">
            <label
              v-for="level in availableLevels"
              :key="level"
              class="filter-option"
            >
              <input
                type="checkbox"
                :checked="selectedLevels.includes(level)"
                @change="toggleLevel(level)"
              />
              <span class="filter-label">{{ level }}</span>
            </label>
          </div>
        </div>
      </div>

      <div v-if="loading" class="state-card">
        Chargement des ressources gratuites...
      </div>
      <div v-else-if="error" class="state-card">
        <p>{{ error }}</p>
        <button @click="fetchResources">Réessayer</button>
      </div>
      <div v-else-if="flatList.length === 0" class="state-card">
        {{ typeConfig.emptyLabel }}
      </div>
      <template v-else>
        <div class="content-wrapper" :style="zoomStyle" ref="contentRef">
          <div class="notion-grid">
          <template v-if="isExerciseMode">
            <NotionCard
              v-for="chapter in paginatedList"
              :key="chapter.id"
              :title="chapter.name"
              description="Cliquez pour explorer les exercices"
              :notion-id="chapter.notionId"
              :disable-prefetch="true"
              :locked="Boolean(chapter.isLocked)"
              @click="openExerciseChapter(chapter)"
              @locked-click="() => onLockedExercise(chapter)"
            >
              <template #meta>
                <span
                  v-if="chapter.isLocked"
                  class="resource-locked-pill"
                >
                  Premium
                </span>
                <span class="resource-chapter-pill">
                  {{ formatCount(chapter.count || chapter.exercises.length, 'exercice') }}
                </span>
                <span
                  v-if="chapter.displayTag"
                  class="resource-tag-pill"
                >
                  {{ chapter.displayTag }}
                </span>
              </template>
            </NotionCard>
          </template>

          <template v-else>
            <NotionCard
              v-for="resource in paginatedList"
              :key="resource.slug"
              :title="getCardTitle(resource)"
              :description="getCardDescription(resource)"
              :notion-id="resource.notion"
              :disable-prefetch="true"
              :locked="Boolean(resource.is_locked)"
              @click="openResource(resource)"
              @locked-click="() => onLockedResource(resource)"
            >
              <template v-if="isSummaryMode" #meta>
                <span
                  v-if="resource._matchInContent"
                  class="resource-match-pill"
                >
                  🔍 Trouvé dans le contenu
                </span>
                <span
                  v-if="resource.is_locked"
                  class="resource-locked-pill"
                >
                  Premium
                </span>
                <span
                  v-if="getSummaryLevel(resource)"
                  class="resource-chapter-pill"
                >
                  {{ getSummaryLevel(resource) }}
                </span>
              </template>
              <template v-else #meta>
                <span
                  v-if="resource._matchInContent"
                  class="resource-match-pill"
                >
                  🔍 Trouvé dans le contenu
                </span>
                <span
                  v-if="resource.is_locked"
                  class="resource-locked-pill"
                >
                  Premium
                </span>
                <span v-if="resource.tag_secondaire" class="resource-tag-pill">
                  {{ resource.tag_secondaire }}
                </span>
              </template>
            </NotionCard>
          </template>
        </div>

        <div v-if="totalPages > 1" class="pagination">
          <button
            class="pagination-btn"
            :disabled="currentPage === 1"
            @click="goToPage(currentPage - 1)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="pagination-icon">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>
          </button>
          
          <div class="pagination-info">
            <span class="pagination-text">Page {{ currentPage }} sur {{ totalPages }}</span>
          </div>
          
          <button
            class="pagination-btn"
            :disabled="currentPage === totalPages"
            @click="goToPage(currentPage + 1)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="pagination-icon">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
            </svg>
          </button>
        </div>
        </div>
      </template>
    </div>
  </MainLayout>
</template>

<style scoped>
.free-course-page {
  min-height: 100vh;
  background: #ffffff;
  padding: 140px 32px 80px;
  max-width: 1200px;
  margin: 0 auto;
}

.content-wrapper {
  transform-origin: top left;
}

@supports (zoom: 1) {
  .content-wrapper {
    zoom: var(--content-zoom, 1);
    transform: none !important;
    width: 100% !important;
  }
}

.header-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.resource-count-badge {
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  background: #eef2ff;
  color: #3730a3;
  font-size: 14px;
  font-weight: 700;
  border-radius: 999px;
  border: 1px solid rgba(59, 130, 246, 0.3);
  white-space: nowrap;
}

.badge-separator {
  margin: 0 8px;
  color: #6366f1;
  font-weight: 600;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 48px;
  padding: 20px 0;
}

.pagination-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #fff;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  background: #f8fafc;
  border-color: #3b82f6;
  color: #3b82f6;
}

.pagination-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.pagination-icon {
  width: 20px;
  height: 20px;
}

.pagination-info {
  padding: 0 12px;
}

.pagination-text {
  font-size: 14px;
  font-weight: 600;
  color: #334155;
}

.filter-section {
  position: relative;
  margin-bottom: 24px;
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 280px;
  max-width: 470px;
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: #94a3b8;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 10px 40px 10px 44px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 14px;
  color: #334155;
  background: #fff;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.search-input::placeholder {
  color: #94a3b8;
}

.clear-search-btn {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  color: #94a3b8;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.clear-search-btn:hover {
  background: #f1f5f9;
  color: #475569;
}

.clear-icon {
  width: 16px;
  height: 16px;
}

.filter-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  color: #475569;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}

.filter-toggle:hover {
  border-color: #3b82f6;
  color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.filter-icon {
  width: 18px;
  height: 18px;
}

.filter-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  background: #3b82f6;
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  border-radius: 999px;
  margin-left: 4px;
}

.filter-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  min-width: 240px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.12);
  z-index: 100;
  padding: 12px;
}

.filter-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 10px;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 10px;
}

.filter-title {
  font-size: 13px;
  font-weight: 700;
  color: #0f172a;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.clear-btn {
  padding: 4px 10px;
  background: transparent;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  color: #64748b;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-btn:hover {
  background: #f1f5f9;
  color: #475569;
}

.filter-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 300px;
  overflow-y: auto;
}

.filter-option {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.filter-option:hover {
  background: #f8fafc;
}

.filter-option input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
  accent-color: #3b82f6;
}

.filter-label {
  flex: 1;
  font-size: 14px;
  color: #334155;
  font-weight: 500;
}

.notion-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 320px));
  gap: 16px;
  justify-content: flex-start;
  justify-items: start;
}

.state-card {
  margin-top: 30px;
  padding: 32px;
  border-radius: 18px;
  border: 1px dashed #cbd5f5;
  text-align: center;
  color: #475569;
}

.state-card button {
  margin-top: 12px;
  padding: 10px 18px;
  border-radius: 12px;
  border: none;
  background: #1d4ed8;
  color: #fff;
  cursor: pointer;
}

.resource-chapter-pill,
.resource-status-pill,
.resource-tag-pill,
.resource-locked-pill,
.resource-match-pill {
  font-size: 12px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 999px;
  border: 1px solid transparent;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.resource-chapter-pill {
  background: #eef2ff;
  color: #3730a3;
  border-color: rgba(59, 130, 246, 0.3);
}

.resource-status-pill {
  background: #e0f2fe;
  color: #0c4a6e;
  border-color: rgba(14, 165, 233, 0.4);
}

.resource-tag-pill {
  background: #dcfce7;
  color: #14532d;
  border-color: rgba(34, 197, 94, 0.35);
}

.resource-locked-pill {
  background: #eef2ff;
  color: #1d4ed8;
  border-color: rgba(99, 102, 241, 0.35);
  text-transform: uppercase;
  font-size: 11px;
}

.resource-match-pill {
  background: #fef3c7;
  color: #92400e;
  border-color: rgba(251, 191, 36, 0.4);
  font-size: 11px;
}

@media (max-width: 768px) {
  .free-course-page {
    padding: 120px 16px 60px;
  }

  .notion-grid {
    grid-template-columns: 1fr;
    justify-content: stretch;
  }
}

@media (max-width: 640px) {
  .free-course-page {
    padding: 110px 14px 56px;
  }

  .header-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 20px;
  }

  .resource-count-badge {
    font-size: 13px;
    padding: 6px 14px;
  }

  .filter-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    max-width: 100%;
    min-width: 100%;
  }

  .filter-toggle {
    width: 100%;
  }

  .notion-grid {
    gap: 12px;
  }

  .pagination {
    margin-top: 32px;
    gap: 12px;
  }

  .pagination-btn {
    width: 36px;
    height: 36px;
  }

  .pagination-icon {
    width: 18px;
    height: 18px;
  }

  .pagination-text {
    font-size: 13px;
  }
}

@media (max-width: 420px) {
  .free-course-page {
    padding: 105px 12px 48px;
  }
}
</style>
