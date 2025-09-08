<template>
  <div class="loading-spinner" :class="sizeClass" :style="spinnerStyle">
    <div class="spinner-ring"></div>
  </div>
</template>

<script>
export default {
  name: 'LoadingSpinner',
  props: {
    size: {
      type: String,
      default: 'medium',
      validator: value => ['small', 'medium', 'large'].includes(value)
    },
    color: {
      type: String,
      default: 'current'
    }
  },
  computed: {
    sizeClass() {
      return `spinner-${this.size}`
    },
    spinnerStyle() {
      if (this.color === 'current') return {}
      return { '--spinner-color': this.color }
    }
  }
}
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;

.loading-spinner {
  display: inline-block;
  position: relative;
}

.spinner-ring {
  border: 2px solid transparent;
  border-top: 2px solid var(--spinner-color, currentColor);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

// Size variants
.spinner-small .spinner-ring {
  width: 16px;
  height: 16px;
}

.spinner-medium .spinner-ring {
  width: 20px;
  height: 20px;
}

.spinner-large .spinner-ring {
  width: 24px;
  height: 24px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style> 