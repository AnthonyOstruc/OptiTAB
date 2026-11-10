// Menu de l'administration : une seule liste, utilisée par le menu latéral
// (EspaceLayout en mode admin), par la page d'accueil de l'administration
// (AdminHome) et par les titres de la barre du haut (DashboardLayout).
import {
  AcademicCapIcon,
  BanknotesIcon,
  BookOpenIcon,
  ChatBubbleLeftRightIcon,
  ClipboardDocumentCheckIcon,
  ClipboardDocumentListIcon,
  DocumentDuplicateIcon,
  DocumentTextIcon,
  EnvelopeIcon,
  FilmIcon,
  GlobeAltIcon,
  NewspaperIcon,
  PhotoIcon,
  QuestionMarkCircleIcon,
  Squares2X2Icon,
  TagIcon,
  TicketIcon,
  UserGroupIcon
} from '@heroicons/vue/24/outline'

export const ADMIN_ACCUEIL = '/admin'

export const ADMIN_SECTIONS = [
  {
    titre: 'Contenus',
    items: [
      { label: 'Cours', description: 'Modifier les cours des chapitres.', to: '/admin/cours', icon: BookOpenIcon },
      { label: 'Exercices', description: 'Gérer les exercices corrigés.', to: '/admin/exercices', icon: ClipboardDocumentListIcon },
      { label: 'Fiches', description: 'Publier les fiches de synthèse et tables.', to: '/admin/sheets', icon: DocumentTextIcon },
      { label: 'Quiz', description: 'Administrer les quiz des chapitres.', to: '/admin/quiz', icon: QuestionMarkCircleIcon },
      { label: 'Notation des quiz', description: 'Corriger les quiz rendus.', to: '/admin/quiz-submissions', icon: ClipboardDocumentCheckIcon }
    ]
  },
  {
    titre: 'Structure du programme',
    items: [
      { label: 'Pays', description: 'Configurer les pays disponibles.', to: '/admin/pays', icon: GlobeAltIcon },
      { label: 'Niveaux', description: 'Gérer les classes et niveaux.', to: '/admin/niveaux', icon: AcademicCapIcon },
      { label: 'Matières', description: 'Organiser les matières.', to: '/admin/matieres', icon: BookOpenIcon },
      { label: 'Thèmes', description: 'Classer les thèmes par matière.', to: '/admin/themes', icon: Squares2X2Icon },
      { label: 'Notions', description: 'Gérer les notions et chapitres.', to: '/admin/notions', icon: TagIcon }
    ]
  },
  {
    titre: 'Contenus avancés',
    items: [
      { label: 'Cours PDF', description: 'Vérifier les exports PDF des cours.', to: '/admin/cours-pdf', icon: DocumentDuplicateIcon },
      { label: 'Cours+', description: 'Gérer les contenus de cours avancés.', to: '/admin/cours-plus', icon: BookOpenIcon },
      { label: 'Exercices+', description: 'Gérer les exercices avancés.', to: '/admin/exercices-plus', icon: ClipboardDocumentCheckIcon },
      { label: 'Quiz+', description: 'Gérer les quiz avancés.', to: '/admin/quiz-plus', icon: QuestionMarkCircleIcon }
    ]
  },
  {
    titre: 'Vidéos et communication',
    items: [
      { label: 'Reel Studio', description: 'Créer des vidéos pédagogiques 9:16.', to: '/admin/reel-studio', icon: FilmIcon },
      { label: 'Fonds vidéo', description: 'Créer les fonds des vidéos courtes.', to: '/admin/reel-background', icon: PhotoIcon },
      { label: 'Témoignages', description: 'Publier les avis WhatsApp et SMS.', to: '/admin/temoignages', icon: ChatBubbleLeftRightIcon },
      { label: 'Newsletter', description: 'Piloter les envois de la newsletter.', to: '/admin/newsletter', icon: EnvelopeIcon },
      { label: 'Ancien blog', description: 'Anciens articles (le blog en ligne est publié depuis le site).', to: '/admin/blog', icon: NewspaperIcon }
    ]
  },
  {
    titre: 'Abonnements',
    items: [
      { label: 'Offres', description: 'Configurer les formules d’abonnement.', to: '/admin/subscriptions', icon: BanknotesIcon },
      { label: 'Abonnés', description: 'Suivre les abonnés actifs.', to: '/admin/subscribers', icon: UserGroupIcon },
      { label: 'Passes', description: 'Gérer les accès temporaires.', to: '/admin/passes', icon: TicketIcon }
    ]
  }
]

export const ADMIN_PAGES = ADMIN_SECTIONS.flatMap((s) => s.items)

// Page d'administration correspondant à une adresse (la plus longue qui convient).
export const pageAdmin = (path) =>
  ADMIN_PAGES.filter((p) => path === p.to || path.startsWith(`${p.to}/`)).sort((a, b) => b.to.length - a.to.length)[0] || null
