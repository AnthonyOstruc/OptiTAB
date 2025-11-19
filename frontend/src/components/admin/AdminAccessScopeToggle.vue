<template>
  <div class="access-toggle" :class="[`size-${size}`, { disabled: loading }]">
    <button
      v-for="option in options"
      :key="option.value"
      type="button"
      class="access-btn"
      :class="{ active: modelValue === option.value }"
      :title="option.description"
      :disabled="loading"
      @click="select(option.value)"
    >
      {{ option.label }}
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: String,
    default: 'paid'
  },
  size: {
    type: String,
    default: 'md'
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const options = [
  { value: 'paid', label: 'Payant', description: 'Réservé aux abonnés' },
  { value: 'free', label: 'Gratuit', description: 'Visible sans abonnement' },
  { value: 'both', label: 'Les 2', description: 'Gratuit et accessible aux abonnés' }
]

function select(value) {
  if (props.loading || value === props.modelValue) {
    return
  }
  emit('update:modelValue', value)
  emit('change', value)
}
</script>

<style scoped>
.access-toggle {
  display: inline-flex;
  border-radius: 999px;
  background: #f1f5f9;
  padding: 3px;
  gap: 4px;
  align-items: center;
}

.access-toggle.disabled {
  opacity: 0.7;
}

.access-btn {
  border: none;
  border-radius: 999px;
  background: transparent;
  color: #0f172a;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 6px 12px;
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease;
}

.access-btn.active {
  background: #0f172a;
  color: #fff;
}

.access-btn:disabled {
  cursor: not-allowed;
}

.size-sm .access-btn {
  font-size: 0.75rem;
  padding: 4px 10px;
}
</style>
