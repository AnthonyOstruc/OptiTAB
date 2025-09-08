<template>
  <div class="admin-pays-wrapper">
    <PaysAdmin />
  </div>
</template>

<script>
import PaysAdmin from '@/components/admin/PaysAdmin.vue'

export default {
  name: 'AdminPays',
  components: {
    PaysAdmin
  }
}
</script>

<style scoped>
.admin-pays-wrapper {
  width: 100%;
  height: 100%;
}
</style>