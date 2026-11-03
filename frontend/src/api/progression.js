import apiClient from './client'

// Progression par chapitre (exercices du chapitre, faits, acquis, à revoir),
// dernier chapitre travaillé et derniers exercices « à revoir ».
export const getMyProgression = () => apiClient.get('/api/users/me/progression/')

// Même chose pour un enfant lié à un compte parent (lien accepté).
export const getChildProgression = (childId) => apiClient.get(`/api/users/children/${childId}/progression/`)

export const getChildOverview = (childId) => apiClient.get(`/api/users/children/${childId}/overview/`)
