<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount, toRef } from 'vue'
import { RouterLink } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import FreeContentCard from '@/components/free-content/FreeContentCard.vue'
import { getFreeResources } from '@/api/free-content'
import { freeContentMeta, freeContentFallback } from '@/config/freeContent'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'

const props = defineProps({
  resourceType: {
    type: String,
    required: true
  }
})

const { openModal } = useModalManager()
const resourceType = toRef(props, 'resourceType')

const resources = ref([])
const loading = ref(false)
const error = ref(null)
const searchTerm = ref('')
const quickFilter = ref('')
let debounceId = null

const tabs = computed(() =>
  Object.entries(freeContentMeta).map(([type, meta]) => ({
    type,
    label: meta.title,
    routeName: meta.routeName
  }))
)

const meta = computed(() => {
  return freeContentMeta[resourceType.value] || {
    title: 'Ressources gratuites',
    highlight: '',
    description: '',
    badge: '',
    accent: '#2563eb',
    subjectLine: '',
    context: '',
    searchPlaceholder: 'Rechercher une ressource gratuite...',
    quickFilters: [],
    hero: { title: '', subtitle: '', stats: [] }
  }
})

const fallbackItems = computed(() => freeContentFallback[resourceType.value] || [])

const displayResources = computed(() => {
  if (resources.value.length > 0) {
    return resources.value
  }
  return fallbackItems.value
})

const showFallbackBanner = computed(() => !loading.value && resources.value.length === 0)

const heroStats = computed(() => meta.value.hero?.stats || [])
const searchPlaceholder = computed(() => meta.value.searchPlaceholder || 'Rechercher une ressource gratuite...')
const hasQuickFilters = computed(() => Array.isArray(meta.value.quickFilters) && meta.value.quickFilters.length > 0)

const fetchResources = async () => {
  loading.value = true
  error.value = null
  try {
    const params = {
      type: resourceType.value
    }
    const useQuickFilter = Array.isArray(meta.value.quickFilters) && meta.value.quickFilters.length > 0
    const term = (useQuickFilter ? quickFilter.value : '') || searchTerm.value
    if (term) {
      params.q = term
    }
    const data = await getFreeResources(params)
    resources.value = Array.isArray(data?.results) ? data.results : data
  } catch (err) {
    console.error('Erreur chargement ressources gratuites', err)
    error.value = err?.message || 'Impossible de charger les aperçus gratuits pour le moment.'
  } finally {
    loading.value = false
  }
}

const triggerFetch = () => {
  if (debounceId) {
    clearTimeout(debounceId)
  }
  debounceId = setTimeout(fetchResources, 320)
}

watch(resourceType, () => {
  quickFilter.value = ''
  searchTerm.value = ''
  fetchResources()
})

watch(searchTerm, triggerFetch)
watch(quickFilter, triggerFetch)

onMounted(() => {
  fetchResources()
})

onBeforeUnmount(() => {
  if (debounceId) {
    clearTimeout(debounceId)
  }
})

const applyQuickFilter = (term) => {
  quickFilter.value = term
}

const openSubscriptionModal = () => {
  openModal(MODAL_IDS.REGISTER)
}

</script>

<template>
  <MainLayout>
    <div class="free-content-page">
      <section class="hero">
        <div class="hero-top">
          <p class="hero-badge">
            {{ meta.badge }}
          </p>
          <h1>{{ meta.hero?.title }}</h1>
          <p class="hero-subtitle">
            {{ meta.hero?.subtitle }}
          </p>
          <p v-if="meta.subjectLine" class="hero-subject">
            {{ meta.subjectLine }}
          </p>
          <p v-if="meta.context" class="hero-context">
            {{ meta.context }}
          </p>
          <div class="hero-ctas">
            <button class="cta-primary" @click="openSubscriptionModal">
              Créer un compte gratuit
            </button>
            <a href="/#tarifs" class="cta-secondary">
              Voir les tarifs famille
            </a>
          </div>
          <div class="hero-stats" v-if="heroStats.length">
            <div v-for="stat in heroStats" :key="stat" class="stat-pill">
              {{ stat }}
            </div>
          </div>
        </div>
      </section>

      <nav class="tabs">
        <RouterLink
          v-for="tab in tabs"
          :key="tab.type"
          :to="{ name: tab.routeName }"
          class="tab"
          :class="{ active: tab.type === resourceType }"
        >
          {{ tab.label }}
        </RouterLink>
      </nav>

      <section class="filters">
        <div class="search-field">
          <input
            v-model="searchTerm"
            type="text"
            :placeholder="searchPlaceholder"
          />
        </div>
        <div v-if="hasQuickFilters" class="quick-filters">
          <button
            v-for="term in meta.quickFilters"
            :key="term"
            :class="['quick-filter', { active: quickFilter === term }]"
            @click="applyQuickFilter(quickFilter === term ? '' : term)"
          >
            {{ term }}
          </button>
        </div>
      </section>

      <section class="cards-wrapper">
        <p v-if="error" class="error-text">{{ error }}</p>

        <div v-if="loading" class="skeleton-grid">
          <div v-for="n in 3" :key="n" class="skeleton-card" />
        </div>

        <div v-else class="cards-grid">
          <FreeContentCard
            v-for="resource in displayResources"
            :key="resource.slug || resource.id"
            :resource="resource"
            @open-subscription="openSubscriptionModal"
          />
        </div>

        <div v-if="showFallbackBanner" class="fallback-banner">
          <p>
            Ajoutez vos cours/exercices dans l'admin « Ressources gratuites » puis relancez la page pour les afficher ici.
          </p>
        </div>
      </section>

      <section v-if="meta.pedago || meta.checklist" class="pedago-section">
        <article v-if="meta.pedago" class="pedago-card">
          <p class="card-eyebrow">{{ meta.pedago.badge }}</p>
          <h3>{{ meta.pedago.title }}</h3>
          <p class="card-subtitle">{{ meta.pedago.subtitle }}</p>
          <ul class="steps-list">
            <li v-for="step in meta.pedago.steps" :key="step.title">
              <span class="step-title">{{ step.title }}</span>
              <span class="step-text">{{ step.text }}</span>
            </li>
          </ul>
          <button
            v-if="meta.pedago.ctaText"
            class="cta-ghost"
            @click="openSubscriptionModal"
          >
            {{ meta.pedago.ctaText }}
          </button>
        </article>
        <article v-if="meta.checklist" class="pedago-card pedago-card--calm">
          <p class="card-eyebrow">{{ meta.checklist.badge }}</p>
          <h3>{{ meta.checklist.title }}</h3>
          <ul class="checklist">
            <li v-for="item in meta.checklist.bullets" :key="item">
              <span class="check-dot"></span>
              <span>{{ item }}</span>
            </li>
          </ul>
          <p v-if="meta.checklist.note" class="card-note">
            {{ meta.checklist.note }}
          </p>
        </article>
      </section>
    </div>
  </MainLayout>
</template>

<style scoped lang="scss">
.free-content-page {
  padding: 140px 24px 80px;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 34px;
}

.hero {
  text-align: center;
}

.hero-badge {
  display: inline-flex;
  padding: 6px 14px;
  border-radius: 999px;
  background: rgba(59, 130, 246, 0.1);
  color: #1d4ed8;
  font-weight: 600;
  margin-bottom: 12px;
}

h1 {
  font-size: clamp(32px, 5vw, 46px);
  color: #0f172a;
  margin: 0;
}

.hero-subtitle {
  font-size: 18px;
  color: #475569;
  margin: 14px auto 26px;
  max-width: 600px;
}

.hero-subject {
  display: inline-flex;
  margin: 0 auto 12px;
  padding: 6px 18px;
  border-radius: 999px;
  background: #e0e7ff;
  color: #1e1b4b;
  font-weight: 600;
}

.hero-context {
  max-width: 720px;
  margin: 0 auto 24px;
  color: #334155;
  line-height: 1.5;
}

.hero-ctas {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

.cta-primary {
  background: linear-gradient(120deg, #2563eb, #7c3aed);
  color: #fff;
  border: none;
  border-radius: 999px;
  padding: 14px 26px;
  font-weight: 600;
  cursor: pointer;
}

.cta-secondary {
  padding: 14px 26px;
  border-radius: 999px;
  border: 1px solid #cbd5f5;
  color: #2563eb;
  font-weight: 600;
  text-decoration: none;
}

.hero-stats {
  margin-top: 24px;
  display: flex;
  gap: 10px;
  justify-content: center;
  flex-wrap: wrap;
}

.stat-pill {
  padding: 6px 16px;
  border-radius: 999px;
  background: #f1f5f9;
  color: #0f172a;
  font-size: 14px;
  font-weight: 600;
}

.tabs {
  display: inline-flex;
  align-self: center;
  border: 1px solid #e2e8f0;
  border-radius: 999px;
  overflow: hidden;
}

.tab {
  padding: 10px 20px;
  text-decoration: none;
  color: #475569;
  font-weight: 600;
}

.tab.active {
  background: #0f172a;
  color: #fff;
}

.filters {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.search-field input {
  width: 100%;
  padding: 16px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  font-size: 16px;
}

.quick-filters {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.quick-filter {
  padding: 8px 16px;
  border-radius: 999px;
  border: 1px solid #cbd5f5;
  background: transparent;
  color: #1d4ed8;
  font-weight: 600;
  cursor: pointer;
}

.quick-filter.active {
  background: #1d4ed8;
  color: #fff;
}

.pedago-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.pedago-card {
  border-radius: 28px;
  padding: 32px;
  background: #0f172a;
  color: #e2e8f0;
  display: flex;
  flex-direction: column;
  gap: 16px;
  box-shadow: 0 25px 50px rgba(15, 23, 42, 0.2);
}

.pedago-card--calm {
  background: #f8fafc;
  color: #0f172a;
  box-shadow: none;
  border: 1px solid #e2e8f0;
}

.card-eyebrow {
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 0.12em;
  color: inherit;
  opacity: 0.8;
  margin: 0;
}

.card-subtitle {
  margin: 0;
  color: inherit;
  opacity: 0.9;
}

.steps-list,
.checklist {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.steps-list li {
  display: flex;
  flex-direction: column;
  gap: 4px;
  background: rgba(255, 255, 255, 0.08);
  padding: 12px 14px;
  border-radius: 16px;
}

.step-title {
  font-weight: 600;
}

.step-text {
  color: inherit;
  opacity: 0.85;
  font-size: 14px;
}

.cta-ghost {
  margin-top: auto;
  align-self: flex-start;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.4);
  padding: 10px 20px;
  background: transparent;
  color: inherit;
  font-weight: 600;
  cursor: pointer;
}

.pedago-card--calm .cta-ghost {
  border-color: #0f172a;
  color: #0f172a;
}

.checklist li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  color: inherit;
}

.check-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: currentColor;
  margin-top: 6px;
}

.card-note {
  margin: 8px 0 0;
  font-size: 14px;
  color: inherit;
  opacity: 0.8;
}

.cards-wrapper {
  display: flex;
  flex-direction: column;
  gap: 20px;
}


.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
}

.skeleton-card {
  border-radius: 24px;
  padding: 28px;
  background: linear-gradient(120deg, #f1f5f9, #e2e8f0, #f1f5f9);
  background-size: 200% 200%;
  animation: shimmer 1.6s infinite;
  min-height: 240px;
}

.fallback-banner {
  background: #fffbeb;
  border: 1px solid #fcd34d;
  border-radius: 20px;
  padding: 16px 24px;
  color: #92400e;
  font-weight: 500;
}

.error-text {
  color: #dc2626;
  font-weight: 600;
}

@keyframes shimmer {
  0% {
    background-position: 0% 50%;
  }
  100% {
    background-position: 100% 50%;
  }
}

@media (max-width: 768px) {
  .free-content-page {
    padding: 120px 16px 60px;
  }

  .tabs {
    flex-direction: column;
  }

  .tab {
    text-align: center;
  }
}
</style>
