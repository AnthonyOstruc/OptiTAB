<template>
  <div class="subscription-manager">
    <div class="subscription-card">
      <div class="card-header">
        <div v-if="!isParentWithOnlyGiftedSubs" class="status-badge" :class="statusClass">
          {{ statusText }}
        </div>
        <button class="refresh-btn" :disabled="isRefreshing || subscriptionStore.loading" @click="refreshSubscription">
          <ArrowPathIcon class="btn-icon" :class="{ spinning: isRefreshing || subscriptionStore.loading }" />
        </button>
      </div>

      <div v-if="inlineMessage" class="inline-message" :class="inlineMessageType">
        <InformationCircleIcon class="inline-icon" />
        <span>{{ inlineMessage }}</span>
      </div>

      <!-- Section abonnements des enfants (en haut pour les parents) -->
      <div v-if="giftedSubscriptions.length" class="gifted-section gifted-section--top">
        <div class="gifted-header">
          <h4>Abonnements de vos enfants</h4>
          <p>Gérez les accès souscrits pour vos enfants.</p>
        </div>
        <div class="gifted-grid">
          <div
            v-for="gift in giftedSubscriptions"
            :key="gift.stripe_subscription_id || gift.started_at"
            class="gifted-card"
          >
            <!-- En-tête avec infos enfant -->
            <div class="gifted-child-header">
              <div class="gifted-child-avatar">
                {{ giftBeneficiaryInitials(gift) }}
              </div>
              <div class="gifted-child-info">
                <p class="gifted-child-name">{{ giftBeneficiaryFullName(gift) }}</p>
                <p class="gifted-child-email">{{ gift.beneficiary?.email || '—' }}</p>
              </div>
            </div>

            <!-- Détails de l'abonnement -->
            <div class="gifted-details">
              <div class="gifted-detail-row">
                <span class="gifted-label">Plan</span>
                <span class="gifted-value">{{ giftPlanLabel(gift) }}</span>
              </div>
              <div v-if="giftLevelLabel(gift)" class="gifted-detail-row">
                <span class="gifted-label">Niveau</span>
                <span class="gifted-value">{{ giftLevelLabel(gift) }}</span>
              </div>
              <div class="gifted-detail-row">
                <span class="gifted-label">Statut</span>
                <span class="gifted-value" :class="giftStatusClass(gift)">{{ giftStatusLabel(gift) }}</span>
              </div>
              <div class="gifted-detail-row">
                <span class="gifted-label">Accès jusqu'au</span>
                <span class="gifted-value">{{ giftAccessUntilLabel(gift) }}</span>
              </div>
              <div class="gifted-detail-row">
                <span class="gifted-label">Renouvellement</span>
                <span class="gifted-value">{{ giftRenewalDateLabel(gift) }}</span>
              </div>
            </div>

            <!-- Actions de gestion -->
            <div class="gifted-actions">
              <template v-if="gift.cancel_at_period_end">
                <button
                  class="gifted-reactivate-btn"
                  :disabled="isGiftReactivating(gift)"
                  @click="reactivateGiftedSubscription(gift)"
                >
                  <ArrowPathIcon class="btn-icon" />
                  {{ isGiftReactivating(gift) ? 'Réactivation…' : 'Réactiver' }}
                </button>
              </template>
              <template v-else>
                <button
                  class="gifted-cancel-btn"
                  :disabled="isGiftCancelling(gift)"
                  @click="confirmGiftCancellation(gift)"
                >
                  <XMarkIcon class="btn-icon" />
                  {{ isGiftCancelling(gift) ? 'Annulation…' : 'Résilier' }}
                </button>
              </template>
            </div>
          </div>
        </div>
      </div>

      <!-- Section passes offerts aux enfants (parents) -->
      <div v-if="giftedPasses.length" class="gifted-section gifted-section--passes">
        <div class="gifted-header">
          <h4>Passes de vos enfants</h4>
          <p>Passes ponctuels achetés pour vos enfants.</p>
        </div>
        <div class="gifted-grid">
          <div
            v-for="pass in giftedPasses"
            :key="`pass-${pass.id}`"
            class="gifted-card gifted-card--pass"
          >
            <!-- En-tête avec infos enfant -->
            <div class="gifted-child-header">
              <div class="gifted-child-avatar">
                {{ giftPassBeneficiaryInitials(pass) }}
              </div>
              <div class="gifted-child-info">
                <p class="gifted-child-name">{{ giftPassBeneficiaryFullName(pass) }}</p>
                <p class="gifted-child-email">{{ pass.beneficiary?.email || '—' }}</p>
              </div>
            </div>

            <!-- Détails du pass -->
            <div class="gifted-details">
              <div class="gifted-detail-row">
                <span class="gifted-label">Pass</span>
                <span class="gifted-value">{{ pass.plan_name }}</span>
              </div>
              <div v-if="giftPassLevelLabel(pass)" class="gifted-detail-row">
                <span class="gifted-label">Niveau</span>
                <span class="gifted-value">{{ giftPassLevelLabel(pass) }}</span>
              </div>
              <div class="gifted-detail-row">
                <span class="gifted-label">Statut</span>
                <span class="gifted-value" :class="pass.is_active ? 'status-active' : 'status-expired'">
                  {{ pass.is_active ? 'Actif' : 'Expiré' }}
                </span>
              </div>
              <div class="gifted-detail-row">
                <span class="gifted-label">Expiration</span>
                <span class="gifted-value">{{ formatPassExpiration(pass) }}</span>
              </div>
              <div class="gifted-detail-row">
                <span class="gifted-label">Type</span>
                <span class="gifted-value">Paiement unique (sans renouvellement)</span>
              </div>
            </div>

            <!-- Badge pass -->
            <div class="gifted-pass-badge">
              <span>Pass ponctuel</span>
            </div>
          </div>
        </div>
      </div>

      <div v-if="isCardLoading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>Chargement de ton abonnement…</p>
      </div>

      <div v-else-if="hasSubscription" class="subscription-details">
        <div class="plan-overview">
          <div class="plan-heading">
            <p class="eyebrow">Plan actuel</p>
            <h3>{{ subscription.plan_name || '—' }}</h3>
            <p v-if="planPriceLabel" class="plan-price">{{ planPriceLabel }}</p>
            <p v-else-if="planBillingLabel" class="plan-period">{{ planBillingLabel }}</p>
            <p v-if="hasMultipleSubscriptionOptions && displayedSubscriptionTitle" class="plan-level-pill">
              <span class="pill-label">Affichage :</span> <span class="pill-value">{{ displayedSubscriptionTitle }}</span>
            </p>
            <div v-if="hasMultipleSubscriptionOptions" class="plan-level-switcher">
              <label for="subscription-level-switch">Voir une autre classe</label>
              <div class="plan-level-switcher-control">
                <select
                  id="subscription-level-switch"
                  v-model="viewSubscriptionKey"
                >
                  <option
                    v-for="option in subscriptionLevelOptions"
                    :key="option.key"
                    :value="option.key"
                  >
                    {{ option.title }}
                  </option>
                </select>
                <p class="plan-level-switcher-hint">
                  Tes autres abonnements, sans changer de classe.
                </p>
              </div>
            </div>
          </div>
          <div class="plan-meta">
            <div class="meta-item">
              <span class="meta-label">Statut</span>
              <span class="meta-value">{{ statusText }}</span>
              <span v-if="statusDescription" class="meta-hint">{{ statusDescription }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">{{ renewalLabel }}</span>
              <span class="meta-value">{{ renewalDateLabel }}</span>
              <span class="meta-hint">{{ renewalHint }}</span>
            </div>
            <div v-if="subscriptionLevelLabel" class="meta-item">
              <span class="meta-label">Classe incluse</span>
              <span class="meta-value">{{ subscriptionLevelLabel }}</span>
              <span class="meta-hint">Un abonnement couvre une classe.</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Abonné depuis</span>
              <span class="meta-value">{{ subscriptionStartLabel }}</span>
              <span v-if="subscriptionStartHint" class="meta-hint">{{ subscriptionStartHint }}</span>
            </div>
            <div v-if="subscription.trial_end" class="meta-item meta-item--trial">
              <span class="meta-label">Essai gratuit</span>
              <span class="meta-value">{{ formatDate(subscription.trial_end) }}</span>
              <span class="meta-hint">{{ trialCountdownText }}</span>
            </div>
          </div>
        </div>

        <div v-if="unlockedLevelsWithSubscriptions.length" class="levels-access-section">
          <h4 class="levels-title">Classes débloquées</h4>
          <div class="levels-grid">
            <div v-for="level in unlockedLevelsWithSubscriptions" :key="level.id" class="level-card">
              <div class="level-info">
                <p class="level-name">{{ level.nom }}</p>
                <p v-if="level.pays?.nom" class="level-pays">{{ level.pays.nom }}</p>
                <p v-if="level.subscription" class="level-status-text">
                  {{ levelSubscriptionStatus(level.subscription) }}
                </p>
              </div>
              <div class="level-actions">
                <template v-if="level.subscription">
                  <template v-if="level.subscription.cancel_at_period_end">
                    <span class="level-status">
                      Résiliation le {{ formatDate(level.subscription.current_period_end) }}
                    </span>
                    <button
                      v-if="!level.subscription.is_gift_received"
                      class="level-reactivate-btn"
                      :disabled="isLevelReactivating(level.subscription)"
                      @click="reactivateSubscriptionForLevel(level.subscription)"
                    >
                      <ArrowPathIcon class="btn-icon" />
                      {{ isLevelReactivating(level.subscription) ? 'Réactivation…' : 'Se réabonner' }}
                    </button>
                  </template>
                  <template v-else-if="level.subscription.is_gift_received">
                    <span class="level-gift-notice">
                      Abonnement offert par un parent
                    </span>
                  </template>
                  <button
                    v-else
                    class="level-cancel-btn"
                    :disabled="isLevelCancelling(level.subscription)"
                    @click="confirmLevelCancellation(level)"
                  >
                    <XMarkIcon class="btn-icon" />
                    {{ isLevelCancelling(level.subscription) ? 'Annulation…' : 'Arrêter cet abonnement' }}
                  </button>
                </template>
                <router-link
                  v-else
                  to="/billing"
                  class="level-upgrade-btn"
                >
                  <ArrowUpIcon class="btn-icon" />
                  S'abonner
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <div
          v-if="!subscription.is_active || subscription.status === 'canceled'"
          class="actions-section"
        >
          <div class="actions-buttons">
            <router-link 
              to="/billing" 
              class="upgrade-btn"
            >
              <ArrowUpIcon class="btn-icon" />
              Choisir un plan
            </router-link>
          </div>
        </div>

        <div class="invoices-section">
          <div class="invoices-header">
            <div class="invoices-header-content">
              <h4>Historique des factures</h4>
              <button class="refresh-btn" :disabled="invoicesLoading" @click="loadInvoices">
                <ArrowPathIcon class="btn-icon" :class="{ spinning: invoicesLoading }" />
              </button>
            </div>
            <p>Télécharge tes factures ou reçois-les par e-mail.</p>
          </div>

          <div v-if="invoicesLoading" class="invoice-loading">
            <div class="loading-spinner small"></div>
            <p>Chargement des factures…</p>
          </div>
          <div v-else-if="invoicesError" class="invoice-error">
            {{ invoicesError }}
          </div>
          <div v-else-if="!invoices.length" class="invoice-empty">
            Aucune facture disponible pour le moment.
          </div>
          <div v-else class="invoice-list">
            <div v-for="invoice in invoices" :key="invoice.id" class="invoice-row">
              <div class="invoice-info">
                <div class="invoice-label">
                  <p class="invoice-date">{{ formatDate(invoice.created_at) }}</p>
                </div>
                <p class="invoice-amount">{{ formatAmount(invoice.amount, invoice.currency) }}</p>
                <p class="invoice-desc">{{ invoiceDescription(invoice) }}</p>
                <p v-if="invoiceLevelLabel(invoice)" class="invoice-level">
                  Niveau : {{ invoiceLevelLabel(invoice) }}
                </p>
                <p v-if="invoicePeriodLabel(invoice)" class="invoice-period">{{ invoicePeriodLabel(invoice) }}</p>
                <p v-if="invoiceValidityLabel(invoice)" class="invoice-note">{{ invoiceValidityLabel(invoice) }}</p>
                <p v-if="invoiceCancellationLabel(invoice)" class="invoice-note">{{ invoiceCancellationLabel(invoice) }}</p>
              </div>
              <div class="invoice-actions">
                <a
                  v-if="invoice.invoice_pdf_url || invoice.hosted_invoice_url"
                  class="invoice-btn"
                  :href="invoice.invoice_pdf_url || invoice.hosted_invoice_url"
                  target="_blank"
                  rel="noopener"
                >
                  <DocumentArrowDownIcon class="btn-icon" />
                  Télécharger
                </a>
                <button
                  class="invoice-btn secondary"
                  :disabled="sendingInvoiceId === invoice.id"
                  @click="sendInvoiceEmail(invoice.id)"
                >
                  <EnvelopeIcon class="btn-icon" />
                  {{ sendingInvoiceId === invoice.id ? 'Envoi…' : 'Par e-mail' }}
                </button>
              </div>
            </div>
          </div>

          <div v-if="invoicesTotalPages > 1" class="invoice-pagination">
            <button
              class="pagination-btn"
              :disabled="invoicesPage <= 1 || invoicesLoading"
              @click="changeInvoicesPage(invoicesPage - 1)"
            >
              Précédent
            </button>
            <span class="pagination-info">Page {{ invoicesPage }} / {{ invoicesTotalPages }}</span>
            <button
              class="pagination-btn"
              :disabled="invoicesPage >= invoicesTotalPages || invoicesLoading"
              @click="changeInvoicesPage(invoicesPage + 1)"
            >
              Suivant
            </button>
          </div>
        </div>
      </div>

      <!-- Pas d'abonnement -->
      <div v-else-if="hasActivePass" class="pass-access">
        <div class="pass-header">
          <div>
            <p class="eyebrow">Pass actif</p>
            <h3>{{ passPlanLabel }}</h3>
            <p class="pass-subtitle">Accès complet à ta classe, sans renouvellement.</p>
          </div>
          <div class="pass-chip">
            Expire {{ passEndDateLabel }}
          </div>
        </div>
        <div class="pass-body">
          <div class="meta-item">
            <span class="meta-label">Fin de validité</span>
            <span class="meta-value">{{ passEndDateLabel }}</span>
            <span class="meta-hint">{{ passEndHint }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">Classe en accès</span>
            <span class="meta-value">{{ subscriptionLevelLabel || 'Ta classe actuelle' }}</span>
            <span class="meta-hint">Le pass suit la classe choisie dans ton compte.</span>
          </div>
        </div>
        <div class="actions-section">
          <div class="actions-buttons">
            <router-link to="/billing" class="upgrade-btn">
              <ArrowUpIcon class="btn-icon" />
              Passer sur un abonnement
            </router-link>
          </div>
        </div>
      </div>

      <div v-else-if="hasManualAccess" class="manual-access">
        <div class="manual-icon">
          <CheckIcon />
        </div>
        <h4>Accès premium accordé</h4>
        <p>{{ manualAccessDescription }}</p>
        <router-link to="/billing" class="get-started-btn">
          Gérer mon accès
        </router-link>
      </div>

      <div v-else class="no-subscription">
        <div class="no-sub-icon">
          <CreditCardIcon />
        </div>
        <h4>Aucun abonnement actif</h4>
        <p>Choisis une formule pour débloquer tous les cours, fiches et exercices corrigés de ta classe.</p>
        <router-link to="/billing" class="get-started-btn">
          Voir les formules
        </router-link>
      </div>
    </div>

    <!-- Confirmation de résiliation -->
    <Modal
      :is-open="showCancelModal"
      title="Résilier l’abonnement ?"
      :icon="ExclamationTriangleIcon"
      :can-close="!isConfirmingCancel"
      size="small"
      @close="closeCancelModal"
    >
      <p class="cancel-text">
        Tu vas résilier l’abonnement<template v-if="cancelTargetLevel?.nom"> <strong>« {{ cancelTargetLevel.nom }} »</strong></template>.
      </p>
      <p class="om-alert om-alert--info">L’accès reste ouvert jusqu’à la fin de la période en cours.</p>
      <template #footer>
        <button type="button" class="om-btn om-btn--ghost" :disabled="isConfirmingCancel" @click="closeCancelModal">Garder mon abonnement</button>
        <button type="button" class="om-btn om-btn--danger" :disabled="isConfirmingCancel" @click="confirmCancel">
          {{ isConfirmingCancel ? 'Résiliation…' : 'Confirmer la résiliation' }}
        </button>
      </template>
    </Modal>

    <!-- Confirmation de résiliation (abonnement offert à un enfant) -->
    <Modal
      :is-open="showGiftCancelModal"
      title="Résilier l’abonnement ?"
      :icon="ExclamationTriangleIcon"
      :can-close="!isConfirmingGiftCancel"
      size="small"
      @close="closeGiftCancelModal"
    >
      <p class="cancel-text">
        Vous allez résilier l’abonnement de <strong>{{ giftBeneficiaryFullName(cancelTargetGift) }}</strong>.
      </p>
      <p class="om-alert om-alert--info">Votre enfant garde l’accès jusqu’à la fin de la période en cours.</p>
      <template #footer>
        <button type="button" class="om-btn om-btn--ghost" :disabled="isConfirmingGiftCancel" @click="closeGiftCancelModal">Garder l’abonnement</button>
        <button type="button" class="om-btn om-btn--danger" :disabled="isConfirmingGiftCancel" @click="confirmGiftCancel">
          {{ isConfirmingGiftCancel ? 'Résiliation…' : 'Confirmer la résiliation' }}
        </button>
      </template>
    </Modal>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { 
  CheckIcon, 
  XMarkIcon, 
  ArrowUpIcon, 
  CreditCardIcon,
  ArrowPathIcon,
  InformationCircleIcon,
  DocumentArrowDownIcon,
  EnvelopeIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'
import Modal from '@/components/common/Modal.vue'
import { cancelSubscription as cancelSubscriptionApi, reactivateSubscription as reactivateSubscriptionApi, getInvoices, emailInvoice } from '@/api/subscriptions'
import { useSubscriptionStore } from '@/stores/subscription'
import { usePaysNiveauStore } from '@/stores/paysNiveau'
import { useUserStore } from '@/stores/user'
import { useToast } from '@/composables/useToast'

const subscriptionStore = useSubscriptionStore()
const paysNiveauStore = usePaysNiveauStore()
const userStore = useUserStore()
const { showToast } = useToast()

const defaultSubscription = {
  has_subscription: false,
  status: 'inactive',
  has_manual_access: false,
  plan_name: '',
  is_active: false,
  cancel_at_period_end: false,
  has_active_pass: false,
  active_pass_ends_at: null,
  features: [],
  unlocked_levels: [],
  subscriptions: []
}

const defaultFeatures = [
  'Accès complet aux cours OptiTAB',
  'Exercices illimités',
  'Suivi intelligent de la progression',
  'Nouveaux contenus en avant-première'
]

const inlineMessage = ref('')
const inlineMessageType = ref('neutral')
const isRefreshing = ref(false)
const initialLoadDone = ref(false)
const invoices = ref([])
const invoicesLoading = ref(false)
const invoicesError = ref('')
const sendingInvoiceId = ref(null)
const invoicesPage = ref(1)
const invoicesTotal = ref(0)
const invoicesPageSize = 3
const cancellingLevelKey = ref('')
const reactivatingLevelKey = ref('')
const viewSubscriptionKey = ref('')

// Pour la gestion des abonnements offerts (enfants)
const cancellingGiftKey = ref('')
const reactivatingGiftKey = ref('')
const showGiftCancelModal = ref(false)
const cancelTargetGift = ref(null)
const isConfirmingGiftCancel = ref(false)

// Modal de résiliation
const showCancelModal = ref(false)
const cancelTargetLevel = ref(null)
const isConfirmingCancel = ref(false)

const baseSubscription = computed(() => subscriptionStore.status || defaultSubscription)
const subscriptionsList = computed(() => {
  const list = baseSubscription.value.subscriptions || []
  return list.filter(sub => {
    const status = String(sub?.status || '').toLowerCase()
    const isActive = Boolean(sub?.is_active)
    if (status === 'canceled' && !isActive) return false
    return true
  })
})
const unlockedLevels = computed(() => baseSubscription.value.unlocked_levels || [])
const levelSubscriptionsMap = computed(() => {
  const map = new Map()
  ;(subscriptionsList.value || []).forEach(sub => {
    const levelId = sub?.niveau?.id
    if (levelId) {
      map.set(Number(levelId), sub)
    }
  })
  return map
})
const selectedLevelId = computed(() => {
  const activeLevel = paysNiveauStore.niveauPaysActuel?.id || userStore.niveau_pays?.id
  if (!activeLevel) return null
  const numeric = Number(activeLevel)
  return Number.isNaN(numeric) ? null : numeric
})
const selectedLevelSubscription = computed(() => {
  if (!selectedLevelId.value) return null
  return levelSubscriptionsMap.value.get(selectedLevelId.value) || null
})
const fallbackActiveSubscription = computed(() => {
  const list = subscriptionsList.value || []
  return list.find(sub => sub?.is_active) || list[0] || null
})

const buildSubscriptionIdentifier = (subscriptionItem) => {
  if (!subscriptionItem) return null
  const numericId = subscriptionItem.id || subscriptionItem.subscription_id
  if (numericId) {
    return {
      key: `id:${numericId}`,
      payload: { subscription_id: numericId }
    }
  }
  const stripeId = subscriptionItem.stripe_subscription_id || subscriptionItem.stripe_id
  if (stripeId) {
    return {
      key: stripeId,
      payload: { stripe_subscription_id: stripeId }
    }
  }
  return null
}

const formatLevelDisplay = (niveau) => {
  if (!niveau?.id) return ''
  const paysName = niveau.pays?.nom
  return paysName ? `${niveau.nom} · ${paysName}` : niveau.nom
}

const subscriptionLevelOptions = computed(() => {
  const list = subscriptionsList.value || []
  const base = baseSubscription.value
  const basePlanName = base?.plan_name || 'Abonnement OptiTAB'
  const options = []

  // Ajouter les abonnements (subscriptions récurrentes)
  list.forEach((sub, index) => {
    const identifier = buildSubscriptionIdentifier(sub)
    const key = identifier?.key || `sub-${index}`
    const levelLabel = formatLevelDisplay(sub.niveau)
    const planName = sub.plan?.name || basePlanName
    options.push({
      key,
      title: levelLabel || planName,
      subtitle: levelLabel ? planName : '',
      level: sub.niveau || null,
      subscription: sub,
      status: sub.status || '',
      isActive: Boolean(sub.is_active),
      isPass: false
    })
  })

  // Ajouter TOUS les passes actifs
  const activePasses = base?.active_passes || []
  activePasses.forEach((pass, index) => {
    const passLevelId = pass.niveau?.id
    const key = passLevelId ? `pass-${passLevelId}` : `pass-${index}`
    // Vérifier si ce niveau n'est pas déjà couvert par un abonnement
    const alreadyCovered = options.some(opt => opt.level?.id === passLevelId && !opt.isPass)
    if (!alreadyCovered) {
      const levelLabel = formatLevelDisplay(pass.niveau)
      options.push({
        key,
        title: levelLabel || pass.plan_name || 'Pass',
        subtitle: pass.plan_name || 'Pass actif',
        level: pass.niveau,
        subscription: {
          is_active: pass.is_active,
          status: 'active',
          current_period_start: pass.starts_at,
          current_period_end: pass.ends_at,
          plan: {
            name: pass.plan_name,
            stripe_price_id: pass.stripe_price_id,
            price: pass.plan_price,
            billing_period: pass.plan_billing_period,
            mode: 'one_time'
          },
          niveau: pass.niveau
        },
        status: 'active',
        isActive: pass.is_active,
        isPass: true
      })
    }
  })

  // Fallback pour ancien format (un seul pass)
  if (!activePasses.length && base?.has_active_pass && base?.pass_niveau) {
    const passLevelId = base.pass_niveau.id
    const alreadyCovered = options.some(opt => opt.level?.id === passLevelId)
    if (!alreadyCovered) {
      const levelLabel = formatLevelDisplay(base.pass_niveau)
      options.push({
        key: `pass-${passLevelId}`,
        title: levelLabel || base.active_pass_plan || 'Pass',
        subtitle: base.active_pass_plan || 'Pass actif',
        level: base.pass_niveau,
        subscription: {
          is_active: true,
          status: 'active',
          current_period_end: base.active_pass_ends_at,
          plan: {
            name: base.active_pass_plan,
            stripe_price_id: base.active_pass_price_id,
            price: base.active_pass_price,
            billing_period: base.active_pass_billing_period,
            mode: 'one_time'
          },
          niveau: base.pass_niveau
        },
        status: 'active',
        isActive: true,
        isPass: true
      })
    }
  }

  // Fallback si aucune option mais on a un abonnement de base
  if (!options.length && base?.has_subscription) {
    const levelLabel = formatLevelDisplay(base.subscription_niveau)
    options.push({
      key: 'base',
      title: levelLabel || basePlanName,
      subtitle: levelLabel ? basePlanName : '',
      level: base.subscription_niveau || null,
      subscription: null,
      status: base.status || '',
      isActive: Boolean(base.is_active),
      isPass: false
    })
  }

  return options
})

const hasMultipleSubscriptionOptions = computed(() => subscriptionLevelOptions.value.length > 1)

const currentViewOption = computed(() => {
  const options = subscriptionLevelOptions.value
  if (!options.length) return null
  if (viewSubscriptionKey.value) {
    return options.find(option => option.key === viewSubscriptionKey.value) || options[0]
  }
  return options[0]
})

// Détermine si l'option affichée actuellement est un pass (non récurrent)
const isCurrentViewPass = computed(() => {
  const option = currentViewOption.value
  if (!option) return false
  if (option.isPass) return true
  const planMode = option.subscription?.plan?.mode
  return planMode === 'one_time'
})

watch(
  [subscriptionLevelOptions, () => selectedLevelId.value],
  ([options, selectedLevel]) => {
    if (!options.length) {
      viewSubscriptionKey.value = ''
      return
    }
    const normalizedSelected = typeof selectedLevel === 'number' ? selectedLevel : null
    const preferredOption = normalizedSelected == null
      ? null
      : options.find(option => {
          const levelId = option.level?.id
          if (levelId == null) return false
          return Number(levelId) === normalizedSelected
        })

    if (!viewSubscriptionKey.value) {
      viewSubscriptionKey.value = preferredOption?.key || options[0].key
      return
    }

    const stillExists = options.some(option => option.key === viewSubscriptionKey.value)
    if (!stillExists) {
      viewSubscriptionKey.value = preferredOption?.key || options[0].key
    }
  },
  { immediate: true }
)

const resolvedViewSubscription = computed(() => (
  currentViewOption.value?.subscription ||
  selectedLevelSubscription.value ||
  fallbackActiveSubscription.value ||
  null
))

const displayedSubscriptionTitle = computed(() => currentViewOption.value?.title || '')

const subscription = computed(() => {
  const base = baseSubscription.value || defaultSubscription
  const source = resolvedViewSubscription.value
  if (!source) return base
  const planPayload = source.plan || {}
  const mergedFeatures = planPayload.features?.length ? planPayload.features : (base.features || defaultFeatures)
  const planCurrency = planPayload.currency ?? base.plan_currency ?? 'EUR'
  return {
    ...base,
    status: source.status || base.status,
    is_active: source.is_active ?? base.is_active,
    is_trial: source.is_trial ?? base.is_trial,
    days_remaining_trial: source.days_remaining_trial ?? base.days_remaining_trial,
    current_period_start: source.current_period_start || base.current_period_start,
    current_period_end: source.current_period_end || base.current_period_end,
    trial_end: source.trial_end || base.trial_end,
    cancel_at_period_end: source.cancel_at_period_end ?? base.cancel_at_period_end,
    plan_name: planPayload.name || base.plan_name,
    plan_id: planPayload.id ?? base.plan_id,
    plan_type: planPayload.plan_type ?? base.plan_type,
    plan_mode: planPayload.mode ?? base.plan_mode,
    plan_billing_period: planPayload.billing_period ?? base.plan_billing_period,
    plan_price: planPayload.price ?? base.plan_price,
    plan_currency: planCurrency,
    plan_stripe_price_id: planPayload.stripe_price_id ?? base.plan_stripe_price_id,
    subscription_niveau: source.niveau || base.subscription_niveau,
    stripe_subscription_id: source.stripe_subscription_id || base.stripe_subscription_id,
    subscription_id: source.id || base.subscription_id,
    features: mergedFeatures
  }
})
const features = computed(() => subscription.value.features?.length ? subscription.value.features : defaultFeatures)
const hasSubscription = computed(() => Boolean(subscription.value.has_subscription || subscription.value.has_active_pass))
const hasManualAccess = computed(() => Boolean(subscription.value.has_manual_access))
const manualAccessLevels = computed(() => {
  const levels = subscription.value.manual_access_levels
  return Array.isArray(levels) ? levels : []
})
const hasManualAccessGlobal = computed(() => {
  if (!hasManualAccess.value) return false
  if (typeof subscription.value.has_manual_access_global === 'boolean') {
    return Boolean(subscription.value.has_manual_access_global)
  }
  return manualAccessLevels.value.length === 0
})
const manualAccessDescription = computed(() => {
  if (hasManualAccessGlobal.value) {
    return "Un administrateur vous a offert l'accès complet aux contenus premium sans abonnement actif."
  }
  if (!manualAccessLevels.value.length) {
    return "Un administrateur vous a offert un accès premium ciblé."
  }
  const labels = manualAccessLevels.value
    .map(level => level?.nom)
    .filter(Boolean)
    .slice(0, 3)
  const suffix = manualAccessLevels.value.length > 3 ? ', ...' : ''
  return `Un administrateur vous a offert l'accès premium pour les niveaux : ${labels.join(', ')}${suffix}.`
})
const isCardLoading = computed(() => !initialLoadDone.value && (subscriptionStore.loading || !subscriptionStore.status))
const cancellationScheduled = computed(() => Boolean(subscription.value.cancel_at_period_end))
const hasActiveAccess = computed(() => subscriptionStore.hasAccess)
const hasActivePass = computed(() => Boolean(subscription.value.has_active_pass))
const isParentWithOnlyGiftedSubs = computed(() => {
  // Utilisateur payeur qui n'a pas d'abonnement propre mais gère des abonnements enfants
  return !hasSubscription.value && giftedSubscriptions.value.length > 0
})
const unlockedLevelsWithSubscriptions = computed(() => {
  const merged = new Map()

  unlockedLevels.value.forEach(level => {
    if (!level?.id) return
    const id = Number(level.id)
    if (Number.isNaN(id) || merged.has(id)) return
    merged.set(id, { ...level, subscription: levelSubscriptionsMap.value.get(id) || null })
  })

  ;(subscriptionsList.value || []).forEach(sub => {
    const niveau = sub?.niveau
    if (!niveau?.id) return
    const id = Number(niveau.id)
    if (Number.isNaN(id)) return
    const existing = merged.get(id) || { ...niveau }
    merged.set(id, {
      ...existing,
      subscription: sub
    })
  })

  return Array.from(merged.values())
})
const giftedSubscriptions = computed(() =>
  (baseSubscription.value.gifted_subscriptions || []).filter(gift => gift?.is_active)
)
const giftedPasses = computed(() =>
  (baseSubscription.value.gifted_passes || []).filter(pass => pass?.is_active && !pass?.is_revoked)
)

// Helpers pour les passes offerts
const giftPassBeneficiaryInitials = (pass) => {
  const first = (pass.beneficiary?.first_name || '').charAt(0).toUpperCase()
  const last = (pass.beneficiary?.last_name || '').charAt(0).toUpperCase()
  return first + last || '?'
}
const giftPassBeneficiaryFullName = (pass) => {
  const first = pass.beneficiary?.first_name || ''
  const last = pass.beneficiary?.last_name || ''
  return `${first} ${last}`.trim() || pass.beneficiary?.email || 'Bénéficiaire'
}
const giftPassLevelLabel = (pass) => {
  if (!pass.niveau) return ''
  const paysName = pass.niveau.pays?.nom
  return paysName ? `${pass.niveau.nom} · ${paysName}` : pass.niveau.nom
}

const invoicesTotalPages = computed(() => {
  if (!invoicesTotal.value) return 1
  return Math.max(1, Math.ceil(invoicesTotal.value / invoicesPageSize))
})

const resolveSubscriptionField = (field) => {
  const directValue = subscription.value?.[field]
  if (directValue) {
    return directValue
  }
  const activeMatch = subscriptionsList.value.find(sub => sub?.is_active && sub?.[field])
  if (activeMatch && activeMatch[field]) {
    return activeMatch[field]
  }
  const anyMatch = subscriptionsList.value.find(sub => sub?.[field])
  if (anyMatch && anyMatch[field]) {
    return anyMatch[field]
  }
  return null
}

const isLevelCancelling = (subscriptionItem) => {
  const identifier = buildSubscriptionIdentifier(subscriptionItem)
  if (!identifier) return false
  return cancellingLevelKey.value === identifier.key
}

const isLevelReactivating = (subscriptionItem) => {
  const identifier = buildSubscriptionIdentifier(subscriptionItem)
  if (!identifier) return false
  return reactivatingLevelKey.value === identifier.key
}

const reactivateSubscriptionForLevel = async (subscriptionItem) => {
  const identifier = buildSubscriptionIdentifier(subscriptionItem)
  if (!identifier) {
    const message = 'Impossible d\'identifier cet abonnement.'
    setInlineMessage(message, 'error')
    showToast(message, 'error')
    return
  }
  try {
    reactivatingLevelKey.value = identifier.key
    await reactivateSubscriptionApi(identifier.payload)
    await loadSubscription(true)
    await loadInvoices()
    const successMessage = 'Abonnement réactivé avec succès !'
    setInlineMessage(successMessage, 'success')
    showToast('Abonnement réactivé', 'success')
  } catch (error) {
    console.error('Erreur lors de la réactivation:', error)
    const serverMessage = error.response?.data?.message || error.response?.data?.error || 'Impossible de réactiver cet abonnement.'
    setInlineMessage(serverMessage, 'error')
    showToast(serverMessage, 'error')
  } finally {
    reactivatingLevelKey.value = ''
  }
}

const confirmLevelCancellation = (level) => {
  if (!level?.subscription) return
  cancelTargetLevel.value = level
  showCancelModal.value = true
}

const closeCancelModal = () => {
  showCancelModal.value = false
  cancelTargetLevel.value = null
  isConfirmingCancel.value = false
}

// Gestion de la touche Échap pour fermer les modaux
const handleEscapeKey = (e) => {
  if (e.key === 'Escape') {
    if (showCancelModal.value) {
      closeCancelModal()
    }
    if (showGiftCancelModal.value) {
      closeGiftCancelModal()
    }
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleEscapeKey)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscapeKey)
})

const confirmCancel = async () => {
  if (!cancelTargetLevel.value?.subscription) return
  isConfirmingCancel.value = true
  await cancelSubscriptionForLevel(cancelTargetLevel.value.subscription)
  closeCancelModal()
}

const statusClass = computed(() => {
  switch (subscription.value.status) {
    case 'active': return 'status-active'
    case 'trialing': return 'status-trial'
    case 'past_due': return 'status-warning'
    case 'canceled': return 'status-canceled'
    case 'manual': return 'status-manual'
    default: return 'status-inactive'
  }
})

const statusText = computed(() => {
  if (subscription.value.cancel_at_period_end && subscription.value.status !== 'canceled') {
    return 'Annulation programmée'
  }
  switch (subscription.value.status) {
    case 'active': return 'Actif'
    case 'trialing': return 'Activation en cours'
    case 'past_due': return 'Paiement en retard'
    case 'canceled': return 'Annulé'
    case 'manual': return 'Accès manuel'
    default: return 'Inactif'
  }
})

const statusDescription = computed(() => {
  // Pass actif : afficher un message spécifique
  if (isCurrentViewPass.value && hasActiveAccess.value) {
    return 'Pass actif, accès valide jusqu\'à expiration.'
  }
  if (subscription.value.cancel_at_period_end && subscription.value.status !== 'canceled' && hasActiveAccess.value) {
    return 'Accès maintenu jusqu\'à la date de fin actuelle.'
  }
  if (!hasActiveAccess.value) {
    if (subscription.value.status === 'canceled') {
      return 'Abonnement annulé et accès interrompu immédiatement.'
    }
    return 'Aucun accès actif sur cet abonnement.'
  }
  switch (subscription.value.status) {
    case 'active': return 'Renouvellement automatique en place.'
    case 'trialing': return 'Profitez de votre période d\'essai.'
    case 'past_due': return 'Veuillez mettre à jour votre moyen de paiement.'
    case 'canceled': return 'Accès maintenu jusqu\'à la fin de la période.'
    case 'manual': return 'Accès accordé par l\'équipe OptiTAB.'
    default: return ''
  }
})

const billingPeriodMap = {
  monthly: { short: 'mois', adjective: 'mensuelle' },
  yearly: { short: 'an', adjective: 'annuelle' },
  weekly: { short: 'semaine', adjective: 'hebdomadaire' },
  daily: { short: 'jour', adjective: 'quotidienne' }
}

const billingPeriodAliases = {
  month: 'monthly',
  months: 'monthly',
  mensuel: 'monthly',
  mensuelle: 'monthly',
  year: 'yearly',
  years: 'yearly',
  annual: 'yearly',
  annually: 'yearly',
  annuel: 'yearly',
  annuellement: 'yearly',
  week: 'weekly',
  weeks: 'weekly',
  hebdo: 'weekly',
  hebdomadaire: 'weekly',
  day: 'daily',
  days: 'daily',
  quotidien: 'daily'
}

const normalizeBillingPeriodKey = (period) => {
  if (!period) return ''
  const normalized = String(period).toLowerCase()
  if (billingPeriodMap[normalized]) return normalized
  return billingPeriodAliases[normalized] || normalized
}

const resolveBillingPeriodMeta = (period) => {
  const key = normalizeBillingPeriodKey(period)
  return billingPeriodMap[key] || null
}

const setInlineMessage = (message, type = 'neutral') => {
  inlineMessage.value = message
  inlineMessageType.value = `msg-${type}`
}

const clearInlineMessage = () => {
  inlineMessage.value = ''
  inlineMessageType.value = 'neutral'
}

const loadSubscription = async (force = false) => {
  try {
    await subscriptionStore.fetchStatus({ force })
    clearInlineMessage()
  } catch (error) {
    console.error('Erreur lors du chargement de l\'abonnement:', error)
    setInlineMessage('Impossible de récupérer votre abonnement. Réessayez dans un instant.', 'error')
  } finally {
    initialLoadDone.value = true
  }
}

const refreshSubscription = async () => {
  try {
    isRefreshing.value = true
    await loadSubscription(true)
    await loadInvoices()
    showToast('Abonnement synchronisé', 'info')
  } finally {
    isRefreshing.value = false
  }
}

const cancelSubscriptionForLevel = async (subscriptionItem) => {
  const identifier = buildSubscriptionIdentifier(subscriptionItem)
  if (!identifier) {
    const message = 'Impossible d\'identifier cet abonnement.'
    setInlineMessage(message, 'error')
    showToast(message, 'error')
    return
  }
  try {
    cancellingLevelKey.value = identifier.key
    await cancelSubscriptionApi(identifier.payload)
    await loadSubscription(true)
    await loadInvoices()
    const successMessage = 'La résiliation de ce niveau est programmée.'
    setInlineMessage(successMessage, 'success')
    showToast('Abonnement annulé pour ce niveau', 'success')
  } catch (error) {
    console.error('Erreur lors de l\'annulation du niveau:', error)
    const serverMessage = error.response?.data?.message || error.response?.data?.error || 'Impossible d\'annuler cet abonnement.'
    setInlineMessage(serverMessage, 'error')
    showToast(serverMessage, 'error')
  } finally {
    cancellingLevelKey.value = ''
  }
}

// Fonctions pour gérer les abonnements offerts (enfants)
const buildGiftIdentifier = (gift) => {
  if (!gift) return null
  const stripeId = gift.stripe_subscription_id
  if (stripeId) {
    return { key: stripeId, payload: { stripe_subscription_id: stripeId } }
  }
  return null
}

const isGiftCancelling = (gift) => {
  const identifier = buildGiftIdentifier(gift)
  if (!identifier) return false
  return cancellingGiftKey.value === identifier.key
}

const isGiftReactivating = (gift) => {
  const identifier = buildGiftIdentifier(gift)
  if (!identifier) return false
  return reactivatingGiftKey.value === identifier.key
}

const confirmGiftCancellation = (gift) => {
  if (!gift) return
  cancelTargetGift.value = gift
  showGiftCancelModal.value = true
}

const closeGiftCancelModal = () => {
  showGiftCancelModal.value = false
  cancelTargetGift.value = null
  isConfirmingGiftCancel.value = false
}

const confirmGiftCancel = async () => {
  if (!cancelTargetGift.value) return
  isConfirmingGiftCancel.value = true
  await cancelGiftedSubscription(cancelTargetGift.value)
  closeGiftCancelModal()
}

const cancelGiftedSubscription = async (gift) => {
  const identifier = buildGiftIdentifier(gift)
  if (!identifier) {
    showToast('Impossible d\'identifier cet abonnement.', 'error')
    return
  }
  try {
    cancellingGiftKey.value = identifier.key
    await cancelSubscriptionApi(identifier.payload)
    await loadSubscription(true)
    showToast('Résiliation programmée pour cet enfant', 'success')
  } catch (error) {
    console.error('Erreur lors de la résiliation:', error)
    const serverMessage = error.response?.data?.message || error.response?.data?.error || 'Impossible de résilier cet abonnement.'
    showToast(serverMessage, 'error')
  } finally {
    cancellingGiftKey.value = ''
  }
}

const reactivateGiftedSubscription = async (gift) => {
  const identifier = buildGiftIdentifier(gift)
  if (!identifier) {
    showToast('Impossible d\'identifier cet abonnement.', 'error')
    return
  }
  try {
    reactivatingGiftKey.value = identifier.key
    await reactivateSubscriptionApi(identifier.payload)
    await loadSubscription(true)
    showToast('Abonnement réactivé pour cet enfant', 'success')
  } catch (error) {
    console.error('Erreur lors de la réactivation:', error)
    const serverMessage = error.response?.data?.message || error.response?.data?.error || 'Impossible de réactiver cet abonnement.'
    showToast(serverMessage, 'error')
  } finally {
    reactivatingGiftKey.value = ''
  }
}

const loadInvoices = async (page = invoicesPage.value) => {
  try {
    invoicesLoading.value = true
    invoicesError.value = ''
    const { data } = await getInvoices({ limit: invoicesPageSize, page })
    invoices.value = data?.invoices || []
    invoicesTotal.value = Number(data?.total || invoicesTotal.value || 0)
    invoicesPage.value = Number(data?.page || page || 1)
  } catch (error) {
    invoices.value = []
    invoicesError.value = 'Impossible de charger vos factures pour le moment.'
    console.error('Erreur chargement factures:', error)
  } finally {
    invoicesLoading.value = false
  }
}

const changeInvoicesPage = async (nextPage) => {
  const target = Number(nextPage)
  if (!target || Number.isNaN(target)) return
  if (target < 1 || target > invoicesTotalPages.value) return
  if (target === invoicesPage.value) return
  invoicesPage.value = target
  await loadInvoices(target)
}

const parseDateSafe = (value) => {
  if (!value) return null
  if (value instanceof Date) {
    return Number.isNaN(value.getTime()) ? null : value
  }
  let working = value
  if (typeof working === 'number') {
    const fromNumber = new Date(working)
    return Number.isNaN(fromNumber.getTime()) ? null : fromNumber
  }
  if (typeof working !== 'string') {
    return null
  }
  let iso = working.trim()
  if (!iso) return null
  if (iso.includes(' ')) {
    iso = iso.replace(' ', 'T')
  }
  if (iso.includes('.')) {
    iso = iso.replace(/(\.\d{3})\d+/, '$1')
  }
  if (iso.endsWith('+00:00')) {
    iso = iso.slice(0, -6) + 'Z'
  }
  if (/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$/.test(iso)) {
    iso += 'Z'
  }
  const parsed = new Date(iso)
  if (!Number.isNaN(parsed.getTime())) {
    return parsed
  }
  const fallback = new Date(working)
  return Number.isNaN(fallback.getTime()) ? null : fallback
}

const formatDate = (dateInput) => {
  const date = parseDateSafe(dateInput)
  if (!date) return '—'
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatDateWithTime = (dateInput) => {
  const date = parseDateSafe(dateInput)
  if (!date) return '—'
  return date.toLocaleString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const isOneDayPassName = (planName) => {
  const normalized = String(planName || '').toLowerCase()
  return normalized.includes('1 jour') || normalized.includes('1jour')
}

const formatPassExpiration = (pass) => {
  if (!pass || !pass.ends_at) return '—'
  // Pour les pass 1 jour, afficher aussi l'heure
  if (isOneDayPassName(pass.plan_name)) {
    return formatDateWithTime(pass.ends_at)
  }
  return formatDate(pass.ends_at)
}

const giftBeneficiaryLabel = (gift) => {
  if (!gift) return '—'
  const beneficiary = gift.beneficiary || {}
  const nameParts = [beneficiary.first_name, beneficiary.last_name].filter(Boolean)
  const fullName = nameParts.join(' ').trim()
  if (fullName) {
    return fullName
  }
  if (beneficiary.display_name) {
    return beneficiary.display_name
  }
  return 'Compte enfant'
}

const giftBeneficiaryFullName = (gift) => {
  if (!gift) return 'Enfant'
  const beneficiary = gift.beneficiary || {}
  const nameParts = [beneficiary.first_name, beneficiary.last_name].filter(Boolean)
  const fullName = nameParts.join(' ').trim()
  return fullName || beneficiary.display_name || beneficiary.email || 'Enfant'
}

const giftBeneficiaryInitials = (gift) => {
  if (!gift) return '?'
  const beneficiary = gift.beneficiary || {}
  const first = (beneficiary.first_name || '').charAt(0).toUpperCase()
  const last = (beneficiary.last_name || '').charAt(0).toUpperCase()
  if (first && last) return first + last
  if (first) return first
  if (beneficiary.email) return beneficiary.email.charAt(0).toUpperCase()
  return '?'
}

const giftLevelLabel = (gift) => {
  if (!gift) return ''
  if (gift.niveau) return formatLevelDisplay(gift.niveau)
  return gift.niveau_label || ''
}

const giftPlanLabel = (gift) => {
  if (!gift) return 'Abonnement'
  return gift.plan?.name || 'Abonnement'
}

const giftStatusLabel = (gift) => {
  if (!gift) return '—'
  if (gift.cancel_at_period_end && gift.current_period_end) {
    return 'Annulation programmée'
  }
  const status = String(gift.status || '').toLowerCase()
  if (status === 'active') return 'Actif'
  if (status === 'trialing') return 'Essai'
  if (status === 'past_due') return 'Paiement en retard'
  if (status === 'canceled') return 'Annulé'
  if (status === 'unpaid') return 'Impayé'
  return status || '—'
}

const giftStatusClass = (gift) => {
  if (!gift) return ''
  if (gift.cancel_at_period_end) return 'status-warning'
  const status = String(gift.status || '').toLowerCase()
  if (status === 'active') return 'status-active'
  if (status === 'trialing') return 'status-trial'
  if (status === 'past_due' || status === 'unpaid') return 'status-danger'
  if (status === 'canceled') return 'status-canceled'
  return ''
}

const giftAccessUntilLabel = (gift) => {
  if (!gift) return '—'
  const dateValue = gift.current_period_end || gift.trial_end || ''
  return dateValue ? formatDate(dateValue) : '—'
}

const giftRenewalDateLabel = (gift) => {
  if (!gift) return '—'
  if (gift.cancel_at_period_end) return 'Annulation programmée'
  const status = String(gift.status || '').toLowerCase()
  if (['canceled', 'unpaid'].includes(status)) return 'Annulé'
  const dateValue = gift.current_period_end || gift.trial_end || ''
  return dateValue ? formatDate(dateValue) : '—'
}

const levelSubscriptionStatus = (subscriptionItem) => {
  if (!subscriptionItem) return ''
  if (subscriptionItem.cancel_at_period_end && subscriptionItem.current_period_end) {
    return `Résiliation programmée · accès jusqu'au ${formatDate(subscriptionItem.current_period_end)}`
  }
  const status = String(subscriptionItem.status || '').toLowerCase()
  if (status === 'trialing') return 'Essai en cours'
  if (status === 'past_due') return 'Paiement en retard'
  if (status === 'incomplete') return 'Paiement en attente'
  if (subscriptionItem.is_active === false) return 'Inactif'
  return 'Abonnement actif'
}

const formatAmount = (value, currency = 'EUR') => {
  if (value === null || value === undefined) return '—'
  const amount = Number(value) || 0
  try {
    return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: String(currency || 'EUR').toUpperCase() }).format(amount)
  } catch {
    return `${amount.toFixed(2).replace('.', ',')} €`
  }
}

const formatPlanPriceValue = (value, currency = 'EUR') => {
  if (value === null || value === undefined) return ''
  const amount = Number(value)
  if (Number.isNaN(amount)) return ''
  try {
    return new Intl.NumberFormat('fr-FR', { style: 'currency', currency }).format(amount)
  } catch (error) {
    console.error('Erreur format prix plan:', error)
    return `${amount.toFixed(2)} ${currency}`
  }
}

const formatRelativeDistance = (dateInput) => {
  const target = parseDateSafe(dateInput)
  if (!target) return ''
  const now = new Date()
  const diffMs = now - target
  if (diffMs < 0) return ''
  const diffDays = Math.floor(diffMs / 86400000)
  if (diffDays === 0) return 'Aujourd\'hui'
  if (diffDays === 1) return 'Depuis 1 jour'
  if (diffDays < 30) return `Depuis ${diffDays} jours`
  const diffMonths = Math.floor(diffDays / 30)
  if (diffMonths === 1) return 'Depuis 1 mois'
  if (diffMonths < 12) return `Depuis ${diffMonths} mois`
  const diffYears = Math.floor(diffMonths / 12)
  return diffYears <= 1 ? 'Depuis 1 an' : `Depuis ${diffYears} ans`
}

const addPeriodToDate = (dateInput, period) => {
  if (!dateInput || !period) return null
  const date = parseDateSafe(dateInput)
  if (!date) return null
  const result = new Date(date.getTime())
  switch (normalizeBillingPeriodKey(period)) {
    case 'monthly':
      result.setMonth(result.getMonth() + 1)
      break
    case 'yearly':
      result.setFullYear(result.getFullYear() + 1)
      break
    case 'weekly':
      result.setDate(result.getDate() + 7)
      break
    case 'daily':
      result.setDate(result.getDate() + 1)
      break
    default:
      return null
  }
  return result.toISOString()
}

const invoicePlanMode = (invoice) => {
  const mode = (invoice?.plan_mode || '').toLowerCase()
  if (['subscription', 'one_time'].includes(mode)) return mode
  if (invoice?.stripe_invoice_id) return 'subscription'
  const desc = (invoice?.description || '').toLowerCase()
  if (desc.includes('paiement pour')) return 'subscription'
  if (desc.includes('pass')) return 'one_time'
  return 'payment'
}

const invoiceType = (invoice) => {
  const mode = invoicePlanMode(invoice)
  if (mode === 'subscription') return 'subscription'
  if (mode === 'one_time') return 'pass'
  return 'payment'
}

const invoicePlanName = (invoice) => (invoice?.plan_name || '').trim()

const invoiceDescription = (invoice) => {
  if (!invoice) return 'Facture OptiTAB'
  const type = invoiceType(invoice)
  const planName = invoicePlanName(invoice)
  if (type === 'subscription') {
    if (planName) return `Abonnement ${planName}`
    const desc = invoice.description?.replace(/paiement pour/i, '').trim()
    if (desc) return `Abonnement ${desc}`
    const currentPlan = subscription.value.plan_name || 'OptiTAB'
    return `Abonnement ${currentPlan}`
  }
  if (type === 'pass') {
    if (planName) return `Pass ${planName}`
    return invoice.description || 'Pass OptiTAB'
  }
  return invoice.description || 'Facture OptiTAB'
}

const invoiceLevelLabel = (invoice) => {
  if (!invoice) return ''
  return invoice.niveau_label || ''
}

const findSubscriptionForInvoice = (invoice) => {
  if (!invoice) return null
  const niveauId = Number(invoice.niveau_id)
  if (!niveauId || Number.isNaN(niveauId)) return null
  return levelSubscriptionsMap.value.get(niveauId) || null
}

const invoicePeriodLabel = (invoice) => {
  if (!invoice) return ''
  const start = invoice.period_start ? formatDate(invoice.period_start) : ''
  const end = invoice.period_end ? formatDate(invoice.period_end) : ''
  if (start && end) return `Période : ${start} → ${end}`
  if (end) return `Fin de période : ${end}`
  if (start) return `Début de période : ${start}`
  return ''
}

const invoiceValidityLabel = (invoice) => {
  if (!invoice?.period_end) return ''
  const endDate = parseDateSafe(invoice.period_end)
  if (!endDate) return ''
  const now = new Date()
  if (endDate.getTime() >= now.getTime()) {
    return `Accès valable jusqu'au ${formatDate(endDate)}`
  }
  return `Accès terminé le ${formatDate(endDate)}`
}

const invoiceCancellationLabel = (invoice) => {
  const subscriptionItem = findSubscriptionForInvoice(invoice)
  if (!subscriptionItem) return ''
  const endDate = subscriptionItem.current_period_end
  if (subscriptionItem.cancel_at_period_end && endDate) {
    return `Résiliation prévue le ${formatDate(endDate)}`
  }
  const status = String(subscriptionItem.status || '').toLowerCase()
  if (status === 'canceled' && endDate) {
    return `Résilié depuis le ${formatDate(endDate)}`
  }
  return ''
}

const resolvedCurrentPeriodStart = computed(() => resolveSubscriptionField('current_period_start'))
const resolvedCurrentPeriodEnd = computed(() => resolveSubscriptionField('current_period_end'))
const resolvedTrialEnd = computed(() => resolveSubscriptionField('trial_end'))

const periodStart = computed(() => resolvedCurrentPeriodStart.value || null)
const renewalDateValue = computed(() => (
  resolvedCurrentPeriodEnd.value ||
  subscription.value.active_pass_ends_at ||
  resolvedTrialEnd.value ||
  null
))
const subscriptionStart = computed(() =>
  subscription.value.started_at ||
  resolvedCurrentPeriodStart.value ||
  null
)
const fallbackRenewalDate = computed(() => {
  if (renewalDateValue.value) return null
  if (subscription.value.plan_mode === 'one_time') return null
  const base = periodStart.value || subscriptionStart.value
  if (!base) return null
  return addPeriodToDate(base, subscription.value.plan_billing_period || subscription.value.plan_period)
})
const shouldShowAccessEndDate = computed(() =>
  hasActiveAccess.value ||
  cancellationScheduled.value ||
  Boolean(subscription.value.has_active_pass)
)
const displayRenewalDate = computed(() => {
  if (!shouldShowAccessEndDate.value) return null
  return renewalDateValue.value || fallbackRenewalDate.value
})
const shouldIncludeTimeForAccessEndDate = computed(() => {
  if (!isCurrentViewPass.value) return false
  if (isOneDayPassName(subscription.value.plan_name || subscription.value.active_pass_plan)) {
    return true
  }

  const billingPeriod = String(
    subscription.value.plan_billing_period || subscription.value.plan_period || ''
  ).toLowerCase()
  if (billingPeriod === 'daily') {
    return true
  }

  const startDate = parseDateSafe(subscriptionStart.value)
  const endDate = parseDateSafe(displayRenewalDate.value)
  if (!startDate || !endDate) return false
  const durationMs = endDate.getTime() - startDate.getTime()
  return durationMs > 0 && durationMs <= 36 * 3_600_000
})

const planPriceLabel = computed(() => {
  const formattedPrice = formatPlanPriceValue(
    subscription.value.plan_price,
    subscription.value.plan_currency || 'EUR'
  )
  if (!formattedPrice) return ''
  // Pour les passes (paiements uniques), pas de période
  if (isCurrentViewPass.value) {
    return `${formattedPrice} (paiement unique)`
  }
  const billingPeriod = subscription.value.plan_billing_period || subscription.value.plan_period
  const meta = resolveBillingPeriodMeta(billingPeriod)
  return meta?.short ? `${formattedPrice} / ${meta.short}` : formattedPrice
})

const planBillingLabel = computed(() => {
  // Pour les passes, pas de facturation récurrente
  if (isCurrentViewPass.value) return ''
  const billingPeriod = subscription.value.plan_billing_period || subscription.value.plan_period
  const meta = resolveBillingPeriodMeta(billingPeriod)
  return meta?.adjective ? `Facturation ${meta.adjective}` : ''
})
const passEndDateLabel = computed(() => {
  if (isOneDayPassName(subscription.value.active_pass_plan || subscription.value.plan_name)) {
    return formatDateWithTime(subscription.value.active_pass_ends_at)
  }
  const billingPeriod = String(
    subscription.value.active_pass_billing_period || subscription.value.plan_billing_period || ''
  ).toLowerCase()
  if (billingPeriod === 'daily') {
    return formatDateWithTime(subscription.value.active_pass_ends_at)
  }
  return formatDate(subscription.value.active_pass_ends_at)
})
const passEndHint = computed(() => {
  const target = parseDateSafe(subscription.value.active_pass_ends_at)
  if (!target) return 'Le pass expirera automatiquement sans renouvellement.'
  const now = new Date()
  const diffMs = target.getTime() - now.getTime()
  if (diffMs <= 0) return 'Pass expiré. Relance un achat pour continuer.'
  const diffHours = Math.ceil(diffMs / 3_600_000)
  if (diffHours < 24) {
    return `Expire dans ${diffHours} heure${diffHours > 1 ? 's' : ''}`
  }
  const diffDays = Math.ceil(diffHours / 24)
  return `Expire dans ${diffDays} jour${diffDays > 1 ? 's' : ''}`
})

const subscriptionLevelLabel = computed(() => formatLevelDisplay(subscription.value.subscription_niveau))
const passPlanLabel = computed(() => subscription.value.active_pass_plan || 'Pass actif')

const renewalLabel = computed(() => {
  if (isCurrentViewPass.value) return 'Expiration'
  if (!shouldShowAccessEndDate.value) return 'Accès terminé'
  if (cancellationScheduled.value) return 'Fin programmée'
  return subscription.value.is_active ? 'Renouvellement' : 'Fin de période'
})
const renewalDateLabel = computed(() => {
  if (shouldIncludeTimeForAccessEndDate.value) {
    return formatDateWithTime(displayRenewalDate.value)
  }
  return formatDate(displayRenewalDate.value)
})
const renewalHint = computed(() => {
  if (isCurrentViewPass.value) {
    return 'Pass à usage unique, sans renouvellement automatique.'
  }
  if (!displayRenewalDate.value) {
    return hasActiveAccess.value
      ? 'Dates en synchronisation avec Stripe.'
      : 'Abonnement inactif. Choisissez une nouvelle offre pour réactiver l\'accès.'
  }
  if (!hasActiveAccess.value) {
    return 'Abonnement arrêté immédiatement. Cette date correspond à la dernière période Stripe.'
  }
  if (cancellationScheduled.value) {
    return 'Annulation programmée, aucun prélèvement après cette date.'
  }
  if (subscription.value.is_active) {
    return 'Le prélèvement se fera automatiquement à cette date.'
  }
  return 'Votre accès reste ouvert jusqu\'à cette date.'
})

const periodEndHint = computed(() => {
  if (isCurrentViewPass.value) {
    return 'Pass à usage unique, l\'accès s\'arrête automatiquement à cette date.'
  }
  if (!displayRenewalDate.value) {
    return hasActiveAccess.value
      ? 'Même après annulation, votre accès reste actif jusqu\'à la fin de la période en cours.'
      : 'Aucun accès actif actuellement.'
  }
  if (!hasActiveAccess.value) {
    return 'Accès interrompu. Cette date provient de la dernière période déclarée par Stripe.'
  }
  if (cancellationScheduled.value) {
    return 'Annulation en cours, accès actif jusqu\'à cette date.'
  }
  return 'Même en cas d\'annulation, l\'accès reste actif jusqu\'à cette date.'
})

const subscriptionStartLabel = computed(() => formatDate(subscriptionStart.value))
const subscriptionStartHint = computed(() => formatRelativeDistance(subscriptionStart.value))

const trialCountdownText = computed(() => {
  if (!subscription.value.trial_end) return ''
  const remaining = Math.max(subscription.value.days_remaining_trial || 0, 0)
  if (remaining > 1) return `${remaining} jours restants`
  if (remaining === 1) return 'Dernier jour d\'essai'
  return 'Se termine aujourd\'hui'
})

const timelineSecondaryLabel = computed(() => {
  if (isCurrentViewPass.value) return 'Expiration du pass'
  if (!hasActiveAccess.value) return 'Accès interrompu'
  if (cancellationScheduled.value) return 'Annulation programmée'
  return subscription.value.is_active ? 'Accès garanti' : 'Fin programmée'
})

const sendInvoiceEmail = async (invoiceId) => {
  if (!invoiceId) return
  try {
    sendingInvoiceId.value = invoiceId
    await emailInvoice(invoiceId)
    showToast('Facture envoyée par email', 'success')
  } catch (error) {
    console.error('Erreur envoi facture:', error)
    const message = error.response?.data?.detail || 'Impossible d\'envoyer cette facture.'
    showToast(message, 'error')
    setInlineMessage(message, 'error')
  } finally {
    sendingInvoiceId.value = null
  }
}

watch(
  () => subscriptionStore.error,
  (err) => {
    if (err) {
      setInlineMessage('Impossible de mettre à jour votre abonnement pour le moment.', 'error')
    }
  }
)

// Lifecycle
onMounted(() => {
  loadSubscription(true)
  loadInvoices()
})
</script>

<style scoped>
/* Mon abonnement : style de l'espace (variables --es-*, avec repli). */
.subscription-manager {
  --sm-navy: var(--es-navy, #1b3c8e);
  --sm-ink: var(--es-ink, #172033);
  --sm-soft: var(--es-ink-soft, #3a4357);
  --sm-muted: var(--es-muted, #667085);
  --sm-line: var(--es-line, #e3e7ef);
  --sm-bg: var(--es-bg, #f5f7fb);
  --sm-green: var(--es-green-700, #3b8544);
  --sm-green-50: var(--es-green-50, #eaf4ea);
  --sm-orange: var(--es-orange-700, #a8620f);
  --sm-orange-50: var(--es-orange-50, #fdf3e6);
  --sm-red: var(--es-red-700, #b42318);
  font-family: var(--es-font, 'Montserrat', sans-serif);
  color: var(--sm-ink);
}

.subscription-card {
  padding: 24px;
  border: 1px solid var(--sm-line);
  border-radius: var(--es-radius, 16px);
  background: #fff;
  box-shadow: var(--es-shadow, 0 4px 16px rgba(16, 24, 40, 0.05));
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 20px;
}

/* Pastilles d'état */
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 999px;
  background: var(--sm-bg);
  font-size: 13px;
  font-weight: 700;
  color: var(--sm-muted);
}

.status-badge::before {
  content: '';
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: currentColor;
}

.status-badge.status-active,
.status-badge.status-manual {
  background: var(--sm-green-50);
  color: var(--sm-green);
}

.status-badge.status-trial {
  background: var(--es-navy-50, #eef1f8);
  color: var(--sm-navy);
}

.status-badge.status-warning {
  background: var(--sm-orange-50);
  color: var(--sm-orange);
}

.status-badge.status-canceled {
  background: #fef3f2;
  color: var(--sm-red);
}

.gifted-value.status-active { color: var(--sm-green); }
.gifted-value.status-trial { color: var(--sm-navy); }
.gifted-value.status-warning { color: var(--sm-orange); }
.gifted-value.status-danger,
.gifted-value.status-canceled,
.gifted-value.status-expired { color: var(--sm-red); }

/* Boutons */
.refresh-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  margin-left: auto;
  border: 1px solid var(--sm-line);
  border-radius: 10px;
  background: #fff;
  color: var(--sm-muted);
  cursor: pointer;
}

.refresh-btn:hover {
  color: var(--sm-navy);
  border-color: var(--es-line-strong, #cfd6e3);
}

.refresh-btn:disabled {
  cursor: default;
  opacity: 0.6;
}

.btn-icon {
  width: 17px;
  height: 17px;
  flex-shrink: 0;
}

.spinning {
  animation: sm-tourne 0.9s linear infinite;
}

@keyframes sm-tourne {
  to { transform: rotate(360deg); }
}

.upgrade-btn,
.get-started-btn,
.level-upgrade-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 44px;
  padding: 0 20px;
  border-radius: 12px;
  background: var(--sm-navy);
  font-size: 15px;
  font-weight: 600;
  color: #fff !important;
  text-decoration: none;
}

.level-upgrade-btn {
  min-height: 36px;
  padding: 0 14px;
  font-size: 14px;
}

.upgrade-btn:hover,
.get-started-btn:hover,
.level-upgrade-btn:hover {
  background: var(--es-navy-dark, #122a66);
}

.level-cancel-btn,
.gifted-cancel-btn,
.level-reactivate-btn,
.gifted-reactivate-btn,
.invoice-btn,
.pagination-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  min-height: 36px;
  padding: 0 14px;
  border: 1px solid var(--sm-line);
  border-radius: 10px;
  background: #fff;
  font: 600 14px var(--es-font, sans-serif);
  color: var(--sm-soft);
  text-decoration: none;
  cursor: pointer;
  transition: border-color 0.15s ease, color 0.15s ease, background-color 0.15s ease;
}

.level-cancel-btn:hover,
.gifted-cancel-btn:hover {
  border-color: #f4c7c3;
  background: #fef3f2;
  color: var(--sm-red);
}

.level-reactivate-btn,
.gifted-reactivate-btn {
  border-color: transparent;
  background: var(--sm-green-50);
  color: var(--sm-green);
}

.invoice-btn:hover,
.pagination-btn:hover:not(:disabled) {
  border-color: var(--sm-navy);
  color: var(--sm-navy);
}

button:disabled {
  cursor: default;
  opacity: 0.6;
}

/* Message en ligne */
.inline-message {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 18px;
  padding: 12px 14px;
  border-radius: 12px;
  background: var(--sm-bg);
  font-size: 14px;
  color: var(--sm-soft);
}

.inline-message.msg-success {
  background: var(--sm-green-50);
  color: var(--sm-green);
}

.inline-message.msg-error {
  background: #fef3f2;
  color: var(--sm-red);
}

.inline-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

/* Chargement */
.loading-state,
.invoice-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 32px 0;
  font-size: 14px;
  color: var(--sm-muted);
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--sm-line);
  border-top-color: var(--sm-navy);
  border-radius: 50%;
  animation: sm-tourne 0.8s linear infinite;
}

.loading-spinner.small {
  width: 22px;
  height: 22px;
  border-width: 2px;
}

/* Plan actuel */
.plan-overview {
  display: grid;
  gap: 20px;
}

.eyebrow {
  margin: 0 0 4px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--sm-muted);
}

.plan-heading h3,
.pass-header h3 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: var(--sm-ink);
}

.plan-price,
.plan-period {
  margin: 4px 0 0;
  font-size: 15px;
  font-weight: 600;
  color: var(--sm-navy);
}

.plan-level-pill {
  display: inline-flex;
  gap: 4px;
  margin: 10px 0 0;
  padding: 4px 12px;
  border-radius: 999px;
  background: var(--es-navy-50, #eef1f8);
  font-size: 13px;
  color: var(--sm-navy);
}

.pill-value {
  font-weight: 700;
}

.plan-level-switcher {
  margin-top: 14px;
}

.plan-level-switcher label {
  display: block;
  margin-bottom: 6px;
  font-size: 13px;
  font-weight: 700;
  color: var(--sm-ink);
}

.plan-level-switcher select {
  height: 40px;
  min-width: 240px;
  padding: 0 12px;
  border: 1px solid var(--es-line-strong, #cfd6e3);
  border-radius: 10px;
  font: 600 14px var(--es-font, sans-serif);
}

.plan-level-switcher-hint {
  margin: 6px 0 0;
  font-size: 12.5px;
  color: var(--sm-muted);
}

.plan-meta,
.pass-body {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 12px;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 14px 16px;
  border-radius: 12px;
  background: var(--sm-bg);
}

.meta-item--trial {
  background: var(--es-navy-50, #eef1f8);
}

.meta-label {
  font-size: 12.5px;
  font-weight: 600;
  color: var(--sm-muted);
}

.meta-value {
  font-size: 16px;
  font-weight: 700;
  color: var(--sm-ink);
}

.meta-hint {
  font-size: 12.5px;
  line-height: 1.4;
  color: var(--sm-muted);
}

/* Sections (classes, factures, abonnements offerts) */
.levels-access-section,
.invoices-section,
.actions-section {
  margin-top: 28px;
  padding-top: 22px;
  border-top: 1px solid var(--sm-line);
}

.levels-title,
.invoices-header h4,
.gifted-header h4 {
  margin: 0;
  font-size: 17px;
  font-weight: 700;
  color: var(--sm-ink);
}

.invoices-header p,
.gifted-header p {
  margin: 4px 0 0;
  font-size: 14px;
  color: var(--sm-muted);
}

.invoices-header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.levels-grid {
  display: grid;
  gap: 10px;
  margin-top: 14px;
}

.level-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 16px;
  border: 1px solid var(--sm-line);
  border-radius: 12px;
}

.level-name {
  margin: 0;
  font-size: 15px;
  font-weight: 700;
}

.level-pays,
.level-status-text {
  margin: 2px 0 0;
  font-size: 13px;
  color: var(--sm-muted);
}

.level-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
}

.level-status {
  font-size: 13px;
  font-weight: 600;
  color: var(--sm-orange);
}

.level-gift-notice {
  font-size: 13px;
  font-weight: 600;
  color: var(--sm-green);
}

.actions-buttons {
  display: flex;
  justify-content: center;
}

/* Factures */
.invoice-list {
  margin-top: 14px;
  border: 1px solid var(--sm-line);
  border-radius: 12px;
  overflow: hidden;
}

.invoice-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 16px;
}

.invoice-row + .invoice-row {
  border-top: 1px solid var(--sm-line);
}

.invoice-info {
  display: grid;
  grid-template-columns: auto 1fr;
  column-gap: 14px;
  align-items: baseline;
  min-width: 0;
}

.invoice-label {
  grid-row: span 2;
  min-width: 150px;
}

.invoice-date {
  margin: 0;
  font-size: 13px;
  font-weight: 600;
  color: var(--sm-muted);
  white-space: nowrap;
}

.invoice-amount {
  margin: 0;
  font-size: 15px;
  font-weight: 700;
}

.invoice-desc,
.invoice-level,
.invoice-period,
.invoice-note {
  grid-column: 2;
  margin: 2px 0 0;
  font-size: 13px;
  line-height: 1.4;
  color: var(--sm-muted);
}

.invoice-actions {
  display: flex;
  flex-shrink: 0;
  gap: 8px;
}

.invoice-btn.secondary {
  color: var(--sm-muted);
}

.invoice-empty,
.invoice-error {
  margin-top: 14px;
  padding: 18px;
  border: 1px dashed var(--es-line-strong, #cfd6e3);
  border-radius: 12px;
  font-size: 14px;
  text-align: center;
  color: var(--sm-muted);
}

.invoice-error {
  border-color: #f4c7c3;
  color: var(--sm-red);
}

.invoice-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: 14px;
}

.pagination-info {
  font-size: 13px;
  color: var(--sm-muted);
}

/* Abonnements et pass offerts aux enfants */
.gifted-section {
  margin-bottom: 24px;
  padding-bottom: 22px;
  border-bottom: 1px solid var(--sm-line);
}

.gifted-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
  margin-top: 14px;
}

.gifted-card {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 16px;
  border: 1px solid var(--sm-line);
  border-radius: 14px;
}

.gifted-child-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.gifted-child-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  border-radius: 50%;
  background: var(--sm-navy);
  font-size: 14px;
  font-weight: 700;
  color: #fff;
}

.gifted-child-name {
  margin: 0;
  font-size: 15px;
  font-weight: 700;
}

.gifted-child-email {
  margin: 0;
  font-size: 13px;
  color: var(--sm-muted);
}

.gifted-details {
  display: grid;
  gap: 6px;
}

.gifted-detail-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  font-size: 13.5px;
}

.gifted-label {
  color: var(--sm-muted);
}

.gifted-value {
  font-weight: 600;
  text-align: right;
}

.gifted-actions {
  display: flex;
  justify-content: flex-end;
}

.gifted-pass-badge {
  align-self: flex-start;
  padding: 3px 10px;
  border-radius: 999px;
  background: var(--sm-bg);
  font-size: 12.5px;
  font-weight: 700;
  color: var(--sm-muted);
}

/* Pass, accès offert, aucun abonnement */
.pass-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.pass-subtitle {
  margin: 4px 0 0;
  font-size: 14px;
  color: var(--sm-muted);
}

.pass-chip {
  padding: 4px 12px;
  border-radius: 999px;
  background: var(--sm-orange-50);
  font-size: 13px;
  font-weight: 700;
  white-space: nowrap;
  color: var(--sm-orange);
}

.manual-access,
.no-subscription {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 28px 12px 12px;
  text-align: center;
}

.manual-icon,
.no-sub-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  margin-bottom: 6px;
  border-radius: 16px;
  background: var(--es-navy-50, #eef1f8);
  color: var(--sm-navy);
}

.manual-icon {
  background: var(--sm-green-50);
  color: var(--sm-green);
}

.manual-icon svg,
.no-sub-icon svg {
  width: 28px;
  height: 28px;
}

.manual-access h4,
.no-subscription h4 {
  margin: 0;
  font-size: 19px;
  font-weight: 700;
}

.manual-access p,
.no-subscription p {
  max-width: 420px;
  margin: 0 0 12px;
  font-size: 14.5px;
  line-height: 1.55;
  color: var(--sm-muted);
}

/* Fenêtres de résiliation */
.cancel-text {
  margin: 0 0 12px;
  line-height: 1.55;
  color: var(--om-ink-soft, #2c3550);
}

/* Téléphone */
@media (max-width: 640px) {
  .subscription-card {
    padding: 18px;
  }

  .plan-heading h3,
  .pass-header h3 {
    font-size: 21px;
  }

  .level-card,
  .invoice-row {
    flex-direction: column;
    align-items: stretch;
  }

  .level-actions,
  .invoice-actions {
    justify-content: flex-start;
  }

  .invoice-actions .invoice-btn {
    flex: 1;
  }

  .pass-header {
    flex-direction: column;
  }

  .plan-level-switcher select {
    width: 100%;
    min-width: 0;
    font-size: 16px;
  }
}
</style>
