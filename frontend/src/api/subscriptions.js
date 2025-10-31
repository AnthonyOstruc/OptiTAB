import apiClient from './client'

export const getPlans = () => apiClient.get('/api/subscriptions/plans/')

export const createCheckoutSession = (priceId) =>
  apiClient.post('/api/subscriptions/create-checkout-session/', { price_id: priceId })

export const getSubscriptionStatus = () =>
  apiClient.get('/api/subscriptions/status/')

export const cancelSubscription = () =>
  apiClient.post('/api/subscriptions/cancel/')

