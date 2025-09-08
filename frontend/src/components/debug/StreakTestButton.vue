<template>
  <div class="streak-test-container">
    <div class="test-header">
      <h3>🧪 Test Badges & Streak</h3>
      <p class="test-subtitle">Interface de test pour administrateur</p>
    </div>
    
    <!-- État actuel simplifié -->
    <div class="status-grid">
      <div class="status-card">
        <span class="status-icon">🔥</span>
        <div class="status-content">
          <span class="status-label">Streak</span>
          <span class="status-value">{{ currentStreak }} jours</span>
        </div>
      </div>
      
      <div class="status-card">
        <span class="status-icon">⭐</span>
        <div class="status-content">
          <span class="status-label">XP</span>
          <span class="status-value">{{ userStore.xp || 0 }}</span>
        </div>
      </div>
      
      <div class="status-card">
        <span class="status-icon">🏆</span>
        <div class="status-content">
          <span class="status-label">Niveau</span>
          <span class="status-value">{{ userStore.level || 0 }}</span>
        </div>
      </div>
      
      <div class="status-card">
        <span class="status-icon">📅</span>
        <div class="status-content">
          <span class="status-label">Vérifié</span>
          <span class="status-value" :class="{ 'checked': isStreakCheckedToday }">
            {{ isStreakCheckedToday ? 'Oui' : 'Non' }}
          </span>
        </div>
      </div>
    </div>

    <!-- Simulation de jours -->
    <div class="simulation-section">
      <h4>🎭 Simulation de Jours</h4>
      <p class="simulation-info">Simulez différents jours pour tester le streak</p>
      
      <div class="simulation-buttons">
        <button @click="simulateDay(1)" class="sim-btn day-1">
          📅 Jour 1
        </button>
        <button @click="simulateDay(2)" class="sim-btn day-2">
          📅 Jour 2
        </button>
        <button @click="simulateDay(3)" class="sim-btn day-3">
          📅 Jour 3
        </button>
        <button @click="simulateDay(4)" class="sim-btn day-4">
          📅 Jour 4
        </button>
        <button @click="simulateDay(5)" class="sim-btn day-5">
          📅 Jour 5
        </button>
        <button @click="simulateDay(7)" class="sim-btn day-7">
          📅 Jour 7
        </button>
        <button @click="simulateDay(10)" class="sim-btn day-10">
          📅 Jour 10
    </button>
        </div>

      <div class="simulation-controls">
        <button @click="simulateStreakBreak" class="sim-btn break">
          💔 Casser le Streak
        </button>
        <button @click="resetSimulation" class="sim-btn reset">
          🔄 Reset Simulation
        </button>
      </div>
          </div>
          
    <!-- Boutons de test simplifiés -->
    <div class="test-actions">
      <button @click="testStreakCheck" class="test-btn primary">
        🔄 Vérifier Streak
      </button>
      
      <button @click="testXPUpdate" class="test-btn success">
        ➕ +5 XP
      </button>
      
      <button @click="testXPDecrease" class="test-btn danger">
        ➖ -5 XP
      </button>
      
      <button @click="resetStreak" class="test-btn warning">
        🗑️ Reset
            </button>
      
      <button @click="refreshData" class="test-btn info">
        🔄 Refresh
            </button>
          </div>

    <!-- Résultats des tests -->
    <div class="test-results" v-if="testResults.length > 0">
      <div class="results-header">
        <h4>📊 Résultats des tests</h4>
        <button @click="clearResults" class="clear-btn">🗑️</button>
      </div>
      <div class="results-list">
        <div v-for="(result, index) in testResults" :key="index" class="result-item" :class="result.type">
          <span class="result-time">{{ result.timestamp }}</span>
          <span class="result-message">{{ result.message }}</span>
          </div>
        </div>
      </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStreak } from '@/composables/useStreak'
import { useXP } from '@/composables/useXP'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const { 
  currentStreak,
  isStreakCheckedToday,
  checkDailyStreak,
  resetStreak: resetStreakData,
  initializeStreak 
} = useStreak()

const { updateUserXPInstantly } = useXP()

const testResults = ref([])

const addTestResult = (message, type = 'info') => {
  const timestamp = new Date().toLocaleTimeString()
  testResults.value.unshift({ timestamp, message, type })
  
  // Garder seulement les 8 derniers résultats
  if (testResults.value.length > 8) {
    testResults.value = testResults.value.slice(0, 8)
  }
}

// Simulation de jours - LOGIQUE CORRIGÉE
const simulateDay = (dayNumber) => {
  try {
    addTestResult(`🎭 Simulation du jour ${dayNumber}...`, 'info')
    
    // Pour simuler un streak de X jours, on doit créer une séquence de connexions
    // qui donne l'impression d'un streak de X jours consécutifs
    
    const today = new Date()
    const yesterday = new Date(today)
    yesterday.setDate(today.getDate() - 1)
    
    // Si on veut simuler un streak de X jours, la dernière connexion doit être hier
    // et le streak doit être X-1 (car aujourd'hui on va le vérifier)
    const lastLoginDate = yesterday.toISOString().split('T')[0]
    const currentStreakValue = dayNumber - 1
    
    // Mettre à jour le localStorage directement
    localStorage.setItem('lastLoginDate', lastLoginDate)
    localStorage.setItem('currentStreak', currentStreakValue.toString())
    localStorage.removeItem('streakCheckedToday')
    
    // Forcer la mise à jour des refs locales
    currentStreak.value = currentStreakValue
    isStreakCheckedToday.value = false
    
    addTestResult(`✅ Streak de ${dayNumber} jours simulé (dernière connexion: ${lastLoginDate})`, 'success')
    
    // Maintenant quand on vérifie le streak, il devrait incrémenter de 1
    setTimeout(() => {
      testStreakCheck()
    }, 500)
    
  } catch (error) {
    addTestResult(`❌ Erreur simulation jour ${dayNumber}: ${error.message}`, 'error')
  }
}

// Simuler une rupture de streak
const simulateStreakBreak = () => {
  try {
    addTestResult('💔 Simulation rupture de streak...', 'warning')
    
    // Simuler une connexion il y a 3 jours (streak cassé)
    const today = new Date()
    const breakDate = new Date(today)
    breakDate.setDate(today.getDate() - 3)
    
    const dateString = breakDate.toISOString().split('T')[0]
    
    // Remettre le streak à 0 car il est cassé
    localStorage.setItem('lastLoginDate', dateString)
    localStorage.setItem('currentStreak', '0')
    localStorage.removeItem('streakCheckedToday')
    
    // Forcer la mise à jour des refs locales
    currentStreak.value = 0
    isStreakCheckedToday.value = false
    
    addTestResult('✅ Rupture de streak simulée (3 jours d\'écart)', 'warning')
    
    setTimeout(() => {
      testStreakCheck()
    }, 500)
    
  } catch (error) {
    addTestResult(`❌ Erreur simulation rupture: ${error.message}`, 'error')
  }
}

// Reset de la simulation
const resetSimulation = () => {
  try {
    addTestResult('🔄 Reset de la simulation...', 'info')
    
    // Remettre la date d'aujourd'hui et streak à 0
    const today = new Date().toISOString().split('T')[0]
    localStorage.setItem('lastLoginDate', today)
    localStorage.setItem('currentStreak', '0')
    localStorage.removeItem('streakCheckedToday')
    
    // Forcer la mise à jour des refs locales
    currentStreak.value = 0
    isStreakCheckedToday.value = false
    
    addTestResult('✅ Simulation remise à aujourd\'hui (streak: 0)', 'success')
    
  } catch (error) {
    addTestResult(`❌ Erreur reset simulation: ${error.message}`, 'error')
  }
}

const testStreakCheck = async () => {
  try {
    addTestResult('🔄 Vérification du streak...', 'info')
    
    const result = await checkDailyStreak()
    
    if (result.success) {
      if (result.alreadyChecked) {
        addTestResult('✅ Streak déjà vérifié aujourd\'hui', 'success')
      } else {
        addTestResult(`🎉 Streak: ${result.streakDays} jours, +${result.xpGained} XP`, 'success')
      }
    } else {
      addTestResult(`❌ Erreur: ${result.reason || 'inconnue'}`, 'error')
    }
  } catch (error) {
    addTestResult(`❌ Erreur: ${error.message}`, 'error')
  }
}

const testXPUpdate = async () => {
  try {
    addTestResult('➕ Test +5 XP...', 'info')
    
    const oldXP = userStore.xp || 0
    const result = await updateUserXPInstantly(5, 'test_manual')
    
    if (result.success) {
      const newXP = userStore.xp || 0
      addTestResult(`✅ XP: ${oldXP} → ${newXP} (+5)`, 'success')
    } else {
      addTestResult('❌ Échec mise à jour XP', 'error')
    }
  } catch (error) {
    addTestResult(`❌ Erreur: ${error.message}`, 'error')
  }
}

const testXPDecrease = async () => {
  try {
    addTestResult('➖ Test -5 XP...', 'info')
    
    const oldXP = userStore.xp || 0
    const result = await updateUserXPInstantly(-5, 'test_manual_decrease')
    
    if (result.success) {
      const newXP = userStore.xp || 0
      addTestResult(`✅ XP: ${oldXP} → ${newXP} (-5)`, 'success')
    } else {
      addTestResult('❌ Échec diminution XP', 'error')
    }
  } catch (error) {
    addTestResult(`❌ Erreur: ${error.message}`, 'error')
  }
}

const resetStreak = () => {
  try {
    resetStreakData()
    addTestResult('🗑️ Streak remis à zéro', 'warning')
  } catch (error) {
    addTestResult(`❌ Erreur reset: ${error.message}`, 'error')
  }
}

const refreshData = async () => {
  try {
    addTestResult('🔄 Rafraîchissement...', 'info')
    initializeStreak()
    addTestResult('✅ Données rafraîchies', 'success')
  } catch (error) {
    addTestResult(`❌ Erreur: ${error.message}`, 'error')
  }
}

const clearResults = () => {
  testResults.value = []
}

onMounted(() => {
  addTestResult('🚀 Test Badges & Streak chargé', 'info')
})
</script>

<style scoped>
.streak-test-container {
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 1.5rem;
  margin: 1rem 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.test-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.test-header h3 {
  margin: 0 0 0.5rem 0;
  color: #1e293b;
  font-size: 1.25rem;
  font-weight: 700;
}

.test-subtitle {
  margin: 0;
  color: #64748b;
  font-size: 0.9rem;
}

/* Grille de statuts */
.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.status-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: all 0.3s ease;
}

.status-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.status-icon {
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  border-radius: 10px;
}

.status-content {
  flex: 1;
}

.status-label {
  display: block;
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-value {
  display: block;
  font-size: 1.1rem;
  color: #1e293b;
  font-weight: 700;
}

.status-value.checked {
  color: #059669;
}

/* Section Simulation */
.simulation-section {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.simulation-section h4 {
  margin: 0 0 0.5rem 0;
  color: #1e293b;
  font-size: 1.1rem;
  font-weight: 600;
}

.simulation-info {
  margin: 0 0 1rem 0;
  color: #64748b;
  font-size: 0.9rem;
}

.simulation-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.simulation-controls {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
}

.sim-btn {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.85rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  min-width: 100px;
}

.sim-btn.day-1 { background: #dbeafe; color: #1e40af; border: 1px solid #93c5fd; }
.sim-btn.day-2 { background: #d1fae5; color: #065f46; border: 1px solid #6ee7b7; }
.sim-btn.day-3 { background: #fef3c7; color: #92400e; border: 1px solid #fcd34d; }
.sim-btn.day-4 { background: #fce7f3; color: #be185d; border: 1px solid #f9a8d4; }
.sim-btn.day-5 { background: #e0e7ff; color: #3730a3; border: 1px solid #a5b4fc; }
.sim-btn.day-7 { background: #fef2f2; color: #991b1b; border: 1px solid #fca5a5; }
.sim-btn.day-10 { background: #f0fdf4; color: #14532d; border: 1px solid #86efac; }

.sim-btn.break { background: #fee2e2; color: #dc2626; border: 1px solid #fca5a5; }
.sim-btn.reset { background: #f3f4f6; color: #374151; border: 1px solid #d1d5db; }

.sim-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.sim-btn:active {
  transform: translateY(0);
}

/* Boutons de test */
.test-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.test-btn {
  padding: 0.75rem 1.25rem;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 120px;
  justify-content: center;
}

.test-btn.primary {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.test-btn.success {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.test-btn.warning {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
}

.test-btn.info {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
  color: white;
  box-shadow: 0 2px 8px rgba(6, 182, 212, 0.3);
}

.test-btn.danger {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
}

.test-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.test-btn:active {
  transform: translateY(0);
}

/* Résultats des tests */
.test-results {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
}

.results-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.results-header h4 {
  margin: 0;
  color: #1e293b;
  font-size: 1rem;
  font-weight: 600;
}

.clear-btn {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s;
}

.clear-btn:hover {
  background: #e2e8f0;
  color: #475569;
}

.results-list {
  max-height: 200px;
  overflow-y: auto;
}

.result-item {
  display: flex;
  padding: 0.75rem 1.5rem;
  border-bottom: 1px solid #f1f5f9;
  align-items: center;
  gap: 0.75rem;
}

.result-item:last-child {
  border-bottom: none;
}

.result-item.success {
  background: #f0fdf4;
  border-left: 4px solid #10b981;
}

.result-item.error {
  background: #fef2f2;
  border-left: 4px solid #ef4444;
}

.result-item.warning {
  background: #fffbeb;
  border-left: 4px solid #f59e0b;
}

.result-item.info {
  background: #f0f9ff;
  border-left: 4px solid #0ea5e9;
}

.result-time {
  color: #64748b;
  font-size: 0.8rem;
  font-weight: 500;
  min-width: 70px;
}

.result-message {
  flex: 1;
  font-size: 0.9rem;
  font-weight: 500;
}

/* Responsive */
@media (max-width: 640px) {
  .streak-test-container {
    padding: 1rem;
  }
  
  .status-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }
  
  .simulation-buttons {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .simulation-controls {
    flex-direction: column;
    align-items: center;
  }
  
  .test-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .test-btn {
    width: 100%;
    max-width: 200px;
  }
}
</style>
