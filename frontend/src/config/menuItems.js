// Import icons from assets
// Note: You'll need to create these icons or use a library like @heroicons/vue
// For now, I'll use placeholder imports
import {
  BookOpenIcon,
  CalculatorIcon,
  AcademicCapIcon,
  DocumentTextIcon,
  EnvelopeIcon,
  UserIcon,
  Squares2X2Icon, // <- icône dashboard
  QuestionMarkCircleIcon, // <- icône quiz
  InformationCircleIcon, // <- icône about
  UserGroupIcon // <- icône cours particuliers
} from '@heroicons/vue/24/outline'
const DashboardIcon = Squares2X2Icon;
// Centralized menu configuration for OptiTAB
// This allows easy reuse across components and consistent navigation
export const menuItems = [
  {
    key: 'dashboard',
    text: 'Tableau de bord',
    icon: DashboardIcon,
    href: '/dashboard',
    description: 'Vue d\'ensemble de votre espace personnel'
  },
  {
    key: 'calculator',
    text: 'Outil de Calcul',
    icon: CalculatorIcon,
    href: '/calculator',
    description: 'Calculatrices et outils mathématiques'
  },
  {
    key: 'cours-particuliers',
    text: 'Cours Particuliers',
    icon: UserGroupIcon,
    href: '/cours-particuliers',
    description: 'Cours particuliers personnalisés'
  },
  {
    key: 'about',
    text: 'À Propos',
    icon: InformationCircleIcon,
    href: '/about',
    description: 'En savoir plus sur OptiTAB'
  },
  {
    key: 'cours',
    text: 'Cours en Ligne',
    icon: BookOpenIcon,
    href: '/cours',
    description: 'Accédez à nos cours en ligne'
  },
  {
    key: 'exercices',
    text: 'Exercices Guidés',
    icon: AcademicCapIcon,
    href: '/exercises',
    description: 'Exercices avec solutions détaillées'
  },
  {
    key: 'quiz',
    text: 'Quiz QCM',
    icon: QuestionMarkCircleIcon,
    href: '/quiz',
    description: 'Quiz à choix multiples'
  },
  {
    key: 'fiches',
    text: 'Fiches Synthèse',
    icon: DocumentTextIcon,
    href: '/sheets',
    description: 'Résumés et fiches de révision'
  },
  {
    key: 'contact',
    text: 'Nous contacter',
    icon: EnvelopeIcon,
    href: '/contact#informations',
    external: false,
    description: 'Contactez notre équipe'
  },
  {
    key: 'login',
    text: 'Connexion',
    icon: UserIcon,
    href: '#',
    emit: 'open-login',
    description: 'Accédez à votre compte'
  },
]

// Helper function to get menu item by key
export const getMenuItemByKey = (key) => {
  return menuItems.find(item => item.key === key)
}

// Helper function to get main navigation items (excluding login)
export const getMainMenuItems = () => {
  return menuItems.filter(item => item.key !== 'login')
}

// Helper function to get authentication items
export const getAuthMenuItems = () => {
  return menuItems.filter(item => item.key === 'login')
} 