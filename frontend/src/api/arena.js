/**
 * Arena (math game) API client.
 * All endpoints are mounted under /api/arena/.
 */
import apiClient from './client'

// ----- Player API -----
export const getArenaConfig = () => apiClient.get('/api/arena/config/')
export const getArenaMe = () => apiClient.get('/api/arena/me/')
export const getArenaChapters = () => apiClient.get('/api/arena/chapters/')
export const getArenaChapter = (slug) => apiClient.get(`/api/arena/chapters/${slug}/`)
export const getArenaLevelPlay = (levelId) => apiClient.get(`/api/arena/levels/${levelId}/play/`)
export const submitArenaAttempt = (levelId, payload) =>
  apiClient.post(`/api/arena/levels/${levelId}/attempts/`, payload)
export const getArenaDaily = () => apiClient.get('/api/arena/daily/')
export const getArenaForge = () => apiClient.get('/api/arena/forge/')
export const getArenaHistory = () => apiClient.get('/api/arena/history/')
export const trackArenaEvent = (name, payload = {}) =>
  apiClient.post('/api/arena/events/', { name, payload })

// ----- Admin API -----
export const adminGetArenaConfig = () => apiClient.get('/api/arena/admin/config/')
export const adminUpdateArenaConfig = (payload) =>
  apiClient.patch('/api/arena/admin/config/', payload)
export const adminGetArenaAnalytics = () => apiClient.get('/api/arena/admin/analytics/')

export const adminListArenaChapters = () => apiClient.get('/api/arena/admin/chapters/')
export const adminCreateArenaChapter = (payload) =>
  apiClient.post('/api/arena/admin/chapters/', payload)
export const adminUpdateArenaChapter = (id, payload) =>
  apiClient.patch(`/api/arena/admin/chapters/${id}/`, payload)
export const adminDeleteArenaChapter = (id) =>
  apiClient.delete(`/api/arena/admin/chapters/${id}/`)

export const adminListArenaLevels = (chapterId) =>
  apiClient.get(`/api/arena/admin/levels/${chapterId ? `?chapter=${chapterId}` : ''}`)
export const adminCreateArenaLevel = (payload) =>
  apiClient.post('/api/arena/admin/levels/', payload)
export const adminUpdateArenaLevel = (id, payload) =>
  apiClient.patch(`/api/arena/admin/levels/${id}/`, payload)
export const adminDeleteArenaLevel = (id) =>
  apiClient.delete(`/api/arena/admin/levels/${id}/`)

export const adminListArenaQuestions = (levelId) =>
  apiClient.get(`/api/arena/admin/questions/${levelId ? `?level=${levelId}` : ''}`)
export const adminCreateArenaQuestion = (payload) =>
  apiClient.post('/api/arena/admin/questions/', payload)
export const adminUpdateArenaQuestion = (id, payload) =>
  apiClient.patch(`/api/arena/admin/questions/${id}/`, payload)
export const adminDeleteArenaQuestion = (id) =>
  apiClient.delete(`/api/arena/admin/questions/${id}/`)

export const adminListArenaDaily = () => apiClient.get('/api/arena/admin/daily/')
export const adminCreateArenaDaily = (payload) =>
  apiClient.post('/api/arena/admin/daily/', payload)
export const adminDeleteArenaDaily = (id) =>
  apiClient.delete(`/api/arena/admin/daily/${id}/`)
