<template>
  <!-- Administration : ancienne coque, inchangée. -->
  <DashboardLayoutClassic v-if="classique">
    <slot />
  </DashboardLayoutClassic>

  <!-- Visiteur non connecté (outil de calcul) : en-tête et pied de page de la vitrine. -->
  <VitrineLayout v-else-if="!userStore.isAuthenticated">
    <div class="dl-public">
      <div v-if="page.sousEntete" class="dl-public__sub"><component :is="page.sousEntete" /></div>
      <slot />
    </div>
  </VitrineLayout>

  <!-- Élèves et parents : nouvel espace. -->
  <EspaceLayout v-else :title="page.titre" :back="page.retour" :pleine-largeur="Boolean(page.pleineLargeur)">
    <template v-if="page.sousEntete" #subheader>
      <component :is="page.sousEntete" />
    </template>
    <slot />
  </EspaceLayout>
</template>

<script setup>
// Toutes les pages connectées passent par ce composant. Depuis le 2026-11-03,
// il affiche le nouvel espace (EspaceLayout) ; l'ancienne coque est conservée
// dans DashboardLayoutClassic.vue pour l'administration (et un retour arrière).
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import DashboardLayoutClassic from './DashboardLayoutClassic.vue'
import EspaceLayout from '@/components/espace/EspaceLayout.vue'
import VitrineLayout from '@/components/vitrine/VitrineLayout.vue'
import CalculatorTabs from '@/components/calculator/CalculatorTabs.vue'
import BillingTabs from '@/components/payments/BillingTabs.vue'
import { useUserStore } from '@/stores/user'
import { ESPACE_ROUTES } from '@/config/espace'

const route = useRoute()
const userStore = useUserStore()

const classique = computed(() => String(route.path || '').startsWith('/admin'))

const ACCUEIL = { to: ESPACE_ROUTES.accueil, label: 'Retour à l’accueil' }
const QUIZ = { to: '/quiz', label: 'Retour aux quiz' }

// Titre (téléphone), flèche retour et éventuels onglets propres à chaque page.
const PAGES = {
  Account: { titre: 'Mon compte', retour: ACCUEIL },
  Billing: { titre: 'Abonnement', retour: ACCUEIL, sousEntete: BillingTabs },
  Subscription: { titre: 'Mon abonnement', retour: { to: '/billing', label: 'Retour aux formules' } },
  Pricing: { titre: 'Formules', retour: ACCUEIL },
  ExercisesHistory: { titre: 'Historique', retour: ACCUEIL },
  QuizzesHistory: { titre: 'Historique des quiz', retour: ACCUEIL },
  QuizSubmissionsStudent: { titre: 'Mes quiz rendus', retour: ACCUEIL },
  Quiz: { titre: 'Quiz', retour: ACCUEIL },
  QuizNotions: { titre: 'Quiz', retour: ACCUEIL },
  QuizByNotion: { titre: 'Quiz du chapitre', retour: QUIZ },
  QuizHomeworkByNotion: { titre: 'Devoir', retour: QUIZ },
  QuizComingSoon: { titre: 'Quiz', retour: ACCUEIL },
  Calculator: { titre: 'Outil de calcul', sousEntete: CalculatorTabs, pleineLargeur: true },
  CoursParticuliers: { titre: 'Cours particuliers', retour: ACCUEIL },
  ExerciceDetail: { titre: 'Exercice', retour: { to: ESPACE_ROUTES.chapitres, label: 'Retour à mes chapitres' } }
}

const page = computed(() => PAGES[route.name] || { titre: '', retour: null })
</script>

<style scoped>
.dl-public {
  max-width: 1280px;
  margin: 0 auto;
  padding: 24px 16px 48px;
}

.dl-public__sub {
  margin-bottom: 20px;
}
</style>
