<template>
  <div class="resource-tab-wrapper">
    <button
      class="nav-arrow nav-arrow-left"
      type="button"
      aria-label="Onglet précédent"
      @click="goToPrevious"
    >
      <ChevronLeftIcon class="arrow-icon" />
    </button>

    <nav class="resource-tab-bar" aria-label="Types de ressources gratuites">
      <button
        v-for="tab in resourceTabs"
        :key="tab.resourceType"
        class="resource-tab"
        :class="{ active: tab.resourceType === activeType }"
        type="button"
        data-track="nav"
        :data-nav-name="tab.navName"
        data-nav-location="header_public"
        @click="goToTab(tab)">
        <component :is="tab.icon" class="tab-icon" aria-hidden="true" />
        <span class="tab-label">{{ tab.label }}</span>
      </button>
    </nav>

    <button
      class="nav-arrow nav-arrow-right"
      type="button"
      aria-label="Onglet suivant"
      @click="goToNext"
    >
      <ChevronRightIcon class="arrow-icon" />
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  BookOpenIcon,
  DocumentTextIcon,
  AcademicCapIcon,
  ChevronLeftIcon,
  ChevronRightIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const route = useRoute()

const resourceTabs = [
  { label: 'Cours', routeName: 'FreeCourses', relatedNames: ['FreeCourses', 'FreeCourseDetail'], resourceType: 'course', navName: 'course', icon: BookOpenIcon },
  { label: 'Synthèse', routeName: 'FreeSummaries', relatedNames: ['FreeSummaries', 'FreeSummaryDetail'], resourceType: 'summary', navName: 'summary', icon: DocumentTextIcon },
  { label: 'Exercices', routeName: 'FreeExercises', relatedNames: ['FreeExercises', 'FreeExerciseDetail', 'FreeExerciseChapter'], resourceType: 'exercise', navName: 'exercise', icon: AcademicCapIcon }
]

const activeType = computed(() => {
  const currentName = route.name || ''
  const match = resourceTabs.find((tab) => tab.relatedNames.includes(currentName))
  return match ? match.resourceType : 'course'
})

const goToTab = (tab) => {
  if (!tab || tab.resourceType === activeType.value) return
  router.push({ name: tab.routeName }).catch(() => {})
}

const activeIndex = computed(() => {
  const currentName = route.name || ''
  return Math.max(
    resourceTabs.findIndex((tab) => tab.relatedNames.includes(currentName)),
    0
  )
})

const goToPrevious = () => {
  const previousIndex =
    activeIndex.value === 0 ? resourceTabs.length - 1 : activeIndex.value - 1
  goToTab(resourceTabs[previousIndex])
}

const goToNext = () => {
  const nextIndex =
    activeIndex.value === resourceTabs.length - 1 ? 0 : activeIndex.value + 1
  goToTab(resourceTabs[nextIndex])
}
</script>

<style scoped>
.resource-tab-wrapper {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  min-width: 0;
  gap: 0.5rem;
  height: 100%;
}

.resource-tab-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  max-width: 460px;
  width: 100%;
  margin: 0;
  padding: 0;
  background: transparent;
  border: none;
  border-radius: 0;
  box-shadow: none;
  height: 100%;
}

.resource-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  padding: 0 1rem;
  height: 40px;
  border: none;
  border-radius: 0;
  background: transparent;
  color: #475569;
  font-weight: 600;
  font-size: 0.86rem;
  cursor: pointer;
  position: relative;
  transition: background 0.2s ease, color 0.2s ease, box-shadow 0.2s ease;
}

.resource-tab:not(:last-child)::after {
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

.resource-tab:hover {
  background: rgba(59, 130, 246, 0.1);
  color: #2563eb;
}

.resource-tab.active {
  background: #3b82f6;
  color: #fff;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.resource-tab.active::after,
.resource-tab:hover::after {
  opacity: 0;
}

.resource-tab:focus-visible {
  outline: 2px solid rgba(59, 130, 246, 0.45);
  outline-offset: 2px;
}

.tab-icon {
  width: 1.15rem;
  height: 1.15rem;
}

.tab-label {
  letter-spacing: 0.02em;
}

.nav-arrow {
  display: none;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  background: #ffffff;
  color: #475569;
  cursor: pointer;
  border-radius: 999px;
  box-shadow: 0 6px 18px rgba(15, 23, 42, 0.12);
  transition: color 0.2s ease, background 0.2s ease, box-shadow 0.2s ease;
}

.nav-arrow:hover {
  color: #2563eb;
  border-color: rgba(37, 99, 235, 0.3);
  box-shadow: 0 10px 20px rgba(37, 99, 235, 0.2);
}

.arrow-icon {
  width: 1.25rem;
  height: 1.25rem;
}

@media (max-width: 640px) {
  .resource-tab-bar {
    max-width: 85%;
    padding: 0.15rem;
  }

  .resource-tab {
    padding: 0 0.7rem;
    gap: 0.35rem;
    font-size: 0.8rem;
  }

  .tab-icon {
    width: 1rem;
    height: 1rem;
  }
}

@media (max-width: 480px) {
  .resource-tab-bar {
    max-width: 75%;
    padding: 0.15rem;
  }

  .resource-tab {
    padding: 0 0.55rem;
    gap: 0.3rem;
    font-size: 0.75rem;
  }

  .tab-icon {
    width: 0.95rem;
    height: 0.95rem;
  }
}

@media (max-width: 530px) {
  .resource-tab-wrapper {
    justify-content: center;
    gap: 0.4rem;
  }

  .nav-arrow {
    display: flex;
    width: 36px;
    height: 36px;
  }

  .resource-tab:not(.active) {
    display: none;
  }

  .resource-tab-bar {
    max-width: 190px;
    padding: 0;
  }

  .resource-tab.active {
    border-radius: 12px;
    width: 100%;
    font-size: 0.8rem;
  }
}

@media (max-width: 340px) {
  .resource-tab-bar {
    max-width: 160px;
  }

  .resource-tab.active {
    font-size: 0.75rem;
    gap: 0.3rem;
    padding: 0 0.5rem;
  }

  .nav-arrow {
    width: 32px;
    height: 32px;
  }

  .arrow-icon {
    width: 0.95rem;
    height: 0.95rem;
  }
}
</style>
