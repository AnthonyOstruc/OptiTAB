<template>
  <ol class="tl">
    <li v-for="(etape, index) in etapes" :key="etape.titre" class="tl__item">
      <span class="tl__node" aria-hidden="true">
        <component :is="etape.icone" v-if="etape.icone" />
        <template v-else>{{ index + 1 }}</template>
      </span>
      <div class="tl__card">
        <p class="tl__meta">
          <span class="tl__step">{{ etape.etiquette || `Étape ${index + 1}` }}</span>
          <span v-if="etape.badge" class="tl__badge">{{ etape.badge }}</span>
        </p>
        <h3 class="tl__title">{{ etape.titre }}</h3>
        <p class="tl__text">{{ etape.texte }}</p>
      </div>
    </li>
  </ol>
</template>

<script setup>
defineProps({
  // [{ titre, texte, etiquette?, badge?, icone? (composant) }]
  etapes: { type: Array, required: true }
})
</script>

<style scoped>
.tl {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin: 0;
  padding: 0;
  list-style: none;
}

/* Le fil qui relie les étapes, dans l'ordre. */
.tl::before {
  content: '';
  position: absolute;
  top: 24px;
  bottom: 24px;
  left: 23px;
  width: 2px;
  background: linear-gradient(180deg, var(--vt-navy) 0%, var(--vt-green) 100%);
  opacity: 0.35;
}

.tl__item {
  position: relative;
  display: grid;
  grid-template-columns: 48px minmax(0, 1fr);
  gap: 18px;
  align-items: start;
}

.tl__node {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: var(--vt-navy);
  box-shadow: 0 0 0 5px #fff;
  font-size: 17px;
  font-weight: 700;
  color: #fff;
}

.tl__item:last-child .tl__node {
  background: var(--vt-green-700);
}

.tl__node :deep(svg) {
  width: 24px;
  height: 24px;
}

.tl__card {
  padding: 18px 22px;
  border: 1px solid var(--vt-line);
  border-radius: var(--vt-radius);
  background: #fff;
  box-shadow: 0 1px 2px rgba(16, 32, 79, 0.04);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.tl__item:hover .tl__card {
  border-color: var(--vt-navy-100);
  box-shadow: var(--vt-shadow);
}

.tl__meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px 10px;
  margin: 0 0 4px;
}

.tl__step {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--vt-green-700);
}

.tl__badge {
  padding: 2px 9px;
  border-radius: 999px;
  background: var(--vt-green-50);
  font-size: 12px;
  font-weight: 700;
  color: var(--vt-green-700);
}

.tl__title {
  font-size: 19px;
}

.tl__text {
  margin: 8px 0 0;
  font-size: 15px;
  line-height: 1.65;
  color: var(--vt-muted);
}

@media (max-width: 640px) {
  .tl::before {
    left: 19px;
  }

  .tl__item {
    grid-template-columns: 40px minmax(0, 1fr);
    gap: 12px;
  }

  .tl__node {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    font-size: 15px;
  }

  .tl__node :deep(svg) {
    width: 20px;
    height: 20px;
  }

  .tl__card {
    padding: 14px 16px;
  }

  .tl__title {
    font-size: 17px;
  }
}
</style>
