import apiClient from './client'

const BASE_URL = '/api/free/learning-resources/'

export const getFreeResources = async (params = {}) => {
  const response = await apiClient.get(BASE_URL, { params })
  return response.data
}

export const getFreeResource = async (slug) => {
  if (!slug) {
    throw new Error('Le slug est requis pour charger une ressource gratuite')
  }
  const response = await apiClient.get(`${BASE_URL}${slug}/`)
  return response.data
}

export default {
  getFreeResources,
  getFreeResource
}
