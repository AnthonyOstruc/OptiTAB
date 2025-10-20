<template>
  <button 
    class="pdf-download-btn" 
    @click="handleDownload"
    :disabled="loading"
    :class="{ 'loading': loading }"
  >
    <span v-if="loading" class="loading-spinner"></span>
    <svg v-else class="pdf-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
      <polyline points="14,2 14,8 20,8"/>
      <line x1="16" y1="13" x2="8" y2="13"/>
      <line x1="16" y1="17" x2="8" y2="17"/>
      <polyline points="10,9 9,9 8,9"/>
    </svg>
    <span class="btn-text">{{ loading ? 'Génération...' : text }}</span>
  </button>
</template>

<script setup>
import { ref } from 'vue'
import { generateExercicePDF, generatePDFFromHTML, generateExercicesListPDF, generateCoursPDF } from '@/utils/pdfGenerator'

const props = defineProps({
  // Type de téléchargement
  type: {
    type: String,
    default: 'single', // 'single', 'list', 'html', 'cours'
    validator: value => ['single', 'list', 'html', 'cours'].includes(value)
  },
  // Données à télécharger
  data: {
    type: [Object, Array],
    required: true
  },
  // Titre du PDF
  title: {
    type: String,
    default: 'Document'
  },
  // Texte du bouton
  text: {
    type: String,
    default: 'Télécharger PDF'
  },
  // Élément HTML à convertir (pour type 'html')
  htmlElement: {
    type: HTMLElement,
    default: null
  },
  // Options pour la génération HTML
  options: {
    type: Object,
    default: () => ({})
  },
  // Utiliser le rendu MathJax si disponible
  useMathJax: {
    type: Boolean,
    default: false
  },
  // Inclure la solution (pour type 'single')
  includeSolution: {
    type: Boolean,
    default: false
  }
})

const loading = ref(false)

async function handleDownload() {
  if (loading.value) return
  
  loading.value = true
  
  try {
    switch (props.type) {
      case 'single':
        await generateExercicePDF(props.data, props.title, props.useMathJax, props.includeSolution)
        break
        
      case 'list':
        await generateExercicesListPDF(props.data, props.title, props.useMathJax, props.includeSolution)
        break
        
      case 'html':
        if (!props.htmlElement) {
          throw new Error('Élément HTML requis pour le type "html"')
        }
        await generatePDFFromHTML(props.htmlElement, `${props.title}.pdf`, props.options)
        break
        
      case 'cours':
        await generateCoursPDF(props.data, props.title, props.useMathJax)
        break
        
      default:
        throw new Error(`Type de téléchargement non supporté: ${props.type}`)
    }
  } catch (error) {
    console.error('Erreur lors du téléchargement du PDF:', error)
    // Vous pouvez ajouter une notification d'erreur ici
    alert('Erreur lors de la génération du PDF. Veuillez réessayer.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.pdf-download-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.pdf-download-btn:hover:not(:disabled) {
  background: #b91c1c;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

.pdf-download-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.pdf-download-btn.loading {
  background: #6b7280;
}

.pdf-icon {
  flex-shrink: 0;
}

.btn-text {
  font-weight: 500;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  flex-shrink: 0;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Variantes de style */
.pdf-download-btn.small {
  padding: 0.5rem 1rem;
  font-size: 0.75rem;
}

.pdf-download-btn.large {
  padding: 1rem 2rem;
  font-size: 1rem;
}

.pdf-download-btn.outline {
  background: transparent;
  color: #dc2626;
  border: 2px solid #dc2626;
}

.pdf-download-btn.outline:hover:not(:disabled) {
  background: #dc2626;
  color: white;
}
</style>
