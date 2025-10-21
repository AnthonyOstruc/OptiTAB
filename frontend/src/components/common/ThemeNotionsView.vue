<template>
  <div class="tnv-wrapper">
    <!-- Loading with Skeleton -->
    <div v-if="loading" class="tnv-loading-skeleton">
      <div v-for="i in 2" :key="i" class="tnv-theme-skeleton">
        <div class="skeleton-theme-header">
          <div class="skeleton-line skeleton-theme-title"></div>
        </div>
        <div class="tnv-skeleton-grid">
          <SkeletonCard v-for="j in 4" :key="j" />
        </div>
      </div>
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
              :notion-id="notion.id"
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
            :notion-id="notion.id"
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
import { ref, onMounted, watch, onBeforeUnmount, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getNotionsPourUtilisateur } from '@/api'
import { getThemesWithNotionsForUser } from '@/api/themes'
import NotionCard from '@/components/UI/NotionCard.vue'
import SkeletonCard from '@/components/common/SkeletonCard.vue'
import { useDataPrefetch } from '@/composables/useDataPrefetch'

const props = defineProps({
  matiereId: { type: [Number, String], required: true },
  notionRouteName: { type: String, required: true }
})

const router = useRouter()
const userStore = useUserStore()
const { prefetchNotionContent } = useDataPrefetch()

const loading = ref(false)
const error = ref('')
const themes = ref([])
const themeToNotions = ref({})
const directNotions = ref([])

function goToNotion(notionId) {
  router.push({ name: props.notionRouteName, params: { notionId } })
}

// Cache hybride mémoire + localStorage pour accélérer l'affichage (5 minutes)
const CACHE_TTL_MS = 300000
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
    
    // Les données sont déjà triées par le backend - pas besoin de re-trier
    const themesList = Array.isArray(data?.themes) ? data.themes : []
    const notions = Array.isArray(data?.notions) ? data.notions : []

    // Grouper les notions par thème (notions déjà triées par theme_id, ordre, titre)
    const grouped = {}
    for (const n of notions) {
      if (!grouped[n.theme]) grouped[n.theme] = []
      grouped[n.theme].push(n)
    }

    themes.value = themesList
    themeToNotions.value = grouped
    directNotions.value = themesList.length === 0 ? notions.filter(n => !n.theme) : []

    const cachePayload = { themes: themes.value, themeToNotions: themeToNotions.value, directNotions: directNotions.value }
    cache.set(key, { t: Date.now(), v: cachePayload })
    writeToStorage(matiereId, cachePayload)
    
    // Précharger automatiquement les 3 premières notions en arrière-plan (non-bloquant)
    await nextTick()
    prefetchTopNotions()
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

/**
 * Précharge les 3 premières notions en arrière-plan
 * pour accélérer la navigation utilisateur
 */
function prefetchTopNotions() {
  // Collecter les 3 premières notions de tous les thèmes
  const topNotions = []
  for (const theme of themes.value) {
    const notionsInTheme = themeToNotions.value[theme.id] || []
    topNotions.push(...notionsInTheme.slice(0, 1)) // 1ère notion de chaque thème
    if (topNotions.length >= 3) break
  }
  
  // Précharger en arrière-plan (fire and forget)
  topNotions.slice(0, 3).forEach(notion => {
    if (notion?.id) {
      setTimeout(() => {
        prefetchNotionContent(notion.id).catch(() => {
          // Ignorer les erreurs silencieusement
        })
      }, 500) // Délai de 500ms pour ne pas bloquer l'UI
    }
  })
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
/* (Reverted) Removed compact spacing overrides */
.tnv-wrapper {
  width: 100%;
  max-width: none;
  /* left align content within dashboard main */
  margin: 0;
}

/* États de chargement et d'erreur */
/* Loading Skeleton */
.tnv-loading-skeleton {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.tnv-theme-skeleton {
  background: transparent;
  border-radius: 0;
}

.skeleton-theme-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #f3f4f6;
}

.skeleton-line {
  height: 12px;
  background: linear-gradient(
    90deg,
    #f3f4f6 0%,
    #e5e7eb 50%,
    #f3f4f6 100%
  );
  background-size: 200% 100%;
  border-radius: 4px;
  animation: skeleton-loading 1.5s ease-in-out infinite;
}

.skeleton-theme-title {
  height: 24px;
  width: 200px;
}

.tnv-skeleton-grid {
  display: grid;
  grid-template-columns: repeat(4, 280px);
  gap: 1rem;
  justify-content: start;
}

@keyframes skeleton-loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

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
  padding: 0.4rem 0.65rem;
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
  
  .tnv-skeleton-grid {
    grid-template-columns: repeat(3, 280px);
  }
}

@media (max-width: 1200px) {
  .tnv-notions-grid {
    grid-template-columns: repeat(2, 280px);
    gap: 1rem;
    justify-content: start;
  }
  
  .tnv-skeleton-grid {
    grid-template-columns: repeat(2, 280px);
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
  
  .tnv-skeleton-grid {
    grid-template-columns: 280px;
  }

  .tnv-theme-block {
    padding: 1.25rem;
    margin-bottom: 1.5rem;
  }

  .tnv-theme-header {
    flex-direction: row;
    align-items: center;
    gap: 0.75rem;
  }

  .tnv-theme-title {
    font-size: 1.25rem;
  }
}

</style>


