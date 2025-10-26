<template>
  <DashboardLayout>
    <section class="exercices-section">
      <!-- Bouton de retour -->
      <BackButton 
        text="Retour aux chapitres" 
        :customAction="goBackToNotions"
        position="top-left"
      />
      
      <!-- Navigation ultra-propre -->
      <div class="clean-navigation">
        <div class="nav-grid">
          <button 
            v-for="t in tabs" 
            :key="t.key"
            :class="['nav-item', { active: t.key === activeTab }]"
            @click="activeTab = t.key; currentPage = 1"
          >
            <span class="nav-icon">{{ t.icon }}</span>
            <span class="nav-label">{{ t.shortLabel }}</span>
            <span class="nav-count">{{ t.count }}</span>
          </button>
        </div>
      </div>

      
      
      <div v-if="loading" class="loading-skeleton-container">
        <SkeletonList :count="4" />
      </div>
      <div v-else-if="error" class="exercices-error">{{ error }}</div>
        <div v-else>
          <div class="exercices-controls">
            <div class="controls-row">
              <!-- Barre de recherche -->
              <div class="search-section">
                <div class="search-container">
                  <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"/>
                    <path d="m21 21-4.35-4.35"/>
                  </svg>
                  <input
                    v-model="searchQuery"
                    type="text"
                    placeholder="Rechercher un exercice..."
                    class="search-input"
                    @input="handleSearch"
                  />
                  <button
                    v-if="searchQuery"
                    @click="clearSearch"
                    class="clear-search-btn"
                    aria-label="Effacer la recherche"
                  >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <line x1="18" y1="6" x2="6" y2="18"/>
                      <line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                  </button>
                </div>
              </div>

              <div class="filter-row">
            <div class="filter-item">
              <span class="filter-label">Exercices par page</span>
              <div class="filter-buttons">
                <button
                  v-for="n in perPageOptions"
                  :key="n"
                  :class="['filter-btn', { active: n === perPage }]"
                  @click="perPage = n; currentPage = 1"
                >
                  {{ n }}
                </button>
              </div>
          </div>

            <div class="filter-divider"></div>

            <div class="filter-item">
              <span class="filter-label">Difficulté</span>
              <div class="filter-buttons">
                <button
                  v-for="d in difficultyOptions"
                  :key="d"
                  :class="['filter-btn', { active: d === selectedDifficulty }]"
                  @click="selectedDifficulty = d; currentPage = 1"
                >
                  <span v-if="d === 'all'" class="difficulty-text">Toutes</span>
                  <span v-else class="difficulty-stars">
                    {{ d === 'easy' ? '★' : d === 'medium' ? '★★' : '★★★' }}
                  </span>
                </button>
              </div>
            </div>
            </div>

          </div>
        </div>
        <div class="exercices-list">
          <ExerciceQCM
            v-for="exercice in paginated"
            :key="exercice.id"
            :eid="exercice.id"
            :titre="exercice.titre || exercice.nom"
            :instruction="exercice.instruction || exercice.contenu || exercice.question"
            :solution="exercice.solution || exercice.reponse_correcte || ''"
            :etapes="exercice.etapes || ''"
            :difficulty="exercice.difficulty || exercice.difficulte || 'medium'"
            :current="statusMap[exercice.id]?.status"
            @status-changed="handleStatus"
          />
          <Pagination :total="filteredExercices.length" :perPage="perPage" :page="currentPage" @update:page="handlePageChange" />
        </div>
      </div>
    </section>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, onActivated, onBeforeUnmount, nextTick, watch, computed } from 'vue'
import { defineOptions } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import SkeletonList from '@/components/common/SkeletonList.vue'
import { getExercices, getStatuses, createStatus, updateStatus, deleteStatus } from '@/api'
import { useUserStore } from '@/stores/user'
import { useSubjectsStore } from '@/stores/subjects/index'
import ExerciceQCM from '@/components/UI/ExerciceQCM.vue'
import Pagination from '@/components/common/Pagination.vue'
import Tabs from '@/components/common/Tabs.vue'
import BackButton from '@/components/common/BackButton.vue'

defineOptions({ name: 'ExercisesByNotion' })

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const subjectsStore = useSubjectsStore()
const notionId = ref(route.params.notionId)

const exercices = ref([])
const perPageOptions = [1,3,5]
const perPage = ref(5)
const currentPage = ref(1)

// Filtre difficulté
const difficultyOptions = ['all','easy','medium','hard']
const selectedDifficulty = ref('all')

// Recherche
const searchQuery = ref('')


// Status filtering tabs avec design amélioré
const tabs = computed(() => [
  { 
    key: 'all', 
    label: 'Exercices restants',
    shortLabel: 'À faire',
    icon: '📝',
    count: exercices.value.filter(e => !statusMap.value[e.id]).length
  },
  { 
    key: 'done', 
    label: 'Exercices réalisés',
    shortLabel: 'Fait',
    icon: '📋',
    count: exercices.value.filter(e => statusMap.value[e.id]).length
  },
  { 
    key: 'acquired', 
    label: 'Acquis',
    shortLabel: 'Acquis',
    icon: '✅',
    count: exercices.value.filter(e => statusMap.value[e.id]?.status === 'acquired').length
  },
  { 
    key: 'not_acquired', 
    label: 'À revoir',
    shortLabel: 'À revoir',
    icon: '❌',
    count: exercices.value.filter(e => statusMap.value[e.id]?.status === 'not_acquired').length
  }
])
const activeTab = ref('all')

// --- Persistence (sessionStorage) ---
const storageKey = `optitab_page_exercices_${notionId}`

function saveViewState() {
  try {
    const state = {
      perPage: perPage.value,
      currentPage: currentPage.value,
      selectedDifficulty: selectedDifficulty.value,
      activeTab: activeTab.value,
      searchQuery: searchQuery.value,
      scrollY: typeof window !== 'undefined' ? (window.scrollY || window.pageYOffset || 0) : 0,
      t: Date.now()
    }
    sessionStorage.setItem(storageKey, JSON.stringify(state))
  } catch (_) {}
}

function restoreViewState() {
  try {
    const raw = sessionStorage.getItem(storageKey)
    if (!raw) return null
    const s = JSON.parse(raw)
    if (s && typeof s === 'object') {
      if (typeof s.perPage === 'number') perPage.value = s.perPage
      if (typeof s.currentPage === 'number') currentPage.value = Math.max(1, s.currentPage)
      if (typeof s.selectedDifficulty === 'string') selectedDifficulty.value = s.selectedDifficulty
      if (typeof s.activeTab === 'string') activeTab.value = s.activeTab
      if (typeof s.searchQuery === 'string') searchQuery.value = s.searchQuery
      return s
    }
  } catch (_) {}
  return null
}

// Fonction pour télécharger tous les exercices en PDF
const downloadAllPDF = async () => {
  try {
    console.log('Download all PDF clicked')
    console.log('Exercices data:', filteredExercices.value)
    
    // Import dynamique pour éviter les erreurs
    const { generateExercicesListPDF } = await import('@/utils/pdfGenerator')
    await generateExercicesListPDF(filteredExercices.value, `Exercices_${notionNom.value}`)
    alert('PDF généré avec succès !')
  } catch (error) {
    console.error('Erreur PDF:', error)
    alert('Erreur lors de la génération du PDF: ' + error.message)
  }
}

const statusMap = ref({}) // exerciceId -> { status, id }

const notionNom = ref('')
const loading = ref(true)
const error = ref('')
const chapitres = ref([])

onMounted(async () => {
  await loadData()
})

// Hook onActivated - appelé quand le composant est réactivé depuis le cache KeepAlive
onActivated(() => {
  // Forcer le rendu MathJax à chaque réactivation pour éviter les problèmes de cache
  // Les composants ExerciceQCM enfants gèrent leur propre rendu, mais on force quand même ici
  nextTick(() => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      try {
        // Vider le cache de MathJax pour forcer un nouveau rendu
        if (window.MathJax.typesetClear) {
          window.MathJax.typesetClear()
        }
        window.MathJax.typesetPromise()
      } catch (error) {
        console.warn('[MathJax] Erreur:', error)
      }
    }
    // S'assurer que le rendu est bien appliqué avec un second appel après un délai
    setTimeout(() => {
      if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise()
      }
    }, 100)
  })
})

async function loadData() {
  loading.value = true
  try {
    const niveauId = userStore.niveau_pays?.id

    // Reset data when notion changes
    exercices.value = []
    statusMap.value = {}

    const [exercicesData, statusesResp] = await Promise.all([
      getExercices({ notion: notionId.value, niveau: niveauId }),
      getStatuses()
    ])

    notionNom.value = 'Notion'

    exercices.value = Array.isArray(exercicesData) ? exercicesData : []
    console.log(`[ExercisesByNotion] Exercices chargés pour niveau ${niveauId}:`, exercices.value.length)

    const stats = statusesResp?.data || []
    const list = Array.isArray(stats) ? stats : (stats?.results || [])
    statusMap.value = Object.fromEntries(
      list.map(s => [
        s.exercice,
        { status: s.est_correct ? 'acquired' : 'not_acquired', id: s.id }
      ])
    )

    // Restaurer l'état de vue
    restoreViewState()

    const total = Math.max(1, Math.ceil((filteredExercices?.value?.length || 0) / Math.max(1, perPage.value)))
    if (currentPage.value > total) currentPage.value = total
    error.value = ''
  } catch (e) {
    console.error('[ExercisesByNotion] Erreur chargement:', e)
    error.value = "Impossible de charger les exercices."
  } finally {
    loading.value = false
    await nextTick()
    
    // Forcer le rendu MathJax après le chargement des exercices
    setTimeout(() => {
      if (window.MathJax && window.MathJax.typesetPromise) {
        try {
          if (window.MathJax.typesetClear) {
            window.MathJax.typesetClear()
          }
          window.MathJax.typesetPromise()
        } catch (error) {
          console.warn('[MathJax] Erreur:', error)
        }
      }
    }, 100)
    
    setTimeout(() => {
      try {
        const raw = sessionStorage.getItem(storageKey)
        if (raw) {
          const s = JSON.parse(raw)
          if (s && typeof s.scrollY === 'number') {
            window.scrollTo({ top: s.scrollY, behavior: 'auto' })
          }
        }
      } catch (_) {}
    }, 50)
  }
}

// Recharger si l'ID de notion change sous KeepAlive
watch(() => route.params.notionId, async (newId, oldId) => {
  if (newId && newId !== oldId) {
    notionId.value = newId
    await loadData()
  }
})

const totalPages = computed(() => Math.ceil(exercices.value.length / perPage.value))

const filteredExercices = computed(() => {
  let list = exercices.value
  
  // Filtre par recherche
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    list = list.filter(e => {
      const title = (e.titre || e.nom || '').toLowerCase()
      const content = (e.instruction || e.contenu || e.question || '').toLowerCase()
      return title.includes(query) || content.includes(query)
    })
  }
  
  // Filtre par difficulté
  if (selectedDifficulty.value !== 'all') {
    list = list.filter(e => e.difficulty === selectedDifficulty.value)
  }
  
  // Filtre par statut
  if (activeTab.value === 'done') {
    // Tous les exercices déjà traités (peu importe le résultat)
    list = list.filter(e => statusMap.value[e.id])
  } else if (activeTab.value === 'all') {
    // Exercices restants : ceux sans statut enregistré
    list = list.filter(e => !statusMap.value[e.id])
  } else {
    // Filtre par statut précis (acquired ou not_acquired)
    list = list.filter(e => statusMap.value[e.id]?.status === activeTab.value)
  }
  
  // Trier les exercices par ID pour avoir l'ordre 1, 2, 3, etc.
  return list.sort((a, b) => {
    const idA = parseInt(a.id) || 0
    const idB = parseInt(b.id) || 0
    return idA - idB
  })
})

const paginated = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  return filteredExercices.value.slice(start, start + perPage.value)
})

function handlePageChange(page) {
  currentPage.value = page
  // scroll to top of exercises
  window.scrollTo({ top: 0, behavior: 'smooth' })
  // Sauvegarder l'état
  saveViewState()
  // Forcer le rendu MathJax après le changement de page
  nextTick(() => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      try {
        if (window.MathJax.typesetClear) {
          window.MathJax.typesetClear()
        }
        window.MathJax.typesetPromise()
      } catch (error) {
        console.warn('[MathJax] Erreur:', error)
      }
    }
  })
}

async function handleStatus({ exerciceId, status }) {
  try {
    if (status) {
      // Vérifier si un statut existe déjà pour cet exercice
      const existingStatus = statusMap.value[exerciceId]
      
      if (existingStatus) {
        // Si un statut existe déjà, le mettre à jour
        await updateStatus(existingStatus.id, {
          exercice: exerciceId,
          reponse_donnee: status,
          est_correct: status === 'acquired'
        })
        // Mettre à jour le statut local
        statusMap.value[exerciceId] = { status, id: existingStatus.id }
        
        // Objectifs journaliers supprimés
      } else {
        // Si aucun statut n'existe, en créer un nouveau
        const response = await createStatus({
          exercice: exerciceId,
          reponse_donnee: status,
          est_correct: status === 'acquired',
          points_obtenus: status === 'acquired' ? 1 : 0,
          temps_seconde: 0
        })
        // Mettre à jour le statut local avec l'ID retourné
        const newId = response?.data?.id || response?.id
        statusMap.value[exerciceId] = { status, id: newId }
      }
      
      // Objectifs journaliers supprimés
    } else {
      // Supprimer le statut de la base de données
      const existingStatus = statusMap.value[exerciceId]
      
      if (existingStatus) {
        await deleteStatus(existingStatus.id)
      }
      
      // Supprimer du statut local
      delete statusMap.value[exerciceId]
    }
  } catch (error) {
    console.error('Erreur lors de la sauvegarde du statut:', error)
    // En cas d'erreur, on peut quand même mettre à jour le statut local
    if (status) {
      statusMap.value[exerciceId] = { status, id: null }
    } else {
      delete statusMap.value[exerciceId]
    }
  }
}

function goBackToNotions() {
  // Rediriger vers exercicies/id (liste des notions d'exercices)
  const matiereId = route.params.matiereId || subjectsStore.activeMatiereId
  if (matiereId) {
    router.push({ 
      name: 'Themes', 
      params: { 
        matiereId: matiereId
      } 
    })
  } else {
    router.back()
  }
}

// Fonctions de recherche
function handleSearch() {
  currentPage.value = 1
  saveViewState()
}

function clearSearch() {
  searchQuery.value = ''
  currentPage.value = 1
  saveViewState()
}


// Sauvegarder à chaque changement significatif
watch([perPage, currentPage, selectedDifficulty, activeTab, searchQuery], () => {
  saveViewState()
})

// Forcer le rendu MathJax quand les exercices affichés changent
watch(paginated, () => {
  nextTick(() => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      try {
        if (window.MathJax.typesetClear) {
          window.MathJax.typesetClear()
        }
        window.MathJax.typesetPromise()
      } catch (error) {
        console.warn('[MathJax] Erreur:', error)
      }
    }
  })
}, { deep: true })

onBeforeUnmount(() => {
  saveViewState()
})

async function generatePDF(includeCorrection = false) {
  try {
    // Dynamically import PDF libraries
    const { default: jsPDF } = await import('jspdf')
    
    // Create a new PDF document with better configuration
    const pdf = new jsPDF({
      orientation: 'p',
      unit: 'mm',
      format: 'a4',
      putOnlyUsedFonts: true,
      floatPrecision: 16
    })
    
    const pageWidth = pdf.internal.pageSize.getWidth()
    const pageHeight = pdf.internal.pageSize.getHeight()
    const margin = 20
    const contentWidth = pageWidth - (2 * margin)
    
    // Enhanced header
    pdf.setFillColor(240, 248, 255)
    pdf.rect(0, 0, pageWidth, 40, 'F')
    
    // Title
    pdf.setFontSize(18)
    pdf.setFont('helvetica', 'bold')
    pdf.setTextColor(30, 64, 175)
    const title = includeCorrection ? 
      `Exercices de ${notionNom.value}` : 
      `Feuille d'exercices - ${notionNom.value}`
    
    const titleWidth = pdf.getTextWidth(title)
    pdf.text(title, (pageWidth - titleWidth) / 2, 20)
    
    // Subtitle
    pdf.setFontSize(10)
    pdf.setFont('helvetica', 'normal')
    pdf.setTextColor(100, 116, 139)
    const subtitle = includeCorrection ? 'Exercices avec corrections détaillées' : 'Énoncés des exercices'
    const subtitleWidth = pdf.getTextWidth(subtitle)
    pdf.text(subtitle, (pageWidth - subtitleWidth) / 2, 28)
    
    // Metadata
    pdf.setTextColor(0, 0, 0)
    pdf.setFontSize(8)
    const date = new Date().toLocaleDateString('fr-FR', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    })
    pdf.text(`Généré le ${date}`, margin, 36)
    pdf.text(`${filteredExercices.value.length} exercice(s)`, pageWidth - margin - 30, 36)
    
    let yPosition = 50
    let exerciseNumber = 1
    
    // Process each exercise with enhanced formatting
    for (const exercice of filteredExercices.value) {
      // Check if we need a new page
      if (yPosition > pageHeight - 100) {
        pdf.addPage()
        yPosition = margin
      }
      
      // Exercise number box
      pdf.setFillColor(59, 130, 246)
      pdf.setTextColor(255, 255, 255)
      pdf.roundedRect(margin, yPosition - 5, 15, 10, 2, 2, 'F')
      pdf.setFontSize(10)
      pdf.setFont('helvetica', 'bold')
      pdf.text(`${exerciseNumber}`, margin + 4, yPosition + 2)
      
      // Exercise title
      pdf.setTextColor(0, 0, 0)
      pdf.setFontSize(12)
      pdf.setFont('helvetica', 'bold')
      if (exercice.titre) {
        pdf.text(exercice.titre, margin + 20, yPosition + 2)
      }
      
      yPosition += 15
      
      // Difficulty indicator
      const difficulty = exercice.difficulty || 'medium'
      const difficultyText = difficulty === 'easy' ? '★☆☆ Facile' : 
                            difficulty === 'medium' ? '★★☆ Moyen' : '★★★ Difficile'
      const difficultyColor = difficulty === 'easy' ? [34, 197, 94] : 
                             difficulty === 'medium' ? [245, 158, 11] : [239, 68, 68]
      
      pdf.setFontSize(8)
      pdf.setFont('helvetica', 'normal')
      pdf.setTextColor(...difficultyColor)
      pdf.text(difficultyText, margin, yPosition)
      
      yPosition += 10
      pdf.setTextColor(0, 0, 0)
      
      // Exercise content (énoncé)
      const question = exercice.question || exercice.contenu || ''
      if (question) {
        pdf.setFontSize(11)
        pdf.setFont('helvetica', 'bold')
        pdf.text('Énoncé :', margin, yPosition)
        yPosition += 8
        
        yPosition = formatScientificContent(
          cleanTextForPDF(question), 
          pdf, 
          yPosition, 
          contentWidth, 
          margin
        )
        yPosition += 10
      }
      
      // If including corrections, add steps and solution
      if (includeCorrection) {
        // Steps if available
        if (exercice.etapes && exercice.etapes.trim()) {
          // Check for page break
          if (yPosition > pageHeight - 60) {
            pdf.addPage()
            yPosition = margin
          }
          
          pdf.setFontSize(11)
          pdf.setFont('helvetica', 'bold')
          pdf.setTextColor(139, 69, 19)
          pdf.text('🔢 Méthode de résolution :', margin, yPosition)
          yPosition += 10
          
          pdf.setTextColor(0, 0, 0)
          yPosition = formatScientificContent(
            cleanTextForPDF(exercice.etapes), 
            pdf, 
            yPosition, 
            contentWidth, 
            margin
          )
          yPosition += 10
        }
        
        // Solution
        const solution = exercice.reponse_correcte || ''
        if (solution) {
          // Check for page break
          if (yPosition > pageHeight - 40) {
            pdf.addPage()
            yPosition = margin
          }
          
          pdf.setFillColor(240, 253, 244)
          pdf.roundedRect(margin - 5, yPosition - 5, contentWidth + 10, 8, 2, 2, 'F')
          
          pdf.setFontSize(11)
          pdf.setFont('helvetica', 'bold')
          pdf.setTextColor(21, 128, 61)
          pdf.text('✅ Réponse :', margin, yPosition)
          yPosition += 10
          
          pdf.setTextColor(0, 0, 0)
          yPosition = formatScientificContent(
            cleanTextForPDF(solution), 
            pdf, 
            yPosition, 
            contentWidth, 
            margin
          )
          yPosition += 5
        }
      }
      
      // Add separator line
      yPosition += 10
      pdf.setDrawColor(229, 231, 235)
      pdf.setLineWidth(0.5)
      pdf.line(margin, yPosition, pageWidth - margin, yPosition)
      yPosition += 20
      
      exerciseNumber++
    }
    
    // Footer on each page
    const pageCount = pdf.internal.getNumberOfPages()
    for (let i = 1; i <= pageCount; i++) {
      pdf.setPage(i)
      pdf.setFontSize(8)
      pdf.setTextColor(107, 114, 128)
      pdf.text(`Page ${i} sur ${pageCount}`, pageWidth - margin - 20, pageHeight - 10)
      
      if (includeCorrection) {
        pdf.text('Document avec corrections', margin, pageHeight - 10)
      } else {
        pdf.text('Document d\'énoncés', margin, pageHeight - 10)
      }
    }
    
    // Generate filename
    const sanitizedChapterName = notionNom.value
      .replace(/[^a-zA-Z0-9\sàâäéèêëïîôöùûüÿç]/g, '')
      .replace(/\s+/g, '_')
      .toLowerCase()
    const suffix = includeCorrection ? '_avec_corrections' : '_enonces'
    const dateStr = new Date().toISOString().split('T')[0]
    const filename = `exercices_${sanitizedChapterName}${suffix}_${dateStr}.pdf`
    
    // Save the PDF
    pdf.save(filename)
    
    // Success notification
    const message = includeCorrection ? 
      'PDF avec corrections généré avec succès !' : 
      'PDF des énoncés généré avec succès !'
    
    // You can replace this with a proper toast notification
    setTimeout(() => {
      alert(message)
    }, 500)
    
  } catch (error) {
    console.error('Erreur lors de la génération du PDF:', error)
    alert('Erreur lors de la génération du PDF. Veuillez vérifier que les données sont chargées et réessayer.')
  }
}

function cleanTextForPDF(text) {
  if (!text) return ''
  
  return text
    // Remove HTML tags but preserve structure
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/p>/gi, '\n\n')
    .replace(/<p[^>]*>/gi, '')
    .replace(/<strong[^>]*>(.*?)<\/strong>/gi, '**$1**')
    .replace(/<em[^>]*>(.*?)<\/em>/gi, '*$1*')
    .replace(/<[^>]*>/g, '')
    // Replace common HTML entities
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    // Handle LaTeX math notation better
    .replace(/\$\$([^$]+)\$\$/g, '\n[$1]\n')  // Display math
    .replace(/\$([^$]+)\$/g, '($1)')          // Inline math
    .replace(/\\ge/g, '≥')
    .replace(/\\le/g, '≤')
    .replace(/\\cdot/g, '·')
    .replace(/\\times/g, '×')
    .replace(/\\div/g, '÷')
    .replace(/\\pm/g, '±')
    .replace(/\\infty/g, '∞')
    .replace(/\\alpha/g, 'α')
    .replace(/\\beta/g, 'β')
    .replace(/\\gamma/g, 'γ')
    .replace(/\\delta/g, 'δ')
    .replace(/\\pi/g, 'π')
    .replace(/\\theta/g, 'θ')
    .replace(/\\lambda/g, 'λ')
    .replace(/\\mu/g, 'μ')
    .replace(/\\sigma/g, 'σ')
    .replace(/\\sum/g, 'Σ')
    .replace(/\\prod/g, 'Π')
    .replace(/\\int/g, '∫')
    .replace(/\\partial/g, '∂')
    .replace(/\\nabla/g, '∇')
    .replace(/\\sqrt/g, '√')
    // Replace common math patterns
    .replace(/\^(\d+)/g, '⁽$1⁾')
    .replace(/\_(\d+)/g, '₍$1₎')
    // Clean up formatting
    .replace(/\*\*([^*]+)\*\*/g, (match, p1) => p1.toUpperCase())  // Bold to uppercase
    .replace(/\*([^*]+)\*/g, '$1')  // Remove italic markers
    // Clean up multiple spaces and newlines
    .replace(/\s+/g, ' ')
    .replace(/\n\s*\n\s*\n/g, '\n\n')
    .replace(/^\s+|\s+$/g, '')
    .trim()
}

function formatScientificContent(text, pdf, startY, contentWidth, margin, isTitle = false) {
  if (!text) return startY
  
  const fontSize = isTitle ? 12 : 10
  const lineHeight = fontSize * 0.4
  
  pdf.setFontSize(fontSize)
  pdf.setFont('helvetica', isTitle ? 'bold' : 'normal')
  
  // Split content into paragraphs
  const paragraphs = text.split('\n\n').filter(p => p.trim())
  let currentY = startY
  
  for (const paragraph of paragraphs) {
    if (paragraph.trim()) {
      // Handle special formatting
      let formattedParagraph = paragraph
      
      // Detect if it's a step or numbered item
      const isStep = /^(🔵|Étape \d+|Question \d+|Réponse)/i.test(paragraph)
      
      if (isStep) {
        pdf.setFont('helvetica', 'bold')
        pdf.setFontSize(fontSize)
      } else {
        pdf.setFont('helvetica', 'normal')
        pdf.setFontSize(fontSize - 1)
      }
      
      const lines = pdf.splitTextToSize(formattedParagraph, contentWidth)
      
      // Check for page break
      if (currentY + (lines.length * lineHeight) > pdf.internal.pageSize.getHeight() - 20) {
        pdf.addPage()
        currentY = margin
      }
      
      pdf.text(lines, margin, currentY)
      currentY += lines.length * lineHeight + (isStep ? 8 : 5)
    }
  }
  
  return currentY
}
</script>

<style scoped>
.exercices-section {
  background: #fff;
  padding: 0 5vw 40px 5vw;
  text-align: center;
}

/* Responsive design pour mobile */
@media (max-width: 768px) {
  .exercices-section {
    padding: 0 3vw 30px 3vw;
  }

  .exercices-title {
    font-size: 1.6rem;
    margin-bottom: 30px;
  }

  .exercices-list {
    gap: 24px;
    max-width: 100%;
    margin: 0;
  }
}

@media (max-width: 680px) {
  .exercices-section {
    padding: 0 2vw 20px 2vw;
  }

  .exercices-title {
    font-size: 1.4rem;
    margin-bottom: 25px;
  }

  .exercices-list {
    gap: 20px;
  }
}

.exercices-title {
  font-size: 2rem;
  color: #193e8e;
  margin-bottom: 40px;
  font-weight: 800;
}
.exercices-list {
  display: flex;
  flex-direction: column;
  gap: 32px;
  max-width: 100%;
  margin: 0 auto;
  align-items: stretch;
  transition: max-width 0.3s ease;
}

.exercices-list.full-width {
  max-width: 95vw;
}
.exercices-loader, .exercices-error {
  font-size: 1.2rem;
  color: #475569;
  margin: 40px 0;
}

/* Responsive pour les messages de chargement et d'erreur */
@media (max-width: 768px) {
  .exercices-loader, .exercices-error {
    font-size: 1rem;
    margin: 30px 0;
  }
}

@media (max-width: 680px) {
  .exercices-loader, .exercices-error {
    font-size: 0.9rem;
    margin: 25px 0;
  }
}

.exercices-controls {
  margin-bottom: 1.5rem;
  padding: 0.75rem 1rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  max-width: 100%;
  margin-left: auto;
  margin-right: auto;
}

.controls-row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

/* Barre de recherche */
.search-section {
  flex: 1;
  min-width: 200px;
}

.search-container {
  position: relative;
  display: flex;
  align-items: center;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  transition: all 0.2s ease;
}

.search-container:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-icon {
  color: #6b7280;
  margin-right: 0.5rem;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 0.875rem;
  color: #374151;
  padding: 0;
}

.search-input::placeholder {
  color: #9ca3af;
}

.clear-search-btn {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  margin-left: 0.5rem;
}

.clear-search-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
  flex-shrink: 0;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-label {
  font-weight: 500;
  color: #6b7280;
  font-size: 0.8rem;
  white-space: nowrap;
}

.filter-divider {
  width: 1px;
  height: 16px;
  background-color: #d1d5db;
  flex-shrink: 0;
}

.filter-buttons {
  display: flex;
  gap: 0.25rem;
}

.filter-btn {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
  font-weight: 500;
  color: #6b7280;
  transition: all 0.2s ease;
  min-width: 2rem;
  text-align: center;
  font-size: 0.8rem;
}

.filter-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
  background: #eff6ff;
}

.filter-btn.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
  box-shadow: 0 1px 4px rgba(59, 130, 246, 0.3);
}

.difficulty-stars {
  color: inherit;
  font-size: 0.8rem;
}

.difficulty-text {
  font-weight: 500;
}

.width-toggle-btn {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  min-width: auto !important;
}

.width-toggle-btn span:first-child {
  font-size: 0.875rem;
}

.pdf-btn {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.pdf-btn:hover:not(:disabled) {
  background: #3b82f6;
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.pdf-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pdf-btn:disabled:hover {
  background: #f9fafb;
  color: #6b7280;
  transform: none;
  box-shadow: none;
}

/* Responsive design for filters */
@media (max-width: 680px) {
  .exercices-controls {
    padding: 0.5rem;
    margin: 0.5rem;
  }

  .controls-row {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .search-section {
    min-width: auto;
    flex: none;
  }

  .search-container {
    padding: 0.4rem 0.6rem;
  }

  .search-input {
    font-size: 0.8rem;
  }

  .search-icon {
    width: 14px;
    height: 14px;
  }

  .filter-row {
    flex-direction: column;
    gap: 0.75rem;
    align-items: center;
  }

  .filter-item {
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
  }

  .filter-divider {
    display: none;
  }

  .filter-buttons {
    gap: 0.25rem;
  }

  .filter-btn {
    padding: 0.2rem 0.4rem;
    font-size: 0.75rem;
    min-width: 1.8rem;
  }
}

/* Navigation ultra-propre */
.clean-navigation {
  margin: 1.5rem 0 1rem 0;
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.4rem;
  width: 100%;
  margin: 0 auto;
}

.nav-item {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  text-align: left;
  min-height: 50px;
}

.nav-item:hover {
  border-color: #3b82f6;
  background: #f8fafc;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-item.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.nav-icon {
  font-size: 1.1rem;
  flex-shrink: 0;
}

.nav-label {
  font-size: 0.75rem;
  font-weight: 600;
  line-height: 1.2;
  flex: 1;
  text-align: left;
}

.nav-count {
  font-size: 0.6rem;
  font-weight: 700;
  background: rgba(0, 0, 0, 0.1);
  padding: 0.15rem 0.4rem;
  border-radius: 10px;
  min-width: 1.2rem;
  height: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.nav-item.active .nav-count {
  background: rgba(255, 255, 255, 0.25);
}

/* Style pour les boutons de téléchargement dans les filtres */
.download-enonces-btn {
  background: #3b82f6 !important;
  color: white !important;
  border-color: #3b82f6 !important;
  transition: all 0.2s ease;
}

.download-enonces-btn:hover {
  background: #2563eb !important;
  border-color: #2563eb !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.download-corriges-btn {
  background: #10b981 !important;
  color: white !important;
  border-color: #10b981 !important;
  transition: all 0.2s ease;
}

.download-corriges-btn:hover {
  background: #059669 !important;
  border-color: #059669 !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

/* Responsive */
@media (max-width: 680px) {
  .clean-navigation {
    margin: 1.5rem 0 1rem 0;
    padding: 0 0.5rem;
  }

  .nav-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.3rem;
    width: 100%;
  }

  .nav-item {
    padding: 0.4rem 0.4rem;
    min-height: 45px;
  }

  .nav-icon {
    font-size: 0.9rem;
  }

  .nav-label {
    font-size: 0.65rem;
  }

  .nav-count {
    font-size: 0.5rem;
    padding: 0.1rem 0.25rem;
    min-width: 1rem;
    height: 1rem;
  }
}

@media (max-width: 360px) {
  .clean-navigation {
    margin: 1.5rem 0 1rem 0;
  }

  .nav-grid {
    grid-template-columns: 1fr;
    gap: 0.3rem;
    width: 100%;
  }

  .nav-item {
    padding: 0.4rem 0.6rem;
    min-height: 40px;
  }

  .nav-icon {
    font-size: 0.85rem;
  }

  .nav-label {
    font-size: 0.6rem;
  }

  .nav-count {
    font-size: 0.5rem;
    padding: 0.1rem 0.2rem;
    min-width: 0.9rem;
    height: 0.9rem;
  }
}

</style> 
