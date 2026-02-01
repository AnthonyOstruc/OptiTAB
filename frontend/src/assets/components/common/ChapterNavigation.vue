<template>
  <nav class="chapter-navigation" aria-label="Navigation des chapitres">
    <button 
      v-for="tab in tabs" 
      :key="tab.key"
      :class="['chapter-nav-btn', { active: tab.key === activeTab }]"
      :aria-pressed="tab.key === activeTab"
      :aria-label="tab.label"
      @click="handleTabClick(tab.key)"
      @mouseenter="prefetchTab(tab.key)"
    >
      <component :is="tab.icon" class="chapter-nav-icon" />
      <span class="chapter-nav-label">{{ tab.label }}</span>
    </button>
  </nav>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  BookOpenIcon, 
  AcademicCapIcon, 
  QuestionMarkCircleIcon,
  DocumentTextIcon
} from '@heroicons/vue/24/outline'
// Prefetch APIs to warm cache on hover
import { getCours } from '@/api/cours'
import { getExercices } from '@/api'
import { getQuiz } from '@/api/quiz'
import { getSynthesisSheets } from '@/api/synthesis'

// Props
const props = defineProps({
  chapitreId: {
    type: [String, Number],
    required: false,
    default: null
  }
})

const route = useRoute()
const router = useRouter()

// Navigation tabs configuration
const tabs = computed(() => {
  const currentPath = route.path
  const notionId = route.params.notionId
  const chapitreId = null // chapitres supprimés
  const matiereId = route.params.matiereId
  
  // Cas 1: On est dans un chapitre spécifique (avec chapitreId) - PRIORITÉ MAXIMALE
  // Cas chapitres supprimés → pas de tabs par chapitre
  
  // Cas 2: On est dans une notion spécifique (liste des chapitres)
  if (notionId && currentPath.includes('/exercices-notion/')) {
    return [
      { 
        key: 'cours', 
        label: 'Cours', 
        icon: BookOpenIcon,
        route: `/course-notion/${notionId}`
      },
      { 
        key: 'sheets', 
        label: 'Synthèse', 
        icon: DocumentTextIcon,
        route: `/sheets-notion/${notionId}`
      },
      { 
        key: 'exercices', 
        label: 'Exercices', 
        icon: AcademicCapIcon,
        route: `/exercices-notion/${notionId}`
      },
      { 
        key: 'quiz', 
        label: 'Quiz', 
        icon: QuestionMarkCircleIcon,
        route: `/quiz-notion/${notionId}`
      }
    ]
  }
  
  // Cas 3: On est dans une matière (liste des notions)
  if (matiereId && currentPath.includes('/notions/')) {
    return [
      { 
        key: 'cours', 
        label: 'Cours', 
        icon: BookOpenIcon,
        route: `/course-notions/${matiereId}`
      },
      { 
        key: 'sheets', 
        label: 'Synthèse', 
        icon: DocumentTextIcon,
        route: `/sheets?matiereId=${matiereId}`
      },
      { 
        key: 'exercices', 
        label: 'Exercices', 
        icon: AcademicCapIcon,
        route: `/notions/${matiereId}`
      },
      { 
        key: 'quiz', 
        label: 'Quiz', 
        icon: QuestionMarkCircleIcon,
        route: `/quiz/${matiereId}`
      }
    ]
  }
  
  // Cas 4: On est dans une notion de cours (liste des chapitres de cours)
  if (notionId && currentPath.includes('/course-notion/')) {
    return [
      { 
        key: 'cours', 
        label: 'Cours', 
        icon: BookOpenIcon,
        route: `/course-notion/${notionId}`
      },
      { 
        key: 'sheets', 
        label: 'Synthèse', 
        icon: DocumentTextIcon,
        route: `/sheets-notion/${notionId}`
      },
      { 
        key: 'exercices', 
        label: 'Exercices', 
        icon: AcademicCapIcon,
        route: `/exercices-notion/${notionId}`
      },
      { 
        key: 'quiz', 
        label: 'Quiz', 
        icon: QuestionMarkCircleIcon,
        route: `/quiz-notion/${notionId}`
      }
    ]
  }
  
  // Cas 5: On est dans une notion de quiz
  if (notionId && currentPath.includes('/quiz-notion/')) {
    return [
      { 
        key: 'cours', 
        label: 'Cours', 
        icon: BookOpenIcon,
        route: `/course-notion/${notionId}`
      },
      { 
        key: 'sheets', 
        label: 'Synthèse', 
        icon: DocumentTextIcon,
        route: `/sheets-notion/${notionId}`
      },
      { 
        key: 'exercices', 
        label: 'Exercices ', 
        icon: AcademicCapIcon,
        route: `/exercices-notion/${notionId}`
      },
      { 
        key: 'quiz', 
        label: 'Quiz', 
        icon: QuestionMarkCircleIcon,
        route: `/quiz-notion/${notionId}`
      }
    ]
  }

  // Cas 6: On est dans une notion de synthèse (fiches)
  if (notionId && currentPath.includes('/sheets-notion/')) {
    return [
      { 
        key: 'cours', 
        label: 'Cours', 
        icon: BookOpenIcon,
        route: `/course-notion/${notionId}`
      },
      { 
        key: 'sheets', 
        label: 'Synthèse', 
        icon: DocumentTextIcon,
        route: `/sheets-notion/${notionId}`
      },
      { 
        key: 'exercices', 
        label: 'Exercices', 
        icon: AcademicCapIcon,
        route: `/exercices-notion/${notionId}`
      },
      { 
        key: 'quiz', 
        label: 'Quiz', 
        icon: QuestionMarkCircleIcon,
        route: `/quiz-notion/${notionId}`
      }
    ]
  }
  
  // Cas 6: On est dans un cours de notion
  if (matiereId && currentPath.includes('/course-notions/')) {
    return [
      { 
        key: 'cours', 
        label: 'Cours', 
        icon: BookOpenIcon,
        route: `/course-notions/${matiereId}`
      },
      { 
        key: 'sheets', 
        label: 'Synthèse', 
        icon: DocumentTextIcon,
        route: `/sheets?matiereId=${matiereId}`
      },
      { 
        key: 'exercices', 
        label: 'Exercices', 
        icon: AcademicCapIcon,
        route: `/notions/${matiereId}`
      },
      { 
        key: 'quiz', 
        label: 'Quiz', 
        icon: QuestionMarkCircleIcon,
        route: `/quiz/${matiereId}`
      }
    ]
  }
  
  // Cas 7: On est dans un quiz de matière
  if (matiereId && currentPath.includes('/quiz/')) {
    return [
      { 
        key: 'cours', 
        label: 'Cours', 
        icon: BookOpenIcon,
        route: `/course-notions/${matiereId}`
      },
      { 
        key: 'sheets', 
        label: 'Synthèse', 
        icon: DocumentTextIcon,
        route: `/sheets?matiereId=${matiereId}`
      },
      { 
        key: 'exercices', 
        label: 'Exercices ', 
        icon: AcademicCapIcon,
        route: `/notions/${matiereId}`
      },
      { 
        key: 'quiz', 
        label: 'Quiz', 
        icon: QuestionMarkCircleIcon,
        route: `/quiz/${matiereId}`
      }
    ]
  }
  
  // Fallback pour les autres cas (pages générales)
  return [
    { 
      key: 'cours', 
      label: 'Cours', 
      icon: BookOpenIcon,
      route: '/online-courses'
    },
    { 
      key: 'sheets', 
      label: 'Synthèse', 
      icon: DocumentTextIcon,
      route: '/sheets'
    },
    { 
      key: 'exercices', 
      label: 'Exercices', 
      icon: AcademicCapIcon,
      route: '/exercises'
    },
    { 
      key: 'quiz', 
      label: 'Quiz', 
      icon: QuestionMarkCircleIcon,
      route: '/quiz'
    }
  ]
})

// Active tab state
const activeTab = ref('exercices')

// Function to update active tab based on current route
function updateActiveTab() {
  const currentPath = route.path
  const chapitreId = props.chapitreId || route.params.chapitreId
  
  // Détection intelligente de l'onglet actif avec priorité pour les chapitres spécifiques
  if (chapitreId && chapitreId !== null) {
    // Navigation à l'intérieur d'un chapitre spécifique
    if (currentPath.includes(`/course/${chapitreId}`)) {
      activeTab.value = 'cours'
    } else if (currentPath.includes(`/exercices/${chapitreId}`)) {
      activeTab.value = 'exercices'
    } else if (currentPath.includes(`/quiz-exercices/${chapitreId}`)) {
      activeTab.value = 'quiz'
    } else if (currentPath.includes(`/sheets/${chapitreId}`)) {
      activeTab.value = 'sheets'
    } else {
      // Si on est dans un chapitre mais pas sur une route spécifique, on reste sur exercices par défaut
      activeTab.value = 'exercices'
    }
  } else {
    // Navigation générale (notions, matières, etc.)
    if (currentPath.includes('/course-notion/') || currentPath.includes('/course-notions/')) {
      activeTab.value = 'cours'
    } else if (currentPath.includes('/exercices-notion/') || currentPath.includes('/notions/')) {
      activeTab.value = 'exercices'
    } else if (currentPath.includes('/sheets-notion/') || currentPath.includes('/sheets')) {
      activeTab.value = 'sheets'
    } else if (currentPath.includes('/quiz-notion/') || 
               (currentPath.includes('/quiz/') && route.params.matiereId)) {
      activeTab.value = 'quiz'
    } else {
      // Fallback : essayer de détecter par défaut
      activeTab.value = 'exercices'
    }
  }
}

// Determine active tab based on current route
onMounted(() => {
  updateActiveTab()
})

// Watch for route changes
watch(() => route.path, () => {
  updateActiveTab()
})

// Prefetch data for a tab (warms in-memory cache)
function prefetchTab(key) {
  const notionId = route.params.notionId
  const matiereId = route.params.matiereId || route.query?.matiereId
  if (!notionId) return
  try {
    if (key === 'cours') {
      getCours(null, notionId)
    } else if (key === 'exercices') {
      getExercices({ notion: notionId })
    } else if (key === 'quiz') {
      getQuiz(notionId)
    } else if (key === 'sheets') {
      if (notionId) {
        getSynthesisSheets({ notion: notionId })
      } else if (matiereId) {
        getSynthesisSheets({ matiere: matiereId })
      } else {
        getSynthesisSheets()
      }
    }
  } catch (_) {}
}

// Handle tab navigation
function handleTabClick(tabKey) {
  const tab = tabs.value.find(t => t.key === tabKey)
  if (tab) {
    // Mise à jour immédiate de l'onglet actif pour un feedback visuel instantané
    activeTab.value = tabKey
    
    // Sauvegarder la position de scroll de la page actuelle pour une meilleure reprise
    try {
      const notionId = route.params.notionId
      const pageType =
        route.path.includes('/exercices-notion/') ? 'exercices' :
        route.path.includes('/course-notion/') ? 'cours' :
        route.path.includes('/quiz-notion/') ? 'quiz' :
        route.path.includes('/sheets-notion/') ? 'sheets' : null
      if (pageType && notionId) {
        const key = `optitab_scroll_${pageType}_${notionId}`
        const state = { scrollY: window.scrollY || window.pageYOffset || 0, t: Date.now() }
        sessionStorage.setItem(key, JSON.stringify(state))
      }
    } catch (_) {}

    // Navigation avec transition fluide
    router.push({
      path: tab.route,
      replace: false // Permet l'utilisation du bouton retour
    }).catch(err => {
      // Gestion des erreurs de navigation
      console.warn('Navigation error:', err)
      // Si la navigation échoue, on revient à l'onglet précédent
      updateActiveTab()
    })
  }
}
</script>

<style scoped>
.chapter-navigation {
  display: flex;
  gap: 0.25rem;
  align-items: center;
  background: rgba(255, 255, 255, 0.9);
  padding: 0.375rem;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(226, 232, 240, 0.8);
  backdrop-filter: blur(8px);
  max-width: fit-content;
  margin: 0 auto;
}

.chapter-nav-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  background: transparent;
  border-radius: 8px;
  color: #64748b;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  position: relative;
}

.chapter-nav-btn:hover {
  background: rgba(248, 250, 252, 0.8);
  color: #334155;
}

/* Info-bulle pédagogique au survol */
.chapter-nav-btn:hover::after {
  content: attr(aria-label);
  position: absolute;
  bottom: -32px;
  left: 50%;
  transform: translateX(-50%);
  background: #1f2937;
  color: #fff;
  font-size: 11px;
  padding: 4px 8px;
  border-radius: 4px;
  white-space: nowrap;
  box-shadow: 0 4px 12px rgba(0,0,0,.15);
  pointer-events: none;
  z-index: 10;
}

.chapter-nav-btn.active {
  background: #3b82f6;
  color: white;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.chapter-nav-btn:focus-visible {
  outline: 3px solid rgba(37, 99, 235, 0.4);
  outline-offset: 2px;
}

.chapter-nav-icon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.chapter-nav-label {
  font-weight: 500;
  letter-spacing: 0.025em;
}

/* Responsive design */
@media (max-width: 768px) {
  .chapter-navigation {
    gap: 0.125rem;
    padding: 0.25rem;
  }
  
  .chapter-nav-btn {
    padding: 0.625rem 0.875rem;
    gap: 0.375rem;
    font-size: 0.8rem;
  }
  
  .chapter-nav-label {
    font-size: 0.8rem;
  }
  
  .chapter-nav-icon {
    width: 1.125rem;
    height: 1.125rem;
  }
}

@media (max-width: 480px) {
  .chapter-nav-btn {
    padding: 0.5rem 0.75rem;
    gap: 0.25rem;
  }
  
  .chapter-nav-label {
    font-size: 0.75rem;
  }
  
  .chapter-nav-icon {
    width: 1rem;
    height: 1rem;
  }
}

@media (max-width: 450px) {
  .chapter-nav-label {
    display: none;
  }
  
  .chapter-nav-btn {
    padding: 0.5rem;
    min-width: 2.5rem;
    justify-content: center;
  }
  
  .chapter-nav-icon {
    width: 1.125rem;
    height: 1.125rem;
  }
}
</style> 
