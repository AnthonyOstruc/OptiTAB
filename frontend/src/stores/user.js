import { defineStore } from 'pinia'
import { fetchUserProfile } from '@/api'
import { calculateUserLevel } from '@/composables/useLevel'
import { apiUtils } from '@/api/client'

// Nettoyage automatique de l'ancienne clé 'user' du localStorage (sécurité)
localStorage.removeItem('user')

export const useUserStore = defineStore('user', {
  state: () => ({
    id: null,
    firstName: '',
    lastName: '',
    email: '',
    telephone: '',
    date_naissance: '',
    niveau_pays: null,
    pays: null,
    role: 'student',
    xp: 0,
    level: 0,
    xp_to_next: 0,
    isAdmin: false,
    isAuthenticated: false,
    isLoading: false
  }),
  actions: {
    // Met à jour l'utilisateur dans le store
    setUser(user) {
      this.id = user.id || user.user_id || null
      this.firstName = user.first_name || ''
      this.lastName = user.last_name || ''
      this.email = user.email || ''
      this.telephone = user.telephone || ''
      this.date_naissance = user.date_naissance || ''
      this.niveau_pays = user.niveau_pays || null
      this.pays = user.pays || null
      this.role = user.role || 'student'
      const xpVal = Number(user.xp ?? 0)
      const computed = calculateUserLevel(xpVal)
      this.xp = xpVal
      this.level = Number(computed.level)
      this.xp_to_next = Number(computed.xp_to_next)
      
      // Forcer l'état admin pour les utilisateurs avec certains emails
      const adminEmails = ['anthonytabet.c@gmail.com', 'admin@optitab.com']
      this.isAdmin = user.is_staff || user.isAdmin || adminEmails.includes(user.email) || false
      
      this.isAuthenticated = true
      this.isLoading = false
    },
    // Réinitialise l'utilisateur (déconnexion ou erreur)
    clearUser() {
      // Arrêter la surveillance des tokens avant de nettoyer
      apiUtils.stopTokenMonitoring()

      // Nettoyer les données utilisateur
      const userId = this.id
      this.id = null
      this.firstName = ''
      this.lastName = ''
      this.email = ''
      this.telephone = ''
      this.date_naissance = ''
      this.niveau_pays = null
      this.pays = null
      this.role = 'student'
      this.xp = 0
      this.level = 0
      this.xp_to_next = 0
      this.isAdmin = false
      this.isAuthenticated = false
      this.isLoading = false

      // Nettoyer le localStorage des données liées à cet utilisateur
      if (userId) {
        const userConfigKey = `configurationCompleted_${userId}`
        localStorage.removeItem(userConfigKey)
      }

      // Nettoyer aussi les autres clés génériques
      const keysToClean = [
        'selectedMatieres',
        'favoriteMatieresIds',
        'activeMatiereId',
        'selectedMatieresIds',
        'access_token',
        'refresh_token'
      ]
      keysToClean.forEach(key => localStorage.removeItem(key))
    },
    // Récupère l'utilisateur via l'API si le token est présent
    async fetchUser() {
      this.isLoading = true
      try {
        // Debug: Vérifier les tokens
        const accessToken = localStorage.getItem('access_token')
        const refreshToken = localStorage.getItem('refresh_token')
        console.log('🔍 Tokens disponibles:', { 
          hasAccess: !!accessToken, 
          hasRefresh: !!refreshToken,
          accessPreview: accessToken ? accessToken.substring(0, 20) + '...' : 'null'
        })
        
        const response = await fetchUserProfile()
        
        // Debug: Afficher la réponse complète
        console.log('📥 Réponse API fetchUserProfile:', response)
        console.log('📊 Données utilisateur reçues:', response.data)
        
        // Extraire les données utilisateur de la réponse
        // Le backend retourne { success: true, data: {...}, message: "..." }
        const userData = response.data?.data || response.data
        console.log('👤 Données utilisateur extraites:', userData)
        
        // Vérifier si l'utilisateur a des données cohérentes
        const hadPaysNiveau = this.pays && this.niveau_pays
        const nowHasPaysNiveau = userData.pays && userData.niveau_pays
        
        // Si l'utilisateur avait des données mais n'en a plus (suppression en BDD)
        if (hadPaysNiveau && !nowHasPaysNiveau && this.id) {
          const userConfigKey = `configurationCompleted_${this.id}`
          localStorage.removeItem(userConfigKey)
          
          // Nettoyer aussi les autres clés liées aux matières
          const keysToClean = [
            'selectedMatieres',
            'favoriteMatieresIds',
            'activeMatiereId',
            'selectedMatieresIds'
          ]
          keysToClean.forEach(key => localStorage.removeItem(key))
        }
        
        // Mettre à jour le store avec les nouvelles données
        this.setUser(userData)
        
        // Le streak sera géré au niveau de l'App entière, pas juste à la connexion
        
        // Redémarrer la surveillance des tokens après récupération réussie
        setTimeout(() => {
          console.log('🔄 Redémarrage de la surveillance des tokens après récupération utilisateur')
          apiUtils.startTokenMonitoring()
        }, 500)

        // Debug: Afficher l'état final du store
        console.log('🏪 État final du store utilisateur:', {
          id: this.id,
          firstName: this.firstName,
          lastName: this.lastName,
          email: this.email,
          pays: this.pays,
          niveau_pays: this.niveau_pays,
          isAuthenticated: this.isAuthenticated
        })
        
      } catch (e) {
        console.error('Erreur lors de la récupération du profil:', e)

        // Analyser l'erreur pour une meilleure gestion
        const errorStatus = e.response?.status
        const errorMessage = e.response?.data?.message || e.message

        if (errorStatus === 401) {
          console.warn('Token invalide ou expiré, déconnexion automatique')
          this.clearUser()
        } else if (errorStatus >= 500) {
          console.warn('Erreur serveur, tentative de reconnexion dans 5 secondes')
          // Pour les erreurs serveur, on peut essayer de nouveau après un délai
          setTimeout(() => {
            if (!this.isAuthenticated) {
              console.log('Nouvelle tentative de récupération du profil après erreur serveur')
              this.fetchUser()
            }
          }, 5000)
        } else {
          console.warn(`Erreur ${errorStatus}: ${errorMessage}`)
          // Pour les autres erreurs, on déconnecte aussi pour éviter les boucles
          this.clearUser()
        }
      } finally {
        this.isLoading = false
      }
    }
  }
}) 