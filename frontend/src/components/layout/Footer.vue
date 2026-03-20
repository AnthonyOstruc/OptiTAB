<template>
  <footer :class="['footer', { 'footer--minimal': isMinimalVariant }]">
    <template v-if="isMinimalVariant">
      <div class="footer-minimal-inner">
        <div class="footer-minimal-top">
          <p class="footer-minimal-brand">OptiTAB</p>
          <p class="footer-minimal-copy">Cours clairs, fiches de synthèse, exercices corrigés pas à pas.</p>
        </div>

        <div class="footer-minimal-contacts">
          <a href="mailto:contact@optitab.net" class="footer-contact">
            <img src="/icons/envelope.svg" alt="Email" />
            contact@optitab.net
          </a>
          <a
            href="https://wa.me/33764040251"
            target="_blank"
            rel="noopener noreferrer"
            class="footer-contact footer-contact--whatsapp"
            data-cta-name="whatsapp"
            data-cta-location="footer"
          >
            <img src="/icons/whatsapp.svg" alt="WhatsApp" />
            WhatsApp
          </a>
        </div>

        <div class="footer-minimal-legal">
          <span class="footer-legal-copyright-text">
            {{ new Date().getFullYear() }} <strong class="footer-copyright-bold">OptiTAB</strong>. Tous droits réservés.
          </span>
          <span class="footer-legal-sep">|</span>
          <template v-for="(link, idx) in legalLinks" :key="link.label">
            <router-link :to="link.href" class="footer-legal-link">{{ link.label }}</router-link>
            <span v-if="idx < legalLinks.length - 1" class="footer-legal-sep">|</span>
          </template>
          <span class="footer-legal-sep">|</span>
          <button type="button" class="footer-legal-link footer-cookie-button" @click="openCookiePreferences">
            Gérer mes cookies
          </button>
        </div>
      </div>
    </template>

    <template v-else>
      <div class="footer-support">
        <h2>Conseillers disponibles 7j/7 - Contactez-nous facilement</h2>
        <p v-if="!isLandingVariant">
          Notre équipe pédagogique est à votre écoute tous les jours, par WhatsApp ou e-mail.<br>
          Posez vos questions, demandez conseil et trouvez la formule qui vous convient.
        </p>
        <div class="footer-contacts">
          <a href="mailto:contact@optitab.net" class="footer-contact">
            <img src="/icons/envelope.svg" alt="Email" />
            contact@optitab.net
          </a>
          <a
            href="https://wa.me/33764040251"
            target="_blank"
            rel="noopener noreferrer"
            class="footer-contact"
            data-cta-name="whatsapp"
            data-cta-location="footer"
          >
            <img src="/icons/whatsapp.svg" alt="WhatsApp" />
            07 64 04 02 51
          </a>
        </div>
      </div>

      <div class="footer-legal-separator"></div>

      <div class="footer-nav-row">
        <span class="footer-legal-copyright-text">
          {{ new Date().getFullYear() }} <strong class="footer-copyright-bold">OptiTAB</strong>. Tous droits réservés.
        </span>
        <template v-if="!isLandingVariant">
          <span class="footer-legal-sep">|</span>
          <template v-for="(link, idx) in navLinks" :key="link.label">
            <router-link :to="link.href" class="footer-legal-link">{{ link.label }}</router-link>
            <span v-if="idx < navLinks.length - 1" class="footer-legal-sep">|</span>
          </template>
          <span class="footer-legal-sep">|</span>
          <GoogleReviewsCompact class="footer-size" />
        </template>
      </div>

      <div class="footer-legal-row">
        <template v-for="(link, idx) in legalLinks" :key="link.label">
          <router-link :to="link.href" class="footer-legal-link">{{ link.label }}</router-link>
          <span v-if="idx < legalLinks.length - 1" class="footer-legal-sep">|</span>
        </template>
        <span class="footer-legal-sep">|</span>
        <button type="button" class="footer-legal-link footer-cookie-button" @click="openCookiePreferences">
          Gérer mes cookies
        </button>
      </div>
    </template>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
import { footerLinks } from '@/config/footerContent.js'
import GoogleReviewsCompact from '@/components/home/GoogleReviewsCompact.vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'default'
  }
})

const isMinimalVariant = computed(() => props.variant === 'minimal')
const isLandingVariant = computed(() => props.variant === 'landing')

const navLinks = footerLinks.filter((link) =>
  ['/cours-particuliers', '/tarifs', '/ressources-gratuites', '/calculator', '/about'].includes(link.href)
)

const legalLinks = footerLinks.filter((link) =>
  ['/legal', '/confidentialite', '/cookies', '/cgu', '/cgv'].includes(link.href)
)

const openCookiePreferences = () => {
  if (typeof window === 'undefined') return
  window.dispatchEvent(new CustomEvent('open-cookie-preferences'))
}
</script>

<style scoped lang="scss">
.footer {
  background: #4e63c2;
  padding: 24px 0 1.5rem;
  margin-top: 0;
}

.footer--minimal {
  padding: 20px 0;
}

.footer-minimal-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 16px;
  display: grid;
  gap: 14px;
}

.footer-minimal-top {
  display: grid;
  gap: 4px;
}

.footer-minimal-brand {
  margin: 0;
  color: #ffffff;
  font-size: 1.1rem;
  font-weight: 800;
}

.footer-minimal-copy {
  margin: 0;
  color: #e0e6f7;
  font-size: 0.9rem;
}

.footer-minimal-contacts {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

.footer-minimal-legal {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.4rem;
  row-gap: 0.25rem;
  color: #dbe4ff;
  font-size: 0.8rem;
}

.footer-support {
  max-width: 700px;
  margin: 0 auto 1.5rem;
  color: #fff;
  text-align: center;
  padding: 0 1rem;
}

.footer-support h2 {
  font-size: 1.08rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-align: center;
}

.footer-support p {
  font-size: 0.92rem;
  margin-bottom: 1.1rem;
  color: #e0e6f7;
  line-height: 1.5;
  text-align: center;
}

.footer-contacts {
  display: flex;
  flex-direction: row;
  gap: 2.5rem;
  align-items: center;
  flex-wrap: wrap;
  margin-top: 0.5rem;
  justify-content: center;
}

.footer-contact {
  color: #fff;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 1.05rem;
  transition: color 0.2s;
}

.footer-contact--whatsapp {
  background: rgba(255, 255, 255, 0.12);
  padding: 6px 12px;
  border-radius: 999px;
}

.footer-contact img {
  width: 22px;
  height: 22px;
  filter: brightness(0) invert(1);
}

.footer-contact:hover {
  color: #c7d2fe;
}

.footer-legal-sep {
  margin: 0 0.3em;
  color: #bfc8e6;
  font-size: 1em;
  user-select: none;
}

.footer-legal-link {
  color: #e0e6f7;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
  font-size: 0.85rem;
  white-space: nowrap;
}

.footer-cookie-button {
  background: none;
  border: none;
  padding: 0;
  font: inherit;
  cursor: pointer;
}

.footer-legal-link:hover {
  color: #fff;
  text-decoration: underline;
}

.footer-size {
  color: #fff !important;
}

.footer-nav-row {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin: 1.2rem auto 0.5rem;
  font-size: 0.85rem;
  color: #e0e6f7;
  row-gap: 0.2rem;
}

.footer-legal-row {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin: 0 auto 0.7rem;
  font-size: 0.8rem;
  color: #c7d2fe;
  row-gap: 0.2rem;
}

.footer-legal-copyright-text {
  color: #e0e6f7;
  font-size: 0.85rem;
  font-weight: 500;
  white-space: nowrap;
}

.footer-legal-separator {
  width: 100%;
  max-width: 900px;
  margin: 1.2rem auto 0.7rem;
  border-top: 1.5px solid #bfc8e6;
  opacity: 0.7;
}

.footer-copyright-bold {
  font-weight: 700;
}

@media (max-width: 768px) {
  .footer {
    padding-bottom: 2.5rem;
    padding-bottom: calc(2.5rem + env(safe-area-inset-bottom));
  }
}

@media (max-width: 700px) {
  .footer-contacts {
    justify-content: center;
    gap: 1rem;
  }

  .footer-nav-row,
  .footer-legal-row,
  .footer-minimal-legal {
    justify-content: center;
    text-align: center;
    padding: 0 0.75rem;
  }

  .footer-legal-link,
  .footer-legal-copyright-text {
    font-size: 0.78rem;
  }
}
</style>
