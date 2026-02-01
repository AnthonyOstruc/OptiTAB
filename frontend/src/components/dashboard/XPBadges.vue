<template>
  <div class="xp-card">
    <!-- Header XP -->
    <div class="xp-header">
      <div class="xp-title">Progression XP</div>
      <div class="xp-level">Niveau {{ level }}</div>
    </div>
    
    <!-- Anneau de progression XP -->
    <div class="xp-ring">
      <svg viewBox="0 0 36 36" class="circular-chart">
        <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
        <path class="circle" :stroke-dasharray="dashArray" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
        <text x="18" y="20.35" class="percentage">{{ xp }} XP</text>
      </svg>
    </div>
    
    <!-- Prochain niveau -->
    <div class="xp-next">{{ xpToNext }} XP pour le prochain niveau</div>
    
    
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'
const userStore = useUserStore()

const level = computed(() => userStore.level || 0)
const xp = computed(() => userStore.xp || 0)
const xpToNext = computed(() => userStore.xp_to_next || 0)


 



const dashArray = computed(() => {
  const currentLevel = Number(level.value || 0)
  const totalXp = Number(xp.value || 0)

  // Seuils exponentiels: niveau n atteint à n^2 * 10 XP
  const currentLevelThreshold = currentLevel * currentLevel * 10
  const nextLevelThreshold = (currentLevel + 1) * (currentLevel + 1) * 10

  const clampedTotal = Math.max(totalXp, currentLevelThreshold)
  const currentInLevel = clampedTotal - currentLevelThreshold
  const span = Math.max(1, nextLevelThreshold - currentLevelThreshold)

  const pct = Math.min(100, Math.round((currentInLevel / span) * 100))
  return `${pct}, 100`
})


 

//
</script>

<style scoped>
.xp-card { 
  background: #fff; 
  border: 1px solid #e5e7eb; 
  border-radius: 16px; 
  padding: 1.5rem; 
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: none;
}

/* Désactive tout effet au survol pour éviter le "mouvement" ou l'ombre plus foncée */
.xp-card:hover { box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); }

.xp-header { 
  display: flex; 
  align-items: center; 
  justify-content: space-between; 
  margin-bottom: 1rem;
}

.xp-title { 
  font-weight: 800; 
  color: #1f2937; 
  font-size: 1.1rem;
}

.xp-level { 
  font-weight: 800; 
  color: #2563eb; 
  background: #eff6ff;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.9rem;
}

.xp-ring { 
  display: flex; 
  justify-content: center; 
  margin: 1rem 0;
}

.circular-chart {
  width: 140px;
  height: 140px;
  max-width: 140px;
  max-height: 140px;
  min-width: 140px;
  min-height: 140px;
  display: block;
}

.circle-bg { 
  fill: none; 
  stroke: #f3f4f6; 
  stroke-width: 3.8; 
}

.circle { 
  fill: none; 
  stroke-width: 2.8; 
  stroke-linecap: round; 
  stroke: #6366f1; 
  animation: progress 1s ease-out forwards;
  filter: drop-shadow(0 2px 4px rgba(99, 102, 241, 0.3));
}

.percentage { 
  fill: #334155; 
  font-family: sans-serif; 
  font-size: 0.35em; 
  text-anchor: middle; 
  font-weight: 800; 
}

@keyframes progress { 
  0% { stroke-dasharray: 0 100; } 
}

.xp-next { 
  text-align: center; 
  color: #64748b; 
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  font-weight: 500;
}

/* Section Streak Professionnelle */
.streak-section {
  border-top: 1px solid #f3f4f6;
  padding-top: 1.5rem;
}

.streak-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.streak-icon-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.streak-icon {
  font-size: 2rem;
  transition: all 0.3s ease;
  filter: grayscale(1);
}

.streak-icon.streak-active {
  filter: grayscale(0);
  animation: pulse 2s infinite;
}

.streak-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #ef4444;
  color: white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.streak-info {
  flex: 1;
  min-width: 0;
}

.streak-title {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  font-weight: 700;
  color: #1f2937;
}

.streak-subtitle {
  margin: 0;
  font-size: 0.85rem;
  color: #6b7280;
  line-height: 1.4;
}

.streak-next-xp {
  margin: 0.25rem 0 0 0;
  color: #059669;
  font-size: 0.8rem;
  font-weight: 600;
  opacity: 0.9;
}

.streak-xp-display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #fef3c7;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  border: 1px solid #fcd34d;
  flex-shrink: 0;
  transition: all 0.3s ease;
  cursor: default;
}

.streak-xp-display:hover {
  background: #fde68a;
  border-color: #f59e0b;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);
}

.xp-icon {
  font-size: 1.5rem;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
  transition: all 0.3s ease;
}

.xp-value {
  font-size: 0.9rem;
  font-weight: 600;
  color: #92400e;
  letter-spacing: 0.025em;
}

/* Barre de progression */
.streak-progress-container {
  margin-bottom: 1.25rem;
}

.streak-progress-bar {
  width: 100%;
  height: 8px;
  background: #f3f4f6;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
}

.streak-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #f59e0b, #d97706);
  border-radius: 4px;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 3px rgba(245, 158, 11, 0.3);
}

.streak-progress-text {
  font-size: 0.8rem;
  color: #6b7280;
  text-align: center;
  font-weight: 500;
}



/* Message de motivation */
.streak-motivation {
  text-align: center;
  padding: 1rem;
  background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
  border-radius: 12px;
  border: 1px solid #bae6fd;
}

.motivation-text {
  margin: 0;
  font-size: 0.9rem;
  color: #0369a1;
  font-weight: 500;
  line-height: 1.5;
}


/* Animations */
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

/* Responsive */
@media (max-width: 1200px) {
  /* Masque le sous-titre du streak (ex: "12 jours - Vous êtes régulier !") */
  .streak-subtitle {
    display: none;
  }
}

@media (max-width: 1100px) {
  /* Masque le bloc couronne +5 XP à droite */
  .streak-xp-display {
    display: none;
  }
}

@media (max-width: 640px) {
  .xp-card {
    padding: 1rem;
  }
  
  .streak-rewards {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .reward-item {
    flex-direction: row;
    justify-content: center;
    gap: 0.75rem;
  }
  

}
</style>

