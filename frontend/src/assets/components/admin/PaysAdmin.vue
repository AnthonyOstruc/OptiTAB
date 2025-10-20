<template>
  <div class="pays-admin">
    <!-- En-tête -->
    <div class="admin-header">
      <div class="header-content">
        <h1>Gestion des Pays</h1>
        <p>Administrez les pays et leurs systèmes éducatifs</p>
      </div>
      <button 
        @click="showCreateModal = true" 
        class="btn btn-primary"
      >
        <!-- icône retirée -->
        Ajouter un pays
      </button>
    </div>

    <!-- Filtres et recherche -->
    <div class="filters-section">
      <div class="search-box">
        <!-- icône retirée -->
        <input 
          v-model="searchTerm" 
          type="text" 
          placeholder="Rechercher un pays..."
          @input="filterPays"
        >
      </div>
      <div class="filter-buttons">
        <button 
          :class="['filter-btn', { active: activeFilter === 'all' }]"
          @click="setFilter('all')"
        >
          Tous ({{ pays.length }})
        </button>
        <button 
          :class="['filter-btn', { active: activeFilter === 'active' }]"
          @click="setFilter('active')"
        >
          Actifs ({{ pays.filter(p => p.est_actif).length }})
        </button>
        <button 
          :class="['filter-btn', { active: activeFilter === 'inactive' }]"
          @click="setFilter('inactive')"
        >
          Inactifs ({{ pays.filter(p => !p.est_actif).length }})
        </button>
      </div>
    </div>

    <!-- Table des pays -->
    <div class="pays-table-container">
      <table class="pays-table">
        <thead>
          <tr>
            <th>Pays</th>
            <th>Code ISO</th>
            <th>Statut</th>
            <th>Niveaux</th>
            <th>Utilisateurs</th>
            <th>Ordre</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pays in filteredPays" :key="pays.id" :class="{ inactive: !pays.est_actif }">
            <td class="pays-cell">
              <span class="pays-flag">{{ pays.drapeau_emoji || '🏳️' }}</span>
              <div class="pays-info">
                <strong>{{ pays.nom }}</strong>
                <small v-if="pays.description">{{ pays.description }}</small>
              </div>
            </td>
            <td>
              <span class="code-iso">{{ pays.code_iso }}</span>
            </td>
            <td>
              <span :class="['status-badge', pays.est_actif ? 'active' : 'inactive']">
                {{ pays.est_actif ? 'Actif' : 'Inactif' }}
              </span>
            </td>
            <td>
              <span class="count-badge">{{ pays.nombre_niveaux || 0 }}</span>
            </td>
            <td>
              <span class="count-badge">{{ pays.nombre_utilisateurs || 0 }}</span>
            </td>
            <td>
              <input 
                v-model.number="pays.ordre" 
                type="number" 
                class="ordre-input"
                @change="updatePaysOrdre(pays)"
                min="0"
              >
            </td>
            <td class="actions-cell">
              <button 
                @click="editPays(pays)" 
                class="action-btn edit-btn"
                title="Modifier"
              >
                 <!-- icône retirée -->
                <span class="action-label">Éditer</span>
              </button>
              <button 
                @click="togglePaysStatus(pays)" 
                :class="['action-btn', pays.est_actif ? 'deactivate-btn' : 'activate-btn']"
                :title="pays.est_actif ? 'Désactiver' : 'Activer'"
              >
                 <!-- icône retirée -->
                <span class="action-label">{{ pays.est_actif ? 'Actif' : 'Inactif' }}</span>
              </button>
              <button 
                @click="confirmDelete(pays)" 
                class="action-btn delete-btn"
                title="Supprimer"
              >
                 <!-- icône retirée -->
                <span class="action-label">Supprimer</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- État vide -->
      <div v-if="filteredPays.length === 0" class="empty-state">
        <div class="empty-icon">🌍</div>
        <h3>Aucun pays trouvé</h3>
        <p v-if="searchTerm">Aucun pays ne correspond à votre recherche "{{ searchTerm }}"</p>
        <p v-else>Commencez par ajouter votre premier pays.</p>
        <button @click="showCreateModal = true" class="btn btn-primary">
          Ajouter un pays
        </button>
      </div>
    </div>

    <!-- Modal de création/édition -->
    <PaysModal 
      v-if="showCreateModal || showEditModal"
      :visible="showCreateModal || showEditModal"
      :pays="selectedPays"
      :mode="showCreateModal ? 'create' : 'edit'"
      @save="handleSavePays"
      @cancel="closeModals"
    />

    <!-- Modal de confirmation de suppression -->
    <ConfirmModal
      v-if="showDeleteModal"
      :visible="showDeleteModal"
      :title="`Supprimer ${paysToDelete?.nom}`"
      :message="`Êtes-vous sûr de vouloir supprimer le pays ${paysToDelete?.nom} ? Cette action est irréversible.`"
      danger
      @confirm="handleDeletePays"
      @cancel="showDeleteModal = false"
    />

    <!-- Notifications -->
    <div v-if="notification" :class="['notification', notification.type]">
      <i :class="getNotificationIcon(notification.type)"></i>
      {{ notification.message }}
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { getPays, createPays, updatePays, deletePays } from '@/api/pays'
import PaysModal from './PaysModal.vue'
import ConfirmModal from '@/components/modals/ConfirmModal.vue'

export default {
  name: 'PaysAdmin',
  components: {
    PaysModal,
    ConfirmModal
  },
  setup() {
    const pays = ref([])
    const filteredPays = ref([])
    const searchTerm = ref('')
    const activeFilter = ref('all')
    const loading = ref(false)
    
    // Modals
    const showCreateModal = ref(false)
    const showEditModal = ref(false)
    const showDeleteModal = ref(false)
    const selectedPays = ref(null)
    const paysToDelete = ref(null)
    
    // Notifications
    const notification = ref(null)

    // Charger les pays
    const loadPays = async () => {
      loading.value = true
      try {
        const response = await getPays()
        pays.value = response.results || response
        filterPays()
      } catch (error) {
        showNotification('Erreur lors du chargement des pays', 'error')
      } finally {
        loading.value = false
      }
    }

    // Filtrer les pays
    const filterPays = () => {
      let filtered = pays.value

      // Filtre par statut
      if (activeFilter.value === 'active') {
        filtered = filtered.filter(p => p.est_actif)
      } else if (activeFilter.value === 'inactive') {
        filtered = filtered.filter(p => !p.est_actif)
      }

      // Filtre par recherche
      if (searchTerm.value) {
        const search = searchTerm.value.toLowerCase()
        filtered = filtered.filter(p => 
          p.nom.toLowerCase().includes(search) ||
          p.code_iso.toLowerCase().includes(search) ||
          (p.description && p.description.toLowerCase().includes(search))
        )
      }

      filteredPays.value = filtered.sort((a, b) => (a.ordre || 0) - (b.ordre || 0))
    }

    // Changer le filtre
    const setFilter = (filter) => {
      activeFilter.value = filter
      filterPays()
    }

    // Créer/éditer un pays
    const editPays = (paysData) => {
      selectedPays.value = { ...paysData }
      showEditModal.value = true
    }

    const handleSavePays = async (paysData) => {
      try {
        if (showCreateModal.value) {
          await createPays(paysData)
          showNotification('Pays créé avec succès', 'success')
        } else {
          await updatePays(selectedPays.value.id, paysData)
          showNotification('Pays modifié avec succès', 'success')
        }
        closeModals()
        await loadPays()
      } catch (error) {
        showNotification('Erreur lors de la sauvegarde', 'error')
      }
    }

    // Changer le statut d'un pays
    const togglePaysStatus = async (paysData) => {
      try {
        await updatePays(paysData.id, { est_actif: !paysData.est_actif })
        paysData.est_actif = !paysData.est_actif
        showNotification(
          `Pays ${paysData.est_actif ? 'activé' : 'désactivé'} avec succès`, 
          'success'
        )
        filterPays()
      } catch (error) {
        showNotification('Erreur lors du changement de statut', 'error')
      }
    }

    // Mettre à jour l'ordre
    const updatePaysOrdre = async (paysData) => {
      try {
        await updatePays(paysData.id, { ordre: paysData.ordre })
        showNotification('Ordre mis à jour', 'success')
        filterPays()
      } catch (error) {
        showNotification('Erreur lors de la mise à jour de l\'ordre', 'error')
        await loadPays() // Recharger pour annuler le changement
      }
    }

    // Supprimer un pays
    const confirmDelete = (paysData) => {
      paysToDelete.value = paysData
      showDeleteModal.value = true
    }

    const handleDeletePays = async () => {
      try {
        await deletePays(paysToDelete.value.id)
        showNotification('Pays supprimé avec succès', 'success')
        showDeleteModal.value = false
        await loadPays()
      } catch (error) {
        showNotification('Erreur lors de la suppression', 'error')
      }
    }

    // Fermer les modals
    const closeModals = () => {
      showCreateModal.value = false
      showEditModal.value = false
      selectedPays.value = null
    }

    // Notifications
    const showNotification = (message, type = 'info') => {
      notification.value = { message, type }
      setTimeout(() => {
        notification.value = null
      }, 4000)
    }

    const getNotificationIcon = (type) => {
      const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
      }
      return icons[type] || icons.info
    }

    onMounted(loadPays)

    return {
      pays,
      filteredPays,
      searchTerm,
      activeFilter,
      loading,
      showCreateModal,
      showEditModal,
      showDeleteModal,
      selectedPays,
      paysToDelete,
      notification,
      loadPays,
      filterPays,
      setFilter,
      editPays,
      handleSavePays,
      togglePaysStatus,
      updatePaysOrdre,
      confirmDelete,
      handleDeletePays,
      closeModals,
      showNotification,
      getNotificationIcon
    }
  }
}
</script>

<style scoped>
.pays-admin {
  padding: 20px;
  background: #f8f9fa;
  min-height: 100vh;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 30px;
}

.header-content h1 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 2rem;
}

.header-content p {
  margin: 0;
  color: #6c757d;
  font-size: 1.1rem;
}

.filters-section {
  background: white;
  padding: 20px 30px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.search-box {
  position: relative;
  flex: 1;
  max-width: 400px;
}

.search-box i {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
}

.search-box input {
  width: 100%;
  padding: 12px 15px 12px 45px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.search-box input:focus {
  outline: none;
  border-color: #007cba;
}

.filter-buttons {
  display: flex;
  gap: 10px;
}

.filter-btn {
  padding: 10px 16px;
  border: 2px solid #e9ecef;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.filter-btn:hover {
  border-color: #007cba;
}

.filter-btn.active {
  background: #007cba;
  color: white;
  border-color: #007cba;
}

.pays-table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.pays-table {
  width: 100%;
  border-collapse: collapse;
}

.pays-table th {
  background: #f8f9fa;
  padding: 15px 20px;
  text-align: left;
  font-weight: 600;
  color: #495057;
  border-bottom: 2px solid #e9ecef;
}

.pays-table td {
  padding: 15px 20px;
  border-bottom: 1px solid #f1f3f4;
  vertical-align: middle;
}

.pays-table tr:hover {
  background: #f8f9fa;
}

.pays-table tr.inactive {
  opacity: 0.6;
}

.pays-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.pays-flag {
  font-size: 1.5rem;
}

.pays-info strong {
  display: block;
  color: #2c3e50;
}

.pays-info small {
  color: #6c757d;
  font-size: 0.85rem;
}

.code-iso {
  background: #e9ecef;
  padding: 4px 8px;
  border-radius: 4px;
  font-family: monospace;
  font-weight: bold;
  font-size: 0.9rem;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status-badge.active {
  background: #d4edda;
  color: #155724;
}

.status-badge.inactive {
  background: #f8d7da;
  color: #721c24;
}

.count-badge {
  background: #007cba;
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
  min-width: 20px;
  text-align: center;
  display: inline-block;
}

.ordre-input {
  width: 60px;
  padding: 6px 8px;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  text-align: center;
}

.actions-cell {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 8px 10px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.edit-btn {
  background: #ffc107;
  color: white;
}

.edit-btn:hover {
  background: #e0a800;
}

.activate-btn {
  background: #28a745;
  color: white;
}

.activate-btn:hover {
  background: #218838;
}

.deactivate-btn {
  background: #6c757d;
  color: white;
}

.deactivate-btn:hover {
  background: #545b62;
}

.delete-btn {
  background: #dc3545;
  color: white;
}

.delete-btn:hover {
  background: #c82333;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #6c757d;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.empty-state h3 {
  margin: 0 0 10px 0;
  color: #495057;
}

.empty-state p {
  margin: 0 0 20px 0;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-primary {
  background: #007cba;
  color: white;
}

.btn-primary:hover {
  background: #005a87;
}

.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 15px 20px;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
  z-index: 1000;
  animation: slideIn 0.3s ease;
}

.notification.success {
  background: #28a745;
}

.notification.error {
  background: #dc3545;
}

.notification.warning {
  background: #ffc107;
  color: #212529;
}

.notification.info {
  background: #17a2b8;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .admin-header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .filters-section {
    flex-direction: column;
    gap: 15px;
  }
  
  .filter-buttons {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .pays-table-container {
    overflow-x: auto;
  }
  
  .pays-table {
    min-width: 800px;
  }
}
</style>
