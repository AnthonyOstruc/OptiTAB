import Phaser from 'phaser'

export default class GameOverScene extends Phaser.Scene {
  constructor() {
    super({ key: 'GameOverScene' })
  }

  init(data) {
    this.finalScore = data?.score ?? 0
    this.category   = data?.category || 'all'
  }

  create() {
    const W = this.scale.width
    const H = this.scale.height

    // ── High score persistence ────────────────────────────────────────────────
    const hsKey = `mathrun_hs_${this.category}`
    const stored = parseInt(localStorage.getItem(hsKey) || '0', 10)
    const isNewRecord = this.finalScore > 0 && this.finalScore > stored
    if (isNewRecord) localStorage.setItem(hsKey, String(this.finalScore))
    const highScore = isNewRecord ? this.finalScore : stored

    // Background
    this.add.rectangle(W / 2, H / 2, W, H, 0x060e1e)

    // Decorative lanes (faded)
    const laneW = W / 3
    const laneColors = [0x0e1d4a, 0x14276b, 0x0d1d4a]
    for (let i = 0; i < 3; i++) {
      this.add.rectangle((i + 0.5) * laneW, H / 2, laneW - 2, H, laneColors[i]).setAlpha(0.5)
    }

    // "Partie terminée" title
    const title = this.add
      .text(W / 2, H * 0.19, 'Partie terminée', {
        fontSize: '32px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#e2e8f0',
        fontStyle: 'bold',
      })
      .setOrigin(0.5)
      .setAlpha(0)

    // Score panel (taller to fit high score row)
    const panelY = H * 0.40
    const panelBg = this.add.graphics().setAlpha(0)
    panelBg.fillStyle(0x1e3a8a, 0.7)
    panelBg.fillRoundedRect(W * 0.12, panelY - 58, W * 0.76, 116, 14)

    // Score label + value
    const scoreLabelTxt = this.add
      .text(W / 2, panelY - 36, 'Score final', {
        fontSize: '14px',
        fontFamily: 'Arial',
        color: '#93c5fd',
      })
      .setOrigin(0.5)
      .setAlpha(0)

    const scoreValueTxt = this.add
      .text(W / 2, panelY - 6, String(this.finalScore), {
        fontSize: '42px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#ffd54f',
        fontStyle: 'bold',
      })
      .setOrigin(0.5)
      .setAlpha(0)

    // Divider inside panel
    const divider = this.add.graphics().setAlpha(0)
    divider.lineStyle(1, 0x3b82f6, 0.4)
    divider.lineBetween(W * 0.18, panelY + 28, W * 0.82, panelY + 28)

    // High score row
    const hiScoreLabel = isNewRecord ? '★  NOUVEAU RECORD  !' : `Meilleur : ${highScore}`
    const hiScoreColor = isNewRecord ? '#fbbf24' : '#64748b'
    const hiScoreTxt = this.add
      .text(W / 2, panelY + 46, hiScoreLabel, {
        fontSize: isNewRecord ? '15px' : '14px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: hiScoreColor,
        fontStyle: isNewRecord ? 'bold' : 'normal',
      })
      .setOrigin(0.5)
      .setAlpha(0)

    // Star rating
    const stars = this._getStars(this.finalScore)
    const starColors = ['#94a3b8', '#fbbf24', '#fbbf24']
    const starTxts = stars.map((star, i) => {
      return this.add
        .text(W / 2 + (i - 1) * 54, H * 0.595, star, {
          fontSize: '42px',
          color: starColors[i],
        })
        .setOrigin(0.5)
        .setAlpha(0)
        .setScale(0.4)
    })

    // Motivational message
    const msg = this._getMessage(this.finalScore)
    const msgTxt = this.add
      .text(W / 2, H * 0.72, msg, {
        fontSize: '16px',
        fontFamily: 'Arial',
        color: '#94a3b8',
        align: 'center',
        wordWrap: { width: W * 0.75 },
      })
      .setOrigin(0.5)
      .setAlpha(0)

    // Restart button
    const btnY = H * 0.86
    const btnW = 210
    const btnH = 52
    const btnBg = this.add.graphics().setAlpha(0).setDepth(5)
    this._drawBtn(btnBg, W / 2, btnY, btnW, btnH, false)

    const restartBtn = this.add
      .text(W / 2, btnY, '↺  Rejouer', {
        fontSize: '20px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#ffffff',
        fontStyle: 'bold',
      })
      .setOrigin(0.5)
      .setDepth(6)
      .setAlpha(0)
      .setInteractive({ useHandCursor: true })

    restartBtn.on('pointerover', () => this._drawBtn(btnBg, W / 2, btnY, btnW, btnH, true))
    restartBtn.on('pointerout', () => this._drawBtn(btnBg, W / 2, btnY, btnW, btnH, false))
    restartBtn.on('pointerdown', () => {
      this.cameras.main.fadeOut(200, 0, 10, 40)
      this.time.delayedCall(200, () =>
        this.scene.start('GameScene', { category: this.category })
      )
    })

    this.input.keyboard.on('keydown-ENTER', () => this.scene.start('GameScene', { category: this.category }))
    this.input.keyboard.on('keydown-SPACE', () => this.scene.start('GameScene', { category: this.category }))

    // Staggered fade-in animation
    this.tweens.add({ targets: title, alpha: 1, duration: 400, delay: 100 })
    this.tweens.add({ targets: panelBg, alpha: 1, duration: 400, delay: 300 })
    this.tweens.add({ targets: scoreLabelTxt, alpha: 1, duration: 400, delay: 400 })
    this.tweens.add({ targets: scoreValueTxt, alpha: 1, duration: 500, delay: 450 })
    this.tweens.add({ targets: divider, alpha: 1, duration: 300, delay: 600 })
    this.tweens.add({ targets: hiScoreTxt, alpha: 1, duration: 400, delay: 650 })

    // Animate stars in with scale effect
    starTxts.forEach((st, i) => {
      this.tweens.add({
        targets: st,
        alpha: 1,
        scaleX: 1,
        scaleY: 1,
        duration: 350,
        delay: 700 + i * 150,
        ease: 'Back.easeOut',
      })
    })

    this.tweens.add({ targets: msgTxt, alpha: 1, duration: 400, delay: 1150 })
    this.tweens.add({ targets: [btnBg, restartBtn], alpha: 1, duration: 400, delay: 1300 })
  }

  _getStars(score) {
    if (score >= 15) return ['★', '★', '★']
    if (score >= 8)  return ['★', '★', '☆']
    if (score >= 3)  return ['★', '☆', '☆']
    return ['☆', '☆', '☆']
  }

  _getMessage(score) {
    if (score >= 15) return 'Excellent ! Tu es un pro des maths !'
    if (score >= 8)  return 'Bien joué ! Continue comme ça.'
    if (score >= 3)  return 'Pas mal ! Réessaie pour t\'améliorer.'
    return 'Continue de t\'entraîner, tu vas progresser !'
  }

  _drawBtn(g, x, y, w, h, hover) {
    g.clear()
    g.fillStyle(hover ? 0x1d4ed8 : 0x2563eb, 1)
    g.fillRoundedRect(x - w / 2, y - h / 2, w, h, 14)
    if (hover) {
      g.lineStyle(2, 0x60a5fa, 0.9)
      g.strokeRoundedRect(x - w / 2, y - h / 2, w, h, 14)
    }
  }
}
