<template>
  <div class="admin-sheets">
    <!-- Guide d'utilisation -->
    <div class="format-help">
      <h3>📋 Guide de création des fiches de synthèse</h3>
      <div class="format-example">
        <pre><code>Titre: [Titre de la fiche]
Notion: [ID de la notion]
Difficulté: [easy/medium/hard] (optionnel, défaut: medium)
Temps de lecture: [nombre] (en minutes, optionnel, défaut: 5)
Statut: [actif/inactif] (optionnel, défaut: actif)
Points clés: [point1,point2,point3] (optionnel, séparés par des virgules)

=== CONTENU ===

[Contenu principal de la fiche avec HTML/LaTeX supporté]

=== EXEMPLES ===

[Exemples pratiques et exercices d'application]

=== CONSEILS ===

[Conseils méthodologiques et astuces]</code></pre>
      </div>
      <div class="format-notes">
        <p><strong>Notes importantes :</strong></p>
        <ul>
          <li><strong>⚠️ Champs obligatoires :</strong> <code>Titre</code> et contenu principal</li>
          <li><strong>Notion :</strong> Utilisez l'ID de la notion (trouvable dans la liste des notions)</li>
          <li><strong>Difficulté :</strong> <code>easy</code>, <code>medium</code> ou <code>hard</code> uniquement</li>
          <li><strong>Temps de lecture :</strong> Estimation en minutes (aide les étudiants à planifier)</li>
          <li><strong>Points clés :</strong> Résumé des concepts essentiels, séparés par des virgules</li>
          <li><strong>Sections :</strong> <code>=== CONTENU ===</code>, <code>=== EXEMPLES ===</code>, <code>=== CONSEILS ===</code></li>
          <li><strong>Contenu :</strong> Supporte HTML et LaTeX (MathJax)</li>
          <li><strong>MathJax :</strong> <code>$formule$</code> (inline) et <code>$$formule$$</code> (bloc)</li>
          <li><strong>HTML :</strong> <code>&lt;strong&gt;</code>, <code>&lt;em&gt;</code>, <code>&lt;ul&gt;</code>, <code>&lt;ol&gt;</code>, etc.</li>
          <li><strong>Listes :</strong> Utilisez des puces • ou des numéros pour structurer</li>
          <li><strong>Mise en forme :</strong> Utilisez des titres <code>&lt;h3&gt;</code>, <code>&lt;h4&gt;</code> pour organiser</li>
        </ul>
      </div>
      
      <div class="working-example">
        <h4>🎯 Exemple concret :</h4>
        <div class="example-code">
          <pre><code>Titre: Théorème de Pythagore
Notion: 15
Difficulté: easy
Temps de lecture: 8
Points clés: triangle rectangle,hypoténuse,cathètes,relation métrique

=== CONTENU ===

Le &lt;strong&gt;théorème de Pythagore&lt;/strong&gt; est une relation fondamentale dans les triangles rectangles.

&lt;h3&gt;Énoncé&lt;/h3&gt;
Dans un triangle rectangle, le carré de l'hypoténuse est égal à la somme des carrés des cathètes :

$$a^2 + b^2 = c^2$$

où :
• $a$ et $b$ sont les cathètes
• $c$ est l'hypoténuse

=== EXEMPLES ===

&lt;h4&gt;Exemple 1 : Calcul de l'hypoténuse&lt;/h4&gt;
Triangle avec cathètes de 3 cm et 4 cm :
$$c = \sqrt{3^2 + 4^2} = \sqrt{9 + 16} = \sqrt{25} = 5 \text{ cm}$$

&lt;h4&gt;Exemple 2 : Calcul d'une cathète&lt;/h4&gt;
Triangle avec hypoténuse de 10 cm et une cathète de 6 cm :
$$b = \sqrt{10^2 - 6^2} = \sqrt{100 - 36} = \sqrt{64} = 8 \text{ cm}$$

=== CONSEILS ===

• &lt;strong&gt;Vérification :&lt;/strong&gt; Toujours vérifier que $a^2 + b^2 = c^2$
• &lt;strong&gt;Unités :&lt;/strong&gt; Attention aux unités dans les calculs
• &lt;strong&gt;Application :&lt;/strong&gt; Utile en géométrie, trigonométrie et physique</code></pre>
        </div>
        <p class="example-note">
          <strong>Résultat :</strong> Cette fiche sera automatiquement formatée avec les sections appropriées, 
          les formules mathématiques rendues et les points clés extraits.
        </p>
      </div>
    </div>

    <!-- En-tête avec actions principales -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">
          <span class="icon">📋</span>
          Fiches de synthèse
        </h1>
        <p class="page-description">Créez et gérez les fiches de révision pour vos étudiants</p>
      </div>
      <div class="header-actions">
        <button 
          class="btn btn-primary" 
          @click="openCreateModal"
          :disabled="loading"
        >
          <span class="icon">➕</span>
          Nouvelle fiche
        </button>
      </div>
    </div>

    <!-- Filtres et recherche -->
    <div class="filters-section">
      <div class="filters-row">
        <div class="filter-group">
          <label>Matière :</label>
          <select v-model="filters.matiere" @change="loadSheets">
            <option value="">Toutes les matières</option>
            <option v-for="matiere in matieres" :key="matiere.id" :value="matiere.id">
              {{ matiere.nom }}
            </option>
          </select>
        </div>
        
        <div class="filter-group">
          <label>Recherche :</label>
          <input 
            v-model="filters.search" 
            @input="debouncedSearch"
            placeholder="Titre, contenu..." 
            class="search-input"
          />
        </div>
        
        <div class="filter-group">
          <button class="btn btn-outline" @click="resetFilters">
            Réinitialiser
          </button>
        </div>
      </div>
    </div>

    <!-- Table des fiches -->
    <div class="sheets-table-container">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Chargement des fiches...</p>
      </div>
      
      <div v-else-if="sheets.length === 0" class="empty-state">
        <div class="empty-icon">📝</div>
        <h3>Aucune fiche de synthèse</h3>
        <p>Commencez par créer votre première fiche de révision</p>
        <button class="btn btn-primary" @click="openCreateModal">
          Créer une fiche
        </button>
      </div>
      
      <table v-else class="sheets-table">
        <thead>
          <tr>
            <th>Titre</th>
            <th>Notion</th>
            <th>Matière</th>
            <th>Difficulté</th>
            <th>Temps de lecture</th>
            <th>Statut</th>
            <th>Créé le</th>
            <th class="actions-col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sheet in sheets" :key="sheet.id" class="sheet-row">
            <td class="title-col">
              <strong>{{ sheet.titre }}</strong>
            </td>
            <td>{{ sheet.notion_nom }}</td>
            <td>
              <span class="matiere-badge">{{ sheet.matiere_nom }}</span>
            </td>
            <td>
              <span class="difficulty-badge" :class="sheet.difficulty">
                {{ getDifficultyLabel(sheet.difficulty) }}
              </span>
            </td>
            <td>{{ sheet.reading_time_minutes }} min</td>
            <td>
              <span class="status-badge" :class="{ active: sheet.est_actif }">
                {{ sheet.est_actif ? 'Actif' : 'Inactif' }}
              </span>
            </td>
            <td>{{ formatDate(sheet.date_creation) }}</td>
            <td class="actions-col">
              <div class="action-buttons">
                <button 
                  class="btn-icon btn-preview" 
                  @click="previewSheet(sheet)"
                  title="Prévisualiser"
                >
                  👁️
                </button>
                <button 
                  class="btn-icon btn-edit" 
                  @click="editSheet(sheet)"
                  title="Modifier"
                >
                  ✏️
                </button>
                <button 
                  class="btn-icon btn-duplicate" 
                  @click="duplicateSheet(sheet)"
                  title="Dupliquer"
                >
                  📋
                </button>
                <button 
                  class="btn-icon btn-delete" 
                  @click="deleteSheet(sheet)"
                  title="Supprimer"
                >
                  🗑️
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal de création/édition -->
    <SheetModal 
      v-if="showModal"
      :sheet="currentSheet"
      :is-edit="isEditMode"
      :notions="notions"
      @close="closeModal"
      @save="handleSave"
      @preview="handlePreview"
    />

    <!-- Modal de prévisualisation -->
    <PreviewModal
      v-if="showPreview"
      :sheet="previewData"
      @close="closePreview"
    />
    

  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { debounce } from 'lodash-es'
import SheetModal from '@/components/admin/SheetModal.vue'
import PreviewModal from '@/components/admin/PreviewModal.vue'
import { 
  getSynthesisSheets, 
  createSynthesisSheet, 
  updateSynthesisSheet, 
  deleteSynthesisSheet,
  duplicateSynthesisSheet
} from '@/api/synthesis'
import { getNotions, getMatieres } from '@/api'

// État réactif
const loading = ref(false)
const sheets = ref([])
const matieres = ref([])
const notions = ref([])

// Modals
const showModal = ref(false)
const showPreview = ref(false)
const currentSheet = ref(null)
const isEditMode = ref(false)
const previewData = ref(null)

// Filtres
const filters = reactive({
  matiere: '',
  search: ''
})

// Computed
const debouncedSearch = debounce(() => {
  loadSheets()
}, 300)

// Méthodes
const loadSheets = async () => {
  loading.value = true
  try {
    const params = {}
    if (filters.matiere) params.matiere = filters.matiere
    if (filters.search) params.search = filters.search
    
    const response = await getSynthesisSheets(params)
    sheets.value = response.data.results || response.data
  } catch (error) {
    console.error('Erreur lors du chargement des fiches:', error)
  } finally {
    loading.value = false
  }
}

const loadMatieres = async () => {
  try {
    const response = await getMatieres()
    matieres.value = response || []
  } catch (error) {
    console.error('Erreur lors du chargement des matières:', error)
    matieres.value = []
  }
}

const loadNotions = async () => {
  try {
    const response = await getNotions()
    notions.value = response || []
  } catch (error) {
    console.error('Erreur lors du chargement des notions:', error)
    notions.value = []
  }
}

const openCreateModal = () => {
  currentSheet.value = null
  isEditMode.value = false
  showModal.value = true
}

const editSheet = (sheet) => {
  console.log('🔍 Données de la fiche à éditer:', sheet)
  currentSheet.value = { ...sheet }
  console.log('🔍 currentSheet après copie:', currentSheet.value)
  isEditMode.value = true
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  currentSheet.value = null
}

const handleSave = async (sheetData) => {
  try {
    if (isEditMode.value) {
      await updateSynthesisSheet(currentSheet.value.id, sheetData)
    } else {
      await createSynthesisSheet(sheetData)
    }
    
    closeModal()
    loadSheets()
  } catch (error) {
    console.error('Erreur lors de la sauvegarde:', error)
    throw error
  }
}

const deleteSheet = async (sheet) => {
  if (confirm(`Êtes-vous sûr de vouloir supprimer la fiche "${sheet.titre}" ?`)) {
    try {
      await deleteSynthesisSheet(sheet.id)
      loadSheets()
    } catch (error) {
      console.error('Erreur lors de la suppression:', error)
    }
  }
}

const duplicateSheet = async (sheet) => {
  try {
    await duplicateSynthesisSheet(sheet.id)
    loadSheets()
  } catch (error) {
    console.error('Erreur lors de la duplication:', error)
  }
}

const previewSheet = (sheet) => {
  previewData.value = sheet
  showPreview.value = true
}

const closePreview = () => {
  showPreview.value = false
  previewData.value = null
}

const handlePreview = (data) => {
  previewData.value = data
  showPreview.value = true
}

const resetFilters = () => {
  filters.matiere = ''
  filters.search = ''
  loadSheets()
}

const getDifficultyLabel = (difficulty) => {
  const labels = {
    easy: 'Facile',
    medium: 'Moyen',
    hard: 'Difficile'
  }
  return labels[difficulty] || difficulty
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('fr-FR')
}

// Initialisation
onMounted(async () => {
  await Promise.all([
    loadSheets(),
    loadMatieres(),
    loadNotions()
  ])
})
</script>

<style scoped>
.admin-sheets {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* En-tête */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e5e7eb;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.875rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.page-description {
  color: #6b7280;
  margin: 0.5rem 0 0 0;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

/* Filtres */
.filters-section {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.filters-row {
  display: flex;
  gap: 2rem;
  align-items: end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

.search-input {
  min-width: 300px;
}

/* Table */
.sheets-table-container {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.sheets-table {
  width: 100%;
  border-collapse: collapse;
}

.sheets-table th {
  background: #f9fafb;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
}

.sheets-table td {
  padding: 1rem;
  border-bottom: 1px solid #f3f4f6;
}

.sheet-row:hover {
  background: #f9fafb;
}

.title-col strong {
  color: #1f2937;
}

.matiere-badge {
  background: #dbeafe;
  color: #1e40af;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.difficulty-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.difficulty-badge.easy {
  background: #d1fae5;
  color: #065f46;
}

.difficulty-badge.medium {
  background: #fef3c7;
  color: #92400e;
}

.difficulty-badge.hard {
  background: #fee2e2;
  color: #991b1b;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  background: #f3f4f6;
  color: #6b7280;
}

.status-badge.active {
  background: #d1fae5;
  color: #065f46;
}

.actions-col {
  width: 200px;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn-icon {
  background: none;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  padding: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-icon:hover {
  background: #f3f4f6;
}

.btn-preview:hover { background: #dbeafe; }
.btn-edit:hover { background: #fef3c7; }
.btn-duplicate:hover { background: #e0e7ff; }
.btn-delete:hover { background: #fee2e2; }

/* États */
.loading-state, .empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #f3f4f6;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: #374151;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: #6b7280;
  margin-bottom: 2rem;
}

/* Boutons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  font-size: 0.875rem;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-outline {
  background: white;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-outline:hover {
  background: #f9fafb;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Guide d'utilisation */
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
  margin-bottom: 1rem;
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

.working-example {
  background: #e9ecef;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 1rem;
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
  margin: 0;
  font-style: italic;
}

/* Responsive */
@media (max-width: 1024px) {
  .filters-row {
    flex-direction: column;
    gap: 1rem;
  }
  
  .search-input {
    min-width: auto;
  }
  
  .sheets-table-container {
    overflow-x: auto;
  }
  
  .action-buttons {
    flex-wrap: wrap;
  }
  
  .format-example,
  .example-code {
    font-size: 0.75rem;
  }
}
</style>
