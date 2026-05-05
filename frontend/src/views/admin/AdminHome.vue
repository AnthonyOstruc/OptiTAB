<template>
  <main class="admin-home">
    <header class="admin-home__header">
      <div>
        <p class="admin-home__eyebrow">Administration</p>
        <h1>Tableau de bord admin</h1>
      </div>
      <RouterLink to="/blog" class="admin-home__preview">
        <NewspaperIcon />
        Voir le blog
      </RouterLink>
    </header>

    <section
      v-for="section in sections"
      :key="section.title"
      class="admin-section"
    >
      <h2>{{ section.title }}</h2>
      <div class="admin-grid">
        <RouterLink
          v-for="item in section.items"
          :key="item.to"
          :to="item.to"
          class="admin-tile"
        >
          <span class="admin-tile__icon">
            <component :is="item.icon" />
          </span>
          <span class="admin-tile__body">
            <span class="admin-tile__title">{{ item.label }}</span>
            <span class="admin-tile__description">{{ item.description }}</span>
          </span>
          <ChevronRightIcon class="admin-tile__arrow" />
        </RouterLink>
      </div>
    </section>
  </main>
</template>

<script setup>
import {
  AcademicCapIcon,
  BanknotesIcon,
  BookOpenIcon,
  ChartBarIcon,
  ClipboardDocumentCheckIcon,
  ClipboardDocumentListIcon,
  DocumentTextIcon,
  EnvelopeIcon,
  FilmIcon,
  GlobeAltIcon,
  NewspaperIcon,
  QuestionMarkCircleIcon,
  Squares2X2Icon,
  TagIcon,
  TrophyIcon,
  UserGroupIcon,
  ChevronRightIcon,
} from '@heroicons/vue/24/outline'

const sections = [
  {
    title: 'Configuration',
    items: [
      { label: 'Pays', description: 'Configurer les pays disponibles.', to: '/admin/pays', icon: GlobeAltIcon },
      { label: 'Niveaux', description: 'Gérer les niveaux scolaires.', to: '/admin/niveaux', icon: AcademicCapIcon },
    ],
  },
  {
    title: 'Structure pédagogique',
    items: [
      { label: 'Matières', description: 'Organiser les matières principales.', to: '/admin/matieres', icon: BookOpenIcon },
      { label: 'Thèmes', description: 'Classer les thèmes par matière.', to: '/admin/themes', icon: Squares2X2Icon },
      { label: 'Notions', description: 'Gérer les notions et chapitres.', to: '/admin/notions', icon: TagIcon },
    ],
  },
  {
    title: 'Contenus',
    items: [
      { label: 'Cours', description: 'Modifier les cours classiques.', to: '/admin/cours', icon: BookOpenIcon },
      { label: 'Exercices', description: 'Gérer les exercices guidés.', to: '/admin/exercices', icon: ClipboardDocumentListIcon },
      { label: 'Quiz', description: 'Administrer les QCM.', to: '/admin/quiz', icon: QuestionMarkCircleIcon },
      { label: 'Fiches', description: 'Publier les fiches et tables.', to: '/admin/sheets', icon: DocumentTextIcon },
      { label: 'Blog', description: 'Créer et valider les articles.', to: '/admin/blog', icon: NewspaperIcon },
    ],
  },
  {
    title: 'Contenus avancés',
    items: [
      { label: 'PDF cours', description: 'Vérifier les exports PDF.', to: '/admin/cours-pdf', icon: DocumentTextIcon },
      { label: 'Cours+', description: 'Gérer les contenus premium cours.', to: '/admin/cours-plus', icon: BookOpenIcon },
      { label: 'Exercices+', description: 'Gérer les exercices premium.', to: '/admin/exercices-plus', icon: ClipboardDocumentCheckIcon },
      { label: 'Quiz+', description: 'Gérer les quiz premium.', to: '/admin/quiz-plus', icon: QuestionMarkCircleIcon },
      { label: 'Reel Studio', description: 'Créer des reels pédagogiques 9:16.', to: '/admin/reel-studio', icon: FilmIcon },
      { label: 'Canva', description: 'Créer les fonds pour vidéos courtes.', to: '/admin/reel-background', icon: FilmIcon },
    ],
  },
  {
    title: 'Communication et paiements',
    items: [
      { label: 'Newsletter', description: 'Piloter les envois newsletter.', to: '/admin/newsletter', icon: EnvelopeIcon },
      { label: 'Abonnements', description: 'Configurer les offres.', to: '/admin/subscriptions', icon: BanknotesIcon },
      { label: 'Abonnés', description: 'Suivre les abonnés actifs.', to: '/admin/subscribers', icon: UserGroupIcon },
      { label: 'Passes', description: 'Gérer les accès temporaires.', to: '/admin/passes', icon: ClipboardDocumentCheckIcon },
      { label: 'Notation quiz', description: 'Corriger les quiz rendus.', to: '/admin/quiz-submissions', icon: ClipboardDocumentListIcon },
    ],
  },
  {
    title: 'Jeu Arena (privé tant que non publié)',
    items: [
      { label: 'Tableau de bord', description: 'KPIs, configuration et publication du jeu.', to: '/admin/arena', icon: ChartBarIcon },
      { label: 'Chapitres Arena', description: 'Créer et organiser les chapitres du jeu.', to: '/admin/arena/chapters', icon: TrophyIcon },
      { label: 'Niveaux Arena', description: 'Gérer les niveaux, difficulté et accès premium.', to: '/admin/arena/levels', icon: Squares2X2Icon },
      { label: 'Questions Arena', description: 'Éditer les énoncés, réponses et explications.', to: '/admin/arena/questions', icon: QuestionMarkCircleIcon },
    ],
  },
]
</script>

<style scoped>
.admin-home {
  width: 100%;
  padding: 24px 24px 96px;
  background: #f8fafc;
  min-height: 100%;
}

.admin-home__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 28px;
}

.admin-home__eyebrow {
  margin: 0 0 4px;
  color: #2563eb;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
}

.admin-home h1 {
  margin: 0;
  color: #0f172a;
  font-size: 30px;
  line-height: 1.2;
}

.admin-home__preview {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: 8px;
  background: #2563eb;
  color: #fff;
  text-decoration: none;
  font-weight: 700;
}

.admin-home__preview svg {
  width: 20px;
  height: 20px;
}

.admin-section {
  margin-bottom: 28px;
}

.admin-section:last-child {
  margin-bottom: 160px;
}

.admin-section h2 {
  margin: 0 0 12px;
  color: #334155;
  font-size: 15px;
  font-weight: 800;
  text-transform: uppercase;
}

.admin-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 12px;
}

.admin-tile {
  display: grid;
  grid-template-columns: 42px 1fr 18px;
  align-items: center;
  gap: 12px;
  min-height: 86px;
  padding: 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #fff;
  color: inherit;
  text-decoration: none;
  transition: border-color 0.16s ease, box-shadow 0.16s ease, transform 0.16s ease;
}

.admin-tile:hover {
  border-color: #93c5fd;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
  transform: translateY(-1px);
}

.admin-tile__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 8px;
  background: #eff6ff;
  color: #2563eb;
}

.admin-tile__icon svg,
.admin-tile__arrow {
  width: 21px;
  height: 21px;
}

.admin-tile__body {
  min-width: 0;
}

.admin-tile__title {
  display: block;
  margin-bottom: 4px;
  color: #0f172a;
  font-size: 16px;
  font-weight: 800;
}

.admin-tile__description {
  display: block;
  color: #64748b;
  font-size: 13px;
  line-height: 1.35;
}

.admin-tile__arrow {
  color: #94a3b8;
}

@media (max-width: 768px) {
  .admin-home {
    padding: 18px 14px 84px;
  }

  .admin-home__header {
    align-items: flex-start;
    flex-direction: column;
  }

  .admin-home h1 {
    font-size: 24px;
  }

  .admin-grid {
    grid-template-columns: 1fr;
  }
}
</style>
