<template>
  <DashboardLayout>
    <div class="notions-page">
      <!-- Navigation Header -->
      <div class="nav-header">
        <BackButton 
          text="Retour au dashboard" 
          :customAction="goBackToMatieres"
          position="top-left"
        />
      </div>

      <!-- Page Title -->
      <div class="page-title">
        <h1>{{ matiereNom }}</h1>
      </div>

      <!-- Main Content -->
      <div class="main-content">
        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Chargement...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="error-state">
          <p>{{ error }}</p>
          <button class="retry-btn" @click="loadNotions(currentMatiereId)">
            Réessayer
          </button>
        </div>

        <!-- Empty State -->
        <div v-else-if="notions.length === 0" class="empty-state">
          <p>Aucune notion disponible pour le moment.</p>
        </div>

        <!-- Notions Content -->
        <div v-else class="notions-container">
          <!-- Themes Organization -->
          <div v-if="notionsByTheme.length > 0" class="themes-layout">
            <div 
              v-for="(themeSection, themeIndex) in notionsByTheme" 
              :key="themeSection.theme?.id || 'no-theme'"
              class="theme-section"
            >
              <!-- Theme Header -->
              <div class="theme-header">
                <h2 class="theme-title">
                  <span class="theme-label">Thème {{ themeSection.theme?.ordre || '?' }}</span>
                  {{ themeSection.theme?.nom || 'Autres notions' }}
                </h2>
              </div>

              <!-- Notions Grid -->
              <div class="notions-grid">
                <div 
                  v-for="(notion, index) in themeSection.notions"
                  :key="notion.id"
                  class="notion-card"
                  @click="onNotionClick(notion.id)"
                >
                  <div class="card-content">
                    <div class="card-title">{{ notion.nom }}</div>
                    <div class="card-subtitle">
                      CHAPITRE {{ index + 1 }}
                    </div>
                    <div class="progress-bar">
                      <div class="progress-fill"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Simple Layout (no themes) -->
          <div v-else class="simple-layout">
            <div class="notions-grid">
              <div 
                v-for="(notion, index) in notions"
                :key="notion.id"
                class="notion-card"
                @click="onNotionClick(notion.id)"
              >
                <div class="card-content">
                  <div class="card-title">{{ notion.nom }}</div>
                  <div class="card-subtitle">
                    CHAPITRE {{ index + 1 }}
                  </div>
                  <div class="progress-bar">
                    <div class="progress-fill"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import { getNotions } from '@/api/notions'
import { getMatieres } from '@/api/matieres'
import { getThemes } from '@/api/themes'
import NotionCard from '@/components/UI/NotionCard.vue'
import MathJax from 'vue-mathjax-next'
import { useSubjectsStore } from '@/stores/subjects/index'
import BackButton from '@/components/common/BackButton.vue'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const subjectsStore = useSubjectsStore()
const userStore = useUserStore()

// Fonction pour revenir aux matières
function goBackToMatieres() {
  router.push({ name: 'Dashboard' })
}

// Utiliser la matière active du store ou celle de la route (normalisée en nombre)
const currentMatiereId = computed(() => {
  const id = subjectsStore.activeMatiereId || route.params.matiereId
  return id ? Number(id) : null
})

const notions = ref([])
const themes = ref([])
const matiereNom = ref('')
const loading = ref(true)
const error = ref('')

// Organiser les notions par thèmes
const notionsByTheme = computed(() => {
  if (!notions.value.length) return []
  
  // Grouper les notions par thème
  const grouped = {}
  const notionsWithoutTheme = []
  
  notions.value.forEach(notion => {
    if (notion.theme) {
      const themeId = notion.theme
      if (!grouped[themeId]) {
        const theme = themes.value.find(t => t.id === themeId)
        grouped[themeId] = {
          theme: theme,
          notions: []
        }
      }
      grouped[themeId].notions.push(notion)
    } else {
      notionsWithoutTheme.push(notion)
    }
  })
  
  // Convertir en tableau et trier par ordre des thèmes
  const result = Object.values(grouped).sort((a, b) => {
    const orderA = a.theme?.ordre || 999
    const orderB = b.theme?.ordre || 999
    return orderA - orderB
  })
  
  // Ajouter les notions sans thème à la fin si il y en a
  if (notionsWithoutTheme.length > 0) {
    result.push({
      theme: null,
      notions: notionsWithoutTheme
    })
  }
  
  return result
})

// Fonction pour charger les données d'une matière
const loadNotions = async (matiereId) => {
  if (!matiereId) return
  
  loading.value = true
  error.value = ''
  
  try {
    console.log('[Notions] Chargement des notions pour la matière:', matiereId)
    
    // Récupérer le nom de la matière, les notions et les thèmes (filtrés par niveau)
    const niveauId = userStore.niveau_pays?.id
    const paysId = userStore.pays?.id || null
    const [matieresResponse, notionsResponse, themesResponse] = await Promise.all([
      getMatieres(),
      getNotions(matiereId, niveauId),
      getThemes(matiereId, niveauId, paysId)
    ])
    
    const matiere = matieresResponse.data.find(m => m.id == matiereId)
    matiereNom.value = matiere ? matiere.nom : 'Matière'
    
    notions.value = notionsResponse.data
    themes.value = themesResponse.data
    
    console.log(`[Notions] Données chargées pour niveau ${niveauId}:`, {
      notions: notionsResponse.data.length,
      themes: themesResponse.data.length,
      matiere: matiere?.nom
    })
  } catch (e) {
    console.error('[Notions] Erreur lors du chargement:', e)
    error.value = "Impossible de charger les notions. Veuillez réessayer."
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadNotions(currentMatiereId.value)
})

// Surveiller les changements de matière active
watch(currentMatiereId, (newMatiereId, oldMatiereId) => {
  console.log('[Notions] Changement de matière détecté:', {
    ancienne: oldMatiereId,
    nouvelle: newMatiereId,
    routeParam: route.params.matiereId
  })
  
  if (newMatiereId && newMatiereId !== oldMatiereId) {
    // Mettre à jour la route si nécessaire
    if (route.params.matiereId != newMatiereId) {
      console.log('[Notions] Mise à jour de la route vers:', newMatiereId)
      router.replace({ 
        name: 'Notions', 
        params: { matiereId: String(newMatiereId) } 
      })
    }
    
    // Charger les nouvelles données
    loadNotions(newMatiereId)
  }
}, { immediate: false })

// Surveiller les changements de niveau de l'utilisateur
watch(() => userStore.niveau_pays, async (newNiveau) => {
  if (newNiveau && currentMatiereId.value) {
    console.log('[Notions] Niveau changé, rechargement des notions:', newNiveau.nom)
    await loadNotions(currentMatiereId.value)
  }
}, { immediate: false })

function onNotionClick(notionId) {
  router.push({ name: 'Chapitres', params: { notionId } })
}
</script>

<style scoped>
.notions-page {
  background: #f8fafc;
  min-height: 100vh;
  /* reduce default offsets to align with other pages */
  padding: 0.5rem 2vw 2rem 0;
}

/* Navigation Header */
.nav-header {
  padding: 0.75rem 1rem 0.75rem 0;
  background: white;
  border-bottom: 1px solid #e2e8f0;
}

/* Page Title */
.page-title {
  background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
  padding: 2rem 2rem 1rem 2rem;
  color: white;
}

.page-title h1 {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Main Content */
.main-content {
  width: 100%;
  max-width: none;
  margin: 0;
  padding: 0;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* Loading Spinner */
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
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-state p {
  color: #64748b;
  margin: 0;
}

/* Error State */
.error-state {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.error-state p {
  color: #64748b;
  margin: 0 0 1rem 0;
}

/* Retry Button */
.retry-btn {
  background: #60a5fa;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s ease;
}

.retry-btn:hover {
  background: #3b82f6;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.empty-state p {
  color: #64748b;
  margin: 0;
}

/* Notions Container */
.notions-container {
  width: 100%;
}

/* Themes Layout */
.themes-layout {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.theme-section {
  background: transparent;
  border: none;
  border-radius: 0;
  overflow: visible;
  box-shadow: none;
}

/* Theme Headers */
.theme-header {
  background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 8px 8px 0 0;
  margin-bottom: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.theme-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: white;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.theme-label {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 400;
}

/* Notions Grid */
.notions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
  padding: 1.5rem;
}

/* Notion Cards */
.notion-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.notion-card:hover {
  border-color: #10b981;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15);
  transform: translateY(-2px);
}

.notion-card:hover::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #10b981, #059669);
}

.card-content {
  padding: 1.5rem;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
}

.card-subtitle {
  font-size: 0.75rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 1rem 0;
  font-weight: 500;
}

.progress-bar {
  width: 100%;
  height: 4px;
  background: #f1f5f9;
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  width: 0%;
  height: 100%;
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
  border-radius: 2px;
  transition: width 0.3s ease;
}

.notion-card:hover .progress-fill {
  width: 30%;
}

/* Simple Layout */
.simple-layout .notions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

/* Responsive */
@media (max-width: 768px) {
  .nav-header {
    padding: 1rem;
  }
  
  .page-title {
    padding: 1.5rem 1rem 1rem 1rem;
  }
  
  .page-title h1 {
    font-size: 1.5rem;
  }
  
  .main-content {
    padding: 1rem;
  }
  
  .theme-header {
    padding: 1rem;
  }
  
  .theme-title {
    font-size: 1.125rem;
  }
  
  .notions-grid {
    grid-template-columns: 1fr;
    padding: 1rem;
  }
  
  .card-content {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .page-title h1 {
    font-size: 1.25rem;
  }
  
  .theme-title {
    font-size: 1rem;
  }
  
  .card-title {
    font-size: 0.9rem;
  }
}
</style> 