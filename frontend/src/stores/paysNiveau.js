/**
 * Store Pinia pour la gestion du système Pays-Niveau
 */
import { defineStore } from 'pinia'
import apiClient from '@/api/client'

export const usePaysNiveauStore = defineStore('paysNiveau', {
  state: () => ({
    // État des sélections actives
    paysActuel: null,
    niveauPaysActuel: null,
    
    // Cache des données
    paysDisponibles: [],
    niveauxPaysDisponibles: [],
    
    // État de chargement
    isLoading: false,
    error: null,
    
    // Métadonnées
    lastUpdate: null,
    cacheExpiry: 5 * 60 * 1000, // 5 minutes
  }),

  getters: {
    /**
     * Vérifie si une sélection complète est active
     */
    hasActiveSelection: (state) => {
      return !!(state.paysActuel && state.niveauPaysActuel)
    },

    /**
     * Retourne l'affichage formaté de la sélection
     */
    selectionDisplay: (state) => {
      if (!state.hasActiveSelection) return 'Aucune sélection'
      
      const pays = state.paysActuel.drapeau_emoji 
        ? `${state.paysActuel.drapeau_emoji} ${state.paysActuel.nom}`
        : state.paysActuel.nom
      
      const niveau = state.niveauPaysActuel.nom_local
      
      return `${pays} - ${niveau}`
    },

    /**
     * Code unique de la sélection (ex: "6eme-FR")
     */
    codeUniqueSelection: (state) => {
      if (!state.niveauPaysActuel) return null
      return state.niveauPaysActuel.code_unique || 
        `${state.niveauPaysActuel.niveau_nom?.toLowerCase().replace(/[èé]/g, 'e').replace(/\s+/g, '')}-${state.paysActuel?.code_iso}`
    },

    /**
     * Paramètres pour les appels API
     */
    apiParams: (state) => {
      if (!state.hasActiveSelection) return {}
      
      return {
        niveau_pays: state.niveauPaysActuel.id,
        pays: state.paysActuel.id,
        niveau: state.niveauPaysActuel.niveau_pays?.id
      }
    },

    /**
     * Vérifie si le cache est valide
     */
    isCacheValid: (state) => {
      if (!state.lastUpdate) return false
      return (Date.now() - state.lastUpdate) < state.cacheExpiry
    },

    /**
     * Niveaux disponibles pour le pays actuel
     */
    niveauxPourPaysActuel: (state) => {
      if (!state.paysActuel) return []
      return state.niveauxPaysDisponibles.filter(np => 
        np.pays_id === state.paysActuel.id || np.pays?.id === state.paysActuel.id
      ).sort((a, b) => a.ordre_local - b.ordre_local)
    }
  },

  actions: {
    /**
     * Charge la liste des pays disponibles
     */
    async loadPaysDisponibles(forceRefresh = false) {
      if (!forceRefresh && this.paysDisponibles.length > 0 && this.isCacheValid) {
        return this.paysDisponibles
      }

      this.isLoading = true
      this.error = null

      try {
        const response = await apiClient.get('/api/pays/')
        this.paysDisponibles = response.data.results || response.data
        this.lastUpdate = Date.now()
        
        console.log('🌍 Pays chargés:', this.paysDisponibles.length)
        return this.paysDisponibles
      } catch (error) {
        this.error = 'Erreur lors du chargement des pays'
        console.error('Erreur chargement pays:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },

    /**
     * Charge les niveaux pour un pays donné
     */
    async loadNiveauxPourPays(paysId, forceRefresh = false) {
      if (!paysId) {
        this.niveauxPaysDisponibles = []
        return []
      }

      this.isLoading = true
      this.error = null

      try {
        const response = await apiClient.get(`/api/pays/${paysId}/niveaux/`)
        const niveaux = response.data.results || response.data
        
        // Mettre à jour le cache pour ce pays
        this.niveauxPaysDisponibles = this.niveauxPaysDisponibles.filter(np => 
          np.pays_id !== paysId && np.pays?.id !== paysId
        )
        this.niveauxPaysDisponibles.push(...niveaux)
        
        console.log('🎓 Niveaux chargés pour pays', paysId, ':', niveaux.length)
        return niveaux
      } catch (error) {
        this.error = 'Erreur lors du chargement des niveaux pour ce pays'
        console.error('Erreur chargement niveaux pour pays:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },

    /**
     * Charge toutes les associations niveau-pays
     */
    async loadTousNiveauxPays(forceRefresh = false) {
      if (!forceRefresh && this.niveauxPaysDisponibles.length > 0 && this.isCacheValid) {
        return this.niveauxPaysDisponibles
      }

      this.isLoading = true
      this.error = null

      try {
        const response = await apiClient.get('/api/niveaux-pays/')
        this.niveauxPaysDisponibles = response.data.results || response.data
        this.lastUpdate = Date.now()
        
        console.log('🔗 Toutes associations niveau-pays chargées:', this.niveauxPaysDisponibles.length)
        return this.niveauxPaysDisponibles
      } catch (error) {
        this.error = 'Erreur lors du chargement des associations niveau-pays'
        console.error('Erreur chargement niveau-pays:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },

    /**
     * Définit le pays actuel
     */
    async setPays(pays) {
      if (typeof pays === 'string' || typeof pays === 'number') {
        const paysObj = this.paysDisponibles.find(p => p.id == pays)
        if (!paysObj) {
          await this.loadPaysDisponibles()
          this.paysActuel = this.paysDisponibles.find(p => p.id == pays) || null
        } else {
          this.paysActuel = paysObj
        }
      } else {
        this.paysActuel = pays
      }

      this.niveauPaysActuel = null

      if (this.paysActuel) {
        await this.loadNiveauxPourPays(this.paysActuel.id)
      }

      console.log('🌍 Pays défini:', this.paysActuel?.nom)
    },

    /**
     * Définit le niveau-pays actuel
     */
    setNiveauPays(niveauPays) {
      if (typeof niveauPays === 'string' || typeof niveauPays === 'number') {
        this.niveauPaysActuel = this.niveauxPaysDisponibles.find(np => np.id == niveauPays) || null
      } else {
        this.niveauPaysActuel = niveauPays
      }

      console.log('🎓 Niveau-pays défini:', this.niveauPaysActuel?.nom_local)
    },

    /**
     * Définit la sélection complète (pays + niveau-pays)
     */
    async setSelection(paysId, niveauPaysId) {
      await this.setPays(paysId)
      this.setNiveauPays(niveauPaysId)
    },

    /**
     * Réinitialise la sélection
     */
    async clearSelection() {
      this.paysActuel = null
      this.niveauPaysActuel = null
      this.error = null
      
      console.log('🧹 Sélection réinitialisée')
    },

    /**
     * Charge le contenu pour la sélection actuelle
     */
    async loadContenuPourSelection(type = 'matieres') {
      if (!this.hasActiveSelection) {
        throw new Error('Aucune sélection active')
      }

      this.isLoading = true
      this.error = null

      try {
        const params = this.apiParams
        const response = await apiClient.get(`/api/${type}/`, { params })
        
        console.log(`📚 ${type} chargé(s) pour la sélection:`, response.data.length || response.data.results?.length)
        return response.data.results || response.data
      } catch (error) {
        this.error = `Erreur lors du chargement du contenu ${type}`
        console.error(`Erreur chargement ${type}:`, error)
        throw error
      } finally {
        this.isLoading = false
      }
    },

    /**
     * Recherche dans le contenu
     */
    async rechercherContenu(terme, typeContenu = null) {
      if (!terme || terme.length < 2) {
        throw new Error('Terme de recherche trop court')
      }

      this.isLoading = true
      this.error = null

      try {
        const params = {
          q: terme,
          ...(this.hasActiveSelection ? this.apiParams : {})
        }

        const response = await apiClient.get('/api/recherche/', { params })
        
        console.log('🔍 Recherche effectuée:', terme, '→', response.data.total, 'résultats')
        return response.data
      } catch (error) {
        this.error = 'Erreur lors de la recherche'
        console.error('Erreur recherche:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },

    /**
     * Obtient les statistiques pour la sélection actuelle
     */
    async getStatistiques() {
      if (!this.hasActiveSelection) {
        throw new Error('Aucune sélection active')
      }

      try {
        const response = await apiClient.get(`/api/niveaux-pays/${this.niveauPaysActuel.id}/contenu/`)
        return response.data.statistiques
      } catch (error) {
        console.error('Erreur chargement statistiques:', error)
        throw error
      }
    },

    /**
     * Sauvegarde la sélection dans le localStorage
     */
    saveSelectionToStorage() {
      if (this.hasActiveSelection) {
        const selection = {
          pays: this.paysActuel,
          niveauPays: this.niveauPaysActuel,
          timestamp: Date.now()
        }
        localStorage.setItem('pays_niveau_selection', JSON.stringify(selection))
      } else {
        localStorage.removeItem('pays_niveau_selection')
      }
    },

    /**
     * Restaure la sélection depuis le localStorage
     */
    async loadSelectionFromStorage() {
      try {
        const saved = localStorage.getItem('pays_niveau_selection')
        if (saved) {
          const selection = JSON.parse(saved)
          
          // Vérifier que la sélection n'est pas trop ancienne (24h)
          const maxAge = 24 * 60 * 60 * 1000
          if (Date.now() - selection.timestamp < maxAge) {
            this.paysActuel = selection.pays
            this.niveauPaysActuel = selection.niveauPays
            
            console.log('📂 Sélection restaurée:', this.selectionDisplay)
            return true
          }
        }
      } catch (error) {
        console.error('Erreur restauration sélection:', error)
      }
      
      return false
    },

    /**
     * Vide le cache
     */
    clearCache() {
      this.paysDisponibles = []
      this.niveauxPaysDisponibles = []
      this.lastUpdate = null
      
      console.log('🗑️ Cache vidé')
    }
  }
})
