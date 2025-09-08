<template>
  <div class="theme-card" @click="$emit('click')" :style="{ '--theme-color': themeColor }">
    <div class="theme-card-inner">
      <!-- Icône du thème -->
      <div class="theme-icon">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      
      <!-- Contenu du thème -->
      <div class="theme-content">
        <h3 class="theme-title">{{ title }}</h3>
        <p class="theme-description">{{ description || 'Cliquez pour explorer les notions' }}</p>
        <div class="theme-badge">
          <span class="notion-count">{{ notionCount }} notion{{ notionCount > 1 ? 's' : '' }}</span>
        </div>
      </div>
      
      <!-- Indicateur d'action -->
      <div class="theme-arrow">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      
      <!-- Effet de brillance -->
      <div class="theme-shine"></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  description: { type: String, default: '' },
  themeColor: { type: String, default: '#3b82f6' },
  notionCount: { type: Number, default: 0 }
})
</script>

<style scoped>
.theme-card {
  width: 100%;
  max-width: 340px;
  perspective: 1000px;
}

.theme-card-inner {
  position: relative;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.theme-card-inner:hover {
  transform: translateY(-6px) scale(1.02);
  border-color: var(--theme-color);
  box-shadow: 
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04),
    0 0 0 4px rgba(var(--theme-color), 0.1);
}

.theme-card-inner:active {
  transform: translateY(-4px) scale(1.01);
}

/* Icône */
.theme-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 56px;
  height: 56px;
  background: var(--theme-color);
  border-radius: 14px;
  margin: 0 auto 1.25rem;
  color: white;
  transition: all 0.3s ease;
}

.theme-card-inner:hover .theme-icon {
  transform: scale(1.1) rotate(5deg);
  box-shadow: 0 8px 16px rgba(var(--theme-color), 0.3);
}

/* Contenu */
.theme-content {
  text-align: center;
  margin-bottom: 1rem;
}

.theme-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  line-height: 1.3;
  transition: color 0.3s ease;
}

.theme-card-inner:hover .theme-title {
  color: var(--theme-color);
}

.theme-description {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0 0 0.75rem 0;
  line-height: 1.5;
  transition: color 0.3s ease;
}

.theme-card-inner:hover .theme-description {
  color: #475569;
}

.theme-badge {
  display: inline-flex;
  align-items: center;
  background: #f1f5f9;
  color: #475569;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.theme-card-inner:hover .theme-badge {
  background: var(--theme-color);
  color: white;
}

/* Flèche */
.theme-arrow {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 36px;
  height: 36px;
  background: #f1f5f9;
  border-radius: 10px;
  margin: 0 auto;
  color: #64748b;
  transition: all 0.3s ease;
}

.theme-card-inner:hover .theme-arrow {
  background: var(--theme-color);
  color: white;
  transform: translateX(4px);
}

/* Effet de brillance */
.theme-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.4),
    transparent
  );
  transition: left 0.5s ease;
}

.theme-card-inner:hover .theme-shine {
  left: 100%;
}

/* Responsive */
@media (max-width: 768px) {
  .theme-card {
    max-width: 300px;
  }
  
  .theme-card-inner {
    padding: 1.25rem 1rem;
  }
  
  .theme-icon {
    width: 48px;
    height: 48px;
    margin-bottom: 1rem;
  }
  
  .theme-title {
    font-size: 1rem;
  }
  
  .theme-description {
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .theme-card {
    max-width: 280px;
  }
  
  .theme-card-inner {
    padding: 1rem 0.875rem;
  }
  
  .theme-icon {
    width: 44px;
    height: 44px;
  }
}
</style>
