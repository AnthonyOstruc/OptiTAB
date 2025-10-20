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
  gap: 10px;
}

.form-fields {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-submit-btn {
  @extend .btn;
  @extend .btn-primary;
  width: 100%;
  padding: 14px 20px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  position: relative;
  min-height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
}
</style> 