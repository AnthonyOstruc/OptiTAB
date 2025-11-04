<template>
  <DashboardLayout>
    <div class="notions-page-base">
      <!-- Navigation Header -->
      <div class="nav-header-base">
        <BackButton 
          text="Retour au dashboard" 
          :customAction="goBackToDashboard"
          position="top-left"
        />
      </div>

      

      <!-- Main Content -->
      <div class="main-content-base">
        <div class="notions-container">
          <ThemeNotionsView
            :matiere-id="currentMatiereId"
            :notion-route-name="'CourseByNotion'"
            :show-search="false"
            :deep-search-in-courses="true"
          />
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import BackButton from '@/components/common/BackButton.vue'
import ThemeNotionsView from '@/components/common/ThemeNotionsView.vue'
import { useSubjectsStore } from '@/stores/subjects/index'
import { useUserStore } from '@/stores/user'

// Nom explicite pour KeepAlive
defineOptions({ name: 'CourseNotions' })

const route = useRoute()
const router = useRouter()
const subjectsStore = useSubjectsStore()
const userStore = useUserStore()

// Récupérer l'ID de la matière courante
const currentMatiereId = computed(() => {
  let id = subjectsStore.activeMatiereId || route.params.matiereId
  if (!id) {
    // Fallback première visite: forcer "Mathématiques" si possible
    try {
      const normalize = (s) => (s || '').toString().normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase()
      const list = (window.__SUBJECTS_CACHE__ && Array.isArray(window.__SUBJECTS_CACHE__)) ? window.__SUBJECTS_CACHE__ : []
      const math = list.find(m => normalize(m.nom || m.titre).includes('mathem'))
      id = math?.id || list[0]?.id || null
      if (id) subjectsStore.setActiveMatiere(id)
    } catch (_) {}
  }
  return id ? Number(id) : null
})

// Fonction pour retourner au dashboard
function goBackToDashboard() {
  router.push('/dashboard')
}
</script>

<style scoped>
.notions-page-base {
  background: #ffffff;
  min-height: 100vh;
  padding: 0;
}

.nav-header-base {
  padding: 0 0 1rem 0;
  background: white;
}

.main-content-base {
  width: 100%;
  max-width: none;
  margin: 0;
  padding: 0;
}

.notions-container {
  width: 100%;
  padding-bottom: 40px;
}
</style> 
