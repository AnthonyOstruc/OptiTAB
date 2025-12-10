<template>
  <div>
    <FormatHelp :format-template="QUIZ_FORMAT_TEMPLATE">
      <template #notes>
        <div class="format-examples">
          <h4>Format énoncé unique</h4>
          <ul>
            <li>Séparez chaque énoncé par une ligne <code>===</code></li>
            <li>Champs : <code>Titre</code>, <code>Difficulté</code>, <code>Images</code>, <code>Énoncé</code></li>
            <li>Chaque bloc crée un quiz avec une seule question “réponse libre” basée sur l'énoncé.</li>
            <li>Images : <code>Images: nom1.jpg, nom2.png</code> et marqueurs <code>[IMAGE_1]</code>, <code>[IMAGE_2]</code> dans le texte si besoin.</li>
          </ul>
        </div>
      </template>
    </FormatHelp>

    <div class="bulk-form">
      <input v-model="notionFilter" type="text" placeholder="Filtrer les notions..." class="filter-input" />
      <select v-model="selectedNotion" required>
        <option disabled value="">Choisir notion</option>
        <option v-for="n in filteredNotions" :key="n.id" :value="n.id">
          {{ (n.nom || n.titre) }}
        </option>
      </select>

      <!-- Upload d'images -->
      <div class="images-upload-section">
        <h4>📁 Images pour les quiz</h4>
        <p class="upload-help">Uploadez les images qui seront référencées dans vos quiz :</p>
        <input 
          type="file" 
          ref="imagesInput" 
          @change="handleImagesSelect" 
          accept="image/*"
          multiple
          class="images-file-input"
        />
        <div v-if="selectedImages.length > 0" class="selected-images">
          <h5>Images sélectionnées :</h5>
          <div v-for="(img, index) in selectedImages" :key="index" class="selected-image-item">
            <img :src="getImagePreview(img)" :alt="img.name" class="image-preview" />
            <span class="image-name">{{ img.name }}</span>
            <button type="button" class="btn-remove" @click="removeSelectedImage(index)">×</button>
          </div>
        </div>
      </div>

      <textarea 
        v-model="rawInput" 
        placeholder="Collez ici vos énoncés (séparés par ===)"
        class="quiz-textarea"
      ></textarea>
      
      <div class="btn-group">
        <button 
          class="btn-preview" 
          @click="handlePreview" 
          :disabled="!rawInput.trim()"
        >
          Prévisualiser
        </button>
        <button 
          class="btn-create" 
          @click="handleCreate" 
          :disabled="!selectedNotion || !previewList.length"
        >
          Créer {{ previewList.length || '' }} énoncés
        </button>
        <button 
          class="btn-clear" 
          @click="clearAll"
          v-if="rawInput || previewList.length"
        >
          Vider
        </button>
      </div>
    </div>

    <!-- Messages -->
    <div v-if="successMsg" class="success-msg">✅ {{ successMsg }}</div>
    <div v-if="errorMsg" class="error-msg">❌ {{ errorMsg }}</div>

    <!-- Aperçu des quiz -->
    <div v-if="previewList.length" class="preview-section">
      <div class="preview-header">
        <h3 class="preview-title">
          🎯 Aperçu ({{ previewList.length }} quiz • {{ getTotalQuestions() }} questions total)
        </h3>
        <button 
          class="btn-toggle-explanations"
          @click="showExplanations = !showExplanations"
        >
          {{ showExplanations ? 'Masquer' : 'Voir' }} explications
        </button>
      </div>
      
      <div class="quiz-grid">
        <div v-for="(quiz, idx) in previewList" :key="idx" class="quiz-preview-card">
          <div class="quiz-header">
            <h4 class="quiz-title">{{ quiz.titre }}</h4>
            <span class="difficulty-badge" :class="quiz.difficulty">
              {{ getDifficultyLabel(quiz.difficulty) }}
            </span>
          </div>
          
          <p class="quiz-instructions">{{ quiz.instruction }}</p>
          
          <div class="questions-summary">
            <span class="questions-count">📝 {{ quiz.questions.length }} questions</span>
            <span v-if="quiz.questions.some(q => q.explanation)" class="explanations-count">💡 {{ quiz.questions.filter(q => q.explanation).length }} explications</span>
            <span v-if="quiz.image" class="images-count">🖼️ {{ quiz.image.split(',').length }} images</span>
          </div>

          <!-- Aperçu des questions avec style quiz réel -->
          <div class="questions-preview">
            <div v-for="(q, qIdx) in quiz.questions" :key="qIdx" class="question-preview">
              <h4 class="question-title-preview">Q{{ qIdx + 1 }}: <span v-html="renderWithImages(q.question, quiz.image)"></span></h4>
              
              <div class="options-container-preview">
                <div v-for="(opt, oIdx) in q.options" :key="oIdx" 
                      class="option-card-preview" 
                      :class="{ correct: oIdx === q.correct_answer }">
                  <div class="option-letter-preview">{{ String.fromCharCode(65 + oIdx) }}</div>
                  <span class="option-text-preview" v-html="renderWithImages(opt, quiz.image)"></span>
                </div>
              </div>
              
              <div v-if="showExplanations && q.explanation" class="explanation-preview">
                <h5 class="explanation-title-preview">Explication :</h5>
                <p class="explanation-text-preview" v-html="renderWithImages(q.explanation, quiz.image)"></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onActivated, nextTick, watch, computed } from 'vue'
import { getNotions } from '@/api'
import { createQuiz, createQuizImage, updateQuiz } from '@/api/quiz'
import FormatHelp from '@/components/admin/FormatHelp.vue'

const chapitres = ref([])
const notions = ref([])
const notionFilter = ref('')
const selectedNotion = ref('')
const rawInput = ref('')
const successMsg = ref('')
const errorMsg = ref('')
const previewList = ref([])
const showExplanations = ref(true)
const selectedImages = ref([])
const imagesInput = ref(null)

// ============================================================================
// CONSTANTES DU FORMAT
// ============================================================================

const QUIZ_FORMAT_TEMPLATE = `=== [Titre de l'énoncé]
Difficulté: [easy/medium/hard]
Images: [nom1.jpg,nom2.png] (optionnel)

Énoncé:
[Votre texte ici]

[IMAGE_1]

[suite de l'énoncé]

===`

// ============================================================================
// CONSTANTES POUR IMAGES
// ============================================================================

const SUPPORTED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
const MAX_IMAGE_SIZE = 10 * 1024 * 1024 // 10MB
const IMAGE_MARKER_REGEX = /\[IMAGE_(\d+)\]/g

// ============================================================================
// CLASSES UTILITAIRES
// ============================================================================

/**
 * Classe pour gérer les images de quiz
 */
class ImageManager {
  constructor() {
    this.images = new Map() // filename -> File
    this.imageTypes = new Map() // filename -> type
  }

  /**
   * Ajoute une image à la collection
   */
  addImage(file) {
    if (!this.validateImage(file)) {
      throw new Error(`Image invalide: ${file.name}`)
    }
    this.images.set(file.name, file)
  }

  /**
   * Supprime une image de la collection
   */
  removeImage(filename) {
    this.images.delete(filename)
    this.imageTypes.delete(filename)
  }

  /**
   * Valide une image
   */
  validateImage(file) {
    if (!SUPPORTED_IMAGE_TYPES.includes(file.type)) {
      return false
    }
    if (file.size > MAX_IMAGE_SIZE) {
      return false
    }
    return true
  }

  /**
   * Récupère une image par nom
   */
  getImage(filename) {
    // Recherche exacte
    let file = this.images.get(filename)
    if (file) return file

    // Recherche insensible à la casse
    for (const [name, imgFile] of this.images) {
      if (name.toLowerCase() === filename.toLowerCase()) {
        return imgFile
      }
    }

    return null
  }

  /**
   * Parse le string d'images pour extraire les noms de fichiers
   */
  parseImageString(imageString) {
    if (!imageString) return []
    return imageString.split(',').map(name => name.trim()).filter(Boolean)
  }

  /**
   * Valide que toutes les images référencées sont disponibles
   */
  validateImageReferences(imageString) {
    const imageNames = this.parseImageString(imageString)
    const missing = []
    
    for (const imageName of imageNames) {
      if (!this.getImage(imageName)) {
        missing.push(imageName)
      }
    }
    
    return {
      valid: missing.length === 0,
      missing
    }
  }

  /**
   * Détermine le type d'image basé sur le contexte du quiz
   */
  determineImageType(quizData, position) {
    // Par défaut, les images sont pour les questions
    return 'question'
  }
}

/**
 * Classe pour créer les quiz avec leurs images
 */
class QuizCreator {
  constructor(imageManager) {
    this.imageManager = imageManager
  }

  /**
   * Crée un quiz avec ses images
   */
  async createQuizWithImages(quizData) {
    try {
      // 1. Créer le quiz d'abord
      const quizRes = await createQuiz({
        notion: Number(quizData.notion),
        titre: quizData.titre,
        contenu: quizData.instruction || quizData.titre || 'Quiz',
        difficulty: quizData.difficulty || 'medium',
        questions_data: Array.isArray(quizData.questions) ? quizData.questions : [],
      })

      const quizId = (quizRes && quizRes.data && quizRes.data.id) ? quizRes.data.id : (quizRes && quizRes.id ? quizRes.id : null)

      // 2. Ajouter les images si présentes
      if (quizData.image) {
        await this.addImagesToQuiz(quizId, quizData)
      }

      return { success: true, quizId }
    } catch (error) {
      console.error('Erreur lors de la création du quiz:', error, error?.response?.data)
      return { 
        success: false, 
        error: error.response?.data ? JSON.stringify(error.response.data) : (error.message || 'Erreur inconnue')
      }
    }
  }

  /**
   * Ajoute les images à un quiz et met à jour les questions avec les URLs réelles
   */
  async addImagesToQuiz(quizId, quizData) {
    const imageNames = this.imageManager.parseImageString(quizData.image)
    const errors = []
    const imageUrls = new Map() // position -> URL

    for (let i = 0; i < imageNames.length; i++) {
      const imageName = imageNames[i]
      const imageFile = this.imageManager.getImage(imageName)

      if (imageFile) {
        try {
          const imageType = this.imageManager.determineImageType(quizData, i + 1)
          
          const response = await createQuizImage({
            quiz: quizId,
            image: imageFile,
            image_type: imageType,
            position: i + 1
          })
          
          // Stocker l'URL de l'image uploadée
          if (response?.data?.image) {
            let returned = response.data.image
            // Normaliser l'URL renvoyée par l'API (chemin relatif -> URL absolue)
            if (!/^https?:\/\//i.test(returned)) {
              const base = (import.meta.env?.VITE_API_BASE_URL) || 'http://127.0.0.1:8000'
              if (returned.startsWith('/')) {
                returned = base + returned
              } else {
                // Probablement un chemin type "quiz_images/xxx.png" => préfixer /media/
                returned = base + '/media/' + returned
              }
            }
            imageUrls.set(i + 1, returned)
          }
        } catch (imageError) {
          console.error(`Erreur lors de l'ajout de l'image ${imageName}:`, imageError)
          errors.push(`Image ${imageName} non ajoutée`)
        }
      } else {
        errors.push(`Image ${imageName} non trouvée`)
      }
    }

    // Mettre à jour les questions du quiz avec les URLs réelles des images
    if (imageUrls.size > 0) {
      try {
        await this.updateQuizQuestionsWithImageUrls(quizId, quizData, imageUrls)
      } catch (error) {
        console.error('Erreur lors de la mise à jour des questions avec les URLs d\'images:', error)
        errors.push('Erreur lors de la mise à jour des URLs d\'images dans les questions')
      }
    }

    return errors
  }

  /**
   * Met à jour les questions du quiz en remplaçant les marqueurs par les URLs réelles
   */
  async updateQuizQuestionsWithImageUrls(quizId, quizData, imageUrls) {
    const updatedQuestions = quizData.questions.map(question => {
      const updatedQuestion = { ...question }
      
      // Remplacer dans la question
      if (updatedQuestion.question) {
        updatedQuestion.question = this.replaceImageMarkersWithUrls(updatedQuestion.question, imageUrls)
      }
      
      // Remplacer dans les options
      if (updatedQuestion.options) {
        updatedQuestion.options = updatedQuestion.options.map(option => 
          this.replaceImageMarkersWithUrls(option, imageUrls)
        )
      }
      
      // Remplacer dans l'explication
      if (updatedQuestion.explanation) {
        updatedQuestion.explanation = this.replaceImageMarkersWithUrls(updatedQuestion.explanation, imageUrls)
      }
      
      return updatedQuestion
    })

    // Mettre à jour le quiz avec les nouvelles questions
    await updateQuiz(quizId, {
      questions_data: updatedQuestions
    })
  }

  /**
   * Remplace les marqueurs [IMAGE_X] par les URLs réelles des images
   */
  replaceImageMarkersWithUrls(text, imageUrls) {
    if (!text) return text
    
    return text.replace(/\[IMAGE_(\d+)\]/g, (match, imageNumber) => {
      const position = parseInt(imageNumber)
      const imageUrl = imageUrls.get(position)
      
      if (imageUrl) {
        return `<img src="${imageUrl}" alt="Image ${position}" style="max-width: 300px; height: auto; border-radius: 6px; margin: 8px 0; border: 1px solid #e5e7eb;" />`
      }
      
      return match // Garder le marqueur si l'URL n'est pas trouvée
    })
  }
}

// ============================================================================
// INSTANCES DES CLASSES
// ============================================================================

const imageManager = new ImageManager()
const quizCreator = new QuizCreator(imageManager)

async function load() {
  try {
    const nt = await getNotions()
    notions.value = Array.isArray(nt) ? nt : (nt?.data || [])
  } catch (e) {
    console.error('Erreur chargement:', e)
  }
}

// Chapitres filtrés (par texte seulement)
const filteredNotions = computed(() => {
  if (!notionFilter.value) {
    return notions.value
  }
  const filter = notionFilter.value.toLowerCase()
  return notions.value.filter(notion =>
    (notion.nom || notion.titre || '').toLowerCase().includes(filter)
  )
})

onMounted(load)

// Hook onActivated - force le rendu MathJax pour l'aperçu
onActivated(() => {
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
    setTimeout(() => {
      if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise()
      }
    }, 100)
  })
})

function getNotionName(id) {
  const n = notions.value.find((n) => n.id === id)
  return n ? n.nom : `Notion ${id}`
}

// ==========================
// Contexte Chapitre (matière, thème, pays, niveau)
// ==========================
function getNotionById(id) {
  return notions.value.find(x => String(x.id) === String(id))
}

function chapterContext(chapitre) {
  if (!chapitre) return null
  const notion = getNotionById(chapitre.notion)
  if (!notion) return { themeNom: '', matiereNom: '', paysNom: '', niveauNom: '' }
  const matiereNom = notion.matiere_nom || (notion.contexte_detail && notion.contexte_detail.matiere_nom) || ''
  const themeNom = notion.theme_nom || ''
  const paysNom = notion.contexte_detail && notion.contexte_detail.pays ? notion.contexte_detail.pays.nom : ''
  const niveauNom = notion.contexte_detail && notion.contexte_detail.niveau ? notion.contexte_detail.niveau.nom : ''
  return { matiereNom, themeNom, paysNom, niveauNom }
}

const currentContext = computed(() => {
  const n = notions.value.find(x => String(x.id) === String(selectedNotion.value))
  return n ? {
    matiereNom: n.matiere_nom || (n.contexte_detail && n.contexte_detail.matiere_nom) || '',
    themeNom: n.theme_nom || '',
    paysNom: n.contexte_detail && n.contexte_detail.pays ? n.contexte_detail.pays.nom : '',
    niveauNom: n.contexte_detail && n.contexte_detail.niveau ? n.contexte_detail.niveau.nom : ''
  } : null
})

function formatNotionOption(n) {
  const ctx = currentContext.value
  const parts = [
    n.nom || n.titre,
    ctx && ctx.matiereNom ? `— ${ctx.matiereNom}` : '',
    ctx && (ctx.paysNom || ctx.niveauNom) ? `— ${[ctx.paysNom, ctx.niveauNom].filter(Boolean).join(' · ')}` : ''
  ].filter(Boolean)
  return parts.join(' ')
}

function getDifficultyLabel(difficulty) {
  const labels = {
    'easy': '⭐ Facile',
    'medium': '⭐⭐ Moyen', 
    'hard': '⭐⭐⭐ Difficile'
  }
  return labels[difficulty] || difficulty
}

function getTotalQuestions() {
  return previewList.value.reduce((total, quiz) => total + quiz.questions.length, 0)
}

// Normalise les retours à la ligne saisis par l'utilisateur
// - "\\" (LaTeX fin de ligne) suivi d'un espace/fin → saut de ligne
// - "\n" littéral → saut de ligne
function normalizeLineBreaks(text) {
  if (!text) return text
  let t = String(text)
  // LaTeX line break: \\ en fin de morceau
  t = t.replace(/\\(\s|$)/g, '\n')
  // Séquence littérale \n
  t = t.replace(/\\n/g, '\n')
  // Alias de retours à la ligne saisis par l'admin:
  // - "//" seul entre espaces → saut de ligne
  t = t.replace(/(^|\s)\/{2}(?=\s|$)/g, '$1\n')
  // - "/n" seul entre espaces → saut de ligne
  t = t.replace(/(^|\s)\/n(?=\s|$)/g, '$1\n')
  // - "$//$" → saut de ligne
  t = t.replace(/(^|\s)\$\/{2}\$(?=\s|$)/g, '$1\n')
  return t
}

// Fonction pour rendre les formules LaTeX avec MathJax
const renderMath = () => {
  nextTick(() => {
    if (window.MathJax) {
      window.MathJax.typesetPromise()
    }
  })
}

// Watcher pour rendre les formules quand la prévisualisation change
watch(previewList, () => {
  if (previewList.value.length > 0) {
    renderMath()
  }
}, { deep: true })

// Watcher pour rendre les formules quand on affiche/masque les explications
watch(showExplanations, () => {
  if (previewList.value.length > 0) {
    nextTick(() => {
      setTimeout(() => renderMath(), 100)  // Délai pour s'assurer que le DOM est mis à jour
    })
  }
})

function parseInput() {
  const text = rawInput.value.trim()
  if (!text) return []

  return parseBlockFormat(text)
}

function parseBlockFormat(text) {
  const blocks = text.split(/^={3,}\s*$/m).map(b => b.trim()).filter(Boolean)
  
  return blocks.map((block) => {
    let titre = ''
    let enonceLines = []
    let difficulty = 'medium'
    let image = ''
    let inEnonce = false

    const lines = block.split('\n')
    
    for (const line of lines) {
      const trimmed = line.trim()
      if (!trimmed) continue

      if (trimmed.startsWith('Titre:')) {
        titre = trimmed.slice(6).trim()
        continue
      }
      if (trimmed.toLowerCase().startsWith('difficult')) {
        const parts = trimmed.split(':')
        difficulty = (parts[1] || difficulty).trim().toLowerCase()
        continue
      }
      if (trimmed.startsWith('Images:')) {
        image = trimmed.slice(7).trim()
        continue
      }
      if (trimmed.toLowerCase().startsWith('énoncé:') || trimmed.toLowerCase().startsWith('enonce:')) {
        const rest = trimmed.split(':').slice(1).join(':').trim()
        if (rest) enonceLines.push(rest)
        inEnonce = true
        continue
      }
      if (titre === '') {
        titre = trimmed
        continue
      }
      if (inEnonce) {
        enonceLines.push(line)
      } else {
        enonceLines.push(line)
      }
    }

    const enonce = normalizeLineBreaks(enonceLines.join('\n').trim())
    const questionText = enonce || titre || 'Énoncé'
    const question = fixQuestion({
      question: questionText,
      options: ['Réponse libre'],
      correct_answer: 0,
      explanation: ''
    })

    return {
      titre: titre || 'Énoncé',
      instruction: enonce || 'Énoncé',
      difficulty,
      image,
      questions: [question],
      chapitre: undefined,
      notion: Number(selectedNotion.value)
    }
  })
}

function fixQuestion(question) {
  const q = { ...question }
  if (!Array.isArray(q.options) || q.options.length === 0) {
    q.options = ['Réponse à rédiger']
    q.correct_answer = 0
  }
  if (typeof q.correct_answer !== 'number' || Number.isNaN(q.correct_answer)) {
    q.correct_answer = 0
  }
  return q
}

async function handleCreate() {
  errorMsg.value = ''
  successMsg.value = ''
  
  try {
    const quizData = parseInput().filter(q => q.titre && q.questions.length > 0)
    
    if (quizData.length === 0) {
      errorMsg.value = 'Aucun quiz valide trouvé. Vérifiez le format.'
      return
    }

    let created = 0
    let totalQuestions = 0
    let errors = []
    
    for (const quiz of quizData) {
      // Valider les références d'images si présentes
      if (quiz.image) {
        const imageValidation = imageManager.validateImageReferences(quiz.image)
        if (!imageValidation.valid) {
          errors.push(`Images manquantes pour "${quiz.titre}": ${imageValidation.missing.join(', ')}`)
          continue
        }
      }

      // Créer le quiz avec ses images
      const result = await quizCreator.createQuizWithImages(quiz)
      
      if (result.success) {
        created++
        totalQuestions += Array.isArray(quiz.questions) ? quiz.questions.length : 0
      } else {
        errors.push(`Erreur pour "${quiz.titre}": ${result.error}`)
      }
    }
    
    let message = `${created} quiz créés avec ${totalQuestions} questions au total !`
    if (errors.length > 0) {
      message += `\n\nErreurs : ${errors.join(' | ')}`
      errorMsg.value = `Certains quiz n'ont pas pu être créés : ${errors.join(' | ')}`
    }
    
    // Sauvegarder le chapitre actuel avant de nettoyer le formulaire
    const currentNotion = selectedNotion.value

    successMsg.value = message
    rawInput.value = ''
    previewList.value = []

    // Remettre le chapitre sélectionné pour permettre d'ajouter d'autres quiz dans le même chapitre
    selectedNotion.value = currentNotion
    
  } catch (e) {
    console.error('Erreur création:', e)
    const apiErr = e?.response?.data
    if (apiErr) {
      try {
        errorMsg.value = typeof apiErr === 'string' ? apiErr : JSON.stringify(apiErr)
      } catch (_) {
        errorMsg.value = 'Erreur lors de la création des quiz.'
      }
    } else {
      errorMsg.value = 'Erreur lors de la création des quiz.'
    }
  }
}

function handlePreview() {
  errorMsg.value = ''
  successMsg.value = ''
  
  try {
    const parsed = parseInput().filter(q => q.titre && q.questions.length > 0)
    previewList.value = parsed
    
    // Debug: afficher les explications parsées
    console.log('Quiz parsés:', parsed.map(quiz => ({
      titre: quiz.titre,
      questions: quiz.questions.map(q => ({
        question: q.question.substring(0, 50) + '...',
        hasExplanation: !!q.explanation,
        explanation: q.explanation,
        explanationLength: q.explanation ? q.explanation.length : 0
      }))
    })))
    
    // Debug spécial pour les explications LaTeX
    parsed.forEach(quiz => {
      quiz.questions.forEach((q, idx) => {
        if (q.explanation) {
          console.log(`Explication Q${idx+1}:`, q.explanation)
        }
      })
    })
    
    if (parsed.length === 0) {
      errorMsg.value = 'Aucun quiz valide trouvé. Vérifiez le format.'
    } else {
      // Rendre les formules LaTeX après la prévisualisation
      nextTick(() => renderMath())
    }
  } catch (e) {
    errorMsg.value = 'Erreur lors du parsing. Vérifiez le format.'
  }
}

function clearAll() {
  rawInput.value = ''
  previewList.value = []
  successMsg.value = ''
  errorMsg.value = ''
}

// ============================================================================
// FONCTIONS POUR GESTION DES IMAGES
// ============================================================================

function handleImagesSelect(event) {
  const files = Array.from(event.target.files)

  files.forEach(file => {
    try {
      imageManager.addImage(file)
    } catch (error) {
      errorMsg.value = error.message
    }
  })

  selectedImages.value = Array.from(imageManager.images.values())
}

function removeSelectedImage(index) {
  const file = selectedImages.value[index]
  imageManager.removeImage(file.name)
  selectedImages.value.splice(index, 1)
  
  if (imagesInput.value) {
    imagesInput.value.value = ''
  }
}

function getImagePreview(file) {
  return URL.createObjectURL(file)
}

/**
 * Remplace les marqueurs [IMAGE_X] par les vraies images dans un texte
 */
function renderWithImages(text, imageString) {
  if (!text) return text
  
  let processed = normalizeLineBreaks(text)
  const imageNames = imageManager.parseImageString(imageString)
  
  // Debug: afficher les informations d'images
  console.log('renderWithImages - text:', processed)
  console.log('renderWithImages - imageString:', imageString)
  console.log('renderWithImages - imageNames:', imageNames)
  console.log('renderWithImages - available images:', Array.from(imageManager.images.keys()))
  
  processed = processed.replace(/\[IMAGE_(\d+)\]/g, (match, imageNumber) => {
    const imageIndex = parseInt(imageNumber) - 1
    
    console.log(`renderWithImages - processing ${match}: imageNumber=${imageNumber}, imageIndex=${imageIndex}`)
    
    if (imageIndex >= 0 && imageIndex < imageNames.length) {
      const imageName = imageNames[imageIndex]
      console.log(`renderWithImages - imageName: ${imageName}`)
      
      const imageFile = imageManager.getImage(imageName)
      console.log(`renderWithImages - imageFile found:`, !!imageFile)
      
      if (imageFile) {
        const imageUrl = URL.createObjectURL(imageFile)
        console.log(`renderWithImages - created URL for ${imageName}:`, imageUrl)
        return `<img src="${imageUrl}" alt="${imageName}" class="quiz-preview-image" style="max-width: 300px; height: auto; border-radius: 6px; margin: 8px 0; border: 1px solid #e5e7eb; display: block;" />`
      }
    }
    
    console.log(`renderWithImages - image not found for ${match}, imageIndex=${imageIndex}, imageNames.length=${imageNames.length}`)
    
    // Si l'image n'est pas trouvée, afficher un placeholder
    return `<span class="image-placeholder" style="background: #fee2e2; color: #dc2626; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; border: 1px dashed #dc2626;">🖼️ Image ${imageNumber} manquante</span>`
  })

  // Forcer le style d'affichage LaTeX: ajouter \\displaystyle dans $...$ et $$...$$ si absent
  function enforceDisplayStyleInMath(t) {
    if (!t) return t
    // D'abord traiter $$...$$ (bloc)
    t = t.replace(/\$\$([\s\S]*?)\$\$/g, (match, inner) => {
      const trimmed = String(inner).trim()
      if (trimmed.startsWith('\\displaystyle')) return match
      return `$$\\displaystyle ${inner}$$`
    })
    // Puis traiter $...$ (inline)
    t = t.replace(/\$([^$\n]+)\$/g, (match, inner) => {
      const trimmed = String(inner).trim()
      if (trimmed.startsWith('\\displaystyle')) return match
      return `$\\displaystyle ${inner}$`
    })
    return t
  }

  processed = enforceDisplayStyleInMath(processed)

  // Marqueurs d'espace vertical réduit: [SM] (~6px) et [XS] (~3px)
  processed = processed.replace(/\[SM\]/g, '<span class="spacer-sm"></span>')
  processed = processed.replace(/\[XS\]/g, '<span class="spacer-xs"></span>')

  // Convertir les sauts de ligne en <br/> pour l'affichage HTML
  processed = processed.replace(/\n/g, '<br/>')

  return processed
}
</script>

<style src="@/styles/admin-common.css"></style>

<style scoped>
/* Styles spécifiques à AdminQuizPlus */

.format-examples {
  margin-top: 1rem;
}

.format-examples h4 {
  color: #374151;
  margin: 1rem 0 0.5rem 0;
}

.format-examples pre {
  background: #1f2937 !important;
  color: #f9fafb !important;
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 0.85rem;
  line-height: 1.4;
}

.format-examples pre code {
  background: transparent !important;
  color: #f9fafb !important;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
}


.quiz-textarea {
  height: 200px;
  padding: 12px;
  border: 2px solid #d1d5db;
  border-radius: 6px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 0.9rem;
  line-height: 1.4;
  resize: vertical;
}

.btn-preview, .btn-create, .btn-clear {
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-preview {
  background: #6b7280;
  color: white;
}

.btn-preview:hover:not(:disabled) {
  background: #4b5563;
}

.btn-create {
  background: #3b82f6;
  color: white;
}

.btn-create:hover:not(:disabled) {
  background: #2563eb;
}

.btn-clear {
  background: #ef4444;
  color: white;
}

.btn-clear:hover {
  background: #dc2626;
}

.btn-preview:disabled, .btn-create:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.preview-title {
  font-size: 1.4rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.btn-toggle-explanations {
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 6px;
  padding: 8px 16px;
  font-size: 0.9rem;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-toggle-explanations:hover {
  background: #e0e7ff;
  border-color: #3b82f6;
  color: #1d4ed8;
}

.quiz-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.quiz-preview-card {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.2s;
  width: 100%;
}

.quiz-preview-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.quiz-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.quiz-instructions {
  color: #6b7280;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.questions-summary {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.questions-count {
  background: #eff6ff;
  color: #1d4ed8;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.explanations-count {
  background: #fef3c7;
  color: #92400e;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.images-count {
  background: #dbeafe;
  color: #1e40af;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.questions-preview {
  margin-top: 1rem;
  border-top: 1px solid #e5e7eb;
  padding-top: 1rem;
}

/* Styles pour l'aperçu des questions - copiés du quiz réel */
.question-preview {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.question-title-preview {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 1.5rem 0;
  line-height: 1.4;
}

.options-container-preview {
  display: grid;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.option-card-preview {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.75rem;
  transition: all 0.2s ease;
  background: white;
}

.option-card-preview.correct {
  border-color: #10b981;
  background: #d1fae5;
}

.option-card-preview.correct .option-text-preview {
  color: #065f46;
  font-weight: 600;
}

.option-letter-preview {
  width: 1.75rem;
  height: 1.75rem;
  border-radius: 50%;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #374151;
  flex-shrink: 0;
  font-size: 0.875rem;
}

.option-card-preview.correct .option-letter-preview {
  background: #10b981;
  color: white;
}

.option-text-preview {
  flex: 1;
  font-size: 0.9rem;
  line-height: 1.4;
  color: #374151;
}

.explanation-preview {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 0.75rem;
  border-left: 4px solid #3b82f6;
}

.explanation-title-preview {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.explanation-text-preview {
  color: #475569;
  line-height: 1.5;
  margin: 0;
  font-size: 0.9rem;
}

.quiz-preview-image {
  max-width: 300px !important;
  height: auto !important;
  border-radius: 6px !important;
  margin: 8px 0 !important;
  border: 1px solid #e5e7eb !important;
  display: block !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.image-placeholder {
  background: #fee2e2 !important;
  color: #dc2626 !important;
  padding: 4px 8px !important;
  border-radius: 4px !important;
  font-size: 0.8rem !important;
  border: 1px dashed #dc2626 !important;
  display: inline-block;
  margin: 4px 0;
}

.spacer-sm {
  display: block;
  height: 6px; /* petit espace vertical */
}

.spacer-xs {
  display: block;
  height: 3px; /* très petit espace vertical (~ moitié de SM) */
}

.option-text-preview .quiz-preview-image {
  max-width: 150px !important;
  margin: 4px 0 !important;
}

@media (max-width: 768px) {
  .quiz-grid {
    flex-direction: column;
  }
  
  .question-preview {
    padding: 1rem;
  }
  
  .question-title-preview {
    font-size: 1rem;
  }
  
  .option-card-preview {
    padding: 0.5rem;
  }
  
  .option-letter-preview {
    width: 1.5rem;
    height: 1.5rem;
    font-size: 0.8rem;
  }
  
  .option-text-preview {
    font-size: 0.85rem;
  }
}
</style> 
