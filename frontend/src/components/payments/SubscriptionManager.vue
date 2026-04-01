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
              <span class="pass-badge-icon">🎫</span>
              <span>Pass ponctuel</span>
            </div>
          </div>
        </div>
      </div>

      <div v-if="isCardLoading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>Mise à jour de votre abonnement…</p>
      </div>

      <div v-else-if="hasSubscription" class="subscription-details">
        <div class="plan-overview">
          <div class="plan-heading">
            <p class="eyebrow">Plan actuel</p>
            <h3>{{ subscription.plan_name || '—' }}</h3>
            <p v-if="planPriceLabel" class="plan-price">{{ planPriceLabel }}</p>
            <p v-else-if="planBillingLabel" class="plan-period">{{ planBillingLabel }}</p>
            <p v-if="displayedSubscriptionTitle" class="plan-level-pill">
              <span class="pill-label">Affichage :</span> <span class="pill-value">{{ displayedSubscriptionTitle }}</span>
            </p>
            <div v-if="hasMultipleSubscriptionOptions" class="plan-level-switcher">
              <label for="subscription-level-switch">Voir un autre niveau</label>
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
                  Consultez vos autres abonnements sans changer de niveau.
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
              <span class="meta-label">Niveau inclus</span>
              <span class="meta-value">{{ subscriptionLevelLabel }}</span>
              <span class="meta-hint">Un abonnement = un seul niveau. Contactez-nous pour changer.</span>
            </div>
            <div v-if="subscription.trial_end" class="meta-item meta-item--trial">
              <span class="meta-label">Essai gratuit</span>
              <span class="meta-value">{{ formatDate(subscription.trial_end) }}</span>
              <span class="meta-hint">{{ trialCountdownText }}</span>
            </div>
          </div>
        </div>

        <div class="timeline-row">
          <div class="timeline-card">
            <span class="timeline-label">Début de l'abonnement</span>
            <span class="timeline-date">{{ subscriptionStartLabel }}</span>
            <span v-if="subscriptionStartHint" class="timeline-hint">{{ subscriptionStartHint }}</span>
          </div>
          <div class="timeline-card">
            <span class="timeline-label">{{ timelineSecondaryLabel }}</span>
            <span class="timeline-date">{{ renewalDateLabel }}</span>
            <span class="timeline-hint">{{ periodEndHint }}</span>
          </div>
        </div>

        <div class="features-section">
          <h4 class="features-title">Fonctionnalités incluses :</h4>
          <ul class="features-list">
            <li v-for="feature in features" :key="feature" class="feature-item">
              <CheckIcon class="feature-icon" />
              {{ feature }}
            </li>
          </ul>
        </div>

        <div v-if="unlockedLevelsWithSubscriptions.length" class="levels-access-section">
          <h4 class="levels-title">Niveaux débloqués</h4>
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
            <p>Retrouvez vos factures et envoyez-les par email en un clic.</p>
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
                  {{ sendingInvoiceId === invoice.id ? 'Envoi...' : 'Envoyer par email' }}
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
            <p class="pass-subtitle">Accès temporaire à ton niveau actuel.</p>
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
            <span class="meta-label">Niveau en accès</span>
            <span class="meta-value">{{ subscriptionLevelLabel || 'Votre niveau actuel' }}</span>
            <span class="meta-hint">Le pass suit ton niveau sélectionné.</span>
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
        <p>Choisissez un plan pour accéder à toutes les fonctionnalités premium.</p>
        <router-link to="/billing" class="get-started-btn">
          Voir les offres
        </router-link>
      </div>
    </div>

    <!-- Modal de confirmation de résiliation -->
    <Teleport to="body">
      <div v-if="showCancelModal" class="modal-overlay" @click.self="closeCancelModal">
        <div class="modal-card" @click.stop>
          <div class="modal-header">
            <h3>Résilier l'abonnement</h3>
            <button class="modal-close" @click="closeCancelModal">×</button>
          </div>
          <div class="modal-body">
            <p>
              Êtes-vous sûr de vouloir résilier l'abonnement
              <strong v-if="cancelTargetLevel?.nom">« {{ cancelTargetLevel.nom }} »</strong> ?
            </p>
            <p class="modal-hint">
              Vous conserverez l'accès à ce niveau jusqu'à la fin de la période en cours.
            </p>
          </div>
          <div class="modal-actions">
            <button class="cancel-btn" @click="closeCancelModal">Annuler</button>
            <button 
              class="confirm-btn confirm-btn--danger" 
              :disabled="isConfirmingCancel"
              @click="confirmCancel"
            >
              {{ isConfirmingCancel ? 'Résiliation...' : 'Confirmer' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Modal de confirmation de résiliation pour enfant -->
    <Teleport to="body">
      <div v-if="showGiftCancelModal" class="modal-overlay" @click.self="closeGiftCancelModal">
        <div class="modal-card" @click.stop>
          <div class="modal-header">
            <h3>Résilier l'abonnement</h3>
            <button class="modal-close" @click="closeGiftCancelModal">×</button>
          </div>
          <div class="modal-body">
            <p>
              Êtes-vous sûr de vouloir résilier l'abonnement de
              <strong>{{ giftBeneficiaryFullName(cancelTargetGift) }}</strong> ?
            </p>
            <p class="modal-hint">
              Votre enfant conservera l'accès jusqu'à la fin de la période en cours.
            </p>
          </div>
          <div class="modal-actions">
            <button class="cancel-btn" @click="closeGiftCancelModal">Annuler</button>
            <button 
              class="confirm-btn confirm-btn--danger" 
              :disabled="isConfirmingGiftCancel"
              @click="confirmGiftCancel"
            >
              {{ isConfirmingGiftCancel ? 'Résiliation...' : 'Confirmer' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>

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
  EnvelopeIcon
} from '@heroicons/vue/24/outline'
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
  return `${amount.toFixed(2)} ${currency}`
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
.subscription-manager {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.subscription-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #f3f4f6;
}

.refresh-btn {
  border: 1px solid #e2e8f0;
  background: #fff;
  border-radius: 999px;
  width: 36px;
  height: 36px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.refresh-btn:not(:disabled):hover {
  background: #f8fafc;
  border-color: #cbd5f5;
}

.btn-icon {
  width: 1.2rem;
  height: 1.2rem;
}

.btn-icon.spinning {
  animation: spin 1s linear infinite;
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

.status-manual {
  background: #ecfdf5;
  color: #047857;
}

.inline-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 2rem;
  padding: 0.85rem 1rem;
  border-radius: 0.75rem;
  font-size: 0.9rem;
}

.inline-message .inline-icon {
  width: 1.1rem;
  height: 1.1rem;
}

.inline-message.msg-success {
  background: #ecfdf5;
  color: #065f46;
}

.inline-message.msg-error {
  background: #fef2f2;
  color: #991b1b;
}

.inline-message.msg-neutral {
  background: #f8fafc;
  color: #0f172a;
}

.loading-state {
  padding: 2rem;
  text-align: center;
}

.loading-spinner {
  width: 2.5rem;
  height: 2.5rem;
  border: 3px solid #e2e8f0;
  border-top-color: #2563eb;
  border-radius: 50%;
  margin: 0 auto 1rem;
  animation: spin 1s linear infinite;
}

.loading-spinner.small {
  width: 1.75rem;
  height: 1.75rem;
}

.subscription-details {
  padding: 0;
}

.plan-overview {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  padding: 2rem;
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 70%);
  border-bottom: 1px solid #f1f5f9;
}

.plan-heading {
  flex: 1 1 100%;
  min-width: 0;
}

.plan-heading .eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.75rem;
  font-weight: 600;
  color: #4f46e5;
  margin-bottom: 0.4rem;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

.plan-heading h3 {
  margin: 0 0 0.35rem;
  font-size: 1.75rem;
  color: #0f172a;
  word-break: break-word;
}

.plan-price {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0b6efb;
  margin: 0;
}

.plan-period {
  margin: 0;
  color: #64748b;
  font-weight: 500;
}

.plan-level-pill {
  display: inline-flex;
  gap: 0.25rem;
  align-items: center;
  margin: 0.75rem 0 0;
  padding: 0.35rem 0.85rem;
  background: #eef2ff;
  border-radius: 999px;
  font-size: 0.85rem;
  color: #1e3a8a;
  font-weight: 500;
  max-width: 100%;
  word-break: break-word;
}

.plan-level-pill .pill-label {
  font-weight: 500;
  color: #1e3a8a;
}

.plan-level-pill .pill-value {
  font-weight: 600;
  color: #111827;
}

.plan-level-switcher {
  margin-top: 0.85rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  max-width: 100%;
}

.plan-level-switcher label {
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #3b82f6;
}

.plan-level-switcher-control {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.plan-level-switcher select {
  border: 1px solid #d1d5db;
  border-radius: 0.6rem;
  padding: 0.55rem 0.75rem;
  font-size: 0.95rem;
  font-weight: 500;
  color: #0f172a;
  background: #fff;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  width: 100%;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.plan-level-switcher select:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15);
}

.plan-level-switcher-hint {
  margin: 0;
  font-size: 0.78rem;
  color: #6b7280;
  line-height: 1.4;
}

.plan-meta {
  flex: 1 1 100%;
  display: flex;
  gap: 1rem;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.meta-item {
  flex: 1 1 calc(50% - 0.5rem);
  min-width: 0;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  padding: 1rem 1.25rem;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
}

.meta-label {
  display: block;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #94a3b8;
  margin-bottom: 0.35rem;
}

.meta-value {
  display: block;
  font-size: 1.2rem;
  font-weight: 700;
  color: #0f172a;
  word-break: break-word;
}

.meta-hint {
  display: block;
  margin-top: 0.35rem;
  font-size: 0.85rem;
  color: #6b7280;
  line-height: 1.4;
}

.meta-item--trial {
  background: #fff7ed;
  border-color: #fed7aa;
}

.timeline-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  gap: 1rem;
  padding: 1.5rem 2rem 0;
  margin-bottom: 1rem;
}

.timeline-card {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 1rem;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  min-height: 135px;
}

.timeline-label {
  font-size: 0.85rem;
  text-transform: uppercase;
  color: #94a3b8;
  letter-spacing: 0.08em;
}

.timeline-date {
  font-size: 1.05rem;
  font-weight: 700;
  color: #0f172a;
}

.timeline-hint {
  font-size: 0.9rem;
  color: #6b7280;
}

.features-section {
  padding: 2rem;
  border-top: 1px solid #f3f4f6;
  margin: 0;
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

.levels-access-section {
  margin: 2rem;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  padding: 1.25rem;
  background: #f8fafc;
}

.levels-title {
  margin: 0 0 1rem;
  font-size: 1rem;
  font-weight: 600;
  color: #0f172a;
}

.levels-grid {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.level-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  background: #fff;
  border: 1px solid #e5e7eb;
}

.level-info {
  display: flex;
  flex-direction: column;
}

.level-name {
  margin: 0;
  font-weight: 600;
  color: #111827;
}

.level-pays {
  margin: 0.15rem 0 0;
  color: #6b7280;
  font-size: 0.9rem;
}

.level-status-text {
  margin: 0.35rem 0 0;
  font-size: 0.85rem;
  color: #4b5563;
}

.level-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.level-status {
  font-size: 0.9rem;
  color: #b45309;
  font-weight: 600;
}

.level-gift-notice {
  font-size: 0.85rem;
  color: #6b7280;
  font-style: italic;
  padding: 0.4rem 0.75rem;
  background: #f3f4f6;
  border-radius: 0.5rem;
}

.level-cancel-btn,
.level-upgrade-btn,
.level-reactivate-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.45rem 0.9rem;
  border-radius: 0.5rem;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.2s ease;
  cursor: pointer;
}

.level-cancel-btn {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #b91c1c;
}

.level-cancel-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.level-reactivate-btn {
  background: linear-gradient(135deg, #10b981, #059669);
  border: none;
  color: white;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
}

.level-reactivate-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #059669, #047857);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
}

.level-reactivate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.level-upgrade-btn {
  border: 1px solid #c7d2fe;
  background: #eef2ff;
  color: #4338ca;
  text-decoration: none;
}

.level-upgrade-btn:hover {
  background: #e0e7ff;
}

.level-cancel-btn:hover:not(:disabled) {
  background: #fee2e2;
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
  margin: 0;
  padding: 2rem;
  border-top: 1px solid #f3f4f6;
}

.actions-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.invoices-section {
  margin: 0;
  padding: 2rem;
  border-top: 1px solid #f3f4f6;
}

.invoices-header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.invoices-header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.invoices-header h4 {
  margin: 0;
  font-size: 1.1rem;
  color: #0f172a;
  flex: 1;
}

.invoices-header p {
  margin: 0;
  color: #64748b;
  font-size: 0.9rem;
}

.invoice-loading,
.invoice-error,
.invoice-empty {
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.75rem;
  text-align: center;
  color: #475569;
  font-size: 0.9rem;
}

.invoice-error {
  background: #fef2f2;
  color: #b91c1c;
}

.invoice-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.invoice-pagination {
  margin-top: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.pagination-btn {
  padding: 0.5rem 1rem;
  border-radius: 999px;
  border: 1px solid #e2e8f0;
  background: #fff;
  color: #0f172a;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.pagination-btn:not(:disabled):hover {
  background: #f8fafc;
  border-color: #cbd5f5;
}

.pagination-info {
  color: #475569;
  font-size: 0.9rem;
  font-weight: 600;
}

.invoice-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f9fafb;
  border: 1px solid #e2e8f0;
  border-radius: 0.85rem;
  padding: 1rem;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.invoice-info {
  flex: 1;
  min-width: 180px;
}

.invoice-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.invoice-date {
  margin: 0;
  font-weight: 600;
  color: #0f172a;
}

.invoice-amount {
  margin: 0.35rem 0 0.15rem;
  color: #0d9488;
  font-weight: 600;
}

.invoice-desc {
  margin: 0;
  color: #475569;
  font-size: 0.9rem;
}

.invoice-level {
  margin: 0.2rem 0 0;
  color: #1d4ed8;
  font-size: 0.85rem;
  font-weight: 600;
}

.invoice-period {
  margin: 0.25rem 0 0;
  font-size: 0.85rem;
  color: #334155;
}

.invoice-note {
  margin: 0.15rem 0 0;
  color: #94a3b8;
  font-size: 0.8rem;
}

.invoice-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.invoice-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.55rem 0.9rem;
  border-radius: 8px;
  border: none;
  background: #1d4ed8;
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  text-decoration: none;
  transition: opacity 0.2s ease;
}

.invoice-btn.secondary {
  background: #0f172a;
}

.invoice-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.upgrade-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #007bff;
  color: white;
  border-radius: 0.5rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
  width: 100%;
  justify-content: center;
}

.upgrade-btn:hover {
  background: #0056b3;
}

.pass-access {
  padding: 2.5rem 2rem;
  border-top: 1px solid #f3f4f6;
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.pass-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1.5rem;
}

.pass-subtitle {
  margin: 0.25rem 0 0;
  color: #6b7280;
}

.pass-chip {
  background: #eef2ff;
  color: #3730a3;
  padding: 0.5rem 1rem;
  border-radius: 999px;
  font-weight: 600;
}

.pass-body {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.25rem;
}

.manual-access,
.no-subscription {
  padding: 3rem 2rem;
  text-align: center;
}

.manual-icon {
  width: 4rem;
  height: 4rem;
  background: #ecfdf5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  color: #047857;
}

.manual-icon svg {
  width: 2rem;
  height: 2rem;
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

.gifted-section {
  margin-top: 2.5rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

.gifted-section--top {
  margin-top: 0;
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  border-top: none;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  background: #f9fafb;
}

.gifted-section--passes {
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  border-top: none;
  border: 1px solid #e0e7ff;
  border-radius: 16px;
  background: linear-gradient(135deg, #f5f3ff 0%, #eff6ff 100%);
}

.gifted-card--pass {
  border-color: #c7d2fe;
  background: linear-gradient(135deg, #ffffff 0%, #f5f3ff 100%);
}

.gifted-pass-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
  border-radius: 8px;
  color: white;
  font-size: 0.85rem;
  font-weight: 600;
}

.pass-badge-icon {
  font-size: 1rem;
}

.gifted-value.status-expired {
  color: #9ca3af;
}

.gifted-header h4 {
  margin: 0 0 0.35rem;
  font-size: 1.2rem;
  color: #111827;
}

.gifted-header p {
  margin: 0 0 1.25rem;
  color: #6b7280;
  font-size: 0.95rem;
}

.gifted-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
}

.gifted-card {
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 1.25rem;
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: box-shadow 0.2s ease;
}

.gifted-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.gifted-child-header {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f3f4f6;
}

.gifted-child-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
  flex-shrink: 0;
}

.gifted-child-info {
  flex: 1;
  min-width: 0;
}

.gifted-child-name {
  margin: 0;
  font-weight: 600;
  color: #111827;
  font-size: 1rem;
}

.gifted-child-email {
  margin: 0.2rem 0 0;
  color: #6b7280;
  font-size: 0.85rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.gifted-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.gifted-detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.gifted-label {
  color: #6b7280;
}

.gifted-value {
  color: #111827;
  font-weight: 500;
  text-align: right;
}

.gifted-value.status-active {
  color: #059669;
}

.gifted-value.status-trial {
  color: #3b82f6;
}

.gifted-value.status-warning {
  color: #d97706;
}

.gifted-value.status-danger {
  color: #dc2626;
}

.gifted-value.status-canceled {
  color: #6b7280;
}

.gifted-actions {
  display: flex;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid #f3f4f6;
}

.gifted-cancel-btn,
.gifted-reactivate-btn {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.gifted-cancel-btn {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #b91c1c;
}

.gifted-cancel-btn:hover:not(:disabled) {
  background: #fee2e2;
}

.gifted-cancel-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.gifted-reactivate-btn {
  background: linear-gradient(135deg, #10b981, #059669);
  border: none;
  color: white;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
}

.gifted-reactivate-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #059669, #047857);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
}

.gifted-reactivate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.gifted-title {
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.6rem;
}

.gifted-meta {
  margin: 0.25rem 0;
  color: #4b5563;
  font-size: 0.92rem;
}

.get-started-btn {
  display: inline-block;
  padding: 1rem 2rem;
  background: #007bff;
  color: white;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
}

.get-started-btn:hover {
  background: #0056b3;
  transform: translateY(-1px);
}

@media (max-width: 1050px) {
  .subscription-manager {
    padding: 0.75rem;
    max-width: 100%;
  }
  
  .subscription-card {
    border-radius: 0.875rem;
  }

  .card-header {
    padding: 1.125rem 1.25rem;
  }

  .status-badge {
    font-size: 0.8125rem;
    padding: 0.4rem 0.875rem;
  }

  .refresh-btn {
    width: 32px;
    height: 32px;
  }

  .btn-icon {
    width: 1.1rem;
    height: 1.1rem;
  }

  .inline-message {
    margin: 0 1.25rem;
    padding: 0.75rem 0.875rem;
    font-size: 0.85rem;
  }

  .plan-overview {
    padding: 1.5rem 1.25rem;
    gap: 1.25rem;
  }

  .plan-heading h3 {
    font-size: 1.5rem;
  }

  .plan-price {
    font-size: 1.35rem;
  }

  .plan-level-pill {
    font-size: 0.8rem;
    padding: 0.3rem 0.75rem;
  }

  .plan-level-switcher select {
    font-size: 0.85rem;
    padding: 0.5rem 0.625rem;
  }

  .plan-level-switcher-hint {
    font-size: 0.7rem;
  }

  .plan-meta {
    justify-content: flex-start;
    gap: 0.75rem;
  }

  .meta-item {
    padding: 0.875rem 1rem;
    min-width: 0;
    flex: 1 1 calc(50% - 0.375rem);
  }

  .meta-label {
    font-size: 0.75rem;
  }

  .meta-value {
    font-size: 1.05rem;
  }

  .meta-hint {
    font-size: 0.8rem;
  }

  .timeline-row {
    padding: 1rem 1.25rem 0;
    gap: 0.875rem;
  }

  .timeline-card {
    padding: 1rem;
    min-height: 120px;
  }

  .timeline-date {
    font-size: 1rem;
  }

  .features-section,
  .actions-section,
  .invoices-section {
    padding: 1.5rem 1.25rem;
  }

  .features-title {
    font-size: 1.05rem;
  }

  .feature-item {
    font-size: 0.9rem;
    padding: 0.4rem 0;
  }

  .feature-icon {
    width: 1.1rem;
    height: 1.1rem;
  }

  .levels-access-section {
    margin: 1.5rem 1.25rem;
    padding: 1rem;
  }

  .levels-title {
    font-size: 0.95rem;
  }

  .level-card {
    padding: 0.875rem;
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .level-info {
    flex: 1;
    min-width: 100%;
  }

  .level-actions {
    width: 100%;
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }

  .level-status {
    text-align: center;
    padding: 0.5rem;
    background: #fff7ed;
    border-radius: 0.5rem;
    font-size: 0.85rem;
  }

  .level-cancel-btn,
  .level-upgrade-btn,
  .level-reactivate-btn {
    flex: 1;
    justify-content: center;
    padding: 0.5rem 0.75rem;
    font-size: 0.8125rem;
  }

  .invoices-header-content {
    gap: 0.875rem;
  }

  .invoices-header h4 {
    font-size: 1.05rem;
  }

  .invoices-header p {
    font-size: 0.85rem;
  }

  .invoices-header .refresh-btn {
    width: 32px;
    height: 32px;
  }

  .invoices-header .btn-icon {
    width: 1.05rem;
    height: 1.05rem;
  }

  .invoice-row {
    padding: 0.875rem;
    gap: 0.625rem;
  }

  .invoice-info {
    min-width: 100%;
  }

  .invoice-actions {
    width: 100%;
    justify-content: stretch;
    gap: 0.5rem;
  }

  .invoice-btn {
    flex: 1;
    justify-content: center;
    padding: 0.5rem 0.75rem;
    font-size: 0.85rem;
  }

  .invoice-date {
    font-size: 0.95rem;
  }

  .invoice-amount {
    font-size: 0.95rem;
  }

  .invoice-desc {
    font-size: 0.85rem;
  }

  .upgrade-btn {
    padding: 0.875rem 1.25rem;
    font-size: 0.95rem;
  }
}

@media (max-width: 640px) {
  .subscription-manager {
    padding: 0.5rem;
  }

  .subscription-card {
    border-radius: 0.75rem;
  }

  .card-header {
    padding: 1rem;
  }

  .status-badge {
    font-size: 0.75rem;
    padding: 0.375rem 0.75rem;
  }

  .plan-overview {
    padding: 1.25rem 1rem;
    gap: 1rem;
    flex-direction: column;
  }

  .plan-heading {
    flex: 1 1 100%;
    width: 100%;
  }

  .plan-heading .eyebrow {
    font-size: 0.7rem;
  }

  .plan-heading h3 {
    font-size: 1.375rem;
    line-height: 1.3;
  }

  .plan-price {
    font-size: 1.25rem;
    margin-top: 0.25rem;
  }

  .plan-period {
    font-size: 0.875rem;
    margin-top: 0.15rem;
  }

  .plan-level-pill {
    font-size: 0.7rem;
    padding: 0.3rem 0.65rem;
    margin-top: 0.5rem;
    display: inline-block;
    width: auto;
    max-width: 100%;
    word-wrap: break-word;
  }

  .plan-level-pill .pill-label {
    display: none;
  }

  .plan-level-pill::before {
    content: "📍 ";
    font-size: 0.75rem;
  }

  .plan-level-switcher {
    margin-top: 0.75rem;
    width: 100%;
  }

  .plan-level-switcher label {
    font-size: 0.7rem;
  }

  .plan-level-switcher select {
    padding: 0.45rem 0.5rem;
    font-size: 0.8rem;
  }

  .plan-level-switcher-hint {
    font-size: 0.68rem;
    line-height: 1.5;
  }

  .plan-meta {
    flex-direction: column;
    gap: 0.75rem;
    width: 100%;
  }

  .meta-item {
    flex: 1 1 100%;
    padding: 0.875rem 1rem;
    min-width: 0;
  }

  .meta-label {
    font-size: 0.75rem;
  }

  .meta-value {
    font-size: 1.05rem;
  }

  .meta-hint {
    font-size: 0.8rem;
  }

  .timeline-row {
    grid-template-columns: 1fr;
    padding: 1rem 0;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
  }

  .timeline-card {
    padding: 0.875rem;
    min-height: auto;
  }

  .timeline-label {
    font-size: 0.75rem;
  }

  .timeline-date {
    font-size: 0.95rem;
  }

  .timeline-hint {
    font-size: 0.85rem;
  }

  .features-section,
  .actions-section,
  .invoices-section {
    padding: 1.25rem 1rem;
  }

  .features-title {
    font-size: 1rem;
    margin-bottom: 0.875rem;
  }

  .feature-item {
    font-size: 0.875rem;
    gap: 0.625rem;
  }

  .feature-icon {
    width: 1rem;
    height: 1rem;
  }

  .levels-access-section {
    margin: 1.25rem 1rem;
    padding: 0.875rem;
  }

  .levels-title {
    font-size: 0.9rem;
    margin-bottom: 0.875rem;
  }

  .levels-grid {
    gap: 0.625rem;
  }

  .level-card {
    padding: 0.75rem;
  }

  .level-name {
    font-size: 0.9rem;
  }

  .level-pays {
    font-size: 0.85rem;
  }

  .level-status-text {
    font-size: 0.8rem;
  }

  .level-cancel-btn,
  .level-upgrade-btn {
    padding: 0.5rem 0.75rem;
    font-size: 0.8rem;
  }

  .invoices-header {
    gap: 0.5rem;
  }

  .invoices-header-content {
    gap: 0.75rem;
  }

  .invoices-header h4 {
    font-size: 1rem;
  }

  .invoices-header p {
    font-size: 0.8125rem;
  }

  .invoices-header .refresh-btn {
    width: 30px;
    height: 30px;
  }

  .invoices-header .btn-icon {
    width: 1rem;
    height: 1rem;
  }

  .invoice-row {
    padding: 0.75rem;
    border-radius: 0.75rem;
  }

  .invoice-date {
    font-size: 0.9rem;
  }

  .invoice-amount {
    font-size: 0.9rem;
    margin: 0.25rem 0 0.1rem;
  }

  .invoice-desc {
    font-size: 0.8125rem;
  }

  .invoice-level {
    font-size: 0.8rem;
  }

  .invoice-period {
    font-size: 0.8rem;
  }

  .invoice-note {
    font-size: 0.75rem;
  }

  .invoice-btn {
    padding: 0.5rem 0.625rem;
    font-size: 0.8125rem;
  }

  .upgrade-btn {
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
  }

  .pass-access {
    padding: 2rem 1.25rem;
    gap: 1.5rem;
  }

  .pass-header {
    flex-direction: column;
    gap: 1rem;
  }

  .pass-header h3 {
    font-size: 1.375rem;
  }

  .pass-subtitle {
    font-size: 0.9rem;
  }

  .pass-chip {
    padding: 0.4rem 0.875rem;
    font-size: 0.85rem;
    align-self: flex-start;
  }

  .pass-body {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .manual-access,
  .no-subscription {
    padding: 2.5rem 1.25rem;
  }

  .manual-access h4,
  .no-subscription h4 {
    font-size: 1.15rem;
  }

  .manual-access p,
  .no-subscription p {
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
  }

  .get-started-btn {
    padding: 0.875rem 1.75rem;
    font-size: 0.95rem;
  }
}

@media (max-width: 480px) {
  .subscription-manager {
    padding: 0.25rem;
  }

  .card-header {
    padding: 0.875rem;
  }

  .plan-overview {
    padding: 1rem 0.875rem;
    gap: 0.875rem;
  }

  .plan-heading .eyebrow {
    font-size: 0.65rem;
  }

  .plan-heading h3 {
    font-size: 1.25rem;
  }

  .plan-price {
    font-size: 1.125rem;
  }

  .plan-period {
    font-size: 0.8rem;
  }

  .plan-level-pill {
    font-size: 0.675rem;
    padding: 0.25rem 0.55rem;
  }

  .plan-level-pill .pill-label {
    display: none;
  }

  .plan-level-pill::before {
    content: "📍 ";
    font-size: 0.7rem;
  }

  .plan-level-switcher label {
    font-size: 0.625rem;
  }

  .plan-level-switcher select {
    font-size: 0.75rem;
    padding: 0.4rem 0.45rem;
  }

  .plan-level-switcher-hint {
    font-size: 0.625rem;
  }

  .meta-item {
    padding: 0.75rem 0.875rem;
  }

  .meta-label {
    font-size: 0.7rem;
  }

  .meta-value {
    font-size: 1rem;
  }

  .meta-hint {
    font-size: 0.75rem;
  }

  .timeline-row {
    padding: 0.875rem 0;
  }

  .features-section,
  .actions-section,
  .invoices-section {
    padding: 1rem 0.875rem;
  }

  .levels-access-section {
    margin: 1rem 0.875rem;
  }

  .invoices-header-content {
    gap: 0.625rem;
  }

  .invoices-header h4 {
    font-size: 0.95rem;
  }

  .invoices-header p {
    font-size: 0.8rem;
  }

  .invoices-header .refresh-btn {
    width: 28px;
    height: 28px;
  }

  .invoices-header .btn-icon {
    width: 0.95rem;
    height: 0.95rem;
  }

  .invoice-actions {
    flex-direction: column;
  }

  .invoice-btn {
    width: 100%;
  }

  .level-actions {
    flex-direction: column;
  }

  .level-cancel-btn,
  .level-upgrade-btn {
    width: 100%;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Modal de résiliation */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(4px);
  animation: fadeIn 0.2s ease;
  overflow-y: auto;
  padding: 2rem 1rem;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-card {
  background: #ffffff;
  border-radius: 20px;
  width: min(90%, 420px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.15), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 1.5rem 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  color: #111827;
  font-size: 1.125rem;
  font-weight: 700;
}

.modal-close {
  background: #f3f4f6;
  border: none;
  font-size: 1.5rem;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
  line-height: 1;
  padding: 0;
  width: 2rem;
  height: 2rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close:hover {
  background: #e5e7eb;
  color: #374151;
}

.modal-body {
  padding: 1.5rem;
}

.modal-body p {
  margin: 0 0 0.75rem;
  color: #374151;
  font-size: 0.9375rem;
  line-height: 1.5;
}

.modal-body p:last-child {
  margin-bottom: 0;
}

.modal-body strong {
  color: #111827;
}

.modal-hint {
  color: #6b7280 !important;
  font-size: 0.875rem !important;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1rem 1.5rem 1.5rem;
  border-top: 1px solid #f3f4f6;
}

.cancel-btn {
  background: #ffffff;
  color: #374151;
  border: 1.5px solid #d1d5db;
  border-radius: 10px;
  padding: 0.625rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-btn:hover {
  background: #f9fafb;
  border-color: #9ca3af;
}

.confirm-btn {
  background: linear-gradient(135deg, #667eea 0%, #5a67d8 100%);
  color: #ffffff;
  border: none;
  border-radius: 10px;
  padding: 0.625rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.confirm-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.confirm-btn--danger {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.confirm-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 480px) {
  .modal-overlay {
    padding: 1rem;
    align-items: center;
  }

  .modal-card {
    width: 100%;
  }

  .modal-actions {
    flex-direction: column;
  }

  .cancel-btn,
  .confirm-btn {
    width: 100%;
    justify-content: center;
  }

  .confirm-btn {
    order: -1;
  }
}
</style>
