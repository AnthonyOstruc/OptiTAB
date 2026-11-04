<template>
  <div class="cq">
    <div v-if="loading" class="es-card cq-card">
      <div class="es-skeleton" style="height: 24px; width: 50%"></div>
      <div v-for="n in 4" :key="n" class="es-skeleton" style="height: 16px; margin-top: 14px"></div>
    </div>

    <div v-else-if="!quiz" class="es-empty cq-empty">
      <strong>Le quiz de ce chapitre arrive bientôt</strong>
      Le cours, la fiche et les exercices sont déjà disponibles.
    </div>

    <!-- Accueil -->
    <section v-else-if="etat === 'accueil'" class="es-card cq-card cq-accueil">
      <span class="cq-accueil__ico"><BoltIcon aria-hidden="true" /></span>
      <p class="es-kicker">Quiz du chapitre</p>
      <h2 class="cq-accueil__titre">{{ quiz.titre }}</h2>
      <p class="cq-accueil__intro">{{ quiz.intro || 'Vérifie en quelques minutes que tu maîtrises le chapitre.' }}</p>
      <ul class="cq-faits">
        <li><QuestionMarkCircleIcon aria-hidden="true" />{{ questions.length }} questions</li>
        <li v-if="quiz.duree"><ClockIcon aria-hidden="true" />environ {{ quiz.duree }} min</li>
        <li><CheckBadgeIcon aria-hidden="true" />correction immédiate</li>
      </ul>
      <ul class="cq-types" aria-label="Types de questions">
        <li v-for="t in typesPresents" :key="t">{{ TYPES[t] }}</li>
      </ul>
      <p v-if="record" class="cq-record">
        <TrophyIcon aria-hidden="true" />
        Ta meilleure note : <strong>{{ virgule(record.note) }}/20</strong>
      </p>
      <button type="button" class="es-btn es-btn--green cq-go" @click="demarrer()">
        {{ record ? 'Refaire le quiz' : 'Commencer le quiz' }}
        <ArrowRightIcon aria-hidden="true" />
      </button>
    </section>

    <!-- Questions -->
    <section v-else-if="etat === 'jeu'" class="cq-jeu">
      <div class="cq-barre" :aria-label="`Question ${position + 1} sur ${serie.length}`">
        <span
          v-for="(idx, i) in serie"
          :key="idx"
          :class="['cq-barre__seg', {
            'is-ok': resultats[idx] === true,
            'is-ko': resultats[idx] === false,
            'is-now': i === position && resultats[idx] === undefined
          }]"
        ></span>
      </div>
      <div class="cq-statut">
        <span>{{ revision ? 'Je refais mes erreurs' : quiz.titre }}</span>
        <span class="cq-statut__score">
          <span v-if="serieBonnes >= 3" class="cq-flamme"><FireIcon aria-hidden="true" />{{ serieBonnes }} de suite</span>
          <span v-if="repondues">{{ bonnes }} juste{{ bonnes > 1 ? 's' : '' }} sur {{ repondues }}</span>
        </span>
      </div>
      <QuizQuestion
        :key="`${essai}-${serie[position]}`"
        :q="questions[serie[position]]"
        :numero="position + 1"
        :total="serie.length"
        :dernier="position === serie.length - 1"
        @reponse="noter"
        @suivant="suivant"
      />
      <button type="button" class="cq-quitter" @click="etat = 'accueil'">Quitter le quiz</button>
    </section>

    <!-- Résultat -->
    <section v-else ref="finRef" class="es-card cq-card cq-fin">
      <ProgressRing :value="bonnes" :max="serie.length" :size="136" :epaisseur="11" class="cq-ring">
        <span v-if="!revision" class="cq-note">
          <strong>{{ virgule(note) }}</strong>
          <small>/ 20</small>
        </span>
        <strong v-else>{{ bonnes }}<small>/{{ serie.length }}</small></strong>
      </ProgressRing>
      <p class="cq-fin__score">
        {{ bonnes }} bonne{{ bonnes > 1 ? 's' : '' }} réponse{{ bonnes > 1 ? 's' : '' }} sur {{ serie.length }}
      </p>
      <h2 class="cq-fin__titre">{{ message.titre }}</h2>
      <p class="cq-fin__texte">{{ message.texte }}</p>
      <p v-if="nouveauRecord" class="cq-record cq-record--new"><TrophyIcon aria-hidden="true" />Nouveau record !</p>

      <!-- Bilan par partie du cours -->
      <div v-if="!revision && bilanParties.length" class="cq-parties">
        <h3 class="cq-parties__titre">Bilan par partie du cours</h3>
        <ul>
          <li v-for="p in bilanParties" :key="p.nom" class="cq-partie">
            <span class="cq-partie__nom" v-html="inline(p.nom)"></span>
            <span class="cq-partie__jauge" aria-hidden="true">
              <span :style="{ width: `${(100 * p.bonnes) / p.total}%` }" :class="`is-${p.etat.cle}`"></span>
            </span>
            <span class="cq-partie__compte">{{ p.bonnes }}/{{ p.total }}</span>
            <span :class="['es-pill', p.etat.pill]">{{ p.etat.label }}</span>
          </li>
        </ul>
        <button v-if="bilanParties.some((p) => p.etat.cle !== 'acquis')" type="button" class="es-btn es-btn--ghost es-btn--sm cq-parties__cours" @click="$emit('go', 'cours')">
          <BookOpenIcon aria-hidden="true" />
          Relire ces parties dans le cours
        </button>
      </div>

      <details class="cq-detail" :open="revision">
        <summary>Détail des questions</summary>
        <ul class="cq-bilan">
          <li v-for="(idx, i) in serie" :key="idx" :class="resultats[idx] ? 'is-ok' : 'is-ko'">
            <CheckCircleIcon v-if="resultats[idx]" aria-hidden="true" />
            <QuestionMarkCircleIcon v-else-if="passees[idx]" aria-hidden="true" />
            <XCircleIcon v-else aria-hidden="true" />
            <span class="cq-bilan__num">{{ i + 1 }}</span>
            <span class="cq-bilan__theme">{{ questions[idx].theme || TYPES[questions[idx].type] }}</span>
            <span v-if="passees[idx]" class="cq-bilan__passee">passée</span>
          </li>
        </ul>
      </details>

      <div class="cq-fin__actions">
        <button v-if="erreurs.length" type="button" class="es-btn es-btn--green" @click="demarrer(erreurs)">
          <ArrowPathIcon aria-hidden="true" />
          Refaire mes {{ erreurs.length }} erreur{{ erreurs.length > 1 ? 's' : '' }}
        </button>
        <button type="button" class="es-btn es-btn--ghost" @click="demarrer()">Recommencer tout le quiz</button>
      </div>
      <div class="cq-fin__liens">
        <button type="button" class="es-link" @click="$emit('go', 'cours')">Revoir le cours</button>
        <button type="button" class="es-link" @click="$emit('go', 'fiche')">Relire la fiche</button>
        <button type="button" class="es-link" @click="$emit('go', 'exercices')">Faire les exercices</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, reactive, ref, watch } from 'vue'
import {
  ArrowPathIcon,
  ArrowRightIcon,
  BoltIcon,
  BookOpenIcon,
  CheckBadgeIcon,
  CheckCircleIcon,
  ClockIcon,
  FireIcon,
  QuestionMarkCircleIcon,
  TrophyIcon,
  XCircleIcon
} from '@heroicons/vue/24/outline'
import ProgressRing from './ProgressRing.vue'
import QuizQuestion from './QuizQuestion.vue'
import { chargerQuiz } from '@/data/quiz'
import { enregistrerNoteQuiz } from '@/api/progression'
import { useProgression } from '@/composables/useProgression'
import { useUserStore } from '@/stores/user'
import { renderInline } from '@/utils/optitabDoc'

const props = defineProps({
  notionId: { type: [String, Number], required: true }
})
defineEmits(['go'])

const TYPES = {
  qcm: 'QCM',
  multi: 'Plusieurs réponses',
  vf: 'Vrai ou faux',
  saisie: 'Réponse à écrire',
  associer: 'Associer',
  ordre: 'Remettre dans l’ordre'
}

const loading = ref(true)
const quiz = ref(null)
const etat = ref('accueil')
const serie = ref([])
const position = ref(0)
const resultats = reactive({})
const passees = reactive({})
const essai = ref(0)
const revision = ref(false)
const serieBonnes = ref(0)
const record = ref(null)
const nouveauRecord = ref(false)

const questions = computed(() => quiz.value?.questions || [])
const typesPresents = computed(() => Object.keys(TYPES).filter((t) => questions.value.some((q) => q.type === t)))
const repondues = computed(() => serie.value.filter((i) => resultats[i] !== undefined).length)
const bonnes = computed(() => serie.value.filter((i) => resultats[i] === true).length)
const erreurs = computed(() => serie.value.filter((i) => resultats[i] === false))

// Note sur 20 (au dixième) et bilan par partie du cours
const note = computed(() => (serie.value.length ? (20 * bonnes.value) / serie.value.length : 0))
const virgule = (n) => (Math.round(n * 10) / 10).toLocaleString('fr-FR', { maximumFractionDigits: 1 })
const inline = (texte) => renderInline(texte || '')
const ETATS = {
  acquis: { cle: 'acquis', label: 'Acquis', pill: 'es-pill--done' },
  encours: { cle: 'encours', label: 'En cours', pill: 'es-pill--progress' },
  revoir: { cle: 'revoir', label: 'À revoir', pill: 'es-pill--review' }
}
const bilanParties = computed(() => {
  const noms = quiz.value?.parties || []
  return noms
    .map((nom) => {
      const ids = serie.value.filter((i) => questions.value[i].partie === nom)
      const ok = ids.filter((i) => resultats[i] === true).length
      const etat = ok === ids.length ? ETATS.acquis : ok * 2 >= ids.length ? ETATS.encours : ETATS.revoir
      return { nom, total: ids.length, bonnes: ok, etat }
    })
    .filter((p) => p.total > 0)
})

const message = computed(() => {
  const r = serie.value.length ? bonnes.value / serie.value.length : 0
  if (revision.value && r === 1) return { titre: 'Toutes tes erreurs sont corrigées !', texte: 'Bravo, tu as retenu la leçon. Refais le quiz complet dans quelques jours pour bien ancrer.' }
  if (r === 1) return { titre: 'Parfait !', texte: 'Tu maîtrises ce chapitre. Passe aux exercices de type examen pour aller plus loin.' }
  if (r >= 0.75) return { titre: 'Très bien !', texte: 'Presque tout est acquis. Refais tes erreurs pour viser le sans-faute.' }
  if (r >= 0.5) return { titre: 'C’est un bon début', texte: 'Relis la fiche, puis refais tes erreurs : chaque correction t’explique la méthode.' }
  return { titre: 'Continue, tu progresses', texte: 'Reprends le cours sur les points manqués, puis retente le quiz : tu verras la différence.' }
})

/* ---------- Note enregistrée et meilleure note ---------- */
// Élève connecté : la note de chaque quiz complet est enregistrée sur son compte
// (tableau de bord, suivi parent). La meilleure note vient du serveur ; une copie
// locale sert seulement quand le serveur n'est pas joignable (ou dans l'aperçu).
const userStore = useUserStore()
const { progression, charger: chargerProgression, invalider } = useProgression()
const cle = () => `optitab.quiz.${props.notionId}`

async function lireRecord() {
  let locale = null
  try {
    const r = JSON.parse(localStorage.getItem(cle()) || 'null')
    if (r && typeof r.note === 'number') locale = r.note
    else if (r && typeof r.best === 'number' && r.total) locale = (20 * r.best) / r.total
  } catch {
    /* pas de copie locale */
  }
  let serveur = null
  if (userStore.isAuthenticated) {
    await chargerProgression().catch(() => null)
    const c = (progression.value?.chapitres || []).find((x) => String(x.id) === String(props.notionId))
    if (c?.quiz) serveur = c.quiz.meilleure
  }
  const meilleure = Math.max(serveur ?? -1, locale ?? -1)
  record.value = meilleure >= 0 ? { note: meilleure } : null
}

function enregistrer() {
  const n = note.value
  nouveauRecord.value = !record.value || n > record.value.note
  if (nouveauRecord.value) {
    record.value = { note: n }
    try {
      localStorage.setItem(cle(), JSON.stringify({ note: n, date: new Date().toISOString() }))
    } catch {
      /* stockage indisponible : le record reste pour cette visite */
    }
  }
  if (!userStore.isAuthenticated) return
  enregistrerNoteQuiz({
    notion: Number(props.notionId),
    bonnes: bonnes.value,
    total: serie.value.length,
    parties: bilanParties.value.map((p) => ({ nom: p.nom, bonnes: p.bonnes, total: p.total, etat: p.etat.cle }))
  })
    .then(() => invalider())
    .catch(() => {
      /* note gardée sur l'appareil ; le prochain quiz complet sera enregistré */
    })
}

/* ---------- Déroulé ---------- */
function demarrer(liste = null) {
  revision.value = Array.isArray(liste)
  serie.value = revision.value ? [...liste] : questions.value.map((_, i) => i)
  serie.value.forEach((i) => delete resultats[i])
  position.value = 0
  serieBonnes.value = 0
  nouveauRecord.value = false
  essai.value += 1
  etat.value = 'jeu'
  window.scrollTo({ top: 0, behavior: 'auto' })
}

function noter(ok, passee = false) {
  const idx = serie.value[position.value]
  resultats[idx] = ok
  if (passee) passees[idx] = true
  else delete passees[idx]
  serieBonnes.value = ok ? serieBonnes.value + 1 : 0
}

function suivant() {
  if (position.value < serie.value.length - 1) {
    position.value += 1
  } else {
    if (!revision.value) enregistrer()
    etat.value = 'fin'
  }
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function charger() {
  loading.value = true
  etat.value = 'accueil'
  try {
    quiz.value = await chargerQuiz(props.notionId)
  } catch {
    quiz.value = null
  } finally {
    loading.value = false
  }
  lireRecord()
}

// Les noms de parties peuvent contenir des formules ($e^{u}$)
const finRef = ref(null)
watch(etat, async (e) => {
  if (e !== 'fin') return
  await nextTick()
  const mj = window.MathJax
  try {
    if (mj?.startup?.promise) await mj.startup.promise
    if (finRef.value && mj?.typesetPromise) await mj.typesetPromise([finRef.value])
  } catch {
    /* formules laissées en texte */
  }
})

onMounted(charger)
watch(() => props.notionId, charger)
</script>

<style scoped>
.cq {
  max-width: 820px;
  margin: 0 auto;
}

.cq-card {
  padding: 28px 32px;
}

.cq-empty {
  padding: 40px 20px;
}

/* ---------- Accueil ---------- */
.cq-accueil {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  background:
    radial-gradient(420px 180px at 50% 0%, var(--es-green-50), transparent 75%),
    #fff;
}

.cq-accueil__ico {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  margin-bottom: 14px;
  border-radius: 18px;
  background: var(--es-green-700);
  color: #fff;
  box-shadow: 0 10px 22px rgba(59, 133, 68, 0.25);
}

.cq-accueil__ico svg {
  width: 30px;
  height: 30px;
}

.cq-accueil__titre {
  margin-top: 6px !important;
  font-size: clamp(22px, 2.4vw, 28px);
  font-weight: 700;
}

.cq-accueil__intro {
  max-width: 520px;
  margin-top: 8px !important;
  font-size: 16px;
  color: var(--es-ink-soft);
}

.cq-faits {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px 20px;
  margin: 18px 0 0;
  padding: 0;
  font-size: 14px;
  font-weight: 600;
  color: var(--es-ink-soft);
  list-style: none;
}

.cq-faits li {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.cq-faits svg {
  width: 18px;
  height: 18px;
  color: var(--es-green-700);
}

.cq-types {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 6px;
  margin: 16px 0 0;
  padding: 0;
  list-style: none;
}

.cq-types li {
  padding: 4px 10px;
  border-radius: 999px;
  background: var(--es-navy-50);
  font-size: 12px;
  font-weight: 600;
  color: var(--es-navy);
}

.cq-record {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 18px !important;
  font-size: 14px;
  color: var(--es-ink-soft);
}

.cq-record svg {
  width: 18px;
  height: 18px;
  color: var(--es-orange);
}

.cq-record--new {
  margin-top: 8px !important;
  font-weight: 700;
  color: var(--es-orange-700);
}

.cq-go {
  min-width: 240px;
  margin-top: 22px;
}

/* ---------- En jeu ---------- */
.cq-barre {
  display: flex;
  gap: 4px;
  margin-bottom: 10px;
}

.cq-barre__seg {
  flex: 1;
  height: 8px;
  border-radius: 4px;
  background: var(--es-line);
  transition: background-color 0.25s ease;
}

.cq-barre__seg.is-now {
  background: var(--es-navy);
}

.cq-barre__seg.is-ok {
  background: var(--es-green);
}

.cq-barre__seg.is-ko {
  background: var(--es-orange);
}

.cq-statut {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
  font-size: 13px;
  font-weight: 600;
  color: var(--es-muted);
}

.cq-statut__score {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: var(--es-ink-soft);
}

.cq-flamme {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  border-radius: 999px;
  background: var(--es-orange-50);
  color: var(--es-orange-700);
}

.cq-flamme svg {
  width: 15px;
  height: 15px;
}

.cq-quitter {
  display: block;
  margin: 16px auto 0;
  border: 0;
  background: none;
  font: 600 13px var(--es-font);
  color: var(--es-muted);
  cursor: pointer;
}

.cq-quitter:hover {
  color: var(--es-ink);
  text-decoration: underline;
}

/* ---------- Résultat ---------- */
.cq-fin {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.cq-ring strong {
  font-size: 30px;
  font-weight: 700;
  line-height: 1;
}

.cq-ring small {
  font-size: 16px;
  color: var(--es-muted);
}

.cq-ring :deep(.ring__fill) {
  stroke: var(--es-green);
}

.cq-note {
  display: flex;
  flex-direction: column;
  align-items: center;
  line-height: 1;
}

.cq-note strong {
  font-size: 34px;
}

.cq-note small {
  margin-top: 4px;
  font-size: 14px;
  font-weight: 600;
}

.cq-fin__score {
  margin-top: 10px !important;
  font-size: 14px;
  font-weight: 600;
  color: var(--es-muted);
}

/* ---------- Bilan par partie ---------- */
.cq-parties {
  width: 100%;
  margin-top: 24px;
  padding: 18px 18px 16px;
  border: 1px solid var(--es-line);
  border-radius: 14px;
  background: var(--es-bg);
  text-align: left;
}

.cq-parties__titre {
  margin-bottom: 12px !important;
  font-size: 15px;
  font-weight: 700;
}

.cq-parties ul {
  display: grid;
  gap: 10px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.cq-partie {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 90px auto auto;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 10px;
  background: #fff;
}

.cq-partie__nom {
  font-size: 14px;
  font-weight: 600;
  color: var(--es-ink);
}

.cq-partie__jauge {
  height: 8px;
  overflow: hidden;
  border-radius: 4px;
  background: var(--es-line);
}

.cq-partie__jauge span {
  display: block;
  height: 100%;
  border-radius: 4px;
}

.cq-partie__jauge .is-acquis {
  background: var(--es-green);
}

.cq-partie__jauge .is-encours {
  background: var(--es-navy);
}

.cq-partie__jauge .is-revoir {
  background: var(--es-orange);
}

.cq-partie__compte {
  font-size: 13px;
  font-weight: 700;
  color: var(--es-ink-soft);
}

.cq-parties__cours {
  max-width: 100%;
  margin-top: 14px;
  white-space: normal;
}

.cq-detail {
  width: 100%;
  margin-top: 16px;
  text-align: left;
}

.cq-detail summary {
  font-size: 14px;
  font-weight: 600;
  color: var(--es-navy);
  cursor: pointer;
}

.cq-detail .cq-bilan {
  margin-top: 12px;
}

@media (max-width: 560px) {
  .cq-partie {
    grid-template-columns: minmax(0, 1fr) auto;
    gap: 8px 10px;
  }

  .cq-partie__nom {
    grid-column: 1 / -1;
  }

  .cq-partie__jauge {
    display: none;
  }
}

.cq-fin__titre {
  margin-top: 16px !important;
  font-size: 24px;
  font-weight: 700;
}

.cq-fin__texte {
  max-width: 520px;
  margin-top: 6px !important;
  font-size: 15px;
  color: var(--es-ink-soft);
}

.cq-bilan {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 8px;
  width: 100%;
  margin: 0;
  padding: 0;
  list-style: none;
  text-align: left;
}

.cq-bilan li {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
}

.cq-bilan li.is-ok {
  background: var(--es-green-50);
  color: var(--es-green-700);
}

.cq-bilan li.is-ko {
  background: var(--es-orange-50);
  color: var(--es-orange-700);
}

.cq-bilan svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.cq-bilan__num {
  font-weight: 700;
}

.cq-bilan__passee {
  margin-left: auto;
  flex-shrink: 0;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.cq-bilan__theme {
  min-width: 0;
  overflow: hidden;
  color: var(--es-ink-soft);
  white-space: nowrap;
  text-overflow: ellipsis;
}

.cq-fin__actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin-top: 24px;
}

.cq-fin__liens {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px 20px;
  margin-top: 18px;
}

.cq-fin__liens .es-link {
  border: 0;
  background: none;
  font-family: var(--es-font);
  cursor: pointer;
}

@media (max-width: 640px) {
  .cq-card {
    padding: 22px 16px;
  }

  .cq-go,
  .cq-fin__actions .es-btn {
    width: 100%;
  }
}
</style>
