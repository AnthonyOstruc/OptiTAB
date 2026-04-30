<template>
  <div class="format-help">
    <div class="format-header">
      <h3>📋 Format requis</h3>
      <div class="format-buttons">
        <button class="btn-format-toggle" @click="toggleHelp" type="button">
          {{ showHelp ? 'Masquer le format' : 'Afficher le format' }}
        </button>
        <button class="btn-format-copy" @click="copyFormat" type="button" title="Copier le format">
          📋 Copier
        </button>
      </div>
    </div>

    <div v-if="showHelp" class="format-content">
      <div class="format-example">
        <pre><code>{{ formatTemplate }}</code></pre>
      </div>
      <div v-if="showNotes" class="format-notes">
        <p><strong>Notes importantes :</strong></p>
        <slot name="notes">
          <ul>
            <li>Utilisez <code>===</code> pour délimiter chaque élément</li>
            <li><strong>⚠️ IMPORTANT :</strong> Sélectionnez d'abord la notion dans la liste déroulante ci-dessus</li>
            <li>Difficulté : <code>easy</code>, <code>medium</code> ou <code>hard</code> uniquement</li>
            <li>MathJax supporté : <code>$formule$</code> (inline) et <code>$$formule$$</code> (bloc)</li>
            <li>Laissez <code>Images:</code> vide si pas d'image</li>
          </ul>
        </slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  formatTemplate: {
    type: String,
    required: true
  },
  initialShow: {
    type: Boolean,
    default: false
  },
  showNotes: {
    type: Boolean,
    default: true
  }
})

const showHelp = ref(props.initialShow)

function toggleHelp() {
  showHelp.value = !showHelp.value
}

async function copyFormat() {
  try {
    await navigator.clipboard.writeText(props.formatTemplate)
    const originalTitle = document.title
    document.title = '✅ Format copié !'
    setTimeout(() => {
      document.title = originalTitle
    }, 2000)
  } catch (error) {
    console.error('Erreur lors de la copie:', error)
    // Fallback pour les navigateurs plus anciens
    const textarea = document.createElement('textarea')
    textarea.value = props.formatTemplate
    document.body.appendChild(textarea)
    textarea.select()
    document.execCommand('copy')
    document.body.removeChild(textarea)
  }
}
</script>

<style scoped>
/* Les styles sont importés depuis admin-common.css */
</style>

