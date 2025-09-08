<template>
  <DashboardLayout>
    <template #default>
      <component :is="dashboardComponent" />
    </template>
  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'
import DashboardStudent from '@/components/dashboard/DashboardStudent.vue'
import DashboardParent from '@/components/dashboard/DashboardParent.vue'

const userStore = useUserStore()
const dashboardComponent = computed(() => (userStore.role === 'parent' ? DashboardParent : DashboardStudent))
</script>

<style scoped>
</style>
