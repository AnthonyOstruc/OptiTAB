<template>
  <VitrineLayout>
    <!-- 1. Accroche + moyens de contact, du plus rapide au plus formel -->
    <section class="vt-page-hero ct-hero">
      <div class="vt-container">
        <h1 class="ct-hero__h1">
          <span class="vt-kicker ct-hero__kicker">Contact</span>
          <span class="vt-sr-only"> – </span>
          <span class="vt-page-hero__title">Une question&nbsp;? <em>Parlons-en.</em></span>
        </h1>
        <p class="vt-page-hero__lead">
          Élève, parent ou futur abonné&nbsp;: nous répondons à toutes les demandes sous 24&nbsp;h, 7&nbsp;jours sur&nbsp;7, et
          souvent bien plus vite sur WhatsApp.
        </p>

        <div class="ct-channels">
          <a
            :href="whatsappUrl"
            target="_blank"
            rel="noopener noreferrer"
            class="vt-card ct-channel ct-channel--whatsapp"
            data-cta-name="whatsapp"
            data-cta-location="contact"
          >
            <span class="ct-channel__icon"><img src="/icons/whatsapp.svg" alt="" width="24" height="24" /></span>
            <span class="ct-channel__body">
              <span class="ct-channel__tag">Le plus rapide</span>
              <strong>WhatsApp</strong>
              <span>{{ vitrineContact.whatsappAffiche }}</span>
            </span>
            <ArrowUpRightIcon class="ct-channel__arrow" aria-hidden="true" />
          </a>
          <a :href="`mailto:${vitrineContact.email}`" class="vt-card ct-channel">
            <span class="ct-channel__icon"><EnvelopeIcon aria-hidden="true" /></span>
            <span class="ct-channel__body">
              <span class="ct-channel__tag ct-channel__tag--muted">Réponse sous 24&nbsp;h</span>
              <strong>E-mail</strong>
              <span>{{ vitrineContact.email }}</span>
            </span>
            <ArrowUpRightIcon class="ct-channel__arrow" aria-hidden="true" />
          </a>
          <a href="#formulaire" class="vt-card ct-channel" @click.prevent="scrollTo('formulaire')">
            <span class="ct-channel__icon"><ChatBubbleLeftRightIcon aria-hidden="true" /></span>
            <span class="ct-channel__body">
              <span class="ct-channel__tag ct-channel__tag--muted">Réponse sous 24&nbsp;h</span>
              <strong>Formulaire</strong>
              <span>Écrire un message</span>
            </span>
            <ArrowDownIcon class="ct-channel__arrow" aria-hidden="true" />
          </a>
        </div>
      </div>
    </section>

    <!-- 2. Réponses rapides puis formulaire -->
    <section id="formulaire" class="vt-section">
      <div class="vt-container ct-main">
        <aside v-reveal class="ct-quick">
          <p class="vt-kicker">Avant d’écrire</p>
          <h2 class="ct-quick__title">La réponse est peut-être ici</h2>
          <ul class="ct-quick__list">
            <li v-for="lien in RACCOURCIS" :key="lien.texte">
              <router-link v-if="lien.to" :to="lien.to" class="ct-quick__link">
                <component :is="lien.icone" class="ct-quick__icon" aria-hidden="true" />
                <span>
                  <strong>{{ lien.texte }}</strong>
                  <span>{{ lien.detail }}</span>
                </span>
                <ChevronRightIcon class="ct-quick__chevron" aria-hidden="true" />
              </router-link>
              <button v-else type="button" class="ct-quick__link" @click="lien.action">
                <component :is="lien.icone" class="ct-quick__icon" aria-hidden="true" />
                <span>
                  <strong>{{ lien.texte }}</strong>
                  <span>{{ lien.detail }}</span>
                </span>
                <ChevronRightIcon class="ct-quick__chevron" aria-hidden="true" />
              </button>
            </li>
          </ul>
          <div class="ct-social">
            <p>Suivez-nous <span>@opti.tab</span></p>
            <div class="ct-social__links">
              <a href="https://instagram.com/opti.tab" target="_blank" rel="noopener noreferrer" aria-label="OptiTAB sur Instagram">
                <img src="/icons/instagram.svg" alt="" width="20" height="20" />
              </a>
              <a href="https://tiktok.com/@optitab" target="_blank" rel="noopener noreferrer" aria-label="OptiTAB sur TikTok">
                <img src="/icons/tiktok.svg" alt="" width="20" height="20" />
              </a>
              <a href="https://facebook.com/optitab" target="_blank" rel="noopener noreferrer" aria-label="OptiTAB sur Facebook">
                <img src="/icons/facebook.svg" alt="" width="20" height="20" />
              </a>
            </div>
          </div>
        </aside>

        <div v-reveal="100" class="vt-card ct-form">
          <h2 class="ct-form__title">Envoyer un message</h2>
          <p class="ct-form__text">Un e-mail de confirmation vous est envoyé dès réception.</p>
          <VitrineContactForm mode="contact" :sujet-initial="sujetInitial" />
        </div>
      </div>
    </section>
  </VitrineLayout>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  ArrowDownIcon,
  ArrowUpRightIcon,
  ChatBubbleLeftRightIcon,
  ChevronRightIcon,
  CreditCardIcon,
  EnvelopeIcon,
  KeyIcon,
  SparklesIcon,
  UserGroupIcon
} from '@heroicons/vue/24/outline'
import VitrineLayout from '@/components/vitrine/VitrineLayout.vue'
import VitrineContactForm from '@/components/vitrine/VitrineContactForm.vue'
import { vReveal } from '@/components/vitrine/reveal'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { vitrineContact } from '@/config/vitrineContent'

const route = useRoute()
const { openModal } = useModalManager()

// Lien direct avec un sujet pré-choisi : /contact?sujet=Partenariat
const sujetInitial = computed(() => String(route.query.sujet || ''))

const whatsappUrl = `https://wa.me/${vitrineContact.whatsapp}?text=${encodeURIComponent(vitrineContact.messageWhatsapp)}`

const scrollTo = (id) => {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const RACCOURCIS = [
  { icone: CreditCardIcon, texte: 'Tarifs et abonnements', detail: 'Formules, paiement, résiliation', to: '/tarifs' },
  { icone: UserGroupIcon, texte: 'Cours particuliers', detail: 'Tarifs et premier échange gratuit', to: '/cours-particuliers' },
  { icone: SparklesIcon, texte: 'Ressources gratuites', detail: 'Cours, fiches et exercices en accès libre', to: '/ressources-gratuites' },
  { icone: KeyIcon, texte: 'Mot de passe oublié', detail: 'Recevoir un lien par e-mail', action: () => openModal(MODAL_IDS.FORGOT_PASSWORD) }
]
</script>

<style scoped>
/* ---------- Accroche et canaux ---------- */

.ct-hero__h1 {
  margin: 0;
}

.ct-hero__kicker {
  display: block;
  margin-bottom: 14px;
}

.ct-channels {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-top: 40px;
}

.ct-channel {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  color: var(--vt-ink);
  text-decoration: none;
  transition: border-color 0.15s ease, box-shadow 0.15s ease, transform 0.15s ease;
}

.ct-channel:hover {
  border-color: var(--vt-navy);
  box-shadow: var(--vt-shadow);
  transform: translateY(-2px);
}

.ct-channel__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  border-radius: 14px;
  background: var(--vt-navy-50);
  color: var(--vt-navy);
}

.ct-channel__icon svg {
  width: 24px;
  height: 24px;
}

.ct-channel--whatsapp .ct-channel__icon {
  background: #e7f8ee;
}

.ct-channel__body {
  display: flex;
  flex-direction: column;
  gap: 1px;
  min-width: 0;
  flex: 1;
  font-size: 14px;
  color: var(--vt-muted);
  overflow-wrap: anywhere;
}

.ct-channel__body strong {
  font-size: 17px;
  color: var(--vt-ink);
}

.ct-channel__tag {
  align-self: flex-start;
  margin-bottom: 4px;
  padding: 2px 8px;
  border-radius: 999px;
  background: var(--vt-green-50);
  font-size: 11px;
  font-weight: 700;
  color: var(--vt-green-700);
}

.ct-channel__tag--muted {
  background: var(--vt-bg-soft);
  color: var(--vt-muted);
}

.ct-channel__arrow {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  color: var(--vt-muted);
}

/* ---------- Réponses rapides + formulaire ---------- */

.ct-main {
  display: grid;
  grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr);
  gap: 56px;
  align-items: start;
}

.ct-quick__title {
  font-size: 26px;
}

.ct-quick__list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin: 20px 0 0;
  padding: 0;
  list-style: none;
}

.ct-quick__link {
  display: flex;
  align-items: center;
  gap: 14px;
  width: 100%;
  padding: 12px;
  border: 0;
  border-radius: 12px;
  background: transparent;
  font: inherit;
  text-align: left;
  color: var(--vt-ink);
  text-decoration: none;
  cursor: pointer;
}

.ct-quick__link:hover {
  background: var(--vt-navy-50);
}

.ct-quick__link > span {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
  font-size: 13px;
  color: var(--vt-muted);
}

.ct-quick__link strong {
  font-size: 15px;
  color: var(--vt-ink);
}

.ct-quick__icon {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
  color: var(--vt-navy);
}

.ct-quick__chevron {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  color: var(--vt-muted);
}

.ct-social {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: 28px;
  padding-top: 22px;
  border-top: 1px solid var(--vt-line);
}

.ct-social p {
  margin: 0;
  font-size: 15px;
  font-weight: 700;
  color: var(--vt-ink);
}

.ct-social p span {
  margin-left: 4px;
  font-weight: 600;
  color: var(--vt-muted);
}

.ct-social__links {
  display: flex;
  gap: 8px;
}

.ct-social__links a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border: 1px solid var(--vt-line);
  border-radius: 12px;
  transition: border-color 0.15s ease, background-color 0.15s ease;
}

.ct-social__links a:hover {
  border-color: var(--vt-navy);
  background: var(--vt-navy-50);
}

.ct-form {
  padding: 32px;
  box-shadow: var(--vt-shadow);
}

.ct-form__title {
  font-size: 24px;
}

.ct-form__text {
  margin: 6px 0 24px;
  font-size: 15px;
  color: var(--vt-muted);
}

/* ---------- Tablette et téléphone ---------- */

@media (max-width: 1080px) {
  .ct-channels {
    grid-template-columns: minmax(0, 1fr);
    max-width: 560px;
  }

  .ct-main {
    grid-template-columns: minmax(0, 1fr);
    gap: 40px;
  }

  .ct-main .ct-form {
    order: -1;
  }
}

@media (max-width: 640px) {
  .ct-channels {
    gap: 10px;
    margin-top: 28px;
  }

  .ct-channel {
    padding: 16px;
  }

  .ct-form {
    padding: 22px 16px;
  }
}
</style>
