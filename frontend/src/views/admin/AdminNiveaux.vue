<template>
  <div class="admin-niveaux">
    <div class="header">
      <h1>Gestion des Niveaux</h1>
      <button @click="openCreateModal" class="btn-primary">
        <i class="fas fa-plus"></i> Nouveau Niveau
      </button>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Chargement des niveaux...</p>
    </div>

    <!-- Statistiques générales -->
    <div v-else class="stats-grid">
      <div class="stat-card">
        <h3>Total Niveaux</h3>
        <p class="stat-number">{{ niveaux.length }}</p>
      </div>
      <div class="stat-card">
        <h3>Niveaux Actifs</h3>
        <p class="stat-number">{{ niveauxActifs }}</p>
      </div>
      <div class="stat-card">
        <h3>Total Matières</h3>
        <p class="stat-number">{{ totalMatieres }}</p>
      </div>
      <div class="stat-card">
        <h3>Total Cours</h3>
        <p class="stat-number">{{ totalCours }}</p>
      </div>
    </div>

    <!-- Liste des niveaux groupés par pays -->
    <div v-if="!loading">
      <div class="filters">
        <div class="filter-group">
          <label>Filtrer les niveaux</label>
          <input
            v-model="niveauFilter"
            type="text"
            placeholder="Nom, description ou pays"
          />
        </div>
        <div class="filter-group">
          <label>Pays</label>
          <select v-model="paysFilter">
            <option value="">Tous les pays</option>
            <option v-for="p in pays" :key="p.id" :value="p.id">
              {{ p.nom }}
            </option>
          </select>
        </div>
        <div class="filter-group">
          <label>Statut</label>
          <select v-model="statusFilter">
            <option value="all">Tous</option>
            <option value="active">Actifs</option>
            <option value="inactive">Inactifs</option>
          </select>
        </div>
      </div>

      <div v-if="filteredNiveaux.length === 0" class="empty-state">
        <p>Aucun niveau ne correspond aux filtres sélectionnés.</p>
      </div>

      <div v-else>
        <div v-for="group in niveauxByPays" :key="group.pays_id" class="pays-group">
          <div class="pays-header">
            <h2 class="pays-title">{{ group.pays_nom }}</h2>
          </div>

          <div class="niveaux-list">
            <div v-for="niveau in group.niveaux" :key="niveau.id" class="niveau-card">
              <div class="niveau-header">
                <div class="niveau-info">
                  <div class="niveau-color" :style="{ backgroundColor: niveau.couleur }"></div>
                  <div>
                    <h3>{{ niveau.nom }}</h3>
                    <p>{{ niveau.description || 'Aucune description' }}</p>
                  </div>
                </div>
                <div class="niveau-actions">
                  <AdminActionsButtons
                    :item="niveau"
                    :actions="['edit', 'delete']"
                    edit-label="Modifier"
                    confirm-message="Êtes-vous sûr de vouloir supprimer ce niveau ?"
                    @edit="editNiveau"
                    @delete="handleDeleteNiveau"
                  />
                </div>
              </div>
  
              <div class="niveau-stats">
                <div class="stat-item">
                  <span class="stat-label">Matières:</span>
                  <span class="stat-value">{{ niveau.statistiques?.matieres || 0 }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Cours:</span>
                  <span class="stat-value">{{ niveau.statistiques?.cours || 0 }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Exercices:</span>
                  <span class="stat-value">{{ niveau.statistiques?.exercices || 0 }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Quiz:</span>
                  <span class="stat-value">{{ niveau.statistiques?.quiz || 0 }}</span>
                </div>
              </div>

              <div class="niveau-status">
                <span :class="['status-badge', niveau.est_actif ? 'active' : 'inactive']">
                  {{ niveau.est_actif ? 'Actif' : 'Inactif' }}
                </span>
                <span class="ordre-badge">Ordre: {{ niveau.ordre }}</span>
                <span v-if="niveau.demo_notion_titre" class="demo-badge" title="Chapitre démo configuré">
                  📖 {{ niveau.demo_notion_titre }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>



    

    <!-- Modal de création/édition -->
    <SimpleModal 
      :is-open="showCreateModal || showEditModal" 
      :title="showEditModal ? 'Modifier le Niveau' : 'Nouveau Niveau'"
      @close="closeModal"
    >
      <form @submit.prevent="saveNiveau" class="niveau-form">
        <div class="form-group">
          <label for="nom">Nom du niveau *</label>
          <input 
            id="nom"
            v-model="formData.nom" 
            type="text" 
            required 
            placeholder="ex: 6ème"
          />
        </div>

        <div class="form-group">
          <label for="pays">Pays *</label>
          <select 
            id="pays"
            v-model="formData.pays" 
            required
          >
            <option value="">Sélectionner un pays</option>
            <option v-for="pays_item in pays" :key="pays_item.id" :value="pays_item.id">
              {{ pays_item.nom }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea 
            id="description"
            v-model="formData.description" 
            placeholder="Description du niveau..."
            rows="3"
          ></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="ordre">Ordre d'affichage</label>
            <input 
              id="ordre"
              v-model.number="formData.ordre" 
              type="number" 
              min="0"
              placeholder="0"
            />
          </div>

          <div class="form-group">
            <label for="couleur">Couleur</label>
            <input 
              id="couleur"
              v-model="formData.couleur" 
              type="color"
              class="color-picker"
            />
          </div>
        </div>

        <div class="form-group">
          <label class="checkbox-label">
            <input 
              v-model="formData.est_actif" 
              type="checkbox"
            />
            Niveau actif
          </label>
        </div>

        <div class="divider"></div>

        <div class="form-group">
          <label>Exercice filter options (JSON)</label>
          <textarea
            v-model="modalFilterOptions"
            rows="4"
            placeholder='Ex: ["Découverte", "Entraînement"]'
          ></textarea>
          <small class="muted">
            Entrez un tableau JSON. L’ordre définit le menu déroulant des exercices.
          </small>
        </div>

        <div class="form-group">
          <label>Valeur par défaut</label>
          <input
            v-model="modalFilterDefault"
            placeholder="Tous"
          />
        </div>

        <div class="divider"></div>

        <!-- Chapitre démo -->
        <h4 class="form-section-title">Chapitre démo (gratuit)</h4>
        <small class="muted" style="display:block;margin-bottom:0.75rem;">
          Choisis un chapitre (notion) et jusqu'à 2 exercices débloqués gratuitement pour les non-abonnés.
        </small>

        <div class="form-group">
          <label for="demo_notion">Chapitre démo</label>
          <select
            id="demo_notion"
            v-model="formData.demo_notion"
            @change="onDemoNotionChange"
          >
            <option :value="null">— Aucun —</option>
            <option v-for="n in demoNotions" :key="n.id" :value="n.id">
              {{ n.titre }}
            </option>
          </select>
        </div>

        <div class="form-group" v-if="formData.demo_notion">
          <label>Exercices démo (max 2)</label>
          <div v-if="demoExercicesLoading" class="muted">Chargement…</div>
          <div v-else-if="demoExercicesOptions.length === 0" class="muted">Aucun exercice pour cette notion.</div>
          <div v-else class="demo-exercices-list">
            <label
              v-for="ex in demoExercicesOptions"
              :key="ex.id"
              class="checkbox-label demo-exercice-item"
            >
              <input
                type="checkbox"
                :value="ex.id"
                v-model="formData.demo_exercices"
                :disabled="formData.demo_exercices.length >= 2 && !formData.demo_exercices.includes(ex.id)"
              />
              {{ ex.titre }}
            </label>
          </div>
          <small class="muted" v-if="formData.demo_exercices.length > 0">
            {{ formData.demo_exercices.length }}/2 exercice(s) sélectionné(s)
          </small>
        </div>
      </form>

      <template #footer>
        <button @click="closeModal" class="btn-secondary">Annuler</button>
        <button @click="saveNiveau" class="btn-primary" :disabled="saving">
          <span v-if="saving">Enregistrement...</span>
          <span v-else>{{ showEditModal ? 'Modifier' : 'Créer' }}</span>
        </button>
      </template>
    </SimpleModal>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useToast } from '@/composables/useToast'
import SimpleModal from '@/components/debug/SimpleModal.vue'
import AdminActionsButtons from '@/components/admin/AdminActionsButtons.vue'
import { 
  getNiveaux, 
  createNiveau, 
  updateNiveau, 
  deleteNiveau
} from '@/api/niveaux.js'
import { getPays } from '@/api/pays.js'
import { getNotions } from '@/api/notions.js'
import { getExercices } from '@/api/exercices.js'

export default {
  name: 'AdminNiveaux',
  components: {
    SimpleModal,
    AdminActionsButtons
  },
  setup() {
    const { showToast } = useToast()
    
    const niveaux = ref([])
    const pays = ref([])
    const loading = ref(false)
    const saving = ref(false)
    const showCreateModal = ref(false)
    const showEditModal = ref(false)
    const niveauFilter = ref('')
    const paysFilter = ref('')
    const statusFilter = ref('all')
    const modalFilterOptions = ref('[]')
    const modalFilterDefault = ref('Tous')
    const formData = ref({
      id: null,
      nom: '',
      description: '',
      pays: null,
      ordre: 0,
      couleur: '#3b82f6',
      est_actif: true,
      exercice_filter_options: [],
      exercice_filter_default: 'Tous',
      demo_notion: null,
      demo_exercices: []
    })

    // Demo chapter state
    const demoNotions = ref([])
    const demoExercicesOptions = ref([])
    const demoExercicesLoading = ref(false)

    // Computed
    const niveauxActifs = computed(() => 
      niveaux.value.filter(n => n.est_actif).length
    )

    const totalMatieres = computed(() => 
      niveaux.value.reduce((sum, n) => sum + (n.statistiques?.matieres || 0), 0)
    )

    const totalCours = computed(() => 
      niveaux.value.reduce((sum, n) => sum + (n.statistiques?.cours || 0), 0)
    )

    // Groupement par pays pour l'affichage
    const filteredNiveaux = computed(() => {
      const query = niveauFilter.value.trim().toLowerCase()
      return niveaux.value.filter(n => {
        if (paysFilter.value) {
          const matchesPaysId = String(n.pays) === String(paysFilter.value)
          const matchesPaysNom = String(n.pays_nom || '').toLowerCase() === String(paysFilter.value).toLowerCase()
          if (!matchesPaysId && !matchesPaysNom) return false
        }
        if (query) {
          const searchable = [
            n.nom,
            n.description,
            n.pays_nom
          ].filter(Boolean).join(' ').toLowerCase()
          if (!searchable.includes(query)) return false
        }
        if (statusFilter.value !== 'all') {
          if (statusFilter.value === 'active' && !n.est_actif) return false
          if (statusFilter.value === 'inactive' && n.est_actif) return false
        }
        return true
      })
    })

    const niveauxByPays = computed(() => {
      const groupsMap = new Map()
      for (const n of filteredNiveaux.value) {
        const key = n.pays ?? `p-${n.pays_nom}`
        if (!groupsMap.has(key)) {
          groupsMap.set(key, {
            pays_id: n.pays ?? key,
            pays_nom: n.pays_nom || 'Pays',
            pays_drapeau: n.pays_drapeau || '',
            niveaux: []
          })
        }
        groupsMap.get(key).niveaux.push(n)
      }
      // Trier les groupes par nom de pays puis niveaux par ordre
      const groups = Array.from(groupsMap.values()).sort((a, b) => a.pays_nom.localeCompare(b.pays_nom))
      groups.forEach(g => g.niveaux.sort((a, b) => (a.ordre ?? 0) - (b.ordre ?? 0)))
      return groups
    })

    // Methods
    const loadNiveaux = async () => {
      try {
        loading.value = true
        const data = await getNiveaux()
        // Les statistiques ne sont plus renvoyées sur la liste pour accélérer
        niveaux.value = Array.isArray(data) ? data : (data?.results || [])
      } catch (error) {
        console.error('Erreur lors du chargement des niveaux:', error)
        showToast('Erreur lors du chargement des niveaux', 'error')
      } finally {
        loading.value = false
      }
    }

    const loadPays = async () => {
      try {
        console.log('🌍 Chargement des pays...')
        const data = await getPays()
        console.log('🌍 Pays récupérés:', data)
        pays.value = data
        console.log('🌍 Pays stockés dans pays.value:', pays.value)
      } catch (error) {
        console.error('Erreur lors du chargement des pays:', error)
        showToast('Erreur lors du chargement des pays', 'error')
      }
    }

    const openCreateModal = async () => {
      closeModal()
      console.log('🎯 Bouton Nouveau Niveau cliqué')
      console.log('showCreateModal avant:', showCreateModal.value)
      console.log('🌍 Appel de loadPays()...')
      await loadPays() // Charger les pays disponibles
      modalFilterOptions.value = '[]'
      modalFilterDefault.value = 'Tous'
      showCreateModal.value = true
      console.log('showCreateModal après:', showCreateModal.value)
    }

    const editNiveau = async (niveau) => {
      console.log('✏️ Édition du niveau:', niveau)
      await loadPays() // Charger les pays disponibles
      formData.value = { 
        id: niveau.id,
        nom: niveau.nom,
        description: niveau.description || '',
        pays: niveau.pays || null,
        ordre: niveau.ordre,
        couleur: niveau.couleur,
        est_actif: niveau.est_actif,
        exercice_filter_options: niveau.exercice_filter_options || [],
        exercice_filter_default: niveau.exercice_filter_default || 'Tous',
        demo_notion: niveau.demo_notion || null,
        demo_exercices: niveau.demo_exercices || []
      }
      modalFilterOptions.value = JSON.stringify(niveau.exercice_filter_options || [], null, 2)
      modalFilterDefault.value = niveau.exercice_filter_default || 'Tous'
      // Load notions for this niveau
      await loadDemoNotions(niveau.id)
      // Load exercices if a demo notion is already selected
      if (niveau.demo_notion) {
        await loadDemoExercices(niveau.demo_notion)
      }
      showEditModal.value = true
    }

    const parseModalFilterOptions = () => {
      try {
        const parsed = JSON.parse(modalFilterOptions.value || '[]')
        if (!Array.isArray(parsed)) {
          showToast('Les options doivent être un tableau JSON', 'error')
          return null
        }
        return parsed
      } catch (error) {
        showToast('Le format JSON des options est invalide', 'error')
        return null
      }
    }

    const saveNiveau = async () => {
      const parsedOptions = parseModalFilterOptions()
      if (parsedOptions === null) {
        return
      }

      formData.value.exercice_filter_options = parsedOptions
      formData.value.exercice_filter_default = modalFilterDefault.value || 'Tous'

      try {
        saving.value = true
        
        if (showEditModal.value) {
          const { id, ...dataToUpdate } = formData.value
          await updateNiveau(id, dataToUpdate)
          showToast('Niveau modifié avec succès', 'success')
        } else {
          await createNiveau(formData.value)
          showToast('Niveau créé avec succès', 'success')
        }
        
        closeModal()
        loadNiveaux()
      } catch (error) {
        console.error('Erreur lors de la sauvegarde:', error)
        showToast('Erreur lors de la sauvegarde', 'error')
      } finally {
        saving.value = false
      }
    }

    const confirmDeleteNiveau = (niveau) => {
      deleteNiveauHandler(niveau.id)
    }

    // Nouvelle fonction qui utilise le composant AdminActionsButtons
    const handleDeleteNiveau = (niveau) => {
      deleteNiveauHandler(niveau.id)
    }

    const deleteNiveauHandler = async (niveauId) => {
      try {
        await deleteNiveau(niveauId)
        showToast('Niveau supprimé avec succès', 'success')
        loadNiveaux()
      } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        showToast('Erreur lors de la suppression', 'error')
      }
    }

    const closeModal = () => {
      showCreateModal.value = false
      showEditModal.value = false
      formData.value = {
        id: null,
        nom: '',
        description: '',
        pays: null,
        ordre: 0,
        couleur: '#3b82f6',
        est_actif: true,
        exercice_filter_options: [],
        exercice_filter_default: 'Tous',
        demo_notion: null,
        demo_exercices: []
      }
      modalFilterOptions.value = '[]'
      modalFilterDefault.value = 'Tous'
      demoNotions.value = []
      demoExercicesOptions.value = []
    }

    // Demo chapter helpers
    const loadDemoNotions = async (niveauId) => {
      try {
        const resp = await getNotions({ niveau: niveauId })
        const data = resp?.data || resp
        demoNotions.value = Array.isArray(data) ? data : (data?.results || [])
      } catch (e) {
        console.error('Erreur chargement notions démo:', e)
        demoNotions.value = []
      }
    }

    const loadDemoExercices = async (notionId) => {
      demoExercicesLoading.value = true
      try {
        const resp = await getExercices({ notion: notionId })
        const data = resp?.data || resp
        demoExercicesOptions.value = Array.isArray(data) ? data : (data?.results || [])
      } catch (e) {
        console.error('Erreur chargement exercices démo:', e)
        demoExercicesOptions.value = []
      } finally {
        demoExercicesLoading.value = false
      }
    }

    const onDemoNotionChange = async () => {
      formData.value.demo_exercices = []
      demoExercicesOptions.value = []
      if (formData.value.demo_notion) {
        await loadDemoExercices(formData.value.demo_notion)
      }
    }

    onMounted(() => {
      loadNiveaux()
      loadPays()
    })

    return {
      niveaux,
      pays,
      loading,
      saving,
      showCreateModal,
      showEditModal,
      formData,
      niveauxActifs,
      totalMatieres,
      totalCours,
      niveauxByPays,
      filteredNiveaux,
      niveauFilter,
      paysFilter,
      statusFilter,
      modalFilterOptions,
      modalFilterDefault,
      demoNotions,
      demoExercicesOptions,
      demoExercicesLoading,
      openCreateModal,
      editNiveau,
      saveNiveau,
      confirmDeleteNiveau,
      handleDeleteNiveau,
      closeModal,
      onDemoNotionChange
    }
  }
}
</script>

<style scoped>
.pays-badge {
  background-color: #f3f4f6;
  color: #374151;
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  font-weight: 500;
  margin-left: 0.5rem;
}

.admin-niveaux {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.filter-group {
  flex: 1;
  min-width: 180px;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.filter-group input,
.filter-group select {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.9rem;

}
.empty-state {
  padding: 1rem 1.5rem;
  background: #f8fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  color: #475569;
  margin-bottom: 1.5rem;
}

.assignment-section {
  margin-bottom: 3rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header h1 {
  margin: 0;
  color: #1f2937;
  font-size: 2rem;
  font-weight: 700;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: #6b7280;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  border: 1px solid #e5e7eb;
}

.stat-card h3 {
  margin: 0 0 0.5rem 0;
  color: #6b7280;
  font-size: 0.875rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-number {
  margin: 0;
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
}

.niveaux-list {
  display: grid;
  gap: 1rem;
}

.niveau-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.niveau-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-1px);
}

.niveau-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.niveau-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.niveau-color {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.niveau-info h3 {
  margin: 0 0 0.25rem 0;
  color: #1f2937;
  font-size: 1.25rem;
  font-weight: 600;
}

.niveau-info p {
  margin: 0;
  color: #6b7280;
  font-size: 0.875rem;
}

.niveau-actions {
  display: flex;
  gap: 0.5rem;
}

.niveau-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

.stat-value {
  font-weight: 600;
  color: #1f2937;
  font-size: 1rem;
}

.niveau-status {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.status-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-badge.active {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.status-badge.inactive {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.ordre-badge {
  padding: 0.375rem 0.75rem;
  background: #f3f4f6;
  color: #374151;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  border: 1px solid #e5e7eb;
}

.niveau-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.divider {
  height: 1px;
  background: #e5e7eb;
  margin: 1rem 0;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.muted {
  color: #6b7280;
  font-size: 0.85rem;
}

.form-group label {
  font-weight: 500;
  color: #374151;
  font-size: 0.875rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.color-picker {
  width: 100%;
  height: 48px;
  padding: 0;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  cursor: pointer;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  margin: 0;
}

.btn-primary,
.btn-secondary,
.btn-danger {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-secondary:hover {
  background: #e5e7eb;
  border-color: #9ca3af;
}

.btn-danger {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(239, 68, 68, 0.2);
}

.btn-danger:hover {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(239, 68, 68, 0.3);
}

.btn-primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

@media (max-width: 768px) {
  .admin-niveaux {
    padding: 1rem;
  }
  
  .header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .header h1 {
    font-size: 1.5rem;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .niveau-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .niveau-actions {
    align-self: flex-end;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
}

.form-section-title {
  margin: 0 0 0.25rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: #1f2937;
}

.demo-exercices-list {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  max-height: 200px;
  overflow-y: auto;
  padding: 0.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #f9fafb;
}

.demo-exercice-item {
  padding: 0.35rem 0.5rem;
  border-radius: 6px;
  transition: background 0.15s;
}

.demo-exercice-item:hover {
  background: #e5e7eb;
}

.demo-badge {
  padding: 0.375rem 0.75rem;
  background: #eff6ff;
  color: #1d4ed8;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  border: 1px solid #bfdbfe;
}
</style> 
