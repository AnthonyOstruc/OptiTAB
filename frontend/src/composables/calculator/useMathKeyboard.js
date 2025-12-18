/**
 * Composable pour le clavier mathématique virtuel
 */
import { ref } from 'vue'
import { KEYBOARD_TOOLS } from './graphConfig'

export function useMathKeyboard() {
  const showCustomKeyboard = ref(false)
  const activeTab = ref('algebra')
  
  // Outils par onglet
  const algebraTools = KEYBOARD_TOOLS.algebra
  const trigonometryTools = KEYBOARD_TOOLS.trigonometry
  const exponentialTools = KEYBOARD_TOOLS.exponential
  const specialFunctions = KEYBOARD_TOOLS.special
  
  function toggleVirtualKeyboard() {
    showCustomKeyboard.value = !showCustomKeyboard.value
  }
  
  function closeKeyboard() {
    showCustomKeyboard.value = false
  }
  
  function openKeyboard() {
    showCustomKeyboard.value = true
  }
  
  function setActiveTab(tab) {
    activeTab.value = tab
  }
  
  /**
   * Insère une valeur dans un mathfield
   * @param {Object} mf - Référence au mathfield
   * @param {string} val - Valeur à insérer
   */
  function insert(mf, val) {
    if (!mf) return
    
    // Gestion spéciale pour certaines insertions
    if (val === '\\frac') {
      mf.executeCommand(['insert', '\\frac{#@}{#?}'])
    } else if (val === '\\sqrt{}') {
      mf.executeCommand(['insert', '\\sqrt{#@}'])
    } else if (val === '\\sqrt[n]{}') {
      mf.executeCommand(['insert', '\\sqrt[#?]{#@}'])
    } else if (val === '^\\square') {
      mf.executeCommand(['insert', '^{#?}'])
    } else if (val.endsWith('(')) {
      mf.executeCommand(['insert', val + '#@)'])
    } else if (val === '\\left|') {
      mf.executeCommand(['insert', '\\left|#@\\right|'])
    } else if (val.endsWith('{')) {
      mf.executeCommand(['insert', val + '#@}'])
    } else {
      mf.executeCommand(['insert', val])
    }
    
    mf.focus()
  }
  
  /**
   * Gère les raccourcis clavier
   * @param {KeyboardEvent} event
   * @param {Object} mf - Référence au mathfield
   * @param {Function} onCalculate - Callback pour le calcul
   */
  function handleKeyDown(event, mf, onCalculate) {
    if (event.key === 'Enter') {
      event.preventDefault()
      if (onCalculate) onCalculate()
    } else if (event.key === 'Escape') {
      closeKeyboard()
    }
  }
  
  return {
    showCustomKeyboard,
    activeTab,
    algebraTools,
    trigonometryTools,
    exponentialTools,
    specialFunctions,
    toggleVirtualKeyboard,
    closeKeyboard,
    openKeyboard,
    setActiveTab,
    insert,
    handleKeyDown
  }
}
