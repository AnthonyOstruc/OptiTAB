<template>
  <div v-if="fieldConfig" class="form-field" :class="fieldClass">
    <!-- Text, Email, Password, Number, Tel, URL inputs -->
    <FormInput
      v-if="isInputField"
      v-model="fieldValue"
      :type="fieldConfig.type"
      :label="fieldConfig.label"
      :placeholder="fieldConfig.placeholder"
      :required="fieldConfig.required"
      :disabled="disabled"
      :autocomplete="fieldConfig.autocomplete"
      :error="getFieldError(fieldName)"
      :help-text="fieldConfig.helpText"
      @blur="handleBlur"
      @input="handleInput"
    />

    <!-- Checkbox fields -->
    <div v-else-if="fieldConfig.type === 'checkbox'" class="checkbox-field">
      <label class="checkbox-label">
        <input
          v-model="fieldValue"
          type="checkbox"
          class="checkbox-input"
          :required="fieldConfig.required"
          :disabled="disabled"
        />
        <span class="checkbox-text" v-html="fieldConfig.label"></span>
      </label>
      <p v-if="getFieldError(fieldName)" class="form-error">
        {{ getFieldError(fieldName) }}
      </p>
    </div>

    <!-- Custom field types can be added here -->
    <div v-else class="unsupported-field">
      <p class="error-message">Field type "{{ fieldConfig.type }}" is not supported</p>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import FormInput from './FormInput.vue'

export default {
  name: 'FormField',
  components: {
    FormInput
  },
  props: {
    fieldName: {
      type: String,
      required: true
    },
    fieldConfig: {
      type: Object,
      required: true
    },
    modelValue: {
      type: [String, Number, Boolean],
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    },
    getFieldError: {
      type: Function,
      required: true
    }
  },
  emits: ['update:modelValue', 'blur', 'input'],
  setup(props, { emit }) {
    // Computed
    const fieldValue = computed({
      get: () => props.modelValue,
      set: (value) => emit('update:modelValue', value)
    })

    const isInputField = computed(() => {
      if (!props.fieldConfig) return false
      const inputTypes = ['text', 'email', 'password', 'number', 'tel', 'url']
      return inputTypes.includes(props.fieldConfig.type)
    })

    const fieldClass = computed(() => ({
      'has-error': props.getFieldError(props.fieldName),
      'is-disabled': props.disabled
    }))

    // Methods
    const handleBlur = (event) => {
      emit('blur', { fieldName: props.fieldName, event })
    }

    const handleInput = (event) => {
      emit('input', { fieldName: props.fieldName, event })
    }

    return {
      fieldValue,
      isInputField,
      fieldClass,
      handleBlur,
      handleInput
    }
  }
}
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;

.form-field {
  &.has-error {
    .checkbox-label {
      color: #ef4444;
    }
  }
  
  &.is-disabled {
    opacity: 0.7;
    pointer-events: none;
  }
}

.checkbox-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  line-height: 1.5;
  color: $text-color;
}

.checkbox-input {
  width: 16px;
  height: 16px;
  accent-color: $primary-color;
  margin-top: 2px;
  flex-shrink: 0;
}

.checkbox-text {
  color: inherit;
  
  :deep(a), :deep(button) {
    color: $primary-color;
    text-decoration: none;
    font-weight: 500;
    cursor: pointer;
    background: none;
    border: none;
    padding: 0;
    font-size: 14px;

    &:hover {
      text-decoration: underline;
    }
  }
}

.form-error {
  color: #ef4444;
  font-size: 14px;
  margin: 0;
  font-weight: 500;
}

.unsupported-field {
  padding: 12px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  
  .error-message {
    color: #dc2626;
    margin: 0;
    font-size: 14px;
  }
}
</style> 