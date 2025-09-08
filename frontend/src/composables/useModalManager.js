import { ref, reactive } from 'vue'

// Global modal state
const modalStates = reactive({})
const activeModals = ref([])

export function useModalManager() {
  // Open a modal
  const openModal = (modalId, options = {}) => {
    modalStates[modalId] = {
      isOpen: true,
      ...options
    }
    
    if (!activeModals.value.includes(modalId)) {
      activeModals.value.push(modalId)
    }
    
    // Prevent body scroll
    document.body.style.overflow = 'hidden'
  }

  // Close a modal
  const closeModal = (modalId) => {
    if (modalStates[modalId]) {
      modalStates[modalId].isOpen = false
    }
    
    const index = activeModals.value.indexOf(modalId)
    if (index > -1) {
      activeModals.value.splice(index, 1)
    }
    
    // Restore body scroll if no active modals
    if (activeModals.value.length === 0) {
      document.body.style.overflow = ''
    }
  }

  // Close all modals
  const closeAllModals = () => {
    Object.keys(modalStates).forEach(modalId => {
      modalStates[modalId].isOpen = false
    })
    activeModals.value = []
    document.body.style.overflow = ''
  }

  // Check if modal is open
  const isModalOpen = (modalId) => {
    return modalStates[modalId]?.isOpen || false
  }

  // Get modal state
  const getModalState = (modalId) => {
    return modalStates[modalId] || { isOpen: false }
  }

  // Update modal options
  const updateModalOptions = (modalId, options) => {
    if (modalStates[modalId]) {
      Object.assign(modalStates[modalId], options)
    }
  }

  return {
    // State
    modalStates,
    activeModals,
    
    // Methods
    openModal,
    closeModal,
    closeAllModals,
    isModalOpen,
    getModalState,
    updateModalOptions
  }
}

// Predefined modal IDs
export const MODAL_IDS = {
  LOGIN: 'login',
  REGISTER: 'register',
  FORGOT_PASSWORD: 'forgot-password',
  SIGNUP: 'signup',
  CONFIRM_DELETE: 'confirm-delete',
  SETTINGS: 'settings',
  AUTO_NIVEAU: 'auto-niveau'
} 