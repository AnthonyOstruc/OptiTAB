<template>
  <div class="skeleton-card">
    <div class="skeleton-header">
      <div class="skeleton-line skeleton-title"></div>
      <div class="skeleton-line skeleton-subtitle"></div>
    </div>
    <div class="skeleton-content">
      <div class="skeleton-line skeleton-text"></div>
      <div class="skeleton-line skeleton-text short"></div>
    </div>
  </div>
</template>

<script setup>
// Skeleton card pour afficher pendant le chargement
</script>

<style scoped>
.skeleton-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  min-height: 150px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.skeleton-header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.skeleton-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: auto;
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
  height: 16px;
  width: 70%;
}

.skeleton-subtitle {
  height: 12px;
  width: 50%;
}

.skeleton-text {
  height: 10px;
  width: 100%;
}

.skeleton-text.short {
  width: 60%;
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
  .skeleton-card {
    padding: 1rem;
    min-height: 120px;
  }
}
</style>

