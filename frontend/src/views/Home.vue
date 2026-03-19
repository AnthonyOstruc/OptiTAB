<script setup>
// Importation des composants principaux de la page d'accueil
import SectionHero from '@/components/home/SectionHero.vue'
import SubjectsSection from '@/components/home/SubjectsSection.vue'
import IntroFeaturesSection from '@/components/home/IntroFeaturesSection.vue'
import DemoSection from '@/components/home/DemoSection.vue'
import WhySubscribeSection from '@/components/home/WhySubscribeSection.vue'
import PricingPlans from '@/components/home/PricingPlans.vue'
import FaqSection from '@/components/home/FaqSection.vue'
import NewsletterSection from '@/components/home/NewsletterSection.vue'
import PricingSection from '@/components/home/PricingSection.vue'
import WhatsappChatButton from '@/components/home/WhatsappChatButton.vue'
import HomeSeoSection from '@/components/home/HomeSeoSection.vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getMatieres } from '@/api'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { useZoom } from '@/composables/useZoom'

// Importation du contenu dynamique depuis la configuration centrale
import {
  sectionHero,
  titreSujets,
  // sujets, // supprimé, tout est dynamique
  liensPiedDePage,
  introPiedDePage,
  contactsPiedDePage,
  introFeatures,
  etapesParcours,
  faq,
  newsletterSection,
  pricingPlans
} from '@/config/homeContent.js'

const matieres = ref([])
const router = useRouter()
const { openModal } = useModalManager()

// Référence pour le contenu avec zoom
const homeContentRef = ref(null)

function computeHomeZoom(width) {
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
  contentHeight,
  zoomLevel,
  supportsNativeZoom,
  detectMobileAndZoomSupport,
  createZoomStyle,
  updateViewportWidth,
  measureContentHeight,
  setupViewportListener,
  cleanupViewportListener
} = useZoom({ computeAutoZoom: computeHomeZoom })

const baseHomeZoomStyle = createZoomStyle({
  cssVar: '--home-zoom',
  heightVar: '--home-content-height',
  mobileZoomAdjustment: (z) => z
})

// En mode mobile (transform: scale), la hauteur calculée peut être sous-estimée sur certains navigateurs,
// ce qui bloque le scroll. On laisse la hauteur "auto" (donc toujours scrollable) et on compense via
// une marge négative pour éviter un grand espace vide.
const homeZoomStyle = computed(() => {
  const style = baseHomeZoomStyle.value
  if (supportsNativeZoom.value) return style

  const z = Number(zoomLevel.value || 1)
  if (!contentHeight.value || !Number.isFinite(z) || z >= 1) {
    return { ...style, height: 'auto', minHeight: 'auto', marginBottom: '' }
  }

  const marginBottom = -Math.round(contentHeight.value * (1 - z))
  return { ...style, height: 'auto', minHeight: 'auto', marginBottom: `${marginBottom}px` }
})

let homeResizeObserver = null
const measureHomeContentHeight = () => {
  measureContentHeight(homeContentRef)
}

const handleViewportChange = async () => {
  updateViewportWidth()
  await nextTick()
  measureHomeContentHeight()
}

const handleResize = () => {
  void handleViewportChange()
}

const handleOrientationChange = () => {
  setTimeout(() => {
    void handleViewportChange()
  }, 200)
}

// Système de zoom JavaScript comme fallback pour mobile
const legacyZoomLevel = ref(1)

function calculateZoom() {
  if (typeof window === 'undefined') return 1
  const width = window.innerWidth
  if (width >= 1400) return 1
  if (width >= 1200) return 0.95
  if (width >= 1024) return 0.9
  if (width >= 900) return 0.85
  if (width >= 768) return 0.8
  if (width >= 640) return 0.72
  if (width >= 520) return 0.68
  if (width >= 420) return 0.64
  if (width >= 360) return 0.60
  return 0.55
}

function applyMobileZoom() {
  if (!homeContentRef.value) return
  const zoom = calculateZoom()
  legacyZoomLevel.value = zoom
  
  // Appliquer le zoom directement via style inline
  // Ceci surcharge tout CSS et fonctionne sur tous les navigateurs
  const el = homeContentRef.value
  
  // Vérifier si le navigateur supporte CSS zoom
  const supportsZoom = 'zoom' in document.body.style
  
  if (supportsZoom) {
    el.style.zoom = zoom
    el.style.transform = ''
    el.style.width = ''
  } else {
    // Fallback pour Firefox
    el.style.zoom = ''
    el.style.transform = `scale(${zoom})`
    el.style.transformOrigin = 'top left'
    el.style.width = `${(100 / zoom).toFixed(2)}%`
  }
}

// Handler pour la sélection d'une matière
const handleSubjectSelected = (subject) => {
  console.log('Matière sélectionnée:', subject)
  // Rediriger vers la page des cours particuliers en haut de la page
  router.push({ name: 'CoursParticuliers' }).then(() => {
    // S'assurer que la page est en haut après la navigation
    window.scrollTo({ top: 0, behavior: 'smooth' })
  })
}

// Handler pour le bouton CTA principal (Créer mon compte gratuit)
const handleCtaMain = () => {
  openModal(MODAL_IDS.REGISTER)
}

// Handler pour le bouton CTA secondaire (Voir la plateforme en action)
const handleCtaSecondary = () => {
  const demoGifs = document.getElementById('demo-gifs')
  if (demoGifs) {
    demoGifs.scrollIntoView({ behavior: 'smooth', block: 'center' })
    return
  }

  const demoSection = document.getElementById('demo')
  if (demoSection) {
    demoSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

// Handler pour le bouton CTA principal des étapes (Je m'abonne maintenant)
const handleStepsCtaMain = () => {
  // Ouvrir le modal d'inscription
  openModal(MODAL_IDS.REGISTER)
}

// Handler pour le bouton CTA secondaire des étapes (Voir les tarifs)
const handleStepsCtaSecondary = () => {
  // Scroller vers la section tarifs dans la même page
  const tarifsSection = document.getElementById('tarifs')
  if (tarifsSection) {
    tarifsSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
  } else {
    // Fallback vers la section des fonctionnalités si tarifs n'existe pas
    setTimeout(() => {
      const featuresSection = document.querySelector('.intro-features-section')
      if (featuresSection) {
        featuresSection.scrollIntoView({ behavior: 'smooth' })
      }
    }, 100) // Petit délai pour s'assurer que la page est chargée
  }
}

// Handler pour le bouton principal de la section démo (S'abonner)
const handleDemoSubscribe = () => {
  // Ouvrir le modal d'inscription
  openModal(MODAL_IDS.REGISTER)
}

// Handler pour le bouton secondaire de la section démo (Voir les tarifs)
const handleDemoPricing = () => {
  // Scroller vers la section tarifs dans la même page
  const tarifsSection = document.getElementById('tarifs')
  if (tarifsSection) {
    tarifsSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

// Handlers pour la section "Pourquoi s'abonner"
const handleExploreFree = () => {
  router.push({ name: 'FreeResourcesHome' })
}

const handleCreateAccount = () => {
  openModal(MODAL_IDS.REGISTER)
}

const handleWhySubscribe = () => {
  const tarifsSection = document.getElementById('tarifs')
  if (tarifsSection) {
    tarifsSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

// Handlers pour la section "Débloquer les bénéfices"
const handleUnlockSubscribe = () => {
  openModal(MODAL_IDS.REGISTER)
}

const handleSeePricing = () => {
  const tarifsSection = document.getElementById('tarifs')
  if (tarifsSection) {
    tarifsSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

onMounted(async () => {
  detectMobileAndZoomSupport()
  setupViewportListener()
  try {
    const { data } = await getMatieres()
    // Afficher uniquement les matières autorisées pour la vitrine
    // Par défaut (champ absent), on considère visible
    matieres.value = (data || []).filter(m => m && m.show_on_home !== false)
  } catch (e) {
    matieres.value = []
  }
  
  // Appliquer le zoom JavaScript immédiatement
  await nextTick()
  measureHomeContentHeight()
  if (typeof window !== 'undefined') {
    // Petit délai pour s'assurer que le DOM est prêt
    setTimeout(() => {
      handleResize()
    }, 50)
    
    // Réappliquer lors du redimensionnement
    window.addEventListener('resize', handleResize, { passive: true })
    
    // Réappliquer lors du changement d'orientation
    window.addEventListener('orientationchange', handleOrientationChange, { passive: true })

    setTimeout(measureHomeContentHeight, 250)

    if (window.ResizeObserver && homeContentRef.value) {
      homeResizeObserver = new ResizeObserver(() => {
        measureHomeContentHeight()
      })
      homeResizeObserver.observe(homeContentRef.value)
    }
  }
})

onUnmounted(() => {
  cleanupViewportListener()
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', handleResize)
    window.removeEventListener('orientationchange', handleOrientationChange)
  }
  homeResizeObserver?.disconnect?.()
  homeResizeObserver = null
})

// --- FIN LOGIQUE JS ---
</script>

<template>
  <MainLayout>
    <div class="home-content-zoom" :style="homeZoomStyle">
      <div class="home-content-inner" ref="homeContentRef">
      <!-- Section Hero (accroche principale) -->
      <SectionHero
        :titre="sectionHero.titre"
        :sous-titre="sectionHero.sousTitre"
        :sous-titre2="sectionHero.sousTitre2"
        :mini-line="sectionHero.miniLine"
        :image="sectionHero.image"
        :image-alt="sectionHero.imageAlt"
        :show-image="sectionHero.showImage"
        :highlight="sectionHero.highlight"
        :micro-benefits="sectionHero.microBenefits"
        :reassurance="sectionHero.reassurance"
        :cta-text="sectionHero.ctaText"
        :cta-hint="sectionHero.ctaHint"
        :cta-secondary="sectionHero.ctaSecondary"
        :cta-secondary-hint="sectionHero.ctaSecondaryHint"
        :bg="sectionHero.bg"
        @cta-main="handleCtaMain"
        @cta-secondary="handleCtaSecondary"
      />

      <!-- Texte SEO (services + liens internes) -->
      <HomeSeoSection />

      <!-- Section Démo avec GIFs et CTA d'abonnement -->
      <DemoSection
        @cta-subscribe="handleDemoSubscribe"
        @cta-pricing="handleDemoPricing"
      />

      <!-- Section Intro Features (accroche + grille) -->
      <IntroFeaturesSection
        :titre="introFeatures.titre"
        :highlight="introFeatures.highlight"
        :description="introFeatures.description"
        :features="introFeatures.features"
      />

      <!-- Section Pourquoi S'abonner (comparaison Gratuit / Découverte / Abonnement) -->
      <WhySubscribeSection
        @explore-free="handleExploreFree"
        @create-account="handleCreateAccount"
        @subscribe="handleWhySubscribe"
      />

      <!-- Section Tarifs / Abonnements -->
      <PricingPlans />

      <!-- Section Matières/Sujets -->
      <SubjectsSection
        :titre="titreSujets"
        :sujets="matieres"
        @subject-selected="handleSubjectSelected"
      />

      <!-- Section FAQ -->
      <FaqSection :faq="faq" />

      <!-- Section Newsletter -->
      <NewsletterSection
        :titre="newsletterSection.titre"
        :description="newsletterSection.description"
        :placeholder="newsletterSection.placeholder"
        :bouton="newsletterSection.bouton"
      />
      </div>
    </div>
    <WhatsappChatButton
      phone="33764040251"
      message="Bonjour, j'ai une question sur Optitab !"
      tooltip="Une question ? Discutons sur WhatsApp !"
    />
  </MainLayout>
</template>

<style scoped lang="scss">
.home {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  height: auto;
  overflow-y: auto;
}
</style>

<!-- Styles globaux pour le zoom - pas de scoped pour éviter les problèmes de priorité -->
<style lang="scss">
.home-content-zoom {
  width: 100%;
  overflow-y: visible;
  overflow-x: hidden;
}

.home-content-inner {
  box-sizing: border-box;
  width: 100%;
  overflow-x: hidden;
}

/* Container principal avec zoom automatique via CSS */
.home-content-outer {
  box-sizing: border-box;
  width: 100%;
  overflow-x: hidden;
}

/* 
 * Zoom CSS avec media queries progressifs (du plus petit au plus grand)
 * Approche mobile-first pour une meilleure compatibilité
 */

/* Mobile très petit (< 360px) - zoom 55% */
@media screen and (max-width: 359px) {
  .home-content-outer { 
    zoom: 0.55 !important;
  }
}

/* Mobile petit (360-419px) - zoom 60% */
@media screen and (min-width: 360px) and (max-width: 419px) {
  .home-content-outer { 
    zoom: 0.60 !important;
  }
}

/* Mobile moyen (420-519px) - zoom 64% */
@media screen and (min-width: 420px) and (max-width: 519px) {
  .home-content-outer { 
    zoom: 0.64 !important;
  }
}

/* Mobile large (520-639px) - zoom 68% */
@media screen and (min-width: 520px) and (max-width: 639px) {
  .home-content-outer { 
    zoom: 0.68 !important;
  }
}

/* Tablette portrait (640-767px) - zoom 72% */
@media screen and (min-width: 640px) and (max-width: 767px) {
  .home-content-outer { 
    zoom: 0.72 !important;
  }
}

/* Tablette (768-899px) - zoom 80% */
@media screen and (min-width: 768px) and (max-width: 899px) {
  .home-content-outer { 
    zoom: 0.8 !important;
  }
}

/* Petit desktop (900-1023px) - zoom 85% */
@media screen and (min-width: 900px) and (max-width: 1023px) {
  .home-content-outer { 
    zoom: 0.85 !important;
  }
}

/* Desktop moyen (1024-1199px) - zoom 90% */
@media screen and (min-width: 1024px) and (max-width: 1199px) {
  .home-content-outer { 
    zoom: 0.9 !important;
  }
}

/* Desktop large (1200-1399px) - zoom 95% */
@media screen and (min-width: 1200px) and (max-width: 1399px) {
  .home-content-outer { 
    zoom: 0.95 !important;
  }
}

/* Desktop très large (>= 1400px) - pas de zoom */
@media screen and (min-width: 1400px) {
  .home-content-outer { 
    zoom: 1 !important;
  }
}

/* 
 * Fallback transform pour Firefox (qui ignore zoom)
 */
@supports not (zoom: 1) {
  @media screen and (max-width: 359px) {
    .home-content-outer { 
      transform: scale(0.55); 
      transform-origin: top left; 
      width: 181.82%; 
    }
  }
  @media screen and (min-width: 360px) and (max-width: 419px) {
    .home-content-outer { 
      transform: scale(0.60); 
      transform-origin: top left; 
      width: 166.67%; 
    }
  }
  @media screen and (min-width: 420px) and (max-width: 519px) {
    .home-content-outer { 
      transform: scale(0.64); 
      transform-origin: top left; 
      width: 156.25%; 
    }
  }
  @media screen and (min-width: 520px) and (max-width: 639px) {
    .home-content-outer { 
      transform: scale(0.68); 
      transform-origin: top left; 
      width: 147.06%; 
    }
  }
  @media screen and (min-width: 640px) and (max-width: 767px) {
    .home-content-outer { 
      transform: scale(0.72); 
      transform-origin: top left; 
      width: 138.89%; 
    }
  }
  @media screen and (min-width: 768px) and (max-width: 899px) {
    .home-content-outer { 
      transform: scale(0.8); 
      transform-origin: top left; 
      width: 125%; 
    }
  }
  @media screen and (min-width: 900px) and (max-width: 1023px) {
    .home-content-outer { 
      transform: scale(0.85); 
      transform-origin: top left; 
      width: 117.65%; 
    }
  }
  @media screen and (min-width: 1024px) and (max-width: 1199px) {
    .home-content-outer { 
      transform: scale(0.9); 
      transform-origin: top left; 
      width: 111.11%; 
    }
  }
  @media screen and (min-width: 1200px) and (max-width: 1399px) {
    .home-content-outer { 
      transform: scale(0.95); 
      transform-origin: top left; 
      width: 105.26%; 
    }
  }
}
</style> 
