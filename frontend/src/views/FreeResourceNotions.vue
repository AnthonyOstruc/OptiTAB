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

const resourceTabs = [
  { label: 'Cours', routeName: 'FreeCourses', resourceType: 'course', icon: '📖' },
  { label: 'Exercices', routeName: 'FreeExercises', resourceType: 'exercise', icon: '✏️' },
  { label: 'Synthèse', routeName: 'FreeSummaries', resourceType: 'summary', icon: '📄' }
]

const currentResourceType = computed(() => props.resourceType)

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
})

const themes = computed(() => {
  if (!resources.value.length) {
    return []
  }

  const fallbackTitle = typeConfig.value.fallback

  if (isExerciseMode.value) {
    const themeGroups = new Map()
    resources.value.forEach((item, index) => {
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
  resources.value.forEach((item, index) => {
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

const goToTab = (tab) => {
  if (!tab || tab.resourceType === props.resourceType) return
  router.push({ name: tab.routeName })
}
</script>

<template>
  <MainLayout>
    <div class="free-course-page">
      <BackButton text="Retour à l'accueil" :custom-action="() => router.push({ name: 'Home' })" position="top-left" />

      <nav class="resource-tab-bar" aria-label="Types de ressources gratuites">
        <button
          v-for="tab in resourceTabs"
          :key="tab.resourceType"
          class="resource-tab"
          :class="{ active: tab.resourceType === currentResourceType }"
          type="button"
          @click="goToTab(tab)"
        >
          <span class="tab-icon">{{ tab.icon }}</span>
          <span class="tab-label">{{ tab.label }}</span>
        </button>
      </nav>

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
  background: #fff;
  padding: 140px 32px 80px;
  max-width: 1200px;
  margin-left: 0;
  margin-right: auto;
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

.resource-tab-bar {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin: 1.5rem 0 2rem 0;
}

.resource-tab {
  background: #ffffff;
  border: 1.5px solid #d1d5db;
  border-radius: 8px;
  padding: 0.65rem 1.25rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  text-align: center;
  font-weight: 500;
  font-size: 0.9rem;
  color: #374151;
  white-space: nowrap;
}

.resource-tab::before {
  display: none;
}

.resource-tab:hover {
  border-color: #3b82f6;
  background: #f8fafc;
  transform: translateY(-1px);
}

.resource-tab.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.25);
}

.resource-tab.active:hover {
  background: #2563eb;
  transform: translateY(-1px);
}

.tab-icon {
  font-size: 1.1rem;
  line-height: 1;
  transition: none;
  filter: none;
}

.resource-tab:hover .tab-icon {
  transform: none;
}

.resource-tab.active .tab-icon {
  transform: none;
  filter: none;
}

.tab-label {
  font-weight: 500;
  font-size: 0.9rem;
  color: inherit;
  transition: none;
  letter-spacing: 0;
}

.resource-tab.active .tab-label {
  color: #ffffff;
  font-weight: 600;
}

@media (max-width: 768px) {
  .resource-tab-bar {
    display: flex;
    width: 100%;
    justify-content: center;
    flex-wrap: wrap;
  }
  
  .resource-tab {
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
  }
  
  .tab-icon {
    font-size: 1rem;
  }
  
  .tab-label {
    font-size: 0.85rem;
  }
}

@media (max-width: 480px) {
  .resource-tab {
    padding: 0.55rem 0.9rem;
    font-size: 0.8rem;
  }
  
  .tab-icon {
    font-size: 0.95rem;
  }
  
  .tab-label {
    font-size: 0.8rem;
  }
}
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
</style>
