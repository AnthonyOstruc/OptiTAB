<script setup>
import { computed, ref } from 'vue'
import { FREE_RESOURCES_SEO_SECTION_TITLES } from '@/config/freeResourcesUx'

const props = defineProps({
  title: {
    type: String,
    default: 'Pourquoi cette page ?'
  },
  summary: {
    type: String,
    default: ''
  },
  sections: {
    type: Array,
    default: () => []
  },
  sectionTitles: {
    type: Array,
    default: () => FREE_RESOURCES_SEO_SECTION_TITLES
  },
  initiallyOpen: {
    type: Boolean,
    default: false
  }
})

const isOpen = ref(Boolean(props.initiallyOpen))
const panelId = `seo-accordion-${Math.random().toString(36).slice(2, 9)}`

const normalizedSections = computed(() => {
  if (!Array.isArray(props.sections) || props.sections.length === 0) return []
  return props.sections
    .map((section, index) => {
      const paragraphs = Array.isArray(section?.paragraphs)
        ? section.paragraphs.map((text) => String(text || '').trim()).filter(Boolean)
        : [String(section?.text || '').trim()].filter(Boolean)
      if (!paragraphs.length) return null
      const title = String(section?.title || props.sectionTitles[index] || `Section ${index + 1}`).trim()
      return { title, paragraphs }
    })
    .filter(Boolean)
})
</script>

<template>
  <section class="seo-accordion" aria-label="Contenu détaillé">
    <h2 class="seo-accordion__title">{{ title }}</h2>
    <p v-if="summary" class="seo-accordion__summary">{{ summary }}</p>

    <button
      type="button"
      class="seo-accordion__toggle"
      :aria-expanded="String(isOpen)"
      :aria-controls="panelId"
      @click="isOpen = !isOpen"
    >
      <span>{{ isOpen ? 'Réduire' : 'Lire plus' }}</span>
    </button>

    <div :id="panelId" class="seo-accordion__panel" role="region" :aria-hidden="String(!isOpen)" v-show="isOpen">
      <article v-for="section in normalizedSections" :key="section.title" class="seo-accordion__section">
        <h3 class="seo-accordion__section-title">{{ section.title }}</h3>
        <p v-for="paragraph in section.paragraphs" :key="paragraph" class="seo-accordion__paragraph">
          {{ paragraph }}
        </p>
      </article>
    </div>
  </section>
</template>

<style scoped>
.seo-accordion {
  margin-top: 18px;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 16px;
  background: #fff;
}

.seo-accordion__title {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 800;
  color: #0f172a;
}

.seo-accordion__summary {
  margin: 8px 0 0;
  color: #475569;
  font-size: 0.9rem;
  line-height: 1.55;
}

.seo-accordion__toggle {
  margin-top: 12px;
  border: 1px solid #cbd5e1;
  border-radius: 999px;
  background: #fff;
  color: #1d4ed8;
  font-size: 0.82rem;
  font-weight: 700;
  padding: 7px 12px;
  cursor: pointer;
}

.seo-accordion__toggle:hover {
  background: #eff6ff;
  border-color: #93c5fd;
}

.seo-accordion__panel {
  margin-top: 12px;
  display: grid;
  gap: 14px;
}

.seo-accordion__section-title {
  margin: 0 0 8px;
  font-size: 0.95rem;
  font-weight: 800;
  color: #0f172a;
}

.seo-accordion__paragraph {
  margin: 0 0 8px;
  color: #334155;
  font-size: 0.88rem;
  line-height: 1.65;
}

.seo-accordion__paragraph:last-child {
  margin-bottom: 0;
}
</style>
