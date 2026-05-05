<template>
  <main class="admin-arena">
    <header class="admin-arena__head">
      <div>
        <p class="eyebrow">Arena · Math game</p>
        <h1>Pilotage du jeu OptiTAB Arena</h1>
      </div>
      <div class="admin-arena__public">
        <label class="switch">
          <input type="checkbox" :checked="config?.is_public" @change="togglePublic($event.target.checked)" />
          <span class="switch__slider" />
        </label>
        <span>{{ config?.is_public ? 'Public' : 'Admin uniquement' }}</span>
      </div>
    </header>

    <section class="admin-arena__grid">
      <RouterLink to="/admin/arena/chapters" class="tile">
        <h3>📘 Chapitres</h3>
        <p>Gérer les chapitres et leur ordre.</p>
      </RouterLink>
      <RouterLink to="/admin/arena/levels" class="tile">
        <h3>🏷 Niveaux</h3>
        <p>Configurer les niveaux par chapitre.</p>
      </RouterLink>
      <RouterLink to="/admin/arena/questions" class="tile">
        <h3>❓ Questions</h3>
        <p>Banque de questions LaTeX, MCQ et numériques.</p>
      </RouterLink>
      <RouterLink to="/admin/arena/daily" class="tile">
        <h3>⚡ Défi quotidien</h3>
        <p>Programmer le défi mis en avant chaque jour.</p>
      </RouterLink>
      <RouterLink to="/jeu" class="tile tile--primary">
        <h3>👁 Aperçu joueur</h3>
        <p>Tester l'expérience tel un élève.</p>
      </RouterLink>
    </section>

    <section v-if="analytics" class="admin-arena__kpis">
      <h2>KPIs</h2>
      <div class="kpis">
        <div class="kpi"><span>{{ analytics.attempts?.total ?? 0 }}</span><small>Tentatives</small></div>
        <div class="kpi"><span>{{ formatPct(analytics.attempts?.avg_accuracy) }}</span><small>Précision moy.</small></div>
        <div class="kpi"><span>{{ analytics.attempts?.avg_xp ? Math.round(analytics.attempts.avg_xp) : 0 }}</span><small>XP moy. / partie</small></div>
        <div class="kpi"><span>{{ analytics.unique_players_30d ?? 0 }}</span><small>Joueurs (30j)</small></div>
      </div>
      <h3>Événements</h3>
      <table class="events">
        <thead><tr><th>Événement</th><th>Nombre</th></tr></thead>
        <tbody>
          <tr v-for="row in analytics.events_by_name" :key="row.name">
            <td>{{ row.name }}</td>
            <td>{{ row.count }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import {
  adminGetArenaConfig,
  adminUpdateArenaConfig,
  adminGetArenaAnalytics,
} from '@/api/arena'

const config = ref(null)
const analytics = ref(null)

async function load() {
  const [{ data: cfg }, { data: stats }] = await Promise.all([
    adminGetArenaConfig(),
    adminGetArenaAnalytics(),
  ])
  config.value = cfg
  analytics.value = stats
}

onMounted(load)

async function togglePublic(value) {
  const { data } = await adminUpdateArenaConfig({ is_public: value })
  config.value = data
}

function formatPct(v) {
  if (typeof v !== 'number') return '—'
  return `${Math.round(v * 100)}%`
}
</script>

<style scoped>
.admin-arena { padding: 24px; max-width: 1080px; margin: 0 auto; }
.admin-arena__head { display: flex; justify-content: space-between; align-items: center; gap: 16px; margin-bottom: 24px; }
.eyebrow { color: #2563eb; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin: 0; font-size: 12px; }
h1 { margin: 4px 0 0; color: #0f172a; }

.admin-arena__public { display: flex; gap: 10px; align-items: center; font-weight: 700; color: #0f172a; }
.switch { position: relative; display: inline-block; width: 44px; height: 24px; }
.switch input { opacity: 0; width: 0; height: 0; }
.switch__slider {
  position: absolute; cursor: pointer; inset: 0;
  background: #e2e8f0; border-radius: 999px; transition: .15s;
}
.switch__slider:before {
  content: ''; position: absolute; height: 18px; width: 18px; left: 3px; top: 3px;
  background: #fff; border-radius: 50%; transition: .15s;
}
.switch input:checked + .switch__slider { background: linear-gradient(135deg, #2563eb, #7c3aed); }
.switch input:checked + .switch__slider:before { transform: translateX(20px); }

.admin-arena__grid { display: grid; gap: 14px; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); }
.tile {
  display: block; padding: 18px;
  background: #fff; border: 1px solid #e2e8f0; border-radius: 14px;
  text-decoration: none; color: inherit;
  transition: border-color .15s ease, transform .15s ease;
}
.tile:hover { border-color: #2563eb; transform: translateY(-2px); }
.tile h3 { margin: 0 0 6px; color: #0f172a; }
.tile p { margin: 0; color: #64748b; font-size: 14px; }
.tile--primary { background: linear-gradient(135deg, #2563eb, #7c3aed); color: #fff; }
.tile--primary p { color: #dbeafe; }

.admin-arena__kpis { margin-top: 32px; }
.kpis { display: grid; gap: 12px; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); margin-bottom: 18px; }
.kpi { background: #fff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 16px; text-align: center; }
.kpi span { display: block; font-size: 22px; font-weight: 800; color: #0f172a; }
.kpi small { color: #64748b; }

.events { width: 100%; border-collapse: collapse; background: #fff; border-radius: 12px; overflow: hidden; }
.events th, .events td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #f1f5f9; }
.events th { background: #f8fafc; color: #475569; font-size: 12px; text-transform: uppercase; letter-spacing: 0.06em; }
</style>
