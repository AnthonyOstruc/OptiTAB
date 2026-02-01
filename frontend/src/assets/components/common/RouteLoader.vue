<template>
  <div class="route-loader">
    <div class="route-loader-header">
      <div class="skeleton-line skeleton-title"></div>
      <div class="skeleton-line skeleton-subtitle"></div>
    </div>
    <div class="skeleton-grid">
      <div v-for="i in 6" :key="i" class="skeleton-card">
        <div class="skeleton-line skeleton-card-title"></div>
        <div class="skeleton-line skeleton-card-text"></div>
        <div class="skeleton-line skeleton-card-text short"></div>
      </div>
    </div>
  </div>
 </template>

<script setup>
// Pure skeleton component for route-level loading states
</script>

<style scoped>
.route-loader {
  background: #fff;
  border-radius: 12px;
  padding: 1.25rem;
}
.route-loader-header { margin-bottom: 1rem; }
.skeleton-line {
  height: 12px;
  background: linear-gradient(90deg, #f3f4f6 0%, #e5e7eb 50%, #f3f4f6 100%);
  background-size: 200% 100%;
  border-radius: 6px;
  animation: skeleton-loading 1.3s ease-in-out infinite;
}
.skeleton-title { height: 22px; width: 240px; margin-bottom: 10px; }
.skeleton-subtitle { width: 320px; }

.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(260px, 1fr));
  gap: 1rem;
}
.skeleton-card { padding: 1rem; border: 1px solid #eef2f7; border-radius: 10px; }
.skeleton-card-title { width: 70%; height: 18px; margin-bottom: 10px; }
.skeleton-card-text { width: 100%; }
.skeleton-card-text.short { width: 60%; margin-top: 8px; }

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@media (max-width: 1100px) {
  .skeleton-grid { grid-template-columns: repeat(2, minmax(260px, 1fr)); }
}
@media (max-width: 700px) {
  .skeleton-grid { grid-template-columns: 1fr; }
}
</style>

