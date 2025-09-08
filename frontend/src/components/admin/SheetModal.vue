<template>
  <div class="modal-overlay" @click="handleOverlayClick">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <h2>{{ isEdit ? 'Modifier' : 'Créer' }} une fiche de synthèse</h2>
        <button class="close-btn" @click="$emit('close')">×</button>
      </div>

      <div class="modal-body">
        <form @submit.prevent="handleSubmit" class="sheet-form">
          <!-- Informations de base -->
          <div class="form-section">
            <h3>Informations générales</h3>
            
            <div class="form-row">
              <div class="form-group">
                <label for="titre" class="required">Titre de la fiche</label>
                <input
                  id="titre"
                  v-model="form.titre"
                  type="text"
                  placeholder="Ex: Les dérivées - Résumé"
                  required
                  class="form-input"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="notion" class="required">Notion (hérite du contexte via Thème)</label>
                <select
                  id="notion"
                  v-model="form.notion"
                  required
                  class="form-select"
                  @change="updateNotionInfo"
                >
                  <option value="">Choisir une notion</option>
                  <option 
                    v-for="notion in props.notions" 
                    :key="notion.id" 
                    :value="notion.id"
                  >
                    {{ formatNotionOption(notion) }}
                  </option>
                </select>
              </div>
              
              <div class="form-group">
                <label for="difficulty">Difficulté</label>
                <select
                  id="difficulty"
                  v-model="form.difficulty"
                  class="form-select"
                >
                  <option value="easy">Facile</option>
                  <option value="medium">Moyen</option>
                  <option value="hard">Difficile</option>
                </select>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="ordre">Ordre d'affichage</label>
                <input
                  id="ordre"
                  v-model.number="form.ordre"
                  type="number"
                  min="0"
                  class="form-input"
                />
              </div>
              
              <div class="form-group">
                <label for="reading_time">Temps de lecture (min)</label>
                <input
                  id="reading_time"
                  v-model.number="form.reading_time_minutes"
                  type="number"
                  min="1"
                  max="60"
                  class="form-input"
                />
              </div>
            </div>
          </div>

          <!-- Contenu principal -->
          <div class="form-section">
            <h3>Contenu de la fiche</h3>
            
            <div class="tabs-container">
              <div class="tabs-header">
                <button 
                  type="button"
                  class="tab-btn"
                  :class="{ active: activeTab === 'editor' }"
                  @click="activeTab = 'editor'"
                >
                  ✏️ Éditeur
                </button>
                <button 
                  type="button"
                  class="tab-btn"
                  :class="{ active: activeTab === 'preview' }"
                  @click="activeTab = 'preview'"
                >
                  👁️ Aperçu
                </button>
              </div>

              <div class="tab-content">
                <div v-if="activeTab === 'editor'" class="editor-tab">
                  <div class="form-group">
                    <label for="summary">Contenu principal (Markdown + LaTeX)</label>
                                      <div class="editor-help">
                    <div class="help-header">
                      <h4 class="help-title">
                        <span class="help-icon">📝</span>
                        Guide de création de fiches de synthèse
                      </h4>
                      <p class="help-subtitle">Créez des fiches claires et structurées pour optimiser l'apprentissage</p>
                    </div>
                    
                    <div class="help-content">
                      <!-- Structure recommandée -->
                      <div class="help-section">
                        <div class="section-header">
                          <h5 class="section-title">
                            <span class="section-icon">🎯</span>
                            Structure recommandée
                          </h5>
                        </div>
                        <div class="structure-example">
                          <div class="code-header">
                            <span class="code-label">Modèle de fiche</span>
                          </div>
                          <pre class="code-block"><code># Titre principal de la notion

## Définition
Définition claire et précise du concept

## Propriétés importantes
• Propriété 1 : description
• Propriété 2 : description
→ Propriété 3 : description

## Formules clés
$$f(x) = ax^2 + bx + c$$
$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

## Exemples d'application
Exemple: Calcul de la dérivée de $f(x) = x^2 + 3x + 1$
Solution: $f'(x) = 2x + 3$

## Points à retenir
⚠️ Attention aux erreurs courantes
💡 Astuce pour mémoriser</code></pre>
                        </div>
                      </div>
                      
                      <!-- Outils de formatage -->
                      <div class="help-section">
                        <div class="section-header">
                          <h5 class="section-title">
                            <span class="section-icon">🔧</span>
                            Outils de formatage
                          </h5>
                        </div>
                        <div class="formatting-tools">
                          <div class="tool-category">
                            <h6 class="category-title">Titres</h6>
                            <div class="tool-grid">
                              <div class="tool-item">
                                <code class="tool-code"># Titre principal</code>
                                <span class="tool-desc">Titre de niveau 1</span>
                              </div>
                              <div class="tool-item">
                                <code class="tool-code">## Sous-titre</code>
                                <span class="tool-desc">Titre de niveau 2</span>
                              </div>
                              <div class="tool-item">
                                <code class="tool-code">### Section</code>
                                <span class="tool-desc">Titre de niveau 3</span>
                              </div>
                            </div>
                          </div>
                          
                          <div class="tool-category">
                            <h6 class="category-title">Texte</h6>
                            <div class="tool-grid">
                              <div class="tool-item">
                                <code class="tool-code">**gras**</code>
                                <span class="tool-desc">Texte en gras</span>
                              </div>
                              <div class="tool-item">
                                <code class="tool-code">*italique*</code>
                                <span class="tool-desc">Texte en italique</span>
                              </div>
                            </div>
                          </div>
                          
                          <div class="tool-category">
                            <h6 class="category-title">Listes</h6>
                            <div class="tool-grid">
                              <div class="tool-item">
                                <code class="tool-code">• Point important</code>
                                <span class="tool-desc">Liste à puces</span>
                              </div>
                              <div class="tool-item">
                                <code class="tool-code">→ Information clé</code>
                                <span class="tool-desc">Liste avec flèche</span>
                              </div>
                            </div>
                          </div>
                          
                          <div class="tool-category">
                            <h6 class="category-title">Mise en forme</h6>
                            <div class="tool-grid">
                              <div class="tool-item">
                                <code class="tool-code">Définition: texte</code>
                                <span class="tool-desc">Définition</span>
                              </div>
                              <div class="tool-item">
                                <code class="tool-code">Théorème: énoncé</code>
                                <span class="tool-desc">Théorème</span>
                              </div>
                              <div class="tool-item">
                                <code class="tool-code">Propriété: description</code>
                                <span class="tool-desc">Propriété</span>
                              </div>
                              <div class="tool-item">
                                <code class="tool-code">Exemple: cas concret</code>
                                <span class="tool-desc">Exemple</span>
                              </div>
                            </div>
                          </div>
                          
                          <div class="tool-category">
                            <h6 class="category-title">Alertes</h6>
                            <div class="tool-grid">
                              <div class="tool-item">
                                <code class="tool-code">⚠️ Attention</code>
                                <span class="tool-desc">Avertissement</span>
                              </div>
                              <div class="tool-item">
                                <code class="tool-code">💡 Conseil</code>
                                <span class="tool-desc">Conseil</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <!-- Formules mathématiques -->
                      <div class="help-section">
                        <div class="section-header">
                          <h5 class="section-title">
                            <span class="section-icon">📐</span>
                            Formules mathématiques (LaTeX)
                          </h5>
                        </div>
                        <div class="math-examples">
                          <div class="math-category">
                            <h6 class="category-title">Formules inline</h6>
                            <div class="math-grid">
                              <div class="math-item">
                                <code class="math-code">$x^2 + y^2 = r^2$</code>
                                <span class="math-desc">Équation du cercle</span>
                              </div>
                              <div class="math-item">
                                <code class="math-code">$\frac{a}{b}$</code>
                                <span class="math-desc">Fraction</span>
                              </div>
                              <div class="math-item">
                                <code class="math-code">$\sqrt{x}$</code>
                                <span class="math-desc">Racine carrée</span>
                              </div>
                            </div>
                          </div>
                          
                          <div class="math-category">
                            <h6 class="category-title">Formules en bloc</h6>
                            <div class="math-grid">
                              <div class="math-item">
                                <code class="math-code">$$\int_{a}^{b} f(x) dx$$</code>
                                <span class="math-desc">Intégrale</span>
                              </div>
                              <div class="math-item">
                                <code class="math-code">$$\lim_{x \to 0} \frac{\sin(x)}{x} = 1$$</code>
                                <span class="math-desc">Limite</span>
                              </div>
                            </div>
                          </div>
                          
                          <div class="math-category">
                            <h6 class="category-title">Symboles courants</h6>
                            <div class="math-grid">
                              <div class="math-item">
                                <code class="math-code">$\alpha, \beta, \gamma$</code>
                                <span class="math-desc">Lettres grecques</span>
                              </div>
                              <div class="math-item">
                                <code class="math-code">$\sum_{i=1}^{n} x_i$</code>
                                <span class="math-desc">Somme</span>
                              </div>
                              <div class="math-item">
                                <code class="math-code">$\prod_{i=1}^{n} x_i$</code>
                                <span class="math-desc">Produit</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <!-- Conseils -->
                      <div class="help-section">
                        <div class="section-header">
                          <h5 class="section-title">
                            <span class="section-icon">💡</span>
                            Conseils pour une bonne synthèse
                          </h5>
                        </div>
                        <div class="tips-container">
                          <div class="tips-grid">
                            <div class="tip-item">
                              <div class="tip-icon">🎯</div>
                              <div class="tip-content">
                                <h6 class="tip-title">Clarté</h6>
                                <p class="tip-desc">Utilisez des phrases courtes et directes</p>
                              </div>
                            </div>
                            <div class="tip-item">
                              <div class="tip-icon">📋</div>
                              <div class="tip-content">
                                <h6 class="tip-title">Structure</h6>
                                <p class="tip-desc">Organisez l'information de manière logique</p>
                              </div>
                            </div>
                            <div class="tip-item">
                              <div class="tip-icon">🔍</div>
                              <div class="tip-content">
                                <h6 class="tip-title">Exemples</h6>
                                <p class="tip-desc">Donnez toujours des exemples concrets</p>
                              </div>
                            </div>
                            <div class="tip-item">
                              <div class="tip-icon">📐</div>
                              <div class="tip-content">
                                <h6 class="tip-title">Formules</h6>
                                <p class="tip-desc">Expliquez le sens des formules, pas juste leur écriture</p>
                              </div>
                            </div>
                            <div class="tip-item">
                              <div class="tip-icon">🔗</div>
                              <div class="tip-content">
                                <h6 class="tip-title">Connexions</h6>
                                <p class="tip-desc">Montrez les liens avec d'autres notions</p>
                              </div>
                            </div>
                            <div class="tip-item">
                              <div class="tip-icon">⚡</div>
                              <div class="tip-content">
                                <h6 class="tip-title">Méthodes</h6>
                                <p class="tip-desc">Incluez des étapes de résolution</p>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                    <textarea
                      id="summary"
                      ref="summaryTextarea"
                      v-model="form.summary"
                      rows="15"
                      placeholder="Rédigez le contenu de votre fiche en Markdown..."
                      class="form-textarea markdown-editor"
                      @input="updatePreview"
                    ></textarea>
                  </div>
                </div>

                <div v-if="activeTab === 'preview'" class="preview-tab">
                  <div class="preview-container" v-html="prepareContentForMathJax(renderedMarkdown)" @vue:mounted="renderMathJax"></div>
                </div>
              </div>
            </div>
          </div>
        </form>
      </div>

      <div class="modal-footer">
        <button type="button" class="btn btn-outline" @click="$emit('close')">
          Annuler
        </button>
        <button type="button" class="btn btn-secondary" @click="handlePreview">
          👁️ Aperçu complet
        </button>
        <button 
          type="button" 
          class="btn btn-primary" 
          @click="handleSubmit"
          :disabled="!form.titre || !form.notion || saving"
        >
          {{ saving ? 'Sauvegarde...' : (isEdit ? 'Mettre à jour' : 'Créer') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, nextTick } from 'vue'

// Props et émissions
const props = defineProps({
  sheet: Object,
  isEdit: Boolean,
  notions: Array
})

const emit = defineEmits(['close', 'save', 'preview'])

// État réactif
const saving = ref(false)
const activeTab = ref('editor')
const summaryTextarea = ref(null)

// Formulaire
const form = reactive({
  titre: '',
  notion: '',
  summary: '',
  difficulty: 'medium',
  ordre: 0,
  reading_time_minutes: 5
})

// Helper d'affichage (même logique que AdminChapitres)
const formatNotionOption = (n) => {
  if (!n) return ''
  const matiere = n.matiere_nom || (n.contexte_detail && n.contexte_detail.matiere_nom) || ''
  const pays = n.contexte_detail && n.contexte_detail.pays ? n.contexte_detail.pays.nom : ''
  const niveau = n.contexte_detail && n.contexte_detail.niveau ? n.contexte_detail.niveau.nom : ''
  const theme = n.theme_nom || ''
  const parts = [n.titre || n.nom, theme, matiere, [pays, niveau].filter(Boolean).join(' - ')].filter(Boolean)
  return parts.join(' — ')
}

const renderedContent = computed(() => {
  if (!form.summary) return '<p class="empty-preview">Écrivez du contenu pour voir l\'aperçu...</p>'
  
  try {
    return unescapeLatex(form.summary)
  } catch (error) {
    return '<p class="error-preview">Erreur dans le contenu</p>'
  }
})

// Traitement LaTeX et Markdown
function unescapeLatex(text) {
  if (!text) return ''
  
  return text
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/\\/g, '\\')
    // Traitement des titres markdown AVANT les sauts de ligne
    .replace(/^###\s+(.+)$/gm, '<h3 class="markdown-h3">$1</h3>')
    .replace(/^##\s+(.+)$/gm, '<h2 class="markdown-h2">$1</h2>')
    .replace(/^#\s+(.+)$/gm, '<h1 class="markdown-h1">$1</h1>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>')
    // Traitement des paragraphes HTML avec styles pour réduire l'espacement
    .replace(/<p[^>]*style="[^"]*color:blue[^"]*"[^>]*>([^<]+)<\/p>/g, '<h2 class="markdown-h2 blue-title">$1</h2>')
    .replace(/<p[^>]*style="[^"]*color:darkorange[^"]*"[^>]*>([^<]+)<\/p>/g, '<h3 class="markdown-h3 orange-title">$1</h3>')
    .replace(/<p[^>]*style="[^"]*color:red[^"]*"[^"]*"[^>]*>([^<]+)<\/p>/g, '<h3 class="markdown-h3 red-title">$1</h3>')
    .replace(/<p[^>]*style="[^"]*color:green[^"]*"[^"]*"[^>]*>([^<]+)<\/p>/g, '<h3 class="markdown-h3 green-title">$1</h3>')
    .replace(/<p[^>]*style="[^"]*color:purple[^"]*"[^"]*"[^>]*>([^<]+)<\/p>/g, '<h3 class="markdown-h3 purple-title">$1</h3>')
    // Traitement des sauts de ligne APRÈS les titres avec espacement réduit
    .replace(/\n\n/g, '<br class="double-break"/>') // Double saut de ligne → br spécial
    .replace(/\n/g, '<br class="single-break"/>') // Saut de ligne simple → br spécial
    // Conserver les espaces multiples mais pas tous les espaces
    .replace(/  /g, '&nbsp;&nbsp;')
}

// MathJax rendering (même logique que ExerciceQCM)
function renderMath() {
  nextTick(() => {
    // Attendre que MathJax soit disponible
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise()
    } else {
      // Si MathJax n'est pas encore chargé, attendre un peu
      const maxRetries = 10
      let tries = 0
      const tryRender = () => {
        if (window.MathJax && window.MathJax.typesetPromise) {
          window.MathJax.typesetPromise()
        } else if (tries++ < maxRetries) {
          setTimeout(tryRender, 150)
        }
      }
      setTimeout(tryRender, 100)
    }
  })
}

function prepareContentForMathJax(content) {
  if (!content) return ''
  
  // Utiliser la même logique que ExerciceQCM
  return unescapeLatex(content)
}

// Méthodes
const initializeForm = () => {
  console.log('🔍 initializeForm appelé avec props.sheet:', props.sheet)
  if (props.sheet) {
    console.log('🔍 Données de la fiche:', {
      titre: props.sheet.titre,
      notion: props.sheet.notion,
      summary: props.sheet.summary,
      difficulty: props.sheet.difficulty,
      ordre: props.sheet.ordre,
      reading_time_minutes: props.sheet.reading_time_minutes
    })
    
    Object.assign(form, {
      titre: props.sheet.titre || '',
      notion: props.sheet.notion || '',
      summary: props.sheet.summary || '',
      difficulty: props.sheet.difficulty || 'medium',
      ordre: props.sheet.ordre || 0,
      reading_time_minutes: props.sheet.reading_time_minutes || 5
    })
    
    console.log('🔍 Form après initialisation:', form)
  }
}

const handleSubmit = async () => {
  if (saving.value) return
  
  saving.value = true
  try {
    const sheetData = {
      ...form,
      key_points: [], // Supprimer les points clés
      formulas: [], // Supprimer les formules
      examples: [] // Supprimer les exemples
    }
    
    await emit('save', sheetData)
  } catch (error) {
    console.error('Erreur lors de la sauvegarde:', error)
  } finally {
    saving.value = false
  }
}

const handlePreview = () => {
  const previewData = {
    titre: form.titre,
    summary: form.summary,
    key_points: [], // Supprimer les points clés
    formulas: [], // Supprimer les formules
    examples: [], // Supprimer les exemples
    difficulty: form.difficulty,
    reading_time_minutes: form.reading_time_minutes
  }
  
  emit('preview', previewData)
}

const handleOverlayClick = (e) => {
  if (e.target === e.currentTarget) {
    emit('close')
  }
}

const insertTemplate = () => {
  const template = `# [Titre de la notion]

## Définition
[Définition claire et précise du concept à synthétiser]

## Propriétés importantes
• [Propriété 1] : [description]
• [Propriété 2] : [description]
→ [Propriété 3] : [description]

## Formules clés
$$[formule principale]$$
$$[formule secondaire]$$

## Méthodes de résolution
1. [Étape 1] : [description]
2. [Étape 2] : [description]
3. [Étape 3] : [description]

## Exemples d'application
**Exemple 1:** [Description du problème]
Solution: [Résolution détaillée]

**Exemple 2:** [Description du problème]
Solution: [Résolution détaillée]

## Points à retenir
⚠️ [Attention aux erreurs courantes]
💡 [Astuce pour mémoriser]

## Applications pratiques
• [Application 1] : [description]
• [Application 2] : [description]

## Liens avec d'autres notions
Cette notion est liée à [autre notion] car [explication du lien]`
  
  form.summary = template
  
  // Focus sur le textarea et positionner le curseur au début
  nextTick(() => {
    if (summaryTextarea.value) {
      summaryTextarea.value.focus()
      summaryTextarea.value.setSelectionRange(0, 0)
    }
  })
}

const insertMarkdown = (before, after) => {
  const textarea = summaryTextarea.value
  if (!textarea) return
  
  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const selectedText = form.summary.substring(start, end)
  
  const newText = form.summary.substring(0, start) + 
                  before + selectedText + after + 
                  form.summary.substring(end)
  
  form.summary = newText
  
  // Repositionner le curseur
  nextTick(() => {
    const newCursorPos = start + before.length + selectedText.length + after.length
    textarea.focus()
    textarea.setSelectionRange(newCursorPos, newCursorPos)
  })
}

const updateNotionInfo = () => {
  // Logique pour mettre à jour des infos basées sur la notion sélectionnée
}

const updatePreview = () => {
  // Mise à jour automatique de l'aperçu
  // Si on est sur l'onglet preview, re-rendre MathJax
  if (activeTab.value === 'preview') {
    setTimeout(renderMath, 100)
  }
}

// Watchers et lifecycle
watch(() => props.sheet, initializeForm, { immediate: true })

onMounted(() => {
  initializeForm()
})

// Watcher pour re-rendre MathJax quand on change d'onglet
watch(activeTab, (newTab) => {
  if (newTab === 'preview') {
    // Attendre que le DOM soit mis à jour
    setTimeout(renderMath, 100)
  }
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
}

.modal-container {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 1000px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  margin: 0;
  color: #1f2937;
  font-size: 1.5rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0.5rem;
  border-radius: 4px;
}

.close-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}

.sheet-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-section {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
}

.form-section h3 {
  margin: 0 0 1rem 0;
  color: #374151;
  font-size: 1.125rem;
  font-weight: 600;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-row:last-child {
  margin-bottom: 0;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #374151;
  font-size: 0.875rem;
}

.form-group label.required::after {
  content: ' *';
  color: #dc2626;
}

.form-input, .form-select, .form-textarea {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-input:focus, .form-select:focus, .form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-textarea {
  resize: vertical;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

.markdown-editor {
  min-height: 300px;
}

/* Onglets */
.tabs-container {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  overflow: hidden;
}

.tabs-header {
  display: flex;
  background: #f3f4f6;
  border-bottom: 1px solid #d1d5db;
}

.tab-btn {
  flex: 1;
  padding: 0.75rem 1rem;
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 500;
  color: #6b7280;
  transition: all 0.2s;
}

.tab-btn.active {
  background: white;
  color: #3b82f6;
  border-bottom: 2px solid #3b82f6;
}

.tab-content {
  background: white;
}

.editor-tab, .preview-tab {
  padding: 1rem;
}

.editor-help {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 1.5rem;
  font-size: 0.875rem;
  max-height: 500px;
  overflow-y: auto;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.help-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #e2e8f0;
}

.help-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin: 0 0 0.75rem 0;
  color: #1e293b;
  font-size: 1.5rem;
  font-weight: 700;
}

.help-icon {
  font-size: 1.25rem;
}

.help-subtitle {
  margin: 0;
  color: #64748b;
  font-size: 1rem;
  font-weight: 500;
}

.help-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.help-section {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: all 0.2s;
}

.help-section:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.section-header {
  margin-bottom: 1rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 0 0.5rem 0;
  color: #1e293b;
  font-size: 1.125rem;
  font-weight: 600;
}

.section-icon {
  font-size: 1.1rem;
}

/* Structure example */
.structure-example {
  background: #1e293b;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.code-header {
  background: #334155;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #475569;
}

.code-label {
  color: #e2e8f0;
  font-size: 0.875rem;
  font-weight: 600;
}

.code-block {
  margin: 0;
  padding: 1.5rem;
  color: #e2e8f0;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.875rem;
  line-height: 1.6;
  overflow-x: auto;
}

.code-block code {
  background: none;
  padding: 0;
  color: inherit;
  border: none;
  box-shadow: none;
}

/* Formatting tools */
.formatting-tools {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.tool-category {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border: 1px solid #3b82f6;
  border-radius: 10px;
  padding: 1.25rem;
}

.category-title {
  margin: 0 0 1rem 0;
  color: #1e40af;
  font-size: 1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.tool-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 0.75rem;
}

.tool-item {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  transition: all 0.2s;
}

.tool-item:hover {
  border-color: #3b82f6;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1);
}

.tool-code {
  background: #f8fafc;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.875rem;
  color: #1e293b;
  border: 1px solid #e2e8f0;
  font-weight: 600;
}

.tool-desc {
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 500;
}

/* Math examples */
.math-examples {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.math-category {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border: 1px solid #f59e0b;
  border-radius: 10px;
  padding: 1.25rem;
}

.math-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 0.75rem;
}

.math-item {
  background: white;
  border: 1px solid #fbbf24;
  border-radius: 8px;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  transition: all 0.2s;
}

.math-item:hover {
  border-color: #f59e0b;
  box-shadow: 0 2px 4px rgba(245, 158, 11, 0.1);
}

.math-code {
  background: #fef3c7;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.875rem;
  color: #92400e;
  border: 1px solid #fbbf24;
  font-weight: 600;
}

.math-desc {
  color: #92400e;
  font-size: 0.875rem;
  font-weight: 500;
}

/* Tips */
.tips-container {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border: 1px solid #10b981;
  border-radius: 10px;
  padding: 1.25rem;
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.tip-item {
  background: white;
  border: 1px solid #bbf7d0;
  border-radius: 10px;
  padding: 1rem;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  transition: all 0.2s;
}

.tip-item:hover {
  border-color: #10b981;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.1);
  transform: translateY(-1px);
}

.tip-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.tip-content {
  flex: 1;
}

.tip-title {
  margin: 0 0 0.25rem 0;
  color: #166534;
  font-size: 0.875rem;
  font-weight: 600;
}

.tip-desc {
  margin: 0;
  color: #059669;
  font-size: 0.8rem;
  line-height: 1.4;
}

.editor-help code {
  background: #e0f2fe;
  padding: 0.125rem 0.25rem;
  border-radius: 3px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.75rem;
  color: #0c4a6e;
  border: 1px solid #bae6fd;
}

.editor-toolbar {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
}

.editor-toolbar {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  align-items: center;
}

.editor-toolbar button {
  padding: 0.25rem 0.5rem;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 3px;
  cursor: pointer;
  font-size: 0.75rem;
  transition: all 0.2s;
}

.editor-toolbar button:hover {
  background: #f3f4f6;
}

.template-btn {
  background: #3b82f6 !important;
  color: white !important;
  border-color: #2563eb !important;
  font-weight: 600;
  padding: 0.5rem 0.75rem !important;
}

.template-btn:hover {
  background: #2563eb !important;
}

.toolbar-divider {
  width: 1px;
  height: 20px;
  background: #d1d5db;
  margin: 0 0.25rem;
}

.preview-container {
  min-height: 300px;
  max-height: 400px;
  overflow-y: auto;
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  background: white;
}

.empty-preview {
  color: #9ca3af;
  font-style: italic;
  text-align: center;
  padding: 2rem;
}

.error-preview {
  color: #dc2626;
  text-align: center;
  padding: 2rem;
}

/* Styles pour les titres markdown - COMPACT */
.preview-container :deep(.markdown-h1) {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
  padding: 0;
  border-bottom: 2px solid #e5e7eb;
}

.preview-container :deep(.markdown-h2) {
  font-size: 1.5rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 0.4rem 0;
  padding: 0;
  border-bottom: 1px solid #f3f4f6;
}

.preview-container :deep(.markdown-h3) {
  font-size: 1.25rem;
  font-weight: 600;
  color: #4b5563;
  margin: 0 0 0.3rem 0;
  padding: 0;
}

/* Styles pour les titres colorés convertis depuis HTML */
.preview-container :deep(.blue-title) {
  color: #2563eb !important;
  font-size: 1.4em !important;
}

.preview-container :deep(.orange-title) {
  color: #ea580c !important;
}

.preview-container :deep(.red-title) {
  color: #dc2626 !important;
}

.preview-container :deep(.green-title) {
  color: #16a34a !important;
}

.preview-container :deep(.purple-title) {
  color: #9333ea !important;
  font-size: 1.3em !important;
}

/* Contrôle précis des sauts de ligne - COMPACT */
.preview-container :deep(.single-break) {
  line-height: 0.1;
  display: block;
  margin: 0;
  padding: 0;
}

.preview-container :deep(.double-break) {
  line-height: 0.2;
  display: block;
  margin: 0;
  padding: 0;
}

/* MathJax Styles pour la prévisualisation */
.preview-container :deep(.MathJax) {
  font-size: 1.1em;
  margin: 0.5rem 0;
}

.preview-container :deep(.MathJax_Display) {
  margin: 1rem 0;
  text-align: center;
}

.preview-container :deep(.MathJax_SVG_Display) {
  margin: 1rem 0;
  text-align: center;
}

.preview-container :deep(.MathJax_SVG) {
  font-size: 1.1em;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem 2rem;
  border-top: 1px solid #e5e7eb;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  font-size: 0.875rem;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-secondary {
  background: #6b7280;
  color: white;
}

.btn-secondary:hover {
  background: #4b5563;
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

/* Responsive */
@media (max-width: 768px) {
  .modal-overlay {
    padding: 1rem;
  }
  
  .modal-container {
    max-height: 95vh;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .modal-header, .modal-body, .modal-footer {
    padding: 1rem;
  }
}
</style>
