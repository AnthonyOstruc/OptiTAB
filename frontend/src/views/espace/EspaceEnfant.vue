<template>
  <EspaceLayout :title="enfant ? enfant.first_name : 'Suivi'" :parent="true" :back="{ to: ESPACE_ROUTES.accueil, label: 'Retour à l’espace parent' }">
    <router-link :to="ESPACE_ROUTES.accueil" class="es-link ee-back">
      <ChevronLeftIcon aria-hidden="true" />
      Espace parent
    </router-link>

    <div v-if="loading" class="es-card ee-card">
      <div class="es-skeleton" style="height: 56px; width: 50%"></div>
      <div class="es-skeleton" style="height: 180px; margin-top: 20px"></div>
    </div>

    <p v-else-if="!enfant" class="es-empty">
      <strong>Suivi indisponible</strong>
      Cet élève n’est pas lié à votre compte, ou n’a pas encore accepté votre demande.
    </p>

    <template v-else>
      <header class="es-card ee-head">
        <span class="ee-avatar" aria-hidden="true">{{ initiales(enfant.first_name, enfant.last_name) }}</span>
        <div class="ee-head__id">
          <h1 class="es-h1">{{ enfant.first_name }} {{ enfant.last_name }}</h1>
          <p>
            <span v-if="enfant.niveau" class="es-pill es-pill--progress es-pill--plain">{{ enfant.niveau }}</span>
            <span>{{ derniere ? `Dernière activité ${depuis(derniere.when)} · ${derniere.chapitre_title || ''}` : 'Pas encore d’activité' }}</span>
          </p>
        </div>
        <p :class="['ee-insight', `ee-insight--${synthese.ton}`]">
          <component :is="synthese.icone" aria-hidden="true" />
          <span>{{ synthese.texte }}</span>
        </p>
      </header>

      <div class="ee-grid">
        <section class="es-card ee-card ee-week" aria-labelledby="ee-week">
          <h2 id="ee-week" class="ee-title">Cette semaine</h2>
          <div class="ee-week__body">
            <ProgressRing :value="metrics.weekly_done || 0" :max="OBJECTIF_SEMAINE" :size="96" :epaisseur="9">
              <strong class="ee-ring__num">{{ metrics.weekly_done || 0 }}</strong>
              <span class="ee-ring__of">sur {{ OBJECTIF_SEMAINE }}</span>
            </ProgressRing>
            <WeekBars :trend="trend" />
          </div>
          <p class="ee-muted">{{ pluriel(joursActifs, 'jour actif', 'jours actifs') }} sur les 7 derniers jours.</p>
        </section>

        <section class="es-card ee-card" aria-labelledby="ee-res">
          <h2 id="ee-res" class="ee-title">Depuis le début</h2>
          <dl class="ee-kpis">
            <div><dt>Exercices faits</dt><dd>{{ metrics.done_total || 0 }}</dd></div>
            <div><dt>Acquis</dt><dd class="ee-ok">{{ metrics.acquired_count || 0 }}</dd></div>
            <div><dt>À revoir</dt><dd class="ee-review">{{ metrics.not_acquired_count || 0 }}</dd></div>
            <div><dt>Réussite</dt><dd>{{ pourcent(metrics.acquired_count, metrics.done_total) }}&nbsp;%</dd></div>
          </dl>
        </section>

        <section class="es-card ee-card ee-wide" aria-labelledby="ee-chap">
          <div class="ee-card__head">
            <h2 id="ee-chap" class="ee-title">Progression par chapitre</h2>
            <span class="ee-muted">{{ chapitresTravailles.length }} / {{ chapitres.length }} chapitres commencés</span>
          </div>
          <ul v-if="chapitresTravailles.length" class="ee-chaps">
            <li v-for="c in chapitresTravailles" :key="c.id">
              <span class="es-theme-ico es-theme-ico--sm" :style="c.visuel.style"><component :is="c.visuel.icone" aria-hidden="true" /></span>
              <span class="ee-chaps__main">
                <span class="ee-chaps__title">{{ c.titre }}</span>
                <span class="ee-chaps__line">
                  <span class="es-bar">
                    <span class="es-bar__ok" :style="{ width: pourcent(c.acquis, c.exercices) + '%' }"></span>
                    <span class="es-bar__review" :style="{ width: pourcent(c.a_revoir, c.exercices) + '%' }"></span>
                  </span>
                  <span class="ee-chaps__count">{{ c.acquis }}/{{ c.exercices }} acquis</span>
                </span>
              </span>
              <span :class="['es-pill', `es-pill--${etatChapitre(c).cle}`]">{{ etatChapitre(c).label }}</span>
            </li>
          </ul>
          <p v-else class="ee-muted">Aucun chapitre commencé pour l’instant.</p>
        </section>

        <section class="es-card ee-card" aria-labelledby="ee-rev">
          <h2 id="ee-rev" class="ee-title">Points à revoir</h2>
          <ul v-if="aRevoir.length" class="ee-list">
            <li v-for="(item, i) in aRevoir" :key="i">
              <span class="ee-dot ee-dot--review" aria-hidden="true"></span>
              <span><strong>{{ titreCourt(item.exercice) }}</strong><span>{{ item.notion }}</span></span>
            </li>
          </ul>
          <p v-else class="ee-muted">Rien à revoir : tous les exercices faits sont compris.</p>
        </section>

        <section class="es-card ee-card" aria-labelledby="ee-act">
          <h2 id="ee-act" class="ee-title">Activité récente</h2>
          <ul v-if="activites.length" class="ee-list">
            <li v-for="a in activites" :key="a.id">
              <span :class="['ee-dot', a.est_correct ? 'ee-dot--ok' : 'ee-dot--review']" aria-hidden="true"></span>
              <span>
                <strong>{{ titreCourt(a.exercice_title) }}</strong>
                <span>{{ a.chapitre_title }} · {{ depuis(a.when) }} · {{ a.est_correct ? 'compris' : 'à revoir' }}</span>
              </span>
            </li>
          </ul>
          <p v-else class="ee-muted">Pas encore d’exercice fait.</p>
        </section>
      </div>

      <section class="es-card ee-help">
        <AcademicCapIcon class="ee-help__icon" aria-hidden="true" />
        <div>
          <h2 class="es-h2">Un chapitre résiste&nbsp;?</h2>
          <p>Un professeur peut reprendre les points à revoir en cours particulier, en visio. Premier échange gratuit.</p>
        </div>
        <router-link to="/cours-particuliers" class="es-btn es-btn--ghost">Découvrir</router-link>
      </section>

      <div class="ee-remove">
        <button type="button" class="ee-remove__btn" :disabled="retrait" @click="retirer">
          Ne plus suivre {{ enfant.first_name }}
        </button>
        <span>Le compte de l’élève reste actif ; seul votre accès à son suivi est retiré.</span>
      </div>
    </template>
  </EspaceLayout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  AcademicCapIcon,
  CheckBadgeIcon,
  ChevronLeftIcon,
  ExclamationTriangleIcon,
  LightBulbIcon
} from '@heroicons/vue/24/outline'
import EspaceLayout from '@/components/espace/EspaceLayout.vue'
import ProgressRing from '@/components/espace/ProgressRing.vue'
import WeekBars from '@/components/espace/WeekBars.vue'
import { getChildOverview, getChildProgression } from '@/api/progression'
import { removeChild } from '@/api/users'
import { ESPACE_ROUTES, OBJECTIF_SEMAINE } from '@/config/espace'
import { depuis, etatChapitre, initiales, joursDepuis, pluriel, pourcent } from '@/utils/espaceFormat'
import { indexThemes, visuelTheme } from '@/utils/espaceTheme'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const enfant = ref(null)
const metrics = ref({})
const trend = ref([])
const activites = ref([])
const progression = ref(null)

const derniere = computed(() => activites.value[0] || null)
const joursActifs = computed(() => trend.value.filter((d) => d.total > 0).length)
const chapitres = computed(() => {
  const liste = progression.value?.chapitres || []
  const themes = indexThemes(liste)
  return liste.map((c) => ({ ...c, visuel: visuelTheme(c.theme, themes.get(c.theme_id)) }))
})
const chapitresTravailles = computed(() => chapitres.value
  .filter((c) => c.faits > 0)
  .sort((a, b) => String(b.derniere_activite || '').localeCompare(String(a.derniere_activite || ''))))
const aRevoir = computed(() => progression.value?.a_revoir || [])

const titreCourt = (titre = '') => String(titre || '').replace(/^(Découverte|Entraînement|Problème|Approfondissement)\s*[-–]\s*/i, '')

const synthese = computed(() => {
  const m = metrics.value || {}
  const prenom = enfant.value?.first_name || 'Votre enfant'
  const inactif = joursDepuis(derniere.value?.when)
  if (!m.done_total) {
    return { ton: 'info', icone: LightBulbIcon, texte: `${prenom} n’a pas encore commencé. Un premier cours et quelques exercices suffisent pour lancer la semaine.` }
  }
  if (inactif !== null && inactif >= 7) {
    return { ton: 'warn', icone: ExclamationTriangleIcon, texte: `Aucune activité depuis ${pluriel(inactif, 'jour')}. Un petit rappel peut aider ${prenom} à reprendre.` }
  }
  if ((m.weekly_done || 0) >= OBJECTIF_SEMAINE) {
    return { ton: 'ok', icone: CheckBadgeIcon, texte: `Objectif de la semaine atteint : ${pluriel(m.weekly_done, 'exercice')} en ${pluriel(joursActifs.value, 'jour')}. Bravo !` }
  }
  return {
    ton: 'info',
    icone: LightBulbIcon,
    texte: `${prenom} a fait ${pluriel(m.weekly_done || 0, 'exercice')} cette semaine, sur ${pluriel(joursActifs.value, 'jour')}. Objectif : ${OBJECTIF_SEMAINE}.`
  }
})

const retrait = ref(false)
async function retirer() {
  const prenom = enfant.value?.first_name || 'cet élève'
  if (!window.confirm(`Ne plus suivre ${prenom} ? Vous pourrez lui renvoyer une demande plus tard.`)) return
  retrait.value = true
  try {
    await removeChild(route.params.childId)
    router.push(ESPACE_ROUTES.accueil)
  } catch {
    retrait.value = false
    window.alert('Impossible de retirer le suivi pour le moment. Réessayez dans un instant.')
  }
}

onMounted(async () => {
  const id = route.params.childId
  const [ov, prog] = await Promise.allSettled([getChildOverview(id), getChildProgression(id)])
  const data = ov.status === 'fulfilled' ? ov.value?.data?.data : null
  if (data?.child) {
    enfant.value = data.child
    metrics.value = data.metrics || {}
    trend.value = data.weekly_trend || []
    activites.value = data.last_activities || []
  }
  progression.value = prog.status === 'fulfilled' ? prog.value?.data?.data : null
  loading.value = false
})
</script>

<style scoped>
.ee-back {
  margin-bottom: 14px;
}

.ee-head {
  display: grid;
  grid-template-columns: auto 1fr;
  align-items: center;
  gap: 16px 18px;
  margin-bottom: 20px;
  padding: 24px;
}

.ee-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  border-radius: 18px;
  background: var(--es-navy);
  font-size: 20px;
  font-weight: 700;
  color: #fff;
}

.ee-head__id p {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-top: 6px !important;
  font-size: 14px;
  color: var(--es-muted);
}

.es .ee-insight {
  grid-column: 1 / -1;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 14px;
  border-radius: 12px;
  background: var(--es-navy-50);
  font-size: 15px;
  font-weight: 600;
  line-height: 1.45;
  color: var(--es-navy);
}

.ee-insight svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  margin-top: 1px;
}

.es .ee-insight--ok {
  background: var(--es-green-50);
  color: var(--es-green-700);
}

.es .ee-insight--warn {
  background: var(--es-orange-50);
  color: var(--es-orange-700);
}

.ee-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
}

.ee-card {
  padding: 20px 22px;
}

.ee-wide {
  grid-column: 1 / -1;
}

.ee-card__head {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: space-between;
  gap: 8px;
}

.es .ee-title {
  margin-bottom: 14px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--es-muted);
}

.ee-muted {
  font-size: 14px;
  color: var(--es-muted);
}

.ee-week__body {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 12px;
}

.ee-week__body .wb {
  flex: 1;
}

.ee-ring__num {
  font-size: 24px;
  font-weight: 700;
  line-height: 1;
}

.ee-ring__of {
  font-size: 11px;
  color: var(--es-muted);
}

.ee-kpis {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin: 0;
}

.ee-kpis div {
  padding: 14px;
  border-radius: 12px;
  background: var(--es-bg);
}

.ee-kpis dt {
  font-size: 13px;
  color: var(--es-muted);
}

.ee-kpis dd {
  margin: 2px 0 0;
  font-size: 24px;
  font-weight: 700;
}

.ee-ok {
  color: var(--es-green-700);
}

.ee-review {
  color: var(--es-orange-700);
}

.ee-chaps,
.ee-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.ee-chaps li {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ee-chaps__main {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.ee-chaps__title {
  font-size: 15px;
  font-weight: 600;
}

.ee-chaps__line {
  display: flex;
  align-items: center;
  gap: 10px;
}

.ee-chaps__line .es-bar {
  width: min(280px, 50%);
}

.ee-chaps__count {
  font-size: 12px;
  font-weight: 700;
  color: var(--es-muted);
}

.ee-list li {
  display: flex;
  gap: 10px;
}

.ee-list li > span:last-child {
  display: flex;
  flex-direction: column;
  min-width: 0;
  font-size: 13px;
  color: var(--es-muted);
}

.ee-list strong {
  font-size: 14px;
  font-weight: 600;
  color: var(--es-ink);
}

.ee-dot {
  width: 8px;
  height: 8px;
  flex-shrink: 0;
  margin-top: 7px;
  border-radius: 50%;
}

.ee-dot--ok {
  background: var(--es-green);
}

.ee-dot--review {
  background: var(--es-orange);
}

.ee-help {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 20px;
  padding: 20px 24px;
}

.ee-help > div {
  flex: 1;
}

.ee-help p {
  margin-top: 4px !important;
  font-size: 14px;
  color: var(--es-muted);
}

.ee-help__icon {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  padding: 10px;
  border-radius: 12px;
  background: var(--es-green-50);
  color: var(--es-green-700);
}

.ee-remove {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px 14px;
  margin-top: 24px;
  font-size: 13px;
  color: var(--es-muted);
}

.ee-remove__btn {
  padding: 0;
  border: 0;
  background: none;
  font: 600 14px var(--es-font);
  color: var(--es-red-700);
  text-decoration: underline;
  text-underline-offset: 3px;
  cursor: pointer;
}

@media (max-width: 860px) {
  .ee-grid {
    grid-template-columns: minmax(0, 1fr);
  }
}

@media (max-width: 640px) {
  .ee-back {
    display: none;
  }

  .ee-head,
  .ee-card {
    padding: 18px 16px;
  }

  .ee-week__body {
    flex-direction: column;
    align-items: stretch;
  }

  .ee-week__body .ring {
    align-self: center;
  }

  .ee-chaps li .es-pill {
    display: none;
  }

  .ee-help {
    flex-wrap: wrap;
  }

  .ee-help .es-btn {
    width: 100%;
  }
}
</style>
