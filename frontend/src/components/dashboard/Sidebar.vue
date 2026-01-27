<template>
  <aside :class="['sidebar', { collapsed }]">
    <nav class="sidebar-menu">
      <div class="sidebar-menu-container">
        <ul>
          <!-- Tableau de bord -->
          <li>
            <button
              type="button"
              :class="['sidebar-item', { active: isActiveRoute('dashboard') }]"
              @click="handleSidebarClick({ key: 'dashboard' })"
              :title="collapsed ? 'Tableau de bord' : ''"
            >
              <span class="sidebar-icon">
                <Squares2X2Icon />
              </span>
              <span v-if="!collapsed" class="sidebar-label">Tableau de bord</span>
            </button>
          </li>

          <!-- Barre de recherche globale (sous Tableau de bord) -->
          <li v-if="!collapsed" class="sidebar-search">
            <div class="search-box" role="search">
              <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/>
                <line x1="20" y1="20" x2="16" y2="16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <input
                v-model="globalQuery"
                type="search"
                class="search-input"
                placeholder="Mes recherches"
                @keydown.enter.prevent="onGlobalEnter"
              />
              <button v-if="globalQuery" class="clear-btn" @click="clearGlobalQuery" aria-label="Effacer la recherche">×</button>
            </div>
          </li>
          
          <!-- Autres éléments du menu -->
          <li v-for="item in otherMenuItems" :key="item.key">
            <button
              type="button"
              :class="['sidebar-item', { active: isActiveRoute(item.key) }]"
              :data-cta-name="item.key === 'abonnement' ? 'subscribe' : null"
              :data-cta-location="item.key === 'abonnement' ? 'nav_sidebar' : null"
              @click="handleSidebarClick(item)"
              @mouseenter="handleSidebarHover(item)"
              :title="collapsed ? item.text : ''"
            >
              <span class="sidebar-icon">
                <component :is="item.icon" />
              </span>
              <span v-if="!collapsed" class="sidebar-label">{{ item.text }}</span>
            </button>
          </li>
          
          <!-- Lien admin -->
          <template v-if="userStore.isAdmin">
            <li class="sidebar-section-header" v-if="!collapsed">
              <span class="section-title">⚙️ Administration</span>
            </li>
            <li>
              <button
                type="button"
                class="sidebar-item"
                :class="{ active: isAdminActive }"
                :title="collapsed ? 'Admin' : ''"
                @click="router.push('/admin/matieres')"
              >
                <span class="sidebar-icon"><AcademicCapIcon class="h-6 w-6" /></span>
                <span v-if="!collapsed" class="sidebar-label">Admin</span>
              </button>
            </li>
            <li>
              <button
                type="button"
                class="sidebar-item"
                :class="{ active: route.path.startsWith('/admin/newsletter') }"
                :title="collapsed ? 'Newsletter' : ''"
                @click="router.push('/admin/newsletter')"
              >
                <span class="sidebar-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="5" width="20" height="14" rx="3"/><path d="M2 7l10 6 10-6"/></svg></span>
                <span v-if="!collapsed" class="sidebar-label">Newsletter</span>
              </button>
            </li>
            <li>
              <button
                type="button"
                class="sidebar-item"
                :class="{ active: route.path.startsWith('/admin/subscriptions') }"
                :title="collapsed ? 'Abonnements' : ''"
                @click="router.push('/admin/subscriptions')"
              >
                <span class="sidebar-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h10"/></svg></span>
                <span v-if="!collapsed" class="sidebar-label">Abonnements</span>
              </button>
            </li>
            <li>
              <button
                type="button"
                class="sidebar-item"
                :class="{ active: route.path.startsWith('/admin/subscribers') }"
                :title="collapsed ? 'Abonnés' : ''"
                @click="router.push('/admin/subscribers')"
              >
                <span class="sidebar-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 11c1.657 0 3-1.79 3-4s-1.343-4-3-4-3 1.79-3 4 1.343 4 3 4z"/><path d="M8 13c-3.866 0-7 2.239-7 5v3h14v-3c0-2.761-3.134-5-7-5z"/></svg></span>
                <span v-if="!collapsed" class="sidebar-label">Abonnés</span>
              </button>
            </li>
            <li>
              <button
                type="button"
                class="sidebar-item"
                :class="{ active: route.path.startsWith('/admin/quiz-submissions') }"
                :title="collapsed ? 'Notation des Quiz' : ''"
                @click="router.push('/admin/quiz-submissions')"
              >
                <span class="sidebar-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg></span>
                <span v-if="!collapsed" class="sidebar-label">Notation Quiz</span>
              </button>
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
import { computed, ref, onMounted, onUnmounted, watch } from 'vue'
import { apiUtils } from '@/api/client'
import { useDataPrefetch } from '@/composables/useDataPrefetch'
import * as analytics from '@/services/analytics'

import { AcademicCapIcon, Squares2X2Icon } from '@heroicons/vue/24/outline'
import { useRoute } from 'vue-router'
import { useSubjectsStore } from '@/stores/subjects/index'

const props = defineProps({ collapsed: Boolean })
const emit = defineEmits(['navigation', 'toggle-collapsed'])

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()
const subjectsStore = useSubjectsStore()
const { prefetchThemesNotions } = useDataPrefetch()
let logoutInProgress = false

// Debounce pour éviter trop de prefetch
let hoverTimeout = null

// Recherche globale (synchronisée avec l'URL: ?q=...)
const globalQuery = ref('')

onMounted(() => {
  const q = route.query?.q
  if (typeof q !== 'undefined' && q !== null) {
    try { globalQuery.value = String(q) } catch {}
  }
})

// Mettre à jour l'URL quand l'utilisateur tape (debounced)
let globalQueryTimer = null
watch(globalQuery, (val) => {
  if (globalQueryTimer) clearTimeout(globalQueryTimer)
  globalQueryTimer = setTimeout(() => {
    const q = (val || '').trim()
    const newQuery = { ...route.query }
    if (q) newQuery.q = q
    else delete newQuery.q
    const currentQ = route.query?.q || ''
    if ((q || '') !== (currentQ || '')) {
      router.replace({ query: newQuery }).catch(() => {})
    }
  }, 200)
})

// Rester synchronisé si l'URL change ailleurs (pages/listes)
watch(() => route.query.q, (val) => {
  const incoming = val ? String(val) : ''
  if (incoming !== (globalQuery.value || '')) globalQuery.value = incoming
})

const onGlobalEnter = () => {
  // Optionnel: rester sur la page courante. Les listes se mettront à jour si visibles.
  // Possibilité: rediriger selon la section active, mais gardons simple pour l'instant.
}

const clearGlobalQuery = () => {
  globalQuery.value = ''
}


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
    'cours': ['/online-courses', '/course-notions', '/course-notion'],
    'exercices': ['/exercises', '/notions', '/exercicies', '/theme-notions', '/exercices-notion', '/exercices', '/chapter-exercises'],
    'fiches': ['/sheets'],
    'quiz': ['/quiz', '/quiz-notions', '/quiz-notion', '/chapter-quiz'],
    'progress': '/progress',
    'calculator': '/calculator',
    'abonnement': ['/billing', '/subscription'],
    'cours-particuliers': '/cours-particuliers',
    'admin': '/admin' // Spécialement pour les routes admin
  }

  const targetRoutes = routeMapping[menuKey]

  if (!targetRoutes) return false

  // Vérification spéciale pour éviter que /cours-particuliers active "cours"
  if (currentPath === '/cours-particuliers') {
    return menuKey === 'cours-particuliers'
  }

  // Si c'est un tableau, vérifier si le chemin actuel correspond à l'un des chemins
  if (Array.isArray(targetRoutes)) {
    return targetRoutes.some(route => currentPath.startsWith(route))
  }

  // Sinon, vérifier l'égalité exacte
  return currentPath === targetRoutes
}

// Fonction pour déterminer si l'onglet Admin doit être actif
const isAdminActive = computed(() => { 
  const p = route.path || ''; 
  return p.startsWith('/admin') && !p.startsWith('/admin/newsletter') && !p.startsWith('/admin/subscriptions') && !p.startsWith('/admin/subscribers') && !p.startsWith('/admin/quiz-submissions')
})

// Prefetch au survol (hover) - déclenché 150ms après le survol
function handleSidebarHover(item) {
  // Annuler le timeout précédent si l'utilisateur survole rapidement plusieurs items
  if (hoverTimeout) {
    clearTimeout(hoverTimeout)
  }
  
  // Seulement pour les routes qui utilisent des matières
  if (!['exercices', 'fiches', 'quiz', 'cours'].includes(item.key)) {
    return
  }
  
  hoverTimeout = setTimeout(() => {
    const activeId = subjectsStore.activeMatiereId || subjectsStore.selectedMatieresIds?.[0] || null
    if (activeId) {
      // Prefetch en arrière-plan de manière non-bloquante
      prefetchThemesNotions(activeId).catch(() => {
        // Ignorer les erreurs de prefetch silencieusement
      })
    }
    // Précharger aussi les chunks de vues associées pour éviter le blanc initial
    try {
      if (item.key === 'exercices') {
        import('@/views/Themes.vue')
      } else if (item.key === 'fiches') {
        import('@/views/SynthesisNotions.vue')
      } else if (item.key === 'quiz') {
        import('@/views/QuizNotions.vue')
      } else if (item.key === 'cours') {
        import('@/views/CourseNotions.vue')
      }
    } catch (_) {}
  }, 150) // Délai de 150ms pour éviter les survols accidentels
}

async function handleSidebarClick(item) {
  // Nettoyer le timeout de hover au clic
  if (hoverTimeout) {
    clearTimeout(hoverTimeout)
    hoverTimeout = null
  }
  
  // Routes simples sans matière
  if (item.key === 'calculator') {
    router.push('/calculator')
  } else if (item.key === 'dashboard') {
    router.push('/dashboard')
  } else if (item.key === 'abonnement') {
    router.push('/billing')
  } else if (item.key === 'cours-particuliers') {
    router.push('/cours-particuliers')
  } 
  // Routes intelligentes avec matière
  else if (['exercices', 'fiches', 'quiz', 'cours'].includes(item.key)) {
    // Déterminer la matière active si possible
    const activeId = subjectsStore.activeMatiereId || subjectsStore.selectedMatieresIds?.[0] || null
    if (item.key === 'exercices') {
      if (activeId) {
        // Prefetch immédiat au clic (si pas déjà fait au hover)
        prefetchThemesNotions(activeId).catch(() => {})
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
        // Prefetch immédiat au clic
        prefetchThemesNotions(activeId).catch(() => {})
        router.push({ name: 'QuizNotions', params: { matiereId: String(activeId) } })
      } else {
        router.push({ name: 'Quiz' })
      }
    } else if (item.key === 'cours') {
      if (activeId) {
        // Prefetch immédiat au clic
        prefetchThemesNotions(activeId).catch(() => {})
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
  return window.innerWidth < 900 // Breakpoint pour plier automatiquement
}

// Détecter si l'utilisateur a déjà une préférence sauvegardée
const hasSavedCollapsePreference = () => {
  try {
    return localStorage.getItem('sidebar-collapsed') !== null
  } catch (_) {
    return false
  }
}

// Fonction pour gérer le redimensionnement de la fenêtre avec debouncing
const handleResize = () => {
  // Annuler le timeout précédent
  if (resizeTimeout) {
    clearTimeout(resizeTimeout)
  }
  
  // Attendre 30ms avant d'exécuter l'action (très rapide)
  resizeTimeout = setTimeout(() => {
    // Respecter la préférence utilisateur si elle existe
    if (hasSavedCollapsePreference()) return
    if (isSmallScreen() && !props.collapsed) {
      // Plier automatiquement sur petit écran seulement si aucune préférence n'est enregistrée
      emit('toggle-collapsed')
    }
    // Sur grand écran : ne pas forcer le dépliement, respecter le choix utilisateur
  }, 30)
}

// Initialiser l'état au montage du composant
onMounted(() => {
  // Vérifier la taille initiale immédiatement
  // Ne pas surcharger le choix utilisateur si une préférence existe déjà
  if (!hasSavedCollapsePreference()) {
    if (isSmallScreen() && !props.collapsed) {
      // Délai minimal pour l'initialisation
      setTimeout(() => {
        emit('toggle-collapsed')
      }, 10)
    }
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
  if (logoutInProgress) return
  logoutInProgress = true
  userStore.isLoading = true

  let localCleanupDone = false
  const runLocalCleanup = () => {
    if (localCleanupDone) return
    localCleanupDone = true
    analytics.logout()
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    userStore.clearUser({ preserveLoadingState: true })
  }

  const redirectHome = async () => {
    try {
      await router.replace({ name: 'Home' })
    } catch (error) {
      console.warn('Redirection post-déconnexion (sidebar) impossible:', error)
    }
  }

  try {
    const refresh = localStorage.getItem('refresh_token')
    if (refresh && refresh !== 'null' && refresh !== 'undefined' && refresh.trim() !== '') {
      try {
        await logoutUser({ refresh })
      } catch (e) {
        console.log('Erreur lors de la déconnexion backend (sidebar):', e.message)
      }
    }
  } catch (e) {
    console.error('Erreur lors de la déconnexion via la sidebar:', e)
  } finally {
    runLocalCleanup()
    await redirectHome()
    userStore.isLoading = false
    logoutInProgress = false
  }
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
  height: 100dvh; /* Utiliser dvh sur navigateurs modernes pour mobile */
  max-height: 100vh;
  max-height: 100dvh; /* Utiliser dvh sur navigateurs modernes pour mobile */
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
  cursor: default;
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
  width: calc(100% - 1rem);
  text-align: left;
  background: transparent;
  border: none;
}
.sidebar-item:focus-visible {
  outline: 2px solid rgba(37, 99, 235, 0.55);
  outline-offset: 2px;
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

.sidebar-item.active .sidebar-icon svg {
  color: #1d4ed8 !important;
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
/* Ensure heroicons are visible even with global svg styles */
.sidebar-icon svg {
  width: 100%;
  height: 100%;
  display: block;
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

/* Barre de recherche globale */
.sidebar-search {
  padding: 0.25rem 0.5rem 0.5rem 0.5rem;
}
.search-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #fff;
  padding: 0.4rem 0.6rem;
}
.search-icon { color: #9ca3af; }
.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 0.95rem;
  background: transparent;
  color: #111827;
}
.search-input::-webkit-search-cancel-button,
.search-input::-webkit-search-decoration {
  -webkit-appearance: none;
  appearance: none;
  display: none;
}
/* Edge/IE legacy: */
.search-input::-ms-clear,
.search-input::-ms-reveal {
  display: none;
  width: 0;
  height: 0;
}
.clear-btn {
  background: #f3f4f6;
  border: none;
  color: #6b7280;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.clear-btn:hover { background: #e5e7eb; }

/* Styles responsives pour le sidebar */
@media (max-width: 900px) {
  .sidebar {
    /* Assurer que le sidebar reste accessible sur tablette */
    z-index: 1000;
    /* Transition plus rapide sur petit écran */
    transition: width 0.08s ease-out;
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
