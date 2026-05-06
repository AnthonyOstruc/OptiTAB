<template>
  <form class="reel-project-form" @submit.prevent="handleSubmit">
    <h3>{{ formTitle }}</h3>

    <div class="form-grid">
      <label>
        Titre
        <input
          v-model="form.title"
          type="text"
          maxlength="255"
          required
          :aria-invalid="titleSubmitted && !canSubmitTitle"
          placeholder="Ex: Defi integrale"
        />
        <span v-if="titleSubmitted && !canSubmitTitle" class="field-error">Titre obligatoire.</span>
      </label>

    </div>

    <div class="form-actions">
      <button class="btn-primary" type="submit" :disabled="loading || !canSubmitTitle">
        {{ loading ? 'Sauvegarde...' : submitLabel }}
      </button>
      <button class="btn-secondary" type="button" @click="$emit('cancel')">Annuler</button>
    </div>
  </form>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'

const DEFAULT_FORM = {
  title: '',
}

const props = defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
  initialValues: {
    type: Object,
    default: () => ({}),
  },
  submitLabel: {
    type: String,
    default: 'Creer le projet',
  },
  formTitle: {
    type: String,
    default: 'Nouveau reel',
  },
})

const emit = defineEmits(['submit', 'cancel'])

const form = reactive({ ...DEFAULT_FORM })
const titleSubmitted = ref(false)
const titleValue = computed(() => String(form.title || '').trim())
const canSubmitTitle = computed(() => titleValue.value.length > 0)

watch(
  () => props.initialValues,
  (values) => {
    Object.assign(form, DEFAULT_FORM, values || {})
    titleSubmitted.value = false
  },
  { immediate: true, deep: true }
)

function handleSubmit() {
  titleSubmitted.value = true
  if (!canSubmitTitle.value) return

  emit('submit', {
    title: titleValue.value,
  })
}
</script>

<style scoped>
.reel-project-form {
  border: 1px solid #dbe4ee;
  border-radius: 12px;
  background: #ffffff;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.reel-project-form h3 {
  margin: 0;
  color: #0f172a;
  font-size: 18px;
}

.form-grid {
  display: grid;
  grid-template-columns: minmax(280px, 1fr);
  gap: 12px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 13px;
  color: #334155;
  font-weight: 700;
}

input {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 14px;
  color: #0f172a;
  background: #fff;
}

input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.field-error {
  color: #b91c1c;
  font-size: 12px;
  font-weight: 700;
}

.form-actions {
  display: flex;
  gap: 10px;
}

.btn-primary,
.btn-secondary {
  border: 0;
  border-radius: 8px;
  padding: 10px 14px;
  font-weight: 700;
  font-size: 14px;
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

.btn-secondary {
  background: #e2e8f0;
  color: #1e293b;
}

@media (max-width: 900px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
