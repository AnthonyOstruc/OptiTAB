import { menuItems } from './menuItems'

// On affiche Tableau de bord puis les autres éléments principaux du header home
const dashboardMenu = menuItems.filter(item => ['dashboard', 'cours', 'calculator', 'exercices', 'quiz', 'fiches'].includes(item.key))

export default dashboardMenu 