<template>
  <DashboardLayout>
    <section class="homework-section">
      <div class="nav-header-base">
        <BackButton
          text="Retour"
          :customAction="goBack"
          position="top-left-dashboard"
        />
      </div>

      <div class="homework-card">
        <header class="homework-header">
          <div class="homework-meta">
            <span class="homework-chip">Notion #{{ notionId }}</span>
            <h2 class="homework-title">Énoncé d'exercice</h2>
            <p class="homework-subtitle">
              Collez ou rédigez ici l'énoncé complet. Aucune question à choix multiple n'est affichée.
            </p>
          </div>
        </header>

        <div class="homework-body">
          <div class="statement-card">
            <h3 class="statement-heading">Énoncé</h3>
            <div class="statement-content" v-html="homeworkStatement"></div>
            <div v-if="!homeworkStatement" class="statement-placeholder">
              Aucun énoncé enregistré pour l'instant. Ajoutez le texte de l'exercice.
            </div>
          </div>
        </div>
      </div>
    </section>
  </DashboardLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import BackButton from '@/components/common/BackButton.vue'

const route = useRoute()
const router = useRouter()
const notionId = route.params.notionId

// Placez ici le texte de l'énoncé. Laisser vide pour afficher le placeholder.
const homeworkStatement = ref('')

function goBack() {
  router.back()
}
</script>

<style scoped>
.homework-section {
  padding: 1rem 0 2rem;
}

.homework-card {
  max-width: 1024px;
  margin: 0 auto;
  padding: 0 1rem 2rem;
}

.homework-header {
  margin-bottom: 1.25rem;
}

.homework-meta {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.homework-chip {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.6rem;
  background: #eef2ff;
  color: #4338ca;
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.9rem;
  width: fit-content;
}

.homework-title {
  margin: 0;
  font-size: 1.4rem;
  font-weight: 800;
  color: #0f172a;
}

.homework-subtitle {
  margin: 0;
  color: #475569;
  font-size: 0.98rem;
}

.statement-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 1.2rem 1.4rem;
  box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
}

.statement-heading {
  margin: 0 0 0.75rem 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: #0f172a;
}

.statement-content {
  white-space: pre-wrap;
  color: #111827;
  line-height: 1.5;
  font-size: 1rem;
}

.statement-placeholder {
  color: #94a3b8;
  font-style: italic;
  font-size: 0.98rem;
}
</style>
