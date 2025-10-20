<template>
  <button 
    :class="['back-button', { 'back-button--top-left': position === 'top-left' }]" 
    @click="goBack"
    :title="title || 'Retour'"
    aria-label="Retour en arrière"
  >
    <svg 
      class="back-icon" 
      width="20" 
      height="20" 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke="currentColor" 
      stroke-width="2" 
      stroke-linecap="round" 
      stroke-linejoin="round"
    >
      <path d="M19 12H5M12 19l-7-7 7-7"/>
    </svg>
    <span v-if="showText" class="back-text">{{ text || 'Retour' }}</span>
  </button>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  text: {
    type: String,
    default: 'Retour'
  },
  title: {
    type: String,
    default: 'Retour en arrière'
  },
  showText: {
    type: Boolean,
    default: true
  },
  customAction: {
    type: Function,
    default: null
  },
  position: {
    type: String,
    default: 'normal', // 'normal' ou 'top-left'
    validator: (value) => ['normal', 'top-left'].includes(value)
  }
})

const router = useRouter()

const goBack = () => {
  if (props.customAction) {
    props.customAction()
  } else {
    router.back()
  }
}
</script>

<style scoped>
.back-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  color: #6b7280;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  margin-bottom: 1rem;
  /* Monter le bouton de retour */
  margin-top: -0.5rem;
  /* Déplacer le bouton vers la gauche */
  margin-left: -0.5rem;
}

.back-button--top-left {
  position: fixed;
  top: 0.5rem;
  left: 0.5rem;
  z-index: 1000;
  margin-bottom: 0;
}

.back-button:hover {
  background: #f9fafb;
  border-color: #d1d5db;
  color: #374151;
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.back-button:active {
  transform: translateY(0);
}

.back-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.back-text {
  white-space: nowrap;
}

/* Version mobile - bouton plus visible */
@media (max-width: 768px) {
  .back-button {
    padding: 0.5rem 0.75rem;
    font-size: 0.9rem;
    /* Monter encore plus sur mobile */
    margin-top: -0.75rem;
    /* Déplacer encore plus vers la gauche sur mobile */
    margin-left: -0.75rem;
    /* Améliorer la visibilité sur mobile */
    background: #ffffff;
    border: 2px solid #3b82f6;
    box-shadow: 0 3px 8px rgba(59, 130, 246, 0.2);
    color: #3b82f6;
    font-weight: 600;
  }
  
  .back-icon {
    width: 18px;
    height: 18px;
  }
  
  .back-text {
    display: none;
  }
  
  .back-button--top-left {
    top: 0.25rem;
    left: 0.25rem;
    /* Améliorer la visibilité en position fixe */
    background: #ffffff;
    border: 2px solid #3b82f6;
    box-shadow: 0 3px 8px rgba(59, 130, 246, 0.2);
    color: #3b82f6;
  }
}

/* Version très petit écran - encore plus visible */
@media (max-width: 480px) {
  .back-button {
    /* Monter encore plus sur très petit écran */
    margin-top: -1rem;
    /* Déplacer encore plus vers la gauche sur très petit écran */
    margin-left: -1rem;
    /* Améliorer encore plus la visibilité sur très petit écran */
    padding: 0.6rem 0.8rem;
    font-size: 1rem;
    background: #ffffff;
    border: 3px solid #3b82f6;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    color: #3b82f6;
    font-weight: 700;
  }
  
  .back-icon {
    width: 20px;
    height: 20px;
  }
  
  .back-button--top-left {
    top: 0.125rem;
    left: 0.125rem;
    /* Améliorer encore plus la visibilité en position fixe */
    background: #ffffff;
    border: 3px solid #3b82f6;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    color: #3b82f6;
    padding: 0.6rem 0.8rem;
  }
}

/* Version ultra-petit écran - visibilité maximale */
@media (max-width: 360px) {
  .back-button {
    /* Visibilité maximale sur ultra-petit écran */
    padding: 0.7rem 1rem;
    font-size: 1.1rem;
    background: #ffffff;
    border: 3px solid #3b82f6;
    box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
    color: #3b82f6;
    font-weight: 700;
    /* Position optimisée */
    margin-top: -0.5rem;
    margin-left: -0.5rem;
  }
  
  .back-icon {
    width: 22px;
    height: 22px;
  }
  
  .back-button--top-left {
    top: 0.25rem;
    left: 0.25rem;
    /* Visibilité maximale en position fixe */
    background: #ffffff;
    border: 3px solid #3b82f6;
    box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
    color: #3b82f6;
    padding: 0.7rem 1rem;
  }
}
</style> 