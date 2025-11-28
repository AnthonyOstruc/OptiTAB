<template>
  <div>
    <h2 class="admin-title">Gestion des Exercices</h2>
    <form class="admin-form" @submit.prevent="handleSave">
      <!-- Sélecteur: on choisit la notion directement (chapitres supprimés) -->
      <div class="form-group">
        <label>Notion:</label>
        <input v-model="notionFormFilter" type="text" placeholder="Filtrer les notions..." class="filter-input" />
        <select v-model="form.notion" required>
          <option value="">Choisir une notion</option>
          <option v-for="n in filteredNotionsForForm" :key="n.id" :value="n.id">{{ formatNotionOption(n) }}</option>
        </select>
      </div>
      <div v-if="currentContext" class="context-panel">
        <!-- En-tête global supprimé (chapitres retirés) -->
        <div class="context-row"><strong>Matière:</strong> <span>{{ currentContext.matiereNom || '—' }}</span></div>
        <div class="context-row"><strong>Thème:</strong> <span>{{ currentContext.themeNom || '—' }}</span></div>
        <div class="context-row"><strong>Pays:</strong> <span>{{ currentContext.paysNom || '—' }}</span></div>
        <div class="context-row"><strong>Niveau:</strong> <span>{{ currentContext.niveauNom || '—' }}</span></div>
        <div class="context-row"><strong>Chemin:</strong> <span>{{ getNotionContextLabel(form.notion) }}</span></div>
        <div class="context-row"><strong>Code:</strong> <code>{{ getNotionContextCode(form.notion) }}</code></div>
        <!-- Stats globales supprimées (chapitres retirés) -->
      </div>
      
      <div class="form-group">
        <label>Titre:</label>
        <input v-model="form.nom" placeholder="Titre de l'exercice" required />
      </div>

      
      
      <div class="form-group">
        <label>Énoncé:</label>
        <textarea v-model="form.enonce" rows="4" required></textarea>
      </div>
      
      <div class="form-group">
        <label>Méthode de résolution:</label>
        <textarea v-model="form.etapes" rows="4" placeholder="Décrivez les étapes de résolution..."></textarea>
      </div>
      
      <div class="form-group">
        <label>Solution:</label>
        <textarea v-model="form.solution" rows="4"></textarea>
      </div>

      <!-- Images (optionnel) pour la prévisualisation immédiate lors de la création/édition -->
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
          Utilisez [IMAGE_1], [IMAGE_2], … dans l'énoncé/étapes/solution. Les fichiers sélectionnés servent à la prévisualisation et peuvent être enregistrés ci-dessous.
        </small>
        <div v-if="selectedImages.length > 0" class="selected-images">
          <h5>Images sélectionnées (aperçu uniquement) :</h5>
          <div v-for="(img, index) in selectedImages" :key="index" class="selected-image-item">
            <img :src="getImagePreview(img)" :alt="img.name" class="image-preview" />
            <span class="image-name">{{ img.name }}</span>
            <button type="button" class="btn-remove" @click="removeSelectedImage(index)">×</button>
          </div>
        </div>
      </div>

      <!-- Gestion des images enregistrées (mode édition) -->
      <div v-if="form.id" class="server-images-section">
        <h5>Images de l'exercice (enregistrées)</h5>
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
                    <option value="donnee">Donnée</option>
                    <option value="solution">Solution</option>
                    <option value="illustration">Illustration</option>
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
                <td style="white-space:nowrap; padding: 0.5rem;">
                  <div style="display: flex; gap: 0.5rem; align-items: center;">
                    <button type="button" class="btn-secondary small" @click="saveImageRow(img)">Enregistrer</button>
                    <button type="button" class="btn-danger small" @click="removeImageRow(img)">Supprimer</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          <div class="add-image-form">
            <h6>Ajouter une image</h6>
            <div class="add-grid">
              <input type="file" accept="image/*" ref="newImageInput" @change="onSelectNewImage($event)" />
              <select v-model="newImage.image_type">
                <option value="donnee">Donnée</option>
                <option value="solution">Solution</option>
                <option value="illustration">Illustration</option>
              </select>
              <input v-model.number="newImage.position" type="number" min="0" placeholder="Position" />
              <input v-model="newImage.legende" placeholder="Légende (optionnel)" />
              <button type="button" class="btn-primary" @click="addNewImage">Ajouter</button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="form-group">
        <label>Difficulté:</label>
        <select v-model="form.difficulte" class="difficulty-select">
          <option value="facile">Facile</option>
          <option value="moyen">Moyen</option>
          <option value="difficile">Difficile</option>
        </select>
      </div>
      
      <div class="form-actions">
        <button class="btn-primary" type="submit">{{ form.id ? 'Mettre à jour' : 'Créer' }}</button>
        <button v-if="form.id" class="btn-secondary" type="button" @click="resetForm">Annuler</button>
        <button class="btn-preview" type="button" @click="handlePreview">Prévisualiser</button>
      </div>
    </form>

    <!-- Prévisualisation -->
    <div v-if="showPreview && previewData" class="preview-section">
      <div class="preview-header">
        <h3>Aperçu de l'exercice {{ form.id ? '(Mode édition)' : '(Mode création)' }}</h3>
        <button class="btn-close-preview" @click="closePreview" title="Fermer la prévisualisation">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 6L6 18"/>
            <path d="M6 6l12 12"/>
          </svg>
        </button>
      </div>
      <div class="preview-item">
        <ExerciceQCM 
          :eid="`preview-${form.id || 'new'}`" 
          :titre="previewData.titre" 
          :instruction="previewData.instruction" 
          :etapes="previewData.etapes" 
          :solution="previewData.solution" 
          :difficulty="previewData.difficulty"
          :preview-images="previewImages"
        />
      </div>
    </div>

    <!-- Filtres -->
    <div class="filters">
      <div class="filter-group">
        <label>Filtrer par notion:</label>
        <input v-model="notionFilter" type="text" placeholder="Filtrer les notions..." class="filter-input" />
        <select v-model="filters.notion">
          <option value="">Toutes les notions</option>
          <option v-for="n in filteredNotionsForFilter" :key="n.id" :value="n.id">{{ formatNotionOption(n) }}</option>
        </select>
      </div>
    </div>

    <!-- Tableau des exercices -->
    <table class="admin-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Titre</th>
          <th>Notion</th>
          <th>Contexte</th>
          <th>Difficulté</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="exercice in paginatedExercices" :key="exercice.id">
          <td>{{ exercice.id }}</td>
          <td>{{ exercice.titre || exercice.nom }}</td>
          <td>{{ getNotionName(exercice.notion) }}</td>
          <td class="ctx-cell">{{ getNotionContextLabel(exercice.notion) }}</td>
          <td>
            <span class="difficulte-badge" :class="`difficulte-${exercice.difficulte || exercice.difficulty}`">
              {{ exercice.difficulte || exercice.difficulty }}
            </span>
          </td>
          <td>
            <AdminActionsButtons
              :item="exercice"
              :actions="['edit', 'duplicate', 'delete']"
              edit-label="Éditer"
              duplicate-label="Dupliquer"
              confirm-message="Êtes-vous sûr de vouloir supprimer cet exercice ?"
              @edit="editExercice"
              @duplicate="handleDuplicateExercice"
              @delete="handleDeleteExercice"
            />
          </td>
        </tr>
        <tr v-if="paginatedExercices.length === 0">
          <td colspan="6" style="text-align:center; font-style: italic;">Aucun exercice trouvé.</td>
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
      Page {{ currentPage }} sur {{ totalPages }} ({{ filteredExercices.length }} exercice(s) au total)
    </div>

    <!-- Modale de duplication -->
    <div v-if="showDuplicateModal" class="modal-overlay" @click="cancelDuplicate">
      <div class="modal-content" @click.stop>
        <h3>Dupliquer l'exercice</h3>
        <p class="modal-description">
          Créer une copie de "<strong>{{ duplicateForm.originalExercice?.titre || duplicateForm.originalExercice?.nom }}</strong>"
        </p>

        <div class="modal-form">
          <div class="form-group">
            <label>Nouvelle notion:</label>
            <select v-model="duplicateForm.newNotion" required>
              <option value="">Choisir une notion</option>
              <option v-for="n in notions" :key="n.id" :value="n.id">{{ (n.titre || n.nom) }}</option>
            </select>
          </div>

          <div class="form-group">
            <label>Nouveau titre:</label>
            <input v-model="duplicateForm.newTitre" placeholder="Titre de la copie" required />
          </div>
        </div>

        <div class="modal-actions">
          <button class="btn-secondary" @click="cancelDuplicate">Annuler</button>
          <button class="btn-primary" @click="confirmDuplicate" :disabled="!duplicateForm.newChapitre || !duplicateForm.newTitre.trim()">
            Dupliquer
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { getExercices, createExercice, updateExercice, deleteExercice, getNotions, getExerciceImages, createExerciceImage, updateExerciceImage, deleteExerciceImage } from '@/api'
import PaysNiveauxSelector from '@/components/admin/PaysNiveauxSelector.vue'
import PaysNiveauxDisplay from '@/components/admin/PaysNiveauxDisplay.vue'
import { AdminActionsButtons } from '@/components/admin'
import ExerciceQCM from '@/components/UI/ExerciceQCM.vue'

const exercices = ref([])
// Chapitres supprimés
const notions = ref([])
const notionFormFilter = ref('')
const notionFilter = ref('')
const selection = ref({})
const form = ref({ 
  id: null, 
  notion: '', 
  nom: '',
  enonce: '', 
  etapes: '', 
  solution: '', 
  difficulte: 'moyen',
  niveaux: []
})
const filters = ref({ notion: '' })

// Pagination
const currentPage = ref(1)
const itemsPerPage = 5

const showPreview = ref(false)
const previewData = ref(null)
const previewImages = ref([])
const selectedImages = ref([])
const imagesInput = ref(null)
const serverImages = ref([])
const imageManageLoading = ref(false)
const newImage = ref({ file: null, image_type: 'donnee', position: 0, legende: '' })
const newImageInput = ref(null)
const showDuplicateModal = ref(false)
const duplicateForm = ref({
  originalExercice: null,
  newChapitre: '',
  newTitre: ''
})

// Computed properties
const filteredExercices = computed(() => {
  let filtered = exercices.value

  if (filters.value.notion) {
    filtered = filtered.filter(e => String(e.notion) === String(filters.value.notion))
  }

  return filtered
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

// Computed properties pour la pagination
const totalPages = computed(() => {
  const total = filteredExercices.value.length
  return Math.ceil(total / itemsPerPage)
})

const paginatedExercices = computed(() => {
  const allFiltered = filteredExercices.value
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

async function loadInitial() {
  try {
    const nts = await getNotions()
    notions.value = nts || []
    await reloadExercices()
  } catch (error) {
    console.error('[AdminExercices] Erreur chargement chapitres:', error)
  }
}

onMounted(loadInitial)

// Watchers simples

watch(() => form.value.notion, async () => {
  await reloadExercices()
})

// Watcher pour réinitialiser la page courante quand les filtres changent
watch(() => filters.value.notion, () => {
  currentPage.value = 1
})

async function reloadExercices() {
  try {
    const params = {}
    // Ne pas filtrer quand "Tous les chapitres" est sélectionné
    if (form.value.notion) params.notion = Number(form.value.notion)
    exercices.value = await getExercices(params)
  } catch (error) {
    console.error('[AdminExercices] Erreur lors du chargement exercices:', error)
    exercices.value = []
  }
}

function resetForm() {
  form.value = { 
    id: null, 
    notion: '', 
    nom: '',
    type: '', 
    enonce: '', 
    etapes: '', 
    solution: '', 
    difficulte: 'moyen',
    niveaux: []
  }
  showPreview.value = false
  previewData.value = null
  previewImages.value = []
  selectedImages.value = []
  serverImages.value = []
  if (imagesInput.value) imagesInput.value.value = ''
}

async function handleSave() {
  if (!form.value.notion || !form.value.enonce) return

  try {
    const difficultyMap = { 'facile': 'easy', 'moyen': 'medium', 'difficile': 'hard' }
    const payload = {
      notion: Number(form.value.notion),
      titre: form.value.nom || 'Exercice',
      contenu: form.value.enonce,
      difficulty: difficultyMap[form.value.difficulte] || 'medium',
      // Champs compatibles modèle Exercice
      question: form.value.enonce,
      reponse_correcte: form.value.solution || '',
      etapes: form.value.etapes || '',
      points: 1
    }

    if (form.value.id) {
      await updateExercice(form.value.id, payload)
    } else {
      await createExercice(payload)
    }

    // Sauvegarder le chapitre actuel avant de reset le formulaire
    const currentNotion = form.value.notion

    resetForm()

    // Remettre le chapitre sélectionné pour permettre d'ajouter un autre exercice dans le même chapitre
    form.value.notion = currentNotion

    await reloadExercices()
  } catch (e) {
    console.error('[AdminExercices] Erreur:', e)
  }
}

function editExercice(exercice) {
  // Extraire les IDs des niveaux pour le composant PaysNiveauxSelector
  const niveauxIds = exercice.niveaux ? exercice.niveaux.map(n => n.id) : []
  
  // Mapper les champs de l'exercice vers le formulaire
  const difficultyMap = { 'easy': 'facile', 'medium': 'moyen', 'hard': 'difficile' }
  
  form.value = { 
    id: exercice.id,
    notion: exercice.notion,
    nom: exercice.titre || exercice.nom || '',
    enonce: exercice.contenu || exercice.question || exercice.enonce || '',
    etapes: exercice.etapes || '',
    solution: exercice.reponse_correcte || exercice.solution || '',
    difficulte: difficultyMap[exercice.difficulty] || exercice.difficulte || 'moyen',
    niveaux: niveauxIds
  }
  
  // Masquer la prévisualisation lors de l'édition
  showPreview.value = false
  previewData.value = null
  // Charger les images existantes depuis l'API
  imageManageLoading.value = true
  ;(async () => {
    try {
      const { data } = await getExerciceImages(exercice.id)
      serverImages.value = (data || []).slice().sort((a, b) => (a.position || 0) - (b.position || 0))
    } catch (e) {
      serverImages.value = []
    } finally {
      imageManageLoading.value = false
    }
  })()
  
  console.log('🔍 Exercice à éditer:', exercice)
  console.log('📝 Formulaire rempli:', form.value)
}

async function removeExercice(id) {
  try {
    await deleteExercice(id)
    await reloadExercices()
  } catch (e) {
    console.error('Erreur:', e)
  }
}

// Nouvelle fonction qui utilise le composant AdminActionsButtons
function handleDeleteExercice(exercice) {
  removeExercice(exercice.id)
}

// Fonction pour dupliquer un exercice
function handleDuplicateExercice(exercice) {
  duplicateForm.value = {
    originalExercice: exercice,
    newChapitre: '',
    newTitre: `${exercice.titre || exercice.nom}`
  }
  showDuplicateModal.value = true
}

// Fonction pour confirmer la duplication
async function confirmDuplicate() {
  if (!duplicateForm.value.newChapitre || !duplicateForm.value.newTitre.trim()) {
    alert('Veuillez sélectionner un chapitre et saisir un titre pour la copie.')
    return
  }

  try {
    const original = duplicateForm.value.originalExercice
    const difficultyMap = { 'easy': 'easy', 'medium': 'medium', 'hard': 'hard' }

    const payload = {
      notion: Number(form.value.notion || duplicateForm.value.newChapitre),
      titre: duplicateForm.value.newTitre.trim(),
      contenu: original.contenu || original.question || original.enonce || '',
      difficulty: original.difficulty || difficultyMap[original.difficulte] || 'medium',
      question: original.contenu || original.question || original.enonce || '',
      reponse_correcte: original.reponse_correcte || original.solution || '',
      etapes: original.etapes || '',
      points: original.points || 1
    }

    await createExercice(payload)
    await reloadExercices()

    showDuplicateModal.value = false
    duplicateForm.value = {
      originalExercice: null,
      newChapitre: '',
      newTitre: ''
    }

    alert('Exercice dupliqué avec succès !')
  } catch (error) {
    console.error('Erreur lors de la duplication:', error)
    alert('Erreur lors de la duplication de l\'exercice.')
  }
}

// Fonction pour annuler la duplication
function cancelDuplicate() {
  showDuplicateModal.value = false
  duplicateForm.value = {
    originalExercice: null,
    newChapitre: '',
    newTitre: ''
  }
}

// Fonction de prévisualisation
function handlePreview() {
  if (!form.value.nom || !form.value.enonce) {
    alert('Veuillez remplir au moins le titre et l\'énoncé pour prévisualiser')
    return
  }
  
  const difficultyMap = { 'facile': 'easy', 'moyen': 'medium', 'difficile': 'hard' }
  
  previewData.value = {
    titre: form.value.nom,
    instruction: form.value.enonce,
    etapes: form.value.etapes || '',
    solution: form.value.solution || '',
    difficulty: difficultyMap[form.value.difficulte] || 'medium'
  }

  // Construire les images d'aperçu: priorité aux nouveaux fichiers, sinon images enregistrées
  if (selectedImages.value.length > 0) {
    previewImages.value = selectedImages.value.map((file, index) => ({
      id: `preview-${index}`,
      image: URL.createObjectURL(file),
      image_type: 'donnee',
      position: index + 1,
      legende: file.name
    }))
  } else if (serverImages.value.length > 0) {
    previewImages.value = serverImages.value
      .slice()
      .sort((a, b) => (a.position || 0) - (b.position || 0))
      .map((img, idx) => ({
        id: img.id ?? `server-${idx}`,
        image: img.image,
        image_type: img.image_type || 'donnee',
        position: img.position || idx + 1,
        legende: img.legende || ''
      }))
  } else {
    previewImages.value = []
  }
  
  showPreview.value = true
}

// Fonction pour fermer la prévisualisation
function closePreview() {
  showPreview.value = false
  previewData.value = null
  previewImages.value = []
}

// ============================
// Images – preview (nouveaux fichiers) + gestion serveur
// ============================
function handleImagesSelect(event) {
  const files = Array.from(event.target.files || [])
  files.forEach(file => {
    try {
      selectedImages.value.push(file)
    } catch (_) {}
  })
}

function removeSelectedImage(index) {
  selectedImages.value.splice(index, 1)
}

function getImagePreview(file) {
  return URL.createObjectURL(file)
}

function onSelectReplaceFile(rowIndex, event) {
  const file = event?.target?.files?.[0]
  if (!file) return
  serverImages.value[rowIndex].__replace_file = file
}

async function saveImageRow(row) {
  try {
    if (!form.value.id || !row?.id) return
    const payload = {
      exercice: form.value.id,
      image_type: row.image_type,
      position: row.position,
      legende: row.legende
    }
    if (row.__replace_file) payload.image = row.__replace_file
    await updateExerciceImage(row.id, payload)
    const { data } = await getExerciceImages(form.value.id)
    serverImages.value = (data || []).slice().sort((a, b) => (a.position || 0) - (b.position || 0))
  } catch (e) {
    console.error('[AdminExercices] saveImageRow error', e)
    alert("Erreur lors de l'enregistrement de l'image")
  }
}

async function removeImageRow(row) {
  if (!row?.id) return
  if (!confirm('Supprimer cette image ?')) return
  try {
    await deleteExerciceImage(row.id)
    serverImages.value = serverImages.value.filter(img => img.id !== row.id)
  } catch (e) {
    console.error('[AdminExercices] removeImageRow error', e)
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
      exercice: form.value.id,
      image: newImage.value.file,
      image_type: newImage.value.image_type || 'donnee',
      position: newImage.value.position || (serverImages.value.length + 1),
      legende: newImage.value.legende || ''
    }
    const res = await createExerciceImage(payload)
    const created = res?.data || null
    if (created) serverImages.value.push(created)
    newImage.value = { file: null, image_type: 'donnee', position: 0, legende: '' }
    if (newImageInput.value) newImageInput.value.value = ''
  } catch (e) {
    console.error('[AdminExercices] addNewImage error', e)
    alert("Erreur lors de l'ajout de l'image")
  }
}

// Helpers d'affichage
// Chapitres supprimés

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

// Fonction pour obtenir le contexte global de tous les chapitres
function getAllChaptersContext() {
  if (chapitres.value.length === 0) return null
  
  // Collecter toutes les matières, thèmes, pays et niveaux uniques
  const matieres = new Set()
  const themes = new Set()
  const pays = new Set()
  const niveaux = new Set()
  
  chapitres.value.forEach(chapitre => {
    const notion = getNotionById(chapitre.notion)
    if (notion) {
      if (notion.matiere_nom) matieres.add(notion.matiere_nom)
      if (notion.theme_nom) themes.add(notion.theme_nom)
      if (notion.contexte_detail?.pays?.nom) pays.add(notion.contexte_detail.pays.nom)
      if (notion.contexte_detail?.niveau?.nom) niveaux.add(notion.contexte_detail.niveau.nom)
    }
  })
  
  return {
    matiereNom: matieres.size > 0 ? Array.from(matieres).join(', ') : '—',
    themeNom: themes.size > 0 ? Array.from(themes).join(', ') : '—',
    paysNom: pays.size > 0 ? Array.from(pays).join(', ') : '—',
    niveauNom: niveaux.size > 0 ? Array.from(niveaux).join(', ') : '—',
    isAllChapters: true
  }
}

const currentContext = computed(() => {
  const n = notions.value.find(x => String(x.id) === String(form.value.notion))
  if (!n) return null
  const matiereNom = n.matiere_nom || (n.contexte_detail && n.contexte_detail.matiere_nom) || ''
  const themeNom = n.theme_nom || ''
  const paysNom = n.contexte_detail && n.contexte_detail.pays ? n.contexte_detail.pays.nom : ''
  const niveauNom = n.contexte_detail && n.contexte_detail.niveau ? n.contexte_detail.niveau.nom : ''
  return { matiereNom, themeNom, paysNom, niveauNom }
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

function slugify(text) {
  return String(text || '')
    .normalize('NFD').replace(/\p{Diacritic}/gu, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '')
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
  const tokens = [n.titre || n.nom, n.theme_nom, n.matiere_nom].filter(Boolean).map(t => slugify(t))
  return tokens.join('_')
}
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
  min-height: 100px;
}

.btn-primary {
  background: #3b82f6;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  margin-right: 0;
  min-width: 120px;
  white-space: nowrap;
}

.btn-secondary {
  background: #6b7280;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  margin-right: 0;
  min-width: 100px;
  white-space: nowrap;
}

.btn-preview {
  background: #6b7280;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  margin-right: 0;
  min-width: 120px;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.btn-preview:hover {
  background: #4b5563;
  transform: translateY(-1px);
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
  align-items: center;
  justify-content: flex-start;
}

.difficulty-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  background: white;
  cursor: pointer;
  transition: border-color 0.2s ease;
}

.difficulty-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.context-panel {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
}

.context-header {
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.context-header h4 {
  margin: 0;
  color: #1e293b;
  font-size: 1rem;
  font-weight: 600;
}

.context-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.25rem 0;
  border-bottom: 1px solid #f1f5f9;
}

.context-row:last-child {
  border-bottom: none;
}

.context-row strong {
  color: #374151;
  font-weight: 500;
  min-width: 80px;
}

.context-row span {
  color: #6b7280;
  text-align: right;
  flex: 1;
}

.context-row code {
  background: #f1f5f9;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.75rem;
  color: #475569;
}

.context-stats {
  display: flex;
  gap: 1rem;
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid #e2e8f0;
}

.stat-item {
  background: #e0f2fe;
  color: #0369a1;
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
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
  margin-right: 0;
  min-width: 80px;
  white-space: nowrap;
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

.ctx-cell { color: #64748b; font-size: 0.8rem; max-width: 320px; }

.admin-table th {
  background: #f9fafb;
  font-weight: 600;
  color: #374151;
}

.admin-table tr:hover {
  background: #f9fafb;
}

.type-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
}

.type-qcm {
  background: #dbeafe;
  color: #1e40af;
}

.type-calcul {
  background: #dcfce7;
  color: #166534;
}

.type-demonstration {
  background: #fef3c7;
  color: #92400e;
}

.type-probleme {
  background: #fce7f3;
  color: #be185d;
}

.difficulte-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
}

.difficulte-facile {
  background: #dcfce7;
  color: #166534;
}

.difficulte-moyen {
  background: #fef3c7;
  color: #92400e;
}

.difficulte-difficile {
  background: #fee2e2;
  color: #991b1b;
}

.context-panel { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 1rem; }
.context-row { display: flex; gap: 0.5rem; font-size: 0.9rem; color: #334155; }

.preview-section {
  margin-top: 2rem;
  margin-bottom: 2rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.preview-section h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: #1f2937;
}

.btn-close-preview {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.375rem;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close-preview:hover {
  background: #f3f4f6;
  color: #374151;
}

.preview-item {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Images UI */
.images-file-input { width: 100%; padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 0.375rem; font-size: 0.875rem; margin-bottom: 0.5rem; }
.selected-images { margin-top: 1rem; border: 1px solid #e5e7eb; border-radius: 0.5rem; padding: 1rem; background: #f9fafb; }
.selected-image-item { display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem; border: 1px solid #e5e7eb; border-radius: 0.375rem; margin-bottom: 0.5rem; background: white; }
.image-preview { width: 40px; height: 30px; object-fit: cover; border-radius: 4px; }
.image-name { flex: 1; font-size: 0.875rem; color: #374151; }
.btn-remove { background: #ef4444; color: white; border: none; border-radius: 50%; width: 24px; height: 24px; cursor: pointer; font-size: 1rem; line-height: 1; display: flex; align-items: center; justify-content: center; }

.server-images-section { margin: 1rem 0 1.5rem; padding: 1rem; border: 1px solid #e5e7eb; border-radius: 8px; background: #fafafa; }
.images-table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; }
.images-table th, .images-table td { border-bottom: 1px solid #e5e7eb; padding: 0.5rem; }
.srv-preview { width: 100px; height: 70px; object-fit: cover; border-radius: 4px; }
.add-image-form { 
  margin-top: 1rem; 
  padding: 1rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
}

.add-image-form h6 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
}
.add-grid { 
  display: grid; 
  grid-template-columns: 1.5fr 1fr 0.6fr 1.2fr 120px; 
  gap: 0.75rem; 
  align-items: center; 
  padding: 0.75rem;
  background: #f9fafb;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
  min-width: 0;
}

.add-grid input[type="file"] {
  min-width: 0;
}

.add-grid select {
  min-width: 0;
}

.add-grid input[type="number"] {
  min-width: 0;
}

.add-grid input[type="text"] {
  min-width: 0;
}

.add-grid .btn-primary {
  min-width: 100px;
  white-space: nowrap;
}
.muted { color: #6b7280; font-style: italic; }

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

/* Responsive pour la prévisualisation */
@media (max-width: 768px) {
  .preview-section {
    margin: 1rem 0;
    padding: 1rem;
  }
  
  .preview-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .form-actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .form-actions button {
    width: 100%;
    margin-right: 0;
    margin-bottom: 0.5rem;
  }
  
  .form-actions button:last-child {
    margin-bottom: 0;
  }
}
</style> 
