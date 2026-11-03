<template>
  <EspaceLayout :title="chapitre?.titre || 'Chapitre'" :back="{ to: ESPACE_ROUTES.chapitres, label: 'Retour à mes chapitres' }" :wide="onglet === 'cours'">
    <header class="ch-hero" :style="visuel.style">
      <nav class="ch-crumbs" aria-label="Fil d’Ariane">
        <router-link :to="ESPACE_ROUTES.chapitres">Mes chapitres</router-link>
        <ChevronRightIcon aria-hidden="true" />
        <span>{{ chapitre?.theme || '…' }}</span>
      </nav>
      <div class="ch-hero__row">
        <span class="es-theme-ico ch-hero__ico"><component :is="visuel.icone" aria-hidden="true" /></span>
        <div class="ch-hero__text">
          <p class="ch-hero__kicker">
            <template v-if="chapitre">Chapitre {{ chapitre.numero }} · {{ chapitre.theme }}</template>
            <template v-else>&nbsp;</template>
          </p>
          <h1 class="ch-hero__title">{{ chapitre?.titre || '' }}</h1>
          <ul v-if="progres.total || chapitre?.derniere_activite" class="ch-hero__facts">
            <li v-if="progres.total"><PencilSquareIcon aria-hidden="true" />{{ progres.total }} exercices corrigés pas à pas</li>
            <li v-if="chapitre?.derniere_activite"><ClockIcon aria-hidden="true" />Dernière activité {{ depuis(chapitre.derniere_activite) }}</li>
          </ul>
        </div>
        <div v-if="progres.total" class="ch-hero__ring" :aria-label="`${progres.acquis} exercices acquis sur ${progres.total}`">
          <ProgressRing :value="progres.acquis" :max="progres.total" :size="88" :epaisseur="8" class="ch-ring">
            <strong>{{ pourcent(progres.acquis, progres.total) }}<small>%</small></strong>
          </ProgressRing>
          <div class="ch-hero__legend">
            <span><i class="ch-dot ch-dot--ok"></i>{{ progres.acquis }}/{{ progres.total }} acquis</span>
            <span v-if="progres.aRevoir"><i class="ch-dot ch-dot--review"></i>{{ progres.aRevoir }} à revoir</span>
            <span v-else><i class="ch-dot"></i>{{ Math.max(0, progres.total - progres.acquis) }} à faire</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Onglets, collés en haut pendant la lecture -->
    <div class="ch-tabs" role="tablist" aria-label="Contenu du chapitre">
      <button
        v-for="t in ONGLETS"
        :key="t.cle"
        type="button"
        role="tab"
        :aria-selected="onglet === t.cle"
        :class="['ch-tab', { 'is-active': onglet === t.cle }]"
        @click="ouvrir(t.cle)"
      >
        <component :is="t.icone" aria-hidden="true" />
        {{ t.label }}
        <span v-if="t.cle === 'exercices' && progres.total" class="ch-tab__count">{{ progres.total }}</span>
      </button>
    </div>

    <div class="ch-body">
      <ChapitreCours v-if="onglet === 'cours'" :notion-id="notionId" @go="ouvrir" />
      <ChapitreFiche v-else-if="onglet === 'fiche'" :notion-id="notionId" @go="ouvrir" />
      <ChapitreExercices v-else :notion-id="notionId" :exercice-initial="route.query.ex || null" @progress="majProgres" />
    </div>

    <!-- Chapitres voisins -->
    <nav v-if="precedent || suivant" class="ch-neighbours" aria-label="Chapitres voisins">
      <router-link v-if="precedent" :to="chapitreLink(precedent.id)" class="ch-neighbour">
        <ChevronLeftIcon aria-hidden="true" />
        <span>
          <small>Chapitre précédent</small>
          <strong>{{ precedent.titre }}</strong>
        </span>
      </router-link>
      <span v-else></span>
      <router-link v-if="suivant" :to="chapitreLink(suivant.id)" class="ch-neighbour ch-neighbour--next">
        <span>
          <small>Chapitre suivant</small>
          <strong>{{ suivant.titre }}</strong>
        </span>
        <ChevronRightIcon aria-hidden="true" />
      </router-link>
    </nav>
  </EspaceLayout>
</template>

<script setup>
import { computed, onMounted, reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  BookOpenIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  ClockIcon,
  DocumentTextIcon,
  PencilSquareIcon
} from '@heroicons/vue/24/outline'
import EspaceLayout from '@/components/espace/EspaceLayout.vue'
import ProgressRing from '@/components/espace/ProgressRing.vue'
import ChapitreCours from '@/components/espace/ChapitreCours.vue'
import ChapitreFiche from '@/components/espace/ChapitreFiche.vue'
import ChapitreExercices from '@/components/espace/ChapitreExercices.vue'
import { useProgression } from '@/composables/useProgression'
import { ESPACE_ROUTES, chapitreLink } from '@/config/espace'
import { depuis, pourcent } from '@/utils/espaceFormat'
import { indexThemes, visuelTheme } from '@/utils/espaceTheme'

const ONGLETS = [
  { cle: 'cours', label: 'Cours', icone: BookOpenIcon },
  { cle: 'fiche', label: 'Fiche', icone: DocumentTextIcon },
  { cle: 'exercices', label: 'Exercices', icone: PencilSquareIcon }
]

const route = useRoute()
const router = useRouter()
const { progression, charger } = useProgression()

const notionId = computed(() => route.params.notionId)
const onglet = computed(() => (ONGLETS.some((o) => o.cle === route.query.onglet) ? route.query.onglet : 'cours'))

const chapitres = computed(() => progression.value?.chapitres || [])
const index = computed(() => chapitres.value.findIndex((c) => String(c.id) === String(notionId.value)))
const chapitre = computed(() => (index.value >= 0 ? { ...chapitres.value[index.value], numero: index.value + 1 } : null))
const precedent = computed(() => (index.value > 0 ? chapitres.value[index.value - 1] : null))
const suivant = computed(() => (index.value >= 0 && index.value < chapitres.value.length - 1 ? chapitres.value[index.value + 1] : null))
const visuel = computed(() => {
  const c = chapitre.value
  return c ? visuelTheme(c.theme, indexThemes(chapitres.value).get(c.theme_id)) : visuelTheme('', 0)
})

// Compteurs du chapitre : ceux du serveur, puis ceux de l'onglet Exercices (à jour en direct).
const progres = reactive({ acquis: 0, aRevoir: 0, total: 0 })

function depuisServeur() {
  const c = chapitre.value
  if (!c) return
  progres.acquis = c.acquis
  progres.aRevoir = c.a_revoir
  progres.total = c.exercices
}

function majProgres(c) {
  progres.acquis = c.acquis
  progres.aRevoir = c.aRevoir
  progres.total = c.total
}

function ouvrir(cle) {
  const query = { ...route.query }
  if (cle === 'cours') delete query.onglet
  else query.onglet = cle
  if (cle !== 'exercices') delete query.ex
  router.push({ query })
  window.scrollTo({ top: 0, behavior: 'auto' })
}

onMounted(async () => {
  await charger()
  depuisServeur()
})

watch(notionId, () => {
  depuisServeur()
  window.scrollTo({ top: 0, behavior: 'auto' })
})
</script>

<style scoped>
/* ---------- Bandeau du chapitre ---------- */

.ch-hero {
  position: relative;
  margin-bottom: 16px;
  padding: 18px 24px 22px;
  overflow: hidden;
  border: 1px solid var(--es-line);
  border-radius: 20px;
  background:
    radial-gradient(520px 200px at 0% 0%, var(--t-bg), transparent 75%),
    #fff;
  box-shadow: var(--es-shadow);
}

.ch-hero::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  height: 4px;
  background: var(--t);
  opacity: 0.85;
}

.ch-crumbs {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 14px;
  font-size: 13px;
  font-weight: 600;
  color: var(--es-muted);
}

.ch-crumbs a {
  color: var(--es-navy);
  text-decoration: none;
}

.ch-crumbs a:hover {
  text-decoration: underline;
}

.ch-crumbs svg {
  width: 14px;
  height: 14px;
}

.ch-hero__row {
  display: flex;
  align-items: center;
  gap: 18px;
}

.ch-hero__ico {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  background: var(--t);
  color: #fff;
  box-shadow: 0 8px 18px rgba(16, 24, 40, 0.12);
}

.ch-hero__ico svg {
  width: 30px;
  height: 30px;
}

.ch-hero__text {
  flex: 1;
  min-width: 0;
}

.ch-hero__kicker {
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--t);
}

.ch-hero__title {
  margin-top: 2px !important;
  font-size: clamp(24px, 2.6vw, 32px);
  font-weight: 700;
  line-height: 1.2;
}

.ch-hero__facts {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 16px;
  margin: 10px 0 0;
  padding: 0;
  font-size: 13px;
  font-weight: 600;
  color: var(--es-muted);
  list-style: none;
}

.ch-hero__facts li {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.ch-hero__facts svg {
  width: 16px;
  height: 16px;
  color: var(--t);
}

.ch-hero__ring {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-shrink: 0;
  padding-left: 22px;
  border-left: 1px solid var(--es-line);
}

.ch-ring strong {
  font-size: 22px;
  font-weight: 700;
  line-height: 1;
}

.ch-ring small {
  font-size: 13px;
}

.ch-ring :deep(.ring__fill) {
  stroke: var(--es-green);
}

.ch-hero__legend {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: var(--es-ink-soft);
  white-space: nowrap;
}

.ch-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  margin-right: 8px;
  border-radius: 50%;
  background: var(--es-line-strong);
}

.ch-dot--ok {
  background: var(--es-green);
}

.ch-dot--review {
  background: var(--es-orange);
}

/* ---------- Onglets collants ---------- */

.ch-tabs {
  position: sticky;
  top: var(--es-top);
  z-index: 20;
  display: flex;
  gap: 4px;
  margin: 0 -8px 22px;
  padding: 8px 8px 0;
  border-bottom: 1px solid var(--es-line);
  background: rgba(245, 247, 251, 0.94);
  backdrop-filter: saturate(1.4) blur(10px);
}

.ch-tab {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 46px;
  padding: 0 16px;
  border: 0;
  background: transparent;
  font: 600 15px var(--es-font);
  color: var(--es-muted);
  cursor: pointer;
}

.ch-tab svg {
  width: 19px;
  height: 19px;
  flex-shrink: 0;
}

.ch-tab::after {
  content: '';
  position: absolute;
  right: 10px;
  bottom: -1px;
  left: 10px;
  height: 3px;
  border-radius: 3px 3px 0 0;
  background: transparent;
}

.ch-tab:hover {
  color: var(--es-ink);
}

.ch-tab.is-active {
  color: var(--es-navy);
}

.ch-tab.is-active::after {
  background: var(--es-navy);
}

.ch-tab__count {
  padding: 1px 8px;
  border-radius: 999px;
  background: var(--es-navy-50);
  font-size: 12px;
  color: var(--es-navy);
}

/* Les ancres du cours doivent passer sous la barre du haut ET les onglets. */
.ch-body :deep(h2),
.ch-body :deep(h3) {
  scroll-margin-top: calc(var(--es-top) + 72px);
}

/* ---------- Chapitres voisins ---------- */

.ch-neighbours {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  margin-top: 36px;
}

.ch-neighbour {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 18px;
  border: 1px solid var(--es-line);
  border-radius: 14px;
  background: #fff;
  text-decoration: none;
  transition: border-color 0.15s ease, box-shadow 0.2s ease;
}

.ch-neighbour:hover {
  border-color: var(--es-navy);
  box-shadow: var(--es-shadow);
}

.ch-neighbour svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  color: var(--es-muted);
}

.ch-neighbour span {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
}

.ch-neighbour small {
  font-size: 12px;
  font-weight: 600;
  color: var(--es-muted);
}

.ch-neighbour strong {
  overflow: hidden;
  font-size: 14px;
  color: var(--es-ink);
  white-space: nowrap;
  text-overflow: ellipsis;
}

.ch-neighbour--next {
  text-align: right;
}

@media (max-width: 1023px) {
  .ch-tabs {
    top: 56px;
  }

  .ch-body :deep(h2),
  .ch-body :deep(h3) {
    scroll-margin-top: 124px;
  }
}

@media (max-width: 760px) {
  .ch-hero {
    margin: -4px 0 12px;
    padding: 16px 16px 18px;
    border-radius: 18px;
  }

  .ch-crumbs {
    display: none;
  }

  .ch-hero__row {
    flex-wrap: wrap;
    gap: 14px;
  }

  .ch-hero__ico {
    width: 48px;
    height: 48px;
    border-radius: 14px;
  }

  .ch-hero__ico svg {
    width: 24px;
    height: 24px;
  }

  .ch-hero__text {
    flex-basis: calc(100% - 64px);
  }

  .ch-hero__kicker {
    font-size: 11px;
  }

  .ch-hero__facts {
    display: none;
  }

  .ch-hero__ring {
    width: 100%;
    padding: 14px 0 0;
    border-top: 1px solid var(--es-line);
    border-left: 0;
  }

  .ch-hero__ring :deep(.ring) {
    width: 64px !important;
    height: 64px !important;
  }

  .ch-ring strong {
    font-size: 17px;
  }

  .ch-hero__legend {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 4px 16px;
  }

  .ch-tabs {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    margin: 0 -16px 16px;
    padding: 0 8px;
    background: rgba(255, 255, 255, 0.96);
  }

  .ch-tab {
    justify-content: center;
    padding: 0 6px;
  }

  .ch-tab__count {
    display: none;
  }

  .ch-neighbours {
    grid-template-columns: minmax(0, 1fr);
    gap: 10px;
  }

  .ch-neighbour--next {
    order: -1;
  }
}

@media (max-width: 374px) {
  .ch-tab svg {
    display: none;
  }
}
</style>
