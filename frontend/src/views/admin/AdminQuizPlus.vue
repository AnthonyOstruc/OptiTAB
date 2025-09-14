<template>
  <div>
    <h2 class="admin-title">🚀 Bulk – Création de Quiz QCM</h2>
    <div class="help-section">
      <p><strong>1.</strong> Sélectionnez le chapitre • <strong>2.</strong> Collez vos quiz au format structuré</p>
      
      <details class="format-help">
        <summary>📖 Guide du format (cliquez pour voir)</summary>
        <div class="format-examples">
          <h4>Format recommandé avec blocs ===</h4>
          <pre><code>Titre: Quiz Dérivées - Niveau 1
Instructions: Testez vos connaissances sur les dérivées
Difficulté: medium
Images: image1.png, image2.jpg

Question: Quelle est la dérivée de $f(x) = x^2$ ?
A: $2x$
B: $x$
C: $2$
D: $x^2$
Correct: A
Explication: La dérivée de $x^2$ est $2x$ d'après la règle...

Question: Quelle est la dérivée de $f(x) = \\sin(x)$ ?
A: $-\\cos(x)$
B: $\\cos(x)$
C: $\\sin(x)$
D: $-\\sin(x)$
Correct: B
Explication: La dérivée de $\\sin(x)$ est $\\cos(x)$...
===
Titre: Quiz Intégrales - Niveau 1
Instructions: Quiz sur les intégrales simples
...
===</code></pre>
          
          <h4>Support des images</h4>
          <ul>
            <li>Uploadez vos images via la section "📁 Images pour les quiz"</li>
            <li>Référencez les images avec : <code>Images: nom_image1.png, nom_image2.jpg</code></li>
            <li>Types supportés : JPG, PNG, GIF, WebP (max 10MB)</li>
            <li>Les images seront associées aux questions du quiz</li>
          </ul>
          
          <h4>Format alternatif (une ligne par quiz)</h4>
          <p><code>Titre ;; Instructions ;; Difficulté ;; JSON_Questions</code></p>
        </div>
      </details>
    </div>

    <div class="bulk-form">
      <input v-model="chapitreFilter" type="text" placeholder="Filtrer les chapitres..." class="filter-input" />
      <div class="form-row">
        <select v-model="selectedChapitre" required class="chapter-select">
          <option disabled value="">📚 Choisir le chapitre</option>
          <option v-for="c in filteredChapitres" :key="c.id" :value="c.id">
            {{ formatChapitreOption(c) }}
          </option>
        </select>
        
        <div class="stats">
          <span v-if="previewList.length" class="stat-item">
            📊 {{ previewList.length }} quiz • {{ getTotalQuestions() }} questions
          </span>
        </div>
      </div>

      <div v-if="currentContext" class="context-panel">
        <div class="context-row"><strong>Matière:</strong> <span>{{ currentContext.matiereNom || '—' }}</span></div>
        <div class="context-row"><strong>Thème:</strong> <span>{{ currentContext.themeNom || '—' }}</span></div>
        <div class="context-row"><strong>Pays:</strong> <span>{{ currentContext.paysNom || '—' }}</span></div>
        <div class="context-row"><strong>Niveau:</strong> <span>{{ currentContext.niveauNom || '—' }}</span></div>
      </div>

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
        placeholder="📝 Collez vos quiz ici au format structuré...

Exemple rapide :
Titre: Quiz Exemple
Instructions: Quiz d'exemple
Difficulté: easy

Question: Combien font 2+2 ?
A: 3
B: 4
C: 5
D: 6
Correct: B
Explication: 2+2=4, c'est mathématique !
==="
        class="quiz-textarea"
      ></textarea>
      
      <div class="btn-group">
        <button 
          class="btn-preview" 
          @click="handlePreview" 
          :disabled="!rawInput.trim()"
        >
          👁️ Prévisualiser
        </button>
        <button 
          class="btn-create" 
          @click="handleCreate" 
          :disabled="!selectedChapitre || !previewList.length"
        >
          ✨ Créer {{ previewList.length || '' }} quiz
        </button>
        <button 
          class="btn-clear" 
          @click="clearAll"
          v-if="rawInput || previewList.length"
        >
          🗑️ Vider
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
          {{ showExplanations ? '🙈 Masquer' : '👁️ Voir' }} explications
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

          <!-- Aperçu des questions -->
          <div class="questions-preview">
            <div v-for="(q, qIdx) in quiz.questions.slice(0, 2)" :key="qIdx" class="question-mini">
              <div class="question-header">
                <strong>Q{{ qIdx + 1 }}:</strong> 
                <div v-html="renderWithImages(q.question, quiz.image)"></div>
              </div>
              
              <div class="options-mini">
                <span v-for="(opt, oIdx) in q.options" :key="oIdx" 
                      class="option-mini" 
                      :class="{ correct: oIdx === q.correct_answer }">
                  {{ String.fromCharCode(65 + oIdx) }}: <span v-html="renderWithImages(opt, quiz.image)"></span>
                </span>
              </div>
              
              <div v-if="showExplanations" class="explanation-section">
                <div v-if="q.explanation" class="explanation-mini">
                  <strong>💡 Explication:</strong> 
                  <div v-html="renderWithImages(q.explanation, quiz.image)"></div>
                </div>
                <div v-else class="no-explanation">
                  <em>⚠️ Aucune explication fournie pour cette question</em>
                </div>
              </div>
            </div>
            <div v-if="quiz.questions.length > 2" class="more-questions">
              ... et {{ quiz.questions.length - 2 }} autres questions
              <span v-if="showExplanations">
                ({{ quiz.questions.slice(2).filter(q => q.explanation).length }} explications dans les autres questions)
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch, computed } from 'vue'
import { getChapitres, getNotions } from '@/api'
import { createQuiz, createQuizImage, updateQuiz } from '@/api/quiz'

const chapitres = ref([])
const notions = ref([])
const chapitreFilter = ref('')
const selectedChapitre = ref('')
const rawInput = ref('')
const successMsg = ref('')
const errorMsg = ref('')
const previewList = ref([])
const showExplanations = ref(true)
const selectedImages = ref([])
const imagesInput = ref(null)

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
        chapitre: Number(quizData.chapitre),
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
    const [ch, nt] = await Promise.all([
      getChapitres(), 
      getNotions()
    ])
    chapitres.value = Array.isArray(ch) ? ch : (ch?.data || [])
    notions.value = Array.isArray(nt) ? nt : (nt?.data || [])
  } catch (e) {
    console.error('Erreur chargement:', e)
  }
}

// Chapitres filtrés (par texte seulement)
const filteredChapitres = computed(() => {
  if (!chapitreFilter.value) {
    return chapitres.value
  }
  const filter = chapitreFilter.value.toLowerCase()
  return chapitres.value.filter(chapitre =>
    formatChapitreOption(chapitre).toLowerCase().includes(filter)
  )
})

onMounted(load)

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
  const c = chapitres.value.find(x => String(x.id) === String(selectedChapitre.value))
  return c ? chapterContext(c) : null
})

function formatChapitreOption(c) {
  const n = getNotionById(c.notion)
  const ctx = chapterContext(c)
  const parts = [
    c.nom,
    n ? `— ${n.nom}` : '',
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

  // Format bloc === ... ===
  if (text.includes('===')) {
    return parseBlockFormat(text)
  }
  
  // Format ligne avec ;;
  return parseLineFormat(text)
}

function parseBlockFormat(text) {
  const blocks = text.split(/^={3,}\s*$/m).map(b => b.trim()).filter(Boolean)
  
  return blocks.map((block) => {
    let titre = ''
    let instruction = ''
    let difficulty = 'medium'
    let image = ''
    const questions = []
    let currentQuestion = null

    const lines = block.split('\n').map(l => l.trim())
    
    for (const line of lines) {
      if (line.startsWith('Titre:')) {
        titre = line.slice(6).trim()
      } else if (line.startsWith('Instructions:')) {
        instruction = line.slice(12).trim()
      } else if (line.startsWith('Difficulté:') || line.startsWith('Difficulty:')) {
        difficulty = line.split(':')[1].trim().toLowerCase()
      } else if (line.startsWith('Images:')) {
        image = line.slice(7).trim()
      } else if (line.startsWith('Question:')) {
        // Sauver la question précédente
        if (currentQuestion && currentQuestion.question) {
          questions.push({ ...currentQuestion })
        }
        // Nouvelle question
        currentQuestion = {
          question: line.slice(9).trim(),
          options: [],
          correct_answer: 0,
          explanation: ''
        }
      } else if (line.match(/^[A-F]:/)) {
        if (currentQuestion) {
          currentQuestion.options.push(line.slice(2).trim())
        }
      } else if (line.startsWith('Correct:')) {
        if (currentQuestion) {
          const answer = line.slice(8).trim().toUpperCase()
          currentQuestion.correct_answer = answer.charCodeAt(0) - 65 // A=0, B=1, etc.
        }
      } else if (line.startsWith('Explication:')) {
        if (currentQuestion) {
          let explanation = line.slice(12).trim()
          // Corriger les doubles backslashes pour MathJax
          explanation = explanation.replace(/\\/g, '\\')
          currentQuestion.explanation = explanation
        }
      } else if (currentQuestion && currentQuestion.explanation && line.trim()) {
        // Continuer l'explication sur plusieurs lignes
        let additionalText = line.trim()
        // Corriger les doubles backslashes pour MathJax
        additionalText = additionalText.replace(/\\/g, '\\')
        currentQuestion.explanation += ' ' + additionalText
      } else if (currentQuestion && line.trim()) {
        // Lignes supplémentaires (ex: [IMAGE_1]) rattachées à l'énoncé
        const extra = line.trim()
        currentQuestion.question = currentQuestion.question
          ? currentQuestion.question + '\n' + extra
          : extra
      }
    }
    
    // Ajouter la dernière question
    if (currentQuestion && currentQuestion.question) {
      questions.push({ ...currentQuestion })
    }

    return {
      titre: titre || 'Quiz sans titre',
      instruction: instruction || 'Quiz',
      difficulty,
      image,
      questions,
      chapitre: Number(selectedChapitre.value)
    }
  })
}

function parseLineFormat(text) {
  const lines = text.split('\n').map(l => l.trim()).filter(Boolean)
  
  return lines.map((line) => {
    const parts = line.split(';;').map(p => p.trim())
    
    let questions = []
    try {
      questions = parts[3] ? JSON.parse(parts[3]) : []
    } catch (e) {
      console.warn('JSON invalide pour les questions:', parts[3])
    }

    return {
      titre: parts[0] || 'Quiz sans titre',
      instruction: parts[1] || 'Quiz',
      difficulty: (parts[2] || 'medium').toLowerCase(),
      questions,
      chapitre: Number(selectedChapitre.value)
    }
  })
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
    const currentChapitre = selectedChapitre.value

    successMsg.value = message
    rawInput.value = ''
    previewList.value = []

    // Remettre le chapitre sélectionné pour permettre d'ajouter d'autres quiz dans le même chapitre
    selectedChapitre.value = currentChapitre
    
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
  if (!text || !imageString) return text
  
  const imageNames = imageManager.parseImageString(imageString)
  
  // Debug: afficher les informations d'images
  console.log('renderWithImages - text:', text)
  console.log('renderWithImages - imageString:', imageString)
  console.log('renderWithImages - imageNames:', imageNames)
  console.log('renderWithImages - available images:', Array.from(imageManager.images.keys()))
  
  return text.replace(/\[IMAGE_(\d+)\]/g, (match, imageNumber) => {
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
}
</script>

<style scoped>
.admin-title {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  font-weight: 700;
  color: #1e293b;
}

.help-section {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 2rem;
}

.format-help summary {
  cursor: pointer;
  font-weight: 600;
  color: #3b82f6;
  margin-bottom: 0.5rem;
}

.format-examples {
  margin-top: 1rem;
}

.format-examples h4 {
  color: #374151;
  margin: 1rem 0 0.5rem 0;
}

.format-examples pre {
  background: #1f2937;
  color: #f9fafb;
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 0.85rem;
  line-height: 1.4;
}

.bulk-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 1000px;
}

.filter-input {
  margin-bottom: 0.5rem;
  width: 100%;
  padding: 0.5rem;
  border: 2px solid #d1d5db;
  border-radius: 6px;
  font-size: 1rem;
}

.form-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.chapter-select {
  padding: 10px 12px;
  border: 2px solid #d1d5db;
  border-radius: 6px;
  font-size: 1rem;
  min-width: 300px;
  background: white;
}

.stats {
  color: #6b7280;
  font-size: 0.9rem;
}

.stat-item {
  background: #eff6ff;
  padding: 4px 8px;
  border-radius: 4px;
  color: #1d4ed8;
}

.quiz-textarea {
  height: 300px;
  padding: 12px;
  border: 2px solid #d1d5db;
  border-radius: 6px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 0.9rem;
  line-height: 1.4;
  resize: vertical;
}

.btn-group {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  flex-wrap: wrap;
}

.btn-preview, .btn-create, .btn-clear {
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-preview {
  background: #f3f4f6;
  color: #374151;
}

.btn-preview:hover:not(:disabled) {
  background: #e5e7eb;
}

.btn-create {
  background: #10b981;
  color: white;
}

.btn-create:hover:not(:disabled) {
  background: #059669;
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

.success-msg {
  color: #10b981;
  font-weight: 600;
  margin-top: 1rem;
  padding: 10px;
  background: #d1fae5;
  border-radius: 6px;
}

.error-msg {
  color: #ef4444;
  font-weight: 600;
  margin-top: 1rem;
  padding: 10px;
  background: #fee2e2;
  border-radius: 6px;
}

.preview-section {
  margin-top: 2rem;
}

.context-panel {
  margin-top: 0.75rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 0.75rem 1rem;
}

.context-row {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-bottom: 0.25rem;
}

.context-row:last-child {
  margin-bottom: 0;
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
  display: grid;
  gap: 1.5rem;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
}

.quiz-preview-card {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.2s;
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

.difficulty-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.difficulty-badge.easy {
  background: #dcfce7;
  color: #166534;
}

.difficulty-badge.medium {
  background: #fef3c7;
  color: #92400e;
}

.difficulty-badge.hard {
  background: #fecaca;
  color: #991b1b;
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

.question-mini {
  font-size: 0.85rem;
  margin-bottom: 1rem;
  padding: 12px;
  background: #f8fafc;
  border-radius: 6px;
  border-left: 3px solid #3b82f6;
}

.question-header {
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.options-mini {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 0.5rem 0;
}

.option-mini {
  font-size: 0.75rem;
  padding: 3px 8px;
  background: #e5e7eb;
  border-radius: 4px;
  border: 1px solid #d1d5db;
}

.option-mini.correct {
  background: #dcfce7;
  color: #166534;
  font-weight: 600;
  border-color: #10b981;
}

.explanation-mini {
  margin-top: 0.75rem;
  padding: 8px;
  background: #fffbeb;
  border-radius: 4px;
  border-left: 3px solid #f59e0b;
  font-size: 0.8rem;
  line-height: 1.4;
}

.explanation-mini strong {
  color: #92400e;
  display: block;
  margin-bottom: 0.25rem;
}

.explanation-section {
  margin-top: 0.75rem;
}

.no-explanation {
  margin-top: 0.75rem;
  padding: 8px;
  background: #fef2f2;
  border-radius: 4px;
  border-left: 3px solid #ef4444;
  font-size: 0.8rem;
  color: #991b1b;
}

.more-questions {
  font-style: italic;
  color: #6b7280;
  font-size: 0.8rem;
  text-align: center;
  padding: 8px;
}

/* ============================================================================
   STYLES POUR LES IMAGES DE PRÉVISUALISATION
   ============================================================================ */

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

/* Images dans les options (plus petites) */
.option-mini .quiz-preview-image {
  max-width: 150px !important;
  margin: 4px 0 !important;
}

/* ============================================================================
   STYLES POUR LA SECTION D'UPLOAD D'IMAGES
   ============================================================================ */

.images-upload-section {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.images-upload-section h4 {
  margin: 0 0 0.5rem 0;
  color: #374151;
  font-size: 1.1rem;
}

.upload-help {
  font-size: 0.9rem;
  color: #6b7280;
  margin-bottom: 1rem;
}

.images-file-input {
  width: 100%;
  padding: 8px;
  border: 2px dashed #d1d5db;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  transition: border-color 0.2s;
}

.images-file-input:hover {
  border-color: #3b82f6;
}

.selected-images {
  margin-top: 1rem;
}

.selected-images h5 {
  margin: 0 0 0.75rem 0;
  color: #374151;
  font-size: 0.95rem;
}

.selected-image-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  margin-bottom: 0.5rem;
}

.image-preview {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid #d1d5db;
}

.image-name {
  flex: 1;
  font-size: 0.9rem;
  color: #374151;
  word-break: break-all;
}

.btn-remove {
  background: #ef4444;
  color: white;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  transition: background-color 0.2s;
}

.btn-remove:hover {
  background: #dc2626;
}

@media (max-width: 768px) {
  .quiz-grid {
    grid-template-columns: 1fr;
  }
  
  .form-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .chapter-select {
    min-width: auto;
  }
  
  .selected-image-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .image-preview {
    align-self: center;
  }
}
</style> 