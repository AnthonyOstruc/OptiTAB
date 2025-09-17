import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { matiereMiddleware, exercicesMiddleware, quizMiddleware } from './middlewares/matiereMiddleware'
import { requireNiveau, routeRequiresNiveau } from './middlewares/niveauMiddleware'

const routes = [
  { path: '/', name: 'Home', component: () => import('@/views/Home.vue') },
  { path: '/dashboard', name: 'Dashboard', component: () => import('@/views/Dashboard.vue') },
  { path: '/child/:childId', name: 'ChildOverview', component: () => import('@/views/ChildOverview.vue'), meta: { requiresAuth: true } },

  { path: '/account', name: 'Account', component: () => import('@/views/Account.vue'), meta: { requiresAuth: true } },
  { path: '/pricing', name: 'Pricing', component: () => import('@/views/Pricing.vue'), meta: { requiresAuth: true } },
  { path: '/exercises', name: 'Exercises', component: () => import('@/views/Exercises.vue'), meta: { requiresAuth: true }, beforeEnter: matiereMiddleware },
  { path: '/online-courses', name: 'OnlineCourses', component: () => import('@/views/OnlineCourses.vue'), meta: { requiresAuth: true }, beforeEnter: matiereMiddleware },
  { path: '/quiz', name: 'Quiz', component: () => import('@/views/Quiz.vue'), meta: { requiresAuth: true }, beforeEnter: matiereMiddleware },
  { path: '/quiz/:matiereId', name: 'QuizNotions', component: () => import('@/views/QuizNotions.vue'), meta: { requiresAuth: true }, beforeEnter: quizMiddleware },
  { path: '/quiz-chapitres/:notionId', name: 'QuizChapitres', component: () => import('@/views/QuizChapitres.vue'), meta: { requiresAuth: true }, beforeEnter: quizMiddleware },
  { path: '/quiz-exercices/:chapitreId', name: 'ChapterQuiz', component: () => import('@/views/ChapterQuiz.vue'), meta: { requiresAuth: true }, beforeEnter: quizMiddleware },
  { path: '/course-notions/:matiereId', name: 'CourseNotions', component: () => import('@/views/CourseNotions.vue'), meta: { requiresAuth: true } },
  { path: '/course-chapitres/:notionId', name: 'CourseChapitres', component: () => import('@/views/CourseChapitres.vue'), meta: { requiresAuth: true } },
  { path: '/course/:chapitreId', name: 'CourseChapitre', component: () => import('@/views/CourseChapitre.vue'), meta: { requiresAuth: true } },
  { path: '/cours/:matiereId/:notionId/:chapitreId', name: 'Cours', component: () => import('@/views/Cours.vue'), meta: { requiresAuth: true } },
  { path: '/cours/:matiereId/:notionId/:chapitreId/:coursId', name: 'CoursDetail', component: () => import('@/views/CoursDetail.vue'), meta: { requiresAuth: true } },
  { path: '/sheets', name: 'Sheets', component: () => import('@/views/Sheets.vue'), meta: { requiresAuth: true }, beforeEnter: matiereMiddleware },
  { path: '/about', name: 'About', component: () => import('@/views/About.vue') },
  { path: '/contact', name: 'Contact', component: () => import('@/views/Contact.vue') },
  { path: '/cours-particuliers', name: 'CoursParticuliers', component: () => import('@/views/CoursParticuliers.vue') },
  { path: '/password-reset', name: 'PasswordReset', component: () => import('@/views/PasswordReset.vue') },
  { path: '/cgv', name: 'CGV', component: () => import('@/views/CGV.vue') },
  { path: '/cgu', name: 'CGU', component: () => import('@/views/CGU.vue') },
  { path: '/confidentialite', name: 'Confidentialite', component: () => import('@/views/Confidentialite.vue') },
  { path: '/legal', name: 'Legal', component: () => import('@/views/Legal.vue') },
  { path: '/cookies', name: 'Cookies', component: () => import('@/views/Cookies.vue') },
  { path: '/conditions', name: 'Conditions', component: () => import('@/views/Conditions.vue') },
  { path: '/notions/:matiereId', name: 'Notions', component: () => import('@/views/Notions.vue'), meta: { requiresAuth: true }, beforeEnter: exercicesMiddleware },
  { path: '/themes/:matiereId', name: 'Themes', component: () => import('@/views/Themes.vue'), meta: { requiresAuth: true }, beforeEnter: exercicesMiddleware },
  { path: '/theme-notions/:themeId', name: 'ThemeNotions', component: () => import('@/views/ThemeNotions.vue'), meta: { requiresAuth: true }, beforeEnter: exercicesMiddleware },
  { path: '/chapitres/:notionId', name: 'Chapitres', component: () => import('@/views/Chapitres.vue'), meta: { requiresAuth: true }, beforeEnter: exercicesMiddleware },
  { path: '/exercices/:chapitreId', name: 'Exercices', component: () => import('@/views/ChapterExercises.vue'), meta: { requiresAuth: true }, beforeEnter: exercicesMiddleware },
  { path: '/exercice/:exerciceId', name: 'ExerciceDetail', component: () => import('@/views/ExerciceDetail.vue'), meta: { requiresAuth: true } },
  { path: '/progress', name: 'Progress', component: () => import('@/views/Progress.vue'), meta: { requiresAuth: true } },
  { path: '/historique-exercices', name: 'ExercisesHistory', component: () => import('@/views/ExercisesHistory.vue'), meta: { requiresAuth: true } },
  { path: '/historique-quiz', name: 'QuizzesHistory', component: () => import('@/views/QuizzesHistory.vue'), meta: { requiresAuth: true } },
  { path: '/calculator', name: 'Calculator', component: () => import('@/views/Calculator.vue') },
  { path: '/test-filtrage-strict', name: 'TestFiltrageStrict', component: () => import('@/views/TestFiltrageStrict.vue') },
  {
    path: '/admin',
    component: () => import('@/views/admin/AdminLayout.vue'),
    meta: { requiresAdmin: true },
    children: [
      { path: 'matieres', name: 'AdminMatieres', component: () => import('@/views/admin/AdminMatieres.vue') },
      { path: 'themes', name: 'AdminThemes', component: () => import('@/views/admin/AdminThemes.vue') },
      { path: 'notions', name: 'AdminNotions', component: () => import('@/views/admin/AdminNotions.vue') },
      { path: 'chapitres', name: 'AdminChapitres', component: () => import('@/views/admin/AdminChapitres.vue') },
      { path: 'exercices', name: 'AdminExercices', component: () => import('@/views/admin/AdminExercices.vue') },
      { path: 'exercices-plus', name: 'AdminExercicesPlus', component: () => import('@/views/admin/AdminExercicesPlus.vue') },
      { path: 'cours', name: 'AdminCours', component: () => import('@/views/admin/AdminCours.vue') },
      { path: 'cours-plus', name: 'AdminCoursPlus', component: () => import('@/views/admin/AdminCoursPlus.vue') },
      { path: 'sheets', name: 'AdminSheets', component: () => import('@/views/admin/AdminSheets.vue') },
      { path: 'quiz', name: 'AdminQuiz', component: () => import('@/views/admin/AdminQuiz.vue') },
      { path: 'quiz-plus', name: 'AdminQuizPlus', component: () => import('@/views/admin/AdminQuizPlus.vue') },
      { path: 'niveaux', name: 'AdminNiveaux', component: () => import('@/views/admin/AdminNiveaux.vue') },
      { path: 'pays', name: 'AdminPays', component: () => import('@/views/admin/AdminPays.vue') },
      { path: '', redirect: { name: 'AdminMatieres' } }
    ]
  },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('@/views/NotFound.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  }
})

// Navigation guard pour protéger le dashboard
router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('access_token')
  const refreshToken = localStorage.getItem('refresh_token')
  const userStore = useUserStore()
  let isAuthenticated = userStore.isAuthenticated
  let isAdmin = userStore.isAdmin

  // Fonction utilitaire pour vérifier si un token JWT est expiré
  const isTokenExpired = (token) => {
    if (!token) return true
    try {
      const part = token.split('.')[1]
      let base64 = part.replace(/-/g, '+').replace(/_/g, '/')
      const pad = base64.length % 4
      if (pad) base64 += '='.repeat(4 - pad)
      const payload = JSON.parse(atob(base64))
      const currentTime = Math.floor(Date.now() / 1000)
      return payload.exp < currentTime
    } catch (error) {
      console.warn('Impossible de décoder le token JWT', error)
      return false
    }
  }

  // Si on a un token mais qu'il est expiré, nettoyer et rediriger
  if (token && isTokenExpired(token)) {
    console.warn('Token d\'accès expiré détecté dans le navigation guard, nettoyage...')
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    userStore.clearUser()
    isAuthenticated = false
    isAdmin = false
  }

  // Si on a un token valide mais que le store n'est pas prêt (ex: après refresh), on recharge l'utilisateur
  if (token && !isTokenExpired(token) && !isAuthenticated) {
    try {
      console.log('Rechargement de l\'utilisateur depuis le navigation guard...')
      await userStore.fetchUser()
      isAuthenticated = userStore.isAuthenticated
      isAdmin = userStore.isAdmin
    } catch (e) {
      console.error('Échec du rechargement utilisateur dans navigation guard:', e)
      // Si fetchUser échoue, nettoyer et considérer comme non authentifié
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      userStore.clearUser()
      isAuthenticated = false
      isAdmin = false
    }
  }

  if ((to.meta.requiresAuth || to.name === 'Dashboard') && !isAuthenticated) {
    next({ name: 'Home' })
  } else if (to.meta.requiresAdmin && (!isAuthenticated || !isAdmin)) {
    next({ name: 'Home' })
  } else if (isAuthenticated && (to.name === 'Home' || to.path === '/')) {
    // Si connecté et essaie d'aller sur la home, redirige vers le dashboard
    next({ name: 'Dashboard' })
  } else {
    // Vérifier si la route nécessite un niveau
    if (isAuthenticated && routeRequiresNiveau(to.name)) {
      requireNiveau(to, from, next)
    } else {
      next()
    }
  }
})

export default router 