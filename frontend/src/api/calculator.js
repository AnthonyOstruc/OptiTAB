import apiClient from './client'

// Fonctions de calcul mathématique
export const deriveExpr = (payload) => apiClient.post('/api/calc/derive/', payload)

// Fonction pour calculer l'intégrale
export const integrateExpr = (payload) => apiClient.post('/api/calc/integrate/', payload)

export const expandExpr = (payload) => apiClient.post('/api/calc/expand/', payload)

// Fonction pour factoriser une expression
export const factorExpr = (payload) => apiClient.post('/api/calc/factor/', payload)

// Fonction pour calculer une limite
export const limitExpr = (payload) => apiClient.post('/api/calc/limit/', payload) 