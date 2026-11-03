<template>
  <div class="vt">
    <VitrineHeader :landing="landing" />
    <main class="vt-main">
      <slot />
    </main>
    <VitrineFooter />
    <WhatsappChatButton
      v-if="showWhatsapp"
      :phone="vitrineContact.whatsapp"
      :message="vitrineContact.messageWhatsapp"
      tooltip="Une question ? Écris-nous sur WhatsApp"
    />
  </div>
</template>

<script setup>
import VitrineHeader from './VitrineHeader.vue'
import VitrineFooter from './VitrineFooter.vue'
import WhatsappChatButton from '@/components/home/WhatsappChatButton.vue'
import { vitrineContact } from '@/config/vitrineContent'
import '@/styles/vitrine.css'

defineProps({
  showWhatsapp: {
    type: Boolean,
    default: true
  },
  // En-tête épuré (pages publicitaires et de paiement).
  landing: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.vt-main {
  flex: 1;
  width: 100%;
  min-width: 0;
  padding-top: calc(72px + env(safe-area-inset-top, 0px));
  overflow-x: clip;
}

.vt-main :deep(section[id]) {
  scroll-margin-top: 88px;
}

@media (max-width: 960px) {
  .vt-main {
    padding-top: calc(64px + env(safe-area-inset-top, 0px));
  }

  .vt-main :deep(section[id]) {
    scroll-margin-top: 72px;
  }
}
</style>
