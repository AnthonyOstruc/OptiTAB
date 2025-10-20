<template>
  <div v-if="visible" class="modal-overlay" @click="handleOverlayClick">
    <div class="modal-container" @click.stop>
      <div class="modal-header" :class="{ danger: danger }">
        <h3>
          <i :class="danger ? 'fas fa-exclamation-triangle' : 'fas fa-question-circle'"></i>
          {{ title }}
        </h3>
      </div>

      <div class="modal-body">
        <p>{{ message }}</p>
      </div>

      <div class="modal-footer">
        <button @click="$emit('cancel')" class="btn btn-secondary">
          <i class="fas fa-times"></i>
          Annuler
        </button>
        <button 
          @click="$emit('confirm')" 
          :class="['btn', danger ? 'btn-danger' : 'btn-primary']"
        >
          <i :class="danger ? 'fas fa-trash' : 'fas fa-check'"></i>
          {{ danger ? 'Supprimer' : 'Confirmer' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConfirmModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: 'Confirmation'
    },
    message: {
      type: String,
      default: 'Êtes-vous sûr de vouloir continuer ?'
    },
    danger: {
      type: Boolean,
      default: false
    }
  },
  emits: ['confirm', 'cancel'],
  setup(props, { emit }) {
    const handleOverlayClick = () => {
      emit('cancel')
    }

    return {
      handleOverlayClick
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  max-width: 400px;
  width: 100%;
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-50px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  padding: 20px 25px;
  border-bottom: 2px solid #f1f3f4;
  background: #f8f9fa;
  border-radius: 12px 12px 0 0;
}

.modal-header.danger {
  background: #f8d7da;
  border-bottom-color: #f5c6cb;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.modal-header.danger h3 {
  color: #721c24;
}

.modal-body {
  padding: 25px;
}

.modal-body p {
  margin: 0;
  color: #495057;
  line-height: 1.5;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  padding: 20px 25px;
  border-top: 2px solid #f1f3f4;
  background: #f8f9fa;
  border-radius: 0 0 12px 12px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
  font-size: 0.95rem;
}

.btn-primary {
  background: #007cba;
  color: white;
}

.btn-primary:hover {
  background: #005a87;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-danger:hover {
  background: #c82333;
}

@media (max-width: 768px) {
  .modal-container {
    margin: 10px;
  }
  
  .modal-footer {
    flex-direction: column;
  }
  
  .btn {
    justify-content: center;
  }
}
</style>
