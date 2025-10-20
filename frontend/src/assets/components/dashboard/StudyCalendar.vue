<template>
  <div class="study-calendar-card">
    <div class="calendar-header">
      <div class="header-info">
        <h3 class="calendar-title">📅 Planning d'Étude</h3>
        <div class="nav-controls">
          <button class="nav-btn" @click="previousMonth" :disabled="isPreviousDisabled">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
              <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/>
            </svg>
          </button>
          <span class="current-month">{{ currentMonthYear }}</span>
          <button class="nav-btn" @click="nextMonth">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
              <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <div class="calendar-grid">
      <!-- En-têtes des jours -->
      <div class="day-header" v-for="day in dayHeaders" :key="day">{{ day }}</div>
      
      <!-- Jours vides au début -->
      <div v-for="n in startPadding" :key="'empty-' + n" class="day-cell empty"></div>
      
             <!-- Jours du mois -->
       <div 
         v-for="day in daysInMonth" 
         :key="day"
         class="day-cell"
         :class="getDayClass(day)"
         @click="selectDay(day)"
       >
         <span class="day-number">{{ day }}</span>
         <div v-if="hasStudySession(day)" class="study-dot" :class="getStudyType(day)"></div>
         <div v-if="hasActivity(day)" class="activity-dot">•</div>
       </div>
    </div>

    <!-- Panneau de planification -->
    <div v-if="selectedDay" class="planning-panel">
      <div class="panel-header">
        <h4>{{ selectedDayFormatted }}</h4>
        <button class="close-btn" @click="selectedDay = null">×</button>
      </div>
      
      <div class="study-sessions">
        <div class="session-item" v-for="session in getSessionsForDay(selectedDay)" :key="session.id">
          <div class="session-time">{{ session.time }}</div>
          <div class="session-content">
            <div class="session-title">{{ session.title }}</div>
            <div class="session-subject">{{ session.subject }}</div>
          </div>
          <button class="remove-session" @click="removeSession(session.id)">×</button>
        </div>
        
        <button class="add-session-btn" @click="showAddSession = true">
          + Ajouter une session
        </button>
      </div>
    </div>

    <!-- Modal d'ajout de session -->
    <div v-if="showAddSession" class="modal-overlay" @click="closeAddSession">
      <div class="modal-content" @click.stop>
        <h4>Nouvelle session d'étude</h4>
        <form @submit.prevent="addStudySession">
          <div class="form-group">
            <label>Heure</label>
            <input type="time" v-model="newSession.time" required>
          </div>
          <div class="form-group">
            <label>Titre</label>
            <input type="text" v-model="newSession.title" placeholder="Ex: Révision chapitre 3" required>
          </div>
          <div class="form-group">
            <label>Matière</label>
            <select v-model="newSession.subject" required>
              <option value="">Choisir une matière</option>
              <option value="Mathématiques">Mathématiques</option>
              <option value="Physique">Physique</option>
              <option value="Chimie">Chimie</option>
              <option value="Français">Français</option>
              <option value="Anglais">Anglais</option>
            </select>
          </div>
          <div class="form-group">
            <label>Type</label>
            <select v-model="newSession.type">
              <option value="study">Étude</option>
              <option value="quiz">Quiz</option>
              <option value="review">Révision</option>
            </select>
          </div>
          <div class="form-actions">
            <button type="button" @click="closeAddSession" class="cancel-btn">Annuler</button>
            <button type="submit" class="save-btn">Sauvegarder</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  statuses: { type: Array, default: () => [] }
})

// État du calendrier
const currentDate = ref(new Date())
const selectedDay = ref(null)
const showAddSession = ref(false)
const studySessions = ref([])

// Nouvelle session
const newSession = ref({
  time: '',
  title: '',
  subject: '',
  type: 'study'
})

const dayHeaders = ['L', 'M', 'M', 'J', 'V', 'S', 'D']

// Computed properties
const currentMonth = computed(() => currentDate.value.getMonth())
const currentYear = computed(() => currentDate.value.getFullYear())
const today = computed(() => new Date())

const currentMonthYear = computed(() => {
  const months = [
    'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
    'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
  ]
  return `${months[currentMonth.value]} ${currentYear.value}`
})

const daysInMonth = computed(() => {
  return new Date(currentYear.value, currentMonth.value + 1, 0).getDate()
})

const startPadding = computed(() => {
  const firstDay = new Date(currentYear.value, currentMonth.value, 1).getDay()
  return firstDay === 0 ? 6 : firstDay - 1
})

const isPreviousDisabled = computed(() => {
  const currentMonthStart = new Date(currentYear.value, currentMonth.value, 1)
  const todayMonthStart = new Date(today.value.getFullYear(), today.value.getMonth(), 1)
  return currentMonthStart <= todayMonthStart
})

const selectedDayFormatted = computed(() => {
  if (!selectedDay.value) return ''
  const date = new Date(currentYear.value, currentMonth.value, selectedDay.value)
  return date.toLocaleDateString('fr-FR', { 
    weekday: 'long', 
    day: 'numeric', 
    month: 'long' 
  })
})

// Dates d'activité basées sur les statuses
const activityDates = computed(() => {
  const dates = new Set()
  props.statuses.forEach(status => {
    if (status.date_creation) {
      const date = new Date(status.date_creation)
      if (date.getMonth() === currentMonth.value && date.getFullYear() === currentYear.value) {
        dates.add(date.getDate())
      }
    }
  })
  return dates
})

// Méthodes
const getDayClass = (day) => {
  const date = new Date(currentYear.value, currentMonth.value, day)
  const isToday = date.toDateString() === today.value.toDateString()
  const isPast = date < today.value && !isToday
  const isSelected = selectedDay.value === day
  const hasActivity = activityDates.value.has(day)
  
  return {
    'today': isToday,
    'past': isPast,
    'selected': isSelected,
    'has-activity': hasActivity,
    'has-study': hasStudySession(day)
  }
}

const hasActivity = (day) => {
  return activityDates.value.has(day)
}

const hasStudySession = (day) => {
  const dateKey = `${currentYear.value}-${currentMonth.value}-${day}`
  return studySessions.value.some(session => session.date === dateKey)
}

const getStudyType = (day) => {
  const dateKey = `${currentYear.value}-${currentMonth.value}-${day}`
  const session = studySessions.value.find(s => s.date === dateKey)
  return session ? session.type : 'study'
}

const getSessionsForDay = (day) => {
  const dateKey = `${currentYear.value}-${currentMonth.value}-${day}`
  return studySessions.value.filter(session => session.date === dateKey)
}

const selectDay = (day) => {
  const date = new Date(currentYear.value, currentMonth.value, day)
  if (date >= today.value || date.toDateString() === today.value.toDateString()) {
    selectedDay.value = day
  }
}

const previousMonth = () => {
  if (!isPreviousDisabled.value) {
    currentDate.value = new Date(currentYear.value, currentMonth.value - 1)
  }
}

const nextMonth = () => {
  currentDate.value = new Date(currentYear.value, currentMonth.value + 1)
}

const addStudySession = () => {
  const dateKey = `${currentYear.value}-${currentMonth.value}-${selectedDay.value}`
  const session = {
    id: Date.now(),
    date: dateKey,
    ...newSession.value
  }
  
  studySessions.value.push(session)
  saveToLocalStorage()
  
  // Reset form
  newSession.value = { time: '', title: '', subject: '', type: 'study' }
  showAddSession.value = false
}

const removeSession = (sessionId) => {
  studySessions.value = studySessions.value.filter(s => s.id !== sessionId)
  saveToLocalStorage()
}

const closeAddSession = () => {
  showAddSession.value = false
  newSession.value = { time: '', title: '', subject: '', type: 'study' }
}

const saveToLocalStorage = () => {
  localStorage.setItem('studySessions', JSON.stringify(studySessions.value))
}

const loadFromLocalStorage = () => {
  const saved = localStorage.getItem('studySessions')
  if (saved) {
    studySessions.value = JSON.parse(saved)
  }
}

onMounted(() => {
  loadFromLocalStorage()
})
</script>

<style scoped>
.study-calendar-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: 
    0 1px 3px 0 rgba(0, 0, 0, 0.1),
    0 1px 2px 0 rgba(0, 0, 0, 0.06);
  transition: all 0.2s ease;
}

.study-calendar-card:hover {
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transform: translateY(-1px);
}

.calendar-header {
  margin-bottom: 1rem;
}

.header-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.calendar-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.nav-btn {
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 0.5rem;
  cursor: pointer;
  color: #64748b;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.nav-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #e2e8f0, #cbd5e1);
  color: #374151;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-btn:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.current-month {
  font-weight: 500;
  color: #374151;
  font-size: 0.875rem;
  min-width: 100px;
  text-align: center;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
  background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
  border-radius: 12px;
  overflow: hidden;
  padding: 2px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.day-header {
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  padding: 0.75rem 0;
  text-align: center;
  font-weight: 600;
  font-size: 0.75rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-radius: 6px;
}

.day-cell {
  background: linear-gradient(135deg, #ffffff, #f8fafc);
  min-height: 42px;
  padding: 0.375rem;
  cursor: pointer;
  position: relative;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  border: 1px solid transparent;
}

.day-cell.empty {
  cursor: default;
  background: #f9fafb;
}

.day-cell:hover:not(.empty):not(.past) {
  background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-color: #cbd5e1;
}

.day-cell.today {
  background: linear-gradient(135deg, #dbeafe, #bfdbfe);
  color: #1e40af;
  font-weight: 700;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
  animation: pulse-today 2s infinite;
}

@keyframes pulse-today {
  0%, 100% { box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2); }
  50% { box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1); }
}

.day-cell.selected {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  font-weight: 700;
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
}

.day-cell.past {
  background: linear-gradient(135deg, #f9fafb, #f3f4f6);
  color: #9ca3af;
  cursor: default;
  opacity: 0.6;
}

.day-cell.has-activity {
  border-left: 3px solid #10b981;
  box-shadow: inset 3px 0 0 #10b981;
}

.day-cell.has-study {
  border-right: 3px solid #f59e0b;
  box-shadow: inset -3px 0 0 #f59e0b;
}

.day-cell.has-activity.has-study {
  box-shadow: inset 3px 0 0 #10b981, inset -3px 0 0 #f59e0b;
}

.day-number {
  font-weight: 500;
  font-size: 0.875rem;
  z-index: 1;
}

.study-dot {
  position: absolute;
  top: 3px;
  right: 3px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  border: 1px solid white;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.study-dot.study { 
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  animation: pulse-study 2s infinite;
}

.study-dot.quiz { 
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  animation: pulse-quiz 2s infinite;
}

.study-dot.review { 
  background: linear-gradient(135deg, #f59e0b, #d97706);
  animation: pulse-review 2s infinite;
}

@keyframes pulse-study {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}

@keyframes pulse-quiz {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}

@keyframes pulse-review {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}

.activity-dot {
  position: absolute;
  bottom: 3px;
  left: 3px;
  color: #10b981;
  font-size: 0.75rem;
  line-height: 1;
  font-weight: 700;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.planning-panel {
  margin-top: 1.25rem;
  padding: 1rem;
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from { 
    opacity: 0; 
    transform: translateY(-10px); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0); 
  }
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.panel-header h4 {
  margin: 0;
  color: #374151;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.session-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background: white;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  border: 1px solid #e5e7eb;
}

.session-time {
  font-weight: 600;
  color: #3b82f6;
  min-width: 60px;
}

.session-content {
  flex: 1;
}

.session-title {
  font-weight: 600;
  color: #374151;
}

.session-subject {
  font-size: 0.875rem;
  color: #6b7280;
}

.remove-session {
  background: none;
  border: none;
  color: #ef4444;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.remove-session:hover {
  background: #fee2e2;
}

.add-session-btn {
  width: 100%;
  padding: 0.875rem;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
  position: relative;
  overflow: hidden;
}

.add-session-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.add-session-btn:hover {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.4);
}

.add-session-btn:hover::before {
  left: 100%;
}

.add-session-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  margin: 1rem;
}

.modal-content h4 {
  margin: 0 0 1.5rem 0;
  color: #374151;
  font-weight: 600;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #374151;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 1rem;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.cancel-btn {
  padding: 0.75rem 1.5rem;
  background: #f3f4f6;
  color: #374151;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.save-btn {
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.cancel-btn:hover {
  background: #e5e7eb;
}

.save-btn:hover {
  background: #2563eb;
}

/* Responsive */
@media (max-width: 768px) {
  .study-calendar-card {
    padding: 0.75rem;
  }
  
  .header-info {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }
  
  .nav-controls {
    align-self: stretch;
    justify-content: center;
  }
  
  .day-cell {
    min-height: 36px;
  }
  
  .day-number {
    font-size: 0.8rem;
  }
  
  .modal-content {
    margin: 0.5rem;
    padding: 1.25rem;
  }
}
</style>
