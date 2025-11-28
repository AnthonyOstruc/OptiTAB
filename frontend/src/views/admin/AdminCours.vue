<template>
  <div>
    <h2 class="admin-title">Gestion des Cours</h2>
    <form class="admin-form" @submit.prevent="handleSave">
      <div class="form-group">
        <label>Notion:</label>
        <input v-model="notionFormFilter" type="text" placeholder="Filtrer les notions..." class="filter-input" />
        <select v-model="form.notion" required>
          <option value="">Choisir une notion</option>
          <option v-for="notion in filteredNotionsForForm" :key="notion.id" :value="notion.id">{{ formatNotionOption(notion) }}</option>
        </select>
      </div>
      <div v-if="currentContext" class="context-panel">
        <div class="context-row"><strong>Matière:</strong> <span>{{ currentContext.matiereNom || '—' }}</span></div>
        <div class="context-row"><strong>Thème:</strong> <span>{{ currentContext.themeNom || '—' }}</span></div>
        <div class="context-row"><strong>Pays:</strong> <span>{{ currentContext.paysNom || '—' }}</span></div>
        <div class="context-row"><strong>Niveau:</strong> <span>{{ currentContext.niveauNom || '—' }}</span></div>
        <div class="context-row"><strong>Chemin:</strong> <span>{{ getNotionContextLabel(form.notion) }}</span></div>
        <div class="context-row"><strong>Code:</strong> <code>{{ getNotionContextCode(form.notion) }}</code></div>
      </div>
      
      <div class="form-group">
        <label>Titre du cours:</label>
        <input v-model="form.titre" placeholder="Titre du cours" required />
      </div>
      
      <div class="form-group">
        <label>Contenu:</label>
        <textarea v-model="form.contenu" rows="6" required></textarea>
        <small style="color: #666; font-size: 0.875rem;">
          Supporte HTML, LaTeX ($formule$), et images avec [IMAGE_1], [IMAGE_2], etc.
        </small>
      </div>

      <div class="form-group">
        <label>Images (optionnel):</label>
        <input
          type="file"
          ref="imagesInput"
          @change="handleImagesSelect"
          accept="image/*"
          multiple
          class="images-file-input"
        />
        <small style="color: #666; font-size: 0.875rem;">
          Sélectionnez les images qui seront référencées dans le contenu avec [IMAGE_1], [IMAGE_2], etc.
        </small>
        <div v-if="selectedImages.length > 0" class="selected-images">
          <h5>Images sélectionnées :</h5>
          <div v-for="(img, index) in selectedImages" :key="index" class="selected-image-item">
            <img :src="getImagePreview(img)" :alt="img.name" class="image-preview" />
            <span class="image-name">{{ img.name }}</span>
            <button type="button" class="btn-remove" @click="removeSelectedImage(index)">×</button>
          </div>
        </div>
      </div>

      <div class="form-group">
        <label>PDF du cours (optionnel):</label>
        <input type="file" accept="application/pdf" @change="onSelectPdf($event)" />
        <small v-if="form.__pdf_file" class="muted">PDF sélectionné: {{ form.__pdf_file.name }}</small>
      </div>

      <!-- Section de gestion des images déjà enregistrées (mode édition) -->
      <div v-if="form.id" class="server-images-section">
        <h5>Images du cours (enregistrées)</h5>
        <div v-if="imageManageLoading" class="muted">Chargement…</div>
        <div v-else>
          <div v-if="serverImages.length === 0" class="muted">Aucune image enregistrée.</div>
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
                    <option value="donnee">Donnée</option>
                    <option value="solution">Solution</option>
                  </select>
                </td>
                <td style="width:100px">
                  <input v-model.number="img.position" type="number" min="0" />
                </td>
                <td>
                  <input v-model="img.legende" placeholder="Légende" />
                </td>
                <td>
                  <input type="file" accept="image/*" @change="onSelectReplaceFile(i, $event)" />
                </td>
                <td style="white-space:nowrap">
                  <button type="button" class="btn-secondary small" @click="saveImageRow(img)">Enregistrer</button>
                  <button type="button" class="btn-danger small" @click="removeImageRow(img)">Supprimer</button>
                </td>
              </tr>
            </tbody>
          </table>

          <div class="add-image-form">
            <h6>Ajouter une image</h6>
            <div class="add-grid">
              <input type="file" accept="image/*" ref="newImageInput" @change="onSelectNewImage($event)" />
              <select v-model="newImage.image_type">
                <option value="illustration">Illustration</option>
                <option value="donnee">Donnée</option>
                <option value="solution">Solution</option>
              </select>
              <input v-model.number="newImage.position" type="number" min="0" placeholder="Position" />
              <input v-model="newImage.legende" placeholder="Légende (optionnel)" />
              <button type="button" class="btn-primary" @click="addNewImage">Ajouter</button>
            </div>
          </div>
        </div>
      </div>
      
      <button class="btn-primary" type="submit">{{ form.id ? 'Mettre à jour' : 'Créer' }}</button>
      <button v-if="form.id" class="btn-secondary" type="button" @click="resetForm">Annuler</button>
      <button class="btn-secondary" type="button" @click="handlePreview">Prévisualiser</button>
    </form>

    <!-- Aperçu (exactement comme dans AdminCoursPlus) -->
    <div v-if="showPreview && previewData" class="preview-section">
      <h3>Aperçu du cours {{ form.id ? '(Mode édition)' : '(Mode création)' }}</h3>
      <div class="preview-item">
        <h4>{{ previewData.titre }}</h4>

        <!-- Informations sur les images (exactement comme dans AdminCoursPlus) -->
        <div v-if="previewData.image" class="preview-image-info">
          <span class="image-indicator">🖼️ Images: {{ previewData.image }}</span>
          <div class="image-status-list">
            <span
              v-for="imgName in previewData.image.split(',').map(name => name.trim()).filter(Boolean)"
              :key="imgName"
              :class="['image-status', getImageFile(imgName) ? 'available' : 'missing']"
            >
              {{ imgName }}: {{ getImageFile(imgName) ? '✅ Disponible' : '❌ Manquante - Assurez-vous d\'avoir uploadé cette image' }}
            </span>
          </div>
        </div>

        <div class="preview-cours">
          <div class="preview-content" v-html="previewRenderedContent"></div>
        </div>
      </div>
    </div>

    <!-- Filtres -->
    <div class="filters">
      <div class="filter-group">
        <label>Filtrer par notion:</label>
        <input v-model="notionFilter" type="text" placeholder="Filtrer les notions..." class="filter-input" />
        <select v-model="filters.notion">
          <option value="all">Toutes les notions</option>
          <option v-for="notion in filteredNotionsForFilter" :key="notion.id" :value="notion.id">
            {{ formatNotionOption(notion) }}
          </option>
        </select>
      </div>
    </div>

    <!-- Tableau des cours -->
    <table class="admin-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Titre</th>
          <th>Notion</th>
          <th>Contexte</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="cours in paginatedCours" :key="cours.id">
          <td>{{ cours.id }}</td>
          <td>{{ cours.titre }}</td>
          <td>{{ getNotionName(cours.notion) }}</td>
          <td class="ctx-cell">{{ getNotionContextLabel(cours.notion) }}</td>
          <td>
            <AdminActionsButtons
              :item="cours"
              :actions="['edit', 'duplicate', 'delete']"
              edit-label="Éditer"
              duplicate-label="Dupliquer"
              confirm-message="Êtes-vous sûr de vouloir supprimer ce cours ?"
              @edit="editCours"
              @duplicate="handleDuplicateCours"
              @delete="handleDeleteCours"
            />
          </td>
        </tr>
        <tr v-if="paginatedCours.length === 0">
          <td colspan="7" style="text-align:center; font-style: italic;">Aucun cours trouvé.</td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="pagination">
      <button 
        class="pagination-btn" 
        @click="currentPage--" 
        :disabled="currentPage === 1"
      >
        Précédent
      </button>
      
      <div class="pagination-numbers">
        <button
          v-for="page in displayedPages"
          :key="page"
          class="pagination-number"
          :class="{ active: page === currentPage }"
          @click="currentPage = page"
        >
          {{ page }}
        </button>
      </div>
      
      <button 
        class="pagination-btn" 
        @click="currentPage++" 
        :disabled="currentPage === totalPages"
      >
        Suivant
      </button>
    </div>
    
    <div v-if="totalPages > 1" class="pagination-info">
      Page {{ currentPage }} sur {{ totalPages }} ({{ filteredCours.length }} cours au total)
    </div>

    <!-- Modale de duplication -->
    <div v-if="showDuplicateModal" class="modal-overlay" @click="cancelDuplicate">
      <div class="modal-content" @click.stop>
        <h3>Dupliquer le cours</h3>
        <p class="modal-description">
          Créer une copie de "<strong>{{ duplicateForm.originalCours?.titre }}</strong>"
        </p>

        <div class="modal-form">
          <div class="form-group">
            <label>Nouvelle notion:</label>
            <input
              v-model="duplicateNotionFilter"
              type="text"
              placeholder="Filtrer les notions..."
              class="filter-input"
              style="margin-bottom:0.5rem"
            />
            <select v-model="duplicateForm.newNotion" required>
              <option value="">Choisir une notion</option>
              <option v-for="notion in filteredNotionsForDuplicate" :key="notion.id" :value="notion.id">
                {{ formatNotionOption(notion) }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>Nouveau titre:</label>
            <input v-model="duplicateForm.newTitre" placeholder="Titre de la copie" required />
          </div>
        </div>

        <div class="modal-actions">
          <button class="btn-secondary" @click="cancelDuplicate">Annuler</button>
          <button class="btn-primary" @click="confirmDuplicate" :disabled="!duplicateForm.newNotion || !duplicateForm.newTitre.trim()">
            Dupliquer
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { getCours, createCours, updateCours, deleteCours, getCoursImages, createCoursImage, updateCoursImage, deleteCoursImage, updateCoursFormData, duplicateCoursImages } from '@/api/cours'
import { getNotions } from '@/api'
import { AdminActionsButtons } from '@/components/admin'
import { renderContentWithImages, renderMath } from '@/utils/scientificRenderer'

// ============================================================================
// CONSTANTES ET CONFIGURATION
// ============================================================================

const SUPPORTED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml']
const MAX_IMAGE_SIZE = 10 * 1024 * 1024 // 10MB

const cours = ref([])
// Chapitres supprimés
const notions = ref([])
const notionFormFilter = ref('')
const notionFilter = ref('')
// Chapitres supprimés
const form = ref({ 
  id: null, 
  notion: '', 
  titre: '', 
  contenu: '',
  ordre: 0,
  difficulty: 'medium',
  __pdf_file: null
})
const filters = ref({ notion: 'all' })

// Pagination
const currentPage = ref(1)
const itemsPerPage = 5

const showPreview = ref(false)
const previewData = ref(null)
const selectedImages = ref([])
const serverImages = ref([]) // images déjà enregistrées pour le cours en édition
const imagesInput = ref(null)
const imageManageLoading = ref(false)
const newImage = ref({ file: null, image_type: 'illustration', position: 0, legende: '' })
const newImageInput = ref(null)
const showDuplicateModal = ref(false)
const duplicateForm = ref({
  originalCours: null,
  newNotion: '',
  newTitre: ''
})
const duplicateNotionFilter = ref('')

// Normaliser le contenu pour ignorer les lignes vides (aligné sur AdminCoursPlus)
function normalizeContent(raw) {
  return String(raw || '')
    .split('\n')
    .map(line => line.trim())
    .filter(line => line.length > 0)
    .join('\n')
}

// Computed properties
const filteredCours = computed(() => {
  let filtered = cours.value
  if (filters.value.notion && filters.value.notion !== 'all') {
    filtered = filtered.filter(c => String(c.notion) === String(filters.value.notion))
  }
  return filtered.sort((a, b) => (a.ordre || 0) - (b.ordre || 0))
})

const filteredNotionsForForm = computed(() => {
  if (!notionFormFilter.value) return notions.value
  const query = notionFormFilter.value.toLowerCase()
  return notions.value.filter(n => (formatNotionOption(n) || '').toLowerCase().includes(query))
})

const filteredNotionsForFilter = computed(() => {
  if (!notionFilter.value) return notions.value
  const query = notionFilter.value.toLowerCase()
  return notions.value.filter(n => (formatNotionOption(n) || '').toLowerCase().includes(query))
})

const filteredNotionsForDuplicate = computed(() => {
  if (!duplicateNotionFilter.value) return notions.value
  const q = duplicateNotionFilter.value.toLowerCase()
  return notions.value.filter(n => {
    const niveauNom = n.niveau_nom
      || (n.contexte_detail && n.contexte_detail.niveau && n.contexte_detail.niveau.nom)
      || ''
    const searchable = [
      n.titre,
      n.nom,
      n.theme_nom,
      n.matiere_nom,
      niveauNom
    ].filter(Boolean).join(' ').toLowerCase()
    return searchable.includes(q)
  })
})

// Computed properties pour la pagination
const totalPages = computed(() => {
  const total = filteredCours.value.length
  return Math.ceil(total / itemsPerPage)
})

const paginatedCours = computed(() => {
  const allFiltered = filteredCours.value
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return allFiltered.slice(start, end)
})

const displayedPages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value
  
  // Afficher au maximum 5 numéros de page
  let startPage = Math.max(1, current - 2)
  let endPage = Math.min(total, current + 2)
  
  // Ajuster si on est proche du début ou de la fin
  if (current <= 3) {
    endPage = Math.min(5, total)
  }
  if (current >= total - 2) {
    startPage = Math.max(1, total - 4)
  }
  
  for (let i = startPage; i <= endPage; i++) {
    pages.push(i)
  }
  
  return pages
})

async function load() {
  try {
    const [nts, cResp] = await Promise.all([
      getNotions(),
      getCours()
    ])
    notions.value = Array.isArray(nts) ? nts : (nts?.data || [])
    cours.value = Array.isArray(cResp?.data) ? cResp.data : (Array.isArray(cResp) ? cResp : [])
  } catch (error) {
    console.error('[AdminCours] Erreur lors du chargement:', error)
    cours.value = []
    // Chapitres supprimés
    notions.value = []
  }
}

onMounted(load)

// Watcher pour réinitialiser la page courante quand les filtres changent
watch(() => filters.value.notion, () => {
  currentPage.value = 1
})

function resetForm() {
  form.value = {
    id: null,
    notion: '',
    titre: '',
    contenu: '',
    ordre: 0,
    difficulty: 'medium'
  }
  showPreview.value = false
  previewData.value = null
  selectedImages.value = []
  serverImages.value = []
  if (imagesInput.value) imagesInput.value.value = ''
  form.value.__pdf_file = null
}

// ============================================================================
// GESTION DES IMAGES
// ============================================================================

function handleImagesSelect(event) {
  const files = Array.from(event.target.files)
  files.forEach(file => {
    try {
      if (!SUPPORTED_IMAGE_TYPES.includes(file.type)) {
        alert(`Type de fichier non supporté: ${file.name}. Utilisez JPG, PNG, GIF, WebP ou SVG.`)
        return
      }
      if (file.size > MAX_IMAGE_SIZE) {
        alert(`Fichier trop volumineux: ${file.name}. Taille maximale: 10MB.`)
        return
      }
      selectedImages.value.push(file)
    } catch (error) {
      console.error('Erreur lors de l\'ajout de l\'image:', error)
      alert(`Erreur lors de l'ajout de ${file.name}`)
    }
  })
}

function removeSelectedImage(index) {
  selectedImages.value.splice(index, 1)
}

function getImagePreview(file) {
  return URL.createObjectURL(file)
}

function onSelectPdf(event) {
  const file = event?.target?.files?.[0]
  if (file && file.type !== 'application/pdf') {
    alert('Veuillez sélectionner un fichier PDF')
    return
  }
  form.value.__pdf_file = file || null
}

// =========================
// Gestion des images côté serveur (édition)
// =========================
function onSelectReplaceFile(rowIndex, event) {
  const file = event?.target?.files?.[0]
  if (!file) return
  serverImages.value[rowIndex].__replace_file = file
}

async function saveImageRow(row) {
  try {
    const payload = {
      cours: form.value.id,
      image_type: row.image_type,
      position: row.position,
      legende: row.legende
    }
    if (row.__replace_file) {
      payload.image = row.__replace_file
    }
    if (row.id) {
      await updateCoursImage(row.id, payload)
    }
    const res = await getCoursImages(form.value.id)
    const imgs = Array.isArray(res?.data) ? res.data : (Array.isArray(res) ? res : [])
    serverImages.value = imgs
      .slice()
      .sort((a, b) => (a.position || 0) - (b.position || 0))
  } catch (e) {
    console.error('Erreur saveImageRow', e)
    alert('Erreur lors de la sauvegarde de l\'image')
  }
}

async function removeImageRow(row) {
  if (!row.id) return
  if (!confirm('Supprimer cette image ?')) return
  try {
    await deleteCoursImage(row.id)
    serverImages.value = serverImages.value.filter(img => img.id !== row.id)
  } catch (e) {
    console.error('Erreur removeImageRow', e)
    alert('Suppression impossible')
  }
}

function onSelectNewImage(event) {
  const file = event?.target?.files?.[0]
  newImage.value.file = file || null
}

async function addNewImage() {
  if (!form.value.id) return
  if (!newImage.value.file) {
    alert('Choisissez un fichier image')
    return
  }
  try {
    const payload = {
      cours: form.value.id,
      image: newImage.value.file,
      image_type: newImage.value.image_type || 'illustration',
      position: newImage.value.position || (serverImages.value.length + 1),
      legende: newImage.value.legende || ''
    }
    const res = await createCoursImage(payload)
    const created = res?.data || null
    if (created) {
      serverImages.value.push(created)
    } else {
      // fallback d'affichage immédiat
      serverImages.value.push({ id: Math.random().toString(36).slice(2), image: '', ...payload })
    }
    newImage.value = { file: null, image_type: 'illustration', position: 0, legende: '' }
    if (newImageInput.value) newImageInput.value.value = ''
  } catch (e) {
    console.error('Erreur addNewImage', e)
    alert('Erreur lors de l\'ajout de l\'image')
  }
}

async function handleSave() {
  if (!form.value.notion || !form.value.titre || !form.value.contenu) return

  try {
    const payload = {
      notion: Number(form.value.notion),
      titre: form.value.titre,
      contenu: normalizeContent(form.value.contenu),
      ordre: form.value.ordre,
      difficulty: form.value.difficulty || 'medium'
    }

    let courseId = form.value.id
    if (courseId) {
      await updateCours(courseId, payload)
    } else {
      const created = await createCours(payload)
      courseId = created?.data?.id || courseId
    }

    // Upload PDF si sélectionné
    if (form.value.__pdf_file && courseId) {
      const fd = new FormData()
      fd.append('pdf_file', form.value.__pdf_file)
      await updateCoursFormData(courseId, fd)
    }

    // Sauvegarder le chapitre actuel avant de reset le formulaire
    const currentNotion = form.value.notion

    resetForm()

    // Remettre le chapitre sélectionné pour permettre d'ajouter un autre cours dans le même chapitre
    form.value.notion = currentNotion

    await load()
  } catch (e) {
    console.error('[AdminCours] Erreur:', e)
  }
}

function editCours(cours) {
  const difficultyValue = cours.difficulty || 'medium'

  form.value = { 
    id: cours.id,
    notion: cours.notion,
    titre: cours.titre || '',
    contenu: cours.contenu || '',
    ordre: cours.ordre || 0,
    difficulty: difficultyValue,
    __pdf_file: null
  }
  
  // Masquer la prévisualisation lors de l'édition
  showPreview.value = false
  previewData.value = null
  // Charger les images existantes (depuis l'API) pour l'édition et la prévisualisation
  imageManageLoading.value = true
  ;(async () => {
    try {
      const res = await getCoursImages(cours.id)
      const imgs = Array.isArray(res?.data) ? res.data : (Array.isArray(res) ? res : [])
      serverImages.value = imgs
        .slice()
        .sort((a, b) => (a.position || 0) - (b.position || 0))
    } catch (e) {
      console.error('[AdminCours] Chargement images serveur échoué', e)
      serverImages.value = []
    } finally {
      imageManageLoading.value = false
    }
  })()
}

async function removeCours(id) {
  try {
    await deleteCours(id)
    await load()
  } catch (e) {
    console.error('Erreur:', e)
  }
}

// Nouvelle fonction qui utilise le composant AdminActionsButtons
function handleDeleteCours(cours) {
  removeCours(cours.id)
}

// Fonction pour dupliquer un cours
function handleDuplicateCours(cours) {
  duplicateForm.value = {
    originalCours: cours,
    newNotion: '',
    newTitre: `${cours.titre}`
  }
  duplicateNotionFilter.value = ''
  showDuplicateModal.value = true
}

// Fonction pour confirmer la duplication
async function confirmDuplicate() {
  if (!duplicateForm.value.newNotion || !duplicateForm.value.newTitre.trim()) {
    alert('Veuillez sélectionner une notion et saisir un titre pour la copie.')
    return
  }

  try {
    const original = duplicateForm.value.originalCours
    const payload = {
      notion: Number(duplicateForm.value.newNotion),
      titre: duplicateForm.value.newTitre.trim(),
      contenu: original.contenu,
      ordre: original.ordre || 0,
      difficulty: original.difficulty || 'medium'
    }

    console.log('Payload envoyé pour duplication cours:', payload)
    console.log('Original cours:', original)

    // Vérifier si la notion de destination a déjà un cours
    const existingCours = cours.value.find(c => String(c.notion) === String(duplicateForm.value.newNotion))
    console.log('Cours existant dans la notion de destination:', existingCours)

    let targetCoursId = null

    if (existingCours) {
      // Si un cours existe déjà, proposer de le remplacer
      const targetNotionName = getNotionName(duplicateForm.value.newNotion)
      const confirmReplace = confirm(
        `La notion "${targetNotionName}" a déjà un cours.\n\n` +
        `Titre actuel: "${existingCours.titre}"\n` +
        `Nouveau titre: "${duplicateForm.value.newTitre.trim()}"\n\n` +
        `Voulez-vous remplacer le cours existant ?`
      )

      if (!confirmReplace) {
        return
      }

      // Remplacer le cours existant
      await updateCours(existingCours.id, payload)
      targetCoursId = existingCours.id
      console.log('Cours existant mis à jour avec succès')
    } else {
      // Créer un nouveau cours
      const created = await createCours(payload)
      targetCoursId = created?.data?.id || created?.id || null
      console.log('Nouveau cours créé avec succès')
    }

    if (original?.id && targetCoursId) {
      await duplicateCourseImages(original.id, targetCoursId, !!existingCours)
    }

    await load()

    showDuplicateModal.value = false
    duplicateForm.value = {
      originalCours: null,
      newNotion: '',
      newTitre: ''
    }
    duplicateNotionFilter.value = ''

    alert('Cours dupliqué avec succès !')
  } catch (error) {
    console.error('Erreur lors de la duplication:', error)
    alert('Erreur lors de la duplication du cours.')
  }
}

// Fonction pour annuler la duplication
function cancelDuplicate() {
  showDuplicateModal.value = false
  duplicateForm.value = {
    originalCours: null,
    newNotion: '',
    newTitre: ''
  }
  duplicateNotionFilter.value = ''
}

// Fonction de prévisualisation (exactement comme dans AdminCoursPlus)
function handlePreview() {
  if (!form.value.titre || !form.value.contenu) {
    alert('Veuillez remplir au moins le titre et le contenu pour prévisualiser')
    return
  }

  // Créer une chaîne de noms d'images séparés par des virgules (comme dans AdminCoursPlus)
  const imageNames = selectedImages.value.map(img => img.name).join(',')

  previewData.value = {
    titre: form.value.titre,
    contenu: normalizeContent(form.value.contenu),
    image: imageNames, // Chaîne de noms d'images séparés par des virgules
    images: selectedImages.value,
    // Images côté serveur (existant) pour le mode édition, utilisées si aucune nouvelle image sélectionnée
    serverImages: serverImages.value
  }

  showPreview.value = true

  // Rendre les formules MathJax après la prévisualisation
  nextTick(() => {
    renderMath()
  })
}

function getNotionById(id) {
  return notions.value.find(x => String(x.id) === String(id))
}

function getNotionName(id) {
  const n = getNotionById(id)
  return n ? (n.titre || n.nom) : id
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
  const contextParts = [ctx.matiereNom, ctx.themeNom].filter(Boolean)
  const geographicParts = [ctx.paysNom, ctx.niveauNom].filter(Boolean)
  const contextLabel = contextParts.join(' / ')
  const geographicLabel = geographicParts.join(' / ')
  const parts = [
    n.titre || n.nom || '',
    contextLabel ? ' - ' + contextLabel : '',
    geographicLabel ? ' (' + geographicLabel + ')' : ''
  ]
    .filter(Boolean)
  return parts.join('')
}

function getNotionContextLabel(notionId) {
  const n = getNotionById(notionId)
  if (!n) return ''
  const matiereNom = n.matiere_nom || (n.contexte_detail && n.contexte_detail.matiere_nom) || ''
  const themeNom = n.theme_nom || ''
  const path = [matiereNom, themeNom, n.titre || n.nom].filter(Boolean)
  return path.join(' › ')
}

function getNotionContextCode(notionId) {
  const n = getNotionById(notionId)
  if (!n) return ''
  const tokens = [n.titre || n.nom, n.theme_nom, n.matiere_nom]
    .filter(Boolean)
    .map(t => slugify(t))
  return tokens.join('_')
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
  // Chapitres supprimés
  return null
})

// Fonction pour créer les données d'images pour la prévisualisation (comme dans AdminCoursPlus)
function getPreviewImages(imageString, coursData = null) {
  // 1) Si l'utilisateur a sélectionné de nouvelles images, on les utilise pour l'aperçu
  const hasNew = !!(coursData && Array.isArray(coursData.images) && coursData.images.length > 0)
  const server = coursData && Array.isArray(coursData.serverImages) ? coursData.serverImages : []
  if (!hasNew && server.length > 0) {
    return server.map((img, index) => ({
      id: img.id ?? `server-${index}`,
      image: img.image, // URL absolue fournie par le backend
      image_type: img.image_type || 'illustration',
      position: img.position || index + 1,
      legende: img.legende || ''
    }))
  }

  // 2) Sinon, reconstituer à partir des fichiers sélectionnés (création ou remplacement)
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

// Fonction pour récupérer un fichier image par nom (comme dans AdminCoursPlus)
function getImageFile(filename) {
  return selectedImages.value.find(img => img.name === filename)
}

// Contenu rendu de la prévisualisation avec rendu scientifique (comme dans AdminCoursPlus)
function renderPreviewContent(cours) {
  const images = getPreviewImages(cours.image, cours)

  // Pour l'aperçu admin, remplacer les marqueurs [IMAGE_X] par l'image correspondante (priorité: images serveur)
  let content = normalizeContent(cours.contenu)

  content = content.replace(/\[IMAGE_(\d+)\]/g, (match, positionStr) => {
    const position = parseInt(positionStr)
    const byPos = images.find(img => Number(img.position) === position) || images[position - 1]

    if (byPos && byPos.image) {
      return `
        <div class="preview-image-container" style="text-align: center; margin: 2em 0;">
          <img src="${byPos.image}" alt="Image ${position}" class="content-image" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
        </div>
      `
    }

    return `
      <div class="preview-image-placeholder">
        <div class="placeholder-icon">🖼️</div>
        <div class="placeholder-text">Image manquante: IMAGE_${position}</div>
        <div class="placeholder-hint">Uploadez cette image dans la section ci-dessus</div>
      </div>
    `
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

// Computed property pour le contenu rendu (utilise maintenant la fonction renderPreviewContent)
const previewRenderedContent = computed(() => {
  if (!previewData.value?.contenu) return ''
  return renderPreviewContent(previewData.value)
})

async function duplicateCourseImages(sourceCoursId, targetCoursId, replaceExisting = false) {
  if (!sourceCoursId || !targetCoursId) return
  try {
    await duplicateCoursImages({
      sourceCoursId,
      targetCoursId,
      replaceExisting
    })
  } catch (error) {
    console.error('[AdminCours] Duplication des images échouée', error)
  }
}

// Chapitres supprimés

function slugify(text) {
  return String(text || '')
    .normalize('NFD').replace(/\p{Diacritic}/gu, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '')
}

// Chapitres supprimés

// Chapitres supprimés
</script>

<style scoped>
.admin-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #1f2937;
}

.admin-form {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #374151;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.filter-input {
  margin-bottom: 0.5rem;
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.form-group textarea {
  resize: vertical;
  min-height: 120px;
}

.btn-primary {
  background: #3b82f6;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  margin-right: 0.5rem;
}

.btn-secondary {
  background: #6b7280;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  margin-right: 0.5rem;
}

.btn-danger {
  background: #ef4444;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
}

.btn-danger.small, .btn-secondary.small {
  padding: 0.4rem 0.75rem;
  font-size: 0.8rem;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.filter-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.filter-group input,
.filter-group select {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.admin-table th,
.admin-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.admin-table th {
  background: #f9fafb;
  font-weight: 600;
  color: #374151;
}

.admin-table tr:hover {
  background: #f9fafb;
}

.preview-section {
  margin-top: 2rem;
  margin-bottom: 2rem;
}

.preview-section h3 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #1f2937;
}

.preview-item {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.cours-preview {
  padding: 1.5rem;
}

.cours-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.cours-titre {
  margin: 0;
  color: #1f2937;
  font-size: 1.25rem;
  font-weight: 600;
}

.cours-contenu {
  margin-bottom: 1rem;
  line-height: 1.6;
  color: #374151;
}

.cours-meta {
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
  color: #6b7280;
  font-size: 0.875rem;
}

/* Styles pour l'upload d'images */
.images-file-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.selected-images {
  margin-top: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1rem;
  background: #f9fafb;
}

.selected-images h5 {
  margin: 0 0 0.5rem 0;
  color: #374151;
  font-size: 0.875rem;
  font-weight: 600;
}

.selected-image-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  margin-bottom: 0.5rem;
  background: white;
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
  color: #374151;
}

.btn-remove {
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Styles pour la prévisualisation des images (comme dans AdminCoursPlus) */
.preview-image-info {
  margin-bottom: 1rem;
}

.server-images-section {
  margin: 1rem 0 1.5rem;
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #fafafa;
}

.images-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.5rem;
}

.images-table th, .images-table td {
  border-bottom: 1px solid #e5e7eb;
  padding: 0.5rem;
}

.srv-preview {
  width: 100px;
  height: 70px;
  object-fit: cover;
  border-radius: 4px;
}

.add-image-form {
  margin-top: 1rem;
}

.add-grid {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr 0.5fr 1fr auto;
  gap: 0.5rem;
  align-items: center;
}

.muted {
  color: #6b7280;
  font-style: italic;
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

/* Styles pour la prévisualisation du cours (comme dans AdminCoursPlus) */
.preview-cours {
  background: #f8f9fa;
  border-radius: 6px;
  padding: 1rem;
}

.preview-content {
  line-height: 1.6;
  color: #333;
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
  max-width: 100%;
}

/* Styles pour les placeholders d'images (comme dans AdminCoursPlus) */
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

/* Styles pour la modale de duplication */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.modal-content h3 {
  margin: 0 0 1rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.modal-description {
  margin: 0 0 1.5rem 0;
  color: #6b7280;
  font-size: 0.9rem;
}

.modal-form {
  margin-bottom: 2rem;
}

.modal-form .form-group {
  margin-bottom: 1rem;
}

.modal-form .form-group:last-child {
  margin-bottom: 0;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.modal-actions .btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Pagination */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 2rem;
  padding: 1rem 0;
}

.pagination-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  transition: all 0.2s;
}

.pagination-btn:hover:not(:disabled) {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-numbers {
  display: flex;
  gap: 0.25rem;
}

.pagination-number {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  transition: all 0.2s;
  min-width: 2.5rem;
}

.pagination-number:hover {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.pagination-number.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

.pagination-info {
  text-align: center;
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.5rem;
  margin-bottom: 2rem;
}

.ctx-cell { 
  color: #64748b; 
  font-size: 0.8rem; 
  max-width: 320px; 
}
</style> 
