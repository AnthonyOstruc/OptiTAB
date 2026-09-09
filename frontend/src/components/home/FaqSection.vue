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
@media (max-width: 800px) {
  .faq-section {
    max-width: 680px;
    width: 100%;
    margin: 0 auto;
    padding: 48px 20px;
  }
  .faq-header {
    margin-bottom: 28px;
  }
  .faq-title {
    font-size: clamp(1.75rem, 5.5vw, 2rem);
    line-height: 1.25;
    margin: 0 0 12px;
    text-wrap: balance;
  }
  .faq-desc {
    font-size: 1rem;
    line-height: 1.6;
    margin: 0;
  }
  .faq-list {
    gap: 12px;
    width: 100%;
  }
  .faq-item {
    border-radius: 14px;
    box-shadow: 0 1px 4px rgba(42,56,183,0.06);
    min-width: 0;
  }
  .faq-question {
    font-size: 1rem;
    line-height: 1.5;
    min-height: 56px;
    padding: 18px 16px;
    gap: 12px;
  }
  .faq-question span {
    min-width: 0;
  }
  .faq-arrow {
    width: 20px;
    height: 20px;
    flex-shrink: 0;
    margin-left: 0;
  }
  .faq-answer {
    font-size: 0.95rem;
    padding: 0 16px 18px;
    line-height: 1.65;
    text-align: left;
  }
}
</style>
