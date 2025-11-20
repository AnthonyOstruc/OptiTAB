<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import NotionCard from '@/components/UI/NotionCard.vue'
import BackButton from '@/components/common/BackButton.vue'
import { getFreeResources } from '@/api/free-content'

const props = defineProps({
  resourceType: {
    type: String,
    default: 'course'
  }
})

const router = useRouter()
const loading = ref(false)
const error = ref(null)
const resources = ref([])
const selectedLevels = ref([])
const showLevelFilter = ref(false)

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
watch(() => props.resourceType, () => {
  fetchResources()
  selectedLevels.value = []
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
  if (selectedLevels.value.length === 0) {
    return resources.value
  }
  return resources.value.filter((resource) => {
    const level = resource?.niveau_nom || resource?.tag_secondaire
    return level && selectedLevels.value.includes(level)
  })
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

const themes = computed(() => {
  if (!filteredResources.value.length) {
    return []
  }

  const fallbackTitle = typeConfig.value.fallback

  if (isExerciseMode.value) {
    const themeGroups = new Map()
    filteredResources.value.forEach((item, index) => {
      const themeKey =
        item.theme_id ??
        (item.matiere ? `matiere-${item.matiere}` : `autres-${index}`)

      if (!themeGroups.has(themeKey)) {
        themeGroups.set(themeKey, {
          id: themeKey,
          name: item.theme_nom || item.matiere_nom || fallbackTitle,
          chaptersMap: new Map(),
          totalCount: 0
        })
      }

      const themeGroup = themeGroups.get(themeKey)
      const chapterKey = item.notion || item.notion_nom || `chapitre-${index}`
      if (!themeGroup.chaptersMap.has(chapterKey)) {
        themeGroup.chaptersMap.set(chapterKey, {
          id: chapterKey,
          notionId: item.notion || chapterKey,
          name: item.notion_nom || 'Chapitre gratuit',
          description: item.notion_description || item.accroche || item.excerpt || '',
          exercises: []
        })
      }

      themeGroup.chaptersMap.get(chapterKey).exercises.push(item)
      themeGroup.totalCount += 1
    })

    return Array.from(themeGroups.values())
      .map((theme) => ({
        id: theme.id,
        name: theme.name,
        chapters: Array.from(theme.chaptersMap.values())
          .map((chapter) => ({
            ...chapter,
            count: chapter.exercises.length
          }))
          .sort((a, b) => a.name.localeCompare(b.name)),
        totalCount: theme.totalCount
      }))
      .sort((a, b) => a.name.localeCompare(b.name))
  }

  const groups = new Map()
  filteredResources.value.forEach((item, index) => {
    const key =
      item.theme_id ??
      (item.matiere ? `matiere-${item.matiere}` : item.notion ? `notion-${item.notion}` : `autres-${index}`)

    if (!groups.has(key)) {
      groups.set(key, {
        id: key,
        name: item.theme_nom || item.matiere_nom || item.notion_nom || fallbackTitle,
        notions: []
      })
    }
    groups.get(key).notions.push(item)
  })

  return Array.from(groups.values()).sort((a, b) => a.name.localeCompare(b.name))
})

const formatCount = (count, overrideLabel) => {
  const label = overrideLabel || typeConfig.value.counterLabel || 'ressource'
  return `${count} ${label}${count > 1 ? 's' : ''}`
}

const openResource = (resource) => {
  if (!resource?.slug) return
  router.push({ name: typeConfig.value.slugRoute, params: { slug: resource.slug } })
}

const openExerciseChapter = (chapter) => {
  const notionId = chapter?.notionId || chapter?.id
  if (!notionId) return
  router.push({
    name: 'FreeExerciseChapter',
    params: { notionId },
    query: { title: chapter?.name || undefined }
  })
}
</script>

<template>
  <MainLayout>
    <div class="free-course-page">
      <BackButton text="Retour à l'accueil" :custom-action="() => router.push({ name: 'Home' })" position="top-left" />

      <div v-if="availableLevels.length > 0" class="filter-section">
        <button class="filter-toggle" @click="showLevelFilter = !showLevelFilter">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="filter-icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 01-.659 1.591l-5.432 5.432a2.25 2.25 0 00-.659 1.591v2.927a2.25 2.25 0 01-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 00-.659-1.591L3.659 7.409A2.25 2.25 0 013 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0112 3z" />
          </svg>
          Filtrer par niveau
          <span v-if="selectedLevels.length > 0" class="filter-badge">{{ selectedLevels.length }}</span>
        </button>
        
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
      <div v-else-if="themes.length === 0" class="state-card">
        {{ typeConfig.emptyLabel }}
      </div>
      <template v-else>
        <section v-for="theme in themes" :key="theme.id" class="theme-block">
          <div class="theme-header">
            <h2>{{ theme.name }}</h2>
            <span class="theme-count">
              {{
                isExerciseMode
                  ? formatCount(theme.totalCount, 'exercice')
                  : formatCount(theme.notions.length)
              }}
            </span>
          </div>

          <template v-if="isExerciseMode">
            <div class="notion-grid">
              <NotionCard
                v-for="chapter in theme.chapters"
                :key="chapter.id"
                :title="chapter.name"
                description="Cliquez pour explorer les exercices"
                :notion-id="chapter.notionId"
                :disable-prefetch="true"
                @click="openExerciseChapter(chapter)"
              >
                <template #meta>
                  <span class="resource-chapter-pill">
                    {{ formatCount(chapter.count || chapter.exercises.length, 'exercice') }}
                  </span>
                  <span
                    v-if="chapter.exercises[0]?.tag_secondaire"
                    class="resource-tag-pill"
                  >
                    {{ chapter.exercises[0].tag_secondaire }}
                  </span>
                </template>
              </NotionCard>
            </div>
          </template>

          <template v-else>
            <div class="notion-grid">
              <NotionCard
                v-for="resource in theme.notions"
                :key="resource.slug"
                :title="getCardTitle(resource)"
                :description="getCardDescription(resource)"
                :notion-id="resource.notion"
                :disable-prefetch="true"
                @click="openResource(resource)"
              >
                <template v-if="isSummaryMode" #meta>
                  <span
                    v-if="getSummaryLevel(resource)"
                    class="resource-chapter-pill"
                  >
                    {{ getSummaryLevel(resource) }}
                  </span>
                </template>
                <template v-else #meta>
                  <span v-if="resource.tag_secondaire" class="resource-tag-pill">
                    {{ resource.tag_secondaire }}
                  </span>
                </template>
              </NotionCard>
            </div>
          </template>
        </section>
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

.filter-section {
  position: relative;
  margin-bottom: 24px;
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

.theme-block {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e2e8f0;
}

.chapter-block {
  margin-bottom: 24px;
}

.chapter-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 8px 0 12px;
  padding: 8px 0;
}

.chapter-header h3 {
  margin: 0;
  font-size: 18px;
  color: #1e293b;
}

.chapter-count {
  font-size: 13px;
  font-weight: 600;
  color: #475569;
}

.theme-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.theme-header h2 {
  margin: 0;
  font-size: 22px;
  color: #0f172a;
}

.theme-count {
  font-size: 14px;
  color: #64748b;
  font-weight: 600;
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
.resource-tag-pill {
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

  .theme-block {
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 18px 16px;
    margin-bottom: 20px;
    box-shadow: 0 12px 28px rgba(15, 23, 42, 0.06);
    background: #fff;
  }

  .theme-header {
    flex-direction: row;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
  }

  .theme-header h2 {
    flex: 1;
    font-size: 1.05rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .theme-count {
    font-size: 0.78rem;
    padding: 3px 10px;
    background: #eef2ff;
    border-radius: 999px;
    color: #1d4ed8;
    white-space: nowrap;
  }

  .notion-grid {
    gap: 12px;
  }
}

@media (max-width: 420px) {
  .free-course-page {
    padding: 105px 12px 48px;
  }

  .theme-block {
    padding: 16px 14px;
  }

  .theme-header h2 {
    font-size: 1rem;
  }

  .theme-count {
    width: auto;
    font-size: 0.76rem;
  }
}
</style>
