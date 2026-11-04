import { ref, reactive, computed, watch } from 'vue'

// Quand on quitte un champ en cliquant ailleurs (case à cocher, bouton), le
// message d'erreur qui apparaît décale la fenêtre pendant le clic : le bouton
// est relâché à côté et le clic est perdu. Pendant un appui (souris ou doigt),
// l'erreur n'est donc affichée qu'une fois le clic terminé.
let appuiEnCours = false
if (typeof window !== 'undefined') {
  window.addEventListener('pointerdown', () => { appuiEnCours = true }, true)
  window.addEventListener('pointercancel', () => { appuiEnCours = false }, true)
  window.addEventListener('keydown', () => { appuiEnCours = false }, true)
}

const apresLeClic = (action) => {
  if (!appuiEnCours) return action()
  let fait = false
  const lancer = () => {
    if (fait) return
    fait = true
    appuiEnCours = false
    window.removeEventListener('click', surClic, true)
    clearTimeout(minuteur)
    action()
  }
  const surClic = () => setTimeout(lancer, 0)
  window.addEventListener('click', surClic, true)
  const minuteur = setTimeout(lancer, 800)
}

// Validation rules
export const validationRules = {
  required: (value) => {
    if (typeof value === 'string') {
      return value.trim().length > 0 || 'Ce champ est requis'
    }
    return value !== null && value !== undefined || 'Ce champ est requis'
  },
  
  email: (value) => {
    if (!value) return true
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(value) || 'Format d\'email invalide'
  },
  
  minLength: (min) => (value) => {
    if (!value) return true
    return value.length >= min || `Minimum ${min} caractères requis`
  },
  
  maxLength: (max) => (value) => {
    if (!value) return true
    return value.length <= max || `Maximum ${max} caractères autorisés`
  },
  
  password: (value) => {
    if (!value) return true
    const hasUpperCase = /[A-Z]/.test(value)
    const hasLowerCase = /[a-z]/.test(value)
    const hasNumbers = /\d/.test(value)
    const hasMinLength = value.length >= 8
    
    if (!hasMinLength) return 'Le mot de passe doit contenir au moins 8 caractères'
    if (!hasUpperCase) return 'Le mot de passe doit contenir au moins une majuscule'
    if (!hasLowerCase) return 'Le mot de passe doit contenir au moins une minuscule'
    if (!hasNumbers) return 'Le mot de passe doit contenir au moins un chiffre'
    
    return true
  },
  
  confirmPassword: (password) => (confirmPassword) => {
    if (!confirmPassword) return 'Veuillez confirmer votre mot de passe'
    return password === confirmPassword || 'Les mots de passe ne correspondent pas'
  }
}

export function useFormValidation(initialData = {}, validationSchema = {}) {
  // State
  const formData = reactive({ ...initialData }) //formData = {firstName: '', lastName: '', email: '', password: '', confirmPassword: '', acceptTerms: false, newsletter: false}
  const errors = reactive({})
  const touched = reactive({})
  const isSubmitting = ref(false)

  // Computed
  const isValid = computed(() => {
    return Object.keys(errors).length === 0 || 
           Object.values(errors).every(error => !error)
  })

  const hasErrors = computed(() => {
    return Object.values(errors).some(error => error)
  })

  // Methods
  const validateField = (fieldName, value) => {
    const rules = validationSchema[fieldName]
    if (!rules) return true

    for (const rule of rules) {
      const result = rule(value, undefined, formData)
      if (result !== true) {
        errors[fieldName] = result
        return false
      }
    }

    delete errors[fieldName]
    return true
  }

  const validateForm = () => {
    let isValid = true
    
    Object.keys(validationSchema).forEach(fieldName => {
      const fieldValid = validateField(fieldName, formData[fieldName])
      if (!fieldValid) {
        isValid = false
      }
    })

    return isValid
  }

  const setFieldValue = (fieldName, value) => {
    formData[fieldName] = value
    if (touched[fieldName]) {
      validateField(fieldName, value)
    }
  }

  const setFieldTouched = (fieldName) => {
    apresLeClic(() => {
      touched[fieldName] = true
      validateField(fieldName, formData[fieldName])
    })
  }

  // Un champ déjà vérifié l'est de nouveau à chaque frappe : l'erreur disparaît
  // dès qu'elle est corrigée (et le bouton d'envoi redevient actif aussitôt).
  watch(formData, () => {
    Object.keys(touched).forEach(fieldName => {
      if (touched[fieldName]) validateField(fieldName, formData[fieldName])
    })
  }, { deep: true })

  const resetForm = () => {
    Object.keys(formData).forEach(key => {
      formData[key] = initialData[key] || ''
    })
    Object.keys(errors).forEach(key => {
      delete errors[key]
    })
    Object.keys(touched).forEach(key => {
      delete touched[key]
    })
    isSubmitting.value = false
  }

  const setErrors = (newErrors) => {
    Object.assign(errors, newErrors)
  }

  const getFieldError = (fieldName) => {
    return errors[fieldName] || ''
  }

  const isFieldTouched = (fieldName) => {
    return touched[fieldName] || false
  }

  const handleSubmit = async (submitFunction) => {
    if (isSubmitting.value) return

    // Mark all fields as touched
    Object.keys(validationSchema).forEach(fieldName => {
      touched[fieldName] = true
    })

    // Validate form
    if (!validateForm()) {
      return false
    }

    isSubmitting.value = true

    try {
      await submitFunction(formData)
      return true
    } catch (error) {
      console.error('Form submission error:', error)
      return false
    } finally {
      isSubmitting.value = false
    }
  }//handleSubmit = 

  return {
    // State
    formData,
    errors,
    touched,
    isSubmitting,
    
    // Computed
    isValid,
    hasErrors,
    
    // Methods
    validateField,
    validateForm,
    setFieldValue,
    setFieldTouched,
    resetForm,
    setErrors,
    getFieldError,
    isFieldTouched,
    handleSubmit
  }
} 