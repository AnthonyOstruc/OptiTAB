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
  },
  description: {
    type: String,
    default: 'Selectionne la ressource la plus utile pour ton objectif du moment.'
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

function resolveCardKey(card) {
  return String(card?.key || card?.type || '').trim().toLowerCase()
}

function resolveIcon(card) {
  const key = resolveCardKey(card)
  return iconByKey[key] || BookOpenIcon
}

function resolveTone(card) {
  const key = resolveCardKey(card)
  if (key === 'exercise') return 'exercise'
  if (key === 'summary') return 'summary'
  return 'course'
}

function resolveBadge(card) {
  const value = String(card?.badge || '').trim()
  return value || 'Acces gratuit'
}

function resolveHint(card) {
  return String(card?.hint || '').trim()
}

function resolveCta(card) {
  const value = String(card?.cta || '').trim()
  return value || 'Decouvrir'
}

function resolveSeoLabel(card) {
  const explicit = String(card?.seoLabel || '').trim()
  if (explicit) return explicit

  const title = String(card?.title || 'cette ressource').trim().toLowerCase()
  return `Acceder a ${title}`
}

function isActive(card) {
  const key = resolveCardKey(card)
  const active = String(props.activeKey || '').trim().toLowerCase()
  return Boolean(active && key && active === key)
}
</script>

<template>
  <section class="top-action-cards" aria-label="Acces rapide aux ressources">
    <div class="top-action-cards__heading">
      <h2 class="top-action-cards__title">{{ title }}</h2>
      <p class="top-action-cards__description">{{ description }}</p>
    </div>

    <div class="top-action-cards__grid">
      <RouterLink
        v-for="card in resolvedCards"
        :key="card.key || card.type || card.title"
        class="top-action-cards__card"
        :class="[
          `top-action-cards__card--${resolveTone(card)}`,
          { 'is-active': isActive(card) }
        ]"
        :to="card.to"
        :aria-label="resolveSeoLabel(card)"
        :title="resolveSeoLabel(card)"
      >
        <span class="top-action-cards__badge">{{ resolveBadge(card) }}</span>

        <div class="top-action-cards__icon" aria-hidden="true">
          <component :is="resolveIcon(card)" />
        </div>

        <div class="top-action-cards__body">
          <h3 class="top-action-cards__card-title">{{ card.title }}</h3>
          <p class="top-action-cards__card-subtitle">{{ card.subtitle }}</p>
          <p v-if="resolveHint(card)" class="top-action-cards__hint">{{ resolveHint(card) }}</p>
        </div>

        <span class="top-action-cards__cta">
          {{ resolveCta(card) }}
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
  gap: 14px;
}

.top-action-cards__heading {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.top-action-cards__title {
  margin: 0;
  font-size: 1.16rem;
  font-weight: 900;
  color: #0f172a;
  letter-spacing: -0.01em;
}

.top-action-cards__description {
  margin: 0;
  font-size: 0.88rem;
  color: #475569;
  line-height: 1.5;
}

.top-action-cards__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.top-action-cards__card {
  --card-accent: #2563eb;
  --card-accent-rgb: 37, 99, 235;
  --card-soft-rgb: 239, 246, 255;
  --card-ring: rgba(37, 99, 235, 0.24);

  position: relative;
  display: grid;
  grid-template-columns: auto 1fr;
  grid-template-rows: auto 1fr auto;
  column-gap: 12px;
  row-gap: 10px;
  align-items: start;
  border: 1px solid #d8e1ef;
  border-radius: 16px;
  padding: 14px;
  min-height: 170px;
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
  text-decoration: none;
  overflow: hidden;
  opacity: 0;
  transform: translateY(8px);
  animation: top-card-reveal 0.45s ease forwards;
  transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
}

.top-action-cards__card:nth-child(2) {
  animation-delay: 0.08s;
}

.top-action-cards__card:nth-child(3) {
  animation-delay: 0.16s;
}

.top-action-cards__card::after {
  content: '';
  position: absolute;
  inset: auto -40% -55% auto;
  width: 190px;
  height: 190px;
  border-radius: 999px;
  background: radial-gradient(circle, rgba(37, 99, 235, 0.16) 0%, rgba(37, 99, 235, 0) 70%);
  pointer-events: none;
}

.top-action-cards__card:hover {
  transform: translateY(-2px);
  border-color: var(--card-ring);
  box-shadow: 0 16px 28px rgba(15, 23, 42, 0.1);
}

.top-action-cards__card:focus-visible {
  outline: 2px solid rgba(37, 99, 235, 0.4);
  outline-offset: 2px;
}

.top-action-cards__card.is-active {
  border-color: var(--card-accent);
  box-shadow: 0 12px 24px rgba(37, 99, 235, 0.18);
}

.top-action-cards__card--exercise {
  --card-accent: #0f766e;
  --card-accent-rgb: 15, 118, 110;
  --card-soft-rgb: 240, 253, 250;
  --card-ring: rgba(15, 118, 110, 0.28);
}

.top-action-cards__card--summary {
  --card-accent: #b45309;
  --card-accent-rgb: 180, 83, 9;
  --card-soft-rgb: 255, 247, 237;
  --card-ring: rgba(180, 83, 9, 0.28);
}

.top-action-cards__badge {
  grid-column: 1 / -1;
  justify-self: start;
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 4px 10px;
  border: 1px solid rgba(var(--card-accent-rgb), 0.34);
  color: var(--card-accent);
  background: rgba(var(--card-soft-rgb), 0.84);
  font-size: 0.67rem;
  font-weight: 800;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

.top-action-cards__icon {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: rgba(var(--card-soft-rgb), 0.76);
  color: var(--card-accent);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: inset 0 0 0 1px rgba(var(--card-accent-rgb), 0.24);
}

.top-action-cards__icon :deep(svg) {
  width: 20px;
  height: 20px;
}

.top-action-cards__body {
  min-width: 0;
}

.top-action-cards__card-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 900;
  color: #0f172a;
}

.top-action-cards__card-subtitle {
  margin: 4px 0 0;
  font-size: 0.82rem;
  line-height: 1.45;
  color: #334155;
}

.top-action-cards__hint {
  margin: 8px 0 0;
  font-size: 0.75rem;
  line-height: 1.35;
  color: #64748b;
}

.top-action-cards__cta {
  grid-column: 1 / -1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  border-radius: 12px;
  border: 1px solid rgba(var(--card-accent-rgb), 0.24);
  color: var(--card-accent);
  background: rgba(var(--card-soft-rgb), 0.72);
  padding: 8px 11px;
  font-size: 0.77rem;
  font-weight: 800;
  line-height: 1.2;
}

.top-action-cards__cta :deep(svg) {
  width: 15px;
  height: 15px;
  transition: transform 0.18s ease;
}

.top-action-cards__card:hover .top-action-cards__cta :deep(svg) {
  transform: translateX(2px);
}

@keyframes top-card-reveal {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .top-action-cards__card {
    opacity: 1;
    transform: none;
    animation: none;
  }
}

@media (max-width: 1024px) {
  .top-action-cards__grid {
    grid-template-columns: 1fr;
  }

  .top-action-cards__card {
    min-height: 0;
  }
}

@media (max-width: 560px) {
  .top-action-cards__title {
    font-size: 1.04rem;
  }

  .top-action-cards__description {
    font-size: 0.83rem;
  }

  .top-action-cards__card {
    padding: 12px;
    row-gap: 8px;
  }
}
</style>
