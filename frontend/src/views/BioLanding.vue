<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import MainLayout from '@/components/layout/MainLayout.vue'
import FaqSection from '@/components/home/FaqSection.vue'
import GoogleReviewsCompact from '@/components/home/GoogleReviewsCompact.vue'
import TestimonialShot from '@/components/landing/TestimonialShot.vue'
import ScreenshotLightbox from '@/components/landing/ScreenshotLightbox.vue'
import { getBioLandingStatus, getPublishedTestimonials } from '@/api/testimonials'
import { setPageSeo, getRobotsForRoute } from '@/services/seo'
import {
  CONTACT,
  FAQ,
  FAQ_SECTION,
  FINAL_CTA,
  GUARANTEES,
  HERO,
  PRICING_TEASER,
  SOCIAL_LINKS,
  SOURCE_LABELS,
  STATS,
  STEPS,
  STEPS_SECTION,
  TESTIMONIALS,
  TESTIMONIALS_SECTION,
  VALUE_PROPS,
  VALUE_SECTION,
  buildWhatsappUrl
} from '@/config/bioLandingContent'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const isDev = Boolean(import.meta.env?.DEV)

// ------------------------------------------------------------
// Mise en ligne : pilotee depuis le studio, pas depuis le code
// ------------------------------------------------------------

// `null` = statut inconnu. On n'affiche rien tant qu'on ne sait pas, sinon
// la page clignoterait avant la redirection d'un visiteur non autorise.
const isPagePublished = ref(null)
const canSeePage = computed(
  () => isPagePublished.value === true || (isPagePublished.value === false && userStore.isAdmin)
)

// Bandeau d'avertissement quand l'admin consulte une page encore hors ligne.
const showOfflineNotice = computed(
  () => isPagePublished.value === false && userStore.isAdmin
)

async function resolveVisibility() {
  let published = false
  try {
    const { data } = await getBioLandingStatus()
    published = Boolean(data?.published)
  } catch (_) {
    // API injoignable : on reste prudent et on considere la page hors ligne.
    published = false
  }

  isPagePublished.value = published

  if (!published) {
    // Hors ligne : jamais indexable, meme si un robot arrive a la rendre.
    setPageSeo({ robots: getRobotsForRoute({ route, noindex: true }) })
    if (!userStore.isAdmin) {
      router.replace({ name: 'Home' })
    }
  }
}

// ------------------------------------------------------------
// Provenance : "Vous venez d'Instagram" grâce à ?utm_source=...
// ------------------------------------------------------------

const sourceLabel = computed(() => {
  const raw = String(route.query.utm_source || '').trim().toLowerCase()
  return SOURCE_LABELS[raw] || ''
})

// Élision : « d'Instagram » mais « de TikTok ».
const sourceSentence = computed(() => {
  const label = sourceLabel.value
  if (!label) return ''
  const startsWithVowel = /^[aeiouyàâäéèêëîïôöûü]/i.test(label)
  return startsWithVowel ? `Vous venez d'${label}` : `Vous venez de ${label}`
})

// ------------------------------------------------------------
// WhatsApp : le CTA principal de la page
// ------------------------------------------------------------

const whatsappUrl = computed(() => buildWhatsappUrl(CONTACT.whatsappMessage))

// ------------------------------------------------------------
// Témoignages : uniquement de vraies captures
// ------------------------------------------------------------

// Source de vérité : le studio d'administration (/admin/temoignages).
// Le tableau du fichier de config sert de repli si l'API est injoignable,
// pour qu'une panne backend ne vide pas la page.
const remoteShots = ref([])
const shotsLoaded = ref(false)

const shots = computed(() => {
  const source = remoteShots.value.length ? remoteShots.value : TESTIMONIALS
  return source.filter((item) => String(item?.src || '').trim())
})

const hasShots = computed(() => shots.value.length > 0)

// Section masquée en production tant qu'aucune capture n'est disponible :
// mieux vaut pas de section qu'une section vide. On attend la réponse de
// l'API avant de trancher, sinon le guide de dev clignoterait au chargement.
const showTestimonials = computed(() => hasShots.value || (isDev && shotsLoaded.value))

// La capture mise en avant s'affiche aussi dans le hero.
const featuredShot = computed(
  () => shots.value.find((item) => item.featured) || shots.value[0] || null
)

const lightboxItems = computed(() =>
  shots.value.map((item) => ({
    id: item.id,
    src: item.src,
    alt: item.alt,
    name: item.name,
    author: item.author,
    role: item.role,
    channel: item.channel
  }))
)

// Libellé d'identité, même règle partout : prénom si autorisé, sinon profil,
// sinon niveau.
function labelOf(item) {
  if (!item) return ''
  return item.name || item.author || item.role || 'Témoignage'
}

function sublabelOf(item) {
  if (!item) return ''
  if (item.name) return [item.author, item.role].filter(Boolean).join(' · ')
  return item.author ? item.role : ''
}

const lightboxOpen = ref(false)
const lightboxIndex = ref(0)

function openShot(testimonial) {
  const index = lightboxItems.value.findIndex((item) => item.id === testimonial.id)
  if (index === -1) return
  lightboxIndex.value = index
  lightboxOpen.value = true
}

// ------------------------------------------------------------
// Barre d'action collante sur mobile
// ------------------------------------------------------------

const showStickyBar = ref(false)

function prefersReducedMotion() {
  if (typeof window === 'undefined' || !window.matchMedia) return false
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

function handleScroll() {
  showStickyBar.value = window.scrollY > 420
}

function scrollToId(id) {
  const target = document.getElementById(id)
  if (!target) return
  target.scrollIntoView({ behavior: prefersReducedMotion() ? 'auto' : 'smooth', block: 'start' })
}

async function loadTestimonials() {
  try {
    const { data } = await getPublishedTestimonials()
    remoteShots.value = Array.isArray(data) ? data : []
  } catch (_) {
    // Backend injoignable : on garde le repli du fichier de config.
    remoteShots.value = []
  } finally {
    shotsLoaded.value = true
  }
}

// La barre collante est en `position: fixed` : elle recouvre le footer, qui
// est rendu par MainLayout, donc hors de portée d'un style scopé. On marque
// le body le temps de la visite pour lui réserver la hauteur de la barre.
// La classe part au démontage : aucune autre page n'est affectée.
const STICKY_BODY_CLASS = 'has-bio-sticky-bar'

onMounted(() => {
  resolveVisibility()
  loadTestimonials()
  document.body.classList.add(STICKY_BODY_CLASS)
  window.addEventListener('scroll', handleScroll, { passive: true })
  handleScroll()
})

onBeforeUnmount(() => {
  document.body.classList.remove(STICKY_BODY_CLASS)
  window.removeEventListener('scroll', handleScroll)
})

// ------------------------------------------------------------
// Pictogrammes des blocs "ce que vous obtenez"
// ------------------------------------------------------------

const ICON_PATHS = {
  book: 'M4 5.5A2.5 2.5 0 0 1 6.5 3H12v16H6.5A2.5 2.5 0 0 0 4 21.5v-16ZM20 5.5A2.5 2.5 0 0 0 17.5 3H12v16h5.5a2.5 2.5 0 0 1 2.5 2.5v-16Z',
  sheet: 'M6 3h8l5 5v13a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Zm8 0v5h5M8.5 13h7M8.5 17h4.5',
  steps: 'M4 19h4v-4H4v4Zm6-6h4V9h-4v4Zm6-6h4V3h-4v4Z',
  chat: 'M21 12a8 8 0 0 1-11.6 7.1L4 21l1.9-5.4A8 8 0 1 1 21 12Z'
}
</script>

<template>
  <MainLayout header-variant="landing" footer-variant="landing">
    <!-- Rien n'est rendu tant que le statut de publication est inconnu :
         un visiteur non autorise ne doit pas entrevoir la page. -->
    <div v-if="canSeePage" class="bio">
      <p v-if="showOfflineNotice" class="bio-offline">
        <strong>Page hors ligne.</strong> Vous seul la voyez. Mettez-la en ligne depuis
        <router-link to="/admin/temoignages">le studio témoignages</router-link>.
      </p>

      <div class="bio-shell">
        <!-- ================= HERO ================= -->
        <section class="block hero-block" :class="{ 'hero-block--solo': !featuredShot }">
          <div class="hero-copy">
            <p class="hero-kicker">{{ sourceSentence || HERO.kicker }}</p>

            <h1>{{ HERO.title }}</h1>

            <p class="hero-subtitle">{{ HERO.subtitle }}</p>

            <!-- La preuve Google est collee au bouton : elle arrive au moment
                 exact ou la decision se prend. -->
            <div class="hero-actions">
              <a
                :href="whatsappUrl"
                class="cta cta--whatsapp"
                target="_blank"
                rel="noopener noreferrer"
                data-cta-name="whatsapp"
                data-cta-location="bio_hero"
              >
                <svg viewBox="0 0 32 32" aria-hidden="true" class="cta__icon">
                  <path fill="currentColor" d="M26.576 5.363c-2.69-2.69-6.406-4.354-10.511-4.354-8.209 0-14.865 6.655-14.865 14.865 0 2.732 0.737 5.291 2.022 7.491l-0.038-0.070-2.109 7.702 7.879-2.067c2.051 1.139 4.498 1.809 7.102 1.809h0.006c8.209-0.003 14.862-6.659 14.862-14.868 0-4.103-1.662-7.817-4.349-10.507l0 0zM16.062 28.228h-0.005c-0 0-0.001 0-0.001 0-2.319 0-4.489-0.64-6.342-1.753l0.056 0.031-0.451-0.267-4.675 1.227 1.247-4.559-0.294-0.467c-1.185-1.862-1.889-4.131-1.889-6.565 0-6.822 5.531-12.353 12.353-12.353s12.353 5.531 12.353 12.353c0 6.822-5.53 12.353-12.353 12.353h-0zM22.838 18.977c-0.371-0.186-2.197-1.083-2.537-1.208-0.341-0.124-0.589-0.185-0.837 0.187-0.246 0.371-0.958 1.207-1.175 1.455-0.216 0.249-0.434 0.279-0.805 0.094-1.15-0.466-2.138-1.087-2.997-1.852l0.010 0.009c-0.799-0.74-1.484-1.587-2.037-2.521l-0.028-0.052c-0.216-0.371-0.023-0.572 0.162-0.757 0.167-0.166 0.372-0.434 0.557-0.65 0.146-0.179 0.271-0.384 0.366-0.604l0.006-0.017c0.043-0.087 0.068-0.188 0.068-0.296 0-0.131-0.037-0.253-0.101-0.357l0.002 0.003c-0.094-0.186-0.836-2.014-1.145-2.758-0.302-0.724-0.609-0.625-0.836-0.637-0.216-0.010-0.464-0.012-0.712-0.012-0.395 0.010-0.746 0.188-0.988 0.463l-0.001 0.002c-0.802 0.761-1.3 1.834-1.3 3.023 0 0.026 0 0.053 0.001 0.079l-0-0.004c0.131 1.467 0.681 2.784 1.527 3.857l-0.012-0.015c1.604 2.379 3.742 4.282 6.251 5.564l0.094 0.043c0.548 0.248 1.25 0.513 1.968 0.74l0.149 0.041c0.442 0.14 0.951 0.221 1.479 0.221 0.303 0 0.601-0.027 0.889-0.078l-0.031 0.004c1.069-0.223 1.956-0.868 2.497-1.749l0.009-0.017c0.165-0.366 0.261-0.793 0.261-1.242 0-0.185-0.016-0.366-0.047-0.542l0.003 0.019c-0.092-0.155-0.34-0.247-0.712-0.434z" />
                </svg>
                {{ HERO.primaryCta }}
              </a>

              <button
                v-if="hasShots"
                type="button"
                class="cta cta--secondary"
                @click="scrollToId('temoignages')"
              >
                {{ HERO.secondaryCta }}
              </button>

              <GoogleReviewsCompact class="hero-reviews" />
            </div>

            <p class="hero-trust">
              <span v-for="item in HERO.trustLine" :key="item">{{ item }}</span>
            </p>
          </div>

          <!-- Colonne de droite uniquement s'il y a une vraie capture a montrer. -->
          <aside v-if="featuredShot" class="hero-side">
            <figure class="hero-shot">
              <img
                :src="featuredShot.src"
                :alt="featuredShot.alt || 'Message reçu par WhatsApp'"
                loading="eager"
              />
              <figcaption>
                <strong>{{ labelOf(featuredShot) }}</strong>
                <span v-if="sublabelOf(featuredShot)">{{ sublabelOf(featuredShot) }}</span>
              </figcaption>
            </figure>
          </aside>
        </section>

        <!-- ================= PREUVE CHIFFRÉE ================= -->
        <section class="block">
          <div class="stat-grid">
            <article v-for="stat in STATS" :key="stat.label" class="stat">
              <span class="stat-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="8.5" stroke="currentColor" stroke-width="1.8" />
                  <path
                    d="M8.5 12.2L10.8 14.5L15.7 9.6"
                    stroke="currentColor"
                    stroke-width="1.9"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </span>
              <span class="stat-text">{{ [stat.value, stat.label].filter(Boolean).join(' ') }}</span>
            </article>
          </div>
        </section>

        <!-- ================= TÉMOIGNAGES ================= -->
        <section v-if="showTestimonials" id="temoignages" class="block">
          <div class="section-head">
            <h2>{{ TESTIMONIALS_SECTION.title }}</h2>
            <p v-if="TESTIMONIALS_SECTION.subtitle">{{ TESTIMONIALS_SECTION.subtitle }}</p>
          </div>

          <template v-if="hasShots">
            <div class="shot-grid">
              <TestimonialShot
                v-for="shot in shots"
                :key="shot.id"
                :testimonial="shot"
                @open="openShot"
              />
            </div>

            <div class="cta-row cta-row--center">
              <a
                :href="whatsappUrl"
                class="cta cta--whatsapp"
                target="_blank"
                rel="noopener noreferrer"
                data-cta-name="whatsapp"
                data-cta-location="bio_testimonials"
              >
                Poser votre question
              </a>
            </div>
          </template>

          <!-- Guide affiché uniquement en développement, jamais en production -->
          <div v-else class="shot-empty">
            <p class="shot-empty__title">Aucune capture publiée</p>
            <p class="shot-empty__text">
              Cette section est <strong>masquée en production</strong> tant qu'aucun témoignage
              n'est publié. Tout se gère depuis le studio :
            </p>
            <ol class="shot-empty__steps">
              <li>Demandez l'accord de la personne et gardez une trace du message.</li>
              <li>Masquez le numéro, la photo de profil et le nom complet sur la capture.</li>
              <li>
                Ouvrez <router-link to="/admin/temoignages">Admin → Témoignages</router-link>,
                déposez la capture, renseignez le prénom et cochez l'accord.
              </li>
              <li>Cochez « Publier » : la capture apparaît ici immédiatement.</li>
            </ol>
            <p class="shot-empty__note">
              Les cartes s'alignent automatiquement : le cadrage est à ratio fixe, donc toutes les
              captures ont la même hauteur quelles que soient leurs dimensions.
            </p>
          </div>
        </section>

        <!-- ================= CE QUE VOUS OBTENEZ ================= -->
        <section class="block">
          <div class="section-head">
            <h2>{{ VALUE_SECTION.title }}</h2>
            <p>{{ VALUE_SECTION.subtitle }}</p>
          </div>

          <div class="value-grid">
            <article v-for="item in VALUE_PROPS" :key="item.title" class="card value-card">
              <span class="value-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24">
                  <path
                    :d="ICON_PATHS[item.icon]"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="1.7"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </span>
              <h3>{{ item.title }}</h3>
              <p>{{ item.text }}</p>
            </article>
          </div>
        </section>

        <!-- ================= COMMENT ÇA SE PASSE ================= -->
        <section class="block">
          <div class="section-head">
            <h2>{{ STEPS_SECTION.title }}</h2>
            <p>{{ STEPS_SECTION.subtitle }}</p>
          </div>

          <ol class="step-grid">
            <li v-for="step in STEPS" :key="step.number" class="card step-card">
              <span class="step-number" aria-hidden="true">Étape {{ step.number }}</span>
              <h3>{{ step.title }}</h3>
              <p>{{ step.text }}</p>
            </li>
          </ol>
        </section>

        <!-- ================= TARIF + RÉASSURANCE ================= -->
        <section class="block">
          <div class="section-head">
            <h2>{{ PRICING_TEASER.title }}</h2>
            <p>{{ PRICING_TEASER.note }}</p>
          </div>

          <div class="pricing-card">
            <div class="pricing-main">
              <p class="pricing-price">
                <span class="pricing-amount">{{ PRICING_TEASER.price }}</span>
                <span class="pricing-suffix">{{ PRICING_TEASER.priceSuffix }}</span>
              </p>
              <router-link
                to="/tarifs"
                class="cta cta--secondary"
                data-cta-name="pricing"
                data-cta-location="bio_pricing"
              >
                {{ PRICING_TEASER.cta }}
              </router-link>
            </div>

            <ul class="guarantee-list">
              <li v-for="item in GUARANTEES" :key="item">
                <svg viewBox="0 0 20 20" aria-hidden="true">
                  <path
                    d="M4.5 10.5 8 14l7.5-8"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2.2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
                {{ item }}
              </li>
            </ul>
          </div>
        </section>

        <!-- ================= FAQ ================= -->
        <section class="block faq-block">
          <FaqSection
            :faq="FAQ"
            :title-prefix="FAQ_SECTION.titlePrefix"
            :title-highlight="FAQ_SECTION.titleHighlight"
            :description="FAQ_SECTION.description"
          />
        </section>

        <!-- ================= CTA FINAL ================= -->
        <section class="block final-block">
          <h2>{{ FINAL_CTA.title }}</h2>
          <p>{{ FINAL_CTA.text }}</p>

          <div class="cta-row cta-row--center">
            <a
              :href="whatsappUrl"
              class="cta cta--whatsapp"
              target="_blank"
              rel="noopener noreferrer"
              data-cta-name="whatsapp"
              data-cta-location="bio_final"
            >
              <svg viewBox="0 0 32 32" aria-hidden="true" class="cta__icon">
                  <path fill="currentColor" d="M26.576 5.363c-2.69-2.69-6.406-4.354-10.511-4.354-8.209 0-14.865 6.655-14.865 14.865 0 2.732 0.737 5.291 2.022 7.491l-0.038-0.070-2.109 7.702 7.879-2.067c2.051 1.139 4.498 1.809 7.102 1.809h0.006c8.209-0.003 14.862-6.659 14.862-14.868 0-4.103-1.662-7.817-4.349-10.507l0 0zM16.062 28.228h-0.005c-0 0-0.001 0-0.001 0-2.319 0-4.489-0.64-6.342-1.753l0.056 0.031-0.451-0.267-4.675 1.227 1.247-4.559-0.294-0.467c-1.185-1.862-1.889-4.131-1.889-6.565 0-6.822 5.531-12.353 12.353-12.353s12.353 5.531 12.353 12.353c0 6.822-5.53 12.353-12.353 12.353h-0zM22.838 18.977c-0.371-0.186-2.197-1.083-2.537-1.208-0.341-0.124-0.589-0.185-0.837 0.187-0.246 0.371-0.958 1.207-1.175 1.455-0.216 0.249-0.434 0.279-0.805 0.094-1.15-0.466-2.138-1.087-2.997-1.852l0.010 0.009c-0.799-0.74-1.484-1.587-2.037-2.521l-0.028-0.052c-0.216-0.371-0.023-0.572 0.162-0.757 0.167-0.166 0.372-0.434 0.557-0.65 0.146-0.179 0.271-0.384 0.366-0.604l0.006-0.017c0.043-0.087 0.068-0.188 0.068-0.296 0-0.131-0.037-0.253-0.101-0.357l0.002 0.003c-0.094-0.186-0.836-2.014-1.145-2.758-0.302-0.724-0.609-0.625-0.836-0.637-0.216-0.010-0.464-0.012-0.712-0.012-0.395 0.010-0.746 0.188-0.988 0.463l-0.001 0.002c-0.802 0.761-1.3 1.834-1.3 3.023 0 0.026 0 0.053 0.001 0.079l-0-0.004c0.131 1.467 0.681 2.784 1.527 3.857l-0.012-0.015c1.604 2.379 3.742 4.282 6.251 5.564l0.094 0.043c0.548 0.248 1.25 0.513 1.968 0.74l0.149 0.041c0.442 0.14 0.951 0.221 1.479 0.221 0.303 0 0.601-0.027 0.889-0.078l-0.031 0.004c1.069-0.223 1.956-0.868 2.497-1.749l0.009-0.017c0.165-0.366 0.261-0.793 0.261-1.242 0-0.185-0.016-0.366-0.047-0.542l0.003 0.019c-0.092-0.155-0.34-0.247-0.712-0.434z" />
                </svg>
              {{ FINAL_CTA.cta }}
            </a>
          </div>

          <p class="final-hint">{{ FINAL_CTA.hint }}</p>

          <div class="social-row">
            <span class="social-label">Retrouvez-nous aussi sur</span>
            <div class="social-links">
              <a
                v-for="social in SOCIAL_LINKS"
                :key="social.name"
                :href="social.href"
                target="_blank"
                rel="noopener noreferrer"
                class="social-link"
              >
                {{ social.name }} <span>{{ social.handle }}</span>
              </a>
            </div>
          </div>
        </section>
      </div>

      <!-- ================= BARRE COLLANTE MOBILE ================= -->
      <Transition name="sticky">
        <div v-show="showStickyBar" class="sticky-bar">
          <div class="sticky-text">
            <strong>Une question ?</strong>
            <span>Réponse rapide, sans engagement</span>
          </div>
          <a
            :href="whatsappUrl"
            class="cta cta--whatsapp cta--sm"
            target="_blank"
            rel="noopener noreferrer"
            data-cta-name="whatsapp"
            data-cta-location="bio_sticky"
          >
            WhatsApp
          </a>
        </div>
      </Transition>

      <ScreenshotLightbox
        :open="lightboxOpen"
        :items="lightboxItems"
        :index="lightboxIndex"
        @close="lightboxOpen = false"
        @update:index="lightboxIndex = $event"
      />
    </div>
  </MainLayout>
</template>

<style scoped lang="scss">
/* ============================================================
   Reprend la charte des autres landings OptiTAB (/start) :
   coquille 1120px, blocs separes par un filet, titres a gauche,
   cartes bleutees 14px, CTA 50px de haut.
   ============================================================ */

.bio {
  background: linear-gradient(180deg, #f8fbff 0%, #ffffff 45%, #f6f8ff 100%);
  min-height: 100%;
}

/* Visible uniquement par l'admin, quand la page n'est pas encore publiee. */
.bio-offline {
  margin: 0;
  padding: 11px 16px;
  background: #fffbeb;
  border-bottom: 1px solid #fcd34d;
  color: #78350f;
  font-size: 0.88rem;
  line-height: 1.5;
  text-align: center;

  a {
    color: #92400e;
    font-weight: 700;
  }
}

.bio-shell {
  max-width: 1120px;
  margin: 0 auto;
  padding: 26px 16px 88px;
  display: grid;
  gap: 0;
}

.block {
  padding: 34px 0;
}

.block + .block {
  border-top: 1px solid rgba(30, 58, 138, 0.12);
}

/* ---------- Titres de section ---------- */

.section-head {
  margin-bottom: 16px;
}

.section-head h2 {
  margin: 0;
  color: #0f172a;
  font-size: clamp(1.45rem, 2.6vw, 2rem);
}

.section-head p {
  margin: 8px 0 0;
  max-width: 70ch;
  color: #475569;
  font-size: 0.96rem;
  line-height: 1.5;
}

/* ---------- Boutons ---------- */

.cta-row {
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.cta-row--center {
  justify-content: center;
}

.cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 50px;
  padding: 0 20px;
  border-radius: 14px;
  font-family: inherit;
  font-size: 1rem;
  font-weight: 800;
  text-decoration: none;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
  -webkit-tap-highlight-color: transparent;

  &:focus-visible {
    outline: 2px solid #2a38b7;
    outline-offset: 3px;
  }
}

/* Glyphe officiel WhatsApp, en aplat de la couleur du texte : c'est un
   trace en contour, donc le combine reste visible sans pastille de fond. */
.cta__icon {
  width: 21px;
  height: 21px;
  flex-shrink: 0;
}

/* Vert officiel WhatsApp #25D366, avec un texte vert tres sombre plutot que
   blanc : blanc sur ce fond ne donne que 2,0:1, illisible en plein soleil et
   non conforme AA. Le texte sombre monte a 10,7:1 tout en gardant la couleur
   exacte de la marque, donc la reconnaissance immediate du canal. */
.cta--whatsapp {
  border: 1px solid #1eb257;
  background: #25d366;
  color: #052e16;

  &:hover {
    background: #22c55e;
    transform: translateY(-1px);
    box-shadow: 0 12px 28px rgba(30, 178, 87, 0.32);
    color: #052e16;
  }
}

.cta--secondary {
  border: 1px solid #c8d6fa;
  background: #ffffff;
  color: #1f2937;
  font-weight: 700;

  &:hover {
    background: #f4f8ff;
    border-color: #a8c1ff;
    color: #1f2937;
  }
}

.cta--sm {
  min-height: 42px;
  padding: 0 16px;
  font-size: 0.92rem;
  border-radius: 11px;
}

/* Bouton principal + preuve Google sur la meme ligne */
.hero-actions {
  margin-top: 24px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px 18px;
}

.hero-reviews {
  flex-shrink: 0;
}

/* Reassurance en texte leger plutot qu'en pastilles : moins dense a l'oeil */
.hero-trust {
  margin: 14px 0 0;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0 8px;
  color: #64748b;
  font-size: 0.88rem;
  font-weight: 600;
}

.hero-trust span + span::before {
  content: '·';
  margin-right: 8px;
  color: #cbd5e1;
}

/* ---------- Carte generique ---------- */

.card {
  border-radius: 14px;
  border: 1px solid #d6e1ff;
  background: linear-gradient(140deg, #ffffff 0%, #f5f8ff 100%);
  padding: 16px 14px;
  transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
}

.card:hover {
  transform: translateY(-2px);
  border-color: #a8c1ff;
  box-shadow: 0 10px 24px rgba(30, 58, 138, 0.1);
}

/* ---------- Hero ---------- */

.hero-block {
  display: grid;
  grid-template-columns: minmax(0, 1.34fr) minmax(0, 0.66fr);
  gap: 22px;
  align-items: start;
}

/* Sans capture a droite, le hero occupe toute la largeur : pas de colonne vide. */
.hero-block--solo {
  grid-template-columns: 1fr;
}

.hero-copy {
  max-width: 820px;
}

.hero-kicker {
  margin: 0;
  color: #2a38b7;
  font-size: 0.82rem;
  letter-spacing: 0.02em;
  font-weight: 800;
}

.hero-copy h1 {
  margin: 10px 0 0;
  max-width: 30ch;
  font-size: clamp(1.52rem, 2.7vw, 2.2rem);
  line-height: 1.08;
  text-wrap: balance;
  color: #0f172a;
}

.hero-subtitle {
  margin: 14px 0 0;
  max-width: 54ch;
  color: #475569;
  font-size: 1.02rem;
  font-weight: 600;
  line-height: 1.45;
  /* global.css active `hyphens: auto` sous 768px : on evite les mots coupes
     sur la phrase la plus lue de la page. */
  hyphens: manual;
}

.hero-side {
  justify-self: end;
  width: 100%;
  max-width: 330px;
}

/* Capture mise en avant */
.hero-shot {
  margin: 0;
  border-radius: 16px;
  border: 1px solid #d6e1ff;
  background: #ffffff;
  overflow: hidden;
  box-shadow: 0 10px 24px rgba(30, 58, 138, 0.1);

  /* Une seule image, sans grille a aligner : aucune raison de la recadrer.
     On la montre entiere, a son ratio naturel. */
  img {
    display: block;
    width: 100%;
    height: auto;
  }

  figcaption {
    display: flex;
    flex-direction: column;
    gap: 1px;
    padding: 10px 13px;
    border-top: 1px solid #e2e9fb;

    strong {
      font-size: 0.9rem;
      font-weight: 800;
      color: #0f172a;
    }

    span {
      font-size: 0.78rem;
      color: #475569;
    }
  }
}

/* ---------- Preuve chiffree ---------- */

.stat-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px 10px;
}

.stat {
  min-height: 40px;
  border-radius: 11px;
  border: 1px solid #d7e3ff;
  background: linear-gradient(145deg, #f8fbff 0%, #f1f5ff 100%);
  padding: 0 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.stat-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  color: #2a38b7;
  display: inline-flex;
  align-items: center;
  justify-content: center;

  svg {
    width: 100%;
    height: 100%;
  }
}

.stat-text {
  color: #1e293b;
  font-size: 0.88rem;
  font-weight: 700;
  line-height: 1.2;
}

/* ---------- Temoignages ---------- */

/* Grille a hauteur de ligne uniforme : chaque carte occupe toute sa cellule. */
.shot-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.shot-grid > * {
  height: 100%;
}

/* Etat vide : guide visible en developpement uniquement */
.shot-empty {
  border-radius: 14px;
  border: 1px dashed #b9cbf0;
  background: #f8fbff;
  padding: 20px 18px;
}

.shot-empty__title {
  margin: 0 0 8px;
  font-size: 1rem;
  font-weight: 800;
  color: #1e3a8a;
}

.shot-empty__text,
.shot-empty__note {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.55;
  color: #475569;
}

.shot-empty__steps {
  margin: 10px 0;
  padding-left: 20px;
  display: grid;
  gap: 5px;
  font-size: 0.9rem;
  line-height: 1.5;
  color: #1e293b;
}

.shot-empty code {
  padding: 1px 5px;
  border-radius: 4px;
  background: #e8eeff;
  color: #1e3a8a;
  font-size: 0.84rem;
}

.shot-empty__note {
  margin-top: 10px;
  font-size: 0.85rem;
}

/* ---------- Ce que vous obtenez ---------- */

.value-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

.value-card h3 {
  margin: 10px 0 5px;
  font-size: 1.02rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.01em;
}

.value-card p {
  margin: 0;
  font-size: 0.88rem;
  line-height: 1.45;
  color: #475569;
  font-weight: 650;
}

.value-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: 11px;
  background: #eef4ff;
  border: 1px solid #cfe0ff;
  color: #2a38b7;

  svg {
    width: 20px;
    height: 20px;
  }
}

/* ---------- Etapes ---------- */

.step-grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

.step-number {
  display: block;
  color: #2a38b7;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

.step-card h3 {
  margin: 6px 0 5px;
  font-size: 1.05rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.01em;
}

.step-card p {
  margin: 0;
  font-size: 0.88rem;
  line-height: 1.45;
  color: #475569;
  font-weight: 650;
}

/* ---------- Tarif ---------- */

.pricing-card {
  display: grid;
  grid-template-columns: 1fr;
  gap: 18px;
  border-radius: 16px;
  border: 1px solid #cfe0ff;
  background: linear-gradient(145deg, #f8fbff 0%, #eef3ff 100%);
  padding: 20px 18px;
}

.pricing-price {
  display: flex;
  align-items: baseline;
  gap: 6px;
  margin: 0 0 14px;
}

.pricing-amount {
  font-size: 2.1rem;
  font-weight: 800;
  color: #1e3a8a;
  line-height: 1;
  letter-spacing: -0.03em;
}

.pricing-suffix {
  font-size: 0.95rem;
  font-weight: 600;
  color: #475569;
}

.pricing-main .cta {
  margin-top: 0;
}

.guarantee-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 9px;
  align-content: center;

  li {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    font-size: 0.9rem;
    font-weight: 650;
    line-height: 1.45;
    color: #1e293b;
  }

  svg {
    flex-shrink: 0;
    width: 15px;
    height: 15px;
    margin-top: 3px;
    color: #16a34a;
  }
}

/* ---------- FAQ ---------- */

.faq-block :deep(.faq-section) {
  margin-bottom: 0;
  padding-top: 0;
}

/* ---------- CTA final ---------- */

.final-block {
  text-align: center;
  border-radius: 18px;
  background: linear-gradient(145deg, #ffffff 0%, #eef2ff 100%);
  border: 1px solid #dbe4ff;
  padding: 30px 20px;
  margin-top: 34px;
}

.final-block + .block,
.block + .final-block {
  border-top: none;
}

.final-block h2 {
  margin: 0;
  color: #0f172a;
  font-size: clamp(1.45rem, 2.6vw, 2rem);
}

.final-block > p {
  margin: 8px auto 0;
  max-width: 60ch;
  color: #475569;
  font-size: 0.96rem;
  line-height: 1.5;
}

.final-hint {
  margin: 12px 0 0;
  color: #475569;
  font-size: 0.9rem;
  font-weight: 700;
}

.social-row {
  margin-top: 22px;
  padding-top: 18px;
  border-top: 1px solid rgba(30, 58, 138, 0.12);
}

.social-label {
  color: #64748b;
  font-size: 0.82rem;
}

.social-links {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
}

.social-link {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  min-height: 36px;
  padding: 0 13px;
  border-radius: 999px;
  border: 1px solid #cfe0ff;
  background: #ffffff;
  color: #1e3a8a;
  font-size: 0.84rem;
  font-weight: 700;
  text-decoration: none;
  transition: background 0.18s ease, border-color 0.18s ease;

  &:hover {
    background: #f4f8ff;
    border-color: #a8c1ff;
    color: #1e3a8a;
  }

  span {
    font-weight: 500;
    color: #64748b;
  }
}

/* ---------- Barre collante mobile ---------- */

.sticky-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 12000;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px calc(10px + env(safe-area-inset-bottom, 0px));
  background: rgba(255, 255, 255, 0.97);
  backdrop-filter: blur(10px);
  border-top: 1px solid #d7e3ff;
  box-shadow: 0 -4px 20px rgba(30, 58, 138, 0.1);
}

.sticky-text {
  display: flex;
  flex-direction: column;
  min-width: 0;
  flex: 1;
  line-height: 1.3;

  strong {
    font-size: 0.86rem;
    color: #0f172a;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  span {
    font-size: 0.75rem;
    color: #475569;
  }
}

.sticky-enter-active,
.sticky-leave-active {
  transition: transform 0.25s ease, opacity 0.25s ease;
}

.sticky-enter-from,
.sticky-leave-to {
  transform: translateY(100%);
  opacity: 0;
}

/* ---------- Points de rupture ---------- */

@media (min-width: 640px) {
  .value-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .step-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .shot-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .pricing-card {
    grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
    align-items: center;
    padding: 24px 22px;
  }

  .final-block {
    padding: 38px 30px;
  }
}

@media (min-width: 961px) {
  .value-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }

  .shot-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }

  .stat-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

@media (max-width: 960px) {
  .hero-block {
    grid-template-columns: 1fr;
  }

  .hero-side {
    justify-self: start;
    max-width: 300px;
  }
}

@media (max-width: 860px) {
  .bio-shell {
    padding-bottom: 40px;
  }
}

@media (min-width: 861px) {
  .sticky-bar {
    display: none;
  }
}

@media (max-width: 480px) {
  .cta-row .cta,
  .hero-actions .cta {
    width: 100%;
  }

  .hero-actions {
    gap: 12px;
  }

  .sticky-bar .cta {
    width: auto;
  }
}

@media (prefers-reduced-motion: reduce) {
  .cta,
  .card,
  .sticky-enter-active,
  .sticky-leave-active {
    transition: none;
  }

  .card:hover,
  .cta--whatsapp:hover {
    transform: none;
  }
}
</style>

<!-- Style non scopé : il doit atteindre le <body>, hors du composant.
     La règle ne s'applique que si la classe est présente, et cette classe
     n'existe que pendant que cette page est montée. -->
<style lang="scss">
body.has-bio-sticky-bar {
  /* Hauteur de la barre WhatsApp + encoche des iPhone, pour que le bas du
     footer (« Gérer mes cookies ») reste accessible. */
  padding-bottom: calc(72px + env(safe-area-inset-bottom, 0px));
}

@media (min-width: 861px) {
  body.has-bio-sticky-bar {
    /* La barre est masquée sur grand écran : pas d'espace à réserver. */
    padding-bottom: 0;
  }
}
</style>
