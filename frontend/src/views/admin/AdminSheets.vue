<template>
  <div>
    <FormatHelp :format-template="FORMAT_TEMPLATE">
      <template #notes>
        <ul>
          <li>Utilisez <code>===</code> pour délimiter chaque fiche</li>
          <li><strong>⚠️ IMPORTANT :</strong> Sélectionnez d'abord la notion dans la liste déroulante ci-dessus</li>
          <li><strong>Champs obligatoires :</strong> <code>Titre</code> et contenu principal</li>
          <li><strong>Difficulté :</strong> <code>easy</code>, <code>medium</code> ou <code>hard</code> uniquement</li>
          <li><strong>Temps de lecture :</strong> Estimation en minutes (optionnel, défaut: 5)</li>
          <li><strong>Points clés :</strong> Résumé des concepts essentiels, séparés par des virgules</li>
          <li><strong>Sections :</strong> <code>=== CONTENU ===</code>, <code>=== EXEMPLES ===</code>, <code>=== CONSEILS ===</code></li>
          <li><strong>Contenu :</strong> Supporte HTML et LaTeX (MathJax)</li>
          <li><strong>MathJax :</strong> <code>$formule$</code> (inline) et <code>$$formule$$</code> (bloc)</li>
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
        <h4>📁 Images pour les fiches</h4>
        <p class="upload-help">Uploadez les images qui seront référencées dans vos fiches :</p>
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
        placeholder="Collez ici vos fiches de synthèse"
        class="sheets-textarea"
      ></textarea>
      
      <div class="btn-group">
        <button 
          class="btn-secondary" 
          @click="handlePreview" 
          :disabled="!rawInput.trim()"
          type="button"
        >
          Prévisualiser
        </button>
        <button 
          class="btn-primary" 
          @click="handleCreate" 
          :disabled="!selectedNotion || !rawInput.trim()"
        >
          Créer les fiches
        </button>
      </div>
    </div>

    <div v-if="successMsg" class="success-msg">{{ successMsg }}</div>
    <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>

    <!-- Aperçu -->
    <div v-if="previewList.length" class="preview-section">
      <h3>Aperçu ({{ previewList.length }})</h3>
      <div v-for="(sheet, idx) in previewList" :key="idx" class="preview-item">
        <h4>{{ sheet.titre }}</h4>
        <div class="preview-sheet">
          <div class="preview-header">
            <span class="difficulty-badge" :class="sheet.difficulty">{{ getDifficultyLabel(sheet.difficulty) }}</span>
            <span class="time-badge">{{ sheet.temps_lecture || 5 }} min</span>
        </div>
          <div v-if="sheet.points_cles" class="preview-keys">
            <strong>Points clés :</strong> {{ sheet.points_cles }}
        </div>
          <div class="preview-content" v-html="sheet.contenu"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getNotions } from '@/api'
import { createSynthesisSheet, createSynthesisImage } from '@/api/synthesis'
import FormatHelp from '@/components/admin/FormatHelp.vue'

// ============================================================================
// CONSTANTES DU FORMAT
// ============================================================================

const FORMAT_TEMPLATE = `Titre: [Titre de la fiche]
Difficulté: [easy/medium/hard]
Temps de lecture: [nombre en minutes]
Points clés: [point1,point2,point3]

=== CONTENU ===

[Contenu principal de la fiche avec HTML/LaTeX supporté]

=== EXEMPLES ===

[Exemples pratiques et exercices d'application]

=== CONSEILS ===

[Conseils méthodologiques et astuces]

===`

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
const selectedImages = ref([])
const imagesInput = ref(null)

// ============================================================================
// FONCTIONS DE PARSING
// ============================================================================

function parseSheets(rawText) {
  const blocks = rawText.split('===').filter(block => block.trim())
  const sheets = []

  for (const block of blocks) {
    try {
      const sheetData = parseSheetBlock(block.trim())
      if (sheetData) {
        sheets.push(sheetData)
      }
    } catch (error) {
      console.error('Erreur lors du parsing d\'une fiche:', error)
    }
  }

  return sheets
}

function parseSheetBlock(block) {
  const lines = block.split('\n')
  const sheet = {
    titre: '',
    contenu: '',
    difficulty: 'medium',
    temps_lecture: 5,
    points_cles: '',
    notion: selectedNotion.value
  }

  let currentSection = null
  let contentLines = []

  for (const line of lines) {
    const trimmed = line.trim()
    
    if (!trimmed) continue

    if (trimmed.startsWith('Titre:')) {
      sheet.titre = trimmed.slice(6).trim()
    } else if (trimmed.match(/^Difficult[eé]:/i)) {
      sheet.difficulty = trimmed.split(':')[1].trim().toLowerCase()
    } else if (trimmed.startsWith('Temps de lecture:')) {
      sheet.temps_lecture = parseInt(trimmed.split(':')[1].trim()) || 5
    } else if (trimmed.startsWith('Points clés:') || trimmed.startsWith('Points cles:')) {
      sheet.points_cles = trimmed.split(':')[1].trim()
    } else if (trimmed === '=== CONTENU ===') {
      currentSection = 'contenu'
    } else if (trimmed === '=== EXEMPLES ===') {
      currentSection = 'exemples'
    } else if (trimmed === '=== CONSEILS ===') {
      currentSection = 'conseils'
    } else if (currentSection) {
      contentLines.push(trimmed)
    }
  }

  sheet.contenu = contentLines.join('\n')

  // Validation
  if (!sheet.titre || !sheet.contenu || !sheet.notion) {
    return null
  }

  return sheet
}

// ============================================================================
// ACTIONS
// ============================================================================

function handlePreview() {
  try {
    previewList.value = parseSheets(rawInput.value)
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

  try {
    const sheetsList = parseSheets(rawInput.value)
    if (sheetsList.length === 0) {
      errorMsg.value = 'Aucune fiche valide trouvée'
      return
    }

    let createdCount = 0
    let errorCount = 0

    for (const sheetData of sheetsList) {
      try {
        const payload = {
          notion: Number(selectedNotion.value),
          titre: sheetData.titre,
          contenu: sheetData.contenu,
          difficulty: sheetData.difficulty || 'medium',
          reading_time_minutes: sheetData.temps_lecture || 5,
          key_points: sheetData.points_cles ? sheetData.points_cles.split(',').map(k => k.trim()) : [],
          est_actif: true
        }

        const created = await createSynthesisSheet(payload)
        const sheetId = created?.data?.id || created?.id

        // Uploader les images sélectionnées si présentes
        if (sheetId && selectedImages.value.length) {
          for (let i = 0; i < selectedImages.value.length; i++) {
            const file = selectedImages.value[i]
            await createSynthesisImage({
              sheet: sheetId,
              image: file,
              image_type: 'illustration',
              position: i + 1,
            })
          }
        }
        createdCount++
  } catch (error) {
        console.error('Erreur lors de la création de la fiche:', error)
        errorCount++
      }
    }

    if (createdCount > 0) {
      successMsg.value = `${createdCount} fiche(s) créée(s)${errorCount > 0 ? `, ${errorCount} erreur(s)` : ''}`
      
      // Sauvegarder la notion actuelle
      const currentNotion = selectedNotion.value
      
      // Nettoyer le formulaire
      rawInput.value = ''
      previewList.value = []
      selectedImages.value = []
      if (imagesInput.value) imagesInput.value.value = ''
      
      // Remettre la notion sélectionnée
      selectedNotion.value = currentNotion
    } else {
      errorMsg.value = 'Aucune fiche n\'a pu être créée'
    }
  } catch (error) {
    console.error('Erreur lors de la création:', error)
    errorMsg.value = 'Erreur lors de la création des fiches'
  }
}

function getDifficultyLabel(difficulty) {
  const labels = {
    'easy': 'Facile',
    'medium': 'Moyen',
    'hard': 'Difficile'
  }
  return labels[difficulty] || difficulty
}

// ============================================================================
// GESTION DES IMAGES
// ============================================================================

function handleImagesSelect(event) {
  const files = Array.from(event.target.files)
  selectedImages.value.push(...files)
}

function getImagePreview(file) {
  return URL.createObjectURL(file)
}

function removeSelectedImage(index) {
  selectedImages.value.splice(index, 1)
}

// ============================================================================
// COMPUTED PROPERTIES
// ============================================================================

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
</script>

<style src="@/styles/admin-common.css"></style>

<style scoped>
/* Styles spécifiques à AdminSheets */

.sheets-textarea {
  height: 200px;
  padding: 12px;
  border: 2px solid #d1d5db;
  border-radius: 6px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 0.9rem;
  line-height: 1.4;
  resize: vertical;
}

.preview-sheet {
  background: #f8f9fa;
  border-radius: 6px;
  padding: 1rem;
}

.preview-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  align-items: center;
}

.time-badge {
  padding: 0.25rem 0.75rem;
  background: #e0e7ff;
  color: #4338ca;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

.preview-keys {
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: #fffbeb;
  border-radius: 6px;
  font-size: 0.875rem;
}

.preview-content {
  line-height: 1.6;
  color: #333;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.preview-content :deep(h3),
.preview-content :deep(h4) {
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
</style>
