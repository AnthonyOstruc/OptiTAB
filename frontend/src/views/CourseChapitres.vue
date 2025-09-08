<template>
  <DashboardLayout>
    <ChapitresListView
      title="Chapitres de cours disponibles"
      :chapitres="chapitres"
      back-button-text="Retour aux notions"
      :back-action="goBackToNotions"
      :on-chapitre-click="onChapitreClick"
    />
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import ChapitresListView from '@/components/common/ChapitresListView.vue'
import { getChapitresByNotion, getNotionDetail } from '@/api'
import { useSubjectsStore } from '@/stores/subjects/index'

const route = useRoute()
const router = useRouter()
const subjectsStore = useSubjectsStore()

const chapitres = ref([])
const matiereIdForNotion = ref(null)

// Récupérer la matière active
const currentMatiereId = computed(() => {
  return subjectsStore.activeMatiereId || route.params.matiereId
})

// Fonction pour revenir aux notions
function goBackToNotions() {
  const matiereId = matiereIdForNotion.value || currentMatiereId.value
  if (matiereId) router.push({ name: 'CourseNotions', params: { matiereId: String(matiereId) } })
  else router.back()
}

function onChapitreClick(chapitreId) {
  router.push({ name: 'CourseChapitre', params: { chapitreId } })
}

onMounted(async () => {
  try {
    const notionId = route.params.notionId
    if (!notionId) return
    
    // Récupérer chapitres de la notion (même logique que Chapitres.vue)
    const chaptersData = await getChapitresByNotion(notionId)
    chapitres.value = Array.isArray(chaptersData) ? chaptersData : []
    
    // Récupérer matiereId pour back bouton
    const notion = await getNotionDetail(notionId)
    matiereIdForNotion.value = notion?.matiere || null
  } catch (error) {
    console.error('Erreur lors du chargement des chapitres de cours:', error)
    chapitres.value = []
  }
})
</script>

 