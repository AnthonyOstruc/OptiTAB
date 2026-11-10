<template>
  <div ref="rootRef" class="cx">
    <div v-if="loading" class="es-card cx-card">
      <div class="es-skeleton" style="height: 40px"></div>
      <div class="es-skeleton" style="height: 220px; margin-top: 16px"></div>
    </div>

    <p v-else-if="erreur" class="es-empty"><strong>Impossible de charger les exercices</strong>Vérifie ta connexion puis recharge la page.</p>

    <div v-else-if="!exercices.length" class="es-empty cx-empty">
      <strong>Les exercices de ce chapitre arrivent bientôt</strong>
      Tu peux déjà lire le cours et la fiche.
    </div>

    <template v-else>
      <!-- Filtres -->
      <div class="cx-tools">
        <div class="cx-seg" role="group" aria-label="Afficher">
          <button
            v-for="f in filtresStatut"
            :key="f.cle"
            type="button"
            :class="['cx-seg__btn', `cx-seg__btn--${f.cle}`, { 'is-active': filtreStatut === f.cle }]"
            :aria-pressed="filtreStatut === f.cle"
            @click="changerFiltre(f.cle)"
          >
            {{ f.label }}
            <span class="cx-seg__count">{{ f.count }}</span>
          </button>
        </div>
        <div class="cx-selects">
          <label v-if="types.length" class="cx-select">
            <span class="es-sr-only">Type d’exercice</span>
            <select v-model="filtreType">
              <option value="all">Tous les types</option>
              <option v-for="t in types" :key="t" :value="t">{{ t }}</option>
            </select>
            <ChevronDownIcon aria-hidden="true" />
          </label>
          <label class="cx-select">
            <span class="es-sr-only">Difficulté</span>
            <select v-model="filtreDifficulte">
              <option value="all">Toutes difficultés</option>
              <option v-for="d in difficultes" :key="d.cle" :value="d.cle">{{ d.label }}</option>
            </select>
            <ChevronDownIcon aria-hidden="true" />
          </label>
        </div>
      </div>

      <!-- Pastilles -->
      <nav v-if="liste.length" class="cx-dots" aria-label="Choisir un exercice">
        <button
          v-for="ex in liste"
          :key="ex.id"
          type="button"
          :class="['cx-dot', `cx-dot--${statut(ex.id) || 'todo'}`, { 'is-current': ex.id === courantId, 'is-locked': estVerrouille(ex.id) }]"
          :aria-label="`Exercice ${ex.numero} : ${titreCourt(ex)}${libelleStatut(ex.id)}`"
          :aria-current="ex.id === courantId ? 'true' : undefined"
          @click="choisir(ex.id)"
        >
          <LockClosedIcon v-if="estVerrouille(ex.id)" aria-hidden="true" />
          <template v-else>{{ ex.numero }}</template>
        </button>
      </nav>

      <p v-if="!liste.length" class="es-empty">
        <strong>{{ messageVide.titre }}</strong>
        {{ messageVide.texte }}
        <button v-if="filtreType !== 'all' || filtreDifficulte !== 'all'" type="button" class="es-btn es-btn--sm es-btn--ghost cx-reset" @click="reinitialiser">Tout afficher</button>
      </p>

      <!-- Exercice courant -->
      <section v-else-if="courant" :key="courant.id" class="es-card cx-card" aria-live="polite">
        <header class="cx-card__head">
          <span class="cx-card__pos">Exercice {{ courant.numero }} <span>sur {{ exercices.length }}</span></span>
          <span v-if="typeDe(courant)" class="cx-tag">{{ typeDe(courant) }}</span>
          <span class="cx-diff" :title="`Difficulté : ${difficulteDe(courant).label}`">
            <span v-for="n in 3" :key="n" :class="{ 'is-on': n <= difficulteDe(courant).niveau }"></span>
            <span class="es-sr-only">Difficulté : {{ difficulteDe(courant).label }}</span>
          </span>
          <span v-if="statut(courant.id)" :class="['es-pill', statut(courant.id) === 'acquired' ? 'es-pill--done' : 'es-pill--review', 'cx-card__status']">
            {{ statut(courant.id) === 'acquired' ? 'Acquis' : 'À revoir' }}
          </span>
        </header>

        <div v-if="estVerrouille(courant.id)" class="cx-locked">
          <LockClosedIcon aria-hidden="true" />
          <strong>{{ titreCourt(courant) }}</strong>
          <p>Cet exercice fait partie de l’abonnement. Abonne-toi pour débloquer tous les exercices corrigés de ta classe.</p>
          <router-link to="/billing#plans" class="es-btn es-btn--green">Voir les formules</router-link>
        </div>
        <div v-else class="cx-qcm">
          <ExerciceQCM
            :eid="courant.id"
            :titre="titreCourt(courant)"
            :instruction="courant.instruction || courant.contenu || courant.question || ''"
            :solution="courant.solution || courant.reponse_correcte || ''"
            :etapes="courant.etapes || ''"
            :preview-images="courant.images || []"
            :difficulty="courant.difficulty || courant.difficulte || 'medium'"
            :current="statut(courant.id)"
            @status-changed="enregistrerStatut"
          />
        </div>

        <p v-if="bravo" class="cx-bravo" role="status">
          <CheckCircleIcon aria-hidden="true" />
          Bien joué&nbsp;! {{ suivantId ? 'On passe au suivant ?' : 'Tu as fait le tour de cette sélection.' }}
        </p>
      </section>

      <!-- Navigation -->
      <div v-if="liste.length" class="cx-nav">
        <button type="button" class="es-btn es-btn--ghost" :disabled="!precedentId" @click="choisir(precedentId)">
          <ChevronLeftIcon aria-hidden="true" />
          <span class="cx-hide-sm">Précédent</span>
        </button>
        <span class="cx-nav__pos">{{ positionCourante }} / {{ liste.length }}</span>
        <button type="button" :class="['es-btn', { 'es-btn--green': bravo }]" :disabled="!suivantId" @click="choisir(suivantId)">
          Exercice suivant
          <ChevronRightIcon aria-hidden="true" />
        </button>
      </div>

      <div class="cx-help">
        <ChatBubbleLeftRightIcon aria-hidden="true" />
        <span>Bloqué&nbsp;? Envoie l’exercice à un prof, il te répond sur WhatsApp.</span>
        <a :href="lienAide" target="_blank" rel="noopener noreferrer" class="es-link" data-cta-name="help-whatsapp" data-cta-location="espace_exercice">
          Demander de l’aide
          <ChevronRightIcon aria-hidden="true" />
        </a>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  ChatBubbleLeftRightIcon,
  CheckCircleIcon,
  ChevronDownIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  LockClosedIcon
} from '@heroicons/vue/24/outline'
import ExerciceQCM from '@/components/UI/ExerciceQCM.vue'
import { createStatus, deleteStatus, updateStatus } from '@/api'
import { chargerExercices } from '@/utils/chapitreContenu'
import { tuneMathOverflow, typesetElements } from '@/utils/scientificRenderer'
import { useProgression } from '@/composables/useProgression'
import { useUserStore } from '@/stores/user'
import { useSubscriptionStore } from '@/stores/subscription'
import { vitrineContact } from '@/config/vitrineContent'

const props = defineProps({
  notionId: { type: [String, Number], required: true },
  exerciceInitial: { type: [String, Number], default: null },
  // Onglet affiché (sinon gardé dans la page, masqué).
  actif: { type: Boolean, default: true }
})
const emit = defineEmits(['progress'])

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const subscriptionStore = useSubscriptionStore()
const { invalider } = useProgression()

const rootRef = ref(null)
const loading = ref(true)
const erreur = ref(false)
const exercices = ref([])
// exerciceId -> { status: 'acquired' | 'not_acquired', id }
const statusMap = ref({})
const filtreStatut = ref('tous')
const filtreType = ref('all')
const filtreDifficulte = ref('all')
const courantId = ref(null)
const bravo = ref(false)

// ---------- Libellés ----------
const PREFIXE = /^(Découverte|Entraînement|Problème|Approfondissement|Synthèse|Bilan|Type concours|Type brevet|Type bac|Type examen|DS)\s*[-–]\s*/i
const titreCourt = (ex) => String(ex?.titre || ex?.nom || 'Exercice').replace(PREFIXE, '')
const DIFFICULTES = {
  easy: { niveau: 1, label: 'facile' },
  medium: { niveau: 2, label: 'moyen' },
  hard: { niveau: 3, label: 'difficile' }
}
const difficulteDe = (ex) => DIFFICULTES[String(ex?.difficulty || ex?.difficulte || 'medium').toLowerCase()] || DIFFICULTES.medium

// Types configurés pour la classe (ex. Découverte, Entraînement, Problème).
const types = computed(() => {
  const options = userStore.niveau_pays?.exercice_filter_options
  const liste = Array.isArray(options) ? options.map((o) => String(o).trim()).filter(Boolean) : []
  return [...new Set(liste)].filter((t) => exercices.value.some((ex) => correspondType(ex, t)))
})
const normaliser = (s) => String(s || '').toLowerCase().trim()
const correspondType = (ex, t) => [ex.exercice_type, ex.type, ex.titre, ex.nom].map(normaliser).some((f) => f.includes(normaliser(t)))
const typeDe = (ex) => types.value.find((t) => correspondType(ex, t)) || (String(ex?.titre || '').match(PREFIXE)?.[1] ?? '')

const difficultes = computed(() => Object.entries(DIFFICULTES)
  .filter(([cle]) => exercices.value.some((ex) => normaliser(ex.difficulty || ex.difficulte) === cle))
  .map(([cle, d]) => ({ cle, label: `${'★'.repeat(d.niveau)} ${d.label.charAt(0).toUpperCase()}${d.label.slice(1)}` })))

// ---------- Statuts ----------
const statut = (id) => statusMap.value[id]?.status || null
const libelleStatut = (id) => (statut(id) === 'acquired' ? ' (acquis)' : statut(id) === 'not_acquired' ? ' (à revoir)' : '')

const compteurs = computed(() => {
  const c = { acquis: 0, aRevoir: 0 }
  exercices.value.forEach((ex) => {
    if (statut(ex.id) === 'acquired') c.acquis += 1
    else if (statut(ex.id) === 'not_acquired') c.aRevoir += 1
  })
  return { ...c, total: exercices.value.length, aFaire: exercices.value.length - c.acquis - c.aRevoir }
})

watch(compteurs, (c) => emit('progress', c), { deep: true })

const FILTRES = [
  { cle: 'tous', label: 'Tous', test: () => true },
  { cle: 'afaire', label: 'À faire', test: (ex) => !statut(ex.id) },
  { cle: 'review', label: 'À revoir', test: (ex) => statut(ex.id) === 'not_acquired' },
  { cle: 'done', label: 'Acquis', test: (ex) => statut(ex.id) === 'acquired' }
]

const filtresStatut = computed(() => FILTRES.map((f) => ({ ...f, count: exercices.value.filter(f.test).length })))

const liste = computed(() => {
  const test = FILTRES.find((f) => f.cle === filtreStatut.value)?.test || (() => true)
  return exercices.value.filter((ex) =>
    test(ex) &&
    (filtreType.value === 'all' || correspondType(ex, filtreType.value)) &&
    (filtreDifficulte.value === 'all' || normaliser(ex.difficulty || ex.difficulte) === filtreDifficulte.value)
  )
})

const messageVide = computed(() => {
  if (filtreStatut.value === 'review') return { titre: 'Rien à revoir', texte: 'Aucun exercice de cette sélection n’est marqué « À revoir ».' }
  if (filtreStatut.value === 'done') return { titre: 'Pas encore d’exercice acquis', texte: 'Marque un exercice « J’ai compris » pour le retrouver ici.' }
  if (filtreStatut.value === 'afaire') return { titre: 'Tout est fait !', texte: 'Tu as traité tous les exercices de cette sélection.' }
  return { titre: 'Aucun exercice', texte: 'Aucun exercice ne correspond à ces filtres.' }
})

// ---------- Exercice courant ----------
const courant = computed(() => liste.value.find((ex) => ex.id === courantId.value) || null)
const positionListe = computed(() => liste.value.findIndex((ex) => ex.id === courantId.value))
const positionCourante = computed(() => Math.max(1, positionListe.value + 1))
const precedentId = computed(() => (positionListe.value > 0 ? liste.value[positionListe.value - 1].id : null))
const suivantId = computed(() => (positionListe.value >= 0 && positionListe.value < liste.value.length - 1 ? liste.value[positionListe.value + 1].id : null))

// Si l'exercice courant sort de la sélection (filtre), on prend le premier.
watch(liste, (l) => {
  if (l.length && !l.some((ex) => ex.id === courantId.value)) courantId.value = l[0].id
})

function choisir(id, { remonter = true } = {}) {
  if (!id) return
  bravo.value = false
  courantId.value = id
  if (String(route.query.ex || '') !== String(id)) {
    router.replace({ query: { ...route.query, ex: String(id) } }).catch(() => {})
  }
  if (remonter) {
    requestAnimationFrame(() => {
      const top = (rootRef.value?.getBoundingClientRect().top || 0) + window.scrollY - 140
      if (window.scrollY > top) window.scrollTo({ top, behavior: 'smooth' })
    })
  }
}

function changerFiltre(cle) {
  filtreStatut.value = cle
}

function reinitialiser() {
  filtreType.value = 'all'
  filtreDifficulte.value = 'all'
  filtreStatut.value = 'tous'
}

// ---------- Accès démo (même règle que l'ancienne page) ----------
const demoNotionId = computed(() => Number(userStore.niveau_pays?.demo_notion) || null)
const demoExerciceIds = computed(() => (Array.isArray(userStore.niveau_pays?.demo_exercices_ids) ? userStore.niveau_pays.demo_exercices_ids.map(Number) : []))
const modeDemo = computed(() => !userStore.isAdmin && !subscriptionStore.hasAccess && demoNotionId.value && Number(props.notionId) === demoNotionId.value)
const estVerrouille = (id) => Boolean(modeDemo.value) && !demoExerciceIds.value.includes(Number(id))

// ---------- Enregistrement « J'ai compris / À revoir » (logique inchangée) ----------
async function enregistrerStatut({ exerciceId, status }) {
  const existant = statusMap.value[exerciceId]
  try {
    if (status) {
      if (existant?.id) {
        await updateStatus(existant.id, { exercice: exerciceId, reponse_donnee: status, est_correct: status === 'acquired' })
        statusMap.value = { ...statusMap.value, [exerciceId]: { status, id: existant.id } }
      } else {
        const response = await createStatus({
          exercice: exerciceId,
          reponse_donnee: status,
          est_correct: status === 'acquired',
          points_obtenus: status === 'acquired' ? 1 : 0,
          temps_seconde: 0
        })
        statusMap.value = { ...statusMap.value, [exerciceId]: { status, id: response?.data?.id || response?.id } }
      }
    } else {
      if (existant?.id) await deleteStatus(existant.id)
      const copie = { ...statusMap.value }
      delete copie[exerciceId]
      statusMap.value = copie
    }
  } catch (e) {
    console.error('[Exercices] Statut non enregistré :', e)
    const copie = { ...statusMap.value }
    if (status) copie[exerciceId] = { status, id: existant?.id || null }
    else delete copie[exerciceId]
    statusMap.value = copie
  }
  bravo.value = status === 'acquired'
  invalider()
}

const lienAide = computed(() => {
  const titre = courant.value ? `« ${titreCourt(courant.value)} »` : 'un exercice'
  return `https://wa.me/${vitrineContact.whatsapp}?text=${encodeURIComponent(`Bonjour, je bloque sur l’exercice ${titre}. Pouvez-vous m’aider ?`)}`
})

// ---------- Chargement ----------
async function charger() {
  loading.value = true
  erreur.value = false
  try {
    const [data, statuts] = await chargerExercices(props.notionId)
    const brut = Array.isArray(data) ? data : []
    exercices.value = brut
      .slice()
      .sort((a, b) => (Number(a.id) || 0) - (Number(b.id) || 0))
      .map((ex, i) => ({ ...ex, numero: i + 1 }))
    const listeStatuts = Array.isArray(statuts?.data) ? statuts.data : (statuts?.data?.results || [])
    statusMap.value = Object.fromEntries(listeStatuts.map((s) => [s.exercice, { status: s.est_correct ? 'acquired' : 'not_acquired', id: s.id }]))
  } catch (e) {
    console.error('[Exercices] Chargement :', e)
    erreur.value = true
  } finally {
    loading.value = false
  }
  const demande = Number(props.exerciceInitial)
  const depart = exercices.value.find((ex) => ex.id === demande) ||
    exercices.value.find((ex) => !statut(ex.id) && !estVerrouille(ex.id)) ||
    exercices.value[0]
  if (depart) courantId.value = depart.id
  emit('progress', compteurs.value)
}

onMounted(charger)
watch(() => props.notionId, charger)

// Lien vers un exercice précis alors que l'onglet est déjà chargé (gardé en mémoire).
watch(() => props.exerciceInitial, (id) => {
  const ex = exercices.value.find((e) => e.id === Number(id))
  if (!ex || ex.id === courantId.value) return
  if (!liste.value.includes(ex)) reinitialiser()
  choisir(ex.id, { remonter: false })
})

// Onglet réaffiché : compteurs du bandeau à jour ; formules arrivées pendant
// qu'il était masqué mises en forme (le calcul de l'exercice ignore les
// onglets masqués) ; formules larges réajustées si la fenêtre a changé.
const LATEX_BRUT = /\\\(|\\\[|\$/
let largeurFenetre = window.innerWidth
watch(() => props.actif, (affiche) => {
  const root = rootRef.value
  if (!affiche || loading.value || !root) return
  emit('progress', compteurs.value)
  const largeurChangee = window.innerWidth !== largeurFenetre
  largeurFenetre = window.innerWidth
  if (LATEX_BRUT.test(root.textContent || '')) {
    typesetElements([root]).then(() => tuneMathOverflow(root)).catch(() => {})
  } else if (largeurChangee) {
    tuneMathOverflow(root)
  }
}, { flush: 'post' })
</script>

<style scoped>
/* ---------- Filtres ---------- */

.cx-tools {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.cx-seg {
  display: inline-flex;
  gap: 2px;
  padding: 4px;
  border-radius: 12px;
  background: #e9edf5;
}

.cx-seg__btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 36px;
  padding: 0 14px;
  border: 0;
  border-radius: 9px;
  background: transparent;
  font: 600 14px var(--es-font);
  color: var(--es-ink-soft);
  cursor: pointer;
  white-space: nowrap;
}

.cx-seg__btn.is-active {
  background: #fff;
  color: var(--es-ink);
  box-shadow: 0 1px 3px rgba(16, 24, 40, 0.12);
}

.cx-seg__count {
  min-width: 22px;
  padding: 1px 6px;
  border-radius: 999px;
  background: rgba(16, 24, 40, 0.06);
  font-size: 12px;
  text-align: center;
  color: var(--es-muted);
}

.cx-seg__btn--review .cx-seg__count {
  background: var(--es-orange-50);
  color: var(--es-orange-700);
}

.cx-seg__btn--done .cx-seg__count {
  background: var(--es-green-50);
  color: var(--es-green-700);
}

.cx-selects {
  display: flex;
  gap: 8px;
}

.cx-select {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.cx-select select {
  min-height: 40px;
  padding: 0 34px 0 12px;
  border: 1px solid var(--es-line-strong);
  border-radius: 10px;
  background: #fff;
  font: 600 14px var(--es-font) !important;
  color: var(--es-ink);
  appearance: none;
  cursor: pointer;
}

.cx-select svg {
  position: absolute;
  right: 10px;
  width: 16px;
  height: 16px;
  color: var(--es-muted);
  pointer-events: none;
}

/* ---------- Pastilles ---------- */

.cx-dots {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 16px;
}

.cx-dot {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border: 1px solid var(--es-line-strong);
  border-radius: 10px;
  background: #fff;
  font: 700 14px var(--es-font);
  color: var(--es-ink-soft);
  cursor: pointer;
  transition: transform 0.1s ease, box-shadow 0.15s ease;
}

.cx-dot svg {
  width: 15px;
  height: 15px;
}

.cx-dot:hover {
  border-color: var(--es-navy);
}

.cx-dot--acquired {
  border-color: var(--es-green);
  background: var(--es-green);
  color: #fff;
}

.cx-dot--not_acquired {
  border-color: var(--es-orange);
  background: var(--es-orange-50);
  color: var(--es-orange-700);
}

.cx-dot.is-locked {
  background: var(--es-bg);
  color: #98a2b3;
}

.cx-dot.is-current {
  box-shadow: 0 0 0 3px #fff, 0 0 0 5px var(--es-navy);
}

/* ---------- Carte ---------- */

.cx-card {
  padding: 20px 24px 24px;
}

.cx-card__head {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  margin-bottom: 4px;
}

.cx-card__pos {
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--es-navy);
}

.cx-card__pos span {
  color: var(--es-muted);
}

.cx-tag {
  padding: 3px 10px;
  border-radius: 999px;
  background: var(--es-navy-50);
  font-size: 12px;
  font-weight: 700;
  color: var(--es-navy);
}

.cx-diff {
  display: inline-flex;
  gap: 3px;
}

.cx-diff > span:not(.es-sr-only) {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--es-line-strong);
}

.cx-diff > span.is-on {
  background: var(--es-orange);
}

.cx-card__status {
  margin-left: auto;
}

/* Habillage du composant d'exercice existant, uniquement ici. */
.cx-qcm :deep(.exercice-card) {
  margin: 0;
  padding: 0;
  border: 0;
  border-radius: 0;
  background: transparent;
  box-shadow: none;
}

.cx-qcm :deep(.exercice-header) {
  padding: 0;
  border: 0;
  background: transparent;
}

.cx-qcm :deep(.header-top) {
  padding: 0;
}

.cx-qcm :deep(.header-first-row) {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 0;
}

.cx-qcm :deep(.exercice-title) {
  flex: 1;
  order: 0;
  margin: 6px 0 0;
  font-family: var(--es-font);
  font-size: 21px;
  font-weight: 700;
  line-height: 1.3;
  text-align: left;
  color: var(--es-ink);
}

.cx-qcm :deep(.header-slot--left) {
  order: 1;
}

.cx-qcm :deep(.header-slot--right) {
  order: 2;
}

.cx-qcm :deep(.difficulty-indicator) {
  display: none;
}

.cx-qcm :deep(.flag-btn),
.cx-qcm :deep(.reset-status-btn) {
  width: 36px;
  height: 36px;
  border: 1px solid var(--es-line);
  border-radius: 10px;
  background: #fff;
  color: var(--es-muted);
}

.cx-qcm :deep(.tabs-container) {
  display: flex;
  gap: 2px;
  margin: 16px 0 0;
  padding: 4px;
  border: 0;
  border-radius: 12px;
  background: #e9edf5;
}

.cx-qcm :deep(.tab-btn) {
  flex: 1;
  flex-direction: row;
  min-width: 0;
  min-height: 40px;
  margin: 0;
  padding: 0 8px;
  border: 0;
  border-radius: 9px;
  background: transparent;
  font: 600 15px var(--es-font);
  color: var(--es-ink-soft);
  box-shadow: none;
}

.cx-qcm :deep(.tab-btn::after),
.cx-qcm :deep(.tab-btn::before) {
  display: none;
}

.cx-qcm :deep(.tab-btn.active) {
  background: #fff;
  color: var(--es-navy);
  box-shadow: 0 1px 3px rgba(16, 24, 40, 0.12);
}

.cx-qcm :deep(.tab-icon) {
  display: none;
}

.cx-qcm :deep(.tab-content) {
  min-height: 0 !important;
  padding: 0;
  background: transparent;
}

.cx-qcm :deep(.content-wrapper) {
  padding: 20px 2px 4px;
}

.cx-qcm :deep(.assessment-section) {
  margin-top: 20px;
  padding: 18px 0 0;
  border-top: 1px solid var(--es-line);
  background: transparent;
}

.cx-qcm :deep(.assessment-header) {
  margin-bottom: 12px;
  text-align: left;
}

.cx-qcm :deep(.assessment-title) {
  margin: 0;
  font-family: var(--es-font);
  font-size: 15px;
  font-weight: 700;
  color: var(--es-ink);
}

.cx-qcm :deep(.assessment-description) {
  display: none;
}

.cx-qcm :deep(.assessment-buttons) {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.cx-qcm :deep(.assessment-btn) {
  min-height: 48px;
  border: 1.5px solid var(--es-line-strong);
  border-radius: 12px;
  background: #fff;
  font: 700 15px var(--es-font);
  color: var(--es-ink);
  box-shadow: none;
  transform: none;
}

.cx-qcm :deep(.assessment-btn .btn-icon) {
  display: none;
}

.cx-qcm :deep(.assessment-btn.acquired:hover),
.cx-qcm :deep(.assessment-btn.acquired.active) {
  border-color: var(--es-green);
  background: var(--es-green-50);
  color: var(--es-green-700);
}

.cx-qcm :deep(.assessment-btn.acquired.active) {
  background: var(--es-green);
  color: #fff;
}

.cx-qcm :deep(.assessment-btn.not-acquired:hover),
.cx-qcm :deep(.assessment-btn.not-acquired.active) {
  border-color: var(--es-orange);
  background: var(--es-orange-50);
  color: var(--es-orange-700);
}

.cx-qcm :deep(.assessment-btn.not-acquired.active) {
  background: var(--es-orange);
  color: #fff;
}

.cx-bravo {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 14px !important;
  padding: 10px 14px;
  border-radius: 12px;
  background: var(--es-green-50);
  font-size: 14px;
  font-weight: 600;
  color: var(--es-green-700);
}

.cx-bravo svg {
  width: 20px;
  height: 20px;
}

.cx-locked {
  padding: 32px 12px;
  text-align: center;
}

.cx-locked svg {
  width: 36px;
  height: 36px;
  color: var(--es-muted);
}

.cx-locked strong {
  display: block;
  margin-top: 10px;
  font-size: 18px;
}

.cx-locked p {
  max-width: 440px;
  margin: 8px auto 18px !important;
  font-size: 15px;
  color: var(--es-muted);
}

/* ---------- Navigation et aide ---------- */

.cx-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: 16px;
}

.cx-nav__pos {
  font-size: 14px;
  font-weight: 700;
  color: var(--es-muted);
  white-space: nowrap;
}

.cx-help {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 12px;
  margin-top: 24px;
  padding: 14px 16px;
  border: 1px solid var(--es-line);
  border-radius: 14px;
  background: #fff;
  font-size: 14px;
  color: var(--es-muted);
}

.cx-help > svg {
  width: 20px;
  height: 20px;
  color: var(--es-green-700);
}

.cx-help > span {
  flex: 1;
  min-width: 200px;
}

.cx-empty,
.cx-reset {
  margin-top: 12px;
}

@media (max-width: 760px) {
  .cx-tools {
    flex-direction: column;
    align-items: stretch;
  }

  .cx-seg {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }

  .cx-seg__btn {
    flex-direction: column;
    gap: 2px;
    min-height: 50px;
    padding: 4px 2px;
    font-size: 13px;
  }

  .cx-selects {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(0, 1fr));
  }

  .cx-select select {
    width: 100%;
  }

  .cx-dots {
    flex-wrap: nowrap;
    margin: 0 -16px 14px;
    padding: 6px 16px;
    overflow-x: auto;
    scrollbar-width: none;
  }

  .cx-dots::-webkit-scrollbar {
    display: none;
  }

  .cx-dot {
    flex-shrink: 0;
  }

  .cx-card {
    margin: 0 -16px;
    padding: 16px;
    border-right: 0;
    border-left: 0;
    border-radius: 0;
  }

  .cx-qcm :deep(.exercice-title) {
    font-size: 18px;
  }

  .cx-hide-sm {
    display: none;
  }
}

@media (max-width: 400px) {
  .cx-selects {
    grid-template-columns: minmax(0, 1fr);
  }
}
</style>
