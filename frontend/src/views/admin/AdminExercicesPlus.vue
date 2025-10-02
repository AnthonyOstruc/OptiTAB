<template>
  <div>
    <FormatHelp :format-template="FORMAT_TEMPLATE">
      <template #notes>
        <ul>
          <li>Utilisez <code>===</code> pour délimiter chaque exercice</li>
          <li><strong>⚠️ IMPORTANT :</strong> Sélectionnez d'abord la notion dans la liste déroulante ci-dessus</li>
          <li>Difficulté : <code>easy</code>, <code>medium</code> ou <code>hard</code> uniquement</li>
          <li>Images multiples : Séparez les noms de fichiers par des virgules : <code>image1.jpg,image2.png</code></li>
          <li>Positionnement d'images : Utilisez <code>[IMAGE_1]</code>, <code>[IMAGE_2]</code>, etc. dans l'énoncé pour positionner les images</li>
          <li>Ordre des images : Les images sont assignées dans l'ordre de leur déclaration (1ère = [IMAGE_1], 2ème = [IMAGE_2], etc.)</li>
          <li>Types d'images automatiques : Les images dans l'énoncé = "Donnée", dans les étapes/solution = "Solution"</li>
          <li>Étapes : Décrivez les étapes de résolution pour guider l'élève</li>
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
        <option v-for="n in filteredNotions" :key="n.id" :value="n.id">{{ (n.nom || n.titre) }}</option>
      </select>

      <!-- Upload d'images -->
      <div class="images-upload-section">
        <h4>📁 Images pour les exercices</h4>
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

      <textarea v-model="rawInput" placeholder="Collez ici vos exercices"></textarea>
      <div class="btn-group">
        <button class="btn-secondary" @click="handlePreview" :disabled="!rawInput.trim()" type="button">Prévisualiser</button>
        <button class="btn-primary" @click="handleCreate" :disabled="!selectedNotion || !rawInput.trim()">Créer les exercices</button>
      </div>
    </div>

    <div v-if="successMsg" class="success-msg">{{ successMsg }}</div>
    <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>
    <div v-if="previewList.length === 0 && rawInput.trim() && hasValidExercices" class="info-msg">Aucun exercice valide trouvé. Vérifiez le format.</div>

    <!-- Aperçu -->
    <div v-if="previewList.length" class="preview-section">
      <h3>Aperçu ({{ previewList.length }})</h3>
      <div v-for="(ex, idx) in previewList" :key="idx" class="preview-item">
        <h4>{{ ex.titre }}</h4>
        <div v-if="ex.image" class="preview-image-info">
          <span class="image-indicator">🖼️ Images: {{ ex.image }}</span>
          <div class="image-status-list">
            <span 
              v-for="imgName in ex.image.split(',').map(name => name.trim()).filter(Boolean)" 
              :key="imgName"
              :class="['image-status', getImageFile(imgName) ? 'available' : 'missing']"
            >
              {{ imgName }}: {{ getImageFile(imgName) ? '✅ Disponible' : '❌ Manquante' }}
            </span>
          </div>
        </div>
        <ExerciceQCM 
          :eid="`preview-${idx}`" 
          :titre="ex.titre" 
          :instruction="ex.instruction" 
          :etapes="ex.etapes" 
          :solution="ex.solution" 
          :difficulty="ex.difficulty" 
          :preview-images="getPreviewImages(ex.image, ex)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getNotions, createExercice, createExerciceImage } from '@/api'
import ExerciceQCM from '@/components/UI/ExerciceQCM.vue'
import FormatHelp from '@/components/admin/FormatHelp.vue'

// ============================================================================
// CONSTANTES ET CONFIGURATION
// ============================================================================

const SUPPORTED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
const MAX_IMAGE_SIZE = 10 * 1024 * 1024 // 10MB
const IMAGE_MARKER_REGEX = /\[IMAGE_(\d+)\]/g

// ============================================================================
// ÉTAT RÉACTIF
// ============================================================================

const notions = ref([])
const notionFilter = ref('')
const selectedNotion = ref('')
const rawInput = ref('')
const successMsg = ref('')
const errorMsg = ref('')
const previewList = ref([])
const hasValidExercices = ref(false)
const selectedImages = ref([])
const imagesInput = ref(null)

// ============================================================================
// CONSTANTES DU FORMAT
// ============================================================================

const FORMAT_TEMPLATE = `=== [Titre de l'exercice]
Difficulté: [easy/medium/hard]
Image: [nom_fichier1.jpg,nom_fichier2.png] (optionnel)

Énoncé: [description de l'exercice]

[IMAGE_1]

[suite de l'énoncé]

[IMAGE_2]

[fin de l'énoncé]

Étapes: [étapes de résolution détaillées]

**Question 1 : [Titre de la première question]**
    ● [Première étape]
    ● [Deuxième étape]
    ● [Troisième étape]

**Question 2 : [Titre de la deuxième question]**
    ● [Première étape]
    ● [Deuxième étape]

Solution:
1. [Réponse à la question 1]
2. [Réponse à la question 2]

===`

// ============================================================================
// CLASSES UTILITAIRES
// ============================================================================

/**
 * Classe pour gérer les images d'exercices
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

    // Recherche partielle
    for (const [name, imgFile] of this.images) {
      if (name.toLowerCase().includes(filename.toLowerCase()) ||
          filename.toLowerCase().includes(name.toLowerCase())) {
        return imgFile
      }
    }

    return null
  }

  /**
   * Détermine le type d'une image basé sur sa position dans le texte
   */
  determineImageType(exerciceData, imagePosition) {
    const imageMarker = `[IMAGE_${imagePosition}]`
    
    // Image dans la solution = type 'solution'
    if (exerciceData.solution && exerciceData.solution.includes(imageMarker)) {
      return 'solution'
    }
    
    // Image dans les étapes = type 'solution'
    if (exerciceData.etapes && exerciceData.etapes.includes(imageMarker)) {
      return 'solution'
    }
    
    // Sinon = type 'donnee' (dans l'énoncé)
    return 'donnee'
  }

  /**
   * Crée les objets d'images pour la prévisualisation
   */
  createPreviewImages(imageString, exerciceData = null) {
    if (!imageString) return []
    
    const imageNames = this.parseImageString(imageString)
    return imageNames.map((name, index) => {
      const file = this.getImage(name)
      const imageType = exerciceData ? this.determineImageType(exerciceData, index + 1) : 'donnee'
      
      return {
        id: `preview-${index}`,
        image: file ? URL.createObjectURL(file) : name,
        image_type: imageType,
        position: index + 1
      }
    })
  }

  /**
   * Parse une chaîne d'images séparées par des virgules
   */
  parseImageString(imageString) {
    return imageString
      .split(',')
      .map(name => name.trim())
      .filter(Boolean)
  }

  /**
   * Vérifie si toutes les images référencées sont disponibles
   */
  validateImageReferences(imageString) {
    if (!imageString) return { valid: true, missing: [] }
    
    const imageNames = this.parseImageString(imageString)
    const missing = imageNames.filter(name => !this.getImage(name))
    
    return {
      valid: missing.length === 0,
      missing,
      available: imageNames.filter(name => this.getImage(name))
    }
  }

  /**
   * Nettoie les ressources (URLs blob)
   */
  cleanup() {
    this.images.clear()
    this.imageTypes.clear()
  }
}

/**
 * Classe pour parser les exercices
 */
class ExerciceParser {
  constructor(imageManager) {
    this.imageManager = imageManager
  }

  /**
   * Parse le texte brut en exercices
   */
  parseExercices(text) {
    if (text.includes('===')) {
      return this.parseBlockFormat(text)
    } else {
      return this.parseLineFormat(text)
    }
  }

  /**
   * Parse le format bloc === ... ===
   */
  parseBlockFormat(text) {
    // Séparer par === et nettoyer
    const blocks = text
      .split(/^===/m) // Séparer au début de chaque bloc
      .map(b => b.trim())
      .filter(b => b && !b.match(/^===$/)) // Exclure les lignes vides et les === isolés

    console.log('🔍 Blocs détectés:', blocks.length)
    return blocks.map((block, index) => this.parseBlock(block, index))
  }

  /**
   * Parse un bloc d'exercice
   */
  parseBlock(block, index) {
    const lines = block.split('\n')
    const exercice = {
      titre: '',
      instruction: '',
      etapes: '',
      solution: '',
      image: '',
      difficulty: 'medium',
      notion: Number(selectedNotion.value)
    }

    let currentSection = null
    let firstLine = true

    for (const line of lines) {
      const trimmedLine = line.trim()
      
      if (!trimmedLine) continue

      // Première ligne non vide = titre (peut contenir des crochets)
      if (firstLine) {
        // Extraire le titre des crochets si présent
        const titleMatch = trimmedLine.match(/^\[(.*)\]$/)
        if (titleMatch) {
          exercice.titre = titleMatch[1].trim()
        } else {
          exercice.titre = trimmedLine
        }
        firstLine = false
        continue
      }

             // Détection des sections
       if (trimmedLine.match(/^Énoncé:/i)) {
         currentSection = 'instruction'
         exercice.instruction = trimmedLine.replace(/^Énoncé:/i, '').trim()
       } else if (trimmedLine.match(/^Étapes?:/i)) {
         currentSection = 'etapes'
         exercice.etapes = trimmedLine.replace(/^Étapes?:/i, '').trim()
       } else if (trimmedLine.startsWith('Solution:')) {
         currentSection = 'solution'
         exercice.solution = trimmedLine.slice(9).trim()
       } else if (trimmedLine.startsWith('Image:')) {
         exercice.image = trimmedLine.slice(6).trim()
       } else if (trimmedLine.match(/^Difficult[eé]:/i)) {
         const match = trimmedLine.match(/^Difficult[eé]:\s*(.+)/i)
         if (match) {
           exercice.difficulty = match[1].trim().toLowerCase()
         }
       } else {
         // Ajouter au contenu de la section actuelle
         if (currentSection) {
           exercice[currentSection] += '\n' + trimmedLine
         }
       }

      firstLine = false
    }

    return exercice
  }

  /**
   * Parse le format ligne ;; ;; ;;
   */
  parseLineFormat(text) {
    const lines = text
      .split('\n')
      .map(l => l.trim())
      .filter(Boolean)

    return lines.map((line) => {
      const parts = line.split(';;').map(p => p.trim())
      return {
        titre: parts[0] || '',
        instruction: parts[1] || '',
        etapes: parts[2] || '',
        solution: parts[3] || '',
        difficulty: (parts[4] || 'medium').toLowerCase(),
        notion: Number(selectedNotion.value),
        image: parts[5] || ''
      }
    })
  }
}

/**
 * Classe pour créer les exercices
 */
class ExerciceCreator {
  constructor(imageManager) {
    this.imageManager = imageManager
  }

  /**
   * Crée un exercice avec ses images
   */
  async createExerciceWithImages(exerciceData) {
    try {
      // 1. Construire le payload pour le backend (nouvelle logique)
      const difficulty = (exerciceData.difficulty || 'medium').toLowerCase()
      // Garantir des champs non vides pour satisfaire le backend
      const safeTitre = (exerciceData.titre && exerciceData.titre.trim()) ? exerciceData.titre.trim() : 'Exercice'
      const safeInstruction = (exerciceData.instruction && exerciceData.instruction.trim()) ? exerciceData.instruction.trim() : safeTitre
      const safeSolution = (exerciceData.solution && exerciceData.solution.trim()) ? exerciceData.solution.trim() : 'A compléter'
      const payload = {
        notion: Number(selectedNotion.value),
        titre: safeTitre,
        contenu: safeInstruction,
        difficulty: ['easy','medium','hard'].includes(difficulty) ? difficulty : 'medium',
        // Champs complémentaires compatibles
        question: safeInstruction,
        reponse_correcte: safeSolution,
        etapes: exerciceData.etapes || '', // Ajouter les étapes
        points: 1
      }

      // 2. Créer l'exercice (API unifiée renvoie déjà l'objet créé)
      const exerciceResponse = await createExercice(payload)
      const exerciceId = exerciceResponse?.id

      // 3. Ajouter les images si présentes
      if (exerciceData.image) {
        await this.addImagesToExercice(exerciceId, exerciceData)
      }

      return { success: true, exerciceId }
    } catch (error) {
      console.error('Erreur lors de la création de l\'exercice:', error, error?.response?.data)
      return { 
        success: false, 
        error: error.response?.data ? JSON.stringify(error.response.data) : (error.message || 'Erreur inconnue')
      }
    }
  }

  /**
   * Ajoute les images à un exercice
   */
  async addImagesToExercice(exerciceId, exerciceData) {
    const imageNames = this.imageManager.parseImageString(exerciceData.image)
    const errors = []

    for (let i = 0; i < imageNames.length; i++) {
      const imageName = imageNames[i]
      const imageFile = this.imageManager.getImage(imageName)

      if (imageFile) {
        try {
          const imageType = this.imageManager.determineImageType(exerciceData, i + 1)
          
          await createExerciceImage({
            exercice: exerciceId,
            image: imageFile,
            image_type: imageType,
            position: i + 1
          })
        } catch (imageError) {
          console.error(`Erreur lors de l'ajout de l'image ${imageName}:`, imageError)
          errors.push(`Image ${imageName} non ajoutée`)
        }
      } else {
        errors.push(`Image ${imageName} non trouvée`)
      }
    }

    return errors
  }
}

// ============================================================================
// INSTANCES DES CLASSES
// ============================================================================

const imageManager = new ImageManager()
const exerciceParser = new ExerciceParser(imageManager)
const exerciceCreator = new ExerciceCreator(imageManager)

// ============================================================================
// FONCTIONS PRINCIPALES
// ============================================================================

async function load() {
  try {
    const nt = await getNotions()
    notions.value = Array.isArray(nt) ? nt : (nt?.data || [])
  } catch (error) {
    console.error('Erreur lors du chargement:', error)
  }
}

function getNotionName(id) {
  const n = notions.value.find((n) => n.id === id)
  return n ? n.nom : id
}

// =============================
// Helpers d'affichage contextuel
// =============================
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

function parseInput() {
  const parsed = exerciceParser.parseExercices(rawInput.value)
  // Injecter notion pour chaque exercice
  return parsed.map(ex => ({ ...ex, notion: Number(selectedNotion.value) }))
}

async function handleCreate() {
  errorMsg.value = ''
  successMsg.value = ''
  
  // Validation de la notion sélectionnée
  if (!selectedNotion.value) {
    errorMsg.value = '⚠️ Veuillez sélectionner une notion dans la liste déroulante.'
    return
  }
  
  try {
    const exercices = parseInput()
    console.log('🔄 Données à envoyer:', exercices)
    
    let created = 0
    let errors = []
    const createdTitles = new Set() // Pour tracker les titres créés dans cette session
    
    for (const exerciceData of exercices) {
      // Normalisation legacy: la couche "chapitre" a été retirée.
      // Certains anciens écrans s'attendent encore à passer un chapitre.
      // On mappe donc sur la notion sélectionnée pour éviter les erreurs runtime.
      // Le backend utilise déjà le champ "notion" dans le payload (cf. ExerciceCreator.createExerciceWithImages).
      exerciceData.chapitre = Number(selectedNotion.value)
      
      // Assurer l'unicité du titre au sein du chapitre (backend unique_together)
      let baseTitle = (exerciceData.titre && exerciceData.titre.trim()) ? exerciceData.titre.trim() : 'Exercice'
      let candidate = baseTitle
      let suffix = 1
      
      // Vérifier seulement contre les titres déjà créés dans cette session
      // Ne pas vérifier contre previewList car ces exercices ne sont pas encore en base
      while (createdTitles.has(candidate.toLowerCase())) {
        suffix += 1
        candidate = `${baseTitle} (${suffix})`
      }
      
      exerciceData.titre = candidate
      createdTitles.add(candidate.toLowerCase()) // Ajouter à la liste des titres créés
      
      // Valider les références d'images
      const imageValidation = imageManager.validateImageReferences(exerciceData.image)
      if (!imageValidation.valid) {
        errors.push(`Images manquantes pour "${exerciceData.titre}": ${imageValidation.missing.join(', ')}`)
        continue
      }

      // Créer l'exercice avec ses images
      const result = await exerciceCreator.createExerciceWithImages(exerciceData)
      
      if (result.success) {
        created++
      } else {
        errors.push(`Erreur pour "${exerciceData.titre}": ${result.error}`)
      }
    }
    
    // Afficher les résultats
    if (created > 0) {
      successMsg.value = `✅ ${created} exercice(s) créé(s) avec succès !`
      if (errors.length > 0) {
        successMsg.value += ` (${errors.length} erreur(s) mineure(s))`
      }

      // Sauvegarder la notion actuelle avant de nettoyer le formulaire
      const currentNotion = selectedNotion.value

      // Nettoyer le formulaire
      rawInput.value = ''
      imageManager.cleanup()
      selectedImages.value = []
      if (imagesInput.value) imagesInput.value.value = ''
      previewList.value = []

      // Remettre la notion sélectionnée pour permettre d'ajouter d'autres exercices dans la même notion
      selectedNotion.value = currentNotion
    }
    
    if (errors.length > 0) {
      errorMsg.value = '⚠️ Erreurs rencontrées :\n' + errors.join('\n')
    }
    
  } catch (error) {
    console.error('Erreur générale:', error)
    errorMsg.value = `❌ Erreur lors de la création : ${error.response?.data?.message || error.message}`
  }
}

function handlePreview() {
  try {
    previewList.value = parseInput()
    hasValidExercices.value = previewList.value.length > 0
  } catch (error) {
    console.error('Erreur lors de la prévisualisation:', error)
    errorMsg.value = `❌ Erreur de format : ${error.message}`
  }
}

// ============================================================================
// COMPUTED PROPERTIES
// ============================================================================

// Notions filtrées (par texte seulement)
const filteredNotions = computed(() => {
  if (!notionFilter.value) {
    return notions.value
  }
  const filter = notionFilter.value.toLowerCase()
  return notions.value.filter(notion =>
    (notion.nom || notion.titre || '').toLowerCase().includes(filter)
  )
})

// ============================================================================
// LIFECYCLE
// ============================================================================

onMounted(load)
</script>

<style src="@/styles/admin-common.css"></style>

<style scoped>
/* Styles spécifiques à AdminExercicesPlus - ajoutés si nécessaire */
</style> 