<template>
  <section class="reel-slide-editor">
    <div class="editor-header">
      <h3>Éditeur de slide</h3>
      <span v-if="slide">Slide #{{ slide.order }}</span>
    </div>

    <p v-if="!slide" class="editor-empty">Sélectionnez une slide pour l'éditer.</p>

    <form v-else class="editor-form" @submit.prevent="handleSave">
      <label>
        Titre
        <input v-model="form.title" type="text" maxlength="255" placeholder="Titre de la slide" />
      </label>
      <div class="size-control">
        <div class="size-control-header">
          <span>Taille titre</span>
          <strong>{{ scaleLabel(form.title_scale) }}</strong>
        </div>
        <div class="size-control-row">
          <input v-model.number="form.title_scale" type="range" min="0.5" max="2" step="0.05" />
          <input v-model.number="form.title_scale" class="scale-number" type="number" min="0.5" max="2" step="0.05" />
          <button type="button" class="btn-reset" @click="form.title_scale = 1">Reset</button>
        </div>
      </div>

      <label>
        Texte écran
        <textarea
          v-model="form.screen_text"
          rows="3"
          maxlength="1200"
          placeholder="Texte principal affiché dans la slide"
        ></textarea>
      </label>
      <div class="size-control">
        <div class="size-control-header">
          <span>Taille texte écran</span>
          <strong>{{ scaleLabel(form.screen_text_scale) }}</strong>
        </div>
        <div class="size-control-row">
          <input v-model.number="form.screen_text_scale" type="range" min="0.5" max="2" step="0.05" />
          <input v-model.number="form.screen_text_scale" class="scale-number" type="number" min="0.5" max="2" step="0.05" />
          <button type="button" class="btn-reset" @click="form.screen_text_scale = 1">Reset</button>
        </div>
      </div>

      <label>
        KaTeX
        <textarea
          v-model="form.katex"
          rows="5"
          placeholder="\\begin{aligned} ... \\end{aligned}"
        ></textarea>
      </label>
      <div class="size-control">
        <div class="size-control-header">
          <span>Taille KaTeX</span>
          <strong>{{ scaleLabel(form.katex_scale) }}</strong>
        </div>
        <div class="size-control-row">
          <input v-model.number="form.katex_scale" type="range" min="0.5" max="2" step="0.05" />
          <input v-model.number="form.katex_scale" class="scale-number" type="number" min="0.5" max="2" step="0.05" />
          <button type="button" class="btn-reset" @click="form.katex_scale = 1">Reset</button>
        </div>
      </div>

      <div class="size-control">
        <div class="size-control-header">
          <span>Vide entre lignes cumulatives</span>
          <strong>{{ cumulativeGapLabel(form.katex_cumulative_gap_em) }}</strong>
        </div>
        <div class="size-control-row">
          <input v-model.number="form.katex_cumulative_gap_em" type="range" min="0" max="1.5" step="0.1" />
          <input v-model.number="form.katex_cumulative_gap_em" class="scale-number" type="number" min="0" max="1.5" step="0.1" />
          <button type="button" class="btn-reset" @click="form.katex_cumulative_gap_em = 0.4">Reset</button>
        </div>
      </div>

      <label class="checkbox-control">
        <input v-model="form.katex_inline_with_previous" type="checkbox" />
        <span>Afficher ce KaTeX sur la même ligne que la slide précédente</span>
      </label>

      <div v-if="form.katex_inline_with_previous" class="size-control">
        <div class="size-control-header">
          <span>Position meme ligne</span>
          <strong>{{ inlineOffsetLabel(form.katex_inline_offset_percent) }}</strong>
        </div>
        <div class="size-control-row">
          <input v-model.number="form.katex_inline_offset_percent" type="range" min="-40" max="40" step="4" />
          <input v-model.number="form.katex_inline_offset_percent" class="scale-number" type="number" min="-40" max="40" step="4" />
          <button type="button" class="btn-reset" @click="form.katex_inline_offset_percent = 0">Reset</button>
        </div>
      </div>

      <label class="checkbox-control">
        <input v-model="form.katex_reset_cumulative" type="checkbox" />
        <span>Repartir sur une nouvelle page de correction à partir de cette slide</span>
      </label>

      <label class="checkbox-control">
        <input v-model="form.katex_drop_previous_line" type="checkbox" />
        <span>Supprimer la dernière ligne précédente</span>
      </label>

      <label class="checkbox-control">
        <input v-model="form.katex_reveal_with_speech" type="checkbox" />
        <span>Animer le KaTeX avec la voix</span>
      </label>

      <p v-if="katexError" class="editor-error">KaTeX invalide: {{ katexError }}</p>

      <div v-if="katexPreviewHtml" class="katex-preview" v-html="katexPreviewHtml"></div>

      <label>
        Script voix
        <textarea
          v-model="form.voice_script"
          rows="3"
          maxlength="2500"
          placeholder="[thoughtful] On commence par identifier la bonne formule..."
        ></textarea>
      </label>
      <p class="voice-help">
        Tags ElevenLabs utiles: [thoughtful], [curious], [excited], [warmly], [whispers], [sighs], [short pause].
      </p>

      <div class="editor-actions">
        <button class="btn-primary" type="submit" :disabled="saving">
          {{ saving ? 'Sauvegarde...' : 'Sauvegarder' }}
        </button>
        <button class="btn-danger" type="button" :disabled="saving" @click="handleDelete">
          Supprimer la slide
        </button>
      </div>
    </form>
  </section>
</template>

<script setup>
import katex from 'katex'
import { computed, reactive, watch } from 'vue'

const props = defineProps({
  slide: {
    type: Object,
    default: null,
  },
  saving: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['save', 'delete'])

const form = reactive({
  title: '',
  screen_text: '',
  katex: '',
  voice_script: '',
  title_scale: 1,
  screen_text_scale: 1,
  katex_scale: 1,
  katex_inline_with_previous: false,
  katex_inline_offset_percent: 0,
  katex_inline_vertical_offset_em: 0,
  katex_cumulative_gap_em: 0.4,
  katex_reset_cumulative: false,
  katex_reveal_with_speech: false,
  katex_drop_previous_line: false,
})

function clampScale(value) {
  return Math.min(2, Math.max(0.5, Number(value) || 1))
}

function scaleLabel(value) {
  return `${Math.round(clampScale(value) * 100)}%`
}

function clampInlineOffset(value) {
  const numeric = Number(value)
  if (!Number.isFinite(numeric)) return 0
  return Math.min(40, Math.max(-40, numeric))
}

function inlineOffsetLabel(value) {
  const offset = Math.round(clampInlineOffset(value))
  if (!offset) return 'milieu'
  return offset > 0 ? `+${offset}%` : `${offset}%`
}

function clampCumulativeGap(value) {
  const numeric = Number(value)
  if (!Number.isFinite(numeric)) return 0.4
  return Math.min(1.5, Math.max(0, Number(numeric.toFixed(2))))
}

function cumulativeGapLabel(value) {
  return `${clampCumulativeGap(value).toFixed(1)}em`
}

watch(
  () => props.slide,
  (slide) => {
    form.title = slide?.title || ''
    form.screen_text = slide?.screen_text || ''
    form.katex = slide?.katex || ''
    form.voice_script = slide?.voice_script || ''
    form.title_scale = clampScale(slide?.title_scale)
    form.screen_text_scale = clampScale(slide?.screen_text_scale)
    form.katex_scale = clampScale(slide?.katex_scale)
    form.katex_inline_with_previous = Boolean(slide?.katex_inline_with_previous)
    form.katex_inline_offset_percent = clampInlineOffset(slide?.katex_inline_offset_percent)
    form.katex_inline_vertical_offset_em = Math.min(1, Math.max(-1, Number(slide?.katex_inline_vertical_offset_em) || 0))
    form.katex_cumulative_gap_em = clampCumulativeGap(slide?.katex_cumulative_gap_em)
    form.katex_reset_cumulative = Boolean(slide?.katex_reset_cumulative)
    form.katex_reveal_with_speech = Boolean(slide?.katex_reveal_with_speech)
    form.katex_drop_previous_line = Boolean(slide?.katex_drop_previous_line)
  },
  { immediate: true, deep: true }
)

const katexError = computed(() => {
  const raw = String(form.katex || '').trim()
  if (!raw) return ''
  try {
    katex.renderToString(raw, { displayMode: true, throwOnError: true })
    return ''
  } catch (error) {
    return String(error?.message || 'Expression invalide')
  }
})

const katexPreviewHtml = computed(() => {
  const raw = String(form.katex || '').trim()
  if (!raw) return ''
  try {
    return katex.renderToString(raw, { displayMode: true, throwOnError: false })
  } catch (_) {
    return ''
  }
})

function handleSave() {
  if (!props.slide?.id) return

  emit('save', {
    id: props.slide.id,
    title: String(form.title || '').trim(),
    screen_text: String(form.screen_text || '').trim(),
    katex: String(form.katex || '').trim(),
    voice_script: String(form.voice_script || '').trim(),
    title_scale: clampScale(form.title_scale),
    screen_text_scale: clampScale(form.screen_text_scale),
    katex_scale: clampScale(form.katex_scale),
    katex_inline_with_previous: Boolean(form.katex_inline_with_previous),
    katex_inline_offset_percent: clampInlineOffset(form.katex_inline_offset_percent),
    katex_inline_vertical_offset_em: Math.min(1, Math.max(-1, Number(form.katex_inline_vertical_offset_em) || 0)),
    katex_cumulative_gap_em: clampCumulativeGap(form.katex_cumulative_gap_em),
    katex_reset_cumulative: Boolean(form.katex_reset_cumulative),
    katex_reveal_with_speech: Boolean(form.katex_reveal_with_speech),
    katex_drop_previous_line: Boolean(form.katex_drop_previous_line),
  })
}

function handleDelete() {
  if (!props.slide?.id) return
  emit('delete', props.slide.id)
}
</script>

<style scoped>
.reel-slide-editor {
  border: 1px solid #dbe4ee;
  border-radius: 12px;
  background: #ffffff;
  padding: 16px;
}

.editor-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.editor-header h3 {
  margin: 0;
  color: #0f172a;
  font-size: 18px;
}

.editor-header span {
  color: #475569;
  font-size: 13px;
  font-weight: 700;
}

.editor-empty {
  margin: 0;
  color: #64748b;
  font-size: 14px;
}

.editor-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 13px;
  font-weight: 700;
  color: #334155;
}

input,
textarea {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 14px;
  color: #0f172a;
  background: #fff;
  font-family: inherit;
}

.size-control {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #f8fafc;
  padding: 10px 12px;
}

.size-control-header,
.size-control-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.size-control-header {
  justify-content: space-between;
  margin-bottom: 8px;
  color: #334155;
  font-size: 13px;
  font-weight: 700;
}

.size-control-header strong {
  color: #1d4ed8;
  font-size: 12px;
}

.size-control-row input[type='range'] {
  flex: 1;
  padding: 0;
}

.scale-number {
  width: 82px;
}

.btn-reset {
  border: 0;
  border-radius: 7px;
  background: #e0ecff;
  color: #1e40af;
  font-size: 12px;
  font-weight: 800;
  padding: 8px 10px;
  cursor: pointer;
}

.btn-reset:hover {
  background: #bfdbfe;
}

.checkbox-control {
  flex-direction: row;
  align-items: center;
  gap: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #f8fafc;
  padding: 10px 12px;
}

.checkbox-control input {
  width: 18px;
  height: 18px;
  padding: 0;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.editor-error {
  margin: -2px 0 0;
  color: #b91c1c;
  font-size: 12px;
  font-weight: 700;
}

.katex-preview {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #f8fafc;
  padding: 12px;
  overflow-x: auto;
}

.katex-preview :deep(.katex-display) {
  margin: 0;
}

.voice-help {
  margin: -6px 0 0;
  color: #64748b;
  font-size: 12px;
  line-height: 1.45;
}

.editor-actions {
  display: flex;
  gap: 10px;
}

.btn-primary,
.btn-danger {
  border: 0;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.btn-primary {
  background: #1d4ed8;
  color: #ffffff;
}

.btn-primary:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

.btn-danger {
  background: #fee2e2;
  color: #991b1b;
}
</style>
