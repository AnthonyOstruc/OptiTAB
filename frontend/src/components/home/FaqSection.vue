<template>
  <section class="faq-section">
    <div class="faq-header">
      <h2 class="faq-title">
        <span>{{ titlePrefix }}</span> <span class="faq-highlight">{{ titleHighlight }}</span>
      </h2>
      <p class="faq-desc">{{ description }}</p>
    </div>
    <div class="faq-list">
      <div v-for="(item, idx) in faq" :key="idx" class="faq-item">
        <button class="faq-question" @click="toggle(idx)" :aria-expanded="opened === idx">
          <span>{{ item.question }}</span>
          <svg class="faq-arrow" :class="{ open: opened === idx }" width="24" height="24" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
        <transition name="faq-fade">
          <div v-if="opened === idx" class="faq-answer">
            {{ item.answer }}
          </div>
        </transition>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
const props = defineProps({
  faq: { type: Array, required: true },
  titlePrefix: { type: String, default: 'Questions' },
  titleHighlight: { type: String, default: 'Fréquentes' },
  description: {
    type: String,
    default: "Trouvez des réponses aux questions courantes sur OptiTAB et notre plateforme d'apprentissage."
  }
})
const opened = ref(null)
function toggle(idx) {
  opened.value = opened.value === idx ? null : idx
}
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;
.faq-section {
  background: #fff;
  padding: 56px 0 32px 0;
  max-width: 900px;
  margin: 0 auto 48px auto;
}
.faq-header {
  text-align: center;
  margin-bottom: 32px;
}
.faq-title {
  font-size: 2.3rem;
  font-weight: 900;
  color: $bleu-principal;
  margin-bottom: 10px;
}
.faq-highlight {
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 900;
}
.faq-desc {
  color: #52525b;
  font-size: 1.1rem;
}
.faq-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.faq-item {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(42, 56, 183, 0.08);
  border: 1.5px solid rgba(42, 56, 183, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
  
  &:hover {
    box-shadow: 0 4px 20px rgba(42, 56, 183, 0.12);
    border-color: rgba(42, 56, 183, 0.2);
  }
}
.faq-question {
  width: 100%;
  text-align: left;
  background: none;
  border: none;
  outline: none;
  font-size: 1.13rem;
  font-weight: 700;
  color: $bleu-principal;
  padding: 22px 28px 22px 22px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: background 0.15s;
}
.faq-question:hover {
  background: rgba(42, 56, 183, 0.05);
  color: #1e2a9a;
}
.faq-arrow {
  margin-left: 18px;
  transition: transform 0.25s, color 0.25s;
  color: #2a38b7;
  
  &.open {
    transform: rotate(180deg);
    color: #667eea;
  }
}
.faq-answer {
  padding: 0 22px 22px 22px;
  color: #52525b;
  font-size: 1.05rem;
  line-height: 1.6;
  animation: fadeIn 0.2s;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}
.faq-fade-enter-active, .faq-fade-leave-active {
  transition: opacity 0.2s;
}
.faq-fade-enter-from, .faq-fade-leave-to {
  opacity: 0;
}
@media (max-width: 700px) {
  .faq-section {
    /* plein largeur relative au conteneur, sans breakout */
    max-width: none;
    width: 100%;
    margin: 0 auto 14px auto;
    padding: 12px 0.25rem; /* réduit les paddings latéraux pour élargir */
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .faq-header { 
    margin-bottom: 16px;
    width: 100%;
    text-align: center;
  }
  .faq-title {
    font-size: 1.22rem; /* plus compact */
    line-height: 1.2;
    margin-bottom: 4px;
    text-align: center;
  }
  .faq-desc {
    font-size: 0.9rem;
    line-height: 1.4;
    padding: 0;
    word-break: normal;
    overflow-wrap: anywhere;
    hyphens: none;
    text-align: center;
  }
  .faq-list { 
    gap: 8px;
    width: 100%;
    max-width: 100%;
    display: flex;
    flex-direction: column;
    align-items: stretch;
  }
  .faq-item { 
    border-radius: 10px; 
    box-shadow: 0 1px 4px rgba(42,56,183,0.06);
    width: 100%;
    max-width: 100%;
  }
  .faq-question {
    font-size: 0.92rem;
    padding: 10px 8px; /* réduit les paddings latéraux pour élargir */
    text-align: left;
    justify-content: space-between;
  }
  .faq-question span {
    text-align: left;
  }
  .faq-arrow { width: 15px; height: 15px; margin-left: 8px; }
  .faq-answer {
    font-size: 0.88rem;
    padding: 0 8px 10px 8px; /* réduit les paddings latéraux pour élargir */
    line-height: 1.5;
    text-align: left;
  }
}

@media (max-width: 380px) {
  .faq-section {
    padding: 12px 0.125rem; /* encore plus réduit pour très petit mobile */
  }
  .faq-title { font-size: 1.12rem; }
  .faq-desc { font-size: 0.86rem; }
  .faq-question { font-size: 0.9rem; padding: 9px 6px; }
  .faq-answer { font-size: 0.86rem; padding: 0 6px 9px 6px; }
}
</style> 
