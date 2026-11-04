<template>
  <figure v-if="f" class="qz-fig">
    <img :src="f.src" :width="f.w" :height="f.h" alt="" loading="lazy" decoding="async" />
  </figure>
</template>

<script setup>
// Figure d'un quiz (style des livres) : affichée à la moitié de sa taille en
// pixels, comme les figures des cours, sans jamais déborder.
defineProps({
  f: { type: Object, default: null }
})
</script>

<style scoped>
.qz-fig {
  display: flex;
  justify-content: center;
  margin: 0;
}

.qz-fig img {
  display: block;
  max-width: 100%;
  height: auto;
}
</style>
