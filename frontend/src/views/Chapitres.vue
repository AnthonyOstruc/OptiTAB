<template>
  <DashboardLayout>
    <section class="chapitres-section">
      <!-- États de chargement et d'erreur -->
      <div v-if="loading" class="chapitres-loader">
        <div class="loader-spinner"></div>
        <p>Chargement des chapitres...</p>
      </div>

      <div v-else-if="error" class="chapitres-error">
        <div class="error-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h3>Erreur de chargement</h3>
        <p>{{ error }}</p>
        <button class="retry-button" @click="loadChapitres">
          Réessayer
        </button>
      </div>

      <!-- Contenu principal avec le composant réutilisable -->
      <ChapitresListView
        v-else
        :title="notionNom"
        :chapitres="chapitres"
        back-button-text="Retour aux thèmes"
        :back-action="goBackToThemes"
        :on-chapitre-click="onChapitreClick"
      />
    </section>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import { getNotionChapitresAvecMeta, getChapitresByNotion, getNotionDetail } from '@/api'
import ChapitresListView from '@/components/common/ChapitresListView.vue'
import { useSubjectsStore } from '@/stores/subjects/index'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const subjectsStore = useSubjectsStore()
const userStore = useUserStore()

// Récupérer la matière active
const currentMatiereId = computed(() => {
  return subjectsStore.activeMatiereId || route.params.matiereId
})

// ID de la matière liée à la notion courante (récupéré via l'API notion)
const matiereIdForNotion = ref(null)

// Fonction pour revenir aux thèmes (liste des thèmes de la matière)
function goBackToThemes() {
  const targetMatiereId = matiereIdForNotion.value || subjectsStore.activeMatiereId || route.params.matiereId
  if (targetMatiereId) {
    router.push({ name: 'Themes', params: { matiereId: String(targetMatiereId) } })
  } else {
    router.push({ name: 'Exercises' })
  }
}

const chapitres = ref([])
const notionNom = ref('')
const loading = ref(true)
const error = ref('')

// Cache simple pour chapitres (mémoire + localStorage)
const CHAP_CACHE_TTL_MS = 120000
function chapStorageKey(notionId) { return `chapitres_meta:${notionId}` }
function readChapitresFromStorage(notionId) {
  try {
    const raw = localStorage.getItem(chapStorageKey(notionId))
    if (!raw) return null
    const parsed = JSON.parse(raw)
    if (!parsed?.t || !parsed?.v) return null
    if (Date.now() - parsed.t > CHAP_CACHE_TTL_MS) return null
    return parsed.v
  } catch (_) { return null }
}
function writeChapitresToStorage(notionId, value) {
  try { localStorage.setItem(chapStorageKey(notionId), JSON.stringify({ t: Date.now(), v: value })) } catch (_) {}
}

// Fonction pour charger les chapitres
async function loadChapitres() {
  const notionId = route.params.notionId
  if (!notionId) return
  
  loading.value = true
  error.value = ''
  
  try {
    // Try cache first
    const cached = readChapitresFromStorage(notionId)
    if (cached) {
      notionNom.value = cached.notion?.nom || cached.notion?.titre || 'Notion'
      matiereIdForNotion.value = cached.notion?.matiere || null
      chapitres.value = Array.isArray(cached.chapitres) ? cached.chapitres : []
      loading.value = false

      // also refresh in background
      getNotionChapitresAvecMeta(notionId)
        .then(r => {
          const d = r?.data || r
          const n = d?.notion || {}
          const lst = d?.chapitres || []
          if (n && Array.isArray(lst)) {
            writeChapitresToStorage(notionId, { notion: n, chapitres: lst })
          }
        })
        .catch(async () => {
          // Fallback: old endpoints
          try {
            const [notion, list] = await Promise.all([
              getNotionDetail(notionId),
              getChapitresByNotion(notionId)
            ])
            writeChapitresToStorage(notionId, { notion, chapitres: Array.isArray(list) ? list : [] })
          } catch (_) {}
        })
      return
    }

    const resp = await getNotionChapitresAvecMeta(notionId)
    const data = resp?.data || resp
    const notion = data?.notion || {}
    const list = data?.chapitres || []
    notionNom.value = notion?.nom || notion?.titre || 'Notion'
    matiereIdForNotion.value = notion?.matiere || null
    chapitres.value = Array.isArray(list) ? list : []
    writeChapitresToStorage(notionId, { notion, chapitres: chapitres.value })
    console.log(`[Chapitres] Chapitres chargés:`, chapitres.value.length)
  } catch (e) {
    console.error('[Chapitres] Erreur endpoint chapitres-avec-meta:', e)
    // Fallback: old endpoints
    try {
      const [notion, list] = await Promise.all([
        getNotionDetail(notionId),
        getChapitresByNotion(notionId)
      ])
      notionNom.value = notion?.nom || notion?.titre || 'Notion'
      matiereIdForNotion.value = notion?.matiere || null
      chapitres.value = Array.isArray(list) ? list : []
      writeChapitresToStorage(notionId, { notion, chapitres: chapitres.value })
      console.log(`[Chapitres] Fallback utilisé, chapitres:`, chapitres.value.length)
    } catch (err) {
      console.error('[Chapitres] Fallback échoué:', err)
      error.value = "Impossible de charger les chapitres. Veuillez réessayer."
    }
  } finally {
    loading.value = false
  }
}


onMounted(() => {
  loadChapitres()
})


function onChapitreClick(chapitreId) {
  router.push({ name: 'Exercices', params: { chapitreId } })
}
</script>

<style scoped>
.chapitres-section {
  background: #fff;
  padding: 0 5vw 40px 5vw;
  text-align: center;
}

/* Chargement */
.chapitres-loader {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.loader-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #10b981;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.chapitres-loader p {
  font-size: 1.125rem;
  color: #64748b;
  margin: 0;
}

/* Erreur */
.chapitres-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.error-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 64px;
  height: 64px;
  background: #fef2f2;
  border-radius: 16px;
  color: #ef4444;
  margin-bottom: 1rem;
}

.chapitres-error h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.chapitres-error p {
  font-size: 1rem;
  color: #64748b;
  margin: 0 0 1.5rem 0;
}

.retry-button {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(16, 185, 129, 0.3);
}
</style> 