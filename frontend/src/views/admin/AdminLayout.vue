<template>
  <DashboardLayout>
    <div class="admin-layout">
      <div class="admin-content">
        <router-view />
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { useRoute } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
const route = useRoute()
function isActive(name) {
  return route.name === name
}
</script>

<style scoped>
.admin-layout {
  width: 100%;
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.admin-content {
  width: 100%;
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}
</style> 