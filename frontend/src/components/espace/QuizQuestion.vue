<template>
  <article ref="racine" class="qq es-card" :class="{ 'is-ok': valide && juste, 'is-ko': valide && !juste }">
    <header class="qq-head">
      <span class="qq-num">Question {{ numero }}<small> / {{ total }}</small></span>
      <span class="qq-tags">
        <span v-if="q.theme" class="qq-theme">{{ q.theme }}</span>
        <span :class="['es-pill', niveauClasse]">{{ q.niveau }}</span>
      </span>
    </header>

    <div class="qq-enonce" v-html="doc(q.enonce, 'statement')"></div>
    <QuizFigure v-if="q.figure" :f="q.figure" class="qq-fig" />

    <p class="qq-consigne">{{ consigne }}</p>

    <!-- QCM (une réponse) et choix multiples -->
    <div v-if="q.type === 'qcm' || q.type === 'multi'" :class="['qq-choix', { 'qq-choix--figures': aFigures }]">
      <button
        v-for="(k, pos) in ordreChoix"
        :key="k"
        type="button"
        :class="['qq-option', etatOption(k)]"
        :aria-pressed="estChoisi(k)"
        :disabled="valide"
        @click="choisir(k)"
      >
        <span class="qq-option__mark" aria-hidden="true">
          <template v-if="q.type === 'multi'">
            <XMarkIcon v-if="valide && estChoisi(k) && !estBonne(k)" />
            <CheckIcon v-else-if="estChoisi(k) || (valide && estBonne(k))" />
          </template>
          <template v-else>{{ LETTRES[pos] }}</template>
        </span>
        <QuizFigure v-if="aFigures" :f="q.choix_figures[k]" class="qq-option__fig" />
        <span v-else class="qq-option__txt" v-html="inline(q.choix[k])"></span>
        <span v-if="valide && q.type === 'multi' && (estChoisi(k) || estBonne(k))" class="qq-option__note">
          {{ !estBonne(k) ? 'fausse' : estChoisi(k) ? 'juste' : passee ? 'vraie' : 'oubliée' }}
        </span>
      </button>
    </div>

    <!-- Vrai / faux -->
    <div v-else-if="q.type === 'vf'" class="qq-vf">
      <button
        v-for="v in [true, false]"
        :key="String(v)"
        type="button"
        :class="['qq-option', 'qq-option--vf', etatVF(v)]"
        :aria-pressed="reponseVF === v"
        :disabled="valide"
        @click="reponseVF = v"
      >
        <CheckIcon v-if="v" aria-hidden="true" /><XMarkIcon v-else aria-hidden="true" />
        {{ v ? 'Vrai' : 'Faux' }}
      </button>
    </div>

    <!-- Réponse écrite -->
    <div v-else-if="q.type === 'saisie'" class="qq-saisie">
      <div :class="['qq-champ', { 'is-ok': valide && juste, 'is-ko': valide && !juste }]">
        <input
          ref="champ"
          v-model="saisie"
          type="text"
          inputmode="text"
          autocomplete="off"
          autocapitalize="off"
          spellcheck="false"
          :placeholder="q.placeholder || 'Ta réponse'"
          :disabled="valide"
          aria-label="Ta réponse"
          @keydown.enter.prevent="valider"
        />
        <span v-if="q.unite" class="qq-unite">{{ q.unite }}</span>
      </div>
      <div v-if="!valide" class="qq-touches" aria-label="Symboles">
        <button v-for="t in TOUCHES" :key="t.l" type="button" class="qq-touche" @mousedown.prevent @click="inserer(t.v)" v-html="t.l"></button>
      </div>
      <p v-if="saisie.trim() && lecture.erreur" class="qq-apercu qq-apercu--erreur">{{ lecture.erreur }}</p>
      <p v-else-if="saisie.trim()" class="qq-apercu">
        <span>Tu as écrit</span>
        <span ref="apercu" class="qq-apercu__math" v-html="apercuHtml"></span>
      </p>
    </div>

    <!-- Associer -->
    <div v-else-if="q.type === 'associer'" class="qq-assoc">
      <ul :class="['qq-assoc__cibles', { 'qq-assoc__cibles--figures': q.droite_figures }]">
        <li v-for="(k, pos) in ordreDroite" :key="k" class="qq-cible">
          <span class="qq-lettre">{{ LETTRES[pos] }}</span>
          <QuizFigure v-if="q.droite_figures" :f="q.droite_figures[k]" />
          <span v-else v-html="inline(q.droite[k])"></span>
        </li>
      </ul>
      <ul class="qq-assoc__lignes">
        <li v-for="(g, i) in q.gauche" :key="i" :class="['qq-ligne', etatLigne(i)]">
          <span class="qq-ligne__txt" v-html="inline(g)"></span>
          <span class="qq-ligne__choix" role="group" :aria-label="`Associer à`">
            <button
              v-for="(k, pos) in ordreDroite"
              :key="k"
              type="button"
              :class="['qq-lettre-btn', { 'is-on': associations[i] === k, 'is-bonne': valide && k === i && associations[i] !== i }]"
              :disabled="valide"
              @click="associations[i] = k"
            >{{ LETTRES[pos] }}</button>
          </span>
        </li>
      </ul>
    </div>

    <!-- Remettre dans l'ordre -->
    <ol v-else-if="q.type === 'ordre'" class="qq-ordre">
      <li v-for="(k, pos) in ordreEtapes" :key="k" :class="['qq-etape', etatEtape(k, pos)]">
        <span class="qq-etape__num">{{ pos + 1 }}</span>
        <span class="qq-etape__txt" v-html="inline(q.etapes[k])"></span>
        <span v-if="!valide" class="qq-etape__btns">
          <button type="button" :disabled="pos === 0" aria-label="Monter" @click="deplacer(pos, -1)"><ChevronUpIcon /></button>
          <button type="button" :disabled="pos === ordreEtapes.length - 1" aria-label="Descendre" @click="deplacer(pos, 1)"><ChevronDownIcon /></button>
        </span>
      </li>
    </ol>

    <!-- Correction -->
    <section v-if="valide" class="qq-correction" aria-live="polite">
      <p :class="['qq-verdict', passee ? 'is-passee' : juste ? 'is-ok' : 'is-ko']">
        <LightBulbIcon v-if="passee" aria-hidden="true" />
        <CheckCircleIcon v-else-if="juste" aria-hidden="true" />
        <XCircleIcon v-else aria-hidden="true" />
        {{ passee ? 'Pas de souci, voici la correction.' : juste ? bravo : 'Pas tout à fait.' }}
      </p>
      <p v-if="!juste && bonneReponseHtml" class="qq-attendu">
        <span>Réponse attendue :</span> <span v-html="bonneReponseHtml"></span>
      </p>
      <ol v-if="!juste && q.type === 'ordre'" class="qq-ordre qq-ordre--corrige">
        <li v-for="(e, i) in q.etapes" :key="i" class="qq-etape is-bonne">
          <span class="qq-etape__num">{{ i + 1 }}</span>
          <span class="qq-etape__txt" v-html="inline(e)"></span>
        </li>
      </ol>
      <div class="qq-explication" v-html="doc(q.explication, 'solution')"></div>
      <QuizFigure v-if="q.figure_corrige" :f="q.figure_corrige" class="qq-fig" />
    </section>

    <footer class="qq-actions">
      <template v-if="!valide">
        <button type="button" class="es-btn es-btn--ghost" @click="passer">Je ne sais pas</button>
        <button type="button" class="es-btn" :disabled="!pret" @click="valider">Valider</button>
      </template>
      <button v-else type="button" class="es-btn" @click="$emit('suivant')">
        {{ dernier ? 'Voir mon résultat' : 'Question suivante' }}
        <ArrowRightIcon aria-hidden="true" />
      </button>
    </footer>
  </article>
</template>

<script setup>
import { computed, nextTick, onMounted, reactive, ref, watch } from 'vue'
import {
  ArrowRightIcon,
  CheckCircleIcon,
  CheckIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  LightBulbIcon,
  XCircleIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'
import QuizFigure from './QuizFigure.vue'
import { OPTITAB_MARKER, isOptitabDoc, renderInline, renderOptitabDoc } from '@/utils/optitabDoc'
import { comparer, lire, nettoyerSaisie, versTex } from '@/utils/quizMath'
import { tuneMathOverflow } from '@/utils/scientificRenderer'

const props = defineProps({
  q: { type: Object, required: true },
  numero: { type: Number, required: true },
  total: { type: Number, required: true },
  dernier: { type: Boolean, default: false }
})
const emit = defineEmits(['reponse', 'suivant'])

const LETTRES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
const TOUCHES = [
  { l: 'x', v: 'x' },
  { l: 'e<sup>□</sup>', v: 'e^(' },
  { l: 'ln', v: 'ln(' },
  { l: '√', v: '√(' },
  { l: '(', v: '(' },
  { l: ')', v: ')' },
  { l: 'x<sup>n</sup>', v: '^' },
  { l: '/', v: '/' }
]
const BRAVOS = ['Bonne réponse !', 'Exact !', 'Bravo !', 'Parfait !', 'Bien vu !']

const racine = ref(null)
const champ = ref(null)
const apercu = ref(null)
const valide = ref(false)
const juste = ref(false)
const bravo = BRAVOS[Math.floor(Math.random() * BRAVOS.length)]

// Ordres mélangés une fois pour toutes à l'affichage de la question
function melange(n) {
  const t = Array.from({ length: n }, (_, i) => i)
  for (let i = n - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[t[i], t[j]] = [t[j], t[i]]
  }
  return t
}
function melangeDifferent(n) {
  // jamais déjà dans le bon ordre
  let t = melange(n)
  for (let k = 0; k < 10 && t.every((v, i) => v === i); k += 1) t = melange(n)
  return t
}

const aFigures = computed(() => Array.isArray(props.q.choix_figures) && props.q.choix_figures.length > 0)
const nbChoix = (props.q.choix_figures || props.q.choix || []).length
const ordreChoix = melange(nbChoix)
const ordreDroite = melange((props.q.droite_figures || props.q.droite || []).length)
const ordreEtapes = ref(props.q.type === 'ordre' ? melangeDifferent(props.q.etapes.length) : [])

const choisis = ref([])
const reponseVF = ref(null)
const saisie = ref('')
const associations = reactive({})

const niveauClasse = computed(() => ({
  Découverte: 'es-pill--done',
  Entraînement: 'es-pill--progress',
  Approfondissement: 'es-pill--review'
}[props.q.niveau] || ''))

const consigne = computed(() => ({
  qcm: 'Choisis la bonne réponse.',
  multi: 'Coche toutes les bonnes réponses (il peut y en avoir plusieurs).',
  vf: 'Vrai ou faux ?',
  saisie: props.q.nature === 'expression' ? 'Écris ta réponse comme sur une calculatrice.' : 'Écris ta réponse.',
  associer: 'Associe chaque ligne à la bonne lettre.',
  ordre: 'Remets les étapes dans le bon ordre avec les flèches.'
}[props.q.type]))

const doc = (texte, context) => renderOptitabDoc(isOptitabDoc(texte) ? texte : `${OPTITAB_MARKER}\n${texte || ''}`, { context })
const inline = (texte) => renderInline(texte || '')

/* ---------- Saisie ---------- */
const lecture = computed(() => lire(nettoyerSaisie(saisie.value, props.q), props.q.nature === 'expression' ? props.q.variable || 'x' : null))
const apercuHtml = computed(() => (lecture.value.arbre ? `$${versTex(lecture.value.arbre)}$` : ''))

function inserer(v) {
  const el = champ.value
  if (!el) return
  const debut = el.selectionStart ?? saisie.value.length
  const fin = el.selectionEnd ?? debut
  saisie.value = saisie.value.slice(0, debut) + v + saisie.value.slice(fin)
  nextTick(() => {
    el.focus()
    el.setSelectionRange(debut + v.length, debut + v.length)
  })
}

/* ---------- Choix ---------- */
const estChoisi = (k) => choisis.value.includes(k)
function choisir(k) {
  if (props.q.type === 'qcm') choisis.value = [k]
  else choisis.value = estChoisi(k) ? choisis.value.filter((x) => x !== k) : [...choisis.value, k]
}
function deplacer(pos, d) {
  const t = [...ordreEtapes.value]
  ;[t[pos], t[pos + d]] = [t[pos + d], t[pos]]
  ordreEtapes.value = t
}

const pret = computed(() => {
  switch (props.q.type) {
    case 'qcm':
    case 'multi':
      return choisis.value.length > 0
    case 'vf':
      return reponseVF.value !== null
    case 'saisie':
      return !!saisie.value.trim() && !lecture.value.erreur
    case 'associer':
      return props.q.gauche.every((_, i) => associations[i] !== undefined)
    case 'ordre':
      return true
    default:
      return false
  }
})

function corriger() {
  const q = props.q
  switch (q.type) {
    case 'qcm':
      return choisis.value[0] === q.bonne
    case 'multi': {
      const b = [...q.bonnes].sort().join()
      return [...choisis.value].sort().join() === b
    }
    case 'vf':
      return reponseVF.value === q.reponse
    case 'saisie':
      return comparer(saisie.value, q).ok
    case 'associer':
      return q.gauche.every((_, i) => associations[i] === i)
    case 'ordre':
      return ordreEtapes.value.every((k, i) => k === i)
    default:
      return false
  }
}

function valider() {
  if (!pret.value || valide.value) return
  juste.value = corriger()
  valide.value = true
  emit('reponse', juste.value, false)
}

// « Je ne sais pas » : la correction s'affiche, la question compte comme à revoir
const passee = ref(false)
function passer() {
  if (valide.value) return
  passee.value = true
  juste.value = false
  valide.value = true
  emit('reponse', false, true)
}

/* ---------- États visuels après correction ---------- */
const estBonne = (k) => (props.q.type === 'qcm' ? k === props.q.bonne : props.q.bonnes.includes(k))
function etatOption(k) {
  const choisi = estChoisi(k)
  if (!valide.value) return { 'is-on': choisi }
  const bon = estBonne(k)
  // une bonne réponse que l'élève n'a pas choisie : en vert pointillé (« oubliée »)
  return { 'is-bonne': bon && choisi, 'is-oubliee': bon && !choisi, 'is-fausse': choisi && !bon, 'is-terne': !bon && !choisi }
}
function etatVF(v) {
  if (!valide.value) return { 'is-on': reponseVF.value === v }
  return { 'is-bonne': v === props.q.reponse, 'is-fausse': reponseVF.value === v && v !== props.q.reponse, 'is-terne': v !== props.q.reponse && reponseVF.value !== v }
}
function etatLigne(i) {
  if (!valide.value) return {}
  return associations[i] === i ? 'is-bonne' : 'is-fausse'
}
function etatEtape(k, pos) {
  if (!valide.value) return {}
  return k === pos ? 'is-bonne' : 'is-fausse'
}

const bonneReponseHtml = computed(() => {
  const q = props.q
  if (q.type === 'saisie') {
    const l = lire(q.reponses[0], q.nature === 'expression' ? q.variable || 'x' : null)
    return l.arbre ? `$${versTex(l.arbre)}$${q.unite ? ` ${q.unite}` : ''}` : ''
  }
  if (q.type === 'associer') {
    return q.gauche
      .map((g, i) => `${inline(g)} → <strong>${LETTRES[ordreDroite.indexOf(i)]}</strong>`)
      .join(' ; ')
  }
  return ''
})

/* ---------- Formules ---------- */
let enCours = null
async function composer(el) {
  if (!el) return
  const mj = window.MathJax
  try {
    if (mj?.startup?.promise) await mj.startup.promise
    if (mj?.typesetPromise) {
      // MathJax ne doit pas composer deux fois en même temps
      enCours = (enCours || Promise.resolve()).then(() => mj.typesetPromise([el]))
      await enCours
    }
  } catch (e) {
    console.warn('[Quiz] MathJax :', e)
  }
  tuneMathOverflow(el)
}

let minuterie = null
watch(apercuHtml, () => {
  clearTimeout(minuterie)
  minuterie = setTimeout(() => nextTick(() => composer(apercu.value)), 120)
})
watch(valide, () => nextTick(() => composer(racine.value)))
onMounted(() => composer(racine.value))
</script>

<style scoped>
.qq {
  padding: 22px 26px 22px;
  transition: border-color 0.2s ease;
}

.qq.is-ok {
  border-color: rgba(59, 133, 68, 0.45);
}

.qq.is-ko {
  border-color: rgba(232, 145, 45, 0.55);
}

.qq-head {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px 12px;
  margin-bottom: 14px;
}

.qq-num {
  font-size: 15px;
  font-weight: 700;
  color: var(--es-navy);
}

.qq-num small {
  font-size: 13px;
  font-weight: 600;
  color: var(--es-muted);
}

.qq-tags {
  display: inline-flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
}

.qq-theme {
  font-size: 12px;
  font-weight: 600;
  color: var(--es-muted);
}

.qq-enonce {
  font-size: 17px;
  line-height: 1.6;
}

.qq-fig {
  margin: 14px auto 4px;
}

.qq-consigne {
  margin: 14px 0 10px !important;
  font-size: 13px;
  font-weight: 600;
  color: var(--es-muted);
}

/* ---------- Choix ---------- */
.qq-choix {
  display: grid;
  gap: 10px;
}

.qq-choix--figures {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.qq-option {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  min-height: 52px;
  padding: 10px 14px;
  border: 1.5px solid var(--es-line-strong);
  border-radius: 14px;
  background: #fff;
  font: 500 16px/1.45 var(--es-font);
  color: var(--es-ink);
  text-align: left;
  cursor: pointer;
  transition: border-color 0.15s ease, background-color 0.15s ease, box-shadow 0.15s ease;
}

.qq-option:not(:disabled):hover {
  border-color: var(--es-navy);
  background: var(--es-navy-50);
}

.qq-option:disabled {
  cursor: default;
}

.qq-option.is-on {
  border-color: var(--es-navy);
  background: var(--es-navy-50);
  box-shadow: 0 0 0 3px rgba(27, 60, 142, 0.12);
}

.qq-option.is-bonne {
  border-color: var(--es-green-700);
  background: var(--es-green-50);
  box-shadow: none;
}

.qq-option.is-oubliee {
  border-color: var(--es-green-700);
  border-style: dashed;
  background: #fff;
  box-shadow: none;
}

.qq-option.is-fausse {
  border-color: var(--es-orange);
  background: var(--es-orange-50);
  box-shadow: none;
}

.qq-option__note {
  margin-left: auto;
  flex-shrink: 0;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--es-green-700);
}

.qq-option.is-fausse .qq-option__note {
  color: var(--es-orange-700);
}

.qq-option.is-terne {
  opacity: 0.6;
}

.qq-option__mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 30px;
  height: 30px;
  border: 1.5px solid var(--es-line-strong);
  border-radius: 9px;
  font-size: 14px;
  font-weight: 700;
  color: var(--es-muted);
  background: #fff;
}

.qq-option__mark svg {
  width: 18px;
  height: 18px;
}

.qq-option.is-on .qq-option__mark {
  border-color: var(--es-navy);
  background: var(--es-navy);
  color: #fff;
}

.qq-option.is-bonne .qq-option__mark {
  border-color: var(--es-green-700);
  background: var(--es-green-700);
  color: #fff;
}

.qq-option.is-oubliee .qq-option__mark {
  border-color: var(--es-green-700);
  color: var(--es-green-700);
}

.qq-option.is-fausse .qq-option__mark {
  border-color: var(--es-orange);
  background: var(--es-orange);
  color: #fff;
}

.qq-choix--figures .qq-option {
  flex-direction: column;
  align-items: stretch;
  padding: 8px;
}

.qq-choix--figures .qq-option__mark {
  align-self: flex-start;
}

.qq-option__txt {
  min-width: 0;
}

/* Le fond blanc des figures se fond dans la couleur du choix (vert, orange) */
.qq-option :deep(img),
.qq-cible :deep(img) {
  mix-blend-mode: multiply;
}

/* ---------- Vrai / faux ---------- */
.qq-vf {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.qq-option--vf {
  justify-content: center;
  font-weight: 700;
}

.qq-option--vf svg {
  width: 20px;
  height: 20px;
}

/* ---------- Saisie ---------- */
.qq-champ {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 14px;
  border: 1.5px solid var(--es-line-strong);
  border-radius: 14px;
  background: #fff;
}

.qq-champ:focus-within {
  border-color: var(--es-navy);
  box-shadow: 0 0 0 3px rgba(27, 60, 142, 0.12);
}

.qq-champ.is-ok {
  border-color: var(--es-green-700);
  background: var(--es-green-50);
}

.qq-champ.is-ko {
  border-color: var(--es-orange);
  background: var(--es-orange-50);
}

.qq-champ input {
  flex: 1;
  min-width: 0;
  height: 52px;
  border: 0;
  outline: 0;
  background: transparent;
  font: 500 18px var(--es-font);
  color: var(--es-ink);
}

.qq-unite {
  font-weight: 600;
  color: var(--es-muted);
}

.qq-touches {
  display: grid;
  grid-template-columns: repeat(8, minmax(0, 1fr));
  gap: 6px;
  margin-top: 10px;
}

@media (max-width: 560px) {
  .qq-touches {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

.qq-touche {
  height: 42px;
  padding: 0 10px;
  border: 1px solid var(--es-line-strong);
  border-radius: 10px;
  background: var(--es-bg);
  font: 600 16px var(--es-font);
  color: var(--es-navy);
  cursor: pointer;
}

.qq-touche:hover {
  border-color: var(--es-navy);
  background: var(--es-navy-50);
}

.qq-touche :deep(sup) {
  font-size: 11px;
}

.qq-apercu {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px 12px;
  margin-top: 12px !important;
  padding: 10px 14px;
  border-radius: 12px;
  background: var(--es-bg);
  font-size: 13px;
  font-weight: 600;
  color: var(--es-muted);
}

.qq-apercu__math {
  font-size: 17px;
  font-weight: 400;
  color: var(--es-ink);
}

.qq-apercu--erreur {
  background: var(--es-orange-50);
  color: var(--es-orange-700);
}

/* ---------- Associer ---------- */
.qq-assoc__cibles {
  display: grid;
  gap: 8px;
  margin: 0 0 14px;
  padding: 0;
  list-style: none;
}

.qq-assoc__cibles--figures {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.qq-cible {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border: 1px solid var(--es-line);
  border-radius: 12px;
  background: #fff;
}

.qq-assoc__cibles--figures .qq-cible {
  flex-direction: column;
  align-items: stretch;
}

.qq-lettre {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: var(--es-navy);
  font-size: 14px;
  font-weight: 700;
  color: #fff;
}

.qq-assoc__lignes {
  display: grid;
  gap: 8px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.qq-ligne {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px 12px;
  padding: 10px 12px;
  border: 1.5px solid var(--es-line-strong);
  border-radius: 12px;
  background: #fff;
}

.qq-ligne.is-bonne {
  border-color: var(--es-green-700);
  background: var(--es-green-50);
}

.qq-ligne.is-fausse {
  border-color: var(--es-orange);
  background: var(--es-orange-50);
}

.qq-ligne__txt {
  font-size: 16px;
}

.qq-ligne__choix {
  display: inline-flex;
  gap: 6px;
}

.qq-lettre-btn {
  width: 40px;
  height: 40px;
  border: 1.5px solid var(--es-line-strong);
  border-radius: 10px;
  background: #fff;
  font: 700 15px var(--es-font);
  color: var(--es-navy);
  cursor: pointer;
}

.qq-lettre-btn.is-on {
  border-color: var(--es-navy);
  background: var(--es-navy);
  color: #fff;
}

.qq-lettre-btn.is-bonne {
  border-color: var(--es-green-700);
  color: var(--es-green-700);
  border-style: dashed;
}

.qq-lettre-btn:disabled {
  cursor: default;
}

/* ---------- Ordre ---------- */
.qq-ordre {
  display: grid;
  gap: 8px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.qq-etape {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border: 1.5px solid var(--es-line-strong);
  border-radius: 12px;
  background: #fff;
}

.qq-etape.is-bonne {
  border-color: var(--es-green-700);
  background: var(--es-green-50);
}

.qq-etape.is-fausse {
  border-color: var(--es-orange);
  background: var(--es-orange-50);
}

.qq-etape__num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--es-navy-50);
  font-size: 14px;
  font-weight: 700;
  color: var(--es-navy);
}

.qq-etape.is-bonne .qq-etape__num {
  background: var(--es-green-700);
  color: #fff;
}

.qq-etape__txt {
  flex: 1;
  min-width: 0;
  font-size: 16px;
}

.qq-etape__btns {
  display: inline-flex;
  flex-direction: column;
  gap: 4px;
}

.qq-etape__btns button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 28px;
  border: 1px solid var(--es-line-strong);
  border-radius: 8px;
  background: #fff;
  color: var(--es-navy);
  cursor: pointer;
}

.qq-etape__btns button:disabled {
  opacity: 0.35;
  cursor: default;
}

.qq-etape__btns svg {
  width: 16px;
  height: 16px;
}

/* ---------- Correction ---------- */
.qq-correction {
  margin-top: 18px;
  padding-top: 16px;
  border-top: 1px solid var(--es-line);
}

.qq-verdict {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 17px;
  font-weight: 700;
}

.qq-verdict svg {
  width: 26px;
  height: 26px;
  flex-shrink: 0;
}

.qq-verdict.is-ok {
  color: var(--es-green-700);
}

.qq-verdict.is-ko {
  color: var(--es-orange-700);
}

.qq-verdict.is-passee {
  color: var(--es-navy);
}

.qq-attendu {
  margin-top: 8px !important;
  font-size: 16px;
}

.qq-attendu > span:first-child {
  font-weight: 600;
  color: var(--es-ink-soft);
}

.qq-ordre--corrige {
  margin-top: 10px;
}

.qq-explication {
  margin-top: 12px;
  font-size: 16px;
  line-height: 1.6;
}

.qq-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

@media (max-width: 640px) {
  .qq {
    padding: 18px 16px;
  }

  .qq-enonce {
    font-size: 16px;
  }

  .qq-option {
    font-size: 15px;
  }

  .qq-actions .es-btn {
    flex: 1;
    padding: 0 12px;
  }
}

@media (max-width: 420px) {
  .qq-choix--figures,
  .qq-assoc__cibles--figures {
    grid-template-columns: minmax(0, 1fr);
  }
}
</style>
