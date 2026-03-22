<template>
  <div class="admin-cours-pdf">
    <header class="page-header">
      <h1>Générateur PDF des cours</h1>
      <p>Collez votre cours, prévisualisez le rendu, puis exportez en PDF natif.</p>
    </header>

    <section class="editor-grid">
      <article class="panel panel-editor">
        <div class="field-row">
          <label for="cours-title">Titre (optionnel)</label>
          <input
            id="cours-title"
            v-model.trim="titre"
            type="text"
            placeholder="Titre du cours (sinon le parseur lit Titre: dans le contenu)"
          />
        </div>

        <div class="field-row">
          <label for="cours-difficulty">Difficulté</label>
          <select id="cours-difficulty" v-model="difficulty">
            <option value="easy">easy</option>
            <option value="medium">medium</option>
            <option value="hard">hard</option>
          </select>
        </div>

        <div class="field-row">
          <label for="cours-source">Contenu du cours</label>
          <textarea
            id="cours-source"
            v-model="contenu"
            placeholder="Collez ici votre cours (.txt/.html) format OptiTAB"
          ></textarea>
        </div>

        <div class="field-row">
          <label for="cours-file">Importer un fichier .txt/.html (optionnel)</label>
          <input id="cours-file" type="file" accept=".txt,.html,.htm,.md" @change="onFileChange" />
        </div>

        <div class="actions-row">
          <button class="btn btn-secondary" :disabled="loadingPreview" @click="handlePreview">
            {{ loadingPreview ? 'Prévisualisation...' : 'Prévisualiser' }}
          </button>
          <button class="btn btn-primary" :disabled="loadingPdf" @click="handleDownloadPdf">
            {{ loadingPdf ? 'Génération PDF...' : 'Mettre en PDF' }}
          </button>
        </div>

        <p v-if="errorMessage" class="feedback feedback-error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="feedback feedback-success">{{ successMessage }}</p>
      </article>

      <article class="panel panel-preview">
        <h2>Aperçu</h2>
        <iframe
          v-if="previewHtml"
          :srcdoc="previewHtml"
          class="preview-frame"
          title="Aperçu du cours"
        ></iframe>
        <div v-else class="preview-empty">
          Lancez une prévisualisation pour voir le rendu du cours.
        </div>
      </article>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { downloadCoursPdfDraft, previewCoursPdfDraft } from '@/api/cours'

const titre = ref('')
const difficulty = ref('medium')
const contenu = ref('')
const previewHtml = ref('')
const loadingPreview = ref(false)
const loadingPdf = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

function resetFeedback() {
  errorMessage.value = ''
  successMessage.value = ''
}

function buildPayload() {
  return {
    title: titre.value || '',
    difficulty: difficulty.value,
    content: contenu.value || '',
  }
}

async function onFileChange(event) {
  const file = event?.target?.files?.[0]
  if (!file) return
  try {
    const text = await file.text()
    contenu.value = text
    successMessage.value = `Fichier importé: ${file.name}`
    errorMessage.value = ''
  } catch (error) {
    errorMessage.value = "Impossible de lire le fichier importé."
  }
}

async function handlePreview() {
  resetFeedback()
  if (!contenu.value.trim()) {
    errorMessage.value = "Collez d'abord un contenu de cours."
    return
  }

  loadingPreview.value = true
  try {
    const { data } = await previewCoursPdfDraft(buildPayload())
    previewHtml.value = data?.html || ''
    successMessage.value = 'Prévisualisation générée.'
  } catch (error) {
    const detail = error?.response?.data?.detail
    errorMessage.value = detail || "Erreur lors de la prévisualisation."
  } finally {
    loadingPreview.value = false
  }
}

async function handleDownloadPdf() {
  resetFeedback()
  if (!contenu.value.trim()) {
    errorMessage.value = "Collez d'abord un contenu de cours."
    return
  }

  loadingPdf.value = true
  try {
    const response = await downloadCoursPdfDraft(buildPayload())
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

    successMessage.value = 'PDF généré et téléchargé.'
  } catch (error) {
    const detail = error?.response?.data?.detail
    errorMessage.value = detail || "Erreur lors de la génération du PDF."
  } finally {
    loadingPdf.value = false
  }
}
</script>

<style scoped>
.admin-cours-pdf {
  padding: 16px;
}

.page-header h1 {
  margin: 0 0 6px;
  font-size: 1.45rem;
  color: #111827;
}

.page-header p {
  margin: 0 0 14px;
  color: #4b5563;
}

.editor-grid {
  display: grid;
  grid-template-columns: minmax(420px, 1fr) minmax(420px, 1fr);
  gap: 16px;
}

.panel {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 14px;
  min-height: 620px;
}

.panel-preview h2 {
  margin: 0 0 10px;
  font-size: 1.05rem;
}

.field-row {
  display: flex;
  flex-direction: column;
  margin-bottom: 12px;
}

.field-row label {
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 6px;
  color: #1f2937;
}

.field-row input[type='text'],
.field-row select,
.field-row textarea,
.field-row input[type='file'] {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 10px;
  font-size: 0.92rem;
  background: #fff;
}

.field-row textarea {
  min-height: 360px;
  resize: vertical;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace;
  line-height: 1.42;
}

.actions-row {
  display: flex;
  gap: 10px;
  margin-top: 6px;
}

.btn {
  border: 0;
  border-radius: 8px;
  padding: 10px 14px;
  font-weight: 600;
  cursor: pointer;
  font-size: 0.92rem;
}

.btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.btn-primary {
  background: #2563eb;
  color: #fff;
}

.btn-secondary {
  background: #e5e7eb;
  color: #111827;
}

.feedback {
  margin-top: 10px;
  font-size: 0.9rem;
}

.feedback-error {
  color: #b91c1c;
}

.feedback-success {
  color: #166534;
}

.preview-frame {
  width: 100%;
  height: 560px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: #fff;
}

.preview-empty {
  height: 560px;
  border: 1px dashed #d1d5db;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  background: #f9fafb;
  text-align: center;
  padding: 16px;
}

@media (max-width: 1200px) {
  .editor-grid {
    grid-template-columns: 1fr;
  }
}
</style>
