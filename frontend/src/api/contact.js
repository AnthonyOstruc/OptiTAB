import apiClient from './client'

/**
 * Envoie un message du formulaire de contact au backend
 */
export async function sendContactMessage({ firstName, lastName, email, subject, message }) {
  const payload = { firstName, lastName, email, subject, message }
  const { data } = await apiClient.post('/api/contact/send/', payload)
  return data
}

export default {
  sendContactMessage,
}

