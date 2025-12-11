<template>
  <div class="exercice-card" :class="{ 
    'completed': current === 'acquired', 
    'acquired': current === 'acquired',
    'not-acquired': current === 'not_acquired'
  }">

    <!-- Header with title, difficulty, and tabs -->
    <div class="exercice-header">
      <div class="header-top">
        <div class="header-first-row">
          <div class="header-slot header-slot--left">
            <button
              class="flag-btn"
              type="button"
              @click="handleReport"
              :aria-pressed="hasReportedIssue"
              :class="{ reported: hasReportedIssue }"
              :title="hasReportedIssue ? 'Signalement envoyé' : 'Signaler une erreur dans cet exercice'"
              aria-label="Signaler une erreur dans cet exercice"
            >
              <span class="flag-icon" aria-hidden="true">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M6 3h10l-1.5 4L16 11H6v10H4V3z"/>
                  <path d="M6 13h9.5l-1.25 3L16 19H6z" opacity="0.2"/>
                </svg>
              </span>
            </button>
          </div>
          <h3 v-if="titre" class="exercice-title">{{ titre }}</h3>
          <div class="header-slot header-slot--right">
            <div v-if="bestScore !== null" class="score-badge" :class="getScoreClass(bestScore)">
              <span class="score-icon">🎯</span>
              <span class="score-text">{{ bestScore.toFixed(1) }}/20</span>
              <span v-if="attemptCount > 1" class="attempt-count" :title="`${attemptCount} tentatives`">
                ({{ attemptCount }})
              </span>
            </div>
            <div class="difficulty-indicator" v-if="difficulty">
              <span class="difficulty-stars">{{ diffStars[difficulty] || '★★' }}</span>
            </div>
            <button
              v-if="!readonly && current"
              class="reset-status-btn"
              @click="resetStatus"
              title="Réinitialiser le statut"
            >
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

      <!-- Navigation Tabs -->
      <div class="tabs-container">
        <!-- Tabs pour exercices multiples (Ex1, Ex2, Ex3, etc.) -->
        <template v-if="exercicesList && exercicesList.length > 0">
          <button 
            v-for="(ex, idx) in exercicesList" 
            :key="idx"
            class="tab-btn" 
            :class="{ 'active': activeTab === `ex${idx}` }"
            @click="activeTab = `ex${idx}`"
          >
            <span class="tab-icon">📝</span>
            <span class="tab-label">Ex {{ idx + 1 }}</span>
          </button>
        </template>
        
        <!-- Tabs standards (Énoncé/Étapes/Solution) -->
        <template v-else>
          <button 
            class="tab-btn" 
            :class="{ 'active': activeTab === 'problem' }"
            @click="activeTab = 'problem'"
          >
            <span class="tab-icon">📝</span>
            <span class="tab-label">Énoncé</span>
          </button>
          <button 
            class="tab-btn" 
            :class="{ 'active': activeTab === 'method' }"
            @click="activeTab = 'method'"
            v-if="etapes"
          >
            <span class="tab-icon">🔢</span>
            <span class="tab-label">Étapes</span>
          </button>
          <button 
            class="tab-btn" 
            :class="{ 'active': activeTab === 'solution' }"
            @click="activeTab = 'solution'"
            v-if="solution"
          >
            <span class="tab-icon">✅</span>
            <span class="tab-label">Solution</span>
          </button>
        </template>
      </div>
    </div>

    <!-- Tab Content -->
    <div class="tab-content" :style="tabContentStyles">
      <!-- Mode exercices multiples -->
      <template v-if="exercicesList && exercicesList.length > 0">
        <div 
          v-for="(ex, idx) in exercicesList" 
          :key="idx"
          v-show="activeTab === `ex${idx}`" 
          class="content-section problem-section"
        >
          <div class="content-wrapper">
            <div class="problem-content" v-html="renderInstructionWithImages(ex.question)" @click="handleImageClick"></div>
          </div>
        </div>
      </template>
      
      <!-- Mode standard (Énoncé/Étapes/Solution) -->
      <template v-else>
        <!-- Problem Tab -->
        <div v-show="activeTab === 'problem'" class="content-section problem-section">
          <div class="content-wrapper">
            <div class="problem-content" v-html="renderInstructionWithImages(instruction)" @click="handleImageClick"></div>
          </div>
        </div>

        <!-- Method Tab -->
        <div v-show="activeTab === 'method'" class="content-section steps-section" v-if="etapes">
          <div class="content-wrapper">
            <div class="steps-content" v-html="renderInstructionWithImages(etapes)" @click="handleImageClick"></div>
          </div>
        </div>

        <!-- Solution Tab -->
        <div v-show="activeTab === 'solution'" class="content-section answer-section" v-if="solution">
          <div class="content-wrapper">
            <div class="answer-content" v-html="renderInstructionWithImages(solution)" @click="handleImageClick"></div>
          </div>
        </div>
      </template>
    </div>

    <!-- Assessment Section (masqué pour les sujets d'examen avec exercices multiples) -->
    <div v-if="!readonly && !exercicesList" class="assessment-section">
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
    
    <!-- Section pour les sujets d'examen - bouton WhatsApp -->
    <div v-if="exercicesList && exercicesList.length > 0" class="exam-actions-section">
      <div class="exam-info">
        <p class="exam-description">📝 Réalisez tous les exercices sur votre copie</p>
        <p class="exam-hint">Envoyez votre travail pour recevoir votre note et la correction</p>
      </div>
      
      <div class="whatsapp-action">
        <button class="whatsapp-btn" @click="sendExamToWhatsApp">
          <svg class="whatsapp-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
          </svg>
          <span class="whatsapp-text">Envoyer par WhatsApp</span>
        </button>
      </div>
    </div>

    <!-- Report Modal -->
    <div v-if="showReportModal" class="report-modal-overlay" @click.self="closeReportModal">
      <div class="report-modal">
        <button class="report-close" type="button" @click="closeReportModal" aria-label="Fermer">
          ×
        </button>
        <div class="report-modal-header">
          <div class="report-icon">🚩</div>
          <div class="report-headings">
            <p class="report-kicker">Merci de nous aider à corriger</p>
            <h4>Signaler un problème</h4>
            <p class="report-subtitle">Décrivez le souci. Vous recevrez un email de confirmation immédiatement.</p>
          </div>
        </div>
        <div class="report-modal-body">
          <label class="report-label">
            Email de contact
            <input
              v-model="reportEmail"
              type="email"
              class="report-input"
              placeholder="vous@example.com"
            />
          </label>
          <div class="report-names">
            <label class="report-label">
              Prénom
              <input
                v-model="reportFirstName"
                type="text"
                class="report-input"
                placeholder="Votre prénom"
              />
            </label>
            <label class="report-label">
              Nom
              <input
                v-model="reportLastName"
                type="text"
                class="report-input"
                placeholder="Votre nom"
              />
            </label>
          </div>
          <label class="report-label">
            Problème rencontré
            <textarea
              v-model="reportDescription"
              rows="4"
              class="report-input"
              placeholder="Ex: L'énoncé contient une faute ou un résultat incorrect..."
            ></textarea>
          </label>
        </div>
        <div class="report-modal-footer">
          <div class="report-actions">
            <button class="report-btn ghost" type="button" @click="closeReportModal" :disabled="sendingReport">
              Annuler
            </button>
            <button class="report-btn primary" type="button" @click="submitReport" :disabled="sendingReport">
              <span v-if="sendingReport" class="report-spinner" aria-hidden="true"></span>
              {{ sendingReport ? 'Envoi...' : 'Envoyer le signalement' }}
            </button>
          </div>
          <div class="report-footnote">
            <span class="report-footnote-icon">✉️</span>
            Un email “votre message a été pris en compte” sera envoyé à l’adresse indiquée.
          </div>
        </div>
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
import { sendContactMessage } from '@/api/contact'
import { useUserStore } from '@/stores/user'
import { useToast } from '@/composables/useToast'

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
  },
  readonly: {
    type: Boolean,
    default: false
  },
  exercicesList: {
    type: Array,
    default: null
  },
  bestScore: {
    type: Number,
    default: null
  },
  attemptCount: {
    type: Number,
    default: 0
  }
})

// Emits
const emit = defineEmits(['status-changed', 'xp-gained'])

const { info: toastInfo, success: toastSuccess, error: toastError } = useToast()
const userStore = useUserStore()

// Reactive data
const showSolution = ref(false)
const exerciceImages = ref([])
const showImageModal = ref(false)
const selectedImage = ref(null)
const activeTab = ref(props.exercicesList && props.exercicesList.length > 0 ? 'ex0' : 'problem')
const hasReportedIssue = ref(false)
const showReportModal = ref(false)
const sendingReport = ref(false)
const reportDescription = ref('')
const reportEmail = ref('')
const reportFirstName = ref('')
const reportLastName = ref('')

// Computed
const diffStars = computed(() => ({
  easy: '★',
  medium: '★★',
  hard: '★★★'
}))

const tabContentStyles = computed(() => {
  const backgrounds = {
    problem: '#f5f7ff',
    method: '#f0f9ff',
    solution: '#f0fdf4'
  }
  // Si c'est un onglet ex0, ex1, ex2, etc., utiliser le background 'problem'
  const bg = activeTab.value.startsWith('ex') ? '#f5f7ff' : (backgrounds[activeTab.value] || '#f5f7ff')
  
  return {
    background: bg,
    borderBottomLeftRadius: '18px',
    borderBottomRightRadius: '18px'
  }
})

const emailPattern = /^[^@\s]+@[^@\s]+\.[^@\s]+$/

// Fonction pour déterminer la classe CSS selon la note
function getScoreClass(score) {
  if (score >= 16) return 'score-excellent'
  if (score >= 12) return 'score-good'
  if (score >= 10) return 'score-average'
  return 'score-needs-work'
}

function prefillReportFields() {
  if (!reportEmail.value && userStore.email) {
    reportEmail.value = userStore.email
  }
  if (!reportFirstName.value && userStore.firstName) {
    reportFirstName.value = userStore.firstName
  }
  if (!reportLastName.value && userStore.lastName) {
    reportLastName.value = userStore.lastName
  }
}

const handleReport = () => {
  if (hasReportedIssue.value) {
    toastInfo('Signalement déjà envoyé pour cet exercice.', 2800)
    return
  }
  prefillReportFields()
  showReportModal.value = true
}

const closeReportModal = () => {
  if (!sendingReport.value) {
    showReportModal.value = false
  }
}

async function submitReport() {
  if (sendingReport.value) return
  const description = (reportDescription.value || '').trim()
  const email = (reportEmail.value || '').trim()
  const first = (reportFirstName.value || userStore.firstName || 'Élève').trim() || 'Élève'
  const last = (reportLastName.value || userStore.lastName || 'OptiTAB').trim() || 'OptiTAB'

  if (!description || description.length < 10) {
    toastError('Décrivez le problème (10 caractères minimum).', 3600)
    return
  }
  if (!email || !emailPattern.test(email)) {
    toastError('Renseignez un email valide pour recevoir la confirmation.', 3600)
    return
  }

  const subject = `Signalement exercice ${props.eid ? `#${props.eid}` : ''} - ${props.titre || 'Exercice'}`
  const message = `${description}\n\n---\nExercice ID: ${props.eid || 'inconnu'}\nTitre: ${props.titre || '—'}`.trim()

  sendingReport.value = true
  try {
    await sendContactMessage({
      firstName: first,
      lastName: last,
      email,
      subject,
      message
    })
    hasReportedIssue.value = true
    showReportModal.value = false
    toastSuccess('Message pris en compte. Un email de confirmation vient de vous être envoyé.', 4200)
  } catch (error) {
    toastError('Impossible d\'envoyer le signalement pour le moment. Réessayez.', 4200)
  } finally {
    sendingReport.value = false
  }
}

// Methods

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

// Fonction pour envoyer l'examen par WhatsApp
function sendExamToWhatsApp() {
  // Construire le message WhatsApp
  const message = `🎓 *Demande de correction*\n\n` +
    `📝 Exercice: ${props.titre}\n` +
    `📚 Type: Sujet d'examen (${props.exercicesList?.length || 0} exercices)\n\n` +
    `Je souhaite envoyer ma copie pour correction.\n` +
    `Merci de me communiquer ma note et la correction détaillée.`
  
  // Encoder le message pour l'URL
  const encodedMessage = encodeURIComponent(message)
  
  // Numéro WhatsApp (à configurer selon vos besoins)
  // Format international sans le + : 33612345678 pour la France, 961XXXXXXXX pour le Liban
  const phoneNumber = '33612345678' // À REMPLACER par votre numéro
  
  // Créer l'URL WhatsApp
  const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodedMessage}`
  
  // Ouvrir WhatsApp dans un nouvel onglet
  window.open(whatsappUrl, '_blank')
  
  // Toast de confirmation
  toastInfo('Redirection vers WhatsApp...')
}

// Détecter la présence de marqueurs d'images [IMAGE_1], [IMAGE_2], ...
function hasImageMarkers() {
  // Si on a une liste d'exercices
  if (props.exercicesList && props.exercicesList.length > 0) {
    return props.exercicesList.some(ex => ex.question && /\[IMAGE_\d+\]/.test(ex.question))
  }
  // Sinon mode standard
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
    // Re-typeset après insertion des images dans le DOM via v-html
    nextTick(() => renderMath())
  } catch (error) {
    // Backend sans endpoint d'images → ignorer silencieusement
    exerciceImages.value = []
    nextTick(() => renderMath())
  }
}

// Watch for content changes to re-render MathJax
watch(() => [props.instruction, props.etapes, props.solution, props.exercicesList], renderMath, { immediate: true, deep: true })

// Watch for preview images changes
watch(() => props.previewImages, () => {
  if (props.eid && props.eid.toString().startsWith('preview-')) {
    exerciceImages.value = props.previewImages || []
    nextTick(() => renderMath())
  }
}, { immediate: true })

// Re-render MathJax when exercise images change (API or preview)
watch(exerciceImages, () => {
  nextTick(() => renderMath())
}, { deep: true })

// Lifecycle
onMounted(() => {
  // Charger les images uniquement si nécessaire
  if (hasImageMarkers() || (props.previewImages && props.previewImages.length > 0)) {
    loadExerciceImages()
  }
  renderMath()
  prefillReportFields()
})

watch(showReportModal, (val) => {
  if (val && typeof window !== 'undefined') {
    // S'assurer que le modal est visible en haut sur mobile
    requestAnimationFrame(() => window.scrollTo({ top: 0, behavior: 'auto' }))
  }
})

// Watcher sur activeTab pour forcer le rendu quand on change d'onglet
watch(activeTab, () => {
  nextTick(() => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      try {
        if (window.MathJax.typesetClear) {
          window.MathJax.typesetClear()
        }
        window.MathJax.typesetPromise()
      } catch (error) {
        // Ignorer les erreurs silencieusement
      }
    }
  })
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
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
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
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
  border-bottom: none;
  display: flex;
  flex-direction: column;
  height: auto;
}


.header-top {
  padding: 16px 28px;
}

.header-first-row {
  display: flex;
  align-items: center;
  width: 100%;
  gap: 12px;
  min-height: 40px;
}

.header-slot {
  display: flex;
  align-items: center;
}

.header-slot--left {
  width: 56px;
  justify-content: flex-start;
}

.header-slot--right {
  justify-content: flex-end;
  gap: 12px;
}

.flag-btn {
  background: #fff7ed;
  border: 1px solid #fdba74;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #c2410c;
  box-shadow: 0 1px 4px rgba(249, 115, 22, 0.25);
}

.flag-btn:hover {
  background: #ffedd5;
  border-color: #f97316;
  color: #9a3412;
}

.flag-btn.reported {
  background: #fef3c7;
  border-color: #f59e0b;
  color: #92400e;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.25);
}

.flag-icon svg {
  display: block;
}

.exercice-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  line-height: 1.3;
  text-align: center;
  flex: 1;
}

.header-controls {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.score-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  line-height: 1;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.score-badge:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.score-icon {
  font-size: 1rem;
}

.score-text {
  font-size: 0.95rem;
  letter-spacing: 0.5px;
}

.attempt-count {
  font-size: 0.75rem;
  opacity: 0.8;
  font-weight: 500;
}

.score-excellent {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.score-good {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.score-average {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.score-needs-work {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.difficulty-indicator {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 4px 10px;
  background: rgba(251, 146, 60, 0.1);
  border-radius: 8px;
  line-height: 1.3;
}

.difficulty-stars {
  font-size: 1rem;
  color: #f59e0b;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(245, 158, 11, 0.3);
  letter-spacing: 2px;
  line-height: 1.3;
  display: inline-block;
}

.reset-status-btn {
  background: #ffffff;
  border: 2px solid #e5e7eb;
  color: #64748b;
  cursor: pointer;
  padding: 6px;
  border-radius: 50%;
  transition: all 0.2s ease;
  flex-shrink: 0;
  width: 32px;
  height: 32px;
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

/* Tabs Container */
.tabs-container {
  display: flex;
  gap: 0;
  padding: 0;
  background: #f8fafc;
  border-top: none;
  width: 100%;
}

.tab-btn {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px 20px;
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: 0.95rem;
  font-weight: 600;
  color: #64748b;
  position: relative;
}

.tab-btn:hover {
  background: rgba(59, 130, 246, 0.05);
  color: #3b82f6;
}

.tab-btn.active {
  color: #3b82f6;
  border-bottom-color: #3b82f6;
  background: #ffffff;
}

.tab-icon {
  font-size: 1.2rem;
  transition: transform 0.3s ease;
}

.tab-btn.active .tab-icon {
  transform: scale(1.1);
}

.tab-label {
  font-weight: 600;
}

/* Tab Content */
.tab-content {
  min-height: 400px;
}

.content-section {
  padding: 32px 28px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.content-wrapper {
  max-width: 100%;
}

.problem-section,
.steps-section,
.answer-section {
  background: transparent;
}

.problem-content,
.steps-content,
.answer-content {
  font-size: 1rem;
  line-height: 1.7;
  color: #1f2937;
  text-align: left;
  overflow-wrap: break-word;
  word-break: break-word;
  overflow: visible;
  max-width: 100%;
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

/* Section pour les sujets d'examen */
.exam-actions-section {
  padding: 32px;
  background: #ffffff;
  border-top: 1px solid #e5e7eb;
}

.exam-info {
  text-align: center;
  margin-bottom: 24px;
}

.exam-description {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 6px 0;
}

.exam-hint {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
  line-height: 1.5;
  font-weight: 400;
}

/* Bouton WhatsApp */
.whatsapp-action {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.whatsapp-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 28px;
  background: #25D366;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(37, 211, 102, 0.25);
}

.whatsapp-btn:hover {
  background: #20BA5A;
  box-shadow: 0 4px 12px rgba(37, 211, 102, 0.35);
  transform: translateY(-1px);
}

.whatsapp-btn:active {
  transform: translateY(0);
}

.whatsapp-icon {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
}

.whatsapp-text {
  font-size: 1rem;
  font-weight: 600;
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

/* MathJax Styles - ajustés pour s'adapter sans scroll horizontal */
.exercice-card :deep(.mathjax-block) {
  max-width: 100%;
  overflow: visible;
  margin: 1rem 0;
}

.exercice-card :deep(.MathJax),
.exercice-card :deep(.MathJax svg),
.exercice-card :deep(.MathJax_SVG),
.exercice-card :deep(.MathJax_SVG_Display svg),
.exercice-card :deep(mjx-container),
.exercice-card :deep(mjx-container[display="true"]) {
  max-width: 100% !important;
  white-space: normal !important;
  overflow: visible !important;
}

.exercice-card :deep(.MathJax_Display),
.exercice-card :deep(.MathJax_SVG_Display) {
  max-width: 100% !important;
  white-space: normal !important;
  margin: 1.25rem 0;
  text-align: center !important;
}

/* Responsive Design */
@media (max-width: 768px) {
  .exercice-card {
    margin: 0 8px 24px 8px;
    border-radius: 16px;
  }

  .header-top {
    padding: 16px 20px;
    flex-wrap: wrap;
  }
  
  .exercice-title {
    font-size: 1.25rem;
  }

  .tabs-container {
    padding: 0;
    overflow-x: auto;
  }

  .tab-btn {
    padding: 14px 16px;
    font-size: 0.875rem;
    min-width: 100px;
  }

  .tab-icon {
    font-size: 1.1rem;
  }

  .content-section {
    padding: 24px 20px;
  }
  
  .assessment-section {
    padding: 24px;
  }
  
  .exam-actions-section {
    padding: 24px;
  }
  
  .whatsapp-btn {
    padding: 12px 24px;
  }
  
  .whatsapp-icon {
    width: 20px;
    height: 20px;
  }
  
  .whatsapp-text {
    font-size: 0.95rem;
  }
  
  .assessment-buttons {
    flex-direction: row;
    gap: 0.75rem;
    justify-content: center;
  }
  
  .assessment-btn {
    flex: 1;
    min-width: auto;
    max-width: none;
    padding: 0.85rem 1rem;
    font-size: 0.875rem;
    border-radius: 10px;
  }
  
  .btn-text {
    font-size: 0.85rem;
  }
  
  .btn-icon {
    font-size: 1.1rem;
  }
  
  /* MathJax responsive - garder la taille normale */
  .exercice-card :deep(.MathJax_Display) {
    margin: 1rem 0;
    max-width: none !important;
  }
  
  .exercice-card :deep(.MathJax) {
    max-width: none !important;
  }
  
  .exercice-card :deep(.MathJax_SVG) {
    max-width: none !important;
  }
  
  .exercice-card :deep(mjx-container) {
    max-width: none !important;
  }
}

@media (max-width: 480px) {
  .exercice-card {
    margin: 0 4px 20px 4px;
    border-radius: 12px;
  }

  .header-top {
    padding: 14px 16px;
  }
  
  .exercice-title {
    font-size: 1.125rem;
  }

  .header-controls {
    gap: 8px;
  }

  .score-badge {
    padding: 5px 10px;
    font-size: 0.85rem;
    gap: 5px;
  }

  .score-text {
    font-size: 0.85rem;
  }

  .attempt-count {
    display: none; /* Masquer le nombre de tentatives sur mobile */
  }

  .difficulty-indicator {
    padding: 4px 8px;
  }

  .reset-status-btn {
    width: 32px;
    height: 32px;
  }

  .tabs-container {
    padding: 0;
  }
  
  .assessment-buttons {
    gap: 0.5rem;
  }
  
  .assessment-btn {
    padding: 0.75rem 0.65rem;
    font-size: 0.8rem;
    gap: 0.5rem;
  }
  
  .btn-text {
    font-size: 0.8rem;
  }
  
  .btn-icon {
    font-size: 1rem;
  }

  .tab-btn {
    padding: 12px 12px;
    font-size: 0.8rem;
    flex-direction: column;
    gap: 4px;
  }

  .tab-icon {
    font-size: 1rem;
  }

  .tab-label {
    font-size: 0.75rem;
  }

  .content-section {
    padding: 20px 16px;
  }
  
  .assessment-section {
    padding: 20px;
  }
  
  .exam-actions-section {
    padding: 20px;
  }
  
  .whatsapp-btn {
    width: 100%;
    padding: 12px 20px;
    font-size: 0.9rem;
  }
  
  .whatsapp-icon {
    width: 20px;
    height: 20px;
  }
  
  .whatsapp-text {
    font-size: 0.9rem;
  }
  
  /* MathJax responsive - garder la taille normale */
  .exercice-card :deep(.MathJax_Display) {
    margin: 0.75rem 0;
    max-width: none !important;
  }
  
  .exercice-card :deep(.MathJax) {
    max-width: none !important;
  }
  
  .exercice-card :deep(.MathJax_SVG) {
    max-width: none !important;
  }
  
  .exercice-card :deep(mjx-container) {
    max-width: none !important;
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
.report-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 12010;
  padding: 1rem;
  backdrop-filter: blur(4px);
}

.report-modal {
  background: #ffffff;
  border-radius: 18px;
  max-width: 520px;
  width: 100%;
  box-shadow: 0 16px 48px rgba(15, 23, 42, 0.16);
  border: 1px solid #e2e8f0;
  padding: 22px;
  color: #0f172a;
  position: relative;
}

.report-modal-header {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  margin-bottom: 10px;
}

.report-icon {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background: linear-gradient(135deg, #fff7ed, #fffbeb);
  color: #c2410c;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  border: 1px solid #fed7aa;
  box-shadow: 0 8px 20px rgba(249, 115, 22, 0.22);
}

.report-headings {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.report-modal-header h4 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 800;
}

.report-kicker {
  margin: 0 0 4px;
  font-size: 0.8rem;
  letter-spacing: 0.02em;
  color: #0f172a;
  text-transform: uppercase;
  font-weight: 700;
}

.report-subtitle {
  margin: 4px 0 0;
  color: #475569;
  font-size: 0.95rem;
}

.report-modal-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 14px 0 10px;
}

.report-label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: #334155;
  font-weight: 700;
  font-size: 0.9rem;
}

.report-input {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 11px 12px;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  background: #f8fafc;
  color: #0f172a;
}

.report-input::placeholder {
  color: #94a3b8;
}

.report-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.18);
  background: #fff;
}

.report-names {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.report-modal-footer {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 12px;
}

.report-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.report-btn {
  border: none;
  border-radius: 12px;
  padding: 11px 15px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.95rem;
  min-width: 150px;
}

.report-btn.primary {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  color: #fff;
  box-shadow: 0 10px 30px rgba(37, 99, 235, 0.35);
}

.report-btn.primary:hover {
  filter: brightness(1.05);
  transform: translateY(-1px);
}

.report-btn.ghost {
  background: #f8fafc;
  color: #0f172a;
  border: 1px solid #e2e8f0;
}

.report-btn.ghost:hover {
  background: #e2e8f0;
}

.report-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.report-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #e5e7eb;
  border-top: 2px solid #fff;
  border-radius: 50%;
  display: inline-block;
  margin-right: 8px;
  animation: spin 1s linear infinite;
  vertical-align: middle;
}

.report-close {
  position: absolute;
  top: 12px;
  right: 12px;
  border: 1px solid #e2e8f0;
  background: #fff;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  color: #475569;
  cursor: pointer;
  font-size: 1rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.report-close:hover {
  background: #f8fafc;
  color: #0f172a;
}

.report-footnote {
  margin: 0;
  color: #475569;
  font-size: 0.86rem;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 10px 12px;
}

.report-footnote-icon {
  font-size: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.report-footnote {
  margin: 10px 0 0;
  color: #475569;
  font-size: 0.85rem;
  text-align: center;
}

@media (max-width: 540px) {
  .report-modal-overlay {
    align-items: flex-start;
    padding: 0.75rem;
  }
  .report-modal {
    padding: 16px;
    width: 100%;
    max-width: none;
    border-radius: 12px;
    margin-top: calc(env(safe-area-inset-top, 12px));
  }
  .report-names {
    grid-template-columns: 1fr;
  }
  .report-actions {
    justify-content: flex-end;
    flex-wrap: wrap;
  }
}

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
  display: flex;
  width: 100%;
  justify-content: center;
  align-items: center;
  margin: 1rem 0;
  text-align: center;
}

/* Centrage des anciennes images insérées directement dans le texte */
.problem-content :deep(img),
.steps-content :deep(img),
.answer-content :deep(img) {
  display: block;
  margin: 0.75rem auto; /* centre horizontalement */
  max-width: 100%;
  height: auto;
}

/* Centrer les images dans les conteneurs legacy */
.exercice-image-container {
  align-items: center; /* centre les images dans les anciens exercices */
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
