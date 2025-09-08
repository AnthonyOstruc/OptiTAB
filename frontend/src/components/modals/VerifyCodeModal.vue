<template>
  <Modal :is-open="isOpen" title="Vérification du compte" size="small" @close="handleClose">
    <form @submit.prevent="handleVerify" class="verify-form">
      <label for="code-input" class="verify-label">Code reçu par email</label>
      <input
        id="code-input"
        v-model="code"
        class="verify-input"
        placeholder="Entrez le code"
        required
        autocomplete="one-time-code"
      />
      <button type="submit" class="verify-btn" :disabled="isSubmitting">
        {{ isSubmitting ? 'Vérification...' : 'Valider' }}
      </button>
      <div v-if="error" class="verify-error">{{ error }}</div>
    </form>
  </Modal>
</template>

<script>
import Modal from '@/components/common/Modal.vue'
import { verifyUserCode } from '@/api'

export default {
  name: 'VerifyCodeModal',
  components: { Modal },
  props: {
    isOpen: { type: Boolean, default: false },
    email: { type: String, required: true }
  },
  emits: ['close', 'verified'],
  data() {
    return {
      code: '',
      error: '',
      isSubmitting: false
    }
  },
  methods: {
    async handleVerify() {
      this.error = ''
      this.isSubmitting = true
      try {
        await verifyUserCode({ email: this.email, code: this.code })
        this.$emit('verified')
        this.code = ''
      } catch (e) {
        this.error = 'Code invalide ou expiré.'
      } finally {
        this.isSubmitting = false
      }
    },
    handleClose() {
      this.$emit('close')
      this.code = ''
      this.error = ''
    }
  }
}
</script>

<style scoped lang="scss">
.verify-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
  margin-top: 10px;
}
.verify-label {
  font-weight: 600;
  color: #333;
}
.verify-input {
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 16px;
  background: #fff;
  color: #222;
  transition: border 0.2s;
}
.verify-input:focus {
  border-color: #2563eb;
  outline: none;
}
.verify-btn {
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 12px 0;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
}
.verify-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
.verify-error {
  color: #ef4444;
  font-size: 15px;
  text-align: center;
  margin-top: -8px;
}
</style> 