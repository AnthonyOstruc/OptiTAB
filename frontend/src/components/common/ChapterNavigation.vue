<template>
  <nav class="chapter-navigation" aria-label="Navigation des chapitres">
    <button 
      v-for="tab in tabs" 
      :key="tab.key"
      :class="['chapter-nav-btn', { active: tab.key === activeTab }]"
      :aria-pressed="tab.key === activeTab"
      :aria-label="tab.label"
      @click="handleTabClick(tab.key)"
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
  QuestionMarkCircleIcon 
} from '@heroicons/vue/24/outline'

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
  const chapitreId = props.chapitreId || route.params.chapitreId
  const matiereId = route.params.matiereId
  
  // Cas 1: On est dans un chapitre spécifique (avec chapitreId) - PRIORITÉ MAXIMALE
  if (chapitreId && chapitreId !== null) {
    return [
      { 
        key: 'cours', 
        label: 'Cours', 
        icon: BookOpenIcon,
        route: `/course/${chapitreId}`
      },
      { 
        key: 'exercices', 
        label: 'Exercices', 
        icon: AcademicCapIcon,
        route: `/exercices/${chapitreId}`
      },
      { 
        key: 'quiz', 
        label: 'Quiz', 
        icon: QuestionMarkCircleIcon,
        route: `/quiz-exercices/${chapitreId}`
      }
    ]
  }
  
  // Cas 2: On est dans une notion spécifique (liste des chapitres)
  if (notionId && currentPath.includes('/chapitres/') && !currentPath.includes('/quiz-chapitres/') && !currentPath.includes('/course-chapitres/')) {
    return [
      { 
        key: 'cours', 
        label: 'Cours', 
        icon: BookOpenIcon,
        route: `/course-chapitres/${notionId}`
      },
      { 
        key: 'exercices', 
        label: 'Exercices', 
        icon: AcademicCapIcon,
        route: `/chapitres/${notionId}`
      },
      { 
        key: 'quiz', 
        label: 'Quiz', 
        icon: QuestionMarkCircleIcon,
        route: `/quiz-chapitres/${notionId}`
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
  if (notionId && currentPath.includes('/course-chapitres/')) {
    return [
      { 
        key: 'cours', 
        label: 'Cours', 
        icon: BookOpenIcon,
        route: `/course-chapitres/${notionId}`
      },
      { 
        key: 'exercices', 
        label: 'Exercices', 
        icon: AcademicCapIcon,
        route: `/chapitres/${notionId}`
      },
      { 
        key: 'quiz', 
        label: 'Quiz', 
        icon: QuestionMarkCircleIcon,
        route: `/quiz-chapitres/${notionId}`
      }
    ]
  }
  
  // Cas 5: On est dans une notion de quiz
  if (notionId && currentPath.includes('/quiz-chapitres/')) {
    return [
      { 
        key: 'cours', 
        label: 'Cours', 
        icon: BookOpenIcon,
        route: `/course-chapitres/${notionId}`
      },
      { 
        key: 'exercices', 
        label: 'Exercices ', 
        icon: AcademicCapIcon,
        route: `/chapitres/${notionId}`
      },
      { 
        key: 'quiz', 
        label: 'Quiz', 
        icon: QuestionMarkCircleIcon,
        route: `/quiz-chapitres/${notionId}`
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
    } else {
      // Si on est dans un chapitre mais pas sur une route spécifique, on reste sur exercices par défaut
      activeTab.value = 'exercices'
    }
  } else {
    // Navigation générale (notions, matières, etc.)
    if (currentPath.includes('/course/') || currentPath.includes('/course-chapitres/') || currentPath.includes('/course-notions/')) {
      activeTab.value = 'cours'
    } else if (currentPath.includes('/exercices/') || 
               (currentPath.includes('/chapitres/') && !currentPath.includes('/quiz-chapitres/') && !currentPath.includes('/course-chapitres/')) ||
               currentPath.includes('/notions/')) {
      activeTab.value = 'exercices'
    } else if (currentPath.includes('/quiz-exercices/') || 
               currentPath.includes('/quiz-chapitres/') || 
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

// Handle tab navigation
function handleTabClick(tabKey) {
  const tab = tabs.value.find(t => t.key === tabKey)
  if (tab) {
    // Mise à jour immédiate de l'onglet actif pour un feedback visuel instantané
    activeTab.value = tabKey
    
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
  background: #ffffff;
  padding: 0.375rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #f1f5f9;
  backdrop-filter: blur(12px);
  max-width: fit-content;
  margin: 0 auto;
}

.chapter-nav-btn {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.875rem 1.25rem;
  border: none;
  background: transparent;
  border-radius: 12px;
  color: #64748b;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  position: relative;
  overflow: hidden;
}

/* Info-bulle pédagogique au survol */
.chapter-nav-btn:hover::after {
  content: attr(aria-label);
  position: absolute;
  bottom: -36px;
  left: 50%;
  transform: translateX(-50%);
  background: #111827;
  color: #fff;
  font-size: 12px;
  padding: 6px 8px;
  border-radius: 6px;
  white-space: nowrap;
  box-shadow: 0 8px 20px rgba(0,0,0,.15);
  pointer-events: none;
}

.chapter-nav-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 12px;
}

.chapter-nav-btn:hover::before {
  opacity: 1;
}

.chapter-nav-btn:hover {
  color: #1e293b;
  transform: translateY(-1px);
}

.chapter-nav-btn.active {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.25);
  transform: translateY(-2px);
}

.chapter-nav-btn:focus-visible {
  outline: 3px solid rgba(37, 99, 235, 0.4);
  outline-offset: 2px;
}

.chapter-nav-btn.active::before {
  display: none;
}

.chapter-nav-icon {
  width: 1.375rem;
  height: 1.375rem;
  flex-shrink: 0;
  transition: transform 0.3s ease;
  position: relative;
  z-index: 1;
}

.chapter-nav-btn:hover .chapter-nav-icon {
  transform: scale(1.1);
}

.chapter-nav-btn.active .chapter-nav-icon {
  transform: scale(1.05);
}

.chapter-nav-label {
  font-weight: 600;
  position: relative;
  z-index: 1;
  letter-spacing: 0.025em;
}

/* Responsive design */
@media (max-width: 768px) {
  .chapter-navigation {
    gap: 0.125rem;
    padding: 0.25rem;
    border-radius: 14px;
  }
  
  .chapter-nav-btn {
    padding: 0.625rem 0.875rem;
    gap: 0.375rem;
    border-radius: 10px;
  }
  
  .chapter-nav-label {
    font-size: 0.8rem;
    line-height: 1.2;
  }
  
  .chapter-nav-icon {
    width: 1.125rem;
    height: 1.125rem;
  }
}

@media (max-width: 480px) {
  .chapter-navigation {
    padding: 0.25rem;
    gap: 0.125rem;
  }
  
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

@media (max-width: 360px) {

  .chapter-nav-label {
    display: none;
  }
  
  .chapter-nav-btn {
    padding: 0.5rem;
    min-width: 2.5rem;
    justify-content: center;
  }
}
</style> 
