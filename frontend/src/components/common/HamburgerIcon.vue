<template>
  <svg 
    class="hamburger-icon"
    :class="{ 'is-active': isActive }"
    width="24" 
    height="24" 
    viewBox="0 0 24 24" 
    fill="none" 
    stroke="currentColor" 
    stroke-width="2" 
    stroke-linecap="round" 
    stroke-linejoin="round"
  >
    <!-- Top line -->
    <line 
      class="hamburger-line top-line"
      x1="3" 
      y1="6" 
      x2="21" 
      y2="6"
    />
    <!-- Middle line -->
    <line 
      class="hamburger-line middle-line"
      x1="3" 
      y1="12" 
      x2="21" 
      y2="12"
    />
    <!-- Bottom line -->
    <line 
      class="hamburger-line bottom-line"
      x1="3" 
      y1="18" 
      x2="21" 
      y2="18"
    />
  </svg>
</template>

<script>
export default {
  name: 'HamburgerIcon',
  props: {
    isActive: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;

.hamburger-icon {
  transition: all 0.3s ease;
  cursor: pointer;
  
  .hamburger-line {
    transition: all 0.3s ease;
    transform-origin: center;
  }
  
  // Active state animations
  &.is-active {
    .top-line {
      transform: rotate(45deg) translate(5px, 5px);
    }
    
    .middle-line {
      opacity: 0;
      transform: scaleX(0);
    }
    
    .bottom-line {
      transform: rotate(-45deg) translate(7px, -6px);
    }
  }
  
  // Hover effect
  &:hover {
    transform: scale(1.1);
  }
}
</style> 