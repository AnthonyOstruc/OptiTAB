<template>
  <DashboardLayout>
    <!-- Section de sélection de matière (affichée seulement si nécessaire) -->
    <section v-if="showMatiereSelection" class="exercises-section">
      <h2 class="exercises-title">Choisissez une matière pour vos exercices guidés</h2>
      
      <!-- Message d'aide si l'utilisateur a des matières sélectionnées -->
      <div v-if="subjectsStore.selectedMatieresIds.length > 0" class="help-message">
        <p>💡 <strong>Astuce :</strong> Vous avez {{ subjectsStore.selectedMatieresIds.length }} matière(s) sélectionnée(s). 
        Cliquez sur une matière ci-dessous ou utilisez vos onglets en haut pour accéder directement à vos matières favorites.</p>
      </div>
      
      <div class="exercises-grid">
        <BaseCard
          v-for="matiere in matieres"
          :key="matiere.id"
          :title="matiere.nom"
          :icon="matiere.svg_icon"
          :description="matiere.description || ''"
          :class="{ 'favorite': subjectsStore.isFavoriteMatiere(matiere.id) }"
          @click="onSubjectClick(matiere)"
        >
          <!-- Indicateur visuel pour les matières favorites -->
          <template v-if="subjectsStore.isFavoriteMatiere(matiere.id)" #badge>
            <span class="favorite-badge">⭐</span>
          </template>
        </BaseCard>
      </div>
      
      <!-- Message si aucune matière n'est disponible -->
      <div v-if="matieres.length === 0" class="no-matiere-message">
        <p>Aucune matière n'est actuellement disponible.</p>
        <p>Veuillez réessayer plus tard ou contactez l'administrateur.</p>
      </div>
    </section>
    
    <!-- Section de chargement -->
    <section v-else-if="isLoading" class="loading-section">
      <div class="loading-spinner">
        <div class="spinner" aria-hidden="true"></div>
        <p>Chargement de vos exercices...</p>
      </div>
    </section>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import BaseCard from '@/components/UI/BaseCard.vue'
import { getMatieres } from '@/api'
import { getMatieresUtilisateur } from '@/api/matieres.js'
import { getThemes } from '@/api/themes'
import { useRouter } from 'vue-router'
import { useSubjectsStore } from '@/stores/subjects/index'
import { useUserStore } from '@/stores/user'
import { useSmartNavigation } from '@/composables/useSmartNavigation'

const router = useRouter()
const matieres = ref([])
const themesParMatiere = ref({})
const isLoading = ref(true)
const subjectsStore = useSubjectsStore()
const userStore = useUserStore()
const { checkAndRedirectIfNeeded } = useSmartNavigation()

// Afficher toujours la section (loader à part) pour éviter l'écran vide
const showMatiereSelection = computed(() => !isLoading.value)

onMounted(async () => {
  try {
    isLoading.value = true
    
    // 1. Vérifier s'il faut rediriger automatiquement vers une matière
    const wasRedirected = await checkAndRedirectIfNeeded()
    if (wasRedirected) {
      console.log('[Exercises] Redirection automatique effectuée')
      return // Navigation automatique effectuée
    }

    // 2. Charger les matières disponibles pour l'utilisateur (includes fallback logique)
    try {
      const resp = await getMatieresUtilisateur()
      const list = resp?.data?.matieres_disponibles || []
      // Adapter au format attendu par la grille (id, nom, description, svg_icon)
      matieres.value = list.map(m => ({
        id: m.id,
        nom: m.nom,
        description: m.description || '',
        svg_icon: m.svg_icon || ''
      }))
    } catch (e) {
      // fallback: endpoint standard
      const { data } = await getMatieres()
      matieres.value = data || []
    }
    // 3. Pré-charger les thèmes de la matière active (si onglet ouvert) puis rediriger
    let activeMatiereId = subjectsStore.activeMatiereId
    const paysId = userStore.pays?.id || null
    const niveauId = userStore.niveau_pays?.id || null
    // Si aucune matière active mais des matières dispo, activer par défaut « Mathématiques » si présente
    if (!activeMatiereId && matieres.value.length > 0) {
      const normalize = (s) => (s || '').toString().normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase()
      const preferred = matieres.value.find(m => normalize(m.nom || m.titre).includes('mathem'))
      activeMatiereId = (preferred || matieres.value[0]).id
      subjectsStore.setActiveMatiere(activeMatiereId)
    }

    if (activeMatiereId) {
      const resp = await getThemes(activeMatiereId, niveauId, paysId)
      themesParMatiere.value[activeMatiereId] = Array.isArray(resp?.data) ? resp.data : (resp?.data || [])
      // Rediriger directement vers la page des thèmes de la matière active
      router.push({ name: 'Themes', params: { matiereId: String(activeMatiereId) } })
      return
    }
    
    // 3. Si l'utilisateur a des matières sélectionnées, proposer une redirection intelligente
    if (subjectsStore.selectedMatieresIds.length > 0 && !subjectsStore.activeMatiereId) {
      console.log('[Exercises] Utilisateur a des matières sélectionnées, proposant une redirection intelligente')
      // La navigation intelligente s'occupera de définir une matière active
    }
    
  } catch (error) {
    console.error('[Exercises] Erreur lors du chargement:', error)
    matieres.value = []
  } finally {
    isLoading.value = false
  }
})

function onSubjectClick(matiere) {
  try {
    // 1. Ajouter la matière aux sélectionnées si pas déjà présente
    if (!subjectsStore.isSelectedMatiere(matiere.id)) {
      subjectsStore.addMatiereId(matiere.id)
      console.log(`[Exercises] Matière ${matiere.nom} ajoutée aux sélectionnées`)
    }
    
    // 2. Définir comme matière active
    subjectsStore.setActiveMatiere(matiere.id)
    console.log(`[Exercises] Matière ${matiere.nom} définie comme active`)
    
    // 3. Naviguer vers les notions de cette matière
    router.push({ name: 'Themes', params: { matiereId: matiere.id.toString() } })
    
  } catch (error) {
    console.error('[Exercises] Erreur lors de la sélection de matière:', error)
  }
}
</script>

<style scoped>
.exercises-section {
  background: #fff;
  /* align with dashboard content left gutter */
  padding: 0.5rem 2vw 2rem 0;
  text-align: left;
}

@media (max-width: 768px) {
  .exercises-section {
    padding-left: 0;
    padding-right: 0;
  }
}

.exercises-title {
  font-size: 1.75rem;
  color: #193e8e;
  margin: 0 0 12px 0.25rem;
  font-weight: 800;
}

.help-message {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 15px 20px;
  margin-bottom: 30px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.help-message p {
  margin: 0;
  color: #6c757d;
  font-size: 0.95rem;
}

.exercises-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  max-width: 1100px;
  margin: 0 auto;
  gap: 30px;
  /* Stretch cards to fill their grid cell */
  justify-items: stretch;
}

.favorite {
  border: 2px solid #ffc107;
  position: relative;
}

.favorite-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 1.2rem;
}

.no-matiere-message {
  text-align: center;
  padding: 40px 20px;
  color: #6c757d;
}

.no-matiere-message p {
  margin: 10px 0;
  font-size: 1.1rem;
}

.loading-section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  background: #fff;
}

.loading-spinner {
  text-align: center;
  color: #193e8e;
  font-size: 1.2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.loading-spinner p {
  margin: 0;
}

.spinner {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 4px solid #e5ecff;
  border-top-color: #2563eb;
  animation: spin 0.9s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style> 
