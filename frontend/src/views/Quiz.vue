<template>
  <DashboardLayout>
    <section class="quiz-section">
      <h2 class="quiz-title">Choisissez une matière pour vos quiz QCM</h2>
      <div class="quiz-grid">
        <BaseCard
          v-for="matiere in matieres"
          :key="matiere.id"
          :title="matiere.nom"
          :icon="matiere.svg_icon"
          :description="matiere.description || ''"
          @click="onSubjectClick(matiere.nom)"
        />
      </div>
    </section>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import BaseCard from '@/components/UI/BaseCard.vue'
import { getMatieres } from '@/api'
import { useRouter } from 'vue-router'
import { useSubjectsStore } from '@/stores/subjects/index'
import { useUserStore } from '@/stores/user'
import { useSmartNavigation } from '@/composables/useSmartNavigation'

const router = useRouter()
const matieres = ref([])
const subjectsStore = useSubjectsStore()
const userStore = useUserStore()
const { checkAndRedirectIfNeeded } = useSmartNavigation()

onMounted(async () => {
  try {
    // Vérifier s'il faut rediriger automatiquement vers une matière
    const wasRedirected = await checkAndRedirectIfNeeded()
    if (wasRedirected) {
      return // Navigation automatique effectuée
    }

    // Charger les matières pour affichage (filtrées par niveau)
    const niveauId = userStore.niveau_pays?.id
    const { data } = await getMatieres(niveauId)
    matieres.value = data
    console.log(`[Quiz] Matières chargées pour niveau ${niveauId}:`, matieres.value.length)
  } catch (e) {
    matieres.value = []
  }
})

function onSubjectClick(matiereNom) {
  const matiere = matieres.value.find(m => m.nom === matiereNom)
  if (matiere) {
    // Définir comme matière active et naviguer
    subjectsStore.setActiveMatiere(matiere.id)
    router.push({ name: 'QuizNotions', params: { matiereId: matiere.id } })
  }
}
</script>

<style scoped>
.quiz-section {
  background: #fff;
  padding: 0 5vw 40px 5vw;
  text-align: center;
}
.quiz-title {
  font-size: 2rem;
  color: #193e8e;
  margin-bottom: 40px;
  font-weight: 800;
}
.quiz-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  max-width: 1100px;
  margin: 0 auto;
  gap: 30px;
  justify-items: center;
}
</style> 