<template>
  <div>
    <FormatHelp :format-template="FORMAT_TEMPLATE">
      <template #notes>
        <ul>
          <li>Utilisez <code>===</code> pour délimiter chaque fiche</li>
          <li><strong>Important :</strong> Sélectionnez d'abord la notion dans la liste</li>
          
          <li>Images multiples : séparez par virgules: <code>img1.jpg,img2.png</code></li>
          <li>Positionnement d'images : utilisez <code>[IMAGE_1]</code>, <code>[IMAGE_2]</code> dans le contenu</li>
          <li>Ordre des images : selon la déclaration (1 = [IMAGE_1], 2 = [IMAGE_2], ...)</li>
          <li>MathJax supporté : <code>$formule$</code> (inline), <code>$$formule$$</code> (bloc)</li>
          <li>Markdown supporté : <code>**gras**</code>, <code>*italique*</code></li>
          <li>Type de fiche : ajoutez <code>Type: summary|table</code> (sinon utilisez le sélecteur ci-dessous)</li>
          <li>Accès gratuit/premium : ajoutez <code>Access: free|paid|both</code> (sinon utilisez le sélecteur ci-dessous)</li>
        </ul>
      </template>
    </FormatHelp>

    <div class="bulk-form">
      <input v-model="notionFilter" type="text" placeholder="Filtrer les notions..." class="filter-input" />
      <select v-model="selectedNotion" required>
        <option disabled value="">Choisir notion</option>
        <option v-for="n in filteredNotions" :key="n.id" :value="n.id">{{ formatNotionOption(n) }}</option>
      </select>

      <label class="scope-label" for="access-scope-select">Accès</label>
      <select id="access-scope-select" v-model="selectedAccessScope" class="scope-select">
        <option v-for="opt in ACCESS_SCOPE_OPTIONS" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>

      <label class="scope-label" for="sheet-type-select">Type</label>
      <select id="sheet-type-select" v-model="selectedSheetType" class="scope-select">
        <option v-for="opt in SHEET_TYPE_OPTIONS" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>

      <!-- Upload d'images -->
      <div class="images-upload-section">
        <h4>Images pour les fiches</h4>
        <p class="upload-help">Uploadez les images référencées dans vos fiches :</p>
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
            <button type="button" class="btn-remove" @click="removeSelectedImage(index)">Supprimer</button>
          </div>
        </div>
      </div>

      <textarea v-model="rawInput" placeholder="Collez ici vos fiches de synthèse (Titre, Description, Images, contenu)"></textarea>
      <div class="btn-group">
        <button class="btn-secondary" @click="handlePreview" :disabled="!rawInput.trim()" type="button">Prévisualiser</button>
        <button class="btn-primary" @click="handleCreate" :disabled="!selectedNotion || !rawInput.trim()">{{ currentEditSheetId ? 'Mettre à jour' : 'Créer les fiches' }}</button>
        <button 
          v-if="currentEditSheetId" 
          class="btn-secondary" 
          type="button" 
          title="Annuler l'édition et revenir en mode création"
          @click="cancelEdit"
        >
          Nouvelle fiche
        </button>
      </div>
    </div>

    <div v-if="successMsg" class="success-msg">{{ successMsg }}</div>
    <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>
    <div v-if="previewList.length === 0 && rawInput.trim() && hasValidSheets" class="info-msg">Aucune fiche valide trouvée. Vérifiez le format.</div>

    <!-- Images enregistrées (mode édition) -->
    <div v-if="serverImages.length" class="server-images-section">
      <h5>Images de la fiche (enregistrées)</h5>
      <div v-if="imageManageLoading" class="muted">Chargement…</div>
      <table v-else class="images-table">
        <thead>
          <tr>
            <th>Aperçu</th>
            <th>Type</th>
            <th>Position</th>
            <th>Légende</th>
            <th>Remplacer</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(img, i) in serverImages" :key="img.id || i">
            <td style="width:120px">
              <img :src="img.image" alt="apercu" class="srv-preview" />
            </td>
            <td>
              <select v-model="img.image_type">
                <option value="illustration">Illustration</option>
              </select>
            </td>
            <td style="width:100px">
              <input v-model.number="img.position" type="number" min="0" />
            </td>
            <td>
              <input v-model="img.caption" placeholder="Légende" />
            </td>
            <td>
              <input type="file" accept="image/*" @change="onSelectReplaceFile(i, $event)" />
            </td>
            <td>
              <div class="img-row-actions">
                <button type="button" class="btn-primary small" @click="saveImageRow(currentEditSheetId, img, i)">Sauvegarder</button>
                <button type="button" class="btn-secondary small" :disabled="!img._file" @click="replaceImageRow(currentEditSheetId, img, i)">Remplacer</button>
                <button type="button" class="btn-danger small" @click="deleteImageRow(currentEditSheetId, img, i)">Supprimer</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="add-image-form">
        <h6>Ajouter une image</h6>
        <div class="add-image-row">
          <select v-model="newImage.image_type">
            <option value="illustration">Illustration</option>
          </select>
          <input v-model.number="newImage.position" type="number" min="0" placeholder="Position" />
          <input v-model="newImage.caption" type="text" placeholder="Légende (optionnel)" />
          <input type="file" accept="image/*" @change="onSelectNewImage($event)" />
          <button type="button" class="btn-primary small" :disabled="!newImage.file" @click="addNewImage(currentEditSheetId)">Ajouter</button>
        </div>
      </div>
      <p class="muted" style="margin-top:6px">Astuce: "Remplacer" met à jour l'image de la même ligne. Utilisez "Supprimer" pour retirer une image.</p>
    </div>

    <!-- Aperçu -->
    <div v-if="previewList.length" class="preview-section">
      <h3>Aperçu ({{ previewList.length }})</h3>
      <div v-for="(sheet, idx) in previewList" :key="idx" class="preview-item">
        <h4>{{ sheet.titre }}</h4>
        <div v-if="sheet.image" class="preview-image-info">
          <span class="image-indicator">Images: {{ sheet.image }}</span>
          <div class="image-status-list">
            <span 
              v-for="imgName in sheet.image.split(',').map(name => name.trim()).filter(Boolean)" 
              :key="imgName"
              :class="['image-status', imageExists(imgName) ? 'available' : 'missing']"
            >
              {{ imgName }}: {{ imageExists(imgName) ? 'Disponible' : 'Manquante' }}
            </span>
          </div>
        </div>
        <div class="preview-sheet">
          <div class="preview-header">
            <span class="time-badge">{{ Math.max(1, Math.round((sheet.summary || '').split(/\s+/).length / 200)) }} min</span>
          </div>
          <div class="preview-content" v-html="renderPreviewContent(sheet)"></div>
        </div>
      </div>
    </div>

    <!-- Filtres -->
    <div class="filters">
      <div class="filter-group">
        <label>Filtrer par notion:</label>
        <input v-model="notionTableFilter" type="text" placeholder="Filtrer les notions..." class="filter-input" />
        <select v-model="filters.notion">
          <option value="all">Toutes les notions</option>
          <option v-for="notion in filteredNotionsForFilter" :key="notion.id" :value="notion.id">
            {{ formatNotionOption(notion) }}
          </option>
        </select>
      </div>
      <div class="filter-group">
        <label>Filtrer par type:</label>
        <select v-model="filters.sheet_type">
          <option value="all">Tous les types</option>
          <option v-for="opt in SHEET_TYPE_OPTIONS" :key="`filter-${opt.value}`" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>
      </div>
    </div>

    <!-- Tableau des fiches de synthèse -->
    <table class="admin-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Titre</th>
          <th>Type</th>
          <th>Notion</th>
          <th>Contexte</th>
          <th>Accès</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="isLoadingSheets">
          <td colspan="7" class="loading-row">Chargement des fiches...</td>
        </tr>
        <template v-else>
          <tr v-for="s in paginatedSheets" :key="s.id">
            <td>{{ s.id }}</td>
            <td>{{ s.titre }}</td>
            <td>
              <select
                class="scope-select-inline"
                :value="normalizeSheetType(s.sheet_type)"
                :disabled="isLoadingSheets || isUpdatingSheetType(s.id) || isUpdatingAccessScope(s.id)"
                @change="handleChangeSheetType(s, $event)"
              >
                <option v-for="opt in SHEET_TYPE_OPTIONS" :key="`table-row-${opt.value}`" :value="opt.value">
                  {{ opt.label }}
                </option>
              </select>
            </td>
            <td>{{ getNotionName(s.notion) }}</td>
             <td class="ctx-cell">{{ getNotionContextLabel(s.notion) }}</td>
             <td>
                <select
                  class="scope-select-inline"
                  :class="accessScopeBadgeClass(s.access_scope)"
                  :value="normalizeAccessScope(s.access_scope)"
                  :disabled="isLoadingSheets || isUpdatingAccessScope(s.id) || isUpdatingSheetType(s.id)"
                  @change="handleChangeAccessScope(s, $event)"
                >
                  <option v-for="opt in ACCESS_SCOPE_OPTIONS" :key="opt.value" :value="opt.value">
                    {{ opt.label }}
                  </option>
                </select>
              </td>
            <td>
              <AdminActionsButtons
                :item="s"
                :actions="['edit', 'duplicate', 'delete']"
                edit-label="Éditer"
                duplicate-label="Dupliquer"
                confirm-message="Êtes-vous sûr de vouloir supprimer cette fiche ?"
                @edit="editSheet"
                @duplicate="handleDuplicateSheet"
                @delete="handleDeleteSheet"
              />
            </td>
          </tr>
          <tr v-if="paginatedSheets.length === 0">
            <td colspan="7" style="text-align:center; font-style: italic;">Aucune fiche trouvée.</td>
          </tr>
        </template>
      </tbody>
    </table>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="pagination">
      <button 
        class="pagination-btn" 
        @click="prevPage" 
        :disabled="currentPage === 1 || isLoadingSheets"
      >
        Précédent
      </button>
      
      <div class="pagination-numbers">
        <button
          v-for="page in displayedPages"
          :key="page"
          class="pagination-number"
          :class="{ active: page === currentPage }"
          @click="goToPage(page)"
          :disabled="isLoadingSheets"
        >
          {{ page }}
        </button>
      </div>
      
      <button 
        class="pagination-btn" 
        @click="nextPage" 
        :disabled="currentPage === totalPages || isLoadingSheets"
      >
        Suivant
      </button>
    </div>
    
    <div v-if="totalPages > 1" class="pagination-info">
      Page {{ currentPage }} sur {{ totalPages }} ({{ totalSheets }} fiches au total)
    </div>
  </div>
  
</template>

<script setup>
import { ref, computed, onMounted, onActivated, nextTick, watch } from 'vue'
import { getNotions, apiClient } from '@/api'
import { getSynthesisSheets, getSynthesisSheet, createSynthesisSheet, updateSynthesisSheet, createSynthesisImage, deleteSynthesisSheet, duplicateSynthesisSheet, updateSynthesisImage, deleteSynthesisImage } from '@/api/synthesis'
import { renderContentWithImages, renderMath, getImageUrl } from '@/utils/scientificRenderer'
import FormatHelp from '@/components/admin/FormatHelp.vue'
import { AdminActionsButtons } from '@/components/admin'

// ============================================================================
// CONSTANTES ET ÉTAT
// ============================================================================

const SUPPORTED_IMAGE_TYPES = [
  'image/jpeg',
  'image/jpg',
  'image/png',
  'image/gif',
  'image/webp',
  'image/svg+xml',
  'image/heic',
  'image/heif',
  'image/avif',
  'image/bmp',
  'image/tiff'
]
const SUPPORTED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.heic', '.heif', '.avif', '.bmp', '.tif', '.tiff']
const MAX_IMAGE_SIZE = 20 * 1024 * 1024 // 20MB
const MAX_IMAGE_SIZE_MB = Math.round(MAX_IMAGE_SIZE / (1024 * 1024))

function getFileExtension(fileName = '') {
  const cleanName = String(fileName || '').trim().toLowerCase()
  const dotIndex = cleanName.lastIndexOf('.')
  if (dotIndex < 0) return ''
  return cleanName.slice(dotIndex)
}

function getFileFingerprint(file) {
  return `${String(file?.name || '').toLowerCase()}::${Number(file?.size || 0)}::${Number(file?.lastModified || 0)}`
}

function validateImageFile(file) {
  if (!file) return { ok: false, reason: 'Fichier image manquant.' }

  const mimeType = String(file.type || '').trim().toLowerCase()
  const extension = getFileExtension(file.name)
  const isMimeSupported = Boolean(mimeType) && SUPPORTED_IMAGE_TYPES.includes(mimeType)
  const isExtensionSupported = !mimeType && SUPPORTED_IMAGE_EXTENSIONS.includes(extension)

  if (!isMimeSupported && !isExtensionSupported) {
    return {
      ok: false,
      reason: `Type non supporte pour "${file.name}". Formats acceptes: JPG, PNG, GIF, WebP, SVG, HEIC, HEIF, AVIF, BMP, TIFF.`
    }
  }

  if (Number(file.size || 0) > MAX_IMAGE_SIZE) {
    return {
      ok: false,
      reason: `"${file.name}" depasse la taille maximale autorisee (${MAX_IMAGE_SIZE_MB} MB).`
    }
  }

  return { ok: true }
}

function extractApiErrorMessage(error, fallback = 'Erreur inconnue') {
  const data = error?.response?.data
  if (!data) return fallback

  if (typeof data === 'string' && data.trim()) return data.trim()

  const direct = data?.detail || data?.message || data?.error
  if (typeof direct === 'string' && direct.trim()) return direct.trim()
  if (Array.isArray(direct) && direct.length) return String(direct[0])

  const preferredKeys = ['image', 'sheet', 'non_field_errors']
  for (const key of preferredKeys) {
    const value = data?.[key]
    if (typeof value === 'string' && value.trim()) return value.trim()
    if (Array.isArray(value) && value.length) return String(value[0])
  }

  for (const value of Object.values(data || {})) {
    if (typeof value === 'string' && value.trim()) return value.trim()
    if (Array.isArray(value) && value.length) return String(value[0])
  }

  return fallback
}

function summarizeFailures(items = [], maxItems = 4) {
  if (!Array.isArray(items) || items.length === 0) return ''
  const list = items.slice(0, maxItems).join(' | ')
  const remaining = items.length - Math.min(items.length, maxItems)
  return remaining > 0 ? `${list} (+${remaining} autre(s))` : list
}

const notions = ref([])
const sheets = ref([])
const notionFilter = ref('')
const selectedNotion = ref('')
const rawInput = ref('')
const successMsg = ref('')
const errorMsg = ref('')
const previewList = ref([])
const hasValidSheets = ref(false)
const selectedImages = ref([])
const imagesInput = ref(null)
// Images déjà enregistrées pour la fiche en édition
const serverImages = ref([])
const imageManageLoading = ref(false)
const currentEditSheetId = ref(null)

// Filtres et pagination pour le tableau (mêmes patterns que AdminCours)
const filters = ref({ notion: 'all', sheet_type: 'all' })
const notionTableFilter = ref('')
const currentPage = ref(1)
const itemsPerPage = 5
const totalSheets = ref(0)
const isLoadingSheets = ref(false)
const ACCESS_SCOPE_OPTIONS = [
  { value: 'paid', label: 'Premium (abonnés)' },
  { value: 'free', label: 'Gratuit' },
  { value: 'both', label: 'Gratuit + Premium' }
]
const selectedAccessScope = ref('paid')
const SHEET_TYPE_OPTIONS = [
  { value: 'summary', label: 'Synthèse' },
  { value: 'table', label: 'Tables & Formules' }
]
const selectedSheetType = ref('summary')

// ============================================================================
// FORMAT D'ENTRÉE (exemple copiable)
// ============================================================================

const FORMAT_TEMPLATE = `=== [NOM DE LA FICHE - SOUS-TITRE]
Images: [image1.png,image2.jpg]
Type: summary
Access: free

Titre: [Titre de la fiche]

## Résumé
Contenu principal de la fiche: texte, listes, formules, etc.
- Point clé 1
- Point clé 2

[IMAGE_1]

### Formule principale
$$a^2 + b^2 = c^2$$

### Exemple
Voici un exemple avec [IMAGE_2]

`

// ============================================================================
// CLASSE DE GESTION D'IMAGES
// ============================================================================

class ImageManager {
  constructor() {
    this.images = new Map()
  }
  addImage(file) {
    const validation = validateImageFile(file)
    if (!validation.ok) throw new Error(validation.reason)

    const existing = this.images.get(file.name)
    if (existing && getFileFingerprint(existing) !== getFileFingerprint(file)) {
      throw new Error(`Un fichier nommé "${file.name}" existe déjà. Renommez le fichier avant import.`)
    }
    this.images.set(file.name, file)
  }
  removeImage(filename) { this.images.delete(filename) }
  getImage(filename) { return this.images.get(filename) }
  clear() { this.images.clear() }
}

const imageManager = new ImageManager()
// Mémoire locale des noms déclarés dans "Images:" par fiche (clé: notionId::titre)
const lastDeclaredImagesByKey = (typeof window !== 'undefined')
  ? (window.__lastDeclaredSheetImages ||= new Map())
  : new Map()

function getSheetKey(notionId, title, sheetType = 'summary') {
  return `${String(notionId || '')}::${String((title || '').toLowerCase())}::${normalizeSheetType(sheetType)}`
}

// ============================================================================
// HELPERS NOTIONS ET AFFICHAGE
// ============================================================================

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
    ctx && ctx.matiereNom ? `- ${ctx.matiereNom}` : '',
    ctx && (ctx.paysNom || ctx.niveauNom) ? `- ${[ctx.paysNom, ctx.niveauNom].filter(Boolean).join(' / ')}` : ''
  ].filter(Boolean)
  return parts.join(' ')
}

// Difficulté supprimée

function getImagePreview(file) { return URL.createObjectURL(file) }
function getImageFile(filename) { return imageManager.getImage(filename) }

function getPreviewImages(imageString) {
  const names = (imageString || '')
    .split(',')
    .map(n => n.trim())
    .filter(Boolean)

  // Helper pour retrouver une image serveur par son basename
  const findServerImageByName = (basename) => {
    try {
      const bn = String(basename).split('?')[0].split('/').pop()
      return (serverImages.value || []).find(si => {
        const siBn = String(si.image || '').split('?')[0].split('/').pop()
        return siBn && bn && siBn.toLowerCase() === bn.toLowerCase()
      })
    } catch (_) { return null }
  }

  let list = []
  if (names.length > 0) {
    list = names.map((name, index) => {
      const file = getImageFile(name)
      if (file) {
        return { id: `preview-${index}`,
          image: URL.createObjectURL(file), image_type: 'illustration', position: index + 1 }
      }
      const srv = findServerImageByName(name)
      if (srv) {
        return { id: srv.id || `srv-${index}`, image: srv.image, image_type: srv.image_type || 'illustration', position: srv.position || (index + 1) }
      }
      // Fallback: construire l’URL media en dossier synthesis_images
      return { id: `fallback-${index}`, image: getImageUrl(name, 'synthesis'), image_type: 'illustration', position: index + 1 }
    })
  } else if (serverImages.value && serverImages.value.length) {
    // Mode édition: pas de noms fournis mais images serveur disponibles
    list = serverImages.value.map((si, idx) => ({
      id: si.id || `srv-${idx}`,
      image: si.image,
      image_type: si.image_type || 'illustration',
      position: si.position || (idx + 1)
    }))
  }

  // Ordonner par position pour respecter [IMAGE_1], [IMAGE_2], ...
  return list.sort((a, b) => (a.position || 0) - (b.position || 0))
}

function renderPreviewContent(sheet) {
  const images = getPreviewImages(sheet.image)
  let content = sheet.summary || ''

  // Inject images by markers; if no markers and images provided, append gallery
  if (!/\[IMAGE_\d+\]/.test(content || '') && images.length > 0) {
    const autoGallery = images.map(img => `
      <div class="content-image-container" style="text-align: center; margin: 2em 0;">
        <img src="${img.image}" alt="Image ${img.position || ''}" class="content-image" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
      </div>
    `).join('\n')
    content = `${content}\n${autoGallery}`
  }

  return renderContentWithImages(content, images)
}

// ============================================================================
// GESTION DES IMAGES
// ============================================================================

function handleImagesSelect(event) {
  const input = event?.target
  const files = Array.from(input?.files || [])
  if (files.length === 0) return

  const existingFingerprints = new Set((selectedImages.value || []).map(getFileFingerprint))
  const rejected = []

  files.forEach(file => {
    const validation = validateImageFile(file)
    if (!validation.ok) {
      rejected.push(validation.reason)
      return
    }

    const fingerprint = getFileFingerprint(file)
    if (existingFingerprints.has(fingerprint)) {
      rejected.push(`"${file.name}" est deja selectionne.`)
      return
    }

    try {
      imageManager.addImage(file)
      selectedImages.value.push(file)
      existingFingerprints.add(fingerprint)
    } catch (e) {
      console.error('Image invalide:', e)
      rejected.push(e?.message || `Impossible d'ajouter "${file.name}".`)
    }
  })

  if (input) input.value = ''
  if (imagesInput.value) imagesInput.value.value = ''

  if (rejected.length > 0) {
    errorMsg.value = `Certaines images n'ont pas ete ajoutees: ${summarizeFailures(rejected, 5)}`
  } else {
    errorMsg.value = ''
  }
}

// Verifie si une image est disponible soit localement (selectionnee) soit cote serveur (deja enregistree)
function imageExists(filename) {
  if (!filename) return false
  const file = getImageFile(filename)
  if (file) return true
  try {
    const bn = String(filename).split('?')[0].split('/').pop()
    return (serverImages.value || []).some(si => {
      const siBn = String(si.image || '').split('?')[0].split('/').pop()
      return siBn && bn && siBn.toLowerCase() === bn.toLowerCase()
    })
  } catch (_) {
    return false
  }
}

function removeSelectedImage(index) {
  const file = selectedImages.value[index]
  imageManager.removeImage(file.name)
  selectedImages.value.splice(index, 1)
}

// ============================================================================
// ACCESS SCOPE HELPERS
// ============================================================================

const ACCESS_SCOPE_LABELS = {
  paid: 'Premium',
  free: 'Gratuit',
  both: 'Gratuit + Premium'
}
const SHEET_TYPE_LABELS = {
  summary: 'Synthèse',
  table: 'Tables & Formules'
}

const DEFAULT_ACCESS_SCOPE = 'paid'
const DEFAULT_SHEET_TYPE = 'summary'
const accessScopeUpdatingIds = ref(new Set())
const sheetTypeUpdatingIds = ref(new Set())

function normalizeAccessScope(value) {
  const v = String(value || '').trim()
  if (v === 'free' || v === 'paid' || v === 'both') return v
  return DEFAULT_ACCESS_SCOPE
}

const normalizeString = (value = '') => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()

function normalizeSheetType(value) {
  const v = String(value || '').trim().toLowerCase()
  if (v === 'table') return 'table'
  return DEFAULT_SHEET_TYPE
}

function parseSheetTypeToken(rawValue = '') {
  const cleanValue = normalizeString(String(rawValue || '').trim())
  if (!cleanValue) return null
  if (cleanValue === 'table') return 'table'
  if (cleanValue === 'summary') return 'summary'
  if (cleanValue.includes('summary') || cleanValue.includes('synthese') || cleanValue.includes('synth')) return 'summary'
  if (cleanValue.includes('tableau') || cleanValue.includes('tableaux')) return 'table'
  if (cleanValue.includes('formule') || cleanValue.includes('formules')) return 'table'
  return null
}

function sheetTypeLabel(value) {
  const normalized = normalizeSheetType(value)
  return SHEET_TYPE_LABELS[normalized] || 'Synthèse'
}

function getSheetIdentityKey(title, sheetType) {
  return `${String(title || '').toLowerCase()}::${normalizeSheetType(sheetType)}`
}

function parseAccessScopeToken(rawValue = '') {
  const cleanValue = normalizeString(String(rawValue || '').trim())
  if (!cleanValue) return null
  if (cleanValue.includes('both') || (cleanValue.includes('gratuit') && cleanValue.includes('premium'))) return 'both'
  if (cleanValue.includes('free') || cleanValue.includes('gratuit')) return 'free'
  if (cleanValue.includes('paid') || cleanValue.includes('premium') || cleanValue.includes('abonne')) return 'paid'
  return null
}

function accessScopeLabel(value) {
  const normalized = normalizeAccessScope(value)
  return ACCESS_SCOPE_LABELS[normalized] || ACCESS_SCOPE_OPTIONS.find(opt => opt.value === normalized)?.label || 'Premium'
}

function accessScopeBadgeClass(value) {
  const normalized = normalizeAccessScope(value)
  if (normalized === 'free') return 'scope-pill scope-pill--free'
  if (normalized === 'both') return 'scope-pill scope-pill--both'
  return 'scope-pill scope-pill--paid'
}

function isUpdatingAccessScope(id) {
  return accessScopeUpdatingIds.value.has(Number(id))
}

function isUpdatingSheetType(id) {
  return sheetTypeUpdatingIds.value.has(Number(id))
}

async function handleChangeAccessScope(targetSheet, event) {
  if (!targetSheet?.id) return
  const nextValue = normalizeAccessScope(event?.target?.value)
  const currentValue = normalizeAccessScope(targetSheet.access_scope)
  if (nextValue === currentValue) return

  const previousValue = targetSheet.access_scope
  targetSheet.access_scope = nextValue
  accessScopeUpdatingIds.value.add(Number(targetSheet.id))

  try {
    // Le serializer backend exige "summary" (même en PATCH), donc on l'envoie inchangé.
    let summaryValue = targetSheet.summary
    if (!summaryValue) {
      try {
        const res = await getSynthesisSheet(targetSheet.id)
        summaryValue = res?.data?.summary ?? res?.summary ?? ''
      } catch (_) {
        summaryValue = ''
      }
    }

    await apiClient.patch(`/api/sheets/${targetSheet.id}/`, {
      access_scope: nextValue,
      summary: summaryValue
    })
  } catch (e) {
    console.error('[AdminSheets] Erreur update access_scope:', e)
    targetSheet.access_scope = previousValue
    alert('Erreur lors de la mise à jour de l’accès')
  } finally {
    accessScopeUpdatingIds.value.delete(Number(targetSheet.id))
  }
}

async function handleChangeSheetType(targetSheet, event) {
  if (!targetSheet?.id) return
  const nextValue = normalizeSheetType(event?.target?.value)
  const currentValue = normalizeSheetType(targetSheet.sheet_type)
  if (nextValue === currentValue) return

  const previousValue = targetSheet.sheet_type
  targetSheet.sheet_type = nextValue
  sheetTypeUpdatingIds.value.add(Number(targetSheet.id))

  try {
    // Le serializer backend exige "summary" (meme en PATCH), donc on l'envoie inchange.
    let summaryValue = targetSheet.summary
    if (!summaryValue) {
      try {
        const res = await getSynthesisSheet(targetSheet.id)
        summaryValue = res?.data?.summary ?? res?.summary ?? ''
      } catch (_) {
        summaryValue = ''
      }
    }

    await apiClient.patch(`/api/sheets/${targetSheet.id}/`, {
      sheet_type: nextValue,
      summary: summaryValue
    })
  } catch (e) {
    console.error('[AdminSheets] Erreur update sheet_type:', e)
    targetSheet.sheet_type = previousValue
    const backendMessage = e?.response?.data?.non_field_errors?.[0]
      || e?.response?.data?.sheet_type?.[0]
      || e?.response?.data?.detail
    alert(backendMessage || 'Erreur lors de la mise a jour du type')
  } finally {
    sheetTypeUpdatingIds.value.delete(Number(targetSheet.id))
  }
}

// ============================================================================
// PARSING
// ============================================================================

function parseSheets(rawText) {
  const blocks = rawText.split('===').filter(b => b.trim())
  const out = []
  for (const block of blocks) {
    // Ne pas trim ici pour préserver les espaces et lignes vides du contenu
    const d = parseSheetBlock(block)
    if (d) out.push(d)
  }
  return out
}

function parseSheetBlock(block) {
  const lines = block.split('\n')
  const sheet = {
    titre: '',
    summary: '',
    image: '',
    notion: null,
    access_scope: null,
    sheet_type: normalizeSheetType(selectedSheetType.value || DEFAULT_SHEET_TYPE)
  }

  if (selectedNotion.value) sheet.notion = Number(selectedNotion.value)

  let currentSection = 'header'
  let contentLines = []

  for (let i = 0; i < lines.length; i++) {
    const rawLine = (lines[i] ?? '')
    const line = rawLine.trim()

    if (currentSection === 'header') {
      if (!line) continue

      const normalizedLine = normalizeString(line)

      // Helpers pour récupérer le texte après le premier ':'
      const afterColonTrim = (l) => l.split(':').slice(1).join(':').trim()
      const afterColonRaw = (l) => {
        const idx = l.indexOf(':')
        return idx >= 0 ? l.slice(idx + 1) : ''
      }

      if (normalizedLine.startsWith('access:') || normalizedLine.startsWith('acces:')) {
        sheet.access_scope = parseAccessScopeToken(afterColonTrim(rawLine))
        continue
      }

      if (normalizedLine.startsWith('type:') || normalizedLine.startsWith('type :')) {
        sheet.sheet_type = parseSheetTypeToken(afterColonTrim(rawLine)) || sheet.sheet_type
        continue
      }

      if (line.toLowerCase().startsWith('image:') || line.toLowerCase().startsWith('images:')) {
        sheet.image = afterColonTrim(rawLine)
      } else if (line.startsWith('Titre:')) {
        sheet.titre = afterColonTrim(rawLine)
      } else if (line.startsWith('Description:')) {
        // Passer en mode contenu et conserver exactement ce qui suit ':'
        currentSection = 'content'
        const firstContent = afterColonRaw(rawLine)
        // Ne pas trim: respecter l'espacement initial
        contentLines.push(firstContent)
      } else if (!sheet.titre && !line.startsWith('===')) {
        // Titre libre sur une ligne sans préfixe
        sheet.titre = rawLine
      } else {
        // Tout le reste est considéré comme contenu, et on conserve la ligne telle quelle
        currentSection = 'content'
        contentLines.push(rawLine)
      }
    } else {
      // Section contenu: conserver exactement la ligne (y compris vides)
      contentLines.push(rawLine)
    }
  }

  sheet.summary = contentLines.join('\n')
  sheet.sheet_type = normalizeSheetType(sheet.sheet_type || selectedSheetType.value || DEFAULT_SHEET_TYPE)

  // Si aucune ligne Images n'a été fournie, utiliser par défaut les noms
  // des images actuellement sélectionnées (pour éviter toute perte au submit)
  if (!sheet.image && selectedImages.value && selectedImages.value.length) {
    sheet.image = selectedImages.value.map(f => f.name).join(',')
  }

  // Mémo: enregistrer les noms déclarés pour cette fiche (utilisé en fallback en édition)
  if (sheet.notion && sheet.titre && sheet.image) {
    lastDeclaredImagesByKey.set(getSheetKey(sheet.notion, sheet.titre, sheet.sheet_type), sheet.image)
  }

  // Pour la prévisualisation, ne pas exiger la notion.
  if (!sheet.titre || !sheet.summary) return null
  return sheet
}

// ============================================================================
// ACTIONS
// ============================================================================

function handlePreview() {
  try {
    hasValidSheets.value = true
    previewList.value = parseSheets(rawInput.value)
    nextTick(() => renderMath())
  } catch (e) {
    console.error('Erreur de prévisualisation:', e)
    errorMsg.value = 'Erreur lors de la prévisualisation'
  }
}

async function handleCreate() {
  if (!selectedNotion.value) {
    errorMsg.value = 'Veuillez sélectionner une notion'
    return
  }

  successMsg.value = ''
  errorMsg.value = ''

  try {
    const list = parseSheets(rawInput.value)
    if (list.length === 0) {
      errorMsg.value = 'Aucune fiche valide trouvée'
      return
    }

    // Récupérer les fiches existantes pour gérer les doublons (notion+titre)
    let existing = []
    try {
      const res = await getSynthesisSheets({ notion: Number(selectedNotion.value) })
      existing = Array.isArray(res?.data) ? res.data : (Array.isArray(res) ? res : [])
    } catch (_) {}
    const byTitleAndType = new Map(existing.map(s => [getSheetIdentityKey(s.titre, s.sheet_type), s.id]))

    let createdCount = 0
    let updatedCount = 0
    let sheetErrorCount = 0
    let uploadedImagesCount = 0
    const sheetFailures = []
    const imageUploadFailures = []

    const isSingleEdit = !!currentEditSheetId.value && list.length === 1

    for (const sheetData of list) {
      const payload = {
        notion: Number(sheetData.notion || selectedNotion.value),
        titre: sheetData.titre,
        summary: sheetData.summary,
        reading_time_minutes: Math.max(1, Math.round(sheetData.summary.split(/\s+/).length / 200)),
        access_scope: sheetData.access_scope || selectedAccessScope.value || DEFAULT_ACCESS_SCOPE,
        sheet_type: normalizeSheetType(sheetData.sheet_type || selectedSheetType.value || DEFAULT_SHEET_TYPE)
      }

      let sheetId
      try {
        const existingId = byTitleAndType.get(getSheetIdentityKey(payload.titre, payload.sheet_type))
        if (isSingleEdit) {
          // Forcer la mise à jour par ID quand en mode édition
          const updated = await updateSynthesisSheet(currentEditSheetId.value, payload)
          sheetId = updated?.id || currentEditSheetId.value
          updatedCount++
        } else if (existingId) {
          const updated = await updateSynthesisSheet(existingId, payload)
          sheetId = updated?.id || existingId
          updatedCount++
        } else {
          const created = await createSynthesisSheet(payload)
          sheetId = created?.id || created?.data?.id
          createdCount++
          if (sheetId) byTitleAndType.set(getSheetIdentityKey(payload.titre, payload.sheet_type), sheetId)
        }
      } catch (e) {
        console.error('Erreur creation/mise a jour fiche:', e)
        sheetErrorCount++
        sheetFailures.push(`${payload.titre || 'Sans titre'}: ${extractApiErrorMessage(e, 'Enregistrement impossible')}`)
        continue
      }

      if (!sheetId) {
        sheetErrorCount++
        sheetFailures.push(`${payload.titre || 'Sans titre'}: ID de fiche introuvable apres sauvegarde`)
        continue
      }

      // Ajouter images si presentes (declarees ou via fichiers selectionnes)
      const uploadedNames = new Set()
      const declared = (sheetData.image && sheetData.image.trim())
        ? sheetData.image
        : (selectedImages.value || []).map(f => f.name).join(',')
      const imageNames = (declared || '').split(',').map(n => n.trim()).filter(Boolean)

      for (let i = 0; i < imageNames.length; i++) {
        const imageName = imageNames[i]
        const file = imageManager.getImage(imageName)
        if (!file) continue
        try {
          await createSynthesisImage({ sheet: sheetId, image: file, image_type: 'illustration', position: i + 1 })
          uploadedNames.add(imageName)
          uploadedImagesCount++
        } catch (e) {
          console.error('Erreur upload image declaree:', e)
          imageUploadFailures.push(`${imageName} (${payload.titre}): ${extractApiErrorMessage(e, 'Upload impossible')}`)
        }
      }

      // Fallback: si des fichiers ont ete selectionnes mais pas declares (ou noms differents),
      // les envoyer quand meme dans l'ordre selectionne.
      if (selectedImages.value && selectedImages.value.length) {
        let position = imageNames.length + 1
        for (const file of selectedImages.value) {
          const key = file.name || ''
          if (key && uploadedNames.has(key)) continue
          try {
            await createSynthesisImage({ sheet: sheetId, image: file, image_type: 'illustration', position })
            uploadedImagesCount++
          } catch (e) {
            console.error('Erreur upload image fallback:', e)
            imageUploadFailures.push(`${file.name || `image-${position}`} (${payload.titre}): ${extractApiErrorMessage(e, 'Upload impossible')}`)
          }
          position += 1
        }
      }

      // Memoiser les images declarees pour cette fiche
      const key = getSheetKey(payload.notion, payload.titre, payload.sheet_type)
      if (declared) lastDeclaredImagesByKey.set(key, declared)
    }

    const hasSavedSheets = createdCount > 0 || updatedCount > 0
    if (hasSavedSheets) {
      const successParts = []
      if (createdCount > 0) successParts.push(`${createdCount} cree(s)`)
      if (updatedCount > 0) successParts.push(`${updatedCount} mise(s) a jour`)
      if (uploadedImagesCount > 0) successParts.push(`${uploadedImagesCount} image(s) envoyee(s)`)
      if (sheetErrorCount > 0) successParts.push(`${sheetErrorCount} erreur(s) fiche`)
      if (imageUploadFailures.length > 0) successParts.push(`${imageUploadFailures.length} image(s) en echec`)
      successMsg.value = successParts.join(', ')

      const errorParts = []
      if (sheetFailures.length > 0) errorParts.push(`Fiches en echec: ${summarizeFailures(sheetFailures)}`)
      if (imageUploadFailures.length > 0) errorParts.push(`Images en echec: ${summarizeFailures(imageUploadFailures, 6)}`)
      errorMsg.value = errorParts.join(' || ')

      // Garder le contenu dans la zone de saisie pour éviter la sensation de perte (UX)
      // Ne pas vider les images sélectionnées; l'utilisateur peut ré-appuyer pour mettre à jour.

      // En mode édition simple, fermer le panneau d'images après la mise à jour
      if (isSingleEdit) {
        serverImages.value = []
        currentEditSheetId.value = null
        selectedSheetType.value = DEFAULT_SHEET_TYPE
        // En mode édition, vider la zone de saisie après mise à jour
        rawInput.value = ''
      }
      await loadTable()
      // Reset prévisualisation pour éviter l'affichage périmé
      previewList.value = []
      hasValidSheets.value = false
      // Effacer le texte saisi après création (pas en mode édition)
      if (!isSingleEdit) {
        rawInput.value = ''
        // Conserver les images sélectionnées pour enchaîner des créations sans re-sélection
        // (ne pas vider selectedImages ni imageManager ici)
      }
      // Auto-hide messages après 4s
      setTimeout(() => { successMsg.value = '' }, 4000)
    } else {
      const errorParts = []
      if (sheetFailures.length > 0) errorParts.push(`Fiches en echec: ${summarizeFailures(sheetFailures)}`)
      if (imageUploadFailures.length > 0) errorParts.push(`Images en echec: ${summarizeFailures(imageUploadFailures, 6)}`)
      errorMsg.value = errorParts.length > 0 ? errorParts.join(' || ') : 'Aucune fiche enregistree'
    }
  } catch (e) {
    console.error('Erreur globale handleCreate:', e)
    errorMsg.value = `Erreur lors de la creation des fiches: ${extractApiErrorMessage(e, 'erreur technique')}`
  }
}

// Sortir du mode édition et repasser en mode création
function cancelEdit() {
  currentEditSheetId.value = null
  serverImages.value = []
  previewList.value = []
  hasValidSheets.value = false
  selectedSheetType.value = DEFAULT_SHEET_TYPE
  // On vide le contenu pour repartir d'une fiche vierge
  rawInput.value = ''
  try { window.scrollTo({ top: 0, behavior: 'smooth' }) } catch (_) {}
}

// ============================================================================
// TABLE ACTIONS
// ============================================================================

function getNotionName(notionId) {
  const n = notions.value.find(x => String(x.id) === String(notionId))
  return n ? (n.nom || n.titre) : '—'
}

function getNotionById(id) { return notions.value.find(x => String(x.id) === String(id)) }

function getNotionContextLabel(notionId) {
  const n = getNotionById(notionId)
  const ctx = notionContext(n)
  const parts = [ctx.matiereNom, ctx.themeNom].filter(Boolean)
  return parts.join(' › ')
}

async function editSheet(s) {
  // Pré-remplir le bloc unique pour édition via le form bulk
  selectedNotion.value = s.notion
  currentEditSheetId.value = s.id
  selectedAccessScope.value = s.access_scope || DEFAULT_ACCESS_SCOPE
  selectedSheetType.value = normalizeSheetType(s.sheet_type || DEFAULT_SHEET_TYPE)

  // Récupérer les images existantes pour préremplir la ligne "Images:"
  let imageNames = ''
  try {
    const detail = await getSynthesisSheet(s.id)
    const data = detail?.data || detail
    if (Array.isArray(data?.images)) {
      // Ordonner par position puis extraire le nom de fichier
      const sorted = [...data.images].sort((a, b) => (a.position || 0) - (b.position || 0))
      imageNames = sorted
        .map(img => {
          const src = img.image || ''
          // extraire le basename de l'URL et retirer la query (?...)
          try {
            const clean = String(src).split('?')[0]
            const parts = clean.split('/')
            return parts[parts.length - 1] || ''
          } catch (_) {
            return ''
          }
        })
        .filter(Boolean)
        .join(',')
    }
    // Alimente aussi l'aperçu des images serveur
    serverImages.value = Array.isArray(data?.images) ? data.images.map(img => ({ ...img, _file: null })) : []
  } catch (e) {
    // En cas d'erreur on laisse vide et on continue
    console.error('[AdminSheets] Impossible de charger les images de la fiche:', e)
    serverImages.value = []
  }

  // Fallback: si aucune image retournée par le serveur, utiliser la dernière
  // déclaration locale pour cette fiche (même session)
  if (!imageNames) {
    const key = getSheetKey(s.notion, s.titre, s.sheet_type)
    const memo = lastDeclaredImagesByKey.get(key)
    if (memo) imageNames = memo
    else if (selectedImages.value && selectedImages.value.length) {
      imageNames = selectedImages.value.map(f => f.name).join(',')
    }
  }

  const header = [
    '=== ' + (s.titre || ''),
    'Images: ' + imageNames,
    'Type: ' + normalizeSheetType(s.sheet_type || DEFAULT_SHEET_TYPE),
    'Access: ' + (s.access_scope || DEFAULT_ACCESS_SCOPE)
  ].join('\n')

  rawInput.value = `${header}\n\n${s.summary || ''}`
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function handleDeleteSheet(s) {
  try {
    await deleteSynthesisSheet(s.id)
    await loadTable()
  } catch (e) {
    console.error('Suppression échouée:', e)
    errorMsg.value = 'Erreur lors de la suppression'
  }
}

async function handleDuplicateSheet(s) {
  try {
    await duplicateSynthesisSheet(s.id)
    await loadTable()
  } catch (e) {
    console.error('Duplication échouée:', e)
    errorMsg.value = 'Erreur lors de la duplication'
  }
}

// ============================================================================
// COMPUTED & INIT
// ============================================================================

const filteredNotions = computed(() => {
  if (!notionFilter.value) return notions.value
  const f = notionFilter.value.toLowerCase()
  return notions.value.filter(n => (formatNotionOption(n) || '').toLowerCase().includes(f))
})

const filteredNotionsForFilter = computed(() => {
  if (!notionTableFilter.value) return notions.value
  const f = notionTableFilter.value.toLowerCase()
  return notions.value.filter(n => (formatNotionOption(n) || '').toLowerCase().includes(f))
})

const paginatedSheets = computed(() => sheets.value)
const totalPages = computed(() => Math.ceil((totalSheets.value || 0) / itemsPerPage))
const displayedPages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value
  let startPage = Math.max(1, current - 2)
  let endPage = Math.min(total, current + 2)
  if (current <= 3) endPage = Math.min(5, total)
  if (current >= total - 2) startPage = Math.max(1, total - 4)
  for (let i = startPage; i <= endPage; i++) pages.push(i)
  return pages
})

watch(() => [filters.value.notion, filters.value.sheet_type], () => {
  currentPage.value = 1
  loadTable()
})

function goToPage(page) {
  const total = totalPages.value || 0
  const maxPage = total > 0 ? total : 1
  const target = Math.min(Math.max(page, 1), maxPage)
  if (target === currentPage.value) return
  currentPage.value = target
  loadTable()
}

function nextPage() {
  if (totalPages.value && currentPage.value < totalPages.value) {
    currentPage.value += 1
    loadTable()
  }
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value -= 1
    loadTable()
  }
}

async function loadTable() {
  try {
    isLoadingSheets.value = true
    const page = Math.max(currentPage.value || 1, 1)
    const notionParam = (filters.value.notion && filters.value.notion !== 'all') ? filters.value.notion : undefined
    const sheetTypeParam = (filters.value.sheet_type && filters.value.sheet_type !== 'all')
      ? normalizeSheetType(filters.value.sheet_type)
      : undefined
    const res = await getSynthesisSheets({
      limit: itemsPerPage,
      offset: (page - 1) * itemsPerPage,
      notion: notionParam,
      sheet_type: sheetTypeParam
    })
    const data = res?.data ?? res
    const results = Array.isArray(data?.results) ? data.results : (Array.isArray(data) ? data : [])
    sheets.value = results.slice().sort((a, b) => String(a.titre || '').localeCompare(String(b.titre || '')))
    const total = Number(data?.count ?? results.length ?? 0)
    totalSheets.value = Number.isFinite(total) ? total : results.length
    const maxPage = Math.max(1, Math.ceil((totalSheets.value || 0) / itemsPerPage))
    if (totalSheets.value > 0 && currentPage.value > maxPage) {
      currentPage.value = maxPage
      await loadTable()
    }
  } catch (e) {
    console.error('[AdminSheets] Erreur chargement des fiches:', e)
    sheets.value = []
    totalSheets.value = 0
  } finally {
    isLoadingSheets.value = false
  }
}

async function loadServerImages(sheetId) {
  if (!sheetId) { serverImages.value = []; return }
  imageManageLoading.value = true
  try {
    const detail = await getSynthesisSheet(sheetId)
    const data = detail?.data || detail
    serverImages.value = Array.isArray(data?.images) ? data.images.map(img => ({ ...img, _file: null })) : []
    const maxPos = serverImages.value.reduce((m, it) => Math.max(m, Number(it.position) || 0), 0)
    if (newImage && newImage.value) newImage.value.position = maxPos + 1
  } catch (e) {
    console.error('[AdminSheets] Erreur chargement images fiche:', e)
    serverImages.value = []
  } finally {
    imageManageLoading.value = false
  }
}

function onSelectReplaceFile(index, event) {
  const input = event?.target
  const f = (input?.files || [])[0]
  if (!f) return

  const validation = validateImageFile(f)
  if (!validation.ok) {
    const rowInvalid = serverImages.value[index]
    if (rowInvalid) rowInvalid._file = null
    errorMsg.value = validation.reason
    if (input) input.value = ''
    return
  }

  const row = serverImages.value[index]
  if (row) row._file = f
  errorMsg.value = ''
  if (input) input.value = ''
}

async function replaceImageRow(sheetId, row, index) {
  try {
    const file = row._file
    if (!file) return
    await updateSynthesisImage(row.id, { image: file, image_type: row.image_type || 'illustration', position: row.position, caption: row.caption })
    await loadServerImages(sheetId)
    serverImages.value[index]._file = null
  } catch (e) {
    console.error('Erreur remplacement image:', e)
    errorMsg.value = 'Erreur lors du remplacement de l\'image'
  }
}

async function saveImageRow(sheetId, row, index) {
  try {
    await updateSynthesisImage(row.id, { image_type: row.image_type, position: row.position, caption: row.caption })
    await loadServerImages(sheetId)
  } catch (e) {
    console.error('Erreur sauvegarde image:', e)
    errorMsg.value = 'Erreur lors de la sauvegarde de l\'image'
  }
}

async function deleteImageRow(sheetId, row, index) {
  try {
    await deleteSynthesisImage(row.id)
    await loadServerImages(sheetId)
  } catch (e) {
    console.error('Erreur suppression image:', e)
    errorMsg.value = 'Erreur lors de la suppression de l\'image'
  }
}

const newImage = ref({ file: null, image_type: 'illustration', position: 0, caption: '' })
function onSelectNewImage(event) {
  const input = event?.target
  const f = (input?.files || [])[0]
  if (!f) {
    newImage.value.file = null
    return
  }

  const validation = validateImageFile(f)
  if (!validation.ok) {
    newImage.value.file = null
    errorMsg.value = validation.reason
    if (input) input.value = ''
    return
  }

  newImage.value.file = f
  errorMsg.value = ''
  if (input) input.value = ''
}

async function addNewImage(sheetId) {
  try {
    if (!newImage.value.file) return
    await createSynthesisImage({
      sheet: sheetId,
      image: newImage.value.file,
      image_type: newImage.value.image_type,
      position: newImage.value.position || null,
      caption: newImage.value.caption || ''
    })
    // reset form
    newImage.value = { file: null, image_type: 'illustration', position: 0, caption: '' }
    await loadServerImages(sheetId)
  } catch (e) {
    console.error('Erreur ajout image:', e)
    errorMsg.value = 'Erreur lors de l\'ajout de l\'image'
  }
}

onMounted(async () => {
  try {
    const nt = await getNotions()
    notions.value = Array.isArray(nt) ? nt : (nt?.data || [])
    await loadTable()
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
/* Styles spécifiques à AdminSheets */
.preview-sheet {
  background: #f8f9fa;
  border-radius: 6px;
  padding: 1rem;
}

.filters .filter-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  background: white;
  appearance: none;
  cursor: pointer;
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

.preview-content {
  line-height: 1.6;
  color: #333;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

/* Tableau admin (repris de AdminCours) */
.admin-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  margin-top: 1.5rem;
}
.admin-table th,
.admin-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
  text-align: left;
}
.admin-table th {
  background: #f8fafc;
  font-weight: 600;
  color: #374151;
}
.admin-table tr:hover {
  background: #f9fafb;
}
.loading-row {
  text-align: center;
  color: #6b7280;
  font-style: italic;
}
.ctx-cell {
  color: #64748b;
  font-size: 0.85rem;
  max-width: 360px;
}
.scope-label {
  font-size: 0.85rem;
  font-weight: 600;
  margin-top: 10px;
}

.scope-select {
  margin-bottom: 10px;
}

.scope-pill {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 600;
  border: 1px solid transparent;
}

.scope-select-inline {
  cursor: pointer;
  padding-right: 1.75rem;
}

.scope-select-inline:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.scope-pill--free {
  background: #dcfce7;
  border-color: #bbf7d0;
  color: #166534;
}

.scope-pill--both {
  background: #e0f2fe;
  border-color: #bae6fd;
  color: #0f172a;
}

.scope-pill--paid {
  background: #fee2e2;
  border-color: #fecaca;
  color: #991b1b;
}

/* Pagination */
.pagination { display:flex; align-items:center; justify-content:center; gap:0.5rem; margin-top: 1.25rem; padding: 0.75rem 0; }
.pagination-btn { padding: 0.5rem 1rem; border: 1px solid #d1d5db; background: white; border-radius: 0.375rem; cursor: pointer; font-size: 0.875rem; font-weight: 500; color: #374151; }
.pagination-btn:hover:not(:disabled) { background: #f3f4f6; border-color: #9ca3af; }
.pagination-btn:disabled { opacity: .5; cursor: not-allowed; }
.pagination-numbers { display:flex; gap: .25rem; }
.pagination-number { padding: .5rem .75rem; border:1px solid #d1d5db; background:white; border-radius:.375rem; cursor:pointer; font-size:.875rem; font-weight:500; color:#374151; min-width:2.5rem; }
.pagination-number:hover { background:#f3f4f6; border-color:#9ca3af; }
.pagination-number.active { background:#3b82f6; border-color:#3b82f6; color:#fff; }
.pagination-info { text-align:center; font-size:.875rem; color:#6b7280; margin-top:.5rem; margin-bottom:1.5rem; }

/* Images manager UI */
.images-table { width: 100%; border-collapse: collapse; background: #fff; margin-top: 10px; }
.images-table th, .images-table td { padding: 8px 10px; border-bottom: 1px solid #e5e7eb; vertical-align: middle; }
.srv-preview { max-width: 110px; max-height: 70px; border-radius: 6px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
.img-row-actions { display: flex; gap: 8px; align-items: center; }
.btn-danger { background: #ef4444; color: #fff; border: 1px solid #ef4444; border-radius: 6px; padding: 6px 10px; cursor: pointer; }
.btn-danger:hover { background: #dc2626; border-color: #dc2626; }
.btn-primary.small, .btn-secondary.small, .btn-danger.small { font-size: 0.85rem; padding: 6px 10px; }
.add-image-form { margin-top: 10px; background: #f9fafb; padding: 10px; border: 1px dashed #d1d5db; border-radius: 8px; }
.add-image-row { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
</style>

