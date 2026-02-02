<template>
  <nav v-if="items.length" class="breadcrumbs" aria-label="Fil d'ariane">
    <ol class="breadcrumbs__list">
      <li
        v-for="(item, index) in items"
        :key="`${item.label || item.name}-${index}`"
        class="breadcrumbs__item"
      >
        <router-link
          v-if="item.to && index < items.length - 1"
          :to="item.to"
          class="breadcrumbs__link"
        >
          {{ item.label || item.name }}
        </router-link>
        <span v-else class="breadcrumbs__current" aria-current="page">
          {{ item.label || item.name }}
        </span>
        <span v-if="index < items.length - 1" class="breadcrumbs__sep">›</span>
      </li>
    </ol>
  </nav>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    default: () => []
  }
})
</script>

<style scoped>
.breadcrumbs {
  width: 100%;
}

.breadcrumbs__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
  font-size: 12px;
  color: #64748b;
}

.breadcrumbs__item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.breadcrumbs__link {
  color: #2563eb;
  font-weight: 600;
  text-decoration: none;
}

.breadcrumbs__link:hover {
  text-decoration: underline;
}

.breadcrumbs__current {
  color: #0f172a;
  font-weight: 700;
}

.breadcrumbs__sep {
  color: #94a3b8;
}
</style>
