<template>
  <div v-if="showModal" class="ai-modal-overlay" @click="closeModal">
    <div class="ai-modal-content" @click.stop>
      <div class="ai-modal-header">
        <h3>🤖 Assistant IA OptiTAB</h3>
        <button @click="closeModal" class="close-btn">✕</button>
      </div>

      <AIAssistant
        :auto-focus="true"
      />
    </div>
  </div>
</template>

<script>
import AIAssistant from './AIAssistant.vue'

export default {
  name: 'AIModal',
  components: {
    AIAssistant
  },
  props: {
    showModal: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    closeModal() {
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
.ai-modal-overlay {
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
}

.ai-modal-content {
  background: #f8f9fa;
  border-radius: 12px;
  width: 90%;
  max-width: 900px;
  height: 80vh;
  max-height: 700px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
}

.ai-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
  background: #f8f9fa;
}

.ai-modal-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.2rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 5px;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #e9ecef;
  color: #333;
}

@media (max-width: 768px) {
  .ai-modal-content {
    width: 95%;
    max-height: 95vh;
  }

  .ai-modal-header {
    padding: 15px;
  }

  .ai-modal-header h3 {
    font-size: 1rem;
  }
}
</style>
