<template>
  <Teleport to="body">
    <Transition name="instructions-dialog-fade">
      <div v-if="open" class="instructions-dialog-backdrop" @mousedown.self="close">
        <div class="instructions-dialog" role="dialog" aria-modal="true" aria-label="Instructions Gemini permanentes">
          <header class="instructions-dialog__header">
            <div>
              <h2>📝 Instructions permanentes pour Gemini</h2>
              <p>
                Ces consignes sont ajoutées automatiquement à <strong>chaque</strong>
                génération d'image. Utile pour imposer un style, éviter un cliché,
                forcer une couleur, etc.
              </p>
            </div>
            <button class="instructions-dialog__close" type="button" @click="close" aria-label="Fermer">✕</button>
          </header>

          <section class="instructions-dialog__body">
            <label class="instructions-dialog__label">
              <span>Mes consignes</span>
              <span class="instructions-dialog__count" :class="{ 'instructions-dialog__count--warn': nearLimit }">
                {{ draft.length }} / {{ maxLength }}
              </span>
            </label>
            <textarea
              class="instructions-dialog__textarea"
              v-model="draft"
              :maxlength="maxLength"
              rows="14"
              :placeholder="placeholder"
              :disabled="loading || saving"
              @keydown.stop
            ></textarea>

            <details class="instructions-dialog__examples">
              <summary>💡 Exemples d'instructions utiles</summary>
              <ul>
                <li>Toujours montrer un ordinateur portable ouvert sur OptiTAB.</li>
                <li>Privilégier les ambiances lumineuses de fin d'après-midi.</li>
                <li>Ne JAMAIS afficher de visage reconnaissable, préférer des silhouettes.</li>
                <li>Le bleu OptiTAB (#29428e) doit toujours être présent comme accent.</li>
                <li>Éviter tout style cartoon ou illustration enfantine.</li>
                <li>Les fonds doivent être épurés type magazine business premium.</li>
              </ul>
            </details>

            <p v-if="feedbackMsg" class="instructions-dialog__feedback" :class="`instructions-dialog__feedback--${feedbackType}`">
              {{ feedbackMsg }}
            </p>
          </section>

          <footer class="instructions-dialog__footer">
            <button class="instructions-dialog__btn instructions-dialog__btn--ghost" type="button" @click="close" :disabled="saving">
              Annuler
            </button>
            <button
              class="instructions-dialog__btn instructions-dialog__btn--primary"
              type="button"
              :disabled="saving || loading || draft === savedValue"
              @click="save"
            >
              {{ saving ? '⏳ Enregistrement...' : '💾 Enregistrer les consignes' }}
            </button>
          </footer>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'
import { getGeminiImageInstructions, saveGeminiImageInstructions } from '@/api/reelStudio'

const props = defineProps({
  open: { type: Boolean, default: false },
})

const emit = defineEmits(['close', 'saved'])

const draft = ref('')
const savedValue = ref('')
const maxLength = ref(6000)
const loading = ref(false)
const saving = ref(false)
const feedbackMsg = ref('')
const feedbackType = ref('info')

const placeholder = 'Une consigne par ligne, par exemple :\n\n- Le laptop doit toujours être un MacBook stylisé.\n- Pas de personnages, juste des objets et des interfaces.\n- Lumière chaude de fenêtre, type ambiance studio.\n- Privilégier les fonds gris perle ou crème.'

watch(() => props.open, async (val) => {
  if (!val) return
  feedbackMsg.value = ''
  loading.value = true
  try {
    const response = await getGeminiImageInstructions()
    const text = String(response?.data?.instructions || '')
    draft.value = text
    savedValue.value = text
    if (response?.data?.max_length) maxLength.value = Number(response.data.max_length)
  } catch (error) {
    feedbackType.value = 'error'
    feedbackMsg.value = "Impossible de charger les consignes. Tu peux quand même en écrire et enregistrer."
  } finally {
    loading.value = false
  }
})

function close() {
  if (saving.value) return
  emit('close')
}

async function save() {
  if (saving.value) return
  saving.value = true
  feedbackMsg.value = ''
  try {
    const response = await saveGeminiImageInstructions(draft.value)
    const text = String(response?.data?.instructions || '')
    savedValue.value = text
    draft.value = text
    feedbackType.value = 'success'
    feedbackMsg.value = '✅ Consignes enregistrées. Elles seront appliquées à toutes les prochaines générations.'
    emit('saved', text)
    setTimeout(() => {
      if (feedbackMsg.value.startsWith('✅')) feedbackMsg.value = ''
    }, 3500)
  } catch (error) {
    feedbackType.value = 'error'
    feedbackMsg.value = `Erreur : ${error?.response?.data?.detail || error?.message || 'enregistrement impossible.'}`
  } finally {
    saving.value = false
  }
}

const nearLimit = ref(false)
watch(draft, (val) => {
  nearLimit.value = val.length > maxLength.value * 0.9
})
</script>

<style scoped>
.instructions-dialog-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 30000;
  padding: 24px;
  backdrop-filter: blur(2px);
}

.instructions-dialog {
  width: min(620px, 100%);
  max-height: 90vh;
  background: #ffffff;
  border-radius: 18px;
  box-shadow: 0 24px 64px rgba(15, 23, 42, 0.32);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.instructions-dialog__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 18px 24px 14px;
  border-bottom: 1px solid #f1f5f9;
}
.instructions-dialog__header h2 {
  margin: 0;
  font-size: 17px;
  color: #29428e;
}
.instructions-dialog__header p {
  margin: 6px 0 0;
  font-size: 13px;
  color: #64748b;
  line-height: 1.4;
}
.instructions-dialog__close {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #94a3b8;
  padding: 4px 8px;
  border-radius: 6px;
}
.instructions-dialog__close:hover:not(:disabled) { background: #f1f5f9; color: #475569; }

.instructions-dialog__body {
  padding: 18px 24px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow-y: auto;
}

.instructions-dialog__label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  font-weight: 700;
  color: #1e293b;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.instructions-dialog__count {
  font-size: 11px;
  font-weight: 600;
  color: #64748b;
  text-transform: none;
  letter-spacing: 0;
}
.instructions-dialog__count--warn { color: #b45309; }

.instructions-dialog__textarea {
  width: 100%;
  resize: vertical;
  min-height: 200px;
  padding: 12px 14px;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  background: #fafbff;
  font-family: 'JetBrains Mono', 'Menlo', 'Consolas', monospace;
  font-size: 13px;
  line-height: 1.55;
  color: #1e293b;
  outline: none;
  transition: border-color 0.12s, background 0.12s;
}
.instructions-dialog__textarea:focus {
  border-color: #29428e;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(41, 66, 142, 0.12);
}
.instructions-dialog__textarea:disabled {
  opacity: 0.6;
}

.instructions-dialog__examples {
  margin-top: 4px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  background: #fafbff;
  padding: 10px 14px;
}
.instructions-dialog__examples summary {
  cursor: pointer;
  font-size: 12px;
  font-weight: 700;
  color: #29428e;
}
.instructions-dialog__examples ul {
  margin: 8px 0 0;
  padding-left: 18px;
  font-size: 12px;
  color: #475569;
  line-height: 1.6;
}
.instructions-dialog__examples li + li { margin-top: 2px; }

.instructions-dialog__feedback {
  margin: 0;
  font-size: 12px;
  font-weight: 600;
  padding: 8px 12px;
  border-radius: 8px;
}
.instructions-dialog__feedback--success {
  color: #15803d;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
}
.instructions-dialog__feedback--error {
  color: #b91c1c;
  background: #fef2f2;
  border: 1px solid #fecaca;
}
.instructions-dialog__feedback--info {
  color: #29428e;
  background: #eef2ff;
  border: 1px solid #c7d2fe;
}

.instructions-dialog__footer {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  padding: 14px 24px 18px;
  border-top: 1px solid #f1f5f9;
  background: #fafbff;
}

.instructions-dialog__btn {
  padding: 9px 18px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  border: none;
  transition: all 0.12s;
}
.instructions-dialog__btn:disabled { opacity: 0.55; cursor: not-allowed; }

.instructions-dialog__btn--ghost {
  background: transparent;
  color: #64748b;
  border: 1px solid #e2e8f0;
}
.instructions-dialog__btn--ghost:hover:not(:disabled) { background: #f1f5f9; color: #1e293b; }

.instructions-dialog__btn--primary {
  background: #29428e;
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(41, 66, 142, 0.28);
}
.instructions-dialog__btn--primary:hover:not(:disabled) {
  background: #1c3070;
  box-shadow: 0 4px 12px rgba(41, 66, 142, 0.36);
}

.instructions-dialog-fade-enter-active,
.instructions-dialog-fade-leave-active { transition: opacity 0.18s; }
.instructions-dialog-fade-enter-from,
.instructions-dialog-fade-leave-to { opacity: 0; }
.instructions-dialog-fade-enter-active .instructions-dialog,
.instructions-dialog-fade-leave-active .instructions-dialog { transition: transform 0.22s; }
.instructions-dialog-fade-enter-from .instructions-dialog,
.instructions-dialog-fade-leave-to .instructions-dialog { transform: translateY(12px) scale(0.98); }
</style>
