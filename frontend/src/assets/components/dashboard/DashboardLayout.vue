<template>
  <div class="dashboard-layout">
    <!-- Header du dashboard -->
    <DashboardHeader 
      :sidebarOpen="sidebarOpen" 
      :sidebar-collapsed="sidebarCollapsed"
      @toggle-sidebar="toggleSidebarCollapsed"
      @subject-changed="handleSubjectChange"
    />
    
    <!-- Contenu principal -->
    <div class="dashboard-main-container">
                <!-- Sidebar principale -->
      <Sidebar 
        v-show="sidebarOpen" 
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
        <main class="dashboard-main">
          <slot />
        </main>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed, ref, onMounted, nextTick, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from './Sidebar.vue'
import DashboardHeader from './DashboardHeader.vue'
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

// Méthodes
const toggleSidebar = () => {
  sidebarStore.toggleOpen()
  emit('sidebar-toggle', sidebarStore.isOpen)
}

const toggleSidebarCollapsed = () => {
  sidebarStore.toggleCollapsed()
  console.log('[DashboardLayout] Sidebar toggled:', { collapsed: sidebarStore.isCollapsed })
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
  
  // Attendre que le DOM soit prêt
  await nextTick()
  
  console.log('[DashboardLayout] onMounted - État final:', { sidebarOpen: sidebarOpen.value, sidebarCollapsed: sidebarCollapsed.value })
  
  // Initialiser la sidebar si elle existe
  if (sidebarRef.value) {
    // La sidebar se charge automatiquement via onMounted
  }
})

onUnmounted(() => {
  // aucun nettoyage nécessaire : le store garde les listeners globaux tant que l'app vit
})

watch(() => route.path, (newPath, oldPath) => {
  console.log('[DashboardLayout] Navigation détectée:', { from: oldPath, to: newPath, sidebarCollapsed: sidebarCollapsed.value })
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

/* Responsive design - Optimisé pour que le header et les onglets restent visibles */
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
    /* Assurer que le layout reste stable même sur très petit écran */
    min-height: 100vh;
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
