<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: 'FAQ'
  },
  description: {
    type: String,
    default: ''
  },
  items: {
    type: Array,
    default: () => []
  },
  maxItems: {
    type: Number,
    default: 6
  }
})

const openedIndex = ref(-1)
const listId = `faq-accordion-${Math.random().toString(36).slice(2, 9)}`

const normalizedItems = computed(() =>
  (Array.isArray(props.items) ? props.items : [])
    .map((item) => ({
      question: String(item?.question || '').trim(),
      answer: String(item?.answer || '').trim()
    }))
    .filter((item) => item.question && item.answer)
    .slice(0, Math.max(1, Number(props.maxItems || 6)))
)

function panelId(index) {
  return `${listId}-panel-${index}`
}
</script>

<template>
  <section class="faq-accordion" aria-label="Questions fréquentes">
    <h2 class="faq-accordion__title">{{ title }}</h2>
    <p v-if="description" class="faq-accordion__description">{{ description }}</p>

    <div class="faq-accordion__list">
      <article v-for="(item, idx) in normalizedItems" :key="item.question" class="faq-accordion__item">
        <h3 class="faq-accordion__question-title">
          <button
            type="button"
            class="faq-accordion__question"
            :aria-expanded="String(openedIndex === idx)"
            :aria-controls="panelId(idx)"
            @click="openedIndex = openedIndex === idx ? -1 : idx"
          >
            {{ item.question }}
          </button>
        </h3>
        <div
          :id="panelId(idx)"
          class="faq-accordion__answer"
          role="region"
          :aria-hidden="String(openedIndex !== idx)"
          v-show="openedIndex === idx"
        >
          <p>{{ item.answer }}</p>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.faq-accordion {
  margin-top: 18px;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 16px;
  background: #fff;
}

.faq-accordion__title {
  margin: 0;
  font-size: 1.06rem;
  font-weight: 800;
  color: #0f172a;
}

.faq-accordion__description {
  margin: 8px 0 0;
  color: #475569;
  font-size: 0.88rem;
}

.faq-accordion__list {
  margin-top: 12px;
  display: grid;
  gap: 8px;
}

.faq-accordion__item {
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
}

.faq-accordion__question-title {
  margin: 0;
}

.faq-accordion__question {
  width: 100%;
  text-align: left;
  border: none;
  background: #f8fafc;
  color: #0f172a;
  font-size: 0.9rem;
  font-weight: 700;
  padding: 12px 14px;
  cursor: pointer;
}

.faq-accordion__question:hover {
  background: #eff6ff;
}

.faq-accordion__answer {
  padding: 10px 14px 12px;
  background: #fff;
}

.faq-accordion__answer p {
  margin: 0;
  color: #334155;
  font-size: 0.86rem;
  line-height: 1.6;
}
</style>
