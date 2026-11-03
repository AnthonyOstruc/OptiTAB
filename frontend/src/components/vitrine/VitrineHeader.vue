<template>
  <header :class="['vt-header', { 'vt-header--scrolled': isScrolled }]">
    <div class="vt-header__inner">
      <router-link
        to="/"
        class="vt-header__brand"
        aria-label="OptiTAB, cours de maths en ligne — accueil"
        data-track="nav"
        data-nav-name="home"
        data-nav-location="header_public"
        @click="onBrandClick"
      >
        <img src="@/assets/logos/Logo_bg.png" alt="OptiTAB, cours en ligne" class="vt-header__logo" width="132" height="43" />
      </router-link>

      <!-- En-tête allégé : sur l'accueil, des ancres vers ses sections ; ailleurs,
           les liens qui ont une page dédiée (Tarifs, Cours particuliers) y mènent.
           Les autres pages sont dans le pied de page. -->
      <nav v-if="!landing" class="vt-header__nav" aria-label="Navigation principale">
        <a
          v-for="item in navItems"
          :key="item.ancre"
          :href="hrefOf(item)"
          :class="['vt-header__link', { 'is-active': isActive(item) }]"
          :aria-current="isActive(item) ? 'true' : null"
          data-track="nav"
          :data-nav-name="item.navName"
          data-nav-location="header_public"
          @click.prevent="goTo(item)"
        >
          {{ item.texte }}
        </a>
      </nav>

      <div class="vt-header__actions">
        <!-- Élève connecté : un seul bouton vers son espace. -->
        <router-link
          v-if="isAuthenticated"
          to="/dashboard"
          class="vt-btn vt-btn--primary vt-btn--sm vt-header__cta"
          data-cta-name="dashboard"
          data-cta-location="header_public"
        >
          <UserCircleIcon aria-hidden="true" />
          Mon espace
        </router-link>
        <!-- Pages publicitaires et de paiement : pas de menu, contact + action principale
             (mêmes marqueurs de suivi que l'ancien en-tête « landing »). -->
        <template v-else-if="landing">
          <button
            type="button"
            class="vt-header__login vt-header__login--compact"
            aria-label="Nous contacter"
            data-track="nav"
            data-nav-name="contact"
            data-nav-location="header_public"
            @click="openContact"
          >
            <EnvelopeIcon class="vt-header__login-icon" aria-hidden="true" />
            <span class="vt-header__login-text">Nous contacter</span>
          </button>
          <button
            type="button"
            class="vt-btn vt-btn--primary vt-btn--sm vt-header__cta"
            :aria-label="landingCta.label"
            :data-cta-name="landingCta.name"
            data-cta-location="header_public"
            @click="onLandingCta"
          >
            <span class="vt-header__cta-long">{{ landingCta.label }}</span>
            <span class="vt-header__cta-short" aria-hidden="true">{{ landingCta.court }}</span>
          </button>
        </template>
        <template v-else>
          <button
            type="button"
            class="vt-header__login"
            aria-label="Se connecter"
            data-cta-name="login"
            data-cta-location="header_public"
            @click="openLogin"
          >
            <UserCircleIcon class="vt-header__login-icon" aria-hidden="true" />
            <span class="vt-header__login-text">Se connecter</span>
          </button>
          <a
            :href="isHome() ? '/#tarifs' : '/tarifs'"
            class="vt-btn vt-btn--primary vt-btn--sm vt-header__cta"
            data-cta-name="pricing"
            data-cta-location="header_public"
            @click.prevent="goTo(subscribeItem)"
          >
            S’abonner
          </a>
        </template>
      </div>
    </div>
  </header>
  <ContactModal
    v-if="landing"
    :isOpen="contactOpen"
    initialSubject="Demande d'information"
    @close="contactOpen = false"
    @success="contactOpen = false"
  />
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { EnvelopeIcon, UserCircleIcon } from '@heroicons/vue/24/outline'
import ContactModal from '@/components/common/ContactModal.vue'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { useUserStore } from '@/stores/user'
import { vitrineAncres } from '@/config/vitrineContent'

const props = defineProps({
  // Pages publicitaires et de paiement : en-tête épuré.
  landing: { type: Boolean, default: false }
})

const route = useRoute()
const router = useRouter()
const { openModal } = useModalManager()
const userStore = useUserStore()

// Pages d'offre : l'action principale mène aux formules de la page (#offre).
const PAGES_OFFRE = ['/plateforme-maths', '/bases-methode', '/exercices-corriges', '/exercices-corriges-pas-a-pas']
const landingCta = computed(() => (PAGES_OFFRE.includes(route.path)
  ? { name: 'pricing', label: 'Choisir un abonnement', court: 'S’abonner' }
  : { name: 'signup', label: 'Créer un compte', court: 'Créer un compte' }))

const onLandingCta = async () => {
  if (landingCta.value.name === 'pricing') {
    const offre = document.getElementById('offre')
    if (offre) offre.scrollIntoView({ behavior: 'smooth', block: 'start' })
    else await router.push({ path: route.path, hash: '#offre' })
    return
  }
  openModal(MODAL_IDS.REGISTER)
}

const contactOpen = ref(false)
const openContact = () => {
  contactOpen.value = true
}

const isScrolled = ref(false)
const activeId = ref('')
let sectionObserver = null

const isAuthenticated = computed(() => userStore.isAuthenticated)

// Les ancres visent toujours les sections de l'accueil : sur une autre page, un
// même identifiant (ex. « tarifs » dans les CGV) ne doit pas être pris pour cible.
const isHome = () => route.path === '/'

// Un élève connecté est renvoyé de l'accueil vers son espace : on ne lui montre
// que les liens qui ont une page dédiée.
const navItems = computed(() =>
  isAuthenticated.value ? vitrineAncres.filter((item) => item.page) : vitrineAncres
)

const subscribeItem = vitrineAncres.find((item) => item.ancre === 'tarifs')

const hrefOf = (item) => (!isHome() && item.page ? item.page : `/#${item.ancre}`)

const isActive = (item) => (isHome() ? activeId.value === item.ancre : route.path === item.page)

const goTo = (item) => {
  if (isHome()) {
    const target = document.getElementById(item.ancre)
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' })
      return
    }
  }
  if (item.page) {
    if (route.path === item.page) window.scrollTo({ top: 0, behavior: 'smooth' })
    else router.push(item.page)
    return
  }
  router.push({ path: '/', hash: `#${item.ancre}` })
}

const onBrandClick = (event) => {
  if (route.path === '/') {
    event.preventDefault()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const openLogin = () => {
  openModal(MODAL_IDS.LOGIN)
}

const onScroll = () => {
  isScrolled.value = window.scrollY > 8
}

// Le lien de la section en cours de lecture est mis en évidence.
const watchSections = () => {
  if (!isHome() || !('IntersectionObserver' in window)) return
  sectionObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) activeId.value = entry.target.id
        else if (activeId.value === entry.target.id) activeId.value = ''
      })
    },
    { rootMargin: '-40% 0px -55% 0px' }
  )
  vitrineAncres.forEach(({ ancre }) => {
    const el = document.getElementById(ancre)
    if (el) sectionObserver.observe(el)
  })
}

onMounted(() => {
  onScroll()
  window.addEventListener('scroll', onScroll, { passive: true })
  // Les sections sont rendues avec la page : on les observe au tour suivant.
  requestAnimationFrame(watchSections)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
  sectionObserver?.disconnect()
  sectionObserver = null
})
</script>

<style scoped>
/* `fixed` et non `sticky` : #app a un overflow-x qui neutralise `sticky`. */
.vt-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 12000;
  background: #fff;
  border-bottom: 1px solid transparent;
  padding-top: env(safe-area-inset-top, 0px);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.vt-header--scrolled {
  border-bottom-color: var(--vt-line);
  box-shadow: 0 6px 24px rgba(16, 32, 79, 0.06);
}

.vt-header__inner {
  display: flex;
  align-items: center;
  gap: 24px;
  max-width: var(--vt-max);
  height: 72px;
  margin: 0 auto;
  padding: 0 var(--vt-gutter);
}

.vt-header__brand {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.vt-header__logo {
  display: block;
  width: 132px;
  height: auto;
}

/* La navigation prend la place restante et ne pousse jamais les boutons hors de l'écran. */
.vt-header__nav {
  display: flex;
  flex: 1 1 auto;
  justify-content: center;
  align-items: center;
  gap: 4px;
  min-width: 0;
  overflow: hidden;
}

.vt-header__link {
  position: relative;
  flex-shrink: 0;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  color: var(--vt-ink-soft);
  text-decoration: none;
  white-space: nowrap;
  transition: color 0.15s ease, background-color 0.15s ease;
}

.vt-header__link:hover {
  color: var(--vt-navy);
  background: var(--vt-navy-50);
}

.vt-header__link.is-active {
  color: var(--vt-navy);
}

.vt-header__link.is-active::after {
  content: '';
  position: absolute;
  left: 14px;
  right: 14px;
  bottom: 3px;
  height: 2px;
  border-radius: 2px;
  background: var(--vt-green);
}

.vt-header__actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  margin-left: auto;
}

.vt-header__login {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 42px;
  padding: 0 14px;
  border: 0;
  border-radius: 10px;
  background: transparent;
  font-family: var(--vt-font);
  font-size: 15px;
  font-weight: 600;
  color: var(--vt-navy);
  white-space: nowrap;
  cursor: pointer;
}

.vt-header__login:hover {
  background: var(--vt-navy-50);
}

.vt-header__login-icon {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
}

.vt-header__cta {
  padding: 0 20px;
}

/* En dessous de 1024 px, seuls le logo et les deux boutons restent. */
@media (max-width: 1023px) {
  .vt-header__nav {
    display: none;
  }
}

@media (max-width: 960px) {
  .vt-header__inner {
    height: 64px;
  }

  .vt-header__logo {
    width: 112px;
  }
}

@media (max-width: 480px) {
  .vt-header__inner {
    gap: 8px;
  }

  .vt-header__logo {
    width: 100px;
  }

  .vt-header__login {
    height: 40px;
    padding: 0 10px;
    border: 1px solid var(--vt-line-strong);
    border-radius: 999px;
    font-size: 14px;
  }

  .vt-header__login-icon {
    display: none;
  }

  .vt-header__cta {
    min-height: 40px;
    padding: 0 14px;
    font-size: 14px;
  }
}

.vt-header__cta-short {
  display: none;
}

/* Pages publicitaires sur téléphone : icône de contact et libellé court. */
@media (max-width: 480px) {
  .vt-header__login--compact {
    width: 40px;
    padding: 0;
    justify-content: center;
  }

  .vt-header__login--compact .vt-header__login-icon {
    display: block;
  }

  .vt-header__login--compact .vt-header__login-text {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
  }

  .vt-header__cta-long {
    display: none;
  }

  .vt-header__cta-short {
    display: inline;
  }
}

/* Très petits écrans : l'icône remplace le texte « Se connecter ». */
@media (max-width: 374px) {
  .vt-header__login {
    width: 40px;
    padding: 0;
    justify-content: center;
  }

  .vt-header__login-icon {
    display: block;
  }

  .vt-header__login-text {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
  }
}
</style>
