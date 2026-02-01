<template>
  <div class="base-card" @click="$emit('click')">
    <div class="base-card__icon" v-if="icon">
      <div class="base-card__icon-svg" v-html="icon"></div>
    </div>
    <h3 class="base-card__title">{{ title }}</h3>
    <p class="base-card__desc" v-if="description">{{ description }}</p>
    <div class="base-card__help-indicator">
      <span class="help-icon">💡</span>
      <span class="help-text">Cliquez pour obtenir de l'aide</span>
      <span class="help-arrow">→</span>
    </div>
    <slot />
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  icon: { type: String, default: '' },
  description: { type: String, default: '' }
})
</script>

<style scoped>
.base-card {
  background: #f3f4f6;
  border-radius: 16px;
  padding: 32px 28px;
  /* Desktop/card grid default size */
  max-width: 320px;
  min-height: 280px;
  box-shadow: 0 2px 8px rgba(30,41,59,0.04);
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  border: 2px solid transparent;
}
.base-card:hover {
  box-shadow: 0 8px 24px rgba(42, 56, 183, 0.15);
  transform: translateY(-4px);
  border-color: rgba(42, 56, 183, 0.2);
}
.base-card:hover .base-card__help-indicator {
  opacity: 1;
  transform: translateY(0);
}
.base-card__icon {
  font-size: 2.2rem;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 56px;
}
.base-card__icon-svg {
  width: 86px;
  height: 86px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}
.base-card__icon-svg svg {
  width: 100%;
  height: 100%;
  display: block;
}
.base-card__title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #3730a3;
  margin-bottom: 8px;
}
.base-card__desc {
  color: #475569;
  font-size: 1rem;
  text-align: center;
  margin-bottom: 12px;
}

.base-card__help-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: auto;
  padding-top: 12px;
  font-size: 0.85rem;
  color: #2a38b7;
  font-weight: 600;
  opacity: 0.7;
  transform: translateY(4px);
  transition: all 0.3s ease;
}

.base-card:hover .base-card__help-indicator {
  opacity: 1;
  transform: translateY(0);
}

.help-icon {
  font-size: 1rem;
}

.help-text {
  font-size: 0.85rem;
}

.help-arrow {
  font-size: 1rem;
  transition: transform 0.3s ease;
}

.base-card:hover .help-arrow {
  transform: translateX(4px);
}

@media (max-width: 768px) {
  .base-card {
    /* On mobile, cards should span full available width */
    width: 100%;
    max-width: none;
    padding: 22px 16px;
    min-height: 250px;
  }

  .base-card__help-indicator {
    gap: 4px;
    font-size: 0.78rem;
  }

  .help-icon,
  .help-arrow {
    font-size: 0.95rem;
  }

  .help-text {
    font-size: 0.78rem;
    white-space: nowrap;
  }
}
</style> 
