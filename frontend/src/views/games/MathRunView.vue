<template>
  <div class="math-run-page">
    <header class="mr-header">
      <router-link to="/dashboard" class="mr-back">← Tableau de bord</router-link>
      <h1 class="mr-title">Math Run</h1>
      <span class="mr-badge">BETA</span>
    </header>

    <!-- Auth gate -->
    <div v-if="!userStore.isAuthenticated" class="mr-auth-gate">
      <div class="mr-gate-box">
        <div class="mr-gate-icon">🎮</div>
        <h2 class="mr-gate-title">Connecte-toi pour jouer</h2>
        <p class="mr-gate-sub">Math Run est disponible pour tous les comptes OptiTAB, gratuitement.</p>
        <router-link to="/login" class="mr-gate-btn">Se connecter</router-link>
      </div>
    </div>

    <!-- Game canvas -->
    <template v-else>
      <div class="mr-canvas-wrapper">
        <div ref="gameContainer" class="mr-canvas-container"></div>
      </div>

      <!-- XP notification -->
      <transition name="xp-fade">
        <div v-if="xpFlash.visible" class="mr-xp-flash">
          +{{ xpFlash.amount }} XP gagné{{ xpFlash.amount > 1 ? 's' : '' }} cette partie !
        </div>
      </transition>

      <!-- Leaderboard panel -->
      <div class="mr-leaderboard" v-if="leaderboard.length > 0">
        <h3 class="mr-lb-title">🏆 Meilleurs scores</h3>
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
          <li v-for="(entry, i) in leaderboard" :key="i" class="mr-lb-row" :class="{ 'mr-lb-me': entry.is_me }">
            <span class="mr-lb-rank">{{ i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : `#${i + 1}` }}</span>
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

// XP tracking
const xpFlash = ref({ visible: false, amount: 0 })
let xpEarned = 0

// Leaderboard
const leaderboard = ref([])
const lbCategory = ref('all')
const lbCategories = [
  { key: 'all',            label: '∞'   },
  { key: 'addition',       label: '+'   },
  { key: 'subtraction',    label: '−'   },
  { key: 'multiplication', label: '×'   },
  { key: 'division',       label: '÷'   },
  { key: 'limits',         label: 'lim' },
  { key: 'derivatives',    label: "d/dx"},
  { key: 'integrals',      label: '∫'   },
  { key: 'sequences',      label: 'uₙ'  },
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

  // Submit score to leaderboard API (silent)
  submitMathRunScore(score, category)

  // Show total XP earned during this game (already awarded per-answer)
  if (userStore.isAuthenticated && xpEarned > 0) {
    xpFlash.value = { visible: true, amount: xpEarned }
    setTimeout(() => { xpFlash.value.visible = false }, 3000)
    xpEarned = 0

    // Refresh leaderboard
    await loadLeaderboard(lbCategory.value)
  } else {
    xpEarned = 0
  }
}

onMounted(async () => {
  window.addEventListener('mathrun:gameover', handleGameOver)
  window.addEventListener('mathrun:correct', handleCorrectAnswer)

  if (!userStore.isAuthenticated) return

  await nextTick()
  if (!gameContainer.value) return
  const config = createPhaserConfig(gameContainer.value)
  game = new Phaser.Game(config)

  // Load initial leaderboard
  await loadLeaderboard('all')
})

onUnmounted(() => {
  window.removeEventListener('mathrun:gameover', handleGameOver)
  window.removeEventListener('mathrun:correct', handleCorrectAnswer)
  if (game) {
    game.destroy(true)
    game = null
  }
})
</script>

<style scoped>
.math-run-page {
  min-height: 100vh;
  background: #060e1e;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-bottom: 40px;
}

.mr-header {
  width: 100%;
  max-width: 480px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px 8px;
}

.mr-back {
  color: #60a5fa;
  text-decoration: none;
  font-size: 13px;
  white-space: nowrap;
  transition: color 0.2s;
}
.mr-back:hover { color: #93c5fd; }

.mr-title {
  color: #ffd54f;
  font-size: 19px;
  font-weight: 700;
  margin: 0;
  flex: 1;
  text-align: center;
}

.mr-badge {
  background: #1d4ed8;
  color: #bfdbfe;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 20px;
  letter-spacing: 0.05em;
}

/* ── Auth gate ── */
.mr-auth-gate {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 16px;
}
.mr-gate-box {
  background: #0f1e3f;
  border: 1px solid #1e3a8a;
  border-radius: 16px;
  padding: 40px 32px;
  text-align: center;
  max-width: 360px;
}
.mr-gate-icon { font-size: 48px; margin-bottom: 16px; }
.mr-gate-title {
  color: #e2e8f0;
  font-size: 20px;
  font-weight: 700;
  margin: 0 0 12px;
}
.mr-gate-sub {
  color: #64748b;
  font-size: 14px;
  margin: 0 0 24px;
  line-height: 1.5;
}
.mr-gate-btn {
  display: inline-block;
  background: #2563eb;
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  padding: 12px 32px;
  border-radius: 10px;
  text-decoration: none;
  transition: background 0.2s;
}
.mr-gate-btn:hover { background: #1d4ed8; }

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
  background: #14532d;
  border: 1px solid #22c55e;
  color: #4ade80;
  font-size: 15px;
  font-weight: 700;
  padding: 10px 24px;
  border-radius: 12px;
  margin-top: 12px;
}
.xp-fade-enter-active, .xp-fade-leave-active { transition: opacity 0.4s; }
.xp-fade-enter-from, .xp-fade-leave-to { opacity: 0; }

/* ── Leaderboard ── */
.mr-leaderboard {
  width: 100%;
  max-width: 480px;
  margin-top: 24px;
  padding: 0 16px;
}
.mr-lb-title {
  color: #e2e8f0;
  font-size: 16px;
  font-weight: 700;
  margin: 0 0 12px;
  text-align: center;
}
.mr-lb-cat-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  justify-content: center;
  margin-bottom: 12px;
}
.mr-lb-tab {
  background: #0f1e3f;
  border: 1px solid #1e3a8a;
  color: #64748b;
  font-size: 12px;
  font-weight: 700;
  padding: 0 10px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}
.mr-lb-tab.active {
  background: #1e3a8a;
  border-color: #3b82f6;
  color: #93c5fd;
}
.mr-lb-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.mr-lb-row {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #0c1a38;
  border: 1px solid #1e3a8a;
  border-radius: 8px;
  padding: 10px 14px;
}
.mr-lb-row.mr-lb-me {
  border-color: #ffd54f;
  background: #1a2a10;
}
.mr-lb-rank { font-size: 18px; min-width: 32px; }
.mr-lb-name { color: #e2e8f0; font-size: 14px; flex: 1; }
.mr-lb-score { color: #ffd54f; font-size: 16px; font-weight: 700; }
</style>
