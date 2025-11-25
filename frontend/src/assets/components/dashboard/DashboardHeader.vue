<template>
  <header class="dashboard-header">
    <!-- Bouton burger fixe en position absolue -->
    <button 
      :class="['burger-btn-fixed', { 'burger-collapsed': sidebarCollapsed, 'sidebar-hidden': !sidebarOpen }]" 
      type="button"
      @click="$emit('toggle-sidebar')" 
      aria-label="Ouvrir ou fermer le menu"
      :aria-pressed="sidebarCollapsed.toString()"
      :aria-expanded="(!sidebarCollapsed).toString()"
    >
      <span class="burger-icon-fixed" :class="{ 'burger-icon-collapsed': sidebarCollapsed }">&#9776;</span>
    </button>

    <!-- Navigation admin (visible uniquement dans les pages admin) -->
    <nav v-if="isAdminPage" class="admin-nav">
      <!-- Groupe 1: Configuration -->
      <div class="nav-group">
        <router-link to="/admin/pays" class="admin-link" :class="{ active: isActive('AdminPays') }">Pays</router-link>
        <router-link to="/admin/niveaux" class="admin-link" :class="{ active: isActive('AdminNiveaux') }">Niveaux</router-link>
      </div>
      
      <div class="nav-separator"></div>
      
      <!-- Groupe 2: Structure/Curriculum -->
      <div class="nav-group">
        <router-link to="/admin/matieres" class="admin-link" :class="{ active: isActive('AdminMatieres') }">Matières</router-link>
        <router-link to="/admin/themes" class="admin-link" :class="{ active: isActive('AdminThemes') }">Thèmes</router-link>
        <router-link to="/admin/notions" class="admin-link" :class="{ active: isActive('AdminNotions') }">Notions</router-link>
        <!-- Chapitres supprimés -->
      </div>
      
      <div class="nav-separator"></div>
      
      <!-- Groupe 3: Contenu de base -->
      <div class="nav-group">
        <router-link to="/admin/cours" class="admin-link" :class="{ active: isActive('AdminCours') }">Cours</router-link>
        <router-link to="/admin/exercices" class="admin-link" :class="{ active: isActive('AdminExercices') }">Exercices</router-link>
        <router-link to="/admin/quiz" class="admin-link" :class="{ active: isActive('AdminQuiz') }">Quiz</router-link>
      </div>
      
      <div class="nav-separator"></div>
      
      <!-- Groupe 4: Contenu avancé -->
      <div class="nav-group">
        <router-link to="/admin/cours-plus" class="admin-link" :class="{ active: isActive('AdminCoursPlus') }">Cours+</router-link>
        <router-link to="/admin/exercices-plus" class="admin-link" :class="{ active: isActive('AdminExercicesPlus') }">Exercices+</router-link>
        <router-link to="/admin/quiz-plus" class="admin-link" :class="{ active: isActive('AdminQuizPlus') }">Quiz+</router-link>
      </div>
      
      <div class="nav-separator"></div>
      
      <!-- Groupe 5: Fiches -->
      <div class="nav-group">
        <router-link to="/admin/sheets" class="admin-link" :class="{ active: isActive('AdminSheets') }">Fiches</router-link>
      </div>
    </nav>

    <!-- Section centrale : Contenu conditionnel (masqué si admin) -->
    <ConditionalHeader 
      v-if="!isCalculatorPage && !isAdminPage"
      :matiere-props="{ matiereId: null }"
      @subject-changed="handleSubjectChange"
      @search="handleSearch"
    />

    <!-- Section droite : Notifications, messages et menu utilisateur -->
    <div class="header-right">
      <!-- Centre de notifications -->
      <NotificationCenter />

      <!-- Menu utilisateur -->
      <UserMenu @logout="handleLogout" />
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import UserMenu from './UserMenu.vue'
import ConditionalHeader from '@/components/common/ConditionalHeader.vue'
import NotificationCenter from '@/components/notifications/NotificationCenter.vue'

// Émissions d'événements
const emit = defineEmits(['toggle-sidebar', 'subject-changed', 'search'])

defineProps({
  sidebarOpen: {
    type: Boolean,
    default: true
  },
  sidebarCollapsed: {
    type: Boolean,
    default: false
  }
})

// Router
const router = useRouter()
const route = useRoute()

// Computed properties
const isCalculatorPage = computed(() => route.name === 'Calculator')
const isAdminPage = computed(() => {
  const path = route.path || '';
  return path.startsWith('/admin') && !path.startsWith('/admin/newsletter') && !path.startsWith('/admin/subscriptions')
})

// Fonction pour déterminer si un onglet admin est actif
function isActive(routeName) {
  return route.name === routeName
}

// Gestionnaires d'événements
const handleSubjectChange = (subjectId) => {
  emit('subject-changed', subjectId)
}

const handleSearch = (searchTerm) => {
  emit('search', searchTerm)
}

// Gestionnaire de déconnexion depuis le menu utilisateur
const handleLogout = () => {
  // La déconnexion est gérée dans le composant UserMenu
  // On peut ajouter ici une logique supplémentaire si nécessaire
  console.log('Déconnexion effectuée depuis le header')
}
</script>

<style scoped>
/* Header principal - Layout professionnel */
.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  padding: 0.7rem 2rem 0.7rem 4rem; /* Padding gauche augmenté pour le burger */
  min-height: 64px;
  position: sticky;
  top: 0;
  z-index: 12001; /* Toujours au-dessus du contenu du dashboard */
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  flex-shrink: 0;

}

/* Bouton burger fixe - Solution professionnelle */
.burger-btn-fixed {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: auto;
  background: #ecfdf5;
  border: 1px solid #34d399;
  border-radius: 8px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(16, 185, 129, 0.25);
  z-index: 101;
  transition: background-color 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.burger-btn-fixed:hover {
  background: #dcfce7;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
  border-color: #059669;
}

.burger-btn-fixed:active {
  background: #bbf7d0;
  box-shadow: 0 2px 10px rgba(16, 185, 129, 0.2);
}

.burger-icon-fixed {
  font-size: 1.5rem;
  color: #047857;
  transition: color 0.2s ease;
  font-weight: 500;
}

.burger-btn-fixed:hover .burger-icon-fixed {
  color: #065f46;
}

.burger-btn-fixed.burger-collapsed {
  border-color: #f97316;
  background: #fff7ed;
  box-shadow: 0 8px 22px rgba(249, 115, 22, 0.3);
}

.burger-btn-fixed.burger-collapsed::after {
  content: '';
  position: absolute;
  inset: -10px;
  border-radius: 50%;
  border: 2px solid rgba(249, 115, 22, 0.5);
  animation: burgerHalo 1.8s ease-in-out infinite;
  pointer-events: none;
}

.burger-btn-fixed.burger-collapsed .burger-icon-fixed {
  color: #c2410c;
}

.burger-btn-fixed.sidebar-hidden {
  border-color: #dc2626;
  background: #fee2e2;
  box-shadow: 0 10px 26px rgba(220, 38, 38, 0.25);
}

.burger-btn-fixed.sidebar-hidden .burger-icon-fixed {
  color: #991b1b;
}

.burger-btn-fixed.sidebar-hidden::after {
  content: '';
  position: absolute;
  inset: -10px;
  border-radius: 50%;
  border: 2px solid rgba(220, 38, 38, 0.5);
  animation: burgerHalo 1.8s ease-in-out infinite;
  pointer-events: none;
}

.burger-icon-fixed.burger-icon-collapsed {
  animation: burgerIconPulse 1.5s ease-in-out infinite;
}

@keyframes burgerHalo {
  0% {
    transform: scale(0.85);
    opacity: 0.55;
  }
  60% {
    transform: scale(1.2);
    opacity: 0;
  }
  100% {
    transform: scale(1.25);
    opacity: 0;
  }
}

@keyframes burgerIconPulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.12);
  }
}

/* Section centrale */
.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
  max-width: 600px;
  margin: 0 2rem;
  min-width: 0;
  overflow: hidden;
}

/* Container de recherche */
.search-container {
  position: relative;
  width: 100%;
  max-width: 400px;
}

/* Barre de recherche */
.header-search {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  font-size: 1rem;
  background: #f8fafc;
  transition: all 0.2s ease;
  color: #374151;
}

.header-search::placeholder {
  color: #9ca3af;
}

.header-search:focus {
  outline: none;
  border-color: #2563eb;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.header-search:hover {
  border-color: #d1d5db;
  background: #fff;
}

/* Icône de recherche */
.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1rem;
  color: #9ca3af;
  pointer-events: none;
}

/* Section droite */
.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-shrink: 0;
  margin-left: auto; /* Garantit l'alignement à droite même si le centre est en position absolue */
  max-width: 42vw;
  overflow: visible;
  /* Important: ne pas bloquer les clics sur la zone centrale quand il y a de l'espace vide */
  pointer-events: none;
}

/* Réactiver les interactions pour le contenu réel du bloc droit */
.header-right > * {
  pointer-events: auto;
}

/* Boutons d'icônes */
.header-icon {
  background: none;
  border: none;
  font-size: 1.35rem;
  cursor: pointer;
  color: #64748b;
  transition: all 0.2s ease;
  padding: 0.5rem;
  border-radius: 8px;
  position: relative;
}

.header-icon:hover {
  color: #2563eb;
  background: #f1f5f9;
  transform: translateY(-1px);
}

.header-icon:active {
  transform: translateY(0);
}

/* Navigation admin dans le header */
.admin-nav {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  flex: 1;
  flex-wrap: wrap;
  overflow-x: auto;
  padding: 0.25rem 0;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE et Edge */
}

.admin-nav::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

.nav-group {
  display: flex;
  gap: 0.4rem;
  align-items: center;
}

.nav-separator {
  width: 1px;
  height: 20px;
  background: #d1d5db;
  margin: 0 0.15rem;
  flex-shrink: 0;
}

.admin-link {
  text-decoration: none;
  color: #374151;
  font-weight: 600;
  padding: 6px 10px;
  border-radius: 6px;
  transition: all 0.2s ease;
  font-size: 0.85rem;
  white-space: nowrap;
  flex-shrink: 0;
}

.admin-link:hover {
  background: #f3f4f6;
  color: #6366f1;
}

.admin-link.active {
  background: #6366f1;
  color: #fff;
  box-shadow: 0 2px 4px rgba(99, 102, 241, 0.2);
}

/* Styles pour le composant NotificationCenter intégré */

/* Responsive design professionnel */
@media (max-width: 1200px) {
  .dashboard-header {
    padding: 0.7rem 1.5rem 0.7rem 3.5rem;
  }
  
  .header-center {
    margin: 0 1.5rem;
    justify-content: center;
  }
  
  .search-container {
    max-width: 350px;
  }
}

@media (max-width: 1024px) {
  .dashboard-header {
    padding: 0.7rem 1rem 0.7rem 3rem;
    min-height: 60px;
  }
  .burger-btn-fixed { left: 0.7rem; }
  
  .header-center {
    margin: 0 1rem;
    min-width: 200px;
    justify-content: center;
  }
  
  .search-container {
    max-width: 300px;
  }
}

@media (max-width: 768px) {
  .dashboard-header {
    padding: 0.6rem 0.7rem 0.6rem 2.8rem;
    min-height: 56px;
  }
  .burger-btn-fixed { left: 0.6rem; }
  
  .header-center {
    margin: 0 0.5rem;
    min-width: 150px;
    max-width: none;
    justify-content: center;
  }
  
  .header-right {
    gap: 0.5rem;
  }
  
  .header-icon {
    font-size: 1.2rem;
    padding: 0.4rem;
  }
  
  .header-bell-icon {
    width: 1.5rem;
    height: 1.5rem;
  }
}

@media (max-width: 480px) {
  .dashboard-header {
    padding: 0.5rem 0.5rem 0.5rem 2.5rem;
    min-height: 52px;
  }
  .burger-btn-fixed { left: 0.5rem; }
  
  .header-center {
    margin: 0 0.3rem;
    min-width: 120px;
    justify-content: center;
  }
  
  .header-right {
    gap: 0.25rem;
  }
  
  .header-icon {
    font-size: 1.1rem;
    padding: 0.3rem;
  }
  
  .header-bell-icon {
    width: 1.4rem;
    height: 1.4rem;
  }
}

@media (max-width: 360px) {
  .dashboard-header {
    padding: 0.4rem 0.4rem 0.4rem 2.2rem;
    min-height: 48px;
  }
  .burger-btn-fixed { left: 0.45rem; }
  
  .header-center {
    margin: 0 0.2rem;
    min-width: 100px;
    justify-content: center;
  }
  
  .header-icon {
    font-size: 1rem;
    padding: 0.25rem;
  }
  
  .header-bell-icon {
    width: 1.3rem;
    height: 1.3rem;
  }

}

@media (max-height: 500px) and (orientation: landscape) {
  .dashboard-header {
    min-height: 44px;
    padding: 0.4rem 0.7rem 0.4rem 2.5rem;
  }
  
  .header-bell-icon {
    width: 1.5rem;
    height: 1.5rem;
  }
}
</style> 
