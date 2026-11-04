<template>
  <div ref="docRef" class="es-doc sci-doc" :style="{ zoom }" v-html="html"></div>
</template>

<script setup>
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'
import { tuneMathOverflow, typesetElements } from '@/utils/scientificRenderer'

// Affiche un contenu de cours ou de fiche (format structuré OptiTAB ou ancien
// format), met ses formules en forme avec MathJax, puis renvoie la liste des
// titres pour construire le sommaire.
//
// Les formules sont calculées par morceaux : d'abord celles de l'écran, avant
// le premier affichage, puis les suivantes en arrière-plan sans figer la page
// (un long cours demande plusieurs secondes à un téléphone modeste). Un bloc
// en attente reste invisible : on ne voit jamais de LaTeX brut.
const props = defineProps({
  html: { type: String, default: '' },
  zoom: { type: Number, default: 1 },
  // Onglet affiché ; masqué, le calcul se met en pause et reprend au retour.
  actif: { type: Boolean, default: true }
})

const emit = defineEmits(['ready'])
const docRef = ref(null)
let alive = true

const nettoyer = (texte) => String(texte || '')
  .replace(/\\\(|\\\)|\\\[|\\\]|\$/g, '')
  .replace(/\\(mathbb|mathrm|text|mathcal|operatorname)\{([^}]*)\}/g, '$2')
  .replace(/\s+/g, ' ')
  .trim()

function collecterTitres(root) {
  const titres = []
  root.querySelectorAll('h2, h3').forEach((h, i) => {
    if (h.closest('.otm-box')) return
    const num = h.querySelector('.otm-h2-num, .otm-q-num')?.textContent?.trim()
    const texte = nettoyer(h.querySelector('.otm-h2-text, .otm-q-text')?.textContent || h.textContent)
    if (!texte || texte.length < 2) return
    h.id = h.id || `es-sec-${i}`
    titres.push({ id: h.id, niveau: h.tagName === 'H3' ? 3 : 2, num: num || '', texte })
  })
  return titres
}

// Ancien format : les tableaux larges défilent dans leur propre cadre.
function envelopperTableaux(root) {
  root.querySelectorAll('table').forEach((table) => {
    if (table.closest('.otm') || table.parentElement?.classList.contains('es-doc-scroll')) return
    const cadre = document.createElement('div')
    cadre.className = 'es-doc-scroll'
    table.parentNode.insertBefore(cadre, table)
    cadre.appendChild(table)
  })
}

// ---------- Calcul des formules par morceaux ----------

const AVEC_FORMULE = /\\\(|\\\[|\$|\\begin\{/
const BUDGET_MS = 40

let tour = 0 // numéro du contenu affiché : un nouveau contenu arrête l'ancien calcul
let boucle = 0 // contenu dont le calcul tourne (0 : aucun)
let attente = [] // blocs dont les formules restent à calculer
let decoupe = false // document découpé en blocs pour ce contenu
let pret = false // premier écran calculé et sommaire envoyé
let titres = []
let largeurReglee = 0 // largeur du document lors du dernier réglage des formules larges

function regler(cible) {
  tuneMathOverflow(cible)
  largeurReglee = docRef.value?.clientWidth || 0
}

// Blocs du document, dans l'ordre : on descend tant qu'un conteneur n'a qu'un enfant.
function decouper(root) {
  let niveau = root
  while (niveau.children.length === 1 && niveau.firstElementChild.children.length) niveau = niveau.firstElementChild
  return [...niveau.children]
}

const estVisible = (bloc) => {
  const r = bloc.getBoundingClientRect()
  return r.bottom > 0 && r.top < window.innerHeight
}

async function traiter(blocs) {
  if (!blocs.length) return
  try {
    await typesetElements(blocs)
  } catch (e) {
    console.warn('[EspaceDoc] MathJax :', e)
  }
  // Retirés de la file même en cas d'erreur : mieux vaut du LaTeX brut qu'un bloc invisible.
  const faits = new Set(blocs)
  attente = attente.filter((b) => !faits.has(b))
  blocs.forEach((b) => b.classList.remove('es-attente'))
  regler(blocs)
}

// Calcule les formules en attente. S'arrête si le contenu change ou si le
// composant disparaît ; se met en pause quand l'onglet est masqué (il
// reprend à son retour, voir le suivi de `actif`).
async function continuer(monTour) {
  const root = docRef.value
  if (!root || !props.actif || boucle === monTour) return
  boucle = monTour
  const encore = () => alive && monTour === tour && props.actif
  try {
    if (!pret) {
      const limite = window.innerHeight * 1.5
      await traiter(attente.filter((b) => b.getBoundingClientRect().top < limite))
      if (!alive || monTour !== tour) return
      pret = true
      emit('ready', titres)
    }
    let parMorceau = 4
    while (attente.length) {
      await new Promise((resolve) => setTimeout(resolve, 0))
      if (!encore()) return
      // Ce que l'élève regarde passe devant (s'il a fait défiler), sinon dans l'ordre.
      const visibles = attente.filter(estVisible)
      const morceau = visibles.length ? visibles : attente.slice(0, parMorceau)
      const debut = performance.now()
      await traiter(morceau)
      const duree = performance.now() - debut
      parMorceau = Math.max(1, Math.min(20, Math.round(morceau.length * BUDGET_MS / Math.max(duree, 1))))
    }
    if (!encore()) return
    // Dernier passage sur tout le document : formules éventuelles hors des blocs.
    await typesetElements([root]).catch((e) => console.warn('[EspaceDoc] MathJax :', e))
    if (encore()) regler(root)
  } finally {
    if (boucle === monTour) boucle = 0
  }
}

async function preparer() {
  const monTour = ++tour
  decoupe = false
  pret = false
  attente = []
  await nextTick()
  const root = docRef.value
  if (!alive || !root || monTour !== tour) return
  titres = collecterTitres(root)
  envelopperTableaux(root)
  try {
    const mj = window.MathJax
    if (mj?.startup?.promise) await mj.startup.promise
    if (mj?.typesetClear) mj.typesetClear([root])
  } catch (e) {
    console.warn('[EspaceDoc] MathJax :', e)
  }
  if (!alive || monTour !== tour) return
  attente = decouper(root).filter((b) => AVEC_FORMULE.test(b.textContent || ''))
  attente.forEach((b) => b.classList.add('es-attente'))
  decoupe = true
  await continuer(monTour)
}

// Avant un saut dans le sommaire : formules calculées jusqu'à la cible (et un
// écran au-delà), pour arriver sur une page qui ne bouge plus.
async function preparerJusqua(cible) {
  if (!attente.length || !cible) return
  const limite = cible.getBoundingClientRect().top + window.innerHeight * 1.5
  await traiter(attente.filter((b) => b.getBoundingClientRect().top < limite))
}

watch(() => props.html, preparer, { immediate: true })

// Taille du texte changée : la place disponible pour les formules larges aussi
// (onglet masqué : réglage fait à son retour).
let aRegler = false
watch(() => props.zoom, () => nextTick(() => {
  if (!docRef.value || !pret) return
  if (props.actif) regler(docRef.value)
  else aRegler = true
}))

// Onglet réaffiché : reprendre un calcul interrompu, sinon réajuster les
// formules larges si la place a changé entre-temps (taille du texte,
// téléphone tourné, fenêtre redimensionnée).
watch(() => props.actif, (affiche) => {
  const root = docRef.value
  if (!affiche || !root || !decoupe) return
  if (!pret || attente.length) continuer(tour)
  else if (aRegler || root.clientWidth !== largeurReglee) regler(root)
  aRegler = false
}, { flush: 'post' })

onBeforeUnmount(() => {
  alive = false
})

defineExpose({ el: docRef, preparerJusqua })
</script>

<style scoped>
.es-doc {
  min-width: 0;
}

/* Bloc dont les formules ne sont pas encore calculées (quelques instants) */
.es-doc :deep(.es-attente) {
  visibility: hidden;
}

.es-doc :deep(.es-doc-scroll) {
  max-width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.es-doc :deep(img) {
  max-width: 100%;
  height: auto;
}

.es-doc :deep(mjx-container[display='true']) {
  max-width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
}
</style>
