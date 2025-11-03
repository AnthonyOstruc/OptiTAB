<template>
  <DashboardLayout>
    <section class="chapter-quiz-section">
      <!-- Bouton de retour -->
      <BackButton 
        :text="currentQuiz ? 'Retour aux quiz' : 'Retour aux chapitres'" 
        :customAction="currentQuiz ? backToList : goBackToNotions"
        position="top-left"
      />
      
      <!-- Navigation par onglets (déplacée au-dessus du titre) -->
      <div v-if="!currentQuiz && !showResults" class="clean-navigation">
        <div class="nav-grid">
          <button 
            v-for="t in tabs" 
            :key="t.key"
            :class="['nav-item', { active: t.key === activeTab }]"
            @click="activeTab = t.key"
          >
            <span class="nav-icon">{{ t.icon }}</span>
            <span class="nav-label">{{ t.shortLabel }}</span>
            <span class="nav-count">
              {{ t.count }}
            </span>
          </button>
        </div>
      </div>


      <div v-if="initialLoading" class="loading-skeleton-container">
        <SkeletonList :count="3" />
      </div>

      <div v-else-if="!currentQuiz && !showResults" class="quiz-list">
        <div 
          v-for="q in paginatedQuiz" 
          :key="q.id" 
          class="quiz-card"
          :class="{ 
            'completed': hasAttemptedQuiz(q.id),
            'saved-progress': savedQuizzes.value && savedQuizzes.value.has(q.id)
          }"
          @click="startQuiz(q)"
        >
          <div class="quiz-card-header">
            <div class="quiz-title-container">
              <span class="quiz-icon">🧩</span>
              <h3 class="quiz-card-title">{{ q.titre }}</h3>
            </div>
            <div
              class="quiz-difficulty-stars"
              :title="`Difficulté : ${getDifficultyLabel(q.difficulty)}`"
            >
              <span v-for="i in getDifficultyStars(q.difficulty)" :key="`filled-${i}`" class="star">★</span>
              <span v-for="i in (3 - getDifficultyStars(q.difficulty))" :key="`empty-${i}`" class="star empty">☆</span>
            </div>
          </div>
          <p class="quiz-card-description">{{ q.instruction }}</p>
          <div class="quiz-card-meta">
            <span class="quiz-questions">{{ q.questions?.length || 0 }} questions</span>
          </div>
          
          
          <!-- Affichage pour les quiz sauvegardés (à continuer) -->
          <div
            v-if="savedQuizzes.value && savedQuizzes.value.has(q.id)"
            class="quiz-status-container quiz-status-saved"
          >
            <!-- Progression à gauche -->
            <div class="quiz-progress-info">
              <span class="progress-icon">🔄</span>
              <span class="progress-text">
                {{ getSavedProgressInfo(q.id)?.progress || 1 }}/{{ getSavedProgressInfo(q.id)?.totalQuestions || q.questions?.length || 0 }}
                <span v-if="getSavedProgressInfo(q.id)?.isJustStarted" class="just-started-indicator">
                  (Débuté)
                </span>
                <span v-else-if="getSavedProgressInfo(q.id)?.isQuizCompleted" class="completed-indicator">
                  (Terminé - Voir résultats)
                </span>
                <span v-else-if="getSavedProgressInfo(q.id)?.questionLost" class="lost-question-indicator">
                  <span v-if="getSavedProgressInfo(q.id)?.isFirstQuestionLost" class="first-question-lost">
                    (Q1 perdue)
                  </span>
                  <span v-else>
                    (Q{{ getSavedProgressInfo(q.id)?.lostQuestion }} perdue)
                  </span>
                </span>
                <span v-else class="saved-question-indicator">
                  (Q{{ getSavedProgressInfo(q.id)?.lostQuestion }} sauvegardée)
                </span>
              </span>
            </div>
            
            <!-- Informations à droite -->
            <div class="quiz-right-info">
              <div class="quiz-saved-time">
                <span class="saved-label">Sauvegardé:</span>
                <span class="saved-time">{{ formatSavedTime(getSavedProgressInfo(q.id)?.lastSaved) }}</span>
              </div>
              <div class="quiz-continue-badge" :class="{ 'completed': getSavedProgressInfo(q.id)?.isQuizCompleted }">
                <span class="continue-text">{{ getSavedProgressInfo(q.id)?.isQuizCompleted ? 'Voir résultats' : 'Continuer' }}</span>
                <span class="continue-arrow">{{ getSavedProgressInfo(q.id)?.isQuizCompleted ? '📊' : '→' }}</span>
              </div>
            </div>
          </div>
          
          <!-- Affichage pour les quiz terminés -->
          <div
            v-else-if="hasAttemptedQuiz(q.id)"
            class="quiz-status-container quiz-status-completed"
          >
            <!-- Tentative et note à droite -->
            <div class="quiz-right-info">
              <div class="quiz-attempts">
                <span class="attempts-label">Tentative:</span>
                <span class="attempts-number">{{ getAttemptCount(q.id) }}</span>
              </div>
              <div class="quiz-score" :class="getScoreColorClass(getLastScore(q.id))">
                <span class="score-value">{{ getLastScore(q.id) }}/10</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Pagination -->
        <div v-if="filteredQuiz.length > itemsPerPage" class="pagination-container">
          <div class="pagination-info">
            Page {{ currentPage }} sur {{ totalPages }} ({{ filteredQuiz.length }} quiz au total)
          </div>
          <div class="pagination-controls">
            <button 
              @click="previousPage" 
              :disabled="currentPage === 1"
              class="pagination-btn"
            >
              ← Précédent
            </button>
            
            <div class="pagination-numbers">
              <button 
                v-for="page in totalPages" 
                :key="page"
                @click="changePage(page)"
                :class="['pagination-number', { active: page === currentPage }]"
              >
                {{ page }}
              </button>
            </div>
            
            <button 
              @click="nextPage" 
              :disabled="currentPage === totalPages"
              class="pagination-btn"
            >
              Suivant →
            </button>
          </div>
        </div>
        
        <!-- Message si aucun quiz dans la catégorie -->
        <div v-if="filteredQuiz.length === 0" class="no-quiz-message">
          <div class="no-quiz-icon">
            {{ activeTab === 'todo' ? '📚' : 
               activeTab === 'continue' ? '🔄' : 
               activeTab === 'below-average' ? '📈' : '🎯' }}
          </div>
          <h3>
            {{ activeTab === 'todo' ? 'Aucun quiz à faire' : 
               activeTab === 'continue' ? 'Aucun quiz en cours' : 
               activeTab === 'below-average' ? 'Aucun quiz à revoir' : 
               'Aucun quiz réussi' }}
          </h3>
          <p>
            {{ activeTab === 'todo' ? 'Tous les quiz de ce chapitre ont été commencés ou terminés.' : 
               activeTab === 'continue' ? 'Commencez un quiz pour pouvoir le reprendre plus tard.' : 
               activeTab === 'below-average' ? 'Bravo ! Aucun quiz n\'a une note inférieure à 5/10.' :
               'Terminez des quiz avec une note d\'au moins 5/10 pour qu\'ils apparaissent ici.' }}
          </p>
        </div>
      </div>

      <!-- Interface du Quiz -->
      <div v-if="currentQuiz && !showResults" class="quiz-interface">
        
        <div class="quiz-progress">
          <div class="progress-bar">
            <div 
              class="progress-fill" 
              :style="{ width: `${((currentQuestionIndex + 1) / currentQuiz.questions.length) * 100}%` }"
            ></div>
          </div>
          <span class="progress-text">{{ currentQuestionIndex + 1 }} / {{ currentQuiz.questions.length }}</span>
        </div>

        <!-- Timer par question -->
        <div class="question-timer">
          <div class="timer-info">
            <span class="timer-label">Temps par question :</span>
            <span class="timer-time" :class="{ 'warning': questionTimeLeft <= 5, 'critical': questionTimeLeft <= 2 }">
              {{ questionTimeLeft }}s
            </span>
          </div>
          <div class="timer-bar">
            <div 
              class="timer-fill-smooth" 
              :key="timerAnimationKey"
              :style="{ 
                animationDuration: timerAnimationDuration,
                backgroundColor: questionTimeLeft <= 5 ? (questionTimeLeft <= 2 ? '#ef4444' : '#f59e0b') : '#10b981',
                animationPlayState: isTimerActive ? 'running' : 'paused'
              }"
            ></div>
          </div>
          <div class="timer-difficulty">
            <span class="difficulty-badge" :class="normalizedDifficulty">
              {{ getDifficultyLabel(normalizedDifficulty) }} - {{ timePerQuestionSeconds }}s
            </span>
          </div>
        </div>

        <div class="question-container">
          <h3 class="question-title" v-html="currentQuestion.question"></h3>
          
          <div class="options-container">
            <div 
              v-for="(option, index) in currentQuestion.options" 
              :key="index"
              class="option-card"
              :class="{ 
                'selected': selectedAnswer === index,
                'correct': showAnswer && index === currentQuestion.correct_answer,
                'incorrect': showAnswer && selectedAnswer === index && index !== currentQuestion.correct_answer,
                'disabled': showAnswer && questionTimeLeft <= 0 && index !== currentQuestion.correct_answer
              }"
              @click="selectAnswer(index)"
            >
              <div class="option-letter">{{ String.fromCharCode(65 + index) }}</div>
              <span class="option-text" v-html="option"></span>
            </div>
          </div>

          <!-- Message de temps écoulé -->
          <div v-if="showAnswer && questionTimeLeft <= 0" class="timeout-message">
            <div class="timeout-icon">⏰</div>
            <p class="timeout-text">Temps écoulé ! La bonne réponse est affichée ci-dessus. Cliquez sur "Question suivante" pour continuer.</p>
          </div>

          <div v-if="showAnswer && currentQuestion.explanation" class="explanation">
            <h4 class="explanation-title">Explication :</h4>
            <p class="explanation-text" v-html="renderExplanation(currentQuestion.explanation)"></p>
          </div>

          <div class="quiz-actions">
            <button 
              v-if="!showAnswer"
              class="btn-primary"
              :disabled="selectedAnswer === null"
              @click="validateAnswer"
            >
              Valider
            </button>
            
            <div v-if="showAnswer" class="answer-actions">
              <button 
                v-if="currentQuestionIndex < currentQuiz.questions.length - 1"
                class="btn-primary"
                @click="nextQuestion"
              >
                Question suivante
              </button>
              <button 
                v-else
                class="btn-success"
                @click="finishQuiz"
              >
                Terminer le quiz
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Résultats du Quiz -->
      <div v-if="showResults" class="quiz-results">
        <div class="results-header">
          <h2 class="results-title">Résultats du Quiz</h2>
          <div class="score-circle" :class="getScoreClass(score)">
            <span class="score-percentage">{{ Math.round(score) }}%</span>
          </div>
        </div>

        <!-- Gamification Results -->
        <div v-if="quizResultSubmitted" class="gamification-results">
          <div class="xp-earned" :class="{ 'no-xp': lastXpGained === 0 }">
            <div class="xp-icon">
              <span v-if="lastXpGained > 0">🎉</span>
              <span v-else>💡</span>
            </div>
            <div class="xp-details">
              <div class="xp-amount">
                <span v-if="lastXpGained > 0">+{{ lastXpGained }} XP</span>
                <span v-else>0 XP</span>
              </div>
              <div class="xp-info">
                <span v-if="currentAttempt === 1 && lastXpGained > 0">🥇 Premier essai réussi ! XP = bonnes réponses × difficulté + bonus sans faute</span>
                <span v-else-if="currentAttempt === 1 && lastXpGained === 0">💪 Premier essai - Continue à t'améliorer !</span>
                <span v-else-if="currentAttempt > 1">🔄 Tentative supplémentaire - Aucun XP</span>
                <span v-else>Continue tes efforts !</span>
              </div>
            </div>
          </div>
          
          <div v-if="levelUp" class="level-up-display">
            <div class="level-up-icon">🆙</div>
            <div class="level-up-text">Niveau {{ userStore.level }} atteint !</div>
          </div>
        </div>

        <div class="results-stats">
          <div class="stat-card">
            <span class="stat-number">{{ correctAnswers }}</span>
            <span class="stat-label">Bonnes réponses</span>
          </div>
          <div class="stat-card">
            <span class="stat-number">{{ wrongAnswers }}</span>
            <span class="stat-label">Mauvaises réponses</span>
          </div>
          <div class="stat-card">
            <span class="stat-number">{{ totalQuestionsInCurrentQuiz }}</span>
            <span class="stat-label">Total questions</span>
          </div>
          <div class="stat-card gamification">
            <span class="stat-number">{{ currentAttempt }}</span>
            <span class="stat-label">Tentative #</span>
          </div>
        </div>



        <div class="results-actions">
          <button class="btn-primary" @click="backToList">Retour à la liste</button>
        </div>
      </div>
    </section>
  </DashboardLayout>
</template>

<script setup>
// Nom explicite pour KeepAlive
defineOptions({ name: 'ChapterQuiz' })
import { ref, computed, onMounted, onActivated, onUnmounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import SkeletonList from '@/components/common/SkeletonList.vue'
import { getQuiz, submitQuizResult, getQuizAttempts } from '@/api/quiz'
import { useUserStore } from '@/stores/user'
import { useSubjectsStore } from '@/stores/subjects/index'
import { useXP } from '@/composables/useXP'
import { calculateUserLevel } from '@/composables/useLevel'
import BackButton from '@/components/common/BackButton.vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const subjectsStore = useSubjectsStore()
const { handleQuizCompletion, updateUserXPInstantly } = useXP()
const quiz = ref([])
const notionNom = ref('')
const initialLoading = ref(true)

// État du quiz en cours
const currentQuiz = ref(null)
const currentQuestionIndex = ref(0)
const selectedAnswer = ref(null)
const showAnswer = ref(false)
const userAnswers = ref([])
const showResults = ref(false)

// Variables gamification
const currentAttempt = ref(1)
const lastXpGained = ref(0)
const levelUp = ref(false)
const quizResultSubmitted = ref(false)
const quizStartTime = ref(null)

// Variables de sauvegarde automatique
const quizSessionId = ref(null)
const lastSavedState = ref(null)
// Timers par question
const questionStartTime = ref(null)
const questionTick = ref(0)
let questionTimerInterval = null

// =============================
// Rendu texte explication (sauts de ligne, espaces, LaTeX)
// =============================
function normalizeLineBreaks(text) {
  if (!text) return text
  let t = String(text)
  // LaTeX line break: \\ → saut de ligne
  t = t.replace(/\\(\s|$)/g, '\n')
  // Séquence littérale \n
  t = t.replace(/\\n/g, '\n')
  // Alias admin
  t = t.replace(/(^|\s)\/{2}(?=\s|$)/g, '$1\n')
  t = t.replace(/(^|\s)\/n(?=\s|$)/g, '$1\n')
  t = t.replace(/(^|\s)\$\/{2}\$(?=\s|$)/g, '$1\n')
  return t
}

function enforceDisplayStyleInMath(t) {
  if (!t) return t
  // $$...$$ block
  t = t.replace(/\$\$([\s\S]*?)\$\$/g, (match, inner) => {
    const trimmed = String(inner).trim()
    if (trimmed.startsWith('\\displaystyle')) return match
    return `$$\\displaystyle ${inner}$$`
  })
  // $...$ inline
  t = t.replace(/\$([^$\n]+)\$/g, (match, inner) => {
    const trimmed = String(inner).trim()
    if (trimmed.startsWith('\\displaystyle')) return match
    return `$\\displaystyle ${inner}$`
  })
  return t
}

function renderExplanation(text) {
  if (!text) return text
  let processed = normalizeLineBreaks(text)
  processed = enforceDisplayStyleInMath(processed)
  // Espaces réduits
  processed = processed.replace(/\[SM\]/g, '<span class="spacer-sm"></span>')
  processed = processed.replace(/\[XS\]/g, '<span class="spacer-xs"></span>')
  // Convertir \n en <br/>
  processed = processed.replace(/\n/g, '<br/>')
  return processed
}

// Normalisation difficulté et paramètres temps/question
const normalizedDifficulty = computed(() => {
  const d = (currentQuiz.value?.difficulty || currentQuiz.value?.difficulte || 'easy').toString().toLowerCase()
  if (['easy', 'facile'].includes(d)) return 'easy'
  if (['medium', 'moyen'].includes(d)) return 'medium'
  if (['hard', 'difficile'].includes(d)) return 'hard'
  return 'easy'
})

const timePerQuestionSeconds = computed(() => {
  const map = { easy: 20, medium: 25, hard: 30 }
  return map[normalizedDifficulty.value] || 20
})

const questionTimeAllowed = computed(() => timePerQuestionSeconds.value)
const questionTimeElapsed = computed(() => {
  // Dépendance réactive pour recalculer chaque seconde
  const _tick = questionTick.value
  if (!questionStartTime.value) return 0
  return Math.max(0, Math.floor((Date.now() - questionStartTime.value) / 1000))
})
const questionTimeLeft = ref(0)

// Pour l'animation CSS fluide
const timerAnimationDuration = computed(() => `${questionTimeAllowed.value}s`)
const timerAnimationKey = ref(0)
const isTimerActive = ref(true)

function startQuestionTimer() {
  if (questionTimerInterval) {
    clearInterval(questionTimerInterval)
    questionTimerInterval = null
  }
  
  // Réinitialiser le temps et activer le timer
  questionTimeLeft.value = questionTimeAllowed.value
  isTimerActive.value = true
  questionStartTime.value = Date.now()
  
  // Incrémenter la clé pour redémarrer l'animation CSS
  timerAnimationKey.value++
  
  questionTimerInterval = setInterval(() => {
    // Déclenche une mise à jour réactive du timer pour le texte uniquement
    questionTimeLeft.value--
    
    // Vérifier si le temps est écoulé
    if (questionTimeLeft.value <= 0) {
      handleTimeOut()
    }
  }, 1000)
}

function handleTimeOut() {
  console.log('⏰ Temps écoulé pour la question', currentQuestionIndex.value + 1)
  
  // Arrêter le timer
  stopQuestionTimer()
  
  // Marquer comme mauvaise réponse (pas de réponse sélectionnée)
  userAnswers.value.push({
    questionIndex: currentQuestionIndex.value,
    selectedAnswer: null, // Aucune réponse sélectionnée
    correctAnswer: currentQuestion.value.correct_answer,
    correct: false, // Automatiquement incorrect
    timeOut: true // Marquer comme temps écoulé
  })
  
  // Afficher la bonne réponse et attendre l'action de l'utilisateur
  showAnswer.value = true
  selectedAnswer.value = null
  
  // Sauvegarder l'état après le timeout
  saveQuizState()
  
  console.log('⏰ Temps écoulé - Affichage de la bonne réponse, attente action utilisateur')
}

function stopQuestionTimer() {
  if (questionTimerInterval) {
    clearInterval(questionTimerInterval)
    questionTimerInterval = null
  }
  // Arrêter l'animation de la barre de progression
  isTimerActive.value = false
}

// Variables pour les onglets
const activeTab = ref('todo')

// --- Persistence (sessionStorage) for list state ---
const quizStorageKey = computed(() => {
  const notionId = route.params.notionId
  return notionId ? `optitab_page_quiz_${notionId}` : 'optitab_page_quiz_generic'
})

function saveQuizListState(extra = {}) {
  try {
    const state = {
      activeTab: activeTab.value,
      currentPage: currentPage?.value ?? 1,
      scrollY: typeof window !== 'undefined' ? (window.scrollY || window.pageYOffset || 0) : 0,
      t: Date.now(),
      ...extra
    }
    sessionStorage.setItem(quizStorageKey.value, JSON.stringify(state))
  } catch (_) {}
}

function restoreQuizListState() {
  try {
    const raw = sessionStorage.getItem(quizStorageKey.value)
    if (!raw) return null
    const s = JSON.parse(raw)
    if (s && typeof s === 'object') {
      if (typeof s.activeTab === 'string') activeTab.value = s.activeTab
      if (typeof s.currentPage === 'number' && currentPage) currentPage.value = Math.max(1, s.currentPage)
      return s
    }
  } catch (_) {}
  return null
}
const chapterQuizAttempts = ref([])
const loadingStats = ref(false)


// Ensemble réactif des quiz sauvegardés (À continuer)
const savedQuizzesSet = ref(new Set())

// Alias pour compatibilité avec le template et le code existant
// (les refs sont auto-déréférencées dans le template)
const savedQuizzes = savedQuizzesSet

// Rafraîchir l'ensemble des quiz sauvegardés depuis localStorage
function refreshSavedQuizzes() {
  try {
    const newSet = new Set()
    quiz.value.forEach(q => {
      if (hasSavedProgress(q.id)) {
        newSet.add(q.id)
        console.log(`✅ Quiz ${q.id} (${q.titre}) détecté comme sauvegardé`)
      }
    })
    // Remplacer la référence pour déclencher la réactivité
    savedQuizzesSet.value = newSet
    console.log('🔄 Rafraîchissement des quiz sauvegardés:', newSet.size, 'quiz trouvés')
    console.log('🔄 IDs des quiz sauvegardés:', Array.from(newSet))
  } catch (e) {
    console.warn('⚠️ Impossible de rafraîchir les quiz sauvegardés:', e)
  }
}

const currentQuestion = computed(() => {
  if (!currentQuiz.value || !currentQuiz.value.questions) return null
  return currentQuiz.value.questions[currentQuestionIndex.value]
})

// Total de toutes les questions de tous les quiz
const totalQuestions = computed(() => {
  return quiz.value.reduce((total, q) => total + (q.questions?.length || 0), 0)
})

const correctAnswers = computed(() => userAnswers.value.filter(answer => answer.correct).length)
const wrongAnswers = computed(() => userAnswers.value.filter(answer => !answer.correct).length)
const totalQuestionsInCurrentQuiz = computed(() => userAnswers.value.length)
const score = computed(() => totalQuestionsInCurrentQuiz.value > 0 ? (correctAnswers.value / totalQuestionsInCurrentQuiz.value) * 100 : 0)

// Computed pour les onglets (logique pédagogique claire)
const tabs = computed(() => {
  // ONGLET 1: À faire - Quiz jamais commencés
  const todoQuiz = quiz.value.filter(q => !hasAttemptedQuiz(q.id) && !(savedQuizzes.value && savedQuizzes.value.has(q.id)))
  
  // ONGLET 3: Sous la moyenne - Quiz complètement terminés avec note < 5/10
  const belowAverageQuiz = quiz.value.filter(q => {
    // Exclure les quiz avec sauvegarde active (priorité à "À continuer")
    if (savedQuizzes.value && savedQuizzes.value.has(q.id)) return false
    
    if (!hasAttemptedQuiz(q.id)) return false
    
    // Vérifier que le quiz est complètement terminé
    const attempts = chapterQuizAttempts.value.filter(a => a.quiz === q.id)
    if (attempts.length > 0) {
      const lastAttempt = attempts[attempts.length - 1]
      const totalQuestions = q.questions?.length || 0
      const questionsAnswered = lastAttempt.total_points || 0
      
      // Si le quiz n'est pas complet, il ne va pas dans "sous la moyenne"
      if (questionsAnswered < totalQuestions) return false
    }
    
    const lastScore = getLastScore(q.id)
    return lastScore < 5
  })
  
  // ONGLET 4: Réussis - Quiz complètement terminés avec note >= 5/10
  const completedQuiz = quiz.value.filter(q => {
    // Exclure les quiz avec sauvegarde active (priorité à "À continuer")
    if (savedQuizzes.value && savedQuizzes.value.has(q.id)) return false
    
    if (!hasAttemptedQuiz(q.id)) return false
    
    // Vérifier que le quiz est complètement terminé
    const attempts = chapterQuizAttempts.value.filter(a => a.quiz === q.id)
    if (attempts.length > 0) {
      const lastAttempt = attempts[attempts.length - 1]
      const totalQuestions = q.questions?.length || 0
      const questionsAnswered = lastAttempt.total_points || 0
      
      // Si le quiz n'est pas complet, il ne va pas dans "réussis"
      if (questionsAnswered < totalQuestions) return false
    }
    
    const lastScore = getLastScore(q.id)
    return lastScore >= 5
  })
  
  // ONGLET 2: À continuer - Quiz commencés mais pas terminés
  const continuableQuiz = quiz.value.filter(q => {
    // Cas 1: Quiz avec sauvegarde active (priorité absolue)
    if (savedQuizzes.value && savedQuizzes.value.has(q.id)) {
      return true
    }
    
    // Cas 2: Quiz avec tentative mais pas complètement terminé
    if (hasAttemptedQuiz(q.id)) {
      const attempts = chapterQuizAttempts.value.filter(a => a.quiz === q.id)
      if (attempts.length > 0) {
        const lastAttempt = attempts[attempts.length - 1]
        const totalQuestions = q.questions?.length || 0
        
        // Vérifier si toutes les questions ont été répondues
        // total_points = nombre total de questions dans le quiz quand terminé
        // Si total_points < totalQuestions, le quiz n'est pas complet
        const questionsAnswered = lastAttempt.total_points || 0
        const isIncomplete = questionsAnswered < totalQuestions
        
        if (isIncomplete) {
          return true
        }
      }
    }
    
    return false
  })
  
  // Toujours afficher "À continuer" s'il y a des quiz à continuer OU si on a des quiz sauvegardés
  const hasSavedQuizzes = savedQuizzes.value && savedQuizzes.value.size > 0
  const shouldShowContinueTab = continuableQuiz.length > 0 || hasSavedQuizzes
  

  
  const tabList = [
    {
      key: 'todo',
      label: 'Quiz à faire',
      shortLabel: 'À faire',
      icon: '📝',
      count: todoQuiz.length,
      description: 'Quiz jamais commencés'
    }
  ]
  
  // Toujours afficher "À continuer" s'il y a des quiz à continuer OU si on a des quiz sauvegardés
  if (shouldShowContinueTab) {
    tabList.push({
      key: 'continue',
      label: 'Quiz à continuer',
      shortLabel: 'À continuer',
      icon: '🔄',
      count: continuableQuiz.length,
      priority: 'high',
      description: 'Quiz commencés mais pas terminés'
    })
  }
  
  // Afficher "Sous la moyenne" s'il y a des quiz avec note < 5
  if (belowAverageQuiz.length > 0) {
    tabList.push({
      key: 'below-average',
      label: 'Sous la moyenne',
      shortLabel: 'À revoir',
      icon: '📈',
      count: belowAverageQuiz.length,
      description: 'Quiz à refaire (note < 5/10)'
    })
  }
  
  // Toujours afficher "Terminés" s'il y a des quiz réussis
  if (completedQuiz.length > 0) {
  tabList.push({
    key: 'done', 
      label: 'Quiz réussis',
      shortLabel: 'Réussis',
    icon: '✅',
      count: completedQuiz.length,
      description: 'Quiz maîtrisés (note ≥ 5/10)'
  })
  }
  
  return tabList
})

// Quand les tentatives changent, s'assurer que l'onglet actif reste valide
watch(chapterQuizAttempts, () => {
  // Vérifier si l'onglet actuel est encore valide
  const currentTabs = tabs.value
  const isActiveTabValid = currentTabs.some(tab => tab.key === activeTab.value)
  
  if (!isActiveTabValid && currentTabs.length > 0) {
    // Basculer vers le premier onglet disponible
    activeTab.value = currentTabs[0].key
  }
  
  // Forcer la mise à jour des computed des onglets
}, { deep: true })

// Variables pour la pagination
const currentPage = ref(1)
const itemsPerPage = 5

// Computed pour les quiz filtrés selon l'onglet actif
const filteredQuiz = computed(() => {
  switch (activeTab.value) {
    case 'todo':
      // À faire: Quiz jamais commencés
      return quiz.value.filter(q => !hasAttemptedQuiz(q.id) && !(savedQuizzes.value && savedQuizzes.value.has(q.id)))
      
    case 'continue':
      // À continuer: Quiz commencés mais pas terminés
      return quiz.value.filter(q => {
        // Cas 1: Quiz avec sauvegarde active (priorité absolue)
        if (savedQuizzes.value && savedQuizzes.value.has(q.id)) return true
        
        // Cas 2: Quiz avec tentative mais pas complètement terminé
        if (hasAttemptedQuiz(q.id)) {
          const attempts = chapterQuizAttempts.value.filter(a => a.quiz === q.id)
          if (attempts.length > 0) {
            const lastAttempt = attempts[attempts.length - 1]
            const totalQuestions = q.questions?.length || 0
            
            // Vérifier si toutes les questions ont été répondues
            const questionsAnswered = lastAttempt.total_points || 0
            return questionsAnswered < totalQuestions
          }
        }
        
        return false
      })
      
    case 'below-average':
      // Sous la moyenne: Quiz complètement terminés avec note < 5/10
      return quiz.value.filter(q => {
        // Exclure les quiz avec sauvegarde active (priorité à "À continuer")
        if (savedQuizzes.value && savedQuizzes.value.has(q.id)) return false
        
        if (!hasAttemptedQuiz(q.id)) return false
        
        // Vérifier que le quiz est complètement terminé
        const attempts = chapterQuizAttempts.value.filter(a => a.quiz === q.id)
        if (attempts.length > 0) {
          const lastAttempt = attempts[attempts.length - 1]
          const totalQuestions = q.questions?.length || 0
          const questionsAnswered = lastAttempt.total_points || 0
          
          // Si le quiz n'est pas complet, il ne va pas dans "sous la moyenne"
          if (questionsAnswered < totalQuestions) return false
        }
        
        const lastScore = getLastScore(q.id)
        return lastScore < 5
      })
      
    case 'done':
      // Réussis: Quiz complètement terminés avec note >= 5/10
      return quiz.value.filter(q => {
        // Exclure les quiz avec sauvegarde active (priorité à "À continuer")
        if (savedQuizzes.value && savedQuizzes.value.has(q.id)) return false
        
        if (!hasAttemptedQuiz(q.id)) return false
        
        // Vérifier que le quiz est complètement terminé
        const attempts = chapterQuizAttempts.value.filter(a => a.quiz === q.id)
        if (attempts.length > 0) {
          const lastAttempt = attempts[attempts.length - 1]
          const totalQuestions = q.questions?.length || 0
          const questionsAnswered = lastAttempt.total_points || 0
          
          // Si le quiz n'est pas complet, il ne va pas dans "réussis"
          if (questionsAnswered < totalQuestions) return false
        }
        
        const lastScore = getLastScore(q.id)
        return lastScore >= 5
      })
      
    default:
  return quiz.value
  }
})

// Computed pour les quiz paginés selon l'onglet actif
const paginatedQuiz = computed(() => {
  const startIndex = (currentPage.value - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  return filteredQuiz.value.slice(startIndex, endIndex)
})

// Computed pour le nombre total de pages
const totalPages = computed(() => {
  return Math.ceil(filteredQuiz.value.length / itemsPerPage)
})

// Fonction pour changer de page
function changePage(page) {
  currentPage.value = page
  saveQuizListState()
}

// Fonction pour aller à la page précédente
function previousPage() {
  if (currentPage.value > 1) {
    currentPage.value--
    saveQuizListState()
  }
}

// Fonction pour aller à la page suivante
function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    saveQuizListState()
  }
}

// Réinitialiser la pagination quand l'onglet change
watch(activeTab, () => {
  currentPage.value = 1
  saveQuizListState()
})

// Fonction de debug pour vérifier l'état des quiz
function debugQuizState() {
  console.log('🔍 Debug - État des quiz (logique pédagogique):')
  quiz.value.forEach(q => {
    const hasAttempt = hasAttemptedQuiz(q.id)
    const hasSave = savedQuizzes.value && savedQuizzes.value.has(q.id)
    const attempts = chapterQuizAttempts.value.filter(a => a.quiz === q.id)
    const lastScore = getLastScore(q.id)
    
    // Vérifier si le quiz est incomplet (à continuer)
    let isIncomplete = false
    if (hasAttempt && attempts.length > 0) {
      const lastAttempt = attempts[attempts.length - 1]
      const totalQuestions = q.questions?.length || 0
      const questionsAnswered = lastAttempt.total_points || 0
      isIncomplete = questionsAnswered < totalQuestions
    }
    
    let category = 'À faire'
    if (hasSave && !hasAttempt) {
      category = 'À continuer (sauvegardé)'
    } else if (isIncomplete) {
      category = 'À continuer (incomplet)'
    } else if (hasAttempt) {
      category = lastScore < 5 ? 'Sous la moyenne (À revoir)' : 'Réussis'
    }
    
    console.log(`Quiz ${q.id} (${q.titre}):`, {
      hasAttempt,
      hasSave,
      attemptsCount: attempts.length,
      lastScore: lastScore,
      category: category,
      belowAverage: hasAttempt && lastScore < 5,
      isIncomplete: isIncomplete,
      totalQuestions: q.questions?.length || 0,
      questionsAnswered: attempts.length > 0 ? (attempts[attempts.length - 1].total_points || 0) : 0
    })
  })
}

// Helper functions
function hasAttemptedQuiz(quizId) {
  return chapterQuizAttempts.value.some(attempt => attempt.quiz === quizId)
}

function getBestScore(quizId) {
  const attempts = chapterQuizAttempts.value.filter(attempt => attempt.quiz === quizId)
  if (attempts.length === 0) return 0
  
  const bestAttempt = attempts.reduce((best, current) => {
    const currentScore = current.total_points > 0 ? (current.score / current.total_points) * 10 : 0
    const bestScore = best.total_points > 0 ? (best.score / best.total_points) * 10 : 0
    return currentScore > bestScore ? current : best
  })
  
  return bestAttempt.total_points > 0 ? Math.round((bestAttempt.score / bestAttempt.total_points) * 10 * 10) / 10 : 0
}

function getAttemptCount(quizId) {
  return chapterQuizAttempts.value.filter(attempt => attempt.quiz === quizId).length
}

// Dernière note sur /10 pour ce quiz
function getLastScore(quizId) {
  const attempts = chapterQuizAttempts.value
    .filter(a => a.quiz === quizId)
    .sort((a, b) => {
      const aDate = new Date(a.date_creation || a.created_at || 0)
      const bDate = new Date(b.date_creation || b.created_at || 0)
      return bDate - aDate
    })

  if (!attempts.length) return 0
  const last = attempts[0]
  if (!last || !last.total_points) return 0
  const score10 = (Number(last.score) || 0) / (Number(last.total_points) || 1) * 10
  return Math.round(score10 * 10) / 10
}

// Fonction pour rendre les formules LaTeX avec MathJax
const renderMath = () => {
  nextTick(() => {
    if (window.MathJax) {
      window.MathJax.typesetPromise()
    }
  })
}

// Watcher pour rendre les formules quand la question change
watch(currentQuestion, () => {
  if (currentQuestion.value) {
    renderMath()
  }
}, { deep: true })

// Watcher pour rendre les formules quand on affiche la réponse
watch(showAnswer, () => {
  if (showAnswer.value) {
    renderMath()
  }
})

async function loadChapterQuizAttempts() {
  try {
    loadingStats.value = true
    const map = []
    // Charger tentatives par quiz courant
    for (const q of (quiz.value || [])) {
      try {
        const resp = await getQuizAttempts(q.id)
        const attempts = Array.isArray(resp) ? resp : (resp?.data || resp?.results || [])
        map.push(...attempts)
      } catch (_) {}
    }
    chapterQuizAttempts.value = map
  } catch (error) {
    console.error('❌ Erreur lors du chargement des tentatives:', error)
    chapterQuizAttempts.value = []
  } finally {
    loadingStats.value = false
  }
}

onMounted(async () => {
  // Nettoyer les sauvegardes corrompues au démarrage
  cleanupCorruptedSaves()
  
  // Ajouter les event listeners pour la détection de déconnexion
  window.addEventListener('beforeunload', handleBeforeUnload)
  window.addEventListener('pagehide', () => {
    if (currentQuiz.value && !showResults.value) {
      saveQuizState()
    }
  })
  
  try {
    const notionId = route.params.notionId
    const targetQuizId = route.query.quizId
    
    console.log(`[ChapterQuiz] 🚀 Chargement optimisé - Notion: ${notionId}, Quiz cible: ${targetQuizId || 'Aucun'}`)
    
    // Paralléliser les opérations de chargement pour plus de fluidité
    const [quizData] = await Promise.all([
      // Charger les quiz par notion
      getQuiz(notionId)
    ])
    
    // Traitement des données de chapitre
    notionNom.value = 'Notion'
    
    // Traitement des données de quiz
    const rawList = Array.isArray(quizData.data) ? quizData.data : (quizData.data?.quiz || [])
    quiz.value = rawList.map((q) => ({
      ...q,
      questions: Array.isArray(q?.questions) ? q.questions : (Array.isArray(q?.questions_data) ? q.questions_data : [])
    }))
    
    console.log(`[ChapterQuiz] ✅ Quiz chargés: ${quiz.value.length}`)
    
    // Désactiver le skeleton de chargement initial
    initialLoading.value = false
    
    // Mettre à jour les quiz sauvegardés IMMÉDIATEMENT après le chargement des quiz
    refreshSavedQuizzes()
    
    // Si un quiz spécifique est ciblé, le démarrer immédiatement
    if (targetQuizId) {
      const targetQuiz = quiz.value.find(q => q.id == targetQuizId)
      if (targetQuiz) {
        const isAutoStart = route.query.autoStart === 'true'
        console.log(`[ChapterQuiz] 🎯 Quiz trouvé: ${targetQuiz.titre} (Auto-start: ${isAutoStart})`)
        
        if (isAutoStart) {
          // Mode turbo: démarrage ultra-rapide
          console.log(`[ChapterQuiz] ⚡ Mode turbo activé`)
          
          
          // Démarrage immédiat sans attendre
          startQuiz(targetQuiz)
          return
        } else {
          // Mode standard avec toutes les données
          loadChapterQuizAttempts().then(() => {
            console.log(`[ChapterQuiz] 📊 Toutes les données chargées`)
          })
          
          await nextTick()
          await startQuiz(targetQuiz)
          return
        }
      } else {
        console.warn(`[ChapterQuiz] ⚠️ Quiz ${targetQuizId} non trouvé`)
      }
    }
    
    // Pour l'affichage normal de la liste, charger toutes les données
    await loadChapterQuizAttempts()
    
    // Mettre à jour l'ensemble réactif des quiz sauvegardés IMMÉDIATEMENT
    refreshSavedQuizzes()
    
    // Préchargement optimisé des quiz sauvegardés
    preloadSavedQuizzes()
    
    // Rendre les formules LaTeX
    await nextTick()
    renderMath()
    
    // Restaurer l'état de la liste (onglet/page) et le scroll
    const saved = restoreQuizListState()
    // Clamp la page si hors bornes
    try {
      const pages = Math.max(1, Math.ceil((filteredQuiz?.value?.length || 0) / (itemsPerPage || 1)))
      if (currentPage.value > pages) currentPage.value = pages
    } catch (_) {}
    await nextTick()
    setTimeout(() => {
      try {
        const raw = sessionStorage.getItem(quizStorageKey.value)
        if (raw) {
          const s = JSON.parse(raw)
          if (s && typeof s.scrollY === 'number') {
            window.scrollTo({ top: s.scrollY, behavior: 'auto' })
          }
        }
      } catch (_) {}
    }, 50)
    
  } catch (e) {
    console.error(`[ChapterQuiz] ❌ Erreur de chargement:`, e)
    quiz.value = []
  } finally {
    // S'assurer que le skeleton disparaît même en cas d'erreur
    initialLoading.value = false
  }
})

// Hook onActivated - appelé quand le composant est réactivé depuis le cache KeepAlive
onActivated(() => {
  // Rafraîchir les quiz sauvegardés à chaque réactivation
  refreshSavedQuizzes()
  
  // Forcer le rendu MathJax à chaque réactivation pour éviter les problèmes de cache
  nextTick(() => {
    renderMath()
    // S'assurer que le rendu est bien appliqué avec un second appel après un délai
    setTimeout(() => {
      renderMath()
    }, 100)
  })
})

// Recharger proprement quand on change de notion sous KeepAlive
async function reloadForNotion(notionId) {
  try {
    // Reset des états clés
    initialLoading.value = true
    quiz.value = []
    currentQuiz.value = null
    currentQuestionIndex.value = 0
    showAnswer.value = false
    userAnswers.value = []
    showResults.value = false

    const targetQuizId = route.query.quizId
    const [quizData] = await Promise.all([
      getQuiz(notionId)
    ])

    notionNom.value = 'Notion'
    const rawList = Array.isArray(quizData.data) ? quizData.data : (quizData.data?.quiz || [])
    quiz.value = rawList.map((q) => ({
      ...q,
      questions: Array.isArray(q?.questions) ? q.questions : (Array.isArray(q?.questions_data) ? q.questions_data : [])
    }))

    // Charger annexes pour la liste
    await loadChapterQuizAttempts()

    refreshSavedQuizzes()

    // Auto-start si demandé
    if (targetQuizId) {
      const targetQuiz = quiz.value.find(q => q.id == targetQuizId)
      if (targetQuiz && route.query.autoStart === 'true') {
        startQuiz(targetQuiz)
      }
    }
  } catch (e) {
    console.error('[ChapterQuiz] Erreur lors du rechargement:', e)
  } finally {
    initialLoading.value = false
  }
}

watch(() => route.params.notionId, async (newId, oldId) => {
  if (newId && newId !== oldId) {
    await reloadForNotion(newId)
  }
})

onUnmounted(() => {
  saveQuizListState()
})

function getDifficultyLabel(difficulty) {
  const labels = {
    'easy': 'Facile',
    'medium': 'Moyen',
    'hard': 'Difficile'
  }
  return labels[difficulty] || difficulty
}

function getDifficultyStars(difficulty) {
  const stars = {
    'easy': 1,
    'medium': 2,
    'hard': 3
  }
  return stars[difficulty] || 1
}

function formatSavedTime(date) {
  if (!date) return 'Inconnu'
  
  const now = new Date()
  const diff = now - date
  const minutes = Math.floor(diff / (1000 * 60))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (minutes < 1) return 'À l\'instant'
  if (minutes < 60) return `Il y a ${minutes}min`
  if (hours < 24) return `Il y a ${hours}h`
  if (days < 7) return `Il y a ${days}j`
  
  return date.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}


async function startQuiz(quizData) {
  // Vérifier l'authentification
  if (!userStore.isAuthenticated) {
    console.warn('⚠️ Utilisateur non authentifié, démarrage du quiz en mode local')
    // Continuer en mode local sans sauvegarde serveur
  }
  
  
  // Démarrage immédiat pour une expérience fluide
  console.log(`[ChapterQuiz] 🚀 Démarrage rapide du quiz: ${quizData.titre}`)
  
  // Normaliser l'objet quiz sélectionné pour garantir 'questions'
  currentQuiz.value = {
    ...quizData,
    questions: Array.isArray(quizData?.questions) ? quizData.questions : (Array.isArray(quizData?.questions_data) ? quizData.questions_data : [])
  }
  
  // Vérifier s'il existe une sauvegarde à restaurer
  const hasRestoredSession = restoreQuizState(currentQuiz.value)
  
  if (!hasRestoredSession) {
    // Nouveau quiz - initialiser l'état
    currentQuestionIndex.value = 0
    selectedAnswer.value = null
    showAnswer.value = false
    userAnswers.value = []
    showResults.value = false
    quizResultSubmitted.value = false
    quizStartTime.value = Date.now()
    
    // Générer un nouvel ID de session
    quizSessionId.value = generateSessionId()
    
    console.log(`🆕 Nouveau quiz démarré - Session: ${quizSessionId.value}`)
    
    // Sauvegarder immédiatement l'état pour que le quiz apparaisse dans "À continuer"
    saveQuizState()
  } else {
    // Réinitialiser seulement les variables d'interface
    selectedAnswer.value = null
    showAnswer.value = false
    // Ne pas écraser l'état des résultats si la restauration a décidé d'afficher le score
    if (!showResults.value) {
      quizResultSubmitted.value = false
    }
    
    console.log(`🔄 Quiz restauré - Session: ${quizSessionId.value}`)
    console.log(`📍 Reprise à la question ${currentQuestionIndex.value + 1}/${currentQuiz.value.questions.length}`)
    
  }
  
  // Sauvegarder l'état initial
  saveQuizState()
  
  // Démarrer le timer de la question actuelle
  startQuestionTimer()
  
  // Charger les tentatives en arrière-plan (non-bloquant)
  getQuizAttempts(quizData.id)
    .then(attempts => {
      const attemptsArray = Array.isArray(attempts) ? attempts : (attempts?.data || attempts?.results || [])
      if (!hasRestoredSession) {
        currentAttempt.value = (attemptsArray.length || 0) + 1
      }
    })
    .catch((error) => {
      console.warn('⚠️ Impossible de charger les tentatives (probablement non connecté):', error.message)
      if (!hasRestoredSession) {
        currentAttempt.value = 1
      }
    })
  
  // Rendre les formules LaTeX au prochain tick (non-bloquant)
  nextTick(() => {
    renderMath()
  })
}

function selectAnswer(index) {
  if (!showAnswer.value && questionTimeLeft.value > 0) {
    selectedAnswer.value = index
    // Le timer continue de tourner, il ne s'arrête que quand on valide
  }
}

function validateAnswer() {
  if (selectedAnswer.value === null) return
  
  // Vérifier les tentatives de triche avant de valider
  if (detectCheating()) {
    alert('🚨 Tentative de triche détectée. Le quiz va redémarrer.')
    clearQuizSave(currentQuiz.value.id)
    location.reload()
    return
  }
  
  // Arrêter le timer et la barre de progression quand on valide
  stopQuestionTimer()
  
  showAnswer.value = true
  const isCorrect = selectedAnswer.value === currentQuestion.value.correct_answer
  
  userAnswers.value.push({
    questionIndex: currentQuestionIndex.value,
    selectedAnswer: selectedAnswer.value,
    correctAnswer: currentQuestion.value.correct_answer,
    correct: isCorrect,
    timestamp: Date.now() // Ajouter timestamp pour traçabilité
  })
  
  // Sauvegarder l'état après chaque réponse
  saveQuizState()
}

function nextQuestion() {
  // Vérifier qu'on ne dépasse pas le nombre total de questions
  if (currentQuestionIndex.value < currentQuiz.value.questions.length - 1) {
    currentQuestionIndex.value++
    selectedAnswer.value = null
    showAnswer.value = false
    
    // Sauvegarder l'état avant de passer à la question suivante
    saveQuizState()
    
    // Rendre les formules LaTeX de la nouvelle question
    renderMath()
    startQuestionTimer()
  } else {
    // Si on est à la dernière question, terminer le quiz
    finishQuiz()
  }
}

async function finishQuiz() {
  showResults.value = true
  stopQuestionTimer()
  
  // Nettoyer la sauvegarde car le quiz est terminé
  clearQuizSave(currentQuiz.value.id)
  
  // Calculer le temps total
  const timeElapsed = quizStartTime.value ? Math.floor((Date.now() - quizStartTime.value) / 1000) : 0
  
  // Calculer les points totaux et le score
  const totalPoints = currentQuiz.value.questions.length
  const score = correctAnswers.value
  
  console.log('🎯 Soumission quiz:', {
    quiz_id: currentQuiz.value.id,
    score: score,
    total_points: totalPoints,
    temps_total_seconde: timeElapsed,
    pourcentage_score: totalPoints > 0 ? (score / totalPoints * 100) : 0,
    tentative_prevue: currentAttempt.value,
    questions_answered: userAnswers.value.length,
    questions_lost: totalPoints - userAnswers.value.length
  })
  
  // Soumettre les résultats pour la gamification
  try {
    const oldLevel = userStore.level
    
    const result = await submitQuizResult({
      quiz_id: currentQuiz.value.id,
      score: score,
      total_points: totalPoints,
      temps_total_seconde: timeElapsed
    })
    
    console.log('🎯 Résultat soumission:', result)
    console.log('🎯 XP dans la réponse:', result?.xp_gagne, result?.data?.xp_gagne)
    console.log('🎯 Tentative dans la réponse:', result?.tentative_numero, result?.data?.tentative_numero)
    
    // Récupérer les XP gagnés depuis la réponse (et afficher immédiatement)
    const xpGained = Number(result?.xp_gagne ?? result?.data?.xp_gagne ?? 0)
    const tentativeActuelle = Number(result?.tentative_numero ?? result?.data?.tentative_numero ?? currentAttempt.value)
    
    console.log('🎯 XP récupérés:', xpGained, 'pour tentative:', tentativeActuelle)
    
    // Afficher tout de suite les résultats de gamification
    lastXpGained.value = xpGained
    currentAttempt.value = tentativeActuelle
    quizResultSubmitted.value = true

    // Objectifs journaliers supprimés
    
    // Utiliser le système de notification XP (gère aussi la mise à jour des XP)
    try {
      await handleQuizCompletion(
        currentQuiz.value.id, 
        xpGained, 
        tentativeActuelle,
        currentQuiz.value.titre || 'Quiz'
      )
    } catch (e) {
      console.warn('⚠️ Notification XP a échoué:', e)
    }
    
    // Validation simple
    if (tentativeActuelle >= 3 && xpGained > 0) {
      console.warn('⚠️ Incohérence détectée: XP > 0 pour tentative >= 3')
    }
    
    console.log('🧮 XP reçus:', { 
      received: xpGained, 
      score: score,
      totalPoints: totalPoints,
      tentative: tentativeActuelle 
    })
    
    // Recharger les tentatives pour mettre à jour les onglets IMMÉDIATEMENT
    await loadChapterQuizAttempts()
    // Rafraîchir la liste des quiz sauvegardés (doit être vide pour ce quiz)
    refreshSavedQuizzes()
    
    console.log('🎯 Quiz terminé, rechargement effectué')
    console.log('🎯 Nombre total de tentatives après rechargement:', chapterQuizAttempts.value.length)
    
    // Debug pour vérifier l'état des quiz
    debugQuizState()
    
    // Forcer la mise à jour réactive des computed pour les onglets
    nextTick(() => {
      // Forcer la réactivité des computed
      console.log('🔄 Mise à jour réactive des onglets après fin de quiz')
    })
    
  } catch (error) {
    console.error('Erreur lors de la soumission du quiz:', error)
    
    // Gérer les erreurs de soumission
    if (error.response?.status === 400 && error.response?.data?.detail) {
      alert(error.response.data.detail)
      // Revenir à la liste des quiz
      await backToList()
      return
    }
    
    // Continuer même en cas d'erreur de gamification
    lastXpGained.value = 0
    quizResultSubmitted.value = false
  }
  
  
  // Les quiz sauvegardés sont maintenant mis à jour automatiquement via computed
}


async function backToList() {
  // NE PAS nettoyer la sauvegarde pour permettre à l'utilisateur de reprendre plus tard
  // Avant de quitter, sauvegarder l'état courant pour éviter tout retour en arrière d'index
  try {
    saveQuizState()
  } catch (_) {}
  // La sauvegarde sera automatiquement nettoyée soit:
  // - Quand le quiz est terminé (dans finishQuiz)
  // - Quand elle expire (1 heure max)
  // - Quand l'utilisateur redémarre le quiz
  
  currentQuiz.value = null
  showResults.value = false
  
  // Recharger les tentatives pour s'assurer que les onglets sont à jour
  await loadChapterQuizAttempts()
  
  // Rafraîchir les quiz sauvegardés pour afficher le bouton "Continuer"
  refreshSavedQuizzes()
  
  // Forcer la mise à jour réactive des computed pour les onglets
  nextTick(() => {
    console.log('🔄 Mise à jour réactive des onglets après retour à la liste')
  })
  
  console.log('🔄 Retour à la liste, tentatives rechargées, quiz sauvegardés rafraîchis')
}

function getScoreClass(score) {
  if (score >= 80) return 'excellent'
  if (score >= 60) return 'good'
  if (score >= 40) return 'average'
  return 'poor'
}

function getScoreColorClass(scoreOn10) {
  const score = Number(scoreOn10)
  if (score < 5) return 'score-below-average' // Rouge : en dessous de la moyenne
  if (score === 5) return 'score-average' // Orange : dans la moyenne
  return 'score-above-average' // Vert : au-dessus de la moyenne
}



// ===== SYSTÈME DE SAUVEGARDE AUTOMATIQUE =====

// Générer un ID de session unique
function generateSessionId() {
  return `quiz_${currentQuiz.value?.id}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

// Sauvegarder l'état actuel du quiz (optimisé)
function saveQuizState() {
  if (!currentQuiz.value || showResults.value) return
  
  const quizState = {
    sessionId: quizSessionId.value,
    quizId: currentQuiz.value.id,
    chapitreId: route.params.chapitreId,
    currentQuestionIndex: currentQuestionIndex.value,
    userAnswers: [...userAnswers.value],
    quizStartTime: quizStartTime.value,
    currentAttempt: currentAttempt.value,
    timestamp: Date.now(),
    // Données de sécurité anti-triche
    questionsCompleted: userAnswers.value.length,
    expectedNextQuestion: currentQuestionIndex.value + 1,
    userId: userStore.id
  }
  
  try {
    localStorage.setItem(`optitab_quiz_save_${currentQuiz.value.id}`, JSON.stringify(quizState))
    lastSavedState.value = quizState
    
    // Mettre à jour la liste réactive des quiz sauvegardés
    const newSet = new Set(savedQuizzes.value)
    newSet.add(currentQuiz.value.id)
    savedQuizzesSet.value = newSet
    
    // Nettoyer le cache de progression pour forcer une mise à jour
    progressInfoCache.delete(currentQuiz.value.id)
    
    console.log(`💾 État du quiz sauvegardé - Question ${currentQuestionIndex.value + 1}`)
    console.log(`💾 Quiz ${currentQuiz.value.id} ajouté aux quiz sauvegardés`)
    console.log(`💾 Total des quiz sauvegardés: ${savedQuizzes.value.size}`)
  } catch (error) {
    console.error('❌ Erreur lors de la sauvegarde:', error)
  }
}

// Restaurer l'état du quiz depuis la sauvegarde
function restoreQuizState(quizData) {
  try {
    const savedStateJson = localStorage.getItem(`optitab_quiz_save_${quizData.id}`)
    if (!savedStateJson) return false
    
    let savedState = JSON.parse(savedStateJson)
    
    // Vérifications de sécurité anti-triche (optimisées)
    if (!isValidSavedState(savedState, quizData)) {
      console.warn('⚠️ État sauvegardé invalide - Tentative de récupération')
      
      // Tentative de récupération : corriger l'index de question si possible
      const totalQuestions = quizData.questions?.length || 0
      const correctedState = { ...savedState }
      
      // Stratégie de récupération plus intelligente
      const answeredQuestions = savedState.userAnswers.length
      
      // Cas 1: Index dépasse le nombre de questions
      if (savedState.currentQuestionIndex >= totalQuestions) {
        correctedState.currentQuestionIndex = Math.min(answeredQuestions, totalQuestions - 1)
        console.log('🔧 Index de question corrigé (hors limites):', savedState.currentQuestionIndex, '→', correctedState.currentQuestionIndex)
      }
      // Cas 2: Index en retard par rapport aux réponses (utilisateur a répondu plus que l'index ne l'indique)
      else if (savedState.currentQuestionIndex < answeredQuestions) {
        correctedState.currentQuestionIndex = answeredQuestions
        console.log('🔧 Index de question corrigé (en retard):', savedState.currentQuestionIndex, '→', correctedState.currentQuestionIndex)
      }
      // Cas 3: Index trop en avance (plus de 1 question d'écart)
      else if (savedState.currentQuestionIndex > answeredQuestions + 1) {
        correctedState.currentQuestionIndex = answeredQuestions
        console.log('🔧 Index de question corrigé (en avance):', savedState.currentQuestionIndex, '→', correctedState.currentQuestionIndex)
      }
      
      // Vérifier si l'état corrigé est valide
      if (isValidSavedState(correctedState, quizData)) {
        console.log('✅ État récupéré avec succès')
        savedState = correctedState
        // Sauvegarder l'état corrigé
        localStorage.setItem(`optitab_quiz_save_${quizData.id}`, JSON.stringify(correctedState))
      } else {
        console.warn('⚠️ Impossible de récupérer l\'état - Suppression pour sécurité')
        clearQuizSave(quizData.id)
        // Nettoyer aussi les autres sauvegardes potentiellement corrompues
        cleanupCorruptedSaves()
        return false
      }
    }
    
    // Vérifier si la sauvegarde n'est pas trop ancienne (1 heure max)
    const maxAge = 60 * 60 * 1000 // 1 heure en millisecondes
    if (Date.now() - savedState.timestamp > maxAge) {
      console.warn('⚠️ Sauvegarde expirée - Nettoyage')
      clearQuizSave(quizData.id)
      return false
    }
    
    
    // LOGIQUE DE RESTAURATION
    // Règle demandée:
    // - Tentative 1 → on saute la question courante (reprendre à la suivante)
    // - Tentatives > 1 → on reprend exactement à la même question
    const totalQuestions = quizData.questions?.length || 0
    const attemptNumber = Number(savedState.currentAttempt) || 1
    const skipCurrentQuestion = attemptNumber <= 1
    
    // VÉRIFICATION SPÉCIALE POUR LA DERNIÈRE QUESTION
    // Si l'utilisateur était sur la dernière question ou l'a dépassée, afficher directement les résultats
    const wasOnLastQuestion = savedState.currentQuestionIndex >= totalQuestions - 1
    const hasCompletedAllQuestions = savedState.userAnswers.length >= totalQuestions
    
    // Considérer le quiz comme terminé UNIQUEMENT si toutes les questions ont été répondues
    if (hasCompletedAllQuestions) {
      console.log('🎯 Quiz terminé - Affichage des résultats')
      
      // Restaurer les réponses précédentes
      userAnswers.value = [...savedState.userAnswers]
      quizStartTime.value = savedState.quizStartTime
      currentAttempt.value = savedState.currentAttempt
      
      // Calculer le score et afficher les résultats
      showResults.value = true
      quizResultSubmitted.value = false
      
      // Nettoyer la sauvegarde car le quiz est terminé
      clearQuizSave(quizData.id)
      
      return true
    }
    
    // Calculer la prochaine question en fonction de l'avancement réel et de la tentative
    const lastQuestionIndex = totalQuestions > 0 ? totalQuestions - 1 : 0
    let rawResumeIndex = 0
    if (totalQuestions > 0) {
      if (skipCurrentQuestion) {
        // Tentative 1: saute la question courante
        rawResumeIndex = Math.min(Math.max(savedState.currentQuestionIndex + 1, 0), lastQuestionIndex)
      } else {
        // Tentatives > 1: reste sur la même question
        rawResumeIndex = Math.min(Math.max(savedState.currentQuestionIndex, 0), lastQuestionIndex)
      }
    }
    // Ne jamais revenir en arrière par rapport aux questions déjà répondues
    const answeredQuestions = savedState.userAnswers.length
    const safeResumeIndex = Math.max(rawResumeIndex, Math.min(answeredQuestions, lastQuestionIndex))
    const clampedResumeIndex = totalQuestions > 0
      ? Math.min(Math.max(safeResumeIndex, 0), lastQuestionIndex)
      : 0
    const resumeQuestionNumber = totalQuestions === 0
      ? 0
      : Math.min(clampedResumeIndex + 1, totalQuestions)
    
    // Restaurer l'état en reprenant sur la bonne question
    quizSessionId.value = savedState.sessionId
    currentQuestionIndex.value = clampedResumeIndex
    userAnswers.value = [...savedState.userAnswers]
    quizStartTime.value = savedState.quizStartTime
    currentAttempt.value = savedState.currentAttempt
    lastSavedState.value = {
      ...savedState,
      currentQuestionIndex: clampedResumeIndex
    }
    
    console.log(`🔄 État du quiz restauré - Reprise à la question ${resumeQuestionNumber}`)
    console.log(`📊 Réponses précédentes: ${userAnswers.value.length}`)
    
    return true
  } catch (error) {
    console.error('❌ Erreur lors de la restauration:', error)
    return false
  }
}
function isValidSavedState(savedState, quizData) {
  // Vérifications rapides en premier
  if (savedState.userId !== userStore.id) {
    console.warn('⚠️ Utilisateur différent détecté')
    return false
  }
  
  if (savedState.quizId !== quizData.id) {
    console.warn('⚠️ Quiz ID différent')
    return false
  }
  
  // Vérifier la cohérence des réponses sauvegardées
  if (savedState.userAnswers && Array.isArray(savedState.userAnswers)) {
    // Vérifier que chaque réponse a un index de question valide
    for (const answer of savedState.userAnswers) {
      if (answer.questionIndex < 0 || answer.questionIndex >= quizData.questions.length) {
        console.warn('⚠️ Réponse avec index de question invalide')
        return false
      }
    }
  } else {
    console.warn('⚠️ userAnswers invalide ou manquant')
    return false
  }
  
  // Vérifier la cohérence du nombre de questions complétées
  if (savedState.questionsCompleted !== savedState.userAnswers.length) {
    console.warn('⚠️ Incohérence dans le nombre de questions')
    return false
  }
  
  // Vérifier que l'index ne dépasse pas le nombre total de questions
  if (savedState.currentQuestionIndex >= quizData.questions.length) {
    console.warn('⚠️ Index de question hors limites')
    return false
  }
  
  // Vérifier que l'index de question est cohérent (plus flexible)
  const totalQuestions = quizData.questions?.length || 0
  const expectedIndex = savedState.userAnswers.length
  
  // Cas légitimes pour l'index de question :
  // 1. Index normal : currentQuestionIndex = userAnswers.length (question suivante à répondre)
  // 2. Question non répondue par timeout : currentQuestionIndex = userAnswers.length (même position)
  // 3. Quiz terminé : currentQuestionIndex peut être >= totalQuestions - 1
  // 4. Dernière question : currentQuestionIndex peut être totalQuestions - 1
  
  // Vérifications de base
  if (savedState.currentQuestionIndex < 0) {
    console.warn('⚠️ Index de question négatif')
    return false
  }
  
  if (savedState.currentQuestionIndex > totalQuestions) {
    console.warn('⚠️ Index de question dépasse le nombre total de questions')
    return false
  }
  
  // Tolérance: un écart peut survenir (navigation/timeout). On normalisera lors de la reprise
  const indexDiff = Math.abs(savedState.currentQuestionIndex - expectedIndex)
  if (indexDiff > 1 && savedState.currentQuestionIndex < totalQuestions - 1) {
    console.info('ℹ️ Index de question incohérent - normalisation automatique à la reprise')
    // Ne pas invalider: la restauration fera un clamp sûr pour éviter de revenir en arrière
  }
  
  console.log('✅ État sauvegardé valide')
  return true
}

// Nettoyer la sauvegarde
function clearQuizSave(quizId) {
  try {
    localStorage.removeItem(`optitab_quiz_save_${quizId}`)
    lastSavedState.value = null
    
    // Retirer le quiz de la liste des quiz sauvegardés (réactif)
    const newSet = new Set(savedQuizzes.value)
    newSet.delete(quizId)
    savedQuizzesSet.value = newSet
    
    // Nettoyer le cache de progression
    progressInfoCache.delete(quizId)
    
    console.log('🧹 Sauvegarde nettoyée')
  } catch (error) {
    console.error('❌ Erreur lors du nettoyage:', error)
  }
}

// Nettoyer automatiquement les sauvegardes corrompues
function cleanupCorruptedSaves() {
  try {
    console.log('🧹 Nettoyage des sauvegardes corrompues...')
    
    // Parcourir toutes les clés de localStorage
    for (let i = localStorage.length - 1; i >= 0; i--) {
      const key = localStorage.key(i)
      if (key && key.startsWith('optitab_quiz_save_')) {
        try {
          const savedStateJson = localStorage.getItem(key)
          if (!savedStateJson) continue
          
          const savedState = JSON.parse(savedStateJson)
          
          // Vérifier si l'état est basique valide (sans vérifier les questions spécifiques)
          if (!savedState.userId || !savedState.quizId || !savedState.userAnswers || !Array.isArray(savedState.userAnswers)) {
            console.log('🗑️ Suppression sauvegarde corrompue:', key)
            localStorage.removeItem(key)
            continue
          }
          
          // Vérifier l'âge de la sauvegarde (plus de 24h = corrompue)
          const maxAge = 24 * 60 * 60 * 1000 // 24 heures
          if (!savedState.timestamp || (Date.now() - savedState.timestamp > maxAge)) {
            console.log('🗑️ Suppression sauvegarde expirée:', key)
            localStorage.removeItem(key)
          }
          
        } catch (error) {
          // Si on ne peut pas parser la sauvegarde, la supprimer
          console.log('🗑️ Suppression sauvegarde non-parseable:', key)
          localStorage.removeItem(key)
        }
      }
    }
    
    console.log('✅ Nettoyage terminé')
  } catch (error) {
    console.error('❌ Erreur lors du nettoyage automatique:', error)
  }
}

// Détecter les tentatives de triche (saut de question)
function detectCheating() {
  if (!lastSavedState.value) return false
  
  // Si l'utilisateur essaie de sauter des questions
  if (currentQuestionIndex.value > lastSavedState.value.expectedNextQuestion) {
    console.warn('🚨 Tentative de triche détectée - Saut de question')
    return true
  }
  
  // Si le nombre de réponses ne correspond pas
  if (userAnswers.value.length < lastSavedState.value.questionsCompleted) {
    console.warn('🚨 Tentative de triche détectée - Réponses manquantes')
    return true
  }
  
  // Si l'index de question dépasse le nombre total de questions
  if (currentQuestionIndex.value >= currentQuiz.value.questions.length) {
    console.warn('🚨 Tentative de triche détectée - Index de question invalide')
    return true
  }
  
  return false
}

// Vérifier si un quiz a une sauvegarde active (optimisée pour la performance)
function hasSavedProgress(quizId) {
  try {
    const savedStateJson = localStorage.getItem(`optitab_quiz_save_${quizId}`)
    if (!savedStateJson) return false
    
    const savedState = JSON.parse(savedStateJson)
    
    // Vérification rapide de l'expiration (1 heure)
    if (Date.now() - savedState.timestamp > 3600000) return false
    
    // Vérification rapide de l'utilisateur
    if (savedState.userId !== userStore.id) return false
    
    // Vérification rapide de la progression
    // Un quiz est considéré comme sauvegardé dès qu'il a été démarré
    // (même sans réponse, dès que currentQuestionIndex >= 0)
    return savedState.currentQuestionIndex >= 0
  } catch (error) {
    return false // Retourner false silencieusement pour la performance
  }
}

// Watcher pour les quiz sauvegardés (affichage badge onglet)
watch(savedQuizzes, (newSavedQuizzes, oldSavedQuizzes) => {
  if (newSavedQuizzes.size !== oldSavedQuizzes.size) {
    console.log('🔄 Quiz sauvegardés mis à jour:', {
      avant: oldSavedQuizzes.size,
      apres: newSavedQuizzes.size
    })
  }
}, { deep: true })

// Optimisation: Préchargement des quiz sauvegardés
const preloadSavedQuizzes = () => {
  // Déclencher une mise à jour réactive
  nextTick(() => {
    // Forcer la mise à jour du computed
    if (quiz.value.length > 0) {
      console.log('⚡ Préchargement des quiz sauvegardés...')
      refreshSavedQuizzes()
    }
  })
}

// Obtenir les informations de progression d'un quiz sauvegardé (optimisé avec cache)
const progressInfoCache = new Map()

function getSavedProgressInfo(quizId) {
  // Vérifier le cache en premier
  if (progressInfoCache.has(quizId)) {
    const cached = progressInfoCache.get(quizId)
    // Cache valide pendant 5 secondes
    if (Date.now() - cached.timestamp < 5000) {
      return cached.data
    }
  }
  
  try {
    const savedStateJson = localStorage.getItem(`optitab_quiz_save_${quizId}`)
    if (!savedStateJson) return null
    
    const savedState = JSON.parse(savedStateJson)
    
    // Calculer la progression
    const totalQuestions = quiz.value.find(q => q.id === quizId)?.questions?.length || 0
    const attemptNumber = Number(savedState.currentAttempt) || 1
    const skipCurrentQuestion = attemptNumber <= 1
    
    // Vérifier si la question actuelle a été répondue (utile pour indiquer perte de question en tentative 1)
    const hasAnsweredCurrentQuestion = savedState.userAnswers.some(answer => answer.questionIndex === savedState.currentQuestionIndex)
    const questionLeftNumber = totalQuestions > 0 ? Math.min(savedState.currentQuestionIndex + 1, totalQuestions) : 0
    
    const lastQuestionIndex = totalQuestions > 0 ? totalQuestions - 1 : 0
    let rawResumeIndex = 0
    
    if (totalQuestions > 0) {
      if (skipCurrentQuestion) {
        // Tentative 1: saute la question courante
        rawResumeIndex = Math.min(Math.max(savedState.currentQuestionIndex + 1, 0), lastQuestionIndex)
      } else {
        // Tentatives > 1: reprend exactement à la même question
        rawResumeIndex = Math.min(Math.max(savedState.currentQuestionIndex, 0), lastQuestionIndex)
      }
    }
    
    const resumeQuestionIndex = totalQuestions > 0 ? rawResumeIndex : 0
    const resumeQuestionNumber = totalQuestions === 0
      ? 0
      : Math.min(resumeQuestionIndex + 1, totalQuestions)
    // Perte de question uniquement en tentative 1 quand on n'a pas répondu
    const questionLost = skipCurrentQuestion && !hasAnsweredCurrentQuestion && totalQuestions > 0 && savedState.currentQuestionIndex < totalQuestions
    const isFirstQuestionLost = skipCurrentQuestion && savedState.currentQuestionIndex === 0 && !hasAnsweredCurrentQuestion
    
    // Si le quiz vient d'être démarré (currentQuestionIndex = 0, pas de réponse, pas de temps écoulé)
    const isJustStarted = savedState.currentQuestionIndex === 0 && savedState.userAnswers.length === 0
    
    // VÉRIFICATION SPÉCIALE POUR LES QUIZ TERMINÉS
    const wasOnLastQuestion = savedState.currentQuestionIndex >= totalQuestions - 1
    const hasCompletedAllQuestions = savedState.userAnswers.length >= totalQuestions
    // Terminé seulement si toutes les questions ont été répondues (ne pas confondre avec "sur la dernière question")
    const isQuizCompleted = hasCompletedAllQuestions
    
    const result = {
      currentQuestion: resumeQuestionNumber,
      totalQuestions: totalQuestions,
      answersGiven: savedState.userAnswers.length,
      lastSaved: new Date(savedState.timestamp),
      progress: resumeQuestionNumber,
      questionLost: questionLost,
      lostQuestion: questionLost ? questionLeftNumber : resumeQuestionNumber,
      isFirstQuestionLost: isFirstQuestionLost, // Indicateur spécial pour la première question non répondue
      hasAnsweredCurrentQuestion: hasAnsweredCurrentQuestion, // Si l'utilisateur a répondu à la question actuelle
      isJustStarted: isJustStarted, // Si le quiz vient d'être démarré
      isQuizCompleted: isQuizCompleted // Si le quiz est terminé (dernière question)
    }
    
    // Mettre en cache le résultat
    progressInfoCache.set(quizId, {
      data: result,
      timestamp: Date.now()
    })
    
    return result
  } catch (error) {
    console.warn('Erreur lors de la récupération des infos de progression:', error)
    return null
  }
}


// Fonction pour revenir aux chapitres
function goBackToNotions() {
  // Rediriger vers quiz/id (liste des notions de quiz)
  const matiereId = route.params.matiereId || subjectsStore.activeMatiereId
  if (matiereId) {
    router.push({ 
      name: 'QuizNotions', 
      params: { 
        matiereId: matiereId
      } 
    })
  } else {
    router.back()
  }
}

// Détecter les tentatives de fermeture/rafraîchissement
function handleBeforeUnload(event) {
  if (currentQuiz.value && !showResults.value) {
    // Sauvegarder une dernière fois avant de quitter
    saveQuizState()
    
    // Afficher un message d'avertissement
    const message = 'Êtes-vous sûr de vouloir quitter ? Votre progression sera sauvegardée.'
    event.returnValue = message
    return message
  }
}

// Nettoyage des timers et event listeners
onUnmounted(() => {
  stopQuestionTimer()
  
  // Retirer les event listeners
  window.removeEventListener('beforeunload', handleBeforeUnload)
  
  // Sauvegarder une dernière fois si nécessaire
  if (currentQuiz.value && !showResults.value) {
    saveQuizState()
  }
  
  console.log('💾 Sauvegarde automatique désactivée')
})
</script>

<style scoped>
.chapter-quiz-section {
  background: #fff;
  min-height: 100vh;
  padding: 0 5vw 40px 5vw;
  text-align: center;
}

@media (max-width: 768px) {
  .chapter-quiz-section {
    padding-left: 0;
    padding-right: 0;
  }
}


.quiz-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  max-width: 100%;
  margin: 0 auto;
  align-items: stretch;
}

.quiz-card {
  background: #ffffff;
  border: 1px solid #f1f5f9;
  border-radius: 16px;
  padding: 0.75rem; /* compact and consistent */
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  width: 100%;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  gap: 0.35rem; /* tighter spacing inside */
  min-height: 88px; /* target compact height */
  height: 88px; /* enforce strict equal height across states */
  overflow: hidden; /* prevent growth from nested content */
}

.quiz-card:hover {
  border-color: #3b82f6 !important;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.quiz-card.completed {
  border-color: #f1f5f9;
  background: #ffffff;
}


.quiz-card.saved-progress {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border-color: #0ea5e9;
  border-left: 4px solid #0ea5e9;
}

.quiz-card.saved-progress:hover {
  border-color: #0284c7;
  box-shadow: 0 8px 25px rgba(14, 165, 233, 0.2);
}

.quiz-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start; /* keep right meta aligned to top */
  gap: 0.6rem;
  margin-bottom: 0.05rem;
}

.quiz-title-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

.quiz-icon {
  font-size: 1.25rem;
  color: #65a30d;
}

.quiz-card-title {
  font-size: 0.92rem; /* slightly smaller */
  font-weight: 700;
  color: #0f172a;
  margin: 0;
  line-height: 1.25;
  text-align: left;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.quiz-difficulty-stars {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #fbbf24;
  font-size: 1rem;
}

.star {
  font-size: 1rem;
  color: currentColor;
}

.star.empty {
  color: #d1d5db;
}

.quiz-card-description {
  color: #64748b;
  margin: 0;
  line-height: 1.25;
  font-size: 0.75rem; /* 12px */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.quiz-card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: nowrap; /* keep on one line */
  font-size: 0.75rem; /* slightly smaller */
  color: #64748b;
  gap: 0.35rem;
  margin-top: 0.05rem;
  min-height: 22px; /* anchor height for badges line */
}

/* Compact badges for attempts/score if present */
.attempt-badge, .score-badge, .quiz-stats-badge, .quiz-continue-badge {
  display: inline-flex;
  align-items: center;
  height: 20px;
  line-height: 20px;
  padding: 0 8px;
  font-size: 0.7rem;
  border-radius: 10px;
}

.quiz-card-meta-right, .quiz-stats, .quiz-meta-right {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  flex-wrap: nowrap;
}

.quiz-interface {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  border: 1px solid #e2e8f0;
}

.quiz-progress {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.progress-bar {
  flex: 1;
  height: 0.5rem;
  background: #e2e8f0;
  border-radius: 0.25rem;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #3b82f6;
  transition: width 0.3s ease;
}

.progress-text {
  font-weight: 600;
  color: #3b82f6;
  min-width: 4rem;
}

.question-container {
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
}

.question-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 2rem 0;
  line-height: 1.4;
  width: 100%;
  max-width: 100%;
}

.options-container {
  display: grid;
  gap: 1rem;
  margin-bottom: 2rem;
  width: 100%;
  max-width: 100%;
}

.option-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  max-width: 100%;
}

.option-card:hover {
  border-color: #3b82f6;
}

.option-card.selected {
  border-color: #3b82f6;
  background: #eff6ff;
}

.option-card.correct {
  border-color: #10b981;
  background: #d1fae5;
}

.option-card.correct .option-text {
  color: #065f46;
  font-weight: 600;
}

.option-card.incorrect {
  border-color: #ef4444;
  background: #fee2e2;
}

.option-card.disabled {
  background: #f8fafc;
  border-color: #e2e8f0;
  color: #9ca3af;
  cursor: not-allowed;
  opacity: 0.6;
}

.option-card.disabled .option-letter {
  background: #e2e8f0;
  color: #9ca3af;
}

.option-card.disabled:hover {
  transform: none;
  box-shadow: none;
  border-color: #e2e8f0;
}

.option-letter {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #374151;
  flex-shrink: 0;
}

.option-card.selected .option-letter {
  background: #3b82f6;
  color: white;
}

.option-card.correct .option-letter {
  background: #10b981;
  color: white;
}

.option-card.incorrect .option-letter {
  background: #ef4444;
  color: white;
}

.option-text {
  flex: 1;
  font-size: 1rem;
  line-height: 1.4;
}

.explanation {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 0.75rem;
  margin-bottom: 2rem;
  border-left: 4px solid #3b82f6;
}

.explanation-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.explanation-text {
  color: #475569;
  line-height: 1.5;
  margin: 0;
  text-align: left;
}

.quiz-actions, .answer-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.btn-primary, .btn-success, .btn-secondary {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.btn-success {
  background: #10b981;
  color: white;
}

.btn-success:hover {
  background: #059669;
}

.btn-secondary {
  background: #f8fafc;
  color: #374151;
  border: 1px solid #e2e8f0;
}

.btn-secondary:hover {
  background: #f1f5f9;
}

.quiz-results {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  border: 1px solid #e2e8f0;
  text-align: center;
}

.results-header {
  margin-bottom: 2rem;
}

.results-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 1rem 0;
}

.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  border: 8px solid;
}

.score-circle.excellent {
  border-color: #10b981;
  background: #d1fae5;
}

.score-circle.good {
  border-color: #3b82f6;
  background: #dbeafe;
}

.score-circle.average {
  border-color: #f59e0b;
  background: #fef3c7;
}

.score-circle.poor {
  border-color: #ef4444;
  background: #fee2e2;
}

.score-percentage {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
}

.results-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 0.5rem;
  text-align: center;
}

.stat-card.gamification {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border: 1px solid #0ea5e9;
}


.stat-number {
  display: block;
  font-size: 2rem;
  font-weight: 700;
  color: #3b82f6;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
}



.results-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

@media (max-width: 768px) {
  .chapter-quiz-section {
    padding: 0 3vw 30px 3vw;
  }


  .question-title {
    font-size: 1.25rem;
  }

  .results-actions, .quiz-actions {
    flex-direction: column;
  }

  .score-circle {
    width: 100px;
    height: 100px;
  }

  .score-percentage {
    font-size: 1.5rem;
  }
}

/* Gamification Styles */
.gamification-results {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border: 2px solid #22c55e;
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
  text-align: center;
}

.xp-earned {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.xp-earned.no-xp {
  opacity: 0.7;
}

.xp-earned.no-xp .xp-icon {
  filter: grayscale(50%);
}

.xp-icon {
  font-size: 3rem;
  flex-shrink: 0;
}

.xp-details {
  text-align: left;
}

.xp-amount {
  font-size: 1.5rem;
  font-weight: 800;
  color: #16a34a;
  margin-bottom: 0.25rem;
}

.xp-earned.no-xp .xp-amount {
  color: #64748b;
}

.xp-info {
  font-size: 0.875rem;
  color: #15803d;
  font-weight: 600;
}

.xp-earned.no-xp .xp-info {
  color: #64748b;
}

.level-up-display {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border: 2px solid #f59e0b;
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  animation: pulse 2s infinite;
}

.level-up-icon {
  font-size: 2rem;
}

.level-up-text {
  font-size: 1.125rem;
  font-weight: 700;
  color: #92400e;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.02);
  }
}


/* Navigation onglets */
.clean-navigation {
  margin: 2rem 0;
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.4rem;
  width: 100%;
  margin: 0 auto;
}

.nav-item {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  min-width: 100px;
  text-align: center;
  font-weight: 500;
  color: #6b7280;
}

.nav-item:hover {
  border-color: #3b82f6;
  background: #f8fafc;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-item.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.nav-icon {
  font-size: 1.1rem;
  flex-shrink: 0;
}

.nav-label {
  font-size: 0.875rem;
  font-weight: 600;
  flex-grow: 1;
  text-align: left;
  margin-left: 0.5rem;
}

.nav-count {
  font-size: 0.75rem;
  font-weight: 700;
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  padding: 0.125rem 0.5rem;
  border-radius: 10px;
  min-width: 20px;
  text-align: center;
}

.nav-item.active .nav-count {
  background: rgba(255, 255, 255, 0.25);
  color: white;
}

/* Animation de chargement pour l'onglet "À continuer" */
.nav-count.loading {
  position: relative;
  animation: pulse-loading 1.5s ease-in-out infinite;
}

.nav-count.loading::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 12px;
  height: 12px;
  background: #3b82f6;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: loading-spin 1s linear infinite;
}

@keyframes pulse-loading {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

@keyframes loading-spin {
  from { transform: translate(-50%, -50%) rotate(0deg); }
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

/* Quiz status container */
.quiz-status-container {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  width: 100%;
}

.quiz-status-saved {
  width: 100%;
  align-self: stretch;
}

.quiz-status-completed {
  width: auto;
  align-self: flex-end;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-left: auto;
}

/* Container des infos à droite (tentative + note) */
.quiz-right-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
  min-width: 0;
}

/* Quiz attempts (à gauche) */
.quiz-attempts {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 0.75rem;
  background: #f8fafc;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.quiz-attempts:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.attempts-label {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
}

.attempts-number {
  font-size: 0.875rem;
  font-weight: 700;
  color: #334155;
  background: #e2e8f0;
  padding: 0.125rem 0.375rem;
  border-radius: 6px;
  min-width: 1.25rem;
  text-align: center;
}

/* Quiz score (à droite) */
.quiz-score {
  padding: 0.5rem 0.75rem;
  border-radius: 10px;
  border: 1px solid;
  transition: all 0.2s ease;
  min-width: 70px;
  text-align: center;
  flex-shrink: 0;
  position: relative;
  overflow: hidden;
}

.quiz-score::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  transition: left 0.5s ease;
}

.quiz-score:hover::before {
  left: 100%;
}

/* Couleurs selon la note */
.quiz-score.score-above-average {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-color: #bbf7d0;
  color: #166534;
  box-shadow: 0 2px 4px rgba(34, 197, 94, 0.08);
}

.quiz-score.score-average {
  background: linear-gradient(135deg, #fffbeb 0%, #fed7aa 100%);
  border-color: #fed7aa;
  color: #92400e;
  box-shadow: 0 2px 4px rgba(245, 158, 11, 0.08);
}

.quiz-score.score-below-average {
  background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
  border-color: #fecaca;
  color: #991b1b;
  box-shadow: 0 2px 4px rgba(239, 68, 68, 0.08);
}

.score-value {
  font-size: 0.875rem;
  font-weight: 700;
  margin: 0;
  position: relative;
  z-index: 1;
}

/* Couleurs du texte selon la note */
.quiz-score.score-above-average .score-value {
  color: #16a34a;
}

.quiz-score.score-average .score-value {
  color: #d97706;
}

.quiz-score.score-below-average .score-value {
  color: #dc2626;
}



/* Quiz à continuer */
.quiz-progress-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: #f0f9ff;
  border: 2px solid #0ea5e9;
  border-radius: 6px;
  flex-shrink: 0;
}

.progress-icon {
  font-size: 1rem;
  animation: rotate 2s linear infinite;
}

.progress-text {
  font-size: 0.875rem;
  font-weight: 700;
  color: #0369a1;
}

.lost-question-indicator {
  font-size: 0.75rem;
  color: #dc2626;
  font-weight: 600;
  margin-left: 0.25rem;
}

.lost-question-indicator.first-question-lost {
  color: #f59e0b;
  font-weight: 700;
}

.saved-question-indicator {
  font-size: 0.75rem;
  color: #10b981;
  font-weight: 600;
  margin-left: 0.25rem;
}

.just-started-indicator {
  font-size: 0.75rem;
  color: #3b82f6;
  font-weight: 600;
  margin-left: 0.25rem;
}

.completed-indicator {
  font-size: 0.75rem;
  color: #3b82f6;
  font-weight: 600;
  margin-left: 0.25rem;
  background: rgba(59, 130, 246, 0.1);
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  border: 1px solid rgba(59, 130, 246, 0.2);
}

.quiz-saved-time {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: #f8fafc;
  border-radius: 6px;
  border: 2px solid #e2e8f0;
  flex-shrink: 0;
}

.saved-label {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 600;
}

.saved-time {
  font-size: 0.8rem;
  font-weight: 700;
  color: #475569;
}

.quiz-continue-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border-radius: 6px;
  transition: all 0.2s ease;
  min-width: 100px;
  text-align: center;
  flex-shrink: 0;
  white-space: nowrap;
}

.continue-text {
  font-size: 0.875rem;
  font-weight: 600;
}

.continue-arrow {
  font-size: 1rem;
  transition: transform 0.2s ease;
}

.quiz-card:hover .quiz-continue-badge {
  transform: translateX(2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.quiz-card:hover .continue-arrow {
  transform: translateX(2px);
}

.quiz-continue-badge.completed {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.quiz-continue-badge.completed:hover {
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Message vide */
.no-quiz-message {
  text-align: center;
  padding: 3rem 2rem;
  background: #f8fafc;
  border-radius: 1rem;
  border: 2px dashed #cbd5e1;
}

.no-quiz-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.no-quiz-message h3 {
  color: #475569;
  margin-bottom: 0.5rem;
}

.no-quiz-message p {
  color: #64748b;
  font-size: 0.875rem;
}

/* Message de temps écoulé */
.timeout-message {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  border: 2px solid #fca5a5;
  border-radius: 12px;
  padding: 1rem;
  margin: 1rem 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  animation: timeout-pulse 1s ease-in-out infinite alternate;
}

.timeout-icon {
  font-size: 1.5rem;
  animation: timeout-shake 0.5s ease-in-out infinite;
}

.timeout-text {
  margin: 0;
  color: #dc2626;
  font-weight: 600;
  font-size: 0.95rem;
}

@keyframes timeout-pulse {
  from {
    background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  }
  to {
    background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  }
}

@keyframes timeout-shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-2px); }
  75% { transform: translateX(2px); }
}

/* Timer par question */
.question-timer {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.timer-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.timer-label {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 600;
}

.timer-time {
  font-size: 1.25rem;
  font-weight: 700;
  color: #10b981;
  transition: color 0.3s ease;
}

.timer-time.warning {
  color: #f59e0b;
}

.timer-time.critical {
  color: #ef4444;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.timer-bar {
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.75rem;
}

.timer-fill {
  height: 100%;
  transition: all 0.3s ease;
  border-radius: 4px;
}

.timer-fill-smooth {
  height: 100%;
  width: 100%;
  border-radius: 4px;
  animation: timer-countdown linear;
  animation-fill-mode: forwards;
}

@keyframes timer-countdown {
  from {
    width: 100%;
  }
  to {
    width: 0%;
  }
}

.timer-difficulty {
  display: flex;
  justify-content: center;
}

.difficulty-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.difficulty-badge.easy {
  background: #dcfce7;
  color: #166534;
}

.difficulty-badge.medium {
  background: #fef3c7;
  color: #92400e;
}

.difficulty-badge.hard {
  background: #fecaca;
  color: #991b1b;
}


@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Pagination */
.pagination-container {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.pagination-info {
  text-align: center;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 600;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.pagination-btn {
  padding: 0.5rem 1rem;
  background: #ffffff;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  color: #374151;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #f1f5f9;
  color: #9ca3af;
}

.pagination-numbers {
  display: flex;
  gap: 0.5rem;
}

.pagination-number {
  width: 40px;
  height: 40px;
  border: 2px solid #e2e8f0;
  background: #ffffff;
  border-radius: 8px;
  color: #374151;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pagination-number:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.pagination-number.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

/* Responsive pour gamification */
@media (max-width: 680px) {
  .chapter-quiz-section {
    padding: 0 2vw 20px 2vw;
  }
}

@media (max-width: 640px) {
  .xp-earned {
    flex-direction: column;
    text-align: center;
  }
  
  .xp-details {
    text-align: center;
  }
  
  .gamification-results {
    padding: 1rem;
  }
  
  .xp-icon {
    font-size: 2.5rem;
  }
  
  .nav-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.3rem;
    width: 100%;
  }
  
  .nav-item {
    padding: 0.4rem 0.4rem;
    min-height: 45px;
  }
  
  .nav-label {
    font-size: 0.75rem;
  }

  .question-timer {
    padding: 0.75rem;
    margin-bottom: 1rem;
  }
  
  .timer-info {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
  
  .timer-time {
    font-size: 1.5rem;
  }

  .quiz-status-container {
    flex-direction: column;
    gap: 0.5rem;
    align-items: stretch;
  }

  .quiz-right-info {
    justify-content: center;
    flex-direction: column;
    gap: 0.5rem;
  }

  .quiz-attempts {
    justify-content: center;
  }

  .quiz-score {
    align-self: center;
    min-width: 100px;
  }

}

@media (max-width: 360px) {
  .nav-grid {
    grid-template-columns: 1fr;
    gap: 0.3rem;
    width: 100%;
  }
  
  .nav-item {
    padding: 0.4rem 0.6rem;
    min-height: 40px;
  }

  .pagination-controls {
    flex-direction: column;
    gap: 1rem;
  }

  .pagination-numbers {
    justify-content: center;
    flex-wrap: wrap;
  }

  .pagination-btn {
    width: 100%;
    max-width: 200px;
  }
}
</style> 
