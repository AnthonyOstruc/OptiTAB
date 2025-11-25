<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import BackButton from '@/components/common/BackButton.vue'
import ExerciceQCM from '@/components/UI/ExerciceQCM.vue'
import { getFreeResources } from '@/api/free-content'
import { renderMath } from '@/utils/scientificRenderer'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const error = ref(null)
const exercises = ref([])
const notionTitle = ref(route.query.title || '')

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
  const baseHeight = `${contentHeight.value}px`
  let z = zoomLevel.value || 1
  if (viewportWidth.value <= 768) {
    z = Math.max(0.6, z - 0.08)
  }
  const widthPercent = (100 / z).toFixed(3)
  return {
    '--content-zoom': z,
    '--content-height': baseHeight,
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

const notionId = computed(() => route.params.notionId)

const formatCount = (count) => `${count} exercice${count > 1 ? 's' : ''}`

const displayedExercises = computed(() =>
  exercises.value.map((item, index) => ({
    id: item.id || item.slug || index,
    slug: item.slug,
    titre: item.titre || item.nom || `Exercice ${index + 1}`,
    instruction: item.question || item.contenu || item.accroche || '',
    solution: item.solution || item.reponse_correcte || '',
    etapes: item.etapes || '',
    difficulty: item.difficulty || item.difficulte || 'medium',
    previewImages: item.images || [],
    badge: item.badge,
    tag: item.tag_secondaire
  }))
)

const exercisesCount = computed(() => displayedExercises.value.length)

const fetchExercises = async () => {
  if (!notionId.value) return
  loading.value = true
  error.value = null
  try {
    const data = await getFreeResources({ type: 'exercise', notion: notionId.value })
    const list = Array.isArray(data?.results) ? data.results : data
    exercises.value = list
    if (!notionTitle.value && list?.length && list[0]?.notion_nom) {
      notionTitle.value = list[0].notion_nom
    }
    await nextTick()
    await safeRenderMath()
  } catch (err) {
    console.error('Erreur chargement exercices gratuits', err)
    error.value = err?.message || "Impossible de charger les exercices gratuits pour ce chapitre."
  } finally {
    loading.value = false
  }
}

const safeRenderMath = async () => {
  try {
    await renderMath()
  } catch (_) {
    // ignore math errors
  }
}

const goBack = () => {
  router.push({ name: 'FreeExercises' })
}

watch(
  () => route.params.notionId,
  () => {
    fetchExercises()
  }
)

watch(
  () => route.query.title,
  (value) => {
    if (value) notionTitle.value = value
  }
)

onMounted(() => {
  fetchExercises()
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

watch(() => zoomLevel.value, () => {
  nextTick(() => measureContentHeight())
})
</script>

<template>
  <MainLayout>
    <div class="free-exercise-chapter-page">
      <BackButton text="Retour aux exercices" :custom-action="goBack" position="top-left" />

      <div v-if="loading" class="state-card">
        Chargement des exercices gratuits...
      </div>
      <div v-else-if="error" class="state-card">
        <p>{{ error }}</p>
        <button @click="fetchExercises">Réessayer</button>
      </div>
      <div v-else-if="displayedExercises.length === 0" class="state-card">
        Aucun exercice gratuit n'est disponible pour ce chapitre pour le moment.
      </div>
      <div v-else class="content-wrapper" :style="zoomStyle" ref="contentRef">
        <div class="exercise-stack">
          <div
            v-for="(exercise, index) in displayedExercises"
            :key="exercise.id"
            class="exercise-card-wrapper"
          >
            <ExerciceQCM
              :eid="exercise.id"
              :titre="exercise.titre"
              :instruction="exercise.instruction"
              :solution="exercise.solution"
              :etapes="exercise.etapes"
              :difficulty="exercise.difficulty"
              :preview-images="exercise.previewImages"
              readonly
            />
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<style scoped>
.free-exercise-chapter-page {
  min-height: 100vh;
  background: #fff;
  padding: 140px 24px 80px;
  width: 100%;
  max-width: none;
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

.exercise-stack {
  display: flex;
  flex-direction: column;
  gap: 32px;
  width: 100%;
}

.exercise-card-wrapper {
  padding: 0;
  border: none;
  border-radius: 0;
  background: transparent;
  box-shadow: none;
}

@media (max-width: 768px) {
  .free-exercise-chapter-page {
    padding: 120px 16px 60px;
  }

  .exercise-card-wrapper {
    padding: 18px;
  }
}
</style>
