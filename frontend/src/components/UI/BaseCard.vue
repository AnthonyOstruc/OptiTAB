<template>
  <div class="base-card" @click="$emit('click')">
    <div class="base-card__icon" v-if="icon">
      <div class="base-card__icon-svg" v-html="icon"></div>
    </div>
    <h3 class="base-card__title">{{ title }}</h3>
    <p class="base-card__desc" v-if="description">{{ description }}</p>
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
  max-width: 320px;
  min-height: 220px;
  box-shadow: 0 2px 8px rgba(30,41,59,0.04);
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: box-shadow 0.2s;
}
.base-card:hover {
  box-shadow: 0 4px 16px rgba(30,41,59,0.10);
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
}
</style> 