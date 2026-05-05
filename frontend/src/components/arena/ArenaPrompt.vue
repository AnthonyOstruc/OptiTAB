<template>
  <div class="arena-prompt" v-html="rendered" />
</template>

<script setup>
import { computed } from 'vue'
import katex from 'katex'
import 'katex/dist/katex.min.css'

const props = defineProps({
  text: { type: String, default: '' },
})

function escapeHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
}

function renderInline(str) {
  return escapeHtml(str).replace(/\$([^$]+)\$/g, (_, expr) => {
    try {
      return katex.renderToString(expr, { throwOnError: false })
    } catch (_) {
      return `$${expr}$`
    }
  })
}

const rendered = computed(() => renderInline(props.text))
</script>

<style scoped>
.arena-prompt {
  font-size: 18px;
  line-height: 1.55;
  color: #0f172a;
}
</style>
