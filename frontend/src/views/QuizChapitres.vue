<template>
  <DashboardLayout>
    <ChapitresListView
      title="Choisissez un chapitre pour vos quiz"
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
import { getChapitresByNotion } from '@/api'
import { useSubjectsStore } from '@/stores/subjects/index'

const route = useRoute()
const router = useRouter()
const subjectsStore = useSubjectsStore()
const chapitres = ref([])

// Récupérer la matière active
const currentMatiereId = computed(() => {
  return subjectsStore.activeMatiereId || route.params.matiereId
})

// Fonction pour revenir aux notions
function goBackToNotions() {
  const matiereId = currentMatiereId.value
  if (matiereId) {
    router.push({ name: 'QuizNotions', params: { matiereId } })
  } else {
    router.back()
  }
}

onMounted(async () => {
  try {
    const notionId = route.params.notionId
    if (!notionId) { chapitres.value = []; return }
    const list = await getChapitresByNotion(notionId)
    chapitres.value = Array.isArray(list) ? list : (list?.data || [])
  } catch (e) {
    chapitres.value = []
  }
})

function onChapitreClick(chapitreId) {
  router.push({ name: 'ChapterQuiz', params: { chapitreId } })
}
</script>

 