<template>
  <div class="cc">
    <div class="cc-progress" aria-hidden="true">
      <span :style="{ transform: `scaleX(${lecture})` }"></span>
    </div>

    <div v-if="loading" class="es-card cc-article">
      <div class="es-skeleton" style="height: 24px; width: 60%"></div>
      <div v-for="n in 6" :key="n" class="es-skeleton" style="height: 16px; margin-top: 14px"></div>
    </div>

    <div v-else-if="!cours" class="es-empty cc-empty">
      <strong>Le cours de ce chapitre arrive bientôt</strong>
      En attendant, tu peux déjà travailler la fiche et les exercices.
      <div class="cc-empty__actions">
        <button type="button" class="es-btn es-btn--sm es-btn--ghost" @click="$emit('go', 'fiche')">Voir la fiche</button>
        <button type="button" class="es-btn es-btn--sm" @click="$emit('go', 'exercices')">Faire les exercices</button>
      </div>
    </div>

    <div v-else class="cc-layout">
      <article ref="articleRef" class="es-card cc-article">
        <div class="cc-toolbar">
          <details v-if="titres.length" ref="tocMobileRef" class="cc-toc-mobile">
            <summary>
              <ListBulletIcon aria-hidden="true" />
              Sommaire
              <span class="cc-toc-mobile__count">{{ sections.length }}</span>
            </summary>
            <ol>
              <li v-for="t in titres" :key="t.id" :class="`is-level-${t.niveau}`">
                <a :href="`#${t.id}`" @click.prevent="aller(t.id, true)">
                  <span v-if="t.num" class="cc-toc__num">{{ t.num }}</span>{{ t.texte }}
                </a>
              </li>
            </ol>
          </details>
          <span class="cc-toolbar__spacer"></span>
          <TextSize v-model="zoom" />
          <a v-if="cours.pdf_url" :href="cours.pdf_url" class="es-btn es-btn--sm es-btn--ghost" :download="`${cours.titre}.pdf`">
            <ArrowDownTrayIcon aria-hidden="true" />
            <span class="cc-hide-sm">PDF</span>
          </a>
        </div>

        <EspaceDoc ref="docRef" :html="html" :zoom="zoom" :actif="actif" @ready="onReady" />

        <div v-if="cours.video_url" class="cc-video">
          <h2 class="es-h2">Vidéo explicative</h2>
          <div class="cc-video__frame">
            <iframe :src="cours.video_url" title="Vidéo du cours" frameborder="0" allowfullscreen loading="lazy"></iframe>
          </div>
        </div>

        <div class="cc-next">
          <CheckCircleIcon class="cc-next__icon" aria-hidden="true" />
          <div>
            <strong>Cours terminé&nbsp;?</strong>
            <span>Retiens l’essentiel avec la fiche, puis entraîne-toi.</span>
          </div>
          <div class="cc-next__actions">
            <button type="button" class="es-btn es-btn--ghost" @click="$emit('go', 'fiche')">La fiche</button>
            <button type="button" class="es-btn" @click="$emit('go', 'exercices')">
              Les exercices
              <ArrowRightIcon aria-hidden="true" />
            </button>
          </div>
        </div>
      </article>

      <aside v-if="sections.length" class="cc-toc" aria-label="Sommaire du cours">
        <p class="cc-toc__title">Sommaire</p>
        <ol>
          <li v-for="t in sections" :key="t.id">
            <a :href="`#${t.id}`" :class="{ 'is-active': actif === t.id }" @click.prevent="aller(t.id)">
              <span v-if="t.num" class="cc-toc__num">{{ t.num }}</span>
              <span>{{ t.texte }}</span>
            </a>
          </li>
        </ol>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { ArrowDownTrayIcon, ArrowRightIcon, CheckCircleIcon, ListBulletIcon } from '@heroicons/vue/24/outline'
import EspaceDoc from './EspaceDoc.vue'
import TextSize from './TextSize.vue'
import { chargerCours } from '@/utils/chapitreContenu'
import { renderContentWithImages } from '@/utils/scientificRenderer'
import { useTailleTexte } from '@/composables/useTailleTexte'

const props = defineProps({
  notionId: { type: [String, Number], required: true },
  // Onglet affiché (sinon gardé dans la page, masqué).
  actif: { type: Boolean, default: true }
})
defineEmits(['go', 'titre'])

const loading = ref(true)
const cours = ref(null)
const titres = ref([])
const actif = ref('')
const lecture = ref(0)
const tocMobileRef = ref(null)
const articleRef = ref(null)
const docRef = ref(null)
const zoom = useTailleTexte()

const html = computed(() => (cours.value?.contenu ? renderContentWithImages(cours.value.contenu, cours.value.images || []) : ''))
const sections = computed(() => titres.value.filter((t) => t.niveau === 2))

async function charger() {
  loading.value = true
  titres.value = []
  try {
    cours.value = await chargerCours(props.notionId)
  } catch {
    cours.value = null
  } finally {
    loading.value = false
  }
}

let observer = null
function onReady(liste) {
  titres.value = liste
  actif.value = liste.find((t) => t.niveau === 2)?.id || ''
  if (observer) observer.disconnect()
  if (typeof IntersectionObserver === 'undefined') return
  observer = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) actif.value = e.target.id })
  }, { rootMargin: '-140px 0px -65% 0px' })
  liste.filter((t) => t.niveau === 2).forEach((t) => {
    const el = document.getElementById(t.id)
    if (el) observer.observe(el)
  })
  majLecture()
}

async function aller(id, fermer = false) {
  if (fermer && tocMobileRef.value) tocMobileRef.value.open = false
  const cible = document.getElementById(id)
  // Formules calculées jusqu'à la section visée : on arrive sur une page stable.
  await docRef.value?.preparerJusqua(cible)
  requestAnimationFrame(() => {
    cible?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    actif.value = id
  })
}

// Barre de lecture : part de l'article déjà parcourue.
function majLecture() {
  const article = articleRef.value
  if (!article) return
  const r = article.getBoundingClientRect()
  const total = r.height - window.innerHeight * 0.6
  lecture.value = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 0
}

// La barre de lecture ne suit le défilement que lorsque le cours est affiché
// (l'onglet reste dans la page, masqué, quand on passe à la fiche ou aux exercices).
function suivreLecture(affiche) {
  window.removeEventListener('scroll', majLecture)
  if (affiche) {
    window.addEventListener('scroll', majLecture, { passive: true })
    majLecture()
  }
}

onMounted(charger)
watch(() => props.actif, suivreLecture, { immediate: true, flush: 'post' })

watch(() => props.notionId, charger)

onBeforeUnmount(() => {
  suivreLecture(false)
  if (observer) observer.disconnect()
})
</script>

<style scoped>
.cc-progress {
  position: fixed;
  top: var(--es-top);
  right: 0;
  left: var(--es-side);
  z-index: 29;
  height: 3px;
  pointer-events: none;
}

.cc-progress span {
  display: block;
  height: 100%;
  background: var(--es-green);
  transform-origin: left center;
  transition: transform 0.1s linear;
}

.cc-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 248px;
  gap: 28px;
  align-items: start;
}

.cc-article {
  padding: 24px 40px 32px;
}

.cc-toolbar {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 -8px 18px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--es-line);
}

.cc-toolbar__spacer {
  flex: 1;
}

/* Sommaire (ordinateur) */
.cc-toc {
  position: sticky;
  top: calc(var(--es-top) + 84px);
  max-height: calc(100vh - var(--es-top) - 108px);
  padding: 4px 0;
  overflow-y: auto;
}

.cc-toc__title {
  margin-bottom: 10px !important;
  padding-left: 14px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--es-muted);
}

.cc-toc ol {
  margin: 0;
  padding: 0;
  list-style: none;
  border-left: 2px solid var(--es-line);
}

.cc-toc a {
  display: flex;
  gap: 8px;
  margin-left: -2px;
  padding: 7px 10px 7px 12px;
  border-left: 2px solid transparent;
  font-size: 13px;
  font-weight: 500;
  line-height: 1.4;
  color: var(--es-muted);
  text-decoration: none;
}

.cc-toc a:hover {
  color: var(--es-ink);
}

.cc-toc a.is-active {
  border-left-color: var(--es-navy);
  font-weight: 700;
  color: var(--es-navy);
}

.cc-toc__num {
  flex-shrink: 0;
  min-width: 18px;
  font-weight: 700;
  color: var(--es-navy);
}

/* Sommaire (téléphone et tablette) */
.cc-toc-mobile {
  display: none;
  position: relative;
}

.cc-toc-mobile summary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 36px;
  padding: 0 12px;
  border: 1px solid var(--es-line-strong);
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: var(--es-ink);
  list-style: none;
  cursor: pointer;
}

.cc-toc-mobile summary::-webkit-details-marker {
  display: none;
}

.cc-toc-mobile summary svg {
  width: 18px;
  height: 18px;
}

.cc-toc-mobile__count {
  padding: 0 7px;
  border-radius: 999px;
  background: var(--es-bg);
  font-size: 12px;
  color: var(--es-muted);
}

.cc-toc-mobile ol {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  z-index: 20;
  width: min(88vw, 380px);
  max-height: 60vh;
  margin: 0;
  padding: 8px;
  overflow-y: auto;
  border: 1px solid var(--es-line);
  border-radius: 14px;
  background: #fff;
  box-shadow: var(--es-shadow-lg);
  list-style: none;
}

.cc-toc-mobile a {
  display: flex;
  gap: 8px;
  padding: 10px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: var(--es-ink);
  text-decoration: none;
}

.cc-toc-mobile li.is-level-3 a {
  padding-left: 28px;
  font-weight: 500;
  color: var(--es-muted);
}

.cc-toc-mobile a:hover {
  background: var(--es-bg);
}

/* Fin du cours */
.cc-video {
  margin-top: 32px;
}

.cc-video__frame {
  position: relative;
  margin-top: 12px;
  padding-top: 56.25%;
  overflow: hidden;
  border-radius: 12px;
  background: #000;
}

.cc-video__frame iframe {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.cc-next {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-top: 36px;
  padding: 18px 20px;
  border-radius: 14px;
  background: var(--es-green-50);
}

.cc-next__icon {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
  color: var(--es-green-700);
}

.cc-next > div:nth-child(2) {
  display: flex;
  flex: 1;
  flex-direction: column;
  font-size: 14px;
  color: var(--es-ink-soft);
}

.cc-next strong {
  font-size: 16px;
  color: var(--es-ink);
}

.cc-next__actions {
  display: flex;
  gap: 8px;
}

.cc-empty {
  padding: 40px 20px;
}

.cc-empty__actions {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 16px;
}

@media (max-width: 1279px) {
  .cc-layout {
    grid-template-columns: minmax(0, 1fr);
  }

  .cc-toc {
    display: none;
  }

  .cc-toc-mobile {
    display: block;
  }
}

@media (max-width: 1023px) {
  .cc-progress {
    top: 56px;
    left: 0;
  }
}

@media (max-width: 640px) {
  .cc-article {
    margin: 0 -16px;
    padding: 16px 16px 24px;
    border-right: 0;
    border-left: 0;
    border-radius: 0;
    box-shadow: none;
  }

  .cc-toolbar {
    margin: 0 0 14px;
  }

  .cc-hide-sm {
    display: none;
  }

  .cc-next {
    flex-wrap: wrap;
  }

  .cc-next__actions {
    width: 100%;
  }

  .cc-next__actions .es-btn {
    flex: 1;
  }
}
</style>
