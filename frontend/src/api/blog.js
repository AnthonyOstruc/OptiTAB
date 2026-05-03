/**
 * API Blog — Appels API pour le blog OptiTAB
 */
import apiClient from './client'

const BASE = '/api/blog'
const BLOG_UPLOAD_TIMEOUT = 120000

function formDataConfig(data) {
  return data instanceof FormData ? { timeout: BLOG_UPLOAD_TIMEOUT } : {}
}

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

export function getBlogNiveaux() {
  return apiClient.get(`${BASE}/niveaux/`)
}

export function getBlogContentTypes() {
  return apiClient.get(`${BASE}/types/`)
}

export function getBlogSitemap() {
  return apiClient.get(`${BASE}/sitemap/`)
}

// ── Admin CRUD — Articles ─────────────────────────────────────────

export function getAdminBlogPosts() {
  return apiClient.get(`${BASE}/admin/posts/`)
}

export function createBlogPost(data) {
  return apiClient.post(`${BASE}/admin/posts/create/`, data, formDataConfig(data))
}

export function updateBlogPost(id, data) {
  return apiClient.patch(`${BASE}/admin/posts/${id}/`, data, formDataConfig(data))
}

export function deleteBlogPost(id) {
  return apiClient.delete(`${BASE}/admin/posts/${id}/delete/`)
}

// ── Admin CRUD — Catégories ───────────────────────────────────────

export function getBlogPostImages(postId) {
  return apiClient.get(`${BASE}/admin/posts/${postId}/images/`)
}

export function createBlogPostImage(postId, data) {
  return apiClient.post(`${BASE}/admin/posts/${postId}/images/`, data, formDataConfig(data))
}

export function updateBlogPostImage(postId, imageId, data) {
  return apiClient.patch(`${BASE}/admin/posts/${postId}/images/${imageId}/`, data, formDataConfig(data))
}

export function deleteBlogPostImage(postId, imageId) {
  return apiClient.delete(`${BASE}/admin/posts/${postId}/images/${imageId}/`)
}

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

// —— Admin CRUD — Niveaux —————————————————————————————————————————————

export function getAdminBlogNiveaux() {
  return apiClient.get(`${BASE}/admin/niveaux/`)
}

export function createBlogNiveau(data) {
  return apiClient.post(`${BASE}/admin/niveaux/create/`, data)
}

export function updateBlogNiveau(id, data) {
  return apiClient.patch(`${BASE}/admin/niveaux/${id}/`, data)
}

export function deleteBlogNiveau(id) {
  return apiClient.delete(`${BASE}/admin/niveaux/${id}/delete/`)
}

// —— Admin CRUD — Types de contenu —————————————————————————————————————

export function getAdminBlogContentTypes() {
  return apiClient.get(`${BASE}/admin/types/`)
}

export function createBlogContentType(data) {
  return apiClient.post(`${BASE}/admin/types/create/`, data)
}

export function updateBlogContentType(id, data) {
  return apiClient.patch(`${BASE}/admin/types/${id}/`, data)
}

export function deleteBlogContentType(id) {
  return apiClient.delete(`${BASE}/admin/types/${id}/delete/`)
}
