<template>
  <main class="admin-page">
    <header class="admin-page__head">
      <h1>🏷 Niveaux Arena</h1>
      <div style="display:flex; gap: 10px; align-items:center;">
        <select v-model="chapterId" @change="load">
          <option :value="null">— Tous les chapitres —</option>
          <option v-for="c in chapters" :key="c.id" :value="c.id">{{ c.title }}</option>
        </select>
        <button class="primary" @click="openCreate" :disabled="!chapterId">+ Nouveau niveau</button>
      </div>
    </header>

    <table class="admin-table">
      <thead>
        <tr><th>Chapitre</th><th>#</th><th>Titre</th><th>Difficulté</th><th>Premium</th><th>Temps</th><th>XP</th><th></th></tr>
      </thead>
      <tbody>
        <tr v-for="l in levels" :key="l.id">
          <td>{{ chapterTitle(l.chapter) }}</td>
          <td>{{ l.order }}</td>
          <td>{{ l.title }}</td>
          <td>{{ l.difficulty }}</td>
          <td>{{ l.is_premium ? '✓' : '—' }}</td>
          <td>{{ l.time_limit_sec }}s</td>
          <td>{{ l.xp_reward }}</td>
          <td class="row-actions">
            <button @click="openEdit(l)">Éditer</button>
            <button class="danger" @click="remove(l)">Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="modalOpen" class="modal-overlay" @click.self="modalOpen=false">
      <div class="modal">
        <h2>{{ editing.id ? 'Éditer le niveau' : 'Nouveau niveau' }}</h2>
        <label>Chapitre
          <select v-model.number="editing.chapter">
            <option v-for="c in chapters" :key="c.id" :value="c.id">{{ c.title }}</option>
          </select>
        </label>
        <label>Titre <input v-model="editing.title" /></label>
        <label>Ordre <input type="number" v-model.number="editing.order" /></label>
        <label>Difficulté
          <select v-model="editing.difficulty">
            <option value="easy">Facile</option>
            <option value="medium">Moyen</option>
            <option value="hard">Difficile</option>
            <option value="elite">Élite (premium)</option>
          </select>
        </label>
        <label>Temps limite (sec) <input type="number" v-model.number="editing.time_limit_sec" /></label>
        <label>XP récompense <input type="number" v-model.number="editing.xp_reward" /></label>
        <label>Seuil de réussite (%) <input type="number" v-model.number="editing.pass_threshold" /></label>
        <label class="check"><input type="checkbox" v-model="editing.is_premium" /> Niveau premium</label>
        <label class="check"><input type="checkbox" v-model="editing.is_active" /> Actif</label>
        <div class="modal__actions">
          <button @click="modalOpen=false">Annuler</button>
          <button class="primary" @click="save">Enregistrer</button>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import {
  adminListArenaChapters,
  adminListArenaLevels,
  adminCreateArenaLevel,
  adminUpdateArenaLevel,
  adminDeleteArenaLevel,
} from '@/api/arena'

const chapters = ref([])
const levels = ref([])
const chapterId = ref(null)
const modalOpen = ref(false)
const editing = ref(blank())

function blank() {
  return {
    id: null, chapter: chapterId.value, title: '', order: 1,
    difficulty: 'easy', time_limit_sec: 90, xp_reward: 20,
    pass_threshold: 60, is_premium: false, is_active: true,
  }
}

function chapterTitle(id) {
  return chapters.value.find((c) => c.id === id)?.title || ''
}

async function loadChapters() {
  const { data } = await adminListArenaChapters()
  chapters.value = Array.isArray(data) ? data : (data?.results || [])
}

async function load() {
  const { data } = await adminListArenaLevels(chapterId.value)
  levels.value = Array.isArray(data) ? data : (data?.results || [])
}

onMounted(async () => {
  await loadChapters()
  await load()
})

function openCreate() { editing.value = blank(); modalOpen.value = true }
function openEdit(l) { editing.value = { ...l }; modalOpen.value = true }

async function save() {
  if (!editing.value.chapter) {
    alert('Sélectionnez un chapitre.')
    return
  }
  if (editing.value.id) {
    await adminUpdateArenaLevel(editing.value.id, editing.value)
  } else {
    await adminCreateArenaLevel(editing.value)
  }
  modalOpen.value = false
  await load()
}

async function remove(l) {
  if (!confirm(`Supprimer "${l.title}" ?`)) return
  await adminDeleteArenaLevel(l.id)
  await load()
}
</script>

<style scoped>@import './arenaAdmin.css';</style>
