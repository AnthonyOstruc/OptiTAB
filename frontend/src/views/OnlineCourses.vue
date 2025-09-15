<template>
  <DashboardLayout>
    <section class="online-courses-section">
      <h2 class="online-courses-title">Choisissez une matière pour vos cours en ligne</h2>
      <div class="online-courses-grid">
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

    // Charger les matières pour affichage
    const { data } = await getMatieres()
    matieres.value = Array.isArray(data) ? data : (data?.results || [])
    // Exposer au cache global léger pour fallback
    try { window.__SUBJECTS_CACHE__ = matieres.value } catch (_) {}

    // Première visite: choisir Mathématiques par défaut si rien d'actif
    if (!subjectsStore.activeMatiereId && matieres.value.length > 0) {
      const normalize = (s) => (s || '').toString().normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase()
      const math = matieres.value.find(m => normalize(m.nom || m.titre).includes('mathem'))
      const chosen = math || matieres.value[0]
      await subjectsStore.addMatiereId(chosen.id)
      await subjectsStore.setActiveMatiere(chosen.id)
      await router.push({ name: 'CourseNotions', params: { matiereId: chosen.id } })
      return
    }

    console.log(`[OnlineCourses] Matières chargées:`, matieres.value.length)
  } catch (e) {
    matieres.value = []
  }
})

function onSubjectClick(matiereNom) {
  const matiere = matieres.value.find(m => m.nom === matiereNom)
  if (matiere) {
    // Définir comme matière active et naviguer
    subjectsStore.setActiveMatiere(matiere.id)
    // Pour l'instant, on navigue vers les notions
    // Plus tard, on pourra créer des routes spécifiques pour les cours
    router.push({ name: 'CourseNotions', params: { matiereId: matiere.id } })
  }
}
</script>

<style scoped>
.online-courses-section {
  background: #fff;
  padding: 0 5vw 40px 5vw;
  text-align: center;
}

.online-courses-title {
  font-size: 2rem;
  color: #193e8e;
  margin-bottom: 40px;
  font-weight: 800;
}

.online-courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  max-width: 800px;
  margin: 0 auto;
}

@media (max-width: 640px) {
  .online-courses-title {
    font-size: 1.5rem;
    margin-bottom: 30px;
  }
  
  .online-courses-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .online-courses-section {
    padding: 0 4vw 30px 4vw;
  }
}
</style> 