import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useSubscriptionStore } from '@/stores/subscription'
import { apiUtils } from '@/api/client'
import { matiereMiddleware, exercicesMiddleware, quizMiddleware } from './middlewares/matiereMiddleware'
import { requireNiveau, routeRequiresNiveau } from './middlewares/niveauMiddleware'

const ALWAYS_SCROLL_TO_TOP_ROUTES = [
  'CGV',
  'CGU',
  'Confidentialite',
  'Legal',
  'Cookies',
  'About',
  'CoursParticuliers',
  'FreeCourses',
  'FreeExercises',
  'FreeSummaries'
]

const routes = [
  { path: '/', name: 'Home', component: () => import('@/views/Home.vue') },
  {
    path: '/ressources-gratuites/cours',
    name: 'FreeCourses',
    component: () => import('@/views/FreeResourceNotions.vue'),
    props: { resourceType: 'course' }
  },
  {
    path: '/ressources-gratuites/cours/:slug',
    name: 'FreeCourseDetail',
    component: () => import('@/views/FreeCourseDetail.vue'),
    props: { resourceType: 'course' }
  },
  {
    path: '/ressources-gratuites/exercices',
    name: 'FreeExercises',
    component: () => import('@/views/FreeResourceNotions.vue'),
    props: { resourceType: 'exercise' }
  },
  {
    path: '/ressources-gratuites/exercices/notion/:notionId',
    name: 'FreeExerciseChapter',
    component: () => import('@/views/FreeExerciseChapter.vue'),
    props: true
  },
  {
    path: '/ressources-gratuites/exercices/:slug',
    name: 'FreeExerciseDetail',
    component: () => import('@/views/FreeCourseDetail.vue'),
    props: { resourceType: 'exercise' }
  },
  {
    path: '/ressources-gratuites/syntheses',
    name: 'FreeSummaries',
    component: () => import('@/views/FreeResourceNotions.vue'),
    props: { resourceType: 'summary' }
  },
  {
    path: '/ressources-gratuites/syntheses/:slug',
    name: 'FreeSummaryDetail',
    component: () => import('@/views/FreeCourseDetail.vue'),
    props: { resourceType: 'summary' }
  },
  { path: '/dashboard', name: 'Dashboard', component: () => import('@/views/Dashboard.vue') },
  { path: '/child/:childId', name: 'ChildOverview', component: () => import('@/views/ChildOverview.vue'), meta: { requiresAuth: true } },

  { path: '/account', name: 'Account', component: () => import('@/views/Account.vue'), meta: { requiresAuth: true } },
  { path: '/pricing', name: 'Pricing', component: () => import('@/views/Pricing.vue'), meta: { requiresAuth: true } },
  { path: '/billing', name: 'Billing', component: () => import('@/views/Billing.vue'), meta: { requiresAuth: true } },
  { path: '/billing/success', name: 'BillingSuccess', component: () => import('@/views/BillingSuccess.vue'), meta: { requiresAuth: true } },
  { path: '/billing/cancel', name: 'BillingCancel', component: () => import('@/views/BillingCancel.vue'), meta: { requiresAuth: true } },
  { path: '/subscription', name: 'Subscription', component: () => import('@/views/Subscription.vue'), meta: { requiresAuth: true } },
  { path: '/exercises', name: 'Exercises', component: () => import('@/views/Exercises.vue'), meta: { requiresAuth: true }, beforeEnter: matiereMiddleware },
  { path: '/online-courses', name: 'OnlineCourses', component: () => import('@/views/OnlineCourses.vue'), meta: { requiresAuth: true }, beforeEnter: matiereMiddleware },
  { path: '/quiz', name: 'Quiz', component: () => import('@/views/Quiz.vue'), meta: { requiresAuth: true }, beforeEnter: matiereMiddleware },
  { 
    path: '/quiz/:matiereId', 
    name: 'QuizNotions', 
    component: () => import('@/views/QuizNotions.vue'), 
    meta: { requiresAuth: true }, 
    beforeEnter: quizMiddleware 
  },
  {
    path: '/quiz-notion/153',
    name: 'QuizHomeworkByNotion',
    component: () => import('@/views/HomeworkByNotion.vue'),
    meta: { requiresAuth: true, requiresSubscription: true }
  },
// Accès direct : remplacé par une page énoncé simple
{ path: '/quiz-notion/:notionId', name: 'QuizByNotion', component: () => import('@/views/HomeworkByNotion.vue'), meta: { requiresAuth: true, requiresSubscription: true }, beforeEnter: quizMiddleware },
  { path: '/quiz-coming-soon', name: 'QuizComingSoon', component: () => import('@/views/QuizComingSoon.vue'), meta: { requiresAuth: true } },
  { 
    path: '/course-notions/:matiereId', 
    name: 'CourseNotions', 
    component: () => import('@/views/CourseNotions.vue'), 
    meta: { requiresAuth: true } 
  },
  // Cours par notion (chapitres supprimés)
{ path: '/course-notion/:notionId', name: 'CourseByNotion', component: () => import('@/views/Cours.vue'), meta: { requiresAuth: true, requiresSubscription: true } },
{ path: '/cours/:matiereId/:notionId/:chapitreId', name: 'Cours', component: () => import('@/views/Cours.vue'), meta: { requiresAuth: true, requiresSubscription: true } },
{ path: '/cours/:matiereId/:notionId/:chapitreId/:coursId', name: 'CoursDetail', component: () => import('@/views/CoursDetail.vue'), meta: { requiresAuth: true, requiresSubscription: true } },
  { 
    path: '/sheets', 
    name: 'Sheets', 
    component: () => import('@/views/SynthesisNotions.vue'), 
    meta: { requiresAuth: true }, 
    beforeEnter: matiereMiddleware 
  },
{ path: '/sheets-notion/:notionId', name: 'SynthesisByNotion', component: () => import('@/views/SheetByNotion.vue'), meta: { requiresAuth: true, requiresSubscription: true }, beforeEnter: matiereMiddleware },
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
  { 
    path: '/exercicies/:matiereId', 
    name: 'Themes', 
    component: () => import('@/views/Themes.vue'), 
    meta: { requiresAuth: true }, 
    beforeEnter: exercicesMiddleware 
  },
{ path: '/theme-notions/:themeId', name: 'ThemeNotions', component: () => import('@/views/ThemeNotions.vue'), meta: { requiresAuth: true }, beforeEnter: exercicesMiddleware },
  // Exercices par notion directement
{ path: '/exercices-notion/:notionId', name: 'ExercicesByNotion', component: () => import('@/views/ChapterExercises.vue'), meta: { requiresAuth: true, requiresSubscription: true }, beforeEnter: exercicesMiddleware },
{ path: '/exercice/:exerciceId', name: 'ExerciceDetail', component: () => import('@/views/ExerciceDetail.vue'), meta: { requiresAuth: true, requiresSubscription: true } },
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
      { path: 'newsletter', name: 'AdminNewsletter', component: () => import('@/views/admin/NewsletterAdmin.vue') },
      { path: 'subscriptions', name: 'AdminSubscriptions', component: () => import('@/views/admin/AdminSubscriptions.vue') },
      { path: 'subscribers', name: 'AdminSubscribers', component: () => import('@/views/admin/AdminSubscribers.vue') },
      { path: 'matieres', name: 'AdminMatieres', component: () => import('@/views/admin/AdminMatieres.vue') },
      { path: 'themes', name: 'AdminThemes', component: () => import('@/views/admin/AdminThemes.vue') },
      { path: 'notions', name: 'AdminNotions', component: () => import('@/views/admin/AdminNotions.vue') },
      // { path: 'chapitres', name: 'AdminChapitres', component: () => import('@/views/admin/AdminChapitres.vue') },
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
  // Restaurer intelligemment la position de scroll
  scrollBehavior(to, from, savedPosition) {
    try {
      if (ALWAYS_SCROLL_TO_TOP_ROUTES.includes(to.name)) {
        return { top: 0, behavior: 'instant' }
      }

      // 1) Gestion des ancres (hash)
      // Sauf pour la liste d'exercices où l'on gère finement l'ancre côté composant
      if (to.hash && to.name !== 'ExercicesByNotion') {
        return { el: to.hash, behavior: 'auto' }
      }

      // 2) Navigation avec bouton retour/avant du navigateur
      if (savedPosition) {
        return savedPosition
      }

      // 3) Revenir sur la liste d'exercices d'une notion: restaurer la position précédente
      if (to.name === 'ExercicesByNotion' && to.params?.notionId) {
        const key = `optitab_page_exercices_${to.params.notionId}`
        const raw = sessionStorage.getItem(key)
        if (raw) {
          try {
            const state = JSON.parse(raw)
            if (state && typeof state.scrollY === 'number') {
              return { left: 0, top: state.scrollY }
            }
          } catch (_) { /* ignore */ }
        }
      }

      // 4) Comportement par défaut: ne pas forcer de scroll
      return false
    } catch (_) {
      return false
    }
  }
})

// Utilitaires de persistance du scroll (comportement "onglets")
function getScrollContainer() {
  try {
    return document.querySelector('.dashboard-main') || document.querySelector('.dashboard-content') || document.scrollingElement || document.documentElement
  } catch (_) {
    return undefined
  }
}

function scrollKeyForRoute(route) {
  if (!route || !route.name) return null
  const id = route.params?.notionId || route.params?.matiereId || route.params?.chapitreId || route.params?.exerciceId || ''
  return `optitab_scroll_route_${route.name}_${id}`
}

function saveScrollForRoute(route) {
  try {
    const key = scrollKeyForRoute(route)
    if (!key) return
    const c = getScrollContainer()
    if (!c) return
    const y = (c === document.documentElement || c === document.body) ? (window.pageYOffset || document.documentElement.scrollTop || 0) : c.scrollTop
    sessionStorage.setItem(key, JSON.stringify({ y, t: Date.now() }))
  } catch (_) {}
}

function restoreScrollForRoute(route) {
  try {
    const key = scrollKeyForRoute(route)
    if (!key) return
    const raw = sessionStorage.getItem(key)
    if (!raw) return
    const s = JSON.parse(raw)
    if (!s || typeof s.y !== 'number') return
    const c = getScrollContainer()
    if (!c) return
    if (c === document.documentElement || c === document.body) {
      window.scrollTo({ top: s.y, behavior: 'auto' })
    } else {
      c.scrollTo({ top: s.y, behavior: 'auto' })
    }
  } catch (_) {}
}

// Enregistrer la position avant navigation, restaurer après
router.beforeEach((to, from, next) => {
  // Sauvegarde opportuniste, ne bloque jamais la navigation
  try { saveScrollForRoute(from) } catch (_) {}
  next()
})

router.afterEach((to) => {
  // Routes qui doivent toujours s'ouvrir en haut (pas de restauration de scroll)
  if (ALWAYS_SCROLL_TO_TOP_ROUTES.includes(to.name)) {
    // Forcer le scroll en haut après le chargement
    setTimeout(() => {
      window.scrollTo({ top: 0, behavior: 'instant' })
    }, 50)
    return
  }
  // Ne rien faire si ancre spécifique
  if (to.hash && to.hash.startsWith('#')) return
  // Restaurer si on a déjà visité la route
  setTimeout(() => restoreScrollForRoute(to), 30)
  setTimeout(() => restoreScrollForRoute(to), 120)
})

// Navigation guard pour protéger le dashboard
router.beforeEach(async (to, from, next) => {
  let token = localStorage.getItem('access_token')
  const refreshToken = localStorage.getItem('refresh_token')
  const userStore = useUserStore()
  const subscriptionStore = useSubscriptionStore()
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

  // Si on a un token mais qu'il est expiré, tenter un rafraîchissement plutôt que de supprimer le refresh token
  if (token && isTokenExpired(token)) {
    console.warn("Token d'accès expiré détecté dans le navigation guard, tentative de rafraîchissement...")
    if (refreshToken) {
      try {
        await apiUtils.refreshToken()
        // Mettre à jour la variable locale token après rafraîchissement
        token = localStorage.getItem('access_token')
        // Recharger le profil si le store n'est pas encore prêt (admin, etc.)
        if (!userStore.isAuthenticated) {
          await userStore.fetchUser()
        }
        isAuthenticated = userStore.isAuthenticated
        isAdmin = userStore.isAdmin
      } catch (e) {
        console.warn('Échec du rafraîchissement dans le navigation guard:', e?.message || e)
        userStore.clearUser()
        subscriptionStore.clear()
        isAuthenticated = false
        isAdmin = false
      }
    } else {
      userStore.clearUser()
      subscriptionStore.clear()
      isAuthenticated = false
      isAdmin = false
    }
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
      subscriptionStore.clear()
      isAuthenticated = false
      isAdmin = false
    }
  }

  // Protection des routes authentifiées
  if ((to.meta.requiresAuth || to.name === 'Dashboard') && !isAuthenticated) {
    next({ name: 'Home' })
  } 
  // Protection des routes admin
  else if (to.meta.requiresAdmin && (!isAuthenticated || !isAdmin)) {
    const fallback = to.meta.onAdminDenied || 'Home'
    next({ name: fallback })
  } 
  // Redirection Home -> Dashboard pour utilisateurs connectés
  // MAIS seulement si on ne vient PAS déjà du Dashboard (évite les boucles)
  else if (isAuthenticated && (to.name === 'Home' || to.path === '/') && from.name !== 'Dashboard') {
    next({ name: 'Dashboard', replace: true })
  } 
  // Autres routes
  else {
    if (isAuthenticated && to.meta.requiresSubscription && !isAdmin) {
      await subscriptionStore.fetchStatus({ force: !subscriptionStore.hasAccess })
      if (!subscriptionStore.hasAccess) {
        const unlocked = await subscriptionStore.refreshUntilAccess({ attempts: 5, interval: 2000 })
        if (!unlocked) {
          return next({ name: 'Billing', query: { redirect: to.fullPath, reason: 'subscription_required' } })
        }
      }
    }
    // Vérifier si la route nécessite un niveau
    if (isAuthenticated && routeRequiresNiveau(to.name)) {
      requireNiveau(to, from, next)
    } else {
      next()
    }
  }
})

export default router 
