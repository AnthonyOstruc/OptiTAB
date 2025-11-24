<template>
  <div class="selected-matiere-header">
    <!-- Menu contextuel (téléporté au body pour être au premier plan) -->
    <teleport to="body">
      <ContextMenu
        :visible="contextMenu.visible"
        :x="contextMenu.x"
        :y="contextMenu.y"
        :is-favorite="contextMenu.isFavorite"
        :matiere-id="contextMenu.matiereId"
        @favorite-toggle="handleContextMenuFavoriteToggle"
        @close="closeContextMenu"
      />
    </teleport>
    <!-- État de chargement (uniquement au premier chargement) -->
    <div v-if="loading && matieres.length === 0" class="loading-state">
      <div class="loading-spinner"></div>
      <span>Chargement des matières...</span>
    </div>
    
    <!-- Affichage des tabs de matières sélectionnées -->
    <div v-else class="matieres-tabs">
      <!-- Conteneur principal des tabs -->
      <div class="tabs-container">
        <!-- Bouton liste déroulante des onglets ouverts (visible uniquement < 500px) -->
        <button 
          v-if="selectedMatieres.length > 0"
          class="open-tabs-btn"
          @click="toggleOpenTabsDropdown($event)"
          :disabled="loading"
          title="Voir les onglets ouverts"
          ref="openTabsButton"
          aria-label="Liste des onglets ouverts"
        >
          <span class="dropdown-arrow">▼</span>
          <span class="active-name">{{ activeMatiere?.nom || 'Sélectionner' }}</span>
        </button>
        
        <!-- Tab "New Matière" par défaut (visible uniquement si aucune matière sélectionnée) -->
        <button 
          v-if="selectedMatieres.length === 0"
          class="matiere-tab new-tab"
          @click="toggleMatiereDropdown($event)"
          :disabled="loading"
          title="Ajouter une nouvelle matière"
          ref="newMatiereButton"
          aria-label="Ajouter une nouvelle matière"
        >
          <span class="tab-icon" aria-hidden="true">+</span>
          <span class="tab-name">New Matière</span>
        </button>
        
        <!-- Tabs des matières sélectionnées (masqués < 500px) -->
        <div 
          v-for="matiere in selectedMatieres" 
          :key="`tab-${matiere.id}`"
          :class="['matiere-tab', 'desktop-tab', { 
            active: activeMatiereId === matiere.id,
            loading: loadingMatiere === matiere.id 
          }]"
          @click="setActiveMatiere(matiere.id)"
          @mousedown="handleTabMouseDown($event, matiere.id)"
          @contextmenu.prevent="showContextMenu($event, matiere)"
          :title="`Voir ${matiere.nom}`"
          :aria-label="`Matière ${matiere.nom}`"
          :aria-selected="activeMatiereId === matiere.id"
          role="tab"
        >
          <span class="tab-icon" v-html="matiere.svg_icon || '📚'" aria-hidden="true"></span>
          <span class="tab-name">{{ matiere.nom }}</span>
          <span class="tab-initials">{{ getInitials(matiere.nom) }}</span>
          <button 
            class="tab-close"
            @click.stop="removeMatiere(matiere.id)"
            :title="`Fermer ${matiere.nom}`"
            :aria-label="`Fermer l'onglet ${matiere.nom}`"
            :disabled="loading"
          >
            ×
          </button>
        </div>
        
        <!-- Bouton "+" compact à droite (style Google Chrome) -->
        <button 
          v-if="selectedMatieres.length > 0"
          class="matiere-tab new-tab-small"
          @click="toggleMatiereDropdown($event)"
          :disabled="loading || availableMatieres.length === 0"
          title="Ajouter une nouvelle matière"
          ref="newMatiereButton"
          aria-label="Ajouter une nouvelle matière"
        >
          <span class="tab-icon" aria-hidden="true">+</span>
        </button>
      </div>

      <!-- Dropdown des matières disponibles (téléporté au body pour être toujours au premier plan) -->
      <teleport to="body">
      <div 
        v-if="showMatiereDropdown" 
        class="matiere-dropdown"
        :style="dropdownStyle"
        role="listbox"
        aria-label="Liste des matières disponibles"
        @keydown="handleDropdownKeydown"
      >
        <div class="dropdown-header">
          <span class="dropdown-title">Matières disponibles</span>
          <button 
            class="dropdown-close" 
            @click="closeMatiereDropdown"
            aria-label="Fermer la liste"
          >
            ×
          </button>
        </div>
        
          <div
            v-for="(matiere, index) in availableMatieres" 
            :key="`dropdown-${matiere.id}`"
            class="dropdown-item"
            @click="selectMatiere(matiere)"
            @contextmenu.prevent="showContextMenu($event, matiere)"
            :class="{ 
              'last-item': index === availableMatieres.length - 1,
              'loading': loadingMatiere === matiere.id 
            }"
            role="option"
            :aria-selected="false"
            :title="`Ouvrir ${matiere.nom}`"
          >
            <div class="dropdown-content-left">
              <span class="dropdown-icon" v-html="matiere.svg_icon || '📚'" aria-hidden="true"></span>
              <span class="dropdown-name">{{ matiere.nom }}</span>
            </div>
            <button 
              class="dropdown-star"
              @click.stop="toggleFavorite(matiere.id)"
              :class="{ 
                'favorite': subjectsStore.isFavoriteMatiere(matiere.id),
                'loading': loadingFavorite === matiere.id 
              }"
              :title="subjectsStore.isFavoriteMatiere(matiere.id) ? 'Retirer des favoris' : 'Ajouter aux favoris'"
              :aria-label="subjectsStore.isFavoriteMatiere(matiere.id) ? `Retirer ${matiere.nom} des favoris` : `Ajouter ${matiere.nom} aux favoris`"
              :disabled="loadingFavorite === matiere.id"
            >
              <span class="star-icon">{{ subjectsStore.isFavoriteMatiere(matiere.id) ? '⭐' : '☆' }}</span>
            </button>
          </div>
        
        <div v-if="availableMatieres.length === 0" class="dropdown-empty">
          <span class="empty-icon">📚</span>
          <span class="empty-text">Toutes les matières sont déjà ouvertes</span>
        </div>
      </div>
      </teleport>
      
      <!-- Dropdown des onglets ouverts (téléporté au body, visible uniquement < 500px) -->
      <teleport to="body">
      <div 
        v-if="showOpenTabsDropdown" 
        class="open-tabs-dropdown"
        :style="openTabsDropdownStyle"
        role="listbox"
        aria-label="Liste des onglets ouverts"
      >
        <div class="dropdown-header">
          <span class="dropdown-title">Onglets ouverts</span>
          <button 
            class="dropdown-close" 
            @click="closeOpenTabsDropdown"
            aria-label="Fermer la liste"
          >
            ×
          </button>
        </div>
        
        <div
          v-for="matiere in selectedMatieres" 
          :key="`open-tab-${matiere.id}`"
          :class="['dropdown-item', {
            'active': activeMatiereId === matiere.id,
            'loading': loadingMatiere === matiere.id 
          }]"
          @click="setActiveMatiereFromDropdown(matiere.id)"
          role="option"
          :aria-selected="activeMatiereId === matiere.id"
          :title="`Voir ${matiere.nom}`"
        >
          <div class="dropdown-content-left">
            <span class="dropdown-icon" v-html="matiere.svg_icon || '📚'" aria-hidden="true"></span>
            <span class="dropdown-name">{{ matiere.nom }}</span>
          </div>
          <button 
            class="dropdown-close-tab"
            @click.stop="removeMatiere(matiere.id)"
            :title="`Fermer ${matiere.nom}`"
            :aria-label="`Fermer l'onglet ${matiere.nom}`"
            :disabled="loading"
          >
            ×
          </button>
        </div>
      </div>
      </teleport>
      
      <!-- Dropdown des favoris (téléporté au body, visible uniquement < 500px) -->
      <teleport to="body">
      <div 
        v-if="showFavoritesDropdown" 
        class="favorites-dropdown"
        :style="favoritesDropdownStyle"
        role="listbox"
        aria-label="Liste des favoris"
      >
        <div class="dropdown-header">
          <span class="dropdown-title">Favoris ⭐</span>
          <button 
            class="dropdown-close" 
            @click="closeFavoritesDropdown"
            aria-label="Fermer la liste"
          >
            ×
          </button>
        </div>
        
        <div
          v-for="matiere in favoriteMatieres" 
          :key="`favorite-dropdown-${matiere.id}`"
          :class="['dropdown-item', {
            'active': activeMatiereId === matiere.id,
            'loading': loadingMatiere === matiere.id 
          }]"
          @click="selectMatiereFromFavoritesDropdown(matiere)"
          role="option"
          :aria-selected="activeMatiereId === matiere.id"
          :title="`Ouvrir ${matiere.nom}`"
        >
          <div class="dropdown-content-left">
            <span class="dropdown-icon" v-html="matiere.svg_icon || '📚'" aria-hidden="true"></span>
            <span class="dropdown-name">{{ matiere.nom }}</span>
          </div>
        </div>
        
        <div v-if="favoriteMatieres.length === 0" class="dropdown-empty">
          <span class="empty-icon">⭐</span>
          <span class="empty-text">Aucun favori</span>
        </div>
      </div>
      </teleport>
      
      <!-- Barre des favoris (style Chrome) -->
      <div v-if="favoriteMatieres.length > 0" class="favorites-bar">
        <div class="favorites-container">
          <!-- Bouton dropdown favoris (visible uniquement < 500px) -->
          <button 
            class="favorites-dropdown-btn"
            @click="toggleFavoritesDropdown($event)"
            :disabled="loading"
            title="Voir les favoris"
            ref="favoritesButton"
            aria-label="Liste des favoris"
          >
            <span class="dropdown-arrow">▼</span>
            <span class="favorites-icon" aria-hidden="true">⭐</span>
            <span class="favorites-dropdown-text">Favoris</span>
          </button>
          
          <div class="favorites-label">
            <span class="favorites-icon" aria-hidden="true">⭐</span>
            <span class="favorites-text">Favoris:</span>
          </div>
          
          <div class="favorites-list">
            <button 
              v-for="matiere in favoriteMatieres" 
              :key="`favorite-${matiere.id}`"
              class="favorite-item desktop-favorite"
              @click="selectMatiere(matiere)"
              @contextmenu.prevent="showContextMenu($event, matiere)"
              :class="{ 
                'active': activeMatiereId === matiere.id,
                'loading': loadingMatiere === matiere.id 
              }"
              :title="`Ouvrir ${matiere.nom}`"
              :aria-label="`Ouvrir la matière favorite ${matiere.nom}`"
              :disabled="loadingMatiere === matiere.id"
            >
              <span class="favorite-icon" v-html="matiere.svg_icon || '📚'" aria-hidden="true"></span>
              <span class="favorite-name">{{ matiere.nom }}</span>
              <span class="favorite-initials">{{ getInitials(matiere.nom) }}</span>
            </button>
          </div>
          
          <button 
            class="favorites-toggle"
            @click="toggleFavoritesVisibility"
            :title="showAllFavorites ? 'Réduire les favoris' : 'Voir tous les favoris'"
            :aria-label="showAllFavorites ? 'Réduire la liste des favoris' : 'Voir tous les favoris'"
            v-if="favoriteMatieres.length > MAX_VISIBLE_FAVORITES"
          >
            {{ showAllFavorites ? '‹' : '›' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useSubjectsStore } from '@/stores/subjects/index'
import { useUserStore } from '@/stores/user'
import { getMatieresUtilisateur } from '@/api/matieres.js'
import ContextMenu from '@/components/common/ContextMenu.vue'

/**
 * Props du composant
 */
const props = defineProps({
  matiereId: {
    type: [Number, String],
    default: null,
    validator: (value) => value === null || (!isNaN(Number(value)) && Number(value) > 0)
  }
})

// Mettre à jour le matiereId du contextMenu quand les props changent
watch(() => props.matiereId, (newId) => {
  contextMenu.value.matiereId = newId || null
})

/**
 * Événements émis par le composant
 */
const emit = defineEmits(['matiere-changed'])

/**
 * Constantes de configuration
 */
const MAX_VISIBLE_FAVORITES = 5 // Nombre maximum de favoris visibles par défaut
const DROPDOWN_OFFSET = 6 // Décalage du dropdown en pixels
const ANIMATION_DURATION = 150 // Durée des animations en ms

/**
 * Instances des composables
 */
const router = useRouter()
const subjectsStore = useSubjectsStore()
const userStore = useUserStore()

/**
 * État du menu contextuel
 */
const contextMenu = ref({
  visible: false,
  x: 0,
  y: 0,
  matiereId: props.matiereId || null,
  isFavorite: false
})

/**
 * État réactif du composant
 */
const matieres = ref([])
const loading = ref(false)
const loadingMatiere = ref(null)
const loadingFavorite = ref(null)
const activeMatiereId = ref(null)
const showMatiereDropdown = ref(false)
const showAllFavorites = ref(false)
const newMatiereButton = ref(null)
const dropdownStyle = ref({})
const showOpenTabsDropdown = ref(false)
const openTabsButton = ref(null)
const openTabsDropdownStyle = ref({})
const showFavoritesDropdown = ref(false)
const favoritesButton = ref(null)
const favoritesDropdownStyle = ref({})

/**
 * Propriétés calculées (Computed Properties)
 */

// Matières sélectionnées avec validation
const selectedMatieres = computed(() => {
  return matieres.value.filter(m => 
    m && m.id && subjectsStore.selectedMatieresIds.includes(m.id)
  )
})

// Matières disponibles pour le dropdown (non sélectionnées)
const availableMatieres = computed(() => {
  return matieres.value.filter(m => 
    m && m.id && !subjectsStore.selectedMatieresIds.includes(m.id)
  )
})

// Matières favorites avec gestion de l'affichage
const favoriteMatieres = computed(() => {
  const favorites = matieres.value.filter(m => 
    m && m.id && subjectsStore.isFavoriteMatiere(m.id)
  )
  
  if (!showAllFavorites.value && favorites.length > MAX_VISIBLE_FAVORITES) {
    return favorites.slice(0, MAX_VISIBLE_FAVORITES)
  }
  
  return favorites
})

// Matière actuellement active
const activeMatiere = computed(() => {
  return matieres.value.find(m => m && m.id === activeMatiereId.value)
})

/**
 * Méthodes utilitaires
 */

/**
 * Gestion sécurisée des erreurs
 * @param {Error} error - L'erreur à traiter
 * @param {string} context - Le contexte où l'erreur s'est produite
 */
const handleError = (error, context) => {
  console.error(`[SelectedMatiereHeader] Erreur dans ${context}:`, error)
  // Ici on pourrait ajouter une notification utilisateur ou un service de logging
}

/**
 * Génère les initiales à partir d'un nom de matière
 * Exemple: "Physique Chimie" -> "PC", "Maths" -> "M"
 * @param {string} name
 * @returns {string}
 */
const getInitials = (name) => {
  try {
    if (!name || typeof name !== 'string') return ''
    const cleaned = name
      .replace(/\([^)]*\)/g, '') // enlever le contenu entre parenthèses
      .replace(/[^\p{L}\s-]/gu, '') // enlever la ponctuation (lettres unicode conservées)
      .trim()
    if (!cleaned) return ''
    const words = cleaned.split(/[\s-]+/).filter(Boolean)
    if (words.length === 0) return ''
    // Limiter à 2 lettres pour garder un rendu compact
    return words.slice(0, 2).map(w => w.charAt(0).toUpperCase()).join('')
  } catch {
    return ''
  }
}

/**
 * Validation d'un ID de matière
 * @param {any} id - L'ID à valider
 * @returns {boolean} - True si l'ID est valide
 */
const isValidMatiereId = (id) => {
  return id !== null && id !== undefined && !isNaN(Number(id)) && Number(id) > 0
}

/**
 * Méthodes de chargement des données
 */

/**
 * Charge la liste des matières depuis l'API
 */
const MATIERES_CACHE_KEY = 'matieres_disponibles_cache'
const MATIERES_CACHE_TTL_MS = 10 * 60 * 1000 // 10 minutes

const readMatieresCache = () => {
  try {
    const raw = localStorage.getItem(MATIERES_CACHE_KEY)
    if (!raw) return null
    const parsed = JSON.parse(raw)
    if (!parsed || !Array.isArray(parsed.data)) return null
    return parsed
  } catch {
    return null
  }
}

const writeMatieresCache = (data) => {
  try {
    const payload = {
      niveauId: userStore.niveau_pays?.id || null,
      ts: Date.now(),
      data
    }
    localStorage.setItem(MATIERES_CACHE_KEY, JSON.stringify(payload))
  } catch {
    // ignore quota errors
  }
}

const clearMatieresCache = () => {
  try { localStorage.removeItem(MATIERES_CACHE_KEY) } catch {}
}

const revalidateMatieresInBackground = async () => {
  try {
    if (!userStore.niveau_pays?.id) return
    const response = await getMatieresUtilisateur()
    if (response && response.data && response.data.matieres_disponibles) {
      const fresh = response.data.matieres_disponibles.filter(m => m && m.id && m.nom)
      const currentIds = (matieres.value || []).map(m => m.id).join(',')
      const freshIds = fresh.map(m => m.id).join(',')
      if (currentIds !== freshIds) {
        matieres.value = fresh
      }
      writeMatieresCache(fresh)
    }
  } catch {}
}

const loadMatieres = async ({ useCache = true } = {}) => {
  // Éviter les appels multiples
  if (loading.value) return

  // Si cache valide pour le même niveau, l'utiliser et ne pas afficher le loader
  if (useCache) {
    const cached = readMatieresCache()
    const sameNiveau = cached?.niveauId === (userStore.niveau_pays?.id || null)
    const fresh = cached && Date.now() - cached.ts < MATIERES_CACHE_TTL_MS
    if (cached && sameNiveau && fresh) {
      matieres.value = cached.data.filter(m => m && m.id && m.nom)
      // Revalidation silencieuse pour récupérer les dernières valeurs
      revalidateMatieresInBackground()
      return
    }
  }

  loading.value = true
  try {
    // Si pas de niveau, ne pas appeler l'API inutilement
    if (!userStore.niveau_pays?.id) {
      matieres.value = []
      return
    }

    const response = await getMatieresUtilisateur()
    if (response && response.data && response.data.matieres_disponibles) {
      const items = response.data.matieres_disponibles.filter(m => m && m.id && m.nom)
      matieres.value = items
      writeMatieresCache(items)
      console.log(`[SelectedMatiereHeader] Matières chargées pour utilisateur:`, items.length)
    } else {
      throw new Error('Format de réponse API invalide')
    }
  } catch (error) {
    handleError(error, 'loadMatieres')
    matieres.value = []
  } finally {
    loading.value = false
  }
}

/**
 * Méthodes de gestion des tabs
 */

/**
 * Supprime une matière de la sélection avec animation
 * @param {number} matiereId - L'ID de la matière à supprimer
 */
const removeMatiere = async (matiereId) => {
  if (!isValidMatiereId(matiereId) || loading.value) return
  
  try {
    // Fermer le dropdown si ouvert
    if (showMatiereDropdown.value) {
      closeMatiereDropdown()
    }
    
    subjectsStore.removeMatiereId(matiereId)
    console.log('[SelectedMatiereHeader] Matière retirée:', matiereId)
    
    // Gestion de la matière active
    if (activeMatiereId.value === matiereId) {
      const remainingMatieres = selectedMatieres.value.filter(m => m.id !== matiereId)
      if (remainingMatieres.length > 0) {
        await nextTick()
        setActiveMatiere(remainingMatieres[0].id)
      } else {
        activeMatiereId.value = null
        emit('matiere-changed', null)
      }
    }
  } catch (error) {
    handleError(error, 'removeMatiere')
  }
}

/**
 * Gère les événements de souris sur les onglets (style Google Chrome)
 * @param {MouseEvent} event - L'événement de souris
 * @param {number} matiereId - L'ID de la matière
 */
const handleTabMouseDown = (event, matiereId) => {
  // Bouton du milieu (molette) = fermer l'onglet
  if (event.button === 1) {
    event.preventDefault()
    event.stopPropagation()
    removeMatiere(matiereId)
    return
  }
  
  // Bouton gauche = comportement normal (géré par @click)
  // Bouton droit = menu contextuel (géré par @contextmenu)
}

/**
 * Définit la matière active
 * @param {number} matiereId - L'ID de la matière à activer
 */
const setActiveMatiere = (matiereId) => {
  if (!isValidMatiereId(matiereId) || loading.value || loadingMatiere.value === matiereId) return
  
  try {
    activeMatiereId.value = matiereId
    // Synchroniser avec le store global
    subjectsStore.setActiveMatiere(matiereId)
    emit('matiere-changed', matiereId)
    console.log('[SelectedMatiereHeader] Matière active changée:', matiereId)
  } catch (error) {
    handleError(error, 'setActiveMatiere')
  }
}

/**
 * Méthodes de gestion du dropdown
 */

/**
 * Calcule la position optimale du dropdown
 * @param {HTMLElement|null} anchorEl - Élément d'ancrage optionnel
 * @returns {Object} - Styles CSS pour positionner le dropdown
 */
const calculateDropdownPosition = (anchorEl = null) => {
  const buttonEl = anchorEl || newMatiereButton.value
  if (!buttonEl || typeof buttonEl.getBoundingClientRect !== 'function') return {}
  
  try {
    const buttonRect = buttonEl.getBoundingClientRect()
    const viewportHeight = window.innerHeight
    const viewportWidth = window.innerWidth
    
    // Position de base
    let position = {
      position: 'fixed',
      top: `${buttonRect.bottom + DROPDOWN_OFFSET}px`,
      left: `${buttonRect.left}px`,
      minWidth: `${Math.max(buttonRect.width, 280)}px`,
      maxWidth: `${Math.min(400, viewportWidth - 20)}px`,
      zIndex: 12005
    }
    
    // Ajustement si le dropdown sort de l'écran
    if (buttonRect.bottom + 300 > viewportHeight) {
      position.top = `${buttonRect.top - 300 - DROPDOWN_OFFSET}px`
      position.bottom = 'auto'
    }
    
    if (buttonRect.left + 280 > viewportWidth) {
      position.left = `${viewportWidth - 300}px`
    }
    
    return position
  } catch (error) {
    handleError(error, 'calculateDropdownPosition')
    return {}
  }
}

/**
 * Affiche/masque le dropdown des matières
 */
const toggleMatiereDropdown = async (event) => {
  if (loading.value) return
  
  try {
    showMatiereDropdown.value = !showMatiereDropdown.value
    
    if (showMatiereDropdown.value) {
      await nextTick()
      const anchorEl = (event && event.currentTarget) || newMatiereButton.value || null
      dropdownStyle.value = calculateDropdownPosition(anchorEl)
    } else {
      dropdownStyle.value = {}
    }
  } catch (error) {
    handleError(error, 'toggleMatiereDropdown')
  }
}

/**
 * Ferme le dropdown
 */
const closeMatiereDropdown = () => {
  showMatiereDropdown.value = false
  dropdownStyle.value = {}
}

/**
 * Affiche/masque le dropdown des onglets ouverts
 */
const toggleOpenTabsDropdown = async (event) => {
  if (loading.value) return
  
  try {
    showOpenTabsDropdown.value = !showOpenTabsDropdown.value
    
    if (showOpenTabsDropdown.value) {
      await nextTick()
      const anchorEl = (event && event.currentTarget) || openTabsButton.value || null
      openTabsDropdownStyle.value = calculateDropdownPosition(anchorEl)
    } else {
      openTabsDropdownStyle.value = {}
    }
  } catch (error) {
    handleError(error, 'toggleOpenTabsDropdown')
  }
}

/**
 * Ferme le dropdown des onglets ouverts
 */
const closeOpenTabsDropdown = () => {
  showOpenTabsDropdown.value = false
  openTabsDropdownStyle.value = {}
}

/**
 * Définit la matière active depuis le dropdown des onglets ouverts
 */
const setActiveMatiereFromDropdown = (matiereId) => {
  if (!isValidMatiereId(matiereId) || loading.value) return
  
  setActiveMatiere(matiereId)
  closeOpenTabsDropdown()
}

/**
 * Affiche/masque le dropdown des favoris
 */
const toggleFavoritesDropdown = async (event) => {
  if (loading.value) return
  
  try {
    showFavoritesDropdown.value = !showFavoritesDropdown.value
    
    if (showFavoritesDropdown.value) {
      await nextTick()
      const anchorEl = (event && event.currentTarget) || favoritesButton.value || null
      favoritesDropdownStyle.value = calculateDropdownPosition(anchorEl)
    } else {
      favoritesDropdownStyle.value = {}
    }
  } catch (error) {
    handleError(error, 'toggleFavoritesDropdown')
  }
}

/**
 * Ferme le dropdown des favoris
 */
const closeFavoritesDropdown = () => {
  showFavoritesDropdown.value = false
  favoritesDropdownStyle.value = {}
}

/**
 * Sélectionne une matière depuis le dropdown des favoris
 */
const selectMatiereFromFavoritesDropdown = (matiere) => {
  if (!matiere?.id || loading.value) return
  
  selectMatiere(matiere)
  closeFavoritesDropdown()
}

/**
 * Sélectionne une matière depuis le dropdown ou les favoris
 * @param {Object} matiere - La matière à sélectionner
 */
const selectMatiere = async (matiere) => {
  if (!matiere?.id || loading.value || loadingMatiere.value === matiere.id) return
  
  loadingMatiere.value = matiere.id
  
  try {
    // Ajouter au store si pas déjà présente
    if (!subjectsStore.selectedMatieresIds.includes(matiere.id)) {
      subjectsStore.addMatiereId(matiere.id)
    }
    
    // Définir comme active immédiatement
    activeMatiereId.value = matiere.id
    // Synchroniser avec le store global
    subjectsStore.setActiveMatiere(matiere.id)
    emit('matiere-changed', matiere.id)
    
    // Fermer le dropdown si ouvert
    if (showMatiereDropdown.value) {
      closeMatiereDropdown()
    }
    
    console.log('[SelectedMatiereHeader] Matière sélectionnée et activée:', matiere.nom)
  } catch (error) {
    handleError(error, 'selectMatiere')
  } finally {
    loadingMatiere.value = null
  }
}

/**
 * Méthodes de gestion du menu contextuel
 */

/**
 * Affiche le menu contextuel
 * @param {Event} event - L'événement de clic droit
 * @param {Object} matiere - La matière concernée
 */
const showContextMenu = (event, matiere) => {
  event.preventDefault()
  
  contextMenu.value = {
    visible: true,
    x: event.clientX,
    y: event.clientY,
    matiereId: matiere.id,
    isFavorite: subjectsStore.isFavoriteMatiere(matiere.id)
  }
}

/**
 * Ferme le menu contextuel
 */
const closeContextMenu = () => {
  contextMenu.value.visible = false
}

/**
 * Gère le basculement des favoris depuis le menu contextuel
 * @param {number} matiereId - L'ID de la matière
 */
const handleContextMenuFavoriteToggle = async (matiereId) => {
  await toggleFavorite(matiereId)
}

/**
 * Méthodes de gestion des favoris
 */

/**
 * Bascule le statut favori d'une matière
 * @param {number} matiereId - L'ID de la matière
 */
const toggleFavorite = async (matiereId) => {
  if (!isValidMatiereId(matiereId) || loadingFavorite.value === matiereId) return
  
  loadingFavorite.value = matiereId
  
  try {
    subjectsStore.toggleFavoriteMatiere(matiereId)
    
    const matiere = matieres.value.find(m => m.id === matiereId)
    const isFavorite = subjectsStore.isFavoriteMatiere(matiereId)
    
    console.log(`[SelectedMatiereHeader] ${matiere?.nom || matiereId} ${isFavorite ? 'ajouté aux' : 'retiré des'} favoris`)
  } catch (error) {
    handleError(error, 'toggleFavorite')
  } finally {
    loadingFavorite.value = null
  }
}

/**
 * Bascule l'affichage complet des favoris
 */
const toggleFavoritesVisibility = () => {
  showAllFavorites.value = !showAllFavorites.value
}

/**
 * Gestionnaires d'événements
 */

/**
 * Gère les clics en dehors du composant pour fermer le dropdown
 * @param {Event} event - L'événement de clic
 */
const handleClickOutside = (event) => {
  try {
    // Gérer le dropdown des matières disponibles
    if (showMatiereDropdown.value) {
      const dropdown = document.querySelector('.matiere-dropdown')
      const button = newMatiereButton.value
      const clickedInsideDropdown = dropdown && dropdown.contains(event.target)
      const clickedOnButton = button && button.contains(event.target)
      const clickedOnTabClose = event.target.classList && event.target.classList.contains('tab-close')
      if (!clickedInsideDropdown && !clickedOnButton || clickedOnTabClose) {
        closeMatiereDropdown()
      }
    }
    
    // Gérer le dropdown des onglets ouverts
    if (showOpenTabsDropdown.value) {
      const openTabsDropdown = document.querySelector('.open-tabs-dropdown')
      const openTabsBtn = openTabsButton.value
      const clickedInsideOpenTabs = openTabsDropdown && openTabsDropdown.contains(event.target)
      const clickedOnOpenTabsBtn = openTabsBtn && openTabsBtn.contains(event.target)
      if (!clickedInsideOpenTabs && !clickedOnOpenTabsBtn) {
        closeOpenTabsDropdown()
      }
    }
    
    // Gérer le dropdown des favoris
    if (showFavoritesDropdown.value) {
      const favoritesDropdown = document.querySelector('.favorites-dropdown')
      const favoritesBtn = favoritesButton.value
      const clickedInsideFavorites = favoritesDropdown && favoritesDropdown.contains(event.target)
      const clickedOnFavoritesBtn = favoritesBtn && favoritesBtn.contains(event.target)
      if (!clickedInsideFavorites && !clickedOnFavoritesBtn) {
        closeFavoritesDropdown()
      }
    }
  } catch (error) {
    handleError(error, 'handleClickOutside')
  }
}

/**
 * Gère les raccourcis clavier
 * @param {KeyboardEvent} event - L'événement clavier
 */
const handleKeydown = (event) => {
  try {
    if (event.key === 'Escape') {
      event.preventDefault()
      if (showMatiereDropdown.value) {
        closeMatiereDropdown()
      }
      if (showOpenTabsDropdown.value) {
        closeOpenTabsDropdown()
      }
      if (showFavoritesDropdown.value) {
        closeFavoritesDropdown()
      }
    }
  } catch (error) {
    handleError(error, 'handleKeydown')
  }
}

/**
 * Gère la navigation clavier dans le dropdown
 * @param {KeyboardEvent} event - L'événement clavier
 */
const handleDropdownKeydown = (event) => {
  try {
    const items = document.querySelectorAll('.dropdown-item:not(:disabled)')
    const currentIndex = Array.from(items).findIndex(item => item === document.activeElement)
    
    switch (event.key) {
      case 'ArrowDown':
        event.preventDefault()
        const nextIndex = currentIndex < items.length - 1 ? currentIndex + 1 : 0
        items[nextIndex]?.focus()
        break
        
      case 'ArrowUp':
        event.preventDefault()
        const prevIndex = currentIndex > 0 ? currentIndex - 1 : items.length - 1
        items[prevIndex]?.focus()
        break
        
      case 'Enter':
      case ' ':
        event.preventDefault()
        if (document.activeElement.classList.contains('dropdown-item')) {
          document.activeElement.click()
        }
        break
        
      case 'Escape':
        event.preventDefault()
        closeMatiereDropdown()
        newMatiereButton.value?.focus()
        break
    }
  } catch (error) {
    handleError(error, 'handleDropdownKeydown')
  }
}

/**
 * Cycle de vie du composant
 */

/**
 * Initialisation du composant
 */
onMounted(async () => {
  try {
    // Charger les données initiales
    await Promise.all([
      loadMatieres({ useCache: true }),
      subjectsStore.loadSelectedMatieresIds(),
      subjectsStore.loadFavoriteMatieresIds(),
      subjectsStore.loadActiveMatiereId()
    ])
    
    const availableIds = matieres.value
      .filter(m => m && m.id)
      .map(m => Number(m.id))
      .filter(Number.isFinite)
    
    const storedSelectedIds = Array.isArray(subjectsStore.selectedMatieresIds)
      ? subjectsStore.selectedMatieresIds.map(id => Number(id)).filter(Number.isFinite)
      : []
    const filteredSelectedIds = storedSelectedIds.filter(id => availableIds.includes(id))
    setSelectedMatieresIdsSafely(filteredSelectedIds)

    const storedActiveId = Number(subjectsStore.activeMatiereId) || null
    const hasValidActive = Boolean(storedActiveId && availableIds.includes(storedActiveId))

    if (hasValidActive) {
      if (!filteredSelectedIds.includes(storedActiveId)) {
        setSelectedMatieresIdsSafely([...filteredSelectedIds, storedActiveId])
      }
      activeMatiereId.value = storedActiveId
    } else {
      await ensurePreferredMatiereActive()
    }
    
    // Configurer les event listeners
    document.addEventListener('click', handleClickOutside, { passive: true })
    document.addEventListener('keydown', handleKeydown, { passive: true })
    _onResize = () => {
      if (showMatiereDropdown.value) {
        dropdownStyle.value = calculateDropdownPosition(newMatiereButton.value || null)
      }
    }
    window.addEventListener('resize', _onResize, { passive: true })

    // Invalidation manuelle déclenchée ailleurs (après mise à jour admin)
    const onInvalidate = () => {
      clearMatieresCache()
      loadMatieres({ useCache: false })
    }
    window.addEventListener('matieres-cache:invalidate', onInvalidate)
    // Sauvegarder pour cleanup
    _listeners.push(onInvalidate)
  } catch (error) {
    handleError(error, 'onMounted')
  }
})

/**
 * Nettoyage lors de la destruction du composant
 */
const _listeners = []
let _onResize = null

onUnmounted(() => {
  try {
    document.removeEventListener('click', handleClickOutside)
    document.removeEventListener('keydown', handleKeydown)
    if (_onResize) {
      window.removeEventListener('resize', _onResize)
    }
    for (const fn of _listeners) {
      window.removeEventListener('matieres-cache:invalidate', fn)
    }
    console.log('[SelectedMatiereHeader] Composant détruit - nettoyage effectué')
  } catch (error) {
    handleError(error, 'onUnmounted')
  }
})

/**
 * Observateurs (Watchers)
 */

// Surveillance des changements de prop matiereId
watch(() => props.matiereId, async (newId) => {
  if (!isValidMatiereId(newId)) return
  
  try {
    console.log('[SelectedMatiereHeader] ID de matière changé:', newId)
    
    // Charger les matières si nécessaire
    if (matieres.value.length === 0) {
      await loadMatieres()
    }
    
    // Ajouter la matière si elle n'est pas déjà sélectionnée
    if (!subjectsStore.selectedMatieresIds.includes(Number(newId))) {
      subjectsStore.addMatiereId(newId)
    }
    
    // Définir comme active si aucune matière n'est active
    if (!activeMatiereId.value) {
      setActiveMatiere(Number(newId))
    }
  } catch (error) {
    handleError(error, 'watch matiereId')
  }
}, { immediate: true })

// Surveillance des changements dans les matières sélectionnées
watch(() => selectedMatieres.value, async (newMatieres, oldMatieres) => {
  try {
    console.log('[SelectedMatiereHeader] Changement dans les matières sélectionnées:', {
      nouvelles: newMatieres.map(m => m.id),
      anciennes: oldMatieres?.map(m => m.id) || [],
      matiereActive: activeMatiereId.value
    })
    
    // Si on a des matières mais pas de matière active, prendre la matière active du store global
    if (!activeMatiereId.value && newMatieres.length > 0) {
      const storeActiveMatiereId = Number(subjectsStore.activeMatiereId) || null
      
      // Si le store a une matière active qui est dans les sélectionnées, l'utiliser
      if (storeActiveMatiereId && newMatieres.find(m => m.id === storeActiveMatiereId)) {
        activeMatiereId.value = storeActiveMatiereId
        return
      }

      // Sinon, forcer une matière préférée (Mathématiques) pour éviter l'état vide
      await ensurePreferredMatiereActive()
    }
  } catch (error) {
    handleError(error, 'watch selectedMatieres')
  }
})

// Surveillance des changements de niveau de l'utilisateur
const normalizeMatiereLabel = (value = '') => {
  return (value || '')
    .toString()
    .normalize('NFD')
    .replace(/\p{Diacritic}/gu, '')
    .toLowerCase()
}

const findPreferredMatiere = () => {
  if (!Array.isArray(matieres.value) || matieres.value.length === 0) return null
  const normalizedTarget = 'mathem'
  const preferred = matieres.value.find((matiere) => {
    const label = normalizeMatiereLabel(matiere.nom || matiere.titre || '')
    return label.includes(normalizedTarget)
  })
  return preferred || matieres.value[0] || null
}

const ensurePreferredMatiereActive = async () => {
  const preferred = findPreferredMatiere()
  if (!preferred || !preferred.id) return null
  const preferredId = Number(preferred.id)
  if (!preferredId) return null

  const selectedIds = Array.isArray(subjectsStore.selectedMatieresIds)
    ? subjectsStore.selectedMatieresIds.map(id => Number(id))
    : []
  const alreadySelected = selectedIds.includes(preferredId)
  if (!alreadySelected) {
    await subjectsStore.addMatiereId(preferredId)
  }

  setActiveMatiere(preferredId)
  return preferred
}

const setSelectedMatieresIdsSafely = (ids = []) => {
  try {
    const selectedModule = subjectsStore?.stores?.selected
    if (selectedModule?.setSelectedMatieresIds) {
      selectedModule.setSelectedMatieresIds(ids)
    } else {
      subjectsStore.selectedMatieresIds = ids
    }
  } catch (error) {
    handleError(error, 'setSelectedMatieresIdsSafely')
  }
}

watch(() => userStore.niveau_pays, async (newNiveau) => {
  if (!newNiveau) return

  try {
    console.log('[SelectedMatiereHeader] Niveau changé, rechargement des matières:', newNiveau.nom)
    await loadMatieres()

    const availableMatiereIds = matieres.value
      .filter(m => m && m.id)
      .map(m => Number(m.id))
      .filter(Number.isFinite)

    const selectedIds = Array.isArray(subjectsStore.selectedMatieresIds)
      ? subjectsStore.selectedMatieresIds.map(id => Number(id)).filter(Number.isFinite)
      : []

    const filteredSelected = selectedIds.filter(id => availableMatiereIds.includes(id))
    setSelectedMatieresIdsSafely(filteredSelected)
    await ensurePreferredMatiereActive()
  } catch (error) {
    handleError(error, 'watch userStore.niveau_pays')
  }
}, { immediate: false })

// Surveillance des changements de la matière active dans le store global
watch(() => subjectsStore.activeMatiereId, async (newActiveMatiereId) => {
  try {
    console.log('[SelectedMatiereHeader] Matière active changée dans le store:', newActiveMatiereId)
    
    // Synchroniser l'état local avec le store si différent
    if (newActiveMatiereId !== activeMatiereId.value) {
      // Vérifier que la matière est dans les sélectionnées
      if (newActiveMatiereId && selectedMatieres.value.find(m => m.id === newActiveMatiereId)) {
        activeMatiereId.value = newActiveMatiereId
        emit('matiere-changed', newActiveMatiereId)
        console.log('[SelectedMatiereHeader] État local synchronisé avec le store:', newActiveMatiereId)
      }
      // Si la matière du store n'est pas sélectionnée, l'ajouter
      else if (newActiveMatiereId && !subjectsStore.selectedMatieresIds.includes(newActiveMatiereId)) {
        subjectsStore.addMatiereId(newActiveMatiereId)
        console.log('[SelectedMatiereHeader] Matière ajoutée automatiquement aux sélectionnées:', newActiveMatiereId)
      } else if (!newActiveMatiereId && selectedMatieres.value.length > 0) {
        await ensurePreferredMatiereActive()
      }
    }
} catch (error) {
  handleError(error, 'watch store activeMatiereId')
}
}, { immediate: false })
</script>

<style scoped>
.selected-matiere-header {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 0;
  position: relative;
  gap: 0.5rem;
  background: #ffffff;
  /* Assurer l'alignement des favoris avec les onglets */
  align-items: flex-start;
}

/* État de chargement amélioré */
.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  padding: 1rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 8px;
  color: #64748b;
  font-size: 0.95rem;
  border: 1px solid #e2e8f0;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #e2e8f0;
  border-top: 2px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Style des tabs comme Google Chrome */
.matieres-tabs {
  width: 100%;
  position: relative;
  /* Assurer que les onglets restent toujours visibles */
  min-height: 60px;
  display: flex;
  flex-direction: column;
}

.tabs-container {
  display: flex;
  gap: 4px;
  width: 100%;
  background: #ffffff;
  border-radius: 6px;
  padding: 1px;
  overflow-x: auto;
  overflow-y: hidden;
  margin-bottom: 0;
  /* Assurer que les onglets restent toujours visibles */
  flex-shrink: 0;
  /* Scroll horizontal fluide */
  scroll-behavior: smooth;
  /* Masquer la scrollbar par défaut mais permettre le scroll */
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 transparent;
}

/* Masquer la scrollbar sur webkit mais permettre le scroll */
.tabs-container::-webkit-scrollbar {
  height: 4px;
}

.tabs-container::-webkit-scrollbar-track {
  background: transparent;
}

.tabs-container::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.tabs-container::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.matiere-tab {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 3px;
  padding: 0.22rem 0.6rem;
  padding-right: 1.8rem; /* espace pour le bouton fermer à droite */
  font-size: 0.75rem;
  color: #64748b;
  cursor: pointer;
  white-space: nowrap;
  min-width: 100px;
  max-width: 160px;
  position: relative;
  flex-shrink: 0;
  height: 28px;
  line-height: 26px;
  /* Assurer que les onglets ne se cassent pas */
  box-sizing: border-box;
}

.matiere-tab:hover {
  /* Pas de changement visuel au hover pour garder fixe */
}

.matiere-tab:focus {
  outline: none;
  /* Pas de changement visuel au focus pour garder fixe */
}

.matiere-tab:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

.matiere-tab.active {
  background: #ffffff;
  color: #3b82f6;
  border-color: #3b82f6;
  box-shadow: 0 1px 3px rgba(59, 130, 246, 0.1);
  font-weight: 500;
  z-index: 10;
}

.matiere-tab.active::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #3b82f6 0%, #1d4ed8 100%);
  border-radius: 3px 3px 0 0;
}

.matiere-tab.loading {
  opacity: 0.7;
  cursor: not-allowed;
  pointer-events: none;
}

.matiere-tab.loading::after {
  content: '';
  position: absolute;
  top: 50%;
  right: 8px;
  width: 12px;
  height: 12px;
  border: 1px solid #e2e8f0;
  border-top: 1px solid #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  transform: translateY(-50%);
}

/* Style spécial pour le tab "New Matière" */
.matiere-tab.new-tab {
  background: #eff6ff; /* bleu très léger pour attirer l'œil */
  color: #1d4ed8;
  border: 1px solid #93c5fd;
  position: relative;
  box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4);
  animation: matierePulse 1.6s ease-in-out infinite;
}

.matiere-tab.new-tab:hover {
  /* Pas de changement visuel au hover pour garder fixe */
}

.matiere-tab.new-tab:disabled {
  background: #f8fafc;
  color: #cbd5e1;
  border-color: #e2e8f0;
}

/* Halo pulsant autour du bouton "New Matière" pour guider l'utilisateur */
.matiere-tab.new-tab::after {
  content: '';
  position: absolute;
  inset: -4px;
  border-radius: 6px;
  border: 2px solid rgba(59, 130, 246, 0.45);
  opacity: 0;
  animation: haloPulse 1.6s ease-out infinite;
  pointer-events: none;
}

@keyframes matierePulse {
  0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.35); }
  50% { box-shadow: 0 0 0 6px rgba(59, 130, 246, 0.08); }
  100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.0); }
}

@keyframes haloPulse {
  0% { opacity: 0; transform: scale(0.98); }
  50% { opacity: 1; transform: scale(1); }
  100% { opacity: 0; transform: scale(1.02); }
}

/* Style pour le petit bouton "+" à droite (comme Google Chrome) */
.matiere-tab.new-tab-small {
  background: #f1f5f9;
  color: #64748b;
  border: 1px dashed #cbd5e1;
  position: relative;
  min-width: 32px;
  max-width: 32px;
  padding: 0.15rem 0.4rem;
  justify-content: center;
}

.matiere-tab.new-tab-small:hover {
  /* Pas de changement visuel au hover pour garder fixe */
}

.matiere-tab.new-tab-small:disabled {
  background: #f8fafc;
  color: #cbd5e1;
  border-color: #e2e8f0;
}

.matiere-tab.new-tab-small .tab-icon {
  font-size: 0.75rem;
  font-weight: bold;
  color: #64748b;
}

.tab-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 14px;
  height: 14px;
  font-size: 0.75rem;
  color: #64748b;
  flex-shrink: 0;
}

.tab-icon svg {
  width: 14px;
  height: 14px;
  display: block;
}

.matiere-tab.active .tab-icon {
  color: #3b82f6;
}

.matiere-tab.new-tab .tab-icon {
  font-size: 0.75rem;
  font-weight: bold;
  color: #64748b;
}

.tab-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 500;
}

.tab-initials {
  display: none;
  font-weight: 700;
  color: #64748b;
  letter-spacing: 0.02em;
}

.tab-close {
  background: none;
  border: none;
  color: #9ca3af;
  font-size: 0.85rem;
  font-weight: bold;
  cursor: pointer;
  padding: 1px;
  border-radius: 3px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  opacity: 0.6;
}

.tab-close:hover {
  opacity: 1;
  background: #fee2e2;
  color: #ef4444;
}

.tab-close:focus {
  outline: none;
  opacity: 1;
  background: #fee2e2;
  color: #ef4444;
  box-shadow: 0 0 0 2px #ef4444;
}

.tab-close:disabled {
  opacity: 0.3;
  cursor: not-allowed;
  pointer-events: none;
}

/* Style pour le dropdown */
.matiere-dropdown {
  position: fixed; /* pour sortir des contexts overflow */
  z-index: 12005; /* au-dessus du header et du contenu */
  min-width: 200px;
  max-width: 280px;
  width: max-content;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  margin-top: 4px;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid #e5e7eb;
  background: #ffffff;
}

.dropdown-title {
  font-size: 0.9rem;
  font-weight: 500;
  color: #64748b;
}

.dropdown-close {
  background: none;
  border: none;
  color: #9ca3af;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  transition: all 0.15s ease;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  opacity: 0.6;
}

.dropdown-close:hover {
  opacity: 1;
  background: #fee2e2;
  color: #ef4444;
  transform: scale(1.05);
}

.dropdown-close:focus {
  outline: none;
  opacity: 1;
  background: #fee2e2;
  color: #ef4444;
  box-shadow: 0 0 0 2px #ef4444;
}



.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  transition: all 0.15s ease;
  background: #ffffff;
  border-bottom: 1px solid #f1f5f9;
  justify-content: space-between;
}

.dropdown-item.last-item {
  border-bottom: none;
  padding: 0.5rem 0.75rem 0.5rem 0.75rem;
}

.dropdown-item:hover {
  background: #ffffff;
  color: #3b82f6;
  border-color: #e5e7eb;
}

.dropdown-item:active {
  background: #ffffff;
  transform: translateX(0);
  color: #64748b;
}

.dropdown-item:focus {
  outline: none;
  background: #ffffff;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15);
}

.dropdown-item.loading {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

.dropdown-item.loading::after {
  content: '';
  position: absolute;
  right: 3rem;
  width: 14px;
  height: 14px;
  border: 1px solid #e2e8f0;
  border-top: 1px solid #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.dropdown-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  color: #64748b;
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  border-radius: 4px;
  background: #f8fafc;
}

.dropdown-content-left {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

.dropdown-name {
  font-size: 0.85rem;
  font-weight: 500;
  color: #64748b;
}

.dropdown-star {
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: #f59e0b;
  font-size: 1rem;
  cursor: pointer;
  padding: 2px;
  border-radius: 4px;
  width: 24px;
  height: 28px;
  flex-shrink: 0;
  transition: all 0.15s ease;
}

.dropdown-star:hover {
  transform: scale(1.1);
}

.dropdown-star:focus {
  outline: none;
  box-shadow: 0 0 0 2px #f59e0b;
}

.dropdown-star.favorite {
  color: #f59e0b;
}

.dropdown-star.loading {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

.star-icon {
  transition: transform 0.15s ease;
}

.dropdown-star:hover .star-icon {
  transform: scale(1.2);
}

.dropdown-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem 1rem;
  color: #9ca3af;
  font-size: 0.9rem;
  text-align: center;
}

.empty-icon {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
  opacity: 0.6;
}

.empty-text {
  font-weight: 500;
  line-height: 1.5;
}

/* Section des favoris - POSITION STATIQUE POUR ÉVITER LE CHEVAUCHEMENT */
.favorites-bar {
  display: flex;
  align-items: center;
  background: transparent;
  border: none;
  border-radius: 0;
  padding: 0;
  margin-top: 0.5rem;
  box-shadow: none;
  position: relative;
  height: 28px;
  /* Aligner avec les onglets */
  width: 100%;
  flex-shrink: 0;
  justify-content: flex-start;
}

.favorites-container {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  overflow-x: auto;
  width: 100%;
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 transparent;
}

.favorites-label {
  display: flex;
  align-items: center;
  gap: 0.2rem;
  background: transparent;
  border: none;
  border-radius: 0;
  padding: 0;
  font-size: 0.75rem;
  color: #64748b;
  flex-shrink: 0;
  box-shadow: none;
}

.favorites-icon {
  font-size: 0.8rem;
  color: #fbbf24;
}

.favorites-text {
  font-weight: 600;
  color: #64748b;
  letter-spacing: 0.025em;
}

.favorites-list {
  display: flex;
  gap: 0.25rem;
  overflow-x: auto;
  flex: 1;
  padding: 0 0.15rem;
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 transparent;
}

.favorite-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 3px;
  padding: 0.15rem 0.4rem;
  font-size: 0.75rem;
  color: #64748b;
  cursor: pointer;
  white-space: nowrap;
  height: 24px;
  flex-shrink: 0;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
}

.favorite-item:hover {
  /* Pas de changement visuel au hover pour garder fixe */
}

.favorite-item:focus {
  outline: none;
  /* Pas de changement visuel au focus pour garder fixe */
}

.favorite-item.active {
  background: #ffffff;
  border-color: #3b82f6;
  color: #1e40af;
  font-weight: 600;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1);
}

.favorite-icon {
  width: 14px;
  height: 14px;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.7;
  flex-shrink: 0;
  color: #94a3b8;
}

.favorite-name {
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  letter-spacing: 0.025em;
  color: inherit;
}

/* Initiales des favoris: masquées par défaut, visibles en mode compact */
.favorite-initials {
  display: none;
  font-weight: 700;
  letter-spacing: 0.02em;
  color: #64748b;
}

.favorites-toggle {
  background: #ffffff;
  color: #64748b;
  border: 1px solid #e5e7eb;
  border-radius: 3px;
  padding: 0.15rem;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 24px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
}

.favorites-toggle:hover {
  /* Pas de changement visuel au hover pour garder fixe */
}

.favorites-toggle:focus {
  outline: none;
  /* Pas de changement visuel au focus pour garder fixe */
}

/* Scrollbar pour le dropdown */
.matiere-dropdown::-webkit-scrollbar,
.dropdown-content::-webkit-scrollbar {
  width: 6px;
}

.matiere-dropdown::-webkit-scrollbar-track,
.dropdown-content::-webkit-scrollbar-track {
  background: #f8fafc;
  border-radius: 3px;
}

.matiere-dropdown::-webkit-scrollbar-thumb,
.dropdown-content::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.matiere-dropdown::-webkit-scrollbar-thumb:hover,
.dropdown-content::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Scrollbar pour les favoris */
.favorites-container::-webkit-scrollbar,
.favorites-list::-webkit-scrollbar {
  height: 3px;
}

.favorites-container::-webkit-scrollbar-track,
.favorites-list::-webkit-scrollbar-track {
  background: transparent;
}

.favorites-container::-webkit-scrollbar-thumb,
.favorites-list::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.favorites-container::-webkit-scrollbar-thumb:hover,
.favorites-list::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Scrollbar pour les tabs */
.tabs-container::-webkit-scrollbar {
  height: 4px;
}

.tabs-container::-webkit-scrollbar-track {
  background: transparent;
}

.tabs-container::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.tabs-container::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Désactiver les animations pour les onglets */
.matiere-tab,
.favorite-item {
  will-change: auto;
}

/* Bouton liste déroulante des onglets ouverts (masqué par défaut, visible < 500px) */
.open-tabs-btn {
  display: none;
  align-items: center;
  gap: 0.25rem;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 3px;
  padding: 0.22rem 0.6rem;
  font-size: 0.75rem;
  color: #64748b;
  cursor: pointer;
  white-space: nowrap;
  flex: 1;
  max-width: 280px;
  min-width: 180px;
  height: 28px;
  line-height: 26px;
  box-sizing: border-box;
}

.open-tabs-btn:hover {
  /* Pas de changement visuel au hover pour garder fixe */
}

.open-tabs-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.dropdown-arrow {
  font-size: 0.65rem;
  color: #64748b;
  flex-shrink: 0;
}

.active-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: 500;
  color: #64748b;
}

/* Dropdown des onglets ouverts */
.open-tabs-dropdown {
  position: fixed;
  z-index: 12005;
  min-width: 220px;
  max-width: 320px;
  width: max-content;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.open-tabs-dropdown .dropdown-item.active {
  background: #eff6ff;
  border-left: 3px solid #3b82f6;
}

.dropdown-close-tab {
  background: none;
  border: none;
  color: #9ca3af;
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.dropdown-close-tab:hover {
  background: #fee2e2;
  color: #ef4444;
}

.dropdown-close-tab:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

/* Bouton dropdown favoris (masqué par défaut, visible < 500px) - largeur automatique complète */
.favorites-dropdown-btn {
  display: none;
  align-items: center;
  gap: 0.25rem;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 3px;
  padding: 0.22rem 0.6rem;
  font-size: 0.75rem;
  color: #64748b;
  cursor: pointer;
  white-space: nowrap;
  width: 100%;
  height: 28px;
  line-height: 26px;
  box-sizing: border-box;
}

.favorites-dropdown-btn:hover {
  /* Pas de changement visuel au hover pour garder fixe */
}

.favorites-dropdown-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.favorites-dropdown-btn .favorites-icon {
  font-size: 0.8rem;
  color: #fbbf24;
  flex-shrink: 0;
}

.favorites-dropdown-btn .dropdown-arrow {
  font-size: 0.65rem;
  color: #64748b;
  flex-shrink: 0;
}

.favorites-dropdown-text {
  font-weight: 600;
  color: #64748b;
}

/* Dropdown des favoris */
.favorites-dropdown {
  position: fixed;
  z-index: 12005;
  min-width: 220px;
  max-width: 320px;
  width: max-content;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.favorites-dropdown .dropdown-item.active {
  background: #fef3c7;
  border-left: 3px solid #fbbf24;
}

/* Responsive Design - Garder les dimensions fixes jusqu'à 768px */
@media (max-width: 1100px) {
  /* Pas de changement de dimensions - garder fixe */
}

@media (max-width: 1024px) {
  /* Pas de changement de dimensions - garder fixe */
}

@media (max-width: 768px) {
  /* Pas de changement - garder les onglets identiques jusqu'à 500px */
}

/* Garder les onglets fixes jusqu'à 500px */
@media (max-width: 550px) {
  /* Pas de changement - garder les onglets identiques */
}

/* Liste déroulante à partir de 500px */
@media (max-width: 500px) {
  /* Afficher le bouton liste déroulante des onglets */
  .open-tabs-btn {
    display: flex !important;
  }
  
  /* Masquer les onglets individuels */
  .matiere-tab.desktop-tab {
    display: none !important;
  }
  
  /* Afficher le bouton liste déroulante des favoris */
  .favorites-dropdown-btn {
    display: flex !important;
  }
  
  /* Masquer le label "Favoris:" */
  .favorites-label {
    display: none !important;
  }
  
  /* Masquer les favoris individuels */
  .favorite-item.desktop-favorite {
    display: none !important;
  }
  
  /* Masquer le bouton toggle des favoris */
  .favorites-toggle {
    display: none !important;
  }
}

/* Les changements sont maintenant gérés dans le breakpoint 500px ci-dessus */

/* Assurer que les onglets restent visibles en mode paysage sur mobile */
@media (max-height: 500px) and (orientation: landscape) {
  .selected-matiere-header {
    min-height: 35px;
    /* Maintenir l'alignement des favoris */
    align-items: flex-start;
  }
  
  .matiere-tab {
    height: 20px;
    font-size: 0.7rem;
  }
  
  .favorites-bar {
    display: flex; /* Garder visible en mode paysage */
    height: 24px;
    margin-top: 0.2rem;
  }
}

/* Accessibilité */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Support pour le mode sombre */
@media (prefers-color-scheme: dark) {
  .selected-matiere-header {
    background: #ffffff;
  }
  
  .matiere-tab,
  .matiere-dropdown,
  .dropdown-header,
  .dropdown-item,
  .favorites-bar,
  .favorites-label,
  .favorite-item,
  .favorites-toggle {
    background: #ffffff;
    border-color: #e5e7eb;
    color: #64748b;
  }
  
  .matiere-tab:hover,
  .dropdown-item:hover,
  .favorite-item:hover,
  .favorites-toggle:hover {
    /* Pas de changement visuel au hover pour garder fixe */
  }
  
  .matiere-tab.active {
    background: #ffffff;
    border-color: #3b82f6;
    color: #3b82f6;
  }
}

/* Effet visuel pour le clic de la molette (style Google Chrome) */
.matiere-tab:active { /* neutralize motion without empty rule */
  transform: none;
}

/* Mode contraste élevé */
@media (prefers-contrast: high) {
  .matiere-tab {
    border: 2px solid;
  }
  
  .matiere-tab.active {
    border-color: #000;
    background: #fff;
    color: #000;
  }
  
  .dropdown-item:focus {
    box-shadow: inset 4px 0 0 #000;
  }
  
  .favorite-item:focus {
    box-shadow: 0 0 0 3px #000;
  }
}
</style>
