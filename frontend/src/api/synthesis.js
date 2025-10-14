import apiClient from './client'

// API pour les fiches de synthèse
export const getSynthesisSheets = (params = {}) => {
  return apiClient.get('/api/sheets/', { params })
}

export const getSynthesisSheet = (id) => {
  return apiClient.get(`/api/sheets/${id}/`)
}

export const createSynthesisSheet = (data) => {
  return apiClient.post('/api/sheets/', data)
}

export const updateSynthesisSheet = (id, data) => {
  return apiClient.put(`/api/sheets/${id}/`, data)
}

export const deleteSynthesisSheet = (id) => {
  return apiClient.delete(`/api/sheets/${id}/`)
}

export const duplicateSynthesisSheet = (id) => {
  return apiClient.post(`/api/sheets/${id}/duplicate/`)
}

// API pour les données de support (notions, matières, etc.) - filtrées par contexte utilisateur
export const getSynthesisNotions = (params = {}) => {
  return apiClient.get('/api/notions/pour-utilisateur/', { params })
}

export const getSynthesisMatieres = () => {
  return apiClient.get('/api/matieres/user_matieres/')
}

export const getPreviewData = (params) => {
  return apiClient.get('/api/sheets/preview_data/', { params })
}

// Upload d'image pour une fiche de synthèse
export const createSynthesisImage = ({ sheet, image, image_type = 'illustration', position, caption }) => {
  const formData = new FormData()
  formData.append('image', image)
  if (image_type) formData.append('image_type', image_type)
  if (position !== undefined && position !== null) formData.append('position', position)
  if (caption) formData.append('caption', caption)
  return apiClient.post(`/api/sheets/${sheet}/add_image/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

// Liste/CRUD des images d'une fiche
export const getSynthesisImages = (sheetId) => apiClient.get(`/api/sheet-images/?sheet=${sheetId}`)

export const updateSynthesisImage = (id, { image, image_type, position, caption } = {}) => {
  const formData = new FormData()
  if (image) formData.append('image', image)
  if (image_type) formData.append('image_type', image_type)
  if (position !== undefined && position !== null) formData.append('position', position)
  if (caption !== undefined) formData.append('caption', caption)
  return apiClient.patch(`/api/sheet-images/${id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export const deleteSynthesisImage = (id) => apiClient.delete(`/api/sheet-images/${id}/`)
