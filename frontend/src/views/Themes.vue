<template>
  <DashboardLayout>
    <section class="themes-section">
      <!-- Bouton de retour vers le dashboard -->
      <BackButton 
        text="Retour au dashboard" 
        :customAction="goBackToMatieres"
        position="top-left"
      />

      <!-- Contenu principal -->
      <div class="themes-content">
        <ThemeNotionsView :matiere-id="currentMatiereId" :notion-route-name="'Chapitres'" />
      </div>
    </section>
  </DashboardLayout>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import { getMatieresUtilisateur } from '@/api'
import ThemeNotionsView from '@/components/common/ThemeNotionsView.vue'
import SelectedMatiereHeader from '@/components/common/SelectedMatiereHeader.vue'
import { useSubjectsStore } from '@/stores/subjects/index'
import { useUserStore } from '@/stores/user'
import BackButton from '@/components/common/BackButton.vue'

const route = useRoute()
const router = useRouter()
const subjectsStore = useSubjectsStore()
const userStore = useUserStore()

// Fonction pour revenir aux matières
function goBackToMatieres() {
  router.push({ name: 'Dashboard' })
}

// Utiliser la matière active du store ou celle de la route (string->number normalisé)
const currentMatiereId = computed(() => {
  const id = subjectsStore.activeMatiereId || route.params.matiereId
  return id ? Number(id) : null
})

// Fonction appelée quand on clique sur un thème
function onThemeClick(themeId) {
  router.push({ name: 'ThemeNotions', params: { themeId } })
}

function onMatiereChanged(newMatiereId) {
  if (newMatiereId && Number(newMatiereId) !== Number(currentMatiereId.value)) {
    router.push({ name: 'Themes', params: { matiereId: String(newMatiereId) } })
  }
}

// Fonction appelée quand on clique sur une notion (fallback)
function onNotionClick(notionId) {
  router.push({ name: 'Chapitres', params: { notionId } })
}

// Le composant enfant gère le chargement et le cache
</script>

<style scoped>
.themes-section {
  background: #ffffff;
  min-height: 100vh;
  padding: 1rem 5vw 3rem 5vw;
}

/* En-tête */
.themes-header { display: none; }

.themes-header-content {
  flex: 1;
}

.themes-title { display: none; }

.themes-subtitle { display: none; }

.themes-header-icon { display: none; }

/* Contenu principal */
.themes-content {
  max-width: 1200px;
  margin: 0 auto;
}

/* Liste H2 + notions */
.themes-list .theme-block {
  background: #ffffff;
  border-radius: 16px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.08);
}

.theme-block-title {
  font-size: 1.5rem;
  font-weight: 800;
  margin: 0 0 0.75rem 0;
  color: #1e293b;
}

.no-notions {
  color: #64748b;
  font-style: italic;
}

/* Chargement et erreurs */
.themes-loader,
.themes-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.loader-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 64px;
  height: 64px;
  background: #fef2f2;
  border-radius: 16px;
  color: #ef4444;
  margin-bottom: 1rem;
}

.retry-button {
  background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3);
}

/* Grilles */
.themes-grid,
.notions-grid {
  width: 100%;
}

.themes-grid-inner,
.notions-grid-inner {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  justify-items: center;
}

/* Fallback sans thèmes */
.no-themes-fallback {
  background: #ffffff;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.fallback-header {
  text-align: center;
  margin-bottom: 2rem;
}

.fallback-header h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.fallback-header p {
  color: #64748b;
  margin: 0;
}

/* État vide */
.themes-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 80px;
  height: 80px;
  background: #f1f5f9;
  border-radius: 20px;
  color: #64748b;
  margin-bottom: 1.5rem;
}

/* Animations */
.theme-card-enter-active,
.notion-card-enter-active {
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.theme-card-enter-from,
.notion-card-enter-from {
  opacity: 0;
  transform: translateY(30px) scale(0.9);
}

.theme-card-enter-to,
.notion-card-enter-to {
  opacity: 1;
  transform: translateY(0) scale(1);
}

/* Responsive */
@media (max-width: 1024px) {
  .themes-section {
    padding: 1.5rem 3vw 3rem 3vw;
  }
  
  .themes-grid-inner,
  .notions-grid-inner {
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
  }
}

@media (max-width: 768px) {
  .themes-section {
    padding: 1rem 2vw 2rem 2vw;
  }
  
  .themes-header {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
    padding: 1.25rem;
  }
  
  .themes-title {
    font-size: 1.75rem;
  }
  
  .themes-grid-inner,
  .notions-grid-inner {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
</style>
