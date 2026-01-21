<script setup>
// Importation des composants principaux de la page d'accueil
import Header from '@/components/layout/Header.vue'
import Footer from '@/components/layout/Footer.vue'
import SectionHero from '@/components/home/SectionHero.vue'
import SubjectsSection from '@/components/home/SubjectsSection.vue'
import IntroFeaturesSection from '@/components/home/IntroFeaturesSection.vue'
import StepsHowItWorks from '@/components/home/StepsHowItWorks.vue'
import DemoSection from '@/components/home/DemoSection.vue'
import FreeContentShowcase from '@/components/home/FreeContentShowcase.vue'
import PricingPlans from '@/components/home/PricingPlans.vue'
import FaqSection from '@/components/home/FaqSection.vue'
import NewsletterSection from '@/components/home/NewsletterSection.vue'
import PricingSection from '@/components/home/PricingSection.vue'
import WhatsappChatButton from '@/components/home/WhatsappChatButton.vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import { ref, onMounted, onUnmounted, computed, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { getMatieres } from '@/api'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'

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
  pricingPlans,
  freeContentHomeBlocks
} from '@/config/homeContent.js'

const matieres = ref([])
const router = useRouter()
const { openModal } = useModalManager()

// Système de zoom automatique pour mobile (comme Cours.vue)
// Utiliser documentElement.clientWidth comme fallback fiable sur mobile
function getViewportWidth() {
  if (typeof window === 'undefined') return 1920
  // Sur mobile, window.innerWidth peut inclure les scrollbars
  // documentElement.clientWidth est plus fiable pour la largeur visible
  return Math.min(
    window.innerWidth || 1920,
    document.documentElement.clientWidth || 1920
  )
}

const viewportWidth = ref(getViewportWidth())
const contentHeight = ref(0)
const homeContentRef = ref(null)

function computeAutoZoom(width) {
  if (width >= 1400) return 1
  if (width >= 1200) return 0.95
  if (width >= 1024) return 0.9
  if (width >= 900) return 0.85
  if (width >= 768) return 0.8
  if (width >= 640) return 0.78
  if (width >= 520) return 0.76
  if (width >= 420) return 0.74
  return 0.72
}

const zoomLevel = computed(() => computeAutoZoom(viewportWidth.value))

// Détection du support CSS zoom
const supportsZoom = computed(() => {
  if (typeof CSS === 'undefined') return false
  try {
    return CSS.supports('zoom', '1')
  } catch {
    return false
  }
})

const zoomStyle = computed(() => {
  const baseHeight = `${contentHeight.value}px`
  let z = zoomLevel.value || 1
  if (viewportWidth.value <= 768) {
    z = Math.max(0.6, z - 0.08)
  }
  const widthPercent = (100 / z).toFixed(3)
  
  // Si le navigateur supporte zoom (Chrome, Edge, Safari), l'utiliser directement
  // Sinon utiliser transform comme fallback (Firefox)
  if (supportsZoom.value) {
    return {
      '--home-zoom': z,
      '--home-content-height': baseHeight,
      zoom: z
    }
  } else {
    return {
      '--home-zoom': z,
      '--home-content-height': baseHeight,
      transform: `scale(${z})`,
      transformOrigin: 'top left',
      width: `${widthPercent}%`
    }
  }
})

function updateViewportWidth() {
  if (typeof window === 'undefined') return
  viewportWidth.value = getViewportWidth()
  nextTick(() => measureContentHeight())
}

function measureContentHeight() {
  if (homeContentRef.value) {
    contentHeight.value = homeContentRef.value.scrollHeight
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

// Handler pour le bouton CTA principal (Découvrir OptiTAB)
const handleCtaMain = () => {
  // Rediriger vers la page À propos
  window.location.href = '/about'
}

// Handler pour le bouton CTA secondaire (Voir les tarifs)
const handleCtaSecondary = () => {
  // Scroller vers la section tarifs dans la même page
  const tarifsSection = document.getElementById('tarifs')
  if (tarifsSection) {
    tarifsSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
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

onMounted(async () => {
  try {
    const { data } = await getMatieres()
    // Afficher uniquement les matières autorisées pour la vitrine
    // Par défaut (champ absent), on considère visible
    matieres.value = (data || []).filter(m => m && m.show_on_home !== false)
  } catch (e) {
    matieres.value = []
  }
  
  // Initialiser le système de zoom immédiatement
  if (typeof window !== 'undefined') {
    // Forcer la mise à jour initiale du viewport
    viewportWidth.value = getViewportWidth()
    
    // Écouter les changements de taille
    window.addEventListener('resize', updateViewportWidth, { passive: true })
    
    // Écouter aussi les changements d'orientation sur mobile
    window.addEventListener('orientationchange', () => {
      setTimeout(() => {
        viewportWidth.value = getViewportWidth()
        measureContentHeight()
      }, 100)
    }, { passive: true })
    
    // Mesurer la hauteur après le chargement complet
    setTimeout(() => {
      measureContentHeight()
    }, 100)
  }
})

onUnmounted(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', updateViewportWidth)
  }
})

// Watcher pour mesurer la hauteur quand le zoom change
watch(zoomLevel, () => {
  nextTick(() => {
    measureContentHeight()
  })
})

// --- FIN LOGIQUE JS ---
</script>

<template>
  <MainLayout>
    <div class="home-content-outer" :style="zoomStyle" ref="homeContentRef">
      <!-- Section Hero (accroche principale) -->
      <SectionHero
        :titre="sectionHero.titre"
        :sous-titre="sectionHero.sousTitre"
        :image="sectionHero.image"
        :highlight="sectionHero.highlight"
        :message-parents="sectionHero.messageParents"
        :cta-text="sectionHero.ctaText"
        :cta-secondary="sectionHero.ctaSecondary"
        :bg="sectionHero.bg"
        @cta-main="handleCtaMain"
        @cta-secondary="handleCtaSecondary"
      />

      <!-- Section Démo avec GIFs et CTA d'abonnement -->
      <DemoSection
        @cta-subscribe="handleDemoSubscribe"
        @cta-pricing="handleDemoPricing"
      />

      <!-- Bloc de ressources gratuites -->
      <FreeContentShowcase :items="freeContentHomeBlocks" />

      <!-- Section Intro Features (accroche + grille) -->
      <IntroFeaturesSection
        :titre="introFeatures.titre"
        :highlight="introFeatures.highlight"
        :description="introFeatures.description"
        :features="introFeatures.features"
      />

      <!-- Section Steps How It Works -->
      <StepsHowItWorks
        :titre="etapesParcours.titre"
        :highlight="etapesParcours.highlight"
        :titre-fin="etapesParcours.titreFin"
        :description="etapesParcours.description"
        :etapes="etapesParcours.etapes"
        :cta-text="etapesParcours.ctaText"
        :cta-secondary="etapesParcours.ctaSecondary"
        :cta-top="etapesParcours.ctaTop"
        :titre-bas="etapesParcours.titreBas"
        @cta-main="handleStepsCtaMain"
        @cta-secondary="handleStepsCtaSecondary"
      />

      <!-- Section Matières/Sujets -->
      <SubjectsSection
        :titre="titreSujets"
        :sujets="matieres"
        @subject-selected="handleSubjectSelected"
      />

      <!-- Section Tarifs / Abonnements -->
      <PricingPlans />

      <!-- Section FAQ -->
      <FaqSection :faq="faq" />

      <!-- Section Newsletter -->
      <NewsletterSection
        :titre="newsletterSection.titre"
        :description="newsletterSection.description"
        :placeholder="newsletterSection.placeholder"
        :bouton="newsletterSection.bouton"
      />
      <WhatsappChatButton
        phone="33764040251"
        message="Bonjour, j'ai une question sur Optitab !"
        tooltip="Une question ? Discutons sur WhatsApp !"
      />
    </div>
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

/* Container pour le zoom automatique sur mobile */
.home-content-outer {
  overflow-x: hidden;
  width: 100%;
  box-sizing: border-box;
  /* Le zoom/transform est appliqué via JavaScript inline style pour une meilleure compatibilité mobile */
}
</style> 
