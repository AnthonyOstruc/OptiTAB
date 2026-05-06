<template>
  <div class="math-run-page">
    <header class="mr-header">
      <router-link to="/dashboard" class="mr-back">← Tableau de bord</router-link>
      <h1 class="mr-title">Math Run</h1>
      <span class="mr-badge">BETA</span>
    </header>

    <div class="mr-canvas-wrapper">
      <div ref="gameContainer" class="mr-canvas-container"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Phaser from 'phaser'
import { createPhaserConfig } from '@/games/math-run/config.js'

const gameContainer = ref(null)
let game = null

onMounted(() => {
  if (!gameContainer.value) return
  const config = createPhaserConfig(gameContainer.value)
  game = new Phaser.Game(config)
})

onUnmounted(() => {
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
  padding-bottom: 24px;
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

.mr-back:hover {
  color: #93c5fd;
}

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

.mr-canvas-wrapper {
  width: 100%;
  max-width: 480px;
  display: flex;
  justify-content: center;
}

.mr-canvas-container {
  width: 100%;
  /* Give Phaser a parent with a defined height so Scale.FIT works correctly.
     On desktop cap at 700px; on narrow screens use the viewport-proportional height. */
  height: min(700px, calc(100vw * 700 / 480));
}
</style>
