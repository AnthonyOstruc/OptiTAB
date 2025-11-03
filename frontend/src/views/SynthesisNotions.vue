<template>
  <DashboardLayout>
    <div class="notions-page-base">
      <div class="nav-header-base">
        <BackButton 
          text="Retour au dashboard" 
          :customAction="goBackToMatieres"
          position="top-left"
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
            :notion-route-name="'SynthesisByNotion'"
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

const route = useRoute()
const router = useRouter()
const subjectsStore = useSubjectsStore()

function goBackToMatieres() {
  router.push({ name: 'Dashboard' })
}

const currentMatiereId = computed(() => {
  const id = subjectsStore.activeMatiereId || route.params.matiereId
  return id ? Number(id) : null
})

const loading = ref(true)
onMounted(() => { loading.value = false })
</script>

<style scoped>
.loading-state { text-align: center; padding: 4rem 2rem; background: white; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);} 
.loading-spinner { width: 40px; height: 40px; border: 3px solid #e5e7eb; border-top: 3px solid #60a5fa; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 1rem; }
@keyframes spin { 0% { transform: rotate(0deg);} 100% { transform: rotate(360deg);} }
</style>
