<template>
  <div class="billing-tabs" role="navigation" aria-label="Abonnement">
    <button
      class="tab"
      :class="{ active: activeTab === 'Subscription' }"
      :aria-label="ctaLabel"
      data-cta-name="subscribe"
      data-cta-location="header_dashboard"
      @click="navigate('Subscription')"
    >
      <svg class="icon" viewBox="0 0 24 24" aria-hidden="true">
        <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <span>{{ ctaLabel }}</span>
    </button>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useSubscriptionStore } from '@/stores/subscription'

const router = useRouter()
const route = useRoute()
const subscriptionStore = useSubscriptionStore()

const activeTab = computed(() => route.name)
// Mobile clarity: adapt the CTA label to user status
const hasAccess = computed(() => subscriptionStore.hasAccess)
const ctaLabel = computed(() => hasAccess.value ? 'Gérer mon abonnement' : 'Activer mon accès')

const navigate = (name) => {
  if (route.name === name) return
  router.push({ name })
}

onMounted(() => {
  if (!subscriptionStore.loading) {
    subscriptionStore.fetchStatus({ force: !subscriptionStore.hasAccess }).catch(() => {})
  }
})
</script>

<style scoped>
.billing-tabs {
  display: flex;
  align-items: center;
  justify-content: center;
}

.tab {
  border: 1px solid #122a66;
  background: #1b3c8e;
  color: #ffffff;
  padding: 0.6rem 1.2rem;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.18s ease;
  font-weight: 600;
  font-size: 0.95rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 6px 14px rgba(27, 60, 142, 0.22);
}

.tab:hover {
  background: #122a66;
  border-color: #122a66;
  transform: translateY(-1px);
  box-shadow: 0 10px 20px rgba(18, 42, 102, 0.25);
}

.tab.active {
  background: linear-gradient(90deg, #1b3c8e 0%, #122a66 100%);
  border-color: #122a66;
  box-shadow: 0 12px 26px rgba(27, 60, 142, 0.28);
}

.tab:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px rgba(27, 60, 142, 0.35), 0 8px 20px rgba(18, 42, 102, 0.25);
}

.icon {
  width: 1.05rem;
  height: 1.05rem;
}

@media (max-width: 640px) {
  .tab {
    font-size: 0.9rem;
    padding: 0.5rem 0.9rem;
    box-shadow: 0 4px 10px rgba(27, 60, 142, 0.18);
  }
}
</style>
