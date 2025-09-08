<template>
  <button 
    :class="buttonClass"
    :disabled="disabled"
    @click="handleClick"
    :title="tooltip"
  >
    <span v-if="icon" class="button-icon">{{ icon }}</span>
    <span>{{ computedLabel }}</span>
  </button>
</template>

<script>
export default {
  name: 'AdminActionButton',
  props: {
    type: {
      type: String,
      required: true,
      validator: (value) => ['edit', 'delete', 'view', 'add', 'save', 'cancel', 'duplicate'].includes(value)
    },
    label: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    },
    tooltip: {
      type: String,
      default: ''
    }
  },
  emits: ['click'],
  computed: {
    buttonClass() {
      const baseClass = 'admin-action-btn'
      const typeClass = this.getTypeClass()
      const loadingClass = this.loading ? 'loading' : ''
      const disabledClass = this.disabled ? 'disabled' : ''
      
      return [baseClass, typeClass, loadingClass, disabledClass].filter(Boolean).join(' ')
    },
    
    icon() {
      const icons = {
        edit: '✏️',
        delete: '🗑️',
        view: '👁️',
        add: '➕',
        save: '💾',
        cancel: '❌',
        duplicate: '📋'
      }
      return icons[this.type] || ''
    },
    
    computedLabel() {
      if (this.label) return this.label
      
      const defaultLabels = {
        edit: 'Éditer',
        delete: 'Supprimer',
        view: 'Voir',
        add: 'Ajouter',
        save: 'Enregistrer',
        cancel: 'Annuler',
        duplicate: 'Dupliquer'
      }
      return defaultLabels[this.type] || ''
    }
  },
  methods: {
    getTypeClass() {
      const typeClasses = {
        edit: 'btn-secondary',
        delete: 'btn-danger',
        view: 'btn-info',
        add: 'btn-primary',
        save: 'btn-success',
        cancel: 'btn-light',
        duplicate: 'btn-info' // Utilise la même couleur que view
      }
      return typeClasses[this.type] || 'btn-secondary'
    },
    
    handleClick(event) {
      if (this.disabled || this.loading) return
      this.$emit('click', event)
    }
  }
}
</script>

<style scoped>
.admin-action-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  border: 1px solid transparent;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  white-space: nowrap;
}

.button-icon {
  font-size: 0.875rem;
}

/* Types de boutons */
.btn-primary {
  background-color: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

.btn-primary:hover:not(.disabled) {
  background-color: #2563eb;
  border-color: #2563eb;
}

.btn-secondary {
  background-color: #6b7280;
  border-color: #6b7280;
  color: white;
}

.btn-secondary:hover:not(.disabled) {
  background-color: #4b5563;
  border-color: #4b5563;
}

.btn-danger {
  background-color: #ef4444;
  border-color: #ef4444;
  color: white;
}

.btn-danger:hover:not(.disabled) {
  background-color: #dc2626;
  border-color: #dc2626;
}

.btn-success {
  background-color: #10b981;
  border-color: #10b981;
  color: white;
}

.btn-success:hover:not(.disabled) {
  background-color: #059669;
  border-color: #059669;
}

.btn-info {
  background-color: #06b6d4;
  border-color: #06b6d4;
  color: white;
}

.btn-info:hover:not(.disabled) {
  background-color: #0891b2;
  border-color: #0891b2;
}

.btn-light {
  background-color: #f3f4f6;
  border-color: #d1d5db;
  color: #374151;
}

.btn-light:hover:not(.disabled) {
  background-color: #e5e7eb;
  border-color: #9ca3af;
}

/* États */
.admin-action-btn.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

.admin-action-btn.loading {
  opacity: 0.7;
  cursor: wait;
}

.admin-action-btn.loading .button-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .admin-action-btn {
    padding: 0.25rem 0.5rem;
    font-size: 0.75rem;
  }
  
  .button-icon {
    font-size: 0.75rem;
  }
}
</style>
