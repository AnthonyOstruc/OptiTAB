<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { FREE_RESOURCES_LEVEL_LINKS } from '@/config/freeResourcesUx'

const props = defineProps({
  basePath: {
    type: String,
    default: '/ressources-gratuites/cours'
  },
  title: {
    type: String,
    default: 'Accès rapide par niveau'
  },
  levels: {
    type: Array,
    default: () => FREE_RESOURCES_LEVEL_LINKS
  }
})

const resolvedLevels = computed(() => {
  if (Array.isArray(props.levels) && props.levels.length > 0) {
    return props.levels
  }
  return FREE_RESOURCES_LEVEL_LINKS
})

function levelTo(level) {
  const queryValue = String(level?.query || '').trim()
  return {
    path: props.basePath,
    query: queryValue ? { q: queryValue } : undefined
  }
}
</script>

<template>
  <section class="quick-links-by-level" aria-label="Liens rapides par niveau">
    <h2 class="quick-links-by-level__title">{{ title }}</h2>
    <ul class="quick-links-by-level__list">
      <li v-for="level in resolvedLevels" :key="level.key || level.label" class="quick-links-by-level__item">
        <RouterLink class="quick-links-by-level__link" :to="levelTo(level)">
          {{ level.label }}
        </RouterLink>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.quick-links-by-level {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.quick-links-by-level__title {
  margin: 0;
  font-size: 1rem;
  font-weight: 800;
  color: #0f172a;
}

.quick-links-by-level__list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.quick-links-by-level__item {
  margin: 0;
}

.quick-links-by-level__link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 7px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 999px;
  text-decoration: none;
  color: #1d4ed8;
  font-size: 0.82rem;
  font-weight: 700;
  background: #fff;
  transition: border-color 0.2s ease, background-color 0.2s ease;
}

.quick-links-by-level__link:hover {
  border-color: #93c5fd;
  background: #eff6ff;
}
</style>
