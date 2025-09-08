<template>
  <div class="form-group">
    <label v-if="label" :for="inputId" class="form-label">
      {{ label }}
      <span v-if="required" class="required-indicator">*</span>
    </label>
    <div class="input-wrapper">
      <input
        :id="inputId"
        v-model="inputValue"
        :type="type"
        :placeholder="placeholder"
        :required="required"
        :disabled="disabled"
        :autocomplete="autocomplete"
        class="form-input"
        :class="inputClass"
        @input="handleInput"
        @focus="handleFocus"
        @blur="handleBlur"
        @keydown="handleKeydown"
      />
    </div>
    <p v-if="error" class="form-error">{{ error }}</p>
    <p v-if="helpText" class="form-help">{{ helpText }}</p>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
export default {
  name: 'FormInput',
  props: {
    modelValue: {
      type: [String, Number],
      default: ''
    },
    type: {
      type: String,
      default: 'text',
      validator: value => ['text', 'email', 'password', 'number', 'tel', 'url', 'date'].includes(value)
    },
    label: {
      type: String,
      default: ''
    },
    placeholder: {
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
    autocomplete: {
      type: String,
      default: ''
    },
    error: {
      type: String,
      default: ''
    },
    helpText: {
      type: String,
      default: ''
    }
  },
  emits: ['update:modelValue', 'input', 'focus', 'blur', 'keydown'],
  setup(props, { emit }) {
    const inputId = `input-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    const inputValue = computed({
      get: () => props.modelValue,
      set: (value) => emit('update:modelValue', value)
    })
    const inputClass = computed(() => ({
      'has-error': props.error,
      'is-disabled': props.disabled
    }))
    const handleInput = (event) => emit('input', event)
    const handleFocus = (event) => emit('focus', event)
    const handleBlur = (event) => emit('blur', event)
    const handleKeydown = (event) => emit('keydown', event)
    return {
      inputId,
      inputValue,
      inputClass,
      handleInput,
      handleFocus,
      handleBlur,
      handleKeydown
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