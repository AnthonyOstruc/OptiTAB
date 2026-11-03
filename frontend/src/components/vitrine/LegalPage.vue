<template>
  <VitrineLayout>
    <header class="lg-hero">
      <div class="lg-hero__grid" aria-hidden="true"></div>
      <div class="vt-container lg-hero__inner">
        <nav ref="docsRef" class="lg-docs" aria-label="Documents légaux">
          <router-link
            v-for="doc in legalDocs"
            :key="doc.lien"
            :to="doc.lien"
            :class="['lg-docs__link', { 'is-active': route.path === doc.lien }]"
            :aria-current="route.path === doc.lien ? 'page' : null"
          >
            {{ doc.court }}
          </router-link>
        </nav>

        <p class="vt-kicker lg-hero__kicker">Informations légales</p>
        <h1 class="lg-hero__title">{{ title }}</h1>
        <p class="lg-hero__intro">{{ intro }}</p>
        <p class="lg-hero__meta">
          <span><CalendarDaysIcon aria-hidden="true" />Mis à jour le {{ updated }}</span>
          <span v-if="readingTime"><ClockIcon aria-hidden="true" />{{ readingTime }} min de lecture</span>
        </p>
      </div>
    </header>

    <div class="vt-container lg-body">
      <!-- Sommaire : colonne fixe sur ordinateur, menu repliable sur téléphone. -->
      <aside v-if="toc.length" class="lg-toc" aria-label="Sommaire">
        <details class="lg-toc__box" :open="tocOpen" @toggle="tocOpen = $event.target.open">
          <summary class="lg-toc__summary">
            <span>Sommaire</span>
            <span class="lg-toc__count">{{ toc.length }} rubriques</span>
            <ChevronDownIcon class="lg-toc__chevron" aria-hidden="true" />
          </summary>
          <ol class="lg-toc__list">
            <li v-for="(item, i) in toc" :key="item.id">
              <a
                :href="`#${item.id}`"
                :class="['lg-toc__link', { 'is-active': activeId === item.id }]"
                :aria-current="activeId === item.id ? 'true' : null"
                @click.prevent="goTo(item.id)"
              >
                <span class="lg-toc__num">{{ i + 1 }}</span>
                <span>{{ item.title }}</span>
              </a>
            </li>
          </ol>
        </details>
      </aside>

      <div class="lg-main">
        <div v-if="$slots.essentiel" class="lg-essentiel">
          <p class="lg-essentiel__title"><SparklesIcon aria-hidden="true" />L’essentiel en bref</p>
          <slot name="essentiel" />
        </div>

        <article ref="docRef" class="lg-doc">
          <slot />
        </article>

        <aside class="lg-contact" aria-label="Contact">
          <div>
            <p class="lg-contact__title">Une question sur ce document&nbsp;?</p>
            <p class="lg-contact__text">Écris-nous, on te répond sous 24&nbsp;h, 7&nbsp;jours sur&nbsp;7.</p>
          </div>
          <div class="lg-contact__actions">
            <a :href="`mailto:${legalInfo.email}`" class="vt-btn vt-btn--primary vt-btn--sm">
              <EnvelopeIcon aria-hidden="true" />
              {{ legalInfo.email }}
            </a>
            <a
              :href="`https://wa.me/${legalInfo.whatsapp}`"
              target="_blank"
              rel="noopener noreferrer"
              class="vt-btn vt-btn--ghost vt-btn--sm"
              data-cta-name="whatsapp"
              data-cta-location="legal"
            >
              WhatsApp · {{ legalInfo.whatsappAffiche }}
            </a>
          </div>
        </aside>
      </div>
    </div>
  </VitrineLayout>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { CalendarDaysIcon, ClockIcon, ChevronDownIcon, EnvelopeIcon, SparklesIcon } from '@heroicons/vue/24/outline'
import VitrineLayout from './VitrineLayout.vue'
import { legalInfo, legalDocs } from '@/config/legalInfo'

defineProps({
  title: { type: String, required: true },
  intro: { type: String, default: '' },
  updated: { type: String, required: true }
})

const route = useRoute()
const docRef = ref(null)
const docsRef = ref(null)
const toc = ref([])
const activeId = ref('')
const readingTime = ref(0)
const tocOpen = ref(true)
let observer = null

const isMobile = () => window.matchMedia('(max-width: 1023px)').matches

const goTo = async (id) => {
  const target = document.getElementById(id)
  if (!target) return
  activeId.value = id
  // Sur téléphone, le sommaire se referme d'abord : sa hauteur ne doit pas fausser
  // la position de la rubrique visée.
  if (isMobile() && tocOpen.value) {
    tocOpen.value = false
    await nextTick()
    await new Promise((resolve) => requestAnimationFrame(resolve))
  }
  target.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

// Le sommaire est construit à partir des sections du document : chaque
// <section id="…"> dont le premier titre <h2> donne l'intitulé.
const buildToc = () => {
  const sections = [...(docRef.value?.querySelectorAll(':scope > section[id]') || [])]
  toc.value = sections.map((section) => ({
    id: section.id,
    title: section.querySelector('h2')?.textContent.trim() || section.id
  }))
  const words = (docRef.value?.innerText || '').split(/\s+/).filter(Boolean).length
  readingTime.value = Math.max(1, Math.round(words / 220))
  return sections
}

// Sur téléphone, la rangée des documents défile : on y amène le document affiché.
const revealActiveDoc = () => {
  const nav = docsRef.value
  const active = nav?.querySelector('.is-active')
  if (!nav || !active || nav.scrollWidth <= nav.clientWidth) return
  const navBox = nav.getBoundingClientRect()
  const activeBox = active.getBoundingClientRect()
  nav.scrollLeft += activeBox.left - navBox.left - (navBox.width - activeBox.width) / 2
}

onMounted(async () => {
  tocOpen.value = !isMobile()
  await nextTick()
  revealActiveDoc()
  // La largeur des boutons change quand la police est chargée : on recadre.
  document.fonts?.ready.then(revealActiveDoc)
  const sections = buildToc()
  if (!('IntersectionObserver' in window) || !sections.length) return
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) activeId.value = entry.target.id
      })
    },
    { rootMargin: '-96px 0px -70% 0px' }
  )
  sections.forEach((section) => observer.observe(section))
})

onBeforeUnmount(() => {
  observer?.disconnect()
  observer = null
})
</script>

<style scoped>
/* ---------- En-tête du document ---------- */

.lg-hero {
  position: relative;
  overflow: hidden;
  padding: 40px 0 44px;
  border-bottom: 1px solid var(--vt-line);
  background:
    radial-gradient(700px 320px at 90% 0%, rgba(95, 172, 96, 0.1), transparent 60%),
    linear-gradient(180deg, #fbfcfe 0%, #f3f6fc 100%);
}

.lg-hero__grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(27, 60, 142, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(27, 60, 142, 0.05) 1px, transparent 1px);
  background-size: 28px 28px;
  -webkit-mask-image: radial-gradient(ellipse 60% 90% at 80% 30%, #000 10%, transparent 70%);
  mask-image: radial-gradient(ellipse 60% 90% at 80% 30%, #000 10%, transparent 70%);
  pointer-events: none;
}

.lg-hero__inner {
  position: relative;
}

.lg-docs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 32px;
}

.lg-docs__link {
  padding: 7px 14px;
  border: 1px solid var(--vt-line-strong);
  border-radius: 999px;
  background: #fff;
  font-size: 14px;
  font-weight: 600;
  color: var(--vt-ink-soft);
  text-decoration: none;
  white-space: nowrap;
  transition: border-color 0.15s ease, color 0.15s ease, background-color 0.15s ease;
}

.lg-docs__link:hover {
  border-color: var(--vt-navy);
  color: var(--vt-navy);
}

.lg-docs__link.is-active {
  border-color: var(--vt-navy);
  background: var(--vt-navy);
  color: #fff;
}

.lg-hero__kicker {
  margin-bottom: 10px;
}

.lg-hero__title {
  max-width: 820px;
  font-size: clamp(32px, 4.2vw, 48px);
}

.lg-hero__intro {
  max-width: 720px;
  margin: 16px 0 0;
  font-size: 18px;
  line-height: 1.65;
  color: var(--vt-muted);
}

.lg-hero__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 20px;
  margin: 22px 0 0;
  font-size: 14px;
  font-weight: 600;
  color: var(--vt-ink-soft);
}

.lg-hero__meta span {
  display: inline-flex;
  align-items: center;
  gap: 7px;
}

.lg-hero__meta svg {
  width: 18px;
  height: 18px;
  color: var(--vt-green-700);
}

/* ---------- Corps : sommaire + texte ---------- */

.lg-body {
  display: grid;
  grid-template-columns: 260px minmax(0, 1fr);
  gap: 56px;
  align-items: start;
  padding-top: 48px;
  padding-bottom: 96px;
}

.lg-main {
  min-width: 0;
  max-width: 780px;
}

.lg-toc {
  position: sticky;
  top: 96px;
  max-height: calc(100vh - 120px);
  overflow-y: auto;
  overscroll-behavior: contain;
  scrollbar-width: thin;
}

.lg-toc__box {
  border: 1px solid var(--vt-line);
  border-radius: var(--vt-radius);
  background: #fff;
}

.lg-toc__summary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 16px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--vt-muted);
  cursor: default;
  list-style: none;
  pointer-events: none;
}

.lg-toc__summary::-webkit-details-marker {
  display: none;
}

.lg-toc__count,
.lg-toc__chevron {
  display: none;
}

.lg-toc__list {
  margin: 0;
  padding: 0 8px 10px;
  list-style: none;
}

.lg-toc__link {
  display: grid;
  grid-template-columns: 24px minmax(0, 1fr);
  gap: 8px;
  align-items: baseline;
  padding: 7px 8px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  line-height: 1.4;
  color: var(--vt-ink-soft);
  text-decoration: none;
  transition: background-color 0.15s ease, color 0.15s ease;
}

.lg-toc__link:hover {
  background: var(--vt-navy-50);
  color: var(--vt-navy);
}

.lg-toc__link.is-active {
  background: var(--vt-navy-50);
  color: var(--vt-navy);
}

.lg-toc__num {
  font-size: 12px;
  font-weight: 700;
  color: var(--vt-muted);
}

.lg-toc__link.is-active .lg-toc__num {
  color: var(--vt-green-700);
}

/* ---------- L'essentiel en bref ---------- */

.lg-essentiel {
  margin-bottom: 40px;
  padding: 22px 24px;
  border: 1px solid var(--vt-navy-100);
  border-radius: var(--vt-radius);
  background: var(--vt-navy-50);
}

.lg-essentiel__title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 12px;
  font-size: 15px;
  font-weight: 700;
  color: var(--vt-navy);
}

.lg-essentiel__title svg {
  width: 20px;
  height: 20px;
}

.lg-essentiel :deep(ul) {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.lg-essentiel :deep(li) {
  position: relative;
  padding-left: 26px;
  font-size: 15px;
  line-height: 1.6;
  color: var(--vt-ink-soft);
}

.lg-essentiel :deep(li)::before {
  content: '';
  position: absolute;
  left: 2px;
  top: 0.35em;
  width: 14px;
  height: 8px;
  border-left: 2.5px solid var(--vt-green-700);
  border-bottom: 2.5px solid var(--vt-green-700);
  transform: rotate(-45deg);
}

/* ---------- Texte du document ---------- */

.lg-doc {
  counter-reset: lg-section;
}

.lg-doc > :deep(section) {
  counter-increment: lg-section;
  padding-bottom: 32px;
  margin-bottom: 32px;
  border-bottom: 1px solid var(--vt-line);
  scroll-margin-top: 96px;
}

.lg-doc > :deep(section:last-child) {
  margin-bottom: 0;
  border-bottom: 0;
}

/* Numérotation automatique des rubriques. */
.lg-doc :deep(h2) {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  margin: 0 0 18px;
  font-size: 23px;
  line-height: 1.3;
}

.lg-doc :deep(h2)::before {
  content: counter(lg-section);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 34px;
  height: 34px;
  margin-top: -2px;
  border-radius: 10px;
  background: var(--vt-navy);
  color: #fff;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0;
}

.lg-doc :deep(h3) {
  margin: 26px 0 10px;
  font-size: 17px;
  line-height: 1.4;
}

.lg-doc :deep(p) {
  margin: 0 0 14px;
  font-size: 16px;
  line-height: 1.75;
  color: var(--vt-ink-soft);
}

.lg-doc :deep(ul) {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 0 0 16px;
  padding: 0;
  list-style: none;
}

.lg-doc :deep(ul > li) {
  position: relative;
  padding-left: 22px;
  font-size: 16px;
  line-height: 1.7;
  color: var(--vt-ink-soft);
}

.lg-doc :deep(ul > li)::before {
  content: '';
  position: absolute;
  left: 4px;
  top: 0.72em;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--vt-green);
}

.lg-doc :deep(strong) {
  color: var(--vt-ink);
}

.lg-doc :deep(a:not(.vt-btn)) {
  color: var(--vt-navy);
  font-weight: 600;
  text-decoration: underline;
  text-decoration-color: rgba(27, 60, 142, 0.35);
  text-underline-offset: 3px;
  overflow-wrap: anywhere;
}

.lg-doc :deep(a:not(.vt-btn):hover) {
  text-decoration-color: currentColor;
}

/* Fiche d'identité (éditeur, hébergeur…) : intitulé à gauche, valeur à droite. */
.lg-doc :deep(.lg-card) {
  margin: 0 0 16px;
  padding: 6px 20px;
  border: 1px solid var(--vt-line);
  border-radius: 14px;
  background: var(--vt-bg-soft);
}

.lg-doc :deep(.lg-card__title) {
  margin: 14px 0 4px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--vt-green-700);
}

.lg-doc :deep(.lg-facts) {
  display: grid;
  grid-template-columns: 180px minmax(0, 1fr);
  margin: 0;
}

.lg-doc :deep(.lg-facts dt),
.lg-doc :deep(.lg-facts dd) {
  margin: 0;
  padding: 11px 0;
  border-top: 1px solid var(--vt-line);
  font-size: 15px;
  line-height: 1.55;
}

.lg-doc :deep(.lg-facts dt:first-of-type),
.lg-doc :deep(.lg-facts dt:first-of-type + dd) {
  border-top: 0;
}

.lg-doc :deep(.lg-facts dt) {
  font-weight: 600;
  color: var(--vt-muted);
}

.lg-doc :deep(.lg-facts dd) {
  color: var(--vt-ink);
}

/* Encadré d'information. */
.lg-doc :deep(.lg-note) {
  margin: 4px 0 16px;
  padding: 14px 18px;
  border-left: 3px solid var(--vt-green);
  border-radius: 0 12px 12px 0;
  background: var(--vt-green-50);
  font-size: 15px;
  line-height: 1.65;
  color: var(--vt-ink-soft);
}

/* Tableaux : défilement horizontal sur petit écran plutôt qu'un débordement. */
.lg-doc :deep(.lg-table-wrap) {
  margin: 0 0 18px;
  overflow-x: auto;
  border: 1px solid var(--vt-line);
  border-radius: 14px;
  -webkit-overflow-scrolling: touch;
}

.lg-doc :deep(.lg-table) {
  width: 100%;
  border-collapse: collapse;
  font-size: 15px;
  line-height: 1.5;
}

.lg-doc :deep(.lg-table th),
.lg-doc :deep(.lg-table td) {
  padding: 12px 16px;
  border-top: 1px solid var(--vt-line);
  text-align: left;
  vertical-align: top;
  color: var(--vt-ink-soft);
}

.lg-doc :deep(.lg-table thead th) {
  border-top: 0;
  background: var(--vt-navy-50);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--vt-navy);
  white-space: nowrap;
}

.lg-doc :deep(.lg-table tbody th) {
  font-weight: 700;
  color: var(--vt-ink);
}

.lg-doc :deep(.lg-tag) {
  display: inline-block;
  padding: 2px 9px;
  border-radius: 999px;
  background: var(--vt-navy-50);
  font-size: 12px;
  font-weight: 700;
  color: var(--vt-navy);
  white-space: nowrap;
}

.lg-doc :deep(.lg-tag--vert) {
  background: var(--vt-green-50);
  color: var(--vt-green-700);
}

.lg-doc :deep(.lg-tag--orange) {
  background: var(--vt-orange-50);
  color: var(--vt-orange-700);
}

.lg-doc :deep(.lg-button) {
  margin: 4px 0 18px;
}

/* ---------- Contact ---------- */

.lg-contact {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 18px 28px;
  margin-top: 48px;
  padding: 24px 26px;
  border: 1px solid var(--vt-line);
  border-radius: var(--vt-radius);
  background: var(--vt-bg-soft);
}

.lg-contact__title {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: var(--vt-ink);
}

.lg-contact__text {
  margin: 4px 0 0;
  font-size: 15px;
  color: var(--vt-muted);
}

.lg-contact__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

/* ---------- Tablette et téléphone ---------- */

@media (max-width: 1023px) {
  .lg-body {
    grid-template-columns: minmax(0, 1fr);
    gap: 24px;
    padding-top: 28px;
  }

  .lg-main {
    max-width: none;
  }

  .lg-toc {
    position: static;
    max-height: none;
    overflow: visible;
  }

  .lg-toc__summary {
    padding: 16px 18px;
    font-size: 15px;
    letter-spacing: 0;
    text-transform: none;
    color: var(--vt-ink);
    cursor: pointer;
    pointer-events: auto;
  }

  .lg-toc__count {
    display: inline;
    margin-left: auto;
    font-size: 13px;
    font-weight: 600;
    color: var(--vt-muted);
  }

  .lg-toc__chevron {
    display: block;
    width: 18px;
    height: 18px;
    color: var(--vt-muted);
    transition: transform 0.2s ease;
  }

  .lg-toc__box[open] .lg-toc__chevron {
    transform: rotate(180deg);
  }

  .lg-toc__box[open] .lg-toc__summary {
    border-bottom: 1px solid var(--vt-line);
  }

  .lg-toc__list {
    padding-top: 8px;
  }

  .lg-toc__link {
    padding: 10px 10px;
    font-size: 15px;
  }
}

@media (max-width: 640px) {
  .lg-hero {
    padding: 28px 0 32px;
  }

  /* Les liens vers les autres documents défilent sur une seule ligne. */
  .lg-docs {
    flex-wrap: nowrap;
    margin: 0 calc(-1 * var(--vt-gutter)) 24px;
    padding: 0 var(--vt-gutter) 4px;
    overflow-x: auto;
    scrollbar-width: none;
  }

  .lg-docs::-webkit-scrollbar {
    display: none;
  }

  .lg-hero__intro {
    font-size: 16px;
  }

  .lg-body {
    padding-bottom: 64px;
  }

  .lg-essentiel {
    margin-bottom: 32px;
    padding: 18px;
  }

  .lg-doc :deep(h2) {
    gap: 12px;
    font-size: 20px;
  }

  .lg-doc :deep(h2)::before {
    width: 30px;
    height: 30px;
    font-size: 14px;
  }

  .lg-doc > :deep(section) {
    padding-bottom: 24px;
    margin-bottom: 24px;
  }

  .lg-doc :deep(p),
  .lg-doc :deep(ul > li) {
    font-size: 15px;
  }

  .lg-doc :deep(.lg-card) {
    padding: 4px 16px;
  }

  .lg-doc :deep(.lg-facts) {
    grid-template-columns: minmax(0, 1fr);
  }

  .lg-doc :deep(.lg-facts dt) {
    padding-bottom: 0;
    font-size: 13px;
  }

  .lg-doc :deep(.lg-facts dd) {
    padding-top: 2px;
    border-top: 0;
  }

  /* Tableaux à plusieurs colonnes : une fiche par ligne, chaque valeur précédée de
     son intitulé (attribut data-label). */
  .lg-doc :deep(.lg-table--cards thead) {
    display: none;
  }

  .lg-doc :deep(.lg-table--cards tr) {
    display: block;
    padding: 14px 16px;
    border-top: 1px solid var(--vt-line);
  }

  .lg-doc :deep(.lg-table--cards tbody tr:first-child) {
    border-top: 0;
  }

  .lg-doc :deep(.lg-table--cards th),
  .lg-doc :deep(.lg-table--cards td) {
    display: block;
    padding: 0;
    border: 0;
  }

  .lg-doc :deep(.lg-table--cards tbody th) {
    margin-bottom: 8px;
    font-size: 16px;
    overflow-wrap: anywhere;
  }

  .lg-doc :deep(.lg-table--cards td) {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 16px;
    padding: 4px 0;
    text-align: right;
  }

  .lg-doc :deep(.lg-table--cards td)::before {
    content: attr(data-label);
    flex-shrink: 0;
    font-size: 13px;
    font-weight: 600;
    color: var(--vt-muted);
    text-align: left;
  }

  .lg-contact {
    padding: 20px 18px;
  }

  .lg-contact__actions,
  .lg-contact__actions .vt-btn {
    width: 100%;
  }
}
</style>
