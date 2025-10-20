<template>
  <div class="pricing-container">
    <div class="pricing-header">
      <h2 class="pricing-title">Choisissez votre plan</h2>
      <p class="pricing-subtitle">Commencez avec 7 jours d'essai gratuit</p>
    </div>

    <div class="billing-toggle">
      <label class="toggle-label">
        <input 
          type="checkbox" 
          v-model="isYearly" 
          class="toggle-input"
        />
        <span class="toggle-slider"></span>
        <span class="toggle-text">
          Facturation annuelle (2 mois gratuits)
        </span>
      </label>
    </div>

    <div class="plans-grid">
      <div 
        v-for="plan in filteredPlans" 
        :key="plan.id"
        class="plan-card"
        :class="{ 
          'popular': plan.plan_type === 'premium',
          'loading': loadingPlan === plan.id
        }"
      >
        <div v-if="plan.plan_type === 'premium'" class="popular-badge">
          Populaire
        </div>
        
        <div class="plan-header">
          <h3 class="plan-name">{{ plan.name }}</h3>
          <div class="plan-price">
            <span class="price-amount">{{ plan.price }}€</span>
            <span class="price-period">/{{ plan.billing_period === 'monthly' ? 'mois' : 'an' }}</span>
          </div>
          <div v-if="isYearly && plan.billing_period === 'yearly'" class="savings">
            Économisez {{ getSavings(plan) }}€/an
          </div>
        </div>

        <ul class="features-list">
          <li v-for="feature in plan.features" :key="feature" class="feature-item">
            <CheckIcon class="feature-icon" />
            {{ feature }}
          </li>
        </ul>

        <button 
          @click="selectPlan(plan)"
          :disabled="loadingPlan === plan.id || (userSubscription && userSubscription.plan_type === plan.plan_type)"
          class="select-plan-btn"
          :class="{ 
            'current': userSubscription && userSubscription.plan_type === plan.plan_type,
            'loading': loadingPlan === plan.id
          }"
        >
          <LoadingSpinner v-if="loadingPlan === plan.id" class="btn-spinner" />
          <span v-else-if="userSubscription && userSubscription.plan_type === plan.plan_type">
            Plan actuel
          </span>
          <span v-else>
            Commencer l'essai gratuit
          </span>
        </button>
      </div>
    </div>

    <!-- Modal de confirmation -->
    <div v-if="showConfirmModal" class="modal-overlay" @click="showConfirmModal = false">
      <div class="modal-content" @click.stop>
        <h3>Confirmer votre choix</h3>
        <p>Vous allez commencer un essai gratuit de 7 jours pour le plan {{ selectedPlan?.name }}.</p>
        <div class="modal-actions">
          <button @click="showConfirmModal = false" class="btn-cancel">
            Annuler
          </button>
          <button @click="proceedToCheckout" class="btn-confirm">
            Continuer
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { CheckIcon } from '@heroicons/vue/24/solid'
import { apiClient } from '@/api'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// Reactive data
const plans = ref([])
const isYearly = ref(false)
const loadingPlan = ref(null)
const showConfirmModal = ref(false)
const selectedPlan = ref(null)
const userSubscription = ref(null)

// Computed
const filteredPlans = computed(() => {
  return plans.value.filter(plan => 
    plan.billing_period === (isYearly.value ? 'yearly' : 'monthly')
  )
})

// Methods
const loadPlans = async () => {
  try {
    const response = await apiClient.get('/subscriptions/plans/')
    plans.value = response.data.plans
  } catch (error) {
    console.error('Erreur lors du chargement des plans:', error)
  }
}

const loadUserSubscription = async () => {
  try {
    const response = await apiClient.get('/subscriptions/status/')
    if (response.data.has_subscription) {
      userSubscription.value = response.data
    }
  } catch (error) {
    console.error('Erreur lors du chargement de l\'abonnement:', error)
  }
}

const getSavings = (yearlyPlan) => {
  const monthlyPlan = plans.value.find(p => 
    p.plan_type === yearlyPlan.plan_type && p.billing_period === 'monthly'
  )
  if (monthlyPlan) {
    return Math.round((monthlyPlan.price * 12) - yearlyPlan.price)
  }
  return 0
}

const selectPlan = (plan) => {
  selectedPlan.value = plan
  showConfirmModal.value = true
}

const proceedToCheckout = async () => {
  if (!selectedPlan.value) return
  
  loadingPlan.value = selectedPlan.value.id
  showConfirmModal.value = false
  
  try {
    const response = await apiClient.post('/subscriptions/create-checkout-session/', {
      price_id: selectedPlan.value.stripe_price_id
    })
    
    // Rediriger vers Stripe Checkout
    window.location.href = response.data.checkout_url
    
  } catch (error) {
    console.error('Erreur lors de la création de la session:', error)
    alert('Erreur lors du processus de paiement. Veuillez réessayer.')
  } finally {
    loadingPlan.value = null
  }
}

// Lifecycle
onMounted(() => {
  loadPlans()
  if (userStore.isAuthenticated) {
    loadUserSubscription()
  }
})
</script>

<style scoped>
.pricing-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.pricing-header {
  text-align: center;
  margin-bottom: 3rem;
}

.pricing-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #1e3a8a;
  margin-bottom: 1rem;
}

.pricing-subtitle {
  font-size: 1.2rem;
  color: #6b7280;
}

.billing-toggle {
  display: flex;
  justify-content: center;
  margin-bottom: 3rem;
}

.toggle-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: 0.75rem;
}

.toggle-input {
  display: none;
}

.toggle-slider {
  width: 50px;
  height: 24px;
  background: #e5e7eb;
  border-radius: 12px;
  position: relative;
  transition: all 0.3s ease;
}

.toggle-slider::after {
  content: '';
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  position: absolute;
  top: 2px;
  left: 2px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.toggle-input:checked + .toggle-slider {
  background: #3b82f6;
}

.toggle-input:checked + .toggle-slider::after {
  transform: translateX(26px);
}

.toggle-text {
  font-weight: 500;
  color: #374151;
}

.plans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.plan-card {
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 1rem;
  padding: 2rem;
  position: relative;
  transition: all 0.3s ease;
}

.plan-card:hover {
  border-color: #3b82f6;
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
}

.plan-card.popular {
  border-color: #3b82f6;
  box-shadow: 0 4px 20px rgba(59, 130, 246, 0.15);
}

.popular-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: #3b82f6;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 600;
}

.plan-header {
  text-align: center;
  margin-bottom: 2rem;
}

.plan-name {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 1rem;
}

.plan-price {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 0.25rem;
}

.price-amount {
  font-size: 3rem;
  font-weight: bold;
  color: #1e3a8a;
}

.price-period {
  font-size: 1rem;
  color: #6b7280;
}

.savings {
  margin-top: 0.5rem;
  color: #10b981;
  font-weight: 600;
  font-size: 0.875rem;
}

.features-list {
  list-style: none;
  padding: 0;
  margin-bottom: 2rem;
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

.select-plan-btn {
  width: 100%;
  padding: 1rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.select-plan-btn:hover:not(:disabled) {
  background: #2563eb;
  transform: translateY(-1px);
}

.select-plan-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.select-plan-btn.current {
  background: #10b981;
}

.select-plan-btn.loading {
  opacity: 0.8;
}

.btn-spinner {
  width: 1.25rem;
  height: 1.25rem;
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
  padding: 2rem;
  border-radius: 1rem;
  max-width: 400px;
  width: 90%;
  text-align: center;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.btn-cancel {
  padding: 0.75rem 1.5rem;
  background: #f3f4f6;
  color: #374151;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
}

.btn-confirm {
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
}

@media (max-width: 768px) {
  .pricing-container {
    padding: 1rem;
  }
  
  .plans-grid {
    grid-template-columns: 1fr;
  }
  
  .pricing-title {
    font-size: 2rem;
  }
}
</style>
