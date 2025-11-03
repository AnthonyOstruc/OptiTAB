<template>
  <nav class="chapter-navigation" aria-label="Navigation des chapitres">
    <!-- Flèche gauche (mobile seulement) -->
    <button 
      class="nav-arrow nav-arrow-left"
      @click="navigatePrevious"
      aria-label="Onglet précédent"
    >
      <ChevronLeftIcon class="arrow-icon" />
    </button>

    <!-- Boutons de navigation -->
    <button 
      v-for="tab in tabs" 
      :key="tab.key"
      v-show="tab.key !== 'quiz'"
      :class="['chapter-nav-btn', { active: tab.key === activeTab }]"
      :aria-pressed="tab.key === activeTab"
      :aria-label="tab.label"
      @click="handleTabClick(tab.key)"
      @mouseenter="prefetchTab(tab.key)"
    >
      <component :is="tab.icon" class="chapter-nav-icon" />
      <span class="chapter-nav-label">{{ tab.label }}</span>
    </button>

    <!-- Flèche droite (mobile seulement) -->
    <button 
      class="nav-arrow nav-arrow-right"
      @click="navigateNext"
      aria-label="Onglet suivant"
    >
      <ChevronRightIcon class="arrow-icon" />
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
  DocumentTextIcon,
  ChevronLeftIcon,
  ChevronRightIcon
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
    // Construire un hash vers le dernier exercice visité si disponible
    let exHash = ''
    try {
      const lastId = sessionStorage.getItem(`optitab_last_exercice_${notionId}`)
      if (lastId) exHash = `#ex-${lastId}`
    } catch (_) {}
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
        route: `/exercices-notion/${notionId}${exHash}`
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
    let exHash = ''
    try {
      const lastId = sessionStorage.getItem(`optitab_last_exercice_${notionId}`)
      if (lastId) exHash = `#ex-${lastId}`
    } catch (_) {}
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
        route: `/exercices-notion/${notionId}${exHash}`
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
    let exHash = ''
    try {
      const lastId = sessionStorage.getItem(`optitab_last_exercice_${notionId}`)
      if (lastId) exHash = `#ex-${lastId}`
    } catch (_) {}
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
        route: `/exercices-notion/${notionId}${exHash}`
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
    let exHash = ''
    try {
      const lastId = sessionStorage.getItem(`optitab_last_exercice_${notionId}`)
      if (lastId) exHash = `#ex-${lastId}`
    } catch (_) {}
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
        route: `/exercices-notion/${notionId}${exHash}`
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
        // Récupérer la vraie position de scroll du conteneur d'app
        const container = (document.querySelector('.dashboard-main') || document.querySelector('.dashboard-content') || document.documentElement)
        const scrollY = (container === document.documentElement || container === document.body)
          ? (window.pageYOffset || document.documentElement.scrollTop || 0)
          : container.scrollTop
        const state = { scrollY, t: Date.now() }
        sessionStorage.setItem(key, JSON.stringify(state))

        // Si on quitte la page Exercices, mettre à jour aussi la clé utilisée par la page pour restaurer
        if (pageType === 'exercices') {
          try {
            const exKey = `optitab_page_exercices_${notionId}`
            const raw = sessionStorage.getItem(exKey)
            const obj = raw ? (JSON.parse(raw) || {}) : {}
            obj.scrollY = state.scrollY
            obj.t = state.t
            sessionStorage.setItem(exKey, JSON.stringify(obj))
          } catch (_) {}
        }
      }
    } catch (_) {}

  // Navigation avec transition fluide
    const target = tab.route
    const navPromise = typeof target === 'string' ? router.push(target) : router.push({ ...target, replace: false })
    Promise.resolve(navPromise).catch(err => {
      // Gestion des erreurs de navigation
      console.warn('Navigation error:', err)
      // Si la navigation échoue, on revient à l'onglet précédent
      updateActiveTab()
    })
  }
}

// Navigation avec flèches (pour mobile)
function navigatePrevious() {
  const currentIndex = tabs.value.findIndex(t => t.key === activeTab.value)
  const previousIndex = currentIndex > 0 ? currentIndex - 1 : tabs.value.length - 1
  handleTabClick(tabs.value[previousIndex].key)
}

function navigateNext() {
  const currentIndex = tabs.value.findIndex(t => t.key === activeTab.value)
  const nextIndex = currentIndex < tabs.value.length - 1 ? currentIndex + 1 : 0
  handleTabClick(tabs.value[nextIndex].key)
}
</script>

<style scoped>
.chapter-navigation {
  display: flex;
  align-items: stretch;
  gap: 0;
  width: 100%;
  max-width: 460px;
  margin: 0.75rem auto 0.5rem auto;
  padding: 0; /* remove surrounding box spacing */
  border-radius: 0; /* no visible container shape */
  border: none; /* remove white box border */
  background: transparent; /* remove background */
  box-shadow: none; /* remove outer shadow */
  height: 40px; /* hauteur fixe pour le conteneur */
}

.chapter-nav-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0 1rem;
  border: none;
  border-radius: 0;
  background: transparent;
  color: #475569;
  font-weight: 600;
  font-size: 0.86rem;
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  white-space: nowrap;
  height: 100%; /* prend toute la hauteur du conteneur */
  min-height: 100%;
  position: relative;
}

/* Barre verticale de séparation entre les boutons */
.chapter-nav-btn:not(:last-child)::after {
  content: '';
  position: absolute;
  right: -0.125rem;
  top: 50%;
  transform: translateY(-50%);
  height: 60%;
  width: 1px;
  background: rgba(203, 213, 225, 0.5);
  transition: opacity 0.2s ease;
}

/* Masquer la barre quand le bouton ou son voisin est actif ou survolé */
.chapter-nav-btn.active::after,
.chapter-nav-btn:hover::after,
.chapter-nav-btn.active + .chapter-nav-btn::before {
  opacity: 0;
}

.chapter-nav-btn:hover {
  background: rgba(59, 130, 246, 0.1);
  color: #2563eb;
}

.chapter-nav-btn.active {
  background: #3b82f6;
  color: #fff;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.chapter-nav-btn:focus-visible {
  outline: 2px solid rgba(59, 130, 246, 0.45);
  outline-offset: 2px;
}

.chapter-nav-icon {
  width: 1.15rem;
  height: 1.15rem;
  flex-shrink: 0;
}

.chapter-nav-label {
  font-weight: 600;
  letter-spacing: 0.02em;
}

/* Responsive design */
@media (max-width: 768px) {
  .chapter-navigation {
    max-width: 90%;
    padding: 0.3rem;
  }
  
  .chapter-nav-btn {
    padding: 0 0.85rem;
    gap: 0.4rem;
    font-size: 0.82rem;
  }
  
  .chapter-nav-label {
    font-size: 0.8rem;
  }
  
  .chapter-nav-icon {
    width: 1.05rem;
    height: 1.05rem;
  }
}

@media (max-width: 480px) {
  .chapter-nav-btn {
    padding: 0 0.7rem;
    gap: 0.3rem;
    font-size: 0.75rem;
  }
  
  .chapter-nav-label {
    font-size: 0.75rem;
  }
  
  .chapter-nav-icon {
    width: 1rem;
    height: 1rem;
  }
}

/* Flèches de navigation mobile */
.nav-arrow {
  display: none; /* Masquées par défaut */
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  border: none;
  background: transparent;
  color: #475569;
  cursor: pointer;
  transition: color 0.2s ease, background 0.2s ease;
  flex-shrink: 0;
}

.nav-arrow:hover {
  color: #3b82f6;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 8px;
}

.arrow-icon {
  width: 1.5rem;
  height: 1.5rem;
}

/* Mode mobile en dessous de 570px */
@media (max-width: 570px) {
  .chapter-navigation {
    max-width: 100%;
    justify-content: space-between;
    padding: 0 0.75rem;
    height: 36px;
  }

  /* Afficher les flèches */
  .nav-arrow {
    display: flex;
    padding: 0.25rem;
  }

  .arrow-icon {
    width: 1.25rem;
    height: 1.25rem;
  }

  /* Masquer tous les boutons sauf l'actif */
  .chapter-nav-btn {
    display: none;
  }

  .chapter-nav-btn.active {
    display: flex;
    flex: 1;
    max-width: 160px;
    font-size: 0.8rem;
    padding: 0 0.75rem;
  }

  /* Garder l'icône et le label pour l'onglet actif */
  .chapter-nav-icon {
    width: 1rem;
    height: 1rem;
  }

  .chapter-nav-label {
    display: block;
  }
}

/* Très petits écrans - Masquer l'icône, montrer seulement le nom */
@media (max-width: 340px) {
  .chapter-navigation {
    padding: 0 0.5rem;
    height: 32px;
  }

  .nav-arrow {
    padding: 0.2rem;
  }

  .arrow-icon {
    width: 1.1rem;
    height: 1.1rem;
  }

  /* Masquer l'icône sur l'onglet actif pour gagner de la place */
  .chapter-nav-btn.active .chapter-nav-icon {
    display: none;
  }
  
  .chapter-nav-btn.active {
    max-width: 140px;
    font-size: 0.75rem;
    padding: 0 0.5rem;
    justify-content: center;
  }

  /* Afficher le label en priorité */
  .chapter-nav-label {
    display: block;
    font-size: 0.75rem;
  }
}
</style> 
