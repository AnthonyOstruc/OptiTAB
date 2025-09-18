<template>
  <header class="dashboard-header">
    <!-- Bouton burger fixe en position absolue -->
    <button 
      class="burger-btn-fixed" 
      @click="$emit('toggle-sidebar')" 
      aria-label="Ouvrir ou fermer le menu"
    >
      <span class="burger-icon-fixed">&#9776;</span>
    </button>

    <!-- Section centrale : Contenu conditionnel -->
    <ConditionalHeader 
      v-if="!isCalculatorPage"
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

// Router
const router = useRouter()
const route = useRoute()

// Computed properties
const isCalculatorPage = computed(() => route.name === 'Calculator')

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
  left: 0.75rem; /* Légèrement plus à gauche pour centrer avec la barre latérale */
  top: 50%;
  transform: translateY(-50%);
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(30, 41, 59, 0.07);
  z-index: 101;
  /* Transitions professionnelles */
  transition: background-color 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  /* POSITION CENTRÉE VERTICALEMENT */
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
}

.burger-btn-fixed:hover {
  background: #f8fafc;
  box-shadow: 0 4px 12px rgba(30, 41, 59, 0.12);
  border-color: #d1d5db;
}

.burger-btn-fixed:active {
  background: #f1f5f9;
  box-shadow: 0 2px 8px rgba(30, 41, 59, 0.07);
}

.burger-icon-fixed {
  font-size: 1.5rem;
  color: #2563eb;
  transition: color 0.2s ease;
  font-weight: 500;
}

.burger-btn-fixed:hover .burger-icon-fixed {
  color: #1e40af;
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