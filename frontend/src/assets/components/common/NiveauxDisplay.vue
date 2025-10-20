<template>
  <div class="niveaux-display">
    <span 
      v-for="niveau in niveaux" 
      :key="niveau.id"
      class="niveau-badge-small"
      :style="{ backgroundColor: niveau.couleur, color: '#fff' }"
    >
      {{ niveau.nom }}
    </span>
    <span v-if="!niveaux || niveaux.length === 0" class="no-niveaux">
      {{ noNiveauxText }}
    </span>
  </div>
</template>

<script setup>
defineProps({
  niveaux: {
    type: Array,
    default: () => []
  },
  noNiveauxText: {
    type: String,
    default: 'Aucun niveau'
  }
})
</script>

<style scoped>
.niveaux-display {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.niveau-badge-small {
  display: inline-block;
  padding: 1px 6px;
  border-radius: 10px;
  font-size: 0.7rem;
  font-weight: 500;
  text-align: center;
  min-width: 40px;
  color: white;
}

.no-niveaux {
  color: #6b7280;
  font-style: italic;
  font-size: 0.9rem;
}
</style> 