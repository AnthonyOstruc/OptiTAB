<template>
  <div ref="docRef" class="es-doc sci-doc" :style="{ zoom }" v-html="html"></div>
</template>

<script setup>
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'
import { tuneMathOverflow } from '@/utils/scientificRenderer'

// Affiche un contenu de cours ou de fiche (format structuré OptiTAB ou ancien
// format), lance MathJax sur ce seul bloc, puis renvoie la liste des titres
// pour construire le sommaire.
const props = defineProps({
  html: { type: String, default: '' },
  zoom: { type: Number, default: 1 }
})

const emit = defineEmits(['ready'])
const docRef = ref(null)
let alive = true

const nettoyer = (texte) => String(texte || '')
  .replace(/\\\(|\\\)|\\\[|\\\]|\$/g, '')
  .replace(/\\(mathbb|mathrm|text|mathcal|operatorname)\{([^}]*)\}/g, '$2')
  .replace(/\s+/g, ' ')
  .trim()

function collecterTitres(root) {
  const titres = []
  root.querySelectorAll('h2, h3').forEach((h, i) => {
    if (h.closest('.otm-box')) return
    const num = h.querySelector('.otm-h2-num, .otm-q-num')?.textContent?.trim()
    const texte = nettoyer(h.querySelector('.otm-h2-text, .otm-q-text')?.textContent || h.textContent)
    if (!texte || texte.length < 2) return
    h.id = h.id || `es-sec-${i}`
    titres.push({ id: h.id, niveau: h.tagName === 'H3' ? 3 : 2, num: num || '', texte })
  })
  return titres
}

// Ancien format : les tableaux larges défilent dans leur propre cadre.
function envelopperTableaux(root) {
  root.querySelectorAll('table').forEach((table) => {
    if (table.closest('.otm') || table.parentElement?.classList.contains('es-doc-scroll')) return
    const cadre = document.createElement('div')
    cadre.className = 'es-doc-scroll'
    table.parentNode.insertBefore(cadre, table)
    cadre.appendChild(table)
  })
}

async function preparer() {
  await nextTick()
  const root = docRef.value
  if (!root) return
  const titres = collecterTitres(root)
  envelopperTableaux(root)
  try {
    const mj = window.MathJax
    if (mj?.startup?.promise) await mj.startup.promise
    if (mj?.typesetPromise) {
      if (mj.typesetClear) mj.typesetClear([root])
      await mj.typesetPromise([root])
    }
  } catch (e) {
    console.warn('[EspaceDoc] MathJax :', e)
  }
  if (!alive) return
  tuneMathOverflow(root)
  emit('ready', titres)
}

watch(() => props.html, preparer, { immediate: true })

onBeforeUnmount(() => {
  alive = false
})

defineExpose({ el: docRef })
</script>

<style scoped>
.es-doc {
  min-width: 0;
}

.es-doc :deep(.es-doc-scroll) {
  max-width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.es-doc :deep(img) {
  max-width: 100%;
  height: auto;
}

.es-doc :deep(mjx-container[display='true']) {
  max-width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
}
</style>
