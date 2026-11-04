import apiClient from './client'

// Progression par chapitre (exercices du chapitre, faits, acquis, à revoir),
// dernier chapitre travaillé et derniers exercices « à revoir ».
export const getMyProgression = () => apiClient.get('/api/users/me/progression/')

// Même chose pour un enfant lié à un compte parent (lien accepté).
export const getChildProgression = (childId) => apiClient.get(`/api/users/children/${childId}/progression/`)

// Note d'un quiz de chapitre passé en entier : { notion, bonnes, total, parties }.
export const enregistrerNoteQuiz = (resultat) => apiClient.post('/api/users/me/quiz-resultats/', resultat)

export const getChildOverview =(childId) => apiClient.get(`/api/users/children/${childId}/overview/`)
