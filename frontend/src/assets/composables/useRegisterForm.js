import { ref, reactive } from 'vue'

export function useRegisterForm() {
  const formData = reactive({
    firstName: '',
    lastName: '',
    phone: '',
    email: '',
    password: '',
    confirmPassword: '',
    acceptTerms: false,
    newsletter: false,
  })
  const touched = reactive({})
  const errors = reactive({})
  const isSubmitting = ref(false)

  function getFieldConfig(field) {
    // À adapter selon la config réelle
    const configs = {
      firstName: { label: 'Prénom', type: 'text', required: true, placeholder: 'Votre prénom' },
      lastName: { label: 'Nom', type: 'text', required: true, placeholder: 'Votre nom' },
      phone: { label: 'Numéro de téléphone', type: 'tel', required: true, placeholder: 'Votre numéro de téléphone' },
      email: { label: 'Email', type: 'email', required: true, placeholder: 'Votre email' },
      password: { label: 'Mot de passe', type: 'password', required: true, placeholder: 'Votre mot de passe' },
      confirmPassword: { label: 'Confirmation', type: 'password', required: true, placeholder: 'Confirmez le mot de passe' },
      acceptTerms: { label: "J'accepte les CGU", type: 'checkbox', required: true },
      newsletter: { label: 'Recevoir la newsletter', type: 'checkbox', required: false },
    }
    return configs[field]
  }
  function getFieldNames() {
    return ['firstName', 'lastName', 'phone', 'email', 'password', 'confirmPassword', 'acceptTerms', 'newsletter']
  }
  function getFieldError(field) {
    return errors[field] || ''
  }
  function setFieldTouched(field) {
    touched[field] = true
  }
  function validate() {
    errors.firstName = !formData.firstName ? 'Champ requis' : ''
    errors.lastName = !formData.lastName ? 'Champ requis' : ''
    errors.phone = !formData.phone ? 'Champ requis' : ''
    errors.email = !formData.email ? 'Champ requis' : ''
    errors.password = !formData.password ? 'Champ requis' : ''
    errors.confirmPassword = formData.confirmPassword !== formData.password ? 'Les mots de passe ne correspondent pas' : ''
    errors.acceptTerms = !formData.acceptTerms ? 'Obligatoire' : ''
    // ... autres règles
    return Object.values(errors).every(e => !e)
  }
  async function submitForm(onSuccess, onError) {
    isSubmitting.value = true
    const valid = validate()
    if (valid) {
      try {
        await onSuccess(formData)
      } catch (e) {
        onError && onError(e)
      }
    }
    isSubmitting.value = false
    return valid
  }
  return {
    formData,
    isSubmitting,
    isValid: () => validate(),
    getFieldError,
    setFieldTouched,
    submitForm,
    getFieldConfig,
    getFieldNames,
  }
} 