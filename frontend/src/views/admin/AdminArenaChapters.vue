<template>
  <main class="admin-page">
    <header class="admin-page__head">
      <h1>📘 Chapitres Arena</h1>
      <button class="primary" @click="openCreate">+ Nouveau chapitre</button>
    </header>

    <table class="admin-table">
      <thead>
        <tr><th>Ordre</th><th>Titre</th><th>Slug</th><th>Premium</th><th>Actif</th><th></th></tr>
      </thead>
      <tbody>
        <tr v-for="c in chapters" :key="c.id">
          <td>{{ c.order }}</td>
          <td>{{ c.title }}</td>
          <td>{{ c.slug }}</td>
          <td>{{ c.is_premium ? '✓' : '—' }}</td>
          <td>{{ c.is_active ? '✓' : '—' }}</td>
          <td class="row-actions">
            <button @click="openEdit(c)">Éditer</button>
            <button class="danger" @click="remove(c)">Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="modalOpen" class="modal-overlay" @click.self="modalOpen = false">
      <div class="modal">
        <h2>{{ editing.id ? 'Éditer le chapitre' : 'Nouveau chapitre' }}</h2>
        <label>Titre <input v-model="editing.title" /></label>
        <label>Slug <input v-model="editing.slug" /></label>
        <label>Description <textarea v-model="editing.description" /></label>
        <label>Icône (emoji) <input v-model="editing.icon" /></label>
        <label>Couleur <input v-model="editing.color" type="color" /></label>
        <label>Ordre <input v-model.number="editing.order" type="number" /></label>
        <label class="check"><input type="checkbox" v-model="editing.is_premium" /> Réservé aux abonnés</label>
        <label class="check"><input type="checkbox" v-model="editing.is_active" /> Actif</label>
        <div class="modal__actions">
          <button @click="modalOpen = false">Annuler</button>
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
  adminCreateArenaChapter,
  adminUpdateArenaChapter,
  adminDeleteArenaChapter,
} from '@/api/arena'

const chapters = ref([])
const modalOpen = ref(false)
const editing = ref(blankChapter())

function blankChapter() {
  return {
    id: null, title: '', slug: '', description: '', icon: '📘',
    color: '#2563eb', order: 0, is_premium: false, is_active: true,
  }
}

async function load() {
  const { data } = await adminListArenaChapters()
  chapters.value = Array.isArray(data) ? data : (data?.results || [])
}
onMounted(load)

function openCreate() { editing.value = blankChapter(); modalOpen.value = true }
function openEdit(c) { editing.value = { ...c }; modalOpen.value = true }

async function save() {
  if (editing.value.id) {
    await adminUpdateArenaChapter(editing.value.id, editing.value)
  } else {
    await adminCreateArenaChapter(editing.value)
  }
  modalOpen.value = false
  await load()
}

async function remove(c) {
  if (!confirm(`Supprimer "${c.title}" ?`)) return
  await adminDeleteArenaChapter(c.id)
  await load()
}
</script>

<style scoped>
@import './arenaAdmin.css';
</style>
