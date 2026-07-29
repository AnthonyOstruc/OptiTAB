/**
 * API Témoignages — captures WhatsApp / SMS affichées sur la page « lien en bio »
 *
 * Public : lecture seule des témoignages publiés.
 * Admin  : CRUD complet depuis le studio (/admin/temoignages).
 */
import apiClient from './client'

const PUBLIC_BASE = '/api/testimonials'
const ADMIN_BASE = '/api/admin/testimonials'

// Les captures peuvent peser quelques Mo : on laisse le temps à l'upload.
const UPLOAD_TIMEOUT = 120000

/**
 * Convertit un objet plat en FormData (obligatoire pour l'envoi de l'image).
 * Les booléens partent en 'true'/'false', format attendu par DRF.
 */
function toFormData(payload = {}) {
  const formData = new FormData()

  Object.entries(payload).forEach(([key, value]) => {
    if (value === undefined || value === null) return
    if (typeof value === 'boolean') {
      formData.append(key, value ? 'true' : 'false')
    } else {
      formData.append(key, value)
    }
  })

  return formData
}

// ── Public ────────────────────────────────────────────────────────

export function getPublishedTestimonials() {
  return apiClient.get(`${PUBLIC_BASE}/`)
}

// ── Admin ─────────────────────────────────────────────────────────

export function getAdminTestimonials() {
  return apiClient.get(`${ADMIN_BASE}/`)
}

export function createTestimonial(payload) {
  return apiClient.post(`${ADMIN_BASE}/create/`, toFormData(payload), {
    timeout: UPLOAD_TIMEOUT
  })
}

export function updateTestimonial(id, payload) {
  return apiClient.patch(`${ADMIN_BASE}/${id}/`, toFormData(payload), {
    timeout: UPLOAD_TIMEOUT
  })
}

export function deleteTestimonial(id) {
  return apiClient.delete(`${ADMIN_BASE}/${id}/`)
}

export function reorderTestimonials(orderedIds) {
  return apiClient.post(`${ADMIN_BASE}/reorder/`, { order: orderedIds })
}

// ── Mise en ligne de la page ──────────────────────────────────────

/** La page /avis est-elle ouverte au public ? Endpoint public. */
export function getBioLandingStatus() {
  return apiClient.get('/api/bio-landing/status/')
}

/** Met la page en ligne ou la retire. Réservé aux administrateurs. */
export function setBioLandingPublished(published) {
  return apiClient.patch('/api/admin/bio-landing/', { published: Boolean(published) })
}
