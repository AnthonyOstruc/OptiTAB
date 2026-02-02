<template>
  <MainLayout>
    <div class="tarifs-page">
      <!-- Hero Section -->
      <section class="tarifs-hero">
        <div class="hero-container">
          <h1 class="hero-title">Nos <span class="highlight">Tarifs</span></h1>
          <p class="hero-subtitle">
            Abonnement mensuel sans engagement • Annulable à tout moment
          </p>
        </div>
      </section>

      <!-- Pricing Section -->
      <PricingPlans />

      <!-- FAQ Section -->
      <section class="tarifs-faq">
        <div class="faq-container">
          <h2 class="faq-title">Questions fréquentes</h2>
          
          <div class="faq-list">
            <div v-for="(item, idx) in faqItems" :key="idx" class="faq-item">
              <h3 class="faq-question">{{ item.question }}</h3>
              <p class="faq-answer">{{ item.answer }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <section class="tarifs-cta">
        <div class="cta-container">
          <h3 class="cta-title">Des questions sur les tarifs ?</h3>
          <p class="cta-desc">Notre équipe est disponible pour vous accompagner.</p>
          <router-link to="/contact" class="cta-btn">
            Nous contacter
          </router-link>
        </div>
      </section>
    </div>
  </MainLayout>
</template>

<script setup>
import { useRoute } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import PricingPlans from '@/components/home/PricingPlans.vue'
import { setPageSeo, buildFaqJsonLd, getRobotsForRoute } from '@/services/seo'

const route = useRoute()

const faqItems = [
  {
    question: 'Puis-je annuler a tout moment ?',
    answer: "Oui, l'abonnement est sans engagement. Vous pouvez annuler quand vous le souhaitez depuis votre espace personnel."
  },
  {
    question: 'Comment fonctionne le paiement ?',
    answer: "Le paiement est securise via Stripe. Vous etes preleve chaque mois a la date d'anniversaire de votre abonnement."
  },
  {
    question: 'Puis-je changer de niveau ?',
    answer: 'Oui, vous pouvez changer de niveau a tout moment depuis votre espace abonne.'
  },
  {
    question: "Y a-t-il une periode d'essai ?",
    answer: 'Consultez nos ressources gratuites pour decouvrir la methode OptiTAB avant de vous abonner.'
  }
]

function normalizeBaseUrl(value) {
  let result = value
  while (result.endsWith('/')) {
    result = result.slice(0, -1)
  }
  return result
}

function getSiteUrl() {
  const fromEnv = String((import.meta.env && import.meta.env.VITE_SITE_URL) || '').trim()
  if (fromEnv) return normalizeBaseUrl(fromEnv)
  if (typeof window !== 'undefined' && window.location && window.location.origin) {
    return window.location.origin
  }
  return 'https://optitab.net'
}

function toAbsoluteUrl(path) {
  const raw = String(path || '').trim()
  if (!raw) return ''
  if (raw.startsWith('http://') || raw.startsWith('https://')) return raw
  const base = getSiteUrl()
  return `${base}${raw.startsWith('/') ? '' : '/'}${raw}`
}

const title = 'Tarifs OptiTAB : abonnement maths en ligne'
const description =
  'Tarifs OptiTAB : abonnement mensuel sans engagement pour acceder aux cours, exercices corriges et fiches de synthese. Paiement securise, annulation a tout moment.'
const faqGraph = buildFaqJsonLd(faqItems)
const jsonLdGraph = [
  {
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Accueil', item: toAbsoluteUrl('/') },
      { '@type': 'ListItem', position: 2, name: 'Tarifs', item: toAbsoluteUrl('/tarifs') }
    ]
  },
  ...(faqGraph ? [faqGraph] : [])
]

setPageSeo({
  title,
  description,
  canonicalPath: '/tarifs',
  robots: getRobotsForRoute({ route }),
  ogType: 'website',
  jsonLdGraph
})
</script>

<style scoped>
.tarifs-page {
  background: #ffffff;
  min-height: 100vh;
}

/* Hero Section */
.tarifs-hero {
  padding: 80px 20px 40px;
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
  text-align: center;
}

.hero-container {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: clamp(28px, 5vw, 42px);
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 12px 0;
  line-height: 1.2;
}

.hero-title .highlight {
  color: #2563eb;
}

.hero-subtitle {
  font-size: 1.1rem;
  color: #64748b;
  margin: 0;
}

/* FAQ Section */
.tarifs-faq {
  padding: 60px 20px;
  background: #f8fafc;
}

.faq-container {
  max-width: 800px;
  margin: 0 auto;
}

.faq-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #0f172a;
  text-align: center;
  margin: 0 0 40px 0;
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.faq-item {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
}

.faq-question {
  font-size: 1.05rem;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 8px 0;
}

.faq-answer {
  font-size: 0.95rem;
  color: #64748b;
  line-height: 1.6;
  margin: 0;
}

/* CTA Section */
.tarifs-cta {
  padding: 60px 20px;
  background: #ffffff;
  border-top: 1px solid #e2e8f0;
}

.cta-container {
  max-width: 500px;
  margin: 0 auto;
  text-align: center;
}

.cta-title {
  font-size: 1.35rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 8px 0;
}

.cta-desc {
  font-size: 1rem;
  color: #64748b;
  margin: 0 0 24px 0;
}

.cta-btn {
  display: inline-block;
  background: #2563eb;
  color: #ffffff;
  font-weight: 600;
  font-size: 1rem;
  border-radius: 8px;
  padding: 14px 32px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.cta-btn:hover {
  background: #1d4ed8;
}

/* Responsive */
@media (max-width: 600px) {
  .tarifs-hero {
    padding: 60px 16px 32px;
  }
  
  .tarifs-faq {
    padding: 48px 16px;
  }
  
  .faq-item {
    padding: 20px;
  }
  
  .tarifs-cta {
    padding: 48px 16px;
  }
}
</style>
