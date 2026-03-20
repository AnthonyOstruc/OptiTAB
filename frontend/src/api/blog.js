/**
 * API Blog — Appels API pour le blog OptiTAB
 */
import apiClient from './client'

const BASE = '/api/blog'

// ── Public ────────────────────────────────────────────────────────

export function getBlogPosts(params = {}) {
  return apiClient.get(`${BASE}/posts/`, { params })
}

export function getBlogPost(slug) {
  return apiClient.get(`${BASE}/posts/${slug}/`)
}

export function getBlogCategories() {
  return apiClient.get(`${BASE}/categories/`)
}

export function getBlogCategoryDetail(slug) {
  return apiClient.get(`${BASE}/categories/${slug}/`)
}

export function getBlogTags() {
  return apiClient.get(`${BASE}/tags/`)
}

export function getBlogTagDetail(slug) {
  return apiClient.get(`${BASE}/tags/${slug}/`)
}

export function getBlogSitemap() {
  return apiClient.get(`${BASE}/sitemap/`)
}

// ── Admin CRUD — Articles ─────────────────────────────────────────

export function getAdminBlogPosts() {
  return apiClient.get(`${BASE}/admin/posts/`)
}

export function createBlogPost(data) {
  const config = data instanceof FormData ? { headers: { 'Content-Type': 'multipart/form-data' } } : {}
  return apiClient.post(`${BASE}/admin/posts/create/`, data, config)
}

export function updateBlogPost(id, data) {
  const config = data instanceof FormData ? { headers: { 'Content-Type': 'multipart/form-data' } } : {}
  return apiClient.patch(`${BASE}/admin/posts/${id}/`, data, config)
}

export function deleteBlogPost(id) {
  return apiClient.delete(`${BASE}/admin/posts/${id}/delete/`)
}

// ── Admin CRUD — Catégories ───────────────────────────────────────

export function getAdminBlogCategories() {
  return apiClient.get(`${BASE}/admin/categories/`)
}

export function createBlogCategory(data) {
  return apiClient.post(`${BASE}/admin/categories/create/`, data)
}

export function updateBlogCategory(id, data) {
  return apiClient.patch(`${BASE}/admin/categories/${id}/`, data)
}

export function deleteBlogCategory(id) {
  return apiClient.delete(`${BASE}/admin/categories/${id}/delete/`)
}

// ── Admin CRUD — Tags ─────────────────────────────────────────────

export function getAdminBlogTags() {
  return apiClient.get(`${BASE}/admin/tags/`)
}

export function createBlogTag(data) {
  return apiClient.post(`${BASE}/admin/tags/create/`, data)
}

export function updateBlogTag(id, data) {
  return apiClient.patch(`${BASE}/admin/tags/${id}/`, data)
}

export function deleteBlogTag(id) {
  return apiClient.delete(`${BASE}/admin/tags/${id}/delete/`)
}
