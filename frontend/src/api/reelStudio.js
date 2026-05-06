import apiClient from './client'

const BASE = '/api/admin/reel-studio'

export function listReelVoices(params = {}) {
  return apiClient.get(`${BASE}/voices/`, { params })
}

export function listReelVoiceLibrary(params = {}) {
  return apiClient.get(`${BASE}/voices/library/`, { params })
}

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

export function saveReelTemplate(id, data) {
  return apiClient.post(`${BASE}/projects/${id}/save-template/`, data)
}

export function generateReelSpeech(id, data = {}) {
  return apiClient.post(`${BASE}/projects/${id}/generate-speech/`, data, { timeout: 120000 })
}

export function generateReelSlideSpeeches(id, data = {}) {
  return apiClient.post(`${BASE}/projects/${id}/generate-slide-speeches/`, data, { timeout: 240000 })
}

export function generateReelSlideSpeech(id, data = {}) {
  return apiClient.post(`${BASE}/slides/${id}/generate-speech/`, data, { timeout: 120000 })
}

export function exportReelVideo(id, data = {}) {
  return apiClient.post(`${BASE}/projects/${id}/export-video/`, data, { timeout: 900000 })
}

export function downloadReelVideo(id) {
  return apiClient.get(`${BASE}/projects/${id}/download-video/`, {
    responseType: 'blob',
    timeout: 120000,
    headers: {
      Accept: '*/*',
    },
  })
}

export function updateReelSlide(id, data) {
  return apiClient.patch(`${BASE}/slides/${id}/`, data)
}

export function deleteReelSlide(id) {
  return apiClient.delete(`${BASE}/slides/${id}/`)
}

export function testReelTTSVoice(data = {}) {
  return apiClient.post(`${BASE}/test-voice/`, data, {
    responseType: 'blob',
    timeout: 60000,
    headers: { Accept: '*/*' },
  })
}
