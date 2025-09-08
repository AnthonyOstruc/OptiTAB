<template>
  <div class="simple-chapitre-box" @click="$emit('click')" tabindex="0">
    <div class="chapitre-content">
      <!-- Icône -->
      <div class="chapitre-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M14 2V8H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      
      <!-- Texte -->
      <div class="chapitre-text">
        <h3 class="chapitre-title">{{ title }}</h3>
        <p class="chapitre-description">{{ description || 'Cliquez pour accéder aux exercices' }}</p>
      </div>

      <!-- Flèche -->
      <div class="chapitre-arrow">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup>

const props = defineProps({
  title: { type: String, required: true },
  description: { type: String, default: '' }
})

defineEmits(['click'])

</script>

<style scoped>
.simple-chapitre-box {
  width: 100%;
  max-width: 700px;
  margin: 0 auto;
  cursor: pointer;
  transition: all 0.2s ease;
}

.chapitre-content {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.simple-chapitre-box:hover .chapitre-content {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
  transform: translateY(-1px);
}

.simple-chapitre-box:active .chapitre-content {
  transform: translateY(0);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Icône */
.chapitre-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 48px;
  height: 48px;
  background: #10b981;
  border-radius: 8px;
  color: white;
  flex-shrink: 0;
}

/* Texte */
.chapitre-text {
  flex: 1;
  min-width: 0;
}

.chapitre-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.25rem 0;
  line-height: 1.4;
}

.chapitre-description {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.4;
}

/* Tags */
.chapitre-tags {
  display: none;
}

.tag {
  display: none;
}

/* Flèche */
.chapitre-arrow {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 32px;
  height: 32px;
  color: #9ca3af;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.simple-chapitre-box:hover .chapitre-arrow {
  color: #3b82f6;
  transform: translateX(2px);
}


/* Responsive */
@media (max-width: 768px) {
  .chapitre-content {
    padding: 1.25rem;
    gap: 0.75rem;
  }

  .chapitre-icon {
    width: 40px;
    height: 40px;
  }

  .chapitre-title {
    font-size: 1rem;
  }

  .chapitre-description {
    font-size: 0.8rem;
  }

  .chapitre-tags {
    display: none;
  }

  .tag {
    display: none;
  }

}

@media (max-width: 480px) {
  .chapitre-content {
    padding: 1rem;
    flex-wrap: wrap;
  }
  
  .chapitre-text {
    flex-basis: 100%;
    order: 2;
  }
  
  .chapitre-icon {
    order: 1;
  }
  
  .chapitre-arrow {
    order: 3;
  }
}
</style>
