<template>
  <div class="skeleton-list">
    <div v-for="i in count" :key="i" class="skeleton-list-item">
      <div class="skeleton-item-header">
        <div class="skeleton-line skeleton-title"></div>
        <div class="skeleton-line skeleton-badge"></div>
      </div>
      <div class="skeleton-line skeleton-description"></div>
      <div class="skeleton-item-footer">
        <div class="skeleton-line skeleton-meta"></div>
        <div class="skeleton-line skeleton-meta short"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  count: { type: Number, default: 3 }
})
</script>

<style scoped>
.skeleton-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.skeleton-list-item {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.skeleton-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.skeleton-item-footer {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.skeleton-line {
  height: 12px;
  background: linear-gradient(
    90deg,
    #f3f4f6 0%,
    #e5e7eb 50%,
    #f3f4f6 100%
  );
  background-size: 200% 100%;
  border-radius: 4px;
  animation: skeleton-loading 1.5s ease-in-out infinite;
}

.skeleton-title {
  height: 18px;
  width: 60%;
}

.skeleton-badge {
  height: 24px;
  width: 80px;
  border-radius: 12px;
}

.skeleton-description {
  height: 14px;
  width: 85%;
}

.skeleton-meta {
  height: 12px;
  width: 100px;
}

.skeleton-meta.short {
  width: 60px;
}

@keyframes skeleton-loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .skeleton-list-item {
    padding: 1rem;
  }
  
  .skeleton-item-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .skeleton-title {
    width: 100%;
  }
}
</style>

