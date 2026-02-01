<template>
  <div class="dashboard-layout">
    <!-- Header du dashboard -->
    <DashboardHeader 
      :sidebar-open="sidebarOpen" 
      :sidebar-collapsed="sidebarCollapsed"
      @toggle-sidebar="handleHeaderToggle"
      @subject-changed="handleSubjectChange"
    />
    
    <!-- Contenu principal -->
    <div class="dashboard-main-container">
                <!-- Sidebar principale -->
      <Sidebar 
        v-if="!isMobile && sidebarOpen" 
        :collapsed="sidebarCollapsed"
        @navigation="handleNavigation"
        @toggle-collapsed="toggleSidebarCollapsed"
        ref="sidebarRef"
      />
    
    <!-- Debug: Indicateur d'état de la sidebar (temporaire) -->
    <div v-if="false" style="position: fixed; top: 10px; right: 10px; background: #333; color: white; padding: 5px; border-radius: 4px; font-size: 12px; z-index: 9999;">
      Sidebar: {{ sidebarCollapsed ? 'Pliée' : 'Dépliée' }}
    </div>
      
      <!-- Contenu du dashboard -->
      <div class="dashboard-content">
        <main class="dashboard-main" :class="dashboardMainClasses">
          <slot />
        </main>
      </div>
    </div>

    <MobileBottomNav v-if="isMobile" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from './Sidebar.vue'
import DashboardHeader from './DashboardHeader.vue'
import MobileBottomNav from './MobileBottomNav.vue'
import { useUserStore } from '@/stores/user'
import { useSidebarStore } from '@/stores/sidebar'

// Props et émissions
const emit = defineEmits(['sidebar-toggle', 'navigation', 'subject-changed'])

// Références
const sidebarRef = ref(null)
const route = useRoute()
const userStore = useUserStore()

// État réactif
const sidebarStore = useSidebarStore()
const sidebarOpen = computed({
  get: () => sidebarStore.isOpen,
  set: (value) => sidebarStore.setOpen(value)
})
const sidebarCollapsed = computed({
  get: () => sidebarStore.isCollapsed,
  set: (value) => sidebarStore.setCollapsed(value)
})
const viewportWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1920)
const isMobile = computed(() => viewportWidth.value <= 768)
const dashboardMainClasses = computed(() => ({
  'with-mobile-nav': isMobile.value
}))
// Conserver l'état d'ouverture original lors d'une fermeture auto sur mobile
const lastDesktopOpenState = ref(sidebarStore.isOpen)
const lastDesktopCollapsedState = ref(sidebarStore.isCollapsed)
let responsiveWatchInitialized = false

const handleResize = () => {
  if (typeof window === 'undefined') return
  viewportWidth.value = window.innerWidth
}

// Méthodes
const toggleSidebar = () => {
  sidebarStore.toggleOpen()
  emit('sidebar-toggle', sidebarStore.isOpen)
}

const toggleSidebarCollapsed = () => {
  sidebarStore.toggleCollapsed()
  console.log('[DashboardLayout] Sidebar toggled:', { collapsed: sidebarStore.isCollapsed })
}

// Desktop: plier/déplier. Mobile: ouvrir/fermer.
const handleHeaderToggle = () => {
  if (isMobile.value) {
    toggleSidebar()
  } else {
    // Cycle desktop: full -> compact -> hidden -> full ...
    if (!sidebarOpen.value) {
      // Réaffiche la barre en mode plein (icônes + labels)
      sidebarStore.setCollapsed(false)
      sidebarStore.setOpen(true)
      return
    }

    if (!sidebarCollapsed.value) {
      // Passer du plein format au mode compact (icônes seules)
      sidebarStore.setCollapsed(true)
      return
    }

    // Sinon (compact), on masque complètement la barre
    sidebarStore.setOpen(false)
  }
}



const handleNavigation = (navigationData) => {
  emit('navigation', navigationData)
}

const handleSubjectChange = (subjectId) => {
  emit('subject-changed', subjectId)
}

// Lifecycle
onMounted(async () => {
  console.log('[DashboardLayout] onMounted - État initial:', { sidebarOpen: sidebarOpen.value, sidebarCollapsed: sidebarCollapsed.value })
  sidebarStore.init()
  window.addEventListener('resize', handleResize, { passive: true })
  handleResize()
  
  // Attendre que le DOM soit prêt
  await nextTick()
  
  console.log('[DashboardLayout] onMounted - État final:', { sidebarOpen: sidebarOpen.value, sidebarCollapsed: sidebarCollapsed.value })
  
  // Initialiser la sidebar si elle existe
  if (sidebarRef.value) {
    // La sidebar se charge automatiquement via onMounted
  }

})

watch(isMobile, (val, oldVal) => {
  // La première exécution intervient à chaque montage du layout;
  // ignorer le mode desktop pour ne pas écraser la préférence sauvegardée.
  if (!responsiveWatchInitialized) {
    responsiveWatchInitialized = true
    if (!val) return
  }

  if (val) {
    if (oldVal === false || oldVal === undefined) {
      lastDesktopOpenState.value = sidebarOpen.value
      lastDesktopCollapsedState.value = sidebarCollapsed.value
    }
    sidebarStore.setOpen(false, { persist: false })
  } else {
    sidebarStore.setOpen(lastDesktopOpenState.value ?? true)
    sidebarStore.setCollapsed(lastDesktopCollapsedState.value ?? false)
  }
}, { immediate: true })

watch(() => sidebarOpen.value, (value) => {
  if (!isMobile.value) {
    lastDesktopOpenState.value = value
  }
})

watch(() => sidebarCollapsed.value, (value) => {
  if (!isMobile.value) {
    lastDesktopCollapsedState.value = value
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

// Watcher pour s'assurer que la sidebar reste pliée lors de la navigation
watch(() => route.path, (newPath, oldPath) => {
  // Si l'utilisateur navigue vers une nouvelle page, on ne change pas l'état de la sidebar
  // La sidebar reste dans son état actuel (pliée ou dépliée)
  console.log('[DashboardLayout] Navigation détectée:', { from: oldPath, to: newPath, sidebarCollapsed: sidebarCollapsed.value })
}, { immediate: false })

// Watcher pour tracer tous les changements de sidebarCollapsed
watch(() => sidebarCollapsed.value, (newValue, oldValue) => {
  console.log('[DashboardLayout] sidebarCollapsed changé:', { 
    from: oldValue, 
    to: newValue, 
    windowWidth: window.innerWidth,
    windowHeight: window.innerHeight,
    stack: new Error().stack 
  })
}, { immediate: false })
</script>

<style scoped>
/* Layout principal du dashboard */
.dashboard-layout {
  height: 100vh;
  height: 100dvh; /* Utiliser dvh sur navigateurs modernes pour mobile */
  /* Fond plein blanc pour retirer le gris en arrière-plan */
  background: #ffffff;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  /* Assurer que le layout reste stable */
  min-height: 100vh;
  min-height: 100dvh; /* Utiliser dvh sur navigateurs modernes pour mobile */
  /* Empêcher le bounce scroll sur iOS qui affecte les éléments fixed */
  overscroll-behavior: contain;
  -webkit-overflow-scrolling: touch;
}

/* Container principal */
.dashboard-main-container {
  display: flex;
  flex: 1;
  min-height: 0;
  position: relative;
  overflow: hidden;
  /* Assurer que le container principal reste stable */
  flex-shrink: 1;
}

/* Contenu du dashboard */
.dashboard-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  background: #fff;
  border-radius: 12px 0 0 0;
  box-shadow: -2px 0 12px rgba(0, 0, 0, 0.05);
  margin: 0;
  /* Eviter les scroll imbriqués: on confie le scroll à .dashboard-main */
  overflow: hidden;
  /* Assurer que le contenu reste stable */
  flex-shrink: 1;
}

/* Zone principale */
.dashboard-main {
  flex: 1;
  padding: 1.5rem 2rem 1.5rem;
  /* Zone de scroll principale (iOS friendly) */
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  /* Réduit l'effet de rebond proche du header/footer sur navigateurs compatibles */
  overscroll-behavior-y: contain;
  touch-action: pan-y;
  background: #fff;
  position: relative;
  display: flex;
  flex-direction: column;
  /* Assurer que le contenu principal reste stable */
  min-height: 0;
  transition: padding-bottom 0.2s ease;
}

.dashboard-main.with-mobile-nav {
  padding-bottom: 5.5rem;
}

/* Responsive design - Optimisé pour que le header et les onglets restent visibles */
@media (max-width: 1200px) {
  .dashboard-main {
    padding: 1.25rem 1.5rem 1.25rem;
  }
}

@media (max-width: 1024px) {
  .dashboard-main {
    padding: 1.25rem 1.5rem 1.25rem;
  }
  
  .dashboard-content {
    margin: 0;
    /* Assurer que le contenu reste stable */
    border-radius: 8px 0 0 0;
  }
}

@media (max-width: 768px) {
  .dashboard-main {
    padding: 0.5rem 1rem 0.75rem;
  }
  
  .dashboard-content {
    margin: 0;
    border-radius: 0;
    /* Assurer que le contenu reste stable sur mobile */
    flex-shrink: 1;
  }
  
  .dashboard-layout {
    background: #fff;
  }
  
  .dashboard-main-container {
    /* Assurer que le container principal reste stable */
    flex-shrink: 1;
    /* Compenser le header fixe sur mobile (56px = min-height du header mobile) */
    margin-top: 56px;
  }
}

@media (max-width: 480px) {
  .dashboard-main {
    padding: 0.5rem 0.75rem;
  }
  
  .dashboard-content {
    /* Assurer que le contenu reste stable */
    flex-shrink: 1;
  }
}

/* Assurer que le layout reste stable même sur très petit écran */
@media (max-width: 360px) {
  .dashboard-main {
    padding: 0.4rem 0.6rem;
  }
}

/* Assurer que le layout reste stable en mode paysage sur mobile */
@media (max-height: 500px) and (orientation: landscape) {
  .dashboard-main {
    padding: 0.5rem 1rem;
  }
}

/* États spéciaux */
.dashboard-layout.loading {
  pointer-events: none;
  opacity: 0.7;
}

.dashboard-layout.loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  z-index: 1000;
}

@keyframes spin {
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

/* Optimisations de performance */
.dashboard-layout {
  will-change: transform;
  transform: translateZ(0);
}

.dashboard-content {
  will-change: transform;
  transform: translateZ(0);
}
</style> 
