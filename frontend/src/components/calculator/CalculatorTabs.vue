<template>
  <div class="calculator-tab-wrapper">
    <nav class="calculator-tab-bar" aria-label="Opérations de calcul">
      <!-- Mode mobile compact (450px et moins) : un seul onglet avec dropdown complet -->
      <div v-if="isMobileCompact" class="mobile-compact-container">
        <button
          class="calculator-tab mobile-compact-btn"
          type="button"
          @click="toggleMobileMenu"
          ref="mobileButton"
        >
          <component :is="activeTabIcon" class="tab-icon" aria-hidden="true" />
          <span class="tab-label">{{ activeTabName }}</span>
          <ChevronDownIcon class="tab-icon-arrow" aria-hidden="true" />
        </button>

        <!-- Dropdown mobile complet -->
        <div v-if="showMobileMenu" class="mobile-dropdown" ref="mobileDropdown">
          <button
            v-for="tab in allTabs"
            :key="tab.id"
            class="dropdown-item"
            :class="{ active: activeTab === tab.id }"
            @click="selectTab(tab.id)"
          >
            <component :is="tab.icon" class="dropdown-icon" />
            <span>{{ tab.name }}</span>
          </button>
        </div>
      </div>

      <!-- Mode normal : onglets visibles + menu Plus -->
      <template v-else>
        <!-- Onglets principaux -->
        <button
          v-for="tab in mainTabs"
          :key="tab.id"
          class="calculator-tab"
          :class="{ active: activeTab === tab.id }"
          type="button"
          @click="selectTab(tab.id)"
        >
          <component :is="tab.icon" class="tab-icon" aria-hidden="true" />
          <span class="tab-label">{{ tab.name }}</span>
        </button>

        <!-- Menu Plus -->
        <div class="plus-menu-container" v-if="moreTabs.length > 0">
          <button
            class="calculator-tab plus-btn"
            :class="{ active: isMoreTabActive }"
            type="button"
            @click="togglePlusMenu"
            ref="plusButton"
          >
            <EllipsisHorizontalIcon class="tab-icon" aria-hidden="true" />
            <span class="tab-label">Plus</span>
          </button>

          <!-- Dropdown -->
          <div v-if="showPlusMenu" class="plus-dropdown" ref="plusDropdown">
            <button
              v-for="tab in moreTabs"
              :key="tab.id"
              class="dropdown-item"
              :class="{ active: activeTab === tab.id }"
              @click="selectTab(tab.id)"
            >
              <component :is="tab.icon" class="dropdown-icon" />
              <span>{{ tab.name }}</span>
            </button>
          </div>
        </div>
      </template>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  ArrowTrendingUpIcon,
  Square3Stack3DIcon,
  ChartBarIcon,
  MinusIcon,
  PlusIcon,
  CubeIcon,
  EllipsisHorizontalIcon,
  ChevronDownIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const route = useRoute()
const showPlusMenu = ref(false)
const showMobileMenu = ref(false)
const plusButton = ref(null)
const plusDropdown = ref(null)
const mobileButton = ref(null)
const mobileDropdown = ref(null)
const windowWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1920)

// Tous les onglets disponibles
const allTabs = [
  {
    id: 'graph',
    name: 'Graphique',
    icon: ChartBarIcon
  },
  {
    id: 'integral',
    name: 'Intégrale',
    icon: Square3Stack3DIcon
  },
  {
    id: 'derivative',
    name: 'Dérivée',
    icon: ArrowTrendingUpIcon
  },
  {
    id: 'expand',
    name: 'Développement',
    icon: PlusIcon
  },
  {
    id: 'factor',
    name: 'Factorisation',
    icon: CubeIcon
  },
  {
    id: 'limit',
    name: 'Limite',
    icon: MinusIcon
  }
]

// Mode mobile compact (450px et moins)
const isMobileCompact = computed(() => windowWidth.value <= 450)

// Onglets principaux (responsive selon la largeur d'écran)
const mainTabs = computed(() => {
  if (isMobileCompact.value) {
    return [] // Pas d'onglets principaux en mode mobile compact
  }
  if (windowWidth.value <= 520) {
    // À 520px et moins, on garde les 2 premiers onglets
    return allTabs.slice(0, 2)
  }
  if (windowWidth.value <= 930) {
    // À 930px et moins, on garde les 3 premiers onglets
    return allTabs.slice(0, 3)
  }
  if (windowWidth.value <= 1070) {
    // À 1070px et moins, on garde les 4 premiers onglets
    return allTabs.slice(0, 4)
  }
  // Au-dessus de 1070px, on affiche les 5 premiers
  return allTabs.slice(0, 5)
})

// Onglets dans le menu "Plus" (responsive)
const moreTabs = computed(() => {
  if (isMobileCompact.value) {
    return [] // Pas de menu Plus en mode mobile compact
  }
  if (windowWidth.value <= 520) {
    // À 520px et moins, les 4 derniers vont dans "Plus"
    return allTabs.slice(2)
  }
  if (windowWidth.value <= 930) {
    // À 930px et moins, les 3 derniers vont dans "Plus"
    return allTabs.slice(3)
  }
  if (windowWidth.value <= 1070) {
    // À 1070px et moins, les 2 derniers vont dans "Plus"
    return allTabs.slice(4)
  }
  // Au-dessus de 1070px, seulement le dernier
  return allTabs.slice(5)
})

// Informations de l'onglet actif pour le mode mobile compact
const activeTabData = computed(() => {
  return allTabs.find(tab => tab.id === activeTab.value) || allTabs[0]
})

const activeTabName = computed(() => activeTabData.value.name)
const activeTabIcon = computed(() => activeTabData.value.icon)

const activeTab = computed(() => route.query.operation || 'graph')

const isMoreTabActive = computed(() => {
  return moreTabs.value.some(tab => tab.id === activeTab.value)
})

const selectTab = (tabId) => {
  showPlusMenu.value = false
  showMobileMenu.value = false
  if (tabId === activeTab.value) return

  router.push({
    name: 'Calculator',
    query: { operation: tabId }
  }).catch(() => {})
}

const togglePlusMenu = () => {
  showPlusMenu.value = !showPlusMenu.value
}

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const handleClickOutside = (event) => {
  if (showPlusMenu.value &&
      plusButton.value &&
      plusDropdown.value &&
      !plusButton.value.contains(event.target) &&
      !plusDropdown.value.contains(event.target)) {
    showPlusMenu.value = false
  }
  if (showMobileMenu.value &&
      mobileButton.value &&
      mobileDropdown.value &&
      !mobileButton.value.contains(event.target) &&
      !mobileDropdown.value.contains(event.target)) {
    showMobileMenu.value = false
  }
}

const handleResize = () => {
  if (typeof window !== 'undefined') {
    windowWidth.value = window.innerWidth
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('resize', handleResize, { passive: true })
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.calculator-tab-wrapper {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  height: 100%;
  width: 100%;
}

.calculator-tab-bar {
  display: flex;
  align-items: center;
  justify-content: flex-start; /* Alignement à gauche */
  gap: 0;
  margin: 0;
  padding: 0;
  background: transparent;
  height: 100%;
  margin-left: 0; /* Force l'alignement à gauche */
}

/* Mode mobile compact : centrage */
@media (max-width: 450px) {
  .calculator-tab-wrapper {
    justify-content: center;
  }
  
  .calculator-tab-bar {
    justify-content: center;
    width: auto;
  }
}

.calculator-tab {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0 0.85rem;
  height: 40px;
  border: none;
  border-radius: 0;
  background: transparent;
  color: #475569;
  font-weight: 600;
  font-size: 0.82rem;
  cursor: pointer;
  position: relative;
  transition: background 0.2s ease, color 0.2s ease, box-shadow 0.2s ease;
  white-space: nowrap;
}

.calculator-tab:not(:last-child)::after {
  content: '';
  position: absolute;
  right: -0.125rem;
  top: 50%;
  transform: translateY(-50%);
  height: 60%;
  width: 1px;
  background: rgba(203, 213, 225, 0.5);
  transition: opacity 0.2s ease;
}

.calculator-tab:hover {
  background: rgba(59, 130, 246, 0.1);
  color: #2563eb;
}

.calculator-tab.active {
  background: #3b82f6;
  color: #fff;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.calculator-tab.active::after,
.calculator-tab:hover::after {
  opacity: 0;
}

.calculator-tab:focus-visible {
  outline: 2px solid rgba(59, 130, 246, 0.45);
  outline-offset: 2px;
}

.tab-icon {
  width: 1.15rem;
  height: 1.15rem;
  flex-shrink: 0;
}

.tab-label {
  letter-spacing: 0.02em;
}

/* Menu Plus */
.plus-menu-container {
  position: relative;
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.plus-btn {
  position: relative;
}

.plus-btn::before {
  content: '';
  position: absolute;
  left: -0.125rem;
  top: 50%;
  transform: translateY(-50%);
  height: 60%;
  width: 1px;
  background: rgba(203, 213, 225, 0.5);
  transition: opacity 0.2s ease;
}

.plus-btn:hover::before,
.plus-btn.active::before {
  opacity: 0;
}

.plus-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  border: 1px solid #e2e8f0;
  min-width: 200px;
  z-index: 13000;
  overflow: hidden;
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem 1rem;
  border: none;
  background: white;
  color: #475569;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
  border-bottom: 1px solid #f1f5f9;
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item:hover {
  background: rgba(59, 130, 246, 0.1);
  color: #2563eb;
}

.dropdown-item.active {
  background: rgba(59, 130, 246, 0.15);
  color: #2563eb;
  font-weight: 600;
}

.dropdown-icon {
  width: 1.15rem;
  height: 1.15rem;
  flex-shrink: 0;
}

/* Mode mobile compact (450px et moins) */
.mobile-compact-container {
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mobile-compact-btn {
  flex: 0 0 auto;
  min-width: 0;
  max-width: 90%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 1rem;
  gap: 0.5rem;
}

.tab-icon-arrow {
  width: 1.1rem;
  height: 1.1rem;
  flex-shrink: 0;
  opacity: 0.7;
  margin-left: 0.25rem;
  transition: transform 0.2s ease;
}

.mobile-compact-btn:hover .tab-icon-arrow {
  transform: translateY(2px);
}

.mobile-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: -90px;
  transform: none;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  border: 1px solid #e2e8f0;
  min-width: 220px;
  max-width: calc(100vw - 2rem);
  z-index: 13000;
  overflow: hidden;
  animation: slideDown 0.2s ease-out;
}

/* Responsive */
@media (max-width: 768px) {
  .calculator-tab {
    padding: 0 0.7rem;
    gap: 0.35rem;
    font-size: 0.8rem;
  }

  .tab-icon {
    width: 1rem;
    height: 1rem;
  }

  .dropdown-icon {
    width: 1rem;
    height: 1rem;
  }
}

</style>
