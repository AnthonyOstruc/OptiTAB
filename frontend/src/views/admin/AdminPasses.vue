<template>
  <div class="admin-passes">
    <div class="hero">
      <div class="title-block">
        <div class="eyebrow">Administration</div>
        <h1>Passes</h1>
        <p class="subtitle">Gérez rapidement les accès one‑time et les remboursements.</p>
      </div>
      <div class="stats">
        <div class="stat">
          <div class="stat-label">Total</div>
          <div class="stat-value">{{ stats.total }}</div>
        </div>
        <div class="stat">
          <div class="stat-label">Actifs</div>
          <div class="stat-value">{{ stats.active }}</div>
        </div>
        <div class="stat">
          <div class="stat-label">Révoqués</div>
          <div class="stat-value">{{ stats.revoked }}</div>
        </div>
        <div class="stat muted">
          <div class="stat-label">Expirés</div>
          <div class="stat-value">{{ stats.expired }}</div>
        </div>
      </div>
    </div>

    <div class="card filter-card">
      <div class="tools">
        <div class="field">
          <span class="field-label">Recherche</span>
          <div class="field-input">
            <input
              v-model="q"
              type="search"
              class="search"
              placeholder="Email, nom ou payment_intent…"
              @keydown.enter.prevent="load"
            />
          </div>
        </div>
        <div class="field compact">
          <span class="field-label">Statut</span>
          <select v-model="status" class="select">
            <option value="all">Tous</option>
            <option value="active">Actifs</option>
            <option value="revoked">Révoqués</option>
          </select>
        </div>
        <button class="btn" @click="load" :disabled="loading">
          {{ loading ? 'Chargement…' : 'Recharger' }}
        </button>
      </div>
    </div>

    <div class="card table-card">
      <div class="table-head">
        <div class="table-title">Liste des passes</div>
        <div class="table-meta">{{ stats.total }} résultat(s)</div>
      </div>
      <table class="table">
        <thead>
          <tr>
            <th>Utilisateur</th>
            <th>Plan</th>
            <th>Paiement</th>
            <th>Début</th>
            <th>Fin</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td data-label="Utilisateur">
              <div class="user-cell">
                <div class="name">{{ displayName(item) }}</div>
                <div class="email">{{ item.email || '—' }}</div>
              </div>
            </td>
            <td data-label="Plan">
              <div class="plan">{{ item.plan_name || '—' }}</div>
              <div class="muted">
                Accès : {{ item.access_days ? `${item.access_days} j` : '—' }}
              </div>
            </td>
            <td data-label="Paiement">
              <div class="amount">{{ formatAmount(item.amount_paid, item.currency) }}</div>
              <div class="muted mono">{{ item.stripe_payment_intent_id || '—' }}</div>
              <div v-if="item.payment_status" class="tag" :class="paymentClass(item.payment_status)">
                {{ item.payment_status }}
              </div>
            </td>
            <td data-label="Début">{{ formatDateTime(item.starts_at) }}</td>
            <td data-label="Fin">{{ formatDateTime(item.ends_at) }}</td>
            <td data-label="Statut">
              <span class="tag" :class="statusClass(item)">{{ statusLabel(item) }}</span>
              <div v-if="item.revoked_at" class="muted micro">Révoqué le {{ formatDateTime(item.revoked_at) }}</div>
            </td>
            <td data-label="Actions">
              <div class="actions">
                <button
                  class="action-btn"
                  :class="item.is_revoked ? 'ghost' : 'danger'"
                  :disabled="savingId === item.id"
                  @click="toggleRevoke(item)"
                >
                  {{ savingId === item.id ? '…' : (item.is_revoked ? 'Annuler révocation' : 'Révoquer') }}
                </button>
                <button
                  class="action-btn ghost"
                  :disabled="savingId === item.id"
                  @click="editEndsAt(item)"
                >
                  Modifier fin
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="!items.length">
            <td colspan="7" class="empty">Aucun pass trouvé</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { adminListPasses, adminUpdatePass } from '@/api/subscriptions'

const q = ref('')
const status = ref('all')
const items = ref([])
const loading = ref(false)
const savingId = ref(null)

const stats = computed(() => {
  const total = items.value.length
  const active = items.value.filter(i => i?.is_active && !i?.is_revoked).length
  const revoked = items.value.filter(i => i?.is_revoked).length
  const expired = items.value.filter(i => !i?.is_revoked && !i?.is_active).length
  return { total, active, revoked, expired }
})

function displayName(item) {
  const name = `${item?.first_name || ''} ${item?.last_name || ''}`.trim()
  return name || item?.email || '—'
}

function formatDateTime(value) {
  if (!value) return '—'
  try {
    const dt = new Date(value)
    if (Number.isNaN(dt.getTime())) return value
    return dt.toLocaleString('fr-FR', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return value
  }
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

function statusLabel(item) {
  if (item?.is_revoked) return 'révoqué'
  if (item?.is_active) return 'actif'
  return 'expiré'
}

function statusClass(item) {
  if (item?.is_revoked) return 'tag-revoked'
  if (item?.is_active) return 'tag-active'
  return 'tag-expired'
}

function paymentClass(statusValue) {
  const s = String(statusValue || '').toLowerCase()
  if (['succeeded', 'paid', 'complete'].includes(s)) return 'tag-paid'
  if (['refunded', 'refund', 'partially_refunded'].includes(s)) return 'tag-refunded'
  if (['failed', 'canceled', 'unpaid', 'past_due'].includes(s)) return 'tag-failed'
  return 'tag-neutral'
}

async function load() {
  const params = { q: q.value || undefined }
  if (status.value === 'active') params.active = 'true'
  if (status.value === 'revoked') params.revoked = 'true'

  loading.value = true
  try {
    const { data } = await adminListPasses(params)
    items.value = data?.passes || []
  } catch (e) {
    alert(e?.response?.data?.detail || 'Erreur de chargement')
  } finally {
    loading.value = false
  }
}

async function toggleRevoke(item) {
  if (!item) return
  const next = !item.is_revoked
  const confirmation = next
    ? 'Révoquer ce pass et couper l’accès immédiatement ?'
    : 'Annuler la révocation de ce pass ?'
  if (typeof window !== 'undefined' && !window.confirm(confirmation)) return
  savingId.value = item.id
  try {
    await adminUpdatePass(item.id, { is_revoked: next })
    await load()
  } catch (e) {
    alert(e?.response?.data?.detail || 'Erreur de mise à jour')
  } finally {
    savingId.value = null
  }
}

async function editEndsAt(item) {
  if (!item) return
  const current = item.ends_at || ''
  const input = window.prompt('Nouvelle date de fin (YYYY-MM-DD ou ISO)', current)
  if (!input) return
  savingId.value = item.id
  try {
    await adminUpdatePass(item.id, { ends_at: input })
    await load()
  } catch (e) {
    alert(e?.response?.data?.detail || 'Erreur de mise à jour')
  } finally {
    savingId.value = null
  }
}

load()
</script>

<style scoped>
.admin-passes {
  padding: 20px;
  background:
    radial-gradient(circle at 20% -20%, rgba(14, 116, 144, 0.08), transparent 55%),
    radial-gradient(circle at 80% 0%, rgba(251, 191, 36, 0.12), transparent 35%),
    #f8fafc;
  min-height: calc(100dvh - 20px);
  font-family: "Space Grotesk", "Manrope", "IBM Plex Sans", "Segoe UI", sans-serif;
}

.hero { display:flex; align-items:flex-end; justify-content:space-between; gap:16px; margin-bottom:14px }
.title-block h1 { font-size:28px; margin:4px 0 6px 0; letter-spacing:-0.02em }
.eyebrow { font-size:12px; text-transform:uppercase; letter-spacing:0.16em; color:#0f766e; font-weight:700 }
.subtitle { color:#475569; margin:0 }

.stats { display:grid; grid-template-columns: repeat(4, minmax(80px, 1fr)); gap:10px }
.stat { background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:10px 12px; box-shadow:0 6px 18px rgba(15, 23, 42, 0.04) }
.stat.muted { background:#f8fafc }
.stat-label { font-size:11px; text-transform:uppercase; letter-spacing:0.08em; color:#64748b; font-weight:700 }
.stat-value { font-size:18px; font-weight:700; color:#0f172a; margin-top:4px }

.card { background:#fff; border:1px solid #e2e8f0; border-radius:16px; padding:14px; box-shadow:0 8px 22px rgba(15, 23, 42, 0.06) }
.filter-card { margin-bottom:12px }
.table-card { padding:12px 14px }
.table-head { display:flex; align-items:center; justify-content:space-between; margin-bottom:6px }
.table-title { font-weight:700; color:#0f172a }
.table-meta { font-size:12px; color:#64748b }

.tools { display:grid; grid-template-columns: 1.2fr 0.5fr auto; gap:12px; align-items:end }
.field { display:flex; flex-direction:column; gap:6px }
.field.compact { max-width:220px }
.field-label { font-size:12px; color:#64748b; font-weight:600 }
.search, .select {
  border:1px solid #e2e8f0;
  border-radius:10px;
  padding:10px 12px;
  background:#f8fafc;
  font-size:14px;
  color:#0f172a;
}
.search:focus, .select:focus { outline:2px solid rgba(14, 116, 144, 0.25); border-color:#0e7490 }

.btn {
  background: linear-gradient(135deg, #0e7490, #0f766e);
  color:#fff;
  border:none;
  border-radius:10px;
  padding:10px 14px;
  font-weight:700;
  cursor:pointer;
  box-shadow:0 10px 18px rgba(14, 116, 144, 0.2);
}
.btn:disabled { opacity:0.7; cursor:not-allowed }

.table { width:100%; border-collapse:collapse; background:#fff }
.table th, .table td { border-bottom:1px solid #edf2f7; padding:12px 8px; text-align:left; font-size:14px; vertical-align:top }
.table th { font-size:12px; text-transform:uppercase; letter-spacing:0.08em; color:#64748b }
.table tbody tr:hover { background:#f8fafc }

.user-cell .name { font-weight:700 }
.user-cell .email { color:#64748b; font-size:12px }
.plan { font-weight:600 }
.muted { color:#64748b; font-size:12px }
.micro { font-size:11px }
.mono { font-family: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; font-size:12px }
.amount { font-weight:600 }
.tag { display:inline-flex; align-items:center; gap:6px; padding:3px 10px; border-radius:999px; font-size:12px; font-weight:700; margin-top:4px }
.tag-active { background:#dcfce7; color:#166534 }
.tag-expired { background:#f1f5f9; color:#475569 }
.tag-revoked { background:#fee2e2; color:#b91c1c }
.tag-paid { background:#e0f2fe; color:#0369a1 }
.tag-refunded { background:#fef3c7; color:#92400e }
.tag-failed { background:#fee2e2; color:#b91c1c }
.tag-neutral { background:#f1f5f9; color:#64748b }

.action-btn { border:none; border-radius:8px; padding:6px 10px; font-size:12px; font-weight:700; cursor:pointer }
.action-btn.danger { background:#b91c1c; color:#fff }
.action-btn.ghost { background:#f1f5f9; color:#0f172a }
.action-btn:disabled { opacity:0.6; cursor:not-allowed }
.actions { display:flex; gap:6px; flex-wrap:wrap }
.empty { text-align:center; color:#64748b; padding:14px }

@media (max-width: 1200px) {
  .stats { grid-template-columns: repeat(2, minmax(80px, 1fr)) }
  .tools { grid-template-columns: 1fr 0.6fr auto }
}

@media (max-width: 900px) {
  .hero { flex-direction:column; align-items:flex-start }
  .tools { grid-template-columns: 1fr; }
  .field.compact { max-width:100% }
}

@media (max-width: 720px) {
  .table thead { display:none }
  .table, .table tbody, .table tr, .table td { display:block; width:100% }
  .table tr {
    border:1px solid #e2e8f0;
    border-radius:14px;
    padding:10px 12px;
    margin-bottom:12px;
    background:#fff;
    box-shadow:0 8px 18px rgba(15, 23, 42, 0.05);
  }
  .table td {
    border-bottom:none;
    padding:8px 0;
    display:flex;
    justify-content:space-between;
    gap:12px;
  }
  .table td::before {
    content: attr(data-label);
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:0.08em;
    color:#94a3b8;
    font-weight:700;
    min-width:110px;
  }
  .table td[data-label="Utilisateur"]::before,
  .table td[data-label="Plan"]::before,
  .table td[data-label="Paiement"]::before {
    align-self:flex-start;
  }
  .user-cell .email, .muted, .mono { word-break: break-all }
  .actions { width:100%; justify-content:flex-end }
  .action-btn { width:100%; text-align:center }
}
</style>
