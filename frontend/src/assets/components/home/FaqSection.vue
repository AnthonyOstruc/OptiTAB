<template>
  <section class="faq-section">
    <div class="faq-header">
      <h2 class="faq-title">
        <span>Questions</span> <span class="faq-highlight">Fréquentes</span>
      </h2>
      <p class="faq-desc">Trouvez des réponses aux questions courantes sur Optitab et notre plateforme d'apprentissage.</p>
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
  faq: { type: Array, required: true }
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
  color: #a78bfa;
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
  background: #fafaff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(30,41,59,0.04);
  border: 1.5px solid #f3f4f6;
  overflow: hidden;
  transition: box-shadow 0.2s;
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
  background: #f3f4f6;
}
.faq-arrow {
  margin-left: 18px;
  transition: transform 0.25s;
}
.faq-arrow.open {
  transform: rotate(180deg);
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
    padding: 36px 0 18px 0;
  }
  .faq-title {
    font-size: 1.5rem;
  }
  .faq-answer, .faq-question {
    font-size: 1rem;
    padding-left: 12px;
    padding-right: 12px;
  }
}
</style> 