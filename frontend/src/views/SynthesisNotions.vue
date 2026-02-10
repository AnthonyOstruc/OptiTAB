<template>
  <DashboardLayout>
    <div class="notions-page-base">
      <div class="nav-header-base">
        <BackButton 
          text="Retour au dashboard" 
          :customAction="goBackToMatieres"
          position="main-notions"
        />
      </div>

      <div class="main-content-base">
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Chargement...</p>
        </div>
        <div v-else class="notions-container">
          <ThemeNotionsView
            :matiere-id="currentMatiereId"
            :notion-route-name="props.notionRouteName"
            :synthesis-sheet-type="props.sheetType"
            :filter-notions-by-sheets="true"
            :show-search="false"
            :deep-search-in-sheets="true"
          />
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import ThemeNotionsView from '@/components/common/ThemeNotionsView.vue'
import BackButton from '@/components/common/BackButton.vue'
import { useSubjectsStore } from '@/stores/subjects/index'

// Nom explicite pour KeepAlive
defineOptions({ name: 'SynthesisNotions' })

const props = defineProps({
  sheetType: {
    type: String,
    default: 'summary'
  },
  notionRouteName: {
    type: String,
    default: 'SynthesisByNotion'
  },
  pageTitle: {
    type: String,
    default: 'Fiches de Synthèse'
  }
})

const route = useRoute()
const router = useRouter()
const subjectsStore = useSubjectsStore()

function goBackToMatieres() {
  router.push({ name: 'Dashboard' })
}

const currentMatiereId = computed(() => {
  const id = subjectsStore.activeMatiereId || route.params.matiereId || route.query.matiereId
  return id ? Number(id) : null
})

const loading = ref(true)
onMounted(() => { loading.value = false })
</script>

<style scoped>
.notions-page-base {
  background: #ffffff;
  min-height: 100vh;
  padding: 0;
}

:deep(.dashboard-main) {
  padding-top: 0 !important;
  padding-left: 0 !important;
}

:deep(.dashboard-main.with-mobile-nav) {
  padding-top: 0 !important;
}

.nav-header-base {
  padding: 0;
  margin: 0 0 3rem 0;
  display: flex;
  background: white;
}

@media (max-width: 1200px) {
  :deep(.dashboard-main) {
    padding-left: 0 !important;
  }
}

@media (max-width: 768px) {
  :deep(.dashboard-main) {
    padding-left: 0 !important;
    padding-right: 0 !important;
  }
}

@media (max-width: 480px) {
  :deep(.dashboard-main) {
    padding-left: 0 !important;
    padding-right: 0 !important;
  }
}

@media (max-width: 360px) {
  :deep(.dashboard-main) {
    padding-left: 0 !important;
    padding-right: 0 !important;
  }
}

.main-content-base {
  width: 100%;
  max-width: none;
  margin: 0;
  padding: 0 2rem 1.5rem 2rem;
}

@media (max-width: 1200px) {
  .main-content-base {
    padding: 0 1.5rem 1.25rem 1.5rem;
  }
}

@media (max-width: 768px) {
  .main-content-base {
    padding: 0 1rem 0.75rem 1rem;
  }
}

@media (max-width: 480px) {
  .main-content-base {
    padding: 0 0.75rem 0.5rem 0.75rem;
  }
}

@media (max-width: 360px) {
  .main-content-base {
    padding: 0 0.6rem 0.4rem 0.6rem;
  }
}

.notions-container {
  width: 100%;
  padding-bottom: 40px;
}

.loading-state { 
  text-align: center; 
  padding: 4rem 2rem; 
  background: white; 
  border-radius: 12px; 
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
} 

.loading-spinner { 
  width: 40px; 
  height: 40px; 
  border: 3px solid #e5e7eb; 
  border-top: 3px solid #60a5fa; 
  border-radius: 50%; 
  animation: spin 1s linear infinite; 
  margin: 0 auto 1rem; 
}

@keyframes spin { 
  0% { transform: rotate(0deg);} 
  100% { transform: rotate(360deg);} 
}
</style>
