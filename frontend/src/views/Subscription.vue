<template>
  <DashboardLayout>
    <div class="subscription-page">
      <SubscriptionManager />
    </div>
  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import SubscriptionManager from '@/components/payments/SubscriptionManager.vue'
</script>

<style scoped>
.subscription-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  padding: 2rem 0;
}
</style>
