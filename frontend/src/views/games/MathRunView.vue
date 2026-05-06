<template>
  <div class="mr-page">
    <header class="mr-header">
      <router-link to="/dashboard" class="mr-back">
        <span class="mr-back-arrow">←</span>
        <span>Tableau de bord</span>
      </router-link>
      <div class="mr-header-title">
        <span class="mr-title-text">Math Run</span>
        <span class="mr-badge">BETA</span>
      </div>
      <div class="mr-header-spacer"></div>
    </header>

    <!-- Auth gate -->
    <div v-if="!userStore.isAuthenticated" class="mr-auth-gate">
      <div class="mr-gate-box">
        <div class="mr-gate-icon">∫</div>
        <h2 class="mr-gate-title">Connecte-toi pour jouer</h2>
        <p class="mr-gate-sub">
          Math Run est disponible gratuitement pour tous les comptes OptiTAB.
          Entraîne-toi, grimpe dans le classement et gagne des XP.
        </p>
        <router-link to="/login" class="mr-gate-btn">Se connecter</router-link>
      </div>
    </div>

    <!-- Game + side panel -->
    <template v-else>
      <div class="mr-canvas-wrapper">
        <div ref="gameContainer" class="mr-canvas-container"></div>
      </div>

      <!-- XP notification -->
      <transition name="xp-fade">
        <div v-if="xpFlash.visible" class="mr-xp-flash">
          <span class="mr-xp-icon">⚡</span>
          +{{ xpFlash.amount }} XP gagné{{ xpFlash.amount > 1 ? 's' : '' }} cette partie !
        </div>
      </transition>

      <!-- Leaderboard -->
      <div class="mr-leaderboard" v-if="leaderboard.length > 0">
        <div class="mr-lb-header">
          <span class="mr-lb-trophy">🏆</span>
          <h3 class="mr-lb-title">Meilleurs scores</h3>
        </div>

        <div class="mr-lb-cat-tabs">
          <button
            v-for="cat in lbCategories"
            :key="cat.key"
            class="mr-lb-tab"
            :class="{ active: lbCategory === cat.key }"
            @click="switchLeaderboard(cat.key)"
          >{{ cat.label }}</button>
        </div>

        <ol class="mr-lb-list">
          <li
            v-for="(entry, i) in leaderboard"
            :key="i"
            class="mr-lb-row"
            :class="{ 'mr-lb-me': entry.is_me }"
          >
            <span class="mr-lb-rank">
              <span v-if="i === 0">🥇</span>
              <span v-else-if="i === 1">🥈</span>
              <span v-else-if="i === 2">🥉</span>
              <span v-else class="mr-lb-rank-num">#{{ i + 1 }}</span>
            </span>
            <span class="mr-lb-name">{{ entry.first_name }}</span>
            <span class="mr-lb-score">{{ entry.score }}</span>
          </li>
        </ol>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import Phaser from 'phaser'
import { createPhaserConfig } from '@/games/math-run/config.js'
import { useUserStore } from '@/stores/user'
import { useXP } from '@/composables/useXP'
import { submitMathRunScore, getMathRunLeaderboard } from '@/games/math-run/api.js'

const userStore = useUserStore()
const { updateUserXPInstantly } = useXP()
const gameContainer = ref(null)
let game = null

const xpFlash = ref({ visible: false, amount: 0 })
let xpEarned  = 0

const leaderboard  = ref([])
const lbCategory   = ref('all')
const lbCategories = [
  { key: 'all',            label: '∞'    },
  { key: 'addition',       label: '+'    },
  { key: 'subtraction',    label: '−'    },
  { key: 'multiplication', label: '×'    },
  { key: 'division',       label: '÷'    },
  { key: 'limits',         label: 'lim'  },
  { key: 'derivatives',    label: 'd/dx' },
  { key: 'integrals',      label: '∫'    },
  { key: 'sequences',      label: 'uₙ'   },
]

async function loadLeaderboard(category = 'all') {
  const res = await getMathRunLeaderboard(category, 10)
  if (!res?.data?.leaderboard) return
  leaderboard.value = res.data.leaderboard.map(e => ({
    ...e,
    is_me: e.user_id === userStore.id,
  }))
}

async function switchLeaderboard(category) {
  lbCategory.value = category
  await loadLeaderboard(category)
}

function handleCorrectAnswer() {
  if (!userStore.isAuthenticated) return
  xpEarned++
  updateUserXPInstantly(1, 'math_run')
}

async function handleGameOver(event) {
  const { score, category } = event.detail
  submitMathRunScore(score, category)
  if (userStore.isAuthenticated && xpEarned > 0) {
    xpFlash.value = { visible: true, amount: xpEarned }
    setTimeout(() => { xpFlash.value.visible = false }, 3500)
    xpEarned = 0
    await loadLeaderboard(lbCategory.value)
  } else {
    xpEarned = 0
  }
}

onMounted(async () => {
  window.addEventListener('mathrun:gameover', handleGameOver)
  window.addEventListener('mathrun:correct',  handleCorrectAnswer)
  if (!userStore.isAuthenticated) return
  await nextTick()
  if (!gameContainer.value) return
  const config = createPhaserConfig(gameContainer.value)
  game = new Phaser.Game(config)
  await loadLeaderboard('all')
})

onUnmounted(() => {
  window.removeEventListener('mathrun:gameover', handleGameOver)
  window.removeEventListener('mathrun:correct',  handleCorrectAnswer)
  if (game) { game.destroy(true); game = null }
})
</script>

<style scoped>
/* ── Page layout ── */
.mr-page {
  min-height: 100vh;
  background: #040d1a;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-bottom: 48px;
}

/* ── Header ── */
.mr-header {
  width: 100%;
  max-width: 480px;
  display: flex;
  align-items: center;
  padding: 10px 16px;
  border-bottom: 1px solid rgba(30, 58, 138, 0.4);
  background: rgba(4, 13, 26, 0.95);
  position: sticky;
  top: 0;
  z-index: 10;
}

.mr-back {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #334155;
  text-decoration: none;
  font-size: 13px;
  transition: color 0.2s;
  flex: 1;
}
.mr-back:hover { color: #64748b; }
.mr-back-arrow { font-size: 14px; }

.mr-header-title {
  display: flex;
  align-items: center;
  gap: 8px;
}
.mr-title-text {
  color: #ffd54f;
  font-size: 17px;
  font-weight: 700;
  letter-spacing: 0.02em;
}
.mr-badge {
  background: rgba(29, 78, 216, 0.6);
  border: 1px solid rgba(59, 130, 246, 0.4);
  color: #93c5fd;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 20px;
  letter-spacing: 0.08em;
}
.mr-header-spacer { flex: 1; }

/* ── Auth gate ── */
.mr-auth-gate {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 20px;
}
.mr-gate-box {
  background: #080f24;
  border: 1px solid rgba(30, 58, 138, 0.6);
  border-radius: 20px;
  padding: 44px 36px;
  text-align: center;
  max-width: 360px;
}
.mr-gate-icon {
  font-size: 52px;
  color: #3b82f6;
  margin-bottom: 20px;
  display: block;
  font-family: Arial, sans-serif;
  font-weight: bold;
}
.mr-gate-title {
  color: #e2e8f0;
  font-size: 20px;
  font-weight: 700;
  margin: 0 0 12px;
}
.mr-gate-sub {
  color: #475569;
  font-size: 14px;
  margin: 0 0 28px;
  line-height: 1.6;
}
.mr-gate-btn {
  display: inline-block;
  background: #2563eb;
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  padding: 13px 36px;
  border-radius: 12px;
  text-decoration: none;
  transition: background 0.2s, transform 0.1s;
}
.mr-gate-btn:hover {
  background: #1d4ed8;
  transform: translateY(-1px);
}

/* ── Canvas ── */
.mr-canvas-wrapper {
  width: 100%;
  max-width: 480px;
  display: flex;
  justify-content: center;
}
.mr-canvas-container {
  width: 100%;
  height: min(700px, calc(100vw * 700 / 480));
}

/* ── XP flash ── */
.mr-xp-flash {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(20, 83, 45, 0.9);
  border: 1px solid rgba(34, 197, 94, 0.6);
  color: #4ade80;
  font-size: 14px;
  font-weight: 700;
  padding: 11px 22px;
  border-radius: 12px;
  margin-top: 14px;
}
.mr-xp-icon { font-size: 16px; }
.xp-fade-enter-active, .xp-fade-leave-active { transition: opacity 0.4s, transform 0.4s; }
.xp-fade-enter-from, .xp-fade-leave-to { opacity: 0; transform: translateY(6px); }

/* ── Leaderboard ── */
.mr-leaderboard {
  width: 100%;
  max-width: 480px;
  margin-top: 24px;
  padding: 0 16px;
}

.mr-lb-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 14px;
}
.mr-lb-trophy { font-size: 18px; }
.mr-lb-title {
  color: #e2e8f0;
  font-size: 15px;
  font-weight: 700;
  margin: 0;
}

.mr-lb-cat-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  justify-content: flex-start;
  margin-bottom: 14px;
}
.mr-lb-tab {
  background: #080f24;
  border: 1px solid rgba(30, 58, 138, 0.5);
  color: #334155;
  font-size: 12px;
  font-weight: 700;
  padding: 0 11px;
  height: 30px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
  font-family: inherit;
}
.mr-lb-tab:hover { color: #64748b; border-color: rgba(30, 58, 138, 0.8); }
.mr-lb-tab.active {
  background: rgba(30, 58, 138, 0.5);
  border-color: rgba(59, 130, 246, 0.7);
  color: #93c5fd;
}

.mr-lb-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.mr-lb-row {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #080f24;
  border: 1px solid rgba(30, 58, 138, 0.4);
  border-radius: 10px;
  padding: 10px 14px;
  transition: border-color 0.15s;
}
.mr-lb-row:hover { border-color: rgba(30, 58, 138, 0.7); }
.mr-lb-row.mr-lb-me {
  border-color: rgba(255, 213, 79, 0.5);
  background: rgba(120, 53, 15, 0.2);
}
.mr-lb-rank {
  font-size: 17px;
  min-width: 30px;
  text-align: center;
}
.mr-lb-rank-num {
  font-size: 12px;
  color: #334155;
  font-weight: 600;
}
.mr-lb-name { color: #94a3b8; font-size: 14px; flex: 1; font-weight: 500; }
.mr-lb-row.mr-lb-me .mr-lb-name { color: #e2e8f0; font-weight: 600; }
.mr-lb-score {
  color: #ffd54f;
  font-size: 15px;
  font-weight: 700;
  min-width: 28px;
  text-align: right;
}
</style>
