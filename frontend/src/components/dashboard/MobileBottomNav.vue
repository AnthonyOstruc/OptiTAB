<template>
  <nav class="mobile-bottom-nav" aria-label="Navigation principale mobile">
    <button
      v-for="item in navItems"
      :key="item.key"
      type="button"
      :class="['mobile-nav-item', { active: isActive(item) }]"
      :data-cta-name="item.key === 'abonnement' ? 'subscribe' : null"
      :data-cta-location="item.key === 'abonnement' ? 'nav_bottom' : null"
      @click.stop="handleClick(item)"
      @touchend.stop.prevent="handleTouch(item, $event)"
      :aria-label="item.text"
    >
      <component :is="item.icon" class="mobile-nav-icon" />
    </button>
  </nav>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import dashboardMenu from '@/config/dashboardMenu'
import { useSubjectsStore } from '@/stores/subjects/index'
import { useUserStore } from '@/stores/user'
import { useDataPrefetch } from '@/composables/useDataPrefetch'
import { getSynthesisSheets } from '@/api/synthesis'

const router = useRouter()
const route = useRoute()

const subjectsStore = useSubjectsStore()
const userStore = useUserStore()
const { prefetchThemesNotions } = useDataPrefetch()

const showTablesFormules = ref(false)
let tablesVisibilityRequestId = 0

const currentMatiereId = computed(() => {
  const routeMatiereIdRaw = route.query?.matiereId
  const routeMatiereId = Array.isArray(routeMatiereIdRaw) ? routeMatiereIdRaw[0] : routeMatiereIdRaw
  const activeId = subjectsStore.activeMatiereId || subjectsStore.selectedMatieresIds?.[0] || routeMatiereId

  if (activeId === undefined || activeId === null || activeId === '') {
    return null
  }

  return String(activeId)
})

const extractSheetCount = (payload) => {
  if (Array.isArray(payload)) return payload.length
  if (Array.isArray(payload?.results)) return payload.results.length
  if (typeof payload?.count === 'number') return payload.count
  return 0
}

const refreshTablesFormulesVisibility = async () => {
  if (!userStore.isAuthenticated) {
    showTablesFormules.value = false
    return
  }

  if (userStore.isAdmin) {
    showTablesFormules.value = true
    return
  }

  const matiereId = currentMatiereId.value
  if (!matiereId) {
    showTablesFormules.value = false
    return
  }

  const requestId = ++tablesVisibilityRequestId
  try {
    const response = await getSynthesisSheets({
      matiere: matiereId,
      sheet_type: 'table',
      limit: 1
    })
    if (requestId !== tablesVisibilityRequestId) return
    showTablesFormules.value = extractSheetCount(response?.data) > 0
  } catch (_) {
    if (requestId !== tablesVisibilityRequestId) return
    showTablesFormules.value = false
  }
}

watch(
  [() => userStore.isAuthenticated, () => userStore.isAdmin, currentMatiereId],
  () => {
    refreshTablesFormulesVisibility()
  },
  { immediate: true }
)

const navItems = computed(() =>
  dashboardMenu
    .filter(item => item.key !== 'tables-formules' || showTablesFormules.value)
    .map(item => ({
      key: item.key,
      text: item.text,
      href: item.href,
      icon: item.icon
    }))
)

const routeMapping = {
  dashboard: '/dashboard',
  cours: ['/online-courses', '/course-notions', '/course-notion', '/cours'],
  exercices: ['/exercises', '/notions', '/exercicies', '/theme-notions', '/exercices-notion', '/exercices', '/chapter-exercises'],
  fiches: ['/sheets', '/sheets-notion'],
  'tables-formules': ['/tables-formules', '/tables-formules-notion'],
  quiz: ['/quiz', '/quiz-notions', '/quiz-notion', '/chapter-quiz'],
  calculator: '/calculator',
  blog: '/blog',
  abonnement: ['/billing']
}

const isActive = (item) => {
  const currentPath = route.path
  const match = routeMapping[item.key]
  if (!match) return currentPath.startsWith(item.href)
  if (Array.isArray(match)) return match.some(path => currentPath.startsWith(path))
  return currentPath.startsWith(match)
}

const handleClick = async (item) => {
  if (!item) return

  // Simple routes without subject context
  if (item.key === 'dashboard') {
    router.push('/dashboard').catch(() => {})
    return
  }
  if (item.key === 'calculator') {
    router.push('/calculator').catch(() => {})
    return
  }
  if (item.key === 'blog') {
    router.push('/blog').catch(() => {})
    return
  }
  if (item.key === 'abonnement') {
    router.push('/billing').catch(() => {})
    return
  }

  // Contextual routes with subject
  if (['exercices', 'fiches', 'tables-formules', 'quiz', 'cours'].includes(item.key)) {
    const activeId = subjectsStore.activeMatiereId || subjectsStore.selectedMatieresIds?.[0] || null

    if (item.key === 'exercices') {
      if (activeId) {
        try { await prefetchThemesNotions(activeId) } catch (_) {}
        router.push({ name: 'Themes', params: { matiereId: String(activeId) } }).catch(() => {})
      } else {
        router.push({ name: 'Exercises' }).catch(() => {})
      }
      return
    }

    if (item.key === 'fiches') {
      if (activeId) {
        router.push({ name: 'Sheets', query: { matiereId: String(activeId) } }).catch(() => {})
      } else {
        router.push({ name: 'Sheets' }).catch(() => {})
      }
      return
    }

    if (item.key === 'tables-formules') {
      if (activeId) {
        router.push({ name: 'TablesFormules', query: { matiereId: String(activeId) } }).catch(() => {})
      } else {
        router.push({ name: 'TablesFormules' }).catch(() => {})
      }
      return
    }

    if (item.key === 'quiz') {
      if (activeId) {
        try { await prefetchThemesNotions(activeId) } catch (_) {}
        router.push({ name: 'QuizNotions', params: { matiereId: String(activeId) } }).catch(() => {})
      } else {
        router.push({ name: 'Quiz' }).catch(() => {})
      }
      return
    }

    if (item.key === 'cours') {
      if (activeId) {
        try { await prefetchThemesNotions(activeId) } catch (_) {}
        router.push({ name: 'CourseNotions', params: { matiereId: String(activeId) } }).catch(() => {})
      } else {
        router.push({ name: 'OnlineCourses' }).catch(() => {})
      }
      return
    }
  }

  // Fallback
  if (item.href) router.push(item.href).catch(() => {})
}

// Handle touch events to prevent click-through on mobile
const handleTouch = async (item, event) => {
  // Prevent the touch event from triggering elements below
  if (event) {
    event.stopPropagation()
    event.preventDefault()
  }
  await handleClick(item)
}
</script>

<style scoped>
.mobile-bottom-nav {
  /* Footer FIXE en bas - ne bouge jamais */
  position: fixed !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 0.65rem 1.25rem calc(env(safe-area-inset-bottom) + 0.65rem);
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(12px);
  border-top: 1px solid rgba(226, 232, 240, 0.9);
  box-shadow: 0 -6px 24px rgba(15, 23, 42, 0.08);
  z-index: 10000;
  /* Block all click events on the footer area to prevent click-through */
  pointer-events: auto;
  /* Visual stability of fixed element on iOS */
  -webkit-tap-highlight-color: transparent;
  -webkit-user-select: none;
  user-select: none;
  /* Improve compositing stability on iOS fixed elements */
  -webkit-transform: translateZ(0);
  transform: translateZ(0);
  /* Empêcher complètement le scroll depuis la barre */
  touch-action: none;
  overscroll-behavior: contain;
  /* Force le navigateur à garder cet élément fixe même pendant le scroll */
  will-change: transform;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
}

/* Bloquer le scroll sur tous les enfants du footer */
.mobile-bottom-nav * {
  touch-action: none;
}

.mobile-nav-item {
  background: none;
  border: none;
  padding: 0.4rem;
  border-radius: 12px;
  color: #94a3b8;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s ease, transform 0.2s ease, background 0.2s ease;
  cursor: pointer;
  /* Re-enable events for interactive buttons */
  pointer-events: auto;
  /* Avoid double-tap zoom on supported iOS versions */
  touch-action: manipulation;
}

.mobile-nav-item:hover {
  color: #1d4ed8;
  transform: translateY(-2px);
}

.mobile-nav-item.active {
  color: #1d4ed8;
  background: rgba(59, 130, 246, 0.12);
}

.mobile-nav-icon {
  width: 24px;
  height: 24px;
}

@media (min-width: 769px) {
  .mobile-bottom-nav {
    display: none;
  }
}
</style>
