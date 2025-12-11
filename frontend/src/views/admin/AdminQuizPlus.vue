<template>
  <div>
    <FormatHelp :format-template="QUIZ_FORMAT_TEMPLATE">
      <template #notes>
        <ul>
          <li>Utilisez <code>===</code> pour délimiter chaque quiz</li>
          <li><strong>⚠️ IMPORTANT :</strong> Sélectionnez d'abord la notion dans la liste déroulante ci-dessus</li>
          <li>Difficulté : <code>easy</code>, <code>medium</code> ou <code>hard</code> uniquement</li>
          <li>Images multiples : Séparez les noms de fichiers par des virgules : <code>image1.jpg,image2.png</code></li>
          <li>Positionnement d'images : Utilisez <code>[IMAGE_1]</code>, <code>[IMAGE_2]</code>, etc. dans les questions pour positionner les images</li>
          <li>Ordre des images : Les images sont assignées dans l'ordre de leur déclaration (1ère = [IMAGE_1], 2ème = [IMAGE_2], etc.)</li>
          <li><strong>Solution :</strong> Utilisez <code>Solution:</code> à la fin pour ajouter la solution complète (visible après correction)</li>
          <li>MathJax supporté : <code>$formule$</code> (inline) et <code>$$formule$$</code> (bloc)</li>
          <li>Markdown supporté : <code>**gras**</code> et <code>*italique*</code></li>
          <li>Laissez <code>Image:</code> vide si pas d'image</li>
        </ul>
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
        <h4>📁 Images pour les sujets d'examen</h4>
        <p class="upload-help">Uploadez les images qui seront référencées dans vos exercices :</p>
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
        placeholder="Collez ici vos sujets d'examen (séparés par ===)"
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
          Créer {{ previewList.length || '' }} sujet(s)
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

    <!-- Aperçu -->
    <div v-if="previewList.length" class="preview-section">
      <h3>Aperçu ({{ previewList.length }})</h3>
      <div v-for="(quiz, idx) in previewList" :key="idx" class="preview-item">
        <h4>{{ quiz.titre }}</h4>
        <div v-if="quiz.image" class="preview-image-info">
          <span class="image-indicator">🖼️ Images: {{ quiz.image }}</span>
          <div class="image-status-list">
            <span 
              v-for="imgName in quiz.image.split(',').map(name => name.trim()).filter(Boolean)" 
              :key="imgName"
              :class="['image-status', getImageFile(imgName) ? 'available' : 'missing']"
            >
              {{ imgName }}: {{ getImageFile(imgName) ? '✅ Disponible' : '❌ Manquante' }}
            </span>
          </div>
        </div>
        
        <!-- Afficher tous les exercices dans un seul composant avec onglets -->
        <ExerciceQCM 
          :eid="`preview-${idx}`" 
          :titre="quiz.titre" 
          :exercices-list="quiz.questions"
          :difficulty="quiz.difficulty" 
          :preview-images="getPreviewImages(quiz.image, quiz)"
        />

        <!-- Aperçu de la solution -->
        <div v-if="quiz.solution" class="preview-solution">
          <div class="preview-solution-header">
            📖 Solution (sera visible après correction)
          </div>
          <div class="preview-solution-content" v-html="renderPreviewSolution(quiz.solution)"></div>
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
import ExerciceQCM from '@/components/UI/ExerciceQCM.vue'

const chapitres = ref([])
const notions = ref([])
const notionFilter = ref('')
const selectedNotion = ref('')
const rawInput = ref('')
const successMsg = ref('')
const errorMsg = ref('')
const previewList = ref([])
const selectedImages = ref([])
const imagesInput = ref(null)

// ============================================================================
// CONSTANTES DU FORMAT
// ============================================================================

const QUIZ_FORMAT_TEMPLATE = `=== [Titre du sujet d'examen]
Difficulté: [easy/medium/hard]
Image: [nom_fichier1.jpg,nom_fichier2.png] (optionnel)

Ex1:
[Énoncé de l'exercice 1]
[IMAGE_1]
[Suite de l'énoncé...]

Ex2:
[Énoncé de l'exercice 2]

Ex3:
[Énoncé de l'exercice 3]

Solution:
[Solution complète du quiz ici]
[Peut contenir plusieurs lignes]
[MathJax et Markdown supportés]

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
    // Par défaut, les images sont pour les questions/exercices
    return 'question'
  }

  /**
   * Crée les objets d'images pour la prévisualisation
   */
  createPreviewImages(imageString, exerciceData = null) {
    if (!imageString) return []
    
    const imageNames = this.parseImageString(imageString)
    return imageNames.map((name, index) => {
      const file = this.getImage(name)
      const imageType = exerciceData ? this.determineImageType(exerciceData, index + 1) : 'question'
      
      return {
        id: `preview-${index}`,
        image: file ? URL.createObjectURL(file) : name,
        image_type: imageType,
        position: index + 1
      }
    })
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
        solution: quizData.solution || '',
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

function parseInput() {
  const text = rawInput.value.trim()
  if (!text) return []

  return parseBlockFormat(text)
}

function parseBlockFormat(text) {
  // Séparer par === et nettoyer
  const blocks = text
    .split(/^===/m) // Séparer au début de chaque bloc
    .map(b => b.trim())
    .filter(b => b && !b.match(/^===$/)) // Exclure les lignes vides et les === isolés

  console.log('🔍 Blocs détectés:', blocks.length)
  return blocks.map((block, index) => parseBlock(block, index))
}

function parseBlock(block, index) {
  const lines = block.split('\n')
  const quiz = {
    titre: '',
    instruction: '',
    difficulty: 'medium',
    image: '',
    questions: [],
    notion: Number(selectedNotion.value),
    solution: ''
  }

  let currentExercice = null
  let currentExNumber = null
  let firstLine = true

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    const trimmedLine = line.trim()
    
    if (!trimmedLine) {
      // Ligne vide - ignorer complètement
      continue
    }

    // Première ligne non vide = titre (peut contenir des crochets)
    if (firstLine) {
      const titleMatch = trimmedLine.match(/^\[(.*)\]$/)
      if (titleMatch) {
        quiz.titre = titleMatch[1].trim()
      } else {
        quiz.titre = trimmedLine
      }
      firstLine = false
      continue
    }

    // Métadonnées du quiz
    if (trimmedLine.match(/^Difficult[eé]:/i)) {
      const match = trimmedLine.match(/^Difficult[eé]:\s*(.+)/i)
      if (match) {
        quiz.difficulty = match[1].trim().toLowerCase()
      }
      continue
    }
    
    if (trimmedLine.match(/^Images?:/i)) {
      quiz.image = trimmedLine.replace(/^Images?:/i, '').trim()
      continue
    }

    if (trimmedLine.match(/^Instructions?:/i)) {
      quiz.instruction = trimmedLine.replace(/^Instructions?:/i, '').trim()
      continue
    }

    // Détection de la section Solution (arrête le parsing des exercices)
    if (trimmedLine.match(/^Solution:/i)) {
      // Sauvegarder le dernier exercice si il existe
      if (currentExercice && currentExercice.question.trim()) {
        quiz.questions.push(fixQuestion(currentExercice))
        currentExercice = null
      }
      
      // Récupérer tout le contenu après "Solution:" jusqu'à la fin du bloc
      const solutionStartIndex = i
      const solutionLines = []
      
      // Ajouter le contenu après "Solution:" sur la même ligne
      const solutionMatch = trimmedLine.match(/^Solution:\s*(.*)$/i)
      if (solutionMatch && solutionMatch[1].trim()) {
        solutionLines.push(solutionMatch[1].trim())
      }
      
      // Ajouter toutes les lignes suivantes
      for (let j = i + 1; j < lines.length; j++) {
        solutionLines.push(lines[j])
      }
      
      quiz.solution = solutionLines.join('\n').trim()
      break // Sortir de la boucle, tout le reste est la solution
    }

    // Détection d'un nouvel exercice (Ex1:, Ex2:, Ex3:, etc.)
    const exMatch = trimmedLine.match(/^Ex(\d+):\s*(.*)$/i)
    if (exMatch) {
      // Sauvegarder l'exercice précédent si il existe
      if (currentExercice && currentExercice.question.trim()) {
        quiz.questions.push(fixQuestion(currentExercice))
      }
      
      // Créer un nouvel exercice
      currentExNumber = parseInt(exMatch[1])
      currentExercice = {
        question: exMatch[2].trim(), // Contenu après Ex1: (peut être vide)
        options: ['Réponse libre'], // Quiz de type "énoncé" sans QCM
        correct_answer: 0,
        explanation: '',
        exNumber: currentExNumber
      }
      continue
    }

    // Si on est dans un exercice, ajouter le contenu
    if (currentExercice !== null) {
      if (currentExercice.question) {
        currentExercice.question += '\n' + trimmedLine // Préserver les retours à la ligne
      } else {
        currentExercice.question = trimmedLine
      }
    }
  }

  // Sauvegarder le dernier exercice
  if (currentExercice && currentExercice.question.trim()) {
    quiz.questions.push(fixQuestion(currentExercice))
  }

  // Si pas d'instruction explicite, utiliser le titre
  if (!quiz.instruction) {
    quiz.instruction = quiz.titre
  }

  return quiz
}

function fixQuestion(question) {
  const q = { ...question }
  
  // Ne PAS normaliser les retours à la ligne pour les exercices d'examen
  // Le texte doit être passé tel quel au composant ExerciceQCM
  // Les marqueurs comme $\\$ seront interprétés par le composant
  
  // Vérifier les options
  if (!Array.isArray(q.options) || q.options.length === 0) {
    q.options = ['Réponse libre']
    q.correct_answer = 0
  }
  
  // Valider correct_answer
  if (typeof q.correct_answer !== 'number' || Number.isNaN(q.correct_answer)) {
    q.correct_answer = 0
  }
  
  // S'assurer que correct_answer est dans les limites
  if (q.correct_answer < 0 || q.correct_answer >= q.options.length) {
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
      errorMsg.value = 'Aucun sujet valide trouvé. Vérifiez le format.'
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
    
    let message = `${created} sujet(s) créé(s) avec ${totalQuestions} exercice(s) au total !`
    if (errors.length > 0) {
      message += `\n\nErreurs : ${errors.join(' | ')}`
      errorMsg.value = `Certains sujets n'ont pas pu être créés : ${errors.join(' | ')}`
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
        errorMsg.value = 'Erreur lors de la création des sujets.'
      }
    } else {
      errorMsg.value = 'Erreur lors de la création des sujets.'
    }
  }
}

function handlePreview() {
  errorMsg.value = ''
  successMsg.value = ''
  
  try {
    const parsed = parseInput().filter(q => q.titre && q.questions.length > 0)
    previewList.value = parsed
    
    if (parsed.length === 0) {
      errorMsg.value = 'Aucun sujet valide trouvé. Vérifiez le format.'
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

function getImageFile(imageName) {
  return imageManager.getImage(imageName)
}

function getPreviewImages(imageString, exerciceData = null) {
  return imageManager.createPreviewImages(imageString, exerciceData)
}

function renderPreviewSolution(solution) {
  if (!solution) return ''
  // Convertir les retours à la ligne en <br> et traiter le Markdown basique
  let html = solution
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
  return html
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

/* Preview Solution */
.preview-solution {
  margin-top: 1.5rem;
  background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
  border: 2px solid #86efac;
  border-radius: 12px;
  overflow: hidden;
}

.preview-solution-header {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
  padding: 0.75rem 1rem;
  font-weight: 600;
  font-size: 1rem;
}

.preview-solution-content {
  padding: 1.25rem;
  color: #166534;
  font-size: 0.95rem;
  line-height: 1.8;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.preview-solution-content strong {
  color: #14532d;
  font-weight: 700;
}

.preview-solution-content em {
  font-style: italic;
}
</style> 
