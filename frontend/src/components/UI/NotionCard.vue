<template>
  <div class="notion-card" @click="$emit('click')">
    <div class="notion-card-inner">
      <!-- Icône de la notion -->
      <div class="notion-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      
      <!-- Contenu de la notion -->
      <div class="notion-content">
        <h3 class="notion-title">{{ title }}</h3>
        <p class="notion-description">{{ description || 'Cliquez pour explorer les chapitres' }}</p>
      </div>
      
      <!-- Indicateur d'action -->
      <div class="notion-arrow">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  description: { type: String, default: '' }
})
</script>

<style scoped>
.notion-card {
  width: 100%;
  max-width: 240px;
  margin: 0 auto;
}

.notion-card-inner {
  position: relative;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.notion-card-inner:hover {
  border-color: #3b82f6;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Icône */
.notion-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 36px;
  height: 36px;
  background: #3b82f6;
  border-radius: 6px;
  margin-bottom: 0.75rem;
  color: white;
}

/* Contenu */
.notion-content {
  flex: 1;
  margin-bottom: 0.75rem;
}

.notion-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.25rem 0;
  line-height: 1.3;
}

.notion-description {
  font-size: 0.75rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.3;
}

/* Flèche */
.notion-arrow {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 24px;
  height: 24px;
  background: #f3f4f6;
  border-radius: 4px;
  color: #6b7280;
}

/* Responsive */
@media (max-width: 768px) {
  .notion-card {
    max-width: 220px;
  }
  
  .notion-card-inner {
    padding: 0.875rem;
  }
  
  .notion-icon {
    width: 32px;
    height: 32px;
    margin-bottom: 0.625rem;
  }
  
  .notion-title {
    font-size: 0.8rem;
  }
  
  .notion-description {
    font-size: 0.7rem;
  }
  
  .notion-arrow {
    width: 20px;
    height: 20px;
  }
}

@media (max-width: 480px) {
  .notion-card {
    max-width: 200px;
  }
  
  .notion-card-inner {
    padding: 0.75rem;
  }
  
  .notion-icon {
    width: 28px;
    height: 28px;
    margin-bottom: 0.5rem;
  }
  
  .notion-title {
    font-size: 0.75rem;
  }
  
  .notion-description {
    font-size: 0.65rem;
  }
  
  .notion-arrow {
    width: 18px;
    height: 18px;
  }
}
</style> 