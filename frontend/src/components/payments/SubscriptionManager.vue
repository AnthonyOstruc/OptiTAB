<template>
  <div class="subscription-manager">
    <div class="subscription-card">
      <div class="card-header">
        <h3 class="card-title">Mon Abonnement</h3>
        <div class="status-badge" :class="statusClass">
          {{ statusText }}
        </div>
      </div>

      <div v-if="subscription.has_subscription" class="subscription-details">
        <!-- Plan actuel -->
        <div class="detail-row">
          <span class="detail-label">Plan actuel :</span>
          <span class="detail-value">{{ subscription.plan_name }}</span>
        </div>

        <!-- Statut -->
        <div class="detail-row">
          <span class="detail-label">Statut :</span>
          <span class="detail-value">{{ statusText }}</span>
        </div>

        <!-- Période d'essai -->
        <div v-if="subscription.is_trial" class="trial-info">
          <div class="trial-badge">
            <GiftIcon class="trial-icon" />
            Essai gratuit
          </div>
          <p class="trial-text">
            {{ subscription.days_remaining_trial }} jour(s) restant(s)
          </p>
        </div>

        <!-- Prochaine facturation -->
        <div v-if="subscription.current_period_end && subscription.is_active" class="detail-row">
          <span class="detail-label">Prochaine facturation :</span>
          <span class="detail-value">{{ formatDate(subscription.current_period_end) }}</span>
        </div>

        <!-- Fonctionnalités -->
        <div class="features-section">
          <h4 class="features-title">Fonctionnalités incluses :</h4>
          <ul class="features-list">
            <li v-for="feature in subscription.features" :key="feature" class="feature-item">
              <CheckIcon class="feature-icon" />
              {{ feature }}
            </li>
          </ul>
        </div>

        <!-- Actions -->
        <div class="actions-section">
          <button 
            v-if="subscription.is_active"
            @click="showCancelModal = true"
            class="cancel-btn"
            :disabled="cancelling"
          >
            <XMarkIcon class="btn-icon" />
            {{ cancelling ? 'Annulation...' : 'Annuler l\'abonnement' }}
          </button>
          
          <router-link 
            v-if="!subscription.is_active || subscription.status === 'canceled'"
            to="/pricing" 
            class="upgrade-btn"
          >
            <ArrowUpIcon class="btn-icon" />
            Choisir un plan
          </router-link>
        </div>
      </div>

      <!-- Pas d'abonnement -->
      <div v-else class="no-subscription">
        <div class="no-sub-icon">
          <CreditCardIcon />
        </div>
        <h4>Aucun abonnement actif</h4>
        <p>Choisissez un plan pour accéder à toutes les fonctionnalités premium.</p>
        <router-link to="/pricing" class="get-started-btn">
          Commencer l'essai gratuit
        </router-link>
      </div>
    </div>

    <!-- Modal de confirmation d'annulation -->
    <div v-if="showCancelModal" class="modal-overlay" @click="showCancelModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <ExclamationTriangleIcon class="warning-icon" />
          <h3>Annuler votre abonnement</h3>
        </div>
        <div class="modal-body">
          <p>Êtes-vous sûr de vouloir annuler votre abonnement ?</p>
          <p class="warning-text">
            Vous perdrez l'accès aux fonctionnalités premium à la fin de votre période de facturation actuelle.
          </p>
        </div>
        <div class="modal-actions">
          <button @click="showCancelModal = false" class="btn-secondary">
            Garder mon abonnement
          </button>
          <button @click="cancelSubscription" :disabled="cancelling" class="btn-danger">
            {{ cancelling ? 'Annulation...' : 'Confirmer l\'annulation' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { 
  CheckIcon, 
  XMarkIcon, 
  ArrowUpIcon, 
  CreditCardIcon,
  GiftIcon,
  ExclamationTriangleIcon 
} from '@heroicons/vue/24/outline'
import { apiClient } from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()

// Reactive data
const subscription = ref({
  has_subscription: false,
  status: 'none'
})
const loading = ref(true)
const showCancelModal = ref(false)
const cancelling = ref(false)

// Computed
const statusClass = computed(() => {
  switch (subscription.value.status) {
    case 'active': return 'status-active'
    case 'trialing': return 'status-trial'
    case 'past_due': return 'status-warning'
    case 'canceled': return 'status-canceled'
    default: return 'status-inactive'
  }
})

const statusText = computed(() => {
  switch (subscription.value.status) {
    case 'active': return 'Actif'
    case 'trialing': return 'Essai gratuit'
    case 'past_due': return 'Paiement en retard'
    case 'canceled': return 'Annulé'
    default: return 'Inactif'
  }
})

// Methods
const loadSubscription = async () => {
  try {
    loading.value = true
    const response = await apiClient.get('/subscriptions/status/')
    subscription.value = response.data
  } catch (error) {
    console.error('Erreur lors du chargement de l\'abonnement:', error)
  } finally {
    loading.value = false
  }
}

const cancelSubscription = async () => {
  try {
    cancelling.value = true
    await apiClient.post('/subscriptions/cancel/')
    
    showCancelModal.value = false
    await loadSubscription() // Recharger les données
    
    // Afficher une notification de succès
    alert('Votre abonnement a été annulé avec succès.')
    
  } catch (error) {
    console.error('Erreur lors de l\'annulation:', error)
    alert('Erreur lors de l\'annulation de votre abonnement.')
  } finally {
    cancelling.value = false
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Lifecycle
onMounted(() => {
  loadSubscription()
})
</script>

<style scoped>
.subscription-manager {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
}

.subscription-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid #f3f4f6;
}

.card-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1f2937;
  margin: 0;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 600;
}

.status-active {
  background: #d1fae5;
  color: #065f46;
}

.status-trial {
  background: #dbeafe;
  color: #1e40af;
}

.status-warning {
  background: #fef3c7;
  color: #92400e;
}

.status-canceled {
  background: #fee2e2;
  color: #991b1b;
}

.status-inactive {
  background: #f3f4f6;
  color: #6b7280;
}

.subscription-details {
  padding: 2rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f9fafb;
}

.detail-label {
  font-weight: 500;
  color: #6b7280;
}

.detail-value {
  font-weight: 600;
  color: #1f2937;
}

.trial-info {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin: 1.5rem 0;
  text-align: center;
}

.trial-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #3b82f6;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.trial-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.trial-text {
  color: #1e40af;
  font-weight: 500;
  margin: 0;
}

.features-section {
  margin: 2rem 0;
}

.features-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.features-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0;
  color: #374151;
}

.feature-icon {
  width: 1.25rem;
  height: 1.25rem;
  color: #10b981;
  flex-shrink: 0;
}

.actions-section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #f3f4f6;
}

.cancel-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #fee2e2;
  color: #dc2626;
  border: 1px solid #fecaca;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  justify-content: center;
}

.cancel-btn:hover:not(:disabled) {
  background: #fecaca;
}

.cancel-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.upgrade-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  border-radius: 0.5rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
  width: 100%;
  justify-content: center;
}

.upgrade-btn:hover {
  background: #2563eb;
}

.btn-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.no-subscription {
  padding: 3rem 2rem;
  text-align: center;
}

.no-sub-icon {
  width: 4rem;
  height: 4rem;
  background: #f3f4f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  color: #9ca3af;
}

.no-sub-icon svg {
  width: 2rem;
  height: 2rem;
}

.no-subscription h4 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.no-subscription p {
  color: #6b7280;
  margin-bottom: 2rem;
}

.get-started-btn {
  display: inline-block;
  padding: 1rem 2rem;
  background: #3b82f6;
  color: white;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
}

.get-started-btn:hover {
  background: #2563eb;
  transform: translateY(-1px);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 1rem;
  max-width: 500px;
  width: 90%;
  overflow: hidden;
}

.modal-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 2rem 2rem 1rem;
}

.warning-icon {
  width: 2rem;
  height: 2rem;
  color: #f59e0b;
}

.modal-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.modal-body {
  padding: 0 2rem 2rem;
}

.modal-body p {
  color: #6b7280;
  margin-bottom: 1rem;
}

.warning-text {
  color: #dc2626;
  font-weight: 500;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  padding: 1.5rem 2rem 2rem;
  border-top: 1px solid #f3f4f6;
}

.btn-secondary {
  flex: 1;
  padding: 0.75rem;
  background: #f3f4f6;
  color: #374151;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
}

.btn-danger {
  flex: 1;
  padding: 0.75rem;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
}

.btn-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .subscription-manager {
    padding: 1rem;
  }
  
  .card-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>
