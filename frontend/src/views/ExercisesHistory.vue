<template>
  <DashboardLayout>
    <div class="history-page">
      <h2 class="page-title">Historique complet des exercices</h2>

      <BaseHistory
        title="🧭 Historique des Exercices"
        list-title="📝 Tous mes exercices"
        loading-text="Chargement de l'historique..."
        api-endpoint="/api/suivis/exercices/stats/"
        :items-per-page="12"
        :navigation-handler="navigateToExercice"
      >
        <!-- Tableau résumé matière/notion -->
        <template #matiere-notion-stats="{ stats }">
          <div class="summary-table">
            <div class="summary-header">
              <div>Matière</div>
              <div>Notion</div>
              <div>Faits</div>
              <div>Réussis</div>
              <div>Ratés</div>
            </div>
            <div v-for="row in stats" :key="`${row.matiere.id}-${row.notion.id}`" class="summary-row">
              <div class="cell matiere">{{ row.matiere.titre }}</div>
              <div class="cell notion">{{ row.notion.titre }}</div>
              <div class="cell count">{{ row.exercice_count }}</div>
              <div class="cell correct">{{ row.correct_count }}</div>
              <div class="cell incorrect">{{ row.incorrect_count }}</div>
            </div>
          </div>
        </template>

        <!-- Liste des items → gérée par BaseHistory avec pagination -->
      </BaseHistory>
    </div>
  </DashboardLayout>
  
</template>

<script setup>
import { useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import BaseHistory from '@/components/dashboard/BaseHistory.vue'

const router = useRouter()

const navigateToExercice = (exercice) => {
  router.push({ name: 'ExerciceDetail', params: { exerciceId: String(exercice.exercice_id) } })
}
</script>

<style scoped>
.history-page { padding: 1rem 0; }
.page-title { font-weight: 800; margin-bottom: 1rem; }

.summary-table {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  background: #fff;
  margin-bottom: 1.25rem;
}
.summary-header,
.summary-row {
  display: grid;
  grid-template-columns: 1.5fr 2fr 0.8fr 0.8fr 0.8fr;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  align-items: center;
}
.summary-header { background: #f9fafb; font-weight: 700; color: #374151; }
.summary-row:not(:last-child) { border-bottom: 1px solid #f3f4f6; }
.summary-row .cell { font-size: 0.875rem; color: #374151; }
.summary-row .cell.correct { color: #059669; font-weight: 600; }
.summary-row .cell.incorrect { color: #dc2626; font-weight: 600; }

@media (max-width: 768px) {
  .summary-header, .summary-row { grid-template-columns: 1fr 1fr 0.7fr 0.7fr 0.7fr; padding: 0.5rem 0.75rem; }
}
</style>


