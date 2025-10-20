<template>
  <div class="admin-actions">
    <AdminActionButton
      v-if="showEdit"
      type="edit"
      :label="editLabel"
      :disabled="editDisabled"
      :loading="editLoading"
      @click="handleEdit"
    />
    
    <AdminActionButton
      v-if="showView"
      type="view"
      :label="viewLabel"
      :disabled="viewDisabled"
      @click="handleView"
    />
    
    <AdminActionButton
      v-if="showDuplicate"
      type="duplicate"
      :label="duplicateLabel"
      :disabled="duplicateDisabled"
      :loading="duplicateLoading"
      @click="handleDuplicate"
    />

    <AdminActionButton
      v-if="showDelete"
      type="delete"
      :label="deleteLabel"
      :disabled="deleteDisabled"
      :loading="deleteLoading"
      @click="handleDelete"
    />

    <!-- Slot pour des actions personnalisées -->
    <slot name="custom-actions"></slot>
  </div>
</template>

<script>
import AdminActionButton from './AdminActionButton.vue'

export default {
  name: 'AdminActionsButtons',
  components: {
    AdminActionButton
  },
  props: {
    // Configuration des actions
    actions: {
      type: Array,
      default: () => ['edit', 'delete'],
      validator: (actions) => actions.every(action =>
        ['edit', 'delete', 'view', 'duplicate'].includes(action)
      )
    },
    
    // Labels personnalisés
    editLabel: {
      type: String,
      default: 'Éditer'
    },
    deleteLabel: {
      type: String,
      default: 'Supprimer'
    },
    viewLabel: {
      type: String,
      default: 'Voir'
    },
    duplicateLabel: {
      type: String,
      default: 'Dupliquer'
    },
    
    // États des boutons
    editDisabled: {
      type: Boolean,
      default: false
    },
    deleteDisabled: {
      type: Boolean,
      default: false
    },
    viewDisabled: {
      type: Boolean,
      default: false
    },
    duplicateDisabled: {
      type: Boolean,
      default: false
    },
    
    // Loading states
    editLoading: {
      type: Boolean,
      default: false
    },
    deleteLoading: {
      type: Boolean,
      default: false
    },
    duplicateLoading: {
      type: Boolean,
      default: false
    },
    
    // Configuration de confirmation pour delete
    confirmDelete: {
      type: Boolean,
      default: true
    },
    confirmMessage: {
      type: String,
      default: 'Êtes-vous sûr de vouloir supprimer cet élément ?'
    },
    
    // Données de l'item pour les événements
    item: {
      type: Object,
      default: () => ({})
    }
  },
  emits: ['edit', 'delete', 'view', 'duplicate'],
  computed: {
    showEdit() {
      return this.actions.includes('edit')
    },
    showDelete() {
      return this.actions.includes('delete')
    },
    showView() {
      return this.actions.includes('view')
    },
    showDuplicate() {
      return this.actions.includes('duplicate')
    }
  },
  methods: {
    handleEdit() {
      this.$emit('edit', this.item)
    },
    
    handleView() {
      this.$emit('view', this.item)
    },

    handleDuplicate() {
      this.$emit('duplicate', this.item)
    },
    
    handleDelete() {
      if (this.confirmDelete) {
        if (confirm(this.confirmMessage)) {
          this.$emit('delete', this.item)
        }
      } else {
        this.$emit('delete', this.item)
      }
    }
  }
}
</script>

<style scoped>
.admin-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  flex-wrap: wrap;
}

/* Responsive */
@media (max-width: 768px) {
  .admin-actions {
    gap: 0.25rem;
    flex-direction: column;
    align-items: stretch;
  }
}

@media (max-width: 480px) {
  .admin-actions {
    gap: 0.25rem;
  }
}
</style>
