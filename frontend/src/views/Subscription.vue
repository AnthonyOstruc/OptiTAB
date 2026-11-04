<template>
  <DashboardLayout>
    <div class="ma">
      <header class="es-page-head ma-head">
        <div>
          <h1 class="es-h1">Mon abonnement</h1>
          <p class="es-sub">Ton accès, tes classes débloquées et tes factures.</p>
        </div>
        <router-link v-if="subscriptionStore.hasAccess" to="/billing" class="es-btn es-btn--ghost es-btn--sm" data-cta-name="subscribe" data-cta-location="subscription">
          Voir les formules
        </router-link>
      </header>

      <SubscriptionManager />

      <p class="ma-aide">
        Une question sur ton abonnement ? Écris-nous sur
        <a href="https://wa.me/33764040251" target="_blank" rel="noopener noreferrer" data-cta-name="whatsapp" data-cta-location="subscription">WhatsApp</a>
        ou à <a href="mailto:contact@optitab.net">contact@optitab.net</a>. Réponse sous 24 h.
      </p>
    </div>
  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import SubscriptionManager from '@/components/payments/SubscriptionManager.vue'
import { useSubscriptionStore } from '@/stores/subscription'

const subscriptionStore = useSubscriptionStore()
</script>

<style scoped>
.ma {
  max-width: 920px;
  margin: 0 auto;
}

.ma-head {
  align-items: center;
}

.ma-aide {
  margin: 24px 0 8px !important;
  font-size: 14px;
  text-align: center;
  color: var(--es-muted);
}

.ma-aide a {
  font-weight: 700;
  color: var(--es-navy) !important;
}
</style>
