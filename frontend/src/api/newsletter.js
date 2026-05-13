import apiClient from './client'

// Abonne un email à la newsletter
export async function subscribeToNewsletter(email, firstName = '', lastName = '') {
  const payload = { email, firstName, lastName }
  const { data } = await apiClient.post('/api/newsletter/subscribe/', payload)
  return data
}

// Lead capture pour la landing diagnostic gratuit maths
// Le backend doit exposer POST /api/newsletter/diagnostic-lead/
// Champs attendus côté serveur :
//   firstName, email, level, difficulty, consentEmailMarketing,
//   consentTimestamp, leadMagnet, formLocation, context (utm, gclid, referrer, landing_path)
export async function submitDiagnosticLead(payload) {
  const { data } = await apiClient.post('/api/newsletter/diagnostic-lead/', payload)
  return data
}

export async function getNewsletterSubscribers(params = {}) {
  const { q = '', active = true, limit = 100, offset = 0 } = params
  const response = await apiClient.get('/api/newsletter/subscribers/', { params: { q, active, limit, offset } })
  // Backend enveloppe: { success, message, data: { total, items } }
  return response.data?.data || { total: 0, items: [] }
}

export async function broadcastNewsletter({ subject, text = '', html = '', limit = 0, onlyInactive = false, useTemplate = true }) {
  const payload = { subject, text, html, limit, onlyInactive, useTemplate }
  const { data } = await apiClient.post('/api/newsletter/broadcast/', payload)
  return data
}

export default {
  subscribeToNewsletter,
  submitDiagnosticLead,
  getNewsletterSubscribers,
  broadcastNewsletter,
}

