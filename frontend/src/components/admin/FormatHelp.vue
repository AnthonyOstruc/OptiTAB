<template>
  <div class="format-help" ref="rootRef">
    <div class="format-header">
      <h3>📋 Format requis</h3>
      <div class="format-buttons">
        <div class="format-btn-group">
          <button class="btn-format-toggle" @click="openPicker('show')" type="button">
            {{ showHelp ? 'Masquer le format' : 'Afficher le format' }}
          </button>
          <button class="btn-format-copy" @click="openPicker('copy')" type="button" title="Copier le format">
            📋 Copier
          </button>
        </div>

        <!-- Picker dropdown -->
        <Transition name="picker-fade">
          <div v-if="pickerMode" class="format-picker" role="dialog" aria-label="Choisir un format">
            <div class="format-picker__header">
              <span>{{ pickerMode === 'copy' ? 'Copier quel format ?' : 'Afficher quel format ?' }}</span>
              <button class="format-picker__close" @click="closePicker" type="button" aria-label="Fermer">✕</button>
            </div>
            <ul class="format-picker__list">
              <li
                v-for="fmt in activeFormats"
                :key="fmt.id"
                class="format-picker__item"
                :class="{ 'format-picker__item--active': selectedFormatId === fmt.id }"
                @click="selectFormat(fmt)"
              >
                <span class="format-picker__icon">{{ fmt.icon }}</span>
                <div class="format-picker__info">
                  <span class="format-picker__label">{{ fmt.label }}</span>
                  <span class="format-picker__desc">{{ fmt.description }}</span>
                </div>
                <span v-if="pickerMode === 'copy'" class="format-picker__action">Copier</span>
                <span v-else class="format-picker__action">Voir</span>
              </li>
            </ul>
          </div>
        </Transition>
      </div>
    </div>

    <div v-if="showHelp && currentTemplate" class="format-content">
      <div class="format-content__label">
        <span>{{ currentFormatLabel }}</span>
      </div>
      <div class="format-example">
        <pre><code>{{ currentTemplate }}</code></pre>
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

    <!-- Toast copié -->
    <Transition name="toast-fade">
      <div v-if="toastVisible" class="format-toast">✅ Format « {{ toastLabel }} » copié !</div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  formatTemplate: {
    type: String,
    default: ''
  },
  formats: {
    type: Array,
    default: () => []
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

const rootRef = ref(null)
const showHelp = ref(props.initialShow)
const pickerMode = ref(null) // 'show' | 'copy' | null
const selectedFormatId = ref(null)
const toastVisible = ref(false)
const toastLabel = ref('')

const activeFormats = computed(() => {
  if (props.formats && props.formats.length) return props.formats
  if (props.formatTemplate) return [{ id: '_default', label: 'Format', icon: '📄', description: '', template: props.formatTemplate }]
  return []
})

const currentTemplate = computed(() => {
  if (!selectedFormatId.value && activeFormats.value.length) return activeFormats.value[0].template
  const found = activeFormats.value.find(f => f.id === selectedFormatId.value)
  return found ? found.template : (activeFormats.value[0]?.template || props.formatTemplate)
})

const currentFormatLabel = computed(() => {
  const found = activeFormats.value.find(f => f.id === selectedFormatId.value)
  return found ? found.label : activeFormats.value[0]?.label || ''
})

function openPicker(mode) {
  if (activeFormats.value.length <= 1) {
    if (mode === 'copy') copyTemplate(currentTemplate.value, currentFormatLabel.value)
    else showHelp.value = !showHelp.value
    return
  }
  pickerMode.value = pickerMode.value === mode ? null : mode
}

function closePicker() {
  pickerMode.value = null
}

function selectFormat(fmt) {
  selectedFormatId.value = fmt.id
  if (pickerMode.value === 'copy') {
    copyTemplate(fmt.template, fmt.label)
  } else {
    showHelp.value = true
  }
  closePicker()
}

async function copyTemplate(text, label) {
  try {
    await navigator.clipboard.writeText(text)
  } catch {
    const ta = document.createElement('textarea')
    ta.value = text
    document.body.appendChild(ta)
    ta.select()
    document.execCommand('copy')
    document.body.removeChild(ta)
  }
  toastLabel.value = label
  toastVisible.value = true
  setTimeout(() => { toastVisible.value = false }, 2500)
}

function handleOutsideClick(e) {
  if (pickerMode.value && rootRef.value && !rootRef.value.contains(e.target)) {
    closePicker()
  }
}

onMounted(() => document.addEventListener('mousedown', handleOutsideClick))
onBeforeUnmount(() => document.removeEventListener('mousedown', handleOutsideClick))
</script>

<style scoped>
.format-help {
  position: relative;
}

.format-btn-group {
  display: flex;
  gap: 8px;
}

.format-picker {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  z-index: 200;
  width: 360px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  box-shadow: 0 8px 32px rgba(15, 23, 42, 0.14), 0 2px 8px rgba(15, 23, 42, 0.08);
  overflow: hidden;
}

.format-picker__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px 10px;
  border-bottom: 1px solid #f1f5f9;
  font-weight: 700;
  font-size: 13px;
  color: #1e293b;
}

.format-picker__close {
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  font-size: 14px;
  padding: 2px 6px;
  border-radius: 6px;
  line-height: 1;
}
.format-picker__close:hover { background: #f1f5f9; color: #475569; }

.format-picker__list {
  list-style: none;
  margin: 0;
  padding: 6px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.format-picker__item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.12s;
}
.format-picker__item:hover { background: #f8faff; }
.format-picker__item--active { background: #eef2ff; }

.format-picker__icon {
  font-size: 20px;
  flex: 0 0 auto;
  line-height: 1;
}

.format-picker__info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.format-picker__label {
  font-weight: 700;
  font-size: 13px;
  color: #1e293b;
}

.format-picker__desc {
  font-size: 11px;
  color: #64748b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.format-picker__action {
  flex: 0 0 auto;
  font-size: 11px;
  font-weight: 600;
  color: #29428e;
  background: #eef2ff;
  padding: 3px 8px;
  border-radius: 999px;
}

.format-content__label {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0 4px;
  font-size: 12px;
  font-weight: 700;
  color: #29428e;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.format-toast {
  position: fixed;
  bottom: 28px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  background: #1e293b;
  color: #ffffff;
  font-size: 14px;
  font-weight: 600;
  padding: 12px 22px;
  border-radius: 999px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.28);
  white-space: nowrap;
  pointer-events: none;
}

.picker-fade-enter-active,
.picker-fade-leave-active { transition: opacity 0.15s, transform 0.15s; }
.picker-fade-enter-from,
.picker-fade-leave-to { opacity: 0; transform: translateY(-6px); }

.toast-fade-enter-active,
.toast-fade-leave-active { transition: opacity 0.2s, transform 0.2s; }
.toast-fade-enter-from,
.toast-fade-leave-to { opacity: 0; transform: translateX(-50%) translateY(8px); }
</style>
