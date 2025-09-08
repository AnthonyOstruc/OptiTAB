<template>
  <div class="ai-floating-container">
    <button
      @click="toggleModal"
      class="ai-floating-btn"
      :class="{ active: showModal }"
      title="Assistant IA OptiTAB"
    >
      <span class="ai-icon">🤖</span>
      <span class="ai-text">IA</span>
    </button>

    <AIModal
      :show-modal="showModal"
      @close="closeModal"
    />
  </div>
</template>

<script>
import AIModal from './AIModal.vue'

export default {
  name: 'AIFloatingButton',
  components: {
    AIModal
  },
  props: {
    // Plus de props nécessaires
  },
  data() {
    return {
      showModal: false
    }
  },
  methods: {
    toggleModal() {
      this.showModal = !this.showModal
    },
    closeModal() {
      this.showModal = false
    }
  }
}
</script>

<style scoped>
.ai-floating-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 999;
}

.ai-floating-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  color: white;
  font-weight: bold;
}

.ai-floating-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.ai-floating-btn.active {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  animation: pulse 2s infinite;
}

.ai-icon {
  font-size: 20px;
  line-height: 1;
}

.ai-text {
  font-size: 10px;
  margin-top: 2px;
  line-height: 1;
}

@keyframes pulse {
  0% {
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  }
  50% {
    box-shadow: 0 4px 25px rgba(245, 87, 108, 0.4);
  }
  100% {
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  }
}

@media (max-width: 768px) {
  .ai-floating-container {
    bottom: 15px;
    right: 15px;
  }

  .ai-floating-btn {
    width: 50px;
    height: 50px;
  }

  .ai-icon {
    font-size: 18px;
  }

  .ai-text {
    font-size: 9px;
  }
}
</style>
