<template>
  <div class="leaderboard-card">
    <div class="leaderboard-header">
      <h3 class="leaderboard-title">Classement</h3>
      <div class="leaderboard-tabs">
        <button :class="['tab', { active: scope === 'global' }]" @click="setScope('global')">Global</button>
        <button :class="['tab', { active: scope === 'pays' }]" @click="setScope('pays')" :disabled="!canScopePays">
          <span v-if="userStore.pays?.drapeau_emoji" class="flag">{{ userStore.pays?.drapeau_emoji }}</span>
          Pays
        </button>
        <button :class="['tab', { active: scope === 'niveau' }]" @click="setScope('niveau')" :disabled="!canScopeNiveau">
          Niveau
        </button>
      </div>
    </div>

    <div class="leaderboard-body" v-if="!loading">
      <!-- Zone de contenu scrollable -->
      <div class="leaderboard-content">
        <div class="leaderboard-item me-item" v-if="me">
          <div class="rank">
            <div class="me-rank">#{{ me.rank }}</div>
            <div class="me-sub">sur {{ me.total }}</div>
          </div>
          <div class="user">
            <div class="info">
              <div class="name">Vous</div>
              <div class="meta">
                <span v-if="me.pays_flag" class="flag">{{ me.pays_flag }}</span>
                <span v-if="me.niveau" class="niveau">{{ me.niveau }}</span>
              </div>
            </div>
          </div>
          <div class="xp">
            <div class="me-xp">{{ me.xp }} XP</div>
            <div class="me-percent">Top {{ me.percentile }}%</div>
          </div>
        </div>
        <ul class="leaderboard-list">
          <!-- Toujours afficher les 5 premiers -->
          <li v-for="u in allLeaderboard.slice(0, 5)" :key="u.id" class="leaderboard-item">
            <div class="rank">
              <span v-if="u.rank === 1" class="trophy gold">🥇</span>
              <span v-else-if="u.rank === 2" class="trophy silver">🥈</span>
              <span v-else-if="u.rank === 3" class="trophy bronze">🥉</span>
              <span v-else>#{{ u.rank }}</span>
            </div>
            <div class="user">
              <div class="avatar">{{ initials(u.display_name) }}</div>
              <div class="info">
                <div class="name">
                  <span v-if="u.pays_flag" class="flag name-flag">{{ u.pays_flag }}</span>
                  <span class="first-name">{{ parseName(u.display_name).firstName }}</span>
                  <span class="last-name">{{ parseName(u.display_name).lastName }}</span>
                </div>
                <div class="meta" v-if="u.niveau">{{ u.niveau }}</div>
              </div>
            </div>
            <div class="xp">{{ u.xp }} XP</div>
          </li>
        </ul>

        <!-- Liste déroulante pour les autres utilisateurs -->
        <div v-if="isExpanded && allLeaderboard.length > 5" class="expanded-section">
          <div class="expanded-header">
            <span class="expanded-title">Autres classés</span>
            <span class="expanded-count">{{ Math.min(allLeaderboard.length - 5, 45) }} utilisateurs</span>
          </div>
          <ul class="leaderboard-list">
            <li v-for="u in allLeaderboard.slice(5, 50)" :key="u.id" class="leaderboard-item expanded-item">
              <div class="rank">
                #{{ u.rank }}
              </div>
              <div class="user">
                <div class="avatar">{{ initials(u.display_name) }}</div>
                <div class="info">
                  <div class="name">
                    <span v-if="u.pays_flag" class="flag name-flag">{{ u.pays_flag }}</span>
                    <span class="first-name">{{ parseName(u.display_name).firstName }}</span>
                    <span class="last-name">{{ parseName(u.display_name).lastName }}</span>
                  </div>
                  <div class="meta" v-if="u.niveau">{{ u.niveau }}</div>
                </div>
              </div>
              <div class="xp">{{ u.xp }} XP</div>
            </li>
          </ul>
        </div>
      </div>

      <!-- Bouton Voir plus toujours visible (désactivé si rien à étendre) -->
      <div class="leaderboard-actions" v-if="allLeaderboard.length > 0">
        <button 
          v-if="!isExpanded" 
          @click="loadMore" 
          class="btn-see-more"
          :disabled="loading || allLeaderboard.length <= 5"
        >
          <span class="btn-text">Voir plus</span>
        </button>
        <button 
          v-else 
          @click="loadLess" 
          class="btn-see-less"
        >
          <span class="btn-text">Voir moins</span>
        </button>
      </div>

      <div v-if="!allLeaderboard.length" class="empty-state">
        <div>Pas encore de classement pour ce filtre.</div>
      </div>
    </div>

    <div class="leaderboard-loading" v-else>
      <div class="skeleton me"></div>
      <div class="skeleton row" v-for="i in 6" :key="i"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { fetchLeaderboard } from '@/api/users'

const userStore = useUserStore()

const scope = ref('global')
const loading = ref(true)
const leaderboard = ref([])
const me = ref(null)
const isExpanded = ref(false)
const allLeaderboard = ref([]) // Stocke tous les utilisateurs

const canScopePays = computed(() => !!userStore?.pays?.id)
const canScopeNiveau = computed(() => !!userStore?.niveau_pays?.id)

function setScope(s) {
  if ((s === 'pays' && !canScopePays.value) || (s === 'niveau' && !canScopeNiveau.value)) return
  scope.value = s
}

function initials(name) {
  if (!name) return 'U'
  const parts = String(name).trim().split(/\s+/)
  if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase()
  return (parts[0].substring(0, 1) + parts[1].substring(0, 1)).toUpperCase()
}

// Découpe un nom "Prénom Nom" pour pouvoir masquer dynamiquement
function parseName(name) {
  const raw = String(name || '').trim()
  if (!raw) return { firstName: '', lastName: '' }
  const parts = raw.split(/\s+/)
  const firstName = parts[0] || ''
  const lastName = parts.slice(1).join(' ') || ''
  return { firstName, lastName }
}

async function load() {
  loading.value = true
  try {
    // Charge maximum 50 utilisateurs (limite fixe)
    const res = await fetchLeaderboard({ scope: scope.value, limit: 50 })
    const data = res?.data?.data || {}
    const leaderboard = data.leaderboard || []
    
    // S'assurer qu'on ne dépasse jamais 50 utilisateurs
    allLeaderboard.value = leaderboard.slice(0, 50)
    me.value = data.me || null
    isExpanded.value = false // Reset à l'état normal
  } catch (e) {
    allLeaderboard.value = []
    me.value = null
  } finally {
    loading.value = false
  }
}

async function loadMore() {
  // On a déjà tous les utilisateurs, on change juste l'affichage
  isExpanded.value = true
}

function loadLess() {
  isExpanded.value = false
}

watch(scope, () => load())
onMounted(() => load())
</script>

<style scoped>
.leaderboard-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  box-shadow: 0 2px 6px rgba(30,41,59,0.06);
  height: 689px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.leaderboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: .75rem;
}
.leaderboard-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 800;
  color: #1f2937;
  white-space: nowrap;
  hyphens: manual;
}
.leaderboard-tabs {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  background: #f3f4f6;
  border-radius: 8px;
  padding: 2px;
  gap: 8px;
  align-items: center;
}
.tab {
  background: transparent;
  border: none;
  padding: .4rem .7rem;
  border-radius: 6px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  white-space: nowrap; /* éviter "Glo-bal" ou "Ni-veau" */
  hyphens: manual;
  text-align: center;
}
.tab.active { background: #fff; color: #111827; box-shadow: 0 1px 2px rgba(0, 0, 0, .06); }
.tab:disabled { opacity: .5; cursor: not-allowed; }

.leaderboard-body { 
  margin-top: .75rem; 
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.leaderboard-content {
  flex: 1;
  overflow-y: auto;
  padding-right: 0.5rem;
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 #f1f5f9;
  -webkit-overflow-scrolling: touch;
}

.leaderboard-content::-webkit-scrollbar {
  width: 6px;
}

.leaderboard-content::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.leaderboard-content::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.leaderboard-content::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.me-item {
  margin-bottom: .75rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}
.me-rank { font-size: 1.25rem; font-weight: 800; color: #2563eb; }
.me-sub { color: #64748b; font-weight: 600; font-size: .85rem; }
.me-xp { font-weight: 800; color: #111827; }
.me-percent { color: #16a34a; font-weight: 700; font-size: .9rem; }

.leaderboard-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: .5rem; }
.leaderboard-item { display: grid; grid-template-columns: 70px 1fr max-content; align-items: center; gap: .75rem; padding: .55rem .75rem; border: 1px solid #e5e7eb; border-radius: 10px; }
.rank { font-weight: 800; color: #475569; text-align: center; }
.trophy { font-size: 1.25rem; }
.trophy.gold { filter: saturate(1.1); }
.trophy.silver { filter: grayscale(.2); }
.trophy.bronze { filter: saturate(.8); }
.user { display: flex; align-items: center; gap: .6rem; }
.avatar { width: 34px; height: 34px; border-radius: 50%; background: #eef2ff; color: #4f46e5; display:flex; align-items:center; justify-content:center; font-weight: 800; }
.info .name { font-weight: 700; color: #111827; display:flex; align-items:center; gap:.4rem; }
.info .name { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.info .name .first-name, .info .name .last-name { white-space: nowrap; }
.info .name .last-name { font-weight: 600; color:#1f2937; }
.name-flag { flex-shrink: 0; }
.info .meta { color: #64748b; font-size: .85rem; }
.flag { font-size: 1.1rem; }
.xp { font-weight: 800; color: #2563eb; white-space: nowrap; min-width: max-content; }

.empty-state { text-align: center; color: #64748b; padding: .75rem; }

.leaderboard-actions {
  margin-top: 1rem;
  text-align: center;
  flex-shrink: 0;
  border-top: 1px solid #f1f5f9;
  padding-top: 1rem;
}

.btn-see-more, .btn-see-less {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.btn-see-more {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-see-more:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
}

.btn-see-more:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-see-less {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-see-less:hover {
  background: #e5e7eb;
  transform: translateY(-1px);
}

.btn-text {
  font-size: 0.9rem;
}

/* Section étendue */
.expanded-section {
  margin-top: 1rem;
  border-top: 1px solid #e5e7eb;
  padding-top: 1rem;
  animation: slideDown 0.3s ease-out;
}

.expanded-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  padding: 0.5rem 0.75rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.expanded-title {
  font-weight: 600;
  color: #475569;
  font-size: 0.9rem;
}

.expanded-count {
  background: #e2e8f0;
  color: #475569;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
}

.expanded-item {
  background: #fafafa;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.expanded-item:hover {
  background: #f1f5f9;
}

/* Animation de déroulement */
@keyframes slideDown {
  from {
    opacity: 0;
    max-height: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    max-height: 400px;
    transform: translateY(0);
  }
}

.leaderboard-loading .skeleton { height: 44px; border-radius: 10px; background: linear-gradient(90deg, #f3f4f6, #e5e7eb, #f3f4f6); background-size: 200% 100%; animation: shimmer 1.2s infinite; margin-bottom: .5rem; }
.leaderboard-loading .skeleton.me { height: 64px; }

@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

@media (max-width: 520px) {
  .leaderboard-header { flex-wrap: wrap; row-gap: .5rem; }
  .leaderboard-title { flex: 1 1 100%; }
  /* Groupe de filtres centré et espacé uniformément */
  .leaderboard-tabs { 
    width: 100%; 
    display: grid; 
    grid-template-columns: repeat(3, 1fr);
    gap: 8px; 
    margin: 0 auto; 
    justify-items: stretch; 
    align-items: center; 
  }
  .tab { font-size: .9rem; padding: .35rem .55rem; text-align: center; }
  .leaderboard-item {
    grid-template-columns: 52px 1fr max-content;
  }
}

/* Sur mobile/tablettes: éviter un scroll interne qui bloque le scroll de page */
@media (max-width: 1000px) {
  .leaderboard-card { height: auto; }
  .leaderboard-content { overflow-y: visible; padding-right: 0; }
}

/* Casse progressive pour éviter toute 2e ligne */
@media (max-width: 1000px) {
  .leaderboard-item .info .name { font-size: 0.95rem; }
}

@media (max-width: 900px) {
  /* Cache le pays si l'espace est limité */
  .leaderboard-item .info .name .name-flag { display: none; }
}

@media (max-width: 820px) {
  /* Réduit la taille du nom */
  .leaderboard-item .info .name { font-size: 0.9rem; }
}

@media (max-width: 760px) {
  /* Cache le nom de famille pour garder une seule ligne */
  .leaderboard-item .info .name .last-name { display: none; }
}
</style>


