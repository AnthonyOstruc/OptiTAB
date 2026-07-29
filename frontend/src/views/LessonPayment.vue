<script setup>
import { computed, onMounted, ref } from 'vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import { createLessonPaymentSession, getLessonPaymentConfig } from '@/api/lessonPayment'

// Montants proposés en un clic : couvrent les durées de cours habituelles.
// Ils ne limitent rien, le champ reste libre.
const QUICK_AMOUNTS = [25, 30, 40, 50, 60, 80]

const minAmount = ref(5)
const maxAmount = ref(500)

const amount = ref('')
const label = ref('')
const payerName = ref('')

const submitting = ref(false)
const errorMessage = ref('')

// Normalise « 42,50 » en « 42.50 » : les deux se saisissent naturellement.
const normalizedAmount = computed(() =>
  String(amount.value).trim().replace(',', '.').replace(/\s/g, '')
)

const parsedAmount = computed(() => {
  const value = Number(normalizedAmount.value)
  return Number.isFinite(value) ? value : null
})

// Validation d'ergonomie uniquement : le serveur revalide tout.
const amountError = computed(() => {
  if (!normalizedAmount.value) return ''
  if (parsedAmount.value === null) return 'Indiquez un montant valide.'
  if (parsedAmount.value < minAmount.value) return `Minimum ${minAmount.value} €.`
  if (parsedAmount.value > maxAmount.value) return `Maximum ${maxAmount.value} €.`
  if (!/^\d+([.]\d{1,2})?$/.test(normalizedAmount.value)) {
    return 'Deux décimales au maximum.'
  }
  return ''
})

// Affichage a la francaise : l'utilisateur saisit « 42,50 », le bouton ne
// doit pas lui repondre « 42.50 ».
const formattedAmount = computed(() =>
  parsedAmount.value === null ? '' : parsedAmount.value.toFixed(2).replace('.', ',')
)

const canSubmit = computed(
  () => !submitting.value && Boolean(normalizedAmount.value) && !amountError.value
)

function pickAmount(value) {
  amount.value = String(value)
  errorMessage.value = ''
}

async function submit() {
  if (!canSubmit.value) return

  submitting.value = true
  errorMessage.value = ''

  try {
    const { data } = await createLessonPaymentSession({
      amount: normalizedAmount.value,
      label: label.value.trim(),
      payer_name: payerName.value.trim()
    })

    // Le backend renvoie `url` (et `session_id`, non utilisé ici :
    // Stripe le rajoute lui-même à l'URL de retour).
    if (data?.url) {
      // Redirection vers Stripe : aucune donnée bancaire ne transite ici.
      window.location.href = data.url
      return
    }

    errorMessage.value = "Le paiement n'a pas pu être ouvert. Réessayez."
    submitting.value = false
  } catch (error) {
    // Trois causes distinctes se cachaient derriere un message unique :
    // serveur injoignable, quota depasse, refus de Stripe. Sur une page de
    // paiement, savoir laquelle change ce que la personne doit faire.
    const status = error?.response?.status
    const body = error?.response?.data

    if (!error?.response) {
      errorMessage.value =
        'Connexion au serveur impossible. Vérifiez votre connexion internet et réessayez.'
    } else if (status === 429) {
      errorMessage.value =
        'Trop de tentatives depuis cet appareil. Patientez quelques minutes avant de réessayer.'
    } else if (body?.error) {
      // Message precis renvoye par le serveur (montant hors bornes, etc.).
      errorMessage.value = body.error
    } else {
      errorMessage.value =
        "Le paiement n'a pas pu être initialisé. Réessayez dans un instant."
    }

    submitting.value = false
  }
}

onMounted(async () => {
  // Les bornes viennent du serveur : l'affichage ne peut pas diverger
  // des règles réellement appliquées.
  try {
    const { data } = await getLessonPaymentConfig()
    if (data?.min_amount) minAmount.value = Number(data.min_amount)
    if (data?.max_amount) maxAmount.value = Number(data.max_amount)
  } catch (_) {
    // Valeurs par défaut conservées : le serveur tranchera de toute façon.
  }
})
</script>

<template>
  <MainLayout header-variant="landing" footer-variant="landing">
    <div class="pay">
      <div class="pay__shell">
        <header class="pay__head">
          <p class="pay__kicker">OptiTAB — Cours particuliers</p>
          <h1>Régler un cours</h1>
          <p class="pay__intro">
            Indiquez le montant convenu, puis réglez par carte bancaire.
            Un reçu vous est envoyé par e-mail.
          </p>
        </header>

        <form class="pay__card" @submit.prevent="submit">
          <label class="field field--amount">
            <span class="field__label">Montant</span>
            <div class="amount-input" :class="{ 'has-error': amountError }">
              <input
                v-model="amount"
                type="text"
                inputmode="decimal"
                autocomplete="off"
                placeholder="0"
                aria-label="Montant à régler en euros"
              />
              <span class="amount-input__currency" aria-hidden="true">€</span>
            </div>
            <p v-if="amountError" class="field__error">{{ amountError }}</p>
            <p v-else class="field__hint">Entre {{ minAmount }} € et {{ maxAmount }} €.</p>
          </label>

          <div class="quick">
            <button
              v-for="value in QUICK_AMOUNTS"
              :key="value"
              type="button"
              class="quick__btn"
              :class="{ 'is-active': normalizedAmount === String(value) }"
              @click="pickAmount(value)"
            >
              {{ value }} €
            </button>
          </div>

          <label class="field">
            <span class="field__label">
              Objet <em>facultatif</em>
            </span>
            <input
              v-model="label"
              type="text"
              maxlength="140"
              placeholder="Cours du 12 mars, 1h30"
            />
          </label>

          <label class="field">
            <span class="field__label">
              Votre nom <em>facultatif</em>
            </span>
            <input v-model="payerName" type="text" maxlength="120" placeholder="Prénom Nom" />
          </label>

          <p v-if="errorMessage" class="pay__error" role="alert">{{ errorMessage }}</p>

          <button type="submit" class="pay__submit" :disabled="!canSubmit">
            <span v-if="submitting">Ouverture du paiement…</span>
            <span v-else-if="parsedAmount">Payer {{ formattedAmount }} €</span>
            <span v-else>Payer</span>
          </button>

          <p class="pay__secure">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path
                d="M12 3l7 3v6c0 4.2-2.9 7.9-7 9-4.1-1.1-7-4.8-7-9V6l7-3Z"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linejoin="round"
              />
              <path
                d="M9 12.5l2 2 4-4.5"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
            Paiement sécurisé par Stripe. Vos données bancaires ne transitent jamais par OptiTAB.
          </p>
        </form>
      </div>
    </div>
  </MainLayout>
</template>

<style scoped lang="scss">
/* Reprend la charte des autres pages : fond bleute, cartes 16px,
   bordures #cfe0ff, CTA bleu 50px. */

.pay {
  background: linear-gradient(180deg, #f8fbff 0%, #ffffff 45%, #f6f8ff 100%);
  min-height: 100%;
}

.pay__shell {
  max-width: 560px;
  margin: 0 auto;
  padding: 30px 16px 72px;
}

.pay__head {
  margin-bottom: 20px;
}

.pay__kicker {
  margin: 0;
  color: #2a38b7;
  font-size: 0.82rem;
  font-weight: 800;
  letter-spacing: 0.02em;
}

.pay__head h1 {
  margin: 10px 0 0;
  font-size: clamp(1.6rem, 5vw, 2.1rem);
  line-height: 1.15;
  color: #0f172a;
}

.pay__intro {
  margin: 12px 0 0;
  color: #475569;
  font-size: 0.98rem;
  line-height: 1.55;
}

.pay__card {
  padding: 22px 20px;
  border-radius: 16px;
  border: 1px solid #cfe0ff;
  background: #ffffff;
  box-shadow: 0 10px 26px rgba(30, 58, 138, 0.07);
}

/* ---------- Champ montant ---------- */

.field {
  display: block;
  margin-bottom: 18px;
}

.field__label {
  display: block;
  margin-bottom: 7px;
  font-size: 0.88rem;
  font-weight: 700;
  color: #1e293b;

  em {
    font-style: normal;
    font-weight: 500;
    color: #94a3b8;
  }
}

.field input[type='text'] {
  width: 100%;
  min-height: 46px;
  padding: 0 13px;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  background: #fff;
  font-family: inherit;
  font-size: 0.98rem;
  color: #0f172a;

  &:focus {
    outline: none;
    border-color: #2a38b7;
    box-shadow: 0 0 0 3px rgba(42, 56, 183, 0.12);
  }
}

.amount-input {
  position: relative;
  display: flex;
  align-items: center;
  border: 1.5px solid #cbd5e1;
  border-radius: 12px;
  background: #fff;
  transition: border-color 0.18s ease, box-shadow 0.18s ease;

  &:focus-within {
    border-color: #2a38b7;
    box-shadow: 0 0 0 3px rgba(42, 56, 183, 0.12);
  }

  &.has-error {
    border-color: #dc2626;
  }

  /* `input[type="text"]` est plus specifique que `.amount-input input` :
     sans ce selecteur, la bordure generique des champs reapparait ici et
     dessine un trait entre le montant et le symbole euro. */
  input[type='text'] {
    flex: 1;
    min-width: 0;
    min-height: 62px;
    padding: 0 8px 0 16px;
    border: none;
    background: transparent;
    font-family: inherit;
    /* Chiffre volontairement grand : c'est LA donnee de la page. */
    font-size: 2rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.02em;

    &:focus {
      outline: none;
      box-shadow: none;
    }
  }
}

.amount-input__currency {
  padding-right: 18px;
  font-size: 1.6rem;
  font-weight: 800;
  color: #64748b;
}

.field__hint,
.field__error {
  margin: 6px 0 0;
  font-size: 0.82rem;
}

.field__hint {
  color: #64748b;
}

.field__error {
  color: #b91c1c;
  font-weight: 600;
}

/* ---------- Montants rapides ---------- */

.quick {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
  margin: -6px 0 20px;
}

.quick__btn {
  min-height: 40px;
  border: 1px solid #cfe0ff;
  border-radius: 10px;
  background: #f8fbff;
  font-family: inherit;
  font-size: 0.92rem;
  font-weight: 700;
  color: #1e3a8a;
  cursor: pointer;
  transition: background 0.16s ease, border-color 0.16s ease;

  &:hover {
    background: #eef4ff;
    border-color: #a8c1ff;
  }

  &.is-active {
    background: #2a38b7;
    border-color: #2a38b7;
    color: #fff;
  }

  &:focus-visible {
    outline: 2px solid #2a38b7;
    outline-offset: 2px;
  }
}

/* ---------- Validation ---------- */

.pay__error {
  margin: 0 0 14px;
  padding: 11px 13px;
  border-radius: 10px;
  border: 1px solid #fecaca;
  background: #fef2f2;
  color: #b91c1c;
  font-size: 0.88rem;
  line-height: 1.5;
}

.pay__submit {
  width: 100%;
  min-height: 52px;
  border: 1px solid #1f4ed2;
  border-radius: 14px;
  background: linear-gradient(180deg, #2f6df4 0%, #2155d8 100%);
  color: #fff;
  font-family: inherit;
  font-size: 1.02rem;
  font-weight: 800;
  cursor: pointer;
  transition: transform 0.18s ease, box-shadow 0.18s ease;

  &:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 12px 28px rgba(37, 99, 235, 0.3);
  }

  &:disabled {
    background: #cbd5e1;
    border-color: #cbd5e1;
    cursor: not-allowed;
  }
}

.pay__secure {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin: 14px 0 0;
  color: #64748b;
  font-size: 0.82rem;
  line-height: 1.5;

  svg {
    flex-shrink: 0;
    width: 16px;
    height: 16px;
    margin-top: 1px;
    color: #16a34a;
  }
}

/* ---------- Ecrans larges ---------- */

@media (min-width: 640px) {
  .pay__shell {
    padding-top: 44px;
  }

  .pay__card {
    padding: 28px 26px;
  }

  .quick {
    grid-template-columns: repeat(6, minmax(0, 1fr));
  }
}

@media (prefers-reduced-motion: reduce) {
  .pay__submit,
  .quick__btn,
  .amount-input {
    transition: none;
  }

  .pay__submit:hover:not(:disabled) {
    transform: none;
  }
}
</style>
