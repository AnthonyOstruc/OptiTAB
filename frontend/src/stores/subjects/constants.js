/**
 * Constantes et configuration pour le store Subjects
 * Centralise toutes les valeurs de configuration pour faciliter la maintenance
 */

/** Clés localStorage pour la persistance des données */
export const STORAGE_KEYS = {
  SELECTED_SUBJECT: 'selected-subject',
  SELECTED_MATIERES: 'selected-matieres-ids',
  FAVORITE_MATIERES: 'favorite-matieres-ids',
  ACTIVE_MATIERE: 'active-matiere-id'
}

/** Valeurs par défaut et limites */
export const DEFAULTS = {
  SUBJECT_ID: 'maths',
  MAX_SELECTED_MATIERES: 10,
  MAX_FAVORITE_MATIERES: 20
}

/** Messages d'erreur standardisés */
export const ERROR_MESSAGES = {
  INVALID_ID: 'ID de matière invalide',
  ALREADY_FAVORITE: 'Matière déjà dans les favoris',
  ALREADY_SELECTED: 'Matière déjà sélectionnée',
  LIMIT_REACHED: 'Limite atteinte',
  NETWORK_ERROR: 'Erreur de connexion réseau',
  BACKEND_UNAVAILABLE: 'Backend indisponible',
  AUTH_REQUIRED: 'Authentification requise'
}

/** Codes d'erreur HTTP */
export const HTTP_STATUS = {
  UNAUTHORIZED: 401,
  NOT_FOUND: 404,
  SERVER_ERROR: 500
}

/** Types d'opérations pour le logging */
export const OPERATION_TYPES = {
  ADD_FAVORITE: 'addFavoriteMatiere',
  REMOVE_FAVORITE: 'removeFavoriteMatiere',
  ADD_SELECTED: 'addMatiereId',
  REMOVE_SELECTED: 'removeMatiereId',
  SET_ACTIVE: 'setActiveMatiere',
  SYNC_BACKEND: 'syncWithBackend',
  LOAD_PREFERENCES: 'loadPreferencesFromServer'
} 