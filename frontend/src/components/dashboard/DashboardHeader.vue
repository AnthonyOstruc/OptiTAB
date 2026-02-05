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
      v-if="showConditionalHeader"
      :matiere-props="{ matiereId: null }"
      @subject-changed="handleSubjectChange"
      @search="handleSearch"
    />
    <CalculatorTabs v-else-if="isCalculatorPage" class="header-calculator-tabs" />
    <BillingTabs v-else-if="isBillingPage" class="header-billing-tabs" />
    <router-link 
      v-else-if="isSubscriptionPage" 
      to="/billing" 
      class="header-back-button" data-cta-name="subscribe" data-cta-location="header_dashboard"
    >
      <span>← Abonnements</span>
    </router-link>

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
import BillingTabs from '@/components/payments/BillingTabs.vue'
import CalculatorTabs from '@/components/calculator/CalculatorTabs.vue'

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
const isBillingPage = computed(() => route.name === 'Billing')
const isSubscriptionPage = computed(() => route.name === 'Subscription')
const isBillingSection = computed(() => ['Billing', 'Subscription'].includes(route.name))
const showConditionalHeader = computed(() => !isCalculatorPage.value && !isAdminPage.value && !isBillingSection.value)

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
  -webkit-transform: translateZ(0);
  transform: translateZ(0);
  /* Permettre le scroll vertical à travers le header */
  touch-action: pan-y;
}

/* Bouton burger fixe - Solution professionnelle */
.burger-btn-fixed {
  position: absolute;
  left: 0.75rem; /* Légèrement plus à gauche pour centrer avec la barre latérale */
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
  /* Transitions professionnelles */
  transition: background-color 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  overflow: visible;
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
  touch-action: pan-y;
}

/* Réactiver les interactions pour le contenu réel du bloc droit */
.header-right > * {
  pointer-events: auto;
}

.header-calculator-tabs {
  position: relative;
  left: 0;
  top: 0;
  transform: none;
  pointer-events: auto;
  max-width: 700px;
  width: auto;
  flex: 1;
}

.header-billing-tabs {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  pointer-events: auto; /* réactive les clics malgré pointer-events:none du header */
}

.header-back-button {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  pointer-events: auto;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 1.2rem; /* reduced height, same width */
  border-radius: 999px;
  background: #2563eb;
  border: 1px solid #1e40af; /* same as billing tab */
  color: #ffffff;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem; /* same as billing tab */
  transition: all 0.18s ease; /* visual parity */
  box-shadow: 0 6px 14px rgba(37, 99, 235, 0.22);
}

@media (hover: hover) {
  .header-back-button:hover {
    background: #1e40af;
    border-color: #1e40af;
    /* keep position fixed: no transform */
    box-shadow: 0 10px 20px rgba(30, 64, 175, 0.25);
  }
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
    /* Garder le même padding pour éviter le décalage */
    padding: 0.7rem 2rem 0.7rem 4rem;
  }
}

@media (max-width: 1024px) {
  .dashboard-header {
    /* Garder le même padding pour éviter le décalage */
    padding: 0.7rem 2rem 0.7rem 4rem;
    min-height: 60px;
  }
  /* Garder la position du burger identique */
}

@media (max-width: 768px) {
  .dashboard-header {
    padding: 0.6rem 0.7rem;
    min-height: 56px;
    /* Header FIXE sur mobile - ne bouge jamais */
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    width: 100%;
    z-index: 12001; /* Cohérent avec desktop */
    pointer-events: auto;
    /* Bloquer complètement le scroll et le zoom sur le header */
    touch-action: none;
    overscroll-behavior: none;
    /* Forcer le navigateur à garder le header fixe (GPU layer) */
    will-change: transform;
    transform: translateZ(0);
    -webkit-transform: translateZ(0);
    -webkit-backface-visibility: hidden;
    backface-visibility: hidden;
  }
  
  /* Permettre les clics sur les éléments interactifs du header */
  .dashboard-header button,
  .dashboard-header a,
  .dashboard-header .clickable {
    touch-action: manipulation;
  }
  
  .burger-btn-fixed { 
    display: none;
  }
  
  .header-center {
    margin: 0 0.5rem;
    min-width: 150px;
    max-width: none;
    justify-content: center;
  }
  /* Mobile: placer le CTA dans le flux, centré, sans chevauchement */
  .header-billing-tabs,
  .header-calculator-tabs,
  .header-back-button {
    position: static;
    transform: none;
    margin: 0 auto;
    flex: 0 0 auto;
    display: flex;
    justify-content: center;
    width: fit-content;
    max-width: calc(100% - 140px); /* leave space for right icons */
  }

  .header-calculator-tabs {
    max-width: calc(100% - 100px);
  }

  .header-back-button {
    font-size: 0.9rem; /* same as billing tab mobile */
    padding: 0.4rem 0.9rem; /* reduced height, same width */
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.18); /* same as billing tab mobile */
    border-color: #1e40af;
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

/* Styles 480px et 360px unifiés - héritent de 768px */

@media (max-height: 500px) and (orientation: landscape) {
  .dashboard-header {
    min-height: 56px;
    padding: 0.6rem 0.7rem;
  }
  
  .burger-btn-fixed {
    display: none;
  }
}
</style>
