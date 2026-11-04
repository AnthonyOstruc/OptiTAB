<template>
  <div class="ae">
    <p v-if="exemple" class="es-demo-banner">
      <SparklesIcon aria-hidden="true" />
      Aperçu avec des données d’exemple : le compte démo n’a encore fait aucun exercice.
    </p>

    <!-- Demande d'un parent -->
    <div v-for="inv in invitations" :key="inv.link_id" class="es-card ae-banner" role="status">
      <span class="ae-banner__icon"><UserGroupIcon aria-hidden="true" /></span>
      <div class="ae-banner__text">
        <strong>{{ inv.parent_display_name }} souhaite suivre ta progression</strong>
        <span>{{ inv.parent_email }} pourra voir tes exercices et tes progrès, sans rien modifier.</span>
      </div>
      <div class="ae-banner__actions">
        <button type="button" class="es-btn es-btn--sm es-btn--green" :disabled="!!invitationEnCours" @click="repondre(inv, 'accept')">Accepter</button>
        <button type="button" class="es-btn es-btn--sm es-btn--ghost" :disabled="!!invitationEnCours" @click="repondre(inv, 'decline')">Refuser</button>
      </div>
    </div>

    <header class="es-page-head ae-head">
      <div>
        <p class="ae-date">{{ dateDuJour() }}</p>
        <h1 class="es-h1 ae-hello">{{ salut }}, {{ prenom }}</h1>
        <p class="es-sub">{{ sousTitre }}</p>
      </div>
      <div class="ae-head__right">
        <span v-if="serie > 0" class="ae-chip ae-chip--fire" :title="`Connecté ${serie} jours de suite`">
          <FireIcon aria-hidden="true" />
          {{ serie }} {{ serie > 1 ? 'jours de suite' : 'jour' }}
        </span>
        <router-link :to="ESPACE_ROUTES.chapitres" class="es-btn es-btn--ghost">
          <BookOpenIcon aria-hidden="true" />
          Tous mes chapitres
        </router-link>
      </div>
    </header>

    <!-- Abonnement -->
    <div v-if="afficherAbonnement" class="es-card ae-banner ae-banner--sub">
      <span class="ae-banner__icon"><LockOpenIcon aria-hidden="true" /></span>
      <div class="ae-banner__text">
        <strong>Débloque toute la {{ classe || 'classe' }}</strong>
        <span>Tous les cours, fiches et exercices corrigés pas à pas. Sans engagement.</span>
      </div>
      <router-link to="/billing" class="es-btn es-btn--green" data-cta-name="subscribe" data-cta-location="espace_accueil">Voir les formules</router-link>
    </div>

    <div class="ae-grid">
      <!-- Reprendre -->
      <section class="ae-hero es-grid-bg" aria-labelledby="ae-hero-title">
        <template v-if="loading">
          <div class="es-skeleton ae-sk" style="width: 40%"></div>
          <div class="es-skeleton ae-sk" style="width: 70%; height: 30px; margin-top: 14px"></div>
          <div class="es-skeleton ae-sk" style="width: 50%; margin-top: 14px"></div>
        </template>
        <template v-else-if="reprise">
          <div class="ae-hero__main">
            <p class="ae-hero__kicker">{{ reprise.dejaCommence ? 'Reprendre où tu t’es arrêté' : 'Pour bien commencer' }}</p>
            <span class="ae-hero__theme">
              <component :is="reprise.visuel.icone" aria-hidden="true" />
              {{ reprise.chapitre.theme }}
            </span>
            <h2 id="ae-hero-title" class="ae-hero__title">{{ reprise.chapitre.titre }}</h2>
            <p class="ae-hero__meta">
              <template v-if="reprise.quand">Dernière activité {{ depuis(reprise.quand) }}</template>
              <template v-else>Lis le cours, relis la fiche, puis entraîne-toi sur les exercices corrigés.</template>
            </p>
            <div class="ae-hero__actions">
              <router-link :to="chapitreLink(reprise.chapitre.id, reprise.dejaCommence ? 'exercices' : 'cours')" class="es-btn es-btn--light ae-hero__cta">
                <PlayIcon aria-hidden="true" />
                {{ reprise.dejaCommence ? 'Continuer les exercices' : 'Commencer le chapitre' }}
              </router-link>
              <router-link :to="chapitreLink(reprise.chapitre.id, reprise.dejaCommence ? 'cours' : 'fiche')" class="es-btn es-btn--on-dark">
                {{ reprise.dejaCommence ? 'Revoir le cours' : 'Voir la fiche' }}
              </router-link>
            </div>
          </div>
          <div v-if="reprise.chapitre.exercices" class="ae-hero__ring">
            <ProgressRing :value="reprise.chapitre.acquis" :max="reprise.chapitre.exercices" :size="148" :epaisseur="12" class="ae-ring--dark">
              <strong class="ae-hero__pct">{{ pourcent(reprise.chapitre.acquis, reprise.chapitre.exercices) }}<small>%</small></strong>
              <span class="ae-hero__pct-label">acquis</span>
            </ProgressRing>
            <ul class="ae-hero__legend">
              <li><i class="ae-dot ae-dot--ok"></i>{{ reprise.chapitre.acquis }} acquis</li>
              <li><i class="ae-dot ae-dot--review"></i>{{ reprise.chapitre.a_revoir }} à revoir</li>
              <li><i class="ae-dot"></i>{{ Math.max(0, reprise.chapitre.exercices - reprise.chapitre.faits) }} à faire</li>
            </ul>
          </div>
        </template>
        <template v-else>
          <div class="ae-hero__main">
            <p class="ae-hero__kicker">Ton programme</p>
            <h2 id="ae-hero-title" class="ae-hero__title">Choisis ta classe pour commencer</h2>
            <div class="ae-hero__actions">
              <router-link to="/account" class="es-btn es-btn--light">Choisir ma classe</router-link>
            </div>
          </div>
        </template>
      </section>

      <!-- Cette semaine -->
      <section class="es-card ae-week" aria-labelledby="ae-week-title">
        <div class="es-card__head">
          <h2 id="ae-week-title" class="es-h2">Cette semaine</h2>
          <span class="ae-week__goal-label">Objectif {{ OBJECTIF_SEMAINE }}</span>
        </div>
        <div class="es-card__body ae-week__body">
          <div class="ae-week__goal">
            <ProgressRing :value="semaine.faits" :max="OBJECTIF_SEMAINE" :size="92" :epaisseur="9">
              <strong class="ae-week__num">{{ semaine.faits }}</strong>
              <span class="ae-week__of">exercices</span>
            </ProgressRing>
            <p class="ae-week__text">
              <strong>{{ messageSemaine.titre }}</strong>
              <span>{{ messageSemaine.texte }}</span>
            </p>
          </div>
          <WeekBars :trend="semaine.trend" />
        </div>
      </section>

      <!-- Chiffres clés -->
      <div class="ae-kpis">
        <div class="es-card ae-kpi">
          <span class="ae-kpi__icon ae-kpi__icon--ok"><CheckBadgeIcon aria-hidden="true" /></span>
          <div class="ae-kpi__body">
            <strong>{{ totaux.acquis }}</strong>
            <span>{{ totaux.acquis > 1 ? 'exercices acquis' : 'exercice acquis' }}</span>
          </div>
          <span class="ae-kpi__foot">sur {{ totaux.exercices }} au programme</span>
        </div>
        <component
          :is="totaux.aRevoir ? 'router-link' : 'div'"
          :to="totaux.aRevoir && aRevoir[0] ? chapitreLink(aRevoir[0].notion_id, 'exercices', aRevoir[0].exercice_id) : undefined"
          class="es-card ae-kpi"
          :class="{ 'es-card--hover': totaux.aRevoir }"
        >
          <span class="ae-kpi__icon ae-kpi__icon--review"><ArrowPathIcon aria-hidden="true" /></span>
          <div class="ae-kpi__body">
            <strong>{{ totaux.aRevoir }}</strong>
            <span>à revoir</span>
          </div>
          <span class="ae-kpi__foot">{{ totaux.aRevoir ? 'Les reprendre maintenant →' : 'Rien en attente' }}</span>
        </component>
        <div class="es-card ae-kpi">
          <span class="ae-kpi__icon"><BookOpenIcon aria-hidden="true" /></span>
          <div class="ae-kpi__body">
            <strong>{{ totaux.commences }}<small>/{{ chapitres.length }}</small></strong>
            <span>chapitres commencés</span>
          </div>
          <span class="es-bar ae-kpi__bar"><span class="es-bar__ok" :style="{ width: pourcent(totaux.commences, chapitres.length) + '%' }"></span></span>
        </div>
      </div>

      <!-- Mon programme -->
      <section class="es-card ae-prog" aria-labelledby="ae-prog-title">
        <div class="es-card__head">
          <div>
            <h2 id="ae-prog-title" class="es-h2">Mon programme</h2>
            <p class="ae-card-sub">Les chapitres en cours, puis les prochains.</p>
          </div>
          <router-link :to="ESPACE_ROUTES.chapitres" class="es-link">
            Les {{ chapitres.length }} chapitres
            <ChevronRightIcon aria-hidden="true" />
          </router-link>
        </div>
        <div class="es-card__body">
          <div v-if="loading" class="ae-prog__list">
            <div v-for="n in 4" :key="n" class="es-skeleton" style="height: 60px"></div>
          </div>
          <ul v-else-if="programme.length" class="ae-prog__list">
            <li v-for="c in programme" :key="c.id">
              <router-link :to="chapitreLink(c.id, c.faits ? 'exercices' : 'cours')" class="ae-chap">
                <span class="es-theme-ico" :style="c.visuel.style"><component :is="c.visuel.icone" aria-hidden="true" /></span>
                <span class="ae-chap__main">
                  <span class="ae-chap__title">{{ c.titre }}</span>
                  <span class="ae-chap__line">
                    <span class="ae-chap__theme">{{ c.theme }}</span>
                    <template v-if="c.exercices">
                      <span class="es-bar ae-chap__bar">
                        <span class="es-bar__ok" :style="{ width: pourcent(c.acquis, c.exercices) + '%' }"></span>
                        <span class="es-bar__review" :style="{ width: pourcent(c.a_revoir, c.exercices) + '%' }"></span>
                      </span>
                      <span class="ae-chap__count">{{ c.acquis }}/{{ c.exercices }}</span>
                    </template>
                  </span>
                </span>
                <LockClosedIcon v-if="estVerrouille(c)" class="ae-chap__lock" aria-label="Réservé aux abonnés" />
                <span v-else :class="['es-pill', `es-pill--${etatChapitre(c).cle}`, 'ae-chap__pill']">{{ etatChapitre(c).label }}</span>
                <ChevronRightIcon class="ae-chev" aria-hidden="true" />
              </router-link>
            </li>
          </ul>
          <p v-else class="es-empty"><strong>Aucun chapitre pour l’instant</strong>Vérifie ta classe dans Mon compte.</p>
        </div>
      </section>

      <!-- Colonne droite -->
      <div class="ae-side">
        <section class="es-card ae-review" aria-labelledby="ae-review-title">
          <div class="es-card__head">
            <h2 id="ae-review-title" class="es-h2">À revoir</h2>
            <span v-if="aRevoir.length" class="ae-count">{{ totaux.aRevoir }}</span>
          </div>
          <div class="es-card__body">
            <ul v-if="aRevoir.length" class="ae-review__list">
              <li v-for="(item, i) in aRevoir.slice(0, 4)" :key="i">
                <router-link :to="chapitreLink(item.notion_id, 'exercices', item.exercice_id)" class="ae-review__item">
                  <span class="ae-review__icon"><ArrowPathIcon aria-hidden="true" /></span>
                  <span class="ae-review__text">
                    <strong>{{ titreCourt(item.exercice) }}</strong>
                    <span>{{ item.notion }}</span>
                  </span>
                  <ChevronRightIcon class="ae-chev" aria-hidden="true" />
                </router-link>
              </li>
            </ul>
            <div v-else class="ae-review__empty">
              <span class="ae-review__empty-icon"><CheckBadgeIcon aria-hidden="true" /></span>
              <strong>Rien à revoir</strong>
              <span>Quand tu marques un exercice « À revoir », il t’attend ici.</span>
            </div>
          </div>
        </section>

        <QuizNotes :chapitres="chapitres" :prefere="reprise?.chapitre?.id" />

        <!-- Ordinateur : la méthode ; téléphone : le prof (le menu latéral n'y est pas) -->
        <section class="es-card ae-tip" aria-labelledby="ae-tip-title">
          <h2 id="ae-tip-title" class="es-h2">La méthode qui marche</h2>
          <ol class="ae-tip__steps">
            <li><span>1</span><div><strong>Lis le cours</strong>avec les exemples et les schémas.</div></li>
            <li><span>2</span><div><strong>Relis la fiche</strong>pour retenir l’essentiel.</div></li>
            <li><span>3</span><div><strong>Entraîne-toi</strong>et marque ce qui est à revoir.</div></li>
          </ol>
        </section>

        <section class="es-card ae-help">
          <div class="ae-help__head">
            <span class="ae-help__photo" aria-hidden="true"></span>
            <div>
              <strong>Bloqué sur un exercice&nbsp;?</strong>
              <span>Anthony, ton prof, te répond sur WhatsApp.</span>
            </div>
          </div>
          <div class="ae-help__actions">
            <a :href="whatsappUrl" target="_blank" rel="noopener noreferrer" class="es-btn es-btn--sm es-btn--green" data-cta-name="whatsapp" data-cta-location="espace_accueil">Poser ma question</a>
            <router-link to="/cours-particuliers" class="es-btn es-btn--sm es-btn--ghost">Cours particuliers</router-link>
          </div>
        </section>
      </div>
    </div>

    <SubscriptionPromptModal :is-open="showSubscriptionPrompt" @close="fermerPromo" />
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import {
  ArrowPathIcon,
  BookOpenIcon,
  CheckBadgeIcon,
  ChevronRightIcon,
  FireIcon,
  LockClosedIcon,
  LockOpenIcon,
  PlayIcon,
  SparklesIcon,
  UserGroupIcon
} from '@heroicons/vue/24/outline'
import ProgressRing from './ProgressRing.vue'
import WeekBars from './WeekBars.vue'
import QuizNotes from './QuizNotes.vue'
import SubscriptionPromptModal from '@/components/modals/SubscriptionPromptModal.vue'
import { fetchMyOverview, fetchParentInvitations, respondParentInvitation } from '@/api/users'
import { useProgression } from '@/composables/useProgression'
import { useUserStore } from '@/stores/user'
import { useSubscriptionStore } from '@/stores/subscription'
import { ESPACE_ROUTES, OBJECTIF_SEMAINE, appliquerExemple, chapitreLink, overviewExemple } from '@/config/espace'
import { vitrineContact } from '@/config/vitrineContent'
import { dateDuJour, depuis, etatChapitre, pluriel, pourcent } from '@/utils/espaceFormat'
import { indexThemes, visuelTheme } from '@/utils/espaceTheme'

const props = defineProps({
  exemple: { type: Boolean, default: false }
})

const userStore = useUserStore()
const subscriptionStore = useSubscriptionStore()
const { progression: progressionServeur, charger } = useProgression()

const loading = ref(true)
const overview = ref(null)
const invitations = ref([])
const invitationEnCours = ref('')

const progression = computed(() => (props.exemple ? appliquerExemple(progressionServeur.value) : progressionServeur.value))
const prenom = computed(() => userStore.firstName || '')
const classe = computed(() => userStore.niveau_pays?.nom || progression.value?.niveau || '')
const serie = computed(() => Number(userStore.loginStreakCount || 0))
const salut = new Date().getHours() >= 18 ? 'Bonsoir' : 'Bonjour'

const themes = computed(() => indexThemes(progression.value?.chapitres || []))
const chapitres = computed(() => (progression.value?.chapitres || []).map((c) => ({ ...c, visuel: visuelTheme(c.theme, themes.value.get(c.theme_id)) })))
const aRevoir = computed(() => progression.value?.a_revoir || [])

// ---------- Accès (abonnement / chapitre démo) ----------
const niveauId = computed(() => userStore.niveau_pays?.id)
const demoNotionId = computed(() => Number(userStore.niveau_pays?.demo_notion) || null)
const aAcces = computed(() => {
  if (userStore.isAdmin || subscriptionStore.hasAccess) return true
  return niveauId.value ? subscriptionStore.accessForLevel(niveauId.value) : false
})
const statutCharge = computed(() => Boolean(subscriptionStore.status) && !subscriptionStore.loading)
const afficherAbonnement = computed(() => statutCharge.value && !aAcces.value && Boolean(niveauId.value))
const estVerrouille = (c) => statutCharge.value && !aAcces.value && c.id !== demoNotionId.value

// ---------- Reprendre ----------
const reprise = computed(() => {
  const liste = chapitres.value
  if (!liste.length) return null
  const derniere = progression.value?.derniere_activite
  let chapitre = derniere ? liste.find((c) => c.id === derniere.notion_id) : null
  if (!chapitre) chapitre = liste.find((c) => c.faits > 0 && c.acquis < c.exercices)
  if (!chapitre && statutCharge.value && !aAcces.value && demoNotionId.value) {
    chapitre = liste.find((c) => c.id === demoNotionId.value)
  }
  if (!chapitre) chapitre = liste.find((c) => !c.faits) || liste[0]
  return {
    chapitre,
    visuel: chapitre.visuel,
    dejaCommence: chapitre.faits > 0,
    quand: derniere?.notion_id === chapitre.id ? derniere.quand : chapitre.derniere_activite
  }
})

// ---------- Semaine ----------
const semaine = computed(() => ({ faits: overview.value?.metrics?.weekly_done || 0, trend: overview.value?.weekly_trend || [] }))

const messageSemaine = computed(() => {
  const faits = semaine.value.faits
  const reste = Math.max(0, OBJECTIF_SEMAINE - faits)
  if (faits === 0) return { titre: 'C’est parti !', texte: `Vise ${OBJECTIF_SEMAINE} exercices d’ici dimanche.` }
  if (reste === 0) return { titre: 'Objectif atteint !', texte: 'Bravo, continue sur ta lancée.' }
  return { titre: 'Beau travail', texte: `Encore ${pluriel(reste, 'exercice')} pour l’objectif.` }
})

const sousTitre = computed(() => {
  if (loading.value) return classe.value
  if (!semaine.value.faits) return `${classe.value ? `${classe.value} · ` : ''}Prêt pour une nouvelle séance ?`
  return `${classe.value ? `${classe.value} · ` : ''}${pluriel(semaine.value.faits, 'exercice')} cette semaine, continue comme ça.`
})

// ---------- Totaux ----------
const totaux = computed(() => chapitres.value.reduce(
  (t, c) => ({
    acquis: t.acquis + c.acquis,
    aRevoir: t.aRevoir + c.a_revoir,
    commences: t.commences + (c.faits > 0 ? 1 : 0),
    exercices: t.exercices + (c.exercices || 0)
  }),
  { acquis: 0, aRevoir: 0, commences: 0, exercices: 0 }
))

// En cours d'abord (du plus récent au plus ancien), puis les prochains chapitres du programme.
const programme = computed(() => {
  const enCours = chapitres.value
    .filter((c) => c.faits > 0 && c.acquis < c.exercices)
    .sort((a, b) => String(b.derniere_activite || '').localeCompare(String(a.derniere_activite || '')))
  const suivants = chapitres.value.filter((c) => !c.faits)
  return [...enCours, ...suivants].slice(0, 5)
})

const titreCourt = (titre = '') => titre.replace(/^(Découverte|Entraînement|Problème|Approfondissement)\s*[-–]\s*/i, '')

const whatsappUrl = `https://wa.me/${vitrineContact.whatsapp}?text=${encodeURIComponent('Bonjour, je bloque sur un exercice OptiTAB, pouvez-vous m’aider ?')}`

// ---------- Invitations parent ----------
async function repondre(inv, action) {
  invitationEnCours.value = action
  try {
    await respondParentInvitation(inv.link_id, action)
    invitations.value = invitations.value.filter((i) => i.link_id !== inv.link_id)
  } catch {
    // On laisse la carte affichée : l'élève pourra réessayer.
  } finally {
    invitationEnCours.value = ''
  }
}

// ---------- Fenêtre d'abonnement (même règle que l'ancien tableau de bord) ----------
const showSubscriptionPrompt = ref(false)
let promoTimer = null
const PROMO_INTERVALLE = 2 * 60 * 1000
const doitProposer = computed(() => !props.exemple && Boolean(userStore.pays && userStore.niveau_pays) && afficherAbonnement.value)

function fermerPromo() {
  showSubscriptionPrompt.value = false
  clearTimeout(promoTimer)
  if (doitProposer.value) promoTimer = setTimeout(() => { if (doitProposer.value) showSubscriptionPrompt.value = true }, PROMO_INTERVALLE)
}

watch(doitProposer, (ok) => {
  if (!ok) {
    showSubscriptionPrompt.value = false
    clearTimeout(promoTimer)
  }
})

onMounted(async () => {
  const [, ov, inv] = await Promise.allSettled([
    charger(),
    props.exemple ? Promise.resolve(null) : fetchMyOverview(),
    props.exemple ? Promise.resolve(null) : fetchParentInvitations()
  ])
  overview.value = props.exemple ? overviewExemple() : (ov.status === 'fulfilled' ? ov.value?.data?.data : null)
  invitations.value = inv.status === 'fulfilled' ? (inv.value?.data?.data?.invitations || []) : []
  loading.value = false

  await subscriptionStore.fetchStatus({ force: true }).catch(() => {})
  if (doitProposer.value) showSubscriptionPrompt.value = true
})

onBeforeUnmount(() => clearTimeout(promoTimer))
</script>

<style scoped>
.ae-grid {
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  gap: 20px;
}

/* ---------- En-tête ---------- */

.ae-head {
  align-items: flex-end;
}

.ae-date {
  margin-bottom: 4px !important;
  font-size: 13px;
  font-weight: 600;
  color: var(--es-muted);
}

.ae-hello {
  font-size: clamp(26px, 2.8vw, 34px);
}

.ae-head__right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.ae-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 44px;
  padding: 0 14px;
  border: 1px solid var(--es-line);
  border-radius: 12px;
  background: #fff;
  font-size: 14px;
  font-weight: 700;
  color: var(--es-ink);
}

.ae-chip svg {
  width: 20px;
  height: 20px;
}

.ae-chip--fire svg {
  color: #e8612d;
}

/* ---------- Bandeaux (invitation, abonnement) ---------- */

.ae-banner {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  padding: 16px 20px;
}

.ae-banner__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  border-radius: 12px;
  background: var(--es-navy-50);
  color: var(--es-navy);
}

.ae-banner__icon svg {
  width: 22px;
  height: 22px;
}

.ae-banner--sub {
  border-color: #cfe5cf;
  background: linear-gradient(90deg, #f3faf3 0%, #fff 60%);
}

.ae-banner--sub .ae-banner__icon {
  background: var(--es-green-50);
  color: var(--es-green-700);
}

.ae-banner__text {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
  font-size: 14px;
  color: var(--es-muted);
}

.ae-banner__text strong {
  font-size: 15px;
  color: var(--es-ink);
}

.ae-banner__actions {
  display: flex;
  gap: 8px;
}

/* ---------- Reprendre ---------- */

.ae-hero {
  grid-column: span 8;
  display: flex;
  align-items: center;
  gap: 28px;
  min-height: 268px;
  padding: 30px 32px;
  overflow: hidden;
  border-radius: 20px;
  background:
    radial-gradient(420px 260px at 92% 8%, rgba(95, 172, 96, 0.32), transparent 70%),
    linear-gradient(135deg, #1e4199 0%, #16336f 55%, #0f2657 100%);
  color: #fff;
  box-shadow: 0 18px 40px rgba(18, 42, 102, 0.22);
}

.ae-sk {
  height: 18px;
  opacity: 0.2;
}

.ae-hero__main {
  display: flex;
  flex: 1;
  flex-direction: column;
  align-items: flex-start;
  min-width: 0;
}

.ae-hero__kicker {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #a9dcaa;
}

.ae-hero__theme {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 14px;
  padding: 4px 10px 4px 8px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  font-size: 12px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.92);
}

.ae-hero__theme svg {
  width: 15px;
  height: 15px;
}

.ae-hero__title {
  margin-top: 10px !important;
  font-size: clamp(24px, 2.6vw, 32px);
  font-weight: 700;
  line-height: 1.2;
  color: #fff !important;
}

.ae-hero__meta {
  margin-top: 8px !important;
  max-width: 460px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.72);
}

.ae-hero__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 24px;
}

.ae-hero__cta {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.18);
}

.ae-hero__ring {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  flex-shrink: 0;
}

.ae-ring--dark :deep(.ring__track) {
  stroke: rgba(255, 255, 255, 0.14);
}

.ae-ring--dark :deep(.ring__fill) {
  stroke: #7fcf81;
}

.ae-hero__pct {
  font-size: 34px;
  font-weight: 700;
  line-height: 1;
  color: #fff;
}

.ae-hero__pct small {
  margin-left: 1px;
  font-size: 18px;
}

.ae-hero__pct-label {
  margin-top: 4px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.65);
}

.ae-hero__legend {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin: 0;
  padding: 0;
  font-size: 13px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.85);
  list-style: none;
}

.ae-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  margin-right: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.35);
}

.ae-dot--ok {
  background: #7fcf81;
}

.ae-dot--review {
  background: var(--es-orange);
}

/* ---------- Semaine ---------- */

.ae-week {
  grid-column: span 4;
}

.ae-week__goal-label {
  padding: 3px 10px;
  border-radius: 999px;
  background: var(--es-bg);
  font-size: 12px;
  font-weight: 700;
  color: var(--es-muted);
}

.ae-week__body {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.ae-week__goal {
  display: flex;
  align-items: center;
  gap: 16px;
}

.ae-week__num {
  font-size: 26px;
  font-weight: 700;
  line-height: 1;
  color: var(--es-ink);
}

.ae-week__of {
  margin-top: 2px;
  font-size: 11px;
  color: var(--es-muted);
}

.ae-week__text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 14px;
  color: var(--es-muted);
}

.ae-week__text strong {
  font-size: 16px;
  color: var(--es-ink);
}

/* ---------- Chiffres clés ---------- */

.ae-kpis {
  grid-column: span 12;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
}

.ae-kpi {
  display: grid;
  grid-template-columns: auto 1fr;
  align-items: center;
  gap: 4px 14px;
  padding: 18px 20px;
  color: inherit;
  text-decoration: none;
}

.ae-kpi__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 46px;
  height: 46px;
  border-radius: 14px;
  background: var(--es-navy-50);
  color: var(--es-navy);
}

.ae-kpi__icon svg {
  width: 24px;
  height: 24px;
}

.ae-kpi__icon--ok {
  background: var(--es-green-50);
  color: var(--es-green-700);
}

.ae-kpi__icon--review {
  background: var(--es-orange-50);
  color: var(--es-orange-700);
}

.ae-kpi__body {
  display: flex;
  flex-direction: column;
  min-width: 0;
  font-size: 14px;
  color: var(--es-muted);
}

.ae-kpi__body strong {
  font-size: 28px;
  font-weight: 700;
  line-height: 1.05;
  color: var(--es-ink);
}

.ae-kpi__body small {
  font-size: 16px;
  font-weight: 600;
  color: var(--es-muted);
}

.ae-kpi__foot {
  grid-column: 1 / -1;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid var(--es-line);
  font-size: 13px;
  font-weight: 600;
  color: var(--es-muted);
}

a.ae-kpi .ae-kpi__foot {
  color: var(--es-orange-700);
}

.ae-kpi__bar {
  grid-column: 1 / -1;
  margin-top: 14px;
  height: 6px;
}

/* ---------- Programme ---------- */

.ae-prog {
  grid-column: span 8;
}

.ae-card-sub {
  margin-top: 2px !important;
  font-size: 13px;
  color: var(--es-muted);
}

.ae-prog__list {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.ae-chap {
  display: flex;
  align-items: center;
  gap: 14px;
  margin: 0 -10px;
  padding: 12px 10px;
  border-radius: 14px;
  text-decoration: none;
  transition: background-color 0.15s ease;
}

.ae-chap:hover {
  background: var(--es-bg);
}

.ae-chap__main {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.ae-chap__title {
  font-size: 15px;
  font-weight: 600;
  line-height: 1.35;
  color: var(--es-ink);
}

.ae-chap__line {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.ae-chap__theme {
  overflow: hidden;
  font-size: 12px;
  font-weight: 600;
  color: var(--es-muted);
  white-space: nowrap;
  text-overflow: ellipsis;
}

.ae-chap__bar {
  width: 140px;
  flex-shrink: 0;
  height: 6px;
}

.ae-chap__count {
  font-size: 12px;
  font-weight: 700;
  color: var(--es-muted);
}

.ae-chap__lock {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  color: #98a2b3;
}

.ae-chev {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  color: #98a2b3;
}

/* ---------- Colonne droite ---------- */

.ae-side {
  grid-column: span 4;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.ae-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 26px;
  height: 26px;
  padding: 0 8px;
  border-radius: 999px;
  background: var(--es-orange-50);
  font-size: 13px;
  font-weight: 700;
  color: var(--es-orange-700);
}

.ae-review__list {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.ae-review__item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0 -10px;
  padding: 10px;
  border-radius: 12px;
  text-decoration: none;
}

.ae-review__item:hover {
  background: var(--es-bg);
}

.ae-review__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  flex-shrink: 0;
  border-radius: 10px;
  background: var(--es-orange-50);
  color: var(--es-orange-700);
}

.ae-review__icon svg {
  width: 16px;
  height: 16px;
}

.ae-review__text {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
  font-size: 12px;
  color: var(--es-muted);
}

.ae-review__text strong,
.ae-review__text > span {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.ae-review__text strong {
  font-size: 14px;
  font-weight: 600;
  color: var(--es-ink);
}

.ae-review__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 12px 8px 4px;
  font-size: 13px;
  text-align: center;
  color: var(--es-muted);
}

.ae-review__empty strong {
  font-size: 15px;
  color: var(--es-ink);
}

.ae-review__empty-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  margin-bottom: 6px;
  border-radius: 50%;
  background: var(--es-green-50);
  color: var(--es-green-700);
}

.ae-review__empty-icon svg {
  width: 22px;
  height: 22px;
}

.ae-tip {
  padding: 20px;
}

.ae-tip__steps {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin: 16px 0 0;
  padding: 0;
  list-style: none;
}

.ae-tip__steps li {
  display: flex;
  gap: 12px;
  font-size: 13px;
  color: var(--es-muted);
}

.ae-tip__steps li > span {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  flex-shrink: 0;
  border-radius: 50%;
  background: var(--es-navy);
  font-size: 13px;
  font-weight: 700;
  color: #fff;
}

.ae-tip__steps li:last-child > span {
  background: var(--es-green);
}

.ae-tip__steps strong {
  display: block;
  font-size: 14px;
  color: var(--es-ink);
}

.ae-help {
  display: none;
  padding: 18px;
}

.ae-help__head {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ae-help__head div {
  display: flex;
  flex-direction: column;
  font-size: 13px;
  color: var(--es-muted);
}

.ae-help__head strong {
  font-size: 15px;
  color: var(--es-ink);
}

.ae-help__photo {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  border-radius: 50%;
  background: #fff url('/images/professeurs/anthony.jpg') 50% 12% / 190% auto no-repeat;
  box-shadow: 0 0 0 2px #fff, 0 0 0 4px var(--es-green-50);
}

.ae-help__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 14px;
}

/* ---------- Tablette et téléphone ---------- */

@media (max-width: 1180px) {
  .ae-hero,
  .ae-prog,
  .ae-week,
  .ae-side {
    grid-column: span 12;
  }

  .ae-week__body {
    flex-direction: row;
    align-items: center;
    gap: 28px;
  }

  .ae-week__body .wb {
    flex: 1;
  }

  .ae-side {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 1023px) {
  .ae-tip {
    display: none;
  }

  .ae-help {
    display: block;
  }
}

@media (max-width: 760px) {
  .ae-grid {
    gap: 14px;
  }

  .ae-head__right .es-btn {
    display: none;
  }

  .ae-head__right {
    order: -1;
  }

  .ae-chip {
    min-height: 32px;
    padding: 0 10px;
    font-size: 13px;
  }

  .ae-hero {
    flex-direction: column;
    align-items: stretch;
    gap: 20px;
    min-height: 0;
    padding: 22px 20px;
    border-radius: 18px;
  }

  .ae-hero__ring {
    flex-direction: row;
    justify-content: flex-start;
    gap: 18px;
    order: -1;
    padding-bottom: 18px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
  }

  .ae-hero__ring :deep(.ring) {
    width: 96px !important;
    height: 96px !important;
  }

  .ae-hero__pct {
    font-size: 24px;
  }

  .ae-hero__pct small {
    font-size: 14px;
  }

  .ae-hero__pct-label {
    font-size: 10px;
  }

  .ae-hero__actions .es-btn {
    flex: 1 1 100%;
  }

  .ae-week__body {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }

  .ae-kpis {
    gap: 10px;
  }

  .ae-kpi {
    grid-template-columns: 1fr;
    gap: 8px;
    padding: 12px;
  }

  .ae-kpi__icon {
    width: 34px;
    height: 34px;
    border-radius: 10px;
  }

  .ae-kpi__icon svg {
    width: 18px;
    height: 18px;
  }

  .ae-kpi__body {
    font-size: 12px;
    line-height: 1.3;
  }

  .ae-kpi__body strong {
    font-size: 22px;
  }

  .ae-kpi__foot {
    display: none;
  }

  .ae-kpi__bar {
    margin-top: 2px;
  }

  .ae-side {
    display: flex;
    gap: 14px;
  }

  .ae-side {
    order: 1;
  }

  .ae-prog {
    order: 2;
  }

  .ae-chap__pill {
    display: none;
  }

  .ae-chap__bar {
    width: 80px;
  }

  .ae-banner {
    flex-wrap: wrap;
    padding: 14px 16px;
  }

  .ae-banner__text {
    flex-basis: calc(100% - 60px);
  }

  .ae-banner__actions,
  .ae-banner--sub .es-btn {
    width: 100%;
  }

  .ae-banner__actions .es-btn {
    flex: 1;
  }
}
</style>
