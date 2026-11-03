<template>
  <div class="ts" role="group" aria-label="Taille du texte">
    <button type="button" class="ts__btn" :disabled="index <= 0" aria-label="Réduire le texte" @click="changer(-1)">
      <span class="ts__a ts__a--sm">A</span>
    </button>
    <span class="ts__value" aria-live="polite">{{ Math.round(modelValue * 100) }}&nbsp;%</span>
    <button type="button" class="ts__btn" :disabled="index >= TAILLES.length - 1" aria-label="Agrandir le texte" @click="changer(1)">
      <span class="ts__a">A</span>
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { TAILLES } from '@/composables/useTailleTexte'

const props = defineProps({
  modelValue: { type: Number, default: 1 }
})
const emit = defineEmits(['update:modelValue'])

const index = computed(() => Math.max(0, TAILLES.indexOf(props.modelValue)))
const changer = (pas) => emit('update:modelValue', TAILLES[Math.min(TAILLES.length - 1, Math.max(0, index.value + pas))])
</script>

<style scoped>
.ts {
  display: inline-flex;
  align-items: center;
  height: 36px;
  border: 1px solid var(--es-line-strong);
  border-radius: 10px;
  background: #fff;
}

.ts__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 100%;
  border: 0;
  background: transparent;
  color: var(--es-ink);
  cursor: pointer;
}

.ts__btn:disabled {
  color: #c0c6d2;
  cursor: default;
}

.ts__btn:first-child {
  border-radius: 10px 0 0 10px;
}

.ts__btn:last-child {
  border-radius: 0 10px 10px 0;
}

.ts__btn:not(:disabled):hover {
  background: var(--es-bg);
}

.ts__a {
  font: 700 17px var(--es-font);
}

.ts__a--sm {
  font-size: 13px;
}

.ts__value {
  min-width: 44px;
  font-size: 12px;
  font-weight: 700;
  text-align: center;
  color: var(--es-muted);
}
</style>
