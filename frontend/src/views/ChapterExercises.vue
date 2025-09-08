<template>
  <DashboardLayout>
    <section class="exercices-section">
      <!-- Bouton de retour -->
      <BackButton 
        text="Retour aux chapitres" 
        :customAction="goBackToChapitres"
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

      <h2 class="exercices-title" style="margin-top: 1.5rem; padding-top: 0.75rem;">Exercices du {{ chapitreNom }}</h2>
      
      <!-- Boutons de téléchargement en lot -->
      <div v-if="!loading && !error && filteredExercices.length > 0" class="download-section">
        <div class="download-actions">
          <h3 class="download-title">📄 Téléchargement en lot</h3>
          <div class="download-buttons">
            <PDFDownloadButton
              type="list"
              :data="filteredExercices"
              :title="`Exercices_${chapitreNom}_Enonces`"
              text="📋 Énoncés seuls"
              :useMathJax="true"
              :includeSolution="false"
              class="pdf-btn download-enonces-btn"
            />
            <PDFDownloadButton
              type="list"
              :data="filteredExercices"
              :title="`Exercices_${chapitreNom}_Corriges`"
              text="📝 Énoncés + Corrigés"
              :useMathJax="true"
              :includeSolution="true"
              class="pdf-btn download-corriges-btn"
            />
          </div>
          <p class="download-info">
            📊 {{ filteredExercices.length }} exercice(s) disponible(s) selon vos filtres actuels
          </p>
        </div>
      </div>
      
      <div v-if="loading" class="exercices-loader">Chargement...</div>
      <div v-else-if="error" class="exercices-error">{{ error }}</div>
      <div v-else>
        <div class="exercices-controls">
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

            <div class="filter-divider"></div>

            <div class="filter-item">
              <span class="filter-label">Affichage</span>
              <div class="filter-buttons">
                <button
                  :class="['filter-btn', 'width-toggle-btn', { active: isFullWidth }]"
                  @click="toggleFullWidth"
                  :title="isFullWidth ? 'Réduire la largeur' : 'Pleine largeur'"
                >
                  <span v-if="isFullWidth">📐</span>
                  <span v-else">↔️</span>
                  {{ isFullWidth ? 'Normal' : 'Large' }}
                </button>
              </div>
            </div>

            <div class="filter-divider"></div>

            <div class="filter-item">
              <span class="filter-label">Export PDF</span>
              <div class="filter-buttons">
                <button
                  class="filter-btn pdf-btn"
                  @click="generatePDF(false)"
                  :disabled="filteredExercices.length === 0"
                  title="Télécharger exercices sans correction"
                >
                  📄 Énoncés
                </button>
                <button
                  class="filter-btn pdf-btn"
                  @click="generatePDF(true)"
                  :disabled="filteredExercices.length === 0"
                  title="Télécharger exercices avec correction"
                >
                  📋 Corrigés
                </button>
              </div>
            </div>

            <div class="filter-divider"></div>

            <div class="filter-item">
              <span class="filter-label">Actions</span>
              <div class="filter-buttons">
                <button
                  class="filter-btn pdf-btn"
                  @click="downloadAllPDF"
                  title="Télécharger tous les exercices en PDF"
                >
                  📄 PDF
                </button>
              </div>
            </div>
          </div>
        </div>
        <div :class="['exercices-list', { 'full-width': isFullWidth }]">
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
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import { getExercices, getChapitres, getStatuses, createStatus, updateStatus, deleteStatus } from '@/api'
import { useUserStore } from '@/stores/user'
import ExerciceQCM from '@/components/UI/ExerciceQCM.vue'
import Pagination from '@/components/common/Pagination.vue'
import Tabs from '@/components/common/Tabs.vue'
import BackButton from '@/components/common/BackButton.vue'
import PDFDownloadButton from '@/components/common/PDFDownloadButton.vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const chapitreId = route.params.chapitreId

const exercices = ref([])
const perPageOptions = [1,3,5]
const perPage = ref(1)
const currentPage = ref(1)

// Filtre difficulté
const difficultyOptions = ['all','easy','medium','hard']
const selectedDifficulty = ref('all')

// Contrôle de largeur
const isFullWidth = ref(false)

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

// Fonction pour télécharger tous les exercices en PDF
const downloadAllPDF = async () => {
  try {
    console.log('Download all PDF clicked')
    console.log('Exercices data:', filteredExercices.value)
    
    // Import dynamique pour éviter les erreurs
    const { generateExercicesListPDF } = await import('@/utils/pdfGenerator')
    await generateExercicesListPDF(filteredExercices.value, `Exercices_${chapitreNom.value}`)
    alert('PDF généré avec succès !')
  } catch (error) {
    console.error('Erreur PDF:', error)
    alert('Erreur lors de la génération du PDF: ' + error.message)
  }
}

const statusMap = ref({}) // exerciceId -> { status, id }

const chapitreNom = ref('')
const loading = ref(true)
const error = ref('')
const chapitres = ref([]) // Ajouter un ref pour stocker les chapitres

onMounted(async () => {
  loading.value = true
  try {
    // Récupérer la liste de chapitres (format data direct via API unifiée)
    const chapitresData = await getChapitres()
    chapitres.value = Array.isArray(chapitresData) ? chapitresData : []
    const chapitre = chapitres.value.find(c => c.id == chapitreId)
    chapitreNom.value = chapitre ? chapitre.nom : 'Chapitre'
    
    // Récupérer les exercices (API unifiée attend un objet params)
    const niveauId = userStore.niveau_pays?.id
    const exercicesData = await getExercices({ chapitre: chapitreId, niveau: niveauId })
    exercices.value = Array.isArray(exercicesData) ? exercicesData : []
    console.log(`[ChapterExercises] Exercices chargés pour niveau ${niveauId}:`, exercices.value.length)
    
    // fetch statuses (adapter au nouveau modèle SuiviExercice)
    const { data: stats } = await getStatuses()
    const list = Array.isArray(stats) ? stats : (stats?.results || [])
    statusMap.value = Object.fromEntries(
      list.map(s => [
        s.exercice,
        { status: s.est_correct ? 'acquired' : 'not_acquired', id: s.id }
      ])
    )

    const notionId = chapitre ? chapitre.notion : chapitre?.notion_id
    // const { data: ficheData } = await getFiches(notionId ? `?notion=${notionId}` : '')
    // fiche.value = ficheData.length ? ficheData[0] : null
    currentPage.value = 1
    error.value = ''
  } catch (e) {
    console.error('[ChapterExercises] Erreur chargement:', e)
    error.value = "Impossible de charger les exercices."
  } finally {
    loading.value = false
  }
})

const totalPages = computed(() => Math.ceil(exercices.value.length / perPage.value))

const filteredExercices = computed(() => {
  let list = exercices.value
  if (selectedDifficulty.value !== 'all') list = list.filter(e=> e.difficulty === selectedDifficulty.value)
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
  return list
})

const paginated = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  return filteredExercices.value.slice(start, start + perPage.value)
})

function handlePageChange(page) {
  currentPage.value = page
  // scroll to top of exercises
  window.scrollTo({ top: 0, behavior: 'smooth' })
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
        
        // Intégration avec les objectifs journaliers (même pour les mises à jour)
        if (status === 'acquired') {
          console.log(`[ChapterExercices] Exercice réussi (mise à jour) - intégration objectifs journaliers`)
          // Importer et utiliser l'intégration des objectifs journaliers
          const { useDailyObjectivesIntegration } = await import('@/composables/useDailyObjectives')
          const { onExerciseCompleted } = useDailyObjectivesIntegration()
          
          // Notifier le système d'objectifs
          onExerciseCompleted({
            exerciceId,
            isSuccess: true,
            status: 'acquired'
          })
        }
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
      
      // Intégration avec les objectifs journaliers
      if (status === 'acquired') {
        console.log(`[ChapterExercices] Exercice réussi - intégration objectifs journaliers`)
        // Importer et utiliser l'intégration des objectifs journaliers
        const { useDailyObjectivesIntegration } = await import('@/composables/useDailyObjectives')
        const { onExerciseCompleted } = useDailyObjectivesIntegration()
        
        // Notifier le système d'objectifs
        onExerciseCompleted({
          exerciceId,
          isSuccess: true,
          status: 'acquired'
        })
      }
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

function goBackToChapitres() {
  try {
    const chapitre = chapitres.value?.find?.(c => c.id == chapitreId)
    const notionId = chapitre ? (chapitre.notion || chapitre.notion_id) : null
    if (notionId) {
      router.push({ name: 'Chapitres', params: { notionId: String(notionId) } })
    } else {
      router.back()
    }
  } catch (err) {
    router.back()
  }
}

function toggleFullWidth() {
  isFullWidth.value = !isFullWidth.value
}

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
      `Exercices de ${chapitreNom.value}` : 
      `Feuille d'exercices - ${chapitreNom.value}`
    
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
    const sanitizedChapterName = chapitreNom.value
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

@media (max-width: 480px) {
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
  max-width: 700px;
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

@media (max-width: 480px) {
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
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.filter-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  flex-wrap: wrap;
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
@media (max-width: 768px) {
  .exercices-controls {
    padding: 0.5rem;
    margin: 0.5rem;
  }

  .filter-row {
    flex-direction: column;
    gap: 0.75rem;
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
  margin: 1.5rem 0;
  padding: 0 1rem;
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;
  max-width: 500px;
  margin: 0 auto;
}

.nav-item {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.75rem 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  text-align: center;
}

.nav-item:hover {
  border-color: #3b82f6;
  background: #f8fafc;
}

.nav-item.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: #ffffff;
}

.nav-icon {
  font-size: 1.25rem;
}

.nav-label {
  font-size: 0.75rem;
  font-weight: 500;
}

.nav-count {
  font-size: 0.625rem;
  font-weight: 600;
  background: rgba(0, 0, 0, 0.1);
  padding: 0.125rem 0.25rem;
  border-radius: 4px;
  min-width: 1.25rem;
}

.nav-item.active .nav-count {
  background: rgba(255, 255, 255, 0.2);
}

/* Style pour le bouton PDF */
.pdf-btn {
  background: #dc2626 !important;
  color: white !important;
  border-color: #dc2626 !important;
  transition: all 0.2s ease;
}

.pdf-btn:hover {
  background: #b91c1c !important;
  border-color: #b91c1c !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
  .clean-navigation {
    margin: 2.5rem 0 1rem 0; /* Plus d'espace en haut pour éviter le chevauchement */
    padding: 0 0.5rem;
  }

  .nav-grid {
    gap: 0.5rem;
  }

  .nav-item {
    padding: 0.5rem 0.25rem;
  }

  .nav-icon {
    font-size: 1.125rem;
  }

  .nav-label {
    font-size: 0.7rem;
  }

  .nav-count {
    font-size: 0.6rem;
    padding: 0.1rem 0.2rem;
  }
}

@media (max-width: 480px) {
  .clean-navigation {
    margin: 3rem 0 1rem 0; /* Encore plus d'espace pour les petits écrans */
  }

  .nav-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.375rem;
  }

  .nav-item {
    padding: 0.625rem 0.25rem;
  }
}

@media (max-width: 360px) {
  .clean-navigation {
    margin: 3.5rem 0 1rem 0; /* Maximum d'espace pour les très petits écrans */
  }

  .nav-grid {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }

  .nav-item {
    flex-direction: row;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
  }
}

/* Styles pour la section de téléchargement */
.download-section {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.download-actions {
  text-align: center;
}

.download-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.download-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.download-enonces-btn {
  background: #3b82f6 !important;
  border-color: #3b82f6 !important;
}

.download-enonces-btn:hover {
  background: #2563eb !important;
  border-color: #2563eb !important;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.download-corriges-btn {
  background: #10b981 !important;
  border-color: #10b981 !important;
}

.download-corriges-btn:hover {
  background: #059669 !important;
  border-color: #059669 !important;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.download-info {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
  font-style: italic;
}

/* Responsive pour la section de téléchargement */
@media (max-width: 640px) {
  .download-buttons {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .download-section {
    padding: 1rem;
    margin: 1rem 0;
  }
  
  .download-title {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .download-section {
    padding: 0.75rem;
    border-radius: 8px;
  }
  
  .download-title {
    font-size: 0.9rem;
    flex-direction: column;
    gap: 0.25rem;
  }
}
</style> 