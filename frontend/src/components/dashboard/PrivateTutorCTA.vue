<template>
  <router-link to="/cours-particuliers" class="tutor-cta-card">
    <div class="tutor-icon">🎓</div>
    <div class="tutor-content">
      <div class="tutor-title">Accompagnement personnalisé</div>
      <div class="tutor-text">Progressez avec un prof particulier</div>
    </div>
    <div class="tutor-arrow">→</div>
  </router-link>
</template>

<script setup>
</script>

<style scoped>
.tutor-cta-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #fff;
  border: 2px solid #3b82f6;
  border-radius: 12px;
  padding: 0.95rem;
  margin-top: 1rem;
  text-decoration: none;
  transition: all 0.2s ease;
  cursor: pointer;
}

.tutor-cta-card:hover {
  border-color: #2563eb;
  background: #eff6ff;
}

.tutor-icon {
  font-size: 1.8rem;
  flex-shrink: 0;
}

.tutor-content {
  flex: 1;
}

.tutor-title {
  font-weight: 700;
  font-size: 0.92rem;
  color: #1e40af;
  margin-bottom: 0.15rem;
}

.tutor-text {
  font-size: 0.8rem;
  color: #64748b;
}

.tutor-arrow {
  font-size: 1.3rem;
  color: #3b82f6;
  font-weight: 700;
  flex-shrink: 0;
}

@media (max-width: 640px) {
  .tutor-cta-card {
    padding: 0.8rem;
  }
  
  .tutor-icon {
    font-size: 1.6rem;
  }
  
  .tutor-title {
    font-size: 0.86rem;
  }
  
  .tutor-text {
    font-size: 0.74rem;
  }
  
  .tutor-arrow {
    font-size: 1.2rem;
  }
}
</style>
