import { ref, computed, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { updateUserXP } from '@/api/users'

// État partagé (singleton) pour les stats d'objectifs (quiz et exercices)
const sharedUserStats = ref({
  quizEasy: 0,
  quizMedium: 0,
  quizHard: 0,
  quizPerfect: 0,
  exercicesCompleted: 0
})

// Indicateur global d'initialisation pour éviter les faux "tous terminés" au chargement
const sharedIsInitialized = ref(false)

// État partagé des objectifs débloqués pour conserver la progression entre les pages
const sharedUnlockedObjectives = ref([])

let objectivesInitialized = false

// Composable pour gérer les objectifs journaliers
export function useDailyObjectives() {
  const userStore = useUserStore()
  
  // Utiliser l'état partagé pour que toutes les pages voient la même progression
  const userStats = sharedUserStats

  // Définition des objectifs journaliers (quiz et exercices)
  const objectiveTypes = {
    quiz_easy: {
      icon: '🟢',
      getText: (target) => `Réussir ${target} quiz simples`,
      xpReward: 3,
      getProgress: () => userStats.value.quizEasy
    },
    quiz_medium: {
      icon: '🟡',
      getText: (target) => `Réussir ${target} quiz moyens`,
      xpReward: 5,
      getProgress: () => userStats.value.quizMedium
    },
    quiz_hard: {
      icon: '🔴',
      getText: (target) => `Réussir ${target} quiz difficiles`,
      xpReward: 8,
      getProgress: () => userStats.value.quizHard
    },
    quiz_perfect: {
      icon: '🎯',
      getText: (target) => `Obtenir 100% sur ${target} quiz`,
      xpReward: 9,
      getProgress: () => userStats.value.quizPerfect
    },
    exercices_completed: {
      icon: '📚',
      getText: (target) => `Réussir ${target} exercices`,
      xpReward: 5,
      getProgress: () => userStats.value.exercicesCompleted
    }
  }

  // Mapping fiable entre type d'objectif et clé du state
  const typeToStatKey = (type) => {
    const map = {
      quiz_easy: 'quizEasy',
      quiz_medium: 'quizMedium',
      quiz_hard: 'quizHard',
      quiz_perfect: 'quizPerfect',
      exercices_completed: 'exercicesCompleted'
    }
    return map[type] || null
  }

  // Configuration des objectifs journaliers (6 défis à débloquer aléatoirement - quiz et exercices)
  const dailyObjectivesConfig = [
    { name: 'Quiz simples', type: 'quiz_easy', target: 3 },
    { name: 'Quiz moyens', type: 'quiz_medium', target: 5 },
    { name: 'Quiz difficiles', type: 'quiz_hard', target: 6 },
    { name: 'Quiz parfaits', type: 'quiz_perfect', target: 2 },
    { name: 'Exercices réussis', type: 'exercices_completed', target: 2 }
  ]

  // État des objectifs débloqués (partagé entre toutes les instances)
  const unlockedObjectives = sharedUnlockedObjectives

  // Initialiser les objectifs débloqués
  const initializeUnlockedObjectives = () => {
    const today = new Date().toDateString()
    const saved = localStorage.getItem(`unlocked_objectives_${today}`)

    if (saved) {
      let savedObjectives = JSON.parse(saved)
      // Filtrer les index invalides (anciens objectifs supprimés)
      savedObjectives = savedObjectives.filter(index => 
        index >= 0 && index < dailyObjectivesConfig.length
      )
      
      if (savedObjectives.length > 0) {
        unlockedObjectives.value = savedObjectives
        console.log(`🎯 [DailyObjectives] Objectifs chargés (nettoyés):`, unlockedObjectives.value)
      } else {
        // Si tous les objectifs sauvegardés sont invalides, recommencer
        const randomIndex = Math.floor(Math.random() * dailyObjectivesConfig.length)
        unlockedObjectives.value = [randomIndex]
        console.log(`🎯 [DailyObjectives] Objectifs invalides supprimés, nouveau départ:`, randomIndex)
      }
      
      // Sauvegarder les objectifs nettoyés
      saveUnlockedObjectives()
    } else {
      // Commencer avec un objectif aléatoire
      const randomIndex = Math.floor(Math.random() * dailyObjectivesConfig.length)
      unlockedObjectives.value = [randomIndex]
      saveUnlockedObjectives()
      console.log(`🎯 [DailyObjectives] Premier objectif débloqué:`, randomIndex, dailyObjectivesConfig[randomIndex].name)
    }
  }

  // Sauvegarder les objectifs débloqués
  const saveUnlockedObjectives = () => {
    const today = new Date().toDateString()
    localStorage.setItem(`unlocked_objectives_${today}`, JSON.stringify(unlockedObjectives.value))
    console.log(`🎯 [DailyObjectives] Objectifs sauvegardés:`, unlockedObjectives.value)
  }

  // Débloquer le prochain objectif dans l'ordre (pas aléatoire)
  const unlockNextObjective = () => {
    const allIndices = Array.from({ length: dailyObjectivesConfig.length }, (_, i) => i)
    const availableIndices = allIndices.filter(i => !unlockedObjectives.value.includes(i))

    if (availableIndices.length > 0) {
      // Prendre le premier objectif disponible (ordre séquentiel)
      const nextIndex = availableIndices[0]
      unlockedObjectives.value.push(nextIndex)
      saveUnlockedObjectives()
      console.log(`🎯 [DailyObjectives] Nouvel objectif débloqué (séquentiel):`, nextIndex, dailyObjectivesConfig[nextIndex].name)
      
      // Émettre un événement pour notifier le déblocage
      window.dispatchEvent(new CustomEvent('objectiveUnlocked', {
        detail: { 
          objective: dailyObjectivesConfig[nextIndex],
          index: nextIndex
        }
      }))
    } else {
      console.log(`🎯 [DailyObjectives] Tous les objectifs sont déjà débloqués !`)
    }
  }

  // Objectifs débloqués seulement
  const unlockedObjectivesList = computed(() => {
    return unlockedObjectives.value
      .filter(index => index < dailyObjectivesConfig.length) // Filtrer les index invalides
      .map(index => {
        const config = dailyObjectivesConfig[index]
        const type = objectiveTypes[config.type]
        
        // Vérifications de sécurité
        if (!config || !type) {
          console.warn(`🎯 [DailyObjectives] Configuration invalide pour l'index ${index}`)
          return null
        }
        
        const progress = type.getProgress()

        return {
          index,
          name: config.name,
          type: config.type,
          target: config.target,
          xpReward: type.xpReward,
          icon: type.icon,
          text: type.getText(config.target),
          progress,
          isCompleted: progress >= config.target,
          percentage: Math.min((progress / config.target) * 100, 100)
        }
      })
      .filter(obj => obj !== null) // Supprimer les objets invalides
  })

  // Objectif actuel (le premier non complété parmi les débloqués)
  const currentObjective = computed(() => {
    // Ne pas retourner d'objectif tant que l'init n'est pas terminée
    if (!sharedIsInitialized.value) return null

    const objectives = unlockedObjectivesList.value
    if (objectives.length === 0) return null

    // Chercher le premier objectif non complété
    const incomplete = objectives.find(obj => !obj.isCompleted)
    
    if (incomplete) {
      return incomplete
    }
    
    // Si tous les objectifs débloqués sont complétés, débloquer automatiquement un nouveau
    const availableIndices = Array.from({ length: dailyObjectivesConfig.length }, (_, i) => i)
      .filter(i => !unlockedObjectives.value.includes(i))
    
    if (availableIndices.length > 0) {
      // Débloquer le prochain objectif disponible (pas aléatoire)
      const nextIndex = availableIndices[0]
      console.log(`🎯 [DailyObjectives] Auto-déblocage objectif ${nextIndex}`)
      unlockedObjectives.value.push(nextIndex)
      saveUnlockedObjectives()
      
      // Retourner le nouvel objectif débloqué
      const config = dailyObjectivesConfig[nextIndex]
      const type = objectiveTypes[config.type]
      const statKey = typeToStatKey(config.type)
      const progress = statKey ? userStats.value[statKey] : 0
      
      return {
        ...config,
        ...type,
        progress,
        isCompleted: progress >= config.target,
        isUnlocked: true
      }
    }
    
    // Si tous les objectifs sont débloqués et complétés
    return null
  })

  // Tous les objectifs avec leur statut (pour le modal)
  const allObjectives = computed(() => {
    return dailyObjectivesConfig.map((config, index) => {
      const isUnlocked = unlockedObjectives.value.includes(index)
      const type = objectiveTypes[config.type]
      
      // Vérifications de sécurité
      if (!config || !type) {
        console.warn(`🎯 [DailyObjectives] Configuration invalide pour l'index ${index}`)
        return null
      }
      
      const progress = isUnlocked ? type.getProgress() : 0

      return {
        index,
        name: config.name,
        type: config.type,
        target: config.target,
        xpReward: type.xpReward,
        icon: type.icon,
        text: type.getText(config.target),
        progress,
        isCompleted: isUnlocked && progress >= config.target,
        isUnlocked,
        percentage: isUnlocked ? Math.min((progress / config.target) * 100, 100) : 0
      }
    }).filter(obj => obj !== null) // Supprimer les objets invalides
  })

  // Clé pour localStorage basée sur la date
  const getStorageKey = (type) => {
    const today = new Date().toDateString()
    return `daily_objective_${type}_${today}`
  }

  // Charger les statistiques depuis localStorage
  const loadTodayStats = () => {
    Object.keys(objectiveTypes).forEach(type => {
      const key = getStorageKey(type)
      const saved = localStorage.getItem(key)
      const statKey = typeToStatKey(type)
      if (saved && statKey && Object.prototype.hasOwnProperty.call(userStats.value, statKey)) {
        userStats.value[statKey] = parseInt(saved, 10) || 0
      }
    })
  }

  // Sauvegarder les statistiques
  const saveStats = () => {
    Object.keys(objectiveTypes).forEach(type => {
      const key = getStorageKey(type)
      const statKey = typeToStatKey(type)
      const value = statKey ? userStats.value[statKey] : 0
      localStorage.setItem(key, String(value ?? 0))
    })
  }

  // Incrémenter une statistique
  const incrementStat = (statType, amount = 1) => {
    const statKey = typeToStatKey(statType)
    console.log(`🎯 [DailyObjectives] incrementStat appelé: ${statType} → ${statKey}`)
    
    if (statKey && Object.prototype.hasOwnProperty.call(userStats.value, statKey)) {
      const oldValue = userStats.value[statKey]
      userStats.value[statKey] += amount
      const newValue = userStats.value[statKey]
      
      console.log(`🎯 [DailyObjectives] ${statKey} mis à jour: ${oldValue} → ${newValue}`)
      
      saveStats()
      
      // Notifier le dashboard pour une mise à jour instantanée
      try {
        window.dispatchEvent(new CustomEvent('dailyObjectiveProgress', {
          detail: { type: statType, value: newValue }
        }))
        console.log(`🎯 [DailyObjectives] Événement émis pour ${statType}`)
      } catch (error) {
        console.error(`🎯 [DailyObjectives] Erreur événement:`, error)
      }
      
      // Vérifier et attribuer les récompenses après chaque mise à jour
      setTimeout(() => {
        checkAndAwardObjectives()
      }, 100)
    } else {
      console.error(`🎯 [DailyObjectives] Stat invalide: ${statType} → ${statKey}`)
      console.error(`🎯 [DailyObjectives] userStats disponibles:`, Object.keys(userStats.value))
    }
  }

  // Réinitialiser les stats du jour (si nécessaire)
  const resetDailyStats = () => {
    Object.keys(userStats.value).forEach(key => {
      userStats.value[key] = 0
    })
    saveStats()
  }

  // Vérifier si l'objectif du jour est complété
  const isDailyObjectiveCompleted = computed(() => {
    if (!currentObjective.value) return false
    return currentObjective.value.progress >= currentObjective.value.target
  })

  // Vérifier si un objectif a déjà été récompensé aujourd'hui
  const getObjectiveRewardKey = (objectiveType) => {
    const today = new Date().toDateString()
    return `daily_objective_reward_${objectiveType}_${today}`
  }

  const hasObjectiveBeenRewarded = (objectiveType) => {
    const key = getObjectiveRewardKey(objectiveType)
    return localStorage.getItem(key) === 'true'
  }

  const markObjectiveAsRewarded = (objectiveType) => {
    const key = getObjectiveRewardKey(objectiveType)
    localStorage.setItem(key, 'true')
  }

  // Attribuer les XP pour un objectif complété
  const awardObjectiveXP = async (objectiveType, xpAmount) => {
    if (hasObjectiveBeenRewarded(objectiveType)) {
      return false // Déjà récompensé aujourd'hui
    }

    console.log(`🎯 [DailyObjectives] Attribution XP: ${xpAmount} pour ${objectiveType}`)
    
    try {
      // Sauvegarder les XP dans le backend
      await updateUserXP({
        xp_delta: xpAmount,
        reason: `daily_objective:${objectiveType}`
      })
      
      // Mettre à jour le userStore local
      const oldXP = userStore.xp || 0
      userStore.xp = oldXP + xpAmount
      
      console.log(`🎯 [DailyObjectives] XP sauvegardés backend et store: ${oldXP} → ${userStore.xp}`)
      
      // Marquer comme récompensé
      markObjectiveAsRewarded(objectiveType)
      
      // Émettre un événement pour notification
      setTimeout(() => {
        console.log(`🎯 [DailyObjectives] Émission notification pour ${objectiveType}`)
        window.dispatchEvent(new CustomEvent('dailyObjectiveCompleted', {
          detail: { objectiveType, xpAmount }
        }))
      }, 500)
      
    } catch (error) {
      console.error(`🎯 [DailyObjectives] Erreur sauvegarde XP:`, error)
      
      // En cas d'erreur, mettre à jour quand même le store local
      const oldXP = userStore.xp || 0
      userStore.xp = oldXP + xpAmount
      
      // Émettre quand même la notification
      window.dispatchEvent(new CustomEvent('dailyObjectiveCompleted', {
        detail: { objectiveType, xpAmount }
      }))
    }
    
    return true // XP attribués avec succès
  }

  // Vérifier et attribuer les récompenses automatiquement
  const checkAndAwardObjectives = () => {
    let hasNewCompletion = false
    
    unlockedObjectivesList.value.forEach(objective => {
      if (objective.isCompleted && !hasObjectiveBeenRewarded(objective.type)) {
        console.log(`🎯 [DailyObjectives] Objectif complété: ${objective.name}`)
        hasNewCompletion = true
        
        // Attribuer les XP
        awardObjectiveXP(objective.type, objective.xpReward)
      }
    })
    
    // Si un objectif vient d'être complété, débloquer un nouveau après un délai
    if (hasNewCompletion) {
      setTimeout(() => {
        // Vérifier s'il reste des objectifs à débloquer
        const availableIndices = Array.from({ length: dailyObjectivesConfig.length }, (_, i) => i)
          .filter(i => !unlockedObjectives.value.includes(i))
        
        if (availableIndices.length > 0) {
          console.log(`🎯 [DailyObjectives] Déblocage d'un nouvel objectif...`)
          unlockNextObjective()
        } else {
          console.log(`🎯 [DailyObjectives] Tous les objectifs sont déjà débloqués !`)
        }
      }, 1500) // Délai pour laisser le temps à la notification de s'afficher
    }
  }

  // Obtenir la progression en pourcentage
  const getProgressPercentage = (objective) => {
    return Math.min(100, (objective.progress / objective.target) * 100)
  }

  // Simuler des événements pour tester (à supprimer en production)
  const simulateQuizEasy = () => incrementStat('quiz_easy')
  const simulateQuizMedium = () => incrementStat('quiz_medium')
  const simulateQuizHard = () => incrementStat('quiz_hard')
  const simulateQuizPerfect = () => incrementStat('quiz_perfect')
  const simulateExerciseCompleted = () => incrementStat('exercices_completed')
  // Streak d'objectifs supprimé

  // Watcher pour sauvegarder automatiquement (une fois)
  if (!objectivesInitialized) {
    loadTodayStats()
    initializeUnlockedObjectives()
    watch(userStats, saveStats, { deep: true })
    objectivesInitialized = true
    sharedIsInitialized.value = true
  }

  return {
    userStats,
    isInitialized: sharedIsInitialized,
    currentObjective,
    unlockedObjectives,
    unlockedObjectivesList,
    allObjectives,
    isDailyObjectiveCompleted,
    getProgressPercentage,
    incrementStat,
    resetDailyStats,
    loadTodayStats,
    checkAndAwardObjectives,
    awardObjectiveXP,
    hasObjectiveBeenRewarded,
    
    // Fonctions de simulation pour tests
    simulateQuizEasy,
    simulateQuizMedium,
    simulateQuizHard,
    simulateQuizPerfect,
    simulateExerciseCompleted
  }
}

// Intégration avec les vraies actions utilisateur
export function useDailyObjectivesIntegration() {
  const { incrementStat } = useDailyObjectives()
  
  // Gestion du streak quotidien (succès consécutifs)
  const getTodayKey = (suffix) => `${suffix}_${new Date().toDateString()}`

  // Fonctions à appeler lors des vraies actions utilisateur
  const onQuizCompleted = (quizResult) => {
    console.log('[DailyObjectives] Quiz completed:', quizResult)
    console.log('[DailyObjectives] Quiz difficulty:', quizResult.difficulty)
    console.log('[DailyObjectives] Quiz success:', quizResult.isSuccess)
    
    if (quizResult.isSuccess) {
      // TOUJOURS incrémenter les quiz par difficulté quand réussis
      const difficulty = quizResult.difficulty?.toLowerCase?.() || 'easy'
      console.log('[DailyObjectives] Difficulté détectée:', difficulty)
      
      if (difficulty === 'facile' || difficulty === 'easy') {
        console.log('[DailyObjectives] Quiz facile réussi - Incrémentation quiz_easy')
        incrementStat('quiz_easy')
      } else if (difficulty === 'moyen' || difficulty === 'moyenne' || difficulty === 'medium') {
        console.log('[DailyObjectives] Quiz moyen réussi - Incrémentation quiz_medium')
        incrementStat('quiz_medium')
      } else if (difficulty === 'difficile' || difficulty === 'hard') {
        console.log('[DailyObjectives] Quiz difficile réussi - Incrémentation quiz_hard')
        incrementStat('quiz_hard')
      }

      // Streak supprimé
    } else {
      console.log('[DailyObjectives] Quiz échoué - Pas d\'incrémentation')
      // Streak supprimé
    }
    
    // Gérer les quiz parfaits (100% de bonnes réponses)
    if (quizResult.percentage === 100) {
      console.log('[DailyObjectives] Quiz parfait détecté (100%)')
      incrementStat('quiz_perfect')
    }
  }

  // Gérer les séries de quiz réussis
  // Streak supprimé

  // Gérer la complétion d'exercices
  const onExerciseCompleted = (exerciseResult) => {
    console.log('[DailyObjectives] Exercise completed:', exerciseResult)
    
    if (exerciseResult.isSuccess) {
      console.log('[DailyObjectives] Exercise réussi - Incrémentation exercices_completed')
      incrementStat('exercices_completed')
    } else {
      console.log('[DailyObjectives] Exercise échoué - Pas d\'incrémentation')
    }
  }

  return {
    onQuizCompleted,
    
    onExerciseCompleted
  }
}
