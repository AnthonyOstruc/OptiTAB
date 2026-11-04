<template>
  <div ref="racine" class="ec">
    <button
      ref="declencheur"
      type="button"
      class="ec__trigger"
      :aria-expanded="ouvert"
      aria-controls="ec-menu"
      :aria-label="`Mon compte : ${nom}`"
      @click="basculer"
    >
      <span class="ec__avatar" aria-hidden="true">{{ initiales }}</span>
      <span class="ec__name">{{ nom }}</span>
      <ChevronDownIcon class="ec__chev" aria-hidden="true" />
    </button>

    <Transition name="ec-pop">
      <div v-if="ouvert" id="ec-menu" class="ec__menu" @keydown.esc.stop="fermer(true)">
        <div class="ec__head">
          <span class="ec__avatar ec__avatar--lg" aria-hidden="true">{{ initiales }}</span>
          <span class="ec__who">
            <strong>{{ nom }}</strong>
            <span>{{ userStore.email }}</span>
          </span>
        </div>

        <!-- Progression (élèves) -->
        <div v-if="avecNiveau" class="ec__level">
          <div class="ec__level-row">
            <strong>Niveau {{ niveau }}</strong>
            <span>{{ formater(xp) }} XP</span>
          </div>
          <div class="ec__bar" role="progressbar" :aria-valuenow="progression" aria-valuemin="0" aria-valuemax="100" :aria-label="`Progression vers le niveau ${niveau + 1}`">
            <span :style="{ width: progression + '%' }"></span>
          </div>
          <p>Encore {{ formater(xpRestant) }} XP avant le niveau {{ niveau + 1 }}</p>
        </div>

        <nav class="ec__links" aria-label="Mon compte">
          <router-link v-for="lien in liens" :key="lien.to" :to="lien.to" class="ec__link" @click="fermer()">
            <component :is="lien.icon" aria-hidden="true" />
            <span>{{ lien.label }}</span>
          </router-link>
        </nav>

        <button type="button" class="ec__link ec__link--out" :disabled="deconnexionEnCours" @click="seDeconnecter">
          <ArrowRightOnRectangleIcon aria-hidden="true" />
          <span>{{ deconnexionEnCours ? 'Déconnexion…' : 'Se déconnecter' }}</span>
        </button>
      </div>
    </Transition>
  </div>
</template>

<script setup>
// Menu du compte de la barre du haut (espace élève et parent) : avatar et nom ;
// au clic, e-mail, progression, liens du compte et déconnexion.
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  AcademicCapIcon,
  ArrowRightOnRectangleIcon,
  ChevronDownIcon,
  CreditCardIcon,
  ShieldCheckIcon,
  UserCircleIcon
} from '@heroicons/vue/24/outline'
import { useUserStore } from '@/stores/user'
import { useSubscriptionStore } from '@/stores/subscription'
import { logoutUser } from '@/api'
import { initiales as initialesDe } from '@/utils/espaceFormat'
import * as analytics from '@/services/analytics'

const userStore = useUserStore()
const subscriptionStore = useSubscriptionStore()
const route = useRoute()
const router = useRouter()

const ouvert = ref(false)
const deconnexionEnCours = ref(false)
const racine = ref(null)
const declencheur = ref(null)

const nom = computed(() => `${userStore.firstName || ''} ${userStore.lastName || ''}`.trim() || 'Mon compte')
const initiales = computed(() => initialesDe(userStore.firstName, userStore.lastName))

// Niveau n atteint à n² × 10 XP (même règle que le serveur).
const avecNiveau = computed(() => userStore.role !== 'parent')
const niveau = computed(() => Number(userStore.level || 0))
const xp = computed(() => Number(userStore.xp || 0))
const seuilSuivant = computed(() => (niveau.value + 1) ** 2 * 10)
const xpRestant = computed(() => Math.max(0, seuilSuivant.value - xp.value))
const progression = computed(() => {
  const debut = niveau.value ** 2 * 10
  const etendue = Math.max(1, seuilSuivant.value - debut)
  return Math.min(100, Math.max(0, Math.round(((xp.value - debut) / etendue) * 100)))
})
const formater = (n) => new Intl.NumberFormat('fr-FR').format(n)

const liens = computed(() => [
  { label: 'Mon compte', to: '/account', icon: UserCircleIcon },
  { label: 'Abonnement', to: subscriptionStore.hasAccess ? '/subscription' : '/billing', icon: CreditCardIcon },
  { label: 'Cours particuliers', to: '/cours-particuliers', icon: AcademicCapIcon },
  ...(userStore.isAdmin ? [{ label: 'Administration', to: '/admin', icon: ShieldCheckIcon }] : [])
])

function basculer() {
  ouvert.value = !ouvert.value
}

function fermer(rendreLeFocus = false) {
  ouvert.value = false
  if (rendreLeFocus) nextTick(() => declencheur.value?.focus())
}

function clicDehors(e) {
  if (ouvert.value && racine.value && !racine.value.contains(e.target)) fermer()
}

function echap(e) {
  if (e.key === 'Escape' && ouvert.value) fermer(true)
}

watch(() => route.fullPath, () => fermer())

async function seDeconnecter() {
  if (deconnexionEnCours.value) return
  deconnexionEnCours.value = true
  userStore.isLoading = true
  try {
    const refresh = localStorage.getItem('refresh_token')
    if (refresh && refresh !== 'null' && refresh !== 'undefined' && refresh.trim() !== '') {
      await logoutUser({ refresh }).catch((error) => console.log('Erreur lors de la déconnexion backend:', error.message))
    }
  } finally {
    analytics.logout()
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    userStore.clearUser({ preserveLoadingState: true })
    fermer()
    await router.replace({ name: 'Home' }).catch((navError) => console.warn('Redirection post-déconnexion impossible:', navError))
    deconnexionEnCours.value = false
    userStore.isLoading = false
  }
}

onMounted(() => {
  document.addEventListener('pointerdown', clicDehors)
  document.addEventListener('keydown', echap)
})
onBeforeUnmount(() => {
  document.removeEventListener('pointerdown', clicDehors)
  document.removeEventListener('keydown', echap)
})
</script>

<style scoped>
.ec {
  position: relative;
}

.ec__trigger {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  height: 44px;
  padding: 0 10px 0 4px;
  border: 1px solid transparent;
  border-radius: 999px;
  background: none;
  font-family: var(--es-font);
  color: var(--es-ink);
  cursor: pointer;
  transition: background-color 0.15s ease, border-color 0.15s ease;
}

.ec__trigger:hover,
.ec__trigger[aria-expanded='true'] {
  border-color: var(--es-line);
  background: #fff;
}

.ec__avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  border-radius: 50%;
  background: var(--es-navy);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.02em;
  color: #fff;
}

.ec__avatar--lg {
  width: 44px;
  height: 44px;
  font-size: 15px;
}

.ec__name {
  overflow: hidden;
  max-width: 180px;
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.ec__chev {
  width: 16px;
  height: 16px;
  color: var(--es-muted);
  transition: transform 0.2s ease;
}

.ec__trigger[aria-expanded='true'] .ec__chev {
  transform: rotate(180deg);
}

/* ---------- Menu ---------- */

.ec__menu {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  z-index: 60;
  width: 300px;
  padding: 8px;
  border: 1px solid var(--es-line);
  border-radius: var(--es-radius);
  background: #fff;
  box-shadow: var(--es-shadow-lg);
}

.ec__head {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 10px 14px;
}

.ec__who {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.ec__who strong {
  overflow: hidden;
  font-size: 15px;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.ec__who span {
  overflow: hidden;
  font-size: 13px;
  color: var(--es-muted);
  white-space: nowrap;
  text-overflow: ellipsis;
}

.ec__level {
  margin: 0 2px 8px;
  padding: 12px 12px 10px;
  border-radius: var(--es-radius-sm);
  background: var(--es-bg);
}

.ec__level-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  font-size: 13px;
}

.ec__level-row span {
  font-weight: 600;
  color: var(--es-muted);
}

.ec__bar {
  overflow: hidden;
  height: 6px;
  margin: 8px 0 7px;
  border-radius: 999px;
  background: var(--es-navy-100);
}

.ec__bar span {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: var(--es-navy);
  transition: width 0.3s ease;
}

.ec__level p {
  font-size: 12px;
  color: var(--es-muted);
}

.ec__links {
  display: flex;
  flex-direction: column;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--es-line);
}

.ec__link {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  min-height: 42px;
  padding: 0 12px;
  border: 0;
  border-radius: 10px;
  background: none;
  font-family: var(--es-font);
  font-size: 14px;
  font-weight: 600;
  color: var(--es-ink-soft);
  text-align: left;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease;
}

.ec__link svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  color: #8a94a8;
}

.ec__link:hover {
  background: var(--es-bg);
  color: var(--es-ink);
}

.ec__link.router-link-active {
  color: var(--es-navy);
}

.ec__link.router-link-active svg {
  color: var(--es-navy);
}

.ec__link--out {
  margin-top: 6px;
  color: var(--es-red-700);
}

.ec__link--out svg {
  color: var(--es-red-700);
}

.ec__link--out:hover {
  background: #fef3f2;
  color: var(--es-red-700);
}

.ec__link:disabled {
  opacity: 0.6;
  cursor: default;
}

.ec-pop-enter-active,
.ec-pop-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.ec-pop-enter-from,
.ec-pop-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

/* Téléphone : l'avatar seul ; le menu prend la largeur de l'écran. */
@media (max-width: 1023px) {
  .ec__trigger {
    height: 40px;
    padding: 0 2px;
  }

  .ec__trigger:hover,
  .ec__trigger[aria-expanded='true'] {
    border-color: transparent;
    background: none;
  }

  .ec__avatar {
    width: 34px;
    height: 34px;
    font-size: 12.5px;
  }

  .ec__name,
  .ec__chev {
    display: none;
  }

  .ec__menu {
    position: fixed;
    top: 62px;
    right: 10px;
    left: auto;
    width: min(320px, calc(100vw - 20px));
  }
}

@media (prefers-reduced-motion: reduce) {
  .ec-pop-enter-active,
  .ec-pop-leave-active,
  .ec__chev {
    transition: none;
  }
}
</style>
