<script setup>
// Importation des composants principaux de la page d'accueil
import Header from '@/components/layout/Header.vue'
import Footer from '@/components/layout/Footer.vue'
import SectionHero from '@/components/home/SectionHero.vue'
import CallToAction from '@/components/home/CallToAction.vue'
import SubjectsSection from '@/components/home/SubjectsSection.vue'
import FeaturesSection from '@/components/home/FeaturesSection.vue'
import IntroFeaturesSection from '@/components/home/IntroFeaturesSection.vue'
import StepsHowItWorks from '@/components/home/StepsHowItWorks.vue'
import FaqSection from '@/components/home/FaqSection.vue'
import NewsletterSection from '@/components/home/NewsletterSection.vue'
import PricingSection from '@/components/home/PricingSection.vue'
import WhatsappChatButton from '@/components/home/WhatsappChatButton.vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import { ref, onMounted } from 'vue'
import { getMatieres } from '@/api'

// Importation du contenu dynamique depuis la configuration centrale
import {
  sectionHero,
  titreSujets,
  // sujets, // supprimé, tout est dynamique
  liensPiedDePage,
  introPiedDePage,
  contactsPiedDePage,
  titreFonctionnalites,
  fonctionnalites,
  introFeatures,
  etapesParcours,
  faq,
  newsletterSection,
  pricingPlans
} from '@/config/homeContent.js'

const matieres = ref([])

// Handler pour la sélection d'une matière
const handleSubjectSelected = (subject) => {
  console.log('Matière sélectionnée:', subject)
  alert(`Matière "${subject.nom}" sélectionnée !`)
}

onMounted(async () => {
  try {
    const { data } = await getMatieres()
    matieres.value = data
  } catch (e) {
    matieres.value = []
  }
})

// --- FIN LOGIQUE JS ---
</script>

<template>
  <MainLayout>
    <!-- Section Hero (accroche principale) -->
    <SectionHero
      :titre="sectionHero.titre"
      :sous-titre="sectionHero.sousTitre"
      :image="sectionHero.image"
      :highlight="sectionHero.highlight"
      :message-parents="sectionHero.messageParents"
      :cta-text="sectionHero.ctaText"
      :cta-secondary="sectionHero.ctaSecondary"
    />


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
    />


    <!-- Section Fonctionnalités clés -->
    <FeaturesSection
      :titre="titreFonctionnalites"
      :fonctionnalites="fonctionnalites"
    />

    <!-- Section Matières/Sujets -->
    <SubjectsSection
      :titre="titreSujets"
      :sujets="matieres"
      @subject-selected="handleSubjectSelected"
    />

    <!-- Section Tarifs / Pricing -->
    <PricingSection
      :titre="pricingPlans.titre"
      :description="pricingPlans.description"
      :plans="pricingPlans.plans"
      :garantie="pricingPlans.garantie"
      :legal="pricingPlans.legal"
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
    <WhatsappChatButton
      phone="33612345678"
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