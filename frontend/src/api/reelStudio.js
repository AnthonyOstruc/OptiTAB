import apiClient from './client'

const BASE = '/api/admin/reel-studio'

export function listReelProjects() {
  return apiClient.get(`${BASE}/projects/`)
}

export function createReelProject(data) {
  return apiClient.post(`${BASE}/projects/`, data)
}

export function getReelProject(id) {
  return apiClient.get(`${BASE}/projects/${id}/`)
}

export function updateReelProject(id, data) {
  return apiClient.patch(`${BASE}/projects/${id}/`, data)
}

export function deleteReelProject(id) {
  return apiClient.delete(`${BASE}/projects/${id}/`)
}

export function generateDemoSlides(id) {
  return apiClient.post(`${BASE}/projects/${id}/generate-demo-slides/`)
}

export function generateSlidesFromTemplate(id, data) {
  return apiClient.post(`${BASE}/projects/${id}/generate-from-template/`, data)
}

export function updateReelSlide(id, data) {
  return apiClient.patch(`${BASE}/slides/${id}/`, data)
}

export function deleteReelSlide(id) {
  return apiClient.delete(`${BASE}/slides/${id}/`)
}
