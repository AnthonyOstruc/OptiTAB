<template>
  <div>
    <FormatHelp :format-template="FORMAT_TEMPLATE">
      <template #notes>
        <ul>
          <li>Utilisez <code>===</code> pour délimiter chaque cours</li>
          <li><strong>⚠️ IMPORTANT :</strong> Sélectionnez d'abord la notion dans la liste déroulante ci-dessus</li>
          <li>Difficulté : <code>easy</code>, <code>medium</code> ou <code>hard</code> uniquement</li>
          <li>Ordre : Numéro pour l'ordre d'affichage (0, 1, 2, etc.)</li>
          <li><strong>Images multiples :</strong> Séparez les noms de fichiers par des virgules : <code>image1.jpg,image2.png</code></li>
          <li><strong>Positionnement d'images :</strong> Utilisez <code>[IMAGE_1]</code>, <code>[IMAGE_2]</code>, etc. dans le contenu pour positionner les images</li>
          <li><strong>Ordre des images :</strong> Les images sont assignées dans l'ordre de leur déclaration (1ère = [IMAGE_1], 2ème = [IMAGE_2], etc.)</li>
          <li><strong>Types d'images automatiques :</strong> Toutes les images = "Illustration" par défaut</li>
          <li><strong>Contenu :</strong> Supporte HTML et LaTeX (MathJax)</li>
          <li>MathJax supporté : <code>$formule$</code> (inline) et <code>$$formule$$</code> (bloc)</li>
          <li>HTML supporté : <code>&lt;strong&gt;gras&lt;/strong&gt;</code>, <code>&lt;em&gt;italique&lt;/em&gt;</code>, etc.</li>
          <li>Laissez <code>Images:</code> vide si pas d'image</li>
          <li><strong>Champs obligatoires :</strong> Seuls <code>Titre:</code> et le contenu sont obligatoires</li>
          <li><strong>Champs optionnels :</strong> <code>Difficulté:</code>, <code>Ordre:</code>, <code>Images:</code>, <code>Description:</code></li>
          <li><strong>Template uniforme :</strong> Utilisez le template ci-dessus pour maintenir la cohérence de tous vos cours</li>
        </ul>
      </template>
    </FormatHelp>

    <div class="bulk-form">
      <input v-model="notionFilter" type="text" placeholder="Filtrer les notions..." class="filter-input" />
      <select v-model="selectedNotion" required>
        <option disabled value="">Choisir notion</option>
        <option v-for="n in filteredNotions" :key="n.id" :value="n.id">{{ formatNotionOption(n) }}</option>
      </select>

      <!-- Upload d'images -->
      <div class="images-upload-section">
        <h4>📁 Images pour les cours</h4>
        <p class="upload-help">Uploadez les images qui seront référencées dans vos cours :</p>
        <input 
          type="file" 
          ref="imagesInput" 
          @change="handleImagesSelect" 
          accept="image/*"
          multiple
          class="images-file-input"
        />
        <!-- Upload PDF optionnel -->
        <div class="pdf-upload" style="margin-top: 12px;">
          <h4>📄 PDF du cours (optionnel)</h4>
          <input type="file" ref="pdfInput" @change="handlePdfSelect" accept="application/pdf" />
        </div>
        <div v-if="selectedImages.length > 0" class="selected-images">
          <h5>Images sélectionnées :</h5>
          <div v-for="(img, index) in selectedImages" :key="index" class="selected-image-item">
            <img :src="getImagePreview(img)" :alt="img.name" class="image-preview" />
            <span class="image-name">{{ img.name }}</span>
            <button type="button" class="btn-remove" @click="removeSelectedImage(index)">×</button>
          </div>
        </div>
      </div>

      <textarea v-model="rawInput" placeholder="Collez ici vos cours"></textarea>
      <div class="btn-group">
        <button class="btn-secondary" @click="handlePreview" :disabled="!rawInput.trim()" type="button">Prévisualiser</button>
        <button class="btn-primary" @click="handleCreate" :disabled="!selectedNotion || !rawInput.trim()">Créer les cours</button>
      </div>
    </div>

    <div v-if="successMsg" class="success-msg">{{ successMsg }}</div>
    <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>
    <div v-if="previewList.length === 0 && rawInput.trim() && hasValidCours" class="info-msg">Aucun cours valide trouvé. Vérifiez le format.</div>

    <!-- Aperçu -->
    <div v-if="previewList.length" class="preview-section">
      <h3>Aperçu ({{ previewList.length }})</h3>
      <div v-for="(cours, idx) in previewList" :key="idx" class="preview-item">
        <h4>{{ cours.titre }}</h4>
        <div v-if="cours.image" class="preview-image-info">
          <span class="image-indicator">🖼️ Images: {{ cours.image }}</span>
          <div class="image-status-list">
            <span 
              v-for="imgName in cours.image.split(',').map(name => name.trim()).filter(Boolean)" 
              :key="imgName"
              :class="['image-status', getImageFile(imgName) ? 'available' : 'missing']"
            >
              {{ imgName }}: {{ getImageFile(imgName) ? '✅ Disponible' : '❌ Manquante - Assurez-vous d\'avoir uploadé cette image' }}
            </span>
          </div>
        </div>
        <div class="preview-cours">
          <div class="preview-header">
            <span class="difficulty-badge" :class="cours.difficulty">{{ getDifficultyLabel(cours.difficulty) }}</span>
            <span class="ordre-badge">Ordre: {{ cours.ordre }}</span>
          </div>
          <div v-if="cours.description" class="preview-description">
            <strong>Description:</strong> {{ cours.description }}
          </div>
          <div class="preview-content" v-html="renderPreviewContent(cours)"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onActivated, nextTick } from 'vue'
import { getNotions } from '@/api'
import { createCours, createCoursImage, getCours, updateCoursFormData, updateCours } from '@/api/cours'
import { renderContentWithImages, renderMath, markdownToHtml } from '@/utils/scientificRenderer'
import FormatHelp from '@/components/admin/FormatHelp.vue'

// ============================================================================
// CONSTANTES ET CONFIGURATION
// ============================================================================

const SUPPORTED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml']
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
const hasValidCours = ref(false)
const selectedImages = ref([])
const imagesInput = ref(null)
const selectedPdf = ref(null)
const pdfInput = ref(null)

// ============================================================================
// CONSTANTES DU FORMAT
// ============================================================================

const FORMAT_TEMPLATE = `=== [NOM DU COURS - SOUS-TITRE]
Difficulté: [easy/medium/hard]
Ordre: [numéro]

Titre: [Titre détaillé du cours]
Description: [Description courte expliquant l'objectif du cours]

<div style="background:#f9f9f9; padding:20px; border-radius:12px; font-family:Arial, sans-serif; line-height:1.6;">

    <h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">I. Définition</h2>
    <div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">
        <p>Une <strong>[CONCEPT PRINCIPAL]</strong> est [définition simple et claire].</p>
        <div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">
            $$[FORMULE DE BASE OU DEFINITION MATHEMATIQUE]$$
        </div>
        <p><strong>Explication :</strong> [Explication pédagogique du concept]</p>
    </div>

    <h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">II. [CONCEPT THEORIQUE PRINCIPAL]</h2>
    <div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">
        <p>[Explication du concept théorique principal]</p>
        <div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">
            $$[FORMULE PRINCIPALE A RETENIR]$$
        </div>
        <p><strong>💡 [CONSEIL IMPORTANT] :</strong> [Conseil méthodologique]</p>
    </div>

    <h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">III. Exemples détaillés</h2>

    <div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">
        <h3 style="color:#34495e; margin-top:0;">Exemple 1 : [TITRE SPECIFIQUE]</h3>
        <p><strong>Énoncé :</strong> [Description de l'exemple]</p>
        <p><strong>Données :</strong> [Valeurs numériques ou paramètres]</p>

        <p><strong>Résolution :</strong></p>
        <div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">
            <ul style="margin:0; padding-left:20px;">
                <li>$[Première étape de calcul]$</li>
                <li>$[Deuxième étape de calcul]$</li>
                <li>$[Troisième étape de calcul]$</li>
                <li>$[Conclusion de l'étape]$</li>
            </ul>
        </div>

        <div style="background:#ecf0f1; padding:10px; border-radius:4px; margin:10px 0;">
            <strong>Résultat final :</strong> [Conclusion de l'exemple]
        </div>
    </div>

    <div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">
        <h3 style="color:#34495e; margin-top:0;">Exemple 2 : [TITRE SPECIFIQUE]</h3>
        <p><strong>Situation :</strong> [Contexte de l'exemple]</p>

        <div style="text-align:center; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">
            $$[APPLICATION DE LA FORMULE]$$
        </div>

        <p><strong>Calculs détaillés :</strong></p>
        <div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">
            <ul style="margin:0; padding-left:20px;">
                <li>$[Calcul étape 1]$</li>
                <li>$[Calcul étape 2]$</li>
                <li>$[Résultat final]$</li>
            </ul>
        </div>

        <div style="background:#e8f5e8; padding:8px; border-radius:4px; margin:10px 0;">
            <strong>✅ Vérification :</strong> [Vérification du résultat]
        </div>
    </div>

    <h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">IV. [SECTION D'APPLICATION - CALCULS]</h2>

    <div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">
        <h3 style="color:#34495e; margin-top:0;">[SOUS-TITRE DE LA METHODE]</h3>
        <p>[Explication de la méthode ou du calcul principal]</p>

        <div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;">
            <strong>Formule [NOM DE LA FORMULE] :</strong><br>
            $$[FORMULE MATHEMATIQUE PRINCIPALE]$$
        </div>

        <div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">
            <strong>💡 Démarche à suivre :</strong><br>
            • [Étape 1 de la méthode]<br>
            • [Étape 2 de la méthode]<br>
            • [Étape 3 de la méthode]
        </div>
    </div>

    <div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">
        <h3 style="color:#34495e; margin-top:0;">Application pratique</h3>
        <p><strong>Problème :</strong> [Énoncé du problème d'application]</p>

        <div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;">
            <strong>Éléments donnés :</strong><br>
            • [Donnée 1]<br>
            • [Donnée 2]<br>
            • [Donnée 3]
        </div>

        <div style="text-align:center; margin:15px 0;">
            <strong>Résolution :</strong>
            <div style="font-size:1.1em; margin:10px 0; padding:10px; background:#ecf0f1; border-radius:4px;">
                $$[CALCUL DETAILLE ETAPE PAR ETAPE]$$
            </div>
        </div>

        <div style="background:#e8f5e8; padding:8px; border-radius:4px; margin:10px 0;">
            <strong>✅ Solution finale :</strong> [Résultat avec justification]
        </div>
    </div>

    <h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">V. Propriétés et caractéristiques</h2>
    <div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">
        <ul style="margin:0; padding-left:20px;">
            <li><strong>Propriété 1 :</strong> [Description de la première propriété importante]</li>
            <li><strong>Propriété 2 :</strong> [Description de la deuxième propriété importante]</li>
            <li><strong>Propriété 3 :</strong> [Description de la troisième propriété importante]</li>
            <li><strong>Aspect graphique :</strong> [Description de la représentation visuelle]</li>
        </ul>
    </div>

    <h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">VI. Erreurs fréquentes et conseils</h2>
    <div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">
        <div style="background:#fdf2f2; padding:12px; border-radius:4px; margin-bottom:10px;">
            <strong>❌ Pièges à éviter :</strong>
            <div style="margin:8px 0;">
                <ul style="margin:0; padding-left:20px;">
                    <li>[Erreur fréquente 1]</li>
                    <li>[Erreur fréquente 2]</li>
                    <li>[Erreur fréquente 3]</li>
                </ul>
            </div>
        </div>

        <div style="background:#f0f9f0; padding:12px; border-radius:4px;">
            <strong>✅ Conseils méthodologiques :</strong>
            <div style="margin:8px 0;">
                <ul style="margin:0; padding-left:20px;">
                    <li>[Conseil pratique 1]</li>
                    <li>[Conseil pratique 2]</li>
                    <li>[Conseil pratique 3]</li>
                </ul>
            </div>
        </div>
    </div>

</div>

===`

// ============================================================================
// CLASSES UTILITAIRES
// ============================================================================

/**
 * Classe pour gérer les images de cours
 */
class ImageManager {
  constructor() {
    this.images = new Map() // filename -> File
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
    return this.images.get(filename)
  }

  /**
   * Liste tous les noms d'images
   */
  getImageNames() {
    return Array.from(this.images.keys())
  }
}

const imageManager = new ImageManager()

// ============================================================================
// FONCTIONS UTILITAIRES
// ============================================================================

function getNotionName(notionId) {
  const notion = notions.value.find(n => n.id == notionId)
  return notion ? (notion.nom || notion.titre) : 'N/A'
}

// Helpers contextuels basés sur Notion
function getNotionById(id) {
  return notions.value.find(x => String(x.id) === String(id))
}

function notionContext(notion) {
  if (!notion) return { themeNom: '', matiereNom: '', paysNom: '', niveauNom: '' }
  const matiereNom = notion.matiere_nom || (notion.contexte_detail && notion.contexte_detail.matiere_nom) || ''
  const themeNom = notion.theme_nom || ''
  const paysNom = notion.contexte_detail && notion.contexte_detail.pays ? notion.contexte_detail.pays.nom : ''
  const niveauNom = notion.contexte_detail && notion.contexte_detail.niveau ? notion.contexte_detail.niveau.nom : ''
  return { matiereNom, themeNom, paysNom, niveauNom }
}

function formatNotionOption(n) {
  const ctx = notionContext(n)
  const parts = [
    n.nom || n.titre,
    ctx && ctx.matiereNom ? `— ${ctx.matiereNom}` : '',
    ctx && (ctx.paysNom || ctx.niveauNom) ? `— ${[ctx.paysNom, ctx.niveauNom].filter(Boolean).join(' · ')}` : ''
  ].filter(Boolean)
  return parts.join(' ')
}

function getDifficultyLabel(difficulty) {
  const labels = {
    'easy': 'Facile',
    'medium': 'Moyen',
    'hard': 'Difficile'
  }
  return labels[difficulty] || difficulty
}

function getImagePreview(file) {
  return URL.createObjectURL(file)
}

function getImageFile(filename) {
  return imageManager.getImage(filename)
}

function getPreviewImages(imageString, coursData = null) {
  const names = (imageString || '')
    .split(',')
    .map(n => n.trim())
    .filter(Boolean)
  return names.map((name, index) => {
    const file = getImageFile(name)
    return {
      id: `preview-${index}`,
      image: file ? URL.createObjectURL(file) : name,
      image_type: 'illustration',
      position: index + 1
    }
  })
}

function renderPreviewContent(cours) {
  const images = getPreviewImages(cours.image, cours)
  
  // Pour l'aperçu admin, remplacer les images manquantes par des placeholders
  let content = cours.contenu
  const imageNames = (cours.image || '').split(',').map(n => n.trim()).filter(Boolean)
  
  content = content.replace(/\[IMAGE_(\d+)\]/g, (match, position) => {
    const index = parseInt(position) - 1
    const imageName = imageNames[index]
    const imageFile = getImageFile(imageName)
    
    if (imageFile) {
      return `
        <div class="preview-image-container" style="text-align: center; margin: 2em 0;">
          <img src="${URL.createObjectURL(imageFile)}" alt="Image ${position}" class="content-image" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
          <div class="image-info" style="margin-top: 0.5rem; font-size: 0.875rem; color: #28a745; font-weight: 500;">✅ ${imageName}</div>
        </div>
      `
    } else {
      return `
        <div class="preview-image-placeholder">
          <div class="placeholder-icon">🖼️</div>
          <div class="placeholder-text">Image manquante: ${imageName || `IMAGE_${position}`}</div>
          <div class="placeholder-hint">Uploadez cette image dans la section ci-dessus</div>
        </div>
      `
    }
  })
  
  // Fallback: s'il n'y a PAS de marqueurs [IMAGE_X] mais qu'on a des images,
  // on les affiche automatiquement à la fin du contenu pour l'aperçu.
  if (!/\[IMAGE_\d+\]/.test(cours.contenu || '') && images.length > 0) {
    const autoGallery = images.map(img => `
      <div class="content-image-container" style="text-align: center; margin: 2em 0;">
        <img 
          src="${img.image}" 
          alt="Image ${img.position || ''}" 
          class="content-image"
          style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"
        />
      </div>
    `).join('\n')
    content = `${content}\n${autoGallery}`
  }
  
  // Utiliser le nouveau rendu Markdown
  return renderContentWithImages(content, images)
}

// ============================================================================
// GESTION DES IMAGES
// ============================================================================

function handleImagesSelect(event) {
  const files = Array.from(event.target.files)
  files.forEach(file => {
    try {
      imageManager.addImage(file)
      selectedImages.value.push(file)
    } catch (error) {
      console.error('Erreur lors de l\'ajout de l\'image:', error)
    }
  })
}

function handlePdfSelect(event) {
  const file = (event.target.files || [])[0]
  selectedPdf.value = file || null
}

function removeSelectedImage(index) {
  const file = selectedImages.value[index]
  imageManager.removeImage(file.name)
  selectedImages.value.splice(index, 1)
}

// ============================================================================
// PARSING ET VALIDATION
// ============================================================================

function parseCours(rawText) {
  const coursBlocks = rawText.split('===').filter(block => block.trim())
  const cours = []

  for (const block of coursBlocks) {
    try {
      const coursData = parseCoursBlock(block.trim())
      if (coursData) {
        cours.push(coursData)
      }
    } catch (error) {
      console.error('Erreur lors du parsing d\'un cours:', error)
    }
  }

  return cours
}

function parseCoursBlock(block) {
  const lines = block.split('\n')
  const cours = {
    titre: '',
    description: '',
    contenu: '',
    difficulty: 'medium',
    ordre: 0,
    image: '',
    matiere: null,
    notion: null
  }

  // Récupérer la notion sélectionnée
  if (selectedNotion.value) {
    const notionObj = notions.value.find(n => n.id == selectedNotion.value)
    if (notionObj) {
      cours.notion = notionObj.id
      cours.matiere = notionObj.matiere || (notionObj.contexte_detail && notionObj.contexte_detail.matiere)
    }
  }

  let currentSection = 'header'
  let contentLines = []

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim()
    
    if (!line) continue

    // Parse header
    if (currentSection === 'header') {
      if (line.startsWith('Difficulté:')) {
        cours.difficulty = line.split(':')[1].trim()
      } else if (line.startsWith('Ordre:')) {
        cours.ordre = parseInt(line.split(':')[1].trim()) || 0
      } else if (line.startsWith('Chapitre:')) {
        // Ignore, chapitre déduit via la notion
      } else if (line.toLowerCase().startsWith('image:') || line.toLowerCase().startsWith('images:')) {
        cours.image = line.split(':')[1].trim()
      } else if (line.startsWith('Titre:')) {
        cours.titre = line.split(':')[1].trim()
      } else if (line.startsWith('Description:')) {
        cours.description = line.split(':')[1].trim()
        currentSection = 'content'
      } else if (!cours.titre && !line.startsWith('===')) {
        cours.titre = line
      }
    } else {
      contentLines.push(line)
    }
  }

  cours.contenu = contentLines.join('\n')

  // Validation
  if (!cours.titre || !cours.contenu || !cours.notion) {
    console.warn('Cours invalide:', cours)
    return null
  }

  return cours
}

// ============================================================================
// ACTIONS
// ============================================================================

function handlePreview() {
  try {
    hasValidCours.value = true
    previewList.value = parseCours(rawInput.value)
    
    // Rendre le contenu MathJax après la prévisualisation
    nextTick(() => {
      renderMath()
    })
  } catch (error) {
    console.error('Erreur lors de la prévisualisation:', error)
    errorMsg.value = 'Erreur lors de la prévisualisation'
  }
}

async function handleCreate() {
  if (!selectedNotion.value) {
    errorMsg.value = 'Veuillez sélectionner une notion'
    return
  }

  // Vérifier que la notion sélectionnée existe
  const notionObj = notions.value.find(n => n.id == selectedNotion.value)
  if (!notionObj) {
    errorMsg.value = 'Notion invalide'
    return
  }

  console.log('Notion trouvée:', notionObj)

  try {
    const coursList = parseCours(rawInput.value)
    if (coursList.length === 0) {
      errorMsg.value = 'Aucun cours valide trouvé'
      return
    }

    let createdCount = 0
    let updatedCount = 0
    let errorCount = 0

    // Un cours par notion (OneToOne). Vérifier l'existant pour éviter 400.
    let existingCourseId = null
    try {
      const existingRes = await getCours(null, Number(selectedNotion.value))
      const list = Array.isArray(existingRes?.data) ? existingRes.data : (Array.isArray(existingRes) ? existingRes : [])
      if (list && list.length > 0) existingCourseId = list[0].id
    } catch (_) {}

    for (const coursData of coursList) {
      try {
        console.log('Création du cours avec les données:', coursData)
        // Créer le cours (payload minimal)
        const payload = {
          notion: Number(coursData.notion || selectedNotion.value),
          titre: coursData.titre,
          contenu: coursData.contenu,
          ordre: coursData.ordre || 0,
          difficulty: coursData.difficulty || 'medium'
        }
        let courseId
        if (existingCourseId) {
          // Mettre à jour l'existant
          const updated = await updateCours(existingCourseId, payload)
          courseId = updated?.id || existingCourseId
          updatedCount++
        } else {
          const { data: createdCours } = await createCours(payload)
          courseId = createdCours?.id
          createdCount++
          existingCourseId = courseId // empêcher 2 créations si plusieurs blocs
        }
        
        // Ajouter les images si présentes
        if (coursData.image && courseId) {
          const imageNames = coursData.image.split(',').map(name => name.trim()).filter(Boolean)
          for (let i = 0; i < imageNames.length; i++) {
            const imageFile = imageManager.getImage(imageNames[i])
            if (imageFile) {
              const payload = {
                cours: courseId,
                image: imageFile,
                image_type: 'illustration',
                position: i + 1
              }
              await createCoursImage(payload)
            }
          }
        }

        // Uploader le PDF si présent
        if (selectedPdf.value && courseId) {
          try {
            const formData = new FormData()
            formData.append('pdf_file', selectedPdf.value)
            await updateCoursFormData(courseId, formData)
          } catch (e) {
            console.error('Erreur upload PDF:', e)
          }
        }
      } catch (error) {
        console.error('Erreur lors de la création/mise à jour du cours:', error, error?.response?.data)
        errorCount++
      }
    }

    if (createdCount > 0 || updatedCount > 0) {
      successMsg.value = `${createdCount} créé(s)${updatedCount ? `, ${updatedCount} mis à jour` : ''}${errorCount > 0 ? `, ${errorCount} erreur(s)` : ''}`

      // Sauvegarder la notion actuelle avant de nettoyer le formulaire
      const currentNotion = selectedNotion.value

      // Nettoyer le formulaire
      rawInput.value = ''
      previewList.value = []
      selectedImages.value = []
      imageManager.images.clear()
      if (imagesInput.value) imagesInput.value.value = ''

      // Remettre la notion sélectionnée pour permettre d'ajouter d'autres cours dans la même notion
      selectedNotion.value = currentNotion
    } else {
      errorMsg.value = 'Aucun cours n\'a pu être créé'
    }
  } catch (error) {
    console.error('Erreur lors de la création:', error)
    errorMsg.value = 'Erreur lors de la création des cours'
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
    formatNotionOption(notion).toLowerCase().includes(filter)
  )
})

// ============================================================================
// INITIALISATION
// ============================================================================

onMounted(async () => {
  try {
    const nt = await getNotions()
    notions.value = Array.isArray(nt) ? nt : (nt?.data || [])
  } catch (error) {
    console.error('Erreur lors du chargement:', error)
  }
})

// Hook onActivated - force le rendu MathJax pour l'aperçu
onActivated(() => {
  nextTick(() => {
    renderMath()
    setTimeout(() => {
      renderMath()
    }, 100)
  })
})
</script>

<style src="@/styles/admin-common.css"></style>

<style scoped>
/* Styles spécifiques à AdminCoursPlus */
.preview-cours {
  background: #f8f9fa;
  border-radius: 6px;
  padding: 1rem;
}

.preview-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.ordre-badge {
  padding: 0.25rem 0.75rem;
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

.preview-description {
  margin-bottom: 1rem;
  color: #666;
  font-style: italic;
}

.preview-content {
  line-height: 1.6;
  color: #333;
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
  max-width: 100%;
}

.preview-content :deep(h1),
.preview-content :deep(h2),
.preview-content :deep(h3),
.preview-content :deep(h4),
.preview-content :deep(h5),
.preview-content :deep(h6) {
  color: #193e8e;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}

.preview-content :deep(p) {
  margin-bottom: 0.5rem;
}

.preview-content :deep(ul),
.preview-content :deep(ol) {
  margin-bottom: 0.5rem;
  padding-left: 1.5rem;
}

@media (max-width: 768px) {
  .preview-header {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style> 