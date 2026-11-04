<template>
  <DashboardLayout>
    <div class="ab">
      <header class="es-page-head ab-head">
        <div>
          <h1 class="es-h1">Abonnement</h1>
          <p class="es-sub">Tous les cours, fiches et exercices corrigés de ta classe, avec le suivi de tes progrès. Sans engagement.</p>
        </div>
        <router-link v-if="aUnAcces" to="/subscription" class="es-btn es-btn--ghost es-btn--sm">
          Gérer mon abonnement
        </router-link>
      </header>

      <!-- Accès déjà actif -->
      <div v-if="aUnAcces" class="ab-statut" role="status">
        <CheckCircleIcon aria-hidden="true" />
        <p><strong>Ton accès est actif</strong><span>{{ resumeAcces }}</span></p>
      </div>

      <!-- Classe à débloquer et bénéficiaire -->
      <section class="es-card ab-reglages" aria-label="Classe et bénéficiaire">
        <div class="ab-champ">
          <label for="billing-level-select" class="ab-label">Classe à débloquer</label>
          <div class="ab-select">
            <select
              id="billing-level-select"
              v-model.number="selectedNiveauId"
              :disabled="niveauxLoading || !niveaux.length"
            >
              <option v-if="niveauxLoading" value="">Chargement…</option>
              <option v-for="niveau in niveaux" :key="niveau.id" :value="niveau.id">
                {{ niveau.nom }}
              </option>
            </select>
          </div>
          <p v-if="levelAlertMessage" class="ab-alerte">{{ levelAlertMessage }}</p>
          <p v-else-if="levelAlreadyUnlocked && !subscribeForChild" class="ab-note ab-note--ok">
            <CheckIcon aria-hidden="true" /> Cette classe est déjà débloquée sur ton compte.
          </p>
          <p v-else class="ab-note">L’abonnement donne accès à tout le programme de cette classe.</p>
        </div>

        <div class="ab-champ">
          <label class="ab-switch">
            <input v-model="subscribeForChild" type="checkbox" />
            <span class="ab-switch__piste" aria-hidden="true"></span>
            <span class="ab-switch__texte">
              <strong>Offrir à quelqu’un d’autre</strong>
              <small>Un enfant, un proche ou un élève</small>
            </span>
          </label>
          <div v-if="subscribeForChild" class="ab-offrir">
            <label for="beneficiary-email" class="ab-label">E-mail du bénéficiaire</label>
            <input
              id="beneficiary-email"
              v-model="beneficiaryEmail"
              type="email"
              class="ab-input"
              placeholder="email@exemple.com"
              :class="{ 'input-error': beneficiaryEmailError }"
            />
            <p v-if="beneficiaryEmailError" class="ab-alerte">{{ beneficiaryEmailError }}</p>
            <p v-else class="ab-note">S’il n’a pas encore de compte OptiTAB, tu pourras le lui créer juste avant le paiement.</p>
          </div>
        </div>
      </section>

      <!-- Formules -->
      <div id="plans" class="ab-formules">
        <PricingCards
          :submitting="submitting"
          :show-current-plan="shouldBlockForSelf"
          :current-price-id="activePlanPriceId"
          :level-already-unlocked="levelAlreadyUnlocked"
          cta-location="billing"
          :disabled-label="!levelReady ? 'Choisir une classe' : 'Déjà souscrit'"
          already-subscribed-label="Déjà souscrit"
          @select="handlePlanClick"
        />
      </div>

      <ul class="ab-garanties">
        <li><LockClosedIcon aria-hidden="true" />Paiement sécurisé par Stripe</li>
        <li><ArrowPathIcon aria-hidden="true" />Sans engagement, annulable en un clic</li>
        <li><DocumentTextIcon aria-hidden="true" />Facture envoyée par e-mail</li>
      </ul>

      <section class="es-card ab-faq" aria-labelledby="ab-faq-titre">
        <h2 id="ab-faq-titre" class="es-h2">Questions fréquentes</h2>
        <details v-for="item in billingFaq" :key="item.question" class="ab-faq__item">
          <summary>{{ item.question }}<ChevronDownIcon aria-hidden="true" /></summary>
          <p>{{ item.answer }}</p>
        </details>
      </section>

      <p class="ab-aide">
        Une question ? Écris-nous sur
        <a href="https://wa.me/33764040251" target="_blank" rel="noopener noreferrer" data-cta-name="whatsapp" data-cta-location="billing">WhatsApp</a>
        ou à <a href="mailto:contact@optitab.net">contact@optitab.net</a>. Réponse sous 24 h.
      </p>
    </div>

    <!-- Message -->
    <Modal
      :is-open="showMessageModal"
      :title="messageModalTitle"
      :icon="InformationCircleIcon"
      size="small"
      @close="closeMessageModal"
    >
      <p class="billing-modal-text">{{ messageModalText }}</p>
      <template #footer>
        <button type="button" class="om-btn om-btn--primary" @click="closeMessageModal">OK</button>
      </template>
    </Modal>

    <!-- Création du compte du bénéficiaire (cadeau) -->
    <Modal
      :is-open="showCreateAccountModal"
      title="Créer un compte pour le bénéficiaire"
      :icon="GiftIcon"
      :can-close="!creatingAccount"
      size="small"
      @close="closeCreateAccountModal"
    >
      <p class="billing-modal-text">
        L’adresse <strong>{{ beneficiaryEmail }}</strong> ne correspond à aucun compte OptiTAB.
        Crée un compte pour ce bénéficiaire afin de lui offrir l’abonnement.
      </p>
      <div class="billing-create-form">
        <div class="billing-create-row">
          <div class="om-field">
            <label class="om-label" for="create-first-name">Prénom</label>
            <input
              id="create-first-name"
              v-model="createAccountForm.first_name"
              type="text"
              class="om-input"
              :class="{ 'is-error': createAccountErrors.first_name }"
              placeholder="Prénom"
            />
            <span v-if="createAccountErrors.first_name" class="billing-field-error">{{ createAccountErrors.first_name }}</span>
          </div>
          <div class="om-field">
            <label class="om-label" for="create-last-name">Nom</label>
            <input
              id="create-last-name"
              v-model="createAccountForm.last_name"
              type="text"
              class="om-input"
              :class="{ 'is-error': createAccountErrors.last_name }"
              placeholder="Nom"
            />
            <span v-if="createAccountErrors.last_name" class="billing-field-error">{{ createAccountErrors.last_name }}</span>
          </div>
        </div>
        <div class="om-field">
          <label class="om-label" for="create-email">E-mail</label>
          <input id="create-email" type="email" class="om-input" :value="beneficiaryEmail" disabled />
        </div>
        <p
          v-if="createAccountMessage"
          :class="['om-alert', createAccountSuccess ? 'om-alert--success' : 'om-alert--error']"
        >
          {{ createAccountMessage }}
        </p>
      </div>
      <template #footer>
        <button type="button" class="om-btn om-btn--ghost" :disabled="creatingAccount" @click="closeCreateAccountModal">Annuler</button>
        <button type="button" class="om-btn om-btn--primary" :disabled="creatingAccount" @click="handleCreateBeneficiaryAccount">
          {{ creatingAccount ? 'Création…' : 'Créer le compte' }}
        </button>
      </template>
    </Modal>
  </DashboardLayout>
</template>

<script setup>
import { onMounted, onUnmounted, ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { createCheckoutSession } from '@/api/subscriptions'
import { checkEmailExists, createChildAccount } from '@/api/users'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import PricingCards from '@/components/shared/PricingCards.vue'
import Modal from '@/components/common/Modal.vue'
import {
  ArrowPathIcon,
  CheckCircleIcon,
  CheckIcon,
  ChevronDownIcon,
  DocumentTextIcon,
  GiftIcon,
  InformationCircleIcon,
  LockClosedIcon
} from '@heroicons/vue/24/outline'
import { useSubscriptionStore } from '@/stores/subscription'
import { getNiveauxByPays } from '@/api/niveaux'
import { useUserStore } from '@/stores/user'
import * as analytics from '@/services/analytics'

const submitting = ref(false)
const subscriptionStore = useSubscriptionStore()
const userStore = useUserStore()
const route = useRoute()

// Arrivée depuis un contenu verrouillé : on descend jusqu'aux formules.
onMounted(() => {
  if (route.hash === '#plans' || route.query.reason === 'subscription_required') {
    setTimeout(() => {
      document.getElementById('plans')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }, 300)
  }
})

// Variables pour offrir un abonnement à quelqu'un d'autre
const subscribeForChild = ref(false)
const beneficiaryEmail = ref('')
const beneficiaryEmailError = ref('')

// Variables pour la modale de création de compte bénéficiaire
const showCreateAccountModal = ref(false)
const pendingPriceId = ref(null)
const createAccountForm = ref({ first_name: '', last_name: '' })
const createAccountErrors = ref({ first_name: '', last_name: '' })
const createAccountMessage = ref('')
const createAccountSuccess = ref(false)
const creatingAccount = ref(false)

// Variables pour le modal de message
const showMessageModal = ref(false)
const messageModalTitle = ref('Information')
const messageModalText = ref('')

const showMessage = (text, title = 'Information') => {
  messageModalTitle.value = title
  messageModalText.value = text
  showMessageModal.value = true
}

const closeMessageModal = () => {
  showMessageModal.value = false
  messageModalText.value = ''
}

// Gestion de la touche Échap pour fermer le modal
const handleEscapeKey = (e) => {
  if (e.key === 'Escape') {
    if (showCreateAccountModal.value) {
      closeCreateAccountModal()
    } else if (showMessageModal.value) {
      closeMessageModal()
    }
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleEscapeKey)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscapeKey)
})

// Validation de l'email bénéficiaire
const validateBeneficiaryEmail = () => {
  beneficiaryEmailError.value = ''
  if (!subscribeForChild.value) return true
  
  if (!beneficiaryEmail.value.trim()) {
    beneficiaryEmailError.value = "L'email de l'élève est requis"
    return false
  }
  
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(beneficiaryEmail.value.trim())) {
    beneficiaryEmailError.value = "Veuillez entrer une adresse email valide"
    return false
  }
  
  return true
}

// Réinitialiser l'email quand on désactive l'option
watch(subscribeForChild, (newVal) => {
  if (!newVal) {
    beneficiaryEmail.value = ''
    beneficiaryEmailError.value = ''
  }
})

const niveaux = ref([])
const niveauxLoading = ref(false)
const niveauxError = ref('')
const selectedNiveauId = ref(
  userStore.niveau_pays?.id ? Number(userStore.niveau_pays.id) : null
)

watch(
  () => userStore.niveau_pays?.id,
  (newId) => {
    if (newId) {
      selectedNiveauId.value = Number(newId)
    }
  }
)


const selectedNiveau = computed(() =>
  niveaux.value.find(n => n.id === selectedNiveauId.value) || null
)
const levelReady = computed(() => Boolean(selectedNiveauId.value))
const levelDisplay = computed(() => {
  if (!selectedNiveau.value) return 'Sélectionner un niveau'
  const paysName = selectedNiveau.value.pays?.nom
  return paysName ? `${selectedNiveau.value.nom} · ${paysName}` : selectedNiveau.value.nom
})
const levelHelper = computed(() => 'Ce niveau déterminera les contenus disponibles dans votre espace.')

const levelAlertMessage = computed(() => {
  if (niveauxError.value) {
    return niveauxError.value
  }
  if (!levelReady.value && !niveauxLoading.value) {
    return 'Choisis la classe à débloquer.'
  }
  return ''
})

// Questions fréquentes adaptées à la facturation/abonnement
const billingFaq = [
  {
    question: 'Quelle formule choisir ?',
    answer: 'Le pass 24 h dépanne avant un contrôle. L’abonnement hebdomadaire convient pour réviser quelques jours. Le mensuel est le plus avantageux dès que tu travailles plus de deux semaines. La formule Accompagné ajoute des questions illimitées à un professeur par WhatsApp ou e-mail.'
  },
  {
    question: 'Puis-je annuler à tout moment ?',
    answer: 'Oui, depuis Mon abonnement. Tu gardes l’accès jusqu’à la fin de la période déjà payée. Les pass sont des paiements uniques, sans renouvellement.'
  },
  {
    question: 'Un abonnement couvre quelle classe ?',
    answer: 'La classe choisie ci-dessus, avec tout son programme. Pour une autre classe ou un autre enfant, il suffit de souscrire une formule de plus.'
  },
  {
    question: 'Le paiement est-il sécurisé ?',
    answer: 'Oui. Le paiement passe par Stripe, leader du paiement en ligne. Aucune donnée de carte n’est stockée chez nous.'
  },
  {
    question: 'Est-ce que je reçois une facture ?',
    answer: 'Oui, une facture est envoyée par e-mail après chaque règlement. Tu la retrouves aussi dans Mon abonnement.'
  }
]

const humanPeriod = (p) => {
  if (p === 'daily') return 'jour'
  if (p === 'weekly') return 'semaine'
  if (p === 'monthly') return 'mois'
  if (p === 'yearly') return 'an'
  return p
}

const hasActiveSubscription = computed(() =>
  Boolean(subscriptionStore.status?.subscriptions?.some(sub => sub?.is_active))
)
const unlockedLevels = computed(() => subscriptionStore.unlockedLevels || [])
const levelAlreadyUnlocked = computed(() =>
  Boolean(
    selectedNiveauId.value &&
    unlockedLevels.value.some(level => Number(level.id) === Number(selectedNiveauId.value))
  )
)
const aUnAcces = computed(() => subscriptionStore.hasAccess)
const resumeAcces = computed(() => {
  const classes = unlockedLevels.value.map((l) => l.nom).filter(Boolean)
  const offre = subscriptionStore.status?.plan_name ? activePlanLabel.value : ''
  return [offre, classes.length ? (classes.length > 1 ? `Classes : ${classes.join(', ')}` : `Classe : ${classes[0]}`) : '']
    .filter(Boolean).join(' · ') || 'Tous les contenus de ta classe sont débloqués.'
})
const isGiftMode = computed(() => subscribeForChild.value)
const shouldBlockForSelf = computed(() => !isGiftMode.value)
const activePlanPriceId = computed(() => subscriptionStore.status?.plan_stripe_price_id || '')
const activePlanLabel = computed(() => {
  const name = subscriptionStore.status?.plan_name || ''
  const period = subscriptionStore.status?.plan_billing_period || ''
  if (name && period) return `${name} (${humanPeriod(period)})`
  if (name) return name
  if (period) return `Offre ${humanPeriod(period)}`
  return 'ton offre actuelle'
})

const isCurrentPrice = (priceId) => {
  if (!priceId || !activePlanPriceId.value) return false
  if (priceId !== activePlanPriceId.value) return false
  return levelAlreadyUnlocked.value
}

const handlePlanClick = (card) => {
  if (!card?.priceId) return
  if ((shouldBlockForSelf.value && levelAlreadyUnlocked.value) || submitting.value) return
  subscribe(card.priceId)
}

onMounted(async () => {
  try {
    await subscriptionStore.fetchStatus({ force: true }).catch(() => {})
    await loadNiveauxOptions()
  } catch (e) {
    console.error('Erreur lors du chargement:', e)
  }
})

async function loadNiveauxOptions() {
  try {
    niveauxLoading.value = true
    niveauxError.value = ''
    const data = await getNiveauxByPays()
    const rawList = Array.isArray(data?.results) ? data.results : data || []
    const activeList = rawList.filter(n => n && (n.est_actif === undefined || n.est_actif))
    niveaux.value = activeList

    const selectedStillActive = activeList.some(n => n.id === selectedNiveauId.value)
    if (!selectedStillActive) {
      selectedNiveauId.value = null
    }

    if (!selectedNiveauId.value && activeList.length) {
      const preferredId = userStore.niveau_pays?.id
      const match = preferredId ? activeList.find(n => n.id === Number(preferredId)) : null
      selectedNiveauId.value = match ? match.id : activeList[0].id
    }
  } catch (error) {
    console.error('Erreur chargement niveaux:', error)
    niveauxError.value = 'Impossible de charger la liste des classes.'
  } finally {
    niveauxLoading.value = false
  }
}

async function subscribe(priceId) {
  try {
    if (!levelReady.value) {
      showMessage('Choisis d’abord la classe à débloquer.', 'Classe à choisir')
      return
    }
    if (shouldBlockForSelf.value && levelAlreadyUnlocked.value) {
      showMessage('Cette classe est déjà débloquée. Choisis une autre classe pour souscrire.', 'Classe déjà débloquée')
      return
    }
    
    // Validation de l'email bénéficiaire pour les parents
    if (subscribeForChild.value && !validateBeneficiaryEmail()) {
      return
    }
    
    // Vérifier si le bénéficiaire a un compte OptiTAB
    if (subscribeForChild.value && beneficiaryEmail.value.trim()) {
      submitting.value = true
      try {
        const res = await checkEmailExists(beneficiaryEmail.value.trim())
        const emailData = res?.data?.data || res?.data || {}
        if (!emailData.exists) {
          // L'email n'existe pas, ouvrir la modale de création de compte
          pendingPriceId.value = priceId
          createAccountForm.value = { first_name: '', last_name: '' }
          createAccountErrors.value = { first_name: '', last_name: '' }
          createAccountMessage.value = ''
          showCreateAccountModal.value = true
          submitting.value = false
          return
        }
      } catch (e) {
        // En cas d'erreur de vérification, on continue avec le flux normal
        console.warn('Erreur vérification email:', e)
      }
    }
    
    await proceedWithCheckout(priceId)
  } catch (e) {
    const msg = e?.response?.data?.error || 'Impossible de démarrer le paiement. Vérifiez la configuration Stripe.'
    showMessage(msg, 'Erreur')
  } finally {
    submitting.value = false
  }
}

async function proceedWithCheckout(priceId) {
  const payload = selectedNiveauId.value
    ? { niveau_pays_id: selectedNiveauId.value }
    : {}
  
  // Ajouter l'email du bénéficiaire si le parent souscrit pour un enfant
  if (subscribeForChild.value && beneficiaryEmail.value.trim()) {
    payload.beneficiary_email = beneficiaryEmail.value.trim()
  }

  if (shouldBlockForSelf.value && isCurrentPrice(priceId)) {
    showMessage('Vous disposez déjà de cet abonnement actif. Utilisez « Gérer mon abonnement » pour le modifier.', 'Abonnement actif')
    return
  }
  if (!priceId) {
    showMessage('Ce plan doit encore être configuré (Price ID manquant).', 'Configuration requise')
    return
  }
  submitting.value = true
  const { data } = await createCheckoutSession(priceId, payload)
  if (data?.checkout_url) {
    analytics.beginCheckout({
      value: data.amount,
      currency: data.currency || 'EUR',
      planName: data.plan_name,
      planMode: data.plan_mode,
      transactionId: data.transaction_id || data.tiktok_event_id || '',
      eventId: data.tiktok_event_id || data.transaction_id || '',
    })
    window.location.assign(data.checkout_url)
  }
}

// Fonctions pour la modale de création de compte
function closeCreateAccountModal() {
  showCreateAccountModal.value = false
  pendingPriceId.value = null
  createAccountForm.value = { first_name: '', last_name: '' }
  createAccountErrors.value = { first_name: '', last_name: '' }
  createAccountMessage.value = ''
}

function validateCreateAccountForm() {
  createAccountErrors.value = { first_name: '', last_name: '' }
  let valid = true
  
  if (!createAccountForm.value.first_name.trim()) {
    createAccountErrors.value.first_name = 'Le prénom est requis'
    valid = false
  }
  if (!createAccountForm.value.last_name.trim()) {
    createAccountErrors.value.last_name = 'Le nom est requis'
    valid = false
  }
  
  return valid
}

async function handleCreateBeneficiaryAccount() {
  if (!validateCreateAccountForm()) return
  
  creatingAccount.value = true
  createAccountMessage.value = ''
  
  try {
    const payload = {
      email: beneficiaryEmail.value.trim(),
      first_name: createAccountForm.value.first_name.trim(),
      last_name: createAccountForm.value.last_name.trim(),
      niveau_pays_id: selectedNiveauId.value || null,
    }
    
    await createChildAccount(payload)
    createAccountSuccess.value = true
    createAccountMessage.value = 'Compte créé ! Redirection vers le paiement…'
    
    // Attendre un peu puis procéder au checkout
    setTimeout(async () => {
      showCreateAccountModal.value = false
      if (pendingPriceId.value) {
        await proceedWithCheckout(pendingPriceId.value)
      }
    }, 1500)
  } catch (e) {
    createAccountSuccess.value = false
    createAccountMessage.value = e?.response?.data?.message || 'Erreur lors de la création du compte'
  } finally {
    creatingAccount.value = false
  }
}
</script>

<style scoped>
/* Page Abonnement : style de l'espace (variables --es-* posées par EspaceLayout). */
.ab {
  max-width: 1040px;
  margin: 0 auto;
}

.ab-head {
  align-items: center;
}

/* Accès actif */
.ab-statut {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  padding: 14px 18px;
  border: 1px solid #cfe7cf;
  border-radius: var(--es-radius-sm);
  background: var(--es-green-50);
}

.ab-statut svg {
  width: 26px;
  height: 26px;
  flex-shrink: 0;
  color: var(--es-green-700);
}

.ab-statut p {
  display: flex;
  flex-direction: column;
  font-size: 14px;
  color: var(--es-ink-soft);
}

.ab-statut strong {
  font-size: 15px;
  color: var(--es-green-700);
}

/* Réglages */
.ab-reglages {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  padding: 22px 24px;
}

.ab-champ {
  min-width: 0;
}

.ab-label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 700;
  color: var(--es-ink);
}

.ab-select {
  position: relative;
}

.ab-select select,
.ab-input {
  width: 100%;
  height: 46px;
  padding: 0 14px;
  border: 1px solid var(--es-line-strong);
  border-radius: 12px;
  background: #fff;
  font: 600 15px var(--es-font);
  color: var(--es-ink);
}

.ab-select select {
  padding-right: 40px;
  appearance: none;
  cursor: pointer;
  background: #fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='%23667085'%3E%3Cpath d='M5.3 7.3a1 1 0 0 1 1.4 0L10 10.6l3.3-3.3a1 1 0 1 1 1.4 1.4l-4 4a1 1 0 0 1-1.4 0l-4-4a1 1 0 0 1 0-1.4Z'/%3E%3C/svg%3E") no-repeat right 14px center / 18px;
}

.ab-input {
  font-weight: 500;
}

.ab-select select:focus,
.ab-input:focus {
  border-color: var(--es-navy);
  outline: 3px solid rgba(27, 60, 142, 0.12);
}

.ab-input.input-error {
  border-color: var(--es-red-700);
}

.ab-note,
.ab-alerte {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 8px !important;
  font-size: 13.5px;
  line-height: 1.45;
  color: var(--es-muted);
}

.ab-note svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.ab-note--ok {
  color: var(--es-green-700);
  font-weight: 600;
}

.ab-alerte {
  color: var(--es-red-700);
  font-weight: 600;
}

/* Interrupteur « Offrir » */
.ab-switch {
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 46px;
  margin-top: 26px;
  cursor: pointer;
}

.ab-switch input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.ab-switch__piste {
  position: relative;
  width: 44px;
  height: 26px;
  flex-shrink: 0;
  border-radius: 999px;
  background: var(--es-line-strong);
  transition: background-color 0.2s ease;
}

.ab-switch__piste::after {
  content: '';
  position: absolute;
  top: 3px;
  left: 3px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 1px 3px rgba(16, 24, 40, 0.2);
  transition: transform 0.2s ease;
}

.ab-switch input:checked + .ab-switch__piste {
  background: var(--es-navy);
}

.ab-switch input:checked + .ab-switch__piste::after {
  transform: translateX(18px);
}

.ab-switch input:focus-visible + .ab-switch__piste {
  outline: 3px solid rgba(95, 172, 96, 0.55);
  outline-offset: 2px;
}

.ab-switch__texte {
  display: flex;
  flex-direction: column;
  font-size: 15px;
  color: var(--es-ink);
}

.ab-switch__texte small {
  font-size: 13px;
  color: var(--es-muted);
}

.ab-offrir {
  margin-top: 14px;
}

/* Formules (composant PricingCards, identique à la page Tarifs) */
.ab-formules {
  margin-top: 28px;
  scroll-margin-top: calc(var(--es-top) + 16px);
}

/* Ici, version plus légère que sur la page Tarifs : pas d'avis répétés dans
   chaque carte ni de mention sous le bouton (garanties affichées en dessous). */
.ab-formules :deep(.card-reviews),
.ab-formules :deep(.card-note) {
  display: none;
}

.ab-formules :deep(.pricing-tab) {
  white-space: nowrap;
}

.ab-formules :deep(.card-features) {
  margin-bottom: 20px;
}

/* Garanties */
.ab-garanties {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px 28px;
  margin: 28px 0 32px;
  padding: 0;
  list-style: none;
}

.ab-garanties li {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--es-ink-soft);
}

.ab-garanties svg {
  width: 18px;
  height: 18px;
  color: var(--es-navy);
}

/* Questions fréquentes */
.ab-faq {
  padding: 22px 24px 8px;
}

.ab-faq .es-h2 {
  margin-bottom: 6px;
}

.ab-faq__item {
  border-bottom: 1px solid var(--es-line);
}

.ab-faq__item:last-child {
  border-bottom: 0;
}

.ab-faq__item summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 16px 0;
  font-size: 15px;
  font-weight: 600;
  color: var(--es-ink);
  cursor: pointer;
  list-style: none;
}

.ab-faq__item summary::-webkit-details-marker {
  display: none;
}

.ab-faq__item summary svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  color: var(--es-muted);
  transition: transform 0.2s ease;
}

.ab-faq__item[open] summary svg {
  transform: rotate(180deg);
}

.ab-faq__item p {
  margin: -4px 0 16px !important;
  font-size: 14.5px;
  line-height: 1.6;
  color: var(--es-ink-soft);
}

.ab-aide {
  margin: 20px 0 8px !important;
  font-size: 14px;
  text-align: center;
  color: var(--es-muted);
}

.ab-aide a {
  font-weight: 700;
  color: var(--es-navy) !important;
}

/* Fenêtres (message, création du compte du bénéficiaire) */
.billing-modal-text {
  margin: 0 0 4px;
  color: var(--om-ink-soft, #2c3550);
  line-height: 1.55;
}

.billing-create-form {
  display: grid;
  gap: 14px;
  margin-top: 14px;
}

.billing-create-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.billing-field-error {
  font-size: 13px;
  font-weight: 600;
  color: var(--om-red, #c0392b);
}

/* Téléphone */
@media (max-width: 760px) {
  .ab-reglages {
    grid-template-columns: 1fr;
    gap: 18px;
    padding: 18px;
  }

  .ab-switch {
    margin-top: 0;
  }

  .ab-select select,
  .ab-input {
    font-size: 16px;
  }

  .ab-garanties {
    flex-direction: column;
    align-items: flex-start;
    margin: 22px 0 24px;
  }

  .ab-faq {
    padding: 18px 18px 6px;
  }

  .billing-create-row {
    grid-template-columns: 1fr;
  }
}
</style>
