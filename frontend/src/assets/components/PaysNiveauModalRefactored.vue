<!-- 
🌍 Composant Modal Refactorisé pour Sélection Pays/Niveau
Architecture: Vue 3 Composition API, Design System professionnel, UX optimisée
-->

<template>
  <div class="pays-niveau-modal-overlay" @click="handleOverlayClick">
    <div 
      class="pays-niveau-modal"
      :class="{ 'modal-large': etapeActuelle === 'niveau' }"
      @click.stop
    >
      <!-- En-tête avec progression -->
      <div class="modal-header">
        <div class="header-content">
          <h2 class="modal-title">
            <IconGlobe class="title-icon" />
            Configuration Éducative
          </h2>
          <button 
            class="close-button"
            @click="$emit('close')"
            :title="'Fermer'"
          >
            <IconX />
          </button>
        </div>
        
        <!-- Indicateur de progression -->
        <div class="progress-indicator">
          <div 
            v-for="(etape, index) in etapes" 
            :key="etape.id"
            class="progress-step"
            :class="{
              'step-completed': isEtapeComplete(etape.id),
              'step-current': etapeActuelle === etape.id,
              'step-clickable': isEtapeAccessible(etape.id)
            }"
            @click="changerEtapeSiPossible(etape.id)"
          >
            <div class="step-circle">
              <IconCheck v-if="isEtapeComplete(etape.id)" class="step-icon" />
              <span v-else class="step-number">{{ index + 1 }}</span>
            </div>
            <span class="step-label">{{ etape.label }}</span>
          </div>
          
          <!-- Barre de progression -->
          <div class="progress-bar">
            <div 
              class="progress-fill"
              :style="{ width: `${progressPourcentage}%` }"
            ></div>
          </div>
        </div>

        <!-- Message d'aide contextuel -->
        <div v-if="messageAide" class="help-message">
          <IconInfo class="help-icon" />
          <span>{{ messageAide }}</span>
        </div>
      </div>

      <!-- Contenu principal -->
      <div class="modal-body">
        <!-- État de chargement global -->
        <div v-if="isLoading && !isInitialized" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Chargement des configurations disponibles...</p>
        </div>

        <!-- État d'erreur -->
        <div v-else-if="erreur" class="error-state">
          <IconAlertCircle class="error-icon" />
          <h3>Erreur de chargement</h3>
          <p>{{ erreur }}</p>
          <button class="button button-outline" @click="initialiser(true)">
            <IconRefreshCcw />
            Réessayer
          </button>
        </div>

        <!-- Contenu principal -->
        <div v-else class="content-area">
          <!-- ÉTAPE 1: Sélection du pays -->
          <transition name="slide-fade" mode="out-in">
            <div v-if="etapeActuelle === 'pays'" key="pays" class="etape-pays">
              <!-- Barre de recherche et filtres -->
              <div class="search-section">
                <div class="search-input-container">
                  <IconSearch class="search-icon" />
                  <input
                    v-model="recherchePays"
                    type="text"
                    placeholder="Rechercher un pays..."
                    class="search-input"
                  />
                  <button 
                    v-if="recherchePays"
                    @click="recherchePays = ''"
                    class="clear-search"
                  >
                    <IconX />
                  </button>
                </div>
              </div>

              <!-- Recommandations -->
              <div v-if="recommendations?.recommandations?.length" class="recommendations-section">
                <h3 class="section-title">
                  <IconStar class="section-icon" />
                  Recommandé pour vous
                </h3>
                <div class="pays-grid pays-grid-compact">
                  <div
                    v-for="pays in paysRecommandes"
                    :key="`rec-${pays.id}`"
                    class="pays-card pays-card-recommended"
                    :class="{ 'pays-selected': paysSelectionne?.id === pays.id }"
                    @click="selectionnerPays(pays)"
                  >
                    <div class="pays-flag">
                      <img 
                        :src="getPaysFlag(pays)"
                        :alt="`Drapeau ${pays.nom}`"
                        @error="handleFlagError"
                      />
                    </div>
                    <div class="pays-info">
                      <h4 class="pays-nom">{{ pays.nom }}</h4>
                      <p class="pays-details">{{ pays.description_courte || 'Système éducatif disponible' }}</p>
                      <div class="recommendation-badge">
                        <IconThumbsUp />
                        Recommandé
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Liste complète des pays -->
              <div class="tous-pays-section">
                <h3 class="section-title">
                  <IconGlobe class="section-icon" />
                  Tous les pays disponibles
                  <span class="count-badge">{{ paysFiltres.length }}</span>
                </h3>
                
                <div v-if="paysFiltres.length === 0" class="empty-state">
                  <IconMapPin class="empty-icon" />
                  <p>Aucun pays ne correspond à votre recherche</p>
                </div>
                
                <div v-else class="pays-grid">
                  <div
                    v-for="pays in paysFiltres"
                    :key="pays.id"
                    class="pays-card"
                    :class="{ 
                      'pays-selected': paysSelectionne?.id === pays.id,
                      'pays-recommended': estPaysRecommande(pays.id)
                    }"
                    @click="selectionnerPays(pays)"
                  >
                    <div class="pays-flag">
                      <img 
                        :src="getPaysFlag(pays)"
                        :alt="`Drapeau ${pays.nom}`"
                        @error="handleFlagError"
                      />
                    </div>
                    <div class="pays-info">
                      <h4 class="pays-nom">{{ pays.nom }}</h4>
                      <p v-if="pays.nom_local && pays.nom_local !== pays.nom" class="pays-nom-local">
                        {{ pays.nom_local }}
                      </p>
                      <p class="pays-details">
                        {{ pays.description_courte || 'Système éducatif disponible' }}
                      </p>
                      <div v-if="estPaysRecommande(pays.id)" class="recommendation-badge">
                        <IconStar />
                        Recommandé
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </transition>

          <!-- ÉTAPE 2: Sélection du niveau -->
          <transition name="slide-fade" mode="out-in">
            <div v-if="etapeActuelle === 'niveau'" key="niveau" class="etape-niveau">
              <!-- Info pays sélectionné -->
              <div class="pays-selectionne-info">
                <div class="pays-header">
                  <img 
                    :src="getPaysFlag(paysSelectionne)"
                    :alt="`Drapeau ${paysSelectionne?.nom}`"
                    class="pays-flag-small"
                  />
                  <h3>{{ paysSelectionne?.nom }}</h3>
                  <button 
                    class="change-pays-button"
                    @click="etapePrecedente"
                    title="Changer de pays"
                  >
                    <IconEdit />
                    Modifier
                  </button>
                </div>
              </div>

              <!-- Filtres pour les niveaux -->
              <div class="filtres-section">
                <div class="filtres-container">
                  <!-- Filtre par âge -->
                  <div class="filtre-group">
                    <label class="filtre-label">
                      <IconCalendar class="label-icon" />
                      Âge
                    </label>
                    <select v-model="filtreAge" class="filtre-select">
                      <option :value="null">Tous les âges</option>
                      <option v-for="age in agesDisponibles" :key="age" :value="age">
                        {{ age }} ans
                      </option>
                    </select>
                  </div>

                  <!-- Filtre par type -->
                  <div class="filtre-group">
                    <label class="filtre-label">
                      <IconBookOpen class="label-icon" />
                      Type d'éducation
                    </label>
                    <select v-model="filtreType" class="filtre-select">
                      <option value="tous">Tous les types</option>
                      <option value="primaire">Primaire</option>
                      <option value="secondaire">Secondaire</option>
                      <option value="superieur">Supérieur</option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- État de chargement des niveaux -->
              <div v-if="isLoadingNiveaux" class="loading-state">
                <div class="loading-spinner"></div>
                <p>Chargement des niveaux pour {{ paysSelectionne?.nom }}...</p>
              </div>

              <!-- Liste des niveaux -->
              <div v-else-if="niveauxFiltres.length > 0" class="niveaux-section">
                <h3 class="section-title">
                  <IconGraduationCap class="section-icon" />
                  Niveaux disponibles
                  <span class="count-badge">{{ niveauxFiltres.length }}</span>
                </h3>
                
                <div class="niveaux-grid">
                  <div
                    v-for="niveau in niveauxFiltres"
                    :key="niveau.id"
                    class="niveau-card"
                    :class="{ 'niveau-selected': niveauSelectionne?.id === niveau.id }"
                    @click="selectionnerNiveau(niveau)"
                  >
                    <div class="niveau-header">
                      <h4 class="niveau-nom">{{ niveau.nom }}</h4>
                      <div v-if="niveau.tranche_age" class="niveau-age">
                        <IconClock class="age-icon" />
                        {{ niveau.tranche_age }}
                      </div>
                    </div>
                    
                    <p v-if="niveau.description" class="niveau-description">
                      {{ niveau.description }}
                    </p>
                    
                    <!-- Statistiques de contenu -->
                    <div class="niveau-stats">
                      <div class="stat-item">
                        <IconBookOpen class="stat-icon" />
                        <span class="stat-number">{{ niveau.nombre_cours || 0 }}</span>
                        <span class="stat-label">Cours</span>
                      </div>
                      <div class="stat-item">
                        <IconFileText class="stat-icon" />
                        <span class="stat-number">{{ niveau.nombre_exercices || 0 }}</span>
                        <span class="stat-label">Exercices</span>
                      </div>
                      <div class="stat-item">
                        <IconHelpCircle class="stat-icon" />
                        <span class="stat-number">{{ niveau.nombre_quiz || 0 }}</span>
                        <span class="stat-label">Quiz</span>
                      </div>
                    </div>

                    <!-- Indicateur de contenu disponible -->
                    <div class="contenu-indicator">
                      <div 
                        class="indicator-dot"
                        :class="{
                          'dot-high': getTotalContenu(niveau) > 20,
                          'dot-medium': getTotalContenu(niveau) > 5 && getTotalContenu(niveau) <= 20,
                          'dot-low': getTotalContenu(niveau) > 0 && getTotalContenu(niveau) <= 5,
                          'dot-none': getTotalContenu(niveau) === 0
                        }"
                      ></div>
                      <span class="indicator-text">
                        {{ getContenuDescription(getTotalContenu(niveau)) }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- État vide -->
              <div v-else class="empty-state">
                <IconGraduationCap class="empty-icon" />
                <h3>Aucun niveau disponible</h3>
                <p>Aucun niveau ne correspond à vos critères pour {{ paysSelectionne?.nom }}</p>
                <button class="button button-outline" @click="resetFiltres">
                  <IconFilter />
                  Réinitialiser les filtres
                </button>
              </div>
            </div>
          </transition>

          <!-- ÉTAPE 3: Confirmation -->
          <transition name="slide-fade" mode="out-in">
            <div v-if="etapeActuelle === 'confirmation'" key="confirmation" class="etape-confirmation">
              <div class="confirmation-content">
                <div class="confirmation-icon">
                  <IconCheckCircle />
                </div>
                
                <h3 class="confirmation-title">Confirmer votre configuration</h3>
                
                <div class="selection-summary">
                  <div class="summary-item">
                    <div class="summary-label">Pays sélectionné :</div>
                    <div class="summary-value">
                      <img 
                        :src="getPaysFlag(paysSelectionne)"
                        :alt="`Drapeau ${paysSelectionne?.nom}`"
                        class="summary-flag"
                      />
                      {{ paysSelectionne?.nom }}
                    </div>
                  </div>
                  
                  <div class="summary-item">
                    <div class="summary-label">Niveau d'étude :</div>
                    <div class="summary-value">
                      <IconGraduationCap class="summary-icon" />
                      {{ niveauSelectionne?.nom }}
                    </div>
                  </div>
                  
                  <div v-if="niveauSelectionne?.tranche_age" class="summary-item">
                    <div class="summary-label">Tranche d'âge :</div>
                    <div class="summary-value">
                      <IconClock class="summary-icon" />
                      {{ niveauSelectionne.tranche_age }}
                    </div>
                  </div>
                </div>

                <!-- Aperçu du contenu disponible -->
                <div v-if="selectionInfo?.statistiques" class="contenu-preview">
                  <h4 class="preview-title">Contenu disponible</h4>
                  <div class="preview-stats">
                    <div class="preview-stat">
                      <div class="stat-circle stat-cours">
                        <IconBookOpen />
                      </div>
                      <div class="stat-info">
                        <span class="stat-number">{{ selectionInfo.statistiques.cours }}</span>
                        <span class="stat-label">Cours</span>
                      </div>
                    </div>
                    <div class="preview-stat">
                      <div class="stat-circle stat-exercices">
                        <IconFileText />
                      </div>
                      <div class="stat-info">
                        <span class="stat-number">{{ selectionInfo.statistiques.exercices }}</span>
                        <span class="stat-label">Exercices</span>
                      </div>
                    </div>
                    <div class="preview-stat">
                      <div class="stat-circle stat-quiz">
                        <IconHelpCircle />
                      </div>
                      <div class="stat-info">
                        <span class="stat-number">{{ selectionInfo.statistiques.quiz }}</span>
                        <span class="stat-label">Quiz</span>
                      </div>
                    </div>
                  </div>
                  
                  <div v-if="!selectionInfo.contenuDisponible" class="no-content-warning">
                    <IconAlertTriangle class="warning-icon" />
                    <p>Peu de contenu est actuellement disponible pour cette configuration. 
                       Nous travaillons continuellement à enrichir notre catalogue.</p>
                  </div>
                </div>

                <div class="confirmation-note">
                  <IconInfo class="note-icon" />
                  <p>Cette configuration déterminera le contenu qui vous sera proposé. 
                     Vous pourrez la modifier à tout moment dans vos préférences.</p>
                </div>
              </div>
            </div>
          </transition>
        </div>
      </div>

      <!-- Actions -->
      <div class="modal-actions">
        <div class="actions-left">
          <button 
            v-if="etapeActuelle !== 'pays'"
            class="button button-outline"
            @click="etapePrecedente"
          >
            <IconChevronLeft />
            Précédent
          </button>
        </div>
        
        <div class="actions-right">
          <button 
            class="button button-outline"
            @click="$emit('close')"
          >
            Annuler
          </button>
          
          <button 
            v-if="etapeActuelle === 'pays'"
            class="button button-primary"
            :disabled="!paysSelectionne"
            @click="changerEtape('niveau')"
          >
            Continuer
            <IconChevronRight />
          </button>
          
          <button 
            v-else-if="etapeActuelle === 'niveau'"
            class="button button-primary"
            :disabled="!niveauSelectionne"
            @click="changerEtape('confirmation')"
          >
            Continuer
            <IconChevronRight />
          </button>
          
          <button 
            v-else-if="etapeActuelle === 'confirmation'"
            class="button button-success"
            :disabled="isLoading"
            @click="handleConfirmer"
          >
            <div v-if="isLoading" class="button-spinner"></div>
            <IconCheck v-else />
            Confirmer
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, watch, onMounted, onUnmounted } from 'vue'
import { usePaysNiveaux } from '@/composables/usePaysNiveaux'

// Imports des icônes depuis Heroicons
import {
  GlobeAltIcon as IconGlobe,
  XMarkIcon as IconX,
  CheckIcon as IconCheck,
  InformationCircleIcon as IconInfo,
  MagnifyingGlassIcon as IconSearch,
  StarIcon as IconStar,
  HandThumbUpIcon as IconThumbsUp,
  MapPinIcon as IconMapPin,
  PencilIcon as IconEdit,
  CalendarIcon as IconCalendar,
  BookOpenIcon as IconBookOpen,
  AcademicCapIcon as IconGraduationCap,
  ClockIcon as IconClock,
  DocumentTextIcon as IconFileText,
  QuestionMarkCircleIcon as IconHelpCircle,
  FunnelIcon as IconFilter,
  CheckCircleIcon as IconCheckCircle,
  ExclamationTriangleIcon as IconAlertTriangle,
  ChevronLeftIcon as IconChevronLeft,
  ChevronRightIcon as IconChevronRight,
  ExclamationCircleIcon as IconAlertCircle,
  ArrowPathIcon as IconRefreshCcw
} from '@heroicons/vue/24/outline'

// ===== PROPS & EMITS =====
const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  autoFocus: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close', 'confirmed'])

// ===== COMPOSABLES =====
const {
  // État
  isLoading,
  isLoadingNiveaux,
  isInitialized,
  pays,
  niveauxDisponibles,
  recommendations,
  paysSelectionne,
  niveauSelectionne,
  etapeActuelle,
  recherchePays,
  filtreAge,
  filtreType,
  erreur,
  
  // Propriétés calculées
  paysFiltres,
  niveauxFiltres,
  selectionInfo,
  peutAvancer,
  messageAide,
  isConfigurationCompleted,
  
  // Méthodes
  initialiser,
  selectionnerPays,
  selectionnerNiveau,
  confirmerSelection,
  changerEtape,
  etapePrecedente,
  reinitialiser,
  mettreAJourFiltres,
  estPaysRecommande
} = usePaysNiveaux()

// ===== PROPRIÉTÉS CALCULÉES =====

const etapes = computed(() => [
  { id: 'pays', label: 'Pays' },
  { id: 'niveau', label: 'Niveau' },
  { id: 'confirmation', label: 'Confirmation' }
])

const progressPourcentage = computed(() => {
  const etapeIndex = etapes.value.findIndex(e => e.id === etapeActuelle.value)
  return ((etapeIndex + 1) / etapes.value.length) * 100
})

const paysRecommandes = computed(() => {
  if (!recommendations.value?.recommandations) return []
  
  return pays.value.filter(pays => 
    recommendations.value.recommandations.includes(pays.id)
  ).slice(0, 3) // Limiter à 3 recommandations
})

const agesDisponibles = computed(() => {
  // Fonction désactivée car les champs age_min et age_max n'existent plus
  return []
})

// ===== MÉTHODES =====

const isEtapeComplete = (etapeId) => {
  switch (etapeId) {
    case 'pays':
      return !!paysSelectionne.value
    case 'niveau':
      return !!niveauSelectionne.value
    case 'confirmation':
      return false // Jamais "complète" jusqu'à confirmation finale
    default:
      return false
  }
}

const isEtapeAccessible = (etapeId) => {
  switch (etapeId) {
    case 'pays':
      return true
    case 'niveau':
      return !!paysSelectionne.value
    case 'confirmation':
      return !!(paysSelectionne.value && niveauSelectionne.value)
    default:
      return false
  }
}

const changerEtapeSiPossible = (etapeId) => {
  if (isEtapeAccessible(etapeId)) {
    changerEtape(etapeId)
  }
}

const getPaysFlag = (pays) => {
  if (!pays) return ''
  
  // Utiliser le code ISO pour les drapeaux via une API publique
  return `https://flagcdn.com/w40/${pays.code_iso?.toLowerCase() || 'xx'}.png`
}

const handleFlagError = (event) => {
  // Image de fallback en cas d'erreur
  event.target.src = '/images/flags/default.png'
}

const getTotalContenu = (niveau) => {
  return (niveau.nombre_cours || 0) + 
         (niveau.nombre_exercices || 0) + 
         (niveau.nombre_quiz || 0)
}

const getContenuDescription = (total) => {
  if (total === 0) return 'Aucun contenu'
  if (total <= 5) return 'Peu de contenu'
  if (total <= 20) return 'Contenu modéré'
  return 'Beaucoup de contenu'
}

const resetFiltres = () => {
  mettreAJourFiltres({
    age: null,
    type: 'tous'
  })
}

const handleOverlayClick = () => {
  emit('close')
}

const handleConfirmer = async () => {
  const success = await confirmerSelection()
  if (success) {
    emit('confirmed', {
      pays: paysSelectionne.value,
      niveau: niveauSelectionne.value
    })
    
    // Fermer le modal automatiquement après un court délai
    setTimeout(() => {
      emit('close')
    }, 1000)
  }
}

// ===== GESTION DU CLAVIER =====
const handleKeydown = (event) => {
  switch (event.key) {
    case 'Escape':
      emit('close')
      break
    case 'ArrowLeft':
      if (etapeActuelle.value !== 'pays') {
        etapePrecedente()
      }
      break
    case 'ArrowRight':
      if (peutAvancer.value) {
        // Logique de navigation suivante
      }
      break
  }
}

// ===== CYCLE DE VIE =====
onMounted(async () => {
  // Initialiser le système
  await initialiser()
  
  // Gestion du clavier
  document.addEventListener('keydown', handleKeydown)
  
  // Focus automatique si demandé
  if (props.autoFocus) {
    // Logique de focus
  }
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})

// ===== WATCHERS =====
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    // Réinitialiser l'état quand on ouvre la modal
    reinitialiser()
    initialiser()
  }
})
</script>

<style scoped>
/* ===== STYLES DE BASE ===== */
.pays-niveau-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.pays-niveau-modal {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transform: scale(0.95);
  animation: modalEnter 0.3s ease-out forwards;
}

.modal-large {
  max-width: 1000px;
}

@keyframes modalEnter {
  to {
    transform: scale(1);
  }
}

/* ===== EN-TÊTE ===== */
.modal-header {
  padding: 24px 24px 0;
  border-bottom: 1px solid #e5e7eb;
  background: #fafafa;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.title-icon {
  width: 24px;
  height: 24px;
  color: #3b82f6;
}

.close-button {
  background: none;
  border: none;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  color: #6b7280;
  transition: all 0.2s;
}

.close-button:hover {
  background: #f3f4f6;
  color: #374151;
}

/* ===== INDICATEUR DE PROGRESSION ===== */
.progress-indicator {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding: 0 20px;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  z-index: 2;
}

.progress-step.step-clickable:hover .step-circle {
  transform: scale(1.1);
}

.step-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e5e7eb;
  border: 2px solid #d1d5db;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  font-weight: 600;
  color: #6b7280;
}

.step-current .step-circle {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
}

.step-completed .step-circle {
  background: #10b981;
  border-color: #10b981;
  color: white;
}

.step-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  transition: color 0.2s;
}

.step-current .step-label {
  color: #3b82f6;
}

.step-completed .step-label {
  color: #10b981;
}

.progress-bar {
  position: absolute;
  top: 20px;
  left: 60px;
  right: 60px;
  height: 2px;
  background: #e5e7eb;
  z-index: 1;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #3b82f6);
  border-radius: 1px;
  transition: width 0.5s ease;
}

/* ===== MESSAGE D'AIDE ===== */
.help-message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 8px;
  color: #0369a1;
  font-size: 0.875rem;
  margin-bottom: 16px;
}

.help-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

/* ===== CORPS DE LA MODAL ===== */
.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.content-area {
  min-height: 400px;
}

/* ===== ÉTATS DE CHARGEMENT ET D'ERREUR ===== */
.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 60px 20px;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-icon {
  width: 48px;
  height: 48px;
  color: #ef4444;
}

/* ===== SECTIONS ===== */
.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 16px 0;
}

.section-icon {
  width: 20px;
  height: 20px;
  color: #3b82f6;
}

.count-badge {
  background: #3b82f6;
  color: white;
  font-size: 0.75rem;
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: 500;
}

/* ===== RECHERCHE ===== */
.search-section {
  margin-bottom: 24px;
}

.search-input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  width: 20px;
  height: 20px;
  color: #6b7280;
}

.search-input {
  width: 100%;
  padding: 12px 16px 12px 44px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.clear-search {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  padding: 4px;
  border-radius: 4px;
  cursor: pointer;
  color: #6b7280;
}

/* ===== GRILLES ===== */
.pays-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.pays-grid-compact {
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}

/* ===== CARTES PAYS ===== */
.pays-card {
  display: flex;
  gap: 12px;
  padding: 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  background: white;
}

.pays-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.pays-card.pays-selected {
  border-color: #3b82f6;
  background: #f0f9ff;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.pays-card-recommended {
  border-color: #fbbf24;
  background: #fffbeb;
}

.pays-flag {
  width: 48px;
  height: 36px;
  flex-shrink: 0;
  border-radius: 4px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f3f4f6;
}

.pays-flag img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.pays-info {
  flex: 1;
  min-width: 0;
}

.pays-nom {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 4px 0;
}

.pays-nom-local {
  font-size: 0.875rem;
  color: #6b7280;
  font-style: italic;
  margin: 0 0 8px 0;
}

.pays-details {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.recommendation-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: #fbbf24;
  color: white;
  font-size: 0.75rem;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 500;
}

/* ===== NIVEAUX ===== */
.pays-selectionne-info {
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 24px;
}

.pays-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.pays-flag-small {
  width: 32px;
  height: 24px;
  border-radius: 4px;
  object-fit: cover;
}

.change-pays-button {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 6px;
  background: white;
  border: 1px solid #d1d5db;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.change-pays-button:hover {
  background: #f3f4f6;
}

/* ===== FILTRES ===== */
.filtres-section {
  margin-bottom: 24px;
}

.filtres-container {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.filtre-group {
  flex: 1;
  min-width: 200px;
}

.filtre-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 6px;
}

.label-icon {
  width: 16px;
  height: 16px;
}

.filtre-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  background: white;
}

/* ===== CARTES NIVEAU ===== */
.niveaux-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
}

.niveau-card {
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s;
  background: white;
}

.niveau-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.niveau-card.niveau-selected {
  border-color: #3b82f6;
  background: #f0f9ff;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.niveau-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.niveau-nom {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  flex: 1;
}

.niveau-age {
  display: flex;
  align-items: center;
  gap: 4px;
  background: #f3f4f6;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  color: #6b7280;
  white-space: nowrap;
}

.age-icon {
  width: 12px;
  height: 12px;
}

.niveau-description {
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.4;
  margin: 0 0 16px 0;
}

/* ===== STATISTIQUES ===== */
.niveau-stats {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  flex: 1;
}

.stat-icon {
  width: 16px;
  height: 16px;
  color: #6b7280;
}

.stat-number {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

.stat-label {
  font-size: 0.75rem;
  color: #6b7280;
  text-align: center;
}

/* ===== INDICATEUR DE CONTENU ===== */
.contenu-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
}

.indicator-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.dot-high {
  background: #10b981;
}

.dot-medium {
  background: #f59e0b;
}

.dot-low {
  background: #ef4444;
}

.dot-none {
  background: #9ca3af;
}

.indicator-text {
  font-size: 0.75rem;
  color: #6b7280;
}

/* ===== CONFIRMATION ===== */
.confirmation-content {
  text-align: center;
  max-width: 500px;
  margin: 0 auto;
}

.confirmation-icon {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.confirmation-icon svg {
  width: 64px;
  height: 64px;
  color: #10b981;
}

.confirmation-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 24px 0;
}

.selection-summary {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #e5e7eb;
}

.summary-item:last-child {
  border-bottom: none;
}

.summary-label {
  font-weight: 500;
  color: #6b7280;
}

.summary-value {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #1f2937;
}

.summary-flag {
  width: 24px;
  height: 18px;
  border-radius: 3px;
  object-fit: cover;
}

.summary-icon {
  width: 16px;
  height: 16px;
  color: #3b82f6;
}

/* ===== APERÇU CONTENU ===== */
.contenu-preview {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
}

.preview-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 16px 0;
  text-align: center;
}

.preview-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 16px;
}

.preview-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.stat-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-cours {
  background: #3b82f6;
}

.stat-exercices {
  background: #10b981;
}

.stat-quiz {
  background: #f59e0b;
}

.no-content-warning {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #fef3c7;
  border: 1px solid #f59e0b;
  border-radius: 8px;
  padding: 12px;
  color: #92400e;
  font-size: 0.875rem;
}

.warning-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.confirmation-note {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 8px;
  padding: 12px;
  color: #0369a1;
  font-size: 0.875rem;
  text-align: left;
}

.note-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  margin-top: 2px;
}

/* ===== ÉTAT VIDE ===== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  width: 48px;
  height: 48px;
  color: #9ca3af;
}

/* ===== ACTIONS ===== */
.modal-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  border-top: 1px solid #e5e7eb;
  background: #fafafa;
}

.actions-left,
.actions-right {
  display: flex;
  gap: 12px;
}

/* ===== BOUTONS ===== */
.button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
  text-decoration: none;
}

.button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.button-outline {
  background: white;
  border-color: #d1d5db;
  color: #374151;
}

.button-outline:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #9ca3af;
}

.button-primary {
  background: #3b82f6;
  color: white;
}

.button-primary:hover:not(:disabled) {
  background: #2563eb;
}

.button-success {
  background: #10b981;
  color: white;
}

.button-success:hover:not(:disabled) {
  background: #059669;
}

.button-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* ===== ANIMATIONS ===== */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from {
  transform: translateX(20px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateX(-20px);
  opacity: 0;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
  .pays-niveau-modal-overlay {
    padding: 10px;
  }

  .pays-niveau-modal {
    max-height: 95vh;
  }

  .modal-header {
    padding: 16px 16px 0;
  }

  .modal-body {
    padding: 16px;
  }

  .modal-actions {
    padding: 16px;
    flex-direction: column;
  }

  .actions-left,
  .actions-right {
    width: 100%;
    justify-content: center;
  }

  .pays-grid {
    grid-template-columns: 1fr;
  }

  .niveaux-grid {
    grid-template-columns: 1fr;
  }

  .progress-indicator {
    padding: 0 10px;
  }

  .filtres-container {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .progress-step {
    gap: 4px;
  }

  .step-circle {
    width: 32px;
    height: 32px;
  }

  .step-label {
    font-size: 0.75rem;
  }

  .modal-title {
    font-size: 1.25rem;
  }

  .pays-card {
    flex-direction: column;
    text-align: center;
  }

  .pays-flag {
    align-self: center;
  }
}
</style>
