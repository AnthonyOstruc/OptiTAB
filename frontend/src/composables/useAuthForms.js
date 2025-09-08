import { useFormValidation, validationRules } from './useFormValidation'

// Form configurations
export const AUTH_FORM_CONFIGS = {
  LOGIN: {
    fields: {
      email: {
        type: 'email',
        label: 'Email',
        placeholder: 'votre@email.com',
        required: true,
        autocomplete: 'email',
        validation: [validationRules.required, validationRules.email]
      },
      password: {
        type: 'password',
        label: 'Mot de passe',
        placeholder: 'Votre mot de passe',
        required: true,
        autocomplete: 'current-password',
        validation: [validationRules.required, validationRules.minLength(6)]
      },
      rememberMe: {
        type: 'checkbox',
        label: 'Se souvenir de moi',
        required: false
      }
    },
    submitText: 'Se connecter',
    socialText: 'Continuer avec Google'
  },
  
  REGISTER: {
    fields: {
      firstName: {
        type: 'text',
        label: 'Prénom',
        placeholder: 'Votre prénom',
        required: true,
        autocomplete: 'given-name',
        validation: [validationRules.required, validationRules.minLength(2)]
      },
      lastName: {
        type: 'text',
        label: 'Nom',
        placeholder: 'Votre nom',
        required: true,
        autocomplete: 'family-name',
        validation: [validationRules.required, validationRules.minLength(2)]
      },
      email: {
        type: 'email',
        label: 'Email',
        placeholder: 'votre@email.com',
        required: true,
        autocomplete: 'email',
        validation: [validationRules.required, validationRules.email]
      },
      password: {
        type: 'password',
        label: 'Mot de passe',
        placeholder: 'Créez un mot de passe',
        required: true,
        autocomplete: 'new-password',
        validation: [validationRules.required, validationRules.password]
      },
      confirmPassword: {
        type: 'password',
        label: 'Confirmer le mot de passe',
        placeholder: 'Confirmez votre mot de passe',
        required: true,
        autocomplete: 'new-password',
        validation: [validationRules.required]
      },
      acceptTerms: {
        type: 'checkbox',
        label: 'J\'accepte les conditions d\'utilisation',
        required: true,
        validation: [(value) => value === true || 'Vous devez accepter les conditions d\'utilisation']
      },
      newsletter: {
        type: 'checkbox',
        label: 'Je souhaite recevoir les actualités et offres d\'OptiTAB',
        required: false
      }
    },
    submitText: 'Créer mon compte',
    socialText: 'Continuer avec Google'
  },
  
  FORGOT_PASSWORD: {
    fields: {
      email: {
        type: 'email',
        label: 'Email',
        placeholder: 'votre@email.com',
        required: true,
        autocomplete: 'email',
        validation: [validationRules.required, validationRules.email]
      }
    },
    submitText: 'Envoyer le lien de réinitialisation',
    socialText: 'Continuer avec Google'
  }
}

export function useAuthForm(formType) {  // formType = 'REGISTER' exemple
  const config = AUTH_FORM_CONFIGS[formType]  // config = AUTH_FORM_CONFIGS['REGISTER']
  
  if (!config) {
    throw new Error(`Unknown form type: ${formType}`)
  }

  // Initialize form data with default values
  const initialData = Object.keys(config.fields).reduce((acc, fieldName) => { //config.fields = 'firstName', 'lastName', 'email', 'password', 'confirmPassword', 'acceptTerms', 'newsletter'
    const field = config.fields[fieldName] // field = {type: 'text', label: 'Prénom', placeholder: 'Votre prénom', required: true, autocomplete: 'given-name', validation: [validationRules.required, validationRules.minLength(2)]}
    acc[fieldName] = field.type === 'checkbox' ? false : '' // acc = {firstName: '', lastName: '', email: '', password: '', confirmPassword: '', acceptTerms: false, newsletter: false}
    return acc
  }, {})//initialData = {firstName: '', lastName: '', email: '', password: '', confirmPassword: '', acceptTerms: false, newsletter: false}

  // Build validation schema
  const validationSchema = Object.keys(config.fields).reduce((acc, fieldName) => { //config.fields = 'firstName', 'lastName', 'email', 'password', 'confirmPassword', 'acceptTerms', 'newsletter'
    const field = config.fields[fieldName]
    if (field.validation) {
      acc[fieldName] = field.validation 
    }
    return acc
  }, {})//validationSchema = {firstName: [validationRules.required, validationRules.minLength(2)], lastName: [validationRules.required, validationRules.minLength(2)], email: [validationRules.required, validationRules.email], password: [validationRules.required, validationRules.password], confirmPassword: [validationRules.required], acceptTerms: [(value) => value === true || 'Vous devez accepter les conditions d\'utilisation'], newsletter: false}

  // Add password confirmation validation for register form
  if (formType === 'REGISTER') { //formType = 'REGISTER'
    validationSchema.confirmPassword.push(
      (value, _all, formData) => validationRules.confirmPassword(formData.password)(value)
    )
  }

  const {
    formData,//formData = {firstName: 'Anthony', lastName: 'TABET', email: 'a@gmail.com', password: '', confirmPassword: '', acceptTerms: false, newsletter: false}  
    errors,//errors = {firstName: '', lastName: '', email: '', password: '', confirmPassword: '', acceptTerms: false, newsletter: false}
    touched,//touched = {firstName: false, lastName: false, email: false, password: false, confirmPassword: false, acceptTerms: false, newsletter: false}
    isSubmitting,//isSubmitting = false
    isValid,
    getFieldError,
    setFieldTouched,
    handleSubmit,
    resetForm
  } = useFormValidation(initialData, validationSchema)//useFormValidation = (initialData, validationSchema)

  // Form submission handler
  const submitForm = async (onSuccess, onError) => {
    const success = await handleSubmit(async (data) => {
      try {
        await onSuccess(data)
        return true
      } catch (error) {
        onError?.(error)
        return false
      }
    })

    return success
  }

  // Field configuration getter
  const getFieldConfig = (fieldName) => {
    return config.fields[fieldName] || null
  }

  // Get all field names
  const getFieldNames = () => {
    return Object.keys(config.fields)
  }

  // Check if field is required
  const isFieldRequired = (fieldName) => {
    return config.fields[fieldName]?.required || false
  }

  // Get field type
  const getFieldType = (fieldName) => {
    return config.fields[fieldName]?.type || 'text'
  }

  return {
    // Configuration
    config,
    
    // Form state
    formData,
    errors,
    touched,
    isSubmitting,
    isValid,
    
    // Methods
    getFieldError,
    setFieldTouched,
    submitForm,
    resetForm,
    getFieldConfig,
    getFieldNames,
    isFieldRequired,
    getFieldType
  }
} 