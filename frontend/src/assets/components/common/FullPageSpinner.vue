<template>
  <div class="fullpage-spinner">
    <span class="spinner"></span>
  </div>
</template>

<style scoped>
.fullpage-spinner {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(255,255,255,0.85);
  z-index: 99999;
  display: flex;
  align-items: center;
  justify-content: center;
}
.spinner {
  width: 48px;
  height: 48px;
  border: 5px solid #e5e7eb;
  border-top: 5px solid #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style> 