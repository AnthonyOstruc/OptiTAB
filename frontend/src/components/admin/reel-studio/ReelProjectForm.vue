<template>
  <form class="reel-project-form" @submit.prevent="handleSubmit">
    <h3>Nouveau reel</h3>

    <div class="form-grid">
      <label>
        Titre
        <input
          v-model="form.title"
          type="text"
          maxlength="255"
          required
          placeholder="Ex: Dérivée piège - Terminale"
        />
      </label>

      <label>
        Thème
        <input
          v-model="form.theme"
          type="text"
          maxlength="255"
          placeholder="Ex: Dérivation"
        />
      </label>

      <label>
        Niveau
        <select v-model="form.level" required>
          <option disabled value="">Sélectionner</option>
          <option v-for="item in levelOptions" :key="item" :value="item">{{ item }}</option>
        </select>
      </label>

      <label>
        Format
        <select v-model="form.format_type" required>
          <option disabled value="">Sélectionner</option>
          <option v-for="item in formatOptions" :key="item" :value="item">{{ item }}</option>
        </select>
      </label>

      <label>
        Durée cible (s)
        <input
          v-model.number="form.target_duration_seconds"
          type="number"
          min="5"
          max="300"
          required
        />
      </label>

      <label>
        Nombre de slides
        <input
          v-model.number="form.slide_count"
          type="number"
          min="1"
          max="30"
          required
        />
      </label>
    </div>

    <div class="form-actions">
      <button class="btn-primary" type="submit" :disabled="loading">
        {{ loading ? 'Création...' : submitLabel }}
      </button>
      <button class="btn-secondary" type="button" @click="$emit('cancel')">Annuler</button>
    </div>
  </form>
</template>

<script setup>
import { reactive, watch } from 'vue'

const DEFAULT_FORM = {
  title: '',
  theme: '',
  level: '',
  format_type: '',
  target_duration_seconds: 30,
  slide_count: 6,
}

const levelOptions = ['Seconde', 'Première', 'Terminale', 'Bac']
const formatOptions = ['Défi rapide', 'Erreur fréquente', 'Correction pas à pas', 'Piège classique']

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
    default: 'Créer le projet',
  },
})

const emit = defineEmits(['submit', 'cancel'])

const form = reactive({ ...DEFAULT_FORM })

watch(
  () => props.initialValues,
  (values) => {
    Object.assign(form, DEFAULT_FORM, values || {})
  },
  { immediate: true, deep: true }
)

function handleSubmit() {
  emit('submit', {
    title: String(form.title || '').trim(),
    theme: String(form.theme || '').trim(),
    level: form.level,
    format_type: form.format_type,
    target_duration_seconds: Number(form.target_duration_seconds || 0),
    slide_count: Number(form.slide_count || 0),
    status: 'draft',
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
  grid-template-columns: repeat(2, minmax(0, 1fr));
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

input,
select {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 14px;
  color: #0f172a;
  background: #fff;
}

input:focus,
select:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
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
