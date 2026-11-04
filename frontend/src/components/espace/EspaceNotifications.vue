<template>
  <div ref="racine" class="en">
    <button
      ref="declencheur"
      type="button"
      class="en__trigger"
      :aria-expanded="ouvert"
      aria-controls="en-panel"
      :aria-label="nonLues ? `Notifications (${nonLues} non lue${nonLues > 1 ? 's' : ''})` : 'Notifications'"
      @click="basculer"
    >
      <BellIcon aria-hidden="true" />
      <span v-if="nonLues" class="en__badge" aria-hidden="true">{{ nonLues > 9 ? '9+' : nonLues }}</span>
    </button>

    <Transition name="en-pop">
      <section v-if="ouvert" id="en-panel" class="en__panel" aria-label="Notifications" @keydown.esc.stop="fermer(true)">
        <header class="en__head">
          <h2>Notifications</h2>
          <button v-if="nonLues" type="button" class="en__action" @click="toutLire">Tout marquer comme lu</button>
        </header>

        <ul v-if="liste.length" class="en__list">
          <li
            v-for="n in liste"
            :key="n.id"
            :class="['en__item', { 'is-unread': !n.read }]"
          >
            <button type="button" class="en__item-main" @click="lire(n)">
              <span :class="['en__icon', `en__icon--${apparence(n.type).ton}`]" aria-hidden="true">
                <component :is="apparence(n.type).icon" />
              </span>
              <span class="en__text">
                <strong>{{ sansEmoji(n.title) }}</strong>
                <span v-if="n.message">{{ sansEmoji(n.message) }}</span>
                <time :datetime="iso(n.timestamp)">{{ quand(n.timestamp) }}</time>
              </span>
              <span v-if="!n.read" class="en__dot"><span class="es-sr-only">Non lue</span></span>
            </button>
            <button type="button" class="en__remove" :aria-label="`Supprimer : ${sansEmoji(n.title)}`" @click="supprimer(n.id)">
              <XMarkIcon aria-hidden="true" />
            </button>
          </li>
        </ul>

        <div v-else class="en__empty">
          <span class="en__empty-icon" aria-hidden="true"><BellIcon /></span>
          <strong>Aucune notification</strong>
          <p>Les nouveautés et tes progrès apparaîtront ici.</p>
        </div>

        <footer v-if="liste.length" class="en__foot">
          <button type="button" class="en__action en__action--muted" @click="toutEffacer">Tout effacer</button>
        </footer>
      </section>
    </Transition>
  </div>
</template>

<script setup>
// Notifications de la barre du haut (espace élève et parent).
// Mêmes données et mêmes actions que l'ancien centre de notifications.
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import {
  BellIcon,
  CheckCircleIcon,
  LockOpenIcon,
  SparklesIcon,
  StarIcon,
  TrophyIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'
import { useNotificationStore } from '@/stores/notifications'
import { deleteNotification, deleteAllNotifications } from '@/api/users'

const store = useNotificationStore()
const route = useRoute()

const ouvert = ref(false)
const racine = ref(null)
const declencheur = ref(null)

const liste = computed(() => [...store.notifications].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)))
const nonLues = computed(() => store.unreadCount)

const APPARENCES = {
  xp_gained: { icon: SparklesIcon, ton: 'orange' },
  level_up: { icon: TrophyIcon, ton: 'navy' },
  exercise_unlocked: { icon: LockOpenIcon, ton: 'green' },
  chapter_completed: { icon: CheckCircleIcon, ton: 'green' },
  achievement: { icon: StarIcon, ton: 'orange' }
}
const apparence = (type) => APPARENCES[type] || { icon: BellIcon, ton: 'navy' }

// Les anciens titres commencent souvent par un émoji (« 🎉 XP Gagnés ! ») :
// l'icône suffit.
const sansEmoji = (texte) => String(texte || '').replace(/^[\p{Extended_Pictographic}️‍\s]+/u, '')

const iso = (date) => {
  const d = new Date(date)
  return Number.isNaN(d.getTime()) ? '' : d.toISOString()
}

function quand(date) {
  const d = new Date(date)
  const minutes = Math.floor((Date.now() - d.getTime()) / 60000)
  if (Number.isNaN(minutes)) return ''
  if (minutes < 1) return 'À l’instant'
  if (minutes < 60) return `Il y a ${minutes} min`
  const heures = Math.floor(minutes / 60)
  if (heures < 24) return `Il y a ${heures} h`
  const jours = Math.floor(heures / 24)
  if (jours < 7) return jours === 1 ? 'Hier' : `Il y a ${jours} jours`
  return d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long' })
}

function basculer() {
  ouvert.value = !ouvert.value
}

function fermer(rendreLeFocus = false) {
  ouvert.value = false
  if (rendreLeFocus) nextTick(() => declencheur.value?.focus())
}

async function lire(n) {
  if (!n.read) await store.markAsRead(n.id)
}

function toutLire() {
  store.markAllAsRead()
}

async function supprimer(id) {
  store.removeNotification(id)
  try {
    await deleteNotification(id)
  } catch (_) {}
}

async function toutEffacer() {
  store.clearAll()
  try {
    await deleteAllNotifications()
  } catch (_) {}
}

function clicDehors(e) {
  if (ouvert.value && racine.value && !racine.value.contains(e.target)) fermer()
}

function echap(e) {
  if (e.key === 'Escape' && ouvert.value) fermer(true)
}

watch(() => route.fullPath, () => fermer())

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
.en {
  position: relative;
}

.en__trigger {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: 1px solid transparent;
  border-radius: 12px;
  background: none;
  color: var(--es-ink-soft);
  cursor: pointer;
  transition: background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease;
}

.en__trigger svg {
  width: 22px;
  height: 22px;
}

.en__trigger:hover,
.en__trigger[aria-expanded='true'] {
  border-color: var(--es-line);
  background: #fff;
  color: var(--es-ink);
}

.en__badge {
  position: absolute;
  top: 5px;
  left: 21px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 8px;
  height: 14px;
  padding: 0 3px;
  border: 2px solid #fff;
  border-radius: 999px;
  background: #d92d20;
  font-family: var(--es-font);
  font-size: 9.5px;
  font-weight: 700;
  line-height: 1;
  color: #fff;
  box-sizing: content-box;
}

/* ---------- Panneau ---------- */

.en__panel {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  z-index: 60;
  display: flex;
  flex-direction: column;
  width: 380px;
  max-height: min(520px, calc(100vh - 100px));
  border: 1px solid var(--es-line);
  border-radius: var(--es-radius);
  background: #fff;
  box-shadow: var(--es-shadow-lg);
  overflow: hidden;
}

.en__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px 12px;
  border-bottom: 1px solid var(--es-line);
}

.en__head h2 {
  font-size: 15px;
  font-weight: 700;
}

.en__action {
  padding: 4px 6px;
  border: 0;
  border-radius: 8px;
  background: none;
  font-family: var(--es-font);
  font-size: 13px;
  font-weight: 600;
  color: var(--es-navy);
  cursor: pointer;
}

.en__action:hover {
  background: var(--es-navy-50);
}

.en__action--muted {
  color: var(--es-muted);
}

.en__action--muted:hover {
  background: var(--es-bg);
  color: var(--es-ink);
}

.en__list {
  flex: 1;
  margin: 0;
  padding: 6px;
  overflow-y: auto;
  list-style: none;
  overscroll-behavior: contain;
  scrollbar-width: thin;
}

.en__item {
  position: relative;
  border-radius: 12px;
}

.en__item + .en__item {
  margin-top: 2px;
}

.en__item-main {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  width: 100%;
  padding: 10px 40px 10px 10px;
  border: 0;
  border-radius: 12px;
  background: none;
  font-family: var(--es-font);
  text-align: left;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.en__item-main:hover {
  background: var(--es-bg);
}

.en__item.is-unread .en__item-main {
  background: var(--es-navy-50);
}

.en__item.is-unread .en__item-main:hover {
  background: var(--es-navy-100);
}

.en__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  flex-shrink: 0;
  border-radius: 10px;
}

.en__icon svg {
  width: 18px;
  height: 18px;
}

.en__icon--navy {
  background: var(--es-navy-100);
  color: var(--es-navy);
}

.en__icon--green {
  background: var(--es-green-50);
  color: var(--es-green-700);
}

.en__icon--orange {
  background: var(--es-orange-50);
  color: var(--es-orange-700);
}

.en__text {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.en__text strong {
  font-size: 14px;
  font-weight: 600;
  line-height: 1.35;
  color: var(--es-ink);
}

.en__text span {
  font-size: 13px;
  line-height: 1.45;
  color: var(--es-ink-soft);
  overflow-wrap: anywhere;
}

.en__text time {
  margin-top: 2px;
  font-size: 12px;
  color: var(--es-muted);
}

.en__dot {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--es-navy);
}

.en__remove {
  position: absolute;
  top: 6px;
  right: 6px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border: 0;
  border-radius: 8px;
  background: none;
  color: var(--es-muted);
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.15s ease, background-color 0.15s ease;
}

.en__remove svg {
  width: 16px;
  height: 16px;
}

.en__item:hover .en__remove,
.en__remove:focus-visible {
  opacity: 1;
}

.en__item:hover .en__dot {
  opacity: 0;
}

.en__remove:hover {
  background: #fff;
  color: var(--es-red-700);
}

.en__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 32px 24px 36px;
  text-align: center;
}

.en__empty-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  margin-bottom: 8px;
  border-radius: 50%;
  background: var(--es-bg);
  color: #98a2b3;
}

.en__empty-icon svg {
  width: 24px;
  height: 24px;
}

.en__empty strong {
  font-size: 14px;
}

.en__empty p {
  font-size: 13px;
  color: var(--es-muted);
}

.en__foot {
  display: flex;
  justify-content: flex-end;
  padding: 8px 10px;
  border-top: 1px solid var(--es-line);
}

.en-pop-enter-active,
.en-pop-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.en-pop-enter-from,
.en-pop-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

/* Écrans tactiles : la croix de suppression reste visible. */
@media (hover: none) {
  .en__remove {
    opacity: 1;
  }

  .en__dot {
    right: 44px;
  }
}

/* Téléphone : panneau sur toute la largeur, sous la barre du haut. */
@media (max-width: 1023px) {
  .en__trigger {
    width: 38px;
    height: 38px;
  }

  .en__trigger:hover,
  .en__trigger[aria-expanded='true'] {
    border-color: transparent;
    background: var(--es-bg);
  }

  .en__panel {
    position: fixed;
    top: 62px;
    right: 10px;
    left: 10px;
    width: auto;
    max-height: calc(100vh - 62px - 96px);
  }
}

@media (prefers-reduced-motion: reduce) {
  .en-pop-enter-active,
  .en-pop-leave-active {
    transition: none;
  }
}
</style>
