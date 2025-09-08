<template>
  <svg 
    class="close-icon"
    width="24" 
    height="24" 
    viewBox="0 0 24 24" 
    fill="none" 
    stroke="currentColor" 
    stroke-width="2" 
    stroke-linecap="round" 
    stroke-linejoin="round"
  >
    <!-- X lines -->
    <line x1="18" y1="6" x2="6" y2="18" />
    <line x1="6" y1="6" x2="18" y2="18" />
  </svg>
</template>

<script>
export default {
  name: 'CloseIcon'
}
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;

.close-icon {
  transition: all 0.2s ease;
  cursor: pointer;
  
  &:hover {
    transform: scale(1.1);
    color: $primary-color;
  }
}
</style> 