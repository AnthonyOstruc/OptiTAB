<template>
  <aside :class="['sidebar', { collapsed }]">
    <nav class="sidebar-menu">
      <div class="sidebar-menu-container">
        <ul>
          <!-- Tableau de bord -->
          <li 
            :class="['sidebar-item', { active: isActiveRoute('dashboard') }]" 
            @click="handleSidebarClick({ key: 'dashboard' })"
            :title="collapsed ? 'Tableau de bord' : ''"
          >
            <span class="sidebar-icon">
              <Squares2X2Icon />
            </span>
            <span v-if="!collapsed" class="sidebar-label">Tableau de bord</span>
          </li>
          
          <!-- Autres éléments du menu -->
          <li 
            :class="['sidebar-item', { active: isActiveRoute(item.key) }]" 
            v-for="item in otherMenuItems" 
            :key="item.key" 
            @click="handleSidebarClick(item)"
            :title="collapsed ? item.text : ''"
          >
            <span class="sidebar-icon">
              <component :is="item.icon" />
            </span>
            <span v-if="!collapsed" class="sidebar-label">{{ item.text }}</span>
          </li>
          
          <!-- Liens spécifiques admin -->
          <template v-if="userStore.isAdmin">
            <li class="sidebar-section-header" v-if="!collapsed">
              <span class="section-title">⚙️ Administration</span>
            </li>
            <li 
              class="sidebar-item" 
              @click="router.push('/admin/matieres')"
              :title="collapsed ? 'Matières' : ''"
            >
              <span class="sidebar-icon"><AcademicCapIcon class="h-6 w-6" /></span>
              <span v-if="!collapsed" class="sidebar-label">Matières</span>
            </li>
            <li 
              class="sidebar-item" 
              @click="router.push('/admin/notions')"
              :title="collapsed ? 'Notions' : ''"
            >
              <span class="sidebar-icon"><LightBulbIcon class="h-6 w-6" /></span>
              <span v-if="!collapsed" class="sidebar-label">Notions</span>
            </li>
            <li 
              class="sidebar-item" 
              @click="router.push('/admin/chapitres')"
              :title="collapsed ? 'Chapitres' : ''"
            >
              <span class="sidebar-icon"><BookOpenIcon class="h-6 w-6" /></span>
              <span v-if="!collapsed" class="sidebar-label">Chapitres</span>
            </li>
            <li 
              class="sidebar-item" 
              @click="router.push('/admin/exercices')"
              :title="collapsed ? 'Exercices' : ''"
            >
              <span class="sidebar-icon"><PencilSquareIcon class="h-6 w-6" /></span>
              <span v-if="!collapsed" class="sidebar-label">Exercices</span>
            </li>
            <li 
              class="sidebar-item" 
              @click="router.push('/admin/exercices-plus')"
              :title="collapsed ? 'Exercices+' : ''"
            >
               <span class="sidebar-icon">
                 <PlusCircleIcon />
               </span>
               <span v-if="!collapsed" class="sidebar-label">Exercices+</span>
            </li>
            <li 
              class="sidebar-item" 
              @click="router.push('/admin/fiches')"
              :title="collapsed ? 'Fiches' : ''"
            >
              <span class="sidebar-icon"><DocumentTextIcon class="h-6 w-6" /></span>
              <span v-if="!collapsed" class="sidebar-label">Fiches</span>
            </li>
            <li 
              class="sidebar-item" 
              @click="router.push('/admin/quiz')"
              :title="collapsed ? 'Quiz' : ''"
            >
              <span class="sidebar-icon"><QuestionMarkCircleIcon class="h-6 w-6" /></span>
              <span v-if="!collapsed" class="sidebar-label">Quiz</span>
            </li>
          </template>
        </ul>
      </div>
    </nav>
  </aside>
</template>

<script setup>
import menu from '@/config/dashboardMenu.js'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { logoutUser } from '@/api'
import { getInitials } from '@/utils'
import { computed, ref, onMounted, onUnmounted } from 'vue'

import { AcademicCapIcon, LightBulbIcon, BookOpenIcon, PencilSquareIcon, PlusCircleIcon, DocumentTextIcon, QuestionMarkCircleIcon, Squares2X2Icon } from '@heroicons/vue/24/outline'
import { useRoute } from 'vue-router'
import { useSubjectsStore } from '@/stores/subjects/index'

const props = defineProps({ collapsed: Boolean })
const emit = defineEmits(['navigation', 'toggle-collapsed'])

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()
const subjectsStore = useSubjectsStore()


// Tous les éléments du menu dans l'ordre défini
const otherMenuItems = computed(() => {
  return menu.filter(item => item.key !== 'dashboard')
})

// Fonction pour déterminer si une route est active
const isActiveRoute = (menuKey) => {
  const currentPath = route.path
  
  // Mapping des clés de menu vers les chemins de route
  const routeMapping = {
    'dashboard': '/dashboard',
    'cours': ['/online-courses', '/course-notions', '/course-chapitres', '/course', '/cours'],
    'exercices': ['/exercises', '/notions', '/themes', '/theme-notions', '/chapitres', '/exercices', '/chapter-exercises'],
    'fiches': ['/sheets'],
    'quiz': ['/quiz', '/quiz-notions', '/quiz-chapitres', '/quiz-exercices', '/chapter-quiz'],
    'progress': '/progress',
    'calculator': '/calculator'
  }
  
  const targetRoutes = routeMapping[menuKey]
  
  if (!targetRoutes) return false
  
  // Si c'est un tableau, vérifier si le chemin actuel correspond à l'un des chemins
  if (Array.isArray(targetRoutes)) {
    return targetRoutes.some(route => currentPath.startsWith(route))
  }
  
  // Sinon, vérifier l'égalité exacte
  return currentPath === targetRoutes
}

async function handleSidebarClick(item) {
  // Routes simples sans matière
  if (item.key === 'calculator') {
    router.push('/calculator')
  } else if (item.key === 'dashboard') {
    router.push('/dashboard')
  } 
  // Routes intelligentes avec matière
  else if (['exercices', 'fiches', 'quiz', 'cours'].includes(item.key)) {
    // Déterminer la matière active si possible
    const activeId = subjectsStore.activeMatiereId || subjectsStore.selectedMatieresIds?.[0] || null
    if (item.key === 'exercices') {
      if (activeId) {
        router.push({ name: 'Themes', params: { matiereId: String(activeId) } })
      } else {
        router.push({ name: 'Exercises' })
      }
    } else if (item.key === 'fiches') {
      if (activeId) {
        router.push({ name: 'Sheets', query: { matiereId: String(activeId) } })
      } else {
        router.push({ name: 'Sheets' })
      }
    } else if (item.key === 'quiz') {
      if (activeId) {
        router.push({ name: 'QuizNotions', params: { matiereId: String(activeId) } })
      } else {
        router.push({ name: 'Quiz' })
      }
    } else if (item.key === 'cours') {
      if (activeId) {
        router.push({ name: 'CourseNotions', params: { matiereId: String(activeId) } })
      } else {
        router.push({ name: 'OnlineCourses' })
      }
    }
  }
}

const userName = computed(() => (userStore.firstName + ' ' + userStore.lastName).trim())
const userInitials = computed(() => getInitials(userStore.firstName, userStore.lastName))

const user = {
  name: userStore.firstName + ' ' + userStore.lastName,
  plan: 'Plan Standard',
  initials: getInitials(userStore.firstName, userStore.lastName)
}

// Variable pour le debouncing
let resizeTimeout = null
let resizeObserver = null

// Fonction pour détecter si l'écran est petit
const isSmallScreen = () => {
  return window.innerWidth < 1024 // Breakpoint pour plier automatiquement
}

// Fonction pour gérer le redimensionnement de la fenêtre avec debouncing
const handleResize = () => {
  // Annuler le timeout précédent
  if (resizeTimeout) {
    clearTimeout(resizeTimeout)
  }
  
  // Attendre 30ms avant d'exécuter l'action (très rapide)
  resizeTimeout = setTimeout(() => {
    if (isSmallScreen() && !props.collapsed) {
      // Plier automatiquement sur petit écran
      emit('toggle-collapsed')
    } else if (!isSmallScreen() && props.collapsed) {
      // Déplier automatiquement sur grand écran
      emit('toggle-collapsed')
    }
  }, 30)
}

// Initialiser l'état au montage du composant
onMounted(() => {
  // Vérifier la taille initiale immédiatement
  if (isSmallScreen() && !props.collapsed) {
    // Délai minimal pour l'initialisation
    setTimeout(() => {
      emit('toggle-collapsed')
    }, 10)
  }
  
  // Ajouter l'écouteur d'événement pour le redimensionnement
  window.addEventListener('resize', handleResize)
  
  // Utiliser ResizeObserver pour une détection plus rapide (si supporté)
  if (window.ResizeObserver) {
    resizeObserver = new ResizeObserver(() => {
      handleResize()
    })
    resizeObserver.observe(document.body)
  }
})

// Nettoyer l'écouteur d'événement
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  // Nettoyer le timeout
  if (resizeTimeout) {
    clearTimeout(resizeTimeout)
  }
  // Nettoyer le ResizeObserver
  if (resizeObserver) {
    resizeObserver.disconnect()
  }
})

const handleLogout = async () => {
  // Récupère le refresh token
  const refresh = localStorage.getItem('refresh_token')
  // Si le token existe et semble valide, on tente de le blacklister côté backend
  if (refresh && refresh !== 'null' && refresh !== 'undefined' && refresh.trim() !== '') {
    try {
      await logoutUser({ refresh })
    } catch (e) {
      // On ignore toute erreur de déconnexion (le backend renvoie toujours un succès désormais)
    }
  }
  // Nettoyage local côté frontend
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  userStore.clearUser()
  router.push('/')
}

// Exposer les fonctions pour le template
defineExpose({
  isActiveRoute,
  handleSidebarClick,
  handleLogout
})
</script>

<style scoped>
.sidebar {
  width: 260px;
  background: #fff;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-height: 100vh;
  justify-content: flex-start;
  position: relative;
  transition: width 0.1s ease-out;
  overflow: hidden;
}
.sidebar.collapsed {
  width: 64px;
}
.sidebar.collapsed .sidebar-label {
  display: none !important;
}
.sidebar.collapsed .sidebar-icon {
  justify-content: center;
  margin-right: 0;
}
.sidebar-close-btn {
  position: absolute;
  top: 18px;
  right: 18px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(30,41,59,0.07);
  transition: background 0.15s;
  z-index: 10;
}
.sidebar-close-btn:hover {
  background: #f1f5f9;
}
.sidebar-close-icon {
  font-size: 1.3rem;
  color: #2563eb;
}
.sidebar-header {
  min-height: 0;
  height: 0;
  margin: 0;
  padding: 0;
}
.sidebar-logo {
  font-size: 2rem;
}
.sidebar-title {
  font-size: 1.25rem;
}
.sidebar-menu {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-menu-container {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 0.5rem 0 2rem 0;
  /* Masquer la scrollbar par défaut mais permettre le scroll */
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 transparent;
}

/* Styles pour la scrollbar WebKit (Chrome, Safari, Edge) */
.sidebar-menu-container::-webkit-scrollbar {
  width: 6px;
}

.sidebar-menu-container::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-menu-container::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
  transition: background 0.2s ease;
}

.sidebar-menu-container::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.sidebar-menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-menu li {
  cursor: pointer;
}
.sidebar-item {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  padding: 0.85rem 0.55rem;
  font-size: 1.08rem;
  color: #222;
  border-radius: 8px;
  cursor: pointer !important;
  transition: all 0.15s ease;
  border-left: 3px solid transparent;
  margin: 0.125rem 0.5rem;
  user-select: none;
}
.sidebar-item.active, .sidebar-item:hover {
  background: #eef4ff;
  color: #2563eb;
  cursor: pointer !important;
}

.sidebar-item.active {
  background: #dbeafe;
  color: #1d4ed8;
  border-left: 3px solid #2563eb;
  font-weight: 600;
}

.sidebar-item.active .sidebar-icon {
  color: #1d4ed8;
}
.sidebar-icon {
  font-size: 1.3rem;
  width: 1.6rem;
  height: 1.6rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2563eb;
  flex-shrink: 0;
  transition: none;
}
.sidebar.collapsed .sidebar-icon {
  width: 1.6rem;
  height: 1.6rem;
  font-size: 1.3rem;
  margin-right: 0;
  justify-content: center;
}
.sidebar-label {
  display: flex;
  align-items: center;
}

.sidebar-section-header {
  padding: 0.75rem 1.5rem 0.25rem 1.5rem;
  margin-top: 1rem;
}

.section-title {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.dropdown-item {
  position: relative;
}

.dropdown-menu {
  list-style: none;
  padding: 0;
  margin: 0;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-top: 0.25rem;
  margin-left: 0.5rem;
  margin-right: 0.5rem;
}

.dropdown-arrow {
  margin-left: auto;
  font-size: 0.75rem;
  transition: transform 0.2s ease-in-out;
  color: #6b7280;
}

.dropdown-arrow.rotated {
  transform: rotate(180deg);
}

.matiere-dropdown-item {
  padding: 0.75rem 1rem;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  transition: background 0.15s;
  border-radius: 6px;
  margin: 0.125rem;
}

.matiere-dropdown-item:hover {
  background: #eef4ff;
}

.matiere-icon {
  font-size: 1.1rem;
  width: 1.2rem;
  height: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.matiere-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #374151;
}

.matiere-stats {
  font-size: 0.75rem;
  color: #6b7280;
  background: #f3f4f6;
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
  flex-shrink: 0;
}

/* Styles responsives pour le sidebar */
@media (max-width: 1024px) {
  .sidebar {
    /* Assurer que le sidebar reste accessible sur tablette */
    z-index: 1000;
    /* Transition plus rapide sur petit écran */
    transition: width 0.08s ease-out;
    height: 100vh;
    max-height: 100vh;
  }
  
  .sidebar.collapsed {
    /* Optimiser l'espace sur petit écran */
    width: 60px;
  }
  
  .sidebar-menu-container {
    /* Assurer que le défilement fonctionne sur tablette */
    overflow-y: auto;
    overflow-x: hidden;
  }
}

@media (max-width: 768px) {
  .sidebar {
    /* Sidebar plus compact sur mobile */
    width: 240px;
    /* Transition ultra-rapide sur mobile */
    transition: width 0.06s ease-out;
    height: 100vh;
    max-height: 100vh;
  }
  
  .sidebar.collapsed {
    width: 56px;
  }
  
  .sidebar-item {
    /* Réduire le padding sur mobile */
    padding: 0.7rem 0.4rem;
    font-size: 1rem;
  }
  
  .sidebar-menu-container {
    /* Assurer que le défilement fonctionne sur mobile */
    overflow-y: auto;
    overflow-x: hidden;
  }
}

@media (max-width: 480px) {
  .sidebar {
    /* Sidebar encore plus compact sur très petit écran */
    width: 220px;
    /* Transition instantanée sur très petit écran */
    transition: width 0.05s ease-out;
    height: 100vh;
    max-height: 100vh;
  }
  
  .sidebar.collapsed {
    width: 52px;
  }
  
  .sidebar-item {
    /* Padding minimal sur très petit écran */
    padding: 0.6rem 0.3rem;
    font-size: 0.95rem;
    margin: 0.1rem 0.3rem;
  }
  
  .sidebar-menu-container {
    /* Assurer que le défilement fonctionne sur très petit écran */
    overflow-y: auto;
    overflow-x: hidden;
  }
}

/* Animation pour le dropdown */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease-in-out;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.sidebar-logo-img {
  height: 80px;
  width: auto;
  display: block;
}


</style> 