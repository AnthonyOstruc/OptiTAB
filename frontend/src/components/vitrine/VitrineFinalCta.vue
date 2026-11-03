<template>
  <section class="fc">
    <div class="vt-container">
      <div class="fc__card">
        <h2 class="fc__title">{{ titre }}</h2>
        <p v-if="texte" class="fc__text">{{ texte }}</p>
        <div class="fc__actions">
          <slot />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  titre: { type: String, required: true },
  texte: { type: String, default: '' }
})
</script>

<style scoped>
.fc {
  padding: 0 0 104px;
}

.fc__card {
  position: relative;
  overflow: hidden;
  padding: 64px 40px;
  border-radius: 28px;
  background:
    radial-gradient(600px 300px at 15% 0%, rgba(95, 172, 96, 0.25), transparent 60%),
    linear-gradient(135deg, var(--vt-navy) 0%, var(--vt-navy-900) 100%);
  text-align: center;
}

.fc__card::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.06) 1px, transparent 1px);
  background-size: 28px 28px;
  -webkit-mask-image: radial-gradient(ellipse 60% 90% at 50% 50%, #000 10%, transparent 75%);
  mask-image: radial-gradient(ellipse 60% 90% at 50% 50%, #000 10%, transparent 75%);
  pointer-events: none;
}

.fc .fc__title {
  position: relative;
  max-width: 720px;
  margin: 0 auto;
  font-size: clamp(28px, 3.6vw, 42px);
  color: #fff;
}

.fc__text {
  position: relative;
  max-width: 580px;
  margin: 16px auto 0;
  font-size: 17px;
  color: rgba(255, 255, 255, 0.8);
}

.fc__actions {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
  margin-top: 32px;
}

@media (max-width: 640px) {
  .fc {
    padding-bottom: 72px;
  }

  .fc__card {
    padding: 44px 20px;
    border-radius: 22px;
  }

  .fc__text {
    font-size: 16px;
  }

  .fc__actions {
    flex-direction: column;
  }

  .fc__actions :deep(.vt-btn) {
    width: 100%;
  }
}
</style>
