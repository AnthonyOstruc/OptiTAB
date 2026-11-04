<template>
  <div class="es es-shell">
    <!-- Menu latéral (ordinateur) -->
    <aside class="es-side" aria-label="Menu principal">
      <router-link :to="homeLink" class="es-side__logo" aria-label="Accueil de mon espace">
        <img src="@/assets/logos/Logo_bg.png" alt="OptiTAB" width="124" height="39" />
      </router-link>

      <router-link v-if="classe" to="/account" class="es-side__class" title="Changer de classe dans Mon compte">
        <span class="es-side__class-icon" aria-hidden="true"><AcademicCapIcon /></span>
        <span class="es-side__class-text">
          <span>Ma classe</span>
          <strong>{{ classe }}</strong>
        </span>
        <ChevronUpDownIcon class="es-side__class-chev" aria-hidden="true" />
      </router-link>

      <nav class="es-side__nav">
        <p class="es-side__group">{{ isParent ? 'Suivi' : 'Apprendre' }}</p>
        <router-link
          v-for="item in mainItems"
          :key="item.to"
          :to="item.to"
          :class="['es-side__item', { 'is-active': isActive(item) }]"
          :aria-current="isActive(item) ? 'page' : undefined"
        >
          <component :is="isActive(item) ? item.iconOn : item.icon" aria-hidden="true" />
          <span>{{ item.label }}</span>
        </router-link>
      </nav>

      <div class="es-side__bottom">
        <!-- Le prof, toujours à portée de main -->
        <div class="es-prof">
          <div class="es-prof__head">
            <span class="es-prof__photo" aria-hidden="true"></span>
            <span class="es-prof__who">
              <strong>Anthony</strong>
              <span>{{ isParent ? 'Professeur, fondateur' : 'Ton prof' }}</span>
            </span>
            <span class="es-prof__online" title="Répond sur WhatsApp"></span>
          </div>
          <p>{{ isParent ? 'Un accompagnement personnalisé pour votre enfant.' : 'Bloqué sur un exercice ? Pose ta question.' }}</p>
          <div class="es-prof__actions">
            <a :href="whatsappUrl" target="_blank" rel="noopener noreferrer" class="es-prof__btn es-prof__btn--wa" data-cta-name="whatsapp" data-cta-location="espace_menu">
              <img src="/icons/whatsapp.svg" alt="" width="16" height="16" />
              WhatsApp
            </a>
            <router-link to="/cours-particuliers" class="es-prof__btn">Cours</router-link>
          </div>
        </div>

        <router-link
          v-for="item in accountItems"
          :key="item.to"
          :to="item.to"
          :class="['es-side__item', 'es-side__item--sm', { 'is-active': isActive(item) }]"
        >
          <component :is="item.icon" aria-hidden="true" />
          <span>{{ item.label }}</span>
        </router-link>
      </div>
    </aside>

    <!-- Barre du haut -->
    <header class="es-top">
      <div class="es-top__left">
        <router-link v-if="back" :to="back.to" class="es-top__back" :aria-label="back.label">
          <ChevronLeftIcon aria-hidden="true" />
        </router-link>
        <router-link :to="homeLink" class="es-top__logo" aria-label="Accueil de mon espace">
          <img src="@/assets/logos/Logo_bg.png" alt="OptiTAB" width="102" height="32" />
        </router-link>
        <p v-if="title" class="es-top__title">{{ title }}</p>
        <EspaceSearch v-if="!isParent" class="es-top__search" />
      </div>
      <div class="es-top__right">
        <router-link v-if="!isParent" :to="{ path: ESPACE_ROUTES.chapitres, query: { recherche: '1' } }" class="es-top__icon-btn" aria-label="Rechercher un chapitre">
          <MagnifyingGlassIcon aria-hidden="true" />
        </router-link>
        <EspaceNotifications />
        <span class="es-top__sep" aria-hidden="true"></span>
        <EspaceCompte />
      </div>
    </header>

    <main :class="['es-main', { 'es-main--full': pleineLargeur }]">
      <div :class="['es-main__inner', { 'es-main__inner--wide': wide }]">
        <div v-if="$slots.subheader" class="es-subheader"><slot name="subheader" /></div>
        <slot />
      </div>
    </main>

    <!-- Barre d'onglets (téléphone) -->
    <nav class="es-tabbar" aria-label="Navigation principale">
      <router-link
        v-for="item in tabItems"
        :key="item.to"
        :to="item.to"
        :class="['es-tabbar__item', { 'is-active': isActive(item) }]"
        :aria-current="isActive(item) ? 'page' : undefined"
      >
        <span class="es-tabbar__pill"><component :is="isActive(item) ? item.iconOn : item.icon" aria-hidden="true" /></span>
        <span>{{ item.short || item.label }}</span>
      </router-link>
    </nav>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import {
  AcademicCapIcon,
  BookOpenIcon,
  CalculatorIcon,
  ChevronLeftIcon,
  ChevronUpDownIcon,
  ClockIcon,
  CreditCardIcon,
  HomeIcon,
  MagnifyingGlassIcon,
  QuestionMarkCircleIcon,
  ShieldCheckIcon,
  UserCircleIcon
} from '@heroicons/vue/24/outline'
import {
  AcademicCapIcon as AcademicCapSolid,
  BookOpenIcon as BookOpenSolid,
  CalculatorIcon as CalculatorSolid,
  ClockIcon as ClockSolid,
  CreditCardIcon as CreditCardSolid,
  HomeIcon as HomeSolid,
  QuestionMarkCircleIcon as QuestionSolid,
  UserCircleIcon as UserCircleSolid
} from '@heroicons/vue/24/solid'
import EspaceNotifications from './EspaceNotifications.vue'
import EspaceCompte from './EspaceCompte.vue'
import EspaceSearch from './EspaceSearch.vue'
import { useUserStore } from '@/stores/user'
import { useSubscriptionStore } from '@/stores/subscription'
import { useQuizDisponible } from '@/composables/useQuizDisponible'
import { ESPACE_ROUTES } from '@/config/espace'
import { vitrineContact } from '@/config/vitrineContent'
import { chapitreDuLien, prechargerChapitre } from '@/utils/chapitreContenu'
import '@/styles/espace.css'

const props = defineProps({
  // Titre court affiché dans la barre du haut sur téléphone.
  title: { type: String, default: '' },
  // Force le menu parent (aperçu ?vue=parent) ; sinon, d'après le compte.
  parent: { type: Boolean, default: null },
  // Flèche retour sur téléphone : { to, label }.
  back: { type: Object, default: null },
  // Pages de lecture (cours) : colonne plus large pour le sommaire.
  wide: { type: Boolean, default: false },
  // Outils plein écran (calculatrice) : pas de marge latérale sur téléphone.
  pleineLargeur: { type: Boolean, default: false }
})

const route = useRoute()
const userStore = useUserStore()
const subscriptionStore = useSubscriptionStore()

const isParent = computed(() => props.parent ?? userStore.role === 'parent')
const homeLink = ESPACE_ROUTES.accueil
const classe = computed(() => (isParent.value ? '' : userStore.niveau_pays?.nom || ''))

const whatsappUrl = computed(() => {
  const texte = isParent.value
    ? 'Bonjour, je souhaite des informations sur l’accompagnement de mon enfant.'
    : 'Bonjour, j’ai une question sur un exercice OptiTAB.'
  return `https://wa.me/${vitrineContact.whatsapp}?text=${encodeURIComponent(texte)}`
})

const ACCUEIL = { label: 'Accueil', to: ESPACE_ROUTES.accueil, icon: HomeIcon, iconOn: HomeSolid, exact: true }
const CHAPITRES = { label: 'Mes chapitres', short: 'Chapitres', to: ESPACE_ROUTES.chapitres, icon: BookOpenIcon, iconOn: BookOpenSolid, prefix: ESPACE_ROUTES.chapitre }
const QUIZ = { label: 'Quiz', to: '/quiz', icon: QuestionMarkCircleIcon, iconOn: QuestionSolid, prefix: '/quiz' }
const CALCUL = { label: 'Outil de calcul', short: 'Calcul', to: '/calculator', icon: CalculatorIcon, iconOn: CalculatorSolid }
const PROF = { label: 'Cours particuliers', short: 'Prof', to: '/cours-particuliers', icon: AcademicCapIcon, iconOn: AcademicCapSolid }
// Abonné : « Abonnement » mène à la gestion (suivi, factures, arrêt) ;
// sinon, aux formules. Les deux pages allument le même lien.
const ABONNEMENT_BASE = { label: 'Abonnement', icon: CreditCardIcon, iconOn: CreditCardSolid, pages: ['/billing', '/subscription'] }
const COMPTE = { label: 'Mon compte', short: 'Compte', to: '/account', icon: UserCircleIcon, iconOn: UserCircleSolid }
const ADMIN = { label: 'Administration', to: '/admin', icon: ShieldCheckIcon, iconOn: ShieldCheckIcon, prefix: '/admin' }

const HISTORIQUE = { label: 'Historique', to: '/historique-exercices', icon: ClockIcon, iconOn: ClockSolid, prefix: '/historique' }

// Quiz : seulement si des quiz sont publiés (ou si l'on est déjà sur une page quiz).
const { quizDisponible, verifier: verifierQuiz } = useQuizDisponible()
const avecQuiz = computed(() => quizDisponible.value || route.path.startsWith('/quiz'))

// L'outil de calcul est masqué des menus (demande du 2026-11-03) ; la page
// /calculator reste accessible et garde ce cadre (onglet actif si on y est).
const avecCalcul = computed(() => route.path === CALCUL.to)

const mainItems = computed(() => {
  if (isParent.value) return [ACCUEIL, PROF]
  return [ACCUEIL, CHAPITRES, ...(avecQuiz.value ? [QUIZ] : []), HISTORIQUE, ...(avecCalcul.value ? [CALCUL] : [])]
})
const ABONNEMENT = computed(() => ({ ...ABONNEMENT_BASE, to: subscriptionStore.hasAccess ? '/subscription' : '/billing' }))
const accountItems = computed(() => [ABONNEMENT.value, COMPTE, ...(userStore.isAdmin ? [ADMIN] : [])])
const tabItems = computed(() => {
  if (isParent.value) return [ACCUEIL, PROF, ABONNEMENT.value, COMPTE]
  return [ACCUEIL, CHAPITRES, ...(avecQuiz.value ? [QUIZ] : []), HISTORIQUE, PROF]
})

const isActive = (item) => {
  const path = route.path
  if (item.exact) return path === item.to
  if (item.pages) return item.pages.includes(path)
  if (path === item.to) return true
  return Boolean(item.prefix && path.startsWith(item.prefix))
}

// Préchargement : quand la souris s'attarde sur un lien de chapitre (ou dès le
// toucher, ou au clavier), son contenu est demandé tout de suite ; le clic
// ouvre ensuite une page déjà prête.
let minuteurPrecharge = null
function chapitreVise(e) {
  const lien = e.target instanceof Element ? e.target.closest('a[href]') : null
  return lien ? chapitreDuLien(lien.getAttribute('href')) : null
}
function prechargerVise(e) {
  const cible = chapitreVise(e)
  if (cible) prechargerChapitre(cible.notionId, [cible.onglet])
}
function survolLien(e) {
  if (e.pointerType !== 'mouse') return
  clearTimeout(minuteurPrecharge)
  const cible = chapitreVise(e)
  if (cible) minuteurPrecharge = setTimeout(() => prechargerChapitre(cible.notionId, [cible.onglet]), 80)
}
function quitterLien() {
  clearTimeout(minuteurPrecharge)
}

// Le défilement se fait sur la page entière (pas dans une zone interne) ;
// `overflow-x: clip` sur #app permet en plus les éléments collants.
onMounted(() => {
  document.documentElement.classList.add('es-page')
  if (!isParent.value) verifierQuiz()
  // Statut gardé une minute dans le magasin : sert au lien « Abonnement ».
  subscriptionStore.fetchStatus().catch(() => {})
  document.addEventListener('pointerover', survolLien, { passive: true })
  document.addEventListener('pointerout', quitterLien, { passive: true })
  document.addEventListener('touchstart', prechargerVise, { passive: true })
  document.addEventListener('focusin', prechargerVise)
})
onBeforeUnmount(() => {
  document.documentElement.classList.remove('es-page')
  clearTimeout(minuteurPrecharge)
  document.removeEventListener('pointerover', survolLien)
  document.removeEventListener('pointerout', quitterLien)
  document.removeEventListener('touchstart', prechargerVise)
  document.removeEventListener('focusin', prechargerVise)
})
</script>

<style>
html.es-page,
html.es-page body {
  background: #f5f7fb;
}

@supports (overflow: clip) {
  html.es-page body,
  html.es-page #app {
    overflow-x: clip !important;
    overflow-y: visible !important;
  }
}

/* Anciennes pages (quiz…) : leurs boutons « Retour » étaient fixés pour
   l'ancienne coque ; ici ils prennent place en haut du contenu. */
.es-shell .back-button--top-left,
.es-shell .back-button--top-left-dashboard,
.es-shell .back-button--main-notions,
.es-shell .back-button--sticky {
  position: static !important;
  inset: auto !important;
  margin: 0 0 16px !important;
  transform: none !important;
}

/* Sur téléphone, la flèche de la barre du haut suffit. */
@media (max-width: 1023px) {
  .es-shell .back-button--top-left,
  .es-shell .back-button--top-left-dashboard,
  .es-shell .back-button--main-notions,
  .es-shell .back-button--sticky {
    display: none !important;
  }
}
</style>

<style scoped>
.es-shell {
  min-height: 100vh;
  background:
    radial-gradient(1200px 380px at 70% -120px, rgba(27, 60, 142, 0.07), transparent 70%),
    var(--es-bg);
}

/* ---------- Menu latéral ---------- */

.es-side {
  position: fixed;
  inset: 0 auto 0 0;
  z-index: 40;
  display: flex;
  flex-direction: column;
  width: var(--es-side);
  padding: 20px 14px 14px;
  overflow-y: auto;
  border-right: 1px solid var(--es-line);
  background: #fff;
  scrollbar-width: thin;
}

.es-side__logo {
  display: inline-flex;
  padding: 2px 10px 20px;
}

.es-side__logo img {
  width: 124px;
  height: auto;
}

.es-side__class {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 2px 20px;
  padding: 10px 10px 10px 10px;
  border: 1px solid var(--es-line);
  border-radius: 14px;
  background: linear-gradient(180deg, #fff 0%, var(--es-bg) 100%);
  text-decoration: none;
  transition: border-color 0.15s ease;
}

.es-side__class:hover {
  border-color: var(--es-line-strong);
}

.es-side__class-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  border-radius: 10px;
  background: var(--es-navy);
  color: #fff;
}

.es-side__class-icon svg {
  width: 20px;
  height: 20px;
}

.es-side__class-text {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--es-muted);
}

.es-side__class-text strong {
  font-size: 15px;
  letter-spacing: 0;
  text-transform: none;
  color: var(--es-ink);
}

.es-side__class-chev {
  width: 18px;
  height: 18px;
  color: #98a2b3;
}

.es-side__nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.es-side__group {
  margin: 0 12px 8px !important;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #98a2b3;
}

.es-side__item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 44px;
  padding: 0 12px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  color: var(--es-ink-soft);
  text-decoration: none;
  transition: background-color 0.15s ease, color 0.15s ease;
}

.es-side__item svg {
  width: 21px;
  height: 21px;
  flex-shrink: 0;
  color: #8a94a8;
}

.es-side__item:hover {
  background: var(--es-bg);
  color: var(--es-ink);
}

.es-side__item.is-active {
  background: var(--es-navy-50);
  color: var(--es-navy);
}

.es-side__item.is-active::before {
  content: '';
  position: absolute;
  top: 10px;
  bottom: 10px;
  left: -14px;
  width: 4px;
  border-radius: 0 4px 4px 0;
  background: var(--es-navy);
}

.es-side__item.is-active svg {
  color: var(--es-navy);
}

.es-side__item--sm {
  min-height: 40px;
  font-size: 14px;
}

.es-side__bottom {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-top: auto;
  padding-top: 16px;
}

/* Carte du prof */
.es-prof {
  margin: 0 2px 12px;
  padding: 14px;
  border-radius: 16px;
  background: linear-gradient(160deg, #1b3c8e 0%, #132d6c 100%);
  color: #fff;
}

.es-prof__head {
  display: flex;
  align-items: center;
  gap: 10px;
}

.es-prof__photo {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  border: 2px solid rgba(255, 255, 255, 0.85);
  border-radius: 50%;
  background: #fff url('/images/professeurs/anthony.jpg') 50% 12% / 190% auto no-repeat;
}

.es-prof__who {
  display: flex;
  flex: 1;
  flex-direction: column;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
}

.es-prof__who strong {
  font-size: 15px;
  color: #fff;
}

.es-prof__online {
  width: 10px;
  height: 10px;
  border: 2px solid #1b3c8e;
  border-radius: 50%;
  background: #5fd068;
  box-shadow: 0 0 0 3px rgba(95, 208, 104, 0.25);
}

.es-prof p {
  margin-top: 10px !important;
  font-size: 13px;
  line-height: 1.45;
  color: rgba(255, 255, 255, 0.85);
}

.es-prof__actions {
  display: grid;
  grid-template-columns: 1.3fr 1fr;
  gap: 6px;
  margin-top: 12px;
}

.es-prof__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  min-height: 34px;
  border-radius: 9px;
  background: rgba(255, 255, 255, 0.14);
  font-size: 13px;
  font-weight: 700;
  color: #fff !important;
  text-decoration: none;
  transition: background-color 0.15s ease;
}

.es-prof__btn:hover {
  background: rgba(255, 255, 255, 0.24);
}

.es-prof__btn--wa {
  background: #fff;
  color: var(--es-green-700) !important;
}

.es-prof__btn--wa:hover {
  background: var(--es-green-50);
}

/* ---------- Barre du haut ---------- */

.es-top {
  position: fixed;
  top: 0;
  right: 0;
  left: var(--es-side);
  z-index: 30;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  height: var(--es-top);
  padding: 0 28px;
  border-bottom: 1px solid var(--es-line);
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: saturate(1.4) blur(12px);
}

.es-top__left {
  display: flex;
  flex: 1;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.es-top__logo,
.es-top__back,
.es-top__title,
.es-top__icon-btn {
  display: none;
}

.es-top__right {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.es-top__sep {
  width: 1px;
  height: 24px;
  margin: 0 4px;
  background: var(--es-line);
}

/* ---------- Contenu ---------- */

.es-main {
  padding: calc(var(--es-top) + 28px) 32px 64px calc(var(--es-side) + 32px);
}

.es-main__inner {
  max-width: 1120px;
  margin: 0 auto;
}

.es-main__inner--wide {
  max-width: 1240px;
}

.es-subheader {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

/* ---------- Barre d'onglets (téléphone) ---------- */

.es-tabbar {
  display: none;
}

@media (max-width: 1023px) {
  .es-side {
    display: none;
  }

  .es-top {
    left: 0;
    height: 56px;
    padding: 0 10px 0 16px;
  }

  .es-top__search,
  .es-top__sep {
    display: none;
  }

  .es-top__logo {
    display: inline-flex;
  }

  .es-top__logo img {
    width: 92px;
    height: auto;
  }

  .es-top__icon-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 38px;
    border-radius: 10px;
    color: var(--es-ink-soft);
  }

  .es-top__icon-btn svg {
    width: 22px;
    height: 22px;
  }

  .es-top__back {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    margin-left: -8px;
    border-radius: 10px;
    color: var(--es-ink);
  }

  .es-top__back svg {
    width: 22px;
    height: 22px;
  }

  .es-top__back + .es-top__logo {
    display: none;
  }

  .es-top__back ~ .es-top__title {
    display: block;
    overflow: hidden;
    max-width: 52vw;
    font-size: 15px;
    font-weight: 700;
    color: var(--es-ink);
    white-space: nowrap;
    text-overflow: ellipsis;
  }

  .es-main {
    padding: calc(56px + 20px) 16px calc(88px + env(safe-area-inset-bottom)) 16px;
  }

  .es-main--full {
    padding-right: 0;
    padding-left: 0;
  }

  .es-tabbar {
    position: fixed;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 30;
    display: flex;
    justify-content: space-around;
    padding: 6px 4px calc(6px + env(safe-area-inset-bottom));
    border-top: 1px solid var(--es-line);
    background: rgba(255, 255, 255, 0.96);
    backdrop-filter: saturate(1.4) blur(12px);
  }

  .es-tabbar__item {
    display: flex;
    flex: 1;
    flex-direction: column;
    align-items: center;
    gap: 2px;
    min-width: 0;
    padding: 2px;
    font-size: 11px;
    font-weight: 600;
    color: #7a8499;
    text-decoration: none;
  }

  .es-tabbar__pill {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 52px;
    height: 30px;
    border-radius: 999px;
    transition: background-color 0.2s ease;
  }

  .es-tabbar__pill svg {
    width: 23px;
    height: 23px;
  }

  .es-tabbar__item.is-active {
    color: var(--es-navy);
  }

  .es-tabbar__item.is-active .es-tabbar__pill {
    background: var(--es-navy-50);
  }
}
</style>
