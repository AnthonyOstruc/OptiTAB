<template>
  <div class="ap">
    <p v-if="exemple" class="es-demo-banner">
      <SparklesIcon width="18" height="18" aria-hidden="true" />
      Aperçu de l’espace parent avec un enfant d’exemple.
    </p>

    <header class="es-page-head">
      <div>
        <h1 class="es-h1">Bonjour {{ prenom }}</h1>
        <p class="es-sub">Le travail de vos enfants, semaine après semaine.</p>
      </div>
      <button type="button" class="es-btn es-btn--ghost" @click="ouvrirAjout">
        <UserPlusIcon aria-hidden="true" />
        Ajouter un enfant
      </button>
    </header>

    <div v-if="loading" class="es-card ap-child">
      <div class="es-skeleton" style="height: 56px; width: 50%"></div>
      <div class="es-skeleton" style="height: 160px; margin-top: 20px"></div>
    </div>

    <!-- Un bloc par enfant -->
    <article v-for="enfant in enfants" :key="enfant.id" class="es-card ap-child" :aria-label="`Suivi de ${enfant.first_name}`">
      <header class="ap-child__head">
        <span class="ap-avatar" aria-hidden="true">{{ initiales(enfant.first_name, enfant.last_name) }}</span>
        <div class="ap-child__id">
          <h2 class="es-h2">{{ enfant.first_name }} {{ enfant.last_name }}</h2>
          <p>
            <span v-if="enfant.niveau" class="es-pill es-pill--progress es-pill--plain">{{ enfant.niveau }}</span>
            <span class="ap-child__last">{{ derniereActivite(enfant) }}</span>
          </p>
        </div>
        <router-link v-if="!exemple" :to="`/child/${enfant.id}`" class="es-link ap-child__more">
          Historique détaillé
          <ChevronRightIcon aria-hidden="true" />
        </router-link>
      </header>

      <p :class="['ap-insight', `ap-insight--${synthese(enfant).ton}`]">
        <component :is="synthese(enfant).icone" aria-hidden="true" />
        <span>{{ synthese(enfant).texte }}</span>
      </p>

      <div class="ap-grid">
        <section class="ap-block" :aria-label="`Semaine de ${enfant.first_name}`">
          <h3 class="ap-block__title">Cette semaine</h3>
          <div class="ap-week">
            <ProgressRing :value="enfant.metrics.weekly_done" :max="OBJECTIF_SEMAINE" :size="84" :epaisseur="8">
              <strong class="ap-ring__num">{{ enfant.metrics.weekly_done }}</strong>
              <span class="ap-ring__of">sur {{ OBJECTIF_SEMAINE }}</span>
            </ProgressRing>
            <WeekBars :trend="details[enfant.id]?.trend || []" />
          </div>
        </section>

        <section class="ap-block" :aria-label="`Résultats de ${enfant.first_name}`">
          <h3 class="ap-block__title">Depuis le début</h3>
          <dl class="ap-kpis">
            <div>
              <dt>Exercices faits</dt>
              <dd>{{ enfant.metrics.done_total }}</dd>
            </div>
            <div>
              <dt>Acquis</dt>
              <dd class="ap-ok">{{ enfant.metrics.acquired_count }}</dd>
            </div>
            <div>
              <dt>À revoir</dt>
              <dd class="ap-review">{{ enfant.metrics.not_acquired_count }}</dd>
            </div>
            <div>
              <dt>Réussite</dt>
              <dd>{{ pourcent(enfant.metrics.acquired_count, enfant.metrics.done_total) }}&nbsp;%</dd>
            </div>
          </dl>
        </section>

        <section class="ap-block ap-block--wide" :aria-label="`Chapitres travaillés par ${enfant.first_name}`">
          <h3 class="ap-block__title">Chapitres travaillés</h3>
          <ul v-if="chapitresTravailles(enfant).length" class="ap-chaps">
            <li v-for="c in chapitresTravailles(enfant)" :key="c.id">
              <span class="ap-chaps__title">{{ c.titre }}</span>
              <span class="ap-chaps__bar">
                <span class="es-bar">
                  <span class="es-bar__ok" :style="{ width: pourcent(c.acquis, c.exercices) + '%' }"></span>
                  <span class="es-bar__review" :style="{ width: pourcent(c.a_revoir, c.exercices) + '%' }"></span>
                </span>
                <span class="ap-chaps__count">{{ c.acquis }}/{{ c.exercices }}</span>
              </span>
            </li>
          </ul>
          <p v-else class="ap-muted">Aucun chapitre commencé pour l’instant.</p>
        </section>

        <section class="ap-block ap-block--wide" :aria-label="`Points à revoir de ${enfant.first_name}`">
          <h3 class="ap-block__title">Points à revoir</h3>
          <ul v-if="(details[enfant.id]?.aRevoir || []).length" class="ap-review-list">
            <li v-for="(item, i) in details[enfant.id].aRevoir.slice(0, 3)" :key="i">
              <span class="ap-review-list__dot" aria-hidden="true"></span>
              <span>
                <strong>{{ titreCourt(item.exercice) }}</strong>
                <span>{{ item.notion }}</span>
              </span>
            </li>
          </ul>
          <p v-else class="ap-muted">Rien à revoir : tous les exercices faits sont compris.</p>
        </section>
      </div>
    </article>

    <!-- Invitations en attente / refusées -->
    <section v-if="enAttente.length || refusees.length" class="es-card ap-pending">
      <h2 class="es-h2">Demandes de suivi</h2>
      <ul>
        <li v-for="inv in enAttente" :key="`p-${inv.link_id}`">
          <ClockIcon aria-hidden="true" />
          <span><strong>{{ inv.first_name }} {{ inv.last_name }}</strong> ({{ inv.email }}) doit accepter la demande depuis son espace.</span>
          <button type="button" class="es-btn es-btn--sm es-btn--ghost" :disabled="retraitEnCours === inv.child_id" @click="annuler(inv)">Annuler</button>
        </li>
        <li v-for="inv in refusees" :key="`d-${inv.link_id}`" class="ap-pending--declined">
          <XCircleIcon aria-hidden="true" />
          <span><strong>{{ inv.first_name }} {{ inv.last_name }}</strong> a refusé la demande de suivi.</span>
          <button type="button" class="es-btn es-btn--sm es-btn--ghost" :disabled="retraitEnCours === inv.child_id" @click="annuler(inv)">Retirer</button>
        </li>
      </ul>
    </section>

    <!-- Ajouter un enfant -->
    <section id="ajouter-enfant" ref="ajoutRef" :class="['es-card', 'ap-add', { 'ap-add--empty': !loading && !enfants.length }]">
      <div class="ap-add__text">
        <h2 class="es-h2">{{ enfants.length ? 'Ajouter un autre enfant' : 'Ajoutez votre enfant pour suivre son travail' }}</h2>
      </div>
      <div class="ap-add__modes" role="tablist" aria-label="Ajouter un enfant">
        <button type="button" role="tab" :aria-selected="mode === 'inviter'" :class="['ap-add__mode', { 'is-active': mode === 'inviter' }]" @click="mode = 'inviter'">Il a déjà un compte</button>
        <button type="button" role="tab" :aria-selected="mode === 'creer'" :class="['ap-add__mode', { 'is-active': mode === 'creer' }]" @click="mode = 'creer'">Créer son compte</button>
      </div>

      <template v-if="mode === 'inviter'">
        <p class="ap-add__hint">Indiquez l’adresse e-mail de son compte OptiTAB. Il reçoit une demande dans son espace et l’accepte en un clic.</p>
        <form class="ap-add__form" @submit.prevent="ajouter">
          <label class="es-sr-only" for="ap-email">E-mail de l’élève</label>
          <input id="ap-email" ref="emailRef" v-model.trim="email" type="email" placeholder="email.eleve@exemple.fr" autocomplete="off" :disabled="exemple" required />
          <button type="submit" class="es-btn" :disabled="ajoutEnCours || exemple">Envoyer la demande</button>
        </form>
      </template>

      <template v-else>
        <p class="ap-add__hint">Votre enfant n’a pas encore de compte&nbsp;? Créez-le ici : il est aussitôt lié au vôtre. Un mot de passe provisoire s’affiche pour sa première connexion.</p>
        <form class="ap-add__grid" @submit.prevent="creer">
          <label class="es-sr-only" for="ap-prenom">Prénom</label>
          <input id="ap-prenom" v-model.trim="nouveau.first_name" type="text" placeholder="Prénom" autocomplete="off" :disabled="exemple" required />
          <label class="es-sr-only" for="ap-nom">Nom</label>
          <input id="ap-nom" v-model.trim="nouveau.last_name" type="text" placeholder="Nom" autocomplete="off" :disabled="exemple" required />
          <label class="es-sr-only" for="ap-email2">E-mail de l’élève</label>
          <input id="ap-email2" v-model.trim="nouveau.email" type="email" placeholder="email.eleve@exemple.fr" autocomplete="off" :disabled="exemple" required />
          <button type="submit" class="es-btn" :disabled="ajoutEnCours || exemple">Créer le compte</button>
        </form>
        <p class="ap-add__note">Pas d’adresse e-mail pour votre enfant&nbsp;? <router-link to="/contact?sujet=Une%20question%20sur%20la%20plateforme">Écrivez-nous</router-link>, nous créons le compte avec vous.</p>
        <p v-if="motDePasse" class="ap-add__pwd" role="status">
          Mot de passe provisoire : <code>{{ motDePasse }}</code>
          <span>Notez-le : il ne sera plus affiché. Votre enfant pourra le changer dans Mon compte.</span>
        </p>
      </template>
      <p v-if="messageAjout" :class="['ap-add__msg', { 'is-error': erreurAjout }]" role="status">{{ messageAjout }}</p>
    </section>

    <section class="es-card ap-help">
      <AcademicCapIcon class="ap-help__icon" aria-hidden="true" />
      <div>
        <h2 class="es-h2">Besoin d’un coup de pouce sur un chapitre&nbsp;?</h2>
        <p>Cours particuliers en visio avec un professeur, du collège à la prépa. Premier échange gratuit.</p>
      </div>
      <router-link to="/cours-particuliers" class="es-btn es-btn--ghost">Découvrir</router-link>
    </section>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, reactive, ref } from 'vue'
import {
  AcademicCapIcon,
  CheckBadgeIcon,
  ChevronRightIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  LightBulbIcon,
  SparklesIcon,
  UserPlusIcon,
  XCircleIcon
} from '@heroicons/vue/24/outline'
import ProgressRing from './ProgressRing.vue'
import WeekBars from './WeekBars.vue'
import { getChildOverview, getChildProgression, getMyProgression } from '@/api/progression'
import { addChild, createChildAccount, fetchMyChildren, removeChild } from '@/api/users'
import { useUserStore } from '@/stores/user'
import { OBJECTIF_SEMAINE, appliquerExemple, enfantsExemple, overviewExemple } from '@/config/espace'
import { depuis, initiales, joursDepuis, pluriel, pourcent } from '@/utils/espaceFormat'

const props = defineProps({
  exemple: { type: Boolean, default: false }
})

const userStore = useUserStore()
const prenom = computed(() => userStore.firstName || '')

const loading = ref(true)
const enfants = ref([])
const enAttente = ref([])
// id enfant -> { trend, chapitres, aRevoir }
const details = reactive({})

const titreCourt = (titre = '') => titre.replace(/^(Découverte|Entraînement|Problème|Approfondissement|Synthèse|Bilan|Type concours|Type brevet|Type bac|Type examen|DS)\s*[-–]\s*/i, '')

function derniereActivite(enfant) {
  const last = enfant.last_activity
  if (!last?.when) return 'Pas encore d’activité'
  return `Dernière activité ${depuis(last.when)}${last.chapitre_title ? ` · ${last.chapitre_title}` : ''}`
}

function joursActifs(enfant) {
  return (details[enfant.id]?.trend || []).filter((d) => d.total > 0).length
}

// Une phrase claire pour le parent, en fonction de la situation.
function synthese(enfant) {
  const m = enfant.metrics || {}
  const prenomEnfant = enfant.first_name || 'Votre enfant'
  const inactif = joursDepuis(enfant.last_activity?.when)
  if (!m.done_total) {
    return { ton: 'info', icone: LightBulbIcon, texte: `${prenomEnfant} n’a pas encore commencé. Un premier cours et quelques exercices suffisent pour lancer la semaine.` }
  }
  if (inactif !== null && inactif >= 7) {
    return { ton: 'warn', icone: ExclamationTriangleIcon, texte: `Aucune activité depuis ${pluriel(inactif, 'jour')}. Un petit rappel peut aider ${prenomEnfant} à reprendre.` }
  }
  if (m.weekly_done >= OBJECTIF_SEMAINE) {
    return { ton: 'ok', icone: CheckBadgeIcon, texte: `Objectif de la semaine atteint : ${pluriel(m.weekly_done, 'exercice')} en ${pluriel(joursActifs(enfant), 'jour')}. Bravo !` }
  }
  return {
    ton: 'info',
    icone: LightBulbIcon,
    texte: `${prenomEnfant} a fait ${pluriel(m.weekly_done || 0, 'exercice')} cette semaine, sur ${pluriel(joursActifs(enfant), 'jour')}. Objectif : ${OBJECTIF_SEMAINE}.`
  }
}

function chapitresTravailles(enfant) {
  return (details[enfant.id]?.chapitres || [])
    .filter((c) => c.faits > 0)
    .sort((a, b) => String(b.derniere_activite || '').localeCompare(String(a.derniere_activite || '')))
    .slice(0, 4)
}

// ---------- Ajouter un enfant (inviter un compte existant ou créer son compte) ----------
const ajoutRef = ref(null)
const emailRef = ref(null)
const mode = ref('inviter')
const email = ref('')
const nouveau = reactive({ first_name: '', last_name: '', email: '' })
const motDePasse = ref('')
const ajoutEnCours = ref(false)
const messageAjout = ref('')
const erreurAjout = ref(false)
const refusees = ref([])
const retraitEnCours = ref(null)

async function creer() {
  ajoutEnCours.value = true
  erreurAjout.value = false
  motDePasse.value = ''
  try {
    const res = await createChildAccount({
      first_name: nouveau.first_name,
      last_name: nouveau.last_name,
      email: nouveau.email.toLowerCase()
    })
    motDePasse.value = res?.data?.data?.temp_password || ''
    messageAjout.value = 'Compte créé et lié au vôtre.'
    Object.assign(nouveau, { first_name: '', last_name: '', email: '' })
    await charger()
  } catch (e) {
    erreurAjout.value = true
    messageAjout.value = e?.response?.data?.message || 'Création impossible : cette adresse e-mail est peut-être déjà utilisée.'
  } finally {
    ajoutEnCours.value = false
  }
}

// Annuler une demande en attente, ou retirer une demande refusée.
async function annuler(inv) {
  retraitEnCours.value = inv.child_id
  try {
    await removeChild(inv.child_id)
    await charger()
  } catch {
    // La liste reste affichée : le parent pourra réessayer.
  } finally {
    retraitEnCours.value = null
  }
}

async function ouvrirAjout() {
  ajoutRef.value?.scrollIntoView({ behavior: 'smooth', block: 'center' })
  await nextTick()
  setTimeout(() => emailRef.value?.focus({ preventScroll: true }), 350)
}

async function ajouter() {
  if (!email.value) return
  ajoutEnCours.value = true
  erreurAjout.value = false
  try {
    const res = await addChild({ email: email.value })
    messageAjout.value = res?.data?.message || 'Demande envoyée. Elle apparaît dans l’espace de votre enfant.'
    email.value = ''
    await charger()
  } catch (e) {
    erreurAjout.value = true
    messageAjout.value = e?.response?.data?.message || 'Impossible d’envoyer la demande pour cette adresse.'
  } finally {
    ajoutEnCours.value = false
  }
}

// ---------- Chargement ----------
async function charger() {
  if (props.exemple) {
    enfants.value = enfantsExemple()
    enAttente.value = []
    const prog = await getMyProgression().catch(() => null)
    const exemple = appliquerExemple(prog?.data?.data)
    details.exemple = { trend: overviewExemple().weekly_trend, chapitres: exemple.chapitres, aRevoir: exemple.a_revoir }
    return
  }
  const res = await fetchMyChildren().catch(() => null)
  const data = res?.data?.data || {}
  enfants.value = data.children || []
  enAttente.value = data.pending_invitations || []
  refusees.value = data.declined_invitations || []
  await Promise.all(enfants.value.map(async (enfant) => {
    const [ov, prog] = await Promise.allSettled([getChildOverview(enfant.id), getChildProgression(enfant.id)])
    const ovData = ov.status === 'fulfilled' ? ov.value?.data?.data : null
    const progData = prog.status === 'fulfilled' ? prog.value?.data?.data : null
    details[enfant.id] = {
      trend: ovData?.weekly_trend || [],
      chapitres: progData?.chapitres || [],
      aRevoir: progData?.a_revoir || []
    }
  }))
}

onMounted(async () => {
  await charger()
  loading.value = false
})
</script>

<style scoped>
.ap-child {
  margin-bottom: 20px;
  padding: 24px;
}

.ap-child__head {
  display: flex;
  align-items: center;
  gap: 16px;
}

.ap-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 52px;
  height: 52px;
  flex-shrink: 0;
  border-radius: 16px;
  background: var(--es-navy);
  font-size: 18px;
  font-weight: 700;
  color: #fff;
}

.ap-child__id {
  flex: 1;
  min-width: 0;
}

.ap-child__id p {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-top: 4px !important;
}

.ap-child__last {
  font-size: 14px;
  color: var(--es-muted);
}

.ap-insight {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin: 18px 0 4px !important;
  padding: 12px 14px;
  border-radius: 12px;
  background: var(--es-navy-50);
  font-size: 15px;
  font-weight: 600;
  line-height: 1.45;
  color: var(--es-navy);
}

.ap-insight svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  margin-top: 1px;
}

.ap-insight--ok {
  background: var(--es-green-50);
  color: var(--es-green-700);
}

.ap-insight--warn {
  background: var(--es-orange-50);
  color: var(--es-orange-700);
}

.ap-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0 32px;
}

.ap-block {
  padding-top: 18px;
  margin-top: 18px;
  border-top: 1px solid var(--es-line);
}

.ap-block__title {
  margin-bottom: 14px !important;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--es-muted);
}

.ap-week {
  display: flex;
  align-items: center;
  gap: 20px;
}

.ap-week .wb {
  flex: 1;
}

.ap-ring__num {
  font-size: 22px;
  font-weight: 700;
  line-height: 1;
}

.ap-ring__of {
  font-size: 11px;
  color: var(--es-muted);
}

.ap-kpis {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin: 0;
}

.ap-kpis div {
  padding: 12px 14px;
  border-radius: 12px;
  background: var(--es-bg);
}

.ap-kpis dt {
  font-size: 13px;
  color: var(--es-muted);
}

.ap-kpis dd {
  margin: 2px 0 0;
  font-size: 22px;
  font-weight: 700;
  color: var(--es-ink);
}

.ap-kpis .ap-ok {
  color: var(--es-green-700);
}

.ap-kpis .ap-review {
  color: var(--es-orange-700);
}

.ap-chaps,
.ap-review-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.ap-chaps li {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.ap-chaps__title {
  font-size: 14px;
  font-weight: 600;
  color: var(--es-ink);
}

.ap-chaps__bar {
  display: flex;
  align-items: center;
  gap: 10px;
}

.ap-chaps__bar .es-bar {
  flex: 1;
}

.ap-chaps__count {
  font-size: 12px;
  font-weight: 700;
  color: var(--es-muted);
}

.ap-review-list li {
  display: flex;
  gap: 10px;
}

.ap-review-list__dot {
  width: 8px;
  height: 8px;
  flex-shrink: 0;
  margin-top: 7px;
  border-radius: 50%;
  background: var(--es-orange);
}

.ap-review-list li > span:last-child {
  display: flex;
  flex-direction: column;
  font-size: 13px;
  color: var(--es-muted);
}

.ap-review-list strong {
  font-size: 14px;
  font-weight: 600;
  color: var(--es-ink);
}

.ap-muted {
  font-size: 14px;
  color: var(--es-muted);
}

/* ---------- Attente, ajout, aide ---------- */

.ap-pending {
  margin-bottom: 20px;
  padding: 20px 24px;
}

.ap-pending ul {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 12px 0 0;
  padding: 0;
  list-style: none;
}

.ap-pending li {
  display: flex;
  gap: 10px;
  font-size: 14px;
  color: var(--es-muted);
}

.ap-pending svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  color: var(--es-orange-700);
}

.ap-pending strong {
  color: var(--es-ink);
}

.ap-add {
  margin-bottom: 20px;
  padding: 24px;
}

.ap-add--empty {
  border: 2px dashed var(--es-navy-100);
  box-shadow: none;
}

.ap-add__text p {
  max-width: 640px;
  margin-top: 6px !important;
  font-size: 15px;
  color: var(--es-muted);
}

.ap-add__form {
  display: flex;
  gap: 10px;
  max-width: 560px;
  margin-top: 16px;
}

.ap-add__form input {
  flex: 1;
  min-width: 0;
  min-height: 44px;
  padding: 0 14px;
  border: 1px solid var(--es-line-strong);
  border-radius: 12px;
  font: 500 16px var(--es-font);
  color: var(--es-ink);
}

.ap-add__form input:focus {
  border-color: var(--es-navy);
  outline: 3px solid rgba(27, 60, 142, 0.15);
}

.ap-add__modes {
  display: inline-flex;
  gap: 2px;
  margin-top: 14px;
  padding: 4px;
  border-radius: 12px;
  background: #e9edf5;
}

.ap-add__mode {
  min-height: 36px;
  padding: 0 14px;
  border: 0;
  border-radius: 9px;
  background: transparent;
  font: 600 14px var(--es-font);
  color: var(--es-ink-soft);
  cursor: pointer;
}

.ap-add__mode.is-active {
  background: #fff;
  color: var(--es-navy);
  box-shadow: 0 1px 3px rgba(16, 24, 40, 0.12);
}

.es .ap-add__hint {
  max-width: 640px;
  margin-top: 12px;
  font-size: 15px;
  color: var(--es-muted);
}

.ap-add__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  max-width: 560px;
  margin-top: 16px;
}

.ap-add__grid input {
  min-width: 0;
  min-height: 44px;
  padding: 0 14px;
  border: 1px solid var(--es-line-strong);
  border-radius: 12px;
  font: 500 16px var(--es-font);
  color: var(--es-ink);
}

.ap-add__grid input:focus {
  border-color: var(--es-navy);
  outline: 3px solid rgba(27, 60, 142, 0.15);
}

.ap-add__grid input[type='email'] {
  grid-column: 1 / -1;
}

.ap-add__grid .es-btn {
  grid-column: 1 / -1;
  justify-self: start;
}

.es .ap-add__note {
  margin-top: 12px;
  font-size: 13px;
  color: var(--es-muted);
}

.ap-add__note a {
  font-weight: 600;
  color: var(--es-navy);
}

.es .ap-add__pwd {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px 10px;
  max-width: 560px;
  margin-top: 14px;
  padding: 12px 14px;
  border: 1px solid #cfe5cf;
  border-radius: 12px;
  background: var(--es-green-50);
  font-size: 14px;
  font-weight: 600;
  color: var(--es-green-700);
}

.ap-add__pwd code {
  padding: 2px 8px;
  border-radius: 6px;
  background: #fff;
  font-size: 15px;
  color: var(--es-ink);
}

.ap-add__pwd span {
  flex-basis: 100%;
  font-weight: 500;
  color: var(--es-ink-soft);
}

.ap-pending li {
  align-items: center;
}

.ap-pending li > span {
  flex: 1;
}

.ap-pending--declined svg {
  color: var(--es-red-700) !important;
}

.ap-add__msg {
  margin-top: 10px !important;
  font-size: 14px;
  font-weight: 600;
  color: var(--es-green-700);
}

.ap-add__msg.is-error {
  color: var(--es-red-700);
}

.ap-help {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
}

.ap-help > div {
  flex: 1;
}

.ap-help p {
  margin-top: 4px !important;
  font-size: 14px;
  color: var(--es-muted);
}

.ap-help__icon {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  padding: 10px;
  border-radius: 12px;
  background: var(--es-green-50);
  color: var(--es-green-700);
}

@media (max-width: 900px) {
  .ap-grid {
    grid-template-columns: minmax(0, 1fr);
  }
}

@media (max-width: 640px) {
  .ap-child,
  .ap-add {
    padding: 18px 16px;
  }

  .ap-child__head {
    flex-wrap: wrap;
  }

  .ap-child__more {
    width: 100%;
  }

  .ap-week {
    flex-direction: column;
    align-items: stretch;
  }

  .ap-week .ring {
    align-self: center;
  }

  .ap-add__form {
    flex-direction: column;
  }

  .ap-add__modes {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    width: 100%;
  }

  .ap-add__grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .ap-add__grid .es-btn {
    justify-self: stretch;
  }

  .ap-pending li {
    flex-wrap: wrap;
  }

  .ap-pending li > span {
    flex-basis: calc(100% - 30px);
  }

  .ap-help {
    flex-wrap: wrap;
  }

  .ap-help .es-btn {
    width: 100%;
  }
}
</style>
