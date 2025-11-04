<template>
  <DashboardLayout>
    <section class="notions-page-base">
      <!-- Bouton de retour vers le dashboard -->
      <div class="nav-header-base">
        <BackButton 
          text="Retour au dashboard" 
          :customAction="goBackToMatieres"
          position="top-left"
        />
      </div>

      <!-- Contenu principal -->
      <div class="main-content-base">
        <div class="notions-container">
          <ThemeNotionsView
            :matiere-id="currentMatiereId"
            :notion-route-name="'ExercicesByNotion'"
            :show-search="false"
            :deep-search-in-exercises="true"
          />
        </div>
      </div>
    </section>
  </DashboardLayout>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import { getMatieresUtilisateur } from '@/api'
import ThemeNotionsView from '@/components/common/ThemeNotionsView.vue'
import SelectedMatiereHeader from '@/components/common/SelectedMatiereHeader.vue'
import { useSubjectsStore } from '@/stores/subjects/index'
import { useUserStore } from '@/stores/user'
import BackButton from '@/components/common/BackButton.vue'

// Nom explicite pour KeepAlive
defineOptions({ name: 'Themes' })

const route = useRoute()
const router = useRouter()
const subjectsStore = useSubjectsStore()
const userStore = useUserStore()

// Fonction pour revenir aux matières
function goBackToMatieres() {
  router.push({ name: 'Dashboard' })
}

// Utiliser la matière active du store ou celle de la route (string->number normalisé)
const currentMatiereId = computed(() => {
  const id = subjectsStore.activeMatiereId || route.params.matiereId
  return id ? Number(id) : null
})

// Fonction appelée quand on clique sur un thème
function onThemeClick(themeId) {
  router.push({ name: 'ThemeNotions', params: { themeId } })
}

function onMatiereChanged(newMatiereId) {
  if (newMatiereId && Number(newMatiereId) !== Number(currentMatiereId.value)) {
    router.push({ name: 'Themes', params: { matiereId: String(newMatiereId) } })
  }
}

// Fonction appelée quand on clique sur une notion (fallback)
function onNotionClick(notionId) {
  router.push({ name: 'ExercicesByNotion', params: { notionId } })
}

// Le composant enfant gère le chargement et le cache
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
