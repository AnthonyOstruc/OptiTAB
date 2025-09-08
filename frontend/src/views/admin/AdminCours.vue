<template>
  <div>
    <h2 class="admin-title">Gestion des Cours</h2>
    <form class="admin-form" @submit.prevent="handleSave">
      <div class="form-group">
        <label>Chapitre:</label>
        <select v-model="form.chapitre" required>
          <option value="">Choisir un chapitre</option>
          <option v-for="chapitre in chapitres" :key="chapitre.id" :value="chapitre.id">{{ formatChapitreOption(chapitre) }}</option>
        </select>
      </div>
      <div v-if="currentContext" class="context-panel">
        <div class="context-row"><strong>Matière:</strong> <span>{{ currentContext.matiereNom || '—' }}</span></div>
        <div class="context-row"><strong>Thème:</strong> <span>{{ currentContext.themeNom || '—' }}</span></div>
        <div class="context-row"><strong>Pays:</strong> <span>{{ currentContext.paysNom || '—' }}</span></div>
        <div class="context-row"><strong>Niveau:</strong> <span>{{ currentContext.niveauNom || '—' }}</span></div>
        <div class="context-row"><strong>Chemin:</strong> <span>{{ getContextLabelByChapitre(form.chapitre) }}</span></div>
        <div class="context-row"><strong>Code:</strong> <code>{{ getContextCodeByChapitre(form.chapitre) }}</code></div>
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
        <label>Ordre d'affichage:</label>
        <input v-model.number="form.ordre" type="number" min="0" />
      </div>
      
      <div class="form-group">
        <label>Difficulté:</label>
        <select v-model="form.difficulte">
          <option value="facile">Facile</option>
          <option value="moyen">Moyen</option>
          <option value="difficile">Difficile</option>
        </select>
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
          <div class="preview-header">
            <span class="difficulty-badge" :class="previewData.difficulty">{{ getDifficultyLabel(previewData.difficulty) }}</span>
            <span class="ordre-badge">Ordre: {{ previewData.ordre }}</span>
          </div>
          <div class="preview-content" v-html="previewRenderedContent"></div>
        </div>
      </div>
    </div>

    <!-- Filtres -->
    <div class="filters">
      <div class="filter-group">
        <label>Filtrer par chapitre:</label>
        <select v-model="filters.chapitre">
          <option value="">Tous les chapitres</option>
          <option v-for="chapitre in chapitres" :key="chapitre.id" :value="chapitre.id">
            {{ chapitre.nom }} ({{ chapitre.notion_nom }})
          </option>
        </select>
      </div>
      
      <div class="filter-group">
        <label>Rechercher:</label>
        <input v-model="filters.nom" type="text" placeholder="Rechercher dans le titre..." />
      </div>
    </div>

    <!-- Tableau des cours -->
    <table class="admin-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Titre</th>
          <th>Chapitre</th>
          <th>Contexte</th>
          <th>Ordre</th>
          <th>Difficulté</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="cours in filteredCours" :key="cours.id">
          <td>{{ cours.id }}</td>
          <td>{{ cours.titre }}</td>
          <td>{{ getChapitreName(cours.chapitre) }}</td>
          <td class="ctx-cell">{{ getContextLabelByChapitre(cours.chapitre) }}</td>
          <td>{{ cours.ordre || 0 }}</td>
          <td><span class="difficulte-badge" :class="`difficulte-${cours.difficulte || cours.difficulty || 'moyen'}`">{{ cours.difficulte || cours.difficulty || 'moyen' }}</span></td>
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
        <tr v-if="filteredCours.length === 0">
          <td colspan="7" style="text-align:center; font-style: italic;">Aucun cours trouvé.</td>
        </tr>
      </tbody>
    </table>

    <!-- Modale de duplication -->
    <div v-if="showDuplicateModal" class="modal-overlay" @click="cancelDuplicate">
      <div class="modal-content" @click.stop>
        <h3>Dupliquer le cours</h3>
        <p class="modal-description">
          Créer une copie de "<strong>{{ duplicateForm.originalCours?.titre }}</strong>"
        </p>

        <div class="modal-form">
          <div class="form-group">
            <label>Nouveau chapitre:</label>
            <select v-model="duplicateForm.newChapitre" required>
              <option value="">Choisir un chapitre</option>
              <option v-for="chapitre in chapitres" :key="chapitre.id" :value="chapitre.id">{{ formatChapitreOption(chapitre) }}</option>
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
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { getCours, createCours, updateCours, deleteCours } from '@/api/cours'
import { getChapitres, getNotions } from '@/api'
import { AdminActionsButtons } from '@/components/admin'
import { renderContentWithImages, renderMath } from '@/utils/scientificRenderer'

// ============================================================================
// CONSTANTES ET CONFIGURATION
// ============================================================================

const SUPPORTED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml']
const MAX_IMAGE_SIZE = 10 * 1024 * 1024 // 10MB

const cours = ref([])
const chapitres = ref([])
const notions = ref([])
const form = ref({ 
  id: null, 
  chapitre: '', 
  titre: '', 
  contenu: '', 
  ordre: 0,
  difficulte: 'moyen'
})
const filters = ref({
  chapitre: '',
  nom: ''
})
const showPreview = ref(false)
const previewData = ref(null)
const selectedImages = ref([])
const imagesInput = ref(null)
const showDuplicateModal = ref(false)
const duplicateForm = ref({
  originalCours: null,
  newChapitre: '',
  newTitre: ''
})

// Computed properties
const filteredCours = computed(() => {
  let filtered = cours.value
  
  if (filters.value.chapitre) {
    filtered = filtered.filter(c => c.chapitre == filters.value.chapitre)
  }
  
  if (filters.value.nom) {
    filtered = filtered.filter(c => 
      c.titre.toLowerCase().includes(filters.value.nom.toLowerCase())
    )
  }
  
  return filtered.sort((a, b) => (a.ordre || 0) - (b.ordre || 0))
})

async function load() {
  try {
    const [chs, nts, cResp] = await Promise.all([
      getChapitres(),
      getNotions(),
      getCours()
    ])
    chapitres.value = Array.isArray(chs) ? chs : (chs?.data || [])
    notions.value = Array.isArray(nts) ? nts : (nts?.data || [])
    cours.value = Array.isArray(cResp?.data) ? cResp.data : (Array.isArray(cResp) ? cResp : [])
  } catch (error) {
    console.error('[AdminCours] Erreur lors du chargement:', error)
    cours.value = []
    chapitres.value = []
    notions.value = []
  }
}

onMounted(load)

function resetForm() {
  form.value = {
    id: null,
    chapitre: '',
    titre: '',
    contenu: '',
    ordre: 0,
    difficulte: 'moyen'
  }
  showPreview.value = false
  previewData.value = null
  selectedImages.value = []
  if (imagesInput.value) imagesInput.value.value = ''
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

// Fonction pour obtenir le label de difficulté (comme dans AdminCoursPlus)
function getDifficultyLabel(difficulty) {
  const labels = {
    'easy': 'Facile',
    'medium': 'Moyen',
    'hard': 'Difficile'
  }
  return labels[difficulty] || difficulty
}

async function handleSave() {
  if (!form.value.chapitre || !form.value.titre || !form.value.contenu) return
  
  try {
    const difficultyMap = { 'facile': 'easy', 'moyen': 'medium', 'difficile': 'hard' }
    const payload = {
      chapitre: Number(form.value.chapitre),
      titre: form.value.titre,
      contenu: form.value.contenu,
      ordre: form.value.ordre,
      difficulty: difficultyMap[form.value.difficulte] || 'medium'
    }
    
    if (form.value.id) {
      await updateCours(form.value.id, payload)
    } else {
      await createCours(payload)
    }
    resetForm()
    await load()
  } catch (e) {
    console.error('[AdminCours] Erreur:', e)
  }
}

function editCours(cours) {
  // Mapping inverse pour la difficulté (anglais vers français)
  const difficultyMap = { 'easy': 'facile', 'medium': 'moyen', 'hard': 'difficile' }
  const difficulte = cours.difficulte || cours.difficulty || 'medium'
  const difficulteFr = difficultyMap[difficulte] || 'moyen'
  
  form.value = { 
    id: cours.id,
    chapitre: cours.chapitre,
    titre: cours.titre || '',
    contenu: cours.contenu || '',
    ordre: cours.ordre || 0,
    difficulte: difficulteFr
  }
  
  // Masquer la prévisualisation lors de l'édition
  showPreview.value = false
  previewData.value = null
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
    newChapitre: '',
    newTitre: `${cours.titre}`
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
    const original = duplicateForm.value.originalCours
    const difficultyMap = { 'facile': 'easy', 'moyen': 'medium', 'difficile': 'hard' }

    const payload = {
      chapitre: Number(duplicateForm.value.newChapitre),
      titre: duplicateForm.value.newTitre.trim(),
      contenu: original.contenu,
      ordre: original.ordre || 0,
      difficulty: original.difficulty || difficultyMap[original.difficulte] || 'medium'
    }

    console.log('Payload envoyé pour duplication cours:', payload)
    console.log('Original cours:', original)

    // Vérifier si le chapitre de destination a déjà un cours
    const existingCours = cours.value.find(c => c.chapitre == duplicateForm.value.newChapitre)
    console.log('Cours existant dans le chapitre de destination:', existingCours)

    if (existingCours) {
      // Si un cours existe déjà, proposer de le remplacer
      const confirmReplace = confirm(
        `Le chapitre "${getChapitreName(duplicateForm.value.newChapitre)}" a déjà un cours.\n\n` +
        `Titre actuel: "${existingCours.titre}"\n` +
        `Nouveau titre: "${duplicateForm.value.newTitre.trim()}"\n\n` +
        `Voulez-vous remplacer le cours existant ?`
      )

      if (!confirmReplace) {
        return
      }

      // Remplacer le cours existant
      await updateCours(existingCours.id, payload)
      console.log('Cours existant mis à jour avec succès')
    } else {
      // Créer un nouveau cours
      await createCours(payload)
      console.log('Nouveau cours créé avec succès')
    }

    await load()

    showDuplicateModal.value = false
    duplicateForm.value = {
      originalCours: null,
      newChapitre: '',
      newTitre: ''
    }

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
    newChapitre: '',
    newTitre: ''
  }
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
    contenu: form.value.contenu,
    ordre: form.value.ordre || 0,
    difficulte: form.value.difficulte || 'moyen',
    difficulty: form.value.difficulte === 'facile' ? 'easy' : form.value.difficulte === 'moyen' ? 'medium' : 'hard',
    image: imageNames, // Chaîne de noms d'images séparés par des virgules
    images: selectedImages.value
  }

  showPreview.value = true

  // Rendre les formules MathJax après la prévisualisation
  nextTick(() => {
    renderMath()
  })
}

// Helpers d'affichage (repris d'AdminExercices)
function getChapitreName(id) {
  const c = chapitres.value.find(x => String(x.id) === String(id))
  return c ? c.nom : id
}

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
  const c = chapitres.value.find(x => String(x.id) === String(form.value.chapitre))
  return c ? chapterContext(c) : null
})

// Fonction pour créer les données d'images pour la prévisualisation (comme dans AdminCoursPlus)
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

// Fonction pour récupérer un fichier image par nom (comme dans AdminCoursPlus)
function getImageFile(filename) {
  return selectedImages.value.find(img => img.name === filename)
}

// Contenu rendu de la prévisualisation avec rendu scientifique (comme dans AdminCoursPlus)
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

// Computed property pour le contenu rendu (utilise maintenant la fonction renderPreviewContent)
const previewRenderedContent = computed(() => {
  if (!previewData.value?.contenu) return ''
  return renderPreviewContent(previewData.value)
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

function getContextLabelByChapitre(chapitreId) {
  const c = chapitres.value.find(x => String(x.id) === String(chapitreId))
  if (!c) return ''
  const n = getNotionById(c.notion)
  const ctx = chapterContext(c)
  const path = [
    ctx?.matiereNom,
    ctx?.themeNom,
    n?.nom,
    c.nom,
    ctx?.paysNom,
    ctx?.niveauNom
  ].filter(Boolean)
  return path.join(' › ')
}

function getContextCodeByChapitre(chapitreId) {
  const c = chapitres.value.find(x => String(x.id) === String(chapitreId))
  if (!c) return ''
  const n = getNotionById(c.notion)
  const ctx = chapterContext(c)
  const tokens = [
    slugify(n?.nom),
    slugify(ctx?.themeNom),
    slugify(ctx?.matiereNom),
    slugify(ctx?.paysNom),
    slugify(ctx?.niveauNom)
  ].filter(Boolean)
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

.cours-ordre {
  font-weight: 500;
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
</style> 