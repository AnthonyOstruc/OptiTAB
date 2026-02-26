<template>
  <MainLayout>
    <main class="free-course-page">
      <div class="header-row">
        <BackButton
          text="Retour a l'accueil"
          :custom-action="() => router.push({ name: 'Home' })"
          position="top-left"
        />
        <div class="resource-count-badge">3 formats gratuits</div>
      </div>

      <header class="page-intro" aria-labelledby="free-resources-title">
        <h1 id="free-resources-title" class="page-title">Ressources gratuites de maths</h1>
        <p class="page-subtitle">
          Cours, exercices corriges et fiches de synthese pour college, lycee et prepa.
        </p>
      </header>

      <section class="top-actions-section" aria-label="Formats de ressources">
        <TopActionCards
          :cards="actionCards"
          description="Comprendre, t'entrainer ou reviser vite: clique sur le format qui te fait progresser tout de suite."
        />
      </section>

      <section v-if="hubPopularLinks.length > 0" class="popular-links-panel" aria-label="Liens populaires ressources gratuites">
        <h2 class="popular-links-panel__title">Liens populaires</h2>
        <ul class="popular-links-panel__list">
          <li v-for="link in hubPopularLinks" :key="link.href" class="popular-links-panel__item">
            <RouterLink :to="link.href" class="popular-links-panel__anchor">
              {{ link.label }}
            </RouterLink>
          </li>
        </ul>
      </section>

      <section class="free-resource-cta" aria-label="Acces professeur ou plateforme">
        <div class="free-resource-cta__copy">
          <p class="free-resource-cta__title">Besoin d'un cadre plus complet ?</p>
          <p class="free-resource-cta__subtitle">
            Cours particuliers de maths en ligne ou abonnement OptiTAB.
          </p>
        </div>
        <div class="free-resource-cta__actions">
          <button
            type="button"
            class="free-resource-cta__btn free-resource-cta__btn--primary"
            @click="openSubscriptionModal"
          >
            Creer un compte gratuit
          </button>
          <RouterLink to="/#tarifs" class="free-resource-cta__btn free-resource-cta__btn--secondary">
            Voir les tarifs
          </RouterLink>
        </div>
      </section>

      <section class="seo-copy-block" aria-label="Explications detaillees">
        <SeoAccordion
          title="Pourquoi cette page de ressources gratuites ?"
          summary="Le detail pedagogique est conserve ici pour comprendre la methode complete."
          :sections="seoSections"
        />
      </section>

      <section class="list-faq-section" aria-label="Questions frequentes">
        <FaqAccordion
          :items="hubAuthorityContent.faq"
          title="FAQ ressources gratuites"
          description="Reponses rapides pour demarrer sans perdre de temps."
        />
      </section>
    </main>
  </MainLayout>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import BackButton from '@/components/common/BackButton.vue'
import TopActionCards from '@/components/free-content/TopActionCards.vue'
import SeoAccordion from '@/components/free-content/SeoAccordion.vue'
import FaqAccordion from '@/components/free-content/FaqAccordion.vue'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { FREE_RESOURCES_AUTHORITY_CONTENT, isKnownBrokenPopularLink } from '@/config/freeResourcesAuthority'
import { FREE_RESOURCES_ACTION_CARDS, FREE_RESOURCES_SEO_SECTION_TITLES } from '@/config/freeResourcesUx'

const router = useRouter()
const { openModal } = useModalManager()
const hubAuthorityContent = FREE_RESOURCES_AUTHORITY_CONTENT.hub
const actionCards = FREE_RESOURCES_ACTION_CARDS

const hubPopularLinks = computed(() =>
  hubAuthorityContent.popularLinks.filter((link) => !isKnownBrokenPopularLink(link?.href))
)

const seoSections = computed(() => {
  const paragraphs = Array.isArray(hubAuthorityContent.introParagraphs)
    ? hubAuthorityContent.introParagraphs
    : []

  return paragraphs
    .map((paragraph, index) => ({
      title: FREE_RESOURCES_SEO_SECTION_TITLES[index] || `Section ${index + 1}`,
      paragraphs: [paragraph]
    }))
    .filter((section) => section.paragraphs.length > 0)
})

const openSubscriptionModal = () => {
  openModal(MODAL_IDS.REGISTER)
}
</script>

<style scoped>
.free-course-page {
  min-height: 100vh;
  background: #ffffff;
  padding: 48px 32px 80px;
  max-width: 1200px;
  margin: 0 auto;
}

.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 16px;
}

.resource-count-badge {
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  background: #eef2ff;
  color: #3730a3;
  font-size: 14px;
  font-weight: 700;
  border-radius: 999px;
  border: 1px solid rgba(59, 130, 246, 0.3);
  white-space: nowrap;
}

.page-intro {
  margin: 0 0 14px 0;
  max-width: 980px;
}

.page-title {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 900;
  color: #0f172a;
  letter-spacing: -0.02em;
  line-height: 1.1;
}

.page-subtitle {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: #475569;
  line-height: 1.6;
}

.top-actions-section {
  max-width: 980px;
  margin: 0 0 16px 0;
}

.free-resource-cta {
  max-width: 980px;
  margin: 0 0 18px 0;
  padding: 20px;
  border-radius: 18px;
  border: 1px solid rgba(37, 99, 235, 0.24);
  background: linear-gradient(135deg, rgba(239, 246, 255, 0.88), rgba(255, 255, 255, 0.98));
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.free-resource-cta__copy {
  flex: 1 1 380px;
}

.free-resource-cta__title {
  margin: 0 0 6px 0;
  font-size: 20px;
  font-weight: 900;
  color: #0f172a;
  line-height: 1.2;
}

.free-resource-cta__subtitle {
  margin: 0;
  font-size: 14px;
  color: #475569;
  line-height: 1.6;
}

.free-resource-cta__actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  flex: 0 0 auto;
  margin-left: auto;
  flex-wrap: wrap;
}

.free-resource-cta__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  padding: 10px 16px;
  font-size: 13px;
  font-weight: 800;
  text-decoration: none;
  border: none;
  cursor: pointer;
  line-height: 1.2;
  white-space: nowrap;
}

.free-resource-cta__btn--primary {
  color: #ffffff;
  background: #2563eb;
}

.free-resource-cta__btn--primary:hover {
  background: #1d4ed8;
}

.free-resource-cta__btn--secondary {
  color: #1d4ed8;
  background: #ffffff;
  border: 1px solid rgba(37, 99, 235, 0.28);
}

.free-resource-cta__btn--secondary:hover {
  background: #eff6ff;
}

.popular-links-panel {
  max-width: 980px;
  margin: 0 0 18px 0;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  background: #f8fafc;
  padding: 18px 20px;
}

.popular-links-panel__title {
  margin: 0 0 10px 0;
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
}

.popular-links-panel__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px 14px;
}

.popular-links-panel__anchor {
  color: #1d4ed8;
  font-weight: 600;
  line-height: 1.45;
  text-decoration: none;
}

.popular-links-panel__anchor:hover {
  text-decoration: underline;
}

.seo-copy-block {
  max-width: 980px;
  margin: 12px 0 0 0;
}

.list-faq-section {
  max-width: 980px;
  margin-top: 12px;
}

@media (max-width: 900px) {
  .popular-links-panel__list {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 700px) {
  .free-course-page {
    padding: 120px 16px 64px;
  }

  .resource-count-badge {
    font-size: 12px;
    padding: 6px 12px;
  }

  .free-resource-cta {
    padding: 16px;
  }

  .free-resource-cta__actions {
    width: 100%;
    margin-left: 0;
  }

  .free-resource-cta__btn {
    width: 100%;
    text-align: center;
  }
}
</style>
