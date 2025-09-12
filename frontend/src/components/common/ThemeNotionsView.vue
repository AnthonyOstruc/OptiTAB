<template>
  <div class="tnv-wrapper">
    <!-- Loading -->
    <div v-if="loading" class="tnv-state tnv-loading">
      <div class="tnv-spinner"></div>
      <p>Chargement des concepts...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="tnv-state tnv-error">
      <div class="tnv-error-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
          <line x1="15" y1="9" x2="9" y2="15" stroke="currentColor" stroke-width="2"/>
          <line x1="9" y1="9" x2="15" y2="15" stroke="currentColor" stroke-width="2"/>
        </svg>
      </div>
      <p>{{ error }}</p>
      <button class="tnv-retry" @click="load(matiereId)">Réessayer</button>
    </div>

    <!-- Content -->
    <div v-else class="tnv-content">
      <!-- Themes with their notions -->
      <div v-if="themes.length > 0" class="tnv-themes">
        <div v-for="theme in themes" :key="theme.id" class="tnv-theme-block">
          <div class="tnv-theme-header">
            <h2 class="tnv-theme-title">{{ theme.nom }}</h2>
            <div class="tnv-theme-count">
              {{ (themeToNotions[theme.id] || []).length }} concept{{ (themeToNotions[theme.id] || []).length > 1 ? 's' : '' }}
            </div>
          </div>
          <div class="tnv-notions-grid">
            <NotionCard
              v-for="notion in (themeToNotions[theme.id] || [])"
              :key="notion.id"
              :title="notion.nom"
              :description="notion.description || ''"
              @click="goToNotion(notion.id)"
            />
            <div v-if="!(themeToNotions[theme.id] && themeToNotions[theme.id].length)" class="tnv-no-notions">
              <div class="tnv-empty-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <polyline points="14,2 14,8 20,8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <polyline points="10,9 9,9 8,9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <p>Aucun concept disponible</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Fallback: show notions directly -->
      <div v-else class="tnv-fallback">
        <div class="tnv-fallback-header">
          <h3>Concepts disponibles</h3>
          <p>Explorez les concepts fondamentaux de cette matière</p>
        </div>
        <div class="tnv-notions-grid">
          <NotionCard
            v-for="notion in directNotions"
            :key="notion.id"
            :title="notion.nom"
            :description="notion.description || ''"
            @click="goToNotion(notion.id)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getNotionsPourUtilisateur } from '@/api'
import { getThemesWithNotionsForUser } from '@/api/themes'
import NotionCard from '@/components/UI/NotionCard.vue'

const props = defineProps({
  matiereId: { type: [Number, String], required: true },
  notionRouteName: { type: String, required: true }
})

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const error = ref('')
const themes = ref([])
const themeToNotions = ref({})
const directNotions = ref([])

function goToNotion(notionId) {
  router.push({ name: props.notionRouteName, params: { notionId } })
}

// Cache hybride mémoire + localStorage pour accélérer l'affichage
const CACHE_TTL_MS = 120000
const cache = new Map()

function storageKey(matiereId) {
  return `tnv_cache:${cacheKey(matiereId)}`
}

function readFromStorage(matiereId) {
  try {
    const raw = localStorage.getItem(storageKey(matiereId))
    if (!raw) return null
    const parsed = JSON.parse(raw)
    if (!parsed || !parsed.t || !parsed.v) return null
    if (Date.now() - parsed.t > CACHE_TTL_MS) return null
    return parsed
  } catch (_) {
    return null
  }
}

function writeToStorage(matiereId, value) {
  try {
    const payload = JSON.stringify({ t: Date.now(), v: value })
    localStorage.setItem(storageKey(matiereId), payload)
  } catch (_) {
    // ignore quota or serialization errors
  }
}

function cacheKey(matiereId) {
  const niveauId = userStore.niveau_pays?.id || 'n'
  const paysId = userStore.pays?.id || 'p'
  return `${matiereId}|${niveauId}|${paysId}`
}

let currentAbortController = null

async function load(matiereId) {
  if (!matiereId) return
  error.value = ''

  const key = cacheKey(matiereId)
  const entry = cache.get(key) || readFromStorage(matiereId)
  if (entry && Date.now() - entry.t < CACHE_TTL_MS) {
    themes.value = entry.v.themes
    themeToNotions.value = entry.v.themeToNotions
    directNotions.value = entry.v.directNotions
    loading.value = false
  } else {
    loading.value = true
  }

  try {
    // Annuler l'appel précédent si toujours en vol
    if (currentAbortController) {
      try { currentAbortController.abort() } catch (_) {}
    }
    currentAbortController = new AbortController()
    const { data } = await getThemesWithNotionsForUser({ matiere: matiereId, signal: currentAbortController.signal })
    const themesList = Array.isArray(data?.themes) ? data.themes : []
    // Tri de secours côté client par ordre puis nom/titre
    const sortedThemes = [...themesList].sort((a, b) => {
      const ao = Number(a?.ordre ?? 0)
      const bo = Number(b?.ordre ?? 0)
      if (ao !== bo) return ao - bo
      const an = (a?.nom ?? a?.titre ?? '').toString()
      const bn = (b?.nom ?? b?.titre ?? '').toString()
      return an.localeCompare(bn)
    })
    const notions = Array.isArray(data?.notions) ? data.notions : []

    const grouped = {}
    for (const n of notions) {
      if (!grouped[n.theme]) grouped[n.theme] = []
      grouped[n.theme].push(n)
    }

    themes.value = sortedThemes
    themeToNotions.value = grouped
    directNotions.value = themesList.length === 0 ? notions.filter(n => !n.theme) : []

    const cachePayload = { themes: themes.value, themeToNotions: themeToNotions.value, directNotions: directNotions.value }
    cache.set(key, { t: Date.now(), v: cachePayload })
    writeToStorage(matiereId, cachePayload)
  } catch (e) {
    if (e?.name === 'CanceledError' || e?.name === 'AbortError') {
      // navigation rapide: ignorer l'erreur annulée
      return
    }
    error.value = 'Erreur lors du chargement des concepts'
  } finally {
    loading.value = false
  }
}

onMounted(() => load(props.matiereId))
watch(() => props.matiereId, (id) => load(id))

onBeforeUnmount(() => {
  if (currentAbortController) {
    try { currentAbortController.abort() } catch (_) {}
  }
})
</script>

<style scoped>
.tnv-wrapper {
  width: 100%;
  max-width: none;
  /* left align content within dashboard main */
  margin: 0;
}

/* États de chargement et d'erreur */
.tnv-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.tnv-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid #e5e7eb;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: tnvspin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes tnvspin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.tnv-error-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 48px;
  height: 48px;
  background: #fef2f2;
  border-radius: 12px;
  color: #ef4444;
  margin-bottom: 1rem;
}

.tnv-retry {
  background: #3b82f6;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 1rem;
}

.tnv-retry:hover {
  background: #2563eb;
  transform: translateY(-1px);
}

/* Blocs de thèmes */
.tnv-theme-block {
  background: transparent;
  border-radius: 0;
  padding: 1rem 0;
  margin-bottom: 1.25rem;
  box-shadow: none;
  border: none;
}

.tnv-theme-block:first-child {
  padding-top: 0.5rem;
}

.tnv-theme-header {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #f3f4f6;
}

.tnv-theme-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.tnv-theme-count {
  background: #f3f4f6;
  color: #6b7280;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
}

/* Grille des notions - EXACTEMENT 4 CARTES PAR LIGNE */
.tnv-notions-grid {
  display: grid;
  /* 4 colonnes fixes, espace constant, alignées à gauche */
  grid-template-columns: repeat(4, 280px);
  gap: 1rem;
  justify-content: start;
  align-items: stretch; /* Toutes les cartes ont la même hauteur dans leur ligne */
}

/* État vide */
.tnv-no-notions {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  color: #6b7280;
  text-align: center;
  grid-column: 1 / -1;
}

.tnv-empty-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 64px;
  height: 64px;
  background: #f9fafb;
  border-radius: 16px;
  color: #9ca3af;
  margin-bottom: 1rem;
}

.tnv-no-notions p {
  margin: 0;
  font-size: 0.875rem;
}

/* Fallback */
.tnv-fallback {
  background: #ffffff;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
}

.tnv-fallback-header {
  text-align: center;
  margin-bottom: 2rem;
}

.tnv-fallback-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.tnv-fallback-header p {
  color: #6b7280;
  margin: 0;
  font-size: 0.875rem;
}

/* Responsive - ADAPTATION POUR 4 CARTES PAR LIGNE */
@media (max-width: 1500px) {
  .tnv-notions-grid {
    grid-template-columns: repeat(3, 280px);
    gap: 1rem;
    justify-content: start;
  }
}

@media (max-width: 1200px) {
  .tnv-notions-grid {
    grid-template-columns: repeat(2, 280px);
    gap: 1rem;
    justify-content: start;
  }
  
  .tnv-theme-block {
    padding: 1.5rem;
  }
}

@media (max-width: 705px) {
  .tnv-notions-grid {
    grid-template-columns: 280px;
    gap: 1rem;
  }

  .tnv-theme-block {
    padding: 1.25rem;
    margin-bottom: 1.5rem;
  }

  .tnv-theme-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .tnv-theme-title {
    font-size: 1.25rem;
  }
}

</style>


