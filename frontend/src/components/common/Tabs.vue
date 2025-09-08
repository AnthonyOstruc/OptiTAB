<template>
  <div :class="['tabs', position]">
    <button
      v-for="t in items"
      :key="t.key"
      :class="['tab-btn',{ active: modelValue===t.key }]"
      @click="$emit('update:modelValue', t.key)"
    >{{ t.label }}</button>
  </div>
</template>

<script setup>
const props = defineProps({
  items: { type: Array, required: true },
  modelValue: { required: true },
  position: { type: String, default: 'top' } // top or inline
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
.tabs{display:flex;gap:1rem;margin-bottom:1rem;}
.tab-btn{background:none;border:none;padding:6px 14px;font-weight:600;color:#374151;cursor:pointer;border-radius:8px 8px 0 0;}
.tab-btn.active{background:#6366f1;color:#fff;}
.tab-btn:hover:not(.active){background:#e0e7ff;}
</style> 