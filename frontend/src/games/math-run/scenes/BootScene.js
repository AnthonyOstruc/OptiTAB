import Phaser from 'phaser'

export default class BootScene extends Phaser.Scene {
  constructor() {
    super({ key: 'BootScene' })
  }

  create() {
    const W = this.scale.width
    const H = this.scale.height

    // Background
    this.add.rectangle(W / 2, H / 2, W, H, 0x0a1628)

    // Decorative lane strips (background)
    const laneW = W / 3
    const laneColors = [0x152a6b, 0x1e3a8a, 0x1a3070]
    for (let i = 0; i < 3; i++) {
      this.add.rectangle((i + 0.5) * laneW, H / 2, laneW - 2, H, laneColors[i]).setAlpha(0.7)
    }
    this.add.rectangle(laneW, H / 2, 2, H, 0x3b82f6, 0.4)
    this.add.rectangle(laneW * 2, H / 2, 2, H, 0x3b82f6, 0.4)

    // Scrolling decoration stripes (purely visual)
    this.stripes = []
    for (let lane = 0; lane < 3; lane++) {
      for (let row = 0; row < 6; row++) {
        const stripe = this.add.rectangle(
          (lane + 0.5) * laneW,
          row * 120 + 60,
          laneW - 10,
          40,
          0xffffff,
          0.04
        )
        this.stripes.push(stripe)
      }
    }

    // Title
    const titleTxt = this.add
      .text(W / 2, H * 0.24, 'Math Run', {
        fontSize: '44px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#ffd54f',
        fontStyle: 'bold',
        stroke: '#1e3a8a',
        strokeThickness: 5,
      })
      .setOrigin(0.5)
      .setAlpha(0)

    // Subtitle
    const subtitleTxt = this.add
      .text(W / 2, H * 0.35, 'Choisis la bonne réponse !', {
        fontSize: '17px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#90caf9',
      })
      .setOrigin(0.5)
      .setAlpha(0)

    // Instructions panel
    const panelH = 100
    const panelY = H * 0.52
    const panelBg = this.add.graphics()
    panelBg.fillStyle(0x1e3a8a, 0.6)
    panelBg.fillRoundedRect(W * 0.1, panelY - panelH / 2, W * 0.8, panelH, 12)
    panelBg.setAlpha(0)

    const instrLines = ['← → pour changer de voie', '3 vies · Score maximum = ?']
    const instrTxts = instrLines.map((line, i) =>
      this.add
        .text(W / 2, panelY - 18 + i * 34, line, {
          fontSize: '15px',
          fontFamily: 'Arial',
          color: '#cbd5e1',
        })
        .setOrigin(0.5)
        .setAlpha(0)
    )

    // Fade in everything
    this.tweens.add({ targets: titleTxt, alpha: 1, duration: 500, delay: 100 })
    this.tweens.add({ targets: subtitleTxt, alpha: 1, duration: 500, delay: 300 })
    this.tweens.add({ targets: panelBg, alpha: 1, duration: 400, delay: 500 })
    instrTxts.forEach((txt, i) => {
      this.tweens.add({ targets: txt, alpha: 1, duration: 400, delay: 550 + i * 80 })
    })

    // High score badge
    const hiScore = Math.max(...['all', 'addition', 'subtraction', 'multiplication', 'division'].map(c => parseInt(localStorage.getItem(`mathrun_hs_${c}`) || '0', 10)))
    if (hiScore > 0) {
      const hsBg = this.add.graphics().setAlpha(0)
      hsBg.fillStyle(0x1e3a8a, 0.8)
      hsBg.fillRoundedRect(W / 2 - 80, H * 0.665 - 18, 160, 36, 10)
      const hsTxt = this.add
        .text(W / 2, H * 0.665, `★  Record : ${hiScore}`, {
          fontSize: '14px',
          fontFamily: "'Segoe UI', Arial, sans-serif",
          color: '#fbbf24',
          fontStyle: 'bold',
        })
        .setOrigin(0.5)
        .setAlpha(0)
      this.tweens.add({ targets: [hsBg, hsTxt], alpha: 1, duration: 400, delay: 750 })
    }

    // Start button
    const btnY = H * 0.80
    const btnW = 220
    const btnH = 56

    this.btnBg = this.add.graphics().setAlpha(0).setDepth(5)
    this.drawBtn(this.btnBg, W / 2, btnY, btnW, btnH, false)

    this.startBtn = this.add
      .text(W / 2, btnY, '▶  Commencer', {
        fontSize: '21px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#ffffff',
        fontStyle: 'bold',
      })
      .setOrigin(0.5)
      .setDepth(6)
      .setAlpha(0)
      .setInteractive({ useHandCursor: true })

    this.startBtn.on('pointerover', () => {
      this.drawBtn(this.btnBg, W / 2, btnY, btnW, btnH, true)
    })
    this.startBtn.on('pointerout', () => {
      this.drawBtn(this.btnBg, W / 2, btnY, btnW, btnH, false)
    })
    this.startBtn.on('pointerdown', () => this.startGame())

    // Keyboard shortcut
    this.input.keyboard.on('keydown-ENTER', () => this.startGame())
    this.input.keyboard.on('keydown-SPACE', () => this.startGame())

    this.tweens.add({
      targets: [this.btnBg, this.startBtn],
      alpha: 1,
      duration: 400,
      delay: 700,
    })

    // Pulse on button
    this.tweens.add({
      targets: this.startBtn,
      scaleX: 1.04,
      scaleY: 1.04,
      duration: 900,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.easeInOut',
      delay: 1000,
    })

    // Animate background stripes
    this.stripeSpeed = 50
  }

  drawBtn(g, x, y, w, h, hover) {
    g.clear()
    g.fillStyle(hover ? 0x1d4ed8 : 0x2563eb, 1)
    g.fillRoundedRect(x - w / 2, y - h / 2, w, h, 14)
    if (hover) {
      g.lineStyle(2, 0x60a5fa, 0.8)
      g.strokeRoundedRect(x - w / 2, y - h / 2, w, h, 14)
    }
  }

  startGame() {
    this.cameras.main.fadeOut(250, 0, 10, 40)
    this.time.delayedCall(250, () => this.scene.start('MenuScene'))
  }

  update(time, delta) {
    const speed = this.stripeSpeed * (delta / 1000)
    const H = this.scale.height
    this.stripes.forEach(stripe => {
      stripe.y += speed
      if (stripe.y > H + 20) stripe.y = -20
    })
  }
}
