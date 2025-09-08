import { ref } from 'vue'

const toasts = ref([])
let nextId = 1

export function useToast() {
  const showToast = (message, type = 'info', duration = 5000) => {
    const id = nextId++
    const toast = {
      id,
      message,
      type,
      visible: true
    }
    
    toasts.value.push(toast)
    
    // Auto remove after duration
    setTimeout(() => {
      removeToast(id)
    }, duration)
    
    return id
  }
  
  const removeToast = (id) => {
    const index = toasts.value.findIndex(toast => toast.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }
  
  const success = (message, duration) => showToast(message, 'success', duration)
  const error = (message, duration) => showToast(message, 'error', duration)
  const warning = (message, duration) => showToast(message, 'warning', duration)
  const info = (message, duration) => showToast(message, 'info', duration)
  
  return {
    toasts,
    showToast,
    removeToast,
    success,
    error,
    warning,
    info
  }
} 