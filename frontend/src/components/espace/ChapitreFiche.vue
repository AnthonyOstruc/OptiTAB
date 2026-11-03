<template>
  <div class="cf">
    <div v-if="loading" class="es-card cf-article">
      <div class="es-skeleton" style="height: 24px; width: 50%"></div>
      <div v-for="n in 5" :key="n" class="es-skeleton" style="height: 16px; margin-top: 14px"></div>
    </div>

    <div v-else-if="!fiche" class="es-empty cf-empty">
      <strong>La fiche de ce chapitre arrive bientôt</strong>
      Le cours et les exercices sont déjà disponibles.
      <div class="cf-empty__actions">
        <button type="button" class="es-btn es-btn--sm es-btn--ghost" @click="$emit('go', 'cours')">Lire le cours</button>
        <button type="button" class="es-btn es-btn--sm" @click="$emit('go', 'exercices')">Faire les exercices</button>
      </div>
    </div>

    <article v-else class="es-card cf-article">
      <div class="cf-toolbar">
        <p class="cf-toolbar__hint">
          <DocumentTextIcon aria-hidden="true" />
          L’essentiel du chapitre, à relire avant un contrôle.
        </p>
        <TextSize v-model="zoom" />
      </div>
      <EspaceDoc :html="html" :zoom="zoom" />
      <div class="cf-next">
        <span>Prêt à t’entraîner&nbsp;?</span>
        <button type="button" class="es-btn" @click="$emit('go', 'exercices')">
          Faire les exercices
          <ArrowRightIcon aria-hidden="true" />
        </button>
      </div>
    </article>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { ArrowRightIcon, DocumentTextIcon } from '@heroicons/vue/24/outline'
import EspaceDoc from './EspaceDoc.vue'
import TextSize from './TextSize.vue'
import { getSynthesisSheet, getSynthesisSheets } from '@/api/synthesis'
import { renderContentWithImages } from '@/utils/scientificRenderer'
import { useTailleTexte } from '@/composables/useTailleTexte'

const props = defineProps({
  notionId: { type: [String, Number], required: true }
})
defineEmits(['go'])

const loading = ref(true)
const fiche = ref(null)
const zoom = useTailleTexte()

const html = computed(() => {
  const brut = (fiche.value?.summary || '').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&')
  return brut ? renderContentWithImages(brut, fiche.value?.images || []) : ''
})

async function charger() {
  loading.value = true
  try {
    const { data } = await getSynthesisSheets({ notion: props.notionId, sheet_type: 'summary' })
    const premiere = Array.isArray(data) ? data[0] : (data?.results || [])[0]
    if (premiere?.id) {
      const detail = await getSynthesisSheet(premiere.id).catch(() => null)
      fiche.value = detail?.data || premiere
    } else {
      fiche.value = null
    }
  } catch {
    fiche.value = null
  } finally {
    loading.value = false
  }
}

onMounted(charger)
watch(() => props.notionId, charger)
</script>

<style scoped>
.cf-article {
  max-width: 920px;
  margin: 0 auto;
  padding: 24px 40px 32px;
}

.cf-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin: 0 -8px 18px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--es-line);
}

.cf-toolbar__hint {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--es-muted);
}

.cf-toolbar__hint svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  color: var(--es-green-700);
}

.cf-next {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 14px;
  margin-top: 32px;
  padding-top: 20px;
  border-top: 1px solid var(--es-line);
  font-size: 15px;
  font-weight: 600;
  color: var(--es-ink-soft);
}

.cf-empty {
  padding: 40px 20px;
}

.cf-empty__actions {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 16px;
}

@media (max-width: 640px) {
  .cf-article {
    margin: 0 -16px;
    padding: 16px 16px 24px;
    border-right: 0;
    border-left: 0;
    border-radius: 0;
    box-shadow: none;
  }

  .cf-toolbar {
    margin: 0 0 14px;
  }

  .cf-toolbar__hint {
    font-size: 13px;
  }

  .cf-next {
    flex-direction: column;
    align-items: stretch;
    text-align: center;
  }
}
</style>
