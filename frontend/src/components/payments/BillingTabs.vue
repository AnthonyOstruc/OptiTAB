<template>
  <div class="billing-tabs" role="navigation" aria-label="Abonnement">
    <button
      class="tab"
      :class="{ active: activeTab === 'Subscription' }"
      :aria-label="ctaLabel"
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
  border: 1px solid #1e40af;
  background: #2563eb;
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
  box-shadow: 0 6px 14px rgba(37, 99, 235, 0.22);
}

.tab:hover {
  background: #1e40af;
  border-color: #1e40af;
  transform: translateY(-1px);
  box-shadow: 0 10px 20px rgba(30, 64, 175, 0.25);
}

.tab.active {
  background: linear-gradient(90deg, #2563eb 0%, #1e40af 100%);
  border-color: #1e40af;
  box-shadow: 0 12px 26px rgba(37, 99, 235, 0.28);
}

.tab:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.35), 0 8px 20px rgba(30, 64, 175, 0.25);
}

.icon {
  width: 1.05rem;
  height: 1.05rem;
}

@media (max-width: 640px) {
  .tab {
    font-size: 0.9rem;
    padding: 0.5rem 0.9rem;
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.18);
  }
}
</style>
