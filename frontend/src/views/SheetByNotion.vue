<template>
  <DashboardLayout>
    <div class="sheet-by-notion-page">
      <div class="top-actions">
        <BackButton text="Retour aux notions" :customAction="goBack" />
      </div>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Chargement...</p>
      </div>

      <div v-else>
        <div v-if="!sheet" class="empty">
          <p>Aucune fiche pour cette notion.</p>
        </div>
        <div v-else class="sheet-container">
          <h1 class="sheet-title">{{ sheet.titre }}</h1>
          <div class="meta">
            <span class="badge">{{ sheet.matiere_nom || sheet.notion?.theme?.matiere?.titre }}</span>
            <span class="badge">{{ sheet.reading_time_minutes || 5 }} min</span>
          </div>
          <div class="sheet-content" v-html="rendered"></div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { defineOptions } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import BackButton from '@/components/common/BackButton.vue'
import { getSynthesisSheets, getSynthesisSheet } from '@/api/synthesis'
import { useSubjectsStore } from '@/stores/subjects/index'
import { renderContentWithImages } from '@/utils/scientificRenderer'

const route = useRoute()
const router = useRouter()
const subjectsStore = useSubjectsStore()

defineOptions({ name: 'SynthesisByNotion' })

const notionId = computed(() => Number(route.params.notionId))
const loading = ref(true)
const sheet = ref(null)

// Simple cache en mémoire pour accélérer les retours sur la même notion
const sheetCache = typeof window !== 'undefined' ? (window.__sheetCache ||= new Map()) : new Map()

const rendered = computed(() => {
  const html = (sheet.value?.summary || '')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
  const images = sheet.value?.images || []
  return renderContentWithImages(html, images)
})

function goBack() {
  // Rediriger vers sheets?matiereId=id (liste des notions de synthèse)
  const matiereId = route.params.matiereId || subjectsStore.activeMatiereId
  if (matiereId) {
    router.push({ 
      name: 'Sheets', 
      query: { 
        matiereId: matiereId
      } 
    })
  } else {
    router.back()
  }
}

async function fetchSheet(nId) {
  loading.value = true
  try {
    if (sheetCache.has(nId)) {
      sheet.value = sheetCache.get(nId)
    } else {
      const { data } = await getSynthesisSheets({ notion: nId })
      const result = Array.isArray(data) ? data[0] : (Array.isArray(data?.results) ? data.results[0] : null)
      let full = result
      if (result?.id) {
        try {
          const detail = await getSynthesisSheet(result.id)
          full = detail?.data || detail
        } catch (_) {
          full = result
        }
      }
      sheet.value = full
      sheetCache.set(nId, full)
    }
  } finally {
    loading.value = false
    await nextTick()
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise()
    }
  }
}

onMounted(() => {
  fetchSheet(notionId.value)
})

// Si l'utilisateur change de notion, recharger intelligemment avec le cache
watch(() => route.params.notionId, (newId, oldId) => {
  const n = Number(newId)
  if (n && n !== Number(oldId)) {
    fetchSheet(n)
  }
})
</script>

<style scoped>
.loading { text-align:center; padding:2rem; }
.spinner { width:36px; height:36px; border:3px solid #e5e7eb; border-top:3px solid #2563eb; border-radius:50%; animation: spin 1s linear infinite; margin: 0 auto 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }
.sheet-title { font-size: 1.5rem; font-weight: 800; margin: 0.25rem 0 0.5rem; color:#1e293b; }
.meta { display:flex; gap:.5rem; margin-bottom: .75rem; }
.badge { background:#eef2ff; color:#1d4ed8; padding:.25rem .5rem; border-radius: 999px; font-size:.75rem; font-weight:600; }
.sheet-content { background:white; border:1px solid #e5e7eb; border-radius:8px; padding:1rem; }
</style>
