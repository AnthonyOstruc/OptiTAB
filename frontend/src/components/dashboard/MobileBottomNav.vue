<template>
  <nav class="mobile-bottom-nav" aria-label="Navigation principale mobile">
    <button
      v-for="item in navItems"
      :key="item.key"
      type="button"
      :class="['mobile-nav-item', { active: isActive(item) }]"
      @click.stop="handleClick(item)"
      @touchend.stop.prevent="handleTouch(item, $event)"
      :aria-label="item.text"
    >
      <component :is="item.icon" class="mobile-nav-icon" />
    </button>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import dashboardMenu from '@/config/dashboardMenu'
import { useSubjectsStore } from '@/stores/subjects/index'
import { useUserStore } from '@/stores/user'
import { useDataPrefetch } from '@/composables/useDataPrefetch'

const router = useRouter()
const route = useRoute()

const navItems = computed(() =>
  dashboardMenu.map(item => ({
    key: item.key,
    text: item.text,
    href: item.href,
    icon: item.icon
  }))
)

const subjectsStore = useSubjectsStore()
const userStore = useUserStore()
const { prefetchThemesNotions } = useDataPrefetch()

const routeMapping = {
  dashboard: '/dashboard',
  cours: ['/online-courses', '/course-notions', '/course-notion', '/cours'],
  exercices: ['/exercises', '/notions', '/exercicies', '/theme-notions', '/exercices-notion', '/exercices', '/chapter-exercises'],
  fiches: ['/sheets', '/sheets-notion'],
  quiz: ['/quiz', '/quiz-notions', '/quiz-notion', '/chapter-quiz'],
  calculator: '/calculator',
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
  if (item.key === 'abonnement') {
    router.push('/billing').catch(() => {})
    return
  }

  // Contextual routes with subject
  if (['exercices', 'fiches', 'quiz', 'cours'].includes(item.key)) {
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
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 0.65rem 1.25rem calc(env(safe-area-inset-bottom) + 0.65rem);
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(12px);
  border-top: 1px solid rgba(226, 232, 240, 0.9);
  box-shadow: 0 -6px 24px rgba(15, 23, 42, 0.08);
  z-index: 1050;
  /* Block all click events on the footer area to prevent click-through */
  pointer-events: auto;
  /* Visual stability of fixed element on iOS */
  -webkit-tap-highlight-color: transparent;
  -webkit-user-select: none;
  user-select: none;
  /* Improve compositing stability on iOS fixed elements */
  -webkit-transform: translateZ(0);
  transform: translateZ(0);
  /* Empêcher complètement le scroll depuis la barre - CRITIQUE pour iOS */
  touch-action: none;
  overscroll-behavior: contain;
  /* Force le navigateur à garder cet élément fixe même pendant le scroll */
  will-change: transform;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
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
