<template>
  <div class="exercice-card" :class="{ 
    'completed': current === 'acquired', 
    'acquired': current === 'acquired',
    'not-acquired': current === 'not_acquired'
  }">

    <!-- Header with title and difficulty -->
    <div class="exercice-header">
      <div class="exercice-title-section">
        <div class="title-row">
          <h3 v-if="titre" class="exercice-title">{{ titre }}</h3>
          <div class="header-controls">
            <div class="difficulty-indicator">
              <span v-if="difficulty" class="difficulty-stars">{{ diffStars[difficulty] || '★★' }}</span>
            </div>
            <button v-if="current" class="reset-status-btn" @click="resetStatus" title="Réinitialiser le statut">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>
                <path d="M21 3v5h-5"/>
                <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>
                <path d="M3 21v-5h5"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Problem Statement -->
    <div class="problem-section">
      <div class="section-header">
        <div class="section-icon-wrapper">
          <div class="section-icon">📝</div>
        </div>
        <div class="section-info">
          <h4 class="section-title">Énoncé du problème</h4>
          <p class="section-description">Lisez attentivement l'énoncé avant de commencer</p>
        </div>
      </div>
      <div class="problem-content" v-html="renderInstructionWithImages(instruction)" @click="handleImageClick"></div>
    </div>

    <!-- Learning Path -->
    <div class="learning-path">
      <div class="path-step active">
        <div class="step-indicator">1</div>
        <span class="step-text">Lecture de l'énoncé</span>
      </div>
      <div class="path-step" :class="{ 'active': showSolution }">
        <div class="step-indicator">2</div>
        <span class="step-text">Analyse de la solution</span>
      </div>
      <div class="path-step" :class="{ 'active': current }">
        <div class="step-indicator">3</div>
        <span class="step-text">Auto-évaluation</span>
      </div>
    </div>

    <!-- Solution Toggle -->
    <div class="solution-toggle">
      <button class="toggle-btn" @click="toggleSolution" :class="{ 'expanded': showSolution }">
        <div class="toggle-content">
          <span class="toggle-icon">{{ showSolution ? '−' : '+' }}</span>
          <div class="toggle-text-group">
            <span class="toggle-text">{{ showSolution ? 'Masquer la solution' : 'Voir la solution' }}</span>
            <span class="toggle-subtext">{{ showSolution ? 'Cliquez pour replier' : 'Cliquez pour découvrir la méthode' }}</span>
          </div>
        </div>
        <div class="toggle-arrow" :class="{ 'rotated': showSolution }">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="m6 9 6 6 6-6"/>
          </svg>
        </div>
    </button>
    </div>

    <!-- Solution Content -->
    <div v-if="showSolution" class="solution-content">
      <!-- Steps Section -->
      <div v-if="etapes" class="solution-section steps-section">
        <div class="section-header">
          <div class="section-icon-wrapper">
            <div class="section-icon">🔢</div>
          </div>
          <div class="section-info">
            <h4 class="section-title">Méthode de résolution</h4>
            <p class="section-description">Suivez ces étapes pour comprendre la démarche</p>
          </div>
        </div>
        <div class="steps-container">
          <div class="steps-content" v-html="renderInstructionWithImages(etapes)" @click="handleImageClick"></div>
        </div>
      </div>

      <!-- Answer Section -->
      <div v-if="solution" class="solution-section answer-section">
        <div class="section-header">
          <div class="section-icon-wrapper">
            <div class="section-icon">✅</div>
          </div>
          <div class="section-info">
            <h4 class="section-title">Réponse</h4>
            <p class="section-description">La solution complète à l'exercice</p>
          </div>
        </div>
        <div class="answer-content" v-html="renderInstructionWithImages(solution)" @click="handleImageClick"></div>
      </div>
    </div>

    <!-- Assessment Section -->
    <div class="assessment-section">
      <div class="assessment-header">
        <h4 class="assessment-title">Auto-évaluation</h4>
        <p class="assessment-description">Évaluez votre compréhension de cet exercice</p>
      </div>
      

      
      <div class="assessment-buttons">
        <button 
          class="assessment-btn acquired" 
          :class="{ 'active': current === 'acquired' }"
          @click="setStatus('acquired')"
        >
          <span class="btn-icon">✅</span>
          <span class="btn-text">J'ai compris</span>
        </button>
        <button 
          class="assessment-btn not-acquired" 
          :class="{ 'active': current === 'not_acquired' }"
          @click="setStatus('not_acquired')"
        >
          <span class="btn-icon">❌</span>
          <span class="btn-text">À revoir</span>
        </button>
      </div>
    </div>

    <!-- Image Modal -->
    <div v-if="showImageModal" class="image-modal-overlay" @click="closeImageModal">
      <div class="image-modal" @click.stop>
        <button class="modal-close-btn" @click="closeImageModal">×</button>
        <img 
          :src="getImageUrl(selectedImage.image)" 
          :alt="`Image ${selectedImage.image_type === 'donnee' ? 'donnée' : 'solution'}`"
          class="modal-image"
        />
        <div class="modal-caption">
          <span class="modal-image-type">{{ selectedImage.image_type === 'donnee' ? 'Donnée' : 'Solution' }}</span>
          <span v-if="selectedImage.position" class="modal-position">Position {{ selectedImage.position }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick, watch } from 'vue'
import { getExerciceImages } from '@/api'

// Props
const props = defineProps({
  eid: {
    type: [String, Number],
    required: true
  },
  titre: {
    type: String,
    default: ''
  },
  instruction: {
    type: String,
    default: ''
  },
  solution: {
    type: String,
    default: ''
  },
  etapes: {
    type: String,
    default: ''
  },
  difficulty: {
    type: String,
    default: 'medium'
  },
  current: {
    type: String,
    default: null
  },
  previewImages: {
    type: Array,
    default: () => []
  }
})

// Emits
const emit = defineEmits(['status-changed', 'xp-gained'])

// Reactive data
const showSolution = ref(false)
const exerciceImages = ref([])
const showImageModal = ref(false)
const selectedImage = ref(null)

// Computed
const diffStars = computed(() => ({
  easy: '★',
  medium: '★★',
  hard: '★★★'
}))

// Methods
function toggleSolution() {
  showSolution.value = !showSolution.value
  if (showSolution.value) {
    renderMath()
  }
}

function setStatus(status) {
  emit('status-changed', { exerciceId: props.eid, status })
}

function resetStatus() {
  emit('status-changed', { exerciceId: props.eid, status: null })
}

function unescapeLatex(text) {
  if (!text) return ''

  // 1) Unescape HTML de base et conserver les backslashes LaTeX
  let base = text
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/\\/g, '\\')

  // Séparer en segments pour préserver les blocs math (que MathJax doit traiter)
  const mathRegex = /(\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\))/g
  const segments = []
  let lastIndex = 0
  let match
  while ((match = mathRegex.exec(base)) !== null) {
    if (match.index > lastIndex) {
      segments.push({ type: 'text', value: base.slice(lastIndex, match.index) })
    }
    segments.push({ type: 'math', value: match[0] })
    lastIndex = match.index + match[0].length
  }
  if (lastIndex < base.length) {
    segments.push({ type: 'text', value: base.slice(lastIndex) })
  }

  const htmlParts = segments.map((seg) => {
    if (seg.type === 'math') {
      // Compat: remplacer tabular par array pour prise en charge MathJax
      let mathBlock = seg.value
        .replace(/\\begin\{tabular\}/g, '\\begin{array}')
        .replace(/\\end\{tabular\}/g, '\\end{array}')

      // Normaliser colonnes: p{...} -> c
      mathBlock = mathBlock.replace(/\\begin\{array\}\{([^}]*)\}/, (m, spec) => {
        const normalized = spec.replace(/p\{[^}]+\}/g, 'c')
        return `\\begin{array}{${normalized}}`
      })

      // Retirer les $ visibles à l'intérieur des cellules (déjà en mode math)
      mathBlock = mathBlock.replace(/\\begin\{array\}\{[^}]*\}([\s\S]*?)\\end\{array\}/g, (full, inner) => {
        const cleanedInner = inner.replace(/\$/g, '')
        return full.replace(inner, cleanedInner)
      })

      return `<div class=\"mathjax-block\">${mathBlock}</div>`
    }

    // Segment texte: markdown léger puis rendu par lignes
    let textPart = seg.value
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\*([^*]+)\*/g, '<em>$1</em>')

    const lines = textPart.split('\n')
    const processed = lines.map((line) => {
      if (line.trim() === '') return '<br/>'

      const bulletMatch = line.match(/^(?:(\s*))\s*●\s+(.+)$/)
      if (bulletMatch) {
        const indentSpaces = Math.max(bulletMatch[1] ? bulletMatch[1].length : 0, 4)
        const marginLeft = indentSpaces * 6
        return `<div class=\"step-bullet\" style=\"margin-left: ${marginLeft}px;\"><span class=\"bullet-symbol\">●</span> <span class=\"bullet-text\">${bulletMatch[2]}</span></div>`
      }

      const indentMatch = line.match(/^(\s+)(.+)$/)
      if (indentMatch && !indentMatch[2].includes('<div') && !indentMatch[2].includes('<strong') && !indentMatch[2].includes('●')) {
        const indentSpaces = indentMatch[1].length
        const marginLeft = indentSpaces * 6
        return `<div class=\"step-line\" style=\"margin-left: ${marginLeft}px;\">${indentMatch[2]}</div>`
      }

      return `<div class=\"step-title\">${line}</div>`
    })

    return processed.join('')
  })

  let result = htmlParts.join('')
  result = result
    .replace(/(<br\/>\s*){3,}/g, '<br/><br/>')
    .replace(/  +/g, '&nbsp;&nbsp;')

  return result
}

function renderInstructionWithImages(instruction) {
  if (!instruction) return ''
  
  // D'abord, traiter le texte de base
  let processedText = unescapeLatex(instruction)
  
  // Si pas d'images, retourner le texte traité
  if (!exerciceImages.value || exerciceImages.value.length === 0) {
    return processedText
  }
  
  // Créer un mapping des images par position
  const imagesByPosition = {}
  exerciceImages.value.forEach(img => {
    if (img.position) {
      imagesByPosition[img.position] = img
    }
  })
  
  // Remplacer les marqueurs [IMAGE_1], [IMAGE_2], etc. par les images
  processedText = processedText.replace(/\[IMAGE_(\d+)\]/g, (match, position) => {
    const image = imagesByPosition[parseInt(position)]
    if (image) {
      return `
        <div class="exercice-image-container inline-image" data-image-position="${position}">
          <img 
            src="${getImageUrl(image.image)}" 
            alt="Image ${image.image_type === 'donnee' ? 'donnée' : 'solution'} - position ${position}"
            class="exercice-image inline"
            style="cursor: pointer;"
          />
        </div>
      `
    }
    return match // Garder le marqueur si l'image n'existe pas
  })
  
  return processedText
}

function renderMath() {
  nextTick(() => {
    const doTypeset = () => {
      try {
        if (window.MathJax && window.MathJax.typesetPromise) {
          return window.MathJax.typesetPromise()
        }
      } catch (_) {}
      return Promise.resolve()
    }

    // Si MathJax expose sa promesse de démarrage, l'utiliser pour garantir le chargement
    if (window.MathJax && window.MathJax.startup && window.MathJax.startup.promise) {
      window.MathJax.startup.promise.then(() => doTypeset())
      return
    }

    // Sinon, attendre jusqu'à disponibilité (durée plus longue qu'avant)
    let tries = 0
    const maxRetries = 50 // ~10s à 200ms d'intervalle
    const tryRender = () => {
      if (window.MathJax && window.MathJax.typesetPromise) {
        doTypeset()
      } else if (tries++ < maxRetries) {
        setTimeout(tryRender, 200)
      }
    }
    tryRender()
  })
}

function getImageUrl(imagePath) {
  // Debug: voir ce que le backend retourne (seulement si pas en mode aperçu)
  if (!props.eid || !props.eid.toString().startsWith('preview-')) {
    console.log('getImageUrl - imagePath reçu:', imagePath, 'type:', typeof imagePath)
  }

  // Si c'est un aperçu et que imagePath est déjà une URL (blob: ou data:)
  if (props.eid && props.eid.toString().startsWith('preview-') &&
      (imagePath && (imagePath.startsWith('blob:') || imagePath.startsWith('data:')))) {
    return imagePath
  }

  // Si c'est déjà une URL absolue http(s), la renvoyer telle quelle
  if (imagePath && /^(https?:)?\/\//i.test(imagePath)) {
    return imagePath
  }

  // Vérifier si S3 est utilisé en priorité
  const s3MediaUrl = window.__ENV__?.VITE_S3_MEDIA_URL || import.meta.env?.VITE_S3_MEDIA_URL

  // Si une URL S3 est configurée, l'utiliser
  if (s3MediaUrl && imagePath) {
    // Nettoyer le chemin d'image et construire l'URL S3
    let cleanImagePath = imagePath.replace(/^\/+/, '') // Supprimer les / de début

    // Si c'est un chemin relatif comme 'exercice_images/filename.png', l'utiliser tel quel
    if (cleanImagePath.includes('/')) {
      const fullUrl = `${s3MediaUrl}/${cleanImagePath}`
      if (!props.eid || !props.eid.toString().startsWith('preview-')) {
        console.log('getImageUrl - URL S3 (chemin relatif):', fullUrl)
      }
      return fullUrl
    }

    // Si c'est juste un nom de fichier, l'utiliser tel quel avec S3
    const fullUrl = `${s3MediaUrl}/${cleanImagePath}`
    if (!props.eid || !props.eid.toString().startsWith('preview-')) {
      console.log('getImageUrl - URL S3 (nom fichier):', fullUrl)
    }
    return fullUrl
  }

  // Détecter l'environnement et construire l'URL de base (backend pour les médias)
  const isProduction = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1'
  let prodMediaBase = null
  try {
    // import.meta.env remplacé à build-time par Vite
    // eslint-disable-next-line no-undef
    prodMediaBase = (import.meta && import.meta.env)
      ? (import.meta.env.VITE_MEDIA_BASE_URL || import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_URL)
      : null
  } catch (_) {
    prodMediaBase = null
  }
  const baseUrl = isProduction
    ? (prodMediaBase || 'https://optitab-backend.onrender.com')
    : 'http://localhost:8000'

  // Construire l'URL complète de l'image
  // Si imagePath est déjà un chemin complet (commence par /media/), l'utiliser tel quel
  if (imagePath && imagePath.startsWith('/media/')) {
    const fullUrl = `${baseUrl}${imagePath}`
    if (!props.eid || !props.eid.toString().startsWith('preview-')) {
      console.log('getImageUrl - URL complète (déjà /media/):', fullUrl)
    }
    return fullUrl
  }
  // Si imagePath est un chemin relatif (commence par exercice_images/), construire l'URL complète
  if (imagePath && imagePath.startsWith('exercice_images/')) {
    const fullUrl = `${baseUrl}/media/${imagePath}`
    if (!props.eid || !props.eid.toString().startsWith('preview-')) {
      console.log('getImageUrl - URL complète (chemin relatif):', fullUrl)
    }
    return fullUrl
  }
  // Si imagePath est juste un nom de fichier, construire le chemin complet
  if (imagePath && !imagePath.startsWith('/') && !imagePath.includes('/')) {
    const fullUrl = `${baseUrl}/media/exercice_images/${imagePath}`
    if (!props.eid || !props.eid.toString().startsWith('preview-')) {
      console.log('getImageUrl - URL complète (nom fichier):', fullUrl)
    }
    return fullUrl
  }
  // Si imagePath est null ou undefined, retourner une chaîne vide
  if (!props.eid || !props.eid.toString().startsWith('preview-')) {
    console.log('getImageUrl - imagePath invalide, retourne:', imagePath || '')
  }
  return imagePath || ''
}

function openImageModal(image) {
  selectedImage.value = image
  showImageModal.value = true
}

function closeImageModal() {
  showImageModal.value = false
  selectedImage.value = null
}

function handleImageClick(event) {
  // Vérifier si le clic est sur une image inline
  if (event.target.classList.contains('exercice-image') && event.target.classList.contains('inline')) {
    const container = event.target.closest('.inline-image')
    if (container) {
      const position = container.dataset.imagePosition
      const image = exerciceImages.value.find(img => img.position === parseInt(position))
      if (image) {
        openImageModal(image)
      }
    }
    return
  }
  // Si c'est une image générique rendue dans le contenu (sans classe spéciale)
  if (event.target && event.target.tagName === 'IMG') {
    openImageModal({ image: event.target.src, image_type: 'aperçu', position: null })
  }
}

// Détecter la présence de marqueurs d'images [IMAGE_1], [IMAGE_2], ...
function hasImageMarkers() {
  const texts = [props.instruction, props.etapes, props.solution].filter(Boolean)
  return texts.some(t => /\[IMAGE_\d+\]/.test(t))
}

// Load exercice images (appelé uniquement si des marqueurs d'images existent)
async function loadExerciceImages() {
  // Mode aperçu avec images passées en props
  if (props.eid && props.eid.toString().startsWith('preview-')) {
    exerciceImages.value = props.previewImages || []
    return
  }
  
  // Si aucun marqueur d'image dans les contenus, ne rien appeler
  if (!hasImageMarkers()) {
    exerciceImages.value = []
    return
  }
  
  try {
    const { data } = await getExerciceImages(props.eid)
    exerciceImages.value = data
  } catch (error) {
    // Backend sans endpoint d'images → ignorer silencieusement
    exerciceImages.value = []
  }
}

// Watch for content changes to re-render MathJax
watch(() => [props.instruction, props.etapes, props.solution], renderMath, { immediate: true })

// Watch for preview images changes
watch(() => props.previewImages, () => {
  if (props.eid && props.eid.toString().startsWith('preview-')) {
    exerciceImages.value = props.previewImages || []
  }
}, { immediate: true })

// Lifecycle
onMounted(() => {
  // Charger les images uniquement si nécessaire
  if (hasImageMarkers() || (props.previewImages && props.previewImages.length > 0)) {
    loadExerciceImages()
  }
  renderMath()
})
</script>

<style scoped>
/* Main Exercise Card */
.exercice-card {
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  margin-bottom: 32px;
  position: relative;
}

.exercice-card:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.exercice-card.completed {
  border-color: #22c55e;
  box-shadow: 0 4px 6px -1px rgba(34, 197, 94, 0.1), 0 2px 4px -1px rgba(34, 197, 94, 0.06);
}

.exercice-card.acquired {
  border-color: #22c55e;
  box-shadow: 0 4px 6px -1px rgba(34, 197, 94, 0.1), 0 2px 4px -1px rgba(34, 197, 94, 0.06);
}

.exercice-card.not-acquired {
  border-color: #ef4444;
  box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.1), 0 2px 4px -1px rgba(239, 68, 68, 0.06);
}


/* Header Section */
.exercice-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 28px 28px 20px 28px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 1px solid #e2e8f0;
}

.exercice-title-section {
  flex: 1;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}

.exercice-title {
  font-size: 1.375rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  line-height: 1.3;
  flex: 1;
}

.header-controls {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.difficulty-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.difficulty-stars {
  font-size: 1rem;
  color: #f59e0b;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(245, 158, 11, 0.3);
}



.reset-status-btn {
  background: #ffffff;
  border: 2px solid #e5e7eb;
  color: #64748b;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: all 0.2s ease;
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.reset-status-btn:hover {
  background: #f8fafc;
  border-color: #3b82f6;
  color: #3b82f6;
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.2);
}

/* Learning Path */
.learning-path {
  display: flex;
  justify-content: space-between;
  padding: 20px 28px;
  background: #fafbfc;
  border-bottom: 1px solid #f1f5f9;
}

.path-step {
  display: flex;
  align-items: center;
  gap: 8px;
  opacity: 0.5;
  transition: all 0.3s ease;
}

.path-step.active {
  opacity: 1;
}

.step-indicator {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #e2e8f0;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.path-step.active .step-indicator {
  background: #3b82f6;
  color: #ffffff;
}

.step-text {
  font-size: 0.875rem;
  font-weight: 500;
  color: #64748b;
  transition: color 0.3s ease;
}

.path-step.active .step-text {
  color: #1e293b;
}

/* Problem Section */
.problem-section {
  padding: 24px 28px;
  border-bottom: 1px solid #f1f5f9;
}

.section-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 20px;
}

.section-icon-wrapper {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e0e7ff;
}

.section-icon {
  font-size: 1.5rem;
}

.section-info {
  flex: 1;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 4px 0;
}

.section-description {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
  line-height: 1.4;
}

.problem-content {
  font-size: 1rem;
  line-height: 1.7;
  color: #1f2937;
  text-align: left;
}

/* Solution Toggle */
.solution-toggle {
  padding: 20px 28px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.toggle-btn {
  width: 100%;
  background: #ffffff;
  border: 2px solid #e5e7eb;
  border-radius: 16px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 600;
  color: #374151;
}

.toggle-btn:hover {
  border-color: #3b82f6;
  background: #eff6ff;
  color: #1d4ed8;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.toggle-btn.expanded {
  background: #3b82f6;
  border-color: #3b82f6;
  color: #ffffff;
}

.toggle-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.toggle-icon {
  font-size: 1.5rem;
  font-weight: bold;
  width: 24px;
  text-align: center;
}

.toggle-text-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.toggle-text {
  font-size: 1rem;
  font-weight: 600;
}

.toggle-subtext {
  font-size: 0.875rem;
  font-weight: 400;
  opacity: 0.8;
}

.toggle-arrow {
  transition: transform 0.3s ease;
}

.toggle-arrow.rotated {
  transform: rotate(180deg);
}

/* Solution Content */
.solution-content {
  background: #fafbfc;
}

.solution-section {
  padding: 24px 28px;
  border-bottom: 1px solid #f1f5f9;
}

.solution-section:last-child {
  border-bottom: none;
}

.steps-section {
  background: #fef7ff;
  border-bottom: 1px solid #f3e8ff;
}

.steps-section .section-icon-wrapper {
  background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
  border-color: #e9d5ff;
}

.answer-section {
  background: #f0fdf4;
  border-bottom: 1px solid #dcfce7;
}

.answer-section .section-icon-wrapper {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-color: #bbf7d0;
}

.steps-container {
  max-width: none;
  margin: 0;
  padding: 0;
}

.steps-content,
.answer-content {
  font-size: 1rem;
  line-height: 1.7;
  color: #1f2937;
  text-align: left;
  padding-left: 0;
  margin-left: 0;
}

/* Amélioration des étapes de résolution - Version simple et propre */
.steps-content :deep(ul),
.steps-content :deep(ol) {
  padding-left: 0 !important;
  margin: 1rem 0;
  list-style: none;
  text-align: left;
}

.steps-content :deep(li) {
  position: relative;
  padding: 0.75rem 0 !important;
  padding-left: 0 !important;
  margin: 0.5rem 0;
  margin-left: 0 !important;
  line-height: 1.6;
  text-align: left !important;
  text-indent: 0 !important;
}

.steps-content :deep(li::before) {
  content: "";
  display: none;
}

/* Styles spécifiques pour les numéros d'étapes */
.steps-content :deep(p) {
  margin: 0.5rem 0 !important;
  padding-left: 0 !important;
  text-align: left !important;
  text-indent: 0 !important;
}

/* Style pour les expressions mathématiques dans les étapes */
.steps-content :deep(.MathJax_Display) {
  margin: 0.75rem 0;
  text-align: center;
}

.steps-content :deep(.MathJax) {
  text-align: center;
}

/* Styles pour les titres de questions */
.step-title {
  display: block;
  line-height: 1.6;
  margin: 0rem 0 0rem 0; /* Marges ultra réduites à zéro */
  font-weight: 600;
  color: #1e293b;
  white-space: normal;
  word-wrap: break-word;
  padding-left: 0; /* Pas d'indentation pour les titres */
}

/* Styles pour les lignes d'étapes avec indentation */
.step-line {
  display: block;
  line-height: 1.6;
  margin: 0rem 0; /* Marges à zéro */
  white-space: normal;
  word-wrap: break-word;
}

/* Styles pour les puces dans les étapes */
.step-bullet {
  display: block;
  line-height: 1.6;
  margin: 0rem 0; /* Marges à zéro */
  position: relative;
  min-height: 1.2em;
  white-space: normal;
  word-wrap: break-word;
}

.bullet-symbol {
  color: #3b82f6;
  font-weight: bold;
  font-size: 1.2em;
  margin-right: 4px; /* Petit espace supplémentaire */
  display: inline-block;
  width: 20px;
  text-align: center;
  vertical-align: top;
}

.bullet-text {
  display: inline-block;
  vertical-align: top;
  line-height: 1.4;
}

/* Styles pour les paragraphes dans les étapes */
.steps-content :deep(p) {
  margin: 0.75rem 0 !important;
  line-height: 1.6;
}

/* Améliorer l'espacement entre les blocs d'étapes */
.steps-content :deep(br + br) {
  margin-top: 0rem; /* Zéro espace */
}

/* Style pour les titres d'étapes */
.steps-content :deep(strong) {
  font-weight: 600;
  color: #1e293b;
  display: inline;
  margin: 0;
}

/* Style pour les expressions mathématiques dans les étapes */
.steps-content :deep(.MathJax_Display) {
  margin: 0.75rem 0;
  text-align: center;
}

.steps-content :deep(.MathJax) {
  text-align: center;
}

/* Assessment Section */
.assessment-section {
  padding: 28px;
  background: #ffffff;
  border-top: 1px solid #e5e7eb;
}

.assessment-section .section-icon-wrapper {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-color: #fcd34d;
}

.assessment-header {
  text-align: center;
  margin-bottom: 20px;
}

.assessment-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.assessment-description {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
  line-height: 1.5;
}



.assessment-content {
  text-align: center;
}

.assessment-question {
  margin-bottom: 24px;
}

.assessment-question h5 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.assessment-question p {
  font-size: 1rem;
  color: #64748b;
  margin: 0;
  line-height: 1.5;
}

.assessment-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.assessment-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 24px;
  border: 2px solid #e5e7eb;
  border-radius: 16px;
  background: #ffffff;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 600;
  font-size: 1rem;
  min-width: 180px;
  justify-content: center;
}

.assessment-btn:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.assessment-btn.success {
  color: #166534;
  border-color: #bbf7d0;
}

.assessment-btn.success:hover {
  background: #dcfce7;
  border-color: #86efac;
}

.assessment-btn.success.active {
  background: #dcfce7;
  border-color: #22c55e;
  color: #15803d;
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.2);
}

.assessment-btn.warning {
  color: #991b1b;
  border-color: #fecaca;
}

.assessment-btn.warning:hover {
  background: #fee2e2;
  border-color: #fca5a5;
}

.assessment-btn.warning.active {
  background: #fee2e2;
  border-color: #ef4444;
  color: #b91c1c;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
}

.btn-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-icon {
  font-size: 1.25rem;
}

.btn-text-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.btn-text {
  font-size: 1rem;
  font-weight: 600;
}

.btn-subtext {
  font-size: 0.875rem;
  font-weight: 400;
  opacity: 0.8;
}

/* Completion Celebration */
.completion-celebration {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  border-top: 1px solid #22c55e;
  padding: 16px 28px;
  text-align: center;
}

.celebration-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.celebration-icon {
  font-size: 1.5rem;
  animation: bounce 1s infinite;
}

.celebration-text {
  font-size: 1rem;
  font-weight: 600;
  color: #15803d;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-4px);
  }
  60% {
    transform: translateY(-2px);
  }
}

/* MathJax Styles */
.exercice-card :deep(.MathJax) {
  max-width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
}

.exercice-card :deep(.MathJax_Display) {
  max-width: 100%;
  overflow-x: auto;
  margin: 1.5rem 0;
}

.exercice-card :deep(.MathJax_SVG_Display) {
  max-width: 100%;
  overflow-x: auto;
}

.exercice-card :deep(.MathJax_SVG) {
  max-width: 100%;
}

/* Responsive Design */
@media (max-width: 768px) {
  .exercice-card {
    margin: 0 8px 24px 8px;
    border-radius: 16px;
  }

  .steps-container {
    padding: 0;
  }

  .steps-content :deep(li) {
    padding: 0.75rem 0;
    margin: 0.375rem 0;
    text-align: left;
  }
  
  .exercice-header {
    padding: 24px 24px 16px 24px;
  }
  
  .title-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .exercice-title {
    font-size: 1.25rem;
  }
  
  .learning-path {
    padding: 16px 24px;
    flex-direction: column;
    gap: 12px;
  }
  
  .path-step {
    width: 100%;
    justify-content: center;
  }
  
  .problem-section,
  .solution-section {
    padding: 20px 24px;
  }
  
  .solution-toggle {
    padding: 16px 24px;
  }
  
  .assessment-section {
    padding: 24px;
  }
  
  .assessment-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .assessment-btn {
    width: 100%;
    max-width: 280px;
  }
  
  /* MathJax responsive */
  .exercice-card :deep(.MathJax_Display) {
    font-size: 0.9em;
    margin: 1rem 0;
  }
  
  .exercice-card :deep(.MathJax_SVG_Display) {
    font-size: 0.9em;
  }
  
  .exercice-card :deep(.MathJax_SVG) {
    font-size: 0.9em;
  }
}

@media (max-width: 480px) {
  .exercice-card {
    margin: 0 4px 20px 4px;
    border-radius: 12px;
  }

  .steps-container {
    padding: 0;
  }

  .steps-content :deep(li) {
    padding: 0.625rem 0;
    margin: 0.25rem 0;
    font-size: 0.9rem;
    text-align: left;
  }
  
  .exercice-header {
    padding: 20px 20px 12px 20px;
  }
  
  .exercice-title {
    font-size: 1.125rem;
  }
  
  .learning-path {
    padding: 12px 20px;
  }
  
  .problem-section,
  .solution-section {
    padding: 16px 20px;
  }
  
  .solution-toggle {
    padding: 12px 20px;
  }
  
  .assessment-section {
    padding: 20px;
  }
  
  /* MathJax responsive */
  .exercice-card :deep(.MathJax_Display) {
    font-size: 0.8em;
    margin: 0.75rem 0;
  }
  
  .exercice-card :deep(.MathJax_SVG_Display) {
    font-size: 0.8em;
  }
  
  .exercice-card :deep(.MathJax_SVG) {
    font-size: 0.8em;
  }
}

/* Text content styles */
.exercice-card :deep(p) {
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
  margin: 0 0 1rem 0;
}

.exercice-card :deep(p:last-child) {
  margin-bottom: 0;
}

.exercice-card :deep(strong) {
  font-weight: 700;
  color: #1e293b;
}

.exercice-card :deep(em) {
  font-style: italic;
  color: #1e293b;
}

.exercice-card :deep(ul),
.exercice-card :deep(ol) {
  padding-left: 0;
  margin: 1rem 0;
}

@media (max-width: 768px) {
  .exercice-card :deep(ul),
  .exercice-card :deep(ol) {
    padding-left: 0;
  }
}

@media (max-width: 480px) {
  .exercice-card :deep(ul),
  .exercice-card :deep(ol) {
    padding-left: 0;
  }
}

/* Styles pour les images */
.exercice-images {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.exercice-image-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.exercice-image {
  max-width: 100%;
  max-height: 150px; /* Hauteur maximale très réduite */
  width: auto;
  height: auto;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  cursor: pointer;
  transition: box-shadow 0.2s ease;
  object-fit: contain; /* Garde les proportions */
}

.exercice-image:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.image-caption {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
}

.image-type-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.image-type-badge.donnee {
  background: #dbeafe;
  color: #1e40af;
}

.image-type-badge.solution {
  background: #dcfce7;
  color: #166534;
}

.image-position {
  color: #6b7280;
  font-style: italic;
}

/* Modal styles */
.image-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.image-modal {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.modal-close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.modal-close-btn:hover {
  background: rgba(0, 0, 0, 0.9);
}

.modal-image {
  width: 100%;
  height: auto;
  display: block;
}

.modal-caption {
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
}

/* Styles pour les images inline dans l'énoncé */
.inline-image {
  display: inline-block;
  margin: 1rem 0;
  text-align: center;
}

.exercice-image.inline {
  max-width: 100%;
  max-height: 120px;
  width: auto;
  height: auto;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  cursor: pointer;
  transition: box-shadow 0.2s ease;
  object-fit: contain;
  margin: 0.5rem 0;
}

.exercice-image.inline:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.modal-image-type {
  font-weight: 600;
  color: #374151;
  font-size: 0.9rem;
}

.modal-position {
  color: #6b7280;
  font-size: 0.8rem;
}

/* Responsive */
@media (max-width: 768px) {
  .exercice-image {
    border-radius: 6px;
    max-height: 100px; /* Très petit sur mobile */
  }
  
  .exercice-image.inline {
    max-height: 80px; /* Très petit sur mobile */
  }
  
  .image-modal {
    max-width: 95vw;
    max-height: 95vh;
  }
  
  .modal-caption {
    padding: 0.75rem;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
}

@media (max-width: 480px) {
  .exercice-image {
    max-height: 250px; /* Encore plus petit sur très petit écran */
  }
}
</style>

