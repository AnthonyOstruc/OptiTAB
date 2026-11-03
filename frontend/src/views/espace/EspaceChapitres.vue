<template>
  <EspaceLayout title="Mes chapitres">
    <header class="es-page-head ec-head">
      <div>
        <h1 class="es-h1">Mes chapitres</h1>
        <p class="es-sub">
          <template v-if="classe">{{ classe }} · </template>{{ pluriel(chapitres.length, 'chapitre') }}
        </p>
      </div>
      <div v-if="totalExercices" class="ec-overall" :aria-label="`${pctAcquis} % des exercices acquis`">
        <div class="ec-overall__top">
          <span>Progression de l’année</span>
          <strong>{{ pctAcquis }}&nbsp;%</strong>
        </div>
        <div class="es-bar es-bar--lg">
          <span class="es-bar__ok" :style="{ width: pctAcquis + '%' }"></span>
          <span class="es-bar__review" :style="{ width: pourcent(totalARevoir, totalExercices) + '%' }"></span>
        </div>
        <div class="ec-overall__legend">
          <span><i class="ec-dot ec-dot--ok"></i>{{ totalAcquis }} acquis</span>
          <span><i class="ec-dot ec-dot--review"></i>{{ totalARevoir }} à revoir</span>
          <span>{{ totalExercices }} exercices</span>
        </div>
      </div>
    </header>

    <!-- Matières (seulement s'il y en a plusieurs) -->
    <div v-if="matieres.length > 1" class="ec-subjects" role="tablist" aria-label="Matière">
      <button
        v-for="m in matieres"
        :key="m.id"
        type="button"
        role="tab"
        :aria-selected="matiereActive === m.id"
        :class="['ec-subject', { 'is-active': matiereActive === m.id }]"
        @click="matiereActive = m.id"
      >
        {{ m.nom }}
      </button>
    </div>

    <div class="ec-tools">
      <div class="ec-filters" role="group" aria-label="Filtrer les chapitres">
        <button
          v-for="f in filtres"
          :key="f.cle"
          type="button"
          :class="['ec-filter', { 'is-active': filtre === f.cle }]"
          :aria-pressed="filtre === f.cle"
          @click="filtre = f.cle"
        >
          {{ f.label }}
          <span class="ec-filter__count">{{ f.count }}</span>
        </button>
      </div>
      <label class="ec-search">
        <MagnifyingGlassIcon aria-hidden="true" />
        <span class="es-sr-only">Rechercher un chapitre</span>
        <input ref="rechercheRef" v-model="recherche" type="search" placeholder="Rechercher un chapitre" />
      </label>
    </div>

    <div v-if="loading" class="ec-theme">
      <div v-for="n in 5" :key="n" class="es-skeleton" style="height: 72px; margin-bottom: 8px"></div>
    </div>

    <template v-else>
      <section v-for="theme in themes" :key="theme.id" class="ec-theme" :aria-labelledby="`ec-theme-${theme.id}`">
        <div class="ec-theme__head" :style="theme.visuel.style">
          <span class="es-theme-ico"><component :is="theme.visuel.icone" aria-hidden="true" /></span>
          <div class="ec-theme__title">
            <h2 :id="`ec-theme-${theme.id}`" class="es-h2">{{ theme.titre }}</h2>
            <span class="ec-theme__count">{{ pluriel(theme.chapitres.length, 'chapitre') }}</span>
          </div>
          <div v-if="theme.exercices" class="ec-theme__progress">
            <span class="es-bar">
              <span class="ec-theme__fill" :style="{ width: pourcent(theme.acquis, theme.exercices) + '%' }"></span>
            </span>
            <span>{{ pourcent(theme.acquis, theme.exercices) }}&nbsp;%</span>
          </div>
        </div>
        <ol class="es-card ec-list">
          <li v-for="c in theme.chapitres" :key="c.id" class="ec-row">
            <router-link :to="chapitreLink(c.id, c.faits ? 'exercices' : 'cours')" class="ec-row__main">
              <span :class="['ec-num', `ec-num--${etatChapitre(c).cle}`]" aria-hidden="true">
                <CheckIcon v-if="etatChapitre(c).cle === 'done'" />
                <template v-else>{{ c.numero }}</template>
              </span>
              <span class="ec-row__text">
                <span class="ec-row__title">{{ c.titre }}</span>
                <span class="ec-row__meta">
                  <span v-if="c.exercices" class="ec-row__bar">
                    <span class="es-bar">
                      <span class="es-bar__ok" :style="{ width: pourcent(c.acquis, c.exercices) + '%' }"></span>
                      <span class="es-bar__review" :style="{ width: pourcent(c.a_revoir, c.exercices) + '%' }"></span>
                    </span>
                  </span>
                  <span class="ec-row__count">
                    <template v-if="c.exercices">{{ c.acquis }}/{{ c.exercices }} acquis</template>
                    <template v-else>Exercices bientôt disponibles</template>
                  </span>
                </span>
              </span>
              <LockClosedIcon v-if="estVerrouille(c)" class="ec-row__lock" aria-label="Réservé aux abonnés" />
              <span v-else :class="['es-pill', `es-pill--${etatChapitre(c).cle}`, 'ec-row__pill']">{{ etatChapitre(c).label }}</span>
            </router-link>
            <div class="ec-row__actions" :aria-label="`Ouvrir ${c.titre}`">
              <router-link :to="chapitreLink(c.id, 'cours')" class="ec-action" title="Cours">
                <BookOpenIcon aria-hidden="true" /><span>Cours</span>
              </router-link>
              <router-link :to="chapitreLink(c.id, 'fiche')" class="ec-action" title="Fiche de synthèse">
                <DocumentTextIcon aria-hidden="true" /><span>Fiche</span>
              </router-link>
              <router-link :to="chapitreLink(c.id, 'exercices')" class="ec-action" title="Exercices">
                <PencilSquareIcon aria-hidden="true" /><span>Exercices</span>
              </router-link>
            </div>
          </li>
        </ol>
      </section>

      <p v-if="!themes.length" class="es-empty">
        <strong>Aucun chapitre ne correspond</strong>
        Essaie un autre filtre ou une autre recherche.
      </p>
    </template>
  </EspaceLayout>
</template>

<script setup>
import { computed, nextTick, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import {
  BookOpenIcon,
  CheckIcon,
  DocumentTextIcon,
  LockClosedIcon,
  MagnifyingGlassIcon,
  PencilSquareIcon
} from '@heroicons/vue/24/outline'
import EspaceLayout from '@/components/espace/EspaceLayout.vue'
import { useProgression } from '@/composables/useProgression'
import { useUserStore } from '@/stores/user'
import { useSubscriptionStore } from '@/stores/subscription'
import { appliquerExemple, chapitreLink, peutVoirExemple } from '@/config/espace'
import { etatChapitre, pluriel, pourcent } from '@/utils/espaceFormat'
import { indexThemes, visuelTheme } from '@/utils/espaceTheme'

const route = useRoute()
const userStore = useUserStore()
const subscriptionStore = useSubscriptionStore()
const { progression: progressionServeur, charger } = useProgression()

const loading = ref(true)
const exemple = computed(() => route.query.exemple === '1' && peutVoirExemple(userStore))
const progression = computed(() => (exemple.value ? appliquerExemple(progressionServeur.value) : progressionServeur.value))
const filtre = ref('tous')
const recherche = ref('')
const rechercheRef = ref(null)
const matiereActive = ref(null)

const classe = computed(() => userStore.niveau_pays?.nom || progression.value?.niveau || '')

// Numérotation continue dans l'ordre du programme.
const tousChapitres = computed(() => (progression.value?.chapitres || []).map((c, i) => ({ ...c, numero: i + 1 })))

const matieres = computed(() => {
  const vues = new Map()
  tousChapitres.value.forEach((c) => { if (!vues.has(c.matiere_id)) vues.set(c.matiere_id, { id: c.matiere_id, nom: c.matiere }) })
  return [...vues.values()]
})

const chapitres = computed(() => {
  const id = matiereActive.value ?? matieres.value[0]?.id
  return matieres.value.length > 1 ? tousChapitres.value.filter((c) => c.matiere_id === id) : tousChapitres.value
})

const totalExercices = computed(() => chapitres.value.reduce((s, c) => s + (c.exercices || 0), 0))
const totalAcquis = computed(() => chapitres.value.reduce((s, c) => s + c.acquis, 0))
const totalARevoir = computed(() => chapitres.value.reduce((s, c) => s + c.a_revoir, 0))
const pctAcquis = computed(() => pourcent(totalAcquis.value, totalExercices.value))

const FILTRES = [
  { cle: 'tous', label: 'Tous', test: () => true },
  { cle: 'progress', label: 'En cours', test: (c) => c.faits > 0 && etatChapitre(c).cle !== 'done' },
  { cle: 'review', label: 'À revoir', test: (c) => c.a_revoir > 0 },
  { cle: 'new', label: 'À commencer', test: (c) => !c.faits },
  { cle: 'done', label: 'Maîtrisés', test: (c) => etatChapitre(c).cle === 'done' }
]

const filtres = computed(() => FILTRES.map((f) => ({ ...f, count: chapitres.value.filter(f.test).length })))

const normaliser = (s) => String(s || '').normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase()

const ordreThemes = computed(() => indexThemes(tousChapitres.value))

const themes = computed(() => {
  const test = FILTRES.find((f) => f.cle === filtre.value)?.test || (() => true)
  const q = normaliser(recherche.value.trim())
  const groupes = new Map()
  chapitres.value
    .filter((c) => test(c) && (!q || normaliser(c.titre).includes(q) || normaliser(c.theme).includes(q)))
    .forEach((c) => {
      if (!groupes.has(c.theme_id)) {
        groupes.set(c.theme_id, { id: c.theme_id, titre: c.theme, chapitres: [], visuel: visuelTheme(c.theme, ordreThemes.value.get(c.theme_id)) })
      }
      groupes.get(c.theme_id).chapitres.push(c)
    })
  // Progression du thème entier (pas seulement des chapitres filtrés).
  return [...groupes.values()].map((g) => {
    const tous = chapitres.value.filter((c) => c.theme_id === g.id)
    return { ...g, exercices: tous.reduce((s, c) => s + (c.exercices || 0), 0), acquis: tous.reduce((s, c) => s + c.acquis, 0) }
  })
})

// Accès : abonnés, administrateurs, et chapitre démo de la classe pour les autres.
const demoNotionId = computed(() => Number(userStore.niveau_pays?.demo_notion) || null)
const aAcces = computed(() => {
  if (userStore.isAdmin || subscriptionStore.hasAccess) return true
  const niveauId = userStore.niveau_pays?.id
  return niveauId ? subscriptionStore.accessForLevel(niveauId) : false
})
const estVerrouille = (c) => Boolean(subscriptionStore.status) && !aAcces.value && c.id !== demoNotionId.value

onMounted(async () => {
  await charger()
  loading.value = false
  subscriptionStore.fetchStatus().catch(() => {})
  // Arrivée depuis la loupe de la barre du haut (téléphone).
  if (route.query.recherche === '1') {
    await nextTick()
    rechercheRef.value?.focus()
  }
})
</script>

<style scoped>
.ec-head {
  align-items: center;
}

.ec-overall {
  width: min(380px, 100%);
  padding: 14px 16px;
  border: 1px solid var(--es-line);
  border-radius: 14px;
  background: #fff;
}

.ec-overall__top {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--es-muted);
}

.ec-overall__top strong {
  font-size: 20px;
  color: var(--es-ink);
}

.ec-overall__legend {
  display: flex;
  flex-wrap: wrap;
  gap: 4px 14px;
  margin-top: 8px;
  font-size: 12px;
  font-weight: 600;
  color: var(--es-muted);
}

.ec-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  margin-right: 5px;
  border-radius: 50%;
}

.ec-dot--ok {
  background: var(--es-green);
}

.ec-dot--review {
  background: var(--es-orange);
}

/* ---------- Matières, filtres, recherche ---------- */

.ec-subjects {
  display: inline-flex;
  gap: 4px;
  margin-bottom: 16px;
  padding: 4px;
  border-radius: 12px;
  background: var(--es-navy-50);
}

.ec-subject {
  min-height: 38px;
  padding: 0 16px;
  border: 0;
  border-radius: 9px;
  background: transparent;
  font: 600 14px var(--es-font);
  color: var(--es-ink-soft);
  cursor: pointer;
}

.ec-subject.is-active {
  background: #fff;
  color: var(--es-navy);
  box-shadow: 0 1px 3px rgba(16, 24, 40, 0.1);
}

.ec-tools {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 24px;
}

.ec-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.ec-filter {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 38px;
  padding: 0 14px;
  border: 1px solid var(--es-line-strong);
  border-radius: 999px;
  background: #fff;
  font: 600 14px var(--es-font);
  color: var(--es-ink-soft);
  cursor: pointer;
}

.ec-filter:hover {
  border-color: var(--es-navy);
}

.ec-filter.is-active {
  border-color: var(--es-navy);
  background: var(--es-navy);
  color: #fff;
}

.ec-filter__count {
  min-width: 22px;
  padding: 1px 7px;
  border-radius: 999px;
  background: var(--es-bg);
  font-size: 12px;
  color: var(--es-muted);
}

.ec-filter.is-active .ec-filter__count {
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
}

.ec-search {
  position: relative;
  display: flex;
  align-items: center;
  width: min(280px, 100%);
}

.ec-search svg {
  position: absolute;
  left: 12px;
  width: 18px;
  height: 18px;
  color: var(--es-muted);
  pointer-events: none;
}

.ec-search input {
  width: 100%;
  min-height: 40px;
  padding: 0 12px 0 38px;
  border: 1px solid var(--es-line-strong);
  border-radius: 12px;
  background: #fff;
  font: 500 15px var(--es-font);
  color: var(--es-ink);
}

.ec-search input:focus {
  border-color: var(--es-navy);
  outline: 3px solid rgba(27, 60, 142, 0.15);
}

/* ---------- Thèmes et lignes ---------- */

.ec-theme {
  margin-bottom: 28px;
}

.ec-theme__head {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.ec-theme__title {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
}

.ec-theme__count {
  font-size: 13px;
  font-weight: 600;
  color: var(--es-muted);
}

.ec-theme__progress {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 200px;
  font-size: 13px;
  font-weight: 700;
  color: var(--t);
}

.ec-theme__progress .es-bar {
  flex: 1;
  height: 6px;
  background: var(--t-bg);
}

.ec-theme__fill {
  background: var(--t);
}

.ec-list {
  margin: 0;
  padding: 4px 0;
  list-style: none;
}

.ec-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 16px 0 0;
}

.ec-row + .ec-row {
  border-top: 1px solid var(--es-line);
}

.ec-row__main {
  display: flex;
  flex: 1;
  align-items: center;
  gap: 14px;
  min-width: 0;
  padding: 14px 8px 14px 18px;
  text-decoration: none;
}

.ec-row__main:hover .ec-row__title {
  color: var(--es-navy);
}

.ec-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  flex-shrink: 0;
  border-radius: 10px;
  background: var(--es-bg);
  font-size: 14px;
  font-weight: 700;
  color: var(--es-muted);
}

.ec-num svg {
  width: 18px;
  height: 18px;
}

.ec-num--progress {
  background: var(--es-navy-50);
  color: var(--es-navy);
}

.ec-num--review {
  background: var(--es-orange-50);
  color: var(--es-orange-700);
}

.ec-num--done {
  background: var(--es-green);
  color: #fff;
}

.ec-row__text {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.ec-row__title {
  font-size: 15px;
  font-weight: 600;
  line-height: 1.35;
  color: var(--es-ink);
  transition: color 0.15s ease;
}

.ec-row__meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.ec-row__bar {
  width: 140px;
}

.ec-row__count {
  font-size: 12px;
  font-weight: 600;
  color: var(--es-muted);
  white-space: nowrap;
}

.ec-row__lock {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  color: #98a2b3;
}

.ec-row__actions {
  display: flex;
  gap: 4px;
}

.ec-action {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 34px;
  padding: 0 10px;
  border-radius: 9px;
  font-size: 13px;
  font-weight: 600;
  color: var(--es-ink-soft);
  text-decoration: none;
}

.ec-action svg {
  width: 17px;
  height: 17px;
  color: var(--es-muted);
}

.ec-action:hover {
  background: var(--es-navy-50);
  color: var(--es-navy);
}

.ec-action:hover svg {
  color: var(--es-navy);
}

@media (max-width: 1180px) {
  .ec-action span {
    display: none;
  }
}

@media (max-width: 760px) {
  .ec-head {
    align-items: stretch;
  }

  .ec-overall {
    width: 100%;
  }

  .ec-tools {
    flex-direction: column;
    align-items: stretch;
  }

  .ec-filters {
    flex-wrap: nowrap;
    margin: 0 -16px;
    padding: 0 16px 2px;
    overflow-x: auto;
    scrollbar-width: none;
  }

  .ec-filters::-webkit-scrollbar {
    display: none;
  }

  .ec-filter {
    flex-shrink: 0;
  }

  .ec-search {
    width: 100%;
  }

  .ec-row {
    padding: 0;
  }

  .ec-row__main {
    padding: 14px 14px;
  }

  .ec-row__actions {
    display: none;
  }

  .ec-row__pill {
    display: none;
  }

  .ec-row__bar {
    width: 96px;
  }

  .ec-theme__progress {
    width: 96px;
  }
}
</style>
