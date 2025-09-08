<template>
  <div class="whatsapp-chat-btn-wrapper">
    <a
      :href="whatsappUrl"
      class="whatsapp-chat-btn"
      target="_blank"
      rel="noopener noreferrer"
      :aria-label="tooltip || 'Contacter sur WhatsApp'"
      :title="tooltip || 'Contacter sur WhatsApp'"
      @mouseenter="handleMouseEnter"
      @mouseleave="handleMouseLeave"
      @focus="handleFocus"
      @blur="handleBlur"
    >
      <img :src="whatsappIcon" alt="WhatsApp" width="32" height="32" />
    </a>
    <div v-if="tooltip && showTooltip" class="whatsapp-tooltip">{{ tooltip }}</div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
const whatsappIcon = '/icons/whatsapp.svg'
const props = defineProps({
  phone: { type: String, required: true }, // format international sans +
  message: { type: String, default: '' },
  tooltip: { type: String, default: '' }
})
const whatsappUrl = computed(() => {
  const base = 'https://wa.me/' + props.phone.replace(/[^0-9]/g, '')
  const msg = props.message ? ('?text=' + encodeURIComponent(props.message)) : ''
  return base + msg
})

const showTooltip = ref(false)
function handleMouseEnter() { showTooltip.value = true }
function handleMouseLeave() { showTooltip.value = false }
function handleFocus() { showTooltip.value = true }
function handleBlur() { showTooltip.value = false }
</script>

<style scoped lang="scss">
.whatsapp-chat-btn-wrapper {
  position: fixed;
  right: 24px;
  bottom: 24px;
  left: auto;
  top: auto;
  transform: none;
  z-index: 12010;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}
.whatsapp-chat-btn {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: #25D366;
  border-radius: 50%;
  box-shadow: 0 4px 16px rgba(30,41,59,0.12);
  transition: box-shadow 0.2s;
  border: none;
  cursor: pointer;
  outline: none;
  text-decoration: none;
  &:hover, &:focus {
    box-shadow: 0 8px 24px rgba(37,211,102,0.18);
  }
}
.whatsapp-chat-btn img {
  width: 32px;
  height: 32px;
  display: block;
}
.whatsapp-tooltip {
  position: absolute;
  right: 100%;
  top: 50%;
  transform: translateY(-50%);
  margin-right: 16px;
  background: #18181b;
  color: #fff;
  font-size: 0.98rem;
  padding: 7px 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(30,41,59,0.10);
  white-space: nowrap;
  opacity: 0.92;
  pointer-events: none;
  user-select: none;
  z-index: 1;
}
@media (max-width: 600px) {
  .whatsapp-chat-btn-wrapper {
    right: 10px;
    bottom: 10px;
    left: auto;
    top: auto;
    transform: none;
  }
  .whatsapp-chat-btn {
    width: 48px;
    height: 48px;
  }
  .whatsapp-chat-btn img {
    width: 26px;
    height: 26px;
  }
  .whatsapp-tooltip {
    font-size: 0.92rem;
    padding: 6px 10px;
    margin-right: 8px;
  }
}
</style> 