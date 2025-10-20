/**
 * Store Pinia pour la gestion des préférences utilisateur
 */
import { defineStore } from 'pinia'

export const usePreferencesStore = defineStore('preferences', {
  state: () => ({
    // Préférences pays/niveau
    paysNiveauPreferences: null,
    
    // Autres préférences
    themePreference: 'auto',
    languagePreference: 'fr',
    
    // Métadonnées
    lastUpdate: null,
  }),

  getters: {
    /**
     * Vérifie si l'utilisateur a des préférences pays/niveau sauvegardées
     */
    hasPaysNiveauPreferences: (state) => {
      return !!(state.paysNiveauPreferences?.pays_id && state.paysNiveauPreferences?.niveau_id)
    },

    /**
     * Retourne les préférences pays/niveau formatées
     */
    formattedPaysNiveauPreferences: (state) => {
      if (!state.paysNiveauPreferences) return null
      
      return {
        paysId: state.paysNiveauPreferences.pays_id,
        paysNom: state.paysNiveauPreferences.pays_nom,
        niveauId: state.paysNiveauPreferences.niveau_id,
        niveauNom: state.paysNiveauPreferences.niveau_nom,
        dateSelection: state.paysNiveauPreferences.date_selection
      }
    }
  },

  actions: {
    /**
     * Sauvegarde les préférences pays/niveau
     */
    async setPaysNiveauPreferences(preferences) {
      this.paysNiveauPreferences = {
        ...preferences,
        date_selection: preferences.date_selection || new Date().toISOString()
      }
      this.lastUpdate = new Date().toISOString()
      
      // Sauvegarder dans localStorage pour persistance
      try {
        localStorage.setItem('preferences_pays_niveau', JSON.stringify(this.paysNiveauPreferences))
      } catch (error) {
        console.warn('Impossible de sauvegarder dans localStorage:', error)
      }
    },

    /**
     * Charge les préférences depuis localStorage
     */
    loadPreferencesFromStorage() {
      try {
        const stored = localStorage.getItem('preferences_pays_niveau')
        if (stored) {
          this.paysNiveauPreferences = JSON.parse(stored)
        }
      } catch (error) {
        console.warn('Impossible de charger les préférences depuis localStorage:', error)
      }
    },

    /**
     * Efface les préférences pays/niveau
     */
    clearPaysNiveauPreferences() {
      this.paysNiveauPreferences = null
      localStorage.removeItem('preferences_pays_niveau')
    },

    /**
     * Met à jour les préférences de thème
     */
    setThemePreference(theme) {
      this.themePreference = theme
      localStorage.setItem('theme_preference', theme)
    },

    /**
     * Met à jour les préférences de langue
     */
    setLanguagePreference(language) {
      this.languagePreference = language
      localStorage.setItem('language_preference', language)
    },

    /**
     * Initialise les préférences au démarrage
     */
    initializePreferences() {
      // Charger les préférences pays/niveau
      this.loadPreferencesFromStorage()
      
      // Charger les autres préférences
      const theme = localStorage.getItem('theme_preference')
      if (theme) this.themePreference = theme
      
      const language = localStorage.getItem('language_preference')
      if (language) this.languagePreference = language
    }
  }
})
