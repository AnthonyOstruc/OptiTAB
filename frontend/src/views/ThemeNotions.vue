<template>
  <DashboardLayout>
    <section class="theme-notions-section">
      <!-- Bouton de retour -->
      <BackButton 
        text="Retour aux thèmes" 
        :customAction="goBackToThemes"
        position="top-left"
      />
      
      <!-- En-tête de la page -->
      <div class="theme-notions-header">
        <div class="theme-notions-header-content">
          <h1 class="theme-notions-title">{{ themeNom }}</h1>
          <p class="theme-notions-subtitle">Sélectionnez une notion pour accéder aux chapitres</p>
        </div>
        <div class="theme-notions-header-icon" :style="{ backgroundColor: themeColor }">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
      </div>

      <!-- Contenu principal -->
      <div class="theme-notions-content">
        <!-- État de chargement -->
        <div v-if="loading" class="theme-notions-loader">
          <div class="loader-spinner"></div>
          <p>Chargement des notions...</p>
        </div>

        <!-- État d'erreur -->
        <div v-else-if="error" class="theme-notions-error">
          <div class="error-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h3>Erreur de chargement</h3>
          <p>{{ error }}</p>
          <button class="retry-button" @click="loadThemeNotions(currentThemeId)">
            Réessayer
          </button>
        </div>

        <!-- Grille des notions -->
        <div v-else class="notions-grid">
          <TransitionGroup 
            name="notion-card" 
            tag="div" 
            class="notions-grid-inner"
          >
            <NotionCard
              v-for="(notion, index) in notions"
              :key="notion.id"
              :title="notion.nom"
              :description="notion.description || `Explorez les chapitres de ${notion.nom}`"
              @click="onNotionClick(notion.id)"
              :style="{ animationDelay: `${index * 0.1}s` }"
            />
          </TransitionGroup>
        </div>

        <!-- Message si aucune notion -->
        <div v-if="!loading && !error && notions.length === 0" class="notions-empty">
          <div class="empty-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h3>Aucune notion disponible</h3>
          <p>Il n'y a pas encore de notions pour ce thème.</p>
        </div>
      </div>
    </section>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import { getThemeDetail, getNotions } from '@/api'
import NotionCard from '@/components/UI/NotionCard.vue'
import { useSubjectsStore } from '@/stores/subjects/index'
import BackButton from '@/components/common/BackButton.vue'

const route = useRoute()
const router = useRouter()
const subjectsStore = useSubjectsStore()

const currentThemeId = computed(() => route.params.themeId)

const notions = ref([])
const themeNom = ref('')
const themeColor = ref('#3b82f6')
const loading = ref(true)
const error = ref('')

// Fonction pour revenir aux thèmes
function goBackToThemes() {
  // Récupérer la matière du thème pour naviguer correctement
  const matiereId = subjectsStore.activeMatiereId
  if (matiereId) {
    router.push({ name: 'Themes', params: { matiereId } })
  } else {
    router.push({ name: 'Dashboard' })
  }
}

// Fonction pour charger les notions d'un thème
const loadThemeNotions = async (themeId) => {
  if (!themeId) return
  
  loading.value = true
  error.value = ''
  
  try {
    console.log('[ThemeNotions] Chargement des notions pour le thème:', themeId)
    
    // Charger les informations du thème
    const themeData = await getThemeDetail(themeId)
    themeNom.value = themeData.nom
    themeColor.value = themeData.couleur || '#3b82f6'
    
    // Charger toutes les notions et filtrer par thème, puis trier par ordre croissant
    const notionsData = await getNotions()
    notions.value = notionsData
      .filter(notion => notion.theme === parseInt(themeId))
      .sort((a, b) => {
        const ao = Number(a?.ordre ?? 0)
        const bo = Number(b?.ordre ?? 0)
        if (ao !== bo) return ao - bo
        return String(a?.nom || '').localeCompare(String(b?.nom || ''))
      })
    
    console.log('[ThemeNotions] Notions chargées:', notions.value.length)
  } catch (e) {
    console.error('[ThemeNotions] Erreur lors du chargement:', e)
    error.value = e.response?.data?.detail || 'Erreur lors du chargement des notions'
  } finally {
    loading.value = false
  }
}

// Fonction appelée quand on clique sur une notion
function onNotionClick(notionId) {
  router.push({ name: 'Chapitres', params: { notionId } })
}

// Lifecycle
onMounted(() => {
  const themeId = currentThemeId.value
  if (themeId) {
    loadThemeNotions(themeId)
  }
})
</script>

<style scoped>
.theme-notions-section {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  min-height: 100vh;
  padding: 2rem 5vw 4rem 5vw;
}

/* En-tête */
.theme-notions-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 3rem;
  box-shadow: 
    0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.theme-notions-header-content {
  flex: 1;
}

.theme-notions-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.theme-notions-subtitle {
  font-size: 1.125rem;
  color: #64748b;
  margin: 0;
  font-weight: 500;
}

.theme-notions-header-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 80px;
  height: 80px;
  border-radius: 20px;
  color: white;
  flex-shrink: 0;
}

/* Contenu principal */
.theme-notions-content {
  max-width: 1200px;
  margin: 0 auto;
}

/* Chargement et erreurs */
.theme-notions-loader,
.theme-notions-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.loader-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 64px;
  height: 64px;
  background: #fef2f2;
  border-radius: 16px;
  color: #ef4444;
  margin-bottom: 1rem;
}

.retry-button {
  background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3);
}

/* Grille des notions */
.notions-grid {
  width: 100%;
}

.notions-grid-inner {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  justify-items: center;
}

/* État vide */
.notions-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 80px;
  height: 80px;
  background: #f1f5f9;
  border-radius: 20px;
  color: #64748b;
  margin-bottom: 1.5rem;
}

/* Animations des cartes */
.notion-card-enter-active {
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.notion-card-enter-from {
  opacity: 0;
  transform: translateY(30px) scale(0.9);
}

.notion-card-enter-to {
  opacity: 1;
  transform: translateY(0) scale(1);
}

/* Responsive */
@media (max-width: 1024px) {
  .theme-notions-section {
    padding: 1.5rem 3vw 3rem 3vw;
  }
  
  .notions-grid-inner {
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.5rem;
  }
}

@media (max-width: 768px) {
  .theme-notions-section {
    padding: 1rem 2vw 2rem 2vw;
  }
  
  .theme-notions-header {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
    padding: 1.25rem;
  }
  
  .theme-notions-title {
    font-size: 1.75rem;
  }
  
  .notions-grid-inner {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
</style>
