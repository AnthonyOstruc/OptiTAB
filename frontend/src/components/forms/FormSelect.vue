<template>
  <div class="form-group">
    <label v-if="label" :for="selectId" class="form-label">
      {{ label }}
      <span v-if="required" class="required-indicator">*</span>
    </label>
    <div class="input-wrapper">
      <select
        :id="selectId"
        v-model="modelValueProxy"
        :required="required"
        :disabled="disabled"
        class="form-input"
        :class="inputClass"
        @focus="handleFocus"
        @blur="handleBlur"
      >
        <option v-for="option in options" :key="option.value" :value="option.value">
          {{ option.label }}
        </option>
      </select>
    </div>
    <p v-if="error" class="form-error">{{ error }}</p>
    <p v-if="helpText" class="form-help">{{ helpText }}</p>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
export default {
  name: 'FormSelect',
  props: {
    modelValue: {
      type: [String, Number],
      default: ''
    },
    label: {
      type: String,
      default: ''
    },
    required: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: ''
    },
    helpText: {
      type: String,
      default: ''
    },
    options: {
      type: Array,
      required: true // [{ value: '', label: '--' }, ...]
    }
  },
  emits: ['update:modelValue', 'focus', 'blur'],
  setup(props, { emit }) {
    const selectId = `select-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    const modelValueProxy = computed({
      get: () => props.modelValue,
      set: (value) => emit('update:modelValue', value)
    })
    const inputClass = computed(() => ({
      'has-error': props.error,
      'is-disabled': props.disabled
    }))
    const handleFocus = (event) => emit('focus', event)
    const handleBlur = (event) => emit('blur', event)
    return {
      selectId,
      modelValueProxy,
      inputClass,
      handleFocus,
      handleBlur
    }
  }
}
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.form-label {
  font-weight: 900;
  color: $text-color;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 4px;
}
.required-indicator {
  color: #ef4444;
  font-weight: 700;
}
.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}
.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 16px;
  background: #fff;
  color: #222;
  transition: border 0.2s;
  margin-bottom: 0;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}
.form-input:focus {
  border-color: #2563eb;
  outline: none;
}
.form-error {
  color: #ef4444;
  font-size: 14px;
  margin: 0;
  font-weight: 500;
}
.form-help {
  color: #6b7280;
  font-size: 14px;
  margin: 0;
}
</style> 