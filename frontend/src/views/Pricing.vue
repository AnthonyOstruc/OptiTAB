<template>
  <DashboardLayout>
    <div class="pricing-page">
      <PricingPlans />
    </div>
  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import PricingPlans from '@/components/payments/PricingPlans.vue'
</script>

<style scoped>
.pricing-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}
</style>