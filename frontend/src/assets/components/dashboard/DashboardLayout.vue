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
    
      <!-- Debug: Indicateur d'etat de la sidebar (temporaire) -->
      <div v-if="false" style="position: fixed; top: 10px; right: 10px; background: #333; color: white; padding: 5px; border-radius: 4px; font-size: 12px; z-index: 9999;">
        Sidebar: {{ sidebarCollapsed ? 'Pliee' : 'Depliee' }}
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
import { computed, ref, onMounted, nextTick, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from './Sidebar.vue'
import DashboardHeader from './DashboardHeader.vue'
import MobileBottomNav from './MobileBottomNav.vue'
import { useUserStore } from '@/stores/user'
import { useSidebarStore } from '@/stores/sidebar'

const emit = defineEmits(['sidebar-toggle', 'navigation', 'subject-changed'])

const sidebarRef = ref(null)
const route = useRoute()
const userStore = useUserStore()

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
const lastDesktopOpenState = ref(true)
const lastDesktopCollapsedState = ref(false)

const handleResize = () => {
  if (typeof window === 'undefined') return
  viewportWidth.value = window.innerWidth
}

const toggleSidebar = () => {
  sidebarStore.toggleOpen()
  emit('sidebar-toggle', sidebarStore.isOpen)
}

const toggleSidebarCollapsed = () => {
  sidebarStore.toggleCollapsed()
  console.log('[DashboardLayout] Sidebar toggled:', { collapsed: sidebarStore.isCollapsed })
}

const handleHeaderToggle = () => {
  if (isMobile.value) {
    toggleSidebar()
  } else {
    if (!sidebarOpen.value) {
      sidebarStore.setCollapsed(false)
      sidebarStore.setOpen(true)
      return
    }

    if (!sidebarCollapsed.value) {
      sidebarStore.setCollapsed(true)
      return
    }

    sidebarStore.setOpen(false)
  }
}

const handleNavigation = (navigationData) => {
  emit('navigation', navigationData)
}

const handleSubjectChange = (subjectId) => {
  emit('subject-changed', subjectId)
}

onMounted(async () => {
  console.log('[DashboardLayout] onMounted - etat initial:', { sidebarOpen: sidebarOpen.value, sidebarCollapsed: sidebarCollapsed.value })
  sidebarStore.init()
  window.addEventListener('resize', handleResize, { passive: true })
  handleResize()
  
  await nextTick()
  
  console.log('[DashboardLayout] onMounted - etat final:', { sidebarOpen: sidebarOpen.value, sidebarCollapsed: sidebarCollapsed.value })
  
  if (sidebarRef.value) {
    // Sidebar initialisee automatiquement
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

watch(isMobile, (val, oldVal) => {
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

watch(() => route.path, (newPath, oldPath) => {
  console.log('[DashboardLayout] Navigation detectee:', { from: oldPath, to: newPath, sidebarCollapsed: sidebarCollapsed.value })
})
</script>

<style scoped>
/* Layout principal du dashboard */
.dashboard-layout {
  height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  /* Assurer que le layout reste stable */
  min-height: 100vh;
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
  overflow-y: auto;
  /* Assurer que le contenu reste stable */
  flex-shrink: 1;
}

/* Zone principale */
.dashboard-main {
  flex: 1;
  padding: 1.5rem 2rem;
  overflow-y: auto;
  background: #fff;
  position: relative;
  display: flex;
  flex-direction: column;
  /* Assurer que le contenu principal reste stable */
  min-height: 0;
}

.dashboard-main.with-mobile-nav {
  padding-bottom: 5.5rem;
}

/* Responsive design - Optimise pour que le header et les onglets restent visibles */
@media (max-width: 1200px) {
  .dashboard-main {
    padding: 1.25rem 1.5rem;
  }
}

@media (max-width: 1024px) {
  .dashboard-main {
    padding: 1rem 1.25rem;
  }
  
  .dashboard-content {
    margin: 0;
    /* Assurer que le contenu reste stable */
    border-radius: 8px 0 0 0;
  }
  
  .dashboard-layout {
    /* Assurer que le layout reste stable sur tablette */
    min-height: 100vh;
  }
}

@media (max-width: 768px) {
  .dashboard-main {
    padding: 0.75rem 1rem;
  }
  
  .dashboard-content {
    margin: 0;
    border-radius: 0;
    /* Assurer que le contenu reste stable sur mobile */
    flex-shrink: 1;
  }
  
  .dashboard-layout {
    background: #fff;
    /* Assurer que le layout reste stable sur mobile */
    min-height: 100vh;
  }
  
  .dashboard-main-container {
    /* Assurer que le container principal reste stable */
    flex-shrink: 1;
  }
}

@media (max-width: 480px) {
  .dashboard-main {
    padding: 0.5rem 0.75rem;
  }
  
  .dashboard-layout {
    /* Assurer que le layout reste stable meme sur tres petit ecran */
    min-height: 100vh;
  }
  
  .dashboard-content {
    /* Assurer que le contenu reste stable */
    flex-shrink: 1;
  }
}

/* Assurer que le layout reste stable meme sur tres petit ecran */
@media (max-width: 360px) {
  .dashboard-main {
    padding: 0.4rem 0.6rem;
  }
  
  .dashboard-layout {
    /* Assurer que le layout reste stable */
    min-height: 100vh;
  }
}

/* Assurer que le layout reste stable en mode paysage sur mobile */
@media (max-height: 500px) and (orientation: landscape) {
  .dashboard-layout {
    /* Assurer que le layout reste stable en mode paysage */
    min-height: 100vh;
  }
  
  .dashboard-main {
    padding: 0.5rem 1rem;
  }
}

/* Etats speciaux */
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
