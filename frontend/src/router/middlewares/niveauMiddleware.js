import { useUserStore } from '@/stores/user'

/**
 * Middleware pour vérifier que l'utilisateur a sélectionné un niveau
 * Redirige vers le dashboard si aucun niveau n'est sélectionné
 */
export function requireNiveau(to, from, next) {
  const userStore = useUserStore()
  
  // Si l'utilisateur n'est pas authentifié, laisser passer (auth middleware s'en occupe)
  if (!userStore.isAuthenticated) {
    return next()
  }
  
  // Si l'utilisateur n'a pas de niveau et n'est pas sur le dashboard
  if (!userStore.niveau_pays && to.name !== 'Dashboard') {
    console.log('🔒 Accès bloqué: niveau requis')
    return next({ name: 'Dashboard' })
  }
  
  // Si l'utilisateur a un niveau, laisser passer
  next()
}

/**
 * Liste des routes qui nécessitent un niveau
 */
export const routesRequiringNiveau = [
  'Cours',
  'Exercises', 
  'Quiz',
  'Sheets',
  'TablesFormules',
  'Themes',
  'Notions',
  'ExercicesByNotion',
  'ChapterExercises',
  'ChapterQuiz',
  'ThemeNotions',
  'CourseByNotion',
  'CourseNotions',
  'QuizByNotion',
  'QuizNotions',
  'TablesByNotion',
  'Progress',
  'Calculator'
]

/**
 * Vérifie si une route nécessite un niveau
 */
export function routeRequiresNiveau(routeName) {
  return routesRequiringNiveau.includes(routeName)
} 
