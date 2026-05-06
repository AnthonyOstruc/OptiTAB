import Phaser from 'phaser'

const CAT_ACCENT = {
  addition: 0x22c55e, subtraction: 0xf59e0b, multiplication: 0xa78bfa,
  division: 0x22d3ee, limits: 0xa855f7, derivatives: 0x818cf8,
  integrals: 0x34d399, sequences: 0xfb923c, all: 0x3b82f6,
}

export default class GameOverScene extends Phaser.Scene {
  constructor() { super({ key: 'GameOverScene' }) }

  init(data) {
    this.finalScore = data?.score ?? 0
    this.category   = data?.category || 'all'
  }

  create() {
    const W = this.scale.width
    const H = this.scale.height
    const accent = CAT_ACCENT[this.category] || 0x3b82f6

    // ── High score persistence ────────────────────────────────────────────────
    const hsKey      = `mathrun_hs_${this.category}`
    const stored     = parseInt(localStorage.getItem(hsKey) || '0', 10)
    const isNewRecord = this.finalScore > 0 && this.finalScore > stored
    if (isNewRecord) localStorage.setItem(hsKey, String(this.finalScore))
    const highScore  = isNewRecord ? this.finalScore : stored

    if (this.finalScore > 0) {
      window.dispatchEvent(new CustomEvent('mathrun:gameover', {
        detail: { score: this.finalScore, category: this.category }
      }))
    }

    // ── Background ────────────────────────────────────────────────────────────
    this.add.rectangle(W / 2, H / 2, W, H, 0x040d1a)

    // Dot grid
    const dots = this.add.graphics()
    dots.fillStyle(0x1e3a8a, 0.35)
    for (let x = 24; x < W; x += 32) {
      for (let y = 24; y < H; y += 32) dots.fillCircle(x, y, 1)
    }

    // Faded lane strips
    const laneW = W / 3
    for (let i = 0; i < 3; i++) {
      this.add.rectangle((i + 0.5) * laneW, H / 2, laneW - 2, H, [0x101e42, 0x182046, 0x101e42][i]).setAlpha(0.4)
    }
    this.add.rectangle(laneW, H / 2, 1, H, 0x3b82f6, 0.2)
    this.add.rectangle(laneW * 2, H / 2, 1, H, 0x3b82f6, 0.2)

    // ── Header ───────────────────────────────────────────────────────────────
    const titleStr = isNewRecord ? '🏆  Nouveau Record !' : 'Partie terminée'
    const titleColor = isNewRecord ? '#ffd54f' : '#e2e8f0'
    const title = this.add
      .text(W / 2, H * 0.10, titleStr, {
        fontSize: isNewRecord ? '28px' : '30px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: titleColor, fontStyle: 'bold',
        stroke: '#1e3a8a', strokeThickness: isNewRecord ? 4 : 3,
      })
      .setOrigin(0.5).setAlpha(0)

    // ── Score panel ───────────────────────────────────────────────────────────
    const panelY = H * 0.28
    const panelW = W * 0.80
    const panelH = 130

    const panelBg = this.add.graphics().setAlpha(0)
    panelBg.fillStyle(0x080f24, 1)
    panelBg.fillRoundedRect(W / 2 - panelW / 2, panelY - panelH / 2, panelW, panelH, 16)
    panelBg.lineStyle(1.5, accent, 0.5)
    panelBg.strokeRoundedRect(W / 2 - panelW / 2, panelY - panelH / 2, panelW, panelH, 16)
    // Top accent bar
    panelBg.fillStyle(accent, 0.7)
    panelBg.fillRoundedRect(W / 2 - panelW / 2 + 2, panelY - panelH / 2 + 1, panelW - 4, 3, 2)

    const scoreLbl = this.add
      .text(W / 2, panelY - 36, 'SCORE FINAL', {
        fontSize: '10px', fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#334155', fontStyle: 'bold', letterSpacing: 1.5,
      })
      .setOrigin(0.5).setAlpha(0)

    // Animated score counter
    const scoreValueTxt = this.add
      .text(W / 2, panelY - 8, '0', {
        fontSize: '52px', fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#ffd54f', fontStyle: 'bold',
      })
      .setOrigin(0.5).setAlpha(0)

    // Divider
    const divider = this.add.graphics().setAlpha(0)
    divider.lineStyle(1, 0x1e3a8a, 0.5)
    divider.lineBetween(W / 2 - panelW / 2 + 24, panelY + 30, W / 2 + panelW / 2 - 24, panelY + 30)

    // High score row
    const hsLabel = isNewRecord ? '★  Nouveau meilleur score !' : `Meilleur : ${highScore} pts`
    const hsColor = isNewRecord ? '#fbbf24' : '#334155'
    const hiScoreTxt = this.add
      .text(W / 2, panelY + 50, hsLabel, {
        fontSize: isNewRecord ? '14px' : '13px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: hsColor, fontStyle: isNewRecord ? 'bold' : 'normal',
      })
      .setOrigin(0.5).setAlpha(0)

    // ── Stars ─────────────────────────────────────────────────────────────────
    const stars      = this._getStars(this.finalScore)
    const starColors = ['#94a3b8', '#fbbf24', '#fbbf24']
    const starsY     = H * 0.555
    const starTxts   = stars.map((star, i) =>
      this.add
        .text(W / 2 + (i - 1) * 58, starsY, star, { fontSize: '44px', color: starColors[i] })
        .setOrigin(0.5).setAlpha(0).setScale(0.35)
    )

    // ── Performance badge ─────────────────────────────────────────────────────
    const perfY  = H * 0.67
    const perf   = this._getPerformance(this.finalScore)
    const perfBg = this.add.graphics().setAlpha(0)
    perfBg.fillStyle(0x080f24, 1)
    perfBg.fillRoundedRect(W / 2 - 155, perfY - 24, 310, 48, 10)
    perfBg.lineStyle(1, 0x1e3a8a, 0.6)
    perfBg.strokeRoundedRect(W / 2 - 155, perfY - 24, 310, 48, 10)
    const perfTxt = this.add
      .text(W / 2, perfY, perf, {
        fontSize: '15px', fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#94a3b8', align: 'center',
        wordWrap: { width: 290 },
      })
      .setOrigin(0.5).setAlpha(0)

    // ── Buttons ───────────────────────────────────────────────────────────────
    const btn1Y = H * 0.795
    const btn2Y = H * 0.885
    const btnW2 = 230
    const btnH2 = 52

    // Retry button
    const retryBg = this.add.graphics().setAlpha(0).setDepth(5)
    this._drawPrimaryBtn(retryBg, W / 2, btn1Y, btnW2, btnH2, false)

    const retryBtn = this.add
      .text(W / 2, btn1Y, '↺  Rejouer', {
        fontSize: '20px', fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#ffffff', fontStyle: 'bold',
      })
      .setOrigin(0.5).setDepth(6).setAlpha(0).setInteractive({ useHandCursor: true })

    retryBtn.on('pointerover', () => this._drawPrimaryBtn(retryBg, W / 2, btn1Y, btnW2, btnH2, true))
    retryBtn.on('pointerout',  () => this._drawPrimaryBtn(retryBg, W / 2, btn1Y, btnW2, btnH2, false))
    retryBtn.on('pointerdown', () => {
      this.cameras.main.fadeOut(200, 4, 13, 26)
      this.time.delayedCall(200, () => this.scene.start('GameScene', { category: this.category }))
    })

    // Menu button
    const menuBg = this.add.graphics().setAlpha(0).setDepth(5)
    this._drawSecondaryBtn(menuBg, W / 2, btn2Y, btnW2, btnH2 - 8, false)

    const menuBtn = this.add
      .text(W / 2, btn2Y, '≡  Changer de mode', {
        fontSize: '16px', fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#64748b',
      })
      .setOrigin(0.5).setDepth(6).setAlpha(0).setInteractive({ useHandCursor: true })

    menuBtn.on('pointerover', () => {
      this._drawSecondaryBtn(menuBg, W / 2, btn2Y, btnW2, btnH2 - 8, true)
      menuBtn.setStyle({ color: '#94a3b8' })
    })
    menuBtn.on('pointerout', () => {
      this._drawSecondaryBtn(menuBg, W / 2, btn2Y, btnW2, btnH2 - 8, false)
      menuBtn.setStyle({ color: '#64748b' })
    })
    menuBtn.on('pointerdown', () => {
      this.cameras.main.fadeOut(200, 4, 13, 26)
      this.time.delayedCall(200, () => this.scene.start('MenuScene'))
    })

    this.input.keyboard.on('keydown-ENTER', () => this.scene.start('GameScene', { category: this.category }))
    this.input.keyboard.on('keydown-SPACE', () => this.scene.start('GameScene', { category: this.category }))
    this.input.keyboard.on('keydown-ESC',   () => this.scene.start('MenuScene'))

    // ── Staggered reveal ─────────────────────────────────────────────────────
    this.tweens.add({ targets: title,         alpha: 1, duration: 420, delay: 100 })
    this.tweens.add({ targets: panelBg,       alpha: 1, duration: 400, delay: 280 })
    this.tweens.add({ targets: scoreLbl,      alpha: 1, duration: 380, delay: 420 })
    this.tweens.add({ targets: scoreValueTxt, alpha: 1, duration: 380, delay: 520 })
    this.tweens.add({ targets: divider,       alpha: 1, duration: 300, delay: 700 })
    this.tweens.add({ targets: hiScoreTxt,    alpha: 1, duration: 380, delay: 750 })

    // Animated score count-up
    if (this.finalScore > 0) {
      this.tweens.addCounter({
        from: 0, to: this.finalScore,
        duration: Math.min(1400, this.finalScore * 80),
        ease: 'Power2',
        delay: 540,
        onUpdate: (tween) => {
          scoreValueTxt.setText(String(Math.round(tween.getValue())))
        },
        onComplete: () => {
          if (isNewRecord) {
            this.tweens.add({
              targets: scoreValueTxt, scaleX: 1.12, scaleY: 1.12,
              duration: 200, yoyo: true, ease: 'Back.easeOut',
            })
          }
        },
      })
    }

    // Stars pop in
    starsY
    starsY
    starTxts.forEach((st, i) => {
      this.tweens.add({
        targets: st, alpha: 1, scaleX: 1, scaleY: 1,
        duration: 360, delay: 820 + i * 140, ease: 'Back.easeOut',
      })
    })

    this.tweens.add({ targets: [perfBg, perfTxt], alpha: 1, duration: 380, delay: 1200 })
    this.tweens.add({ targets: [retryBg, retryBtn], alpha: 1, duration: 380, delay: 1350 })
    this.tweens.add({ targets: [menuBg, menuBtn],  alpha: 1, duration: 320, delay: 1480 })

    // New record particle burst
    if (isNewRecord) {
      this.time.delayedCall(1500, () => {
        for (let i = 0; i < 30; i++) {
          const angle = Math.random() * Math.PI * 2
          const speed = 60 + Math.random() * 120
          const dot   = this.add.circle(W / 2, H * 0.28, 3 + Math.random() * 4, 0xffd54f).setDepth(25)
          this.tweens.add({
            targets: dot,
            x: W / 2 + Math.cos(angle) * speed,
            y: H * 0.28 + Math.sin(angle) * speed,
            alpha: 0, delay: Math.random() * 80,
            duration: 500 + Math.random() * 300,
            ease: 'Power2.easeOut',
            onComplete: () => dot.destroy(),
          })
        }
      })
    }
  }

  _getStars(score) {
    if (score >= 15) return ['★', '★', '★']
    if (score >= 8)  return ['★', '★', '☆']
    if (score >= 3)  return ['★', '☆', '☆']
    return ['☆', '☆', '☆']
  }

  _getPerformance(score) {
    if (score >= 20) return 'Incroyable ! Tu maîtrises parfaitement.'
    if (score >= 15) return 'Excellent ! Tu es en avance sur ton programme.'
    if (score >= 8)  return 'Bien joué ! Continue à t\'entraîner.'
    if (score >= 3)  return 'Pas mal ! Rejoue pour progresser.'
    return 'Continue, chaque partie compte !'
  }

  _drawPrimaryBtn(g, x, y, w, h, hover) {
    g.clear()
    g.fillStyle(hover ? 0x1d4ed8 : 0x2563eb, 1)
    g.fillRoundedRect(x - w / 2, y - h / 2, w, h, 14)
    g.fillStyle(0xffffff, 0.1)
    g.fillRoundedRect(x - w / 2 + 4, y - h / 2 + 4, w - 8, h * 0.4, 10)
    if (hover) {
      g.lineStyle(2, 0x93c5fd, 0.8)
      g.strokeRoundedRect(x - w / 2, y - h / 2, w, h, 14)
    }
  }

  _drawSecondaryBtn(g, x, y, w, h, hover) {
    g.clear()
    g.fillStyle(0x080f24, 1)
    g.fillRoundedRect(x - w / 2, y - h / 2, w, h, 12)
    g.lineStyle(1, hover ? 0x334155 : 0x1a2740, 1)
    g.strokeRoundedRect(x - w / 2, y - h / 2, w, h, 12)
  }
}
