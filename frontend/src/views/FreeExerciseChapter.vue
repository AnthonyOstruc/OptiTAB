<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import BackButton from '@/components/common/BackButton.vue'
import ExerciceQCM from '@/components/UI/ExerciceQCM.vue'
import { getFreeResources } from '@/api/free-content'
import { renderMath } from '@/utils/scientificRenderer'
import { useZoom } from '@/composables/useZoom'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const error = ref(null)
const exercises = ref([])
const notionTitle = ref(route.query.title || '')
const currentPage = ref(1)
const itemsPerPage = 5

const contentRef = ref(null)

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

const zoomStyle = createZoomStyle({
  cssVar: '--content-zoom',
  heightVar: '--content-height',
  mobileZoomAdjustment: (z) => Math.max(0.6, z - 0.08)
})

function measureContentHeightForFreeExercises() {
  measureContentHeight(contentRef)
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
    tag: item.tag_secondaire,
    _locked: Boolean(item.is_locked)
  }))
)

const exercisesCount = computed(() => displayedExercises.value.length)

const orderedExercises = computed(() => {
  const unlocked = displayedExercises.value.filter((ex) => !ex._locked)
  const locked = displayedExercises.value.filter((ex) => ex._locked)
  return [...unlocked, ...locked]
})

const totalPages = computed(() =>
  Math.max(1, Math.ceil((orderedExercises.value.length || 0) / itemsPerPage))
)

const paginatedExercises = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return orderedExercises.value.slice(start, start + itemsPerPage)
})

const fetchExercises = async () => {
  if (!notionId.value) return
  loading.value = true
  error.value = null
  try {
    const data = await getFreeResources({ type: 'exercise', notion: notionId.value })
    const list = Array.isArray(data?.results) ? data.results : data
    exercises.value = list
    currentPage.value = 1
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
  detectMobileAndZoomSupport()
  updateViewportWidth()
  setupViewportListener()
  fetchExercises()
})

onBeforeUnmount(() => {
  cleanupViewportListener()
})

watch(viewportWidth, () => {
  nextTick(() => measureContentHeightForFreeExercises())
})

const goToPage = (page) => {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  nextTick(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
    measureContentHeightForFreeExercises()
  })
}
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
        <div class="exercise-stack" v-if="displayedExercises.length > 0">
          <div
            v-for="(exercise, index) in paginatedExercises"
            :key="exercise.id || exercise.slug || index"
            class="exercise-card-wrapper"
            :class="{ 'locked-tabs': exercise._locked }"
          >
            <div v-if="exercise._locked" class="locked-pill">Exercice premium</div>
            <ExerciceQCM
              :eid="exercise.id || exercise.slug || index"
              :titre="exercise.titre"
              :instruction="exercise._locked ? `<span class='locked-blur'>${exercise.instruction}</span>` : exercise.instruction"
              :solution="exercise.solution"
              :etapes="exercise.etapes"
              :difficulty="exercise.difficulty"
              :preview-images="exercise.previewImages"
              readonly
            />
          </div>
          <div v-if="totalPages > 1" class="pagination">
            <button
              class="pagination-btn"
              :disabled="currentPage === 1"
              @click="goToPage(currentPage - 1)"
            >
              &larr;
            </button>
            <span class="pagination-text">Page {{ currentPage }} / {{ totalPages }}</span>
            <button
              class="pagination-btn"
              :disabled="currentPage === totalPages"
              @click="goToPage(currentPage + 1)"
            >
              &rarr;
            </button>
          </div>
        </div>
        <div v-else class="state-card">
          Aucun exercice gratuit n'est disponible pour ce chapitre pour le moment.
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

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: 16px;
}

.pagination-btn {
  border: 1px solid #e2e8f0;
  background: #fff;
  color: #1e293b;
  padding: 8px 12px;
  border-radius: 10px;
  cursor: pointer;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-text {
  font-weight: 700;
  color: #0f172a;
}

.locked-pill {
  position: absolute;
  top: 12px;
  right: 12px;
  background: #eef2ff;
  color: #1d4ed8;
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  border: 1px solid rgba(59, 130, 246, 0.4);
  z-index: 2;
}

.locked-tabs {
  position: relative;
}

:deep(.locked-blur) {
  filter: blur(2px);
  display: inline-block;
  position: relative;
}

:deep(.locked-blur)::after {
  content: ' 🔒';
  color: #1d4ed8;
  font-weight: 700;
}

:deep(.locked-tabs .tabs-container .tab-btn:nth-child(2)),
:deep(.locked-tabs .tabs-container .tab-btn:nth-child(3)) {
  position: relative;
  overflow: hidden;
}

:deep(.locked-tabs .tabs-container .tab-btn:nth-child(2)::after),
:deep(.locked-tabs .tabs-container .tab-btn:nth-child(3)::after) {
  content: '🔒';
  margin-left: 6px;
  font-size: 12px;
}

:deep(.locked-tabs .tabs-container .tab-btn:nth-child(2)),
:deep(.locked-tabs .tabs-container .tab-btn:nth-child(3)) {
  opacity: 0.8;
  pointer-events: none;
}

:deep(.locked-tabs .steps-section),
:deep(.locked-tabs .answer-section) {
  position: relative;
  filter: blur(2px);
  pointer-events: none;
}

:deep(.locked-tabs .steps-section::after),
:deep(.locked-tabs .answer-section::after) {
  content: 'Section réservée aux abonnés';
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, rgba(255,255,255,0.86), rgba(255,255,255,0.92));
  color: #1d4ed8;
  font-weight: 700;
  border: 1px dashed #cbd5f5;
  border-radius: 12px;
}

:deep(.locked-tabs .problem-section .problem-content) {
  position: relative;
}

:deep(.locked-tabs .problem-section .problem-content > :nth-of-type(n+3)) {
  filter: blur(5px);
  opacity: 0.35;
  pointer-events: none;
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
