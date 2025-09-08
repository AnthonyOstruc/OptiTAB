<template>
  <div>
    <h2 class="admin-title">Bulk – Ajout de Cours</h2>
    <div class="format-help">
      <h3>📋 Format requis :</h3>
      <div class="format-example">
        <pre><code>=== [NOM DU COURS - SOUS-TITRE]
Difficulté: [easy/medium/hard]
Ordre: [numéro]

Titre: [Titre détaillé du cours]
Description: [Description courte expliquant l'objectif du cours]

&lt;div style="background:#f9f9f9; padding:20px; border-radius:12px; font-family:Arial, sans-serif; line-height:1.6;"&gt;

    &lt;h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;"&gt;I. Définition&lt;/h2&gt;
    &lt;div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;"&gt;
        &lt;p&gt;Une &lt;strong&gt;[CONCEPT PRINCIPAL]&lt;/strong&gt; est [définition simple et claire].&lt;/p&gt;
        &lt;div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;"&gt;
            $$[FORMULE DE BASE OU DEFINITION MATHEMATIQUE]$$
        &lt;/div&gt;
        &lt;p&gt;&lt;strong&gt;Explication :&lt;/strong&gt; [Explication pédagogique du concept]&lt;/p&gt;
    &lt;/div&gt;

    &lt;h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;"&gt;II. [CONCEPT THEORIQUE PRINCIPAL]&lt;/h2&gt;
    &lt;div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;"&gt;
        &lt;p&gt;[Explication du concept théorique principal]&lt;/p&gt;
        &lt;div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;"&gt;
            $$[FORMULE PRINCIPALE A RETENIR]$$
        &lt;/div&gt;
        &lt;p&gt;&lt;strong&gt;💡 [CONSEIL IMPORTANT] :&lt;/strong&gt; [Conseil méthodologique]&lt;/p&gt;
    &lt;/div&gt;

    &lt;h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;"&gt;III. Exemples détaillés&lt;/h2&gt;

    &lt;div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;"&gt;
        &lt;h3 style="color:#34495e; margin-top:0;"&gt;Exemple 1 : [TITRE SPECIFIQUE]&lt;/h3&gt;
        &lt;p&gt;&lt;strong&gt;Énoncé :&lt;/strong&gt; [Description de l'exemple]&lt;/p&gt;
        &lt;p&gt;&lt;strong&gt;Données :&lt;/strong&gt; [Valeurs numériques ou paramètres]&lt;/p&gt;

        &lt;p&gt;&lt;strong&gt;Résolution :&lt;/strong&gt;&lt;/p&gt;
        &lt;div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;"&gt;
            &lt;ul style="margin:0; padding-left:20px;"&gt;
                &lt;li&gt;$[Première étape de calcul]$&lt;/li&gt;
                &lt;li&gt;$[Deuxième étape de calcul]$&lt;/li&gt;
                &lt;li&gt;$[Troisième étape de calcul]$&lt;/li&gt;
                &lt;li&gt;$[Conclusion de l'étape]$&lt;/li&gt;
            &lt;/ul&gt;
        &lt;/div&gt;

        &lt;div style="background:#ecf0f1; padding:10px; border-radius:4px; margin:10px 0;"&gt;
            &lt;strong&gt;Résultat final :&lt;/strong&gt; [Conclusion de l'exemple]
        &lt;/div&gt;
    &lt;/div&gt;

    &lt;div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;"&gt;
        &lt;h3 style="color:#34495e; margin-top:0;"&gt;Exemple 2 : [TITRE SPECIFIQUE]&lt;/h3&gt;
        &lt;p&gt;&lt;strong&gt;Situation :&lt;/strong&gt; [Contexte de l'exemple]&lt;/p&gt;

        &lt;div style="text-align:center; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;"&gt;
            $$[APPLICATION DE LA FORMULE]$$
        &lt;/div&gt;

        &lt;p&gt;&lt;strong&gt;Calculs détaillés :&lt;/strong&gt;&lt;/p&gt;
        &lt;div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;"&gt;
            &lt;ul style="margin:0; padding-left:20px;"&gt;
                &lt;li&gt;$[Calcul étape 1]$&lt;/li&gt;
                &lt;li&gt;$[Calcul étape 2]$&lt;/li&gt;
                &lt;li&gt;$[Résultat final]$&lt;/li&gt;
            &lt;/ul&gt;
        &lt;/div&gt;

        &lt;div style="background:#e8f5e8; padding:8px; border-radius:4px; margin:10px 0;"&gt;
            &lt;strong&gt;✅ Vérification :&lt;/strong&gt; [Vérification du résultat]
        &lt;/div&gt;
    &lt;/div&gt;

    &lt;h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;"&gt;IV. [SECTION D'APPLICATION - CALCULS]&lt;/h2&gt;

    &lt;div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;"&gt;
        &lt;h3 style="color:#34495e; margin-top:0;"&gt;[SOUS-TITRE DE LA METHODE]&lt;/h3&gt;
        &lt;p&gt;[Explication de la méthode ou du calcul principal]&lt;/p&gt;

        &lt;div style="text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;"&gt;
            &lt;strong&gt;Formule [NOM DE LA FORMULE] :&lt;/strong&gt;&lt;br&gt;
            $$[FORMULE MATHEMATIQUE PRINCIPALE]$$
        &lt;/div&gt;

        &lt;div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;"&gt;
            &lt;strong&gt;💡 Démarche à suivre :&lt;/strong&gt;&lt;br&gt;
            • [Étape 1 de la méthode]&lt;br&gt;
            • [Étape 2 de la méthode]&lt;br&gt;
            • [Étape 3 de la méthode]
        &lt;/div&gt;
    &lt;/div&gt;

    &lt;div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;"&gt;
        &lt;h3 style="color:#34495e; margin-top:0;"&gt;Application pratique&lt;/h3&gt;
        &lt;p&gt;&lt;strong&gt;Problème :&lt;/strong&gt; [Énoncé du problème d'application]&lt;/p&gt;

        &lt;div style="background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;"&gt;
            &lt;strong&gt;Éléments donnés :&lt;/strong&gt;&lt;br&gt;
            • [Donnée 1]&lt;br&gt;
            • [Donnée 2]&lt;br&gt;
            • [Donnée 3]
        &lt;/div&gt;

        &lt;div style="text-align:center; margin:15px 0;"&gt;
            &lt;strong&gt;Résolution :&lt;/strong&gt;
            &lt;div style="font-size:1.1em; margin:10px 0; padding:10px; background:#ecf0f1; border-radius:4px;"&gt;
                $$[CALCUL DETAILLE ETAPE PAR ETAPE]$$
            &lt;/div&gt;
        &lt;/div&gt;

        &lt;div style="background:#e8f5e8; padding:8px; border-radius:4px; margin:10px 0;"&gt;
            &lt;strong&gt;✅ Solution finale :&lt;/strong&gt; [Résultat avec justification]
        &lt;/div&gt;
    &lt;/div&gt;

    &lt;h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;"&gt;V. Propriétés et caractéristiques&lt;/h2&gt;
    &lt;div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;"&gt;
        &lt;ul style="margin:0; padding-left:20px;"&gt;
            &lt;li&gt;&lt;strong&gt;Propriété 1 :&lt;/strong&gt; [Description de la première propriété importante]&lt;/li&gt;
            &lt;li&gt;&lt;strong&gt;Propriété 2 :&lt;/strong&gt; [Description de la deuxième propriété importante]&lt;/li&gt;
            &lt;li&gt;&lt;strong&gt;Propriété 3 :&lt;/strong&gt; [Description de la troisième propriété importante]&lt;/li&gt;
            &lt;li&gt;&lt;strong&gt;Aspect graphique :&lt;/strong&gt; [Description de la représentation visuelle]&lt;/li&gt;
        &lt;/ul&gt;
    &lt;/div&gt;

    &lt;h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;"&gt;VI. Erreurs fréquentes et conseils&lt;/h2&gt;
    &lt;div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;"&gt;
        &lt;div style="background:#fdf2f2; padding:12px; border-radius:4px; margin-bottom:10px;"&gt;
            &lt;strong&gt;❌ Pièges à éviter :&lt;/strong&gt;
            &lt;div style="margin:8px 0;"&gt;
                &lt;ul style="margin:0; padding-left:20px;"&gt;
                    &lt;li&gt;[Erreur fréquente 1]&lt;/li&gt;
                    &lt;li&gt;[Erreur fréquente 2]&lt;/li&gt;
                    &lt;li&gt;[Erreur fréquente 3]&lt;/li&gt;
                &lt;/ul&gt;
            &lt;/div&gt;
        &lt;/div&gt;

        &lt;div style="background:#f0f9f0; padding:12px; border-radius:4px;"&gt;
            &lt;strong&gt;✅ Conseils méthodologiques :&lt;/strong&gt;
            &lt;div style="margin:8px 0;"&gt;
                &lt;ul style="margin:0; padding-left:20px;"&gt;
                    &lt;li&gt;[Conseil pratique 1]&lt;/li&gt;
                    &lt;li&gt;[Conseil pratique 2]&lt;/li&gt;
                    &lt;li&gt;[Conseil pratique 3]&lt;/li&gt;
                &lt;/ul&gt;
            &lt;/div&gt;
        &lt;/div&gt;
    &lt;/div&gt;

&lt;/div&gt;

===</code></pre>
      </div>
      <div class="format-notes">
        <p><strong>Notes importantes :</strong></p>
        <ul>
          <li>Utilisez <code>===</code> pour délimiter chaque cours</li>
          <li><strong>⚠️ IMPORTANT :</strong> Sélectionnez d'abord le chapitre dans la liste déroulante ci-dessus</li>
          <li><strong>Chapitre :</strong> Le chapitre est automatiquement défini par votre sélection dans le dropdown</li>
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
      </div>
      

    </div>

    <div class="bulk-form">
      <select v-model="selectedChapitre" required>
        <option disabled value="">Choisir chapitre</option>
        <option v-for="c in chapitres" :key="c.id" :value="c.id">{{ formatChapitreOption(c) }}</option>
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
        <div v-if="selectedImages.length > 0" class="selected-images">
          <h5>Images sélectionnées :</h5>
          <div v-for="(img, index) in selectedImages" :key="index" class="selected-image-item">
            <img :src="getImagePreview(img)" :alt="img.name" class="image-preview" />
            <span class="image-name">{{ img.name }}</span>
            <button type="button" class="btn-remove" @click="removeSelectedImage(index)">×</button>
          </div>
        </div>
      </div>

      <textarea v-model="rawInput" placeholder="Coller ici vos cours…" rows="20"></textarea>
      <div class="btn-group">
        <button class="btn-secondary" @click="handlePreview" :disabled="!rawInput.trim()" type="button">Prévisualiser</button>
        <button class="btn-primary" @click="handleCreate" :disabled="!selectedChapitre || !rawInput.trim()">Créer les cours</button>
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
import { ref, onMounted, nextTick } from 'vue'
import { getChapitres, getNotions } from '@/api'
import { createCours, createCoursImage, getCours, updateCours } from '@/api/cours'
import { renderContentWithImages, renderMath, markdownToHtml } from '@/utils/scientificRenderer'

// ============================================================================
// CONSTANTES ET CONFIGURATION
// ============================================================================

const SUPPORTED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml']
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
const hasValidCours = ref(false)
const selectedImages = ref([])
const imagesInput = ref(null)

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
  return notion ? notion.nom : 'N/A'
}

// Helpers contextuels (comme AdminExercicesPlus)
function getNotionById(id) {
  return notions.value.find(x => String(x.id) === String(id))
}

function chapterContext(c) {
  if (!c) return null
  const notion = getNotionById(c.notion)
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
          <img src="${URL.createObjectURL(imageFile)}" alt="Image ${position}" class="preview-image" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
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
    chapitre: selectedChapitre.value,
    matiere: null,
    notion: null
  }

  // Récupérer la matière et notion à partir du chapitre sélectionné
  if (selectedChapitre.value) {
    const selectedChapitreObj = chapitres.value.find(c => c.id == selectedChapitre.value)
    if (selectedChapitreObj) {
      const notionObj = notions.value.find(n => n.id == selectedChapitreObj.notion)
      if (notionObj) {
        cours.notion = notionObj.id
        cours.matiere = notionObj.matiere
      }
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
        // Ignore, on utilise selectedChapitre
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
  if (!cours.titre || !cours.contenu || !cours.matiere || !cours.chapitre) {
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
  if (!selectedChapitre.value) {
    errorMsg.value = 'Veuillez sélectionner un chapitre'
    return
  }

  // Vérifier que le chapitre sélectionné a une notion et une matière
  const selectedChapitreObj = chapitres.value.find(c => c.id == selectedChapitre.value)
  if (!selectedChapitreObj) {
    errorMsg.value = 'Chapitre invalide'
    return
  }

  const notionObj = notions.value.find(n => n.id == selectedChapitreObj.notion)
  if (!notionObj) {
    errorMsg.value = 'Notion invalide pour ce chapitre'
    return
  }

  console.log('Chapitre sélectionné:', selectedChapitreObj)
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

    // Un cours par chapitre (OneToOne). Vérifier l'existant pour éviter 400.
    let existingCourseId = null
    try {
      const existingRes = await getCours(null, null, Number(selectedChapitre.value))
      const list = Array.isArray(existingRes?.data) ? existingRes.data : (Array.isArray(existingRes) ? existingRes : [])
      if (list && list.length > 0) existingCourseId = list[0].id
    } catch (_) {}

    for (const coursData of coursList) {
      try {
        console.log('Création du cours avec les données:', coursData)
        // Créer le cours (payload minimal)
        const payload = {
          chapitre: Number(coursData.chapitre),
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
      } catch (error) {
        console.error('Erreur lors de la création/mise à jour du cours:', error, error?.response?.data)
        errorCount++
      }
    }

    if (createdCount > 0 || updatedCount > 0) {
      successMsg.value = `${createdCount} créé(s)${updatedCount ? `, ${updatedCount} mis à jour` : ''}${errorCount > 0 ? `, ${errorCount} erreur(s)` : ''}`
      rawInput.value = ''
      previewList.value = []
      selectedImages.value = []
      imageManager.images.clear()
      if (imagesInput.value) imagesInput.value.value = ''
    } else {
      errorMsg.value = 'Aucun cours n\'a pu être créé'
    }
  } catch (error) {
    console.error('Erreur lors de la création:', error)
    errorMsg.value = 'Erreur lors de la création des cours'
  }
}

// ============================================================================
// INITIALISATION
// ============================================================================

onMounted(async () => {
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
})
</script>

<style scoped>
.admin-title {
  font-size: 2rem;
  color: #193e8e;
  margin-bottom: 2rem;
  text-align: center;
  font-weight: 800;
}

.format-help {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.format-help h3 {
  color: #193e8e;
  margin-bottom: 1rem;
}

.format-example {
  background: #2d3748;
  color: #e2e8f0;
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 1rem;
  overflow-x: auto;
}

.format-example pre {
  margin: 0;
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
}

.format-notes {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 6px;
  padding: 1rem;
}

.format-notes p {
  margin: 0 0 0.5rem 0;
  font-weight: 600;
}

.format-notes ul {
  margin: 0;
  padding-left: 1.5rem;
}

.format-notes li {
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.format-notes code {
  background: #f1f2f6;
  padding: 0.125rem 0.25rem;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
}

.bulk-form {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.bulk-form select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  margin-bottom: 1.5rem;
}

.images-upload-section {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.images-upload-section h4 {
  margin: 0 0 0.5rem 0;
  color: #193e8e;
}

.upload-help {
  color: #666;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.images-file-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.selected-images {
  margin-top: 1rem;
}

.selected-images h5 {
  margin: 0 0 0.5rem 0;
  color: #193e8e;
}

.selected-image-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border: 1px solid #eee;
  border-radius: 6px;
  margin-bottom: 0.5rem;
}

.image-preview {
  width: 40px;
  height: 30px;
  object-fit: cover;
  border-radius: 4px;
}

.image-name {
  flex: 1;
  font-size: 0.875rem;
}

.btn-remove {
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
}

.bulk-form textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  font-family: 'Courier New', monospace;
  resize: vertical;
  margin-bottom: 1rem;
}

.btn-group {
  display: flex;
  gap: 1rem;
}

.btn-primary {
  background: #193e8e;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
}

.btn-secondary {
  background: #6c757d;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
}

.btn-primary:disabled,
.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.success-msg {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.error-msg {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.info-msg {
  background: #d1ecf1;
  color: #0c5460;
  border: 1px solid #bee5eb;
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.preview-section {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
}

.preview-section h3 {
  color: #193e8e;
  margin-bottom: 1rem;
}

.preview-item {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  overflow: hidden;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.preview-item h4 {
  color: #193e8e;
  margin: 0 0 0.5rem 0;
}

.preview-image-info {
  margin-bottom: 1rem;
}

.image-indicator {
  font-weight: 600;
  color: #666;
}

.image-status-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.image-status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.image-status.available {
  background: #d4edda;
  color: #155724;
}

.image-status.missing {
  background: #f8d7da;
  color: #721c24;
}

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

.difficulty-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
}

.difficulty-badge.easy {
  background: #e8f5e8;
  color: #2e7d32;
}

.difficulty-badge.medium {
  background: #fff3e0;
  color: #f57c00;
}

.difficulty-badge.hard {
  background: #ffebee;
  color: #c62828;
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

.preview-image-placeholder {
  background: #f8f9fa;
  border: 2px dashed #dee2e6;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  margin: 1rem 0;
  color: #6c757d;
}

.placeholder-icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.placeholder-text {
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #dc3545;
}

.placeholder-hint {
  font-size: 0.875rem;
  color: #6c757d;
  font-style: italic;
}

.working-example {
  background: #e9ecef;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 2rem;
  margin-bottom: 2rem;
}

.working-example h4 {
  color: #193e8e;
  margin-bottom: 1rem;
}

.example-code {
  background: #2d3748;
  color: #e2e8f0;
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 1rem;
  overflow-x: auto;
}

.example-code pre {
  margin: 0;
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
}

.example-note {
  font-size: 0.875rem;
  color: #666;
  margin-top: 0.5rem;
}

@media (max-width: 768px) {
  .btn-group {
    flex-direction: column;
  }
  
  .preview-header {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .image-status-list {
    flex-direction: column;
  }
}
</style> 