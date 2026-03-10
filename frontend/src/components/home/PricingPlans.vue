<template>
  <section class="pricing-plans-section" id="tarifs">
    <!-- Header -->
    <div class="pricing-header">
      <h2 class="pricing-title">
        Choisissez votre <span class="pricing-highlight">Abonnement Maths</span>
      </h2>
      <p class="pricing-desc">Accès complet aux cours, fiches de synthèse et exercices corrigés pas à pas — sans engagement, annulable à tout moment.</p>
    </div>

    <!-- Pricing Cards Component -->
    <PricingCards 
      :submitting="submitting"
      cta-location="pricing"
      @select="handleSubscribe"
    />

    <!-- Modal de sélection du niveau -->
    <div
      v-if="showLevelModal"
      class="level-modal-overlay"
      @click="closeLevelModal"
    >
      <div class="level-modal" @click.stop>
        <button
          class="modal-close"
          type="button"
          :disabled="submitting"
          @click="closeLevelModal"
        >
          <span aria-hidden="true">&times;</span>
        </button>
        <div class="modal-header">
          <p class="modal-eyebrow">Activation de l'accès</p>
          <h3>Choisis ton niveau</h3>
          <p class="modal-subtitle">
            L'abonnement <strong>{{ pendingPlanName || 'OptiTAB' }}</strong> débloquera un seul niveau.
            Sélectionne celui que tu veux activer maintenant.
          </p>
        </div>
        <div class="modal-body">
          <div v-if="niveauxLoading" class="modal-loading">
            <div class="spinner small"></div>
            <p>Chargement des niveaux…</p>
          </div>
          <div v-else-if="niveauxError" class="modal-error">
            <p>{{ niveauxError }}</p>
            <button type="button" class="modal-refresh" @click="loadLevels(true)">
              Réessayer
            </button>
          </div>
          <div v-else class="modal-select-group">
            <label for="home-level-select">Niveau à débloquer</label>
            <div class="modal-select-wrapper">
              <select
                id="home-level-select"
                v-model.number="selectedNiveauId"
              >
                <option
                  v-for="niveau in niveaux"
                  :key="niveau.id"
                  :value="niveau.id"
                >
                  {{ niveau.nom }}
                  <span v-if="niveau.pays?.nom"> — {{ niveau.pays.nom }}</span>
                </option>
              </select>
            </div>
            <p class="modal-hint">
              Tu pourras débloquer un autre niveau plus tard avec un nouvel abonnement.
            </p>
            <p v-if="selectedNiveauLabel" class="modal-selection">
              Accès prévu : {{ selectedNiveauLabel }}
            </p>
          </div>
          <p
            v-if="!userStore.isAuthenticated"
            class="modal-signup-hint"
          >
            Pas encore de compte ? Choisis ton niveau puis crée ton compte gratuitement pour finaliser le paiement.
          </p>
        </div>
        <div class="modal-actions">
          <button
            type="button"
            class="modal-btn secondary"
            :disabled="submitting"
            @click="closeLevelModal"
          >
            Annuler
          </button>
          <button
            type="button"
            class="modal-btn primary"
            :disabled="submitting || !selectedNiveauId"
            @click="confirmSubscription"
          >
            {{ submitting ? 'Redirection…' : 'Continuer vers le paiement' }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { createCheckoutSession } from '@/api/subscriptions'
import PricingCards from '@/components/shared/PricingCards.vue'
import { useUserStore } from '@/stores/user'
import { getNiveauxByPays } from '@/api/niveaux'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { useCheckoutIntentStore } from '@/stores/checkoutIntent'
import { useToast } from '@/composables/useToast'

const submitting = ref(false)
const userStore = useUserStore()
const checkoutIntentStore = useCheckoutIntentStore()
const { openModal } = useModalManager()
const { info: showInfoToast, error: showErrorToast } = useToast()
const niveaux = ref([])
const niveauxLoading = ref(false)
const niveauxError = ref('')
const selectedNiveauId = ref(
  userStore.niveau_pays?.id ? Number(userStore.niveau_pays.id) : null
)
const showLevelModal = ref(false)
const pendingPriceId = ref('')
const pendingPlanName = ref('')

watch(
  () => userStore.niveau_pays?.id,
  (newId) => {
    if (newId) {
      selectedNiveauId.value = Number(newId)
    }
  }
)

const selectedNiveau = computed(() =>
  niveaux.value.find(n => Number(n.id) === Number(selectedNiveauId.value)) || null
)

const selectedNiveauLabel = computed(() => {
  if (!selectedNiveau.value) return ''
  const pays = selectedNiveau.value.pays?.nom
  return pays ? `${selectedNiveau.value.nom} · ${pays}` : selectedNiveau.value.nom
})

async function loadLevels(force = false) {
  if (niveauxLoading.value) return
  if (!force && niveaux.value.length) return
  try {
    niveauxLoading.value = true
    niveauxError.value = ''
    const data = await getNiveauxByPays()
    const rawList = Array.isArray(data?.results)
      ? data.results
      : Array.isArray(data)
        ? data
        : (Array.isArray(data?.data) ? data.data : [])
    const activeList = rawList.filter(n => n && (n.est_actif === undefined || n.est_actif))
    niveaux.value = activeList
    if (!selectedNiveauId.value && activeList.length) {
      const preferredId = userStore.niveau_pays?.id
      const match = preferredId ? activeList.find(n => Number(n.id) === Number(preferredId)) : null
      selectedNiveauId.value = match ? match.id : activeList[0].id
    }
  } catch (error) {
    console.error('Erreur lors du chargement des niveaux:', error)
    niveauxError.value = 'Impossible de récupérer les niveaux pour le moment.'
  } finally {
    niveauxLoading.value = false
  }
}

async function handleSubscribe(card) {
  const priceId = card?.priceId
  if (!priceId) {
    showErrorToast('Ce plan doit encore être configuré (Price ID manquant).')
    return
  }
  pendingPriceId.value = priceId
  pendingPlanName.value = card?.title || 'OptiTAB'
  await loadLevels()
  if (!niveaux.value.length) {
    showErrorToast('Impossible de proposer les niveaux pour le moment, réessaie plus tard.')
    pendingPriceId.value = ''
    pendingPlanName.value = ''
    return
  }
  if (!selectedNiveauId.value) {
    selectedNiveauId.value = niveaux.value[0].id
  }
  showLevelModal.value = true
}

const closeLevelModal = () => {
  if (submitting.value) return
  showLevelModal.value = false
  pendingPriceId.value = ''
  pendingPlanName.value = ''
}

async function confirmSubscription() {
  if (!pendingPriceId.value) {
    closeLevelModal()
    return
  }
  if (!selectedNiveauId.value) {
    showErrorToast('Choisis un niveau pour continuer.')
    return
  }
  if (!userStore.isAuthenticated) {
    checkoutIntentStore.setIntent({
      priceId: pendingPriceId.value,
      niveauId: selectedNiveauId.value,
      planName: pendingPlanName.value,
      niveauLabel: selectedNiveauLabel.value,
      source: 'home-pricing'
    })
    showInfoToast('Crée ton compte gratuit pour finaliser le paiement.', 6000)
    closeLevelModal()
    openModal(MODAL_IDS.REGISTER)
    return
  }
  try {
    submitting.value = true
    const { data } = await createCheckoutSession(pendingPriceId.value, {
      niveau_pays_id: selectedNiveauId.value
    })
    const redirectUrl = data?.checkout_url || data?.url
    if (redirectUrl) {
      window.location.href = redirectUrl
    } else {
      showErrorToast("Impossible d'ouvrir la page de paiement. Réessaie plus tard.")
    }
  } catch (err) {
    console.error(err)
    showErrorToast("Une erreur est survenue lors de la création du paiement.")
  } finally {
    submitting.value = false
    showLevelModal.value = false
    pendingPriceId.value = ''
    pendingPlanName.value = ''
  }
}
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;

.pricing-plans-section {
  padding: 80px 0;
  background: #f8f9fa;
}

.pricing-header {
  max-width: 800px;
  margin: 0 auto 60px;
  text-align: center;
  padding: 0 2vw;
}

.pricing-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #0f172a;
  margin-bottom: 16px;
  line-height: 1.2;
}

.pricing-highlight {
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.pricing-desc {
  font-size: 1.15rem;
  color: #475569;
  line-height: 1.6;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Modal styles */
.level-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}

.level-modal {
  background: #fff;
  border-radius: 20px;
  max-width: 520px;
  width: 100%;
  padding: 2rem;
  position: relative;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: transparent;
  border: none;
  font-size: 1.5rem;
  color: #64748b;
  cursor: pointer;
  
  &:hover {
    color: #0f172a;
  }
}

.modal-header {
  text-align: center;
  margin-bottom: 1.5rem;
  
  h3 {
    font-size: 1.5rem;
    margin: 0.5rem 0;
    color: #0f172a;
  }
}

.modal-eyebrow {
  text-transform: uppercase;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  color: #6366f1;
  margin: 0;
}

.modal-subtitle {
  font-size: 0.95rem;
  color: #475569;
  margin: 0.5rem 0 0;
}

.modal-body {
  margin-bottom: 1rem;
}

.modal-loading {
  text-align: center;
  padding: 2rem 0;
  
  .spinner {
    width: 48px;
    height: 48px;
    border: 4px solid rgba(42, 56, 183, 0.1);
    border-top-color: #2a38b7;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin: 0 auto 20px;
  }
  
  p {
    color: #64748b;
    font-size: 1rem;
  }
}

.modal-error {
  text-align: center;
  color: #dc2626;
}

.modal-refresh {
  margin-top: 1rem;
  background: #f1f5f9;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
}

.modal-select-group {
  label {
    display: block;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: #0f172a;
  }
}

.modal-select-wrapper select {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  padding: 0.85rem 1rem;
  font-size: 1rem;
  background: #f8fafc;
  
  &:focus {
    outline: none;
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
  }
}

.modal-hint {
  margin: 0.5rem 0 0;
  font-size: 0.85rem;
  color: #64748b;
}

.modal-selection {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #eef2ff;
  color: #4338ca;
  border-radius: 8px;
  font-weight: 600;
}

.modal-signup-hint {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: #0f172a;
  background: #f8fafc;
  border-radius: 12px;
  padding: 0.85rem 1rem;
  border: 1px dashed #c7d2fe;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.modal-btn {
  border: none;
  border-radius: 14px;
  padding: 0.85rem 1.6rem;
  font-weight: 700;
  cursor: pointer;
}

.modal-btn.secondary {
  background: #f1f5f9;
  color: #0f172a;
}

.modal-btn.primary {
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  color: #fff;
  min-width: 220px;
  display: inline-flex;
  justify-content: center;
}

.spinner.small {
  width: 28px;
  height: 28px;
  border-width: 3px;
  margin: 0 auto 0.8rem;
}

@media (max-width: 768px) {
  .pricing-plans-section {
    padding: 60px 0;
  }
  
  .pricing-header {
    margin-bottom: 48px;
  }
  
  .pricing-title {
    font-size: 2rem;
  }
  
  .pricing-desc {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .pricing-title {
    font-size: 1.75rem;
  }
}
</style>
