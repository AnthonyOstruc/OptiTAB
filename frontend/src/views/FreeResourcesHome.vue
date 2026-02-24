<template>
  <MainLayout>
    <div class="free-resources-home-zoom" :style="freeResourcesZoomStyle">
      <div ref="freeResourcesContentRef" class="free-resources-home">
        <!-- Hero Section -->
        <section class="hero-section">
          <div class="hero-container">
            <span class="hero-badge">
              <SparklesIcon class="badge-icon" />
              100% Gratuit
            </span>
            <h1 class="hero-title">Ressources gratuites <span class="highlight">OptiTAB</span></h1>
            <p class="hero-subtitle">
              Découvrez gratuitement notre méthode : cours structurés, exercices corrigés pas-à-pas et fiches de synthèse pour réviser efficacement.
            </p>
          </div>
        </section>

        <section class="authority-intro" aria-label="Introduction ressources gratuites">
          <div class="authority-container">
            <h2 class="authority-title">Un parcours clair pour progresser en maths</h2>
            <p
              v-for="paragraph in hubAuthorityContent.introParagraphs"
              :key="paragraph"
              class="authority-paragraph"
            >
              {{ paragraph }}
            </p>
          </div>
        </section>

        <!-- Cards Section -->
        <section class="cards-section">
          <div class="cards-container">
            <article
              v-for="item in freeContentHomeBlocks"
              :key="item.type"
              class="resource-card"
            >
              <router-link :to="item.to" class="card-link">
                <div class="card-header">
                  <div class="badge" :class="`badge-${item.type}`">
                    {{ item.badge }}
                  </div>
                  <div class="card-icon">
                    <component :is="getIcon(item.type)" />
                  </div>
                </div>
                
                <h2 class="card-title">{{ item.title }}</h2>
                <p class="card-highlight">{{ item.highlight }}</p>
                <p class="card-description">{{ item.description }}</p>
                
                <ul class="features-list">
                  <li v-for="bullet in item.bullets" :key="bullet">
                    <CheckCircleIcon class="check-icon" />
                    <span>{{ bullet }}</span>
                  </li>
                </ul>
                
                <span class="explore-btn">
                  Explorer gratuitement
                  <ArrowRightIcon class="arrow-icon" />
                </span>
              </router-link>
            </article>
          </div>
        </section>

        <section class="popular-links" aria-label="Liens populaires ressources gratuites">
          <div class="popular-links__container">
            <h2 class="popular-links__title">Liens populaires</h2>
            <ul class="popular-links__list">
              <li v-for="link in hubPopularLinks" :key="link.href" class="popular-links__item">
                <router-link :to="link.href" class="popular-links__anchor">
                  {{ link.label }}
                </router-link>
              </li>
            </ul>
          </div>
        </section>

        <!-- CTA Section -->
        <section class="cta-section">
          <div class="cta-container">
            <h3 class="cta-title">Envie d'aller plus loin ?</h3>
            <p class="cta-desc">Accédez à l'ensemble des cours, exercices et synthèses avec un abonnement OptiTAB.</p>
            <div class="cta-buttons">
              <button class="cta-primary" @click="openSubscriptionModal">
                Créer un compte gratuit
              </button>
              <router-link to="/#tarifs" class="cta-secondary">
                Voir les tarifs
              </router-link>
            </div>
          </div>
        </section>

        <!-- FAQ Section -->
        <FaqSection :faq="hubAuthorityContent.faq" />
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import MainLayout from '@/components/layout/MainLayout.vue'
import FaqSection from '@/components/home/FaqSection.vue'
import { freeContentHomeBlocks } from '@/config/freeContent'
import { FREE_RESOURCES_AUTHORITY_CONTENT, isKnownBrokenPopularLink } from '@/config/freeResourcesAuthority'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { useZoom } from '@/composables/useZoom'
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { 
  SparklesIcon, 
  CheckCircleIcon, 
  ArrowRightIcon,
  BookOpenIcon,
  AcademicCapIcon,
  DocumentTextIcon
} from '@heroicons/vue/24/outline'

const { openModal } = useModalManager()
const hubAuthorityContent = FREE_RESOURCES_AUTHORITY_CONTENT.hub
const hubPopularLinks = computed(() =>
  hubAuthorityContent.popularLinks.filter((link) => !isKnownBrokenPopularLink(link?.href))
)

// --- Mobile/desktop zoom (même logique que Home/About) ---
const freeResourcesContentRef = ref(null)

function computeFreeResourcesHomeZoom(width) {
  if (width >= 1400) return 1
  if (width >= 1200) return 0.95
  if (width >= 1024) return 0.9
  if (width >= 900) return 0.85
  if (width >= 768) return 0.8
  if (width >= 640) return 0.72
  if (width >= 520) return 0.68
  if (width >= 420) return 0.64
  if (width >= 360) return 0.6
  return 0.55
}

const {
  detectMobileAndZoomSupport,
  createZoomStyle,
  updateViewportWidth,
  measureContentHeight,
  setupViewportListener,
  cleanupViewportListener
} = useZoom({ computeAutoZoom: computeFreeResourcesHomeZoom })

const freeResourcesZoomStyle = createZoomStyle({
  cssVar: '--free-resources-zoom',
  heightVar: '--free-resources-content-height',
  mobileZoomAdjustment: (z) => z
})

let freeResourcesResizeObserver = null
const measureFreeResourcesHeight = () => {
  measureContentHeight(freeResourcesContentRef)
}

const handleViewportChange = async () => {
  updateViewportWidth()
  await nextTick()
  measureFreeResourcesHeight()
}

const handleResize = () => {
  void handleViewportChange()
}

const handleOrientationChange = () => {
  setTimeout(() => {
    void handleViewportChange()
  }, 200)
}

onMounted(async () => {
  detectMobileAndZoomSupport()
  setupViewportListener()

  await nextTick()
  measureFreeResourcesHeight()

  if (typeof window !== 'undefined') {
    window.addEventListener('resize', handleResize, { passive: true })
    window.addEventListener('orientationchange', handleOrientationChange, { passive: true })

    setTimeout(measureFreeResourcesHeight, 250)

    if (window.ResizeObserver && freeResourcesContentRef.value) {
      freeResourcesResizeObserver = new ResizeObserver(() => {
        measureFreeResourcesHeight()
      })
      freeResourcesResizeObserver.observe(freeResourcesContentRef.value)
    }
  }
})

onUnmounted(() => {
  cleanupViewportListener()
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', handleResize)
    window.removeEventListener('orientationchange', handleOrientationChange)
  }
  freeResourcesResizeObserver?.disconnect?.()
  freeResourcesResizeObserver = null
})

const getIcon = (type) => {
  const icons = {
    course: BookOpenIcon,
    exercise: AcademicCapIcon,
    summary: DocumentTextIcon
  }
  return icons[type] || BookOpenIcon
}

const openSubscriptionModal = () => {
  openModal(MODAL_IDS.REGISTER)
}
</script>

<style scoped>
.free-resources-home-zoom {
  width: 100%;
  overflow-x: hidden;
  overflow-y: visible;
}

.free-resources-home {
  background: #ffffff;
  min-height: 100vh;
}

/* Hero Section */
.hero-section {
  padding: 80px 20px 60px;
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
  text-align: center;
}

.hero-container {
  max-width: 800px;
  margin: 0 auto;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #ecfdf5;
  border: 1px solid #10b981;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 600;
  color: #047857;
  margin-bottom: 24px;
}

.badge-icon {
  width: 18px;
  height: 18px;
  color: #10b981;
}

.hero-title {
  font-size: clamp(28px, 5vw, 42px);
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 16px 0;
  line-height: 1.2;
}

.hero-title .highlight {
  color: #2563eb;
}

.hero-subtitle {
  font-size: 1.1rem;
  color: #64748b;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
}

.authority-intro {
  padding: 8px 20px 10px;
}

.authority-container {
  max-width: 1040px;
  margin: 0 auto;
}

.authority-title {
  margin: 0 0 14px 0;
  font-size: clamp(22px, 3vw, 30px);
  font-weight: 800;
  color: #0f172a;
  line-height: 1.2;
}

.authority-paragraph {
  margin: 0 0 16px 0;
  font-size: 1rem;
  line-height: 1.72;
  color: #334155;
}

.authority-paragraph:last-child {
  margin-bottom: 0;
}

/* Cards Section */
.cards-section {
  padding: 40px 20px 80px;
}

.cards-container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.resource-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.resource-card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  transform: translateY(-4px);
}

.card-link {
  display: flex;
  flex-direction: column;
  padding: 28px;
  text-decoration: none;
  color: inherit;
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.badge {
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-course {
  background: #eff6ff;
  color: #2563eb;
  border: 1px solid #bfdbfe;
}

.badge-exercise {
  background: #ecfdf5;
  color: #10b981;
  border: 1px solid #a7f3d0;
}

.badge-summary {
  background: #fef3f2;
  color: #ef4444;
  border: 1px solid #fecaca;
}

.card-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  border-radius: 12px;
  color: #64748b;
}

.card-icon svg {
  width: 24px;
  height: 24px;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 8px 0;
}

.card-highlight {
  font-size: 0.85rem;
  font-weight: 600;
  color: #2563eb;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 12px 0;
}

.card-description {
  font-size: 0.95rem;
  color: #64748b;
  line-height: 1.5;
  margin: 0 0 20px 0;
}

.features-list {
  list-style: none;
  padding: 0;
  margin: 0 0 24px 0;
  flex-grow: 1;
}

.features-list li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 0.9rem;
  color: #334155;
  margin-bottom: 10px;
  line-height: 1.4;
}

.check-icon {
  width: 18px;
  height: 18px;
  color: #10b981;
  flex-shrink: 0;
  margin-top: 1px;
}

.explore-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: #0f172a;
  color: #ffffff;
  font-weight: 600;
  font-size: 0.95rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  width: 100%;
  justify-content: center;
}

.resource-card:hover .explore-btn {
  background: #1e293b;
}

.arrow-icon {
  width: 18px;
  height: 18px;
}

.popular-links {
  padding: 0 20px 44px;
}

.popular-links__container {
  max-width: 1040px;
  margin: 0 auto;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  border-radius: 16px;
  padding: 24px;
}

.popular-links__title {
  margin: 0 0 14px 0;
  font-size: 1.2rem;
  font-weight: 800;
  color: #0f172a;
}

.popular-links__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 10px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.popular-links__item {
  margin: 0;
}

.popular-links__anchor {
  display: inline-flex;
  width: 100%;
  color: #1d4ed8;
  font-weight: 600;
  line-height: 1.5;
  text-decoration: none;
}

.popular-links__anchor:hover {
  text-decoration: underline;
}

/* CTA Section */
.cta-section {
  padding: 60px 20px;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
}

.cta-container {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

.cta-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 8px 0;
}

.cta-desc {
  font-size: 1rem;
  color: #64748b;
  margin: 0 0 24px 0;
}

.cta-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-primary {
  background: #2563eb;
  color: #ffffff;
  font-weight: 600;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  padding: 14px 28px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cta-primary:hover {
  background: #1d4ed8;
}

.cta-secondary {
  background: #ffffff;
  color: #2563eb;
  font-weight: 600;
  font-size: 1rem;
  border: 1px solid #2563eb;
  border-radius: 8px;
  padding: 14px 28px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.cta-secondary:hover {
  background: #eff6ff;
}

/* Responsive */
@media (max-width: 900px) {
  .cards-container {
    grid-template-columns: 1fr;
    max-width: 500px;
  }

  .popular-links__list {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 700px) {
  .hero-section {
    padding-top: 120px;
  }
}

@media (max-width: 600px) {
  .hero-section {
    padding: 120px 16px 40px;
  }
  
  .cards-section {
    padding: 24px 16px 60px;
  }

  .authority-intro {
    padding: 10px 16px 14px;
  }

  .popular-links {
    padding: 0 16px 36px;
  }
  
  .card-link {
    padding: 24px;
  }
  
  .cta-section {
    padding: 48px 16px;
  }
  
  .cta-buttons {
    flex-direction: column;
    align-items: stretch;
  }
  
  .cta-primary,
  .cta-secondary {
    width: 100%;
  }
}
</style>
