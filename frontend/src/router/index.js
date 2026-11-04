import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useSubscriptionStore } from '@/stores/subscription'
import { apiUtils } from '@/api/client'
import * as analytics from '@/services/analytics'
import { applyRouteSeo } from '@/services/seo'
import { matiereMiddleware, quizMiddleware } from './middlewares/matiereMiddleware'
import { versBlog, versRessources } from './ressources'
import { requireNiveau, routeRequiresNiveau } from './middlewares/niveauMiddleware'

const RessourcesGratuites = () => import('@/views/RessourcesGratuites.vue')

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
  'FreeSummaries',
  'HelpGraphe'
]

// Anciennes adresses de l'espace connecté (listes de chapitres, cours, fiches,
// exercices par chapitre) : elles renvoient toutes vers le nouvel espace. Leurs
// noms sont conservés pour que les liens internes, favoris et notifications marchent.
const versChapitres = () => ({ path: '/chapitres' })
const versChapitre = (onglet) => (to) => {
  const query = onglet ? { onglet } : {}
  const exercice = String(to.hash || '').match(/^#ex-(\d+)/)
  if (exercice) query.ex = exercice[1]
  return { path: `/chapitre/${to.params.notionId}`, query, hash: '' }
}

const routes = [
  // Vitrine refaite le 2026-11-02. L'ancienne page (views/Home.vue) est conservée :
  // la remettre en place = remplacer HomeVitrine.vue par Home.vue ci-dessous.
  { path: '/', name: 'Home', component: () => import('@/views/HomeVitrine.vue') },
  { path: '/apercu/accueil', redirect: '/' },
  // Adresses de l'aperçu du nouvel espace (validé et mis en place le 2026-11-03).
  { path: '/apercu/espace', redirect: (to) => ({ path: '/dashboard', query: to.query }) },
  { path: '/apercu/espace/chapitres', redirect: (to) => ({ path: '/chapitres', query: to.query }) },
  { path: '/apercu/espace/chapitre/:notionId', redirect: (to) => ({ path: `/chapitre/${to.params.notionId}`, query: to.query }) },
  { path: '/start', name: 'StartLanding', component: () => import('@/views/GoogleAdsLanding.vue') },
  { path: '/commencer', redirect: '/start' },
  // Page "lien en bio" partagee sur tous les reseaux sociaux.
  // Sa mise en ligne se pilote depuis le studio (/admin/temoignages) : la vue
  // interroge l'API au chargement et renvoie les visiteurs a l'accueil tant
  // que la page n'est pas publiee. Pas de garde de routeur ici, sinon il
  // faudrait un appel reseau avant chaque navigation du site.
  { path: '/avis', name: 'BioLanding', component: () => import('@/views/BioLanding.vue') },
  // Ancienne adresse conservee : un lien deja partage ne doit jamais casser.
  { path: '/optitab', redirect: '/avis' },
  ...['instagram', 'facebook', 'tiktok', 'youtube', 'snapchat'].map((network) => ({
    path: `/${network}`,
    redirect: {
      path: '/avis',
      query: {
        utm_source: network,
        utm_medium: 'bio'
      }
    }
  })),
  {
    path: '/jeux/math-run',
    name: 'MathRun',
    component: () => import('@/views/games/MathRunView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true, onAdminDenied: 'Dashboard' }
  },
  { path: '/tarifs', name: 'TarifsPage', component: () => import('@/views/TarifsPage.vue') },

  // Versement ponctuel pour un cours particulier : lien envoye au cas par cas.
  // Le noindex est declare dans NOINDEX_ROUTE_NAMES (services/seo.js) :
  // `meta.robots` n'est pas lu par applyRouteSeo.
  { path: '/paiement', name: 'LessonPayment', component: () => import('@/views/LessonPayment.vue') },
  {
    path: '/paiement/merci',
    name: 'LessonPaymentThanks',
    component: () => import('@/views/LessonPaymentThanks.vue')
  },
  { path: '/plateforme-maths', name: 'GoogleAdsLanding', component: () => import('@/views/GoogleAdsLanding.vue') },
  { path: '/bases-methode', name: 'BasesMethodeLanding', component: () => import('@/views/GoogleAdsLanding.vue') },
  {
    path: '/exercices-corriges',
    alias: ['/exercices-corriges-pas-a-pas'],
    name: 'ExercicesCorrigesLanding',
    component: () => import('@/views/GoogleAdsLanding.vue')
  },
  {
    path: '/diagnostic-maths-gratuit',
    name: 'DiagnosticLanding',
    component: () => import('@/views/DiagnosticLanding.vue')
  },
  {
    path: '/diagnostic-merci',
    name: 'DiagnosticMerci',
    component: () => import('@/views/DiagnosticMerci.vue'),
    meta: { robots: 'noindex,nofollow' }
  },
  // Ressources gratuites : pages statiques (scripts/ressources). Les anciennes
  // adresses gardent leur nom de route et mènent à la page statique.
  { path: '/ressources-gratuites/maths/:chemin(.*)*', name: 'RessourcesGratuitesPage', component: RessourcesGratuites, beforeEnter: versRessources },
  { path: '/ressources-gratuites', name: 'FreeResourcesHome', component: RessourcesGratuites, beforeEnter: versRessources },
  { path: '/ressources-gratuites/cours', name: 'FreeCourses', component: RessourcesGratuites, beforeEnter: versRessources },
  { path: '/ressources-gratuites/cours/:pays/:niveauGroup/:matiere/:slug-:id(\\d+)', name: 'FreeCourseSlugGrouped', component: RessourcesGratuites, beforeEnter: versRessources },
  { path: '/ressources-gratuites/cours/:pays/:matiere/:slug-:id(\\d+)', name: 'FreeCourseSlug', component: RessourcesGratuites, beforeEnter: versRessources },
  { path: '/ressources-gratuites/cours/:slug', name: 'FreeCourseDetail', component: RessourcesGratuites, beforeEnter: versRessources },
  { path: '/ressources-gratuites/exercices', name: 'FreeExercises', component: RessourcesGratuites, beforeEnter: versRessources },
  { path: '/ressources-gratuites/exercices/notion/:notionId', name: 'FreeExerciseChapter', component: RessourcesGratuites, beforeEnter: versRessources },
  { path: '/ressources-gratuites/exercices/:pays/:niveauGroup/:matiere/:slug-:id(\\d+)', name: 'FreeExerciseChapterSlugGrouped', component: RessourcesGratuites, beforeEnter: versRessources },
  { path: '/ressources-gratuites/exercices/:pays/:matiere/:slug-:id(\\d+)', name: 'FreeExerciseChapterSlug', component: RessourcesGratuites, beforeEnter: versRessources },
  { path: '/ressources-gratuites/exercices/:pays/:slug-:id(\\d+)', name: 'FreeExerciseChapterSlugLegacy', component: RessourcesGratuites, beforeEnter: versRessources },
  { path: '/ressources-gratuites/exercices/:slug', name: 'FreeExerciseDetail', component: RessourcesGratuites, beforeEnter: versRessources },
  { path: '/ressources-gratuites/syntheses', name: 'FreeSummaries', component: RessourcesGratuites, beforeEnter: versRessources },
  { path: '/ressources-gratuites/syntheses/:pays/:niveauGroup/:matiere/:slug-:id(\\d+)', name: 'FreeSummarySlugGrouped', component: RessourcesGratuites, beforeEnter: versRessources },
  { path: '/ressources-gratuites/syntheses/:pays/:matiere/:slug-:id(\\d+)', name: 'FreeSummarySlug', component: RessourcesGratuites, beforeEnter: versRessources },
  { path: '/ressources-gratuites/syntheses/:slug', name: 'FreeSummaryDetail', component: RessourcesGratuites, beforeEnter: versRessources },
  // Espace connecté refait le 2026-11-03 (views/espace). Ancien tableau de bord
  // conservé hors route : views/Dashboard.vue, views/ChildOverview.vue.
  { path: '/dashboard', name: 'Dashboard', component: () => import('@/views/espace/EspaceAccueil.vue'), meta: { requiresAuth: true } },
  { path: '/chapitres', name: 'Chapitres', component: () => import('@/views/espace/EspaceChapitres.vue'), meta: { requiresAuth: true } },
  { path: '/chapitre/:notionId', name: 'Chapitre', component: () => import('@/views/espace/EspaceChapitre.vue'), meta: { requiresAuth: true, requiresSubscription: true } },
  { path: '/child/:childId', name: 'ChildOverview', component: () => import('@/views/espace/EspaceEnfant.vue'), meta: { requiresAuth: true } },

  { path: '/account', name: 'Account', component: () => import('@/views/Account.vue'), meta: { requiresAuth: true } },
  // Ancienne page de formules (appelait une adresse serveur disparue) : les formules sont sur /billing.
  { path: '/pricing', name: 'Pricing', redirect: (to) => ({ path: '/billing', query: to.query, hash: to.hash }) },
  { path: '/billing', name: 'Billing', component: () => import('@/views/Billing.vue'), meta: { requiresAuth: true } },
  { path: '/billing/success', name: 'BillingSuccess', component: () => import('@/views/BillingSuccess.vue') },
  { path: '/billing/cancel', name: 'BillingCancel', component: () => import('@/views/BillingCancel.vue') },
  { path: '/subscription', name: 'Subscription', component: () => import('@/views/Subscription.vue'), meta: { requiresAuth: true } },
  { path: '/exercises', name: 'Exercises', redirect: versChapitres },
  { path: '/online-courses', name: 'OnlineCourses', redirect: versChapitres },
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
  { path: '/course-notions/:matiereId', name: 'CourseNotions', redirect: versChapitres },
  { path: '/course-notion/:notionId', name: 'CourseByNotion', redirect: versChapitre(null) },
  { path: '/cours/:matiereId/:notionId/:chapitreId', name: 'Cours', redirect: versChapitre(null) },
  { path: '/cours/:matiereId/:notionId/:chapitreId/:coursId', name: 'CoursDetail', redirect: versChapitre(null) },
  { path: '/sheets', name: 'Sheets', redirect: versChapitres },
  { path: '/tables-formules', name: 'TablesFormules', redirect: versChapitres },
  { path: '/sheets-notion/:notionId', name: 'SynthesisByNotion', redirect: versChapitre('fiche') },
  { path: '/tables-formules-notion/:notionId', name: 'TablesByNotion', redirect: versChapitre('fiche') },
  { path: '/about', name: 'About', component: () => import('@/views/About.vue') },
  { path: '/contact', name: 'Contact', component: () => import('@/views/Contact.vue') },
  // Blog public.
  // Pages statiques générées à la construction (scripts/ressources/blog.mjs).
  { path: '/blog/:chemin(.*)*', name: 'Blog', component: RessourcesGratuites, beforeEnter: versBlog },
  { path: '/cours-particuliers', name: 'CoursParticuliers', component: () => import('@/views/CoursParticuliers.vue') },
  { path: '/password-reset', name: 'PasswordReset', component: () => import('@/views/PasswordReset.vue') },
  { path: '/cgv', name: 'CGV', component: () => import('@/views/CGV.vue') },
  { path: '/cgu', name: 'CGU', component: () => import('@/views/CGU.vue') },
  { path: '/confidentialite', name: 'Confidentialite', component: () => import('@/views/Confidentialite.vue') },
  { path: '/legal', name: 'Legal', component: () => import('@/views/Legal.vue') },
  { path: '/cookies', name: 'Cookies', component: () => import('@/views/Cookies.vue') },
  { path: '/conditions', name: 'Conditions', component: () => import('@/views/Conditions.vue') },
  { path: '/notions/:matiereId', name: 'Notions', redirect: versChapitres },
  { path: '/exercicies/:matiereId', name: 'Themes', redirect: versChapitres },
  { path: '/theme-notions/:themeId', name: 'ThemeNotions', redirect: versChapitres },
  { path: '/exercices-notion/:notionId', name: 'ExercicesByNotion', redirect: versChapitre('exercices') },
  // Un exercice seul : la page retrouve son chapitre et y renvoie (?ex=).
  { path: '/exercice/:exerciceId', name: 'ExerciceDetail', component: () => import('@/views/ExerciceDetail.vue'), meta: { requiresAuth: true, requiresSubscription: true } },
  { path: '/progress', name: 'Progress', redirect: versChapitres },
  { path: '/historique-exercices', name: 'ExercisesHistory', component: () => import('@/views/ExercisesHistory.vue'), meta: { requiresAuth: true } },
  { path: '/historique-quiz', name: 'QuizzesHistory', component: () => import('@/views/QuizzesHistory.vue'), meta: { requiresAuth: true } },
  { path: '/mes-quiz-rendus', name: 'QuizSubmissionsStudent', component: () => import('@/views/QuizSubmissionsStudent.vue'), meta: { requiresAuth: true } },
  { path: '/calculator', name: 'Calculator', component: () => import('@/views/Calculator.vue') },
  { path: '/aide-grapheur', name: 'HelpGraphe', component: () => import('@/views/HelpGraphe.vue') },
  {
    path: '/admin',
    component: () => import('@/views/admin/AdminLayout.vue'),
    meta: { requiresAdmin: true },
    children: [
      { path: '', name: 'AdminHome', component: () => import('@/views/admin/AdminHome.vue') },
      { path: 'newsletter', name: 'AdminNewsletter', component: () => import('@/views/admin/NewsletterAdmin.vue') },
      { path: 'subscriptions', name: 'AdminSubscriptions', component: () => import('@/views/admin/AdminSubscriptions.vue') },
      { path: 'subscribers', name: 'AdminSubscribers', component: () => import('@/views/admin/AdminSubscribers.vue') },
      { path: 'passes', name: 'AdminPasses', component: () => import('@/views/admin/AdminPasses.vue') },
      { path: 'matieres', name: 'AdminMatieres', component: () => import('@/views/admin/AdminMatieres.vue') },
      { path: 'themes', name: 'AdminThemes', component: () => import('@/views/admin/AdminThemes.vue') },
      { path: 'notions', name: 'AdminNotions', component: () => import('@/views/admin/AdminNotions.vue') },
      // { path: 'chapitres', name: 'AdminChapitres', component: () => import('@/views/admin/AdminChapitres.vue') },
      { path: 'exercices', name: 'AdminExercices', component: () => import('@/views/admin/AdminExercices.vue') },
      { path: 'exercices-plus', name: 'AdminExercicesPlus', component: () => import('@/views/admin/AdminExercicesPlus.vue') },
      { path: 'cours', name: 'AdminCours', component: () => import('@/views/admin/AdminCours.vue') },
      { path: 'cours-pdf', name: 'AdminCoursPdf', component: () => import('@/views/admin/AdminCoursPdf.vue') },
      { path: 'cours-plus', name: 'AdminCoursPlus', component: () => import('@/views/admin/AdminCoursPlus.vue') },
      { path: 'sheets', name: 'AdminSheets', component: () => import('@/views/admin/AdminSheets.vue') },
      { path: 'quiz', name: 'AdminQuiz', component: () => import('@/views/admin/AdminQuiz.vue') },
      { path: 'quiz-plus', name: 'AdminQuizPlus', component: () => import('@/views/admin/AdminQuizPlus.vue') },
      { path: 'quiz-submissions', name: 'AdminQuizSubmissions', component: () => import('@/views/admin/AdminQuizSubmissions.vue') },
      { path: 'niveaux', name: 'AdminNiveaux', component: () => import('@/views/admin/AdminNiveaux.vue') },
      { path: 'pays', name: 'AdminPays', component: () => import('@/views/admin/AdminPays.vue') },
      { path: 'reel-studio', name: 'AdminReelStudio', component: () => import('@/views/admin/ReelStudioAdminPage.vue') },
      { path: 'reel-background', name: 'AdminReelBackground', component: () => import('@/views/admin/AdminReelBackground.vue') },
      { path: 'blog', name: 'AdminBlog', component: () => import('@/views/admin/AdminBlog.vue') },
      { path: 'temoignages', name: 'AdminTestimonials', component: () => import('@/views/admin/AdminTestimonials.vue') },
    ]
  },
  // Aperçu d'un quiz sans connexion, en local seulement (relecture et captures du chantier).
  ...(import.meta.env.DEV ? [{ path: '/apercu/quiz/:notionId', name: 'ApercuQuiz', component: () => import('@/views/espace/ApercuQuiz.vue') }] : []),
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('@/views/NotFound.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  // Toujours remonter en haut lors d'un clic sur un lien (sauf ancre ou back/forward)
  scrollBehavior(to, from, savedPosition) {
    try {
      if (ALWAYS_SCROLL_TO_TOP_ROUTES.includes(to.name)) {
        return { top: 0, left: 0, behavior: 'auto' }
      }

      // Nouvel espace : changer d'onglet ou d'exercice dans un chapitre ne fait pas
      // défiler ici, la page gère elle-même la position (reprise de lecture par onglet).
      if (to.name === 'Chapitre' && from.name === to.name && to.params.notionId === from.params.notionId) {
        return false
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

      // 3) Comportement par défaut: remonter en haut
      return { top: 0, left: 0, behavior: 'auto' }
    } catch (_) {
      return { top: 0, left: 0, behavior: 'auto' }
    }
  }
})

// Normalize trailing slashes (fallback if edge redirects aren't configured yet)
router.beforeEach((to) => {
  try {
    const path = String(to?.path || '')
    if (path.length > 1 && /\/+$/.test(path)) {
      const normalizedPath = path.replace(/\/+$/, '')
      if (normalizedPath && normalizedPath !== path) {
        return {
          path: normalizedPath,
          query: to.query,
          hash: to.hash,
          replace: true
        }
      }
    }
    return true
  } catch (_) {
    return true
  }
})

router.afterEach((to) => {
  try { applyRouteSeo(to) } catch (_) {}
  try { analytics.pageView(to.fullPath) } catch (_) {}
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
    // Même page (seuls l'onglet ou l'exercice changent) : l'accès vient d'être vérifié.
    const memePage = from.name === to.name && from.path === to.path
    if (isAuthenticated && to.meta.requiresSubscription && !isAdmin && !memePage) {
      // Bypass pour le chapitre démo de l'utilisateur
      const demoNotionId = userStore.niveau_pays?.demo_notion
      const routeNotionId = to.params.notionId
      const isDemoAccess = demoNotionId && routeNotionId && Number(routeNotionId) === Number(demoNotionId)
      if (!isDemoAccess) {
        const currentLevelId = userStore.niveau_pays?.id
        // Statut gardé une minute : d'une page à l'autre, la vérification est immédiate.
        await subscriptionStore.fetchStatus()
        if (!subscriptionStore.accessForLevel(currentLevelId)) {
          // Pas d'accès d'après le statut connu : on redemande au serveur avant de conclure
          // (deux fois seulement en cas de coupure réseau).
          await subscriptionStore.fetchStatus({ force: true })
          if (subscriptionStore.error) {
            await new Promise((resolve) => setTimeout(resolve, 800))
            await subscriptionStore.fetchStatus({ force: true })
          }
          if (!subscriptionStore.accessForLevel(currentLevelId)) {
            return next({ name: 'Billing', hash: '#plans', query: { redirect: to.fullPath, reason: 'subscription_required' } })
          }
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
