<template>
  <div class="ring" :style="{ width: size + 'px', height: size + 'px' }">
    <svg :viewBox="`0 0 ${size} ${size}`" aria-hidden="true">
      <circle :cx="size / 2" :cy="size / 2" :r="rayon" class="ring__track" :stroke-width="epaisseur" />
      <circle
        :cx="size / 2"
        :cy="size / 2"
        :r="rayon"
        class="ring__fill"
        :class="{ 'ring__fill--done': pct >= 100 }"
        :stroke-width="epaisseur"
        :stroke-dasharray="circonference"
        :stroke-dashoffset="decalage"
      />
    </svg>
    <div class="ring__center"><slot /></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: { type: Number, default: 0 },
  max: { type: Number, default: 100 },
  size: { type: Number, default: 112 },
  epaisseur: { type: Number, default: 10 }
})

const rayon = computed(() => (props.size - props.epaisseur) / 2)
const circonference = computed(() => 2 * Math.PI * rayon.value)
const pct = computed(() => (props.max ? Math.min(100, (props.value / props.max) * 100) : 0))
const decalage = computed(() => circonference.value * (1 - pct.value / 100))
</script>

<style scoped>
.ring {
  position: relative;
  flex-shrink: 0;
}

.ring svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.ring__track {
  fill: none;
  stroke: var(--es-navy-50);
}

.ring__fill {
  fill: none;
  stroke: var(--es-navy);
  stroke-linecap: round;
  transition: stroke-dashoffset 0.6s ease;
}

.ring__fill--done {
  stroke: var(--es-green);
}

.ring__center {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}
</style>
