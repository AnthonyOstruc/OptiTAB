import { BaseAPI } from './base'
import apiClient from './client'

const contextes = new BaseAPI('/api/contextes/')

export const getContextes = (params = {}) => contextes.getAll(params)
export const getContexteDetail = (id) => contextes.getById(id)
export const createContexte = (data) => contextes.create(data)
export const updateContexte = (id, data) => contextes.update(id, data)
export const deleteContexte = (id) => contextes.delete(id)
export const getContextesPourUtilisateur = async () => {
  const { data } = await apiClient.get('/api/contextes/pour-utilisateur/')
  return data
}

export default {
  getContextes,
  getContexteDetail,
  createContexte,
  updateContexte,
  deleteContexte,
  getContextesPourUtilisateur
}


