<template>
  <DashboardLayout>
    <div class="notions-page-base">
      <!-- Navigation Header -->
      <div class="nav-header-base">
        <BackButton 
          text="Retour au dashboard" 
          :customAction="goBackToDashboard"
          position="top-left"
        />
      </div>

      

      <!-- Main Content -->
      <div class="main-content-base">
        <div class="notions-container">
          <ThemeNotionsView :matiere-id="currentMatiereId" :notion-route-name="'CourseChapitres'" />
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import BackButton from '@/components/common/BackButton.vue'
import ThemeNotionsView from '@/components/common/ThemeNotionsView.vue'
import { useSubjectsStore } from '@/stores/subjects/index'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const subjectsStore = useSubjectsStore()
const userStore = useUserStore()

// Récupérer l'ID de la matière courante
const currentMatiereId = computed(() => {
  const id = subjectsStore.activeMatiereId || route.params.matiereId
  return id ? Number(id) : null
})

// Fonction pour retourner au dashboard
function goBackToDashboard() {
  router.push('/dashboard')
}
</script>

<style src="@/styles/notions-layout.css"></style>

<style scoped>
.course-notions-page {
  background: #ffffff;
  min-height: 100vh;
  /* reset local paddings to rely solely on DashboardLayout spacing */
  padding: 0;
}

/* Navigation Header */
.nav-header {
  /* no extra padding; use layout's own padding */
  padding: 0 0 1rem 0;
  background: white;
}

/* Page Title */
.page-title {
  background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
  padding: 2rem 2rem 1rem 2rem;
  color: white;
}

.page-title h1 {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Main Content */
.main-content {
  width: 100%;
  max-width: none;
  margin: 0;
  padding: 0;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* Loading Spinner */
.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top: 3px solid #60a5fa;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-state p {
  color: #64748b;
  margin: 0;
}

/* Error State */
.error-state {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.error-state p {
  color: #64748b;
  margin: 0 0 1rem 0;
}

/* Retry Button */
.retry-btn {
  background: #60a5fa;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s ease;
}

.retry-btn:hover {
  background: #3b82f6;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.empty-state p {
  color: #64748b;
  margin: 0;
}

/* Notions Container */
.notions-container {
  width: 100%;
}

/* Overrides internes pour ThemeNotionsView afin d'aligner tout à gauche */
:deep(.tnv-wrapper) {
  max-width: none;
  width: 100%;
  margin: 0;
}

:deep(.tnv-themes) {
  margin: 0;
}

:deep(.tnv-theme-block) {
  padding-left: 0;
  padding-right: 0;
}

:deep(.tnv-notions-grid) {
  padding-left: 0;
  padding-right: 0;
}

/* Themes Layout */
.themes-layout {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.theme-section {
  background: transparent;
  border: none;
  border-radius: 0;
  overflow: visible;
  box-shadow: none;
}

/* Theme Headers */
.theme-header {
  background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 8px 8px 0 0;
  margin-bottom: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.theme-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: white;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.theme-label {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 400;
}

/* Notions Grid */
.notions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
  padding: 1.5rem;
}

/* Notion Cards */
.notion-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.notion-card:hover {
  border-color: #10b981;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15);
  transform: translateY(-2px);
}

.notion-card:hover::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #10b981, #059669);
}

.card-content {
  padding: 1.5rem;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
}

.card-subtitle {
  font-size: 0.75rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 1rem 0;
  font-weight: 500;
}

.progress-bar {
  width: 100%;
  height: 4px;
  background: #f1f5f9;
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  width: 0%;
  height: 100%;
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
  border-radius: 2px;
  transition: width 0.3s ease;
}

.notion-card:hover .progress-fill {
  width: 30%;
}

/* Simple Layout */
.simple-layout .notions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

/* Responsive */
@media (max-width: 768px) {
  .nav-header {
    padding: 1rem;
  }
  
  .page-title {
    padding: 1.5rem 1rem 1rem 1rem;
  }
  
  .page-title h1 {
    font-size: 1.5rem;
  }
  
  .main-content {
    padding: 1rem;
  }
  
  .theme-header {
    padding: 1rem;
  }
  
  .theme-title {
    font-size: 1.125rem;
  }
  
  .notions-grid {
    grid-template-columns: 1fr;
    padding: 1rem;
  }
  
  .card-content {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .page-title h1 {
    font-size: 1.25rem;
  }
  
  .theme-title {
    font-size: 1rem;
  }
  
  .card-title {
    font-size: 0.9rem;
  }
}
</style> 