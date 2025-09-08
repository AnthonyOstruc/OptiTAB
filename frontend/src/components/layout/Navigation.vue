<template>
  <nav class="navigation">
    <!-- Main navigation items on the left -->
    <div class="nav-items">
      <div 
        v-for="item in leftMenuItems" 
        :key="item.key"
        class="nav-item cursor-pointer"
        @click="handleItemClick(item)"
      >
        <component :is="item.icon" class="nav-icon" />
        <span class="nav-text">{{ item.text }}</span>
      </div>
    </div>

    <!-- Onglets de matières (centre) -->
    <div v-if="shouldShowMatieresTab" class="matieres-tabs">
      <!-- Onglets des matières sélectionnées -->
      <div class="tabs-container">
        <div 
          v-for="matiere in selectedMatieres" 
          :key="`tab-${matiere.id}`"
          :class="['matiere-tab', { active: subjectsStore.activeMatiereId === matiere.id }]"
          @click="setActiveMatiere(matiere.id)"
          @mousedown="handleTabMouseDown($event, matiere.id)"
        >
          <span class="tab-name">{{ matiere.nom }}</span>
          <button 
            class="tab-close"
            @click.stop="removeMatiere(matiere.id)"
          >
            ×
          </button>
        </div>
        
        <!-- Bouton pour ajouter une matière -->
        <button 
          v-if="availableMatieres.length > 0"
          class="matiere-tab new-tab"
          @click="toggleMatieresDropdown"
        >
          <span class="tab-icon">+</span>
        </button>
      </div>
      
      <!-- Dropdown des matières disponibles -->
      <div v-if="showMatieresDropdown" class="matieres-dropdown">
        <div
          v-for="matiere in availableMatieres" 
          :key="`dropdown-${matiere.id}`"
          class="dropdown-item"
          @click="selectMatiere(matiere)"
        >
          <span class="dropdown-icon" v-html="matiere.svg_icon || '📚'"></span>
          <span class="dropdown-name">{{ matiere.nom }}</span>
        </div>
      </div>
    </div>

    <!-- Auth and contact items on the right -->
    <div class="right-items">
      <component 
        :is="item.external ? 'a' : 'div'"
        v-for="item in rightMenuItems" 
        :key="item.key"
        :href="item.external ? item.href : undefined"
        :target="item.external ? '_blank' : undefined"
        :rel="item.external ? 'noopener noreferrer' : undefined"
        :class="['right-item', 'cursor-pointer', item.key === 'login' ? 'btn-login' : '']"
        @click="handleItemClick(item)"
      >
        <component :is="item.icon" class="right-icon" />
        <span class="right-text">{{ item.text }}</span>
      </component>
    </div>
  </nav>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { menuItems } from '@/config/menuItems'

import { useSubjectsStore } from '@/stores/subjects/index'
import { useUserStore } from '@/stores/user'
import { getMatieresUtilisateur } from '@/api/matieres.js'

const emit = defineEmits(['open-login'])
const router = useRouter()
const route = useRoute()
const subjectsStore = useSubjectsStore()
const userStore = useUserStore()


// État pour les matières
const matieres = ref([])
const showMatieresDropdown = ref(false)
const isLoadingMatieres = ref(false)

// Left side: Main navigation items
const leftMenuItems = computed(() => {
  return menuItems.filter(item => 
    ['cours', 'calculator', 'exercices', 'quiz', 'fiches'].includes(item.key)
  )
})

// Right side: Contact and authentication
const rightMenuItems = computed(() => {
  return menuItems.filter(item => 
    ['contact', 'login'].includes(item.key)
  )
})

// Matières sélectionnées pour les onglets
const selectedMatieres = computed(() => {
  return matieres.value.filter(m => 
    m && m.id && subjectsStore.selectedMatieresIds.includes(m.id)
  )
})

// Matières disponibles pour le dropdown
const availableMatieres = computed(() => {
  return matieres.value.filter(m => 
    m && m.id && !subjectsStore.selectedMatieresIds.includes(m.id)
  )
})

// Pages où afficher les onglets de matières
const shouldShowMatieresTab = computed(() => {
  return ['Quiz', 'Exercises', 'Sheets', 'Notions', 'QuizNotions', 'QuizChapitres', 'Chapitres', 'ChapterExercises', 'ChapterQuiz'].includes(route.name)
})

const handleItemClick = async (item) => {
  try {
    if (item.emit) {
      emit(item.emit)
      return
    }
    
    // Navigation externe (email, etc.)
    if (item.external && item.href) {
      window.open(item.href, '_blank', 'noopener,noreferrer')
      return
    }
    
    // Navigation intelligente pour les sections avec matières
    if (['exercices', 'fiches', 'quiz'].includes(item.key)) {
      console.log(`[Navigation] Navigation vers: ${item.key}`)
      // Navigation intelligente - à implémenter selon les besoins
      return
    }
    
    // Navigation normale pour les autres liens
    if (item.href && !item.external) {
      console.log(`[Navigation] Navigation normale vers: ${item.href}`)
      await router.push(item.href)
    }
  } catch (error) {
    console.error(`[Navigation] Erreur lors de la navigation pour ${item.key}:`, error)
    // Fallback vers navigation normale
    if (item.href && !item.external) {
      await router.push(item.href)
    }
  }
}

// Fonctions de gestion des matières
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

const invalidateMatieresCache = () => {
  try { localStorage.removeItem(MATIERES_CACHE_KEY) } catch {}
  try { window.dispatchEvent(new Event('matieres-cache:invalidate')) } catch {}
}

const loadMatieres = async ({ useCache = true } = {}) => {
  if (!userStore.niveau_pays?.id) {
    matieres.value = []
    return
  }

  // Essayer le cache pour ce niveau
  if (useCache) {
    const cached = readMatieresCache()
    const sameNiveau = cached?.niveauId === (userStore.niveau_pays?.id || null)
    const fresh = cached && Date.now() - cached.ts < MATIERES_CACHE_TTL_MS
    if (cached && sameNiveau && fresh) {
      matieres.value = cached.data.filter(m => m && m.id && m.nom)
      return
    }
  }

  try {
    isLoadingMatieres.value = true
    const response = await getMatieresUtilisateur()
    const items = response.data.matieres_disponibles.filter(m => m && m.id && m.nom)
    matieres.value = items
    writeMatieresCache(items)
    console.log(`[Navigation] Matières chargées pour utilisateur:`, items.length)
  } catch (error) {
    console.error('[Navigation] Erreur lors du chargement des matières:', error)
    matieres.value = []
  } finally {
    isLoadingMatieres.value = false
  }
}

const setActiveMatiere = (matiereId) => {
  subjectsStore.setActiveMatiere(matiereId)
  console.log('[Navigation] Matière active définie:', matiereId)
}

const selectMatiere = (matiere) => {
  if (!subjectsStore.selectedMatieresIds.includes(matiere.id)) {
    subjectsStore.addMatiereId(matiere.id)
  }
  setActiveMatiere(matiere.id)
  showMatieresDropdown.value = false
}

const removeMatiere = (matiereId) => {
  subjectsStore.removeMatiereId(matiereId)
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

const toggleMatieresDropdown = () => {
  showMatieresDropdown.value = !showMatieresDropdown.value
}

// Watcher pour recharger les matières quand le niveau change
watch(() => userStore.niveau_pays, async (newNiveau) => {
  if (newNiveau) {
    console.log('[Navigation] Niveau changé, rechargement des matières:', newNiveau.nom)
    await loadMatieres()
    // Nettoyer les matières sélectionnées qui ne sont plus disponibles pour ce niveau
    const availableMatiereIds = matieres.value.map(m => m.id)
    subjectsStore.selectedMatieresIds = subjectsStore.selectedMatieresIds.filter(id => 
      availableMatiereIds.includes(id)
    )
  }
}, { immediate: false })

// Initialisation
onMounted(async () => {
  await Promise.all([
    loadMatieres({ useCache: true }),
    subjectsStore.initialize()
  ])
})
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;

.navigation {
  @extend .flex-between;
  width: 100%;
  gap: 20px;
}

.nav-items {
  @extend .flex;
  gap: 15px;
  flex-wrap: wrap;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  text-decoration: none;
  color: #10257f;
  font-weight: 500;
  border-radius: 6px;
  transition: all 0.2s ease;
  
  &:hover {
    background: rgba(102, 126, 234, 0.1);
    color: #667eea;
  }
}

.nav-icon {
  width: 20px;
  height: 20px;
}

.nav-text {
  font-size: 14px;
}

.right-items {
  @extend .flex;
  gap: 10px;
}

.right-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding:8px 12px;
  text-decoration: none;
  color: #10257f;
  font-weight: 500;
  border-radius: 6px;
  transition: all 0.2s ease;
  
  &:hover {
    background: rgba(102, 126, 234, 0.1);
    color: #667eea;
  }
  
  // Special styling for login button
  &:last-child {
    background: #667eea;
    color: white;
    
    &:hover {
      background: #5a67d8;
      transform: translateY(-1px);
    }
  }
}

.right-icon {
  width: 18px;
  height: 18px;
}

.right-text {
  font-size: 14px;
}

// Styles pour les onglets de matières
.matieres-tabs {
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
}

.tabs-container {
  display: flex;
  gap: 2px;
  align-items: center;
}

.matiere-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 12px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
  max-width: 120px;

  &:hover {
    background: #f1f5f9;
    border-color: #cbd5e1;
  }

  &.active {
    background: #3b82f6;
    color: white;
    border-color: #3b82f6;
    font-weight: 500;
  }

  &.new-tab {
    background: #f1f5f9;
    border: 1px dashed #cbd5e1;
    color: #64748b;
    min-width: 32px;
    max-width: 32px;
    justify-content: center;
    padding: 6px;

    &:hover {
      background: #e2e8f0;
      border-color: #94a3b8;
    }
  }
}

.tab-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.tab-close {
  background: none;
  border: none;
  color: inherit;
  font-size: 14px;
  cursor: pointer;
  padding: 0;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 2px;
  opacity: 0.7;

  &:hover {
    opacity: 1;
    background: rgba(255, 255, 255, 0.2);
  }
}

.tab-icon {
  font-size: 14px;
  font-weight: bold;
}

.matieres-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 1000;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  min-width: 200px;
  margin-top: 4px;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  cursor: pointer;
  transition: background-color 0.15s ease;
  border-bottom: 1px solid #f1f5f9;

  &:last-child {
    border-bottom: none;
  }

  &:hover {
    background: #f8fafc;
  }
}

.dropdown-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

.dropdown-name {
  font-size: 13px;
  color: #374151;
  font-weight: 500;
}

/* Effet visuel pour le clic de la molette (style Google Chrome) */
.matiere-tab:active {
  transform: scale(0.95);
  transition: transform 0.1s ease;
}

// Mobile screens - hide navigation, show hamburger
@media (max-width: #{$max-width-media}) {
  .navigation {
    display: none;
  }
}
</style> 