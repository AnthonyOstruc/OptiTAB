<template>
  <div class="chapitre-box" @click="$emit('click')" tabindex="0">
    <div class="chapitre-box-inner">
      <!-- En-tête du chapitre -->
      <div class="chapitre-header">
        <div class="chapitre-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M14 2V8H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M16 13H8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M16 17H8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M10 9H9H8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div class="chapitre-info">
          <h3 class="chapitre-title">{{ title }}</h3>
          <p class="chapitre-subtitle">{{ subtitle || description || 'Cliquez pour accéder aux exercices' }}</p>
        </div>
      </div>
      
      <!-- Actions du chapitre -->
      <div class="chapitre-actions">
        <div class="chapitre-stats" v-if="difficulty || duration">
          <span class="stat-item" v-if="difficulty">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z" fill="currentColor"/>
            </svg>
            {{ difficulty }}
          </span>
          <span class="stat-item" v-if="duration">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              <polyline points="12,6 12,12 16,14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            {{ duration }}
          </span>
        </div>
        
        <div class="chapitre-arrow">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
      </div>
      
      <!-- Effet de brillance -->
      <div class="chapitre-shine"></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  difficulty: { type: String, default: '' },
  duration: { type: String, default: '' },
  description: { type: String, default: '' }
})
</script>

<style scoped>
.chapitre-box {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  perspective: 1000px;
}

.chapitre-box-inner {
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
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chapitre-box-inner:hover {
  transform: translateY(-4px) scale(1.01);
  border-color: #3b82f6;
  box-shadow: 
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04),
    0 0 0 4px rgba(59, 130, 246, 0.1);
}

.chapitre-box-inner:active {
  transform: translateY(-2px) scale(1.005);
}

.chapitre-box-inner:focus-within {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 
    0 0 0 3px rgba(59, 130, 246, 0.1),
    0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* En-tête */
.chapitre-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.chapitre-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 12px;
  color: white;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.chapitre-box-inner:hover .chapitre-icon {
  transform: scale(1.1) rotate(5deg);
  box-shadow: 0 8px 16px rgba(16, 185, 129, 0.3);
}

.chapitre-info {
  flex: 1;
  min-width: 0;
}

.chapitre-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
  line-height: 1.3;
  transition: color 0.3s ease;
}

.chapitre-box-inner:hover .chapitre-title {
  color: #1e40af;
}

.chapitre-subtitle {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
  line-height: 1.4;
  transition: color 0.3s ease;
}

.chapitre-box-inner:hover .chapitre-subtitle {
  color: #475569;
}

/* Actions */
.chapitre-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-shrink: 0;
}

.chapitre-stats {
  display: flex;
  gap: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  font-weight: 500;
  color: #64748b;
  background: #f1f5f9;
  padding: 0.375rem 0.75rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.chapitre-box-inner:hover .stat-item {
  background: #e0e7ff;
  color: #3b82f6;
}

.chapitre-arrow {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 40px;
  height: 40px;
  background: #f1f5f9;
  border-radius: 10px;
  color: #64748b;
  transition: all 0.3s ease;
}

.chapitre-box-inner:hover .chapitre-arrow {
  background: #3b82f6;
  color: white;
  transform: translateX(4px);
}

/* Effet de brillance */
.chapitre-shine {
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

.chapitre-box-inner:hover .chapitre-shine {
  left: 100%;
}

/* Responsive */
@media (max-width: 768px) {
  .chapitre-box-inner {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
    padding: 1.25rem;
  }
  
  .chapitre-header {
    width: 100%;
  }
  
  .chapitre-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .chapitre-stats {
    gap: 0.75rem;
  }
  
  .stat-item {
    font-size: 0.7rem;
    padding: 0.25rem 0.5rem;
  }
  
  .chapitre-title {
    font-size: 1.125rem;
  }
  
  .chapitre-subtitle {
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .chapitre-box-inner {
    padding: 1rem;
  }
  
  .chapitre-icon {
    width: 40px;
    height: 40px;
  }
  
  .chapitre-title {
    font-size: 1rem;
  }
  
  .chapitre-subtitle {
    font-size: 0.75rem;
  }
  
  .chapitre-stats {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .stat-item {
    font-size: 0.65rem;
    padding: 0.25rem 0.5rem;
  }
}
</style> 