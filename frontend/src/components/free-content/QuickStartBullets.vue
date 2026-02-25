<script setup>
import { computed } from 'vue'
import { FREE_RESOURCES_QUICK_START_ITEMS } from '@/config/freeResourcesUx'

const props = defineProps({
  title: {
    type: String,
    default: 'En 10 secondes'
  },
  items: {
    type: Array,
    default: () => FREE_RESOURCES_QUICK_START_ITEMS
  }
})

const resolvedItems = computed(() => {
  if (Array.isArray(props.items) && props.items.length > 0) {
    return props.items
  }
  return FREE_RESOURCES_QUICK_START_ITEMS
})
</script>

<template>
  <section class="quick-start-bullets" aria-label="Guide de démarrage rapide">
    <h2 class="quick-start-bullets__title">{{ title }}</h2>
    <ul class="quick-start-bullets__list">
      <li v-for="item in resolvedItems" :key="item" class="quick-start-bullets__item">
        {{ item }}
      </li>
    </ul>
  </section>
</template>

<style scoped>
.quick-start-bullets {
  border: 1px solid rgba(59, 130, 246, 0.22);
  border-radius: 14px;
  padding: 12px 14px;
  background: linear-gradient(135deg, rgba(239, 246, 255, 0.85), #ffffff);
}

.quick-start-bullets__title {
  margin: 0 0 8px;
  font-size: 0.96rem;
  font-weight: 800;
  color: #0f172a;
}

.quick-start-bullets__list {
  margin: 0;
  padding-left: 18px;
  display: grid;
  gap: 4px;
}

.quick-start-bullets__item {
  color: #334155;
  font-size: 0.84rem;
  line-height: 1.45;
}
</style>
