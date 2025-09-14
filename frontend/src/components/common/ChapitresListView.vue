<template>
  <div class="chapitres-list-view">
    <!-- Bouton de retour -->
    <BackButton 
      :text="backButtonText" 
      :customAction="backAction"
      position="top-left"
    />
    
    <!-- Titre principal -->
    <h2 class="chapitres-title">{{ title }}</h2>
    
    <!-- Liste des chapitres -->
    <div class="chapitres-list">
      <SimpleChapitreBox
        v-for="chapitre in chapitres"
        :key="chapitre.id"
        :title="chapitre.nom"
        :description="chapitre.description"
        @click="onChapitreClick(chapitre.id)"
      />
    </div>
    
    <!-- Message si aucun chapitre -->
    <div v-if="chapitres.length === 0" class="chapitres-empty">
      <div class="empty-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M14 2V8H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <h3>Aucun chapitre disponible</h3>
      <p>Il n'y a pas encore de chapitres pour cette notion.</p>
    </div>
  </div>
</template>

<script setup>
import SimpleChapitreBox from '@/components/UI/SimpleChapitreBox.vue'
import BackButton from '@/components/common/BackButton.vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  chapitres: {
    type: Array,
    default: () => []
  },
  backButtonText: {
    type: String,
    default: 'Retour'
  },
  backAction: {
    type: Function,
    required: true
  },
  onChapitreClick: {
    type: Function,
    required: true
  }
})
</script>

<style scoped>
.chapitres-list-view {
  background: #fff;
  padding: 0 5vw 40px 5vw;
  text-align: left;
  position: relative;
}

.chapitres-title {
  font-size: 2rem;
  color: #193e8e;
  margin-bottom: 40px;
  font-weight: 800;
}

.chapitres-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 700px;
  margin: 0 auto;
  align-items: stretch;
}

/* État vide */
.chapitres-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  color: #6b7280;
  text-align: center;
}

.empty-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 64px;
  height: 64px;
  background: #f9fafb;
  border-radius: 16px;
  color: #9ca3af;
  margin-bottom: 1rem;
}

.chapitres-empty h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.chapitres-empty p {
  font-size: 1rem;
  color: #64748b;
  margin: 0;
}

/* Responsive */
@media (max-width: 640px) {
  .chapitres-title {
    font-size: 1.5rem;
    margin-bottom: 30px;
  }
  
  .chapitres-list {
    gap: 1rem;
  }
  
  .chapitres-list-view {
    padding: 0 4vw 30px 4vw;
  }
}
</style>
