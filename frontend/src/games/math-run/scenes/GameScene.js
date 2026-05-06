import Phaser from 'phaser'
import { getRandomQuestion } from '../data/questions.js'
import { sfx } from '../audio.js'

const C = {
  LANE: [0x152a6b, 0x1e3a8a, 0x1a3070],
  DIVIDER: 0x3b82f6,
  HUD_BG: 0x060e1e,
  Q_BG: 0x162a60,
  Q_BORDER: 0x2563eb,
  ANSWER_BG: 0x1d4ed8,
  ANSWER_BORDER: 0x60a5fa,
  PLAYER_BODY: 0xffd54f,
  PLAYER_HEAD: 0xffca28,
  PLAYER_SHOES: 0x263238,
  STRIPE: 0xffffff,
  CORRECT: 0x22c55e,
  WRONG: 0xef4444,
  HEART: 0xff5252,
  TEXT: 0xffffff,
}

const HUD_H = 52
const Q_H = 62
const GAME_TOP = HUD_H + Q_H
const PLAYER_OFFSET_FROM_BOTTOM = 140
const MOBILE_BTN_OFFSET = 52

// Speed tiers: [minScore, fallDuration, stripeSpeed]
const SPEED_TIERS = [
  [0,  2800, 65],
  [5,  2300, 90],
  [10, 1900, 120],
  [15, 1500, 155],
  [20, 1200, 190],
]

export default class GameScene extends Phaser.Scene {
  constructor() {
    super({ key: 'GameScene' })
  }

  init(data) {
    this.score = 0
    this.lives = 3
    this.currentLane = 1
    this.isEvaluating = false
    this.answerBlocks = []
    this.blockTweens = []
    this.playerPos = { x: 0 }
    this.currentTier = 0
    this.runTick = 0
    this.streak = 0
    this.category = data?.category || 'all'
    this.isPaused = false
  }

  create() {
    const W = this.scale.width
    const H = this.scale.height
    this.W = W
    this.H = H
    this.laneW = W / 3
    this.laneX = [W / 6, W / 2, (5 * W) / 6]
    this.playerY = H - PLAYER_OFFSET_FROM_BOTTOM
    this.blockStartY = GAME_TOP + 30
    this.blockTargetY = this.playerY - 30
    this.playerPos.x = this.laneX[1]

    this._buildLanes()
    this._buildStripes()
    this._buildHUD()
    this._buildQuestionPanel()
    this._buildPlayer()
    this._buildMobileControls()
    this._bindKeys()
    this._buildPauseOverlay()

    this.input.keyboard.on('keydown-ESC', () => this._togglePause())
    this.input.keyboard.on('keydown-P',   () => this._togglePause())

    this.time.delayedCall(400, () => this._nextQuestion())
  }

  // ─── Lane backgrounds ──────────────────────────────────────────────────────
  _buildLanes() {
    for (let i = 0; i < 3; i++) {
      this.add.rectangle(this.laneX[i], this.H / 2, this.laneW, this.H, C.LANE[i])
    }
    for (let i = 1; i < 3; i++) {
      this.add.rectangle(this.laneW * i, this.H / 2, 2, this.H, C.DIVIDER, 0.35)
    }
  }

  // ─── Scrolling stripes (running feel) ─────────────────────────────────────
  _buildStripes() {
    this.stripes = []
    const stripeH = 80
    const gameAreaH = this.H - GAME_TOP
    const count = Math.ceil(gameAreaH / stripeH) + 2

    for (let lane = 0; lane < 3; lane++) {
      for (let row = 0; row < count; row++) {
        if (row % 2 === 0) {
          const stripe = this.add.rectangle(
            this.laneX[lane],
            GAME_TOP + row * stripeH,
            this.laneW - 6,
            stripeH * 0.45,
            C.STRIPE,
            0.04
          )
          this.stripes.push(stripe)
        }
      }
    }
    this.stripeSpeed = 65
    this.stripeLoopH = this.H - GAME_TOP + stripeH
  }

  // ─── HUD (score + lives) ──────────────────────────────────────────────────
  _buildHUD() {
    this.add.rectangle(this.W / 2, HUD_H / 2, this.W, HUD_H, C.HUD_BG).setDepth(10)

    this.scoreTxt = this.add
      .text(14, 8, 'Score : 0', {
        fontSize: '17px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#e2e8f0',
        fontStyle: 'bold',
      })
      .setDepth(11)

    this.streakTxt = this.add
      .text(14, 29, '', {
        fontSize: '12px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#fbbf24',
        fontStyle: 'bold',
      })
      .setDepth(11)
      .setAlpha(0)

    this.livesTxt = this.add
      .text(this.W - 14, 12, '♥  ♥  ♥', {
        fontSize: '19px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#ff5252',
      })
      .setOrigin(1, 0)
      .setDepth(11)

    // Category icon (center of HUD bar, only for non-mixed modes)
    const catIcon  = { addition: '+', subtraction: '−', multiplication: '×', division: '÷' }
    const catColor = { addition: '#4ade80', subtraction: '#fbbf24', multiplication: '#c4b5fd', division: '#67e8f9' }
    if (this.category !== 'all') {
      this.add
        .text(this.W / 2, HUD_H / 2, catIcon[this.category] || '', {
          fontSize: '21px',
          fontFamily: 'Arial',
          color: catColor[this.category] || '#93c5fd',
          fontStyle: 'bold',
        })
        .setOrigin(0.5)
        .setDepth(11)
    }
  }

  // ─── Question panel ────────────────────────────────────────────────────────
  _buildQuestionPanel() {
    const panelY = HUD_H + Q_H / 2
    this.add.rectangle(this.W / 2, panelY, this.W, Q_H, C.Q_BG).setDepth(10)
    this.add.rectangle(this.W / 2, HUD_H, this.W, 2, C.Q_BORDER, 0.7).setDepth(11)
    this.add.rectangle(this.W / 2, HUD_H + Q_H, this.W, 2, C.Q_BORDER, 0.4).setDepth(11)

    this.questionTxt = this.add
      .text(this.W / 2, panelY, '', {
        fontSize: '24px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#ffffff',
        fontStyle: 'bold',
      })
      .setOrigin(0.5)
      .setDepth(11)
  }

  // ─── Player character (drawn with Graphics) ───────────────────────────────
  _buildPlayer() {
    this.playerGfx = this.add.graphics().setDepth(15)
    this._drawPlayer()

    this.laneBar = this.add
      .rectangle(this.laneX[1], this.playerY + 48, this.laneW - 16, 6, C.Q_BORDER)
      .setAlpha(0.7)
      .setDepth(14)
  }

  _drawPlayer() {
    const g = this.playerGfx
    g.clear()
    const x = this.playerPos.x
    const y = this.playerY

    const t = this.runTick * Math.PI * 2
    const bounce  = Math.abs(Math.sin(t * 2)) * 2.5  // body up/down 2.5 px
    const legSwing = Math.sin(t) * 9                  // shoes forward/back 9 px
    const armSwing = Math.sin(t + Math.PI) * 7        // arms opposite phase

    // ── Legs (thighs then shoes, drawn behind body) ───────────────────────────
    g.fillStyle(0xe6a800, 1)                           // slightly darker than body
    g.fillRoundedRect(x - 13, y + 19 - bounce, 11, 17, 3)  // left thigh
    g.fillRoundedRect(x + 2,  y + 19 - bounce, 11, 17, 3)  // right thigh

    g.fillStyle(C.PLAYER_SHOES, 1)
    g.fillRoundedRect(x - 17 + legSwing, y + 32 - bounce, 14, 9, 4)   // left shoe
    g.fillRoundedRect(x + 3  - legSwing, y + 32 - bounce, 14, 9, 4)   // right shoe

    // ── Body ─────────────────────────────────────────────────────────────────
    g.fillStyle(C.PLAYER_BODY, 1)
    g.fillRoundedRect(x - 13, y - 18 - bounce, 26, 38, 6)

    // ── Arms ─────────────────────────────────────────────────────────────────
    g.fillStyle(C.PLAYER_HEAD, 1)
    g.fillRoundedRect(x - 20, y - 12 - bounce + armSwing,  8, 20, 4)  // left arm
    g.fillRoundedRect(x + 12, y - 12 - bounce - armSwing,  8, 20, 4)  // right arm

    // ── Head ─────────────────────────────────────────────────────────────────
    g.fillStyle(C.PLAYER_HEAD, 1)
    g.fillCircle(x, y - 34 - bounce, 17)

    // ── Eyes ─────────────────────────────────────────────────────────────────
    g.fillStyle(0x1a237e, 1)
    g.fillCircle(x - 6, y - 36 - bounce, 5)
    g.fillCircle(x + 6, y - 36 - bounce, 5)

    g.fillStyle(0xffffff, 1)
    g.fillCircle(x - 5, y - 38 - bounce, 2)
    g.fillCircle(x + 7, y - 38 - bounce, 2)
  }

  // ─── Mobile controls ──────────────────────────────────────────────────────
  _buildMobileControls() {
    const y = this.H - MOBILE_BTN_OFFSET
    const btnW = 80
    const btnH = 52

    this._makeBtn(this.W * 0.08, y, btnW, btnH, '◀', () => this._moveLeft())
    this._makeBtn(this.W / 2,    y, 58,   btnH, '⏸', () => this._togglePause())
    this._makeBtn(this.W * 0.92, y, btnW, btnH, '▶', () => this._moveRight())
  }

  _makeBtn(x, y, w, h, label, callback) {
    const bg = this.add.graphics().setDepth(20)
    const draw = (pressed) => {
      bg.clear()
      bg.fillStyle(pressed ? C.Q_BORDER : C.Q_BG, pressed ? 1 : 0.85)
      bg.fillRoundedRect(x - w / 2, y - h / 2, w, h, 12)
      bg.lineStyle(2, C.ANSWER_BORDER, 0.6)
      bg.strokeRoundedRect(x - w / 2, y - h / 2, w, h, 12)
    }
    draw(false)

    const btn = this.add
      .text(x, y, label, {
        fontSize: '26px',
        fontFamily: 'Arial',
        color: '#93c5fd',
      })
      .setOrigin(0.5)
      .setDepth(21)
      .setInteractive({ useHandCursor: true })

    btn.on('pointerdown', () => { draw(true); callback() })
    btn.on('pointerup', () => draw(false))
    btn.on('pointerout', () => draw(false))
  }

  // ─── Keyboard ─────────────────────────────────────────────────────────────
  _bindKeys() {
    this.input.keyboard.on('keydown-LEFT', () => this._moveLeft())
    this.input.keyboard.on('keydown-RIGHT', () => this._moveRight())
    this.input.keyboard.on('keydown-A', () => this._moveLeft())
    this.input.keyboard.on('keydown-D', () => this._moveRight())
  }

  // ─── Lane movement ─────────────────────────────────────────────────────────
  _moveLeft() {
    if (this.isEvaluating || this.currentLane <= 0) return
    this.currentLane--
    sfx.laneSwitch()
    this._animatePlayerToLane()
  }

  _moveRight() {
    if (this.isEvaluating || this.currentLane >= 2) return
    this.currentLane++
    sfx.laneSwitch()
    this._animatePlayerToLane()
  }

  _animatePlayerToLane() {
    const targetX = this.laneX[this.currentLane]
    this.tweens.killTweensOf(this.playerPos)
    this.tweens.add({ targets: this.playerPos, x: targetX, duration: 150, ease: 'Power2' })
    this.tweens.add({ targets: this.laneBar,   x: targetX, duration: 150, ease: 'Power2' })
  }

  // ─── Speed / difficulty ────────────────────────────────────────────────────
  _getTier() {
    for (let i = SPEED_TIERS.length - 1; i >= 0; i--) {
      if (this.score >= SPEED_TIERS[i][0]) return i
    }
    return 0
  }

  _getFallDuration() {
    return SPEED_TIERS[this._getTier()][1]
  }

  _updateSpeed() {
    const tier = this._getTier()
    if (tier <= this.currentTier) return
    this.currentTier = tier
    this.stripeSpeed = SPEED_TIERS[tier][2]
    sfx.speedUp()
    this._showSpeedUp()
  }

  _showSpeedUp() {
    const msg = this.add
      .text(this.W / 2, this.H * 0.38, '⚡ VITESSE +', {
        fontSize: '22px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#fbbf24',
        fontStyle: 'bold',
        stroke: '#000c1a',
        strokeThickness: 3,
      })
      .setOrigin(0.5)
      .setAlpha(0)
      .setDepth(22)

    this.tweens.add({
      targets: msg,
      alpha: 1,
      y: this.H * 0.32,
      duration: 300,
      hold: 700,
      yoyo: true,
      onComplete: () => msg.destroy(),
    })
  }

  // ─── Question / answer flow ────────────────────────────────────────────────
  _nextQuestion() {
    if (this.isEvaluating) return
    this._updateSpeed()

    const q = getRandomQuestion(this.category)
    this.currentQuestion = q

    this.questionTxt.setAlpha(0).setText(q.question)
    this.tweens.add({ targets: this.questionTxt, alpha: 1, duration: 250 })

    this._spawnBlocks(q)
  }

  _spawnBlocks(q) {
    this._clearBlocks()
    const bW = this.laneW - 22
    const bH = 52
    const fallDuration = this._getFallDuration()

    for (let i = 0; i < 3; i++) {
      const container = this.add.container(this.laneX[i], this.blockStartY).setDepth(12)

      const bg = this.add.graphics()
      bg.fillStyle(C.ANSWER_BG, 1)
      bg.fillRoundedRect(-bW / 2, -bH / 2, bW, bH, 10)
      bg.lineStyle(2, C.ANSWER_BORDER, 0.7)
      bg.strokeRoundedRect(-bW / 2, -bH / 2, bW, bH, 10)

      const txt = this.add
        .text(0, 0, String(q.answers[i]), {
          fontSize: '21px',
          fontFamily: "'Segoe UI', Arial, sans-serif",
          color: '#ffffff',
          fontStyle: 'bold',
        })
        .setOrigin(0.5)

      container.add([bg, txt])

      const tween = this.tweens.add({
        targets: container,
        y: this.blockTargetY,
        duration: fallDuration,
        ease: 'Linear',
        onComplete: () => {
          if (!this.isEvaluating) this._evaluate()
        },
      })

      this.answerBlocks.push({ container, answer: q.answers[i] })
      this.blockTweens.push(tween)
    }
  }

  _clearBlocks() {
    this.blockTweens.forEach(t => { if (t?.isPlaying?.()) t.stop() })
    this.answerBlocks.forEach(b => b.container?.destroy())
    this.answerBlocks = []
    this.blockTweens = []
  }

  // ─── Answer evaluation ─────────────────────────────────────────────────────
  _evaluate() {
    if (this.isEvaluating) return
    this.isEvaluating = true

    this.blockTweens.forEach(t => { if (t?.isPlaying?.()) t.stop() })

    const selected = this.answerBlocks[this.currentLane]
    const correct = selected && String(selected.answer) === String(this.currentQuestion.correctAnswer)

    if (correct) {
      this.streak++
      const mult = this._getMultiplier()
      this.score += mult
      this.scoreTxt.setText('Score : ' + this.score)
      this._updateStreakDisplay()
      if (this.streak === 3 || this.streak === 5 || this.streak === 10) {
        this.time.delayedCall(220, () => this._showCombo(this.streak))
        this._emitParticles(this.W / 2, this.H * 0.5, C.PLAYER_BODY, 22)
      }
      if (mult > 1) this._showBonus(mult)
    } else {
      this.streak = 0
      this._updateStreakDisplay()
      this.lives--
      this._updateHearts()
    }

    // Sound: game-over tone takes priority over wrong buzz so they don't overlap
    if (correct) {
      sfx.correct()
    } else if (this.lives <= 0) {
      sfx.gameOver()
    } else {
      sfx.wrong()
    }

    this._showFeedback(correct)

    if (this.lives <= 0) {
      this.time.delayedCall(1300, () => {
        this.scene.start('GameOverScene', { score: this.score, category: this.category })
      })
    } else {
      this.time.delayedCall(1100, () => {
        this._clearBlocks()
        this.isEvaluating = false
        this._nextQuestion()
      })
    }
  }

  // ─── Particle burst ───────────────────────────────────────────────────────
  _emitParticles(cx, cy, color, count = 14) {
    for (let i = 0; i < count; i++) {
      const angle  = (i / count) * Math.PI * 2 + Math.random() * 0.4
      const speed  = 55 + Math.random() * 90
      const radius = 3 + Math.random() * 5
      const delay  = Math.random() * 60

      const dot = this.add.circle(cx, cy, radius, color).setDepth(25).setAlpha(0.95)

      this.tweens.add({
        targets: dot,
        x: cx + Math.cos(angle) * speed,
        y: cy + Math.sin(angle) * speed - 18,
        alpha: 0,
        scaleX: 0.15,
        scaleY: 0.15,
        delay,
        duration: 420 + Math.random() * 200,
        ease: 'Power2.easeOut',
        onComplete: () => dot.destroy(),
      })
    }
  }

  _showFeedback(correct) {
    if (correct) {
      this._emitParticles(this.playerPos.x, this.playerY - 20, C.CORRECT, 16)
      this._emitParticles(this.playerPos.x, this.playerY - 20, C.PLAYER_BODY, 8)
    }

    const color = correct ? C.CORRECT : C.WRONG
    const W = this.W
    const H = this.H

    // Screen flash
    const flash = this.add.rectangle(W / 2, H / 2, W, H, color, 0).setDepth(18)
    this.tweens.add({
      targets: flash,
      alpha: correct ? 0.18 : 0.28,
      yoyo: true,
      duration: 280,
      onComplete: () => flash.destroy(),
    })

    // Feedback label
    const label = correct ? '✓  Correct !' : '✗  Incorrect'
    const labelColor = correct ? '#4ade80' : '#f87171'
    const msg = this.add
      .text(W / 2, H / 2 - 40, label, {
        fontSize: '32px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: labelColor,
        fontStyle: 'bold',
        stroke: '#000c1a',
        strokeThickness: 3,
      })
      .setOrigin(0.5)
      .setAlpha(0)
      .setDepth(19)

    this.tweens.add({
      targets: msg,
      alpha: 1,
      y: H / 2 - 70,
      duration: 280,
      hold: 500,
      yoyo: true,
      onComplete: () => msg.destroy(),
    })

    // Highlight selected block
    const selBlock = this.answerBlocks[this.currentLane]
    if (selBlock) {
      const bx = selBlock.container.x
      const by = selBlock.container.y
      const bW = this.laneW - 22
      const hl = this.add.graphics().setDepth(13)
      hl.fillStyle(color, 0.45)
      hl.fillRoundedRect(bx - bW / 2, by - 26, bW, 52, 10)
      this.time.delayedCall(900, () => hl.destroy())
    }

    // Show correct answer if wrong
    if (!correct) {
      const correctIdx = this.answerBlocks.findIndex(
        b => String(b.answer) === String(this.currentQuestion.correctAnswer)
      )
      if (correctIdx !== -1) {
        const cb = this.answerBlocks[correctIdx]
        const cbW = this.laneW - 22
        const correctHl = this.add.graphics().setDepth(13)
        correctHl.fillStyle(C.CORRECT, 0.35)
        correctHl.fillRoundedRect(cb.container.x - cbW / 2, cb.container.y - 26, cbW, 52, 10)
        this.time.delayedCall(900, () => correctHl.destroy())
      }
    }
  }

  _updateHearts() {
    const hearts = Array(Math.max(this.lives, 0)).fill('♥').join('  ')
    this.livesTxt.setText(hearts || '—')
  }

  // ─── Pause system ─────────────────────────────────────────────────────────
  _buildPauseOverlay() {
    const W = this.W
    const H = this.H
    const panelW = 284
    const panelH = 196
    const panelX = W / 2 - panelW / 2
    const panelY = H / 2 - panelH / 2

    this.pauseBg = this.add.rectangle(W / 2, H / 2, W, H, 0x000000, 0.72).setDepth(30)

    this.pausePanel = this.add.graphics().setDepth(31)
    this.pausePanel.fillStyle(0x0c1a38, 1)
    this.pausePanel.fillRoundedRect(panelX, panelY, panelW, panelH, 16)
    this.pausePanel.lineStyle(2, 0x2563eb, 0.9)
    this.pausePanel.strokeRoundedRect(panelX, panelY, panelW, panelH, 16)

    this.pauseTitle = this.add
      .text(W / 2, H / 2 - 67, '⏸  PAUSE', {
        fontSize: '22px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#e2e8f0',
        fontStyle: 'bold',
      })
      .setOrigin(0.5)
      .setDepth(32)

    // Resume button
    this.resumeBg = this.add.graphics().setDepth(32)
    const resumeY = H / 2 - 12
    this._drawPauseBtn(this.resumeBg, W / 2, resumeY, 228, 48, false)
    this.resumeBtn = this.add
      .text(W / 2, resumeY, '▶  Reprendre', {
        fontSize: '18px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#ffffff',
        fontStyle: 'bold',
      })
      .setOrigin(0.5)
      .setDepth(33)
      .setInteractive({ useHandCursor: true })
    this.resumeBtn.on('pointerover', () => this._drawPauseBtn(this.resumeBg, W / 2, resumeY, 228, 48, true))
    this.resumeBtn.on('pointerout',  () => this._drawPauseBtn(this.resumeBg, W / 2, resumeY, 228, 48, false))
    this.resumeBtn.on('pointerdown', () => this._resumeGame())

    // Change category button
    this.menuBg = this.add.graphics().setDepth(32)
    const menuY = H / 2 + 50
    this._drawMenuBtn(this.menuBg, W / 2, menuY, 228, 42, false)
    this.menuBtn = this.add
      .text(W / 2, menuY, '≡  Changer de catégorie', {
        fontSize: '15px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#93c5fd',
      })
      .setOrigin(0.5)
      .setDepth(33)
      .setInteractive({ useHandCursor: true })
    this.menuBtn.on('pointerover', () => this._drawMenuBtn(this.menuBg, W / 2, menuY, 228, 42, true))
    this.menuBtn.on('pointerout',  () => this._drawMenuBtn(this.menuBg, W / 2, menuY, 228, 42, false))
    this.menuBtn.on('pointerdown', () => {
      this.tweens.resumeAll()
      this.cameras.main.fadeOut(200, 0, 10, 40)
      this.time.delayedCall(200, () => this.scene.start('MenuScene'))
    })

    this._pauseObjs = [
      this.pauseBg, this.pausePanel, this.pauseTitle,
      this.resumeBg, this.resumeBtn,
      this.menuBg, this.menuBtn,
    ]
    this._pauseObjs.forEach(o => o.setVisible(false))
  }

  _drawPauseBtn(g, x, y, w, h, hover) {
    g.clear()
    g.fillStyle(hover ? 0x1d4ed8 : 0x2563eb, 1)
    g.fillRoundedRect(x - w / 2, y - h / 2, w, h, 10)
  }

  _drawMenuBtn(g, x, y, w, h, hover) {
    g.clear()
    g.fillStyle(hover ? 0x1a2f5a : 0x0c1a38, 1)
    g.lineStyle(1, 0x3b82f6, hover ? 0.9 : 0.5)
    g.strokeRoundedRect(x - w / 2, y - h / 2, w, h, 10)
  }

  _togglePause() {
    if (this.isEvaluating) return  // no pause during answer feedback
    if (this.isPaused) this._resumeGame()
    else this._pauseGame()
  }

  _pauseGame() {
    this.isPaused = true
    this.tweens.pauseAll()
    this._pauseObjs.forEach(o => o.setVisible(true))
  }

  _resumeGame() {
    this._pauseObjs.forEach(o => o.setVisible(false))
    this.tweens.resumeAll()
    this.isPaused = false
  }

  // ─── Combo / streak system ────────────────────────────────────────────────
  _getMultiplier() {
    if (this.streak >= 10) return 5
    if (this.streak >= 5)  return 3
    if (this.streak >= 3)  return 2
    return 1
  }

  _updateStreakDisplay() {
    if (this.streak >= 2) {
      this.streakTxt.setText(`🔥 ×${this.streak}`).setAlpha(1)
    } else {
      this.streakTxt.setAlpha(0)
    }
  }

  _showCombo(n) {
    const colors = { 3: '#fbbf24', 5: '#f97316', 10: '#ef4444' }
    const color = colors[n] || '#fbbf24'
    const msg = this.add
      .text(this.W / 2, this.H * 0.46, `COMBO ×${n} !`, {
        fontSize: '28px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color,
        fontStyle: 'bold',
        stroke: '#000c1a',
        strokeThickness: 3,
      })
      .setOrigin(0.5)
      .setAlpha(0)
      .setDepth(22)

    this.tweens.add({
      targets: msg,
      alpha: 1,
      y: this.H * 0.39,
      duration: 300,
      hold: 600,
      yoyo: true,
      onComplete: () => msg.destroy(),
    })
  }

  _showBonus(n) {
    const bonus = this.add
      .text(this.playerPos.x + 34, this.playerY - 65, `+${n}`, {
        fontSize: '20px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#fbbf24',
        fontStyle: 'bold',
        stroke: '#000c1a',
        strokeThickness: 2,
      })
      .setOrigin(0.5)
      .setAlpha(0)
      .setDepth(24)

    this.tweens.add({
      targets: bonus,
      alpha: 1,
      y: this.playerY - 96,
      duration: 260,
      hold: 380,
      yoyo: true,
      onComplete: () => bonus.destroy(),
    })
  }

  // ─── Update loop ──────────────────────────────────────────────────────────
  update(time, delta) {
    if (this.isPaused) return

    // Scrolling lane stripes
    const speed = this.stripeSpeed * (delta / 1000)
    this.stripes.forEach(stripe => {
      stripe.y += speed
      if (stripe.y > this.H + 40) stripe.y -= this.stripeLoopH
    })

    // Player run animation (full cycle every 320 ms)
    this.runTick = (this.runTick + delta / 320) % 1
    this._drawPlayer()
  }
}
