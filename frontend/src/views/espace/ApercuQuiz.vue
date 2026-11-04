<template>
  <div class="es apercu-quiz">
    <!-- ?notes=1 : cartes « Mes quiz » (élève) et « Notes aux quiz » (parent) avec des notes d'exemple -->
    <div v-if="route.query.notes" class="apercu-notes">
      <QuizNotes :chapitres="exemple" />
      <QuizNotes :chapitres="exemple" parent />
      <QuizNotes :chapitres="[{ id: route.params.notionId, titre: 'Fonction exponentielle' }]" />
    </div>
    <ChapitreQuiz v-else :notion-id="route.params.notionId" />
  </div>
</template>

<script setup>
// Aperçu local d'un quiz (route déclarée seulement en développement) : permet
// de relire et de photographier un quiz du chantier sans compte élève.
import { useRoute } from 'vue-router'
import ChapitreQuiz from '@/components/espace/ChapitreQuiz.vue'
import QuizNotes from '@/components/espace/QuizNotes.vue'
import '@/styles/espace.css'

const route = useRoute()
const ilYa = (jours) => new Date(Date.now() - jours * 86400000).toISOString()
const exemple = [
  { id: 85, titre: 'Fonction exponentielle', quiz: { derniere: 16.3, meilleure: 17.5, essais: 3, quand: ilYa(0.1), a_revoir: ['Limites'] } },
  { id: 86, titre: 'Fonction logarithme népérien', quiz: { derniere: 11.3, meilleure: 11.3, essais: 1, quand: ilYa(2), a_revoir: ['Fonctions de la forme $e^{u}$', 'Un modèle exponentiel'] } },
  { id: 87, titre: 'Dérivation et convexité', quiz: { derniere: 7.5, meilleure: 7.5, essais: 1, quand: ilYa(5), a_revoir: [] } }
]
</script>

<style scoped>
.apercu-quiz {
  min-height: 100vh;
  padding: 24px 16px 48px;
  background: var(--es-bg);
}

.apercu-notes {
  display: grid;
  gap: 20px;
  max-width: 420px;
  margin: 0 auto;
}
</style>
