import apiClient from './client'

export const getPlans = () => apiClient.get('/api/subscriptions/plans/')

export const createCheckoutSession = (priceId, extraPayload = {}) =>
  apiClient.post('/api/subscriptions/create-checkout-session/', {
    ...extraPayload,
    price_id: priceId
  })

export const createGuestCheckoutSession = (priceId, extraPayload = {}) =>
  apiClient.post('/api/subscriptions/guest-checkout-session/', {
    ...extraPayload,
    price_id: priceId
  })

export const getSubscriptionStatus = () =>
  apiClient.get('/api/subscriptions/status/')

export const finalizeCheckoutSession = (sessionId) =>
  apiClient.get('/api/subscriptions/checkout-session/status/', {
    params: { session_id: sessionId }
  })

export const finalizeGuestCheckoutSession = (sessionId) =>
  apiClient.get('/api/subscriptions/guest-checkout/status/', {
    params: { session_id: sessionId }
  })

export const cancelSubscription = (identifier = null) => {
  if (identifier && typeof identifier === 'object') {
    return apiClient.post('/api/subscriptions/cancel/', identifier)
  }
  if (identifier && typeof identifier === 'string' && identifier.startsWith('sub_')) {
    return apiClient.post('/api/subscriptions/cancel/', { stripe_subscription_id: identifier })
  }
  if (identifier) {
    return apiClient.post('/api/subscriptions/cancel/', { subscription_id: identifier })
  }
  return apiClient.post('/api/subscriptions/cancel/', {})
}

export const reactivateSubscription = (identifier = null) => {
  if (identifier && typeof identifier === 'object') {
    return apiClient.post('/api/subscriptions/reactivate/', identifier)
  }
  if (identifier && typeof identifier === 'string' && identifier.startsWith('sub_')) {
    return apiClient.post('/api/subscriptions/reactivate/', { stripe_subscription_id: identifier })
  }
  if (identifier) {
    return apiClient.post('/api/subscriptions/reactivate/', { subscription_id: identifier })
  }
  return apiClient.post('/api/subscriptions/reactivate/', {})
}

export const getInvoices = (params = {}) =>
  apiClient.get('/api/subscriptions/invoices/', { params })

export const emailInvoice = (invoiceId) =>
  apiClient.post(`/api/subscriptions/invoices/${invoiceId}/email/`)

// Admin endpoints
export const adminListPlans = () => apiClient.get('/api/subscriptions/admin/plans/')
export const adminCreatePlan = (payload) => apiClient.post('/api/subscriptions/admin/plans/', payload)
export const adminUpdatePlan = (id, payload) => apiClient.patch(`/api/subscriptions/admin/plans/${id}/`, payload)
export const adminDeletePlan = (id) => apiClient.delete(`/api/subscriptions/admin/plans/${id}/`)
export const adminListPasses = (params = {}) => apiClient.get('/api/subscriptions/admin/passes/', { params })
export const adminUpdatePass = (id, payload) => apiClient.patch(`/api/subscriptions/admin/passes/${id}/`, payload)
export const adminListSubscribers = (params = {}) => apiClient.get('/api/subscriptions/admin/subscribers/', { params })
export const adminChangeSubscriberPlan = (payload) => apiClient.post('/api/subscriptions/admin/subscribers/change-plan/', payload)
export const adminCancelSubscriberSubscription = (payload) => apiClient.post('/api/subscriptions/admin/subscribers/cancel/', payload)
export const adminSyncFromStripe = () => apiClient.post('/api/subscriptions/admin/sync-from-stripe/')
