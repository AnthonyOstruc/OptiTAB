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
        :type="actualType"
        :placeholder="placeholder"
        :required="required"
        :disabled="disabled"
        :name="name"
        :autocomplete="autocomplete"
        class="form-input"
        :class="inputClass"
        @input="handleInput"
        @focus="handleFocus"
        @blur="handleBlur"
        @keydown="handleKeydown"
      />
      <!-- Password visibility toggle button -->
      <button
        v-if="type === 'password'"
        type="button"
        class="password-toggle"
        @click="togglePasswordVisibility"
        :disabled="disabled"
        tabindex="-1"
      >
        <svg
          v-if="isPasswordVisible"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
          <line x1="1" y1="1" x2="23" y2="23"></line>
        </svg>
        <svg
          v-else
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
          <circle cx="12" cy="12" r="3"></circle>
        </svg>
      </button>
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
    name: {
      type: String,
      default: ''
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
    const isPasswordVisible = ref(false)

    const inputValue = computed({
      get: () => props.modelValue,
      set: (value) => emit('update:modelValue', value)
    })

    const inputClass = computed(() => ({
      'has-error': props.error,
      'is-disabled': props.disabled
    }))

    const actualType = computed(() => {
      if (props.type === 'password') {
        return isPasswordVisible.value ? 'text' : 'password'
      }
      return props.type
    })

    const handleInput = (event) => emit('input', event)
    const handleFocus = (event) => emit('focus', event)
    const handleBlur = (event) => emit('blur', event)
    const handleKeydown = (event) => emit('keydown', event)

    const togglePasswordVisibility = () => {
      isPasswordVisible.value = !isPasswordVisible.value
    }

    return {
      inputId,
      inputValue,
      inputClass,
      actualType,
      isPasswordVisible,
      handleInput,
      handleFocus,
      handleBlur,
      handleKeydown,
      togglePasswordVisibility
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

.password-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  transition: color 0.2s ease;

  &:hover:not(:disabled) {
    color: #374151;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  &:focus {
    outline: 2px solid #2563eb;
    outline-offset: 2px;
  }
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

  // Add padding-right for password fields with toggle button
  &[type="password"] {
    padding-right: 48px;
  }
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