<template>
  <DashboardLayout>
    <div class="synthesis-page">
      <!-- Header compact -->
      <header class="page-header">
        <div class="header-content">
          <h1 class="page-title">
            <span class="title-icon">📋</span>
            Fiches de Synthèse
          </h1>
          <p class="page-subtitle">{{ activeMatiereNom }}</p>
      </div>

        <!-- Barre de recherche moderne -->
        <div class="search-section">
          <div class="search-input-wrapper">
            <input 
              v-model="searchTerm" 
              type="text" 
              placeholder="Rechercher une fiche..."
              class="search-input"
            >
            <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="m21 21-4.35-4.35"></path>
            </svg>
          </div>
        </div>
      </header>

      <!-- États de chargement -->
      <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
        <span>Chargement des fiches...</span>
        </div>

      <div v-else-if="error" class="error-container">
        <div class="error-icon">⚠️</div>
          <h3>Erreur de chargement</h3>
          <p>{{ error }}</p>
        <button @click="loadData" class="retry-button">Réessayer</button>
        </div>

      <!-- Grille de fiches modernes -->
      <div v-else class="fiches-grid">
        <div v-if="filteredFiches.length === 0" class="empty-state">
          <div class="empty-icon">📄</div>
          <h3>Aucune fiche trouvée</h3>
          <p>{{ searchTerm ? 'Aucune fiche ne correspond à votre recherche.' : 'Aucune fiche de synthèse disponible.' }}</p>
        </div>

        <div 
          v-for="fiche in filteredFiches" 
                :key="fiche.id"
                class="fiche-card"
                @click="openFiche(fiche)"
              >
          <!-- En-tête de la carte -->
          <div class="card-header">
            <div class="card-meta">
              <span class="matiere-badge">{{ fiche.matiere_nom }}</span>
              <span class="reading-time">{{ fiche.reading_time_minutes || 5 }}min</span>
                  </div>
                </div>
                
          <!-- Contenu principal -->
          <div class="card-body">
                  <h3 class="fiche-title">{{ fiche.titre }}</h3>
                </div>
                
          <!-- Pied de carte -->
          <div class="card-footer">
            <div class="stats-box">
              <div class="stats-content">
                    <span class="stat">{{ countWords(fiche.summary) }} mots</span>
                <span class="stat">{{ countFormulas(fiche.summary) }} formules</span>
                  </div>
            </div>
            <button class="view-button">
              <span>Ouvrir</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M7 17l9.2-9.2M17 17V7H7"></path>
              </svg>
                  </button>
                </div>
              </div>
            </div>

      <!-- Modal moderne pour afficher la fiche -->
      <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal-container" @click.stop>
          <!-- Header du modal -->
        <div class="modal-header">
            <div class="modal-title-section">
              <h2 class="modal-title">{{ selectedFiche?.titre }}</h2>
              <div class="modal-meta">
                <span class="meta-badge matiere">{{ selectedFiche?.matiere_nom }}</span>
                <span class="meta-badge time">{{ selectedFiche?.reading_time_minutes || 5 }}min</span>
        </div>
            </div>
            <button @click="closeModal" class="close-button">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
        </div>
        
          <!-- Contenu du modal ultra-compact -->
          <div class="modal-body">
            <div class="synthesis-content" v-html="prepareContent(selectedFiche?.summary)"></div>
        </div>
        
          <!-- Footer du modal -->
          <div class="modal-footer">
          <div class="content-stats">
              <span class="stat-chip">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14,2 14,8 20,8"></polyline>
                </svg>
              {{ countWords(selectedFiche?.summary) }} mots
            </span>
              <span class="stat-chip">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="3"></circle>
                  <path d="M12 1v6m0 6v6m11-7h-6m-6 0H1"></path>
                </svg>
              {{ countFormulas(selectedFiche?.summary) }} formules
            </span>
          </div>
        </div>
      </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import { getSynthesisSheets, getSynthesisMatieres } from '@/api/synthesis'
import { useSubjectsStore } from '@/stores/subjects/index'
import { useSmartNavigation } from '@/composables/useSmartNavigation'
import { useUserStore } from '@/stores/user'

// Composables
const route = useRoute()
const router = useRouter()
const subjectsStore = useSubjectsStore()
const userStore = useUserStore()
const { matiereIdFromRoute } = useSmartNavigation()

// État réactif
const fiches = ref([])
const matieres = ref([])
const loading = ref(true)
const error = ref('')
const searchTerm = ref('')
const showModal = ref(false)
const selectedFiche = ref(null)

// Computed
const activeMatiereId = computed(() => {
  return matiereIdFromRoute.value || subjectsStore.activeMatiereId
})

const activeMatiereNom = computed(() => {
  if (!activeMatiereId.value) return 'Toutes les matières'
  const matiere = matieres.value.find(m => m.id == activeMatiereId.value)
  return matiere ? matiere.nom : 'Matière'
})

const userContext = computed(() => {
  if (!userStore.isAuthenticated) return 'Non connecté'
  const pays = userStore.pays?.nom || 'Pays non défini'
  const niveau = userStore.niveau_pays?.nom || 'Niveau non défini'
  return `${pays} - ${niveau}`
})

const filteredFiches = computed(() => {
  let result = fiches.value
  
  if (searchTerm.value.trim()) {
    const term = searchTerm.value.toLowerCase()
    result = result.filter(f => 
      f.titre.toLowerCase().includes(term) ||
      f.summary.toLowerCase().includes(term)
    )
  }
  
  return result.sort((a, b) => a.titre.localeCompare(b.titre))
})

// Méthodes
async function loadData() {
  loading.value = true
  error.value = ''
  
  try {
    const params = {}
    if (activeMatiereId.value) {
      params.matiere = activeMatiereId.value
    }

    const [fichesResponse, matieresResponse] = await Promise.all([
      getSynthesisSheets(params),
      getSynthesisMatieres()
    ])
    
    fiches.value = fichesResponse.data
    const matData = matieresResponse.data?.matieres_disponibles || matieresResponse.data || []
    matieres.value = Array.isArray(matData) ? matData : []
    
  } catch (e) {
    console.error('Erreur lors du chargement:', e)
    error.value = "Impossible de charger les fiches de synthèse."
  } finally {
    loading.value = false
  }
}

function getPreviewContent(content) {
  if (!content) return ''
  
  // Nettoyer le contenu : enlever HTML, LaTeX, Markdown et caractères spéciaux
  let cleanText = content
    .replace(/<[^>]*>/g, '') // Enlever les balises HTML
    .replace(/\$[^$]*\$/g, '') // Enlever les formules LaTeX inline
    .replace(/\$\$[^$]*\$\$/g, '') // Enlever les formules LaTeX en bloc
    .replace(/^#+\s*/gm, '') // Enlever les titres Markdown
    .replace(/\*\*([^*]+)\*\*/g, '$1') // Enlever le gras Markdown
    .replace(/\*([^*]+)\*/g, '$1') // Enlever l'italique Markdown
    .replace(/`([^`]+)`/g, '$1') // Enlever le code inline
    .replace(/\n+/g, ' ') // Remplacer les sauts de ligne par des espaces
    .replace(/\s+/g, ' ') // Normaliser les espaces multiples
    .trim()
  
  // Limiter à 120 caractères et ajouter des points de suspension si nécessaire
  return cleanText.length > 120 ? cleanText.substring(0, 120) + '...' : cleanText
}

function prepareContent(content) {
  if (!content) return ''
  
  return content
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    // Convertir les paragraphes colorés en titres
    .replace(/<p[^>]*style="[^"]*color:blue[^"]*"[^>]*>([^<]+)<\/p>/g, '<h2 class="section-title blue">$1</h2>')
    .replace(/<p[^>]*style="[^"]*color:darkorange[^"]*"[^>]*>([^<]+)<\/p>/g, '<h3 class="subsection-title orange">$1</h3>')
    .replace(/<p[^>]*style="[^"]*color:red[^"]*"[^>]*>([^<]+)<\/p>/g, '<div class="alert-box warning">$1</div>')
    .replace(/<p[^>]*style="[^"]*color:green[^"]*"[^>]*>([^<]+)<\/p>/g, '<div class="alert-box success">$1</div>')
    .replace(/<p[^>]*style="[^"]*color:purple[^"]*"[^>]*>([^<]+)<\/p>/g, '<h4 class="example-title">$1</h4>')
    // Traitement des titres markdown
    .replace(/^###\s+(.+)$/gm, '<h3 class="subsection-title">$1</h3>')
    .replace(/^##\s+(.+)$/gm, '<h2 class="section-title">$1</h2>')
    .replace(/^#\s+(.+)$/gm, '<h1 class="main-title">$1</h1>')
    // Formatage
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>')
    // Sauts de ligne
    .replace(/\n\n/g, '<br/>')
    .replace(/\n/g, '<br/>')
    .trim()
}

function countWords(text) {
  if (!text) return 0
  return text.replace(/<[^>]*>/g, '').trim().split(/\s+/).length
}

function countFormulas(text) {
  if (!text) return 0
  const patterns = [/\$[^$]+\$/g, /\$\$[^$]+\$\$/g]
  let count = 0
  patterns.forEach(pattern => {
    const matches = text.match(pattern)
    if (matches) count += matches.length
  })
  return count
}

function openFiche(fiche) {
  selectedFiche.value = fiche
  showModal.value = true
  nextTick(() => {
        if (window.MathJax && window.MathJax.typesetPromise) {
          window.MathJax.typesetPromise()
    }
  })
}

function closeModal() {
  showModal.value = false
  selectedFiche.value = null
}

// Lifecycle
onMounted(loadData)
</script>

<style scoped>
.synthesis-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  padding: 1rem;
}

/* Header moderne */
.page-header {
  background: white;
  border-radius: 0;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(148, 163, 184, 0.1);
}

.header-content {
  margin-bottom: 1rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.title-icon {
  font-size: 1.5rem;
}

.page-subtitle {
  color: #64748b;
  font-size: 1rem;
  margin: 0;
  font-weight: 500;
}

.search-section {
  display: flex;
  justify-content: center;
}

.search-input-wrapper {
  position: relative;
  max-width: 400px;
  width: 100%;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 2px solid #e2e8f0;
  border-radius: 0;
  font-size: 1rem;
  background: #f8fafc;
  transition: all 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
}

/* États */
.loading-container, .error-container {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.retry-button {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.retry-button:hover {
  background: #2563eb;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 0;
  grid-column: 1 / -1;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

/* Grille de fiches moderne */
.fiches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.fiche-card {
  background: white;
  border-radius: 0;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(148, 163, 184, 0.1);
  position: relative;
  overflow: hidden;
}

.fiche-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
}

.fiche-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.card-header {
  margin-bottom: 1rem;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.matiere-badge {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 0;
  font-size: 0.75rem;
  font-weight: 600;
}

.reading-time {
  color: #64748b;
  font-size: 0.75rem;
  font-weight: 500;
}

.card-body {
  margin-bottom: 1rem;
}

.fiche-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  line-height: 1.3;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #f1f5f9;
}

.stats-box {
  position: relative;
}

.stats-content {
  display: flex;
  gap: 1rem;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.stats-box:hover .stats-content {
  opacity: 1;
}

.stat {
  color: #94a3b8;
  font-size: 0.75rem;
  font-weight: 500;
  background: rgba(148, 163, 184, 0.1);
  padding: 0.25rem 0.5rem;
  border-radius: 0;
}

.view-button {
  background: #f1f5f9;
  color: #475569;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.view-button:hover {
  background: #3b82f6;
  color: white;
}

/* Modal moderne */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
  backdrop-filter: blur(4px);
}

.modal-container {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 2rem 2rem 1rem 2rem;
  border-bottom: 1px solid #f1f5f9;
}

.modal-title-section {
  flex: 1;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.75rem 0;
  line-height: 1.3;
}

.modal-meta {
  display: flex;
  gap: 0.75rem;
}

.meta-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.meta-badge.matiere {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: white;
}

.meta-badge.time {
  background: #f1f5f9;
  color: #64748b;
}

.close-button {
  background: #f8fafc;
  border: none;
  border-radius: 8px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #64748b;
  transition: all 0.2s;
}

.close-button:hover {
  background: #f1f5f9;
  color: #374151;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 1rem 2rem 2rem 2rem;
}

/* Contenu de synthèse ultra-compact */
.synthesis-content {
  font-family: 'Inter', -apple-system, sans-serif;
  line-height: 1.4;
  color: #374151;
  font-size: 0.95rem;
}

.synthesis-content :deep(.main-title) {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 3px solid #3b82f6;
}

.synthesis-content :deep(.section-title) {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1e293b;
  margin: 1rem 0 0.3rem 0;
  padding: 0.5rem 0.75rem;
  background: linear-gradient(135deg, #eff6ff, #dbeafe);
  border-left: 4px solid #3b82f6;
  border-radius: 0 8px 8px 0;
}

.synthesis-content :deep(.section-title.blue) {
  background: linear-gradient(135deg, #eff6ff, #dbeafe);
  border-left-color: #3b82f6;
  color: #1e40af;
}

.synthesis-content :deep(.subsection-title) {
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  margin: 0.6rem 0 0.2rem 0;
  padding: 0.25rem 0.5rem;
  background: #f8fafc;
  border-left: 3px solid #10b981;
  border-radius: 0 6px 6px 0;
}

.synthesis-content :deep(.subsection-title.orange) {
  border-left-color: #f59e0b;
  background: #fffbeb;
  color: #d97706;
}

.synthesis-content :deep(.example-title) {
  font-size: 0.9rem;
  font-weight: 600;
  color: #7c3aed;
  margin: 0.4rem 0 0.2rem 0;
  padding: 0.25rem 0.5rem;
  background: #faf5ff;
  border-left: 3px solid #7c3aed;
  border-radius: 0 6px 6px 0;
}

.synthesis-content :deep(.alert-box) {
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  margin: 0.4rem 0;
  font-weight: 500;
  font-size: 0.9rem;
}

.synthesis-content :deep(.alert-box.warning) {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
}

.synthesis-content :deep(.alert-box.success) {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #059669;
}

.synthesis-content :deep(p) {
  margin: 0.2rem 0;
  line-height: 1.5;
}

.synthesis-content :deep(ul),
.synthesis-content :deep(ol) {
  margin: 0.3rem 0 0.3rem 1.2rem;
  padding: 0;
}

.synthesis-content :deep(li) {
  margin: 0.1rem 0;
  line-height: 1.4;
}

.synthesis-content :deep(strong) {
  font-weight: 700;
  color: #1e293b;
}

.synthesis-content :deep(em) {
  color: #64748b;
  font-style: italic;
}

/* MathJax ultra-compact */
.synthesis-content :deep(.MathJax) {
  font-size: 0.95rem !important;
  margin: 0.2rem 0 !important;
}

.synthesis-content :deep(.MathJax_Display),
.synthesis-content :deep(.MathJax_SVG_Display) {
  margin: 0.3rem 0 !important;
  text-align: center !important;
}

.modal-footer {
  padding: 1rem 2rem;
  border-top: 1px solid #f1f5f9;
  background: #fafbfc;
}

.content-stats {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.stat-chip {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: white;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #64748b;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .synthesis-page {
    padding: 0.5rem;
  }
  
  .page-header {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
  
  .fiches-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .modal-overlay {
    padding: 1rem;
  }
  
  .modal-header, .modal-body, .modal-footer {
    padding: 1rem;
  }
  
  .content-stats {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style> 