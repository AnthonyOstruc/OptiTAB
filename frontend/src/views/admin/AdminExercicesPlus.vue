<template>
  <div>
    <h2 class="admin-title">Bulk – Ajout d'Exercices</h2>
    <div class="format-help">
      <h3>📋 Format requis :</h3>
             <div class="format-example">
         <pre><code>=== [Titre de l'exercice]
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

===
</code></pre>
       </div>
                     <div class="format-notes">
                 <p><strong>Notes importantes :</strong></p>
                 <ul>
                   <li>Utilisez <code>===</code> pour délimiter chaque exercice</li>
                   <li><strong>⚠️ IMPORTANT :</strong> Sélectionnez d'abord le chapitre dans la liste déroulante ci-dessus</li>
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
               </div>
    </div>

    <div class="bulk-form">
      <select v-model="selectedChapitre" required>
        <option disabled value="">Choisir chapitre</option>
        <option v-for="c in chapitres" :key="c.id" :value="c.id">{{ formatChapitreOption(c) }}</option>
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

      <textarea v-model="rawInput" placeholder="Coller ici vos exercices…"></textarea>
      <div class="btn-group">
        <button class="btn-secondary" @click="handlePreview" :disabled="!rawInput.trim()" type="button">Prévisualiser</button>
        <button class="btn-primary" @click="handleCreate" :disabled="!selectedChapitre || !rawInput.trim()">Créer les exercices</button>
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
import { ref, onMounted } from 'vue'
import { getChapitres, getNotions, createExercice, createExerciceImage } from '@/api'
import ExerciceQCM from '@/components/UI/ExerciceQCM.vue'

// ============================================================================
// CONSTANTES ET CONFIGURATION
// ============================================================================

const SUPPORTED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
const MAX_IMAGE_SIZE = 10 * 1024 * 1024 // 10MB
const IMAGE_MARKER_REGEX = /\[IMAGE_(\d+)\]/g

// ============================================================================
// ÉTAT RÉACTIF
// ============================================================================

const chapitres = ref([])
const notions = ref([])
const selectedChapitre = ref('')
const rawInput = ref('')
const successMsg = ref('')
const errorMsg = ref('')
const previewList = ref([])
const hasValidExercices = ref(false)
const selectedImages = ref([])
const imagesInput = ref(null)

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
      chapitre: Number(selectedChapitre.value)
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
        chapitre: Number(selectedChapitre.value),
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
        chapitre: Number(exerciceData.chapitre || selectedChapitre.value),
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
    const [ch, nt] = await Promise.all([
      getChapitres(),
      getNotions()
    ])
    chapitres.value = Array.isArray(ch) ? ch : (ch?.data || [])
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
  return exerciceParser.parseExercices(rawInput.value)
}

async function handleCreate() {
  errorMsg.value = ''
  successMsg.value = ''
  
  // Validation du chapitre sélectionné
  if (!selectedChapitre.value) {
    errorMsg.value = '⚠️ Veuillez sélectionner un chapitre dans la liste déroulante.'
    return
  }
  
  try {
    const exercices = parseInput()
    console.log('🔄 Données à envoyer:', exercices)
    
    let created = 0
    let errors = []
    const createdTitles = new Set() // Pour tracker les titres créés dans cette session
    
    for (const exerciceData of exercices) {
      // Normaliser chapitre pour la nouvelle API
      exerciceData.chapitre = Number(selectedChapitre.value)
      
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
      
      // Nettoyer le formulaire
      rawInput.value = ''
      imageManager.cleanup()
      selectedImages.value = []
      if (imagesInput.value) imagesInput.value.value = ''
      previewList.value = []
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
// LIFECYCLE
// ============================================================================

onMounted(load)
</script>

<style scoped>
.admin-title {font-size: 1.4rem;margin-bottom:1rem;}
.format-help{margin-bottom:2rem;padding:1rem;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0;}
.format-example{margin:1rem 0;}
.format-example pre{background:#1e293b;color:#e2e8f0;padding:1rem;border-radius:6px;overflow-x:auto;}
.format-notes ul{margin:0.5rem 0;padding-left:1.5rem;}
.format-notes li{margin:0.25rem 0;}
.bulk-form{display:flex;flex-direction:column;gap:1rem;margin-bottom:2rem;}
.bulk-form select,.bulk-form textarea{padding:0.75rem;border:1px solid #d1d5db;border-radius:6px;font-size:1rem;}
.bulk-form textarea{min-height:200px;resize:vertical;}
.btn-group{display:flex;gap:1rem;}
.btn-primary{background:#3b82f6;color:#fff;border:none;padding:0.75rem 1.5rem;border-radius:6px;cursor:pointer;font-weight:600;}
.btn-secondary{background:#6b7280;color:#fff;border:none;padding:0.75rem 1.5rem;border-radius:6px;cursor:pointer;}
.btn-primary:disabled,.btn-secondary:disabled{opacity:0.5;cursor:not-allowed;}
.success-msg{color:#059669;background:#d1fae5;padding:1rem;border-radius:6px;margin:1rem 0;white-space:pre-line;}
.error-msg{color:#dc2626;background:#fee2e2;padding:1rem;border-radius:6px;margin:1rem 0;white-space:pre-line;}
.info-msg{color:#7c3aed;background:#ede9fe;padding:1rem;border-radius:6px;margin:1rem 0;}
.preview-section{margin-top:2rem;}
.preview-item{margin-bottom:2rem;padding:1rem;border:1px solid #e5e7eb;border-radius:8px;background:#fff;}

/* Styles pour les images */
.images-upload-section {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  background: #f9fafb;
  margin-bottom: 1rem;
}

.images-upload-section h4 {
  margin: 0 0 0.5rem 0;
  color: #374151;
  font-size: 1.1rem;
}

.upload-help {
  margin: 0 0 1rem 0;
  color: #6b7280;
  font-size: 0.9rem;
}

.images-file-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px dashed #d1d5db;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  margin-bottom: 1rem;
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
  font-size: 0.9rem;
}

.selected-image-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
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
}

.btn-remove {
  background: #dc2626;
  color: white;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-remove:hover {
  background: #b91c1c;
}

.preview-image-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin: 0.5rem 0;
  padding: 0.75rem;
  background: #f3f4f6;
  border-radius: 6px;
}

.image-indicator {
  font-size: 0.9rem;
  color: #374151;
  font-weight: 600;
}

.image-status-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.image-status {
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  display: inline-block;
  width: fit-content;
}

.image-status.available {
  color: #059669;
  background: #d1fae5;
}

.image-status.missing {
  color: #dc2626;
  background: #fee2e2;
}

/* Responsive */
@media (max-width: 768px) {
  .btn-group {
    flex-direction: column;
  }
  
  .selected-image-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}
</style> 