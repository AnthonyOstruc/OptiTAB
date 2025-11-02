<template>
  <div class="admin-subscribers">
    <div class="header">
      <h1>Abonnés</h1>
      <div class="tools">
        <input v-model="q" type="search" class="search" placeholder="Rechercher email/nom…" />
        <label class="inline"><input type="checkbox" v-model="activeOnly" /> Actifs uniquement</label>
        <button class="btn" @click="load">Recharger</button>
        <button class="btn secondary" @click="sync" :disabled="syncing">{{ syncing ? 'Sync…' : 'Synchroniser Stripe' }}</button>
      </div>
    </div>

    <div class="card">
      <table class="table">
        <thead>
          <tr>
            <th>Utilisateur</th>
            <th>Type</th>
            <th>Plan</th>
            <th>Statut</th>
            <th>Début</th>
            <th>Prix payé</th>
            <th>Fin</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="it in items" :key="`${it.type}-${it.user_id}-${it.plan_id}-${it.ends_at || it.current_period_end || ''}`">
            <td>
              <div class="user-cell">
                <div class="name">{{ it.first_name }} {{ it.last_name }}</div>
                <div class="email">{{ it.email }}</div>
              </div>
            </td>
            <td>
              <span class="tag" :class="tagClass(it.type)">{{ formatType(it.type) }}</span>
            </td>
            <td>
              <div class="plan">{{ it.plan_name }}</div>
              <div class="muted" v-if="it.type==='subscription'">{{ it.billing_period || '—' }}</div>
              <div class="muted" v-else-if="it.type==='pass'">fin {{ formatDate(it.ends_at) }}</div>
              <div class="muted" v-else>Accès accordé manuellement</div>
            </td>
            <td>
              <span v-if="it.type==='subscription'">{{ it.status }} <span v-if="it.is_trial" class="muted">(essai)</span></span>
              <span v-else-if="it.type==='pass'">{{ it.is_active ? 'actif' : 'expiré' }}</span>
              <span v-else>Accès manuel</span>
            </td>
            <td>
              <span>{{ formatDate(startDate(it)) }}</span>
            </td>
            <td>{{ formatAmount(it.amount_paid, it.currency) }}</td>
            <td>
              <span>{{ formatDate(endDate(it)) }}</span>
            </td>
          </tr>
          <tr v-if="!items.length"><td colspan="7" class="empty">Aucun résultat</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { apiClient } from '@/api'

const q = ref('')
const activeOnly = ref(false)
const items = ref([])

function formatDate(v) {
  if (!v) return '—'
  try { return new Date(v).toLocaleString('fr-FR') } catch { return v }
}

function formatAmount(amount, currency) {
  if (amount === undefined || amount === null) return '—'
  const cur = (currency || 'EUR').toUpperCase()
  try {
    return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: cur }).format(amount)
  } catch (e) {
    return `${amount} ${cur}`
  }
}

function tagClass(type) {
  if (type === 'subscription') return 'tag-sub'
  if (type === 'manual') return 'tag-manual'
  return 'tag-one'
}

function formatType(type) {
  switch (type) {
    case 'subscription': return 'abonnement'
    case 'pass': return 'pass'
    case 'manual': return 'manuel'
    default: return type
  }
}

function startDate(item) {
  if (!item) return null
  if (item.type === 'subscription') return item.current_period_start
  if (item.type === 'pass') return item.starts_at
  return item.current_period_start || item.starts_at
}

function endDate(item) {
  if (!item) return null
  if (item.type === 'subscription') return item.current_period_end
  if (item.type === 'pass') return item.ends_at
  return item.current_period_end || item.ends_at
}

async function load() {
  const params = { q: q.value || undefined, active: activeOnly.value ? 'true' : 'false' }
  const { data } = await apiClient.get('/api/subscriptions/admin/subscribers/', { params })
  items.value = data?.items || []
}

load()

const syncing = ref(false)
async function sync() {
  try {
    syncing.value = true
    await apiClient.post('/api/subscriptions/admin/sync-from-stripe/')
    await load()
    alert('Synchronisation terminée.')
  } catch (e) {
    alert('Erreur de synchronisation')
  } finally {
    syncing.value = false
  }
}
</script>

<style scoped>
.admin-subscribers { padding: 16px; }
.header { display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:12px }
.tools { display:flex; align-items:center; gap:8px }
.inline { display:flex; align-items:center; gap:6px }
.search { border:1px solid #e5e7eb; border-radius:8px; padding:8px; background:#fafafa }
.btn { background:#2a38b7; color:#fff; border:none; border-radius:8px; padding:8px 12px; font-weight:700; cursor:pointer }
.card { background:#fff; border:1px solid #e5e7eb; border-radius:12px; padding:12px }
.table { width:100%; border-collapse:collapse }
.table th, .table td { border-bottom:1px solid #eee; padding:10px; text-align:left; font-size:14px }
.user-cell .name { font-weight:700 }
.user-cell .email { color:#6b7280; font-size:12px }
.muted { color:#6b7280; font-size:12px }
.tag { padding:2px 8px; border-radius:999px; font-size:12px; font-weight:700 }
.tag-sub { background:#e8f0ff; color:#1d4ed8 }
.tag-one { background:#ecfdf5; color:#065f46 }
.tag-manual { background:#fef3c7; color:#92400e }
.empty { text-align:center; color:#6b7280 }
</style>
