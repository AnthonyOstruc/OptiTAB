<template>
  <figure
    ref="rootRef"
    class="mk"
    role="region"
    aria-roledescription="carrousel"
    aria-label="Exemples de corrections pas à pas"
    @mouseenter="hover = true"
    @mouseleave="hover = false"
    @focusin="onFocusIn"
    @focusout="onFocusOut"
  >
    <p class="vt-sr-only" :aria-live="manual ? 'polite' : 'off'">
      Exemple {{ index + 1 }} sur {{ total }}. {{ current.alt }}
    </p>

    <div
      class="mk-window"
      aria-hidden="true"
      @pointerdown="onPointerDown"
      @pointerup="onPointerUp"
      @pointercancel="swipe = null"
    >
      <div class="mk-bar">
        <span class="mk-dot"></span><span class="mk-dot"></span><span class="mk-dot"></span>
        <span class="mk-url">optitab.net</span>
        <!-- Sur téléphone, la classe passe dans la barre : une ligne de gagnée. -->
        <Transition name="mk-swap" mode="out-in">
          <span :key="current.id" class="mk-bar__chip">{{ current.niveau }}</span>
        </Transition>
      </div>

      <!-- Toutes les diapositives occupent la même case : la carte garde la hauteur
           de la plus grande, la page ne bouge donc pas quand l'exemple change. -->
      <div class="mk-slides">
        <article
          v-for="(ex, i) in exemples"
          :key="ex.id"
          :class="['mk-slide', { 'is-active': i === index }]"
        >
          <div class="mk-meta">
            <span class="mk-chip mk-chip--navy">{{ ex.niveau }}</span>
            <span class="mk-chip mk-chip--extra">{{ ex.type }}</span>
          </div>

          <p class="mk-statement"><MathText :items="ex.enonce" /></p>

          <div class="mk-method">
            <span class="mk-tag">Méthode</span>
            <span class="mk-method__text">{{ ex.methode.titre }}&nbsp;: <MathText :items="ex.methode.formule" /></span>
          </div>

          <ol class="mk-steps">
            <li v-for="(etape, n) in ex.etapes" :key="n" class="mk-step">
              <p class="mk-step__head"><span class="mk-step__num">Étape {{ n + 1 }}</span>{{ etape.titre }}</p>

              <div v-if="etape.lignes" class="mk-step__body">
                <p v-for="(ligne, l) in etape.lignes" :key="l"><MathText :items="ligne" /></p>
              </div>

              <!-- Tableau de variations (un seul extremum) -->
              <div v-if="etape.visuel?.type === 'variations'" class="mk-vt">
                <div class="mk-vt__lab"><MathText :items="[etape.visuel.libelles[0]]" /></div>
                <div class="mk-vt__cells">
                  <span v-for="(val, k) in etape.visuel.x" :key="k" :style="{ '--at': ['10%', '50%', '90%'][k] }"><MathText :items="[val]" /></span>
                </div>

                <div class="mk-vt__lab"><MathText :items="[etape.visuel.libelles[1]]" /></div>
                <div class="mk-vt__cells mk-vt__cells--sign">
                  <span class="mk-vt__sign" style="--at: 30%"><MathText :items="[etape.visuel.signes[0]]" /></span>
                  <span class="mk-vt__zero" style="--at: 50%"><MathText :items="[etape.visuel.signes[1]]" /></span>
                  <span class="mk-vt__sign" style="--at: 70%"><MathText :items="[etape.visuel.signes[2]]" /></span>
                </div>

                <div class="mk-vt__lab"><MathText :items="[etape.visuel.libelles[2]]" /></div>
                <div class="mk-vt__cells mk-vt__cells--var">
                  <svg class="mk-vt__arrows" viewBox="0 0 300 52">
                    <defs>
                      <marker :id="`mk-vt-${ex.id}`" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto">
                        <path d="M0 0 L10 5 L0 10 Z" />
                      </marker>
                    </defs>
                    <path d="M46 14 L128 39" :marker-end="`url(#mk-vt-${ex.id})`" />
                    <path d="M172 39 L240 17" :marker-end="`url(#mk-vt-${ex.id})`" />
                  </svg>
                  <span class="mk-vt__top" style="--at: 10%"><MathText :items="[etape.visuel.haut[0]]" /></span>
                  <span class="mk-vt__bottom" style="--at: 50%"><MathText :items="[etape.visuel.bas]" /></span>
                  <span class="mk-vt__top" style="--at: 90%"><MathText :items="[etape.visuel.haut[1]]" /></span>
                </div>
              </div>

              <!-- Figure : tracés SVG + étiquettes posées en pourcentage -->
              <div
                v-else-if="etape.visuel?.type === 'figure'"
                class="mk-fig"
                :style="{
                  aspectRatio: `${etape.visuel.vue[0]} / ${etape.visuel.vue[1]}`,
                  maxWidth: etape.visuel.largeur ? `${etape.visuel.largeur}px` : null
                }"
              >
                <svg class="mk-fig__svg" :viewBox="`0 0 ${etape.visuel.vue[0]} ${etape.visuel.vue[1]}`">
                  <defs>
                    <marker :id="`mk-fl-${ex.id}`" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
                      <path d="M0 0 L10 5 L0 10 Z" class="mk-fig__tete" />
                    </marker>
                  </defs>
                  <path
                    v-for="(t, k) in etape.visuel.traces"
                    :key="`t${k}`"
                    :d="t.d"
                    :class="`mk-fig__${t.style}`"
                    :marker-end="t.fleche ? `url(#mk-fl-${ex.id})` : null"
                  />
                  <circle
                    v-for="(p, k) in etape.visuel.points || []"
                    :key="`p${k}`"
                    :cx="p.c[0]"
                    :cy="p.c[1]"
                    r="3.2"
                    :class="`mk-fig__point mk-fig__point--${p.ton || 'navy'}`"
                  />
                </svg>
                <span
                  v-for="(lab, k) in etape.visuel.etiquettes"
                  :key="`e${k}`"
                  :class="['mk-fig__lab', `mk-fig__lab--${lab.ancre || 'c'}`, lab.ton ? `mk-fig__lab--${lab.ton}` : '']"
                  :style="{ left: `${(lab.x / etape.visuel.vue[0]) * 100}%`, top: `${(lab.y / etape.visuel.vue[1]) * 100}%` }"
                >
                  <template v-if="lab.texte">{{ lab.texte }}</template>
                  <MathText v-else :items="[lab]" />
                </span>
              </div>
            </li>
          </ol>

          <p class="mk-result">
            <CheckCircleIcon class="mk-result-icon" />
            <span><MathText :items="ex.resultat" /></span>
          </p>
        </article>
      </div>
    </div>

    <div class="mk-float mk-float--sheet" aria-hidden="true">
      <span class="mk-float-icon mk-float-icon--green"><DocumentTextIcon /></span>
      <Transition name="mk-swap" mode="out-in">
        <span :key="current.id" class="mk-float-text">
          <strong>Fiche de synthèse</strong>
          <span>{{ current.fiche }}</span>
        </span>
      </Transition>
    </div>

    <div class="mk-float mk-float--progress" aria-hidden="true">
      <span class="mk-ring" :style="{ '--p': current.progression }">
        <span>{{ current.progression }} %</span>
      </span>
      <Transition name="mk-swap" mode="out-in">
        <span :key="current.id" class="mk-float-text">
          <strong>Ta progression</strong>
          <span class="mk-xp">+{{ current.xp }} XP aujourd’hui</span>
        </span>
      </Transition>
    </div>

    <!-- Navigation : une barre par exemple ; celle en cours se remplit en 5 s,
         et la fin de son animation fait passer à l'exemple suivant. -->
    <div class="mk-nav">
      <button
        v-for="(ex, i) in exemples"
        :key="ex.id"
        type="button"
        :class="['mk-nav__dot', { 'is-active': i === index }]"
        :aria-label="`Exemple ${i + 1} sur ${total} : ${ex.niveau}`"
        :aria-current="i === index ? 'true' : null"
        @click="goTo(i, true)"
      >
        <span
          v-if="i === index"
          :class="['mk-nav__fill', { 'is-running': playing }]"
          :style="{ animationPlayState: paused ? 'paused' : 'running' }"
          @animationend="next"
        ></span>
      </button>
      <button
        type="button"
        class="mk-nav__toggle"
        :aria-label="playing ? 'Mettre en pause le défilement des exemples' : 'Reprendre le défilement des exemples'"
        @click="playing = !playing"
      >
        <PauseIcon v-if="playing" aria-hidden="true" />
        <PlayIcon v-else aria-hidden="true" />
      </button>
    </div>
  </figure>
</template>

<script setup>
import { ref, computed, h, createTextVNode, onMounted, onBeforeUnmount } from 'vue'
import { CheckCircleIcon, DocumentTextIcon, PauseIcon, PlayIcon } from '@heroicons/vue/24/solid'
import { vitrineExemples } from '@/config/vitrineExemples.js'
// Formules pré-rendues par KaTeX (scripts/vitrine-math.mjs) : aucun moteur chargé ici.
import M from '@/config/vitrineMath.js'

const exemples = vitrineExemples
const total = exemples.length

const escapeHtml = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c])

const mathHtml = (tex) => {
  if (M[tex]) return M[tex]
  if (import.meta.env.DEV) console.warn(`[vitrine] Formule non pré-rendue (lancer node scripts/vitrine-math.mjs) : ${tex}`)
  return escapeHtml(tex)
}

// Une ligne = liste de morceaux : texte, formule, formule surlignée ou groupe insécable.
const MathText = (props) =>
  (props.items || []).map((s) => {
    if (typeof s === 'string') return createTextVNode(s)
    if (s.groupe) return h('span', { class: 'mk-nowrap' }, MathText({ items: s.groupe }))
    return h('span', {
      class: s.pill ? ['mk-pill', `mk-pill--${s.pill}`] : 'mk-m',
      innerHTML: mathHtml(s.tex)
    })
  })
MathText.props = ['items']

const rootRef = ref(null)
const index = ref(0)
const current = computed(() => exemples[index.value])

const playing = ref(true)
const manual = ref(false)
const hover = ref(false)
const keyboardFocus = ref(false)
const inView = ref(true)
const pageHidden = ref(false)
const paused = computed(() => hover.value || keyboardFocus.value || !inView.value || pageHidden.value)

const goTo = (i, byUser = false) => {
  index.value = (i + total) % total
  if (byUser) manual.value = true
}

const next = () => goTo(index.value + 1)

const onFocusIn = (event) => {
  if (event.target?.matches?.(':focus-visible')) keyboardFocus.value = true
}

const onFocusOut = (event) => {
  if (!rootRef.value?.contains(event.relatedTarget)) keyboardFocus.value = false
}

// Glisser du doigt vers la gauche ou la droite pour changer d'exemple.
const swipe = ref(null)
const onPointerDown = (event) => {
  if (event.pointerType === 'mouse') return
  swipe.value = { x: event.clientX, y: event.clientY }
}
const onPointerUp = (event) => {
  if (!swipe.value) return
  const dx = event.clientX - swipe.value.x
  const dy = event.clientY - swipe.value.y
  swipe.value = null
  if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy) * 1.4) goTo(index.value + (dx < 0 ? 1 : -1), true)
}

let observer = null
const onVisibility = () => {
  pageHidden.value = document.hidden
}

onMounted(() => {
  // Mouvement réduit demandé : pas de défilement automatique (les barres restent cliquables).
  if (window.matchMedia?.('(prefers-reduced-motion: reduce)').matches) playing.value = false
  document.addEventListener('visibilitychange', onVisibility)
  if ('IntersectionObserver' in window && rootRef.value) {
    observer = new IntersectionObserver(([entry]) => {
      inView.value = entry.isIntersecting
    }, { threshold: 0.35 })
    observer.observe(rootRef.value)
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('visibilitychange', onVisibility)
  observer?.disconnect()
  observer = null
})
</script>

<style scoped>
.mk {
  position: relative;
  margin: 0;
  padding: 28px 36px 60px 28px;
}

.mk-window {
  position: relative;
  overflow: hidden;
  border: 1px solid var(--vt-line);
  border-radius: 20px;
  background: #fff;
  box-shadow: var(--vt-shadow-lg);
  touch-action: pan-y;
}

.mk-bar {
  display: flex;
  align-items: center;
  gap: 7px;
  height: 34px;
  padding: 0 14px;
  border-bottom: 1px solid var(--vt-line);
  background: var(--vt-bg-soft);
}

.mk-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #d9deea;
}

/* À gauche : la carte « Fiche de synthèse » occupe le coin droit. */
.mk-url {
  margin-left: 10px;
  padding: 3px 12px;
  border-radius: 999px;
  background: #fff;
  border: 1px solid var(--vt-line);
  font-size: 12px;
  font-weight: 600;
  color: var(--vt-muted);
}

.mk-bar__chip {
  display: none;
  margin-left: 6px;
  padding: 2px 9px;
  border: 1px solid var(--vt-navy-100);
  border-radius: 999px;
  background: var(--vt-navy-50);
  font-size: 11px;
  font-weight: 700;
  color: var(--vt-navy);
  white-space: nowrap;
}

/* ---------- Diapositives ---------- */

.mk-slides {
  display: grid;
}

.mk-slide {
  grid-area: 1 / 1;
  display: flex;
  flex-direction: column;
  padding: 16px 20px 18px;
  font-size: 14px;
  line-height: 1.45;
  color: var(--vt-ink-soft);
  opacity: 0;
  visibility: hidden;
  transform: translateY(8px);
  transition: opacity 0.45s ease, transform 0.45s ease, visibility 0s linear 0.45s;
}

.mk-slide.is-active {
  opacity: 1;
  visibility: visible;
  transform: none;
  transition-delay: 0.12s, 0.12s, 0s;
}

.mk-slide p {
  margin: 0;
}

/* Formules KaTeX (rendu de manuel), un peu plus grandes que le texte. */
.mk-slide :deep(.katex) {
  font-size: 1.14em;
  color: var(--vt-ink);
}

.mk :deep(.mk-nowrap) {
  white-space: nowrap;
}

.mk-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}

.mk-chip {
  padding: 2px 9px;
  border-radius: 999px;
  background: var(--vt-bg-soft);
  border: 1px solid var(--vt-line);
  font-size: 12px;
  font-weight: 700;
  color: var(--vt-muted);
}

.mk-chip--navy {
  background: var(--vt-navy-50);
  border-color: var(--vt-navy-100);
  color: var(--vt-navy);
}

.mk-slide .mk-statement {
  margin-bottom: 10px;
  padding: 8px 12px;
  border-left: 3px solid var(--vt-navy);
  border-radius: 0 10px 10px 0;
  background: var(--vt-navy-50);
  font-size: 15px;
  font-weight: 600;
  color: var(--vt-ink);
}

/* ---------- Méthode ---------- */

.mk-method {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px 10px;
  margin-bottom: 10px;
  padding: 7px 11px;
  border: 1px solid #cfe8cf;
  border-radius: 10px;
  background: var(--vt-green-50);
}

.mk-tag {
  padding: 2px 8px;
  border-radius: 6px;
  background: var(--vt-green-700);
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.mk-method__text {
  font-weight: 600;
  color: var(--vt-ink);
}

/* Bleu (a) et vert (b) : les mêmes couleurs dans la méthode et dans le calcul. */
.mk :deep(.mk-pill) {
  display: inline-block;
  margin: 1px 3px;
  padding: 2px 6px;
  border-radius: 6px;
  line-height: 1.55;
}

.mk :deep(.mk-pill--a) {
  background: #e3e9f8;
  box-shadow: inset 0 0 0 1px #c5d1ef;
}

.mk :deep(.mk-pill--a .katex) {
  color: var(--vt-navy);
}

.mk :deep(.mk-pill--b) {
  background: #dff1df;
  box-shadow: inset 0 0 0 1px #bfe0c0;
}

.mk :deep(.mk-pill--b .katex) {
  color: var(--vt-green-700);
}

/* ---------- Étapes (comme sur la plateforme) ---------- */

.mk-steps {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 0 0 12px;
  padding: 0;
  list-style: none;
}

.mk-step__head {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 2px;
  font-size: 14px;
  font-weight: 700;
  color: var(--vt-ink);
}

.mk-step__num {
  flex-shrink: 0;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--vt-navy);
}

.mk-step__body {
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding-left: 12px;
  border-left: 2px solid var(--vt-navy-100);
}

.mk-step__body + .mk-fig,
.mk-step__body + .mk-vt {
  margin-top: 6px;
}

/* ---------- Tableau de variations ---------- */

.mk-vt {
  display: grid;
  grid-template-columns: 58px minmax(0, 1fr);
  overflow: hidden;
  border: 1px solid var(--vt-navy-100);
  border-radius: 10px;
}

.mk-vt__lab {
  display: flex;
  align-items: center;
  justify-content: center;
  border-right: 1px solid var(--vt-navy-100);
  background: var(--vt-navy-50);
}

.mk-vt__lab :deep(.katex) {
  color: var(--vt-navy);
}

.mk-vt__cells {
  position: relative;
  height: 28px;
}

.mk-vt__lab:not(:nth-last-child(2)),
.mk-vt__cells:not(:last-child) {
  border-bottom: 1px solid var(--vt-navy-100);
}

.mk-vt__cells > span {
  position: absolute;
  top: 50%;
  left: var(--at);
  transform: translate(-50%, -50%);
  white-space: nowrap;
}

/* Le 0 de f′ est posé sur la barre verticale, comme dans un tableau de lycée. */
.mk-vt__cells--sign::before {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: 50%;
  border-left: 1px solid var(--vt-navy-100);
}

.mk-vt__zero {
  padding: 0 3px;
  background: #fff;
}

.mk-vt__sign :deep(.katex) {
  font-size: 1.3em;
  font-weight: 700;
}

.mk-vt__cells--var {
  height: auto;
}

.mk-vt__arrows {
  display: block;
  width: 100%;
  height: auto;
  min-height: 46px;
}

.mk-vt__arrows path {
  fill: none;
  stroke: var(--vt-navy);
  stroke-width: 1.7;
  stroke-linecap: round;
}

.mk-vt__arrows marker path {
  fill: var(--vt-navy);
  stroke: none;
}

.mk-vt__cells--var > span.mk-vt__top {
  top: 4px;
  transform: translateX(-50%);
}

.mk-vt__cells--var > span.mk-vt__bottom {
  top: auto;
  bottom: 2px;
  transform: translateX(-50%);
}

.mk-vt__bottom :deep(.katex) {
  font-weight: 700;
  color: var(--vt-green-700);
}

/* ---------- Figures ---------- */

.mk-fig {
  position: relative;
  width: 100%;
  margin: 0 auto;
  container-type: inline-size;
}

.mk-fig__svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  overflow: visible;
}

.mk-fig__svg path {
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.mk-fig__axe {
  stroke: #9aa6c2;
  stroke-width: 1.2;
}

.mk-fig__tete {
  fill: #9aa6c2;
  stroke: none;
}

.mk-fig__trait {
  stroke: var(--vt-navy);
  stroke-width: 2;
}

.mk-fig__angle {
  stroke: var(--vt-navy);
  stroke-width: 1.2;
}

.mk-fig__courbe,
.mk-fig__chemin-a {
  stroke: var(--vt-navy);
  stroke-width: 2.2;
}

.mk-fig__vert {
  stroke: var(--vt-green);
  stroke-width: 2.6;
}

.mk-fig__chemin-b {
  stroke: var(--vt-green-700);
  stroke-width: 2.2;
}

.mk-fig__branche {
  stroke: #b9c3da;
  stroke-width: 1.4;
}

.mk-fig__fin {
  stroke: #c5d1ef;
  stroke-width: 1;
}

.mk-fig__unite {
  stroke: var(--vt-navy);
  stroke-width: 1.6;
}

.mk-fig__svg .mk-fig__case {
  fill: #fff;
  stroke: var(--vt-navy-100);
  stroke-width: 1;
}

.mk-fig__svg .mk-fig__case-a {
  fill: #dbe3f6;
  stroke: #c5d1ef;
  stroke-width: 1;
}

.mk-fig__svg .mk-fig__case-b {
  fill: #d6eed6;
  stroke: #bfe0c0;
  stroke-width: 1;
}

.mk-fig__point {
  stroke: #fff;
  stroke-width: 1.4;
}

.mk-fig__point--navy {
  fill: var(--vt-navy);
}

.mk-fig__point--vert {
  fill: var(--vt-green-700);
}

/* Étiquettes : taille liée à la largeur de la figure, pour rester à l'échelle. */
.mk-fig__lab {
  position: absolute;
  font-size: clamp(11px, 3.4cqw, 14px);
  line-height: 1;
  white-space: nowrap;
  transform: translate(-50%, -50%);
}

.mk-fig__lab--g {
  transform: translate(0, -50%);
}

.mk-fig__lab--d {
  transform: translate(-100%, -50%);
}

.mk-fig__lab :deep(.katex) {
  font-size: 1.12em;
  color: var(--vt-ink);
}

.mk-fig__lab--navy :deep(.katex) {
  color: var(--vt-navy);
}

.mk-fig__lab--vert,
.mk-fig__lab--vert :deep(.katex) {
  color: var(--vt-green-700);
}

.mk-fig__lab--muted :deep(.katex) {
  color: #8a94ab;
}

.mk-fig__lab--vert:not(:has(.katex)) {
  font-size: clamp(11px, 3cqw, 13px);
  font-style: italic;
  font-weight: 600;
}

/* ---------- Résultat ---------- */

/* Toujours en bas de la carte, quelle que soit la longueur de l'exemple. */
.mk-slide .mk-result {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: auto;
  padding: 8px 12px;
  border-radius: 12px;
  background: var(--vt-green-50);
  border: 1px solid #cfe8cf;
  font-size: 14px;
  font-weight: 700;
  color: var(--vt-green-700);
}

.mk-result :deep(.katex) {
  color: var(--vt-green-700);
}

.mk-result-icon {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
}

/* ---------- Cartes flottantes ---------- */

.mk-float {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px 12px 12px;
  border: 1px solid var(--vt-line);
  border-radius: 16px;
  background: #fff;
  box-shadow: var(--vt-shadow-lg);
  animation: mk-float 6s ease-in-out infinite;
}

.mk-float--sheet {
  top: 0;
  right: 0;
}

/* Mord sur le bas de la carte sans jamais toucher l'encadré du résultat. */
.mk-float--progress {
  bottom: 0;
  left: 0;
  animation-delay: -3s;
}

.mk-float-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 12px;
}

.mk-float-icon svg {
  width: 22px;
  height: 22px;
}

.mk-float-icon--green {
  background: var(--vt-green-50);
  color: var(--vt-green-700);
}

.mk-float-text {
  display: flex;
  flex-direction: column;
  line-height: 1.3;
  font-size: 12px;
  color: var(--vt-muted);
}

.mk-float-text strong {
  font-size: 14px;
  color: var(--vt-ink);
}

.mk-xp {
  color: var(--vt-green-700);
  font-weight: 700;
}

.mk-ring {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: conic-gradient(var(--vt-green) calc(var(--p) * 1%), var(--vt-navy-50) 0);
  font-size: 11px;
  font-weight: 700;
  color: var(--vt-ink);
  transition: --p 0.9s ease;
}

.mk-ring::before {
  content: '';
  position: absolute;
  inset: 5px;
  border-radius: 50%;
  background: #fff;
}

.mk-ring span {
  position: relative;
}

.mk-swap-enter-active,
.mk-swap-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.mk-swap-enter-from {
  opacity: 0;
  transform: translateY(4px);
}

.mk-swap-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

@keyframes mk-float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-6px);
  }
}

/* ---------- Navigation ---------- */

.mk-nav {
  position: absolute;
  right: 36px;
  bottom: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.mk-nav__dot {
  position: relative;
  width: 22px;
  height: 22px;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
}

/* Barre visible de 4 px, dans une zone cliquable de 22 px. */
.mk-nav__dot::before {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  top: 9px;
  height: 4px;
  border-radius: 4px;
  background: #cfd6e4;
  transition: background-color 0.2s ease;
}

.mk-nav__dot:hover::before {
  background: #aab5cc;
}

.mk-nav__dot.is-active {
  width: 44px;
}

.mk-nav__dot.is-active::before {
  background: var(--vt-navy-100);
}

.mk-nav__fill {
  position: absolute;
  left: 0;
  top: 9px;
  height: 4px;
  width: 100%;
  border-radius: 4px;
  background: var(--vt-navy);
  transform-origin: left center;
}

.mk-nav__fill.is-running {
  animation: mk-fill 5s linear forwards;
}

@keyframes mk-fill {
  from {
    transform: scaleX(0);
  }
  to {
    transform: scaleX(1);
  }
}

.mk-nav__toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  margin-left: 4px;
  padding: 0;
  border: 1px solid var(--vt-line-strong);
  border-radius: 50%;
  background: #fff;
  color: var(--vt-navy);
  cursor: pointer;
}

.mk-nav__toggle:hover {
  border-color: var(--vt-navy);
}

.mk-nav__toggle svg {
  width: 13px;
  height: 13px;
}

.mk-nav button:focus-visible {
  outline: 3px solid rgba(95, 172, 96, 0.55);
  outline-offset: 2px;
  border-radius: 6px;
}

@media (prefers-reduced-motion: reduce) {
  .mk-float {
    animation: none;
  }

  .mk-slide,
  .mk-slide.is-active {
    transform: none;
    transition: opacity 0.2s ease, visibility 0s;
  }
}

/* Téléphone : version allégée. Pas de cartes flottantes, la classe passe dans la
   barre de la fenêtre, schémas un peu plus petits. */
@media (max-width: 640px) {
  .mk {
    padding: 0 0 40px;
  }

  .mk-float,
  .mk-url,
  .mk-meta {
    display: none;
  }

  .mk-bar {
    height: 32px;
  }

  .mk-bar__chip {
    display: inline-block;
  }

  .mk-slide {
    padding: 12px 14px 14px;
    font-size: 13px;
  }

  .mk-slide .mk-statement {
    padding: 8px 11px;
    font-size: 14px;
  }

  .mk-step__head {
    font-size: 13px;
  }

  .mk-fig {
    width: 88%;
  }

  .mk-vt {
    grid-template-columns: 50px minmax(0, 1fr);
  }

  /* Pas la ligne des variations : sa hauteur suit celle des flèches. */
  .mk-vt__cells:not(.mk-vt__cells--var) {
    height: 26px;
  }

  .mk-nav {
    right: 50%;
    bottom: 6px;
    transform: translateX(50%);
  }
}

/* Petits téléphones (après le bloc 640 px pour le surcharger) : texte un peu plus
   petit et formules autorisées à passer à la ligne. */
@media (max-width: 374px) {
  .mk-slide {
    padding: 12px 12px 14px;
    font-size: 12px;
  }

  .mk-slide .mk-statement {
    font-size: 13px;
  }

  .mk :deep(.mk-nowrap) {
    white-space: normal;
  }
}
</style>

<style>
/* Permet d'animer la jauge de progression (propriété personnalisée typée). */
@property --p {
  syntax: '<number>';
  inherits: false;
  initial-value: 0;
}
</style>
