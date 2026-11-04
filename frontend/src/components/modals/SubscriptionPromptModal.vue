<template>
  <Modal
    :is-open="isOpen"
    title="Accède à tout OptiTAB"
    subtitle="Toute ta classe, sans limite."
    :icon="LockOpenIcon"
    centered
    size="small"
    @close="fermer"
  >
    <div class="sp">
      <p class="sp-prix">
        <span class="sp-prix__des">Dès</span>
        <strong>{{ prixMinimum }}</strong>
      </p>
      <p class="sp-prix__note">Pass ponctuel ou abonnement sans engagement</p>

      <ul class="sp-avantages">
        <li v-for="avantage in AVANTAGES" :key="avantage">
          <CheckIcon aria-hidden="true" />
          {{ avantage }}
        </li>
      </ul>

      <button type="button" class="om-btn om-btn--primary om-btn--block" data-cta-name="pricing" data-cta-location="dashboard-modal" @click="voirLesFormules">
        Voir les formules
        <ArrowRightIcon aria-hidden="true" />
      </button>
      <button type="button" class="om-link sp-plus-tard" @click="fermer">Plus tard</button>

      <p class="sp-rassurance">
        <ShieldCheckIcon aria-hidden="true" />
        Paiement sécurisé · Sans engagement
      </p>
    </div>
  </Modal>
</template>

<script setup>
// Invitation à s'abonner (espace élève) : court et simple. Le prix d'appel est
// le plus bas des formules en vente ; le choix se fait sur la page Abonnement.
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import Modal from '@/components/common/Modal.vue'
import { getPlans } from '@/api/subscriptions'
import { DEFAULT_PLANS } from '@/config/subscriptions'
import { ArrowRightIcon, CheckIcon, LockOpenIcon, ShieldCheckIcon } from '@heroicons/vue/24/outline'

defineProps({
  isOpen: { type: Boolean, default: false }
})

const emit = defineEmits(['close'])
const router = useRouter()

const AVANTAGES = [
  'Tous les chapitres de ta classe',
  'Tous les exercices corrigés pas à pas',
  'Le suivi de tes progrès et des exercices à revoir'
]

const plans = ref(DEFAULT_PLANS)
onMounted(async () => {
  try {
    const { data } = await getPlans()
    const liste = Array.isArray(data?.plans) ? data.plans : Array.isArray(data) ? data : []
    if (liste.length) plans.value = liste
  } catch {
    // Prix par défaut en cas de coupure réseau.
  }
})

const prixMinimum = computed(() => {
  const prix = plans.value.map((p) => Number(p.price)).filter((p) => p > 0)
  const min = prix.length ? Math.min(...prix) : 0
  return `${min.toFixed(2).replace('.', ',')} €`
})

function fermer() {
  emit('close')
}

function voirLesFormules() {
  emit('close')
  router.push({ name: 'Billing', hash: '#plans' })
}
</script>

<style scoped>
/* Cadre et éléments communs (.om-btn, .om-link) : components/common/Modal.vue */
.sp {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.sp-prix {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 8px;
  margin: 4px 0 0;
  color: var(--om-navy-900, #0d1f4f);
}

.sp-prix__des {
  font-size: 18px;
  font-weight: 600;
  color: var(--om-muted, #5d667d);
}

.sp-prix strong {
  font-size: 44px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.sp-prix__note {
  margin: 6px 0 22px;
  font-size: 14px;
  color: var(--om-muted, #5d667d);
}

.sp-avantages {
  display: grid;
  gap: 10px;
  width: 100%;
  margin: 0 0 24px;
  padding: 18px 20px;
  border-radius: 14px;
  background: var(--om-bg-soft, #f6f8fc);
  list-style: none;
  text-align: left;
}

.sp-avantages li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 15px;
  font-weight: 600;
  line-height: 1.4;
  color: var(--om-ink, #172033);
}

.sp-avantages svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  color: var(--om-green-700, #2f7a3a);
  stroke-width: 2.4;
}

.sp-plus-tard {
  margin-top: 12px;
  font-size: 14.5px;
}

.sp-rassurance {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin: 18px 0 0;
  font-size: 13px;
  color: var(--om-muted, #5d667d);
}

.sp-rassurance svg {
  width: 16px;
  height: 16px;
}
</style>
