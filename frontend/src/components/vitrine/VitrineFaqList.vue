<template>
  <div class="fq">
    <details v-for="(item, index) in items" :key="item.question" class="fq__item" :open="openFirst && index === 0">
      <summary class="fq__question">
        {{ item.question }}
        <ChevronDownIcon class="fq__chevron" aria-hidden="true" />
      </summary>
      <p class="fq__answer">{{ item.answer }}</p>
    </details>
  </div>
</template>

<script setup>
import { ChevronDownIcon } from '@heroicons/vue/24/outline'

defineProps({
  // [{ question, answer }]
  items: { type: Array, required: true },
  openFirst: { type: Boolean, default: true }
})
</script>

<style scoped>
.fq {
  border-top: 1px solid var(--vt-line);
}

.fq__item {
  border-bottom: 1px solid var(--vt-line);
}

.fq__question {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 20px 4px;
  font-size: 17px;
  font-weight: 700;
  color: var(--vt-ink);
  cursor: pointer;
  list-style: none;
}

.fq__question::-webkit-details-marker {
  display: none;
}

.fq__question:hover {
  color: var(--vt-navy);
}

.fq__chevron {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  color: var(--vt-muted);
  transition: transform 0.2s ease;
}

.fq__item[open] .fq__chevron {
  transform: rotate(180deg);
  color: var(--vt-navy);
}

.fq__answer {
  margin: -4px 0 0;
  padding: 0 40px 22px 4px;
  font-size: 16px;
  line-height: 1.7;
  color: var(--vt-muted);
}

@media (max-width: 640px) {
  .fq__question {
    padding: 18px 2px;
    font-size: 16px;
  }

  .fq__answer {
    padding: 0 8px 20px 2px;
    font-size: 15px;
  }
}
</style>
