<template>
  <div class="admin-subscriptions">
    <div class="header">
      <h1>Gestion des abonnements</h1>
    </div>

    <div class="card form">
      <h2>{{ editId ? 'Modifier un plan' : 'Ajouter un plan' }}</h2>
      <div class="row">
        <label>Nom<input v-model="form.name" placeholder="Ex: Mensuel, Annuel, Pass 24h" /></label>
        <label>Type
          <select v-model="form.plan_type">
            <option value="basic">Basic</option>
            <option value="premium">Premium</option>
          </select>
        </label>
        <label>Mode
          <select v-model="form.mode">
            <option value="subscription">Abonnement</option>
            <option value="one_time">One‑time (pass)</option>
          </select>
        </label>
      </div>
      <div class="row">
        <label>Période
          <select v-model="form.billing_period">
            <option value="daily">Journalier</option>
            <option value="weekly">Hebdomadaire</option>
            <option value="monthly">Mensuel</option>
            <option value="yearly">Annuel</option>
          </select>
        </label>
        <label>Prix (€)<input v-model.number="form.price" type="number" step="0.01" min="0" /></label>
        <label>Stripe Price ID (LIVE)<input v-model="form.stripe_price_id" placeholder="price_live_..." /></label>
        <label>Stripe Price ID (TEST)<input v-model="form.stripe_price_id_test" placeholder="price_test_..." /></label>
        <label v-if="form.mode === 'one_time'">Accès (jours)<input v-model.number="form.access_days" type="number" min="1" /></label>
      </div>
      <div class="row row-align-end">
        <label class="grow">Fonctionnalités (optionnel)
          <input v-model="featuresText" placeholder="séparées par des virgules" />
        </label>
        <label class="inline"><input type="checkbox" v-model="form.is_active" /> Actif</label>
      </div>
      <div class="actions">
        <button class="btn" @click="submit" :disabled="submitting">{{ submitting ? 'Enregistrement…' : (editId ? 'Mettre à jour' : 'Ajouter') }}</button>
        <button v-if="editId" class="btn secondary" @click="resetForm">Annuler</button>
      </div>
    </div>

    <div class="card">
      <div class="tools">
        <input v-model="q" type="search" class="search" placeholder="Rechercher par nom ou price_id…" />
        <button class="btn" @click="load">Recharger</button>
      </div>
      <table class="table">
        <thead>
          <tr>
            <th>Nom</th>
            <th>Mode</th>
            <th>Période</th>
            <th>Prix (€)</th>
            <th>Price ID (LIVE)</th>
            <th>Price ID (TEST)</th>
            <th>Accès</th>
            <th>Actif</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in filtered" :key="p.id">
            <td>{{ p.name }}</td>
            <td><span class="tag" :class="mode(p) === 'subscription' ? 'tag-sub' : 'tag-one'">{{ mode(p) }}</span></td>
            <td>{{ humanPeriod(p.billing_period) }}</td>
            <td>{{ Number(p.price || 0).toFixed(2) }}</td>
            <td class="mono">{{ p.stripe_price_id_live || p.stripe_price_id }}</td>
            <td class="mono">{{ p.stripe_price_id_test || '—' }}</td>
            <td>{{ p.access_days || (mode(p) === 'subscription' ? '—' : 0) }}</td>
            <td>{{ p.is_active ? 'Oui' : 'Non' }}</td>
            <td class="row-actions">
              <button class="link" @click="startEdit(p)">Modifier</button>
              <button class="link danger" @click="remove(p)">Supprimer</button>
            </td>
          </tr>
          <tr v-if="!filtered.length"><td colspan="9" class="empty">Aucun plan trouvé</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { adminListPlans, adminCreatePlan, adminUpdatePlan, adminDeletePlan } from '@/api/subscriptions'

const plans = ref([])
const q = ref('')
const editId = ref(null)
const form = ref({
  name: '',
  plan_type: 'basic',
  mode: 'subscription',
  billing_period: 'monthly',
  price: 0,
  stripe_price_id: '',
  stripe_price_id_test: '',
  access_days: null,
  is_active: true,
  features: []
})
const featuresText = ref('')

function mode(p) {
  return (p?.mode || p?.plan_mode || '').toLowerCase() || 'subscription'
}
function humanPeriod(p) {
  const v = (p || '').toLowerCase()
  if (v === 'daily') return 'Journalier'
  if (v === 'weekly') return 'Hebdomadaire'
  if (v === 'monthly') return 'Mensuel'
  if (v === 'yearly') return 'Annuel'
  return p
}

async function load() {
  const { data } = await adminListPlans()
  plans.value = data?.plans || []
}

const filtered = computed(() => {
  const s = (q.value || '').toLowerCase()
  if (!s) return plans.value
  return plans.value.filter(p =>
    String(p.name || '').toLowerCase().includes(s) ||
    String(p.stripe_price_id || '').toLowerCase().includes(s) ||
    String(p.stripe_price_id_live || '').toLowerCase().includes(s) ||
    String(p.stripe_price_id_test || '').toLowerCase().includes(s)
  )
})

onMounted(load)

function resetForm() {
  editId.value = null
  form.value = {
    name: '',
    plan_type: 'basic',
    mode: 'subscription',
    billing_period: 'monthly',
    price: 0,
    stripe_price_id: '',
    stripe_price_id_test: '',
    access_days: null,
    is_active: true,
    features: []
  }
  featuresText.value = ''
}

function startEdit(p) {
  editId.value = p.id
  form.value = {
    name: p.name,
    plan_type: p.plan_type,
    mode: mode(p),
    billing_period: p.billing_period,
    price: Number(p.price || 0),
    stripe_price_id: p.stripe_price_id_live || p.stripe_price_id,
    stripe_price_id_test: p.stripe_price_id_test || '',
    access_days: p.access_days || null,
    is_active: !!p.is_active,
    features: Array.isArray(p.features) ? p.features : []
  }
  featuresText.value = (form.value.features || []).join(', ')
}

const submitting = ref(false)
async function submit() {
  try {
    submitting.value = true
    const payload = { ...form.value, features: (featuresText.value || '').split(',').map(s => s.trim()).filter(Boolean) }
    if (!editId.value) await adminCreatePlan(payload)
    else await adminUpdatePlan(editId.value, payload)
    await load()
    resetForm()
  } catch (e) {
    alert(e?.response?.data?.detail || 'Erreur de sauvegarde')
  } finally {
    submitting.value = false
  }
}

async function remove(p) {
  if (!confirm(`Supprimer le plan "${p.name}" ?`)) return
  try {
    await adminDeletePlan(p.id)
    await load()
  } catch (e) {
    alert('Suppression impossible')
  }
}
</script>

<style scoped>
.admin-subscriptions { padding: 16px; }
.header { display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom: 12px; }
.btn { background:#2a38b7; color:#fff; border:none; border-radius:8px; padding:8px 12px; font-weight:700; text-decoration:none; cursor:pointer }
.btn.secondary { background:#f3f4f6; color:#111827; border:1px solid #e5e7eb }
.card { background:#fff; border:1px solid #e5e7eb; border-radius:12px; padding:12px; margin-bottom:12px }
.tools { display:flex; gap:8px; align-items:center; margin-bottom:8px }
.search { flex:1; border:1px solid #e5e7eb; border-radius:8px; padding:8px; background:#fafafa }
.form .row { display:flex; gap:8px; align-items:center; margin-bottom:8px }
.form .row-align-end { align-items:flex-end }
.form label { display:flex; flex-direction:column; gap:6px; font-weight:600; flex: 1 }
.form .grow { flex: 1 1 auto }
.form .inline { display:flex; flex-direction:row; align-items:center; gap:6px; font-weight:600; flex: 0 0 auto; align-self:flex-end; margin-bottom: 0; padding-left: 16px }
.form input, .form select { border:1px solid #e5e7eb; border-radius:8px; padding:8px; background:#fafafa }
.table { width:100%; border-collapse:collapse }
.table th, .table td { border-bottom:1px solid #eee; padding:10px; text-align:left; font-size:14px }
.row-actions { display:flex; gap:10px }
.link { color:#2a38b7; text-decoration:none; font-weight:600 }
.link.danger { color:#b91c1c }
.empty { text-align:center; color:#6b7280 }
.hint { color:#374151; margin-top:8px }
.tag { padding:2px 8px; border-radius:999px; font-size:12px; font-weight:700 }
.tag-sub { background:#e8f0ff; color:#1d4ed8 }
.tag-one { background:#ecfdf5; color:#065f46 }
.mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; font-size:12px }
</style>
