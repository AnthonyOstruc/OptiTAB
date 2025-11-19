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
      counterLabel: 'exercice'
    }
  }
  return {
    slugRoute: 'FreeCourseDetail',
    fallback: 'Chapitres à découvrir',
    emptyLabel: 'Aucun chapitre gratuit disponible pour le moment.',
    counterLabel: 'chapitre'
  }
})

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

  const groups = new Map()
  const fallbackTitle = typeConfig.value.fallback

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

const formatCount = (count) => {
  const label = typeConfig.value.counterLabel || 'ressource'
  return `${count} ${label}${count > 1 ? 's' : ''}`
}

const openResource = (resource) => {
  if (!resource?.slug) return
  router.push({ name: typeConfig.value.slugRoute, params: { slug: resource.slug } })
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
              {{ formatCount(theme.notions.length) }}
            </span>
          </div>
          <div class="notion-grid">
            <NotionCard
              v-for="resource in theme.notions"
              :key="resource.slug"
              :title="resource.titre"
              :notion-id="resource.notion"
              :disable-prefetch="true"
              @click="openResource(resource)"
            />
          </div>
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
