<template>
  <div class="user-preferences-page">
    <div class="page-header">
      <h1>⚙️ Mes Préférences</h1>
      <p>Configurez votre profil et vos préférences d'apprentissage</p>
    </div>

    <div class="preferences-container">
      <!-- Section Localisation -->
      <div class="preference-section">
        <h2>🌍 Localisation et Système Éducatif</h2>
        <div class="section-grid">
          <PaysSelector />
          <NiveauSelector />
        </div>
      </div>

      <!-- Section Profil -->
      <div class="preference-section">
        <h2>👤 Informations Personnelles</h2>
        <div class="profile-form">
          <div class="form-row">
            <div class="form-group">
              <label for="first_name">Prénom</label>
              <input 
                id="first_name"
                v-model="profileData.first_name"
                type="text" 
                class="form-input"
                placeholder="Votre prénom"
              >
            </div>
            <div class="form-group">
              <label for="last_name">Nom</label>
              <input 
                id="last_name"
                v-model="profileData.last_name"
                type="text" 
                class="form-input"
                placeholder="Votre nom"
              >
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="civilite">Civilité</label>
              <select id="civilite" v-model="profileData.civilite" class="form-select">
                <option value="">Sélectionnez...</option>
                <option value="Monsieur">Monsieur</option>
                <option value="Madame">Madame</option>
                <option value="Autre">Autre</option>
              </select>
            </div>
            <div class="form-group">
              <label for="date_naissance">Date de naissance</label>
              <input 
                id="date_naissance"
                v-model="profileData.date_naissance"
                type="date" 
                class="form-input"
              >
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="telephone">Téléphone</label>
              <input 
                id="telephone"
                v-model="profileData.telephone"
                type="tel" 
                class="form-input"
                placeholder="Votre numéro de téléphone"
              >
            </div>
            <div class="form-group">
              <label for="email">Email</label>
              <input 
                id="email"
                :value="userStore.user?.email"
                type="email" 
                class="form-input"
                disabled
                title="L'email ne peut pas être modifié"
              >
            </div>
          </div>

          <div class="form-actions">
            <button 
              @click="saveProfile" 
              class="btn-primary"
              :disabled="savingProfile"
            >
              <span v-if="savingProfile">Enregistrement...</span>
              <span v-else>Enregistrer les modifications</span>
            </button>
            <button 
              @click="resetProfileForm" 
              class="btn-secondary"
              type="button"
            >
              Annuler
            </button>
          </div>
        </div>
      </div>

      <!-- Section Statistiques -->
      <div class="preference-section">
        <h2>📊 Votre Profil d'Apprentissage</h2>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">🏆</div>
            <div class="stat-info">
              <h3>Niveau Actuel</h3>
              <p>{{ userStore.user?.niveau_pays?.nom || 'Non défini' }}</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🌍</div>
            <div class="stat-info">
              <h3>Pays</h3>
              <p>{{ userStore.user?.pays?.nom || 'Non défini' }}</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">⏱️</div>
            <div class="stat-info">
              <h3>Membre depuis</h3>
              <p>{{ formatDate(userStore.user?.date_joined) }}</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📚</div>
            <div class="stat-info">
              <h3>Dernière connexion</h3>
              <p>{{ formatDate(userStore.user?.last_login) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToast } from '@/composables/useToast'
import PaysSelector from '@/components/user/PaysSelector.vue'
import NiveauSelector from '@/components/user/NiveauSelector.vue'
import { updateUserProfile } from '@/api/users.js'

export default {
  name: 'UserPreferences',
  components: {
    PaysSelector,
    NiveauSelector
  },
  setup() {
    const userStore = useUserStore()
    const { showToast } = useToast()
    
    const savingProfile = ref(false)
    const profileData = reactive({
      first_name: '',
      last_name: '',
      civilite: '',
      date_naissance: '',
      telephone: ''
    })

    const loadProfileData = () => {
      if (userStore.user) {
        profileData.first_name = userStore.user.first_name || ''
        profileData.last_name = userStore.user.last_name || ''
        profileData.civilite = userStore.user.civilite || ''
        profileData.date_naissance = userStore.user.date_naissance || ''
        profileData.telephone = userStore.user.telephone || ''
      }
    }

    const saveProfile = async () => {
      try {
        savingProfile.value = true
        await updateUserProfile(profileData)
        await userStore.fetchUser()
        showToast('Profil mis à jour avec succès', 'success')
      } catch (error) {
        console.error('Error updating profile:', error)
        showToast('Erreur lors de la mise à jour du profil', 'error')
      } finally {
        savingProfile.value = false
      }
    }

    const resetProfileForm = () => {
      loadProfileData()
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'Non disponible'
      
      try {
        const date = new Date(dateString)
        return date.toLocaleDateString('fr-FR', {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        })
      } catch {
        return 'Date invalide'
      }
    }

    onMounted(() => {
      loadProfileData()
    })

    return {
      userStore,
      savingProfile,
      profileData,
      saveProfile,
      resetProfileForm,
      formatDate
    }
  }
}
</script>

<style scoped>
.user-preferences-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-header h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
}

.page-header p {
  margin: 0;
  color: #6b7280;
  font-size: 1.125rem;
}

.preferences-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.preference-section {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.preference-section h2 {
  margin: 0 0 1.5rem 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.profile-form {
  max-width: 600px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

.form-input, .form-select {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-input:focus, .form-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input:disabled {
  background-color: #f9fafb;
  color: #6b7280;
  cursor: not-allowed;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-primary, .btn-secondary {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  font-size: 1rem;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: #e5e7eb;
  color: #374151;
}

.btn-secondary:hover {
  background: #d1d5db;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 2rem;
  width: 60px;
  height: 60px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-info h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.stat-info p {
  margin: 0;
  color: #6b7280;
  font-size: 0.875rem;
}

/* Responsive */
@media (max-width: 768px) {
  .user-preferences-page {
    padding: 1rem;
  }
  
  .section-grid {
    grid-template-columns: 1fr;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>
