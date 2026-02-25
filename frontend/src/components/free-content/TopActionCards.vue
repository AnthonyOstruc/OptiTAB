<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { BookOpenIcon, AcademicCapIcon, DocumentTextIcon, ArrowRightIcon } from '@heroicons/vue/24/outline'
import { FREE_RESOURCES_ACTION_CARDS } from '@/config/freeResourcesUx'

const props = defineProps({
  cards: {
    type: Array,
    default: () => []
  },
  activeKey: {
    type: String,
    default: ''
  },
  title: {
    type: String,
    default: 'Choisis ton format'
  }
})

const resolvedCards = computed(() => {
  if (Array.isArray(props.cards) && props.cards.length > 0) {
    return props.cards
  }
  return FREE_RESOURCES_ACTION_CARDS
})

const iconByKey = Object.freeze({
  course: BookOpenIcon,
  exercise: AcademicCapIcon,
  summary: DocumentTextIcon
})

function resolveIcon(card) {
  const key = String(card?.key || card?.type || '').trim().toLowerCase()
  return iconByKey[key] || BookOpenIcon
}

function isActive(card) {
  const key = String(card?.key || card?.type || '').trim().toLowerCase()
  const active = String(props.activeKey || '').trim().toLowerCase()
  return Boolean(active && key && active === key)
}
</script>

<template>
  <section class="top-action-cards" aria-label="Accès rapide aux ressources">
    <h2 class="top-action-cards__title">{{ title }}</h2>
    <div class="top-action-cards__grid">
      <RouterLink
        v-for="card in resolvedCards"
        :key="card.key || card.type || card.title"
        class="top-action-cards__card"
        :class="{ 'is-active': isActive(card) }"
        :to="card.to"
      >
        <div class="top-action-cards__icon">
          <component :is="resolveIcon(card)" />
        </div>
        <div class="top-action-cards__body">
          <h3 class="top-action-cards__card-title">{{ card.title }}</h3>
          <p class="top-action-cards__card-subtitle">{{ card.subtitle }}</p>
        </div>
        <span class="top-action-cards__cta">
          Ouvrir
          <ArrowRightIcon />
        </span>
      </RouterLink>
    </div>
  </section>
</template>

<style scoped>
.top-action-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.top-action-cards__title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 800;
  color: #0f172a;
}

.top-action-cards__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.top-action-cards__card {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 10px;
  align-items: center;
  border: 1px solid #dbe2f0;
  border-radius: 14px;
  padding: 12px;
  background: #fff;
  text-decoration: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
}

.top-action-cards__card:hover {
  border-color: #93c5fd;
  box-shadow: 0 10px 20px rgba(37, 99, 235, 0.1);
  transform: translateY(-1px);
}

.top-action-cards__card.is-active {
  border-color: #2563eb;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(255, 255, 255, 1));
}

.top-action-cards__icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: #eff6ff;
  color: #1d4ed8;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.top-action-cards__icon :deep(svg) {
  width: 18px;
  height: 18px;
}

.top-action-cards__body {
  min-width: 0;
}

.top-action-cards__card-title {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 800;
  color: #0f172a;
}

.top-action-cards__card-subtitle {
  margin: 2px 0 0;
  font-size: 0.78rem;
  line-height: 1.35;
  color: #475569;
}

.top-action-cards__cta {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 0.75rem;
  font-weight: 700;
  color: #1d4ed8;
  white-space: nowrap;
}

.top-action-cards__cta :deep(svg) {
  width: 14px;
  height: 14px;
}

@media (max-width: 960px) {
  .top-action-cards__grid {
    grid-template-columns: 1fr;
  }
}
</style>
