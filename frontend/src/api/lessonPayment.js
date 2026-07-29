/**
 * API Versements ponctuels — cours particuliers.
 *
 * Le professeur envoie le lien /paiement, la personne saisit le montant
 * convenu et règle par carte. Aucun compte requis.
 */
import apiClient from './client'

const BASE = '/api/subscriptions/lesson-payment'

/** Bornes de montant appliquées par le serveur (min, max, devise). */
export function getLessonPaymentConfig() {
  return apiClient.get(`${BASE}/config/`)
}

/**
 * Crée la session Stripe et renvoie l'URL de paiement.
 * @param {{ amount: string|number, label?: string, payer_name?: string }} payload
 */
export function createLessonPaymentSession(payload) {
  return apiClient.post(`${BASE}/create-session/`, payload)
}

/** État d'un versement, pour la page de confirmation. */
export function getLessonPaymentStatus(sessionId) {
  return apiClient.get(`${BASE}/status/`, { params: { session_id: sessionId } })
}
