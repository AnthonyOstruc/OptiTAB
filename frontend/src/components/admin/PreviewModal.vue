<template>
  <div class="preview-overlay" @click="handleOverlayClick">
    <div class="preview-container" @click.stop>
      <!-- Header moderne -->
      <div class="preview-header">
        <div class="header-content">
          <h2 class="preview-title">
            <span class="title-icon">👁️</span>
            Aperçu de la fiche
          </h2>
          <div class="preview-meta">
            <span class="difficulty-badge" :class="sheet?.difficulty">
              {{ getDifficultyLabel(sheet?.difficulty) }}
            </span>
            <span class="reading-time">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12,6 12,12 16,14"></polyline>
              </svg>
              {{ sheet?.reading_time_minutes || 5 }} min
            </span>
          </div>
        </div>
        <button class="close-button" @click="$emit('close')">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <!-- Contenu principal ultra-compact -->
      <div class="preview-body">
        <div class="sheet-preview">
          <!-- En-tête de la fiche -->
          <div class="sheet-header">
            <h1 class="sheet-title">{{ sheet?.titre || 'Titre de la fiche' }}</h1>
            <div class="sheet-context" v-if="sheet?.notion_info">
              <div class="context-badges">
                <span class="context-badge notion">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14,2 14,8 20,8"></polyline>
                  </svg>
                  {{ sheet.notion_info.titre }}
              </span>
                <span v-if="sheet.notion_info.theme" class="context-badge theme">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="3"></circle>
                    <path d="M12 1v6m0 6v6m11-7h-6m-6 0H1"></path>
                  </svg>
                  {{ sheet.notion_info.theme.titre }}
              </span>
                <span v-if="sheet.notion_info.theme?.matiere" class="context-badge matiere">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                  </svg>
                  {{ sheet.notion_info.theme.matiere.titre }}
              </span>
              </div>
            </div>
          </div>

          <!-- Contenu principal -->
          <div class="sheet-content">
            <div v-if="sheet?.summary" class="main-content">
              <div class="content-html" v-html="prepareContent(renderedContent)"></div>
            </div>
            
            <div v-else class="empty-content">
              <div class="empty-icon">📄</div>
              <h3>Aucun contenu à prévisualiser</h3>
              <p>Ajoutez du contenu pour voir l'aperçu</p>
            </div>
          </div>

          <!-- Points clés -->
          <div v-if="hasKeyPoints" class="sheet-section key-points">
            <h3 class="section-title">
              <span class="section-icon">🎯</span>
              Points clés à retenir
            </h3>
            <ul class="key-points-list">
              <li v-for="point in sheet.key_points" :key="point" v-html="prepareContent(point)"></li>
            </ul>
          </div>

          <!-- Formules importantes -->
          <div v-if="hasFormulas" class="sheet-section formulas">
            <h3 class="section-title">
              <span class="section-icon">📐</span>
              Formules importantes
            </h3>
            <div class="formulas-list">
              <div v-for="formula in sheet.formulas" :key="formula" class="formula-item">
                <div class="formula-content" v-html="prepareContent(formula)"></div>
              </div>
            </div>
          </div>

          <!-- Exemples -->
          <div v-if="hasExamples" class="sheet-section examples">
            <h3 class="section-title">
              <span class="section-icon">💡</span>
              Exemples et applications
            </h3>
            <div class="examples-list">
              <div v-for="example in sheet.examples" :key="example" class="example-item">
                <div class="example-content" v-html="prepareContent(example)"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer moderne -->
      <div class="preview-footer">
        <div class="content-stats">
          <span class="stat-chip">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14,2 14,8 20,8"></polyline>
            </svg>
            {{ wordCount }} mots
          </span>
          <span class="stat-chip">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M12 1v6m0 6v6m11-7h-6m-6 0H1"></path>
            </svg>
            {{ countFormulas(sheet?.summary) }} formules
          </span>
          <span class="stat-chip">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12,6 12,12 16,14"></polyline>
            </svg>
            {{ estimatedReadingTime }} min
          </span>
        </div>
        <button class="close-action-btn" @click="$emit('close')">
          <span>Fermer</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, watch, nextTick } from 'vue'

// Props et émissions
const props = defineProps({
  sheet: Object
})

const emit = defineEmits(['close'])

// Computed
const renderedContent = computed(() => {
  if (!props.sheet?.summary) return ''
  
  try {
    return unescapeLatex(props.sheet.summary)
  } catch (error) {
    return '<p class="error">Erreur dans le rendu du contenu</p>'
  }
})

const hasKeyPoints = computed(() => {
  return props.sheet?.key_points && props.sheet.key_points.length > 0
})

const hasFormulas = computed(() => {
  return props.sheet?.formulas && props.sheet.formulas.length > 0
})

const hasExamples = computed(() => {
  return props.sheet?.examples && props.sheet.examples.length > 0
})

const wordCount = computed(() => {
  if (!props.sheet?.summary) return 0
  return props.sheet.summary.split(/\s+/).filter(word => word.length > 0).length
})

const estimatedReadingTime = computed(() => {
  // Estimation: 200 mots par minute
  const wordsPerMinute = 200
  const minutes = Math.ceil(wordCount.value / wordsPerMinute)
  return Math.max(1, minutes)
})

// Méthodes
const getDifficultyLabel = (difficulty) => {
  const labels = {
    easy: 'Facile',
    medium: 'Moyen',
    hard: 'Difficile'
  }
  return labels[difficulty] || difficulty
}

const handleOverlayClick = (e) => {
  if (e.target === e.currentTarget) {
    emit('close')
  }
}

function countFormulas(text) {
  if (!text) return 0
  const patterns = [/\$[^$]+\$/g, /\$\$[^$]+\$\$/g]
  let count = 0
  patterns.forEach(pattern => {
    const matches = text.match(pattern)
    if (matches) count += matches.length
  })
  return count
}

// Traitement LaTeX et Markdown
function unescapeLatex(text) {
  if (!text) return ''
  
  return text
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/\\/g, '\\')
    .trim()
}

function prepareContent(content) {
  if (!content) return ''
  
  return content
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    // Convertir les paragraphes colorés en titres
    .replace(/<p[^>]*style="[^"]*color:blue[^"]*"[^>]*>([^<]+)<\/p>/g, '<h2 class="section-title blue">$1</h2>')
    .replace(/<p[^>]*style="[^"]*color:darkorange[^"]*"[^>]*>([^<]+)<\/p>/g, '<h3 class="subsection-title orange">$1</h3>')
    .replace(/<p[^>]*style="[^"]*color:red[^"]*"[^>]*>([^<]+)<\/p>/g, '<div class="alert-box warning">$1</div>')
    .replace(/<p[^>]*style="[^"]*color:green[^"]*"[^>]*>([^<]+)<\/p>/g, '<div class="alert-box success">$1</div>')
    .replace(/<p[^>]*style="[^"]*color:purple[^"]*"[^>]*>([^<]+)<\/p>/g, '<h4 class="example-title">$1</h4>')
    // Traitement des titres markdown
    .replace(/^###\s+(.+)$/gm, '<h3 class="subsection-title">$1</h3>')
    .replace(/^##\s+(.+)$/gm, '<h2 class="section-title">$1</h2>')
    .replace(/^#\s+(.+)$/gm, '<h1 class="main-title">$1</h1>')
    // Formatage
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>')
    // Sauts de ligne
    .replace(/\n\n/g, '<br/>')
    .replace(/\n/g, '<br/>')
    .trim()
}

// MathJax rendering
function renderMath() {
  nextTick(() => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise()
    } else {
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

// Watcher pour re-rendre MathJax quand le contenu change
watch(() => props.sheet, () => {
  if (props.sheet) {
    setTimeout(renderMath, 100)
  }
}, { deep: true })

onMounted(() => {
  if (props.sheet) {
    setTimeout(renderMath, 100)
  }
})
</script>

<style scoped>
.preview-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
  backdrop-filter: blur(4px);
}

.preview-container {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}

/* Header moderne */
.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 2rem 2rem 1rem 2rem;
  border-bottom: 1px solid #f1f5f9;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.header-content {
  flex: 1;
}

.preview-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.75rem 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.title-icon {
  font-size: 1.25rem;
}

.preview-meta {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.difficulty-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.difficulty-badge.easy {
  background: linear-gradient(135deg, #dcfce7, #bbf7d0);
  color: #166534;
}

.difficulty-badge.medium {
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  color: #92400e;
}

.difficulty-badge.hard {
  background: linear-gradient(135deg, #fee2e2, #fecaca);
  color: #991b1b;
}

.reading-time {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 500;
}

.close-button {
  background: #f8fafc;
  border: none;
  border-radius: 8px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #64748b;
  transition: all 0.2s;
}

.close-button:hover {
  background: #f1f5f9;
  color: #374151;
}

/* Body ultra-compact */
.preview-body {
  flex: 1;
  overflow-y: auto;
  padding: 0;
}

.sheet-preview {
  padding: 1rem 2rem 2rem 2rem;
}

/* En-tête de la fiche */
.sheet-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e2e8f0;
}

.sheet-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0 0 0.75rem 0;
  line-height: 1.2;
}

.sheet-context {
  margin-top: 0.75rem;
}

.context-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.context-badge {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.context-badge.notion {
  background: linear-gradient(135deg, #eff6ff, #dbeafe);
  color: #1e40af;
}

.context-badge.theme {
  background: linear-gradient(135deg, #f0fdf4, #dcfce7);
  color: #166534;
}

.context-badge.matiere {
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  color: #92400e;
}

/* Contenu principal */
.sheet-content {
  margin-bottom: 1.5rem;
}

.main-content {
  font-family: 'Inter', -apple-system, sans-serif;
  line-height: 1.4;
  color: #374151;
  font-size: 0.95rem;
}

.empty-content {
  text-align: center;
  padding: 2rem;
  color: #94a3b8;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-content h3 {
  margin: 0 0 0.5rem 0;
  color: #64748b;
}

.empty-content p {
  margin: 0;
  color: #94a3b8;
}

/* Sections */
.sheet-section {
  margin: 1rem 0;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
  border-left: 4px solid #3b82f6;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.75rem 0;
}

.section-icon {
  font-size: 1.1rem;
}

/* Points clés */
.key-points-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.key-points-list li {
  padding: 0.25rem 0;
  position: relative;
  padding-left: 1.25rem;
  margin: 0.2rem 0;
  line-height: 1.4;
}

.key-points-list li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #10b981;
  font-weight: bold;
  font-size: 0.9rem;
}

/* Formules */
.formulas-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.formula-item {
  background: white;
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.formula-content {
  font-size: 0.95rem;
  line-height: 1.4;
}

/* Exemples */
.examples-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.example-item {
  background: white;
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  line-height: 1.4;
}

.example-content {
  line-height: 1.4;
  font-size: 0.95rem;
}

/* Footer moderne */
.preview-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  border-top: 1px solid #f1f5f9;
  background: #fafbfc;
}

.content-stats {
  display: flex;
  gap: 0.75rem;
}

.stat-chip {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: white;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #64748b;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.close-action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.close-action-btn:hover {
  background: #2563eb;
}

/* Contenu de synthèse ultra-compact */
.main-content :deep(.main-title) {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 3px solid #3b82f6;
}

.main-content :deep(.section-title) {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1e293b;
  margin: 1rem 0 0.3rem 0;
  padding: 0.5rem 0.75rem;
  background: linear-gradient(135deg, #eff6ff, #dbeafe);
  border-left: 4px solid #3b82f6;
  border-radius: 0 8px 8px 0;
}

.main-content :deep(.section-title.blue) {
  background: linear-gradient(135deg, #eff6ff, #dbeafe);
  border-left-color: #3b82f6;
  color: #1e40af;
}

.main-content :deep(.subsection-title) {
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  margin: 0.6rem 0 0.2rem 0;
  padding: 0.25rem 0.5rem;
  background: #f8fafc;
  border-left: 3px solid #10b981;
  border-radius: 0 6px 6px 0;
}

.main-content :deep(.subsection-title.orange) {
  border-left-color: #f59e0b;
  background: #fffbeb;
  color: #d97706;
}

.main-content :deep(.example-title) {
  font-size: 0.9rem;
  font-weight: 600;
  color: #7c3aed;
  margin: 0.4rem 0 0.2rem 0;
  padding: 0.25rem 0.5rem;
  background: #faf5ff;
  border-left: 3px solid #7c3aed;
  border-radius: 0 6px 6px 0;
}

.main-content :deep(.alert-box) {
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  margin: 0.4rem 0;
  font-weight: 500;
  font-size: 0.9rem;
}

.main-content :deep(.alert-box.warning) {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
}

.main-content :deep(.alert-box.success) {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #059669;
}

.main-content :deep(p) {
  margin: 0.2rem 0;
  line-height: 1.5;
}

.main-content :deep(ul),
.main-content :deep(ol) {
  margin: 0.3rem 0 0.3rem 1.2rem;
  padding: 0;
}

.main-content :deep(li) {
  margin: 0.1rem 0;
  line-height: 1.4;
}

.main-content :deep(strong) {
  font-weight: 700;
  color: #1e293b;
}

.main-content :deep(em) {
  color: #64748b;
  font-style: italic;
}

/* MathJax ultra-compact */
.main-content :deep(.MathJax) {
  font-size: 0.95rem !important;
  margin: 0.2rem 0 !important;
}

.main-content :deep(.MathJax_Display),
.main-content :deep(.MathJax_SVG_Display) {
  margin: 0.3rem 0 !important;
  text-align: center !important;
}

/* Responsive */
@media (max-width: 768px) {
  .preview-overlay {
    padding: 1rem;
  }
  
  .preview-container {
    max-height: 95vh;
  }
  
  .preview-header,
  .preview-footer {
    padding: 1rem;
  }
  
  .sheet-preview {
    padding: 1rem;
  }
  
  .preview-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .content-stats {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .context-badges {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
