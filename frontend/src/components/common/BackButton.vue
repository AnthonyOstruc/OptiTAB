<template>
  <button 
    :class="['back-button', { 
      'back-button--top-left': position === 'top-left',
      'back-button--top-left-dashboard': position === 'top-left-dashboard',
      'back-button--main-notions': position === 'main-notions',
      'back-button--sticky': position === 'sticky'
    }]" 
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
    default: 'normal', // 'normal', 'top-left', 'top-left-dashboard', 'main-notions', ou 'sticky'
    validator: (value) => ['normal', 'top-left', 'top-left-dashboard', 'main-notions', 'sticky'].includes(value)
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
}

.back-button--top-left {
  position: fixed;
  top: calc(var(--header-height, 60px));
  left: env(safe-area-inset-left, 0px);
  z-index: 9000; /* sous les modales */
  margin: 0;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.back-button--top-left-dashboard {
  position: fixed;
  top: 1px;
  left: 1px;
  z-index: 9000; /* sous les modales */
  margin: 0;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Position dédiée aux 4 pages principales: Quiz, Exercices, Cours, Fiches */
.back-button--main-notions {
  position: fixed;
  top: 1px;
  left: 1px;
  z-index: 9000;
  margin: 0;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.back-button--sticky {
  position: sticky;
  top: 20px;
  z-index: 9000; /* sous les modales */
  margin: 0;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
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

@media (max-width: 768px) {
  .back-button--top-left {
    /* En mobile, le header fait 56px + marge pour éviter le clash */
    top: 25px;
    left: 1px;
  }
  
  .back-button--top-left-dashboard {
    /* Autres pages non principales */
    top: 25px;
    left: 1px;
  }
  
  /* Position dédiée aux 4 pages principales en mobile */
  .back-button--main-notions {
    top: 30px;
    left: 1px;
  }
  
  .back-button--sticky {
    top: 10px;
  }
  
  .back-text {
    display: none;
  }
}

@media (max-width: 480px) {
  .back-button--top-left-dashboard {
    /* Autres pages non principales */
    top: 21px;
    left: 1px;
  }
  
  /* Position dédiée aux 4 pages principales en mobile petit écran */
  .back-button--main-notions {
    top: 30px;
    left: 1px;
  }
  
  .back-button--sticky {
    top: 5px;
  }
}
</style> 
