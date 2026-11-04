<template>
  <form @submit.prevent="handleSubmit" class="dynamic-form">
    <!-- Form Fields -->
    <div class="form-fields">
      <template v-for="fieldName in fieldNames" :key="fieldName">
        <FormField
          :field-name="fieldName"
          :field-config="getFieldConfig(fieldName)"
          v-model="formData[fieldName]"
          :disabled="isSubmitting"
          :get-field-error="getFieldError"
          @blur="handleFieldBlur"
          @input="handleFieldInput"
        />
      </template>
    </div>

    <!-- Custom Form Content -->
    <slot name="form-content" />

    <!-- Submit Button -->
    <button 
      type="submit" 
      class="form-submit-btn"
      :disabled="isSubmitting || !isValid"
    >
      <LoadingSpinner v-if="isSubmitting" />
      <span v-else>{{ submitText }}</span>
    </button>

    <!-- Custom Actions -->
    <slot name="form-actions" />
  </form>
</template>

<script>
import FormField from './FormField.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

export default {
  name: 'DynamicForm',
  components: {
    FormField,
    LoadingSpinner
  },
  props: {
    // Form configuration
    fieldNames: {
      type: Array,
      required: true
    },
    getFieldConfig: {
      type: Function,
      required: true
    },
    
    // Form state
    formData: {
      type: Object,
      required: true
    },
    isSubmitting: {
      type: Boolean,
      default: false
    },
    isValid: {
      type: Boolean,
      default: true
    },
    
    // Form methods
    getFieldError: {
      type: Function,
      required: true
    },
    setFieldTouched: {
      type: Function,
      required: true
    },
    
    // UI
    submitText: {
      type: String,
      default: 'Soumettre'
    }
  },
  emits: ['submit', 'field-blur', 'field-input'],
  setup(props, { emit }) {
    // Methods
    const handleSubmit = () => {
      emit('submit')
    }

    const handleFieldBlur = ({ fieldName, event }) => {
      props.setFieldTouched(fieldName)
      emit('field-blur', { fieldName, event })
    }

    const handleFieldInput = ({ fieldName, event }) => {
      emit('field-input', { fieldName, event })
    }

    return {
      handleSubmit,
      handleFieldBlur,
      handleFieldInput
    }
  }
}
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;

.dynamic-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.form-fields {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

/* Bouton principal des fenêtres (même style que .om-btn--primary). */
.form-submit-btn {
  width: 100%;
  min-height: 50px;
  margin-top: 4px;
  padding: 0 24px;
  border: 0;
  border-radius: 999px;
  background: var(--om-navy, #1b3c8e);
  color: #fff;
  font-family: var(--om-font, 'Montserrat', sans-serif);
  font-size: 15.5px;
  font-weight: 600;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;

  &:hover:not(:disabled) {
    background: var(--om-navy-700, #163274);
    box-shadow: 0 8px 22px rgba(27, 60, 142, 0.25);
  }

  &:focus-visible {
    outline: 2px solid var(--om-navy, #1b3c8e);
    outline-offset: 3px;
  }

  &:disabled {
    opacity: 0.55;
    cursor: not-allowed;
  }
}
</style> 