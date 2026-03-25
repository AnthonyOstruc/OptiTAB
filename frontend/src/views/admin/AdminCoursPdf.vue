<template>
  <div>
    <FormatHelp :format-template="FORMAT_TEMPLATE">
      <template #notes>
        <ul>
          <li>Utilise un bloc par exercice: <code>=== [Titre]</code> puis les champs d identite (niveau, matiere, chapitre, notion, type, difficulte, temps, objectif).</li>
          <li>Format pedagogique recommande: <code>Prerequis</code>, <code>Competences_visees</code>, <code>Enonce_eleve</code>, <code>Questions</code>, <code>Aides_progressives</code>, <code>Correction_pedagogique_detaillee</code>, <code>Reponse_finale</code>, <code>A_retenir</code>, <code>Prolongement</code>.</li>
          <li>Dans <code>Questions:</code> utilise des lignes numerotees <code>1.</code>, <code>2.</code>, <code>3.</code> pour un rendu parfaitement aligne.</li>
          <li>Tu peux aussi utiliser les variantes en balises: <code>[OBJECTIF]</code>, <code>[PREREQUIS]</code>, <code>[ENONCE]</code>, <code>[REPONSE FINALE]</code>, <code>[A RETENIR]</code>.</li>
          <li>Pour les images: declare <code>Images:</code> puis place <code>[IMAGE_1]</code>, <code>[IMAGE_2]</code> dans la partie concernee.</li>
          <li>Evite les gros tableaux inline dans l enonce: garde les details dans la correction pour un PDF premium propre.</li>
        </ul>
      </template>
    </FormatHelp>

    <div class="bulk-form">
      <input v-model="notionFilter" type="text" placeholder="Filtrer les notions..." class="filter-input" />
      <select v-model="selectedNotion">
        <option value="">Choisir notion</option>
        <option v-for="n in filteredNotions" :key="n.id" :value="n.id">{{ formatNotionOption(n) }}</option>
      </select>

      <div class="images-upload-section">
        <h4>Images de l annale</h4>
        <p class="upload-help">Uploadez les images referencees dans votre bloc.</p>
        <input
          type="file"
          accept="image/*"
          multiple
          class="images-file-input"
          @change="handleImagesSelect"
        />

        <div v-if="selectedImages.length > 0" class="selected-images">
          <h5>Images selectionnees :</h5>
          <div v-for="(img, index) in selectedImages" :key="getFileKey(img)" class="selected-image-item">
            <img :src="getImagePreview(img)" :alt="img.name" class="image-preview" />
            <span class="image-name">{{ img.name }}</span>
            <button type="button" class="btn-remove" @click="removeSelectedImage(index)">x</button>
          </div>
        </div>
      </div>

      <div class="import-row">
        <label for="cours-file">Importer un fichier .txt/.html/.md (optionnel)</label>
        <input
          id="cours-file"
          type="file"
          accept=".txt,.html,.htm,.md"
          @change="onFileChange"
        />
      </div>

      <textarea
        v-model="rawInput"
        placeholder="Collez ici votre annale d exercices (ou un cours) au format OptiTAB"
      ></textarea>

      <div class="btn-group">
        <button class="btn-secondary" :disabled="loadingPreview || !canRunActions" @click="handlePreview">
          {{ loadingPreview ? 'Previsualisation...' : 'Previsualiser' }}
        </button>
        <button class="btn-primary" :disabled="loadingPdf || !canRunActions" @click="handleDownloadPdf">
          {{ loadingPdf ? 'Generation PDF...' : 'Mettre en PDF' }}
        </button>
      </div>
    </div>

    <div v-if="successMessage" class="success-msg">{{ successMessage }}</div>
    <div v-if="errorMessage" class="error-msg">{{ errorMessage }}</div>

    <div v-if="hasImageStatus" class="preview-image-info image-status-box">
      <span class="image-indicator">Images detectees</span>
      <div class="image-status-list">
        <span
          v-for="img in imageStatuses"
          :key="`${img.position}-${img.name}`"
          :class="['image-status', img.available ? 'available' : 'missing']"
        >
          [IMAGE_{{ img.position }}] {{ img.name }} : {{ img.available ? 'Disponible' : 'Manquante' }}
        </span>
      </div>
    </div>

    <div v-if="previewHtml" class="preview-section pdf-preview-section">
      <h3>Apercu PDF</h3>
      <iframe :srcdoc="previewHtml" class="preview-frame" title="Apercu du cours PDF"></iframe>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { getNotions } from '@/api'
import { downloadCoursPdfDraft, previewCoursPdfDraft } from '@/api/cours'
import FormatHelp from '@/components/admin/FormatHelp.vue'

const MAX_IMAGE_SIZE = 20 * 1024 * 1024 // 20MB

const rawInput = ref('')
const previewHtml = ref('')
const selectedImages = ref([])
const notions = ref([])
const notionFilter = ref('')
const selectedNotion = ref('')
const loadingPreview = ref(false)
const loadingPdf = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const imagePreviewUrls = new Map()
const imageDataUrls = new Map()

const FORMAT_TEMPLATE = `=== [TEMPLATE MAITRE - EXERCICE PEDAGOGIQUE]
Titre: Derivation - Lecture graphique de la tangente
Niveau: Premiere
Matiere: Mathematiques
Chapitre: Derivation
Notion: Nombre derive
Sous_notion: Lecture graphique
Type d exercice: application
Difficulte: moyen
Temps estime: 15 min
Objectif pedagogique principal: Determiner un nombre derive a partir d une tangente.
Prerequis: Coefficient directeur, equation de droite, lecture de points.
Erreurs frequentes: Confondre pente positive/negative ; inversion dans la formule.
Images: lecturegraphique.png

Competences_visees:
- Identifier les informations utiles dans un graphique.
- Appliquer la formule du coefficient directeur.
- Justifier chaque etape du calcul.
- Rediger une conclusion mathematique.
- Verifier la coherence du resultat.

Enonce_eleve:
- Contexte: On etudie la pente de la tangente a une courbe.
- Consigne principale: Determiner les nombres derives demandes.
- Donnees: Tangente en C(-1;2) passant par (1;0) et tangente en D(2;0) passant par (0;-1).
[IMAGE_1]

Questions:
1. Determiner graphiquement f'(-1).
2. Determiner graphiquement f'(2).

Decoupage_pedagogique:
- Etape 1: comprendre ce qu on cherche.
- Etape 2: identifier la bonne methode.
- Etape 3: appliquer proprement.
- Etape 4: conclure.
- Etape 5: verifier le resultat.

Aides_progressives:
- Indice 1: Le nombre derive est la pente de la tangente.
- Indice 2: Utiliser m = (y2 - y1)/(x2 - x1).
- Indice 3: Remplacer par les coordonnees des deux points de chaque tangente.

Correction_pedagogique_detaillee:
- Etape 1 (Question 1): on prend C(-1;2) et (1;0), donc f'(-1) = (0-2)/(1-(-1)) = -2/2 = -1.
- Etape 2 (Question 2): on prend D(2;0) et (0;-1), donc f'(2) = (-1-0)/(0-2) = -1/-2 = 1/2.
- Vigilance: ne pas inverser l ordre des soustractions.

Reponse_finale:
- f'(-1) = -1
- f'(2) = 1/2
- Conclusion: la fonction est decroissante en -1 et croissante en 2.

A_retenir:
- Le nombre derive en a est le coefficient directeur de la tangente en a.
- Le signe de la pente donne le sens de variation local.
- Piege classique: oublier les parenthèses avec les nombres negatifs.

Prolongement:
- Variante plus simple: tangente passant par des points entiers.
- Variante plus difficile: deduire une equation de tangente.
- Question bonus: comparer les pentes obtenues et interpreter.

===`

const canRunActions = computed(() => rawInput.value.trim().length > 0)

const declaredImageNames = computed(() => extractDeclaredImageNames(rawInput.value))

const imageMarkerPositions = computed(() => {
  const positions = new Set()
  const markerRegex = /\[\s*IMAGE\s*_?\s*(\d+)\s*\]/gi
  String(rawInput.value || '').replace(markerRegex, (_match, positionRaw) => {
    const position = Number.parseInt(positionRaw, 10)
    if (Number.isFinite(position) && position > 0) {
      positions.add(position)
    }
    return _match
  })
  return Array.from(positions).sort((a, b) => a - b)
})

const expectedImageNames = computed(() => {
  if (declaredImageNames.value.length > 0) {
    return declaredImageNames.value
  }
  if (selectedImages.value.length > 0) {
    return selectedImages.value.map((file) => file.name)
  }
  if (imageMarkerPositions.value.length > 0) {
    return imageMarkerPositions.value.map((position) => `IMAGE_${position}`)
  }
  return []
})

const imageStatuses = computed(() =>
  expectedImageNames.value.map((name, index) => ({
    name,
    position: index + 1,
    available: Boolean(findImageFileByName(name) || selectedImages.value[index]),
  }))
)

const hasImageStatus = computed(() => imageStatuses.value.length > 0)
const filteredNotions = computed(() => {
  const all = notions.value || []
  if (!notionFilter.value) return all
  const filter = notionFilter.value.toLowerCase()
  return all.filter((notion) => formatNotionOption(notion).toLowerCase().includes(filter))
})

function resetFeedback() {
  errorMessage.value = ''
  successMessage.value = ''
}

function normalizeDifficulty(rawValue) {
  const normalized = String(rawValue || '').trim().toLowerCase()
  if (!normalized) return ''

  const aliases = {
    facile: 'easy',
    easy: 'easy',
    moyen: 'medium',
    medium: 'medium',
    difficile: 'hard',
    hard: 'hard',
  }

  return aliases[normalized] || 'medium'
}

function notionContext(notion) {
  if (!notion) return { matiereNom: '', themeNom: '', paysNom: '', niveauNom: '' }
  const matiereNom = notion.matiere_nom || notion.contexte_detail?.matiere_nom || ''
  const themeNom = notion.theme_nom || ''
  const paysNom = notion.pays_nom || notion.contexte_detail?.pays?.nom || ''
  const niveauNom = notion.niveau_nom || notion.contexte_detail?.niveau?.nom || ''
  return { matiereNom, themeNom, paysNom, niveauNom }
}

function formatNotionOption(n) {
  if (!n) return ''
  const ctx = notionContext(n)
  const contextParts = [ctx.matiereNom, ctx.themeNom].filter(Boolean).join(' / ')
  const geoParts = [ctx.paysNom, ctx.niveauNom].filter(Boolean).join(' / ')
  const parts = [
    n.nom || n.titre || '',
    contextParts ? ` - ${contextParts}` : '',
    geoParts ? ` (${geoParts})` : '',
  ].filter(Boolean)
  return parts.join('')
}

function extractDeclaredImageNames(source) {
  const match = String(source || '').match(/^\s*images?\s*:\s*(.+)$/im)
  if (!match) return []
  return match[1]
    .split(',')
    .map((name) => name.trim())
    .filter(Boolean)
}

function extractTitleFromInput(source) {
  const text = String(source || '')
  const explicitTitle = text.match(/^\s*(titre|title)\s*:\s*(.+)$/im)
  if (explicitTitle?.[2]) return explicitTitle[2].trim()

  const blockTitle = text.match(/^\s*===\s*\[([^\]]+)\]\s*$/m)
  if (blockTitle?.[1]) return blockTitle[1].trim()

  const firstLine = text
    .split('\n')
    .map((line) => line.trim())
    .find(
      (line) =>
        line &&
        line !== '===' &&
        !/^(images?|titre|title|difficulte|difficult[eé]|difficulty|ordre|order|description)\s*:/i.test(line)
    )

  return firstLine ? firstLine.replace(/^\[|\]$/g, '').trim() : ''
}

function extractDifficultyFromInput(source) {
  const match = String(source || '').match(/^\s*(difficulte|difficult[eé]|difficulty)\s*:\s*(.+)$/im)
  return match?.[2] ? normalizeDifficulty(match[2]) : ''
}

function getFileKey(file) {
  return `${String(file?.name || '')}:${Number(file?.size || 0)}:${Number(file?.lastModified || 0)}`
}

function getImagePreview(file) {
  const key = getFileKey(file)
  if (!key) return ''
  if (!imagePreviewUrls.has(key)) {
    imagePreviewUrls.set(key, URL.createObjectURL(file))
  }
  return imagePreviewUrls.get(key)
}

function releaseImagePreview(file) {
  const key = getFileKey(file)
  const objectUrl = imagePreviewUrls.get(key)
  if (objectUrl) {
    URL.revokeObjectURL(objectUrl)
    imagePreviewUrls.delete(key)
  }
}

function findImageFileByName(name) {
  const target = String(name || '').trim().toLowerCase()
  if (!target) return null

  const exact = selectedImages.value.find(
    (file) => String(file?.name || '').trim().toLowerCase() === target
  )
  if (exact) return exact

  return (
    selectedImages.value.find((file) => {
      const candidate = String(file?.name || '').trim().toLowerCase()
      return candidate.includes(target) || target.includes(candidate)
    }) || null
  )
}

function removeSelectedImage(index) {
  const file = selectedImages.value[index]
  if (file) {
    releaseImagePreview(file)
    imageDataUrls.delete(getFileKey(file))
  }
  selectedImages.value.splice(index, 1)
}

function handleImagesSelect(event) {
  resetFeedback()
  const files = Array.from(event?.target?.files || [])
  if (!files.length) return

  const nextByName = new Map(
    selectedImages.value.map((file) => [String(file?.name || '').toLowerCase(), file])
  )
  const rejected = []

  for (const file of files) {
    const mime = String(file?.type || '').toLowerCase()
    if (mime && !mime.startsWith('image/')) {
      rejected.push(`${file.name} (type non image)`)
      continue
    }
    if (Number(file?.size || 0) > MAX_IMAGE_SIZE) {
      rejected.push(`${file.name} (plus de 20MB)`)
      continue
    }

    const key = String(file?.name || '').toLowerCase()
    const previousFile = nextByName.get(key)
    if (previousFile) {
      releaseImagePreview(previousFile)
      imageDataUrls.delete(getFileKey(previousFile))
    }
    nextByName.set(key, file)
  }

  selectedImages.value = Array.from(nextByName.values())

  if (rejected.length > 0) {
    errorMessage.value = `Images ignorees : ${rejected.join(', ')}`
  } else {
    successMessage.value = `${files.length} image(s) ajoutee(s).`
  }

  if (event?.target) {
    event.target.value = ''
  }
}

async function onFileChange(event) {
  const file = event?.target?.files?.[0]
  if (!file) return
  try {
    rawInput.value = await file.text()
    successMessage.value = `Fichier importe: ${file.name}`
    errorMessage.value = ''
  } catch (_error) {
    errorMessage.value = 'Impossible de lire le fichier importe.'
  } finally {
    if (event?.target) {
      event.target.value = ''
    }
  }
}

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

function fileToDataUrl(file) {
  const key = getFileKey(file)
  if (!key) return Promise.resolve('')
  if (imageDataUrls.has(key)) {
    return Promise.resolve(imageDataUrls.get(key))
  }

  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => {
      const result = String(reader.result || '')
      imageDataUrls.set(key, result)
      resolve(result)
    }
    reader.onerror = () => reject(new Error(`Impossible de lire l image ${file.name}`))
    reader.readAsDataURL(file)
  })
}

function buildInlineImageHtml(dataUrl, imageLabel, position) {
  return `
<figure style="text-align:center;margin:24px 0;">
  <img src="${dataUrl}" alt="${escapeHtml(imageLabel || `Image ${position}`)}" style="max-width:100%;height:auto;border-radius:8px;" />
</figure>`
}

async function buildSourceWithInlineImages() {
  const source = String(rawInput.value || '')
  if (!source.trim()) return ''

  const names = expectedImageNames.value
  const markerRegex = /\[\s*IMAGE\s*_?\s*(\d+)\s*\]/gi
  const markerPositions = new Set()

  source.replace(markerRegex, (_match, positionRaw) => {
    const position = Number.parseInt(positionRaw, 10)
    if (Number.isFinite(position) && position > 0) {
      markerPositions.add(position)
    }
    return _match
  })

  const inlineImagesByPosition = {}
  for (const position of markerPositions) {
    const positionIndex = position - 1
    const imageName = names[positionIndex] || `IMAGE_${position}`
    const imageFile = findImageFileByName(imageName) || selectedImages.value[positionIndex]
    if (!imageFile) continue

    const dataUrl = await fileToDataUrl(imageFile)
    inlineImagesByPosition[position] = buildInlineImageHtml(dataUrl, imageName, position)
  }

  let output = source.replace(markerRegex, (match, positionRaw) => {
    const position = Number.parseInt(positionRaw, 10)
    return inlineImagesByPosition[position] || match
  })

  if (markerPositions.size === 0 && names.length > 0) {
    const gallery = []
    for (let index = 0; index < names.length; index += 1) {
      const imageName = names[index]
      const imageFile = findImageFileByName(imageName) || selectedImages.value[index]
      if (!imageFile) continue
      const dataUrl = await fileToDataUrl(imageFile)
      gallery.push(buildInlineImageHtml(dataUrl, imageName, index + 1))
    }
    if (gallery.length > 0) {
      output = `${output}\n${gallery.join('\n')}`
    }
  }

  return output
}

async function buildPayload() {
  const content = await buildSourceWithInlineImages()
  const payload = { content }

  const title = extractTitleFromInput(rawInput.value)
  const difficulty = extractDifficultyFromInput(rawInput.value)

  if (title) payload.title = title
  if (difficulty) payload.difficulty = difficulty

  return payload
}

async function handlePreview() {
  resetFeedback()
  if (!canRunActions.value) {
    errorMessage.value = 'Collez un contenu de cours avant de previsualiser.'
    return
  }

  loadingPreview.value = true
  try {
    const payload = await buildPayload()
    const { data } = await previewCoursPdfDraft(payload)
    previewHtml.value = data?.html || ''
    successMessage.value = 'Previsualisation generee.'
  } catch (error) {
    const detail = error?.response?.data?.detail
    errorMessage.value = detail || 'Erreur pendant la previsualisation.'
  } finally {
    loadingPreview.value = false
  }
}

async function handleDownloadPdf() {
  resetFeedback()
  if (!canRunActions.value) {
    errorMessage.value = 'Collez un contenu de cours avant la generation PDF.'
    return
  }

  loadingPdf.value = true
  try {
    const payload = await buildPayload()
    const response = await downloadCoursPdfDraft(payload)
    const blob = new Blob([response.data], { type: 'application/pdf' })
    const objectUrl = URL.createObjectURL(blob)

    const contentDisposition = response?.headers?.['content-disposition'] || ''
    const match = /filename=\"?([^\";]+)\"?/i.exec(contentDisposition)
    const filename = (match && match[1]) || 'cours.pdf'

    const link = document.createElement('a')
    link.href = objectUrl
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(objectUrl)

    successMessage.value = 'PDF genere et telecharge.'
  } catch (error) {
    const detail = error?.response?.data?.detail
    errorMessage.value = detail || 'Erreur pendant la generation PDF.'
  } finally {
    loadingPdf.value = false
  }
}

onBeforeUnmount(() => {
  for (const objectUrl of imagePreviewUrls.values()) {
    URL.revokeObjectURL(objectUrl)
  }
  imagePreviewUrls.clear()
  imageDataUrls.clear()
})

onMounted(async () => {
  try {
    const response = await getNotions()
    notions.value = Array.isArray(response) ? response : response?.data || []
  } catch (_error) {
    notions.value = []
  }
})
</script>

<style src="@/styles/admin-common.css"></style>

<style scoped>
.import-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.import-row label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1f2937;
}

.import-row input[type='file'] {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 10px;
  font-size: 0.9rem;
  background: #fff;
}

.image-status-box {
  margin-top: 12px;
}

.pdf-preview-section {
  margin-top: 24px;
}

.preview-frame {
  width: 100%;
  min-height: 760px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  background: #fff;
}

@media (max-width: 768px) {
  .preview-frame {
    min-height: 560px;
  }
}
</style>
