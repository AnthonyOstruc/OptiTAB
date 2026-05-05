<template>
  <main class="admin-page">
    <header class="admin-page__head">
      <h1>❓ Questions Arena</h1>
      <div style="display:flex; gap:10px; align-items:center;">
        <select v-model.number="levelId" @change="load">
          <option :value="null">— Choisir un niveau —</option>
          <optgroup v-for="c in chapters" :key="c.id" :label="c.title">
            <option v-for="l in levelsByChapter[c.id] || []" :key="l.id" :value="l.id">
              N{{ l.order }} · {{ l.title }}
            </option>
          </optgroup>
        </select>
        <button class="primary" @click="openCreate" :disabled="!levelId">+ Nouvelle question</button>
      </div>
    </header>

    <table class="admin-table" v-if="levelId">
      <thead><tr><th>#</th><th>Type</th><th>Énoncé</th><th>Poids</th><th></th></tr></thead>
      <tbody>
        <tr v-for="q in questions" :key="q.id">
          <td>{{ q.order }}</td>
          <td>{{ q.type }}</td>
          <td class="prompt-cell">{{ q.prompt }}</td>
          <td>{{ q.weight }}</td>
          <td class="row-actions">
            <button @click="openEdit(q)">Éditer</button>
            <button class="danger" @click="remove(q)">Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else style="color:#94a3b8">Sélectionnez un niveau pour voir ses questions.</p>

    <div v-if="modalOpen" class="modal-overlay" @click.self="modalOpen=false">
      <div class="modal">
        <h2>{{ editing.id ? 'Éditer la question' : 'Nouvelle question' }}</h2>
        <label>Niveau
          <select v-model.number="editing.level">
            <optgroup v-for="c in chapters" :key="c.id" :label="c.title">
              <option v-for="l in levelsByChapter[c.id] || []" :key="l.id" :value="l.id">
                N{{ l.order }} · {{ l.title }}
              </option>
            </optgroup>
          </select>
        </label>
        <label>Ordre <input type="number" v-model.number="editing.order" /></label>
        <label>Type
          <select v-model="editing.type">
            <option value="mcq">MCQ</option>
            <option value="numeric">Numérique</option>
          </select>
        </label>
        <label>Énoncé (LaTeX entre $...$) <textarea v-model="editing.prompt" /></label>
        <template v-if="editing.type === 'mcq'">
          <label>Choix (un par ligne)
            <textarea v-model="choicesText" />
          </label>
          <label>Index corrects (séparés par des virgules, ex: 0,2)
            <input v-model="correctText" />
          </label>
        </template>
        <template v-else>
          <label>Valeur attendue <input v-model="numericValue" /></label>
          <label>Tolérance <input v-model="numericTolerance" /></label>
        </template>
        <label>Indice (premium) <textarea v-model="editing.hint" /></label>
        <label>Solution détaillée <textarea v-model="editing.explanation" /></label>
        <label>Poids <input type="number" v-model.number="editing.weight" /></label>
        <div class="modal__actions">
          <button @click="modalOpen=false">Annuler</button>
          <button class="primary" @click="save">Enregistrer</button>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import {
  adminListArenaChapters,
  adminListArenaLevels,
  adminListArenaQuestions,
  adminCreateArenaQuestion,
  adminUpdateArenaQuestion,
  adminDeleteArenaQuestion,
} from '@/api/arena'

const chapters = ref([])
const levelsAll = ref([])
const questions = ref([])
const levelId = ref(null)
const modalOpen = ref(false)
const editing = ref(blank())
const choicesText = ref('')
const correctText = ref('')
const numericValue = ref('')
const numericTolerance = ref('0')

const levelsByChapter = computed(() => {
  const map = {}
  for (const l of levelsAll.value) {
    if (!map[l.chapter]) map[l.chapter] = []
    map[l.chapter].push(l)
  }
  for (const id of Object.keys(map)) map[id].sort((a, b) => a.order - b.order)
  return map
})

function blank() {
  return {
    id: null, level: levelId.value, order: 1, type: 'mcq', prompt: '',
    choices: [], correct: [], hint: '', explanation: '', weight: 1,
  }
}

async function loadStructure() {
  const [{ data: cs }, { data: ls }] = await Promise.all([
    adminListArenaChapters(),
    adminListArenaLevels(),
  ])
  chapters.value = Array.isArray(cs) ? cs : (cs?.results || [])
  levelsAll.value = Array.isArray(ls) ? ls : (ls?.results || [])
}

async function load() {
  if (!levelId.value) { questions.value = []; return }
  const { data } = await adminListArenaQuestions(levelId.value)
  questions.value = Array.isArray(data) ? data : (data?.results || [])
}

onMounted(async () => { await loadStructure() })

function openCreate() {
  editing.value = blank()
  choicesText.value = ''
  correctText.value = ''
  numericValue.value = ''
  numericTolerance.value = '0'
  modalOpen.value = true
}

function openEdit(q) {
  editing.value = { ...q }
  if (q.type === 'mcq') {
    choicesText.value = (q.choices || []).join('\n')
    correctText.value = (q.correct || []).join(',')
  } else {
    numericValue.value = String(q.correct?.value ?? '')
    numericTolerance.value = String(q.correct?.tolerance ?? 0)
  }
  modalOpen.value = true
}

function preparePayload() {
  const payload = { ...editing.value }
  if (payload.type === 'mcq') {
    payload.choices = choicesText.value.split('\n').map((s) => s.trim()).filter(Boolean)
    payload.correct = correctText.value.split(',').map((s) => parseInt(s.trim(), 10)).filter(Number.isInteger)
  } else {
    payload.choices = []
    payload.correct = {
      value: Number(numericValue.value),
      tolerance: Number(numericTolerance.value) || 0,
    }
  }
  return payload
}

async function save() {
  const payload = preparePayload()
  if (payload.id) {
    await adminUpdateArenaQuestion(payload.id, payload)
  } else {
    await adminCreateArenaQuestion(payload)
  }
  modalOpen.value = false
  await load()
}

async function remove(q) {
  if (!confirm('Supprimer cette question ?')) return
  await adminDeleteArenaQuestion(q.id)
  await load()
}
</script>

<style scoped>
@import './arenaAdmin.css';
.prompt-cell { max-width: 480px; white-space: nowrap; text-overflow: ellipsis; overflow: hidden; }
</style>
