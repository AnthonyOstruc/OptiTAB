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
import { ref, onMounted } from 'vue'
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

// Référence pour le contenu (utilisé potentiellement pour d'autres fonctionnalités)
const homeContentRef = ref(null)

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
})

// --- FIN LOGIQUE JS ---
</script>

<template>
  <MainLayout>
    <div class="home-content-outer" ref="homeContentRef">
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

/* Container principal avec zoom automatique via CSS */
.home-content-outer {
  box-sizing: border-box;
  width: 100%;
  overflow-x: hidden;
}

/* 
 * Zoom CSS via media queries - fonctionne sur Chrome, Safari, Edge (desktop + mobile)
 * Firefox n'a pas besoin de zoom car il gère mieux le responsive nativement
 */
@supports (zoom: 1) {
  @media (max-width: 1399px) and (min-width: 1200px) {
    .home-content-outer { zoom: 0.95; }
  }
  @media (max-width: 1199px) and (min-width: 1024px) {
    .home-content-outer { zoom: 0.9; }
  }
  @media (max-width: 1023px) and (min-width: 900px) {
    .home-content-outer { zoom: 0.85; }
  }
  @media (max-width: 899px) and (min-width: 768px) {
    .home-content-outer { zoom: 0.8; }
  }
  @media (max-width: 767px) and (min-width: 640px) {
    .home-content-outer { zoom: 0.72; }
  }
  @media (max-width: 639px) and (min-width: 520px) {
    .home-content-outer { zoom: 0.68; }
  }
  @media (max-width: 519px) and (min-width: 420px) {
    .home-content-outer { zoom: 0.64; }
  }
  @media (max-width: 419px) and (min-width: 360px) {
    .home-content-outer { zoom: 0.60; }
  }
  @media (max-width: 359px) {
    .home-content-outer { zoom: 0.55; }
  }
}

/* 
 * Fallback pour Firefox qui ne supporte pas zoom
 * On utilise transform: scale() avec ajustement de width
 */
@supports not (zoom: 1) {
  @media (max-width: 1399px) and (min-width: 1200px) {
    .home-content-outer { 
      transform: scale(0.95); 
      transform-origin: top left; 
      width: calc(100% / 0.95); 
    }
  }
  @media (max-width: 1199px) and (min-width: 1024px) {
    .home-content-outer { 
      transform: scale(0.9); 
      transform-origin: top left; 
      width: calc(100% / 0.9); 
    }
  }
  @media (max-width: 1023px) and (min-width: 900px) {
    .home-content-outer { 
      transform: scale(0.85); 
      transform-origin: top left; 
      width: calc(100% / 0.85); 
    }
  }
  @media (max-width: 899px) and (min-width: 768px) {
    .home-content-outer { 
      transform: scale(0.8); 
      transform-origin: top left; 
      width: calc(100% / 0.8); 
    }
  }
  @media (max-width: 767px) and (min-width: 640px) {
    .home-content-outer { 
      transform: scale(0.72); 
      transform-origin: top left; 
      width: calc(100% / 0.72); 
    }
  }
  @media (max-width: 639px) and (min-width: 520px) {
    .home-content-outer { 
      transform: scale(0.68); 
      transform-origin: top left; 
      width: calc(100% / 0.68); 
    }
  }
  @media (max-width: 519px) and (min-width: 420px) {
    .home-content-outer { 
      transform: scale(0.64); 
      transform-origin: top left; 
      width: calc(100% / 0.64); 
    }
  }
  @media (max-width: 419px) and (min-width: 360px) {
    .home-content-outer { 
      transform: scale(0.60); 
      transform-origin: top left; 
      width: calc(100% / 0.60); 
    }
  }
  @media (max-width: 359px) {
    .home-content-outer { 
      transform: scale(0.55); 
      transform-origin: top left; 
      width: calc(100% / 0.55); 
    }
  }
}
</style> 
