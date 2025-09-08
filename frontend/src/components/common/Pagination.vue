<template>
  <div class="pagination" v-if="totalPages > 1">
    <button class="nav-btn" :disabled="currentPage===1" @click="$emit('update:page', currentPage-1)">Préc.</button>
    <template v-for="item in pages" :key="item">
      <span v-if="typeof item === 'string'" class="ellipsis">…</span>
      <button v-else
        :class="['page-btn', { active: item===currentPage }]"
        @click="$emit('update:page', item)"
      >{{ item }}</button>
    </template>
    <button class="nav-btn" :disabled="currentPage===totalPages" @click="$emit('update:page', currentPage+1)">Suiv.</button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  total: { type: Number, required: true },
  perPage: { type: Number, required: true },
  page: { type: Number, required: true }
})

defineEmits(['update:page'])

const totalPages = computed(() => Math.ceil(props.total / props.perPage))

const currentPage = computed(() => props.page)

const windowSize = 2
const pages = computed(() => {
  const n = totalPages.value
  const current = currentPage.value
  if (n <= 7) {
    return [...Array(n).keys()].map(i => i + 1)
  }

  const pagesSet = new Set([1, n])
  for (let i = current - windowSize; i <= current + windowSize; i++) {
    if (i > 1 && i < n) pagesSet.add(i)
  }

  const sorted = Array.from(pagesSet).sort((a,b)=>a-b)

  // insert ellipsis markers
  const result = []
  let prev = 0
  for (const p of sorted) {
    if (prev && p - prev > 1) {
      result.push('ellipsis-' + prev) // placeholder
    }
    result.push(p)
    prev = p
  }
  return result
})
</script>

<style scoped>
.pagination { display: flex; gap: 0.4rem; align-items: center; justify-content: center; margin-top: 1.5rem; flex-wrap: wrap; }
.page-btn, .nav-btn { background: #e5e7eb; border: none; border-radius: 6px; padding: 6px 12px; cursor: pointer; font-weight:600; }
.page-btn.active{ background:#6366f1; color:#fff; }
.page-btn:hover:not(.active), .nav-btn:hover:not(:disabled){ background:#cbd5e1; }
.nav-btn:disabled{ opacity:0.5; cursor:not-allowed; }
.ellipsis{padding:0 4px;font-weight:700;}
</style> 