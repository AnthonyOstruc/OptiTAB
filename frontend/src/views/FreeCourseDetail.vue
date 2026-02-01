<script setup>
import { ref, onMounted, nextTick, watch, computed, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import BackButton from '@/components/common/BackButton.vue'
import ExerciceQCM from '@/components/UI/ExerciceQCM.vue'
import { getFreeResource } from '@/api/free-content'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { renderContentWithImages, renderMath } from '@/utils/scientificRenderer'
import { setPageSeo } from '@/services/seo'
import { useUserStore } from '@/stores/user'
import { useSubscriptionStore } from '@/stores/subscription'

const props = defineProps({
  resourceType: {
    type: String,
    default: 'course'
  }
})

const route = useRoute()
const router = useRouter()
const { openModal } = useModalManager()
const userStore = useUserStore()
const subscriptionStore = useSubscriptionStore()

const resource = ref(null)
const loading = ref(false)
const error = ref(null)
const tableOfContents = ref([])
const isTocExpanded = ref(false)
const contentRef = ref(null)
const viewportWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1920)
const contentHeight = ref(0)
const renderedContent = computed(() => {
  if (!resource.value) return ''
  if (resource.value.contenu) {
    return renderContentWithImages(resource.value.contenu, resource.value.images || [])
  }
  return resource.value.contenu_html || ''
})
const isExerciseResource = computed(() => props.resourceType === 'exercise')
const exerciseInstruction = computed(() => {
  if (!resource.value) return ''
  return resource.value.question || resource.value.contenu || resource.value.accroche || ''
})
const exerciseSteps = computed(() => (resource.value?.etapes ? resource.value.etapes : ''))
const exerciseSolution = computed(() => {
  if (!resource.value) return ''
  return resource.value.solution || resource.value.reponse_correcte || ''
})
const exerciseDifficulty = computed(() => resource.value?.difficulty || 'medium')
const exerciseImages = computed(() => resource.value?.images || [])

const safeRenderMath = async () => {
  try {
    await renderMath()
  } catch (_) {
    // Ignore MathJax failures (e.g., when the content is empty or MathJax is busy)
  }
}
const showScrollTopButton = ref(false)
const backButtonLabel = computed(() => {
  if (props.resourceType === 'exercise') {
    return 'Retour aux exercices gratuits'
  }
  if (props.resourceType === 'summary') {
    return 'Retour aux fiches'
  }
  return 'Retour aux chapitres'
})

const subscriptionCtaLabel = computed(() => (subscriptionStore.hasAccess ? 'Gérer mon abonnement' : "S'abonner"))

const onSubscriptionCtaClick = () => {
  if (!userStore.isAuthenticated) {
    openModal(MODAL_IDS.REGISTER)
    return
  }

  if (subscriptionStore.hasAccess) {
    router.push({ name: 'Subscription' }).catch(() => {})
    return
  }

  router.push({
    name: 'Billing',
    query: {
      redirect: route.fullPath,
      reason: 'free_resource_detail_cta'
    }
  }).catch(() => {})
}

function computeAutoZoom(width) {
  let base
  if (width >= 1400) base = 1
  else if (width >= 1200) base = 0.95
  else if (width >= 1024) base = 0.9
  else if (width >= 900) base = 0.85
  else if (width >= 768) base = 0.8
  else if (width >= 640) base = 0.78
  else if (width >= 520) base = 0.76
  else if (width >= 420) base = 0.74
  else base = 0.72

  if (width < 1024) {
    const extra = width < 768 ? 0.1 : 0.07
    return Math.max(0.6, base - extra)
  }
  return base
}

const zoomLevel = computed(() => computeAutoZoom(viewportWidth.value))

const zoomStyle = computed(() => {
  let z = zoomLevel.value || 1
  if (viewportWidth.value <= 768) {
    z = Math.max(0.6, z - 0.08)
  }
  const widthPercent = (100 / z).toFixed(3)

  const style = {
    transform: `scale(${z})`,
    transformOrigin: 'top left',
    width: `${widthPercent}%`,
    height: 'auto',
    minHeight: 'auto'
  }

  if (contentHeight.value > 0 && Number.isFinite(z) && z < 1) {
    const marginBottom = -Math.round(contentHeight.value * (1 - z))
    style.marginBottom = `${marginBottom}px`
  }

  return style
})

const fetchResource = async () => {
  loading.value = true
  error.value = null
  try {
    resource.value = await getFreeResource(route.params.slug)
  } catch (err) {
    console.error('Erreur chargement de la ressource gratuite', err)
    error.value = err?.message || "Impossible de charger cette ressource gratuite."
  } finally {
    loading.value = false
  }
}

const buildTableOfContents = () => {
  tableOfContents.value = []
  const root = contentRef.value
  if (!root) return
  const selectors = root.querySelectorAll('h1, h2, h3')
  const toc = []
  selectors.forEach((heading, index) => {
    const level = Number(heading.tagName.replace('H', ''))
    const text = heading.textContent?.trim()
    if (!text) return
    const id = heading.id || `free-course-heading-${index}`
    heading.id = id
    toc.push({ id, text, level })
  })
  tableOfContents.value = toc
}

const measureContentHeight = () => {
  if (!contentRef.value) {
    contentHeight.value = 0
    return
  }
  contentHeight.value = contentRef.value.scrollHeight || contentRef.value.offsetHeight || 0
}

const updateViewportWidth = () => {
  if (typeof window === 'undefined') return
  viewportWidth.value = window.innerWidth
  nextTick(() => measureContentHeight())
}

const handleScroll = () => {
  const threshold = 300
  showScrollTopButton.value = (window.scrollY || document.documentElement.scrollTop || 0) > threshold
}

const scrollToTop = () => {
  if (typeof window === 'undefined') return
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const scrollToSection = (id) => {
  const el = document.getElementById(id)
  if (!el) return
  el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const goBack = () => {
  let routeName = 'FreeCourses'
  if (props.resourceType === 'exercise') {
    routeName = 'FreeExercises'
  } else if (props.resourceType === 'summary') {
    routeName = 'FreeSummaries'
  }
  router.push({ name: routeName })
}

const openSignup = () => {
  openModal(MODAL_IDS.REGISTER)
}

function stripHtml(input) {
  return String(input || '').replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim()
}

function pickSeoDescription(value, resourceType) {
  const type = String(resourceType || '').trim().toLowerCase()
  const raw = type === 'exercise'
    ? (value?.question || value?.excerpt || value?.accroche || value?.contenu || value?.contenu_html || '')
    : (type === 'summary'
        ? (value?.accroche || value?.excerpt || value?.contenu || value?.contenu_html || '')
        : (value?.excerpt || value?.accroche || value?.contenu || value?.contenu_html || ''))

  const cleaned = stripHtml(raw)
  if (!cleaned) return ''
  return cleaned.length > 160 ? `${cleaned.slice(0, 157).trimEnd()}...` : cleaned
}

function pickSeoImage(value) {
  const cover = value?.cover_image
  if (cover) return cover
  const img = Array.isArray(value?.images) ? value.images[0]?.image : ''
  return img || ''
}

function clampMetaDescription(text) {
  const cleaned = String(text || '').replace(/\s+/g, ' ').trim()
  if (!cleaned) return ''
  return cleaned.length > 160 ? `${cleaned.slice(0, 157).trimEnd()}...` : cleaned
}

function clampTitle(text, maxLength = 70) {
  const cleaned = String(text || '').replace(/\s+/g, ' ').trim()
  if (!cleaned) return ''
  if (cleaned.length <= maxLength) return cleaned
  const truncated = cleaned.slice(0, maxLength - 1)
  const cut = truncated.lastIndexOf(' ')
  return `${(cut > 20 ? truncated.slice(0, cut) : truncated).trimEnd()}…`
}

function normalizeSeoSubject(matiereNom) {
  const raw = String(matiereNom || '').replace(/\s+/g, ' ').trim()
  if (!raw) return { display: 'Maths', phrase: 'maths' }
  if (/math/i.test(raw)) return { display: 'Maths', phrase: 'maths' }
  return { display: raw, phrase: raw }
}

function buildSeoTitle({ resourceType, baseTitle, subjectDisplay, niveauNom }) {
  const type = String(resourceType || '').trim().toLowerCase()
  const niveau = String(niveauNom || '').replace(/\s+/g, ' ').trim()
  const levelPart = niveau ? ` (${niveau})` : ''
  const subject = String(subjectDisplay || '').trim()

  const prefix = type === 'exercise'
    ? `Exercice corrigé gratuit de ${subject}${levelPart}`
    : (type === 'summary'
        ? `Fiche de révision gratuite de ${subject}${levelPart}`
        : `Cours gratuit de ${subject}${levelPart}`)

  const mainTitle = String(baseTitle || '').replace(/\s+/g, ' ').trim()
  const full = mainTitle ? `${prefix} : ${mainTitle}` : prefix
  return clampTitle(full, 70)
}

function buildSeoDescription({ resourceType, subjectPhrase, niveauNom, baseDescription, baseTitle }) {
  const type = String(resourceType || '').trim().toLowerCase()
  const niveau = String(niveauNom || '').replace(/\s+/g, ' ').trim()
  const levelPart = niveau ? ` (${niveau})` : ''
  const subject = String(subjectPhrase || '').trim() || 'maths'

  const intro = type === 'exercise'
    ? `Exercice corrigé gratuit de ${subject}${levelPart}.`
    : (type === 'summary'
        ? `Fiche de révision gratuite de ${subject}${levelPart}.`
        : `Cours gratuit de ${subject}${levelPart}.`)

  const detail = String(baseDescription || baseTitle || '').replace(/\s+/g, ' ').trim()
  const extra = type === 'exercise'
    ? 'Correction détaillée et méthode.'
    : (type === 'summary'
        ? 'Formules, méthodes et exemples.'
        : 'Cours clair, méthodes et exemples.')

  return clampMetaDescription([intro, detail, extra, 'Accès gratuit sur OptiTAB.'].filter(Boolean).join(' '))
}

function getSiteUrl() {
  const fromEnv = String(import.meta?.env?.VITE_SITE_URL || '').trim()
  if (fromEnv) return fromEnv.replace(/\/+$/, '')
  if (typeof window !== 'undefined' && window.location?.origin) return window.location.origin
  return 'https://optitab.net'
}

function toAbsoluteUrl(maybeUrlOrPath) {
  const raw = String(maybeUrlOrPath || '').trim()
  if (!raw) return ''
  if (/^https?:\/\//i.test(raw)) return raw
  const base = getSiteUrl()
  return `${base}${raw.startsWith('/') ? '' : '/'}${raw}`
}

function toIsoDate(value) {
  if (!value) return ''
  try {
    const date = new Date(value)
    if (Number.isNaN(date.getTime())) return ''
    return date.toISOString()
  } catch (_) {
    return ''
  }
}

function seoPrefixForResourceType(type) {
  if (type === 'exercise') return 'Exercice corrigé gratuit'
  if (type === 'summary') return 'Fiche de révision gratuite'
  return 'Cours gratuit'
}

watch(
  resource,
  (value) => {
    if (!value) return
    const canonicalSlug = value?.slug ? String(value.slug) : ''
    const currentSlug = route?.params?.slug ? String(route.params.slug) : ''
    if (canonicalSlug && currentSlug && canonicalSlug !== currentSlug) {
      router.replace({
        name: route.name,
        params: { ...route.params, slug: canonicalSlug },
        query: route.query,
        hash: route.hash
      }).catch(() => {})
      return
    }
    const prefix = seoPrefixForResourceType(props.resourceType)
    const matiere = value?.matiere_nom ? String(value.matiere_nom).trim() : ''
    const niveau = value?.niveau_nom ? String(value.niveau_nom).trim() : (value?.tag_secondaire ? String(value.tag_secondaire).trim() : '')
    const baseTitle = value?.titre ? String(value.titre).trim() : ''

    const subject = normalizeSeoSubject(matiere)
    const contextParts = [prefix, subject.display, niveau].filter(Boolean)
    const context = contextParts.join(' ').trim()

    const title = buildSeoTitle({
      resourceType: props.resourceType,
      baseTitle,
      subjectDisplay: subject.display,
      niveauNom: niveau
    }) || (baseTitle || context || undefined)

    const baseDescription = pickSeoDescription(value, props.resourceType)
    const description = buildSeoDescription({
      resourceType: props.resourceType,
      subjectPhrase: subject.phrase,
      niveauNom: niveau,
      baseDescription,
      baseTitle,
    }) || undefined
    const image = pickSeoImage(value) || undefined
    const imageAbs = image ? toAbsoluteUrl(image) : ''
    const canonicalUrl = toAbsoluteUrl(route.path)
    const siteUrl = getSiteUrl()
    const organizationId = `${siteUrl}/#organization`
    const websiteId = `${siteUrl}/#website`
    const webPageId = `${canonicalUrl}#webpage`
    const categoryPath = props.resourceType === 'exercise'
      ? '/ressources-gratuites/exercices'
      : (props.resourceType === 'summary' ? '/ressources-gratuites/syntheses' : '/ressources-gratuites/cours')
    const categoryLabel = props.resourceType === 'exercise'
      ? 'Exercices corrigés gratuits'
      : (props.resourceType === 'summary' ? 'Fiches de synthèse gratuites' : 'Cours gratuits')
    const dateModified = toIsoDate(value?.date_modification || value?.updated_at || value?.date_update || value?.date_mise_a_jour)

    const jsonLdGraph = [
      {
        '@type': 'BreadcrumbList',
        itemListElement: [
          { '@type': 'ListItem', position: 1, name: 'Accueil', item: toAbsoluteUrl('/') },
          { '@type': 'ListItem', position: 2, name: categoryLabel, item: toAbsoluteUrl(categoryPath) },
          { '@type': 'ListItem', position: 3, name: baseTitle || context || 'Ressource gratuite', item: canonicalUrl }
        ]
      },
      {
        '@type': 'Article',
        '@id': `${canonicalUrl}#article`,
        headline: baseTitle || context || 'Ressource gratuite',
        description: description || clampMetaDescription(baseDescription) || undefined,
        inLanguage: 'fr-FR',
        isPartOf: { '@id': websiteId },
        mainEntityOfPage: { '@id': webPageId },
        author: { '@id': organizationId },
        publisher: { '@id': organizationId },
        image: imageAbs ? [imageAbs] : undefined,
        dateModified: dateModified || undefined,
        keywords: [matiere, niveau].filter(Boolean).join(', ') || undefined
      }
    ]

    setPageSeo({
      title,
      description,
      canonicalPath: route.path,
      robots: 'index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1',
      ogType: 'article',
      image,
      jsonLdGraph
    })
  },
  { immediate: true }
)

watch(
  error,
  (value) => {
    const message = String(value || '').trim()
    if (!message) return
    setPageSeo({
      title: 'Ressource introuvable',
      description: 'Cette ressource gratuite est introuvable ou indisponible.',
      canonicalPath: route.path,
      robots: 'noindex,follow'
    })
  }
)

watch(
  () => route.params.slug,
  () => {
    resource.value = null
    fetchResource()
  }
)

watch(
  renderedContent,
  async (html) => {
    if (!html) {
      tableOfContents.value = []
      return
    }
    await nextTick()
    buildTableOfContents()
    await safeRenderMath()
    measureContentHeight()
  },
  { immediate: true }
)

watch(zoomLevel, () => {
  nextTick(() => measureContentHeight())
})

onMounted(() => {
  fetchResource()
  if (typeof window !== 'undefined') {
    window.addEventListener('resize', updateViewportWidth, { passive: true })
    window.addEventListener('scroll', handleScroll, { passive: true })
  }
})

onBeforeUnmount(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', updateViewportWidth)
    window.removeEventListener('scroll', handleScroll)
  }
})
</script>

<template>
  <MainLayout>
    <section class="cours-section">
      <BackButton 
        :text="backButtonLabel" 
        :custom-action="goBack"
        position="top-left"
      />

      <div class="cours-body">
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner" aria-hidden="true"></div>
          <p class="loading-text">Chargement de la ressource...</p>
        </div>

        <div v-else-if="error" class="error-state">
          <p>{{ error }}</p>
          <button @click="fetchResource">Réessayer</button>
        </div>

        <div v-else-if="resource" class="cours-container">
           <header class="cours-header">
             <div class="cours-title-row">
               <h1 class="cours-title">{{ resource.titre }}</h1>
             </div>
           </header>

           <section class="free-resource-cta" aria-label="Accès professeur ou plateforme">
             <div class="free-resource-cta__copy">
               <p class="free-resource-cta__title">Besoin d’un professeur ou d’un accès complet&nbsp;?</p>
               <p class="free-resource-cta__subtitle">Cours particuliers de maths en ligne • Abonnement plateforme OptiTAB</p>
             </div>
             <div class="free-resource-cta__actions">
               <router-link
                 :to="{ name: 'CoursParticuliers' }"
                 class="free-resource-cta__btn free-resource-cta__btn--primary"
                 data-track="nav"
                 data-nav-name="tutoring"
                 data-nav-location="free_resource_detail_banner"
               >
                 Cours particuliers
               </router-link>
               <button
                 type="button"
                 class="free-resource-cta__btn free-resource-cta__btn--secondary"
                 data-cta-name="subscribe"
                 data-cta-location="free_resource_detail_banner"
                 @click="onSubscriptionCtaClick"
               >
                 {{ subscriptionCtaLabel }}
               </button>
             </div>
           </section>

           <div v-if="isExerciseResource" class="exercise-detail-body">
             <ExerciceQCM
               :eid="resource.id"
              :titre="resource.titre"
              :instruction="exerciseInstruction"
              :etapes="exerciseSteps"
              :solution="exerciseSolution"
              :difficulty="exerciseDifficulty"
              :preview-images="exerciseImages"
              :readonly="true"
            />
          </div>

          <nav v-if="tableOfContents.length && !isExerciseResource" class="toc-container">
            <div class="toc-header" @click="isTocExpanded = !isTocExpanded">
              <div class="toc-header-content">
                <svg class="toc-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="8" y1="6" x2="21" y2="6"/>
                  <line x1="8" y1="12" x2="21" y2="12"/>
                  <line x1="8" y1="18" x2="21" y2="18"/>
                  <line x1="3" y1="6" x2="3.01" y2="6"/>
                  <line x1="3" y1="12" x2="3.01" y2="12"/>
                  <line x1="3" y1="18" x2="3.01" y2="18"/>
                </svg>
                <h3 class="toc-title">Sommaire</h3>
              </div>
              <svg class="toc-toggle-icon" :class="{ expanded: isTocExpanded }" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9" />
              </svg>
          </div>
          <transition name="toc-expand">
              <div v-show="isTocExpanded" class="toc-body">
                <ul class="toc-list">
                  <li 
                    v-for="(item, index) in tableOfContents" 
                    :key="item.id || index"
                    :class="['toc-item', `toc-level-${item.level}`]"
                  >
                    <a class="toc-link" href="#" @click.prevent="scrollToSection(item.id)">
                      {{ item.text }}
                    </a>
                  </li>
                </ul>
              </div>
            </transition>
          </nav>

           <div v-if="!isExerciseResource" class="cours-content-outer" :style="zoomStyle">
             <div class="cours-content" ref="contentRef" v-html="renderedContent" />
           </div>

           <transition name="scroll-top-fade">
             <button
               v-show="showScrollTopButton && !isExerciseResource"
              class="scroll-top-btn"
              @click="scrollToTop"
              aria-label="Retour en haut"
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="18 15 12 9 6 15" />
              </svg>
            </button>
          </transition>
        </div>
      </div>
    </section>
  </MainLayout>
</template>

<style scoped>
.cours-section {
  padding: 48px 2vw 60px;
  background: #fff;
  min-height: 100vh;
  position: relative;
}

.cours-body {
  width: 100%;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 4px solid #e5ecff;
  border-top-color: #2563eb;
  animation: spin 0.9s linear infinite;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 36px 0;
}

.loading-text {
  margin: 0;
  font-weight: 600;
  color: #1d3b8b;
  font-size: 15px;
}

@media (max-width: 768px) {
  .cours-section {
    padding-top: 32px;
  }

  .cours-header {
    margin-bottom: 0;
  }
}

.cours-header {
  text-align: center;
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.cours-title-row {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.cours-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.cours-badge,
.cours-type-pill {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 999px;
  border: 1px solid transparent;
}

.cours-badge {
  background: #e0f2fe;
  color: #0f172a;
  border-color: rgba(37, 99, 235, 0.4);
}

.cours-type-pill {
  background: #f1f5f9;
  color: #1d3557;
  border-color: rgba(148, 163, 184, 0.5);
}

.cours-context {
  margin: 0;
  color: #475569;
  font-weight: 600;
  font-size: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: center;
}

.exercise-detail-body {
  margin: 20px 0 0;
  width: 100%;
  padding: 0 0 24px;
}

.free-resource-cta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 16px;
  border-radius: 18px;
  border: 1px solid rgba(59, 130, 246, 0.25);
  background: linear-gradient(90deg, rgba(59, 130, 246, 0.10), rgba(99, 102, 241, 0.07));
  margin: 18px 0 22px 0;
}

.free-resource-cta__copy {
  min-width: 0;
}

.free-resource-cta__title {
  margin: 0;
  font-size: 14px;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.01em;
}

.free-resource-cta__subtitle {
  margin: 4px 0 0 0;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  line-height: 1.45;
}

.free-resource-cta__actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  flex-wrap: wrap;
  white-space: nowrap;
}

.free-resource-cta__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  min-height: 40px;
  padding: 10px 18px;
  border-radius: 999px;
  font-weight: 800;
  font-size: 13px;
  letter-spacing: -0.01em;
  border: 1px solid transparent;
  text-decoration: none;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  user-select: none;
  transition: transform 0.15s ease, box-shadow 0.2s ease, background 0.2s ease, color 0.2s ease, border-color 0.2s ease;
}

.free-resource-cta__btn--primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 55%, #1d4ed8 100%);
  color: #fff;
  border-color: rgba(255, 255, 255, 0.18);
  box-shadow: 0 14px 32px rgba(59, 130, 246, 0.24);
}

.free-resource-cta__btn--primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 18px 38px rgba(59, 130, 246, 0.3);
}

.free-resource-cta__btn--primary::after {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: linear-gradient(120deg, rgba(255, 255, 255, 0.22), rgba(255, 255, 255, 0) 52%);
  transform: translateX(-70%);
  transition: transform 0.55s ease;
}

.free-resource-cta__btn--primary:hover::after {
  transform: translateX(-15%);
}

.free-resource-cta__btn--secondary {
  background: rgba(255, 255, 255, 0.9);
  color: #2563eb;
  border-color: rgba(59, 130, 246, 0.25);
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.06);
}

.free-resource-cta__btn--secondary:hover {
  transform: translateY(-1px);
  background: rgba(59, 130, 246, 0.08);
  border-color: rgba(59, 130, 246, 0.32);
  box-shadow: 0 14px 28px rgba(15, 23, 42, 0.08);
}

.free-resource-cta__btn:active {
  transform: translateY(0);
}

.free-resource-cta__btn:focus-visible {
  outline: 2px solid rgba(59, 130, 246, 0.45);
  outline-offset: 2px;
}

@media (max-width: 640px) {
  .free-resource-cta {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
    width: 100%;
  }

  .free-resource-cta__actions {
    justify-content: stretch;
  }

  .free-resource-cta__btn {
    width: 100%;
  }
}

.exercise-intro {
  font-size: 16px;
  color: #1f2937;
  margin: 0 0 16px;
}

.exercise-section {
  margin-bottom: 24px;
  padding: 18px;
  border-radius: 20px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
}

.exercise-section h3 {
  margin: 0 0 12px;
  font-size: 18px;
  color: #0f172a;
}

.exercise-card {
  background: #fff;
  border-radius: 24px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 20px 45px rgba(15, 23, 42, 0.08);
  padding: 20px 22px;
  margin: 18px 0 16px;
}

.exercise-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 12px;
}

.exercise-card-title {
  margin: 0;
  font-size: clamp(20px, 2vw, 26px);
  font-weight: 700;
  color: #0f172a;
}

.exercise-card-subtitle {
  margin: 4px 0 0;
  color: #475569;
  font-size: 15px;
}

.exercise-card-star {
  border-radius: 999px;
  border: 1px solid #d1d5db;
  background: #fefefe;
  width: 42px;
  height: 42px;
  font-size: 18px;
  cursor: pointer;
}

.exercise-card-tabs {
  display: flex;
  justify-content: flex-start;
  gap: 8px;
  margin-top: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e2e8f0;
}

.exercise-card-panel {
  margin-top: 10px;
  padding: 0;
}

.exercise-section-card {
  background: #f9fafb;
  border-radius: 18px;
  border: 1px solid #e2e8f0;
  padding: 16px 18px;
  min-height: 190px;
  font-size: 16px;
  line-height: 1.4;
}

.exercise-section-card :deep(*) {
  margin: 0;
  line-height: inherit;
}

.exercise-section-card :deep(p + p),
.exercise-section-card :deep(p + ul),
.exercise-section-card :deep(p + ol),
.exercise-section-card :deep(ul + p),
.exercise-section-card :deep(ol + p),
.exercise-section-card :deep(li + li) {
  margin-top: 4px;
}

.exercise-section-card :deep(ul),
.exercise-section-card :deep(ol) {
  padding-left: 18px;
}

.exercise-section-card :deep(li) {
  padding: 0;
}

.exercise-tabs {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 18px;
  padding-bottom: 4px;
  border-bottom: 1px solid #dbeafe;
}

.exercise-tab {
  border: none;
  background: transparent;
  padding: 8px 20px;
  font-weight: 600;
  color: #64748b;
  border-radius: 999px;
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease;
}

.exercise-tab.active {
  color: #0f172a;
  background: #e0f2fe;
  box-shadow: inset 0 -3px 0 0 #2563eb;
}

.cours-title {
  font-size: clamp(24px, 3vw, 30px);
  color: #193e8e;
  margin: 0 0 8px;
  font-weight: 800;
}

.detail-meta {
  color: #475569;
  font-weight: 600;
  margin: 8px 0 0;
}

.inline-back {
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 999px;
  border: 1px solid rgba(25, 62, 142, 0.3);
  background: #f5f8ff;
  color: #193e8e;
  font-weight: 600;
  cursor: pointer;
  transition: border-color 0.2s ease, color 0.2s ease;
}

.inline-back:hover {
  border-color: #193e8e;
}

.toc-container {
  margin: 12px 0 18px;
  width: 100%;
  border-radius: 24px;
  background: #f5f8ff;
  border: 1px solid rgba(25, 62, 142, 0.12);
  overflow: hidden;
  transform-origin: top left;
}

@media (max-width: 1024px) {
  .toc-container {
    transform: scale(0.96);
  }
}

@media (max-width: 768px) {
  .toc-container {
    transform: scale(0.85);
    margin: 0 auto;
  }

  .toc-header {
    font-size: 0.95rem;
    padding: 6px 14px;
  }

  .toc-body {
    padding: 8px 14px 12px;
  }

  .toc-item {
    font-size: 0.9rem;
  }

  .toc-level-3 .toc-link {
    padding-left: 18px;
    font-size: 0.85rem;
  }
}

.toc-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 18px;
  cursor: pointer;
  color: #1d3b8b;
  font-weight: 600;
  font-size: 16px;
}

.toc-header-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.toc-body {
  border-top: 1px solid rgba(25, 62, 142, 0.12);
  padding: 10px 22px 16px;
}

.toc-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.toc-item {
  font-size: 16px;
  color: #0f172a;
}

.toc-link {
  text-decoration: none;
  color: #193e8e;
  font-weight: 600;
}

.toc-level-3 .toc-link {
  font-weight: 400;
  color: #1d4ed8;
  padding-left: 24px;
}

.cours-content-outer {
  width: 100%;
  transform-origin: top left;
  transition: transform 0.2s ease;
  overflow-x: hidden;
  margin-top: -8px;
}

.cours-content {
  width: 100%;
  padding: 0 0 40px;
  line-height: 1.75;
  color: #1f2937;
  font-size: 17px;
}

.cours-content :deep(h1),
.cours-content :deep(h2),
.cours-content :deep(h3) {
  color: #0f172a;
  margin-top: 32px;
  border-bottom: 2px solid #3b82f6;
  padding-bottom: 8px;
}

.scroll-top-btn {
  position: fixed;
  bottom: 28px;
  left: 24px;
  width: 50px;
  height: 50px;
  border: none;
  border-radius: 50%;
  background: #1d3b8b;
  color: #fff;
  box-shadow: 0 15px 30px rgba(29, 59, 139, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 1200;
}

.scroll-top-fade-enter-active,
.scroll-top-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.scroll-top-fade-enter-from,
.scroll-top-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
