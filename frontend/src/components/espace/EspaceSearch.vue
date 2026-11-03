<template>
  <div ref="rootRef" class="sr" @keydown="clavier">
    <label class="sr__field">
      <MagnifyingGlassIcon class="sr__icon" aria-hidden="true" />
      <span class="es-sr-only">Rechercher un chapitre</span>
      <input
        ref="inputRef"
        v-model="q"
        type="search"
        role="combobox"
        aria-autocomplete="list"
        :aria-expanded="ouvert"
        aria-controls="sr-list"
        placeholder="Rechercher un chapitre…"
        autocomplete="off"
        @focus="ouvrir"
      />
      <kbd class="sr__kbd" aria-hidden="true">Ctrl K</kbd>
    </label>

    <div v-if="ouvert" class="sr__panel">
      <p class="sr__label">{{ q.trim() ? 'Chapitres' : 'Récemment travaillés' }}</p>
      <ul v-if="resultats.length" id="sr-list" role="listbox">
        <li v-for="(c, i) in resultats" :key="c.id" role="option" :aria-selected="i === actif">
          <router-link
            :to="chapitreLink(c.id)"
            :class="['sr__item', { 'is-active': i === actif }]"
            @mouseenter="actif = i"
            @click="fermer"
          >
            <span class="es-theme-ico es-theme-ico--sm" :style="c.visuel.style">
              <component :is="c.visuel.icone" aria-hidden="true" />
            </span>
            <span class="sr__text">
              <strong>{{ c.titre }}</strong>
              <span>{{ c.theme }}</span>
            </span>
            <span v-if="c.exercices" class="sr__count">{{ c.acquis }}/{{ c.exercices }}</span>
          </router-link>
        </li>
      </ul>
      <p v-else class="sr__empty">Aucun chapitre ne correspond à « {{ q }} ».</p>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { MagnifyingGlassIcon } from '@heroicons/vue/24/outline'
import { useProgression } from '@/composables/useProgression'
import { chapitreLink } from '@/config/espace'
import { indexThemes, visuelTheme } from '@/utils/espaceTheme'

const router = useRouter()
const { progression, charger } = useProgression()

const rootRef = ref(null)
const inputRef = ref(null)
const q = ref('')
const ouvert = ref(false)
const actif = ref(0)

const normaliser = (s) => String(s || '').normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase()

const resultats = computed(() => {
  const chapitres = progression.value?.chapitres || []
  const themes = indexThemes(chapitres)
  const recherche = normaliser(q.value.trim())
  let liste
  if (recherche) {
    const mots = recherche.split(/\s+/)
    liste = chapitres.filter((c) => {
      const texte = normaliser(`${c.titre} ${c.theme}`)
      return mots.every((m) => texte.includes(m))
    })
  } else {
    const recents = chapitres.filter((c) => c.faits > 0)
      .sort((a, b) => String(b.derniere_activite || '').localeCompare(String(a.derniere_activite || '')))
    liste = recents.length ? recents : chapitres
  }
  return liste.slice(0, 7).map((c) => ({ ...c, visuel: visuelTheme(c.theme, themes.get(c.theme_id)) }))
})

watch(q, () => { actif.value = 0 })

function ouvrir() {
  ouvert.value = true
  charger()
}

function fermer() {
  ouvert.value = false
  q.value = ''
  inputRef.value?.blur()
}

function clavier(e) {
  if (!ouvert.value) return
  if (e.key === 'ArrowDown') {
    e.preventDefault()
    actif.value = Math.min(resultats.value.length - 1, actif.value + 1)
  } else if (e.key === 'ArrowUp') {
    e.preventDefault()
    actif.value = Math.max(0, actif.value - 1)
  } else if (e.key === 'Enter') {
    const c = resultats.value[actif.value]
    if (c) {
      e.preventDefault()
      router.push(chapitreLink(c.id))
      fermer()
    }
  } else if (e.key === 'Escape') {
    fermer()
  }
}

function clicDehors(e) {
  if (ouvert.value && rootRef.value && !rootRef.value.contains(e.target)) ouvert.value = false
}

function raccourci(e) {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault()
    inputRef.value?.focus()
  }
}

onMounted(() => {
  document.addEventListener('mousedown', clicDehors)
  document.addEventListener('keydown', raccourci)
})

onBeforeUnmount(() => {
  document.removeEventListener('mousedown', clicDehors)
  document.removeEventListener('keydown', raccourci)
})
</script>

<style scoped>
.sr {
  position: relative;
  width: min(420px, 100%);
}

.sr__field {
  position: relative;
  display: flex;
  align-items: center;
}

.sr__icon {
  position: absolute;
  left: 12px;
  width: 18px;
  height: 18px;
  color: var(--es-muted);
  pointer-events: none;
}

.sr__field input {
  width: 100%;
  height: 40px;
  padding: 0 64px 0 38px;
  border: 1px solid var(--es-line);
  border-radius: 12px;
  background: var(--es-bg);
  font: 500 15px var(--es-font) !important;
  color: var(--es-ink);
  transition: border-color 0.15s ease, background-color 0.15s ease, box-shadow 0.15s ease;
}

.sr__field input::placeholder {
  color: #8a93a6;
}

.sr__field input:focus {
  border-color: var(--es-navy);
  background: #fff;
  outline: none;
  box-shadow: 0 0 0 3px rgba(27, 60, 142, 0.12);
}

.sr__field input::-webkit-search-cancel-button {
  display: none;
}

.sr__kbd {
  position: absolute;
  right: 10px;
  padding: 2px 6px;
  border: 1px solid var(--es-line-strong);
  border-radius: 6px;
  background: #fff;
  font: 600 11px var(--es-font);
  color: var(--es-muted);
}

.sr__panel {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  width: max(100%, 440px);
  padding: 8px;
  border: 1px solid var(--es-line);
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 20px 48px rgba(16, 24, 40, 0.16);
}

.sr__label {
  padding: 6px 10px 8px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--es-muted);
}

.sr__panel ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

.sr__item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 10px;
  border-radius: 10px;
  text-decoration: none;
}

.sr__item.is-active {
  background: var(--es-bg);
}

.sr__text {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
  font-size: 12px;
  color: var(--es-muted);
}

.sr__text strong {
  overflow: hidden;
  font-size: 14px;
  font-weight: 600;
  color: var(--es-ink);
  white-space: nowrap;
  text-overflow: ellipsis;
}

.sr__count {
  font-size: 12px;
  font-weight: 700;
  color: var(--es-muted);
}

.sr__empty {
  padding: 14px 10px;
  font-size: 14px;
  color: var(--es-muted);
}
</style>
