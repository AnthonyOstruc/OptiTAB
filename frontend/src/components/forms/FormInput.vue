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
/* Même style que les fenêtres (components/common/Modal.vue, variables --om-*). */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 7px;
}
.form-label {
  font-family: var(--om-font, 'Montserrat', sans-serif);
  font-weight: 600;
  color: var(--om-ink-soft, #2c3550);
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 4px;
}
.required-indicator {
  color: var(--om-red, #c0392b);
  font-weight: 600;
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
  color: var(--om-muted, #5d667d);
  transition: color 0.2s ease;

  &:hover:not(:disabled) {
    color: var(--om-navy, #1b3c8e);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  &:focus {
    outline: 2px solid #1b3c8e;
    outline-offset: 2px;
  }
}
.form-input {
  width: 100%;
  min-height: 48px;
  padding: 12px 16px;
  border: 1.5px solid var(--om-line-strong, #cfd6e4);
  border-radius: 12px;
  font-family: var(--om-font, 'Montserrat', sans-serif);
  font-size: 15.5px;
  font-weight: 500;
  background: #fff;
  color: var(--om-ink, #121a33);
  transition: border-color 0.2s, box-shadow 0.2s;
  margin-bottom: 0;

  &::placeholder {
    color: #8a93a8;
  }

  // Place pour le bouton « afficher le mot de passe »
  &[type="password"],
  .input-wrapper:has(.password-toggle) & {
    padding-right: 48px;
  }

  &.has-error {
    border-color: var(--om-red, #c0392b);
  }

  &.is-disabled {
    background: var(--om-bg-soft, #f6f8fc);
  }
}
.form-input:focus {
  border-color: var(--om-navy, #1b3c8e);
  outline: none;
  box-shadow: 0 0 0 4px rgba(27, 60, 142, 0.12);
}
.form-input.has-error:focus {
  box-shadow: 0 0 0 4px rgba(192, 57, 43, 0.12);
}
.form-error {
  color: var(--om-red, #c0392b);
  font-size: 13.5px;
  margin: 0;
  font-weight: 500;
}
.form-help {
  color: var(--om-muted, #5d667d);
  font-size: 13.5px;
  margin: 0;
}
</style> 