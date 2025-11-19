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
    return resource?.accroche || resource?.excerpt || 'Cliquez pour lire la fiche'
  }
  return resource?.accroche || resource?.excerpt || 'Cliquez pour explorer ce chapitre'
}

const getAccessLabel = (resource) => {
  return resource?.badge || resource?.type_label || ''
}

const getChapterLabel = (resource) => {
  if (!resource) return ''
  if (isSummaryMode.value) {
    return resource?.niveau_nom || resource?.notion_nom || resource?.theme_nom || ''
  }
  return resource?.notion_nom || resource?.theme_nom || ''
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
</script>

<template>
  <MainLayout>
    <div class="free-course-page">
      <BackButton text="Retour à l'accueil" :custom-action="() => router.push({ name: 'Home' })" position="top-left" />

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
                <template #meta>
                  <span
                    v-if="typeConfig.chapterLabel && getChapterLabel(resource)"
                    class="resource-chapter-pill"
                  >
                    {{ typeConfig.chapterLabel }} : {{ getChapterLabel(resource) }}
                  </span>
                  <span
                    v-if="getAccessLabel(resource)"
                    class="resource-status-pill"
                  >
                    {{ getAccessLabel(resource) }}
                  </span>
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
  padding: 140px 24px 80px;
  max-width: 960px;
  margin: 0 auto;
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
</style>
