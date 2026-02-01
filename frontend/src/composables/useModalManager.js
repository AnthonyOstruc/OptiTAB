import { ref, reactive } from 'vue'
import { lockBodyScroll, unlockBodyScroll } from '@/utils/bodyScrollLock'

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
    
    lockBodyScroll(`modal:${modalId}`, { mode: 'overflow' })
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
    
    unlockBodyScroll(`modal:${modalId}`)
  }

  // Close all modals
  const closeAllModals = () => {
    Object.keys(modalStates).forEach(modalId => {
      modalStates[modalId].isOpen = false
    })

    const modalsToUnlock = [...activeModals.value]
    activeModals.value = []
    modalsToUnlock.forEach((modalId) => unlockBodyScroll(`modal:${modalId}`))
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
