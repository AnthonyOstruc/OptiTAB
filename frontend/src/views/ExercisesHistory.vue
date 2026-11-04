<template>
  <EspaceLayout title="Historique">
    <header class="es-page-head">
      <div>
        <h1 class="es-h1">Historique</h1>
        <p class="es-sub">Tous les exercices que tu as faits, chapitre par chapitre.</p>
      </div>
    </header>

    <!-- Chargement -->
    <div v-if="etat === 'chargement'" aria-busy="true" aria-label="Chargement de l’historique">
      <div class="hi-stats">
        <div v-for="i in 4" :key="i" class="es-skeleton hi-skel hi-skel--stat"></div>
      </div>
      <div class="es-skeleton hi-skel hi-skel--card"></div>
    </div>

    <!-- Erreur -->
    <div v-else-if="etat === 'erreur'" class="es-empty hi-message">
      <strong>Impossible de charger ton historique</strong>
      Vérifie ta connexion, puis réessaie.
      <button type="button" class="es-btn es-btn--ghost es-btn--sm" @click="charger(true)">Réessayer</button>
    </div>

    <!-- Aucun exercice -->
    <div v-else-if="!exercices.length" class="es-card hi-vide">
      <span class="hi-vide__ico" aria-hidden="true"><ClockIcon /></span>
      <h2 class="es-h2">Aucun exercice pour l’instant</h2>
      <p>Dès que tu indiques « J’ai compris » ou « À revoir » sur un exercice, il apparaît ici.</p>
      <router-link :to="ESPACE_ROUTES.chapitres" class="es-btn">Voir mes chapitres</router-link>
    </div>

    <template v-else>
      <!-- Chiffres clés -->
      <section class="hi-stats" aria-label="En résumé">
        <div class="es-card hi-stat">
          <span class="hi-stat__label">Exercices faits</span>
          <strong class="hi-stat__value">{{ total }}</strong>
          <span class="hi-stat__hint">dans {{ pluriel(chapitres.length, 'chapitre') }}</span>
        </div>
        <div class="es-card hi-stat hi-stat--ok">
          <span class="hi-stat__label"><i aria-hidden="true"></i>Compris</span>
          <strong class="hi-stat__value">{{ compris }}</strong>
          <span class="hi-stat__hint">{{ pourcent(compris, total) }}&nbsp;% de tes exercices</span>
        </div>
        <div class="es-card hi-stat hi-stat--review">
          <span class="hi-stat__label"><i aria-hidden="true"></i>À revoir</span>
          <strong class="hi-stat__value">{{ aRevoir }}</strong>
          <span class="hi-stat__hint">{{ aRevoir ? 'à retravailler' : 'rien à reprendre' }}</span>
        </div>
        <div class="es-card hi-stat">
          <span class="hi-stat__label">Cette semaine</span>
          <strong class="hi-stat__value">{{ cetteSemaine }}</strong>
          <span class="hi-stat__hint">{{ cetteSemaine > 1 ? 'exercices' : 'exercice' }} sur 7 jours</span>
        </div>
      </section>

      <!-- Par chapitre -->
      <section class="es-card hi-card" aria-labelledby="hi-chapitres-titre">
        <div class="hi-card__head">
          <h2 id="hi-chapitres-titre" class="es-h2">Par chapitre</h2>
          <label class="hi-select">
            <span class="es-sr-only">Trier les chapitres</span>
            <ArrowsUpDownIcon aria-hidden="true" />
            <select v-model="tri">
              <option value="recent">Activité récente</option>
              <option value="faits">Les plus travaillés</option>
              <option value="revoir">À revoir d’abord</option>
              <option value="programme">Ordre du programme</option>
            </select>
          </label>
        </div>

        <ul class="hi-chaps">
          <li v-for="c in chapitresAffiches" :key="c.cle">
            <component :is="c.lien ? 'router-link' : 'div'" :to="c.lien || undefined" :class="['hi-chap', { 'hi-chap--lien': c.lien }]">
              <span class="es-theme-ico es-theme-ico--sm" :style="c.visuel.style" aria-hidden="true">
                <component :is="c.visuel.icone" />
              </span>
              <span class="hi-chap__main">
                <span class="hi-chap__titre">{{ c.titre }}</span>
                <span class="hi-chap__meta">{{ c.meta }}</span>
              </span>
              <span class="hi-chap__prog">
                <span class="es-bar" aria-hidden="true">
                  <span class="es-bar__ok" :style="{ width: pourcent(c.compris, c.faits) + '%' }"></span>
                  <span class="es-bar__review" :style="{ width: pourcent(c.aRevoir, c.faits) + '%' }"></span>
                </span>
                <span class="hi-chap__compte">
                  <span class="hi-dot hi-dot--ok" aria-hidden="true"></span>{{ c.compris }} compris
                  <span class="hi-dot hi-dot--review" aria-hidden="true"></span>{{ c.aRevoir }} à revoir
                </span>
              </span>
              <span :class="['hi-pct', `hi-pct--${niveauReussite(c.compris, c.faits)}`]" :title="`${c.compris} compris sur ${c.faits}`">
                {{ pourcent(c.compris, c.faits) }}&nbsp;%
              </span>
              <ChevronRightIcon v-if="c.lien" class="hi-chap__chev" aria-hidden="true" />
              <span v-else class="hi-chap__chev" aria-hidden="true"></span>
            </component>
          </li>
        </ul>

        <button v-if="chapitres.length > CHAPITRES_VISIBLES" type="button" class="hi-plus" @click="tousLesChapitres = !tousLesChapitres">
          {{ tousLesChapitres ? 'Réduire la liste' : chapitres.length - CHAPITRES_VISIBLES > 1 ? `Afficher les ${chapitres.length - CHAPITRES_VISIBLES} autres chapitres` : 'Afficher l’autre chapitre' }}
          <ChevronDownIcon :class="{ 'is-up': tousLesChapitres }" aria-hidden="true" />
        </button>
      </section>

      <!-- Tous les exercices -->
      <section class="es-card hi-card" aria-labelledby="hi-exercices-titre">
        <div class="hi-card__head hi-card__head--wrap">
          <h2 id="hi-exercices-titre" class="es-h2">Tous mes exercices</h2>
          <div class="hi-filtres">
            <div class="hi-seg" role="group" aria-label="Afficher">
              <button
                v-for="f in FILTRES"
                :key="f.cle"
                type="button"
                :class="['hi-seg__btn', { 'is-active': filtre === f.cle }]"
                :aria-pressed="filtre === f.cle"
                @click="filtre = f.cle"
              >
                {{ f.label }} <span class="hi-seg__n">{{ compte(f.cle) }}</span>
              </button>
            </div>
            <label v-if="chapitres.length > 1" class="hi-select hi-select--chap">
              <span class="es-sr-only">Chapitre</span>
              <select v-model="filtreChapitre">
                <option value="">Tous les chapitres</option>
                <option v-for="c in chapitresParTitre" :key="c.cle" :value="c.cle">{{ c.titre }}</option>
              </select>
            </label>
          </div>
        </div>

        <p v-if="!exercicesFiltres.length" class="hi-aucun">Aucun exercice avec ces filtres.</p>

        <div v-for="g in groupes" :key="g.cle" class="hi-jour">
          <h3 class="hi-jour__titre">{{ g.titre }}</h3>
          <ul class="hi-exs">
            <li v-for="e in g.items" :key="e.id">
              <router-link :to="lienExercice(e)" class="hi-ex">
                <span :class="['hi-ex__etat', e.est_correct ? 'is-ok' : 'is-review']" aria-hidden="true">
                  <CheckIcon v-if="e.est_correct" />
                  <ArrowPathIcon v-else />
                </span>
                <span class="hi-ex__main">
                  <span class="hi-ex__titre">
                    <span v-if="e.type" class="hi-ex__type">{{ e.type }}</span>{{ e.nom }}
                  </span>
                  <span class="hi-ex__meta">{{ e.notion?.titre }}</span>
                </span>
                <span :class="['es-pill', e.est_correct ? 'es-pill--done' : 'es-pill--review', 'hi-ex__pill']" aria-hidden="true">
                  {{ e.est_correct ? 'Compris' : 'À revoir' }}
                </span>
                <span class="es-sr-only">{{ e.est_correct ? 'Compris' : 'À revoir' }}</span>
                <time class="hi-ex__heure" :datetime="e.date_creation">{{ heure(e.date_creation) }}</time>
              </router-link>
            </li>
          </ul>
        </div>

        <button v-if="restants > 0" type="button" class="hi-plus" @click="limite += PAR_PAGE">
          Afficher {{ Math.min(restants, PAR_PAGE) }} exercices de plus
          <ChevronDownIcon aria-hidden="true" />
        </button>
      </section>
    </template>
  </EspaceLayout>
</template>

<script setup>
// Historique des exercices (espace élève) : chiffres clés, progression par
// chapitre et liste datée de tous les exercices marqués « compris » ou « à revoir ».
import { computed, onMounted, ref, watch } from 'vue'
import {
  ArrowPathIcon,
  ArrowsUpDownIcon,
  CheckIcon,
  ChevronDownIcon,
  ChevronRightIcon,
  ClockIcon
} from '@heroicons/vue/24/outline'
import EspaceLayout from '@/components/espace/EspaceLayout.vue'
import apiClient, { apiUtils } from '@/api/client'
import { useProgression } from '@/composables/useProgression'
import { ESPACE_ROUTES, chapitreLink } from '@/config/espace'
import { pluriel, pourcent } from '@/utils/espaceFormat'
import { indexThemes, visuelTheme } from '@/utils/espaceTheme'

const URL_STATS = '/api/suivis/exercices/stats/'
const CHAPITRES_VISIBLES = 8
const PAR_PAGE = 20
const FILTRES = [
  { cle: 'tous', label: 'Tous' },
  { cle: 'compris', label: 'Compris' },
  { cle: 'revoir', label: 'À revoir' }
]

const { progression, charger: chargerProgression } = useProgression()

const etat = ref('chargement')
const brut = ref([])
const tri = ref('recent')
const tousLesChapitres = ref(false)
const filtre = ref('tous')
const filtreChapitre = ref('')
const limite = ref(PAR_PAGE)

async function charger(force = false) {
  if (!brut.value.length) etat.value = 'chargement'
  try {
    const [res] = await Promise.all([
      force ? apiClient.get(URL_STATS) : apiUtils.cachedGet(URL_STATS, { ttl: 30000 }),
      chargerProgression().catch(() => null)
    ])
    brut.value = Array.isArray(res?.data?.exercice_list) ? res.data.exercice_list : []
    etat.value = 'pret'
  } catch (_) {
    etat.value = 'erreur'
  }
}

onMounted(() => charger())

// « Découverte - Lire graphiquement… » → type « Découverte » + nom.
function decouperTitre(titre = '') {
  const m = String(titre).match(/^([\p{Lu}][\p{L}’' ]{2,24}?)\s+[-–]\s+(.+)$/u)
  return m ? { type: m[1], nom: m[2] } : { type: '', nom: titre }
}

const exercices = computed(() => brut.value
  .map((e) => ({ ...e, ...decouperTitre(e.exercice_titre) }))
  .sort((a, b) => new Date(b.date_creation) - new Date(a.date_creation)))

const total = computed(() => exercices.value.length)
const compris = computed(() => exercices.value.filter((e) => e.est_correct).length)
const aRevoir = computed(() => total.value - compris.value)
const cetteSemaine = computed(() => {
  const depuis = Date.now() - 7 * 86400000
  return exercices.value.filter((e) => new Date(e.date_creation).getTime() >= depuis).length
})

// Chapitres de la classe actuelle (ordre du programme, couleurs des thèmes).
const chapitresClasse = computed(() => progression.value?.chapitres || [])
const ordreClasse = computed(() => new Map(chapitresClasse.value.map((c, i) => [String(c.id), i])))
const themesClasse = computed(() => indexThemes(chapitresClasse.value))
const plusieursMatieres = computed(() => new Set(exercices.value.map((e) => e.matiere?.id)).size > 1)

const chapitres = computed(() => {
  const parNotion = new Map()
  const themesHorsClasse = new Map()
  for (const e of exercices.value) {
    const cle = String(e.notion?.id ?? '')
    if (!parNotion.has(cle)) {
      const dansLaClasse = ordreClasse.value.has(cle)
      const themeId = e.theme?.id
      let indexTheme = themesClasse.value.get(themeId)
      if (indexTheme === undefined) {
        if (!themesHorsClasse.has(themeId)) themesHorsClasse.set(themeId, themesClasse.value.size + themesHorsClasse.size)
        indexTheme = themesHorsClasse.get(themeId)
      }
      const meta = [plusieursMatieres.value ? e.matiere?.titre : '', e.theme?.titre, dansLaClasse ? '' : 'autre classe']
        .filter(Boolean).join(' · ')
      parNotion.set(cle, {
        cle,
        titre: e.notion?.titre || 'Chapitre',
        meta,
        visuel: visuelTheme(e.theme?.titre || '', indexTheme),
        lien: cle ? chapitreLink(cle, 'exercices') : null,
        ordre: dansLaClasse ? ordreClasse.value.get(cle) : Infinity,
        faits: 0,
        compris: 0,
        aRevoir: 0,
        derniere: 0
      })
    }
    const c = parNotion.get(cle)
    c.faits += 1
    if (e.est_correct) c.compris += 1
    else c.aRevoir += 1
    c.derniere = Math.max(c.derniere, new Date(e.date_creation).getTime())
  }
  return [...parNotion.values()]
})

const TRIS = {
  recent: (a, b) => b.derniere - a.derniere,
  faits: (a, b) => b.faits - a.faits || b.derniere - a.derniere,
  revoir: (a, b) => b.aRevoir - a.aRevoir || pourcent(a.compris, a.faits) - pourcent(b.compris, b.faits),
  programme: (a, b) => a.ordre - b.ordre || a.titre.localeCompare(b.titre, 'fr')
}
const chapitresTries = computed(() => [...chapitres.value].sort(TRIS[tri.value]))
const chapitresAffiches = computed(() => (tousLesChapitres.value ? chapitresTries.value : chapitresTries.value.slice(0, CHAPITRES_VISIBLES)))
const chapitresParTitre = computed(() => [...chapitres.value].sort((a, b) => a.titre.localeCompare(b.titre, 'fr')))

function niveauReussite(part, totalFaits) {
  const p = pourcent(part, totalFaits)
  if (p >= 80) return 'ok'
  if (p >= 50) return 'mid'
  return 'low'
}

// Liste des exercices : filtres, regroupement par jour, « afficher plus ».
function compte(cle) {
  const base = filtreChapitre.value ? exercices.value.filter((e) => String(e.notion?.id) === filtreChapitre.value) : exercices.value
  if (cle === 'compris') return base.filter((e) => e.est_correct).length
  if (cle === 'revoir') return base.filter((e) => !e.est_correct).length
  return base.length
}

const exercicesFiltres = computed(() => exercices.value.filter((e) => {
  if (filtreChapitre.value && String(e.notion?.id) !== filtreChapitre.value) return false
  if (filtre.value === 'compris') return e.est_correct
  if (filtre.value === 'revoir') return !e.est_correct
  return true
}))

watch([filtre, filtreChapitre], () => { limite.value = PAR_PAGE })

const restants = computed(() => Math.max(0, exercicesFiltres.value.length - limite.value))

const cleJour = (d) => `${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`

function titreJour(d) {
  const aujourdHui = new Date()
  const hier = new Date(Date.now() - 86400000)
  if (cleJour(d) === cleJour(aujourdHui)) return 'Aujourd’hui'
  if (cleJour(d) === cleJour(hier)) return 'Hier'
  const options = { weekday: 'long', day: 'numeric', month: 'long' }
  if (d.getFullYear() !== aujourdHui.getFullYear()) options.year = 'numeric'
  const texte = d.toLocaleDateString('fr-FR', options)
  return texte.charAt(0).toUpperCase() + texte.slice(1)
}

const groupes = computed(() => {
  const liste = []
  for (const e of exercicesFiltres.value.slice(0, limite.value)) {
    const d = new Date(e.date_creation)
    const cle = cleJour(d)
    if (!liste.length || liste[liste.length - 1].cle !== cle) liste.push({ cle, titre: titreJour(d), items: [] })
    liste[liste.length - 1].items.push(e)
  }
  return liste
})

const heure = (iso) => new Date(iso).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })

// L'exercice s'ouvre toujours dans la page de son chapitre (nouvel affichage),
// même quand le chapitre appartient à une autre classe.
function lienExercice(e) {
  const notionId = e.notion?.id
  if (notionId) return chapitreLink(String(notionId), 'exercices', e.exercice_id)
  return { name: 'ExerciceDetail', params: { exerciceId: String(e.exercice_id) } }
}
</script>

<style scoped>
/* ---------- Chargement, erreur, vide ---------- */

.hi-skel--stat {
  height: 108px;
  border-radius: var(--es-radius);
}

.hi-skel--card {
  height: 420px;
  margin-top: 20px;
  border-radius: var(--es-radius);
}

.hi-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.hi-message .es-btn {
  margin-top: 10px;
}

.hi-vide {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 48px 24px;
  text-align: center;
}

.hi-vide__ico {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  margin-bottom: 6px;
  border-radius: 16px;
  background: var(--es-navy-50);
  color: var(--es-navy);
}

.hi-vide__ico svg {
  width: 28px;
  height: 28px;
}

.hi-vide p {
  max-width: 420px;
  margin-bottom: 12px !important;
  font-size: 15px;
  line-height: 1.5;
  color: var(--es-muted);
}

/* ---------- Chiffres clés ---------- */

.hi-stats {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.hi-stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 18px 20px;
}

.hi-stat__label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--es-muted);
}

.hi-stat__label i {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.hi-stat--ok .hi-stat__label i {
  background: var(--es-green);
}

.hi-stat--review .hi-stat__label i {
  background: var(--es-orange);
}

.hi-stat__value {
  font-size: 30px;
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.02em;
  color: var(--es-ink);
}

.hi-stat--ok .hi-stat__value {
  color: var(--es-green-700);
}

.hi-stat--review .hi-stat__value {
  color: var(--es-orange-700);
}

.hi-stat__hint {
  font-size: 13px;
  color: var(--es-muted);
}

/* ---------- Cartes ---------- */

.hi-card {
  margin-top: 20px;
  padding-bottom: 8px;
}

.hi-card__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 18px 20px 14px;
  border-bottom: 1px solid var(--es-line);
}

.hi-card__head--wrap {
  flex-wrap: wrap;
}

.hi-card__head h2 {
  white-space: nowrap;
}

.hi-select {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.hi-select svg {
  position: absolute;
  left: 11px;
  width: 16px;
  height: 16px;
  color: var(--es-muted);
  pointer-events: none;
}

.hi-select select {
  height: 38px;
  padding: 0 34px 0 34px;
  border: 1px solid var(--es-line-strong);
  border-radius: 10px;
  background: #fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='%23667085'%3E%3Cpath d='M5.3 7.3a1 1 0 0 1 1.4 0L10 10.6l3.3-3.3a1 1 0 1 1 1.4 1.4l-4 4a1 1 0 0 1-1.4 0l-4-4a1 1 0 0 1 0-1.4Z'/%3E%3C/svg%3E") no-repeat right 10px center / 16px;
  font: 600 14px var(--es-font);
  color: var(--es-ink-soft);
  cursor: pointer;
  appearance: none;
}

.hi-select--chap select {
  max-width: 260px;
  padding-left: 12px;
  text-overflow: ellipsis;
}

.hi-select select:hover {
  border-color: var(--es-navy);
}

.hi-plus {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: calc(100% - 24px);
  min-height: 42px;
  margin: 6px 12px 4px;
  border: 0;
  border-radius: 10px;
  background: none;
  font: 600 14px var(--es-font);
  color: var(--es-navy);
  cursor: pointer;
}

.hi-plus:hover {
  background: var(--es-navy-50);
}

.hi-plus svg {
  width: 16px;
  height: 16px;
  transition: transform 0.2s ease;
}

.hi-plus svg.is-up {
  transform: rotate(180deg);
}

/* ---------- Par chapitre ---------- */

.hi-chaps,
.hi-exs {
  margin: 0;
  padding: 0;
  list-style: none;
}

.hi-chaps {
  padding: 6px 8px 0;
}

.hi-chap {
  display: grid;
  grid-template-columns: 32px minmax(0, 1fr) minmax(180px, 240px) 64px 18px;
  align-items: center;
  gap: 16px;
  padding: 12px;
  border-radius: 12px;
  color: inherit;
  text-decoration: none;
}

.hi-chaps li + li .hi-chap {
  box-shadow: 0 -1px 0 var(--es-line);
}

.hi-chap--lien {
  transition: background-color 0.15s ease;
}

.hi-chap--lien:hover {
  background: var(--es-bg);
}

.hi-chaps li + li .hi-chap--lien:hover,
.hi-chaps li:hover + li .hi-chap {
  box-shadow: none;
}

.hi-chap__main {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.hi-chap__titre {
  font-size: 15px;
  font-weight: 600;
  line-height: 1.35;
  color: var(--es-ink);
}

.hi-chap__meta {
  font-size: 13px;
  color: var(--es-muted);
}

.hi-chap__prog {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.hi-chap__compte {
  display: inline-flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 2px 6px;
  font-size: 12.5px;
  color: var(--es-muted);
}

.hi-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.hi-dot--ok {
  background: var(--es-green);
}

.hi-dot--review {
  margin-left: 6px;
  background: var(--es-orange);
}

.hi-pct {
  justify-self: end;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 700;
  white-space: nowrap;
}

.hi-pct--ok {
  background: var(--es-green-50);
  color: var(--es-green-700);
}

.hi-pct--mid {
  background: var(--es-navy-50);
  color: var(--es-navy);
}

.hi-pct--low {
  background: var(--es-orange-50);
  color: var(--es-orange-700);
}

.hi-chap__chev {
  width: 18px;
  height: 18px;
  color: #98a2b3;
}

.hi-chap--lien:hover .hi-chap__chev {
  color: var(--es-navy);
}

/* ---------- Tous les exercices ---------- */

.hi-filtres {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
}

.hi-seg {
  display: inline-flex;
  padding: 3px;
  border-radius: 12px;
  background: var(--es-bg);
  box-shadow: inset 0 0 0 1px var(--es-line);
}

.hi-seg__btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 32px;
  padding: 0 12px;
  border: 0;
  border-radius: 9px;
  background: none;
  font: 600 13.5px var(--es-font);
  color: var(--es-muted);
  white-space: nowrap;
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease, box-shadow 0.15s ease;
}

.hi-seg__btn:hover {
  color: var(--es-ink);
}

.hi-seg__btn.is-active {
  background: #fff;
  color: var(--es-navy);
  box-shadow: 0 1px 2px rgba(16, 24, 40, 0.08), 0 0 0 1px var(--es-line);
}

.hi-seg__n {
  min-width: 20px;
  padding: 1px 6px;
  border-radius: 999px;
  background: rgba(16, 24, 40, 0.06);
  font-size: 12px;
  text-align: center;
}

.hi-seg__btn.is-active .hi-seg__n {
  background: var(--es-navy-50);
}

.hi-aucun {
  padding: 32px 20px;
  font-size: 14px;
  color: var(--es-muted);
  text-align: center;
}

.hi-jour {
  padding: 0 8px;
}

.hi-jour__titre {
  margin: 0;
  padding: 18px 12px 8px;
  font-size: 12px !important;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--es-muted) !important;
}

.hi-ex {
  display: grid;
  grid-template-columns: 32px minmax(0, 1fr) auto 48px;
  align-items: center;
  gap: 14px;
  padding: 10px 12px;
  border-radius: 12px;
  color: inherit;
  text-decoration: none;
  transition: background-color 0.15s ease;
}

.hi-ex:hover {
  background: var(--es-bg);
}

.hi-ex__etat {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
}

.hi-ex__etat svg {
  width: 17px;
  height: 17px;
  stroke-width: 2.2;
}

.hi-ex__etat.is-ok {
  background: var(--es-green-50);
  color: var(--es-green-700);
}

.hi-ex__etat.is-review {
  background: var(--es-orange-50);
  color: var(--es-orange-700);
}

.hi-ex__main {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.hi-ex__titre {
  overflow: hidden;
  font-size: 14.5px;
  font-weight: 600;
  line-height: 1.4;
  color: var(--es-ink);
  white-space: nowrap;
  text-overflow: ellipsis;
}

.hi-ex:hover .hi-ex__titre {
  color: var(--es-navy);
}

.hi-ex__type {
  margin-right: 8px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.02em;
  color: var(--es-muted);
}

.hi-ex__meta {
  overflow: hidden;
  font-size: 13px;
  color: var(--es-muted);
  white-space: nowrap;
  text-overflow: ellipsis;
}

.hi-ex__heure {
  font-size: 13px;
  color: var(--es-muted);
  text-align: right;
  font-variant-numeric: tabular-nums;
}

/* ---------- Tablette ---------- */

@media (max-width: 1100px) {
  .hi-chap {
    grid-template-columns: 32px minmax(0, 1fr) 160px 60px 18px;
    gap: 12px;
  }
}

/* ---------- Téléphone ---------- */

@media (max-width: 760px) {
  .hi-stats {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
  }

  .hi-stat {
    padding: 14px 16px;
  }

  .hi-stat__value {
    font-size: 26px;
  }

  .hi-stat__hint {
    font-size: 12px;
  }

  .hi-card {
    margin-top: 14px;
  }

  .hi-card__head {
    padding: 16px 16px 12px;
  }

  /* Menus en 16 px sur téléphone (pas de zoom automatique) : sans icône,
     ils peuvent rétrécir pour tenir à côté du titre. */
  .hi-card__head > .hi-select {
    flex: 0 1 auto;
    min-width: 0;
  }

  .hi-select svg {
    display: none;
  }

  .hi-select select {
    width: 100%;
    min-width: 0;
    height: 38px;
    padding: 0 30px 0 12px;
    font-size: 16px;
    text-overflow: ellipsis;
  }

  .hi-chaps {
    padding: 4px 4px 0;
  }

  .hi-chap {
    grid-template-columns: 32px minmax(0, 1fr) auto;
    grid-template-areas:
      'ico main pct'
      'prog prog prog';
    gap: 10px 12px;
    padding: 12px;
  }

  .hi-chap .es-theme-ico {
    grid-area: ico;
  }

  .hi-chap__main {
    grid-area: main;
  }

  .hi-chap__prog {
    grid-area: prog;
  }

  .hi-pct {
    grid-area: pct;
  }

  .hi-chap__chev {
    display: none;
  }

  .hi-chap__titre {
    font-size: 14.5px;
  }

  .hi-filtres,
  .hi-seg {
    width: 100%;
  }

  .hi-seg__btn {
    flex: 1;
    justify-content: center;
    padding: 0 6px;
  }

  .hi-select--chap,
  .hi-select--chap select {
    width: 100%;
    max-width: none;
  }

  .hi-jour {
    padding: 0 4px;
  }

  .hi-ex {
    grid-template-columns: 32px minmax(0, 1fr) auto;
    gap: 12px;
    padding: 10px 12px;
  }

  .hi-ex__pill {
    display: none;
  }

  .hi-ex__titre {
    white-space: normal;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }
}
</style>
