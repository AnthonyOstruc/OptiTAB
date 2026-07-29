<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import { getLessonPaymentStatus } from '@/api/lessonPayment'
import { buildWhatsappUrl } from '@/config/bioLandingContent'

const route = useRoute()

const state = ref('loading') // loading | paid | pending | error
const amount = ref(null)
const label = ref('')
const payerName = ref('')

// « 5.00 € » sur une page francaise fait negligé : on affiche « 5,00 € ».
const formattedAmount = computed(() =>
  amount.value === null ? '' : Number(amount.value).toFixed(2).replace('.', ',')
)

const sessionId = computed(() => String(route.query.session_id || '').trim())
const whatsappUrl = computed(() =>
  buildWhatsappUrl("Bonjour, j'ai une question sur un versement effectué.")
)

// Le webhook Stripe peut arriver après le retour du client. On réinterroge
// quelques secondes plutôt que d'annoncer à tort un paiement non abouti.
const MAX_ATTEMPTS = 5
const RETRY_DELAY = 2000
let attempts = 0
let retryTimer = null

async function check() {
  if (!sessionId.value) {
    state.value = 'error'
    return
  }

  try {
    const { data } = await getLessonPaymentStatus(sessionId.value)
    amount.value = data?.amount ?? null
    label.value = data?.label || ''
    payerName.value = data?.payer_name || ''

    if (data?.paid) {
      state.value = 'paid'
      return
    }

    attempts += 1
    if (attempts < MAX_ATTEMPTS) {
      state.value = 'loading'
      retryTimer = window.setTimeout(check, RETRY_DELAY)
    } else {
      state.value = 'pending'
    }
  } catch (_) {
    state.value = 'error'
  }
}

onMounted(check)

onBeforeUnmount(() => {
  if (retryTimer) window.clearTimeout(retryTimer)
})
</script>

<template>
  <MainLayout header-variant="landing" footer-variant="landing">
    <div class="thanks">
      <div class="thanks__card">
        <!-- Paiement confirmé -->
        <template v-if="state === 'paid'">
          <span class="thanks__icon thanks__icon--ok" aria-hidden="true">
            <svg viewBox="0 0 24 24">
              <path
                d="M5 12.5l4.5 4.5L19 7.5"
                fill="none"
                stroke="currentColor"
                stroke-width="2.4"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </span>
          <h1>Paiement reçu</h1>
          <p v-if="amount" class="thanks__amount">{{ formattedAmount }} €</p>
          <p v-if="label" class="thanks__label">{{ label }}</p>
          <p class="thanks__text">
            Merci{{ payerName ? `, ${payerName}` : '' }}. Un reçu vous est envoyé par e-mail.
          </p>
        </template>

        <!-- En cours de vérification -->
        <template v-else-if="state === 'loading'">
          <span class="thanks__spinner" aria-hidden="true"></span>
          <h1>Vérification en cours</h1>
          <p class="thanks__text">Quelques secondes, le temps que la banque confirme.</p>
        </template>

        <!-- Confirmation tardive -->
        <template v-else-if="state === 'pending'">
          <span class="thanks__icon thanks__icon--wait" aria-hidden="true">
            <svg viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="1.9" />
              <path
                d="M12 7.5V12l3 1.8"
                fill="none"
                stroke="currentColor"
                stroke-width="1.9"
                stroke-linecap="round"
              />
            </svg>
          </span>
          <h1>Paiement en cours de traitement</h1>
          <p class="thanks__text">
            Votre banque n'a pas encore confirmé. C'est généralement une affaire de minutes.
            Si vous avez été débité sans recevoir de reçu, écrivez-nous.
          </p>
        </template>

        <!-- Session introuvable -->
        <template v-else>
          <span class="thanks__icon thanks__icon--err" aria-hidden="true">
            <svg viewBox="0 0 24 24">
              <path
                d="M12 7.5v5.5M12 16.2v.6"
                fill="none"
                stroke="currentColor"
                stroke-width="2.2"
                stroke-linecap="round"
              />
              <circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="1.9" />
            </svg>
          </span>
          <h1>Versement introuvable</h1>
          <p class="thanks__text">
            Ce lien de confirmation n'est plus valide. Si vous avez été débité,
            contactez-nous, on vérifie tout de suite.
          </p>
        </template>

        <div class="thanks__actions">
          <a
            :href="whatsappUrl"
            class="thanks__btn thanks__btn--wa"
            target="_blank"
            rel="noopener noreferrer"
            data-cta-name="whatsapp"
            data-cta-location="lesson_payment_thanks"
          >
            <svg viewBox="0 0 32 32" aria-hidden="true" class="thanks__wa-icon">
              <path fill="currentColor" d="M26.576 5.363c-2.69-2.69-6.406-4.354-10.511-4.354-8.209 0-14.865 6.655-14.865 14.865 0 2.732 0.737 5.291 2.022 7.491l-0.038-0.070-2.109 7.702 7.879-2.067c2.051 1.139 4.498 1.809 7.102 1.809h0.006c8.209-0.003 14.862-6.659 14.862-14.868 0-4.103-1.662-7.817-4.349-10.507l0 0zM16.062 28.228h-0.005c-0 0-0.001 0-0.001 0-2.319 0-4.489-0.64-6.342-1.753l0.056 0.031-0.451-0.267-4.675 1.227 1.247-4.559-0.294-0.467c-1.185-1.862-1.889-4.131-1.889-6.565 0-6.822 5.531-12.353 12.353-12.353s12.353 5.531 12.353 12.353c0 6.822-5.53 12.353-12.353 12.353h-0zM22.838 18.977c-0.371-0.186-2.197-1.083-2.537-1.208-0.341-0.124-0.589-0.185-0.837 0.187-0.246 0.371-0.958 1.207-1.175 1.455-0.216 0.249-0.434 0.279-0.805 0.094-1.15-0.466-2.138-1.087-2.997-1.852l0.010 0.009c-0.799-0.74-1.484-1.587-2.037-2.521l-0.028-0.052c-0.216-0.371-0.023-0.572 0.162-0.757 0.167-0.166 0.372-0.434 0.557-0.65 0.146-0.179 0.271-0.384 0.366-0.604l0.006-0.017c0.043-0.087 0.068-0.188 0.068-0.296 0-0.131-0.037-0.253-0.101-0.357l0.002 0.003c-0.094-0.186-0.836-2.014-1.145-2.758-0.302-0.724-0.609-0.625-0.836-0.637-0.216-0.010-0.464-0.012-0.712-0.012-0.395 0.010-0.746 0.188-0.988 0.463l-0.001 0.002c-0.802 0.761-1.3 1.834-1.3 3.023 0 0.026 0 0.053 0.001 0.079l-0-0.004c0.131 1.467 0.681 2.784 1.527 3.857l-0.012-0.015c1.604 2.379 3.742 4.282 6.251 5.564l0.094 0.043c0.548 0.248 1.25 0.513 1.968 0.74l0.149 0.041c0.442 0.14 0.951 0.221 1.479 0.221 0.303 0 0.601-0.027 0.889-0.078l-0.031 0.004c1.069-0.223 1.956-0.868 2.497-1.749l0.009-0.017c0.165-0.366 0.261-0.793 0.261-1.242 0-0.185-0.016-0.366-0.047-0.542l0.003 0.019c-0.092-0.155-0.34-0.247-0.712-0.434z" />
            </svg>
            Écrire sur WhatsApp
          </a>
          <router-link to="/" class="thanks__btn thanks__btn--ghost">
            Retour à l'accueil
          </router-link>
        </div>

      </div>
    </div>
  </MainLayout>
</template>

<style scoped lang="scss">
.thanks {
  background: linear-gradient(180deg, #f8fbff 0%, #ffffff 45%, #f6f8ff 100%);
  min-height: 100%;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 40px 16px 72px;
}

.thanks__card {
  width: 100%;
  max-width: 480px;
  padding: 30px 24px 26px;
  border-radius: 18px;
  border: 1px solid #cfe0ff;
  background: #ffffff;
  box-shadow: 0 10px 26px rgba(30, 58, 138, 0.07);
  text-align: center;
}

.thanks__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  margin-bottom: 16px;
  border-radius: 50%;

  svg {
    width: 28px;
    height: 28px;
  }

  &--ok {
    background: #e7f8ec;
    color: #128c4a;
  }

  &--wait {
    background: #fffbeb;
    color: #b45309;
  }

  &--err {
    background: #fef2f2;
    color: #b91c1c;
  }
}

.thanks__spinner {
  display: inline-block;
  width: 34px;
  height: 34px;
  margin-bottom: 18px;
  border: 3px solid #dbe4ff;
  border-top-color: #2a38b7;
  border-radius: 50%;
  animation: thanks-spin 0.8s linear infinite;
}

@keyframes thanks-spin {
  to {
    transform: rotate(360deg);
  }
}

.thanks__card h1 {
  margin: 0 0 10px;
  font-size: clamp(1.35rem, 4.4vw, 1.7rem);
  line-height: 1.2;
  color: #0f172a;
}

.thanks__amount {
  margin: 0 0 4px;
  font-size: 2.1rem;
  font-weight: 800;
  color: #1e3a8a;
  letter-spacing: -0.02em;
}

.thanks__label {
  margin: 0 0 12px;
  color: #475569;
  font-size: 0.92rem;
  font-weight: 600;
}

.thanks__text {
  margin: 0;
  color: #475569;
  font-size: 0.96rem;
  line-height: 1.55;
}

.thanks__actions {
  display: flex;
  flex-direction: column;
  gap: 9px;
  margin-top: 22px;
}

.thanks__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 46px;
  padding: 0 18px;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 700;
  text-decoration: none;
  /* Un libelle coupe en deux lignes casse l'alignement des deux boutons. */
  white-space: nowrap;

  &--wa {
    border: 1px solid #1eb257;
    background: #25d366;
    color: #052e16;

    &:hover {
      background: #22c55e;
      color: #052e16;
    }
  }

  &--ghost {
    border: 1px solid #c8d6fa;
    background: #fff;
    color: #1f2937;

    &:hover {
      background: #f4f8ff;
      color: #1f2937;
    }
  }
}

.thanks__wa-icon {
  width: 17px;
  height: 17px;
  flex-shrink: 0;
}

@media (min-width: 560px) {
  .thanks__actions {
    flex-direction: row;
    justify-content: center;
  }

  /* Pas de `flex: 1` : etirer les boutons a parts egales forcait le libelle
     WhatsApp a se replier sur deux lignes. */
}

@media (prefers-reduced-motion: reduce) {
  .thanks__spinner {
    animation-duration: 2.4s;
  }
}
</style>
