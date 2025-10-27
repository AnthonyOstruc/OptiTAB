<template>
  <div class="admin-newsletter">
    <h1>Newsletter</h1>
    <div class="grid">
      <section class="card">
        <h2>Envoyer un email</h2>
        <form @submit.prevent="onSend">
          <label>
            Sujet
            <input v-model="form.subject" type="text" required placeholder="Sujet de l'email" />
          </label>
          <label>
            Message (texte)
            <textarea v-model="form.text" rows="6" placeholder="Contenu texte (affiché si client ne supporte pas HTML)"></textarea>
          </label>
          <label class="inline" style="gap:8px"><input v-model="form.useTemplate" type="checkbox" /> Utiliser le modèle OptiTAB (en-tête + footer)</label>
<label>
  Message (HTML)
  <textarea v-model="form.html" rows="8" placeholder="Optionnel si vous utilisez le modèle. Laissez vide pour utiliser seulement le texte."></textarea>
</label>
<div class="inline"><label><input v-model="form.onlyInactive" type="checkbox" /> Cibler désabonnés (réactivation)</label></div>
          <button type="submit" :disabled="loading">{{ loading ? 'Envoi…' : 'Envoyer' }}</button>
          <p v-if="sendMessage" class="hint">{{ sendMessage }}</p>
        </form>
      </section>
      <section class="card">
        <div class="table-header">
          <h2>Abonnés actuels</h2>
          <div class="filters">
            <input v-model="filters.q" type="search" placeholder="Rechercher email…" @input="debouncedLoad" />
            <select v-model="filters.active" @change="load">
              <option value="all">Tous</option>
              <option :value="true">Actifs</option>
              <option :value="false">Désabonnés</option>
            </select>
          </div>
        </div>
        <table class="table">
          <thead>
            <tr><th>Email</th><th>Nom</th><th>Statut</th><th>Inscription</th></tr>
          </thead>
          <tbody>
            <tr v-for="s in subscribers" :key="s.email">
              <td>{{ s.email }}</td>
              <td>{{ (s.first_name || '') + ' ' + (s.last_name || '') }}</td>
              <td><span :class="s.est_actif ? 'badge active' : 'badge inactive'">{{ s.est_actif ? 'Actif' : 'Désabonné' }}</span></td>
              <td>{{ formatDate(s.date_creation) }}</td>
            </tr>
            <tr v-if="!subscribers.length"><td colspan="4" class="empty">Aucun résultat</td></tr>
          </tbody>
        </table>
        <div class="pagination">
          <button @click="prev" :disabled="offset === 0">Précédent</button>
          <span class="pagination-info">{{ offset + 1 }}–{{ Math.min(offset + limit, total) }} / {{ total }}</span>
          <button @click="next" :disabled="offset + limit >= total">Suivant</button>
        </div>
      </section>
    </div>
  </div>
  
</template>

<script setup>
import { ref } from 'vue'
import { getNewsletterSubscribers, broadcastNewsletter } from '@/api/newsletter'

const subscribers = ref([])
const total = ref(0)
const offset = ref(0)
const limit = ref(20)
const loading = ref(false)
const sendMessage = ref('')

const filters = ref({ q: '', active: 'all' })

function formatDate(d) {
  try { return new Date(d).toLocaleString() } catch { return d }
}

async function load() {
  const activeParam = filters.value.active
  const { items, total: t } = await getNewsletterSubscribers({ q: filters.value.q, active: activeParam, limit: limit.value, offset: offset.value })
  subscribers.value = items || []
  total.value = t || 0
}

let timer = null
function debouncedLoad() {
  if (timer) clearTimeout(timer)
  timer = setTimeout(() => load(), 300)
}

function next() {
  offset.value = Math.min(offset.value + limit.value, Math.max(total.value - limit.value, 0))
  load()
}
function prev() {
  offset.value = Math.max(offset.value - limit.value, 0)
  load()
}

const form = ref({ subject: '', text: '', html: '', onlyInactive: false, useTemplate: true })
async function onSend() {
  if (!form.value.subject) return
  loading.value = true
  sendMessage.value = ''
  try {
    const res = await broadcastNewsletter({ ...form.value })
    sendMessage.value = res?.message || 'Envoi terminé.'
  } catch (e) {
    sendMessage.value = e?.response?.data?.message || 'Erreur lors de l\'envoi.'
  } finally {
    loading.value = false
  }
}

load()
</script>

<style scoped>
.admin-newsletter { padding: 16px; }
.grid { display: grid; grid-template-columns: 1fr 1.4fr; gap: 16px; align-items: start; }
.card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; }
.card h2 { margin: 0 0 12px 0; }
label { display: block; margin-bottom: 10px; font-weight: 600; }
input[type="text"], textarea, input[type="number"], input[type="search"], select { width: 100%; border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px; font-size: 14px; background:#fafafa }
.inline { display: flex; gap: 16px; align-items: center; }
button { background: #2a38b7; color: #fff; border: none; padding: 10px 16px; border-radius: 8px; cursor: pointer; }
button[disabled] { opacity: 0.6; cursor: not-allowed; }
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { border-bottom: 1px solid #eee; padding: 10px; text-align: left; font-size: 14px }
.table .empty { text-align: center; color: #6b7280 }
.badge { padding: 4px 8px; border-radius: 9999px; font-size: 12px }
.badge.active { background: #e8f9ee; color: #15803d }
.badge.inactive { background: #fee2e2; color: #b91c1c }
.table-header { display:flex; align-items:center; justify-content:space-between; gap:12px }
.filters { display:flex; gap:8px }
.hint { margin-top:8px; color:#374151 }
.pagination { display: flex; align-items: center; justify-content: center; gap: 16px; margin-top: 16px; }
.pagination-info { padding: 0 8px; font-weight: 500; color: #374151; }
@media (max-width: 1000px){ .grid { grid-template-columns: 1fr; } }
</style>