import Phaser from 'phaser'

const CATEGORIES = [
  { key: 'all',            label: 'Tout  (mixte)',    icon: '∞', bgColor: 0x1e3a8a, border: 0x3b82f6, txt: '#93c5fd', count: 30 },
  { key: 'addition',       label: 'Addition',         icon: '+', bgColor: 0x14532d, border: 0x22c55e, txt: '#4ade80', count: 6  },
  { key: 'subtraction',    label: 'Soustraction',     icon: '−', bgColor: 0x78350f, border: 0xf59e0b, txt: '#fbbf24', count: 6  },
  { key: 'multiplication', label: 'Multiplication',   icon: '×', bgColor: 0x4c1d95, border: 0xa78bfa, txt: '#c4b5fd', count: 12 },
  { key: 'division',       label: 'Division',         icon: '÷', bgColor: 0x164e63, border: 0x22d3ee, txt: '#67e8f9', count: 6  },
]

export default class MenuScene extends Phaser.Scene {
  constructor() {
    super({ key: 'MenuScene' })
  }

  create() {
    const W = this.scale.width
    const H = this.scale.height

    // Background
    this.add.rectangle(W / 2, H / 2, W, H, 0x060e1e)
    const laneColors = [0x0e1d4a, 0x14276b, 0x0d1d4a]
    for (let i = 0; i < 3; i++) {
      this.add.rectangle((i + 0.5) * W / 3, H / 2, W / 3 - 2, H, laneColors[i]).setAlpha(0.35)
    }

    // Title
    const title = this.add
      .text(W / 2, H * 0.11, 'Choisir une catégorie', {
        fontSize: '26px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#e2e8f0',
        fontStyle: 'bold',
      })
      .setOrigin(0.5)
      .setAlpha(0)

    const sub = this.add
      .text(W / 2, H * 0.185, 'Quelle opération veux-tu pratiquer ?', {
        fontSize: '14px',
        fontFamily: 'Arial',
        color: '#475569',
      })
      .setOrigin(0.5)
      .setAlpha(0)

    this.tweens.add({ targets: title, alpha: 1, duration: 380, delay: 60  })
    this.tweens.add({ targets: sub,   alpha: 1, duration: 380, delay: 160 })

    // Category buttons — 5 stacked
    const btnW   = 418
    const btnH   = 62
    const startY = H * 0.295
    const gap    = H * 0.104          // ~72 px at H=700

    CATEGORIES.forEach((cat, i) => {
      this._makeBtn(W / 2, startY + i * gap, btnW, btnH, cat, i)
    })

    // Back link
    const back = this.add
      .text(W / 2, H * 0.935, '← Retour au menu', {
        fontSize: '14px',
        fontFamily: 'Arial',
        color: '#334155',
      })
      .setOrigin(0.5)
      .setAlpha(0)
      .setInteractive({ useHandCursor: true })

    back.on('pointerover', () => back.setColor('#64748b'))
    back.on('pointerout',  () => back.setColor('#334155'))
    back.on('pointerdown', () => {
      this.cameras.main.fadeOut(200, 0, 10, 40)
      this.time.delayedCall(200, () => this.scene.start('BootScene'))
    })

    this.tweens.add({ targets: back, alpha: 1, duration: 350, delay: 700 })
    this.input.keyboard.on('keydown-ESC', () => this.scene.start('BootScene'))
  }

  _makeBtn(cx, cy, btnW, btnH, cat, index) {
    // Background (redrawn on hover)
    const bg = this.add.graphics().setAlpha(0).setDepth(3)
    const draw = (hovered) => {
      bg.clear()
      bg.fillStyle(cat.bgColor, hovered ? 0.85 : 0.65)
      bg.fillRoundedRect(cx - btnW / 2, cy - btnH / 2, btnW, btnH, 12)
      bg.lineStyle(2, cat.border, hovered ? 1 : 0.5)
      bg.strokeRoundedRect(cx - btnW / 2, cy - btnH / 2, btnW, btnH, 12)
    }
    draw(false)

    // Icon halo
    const halo = this.add.graphics().setAlpha(0).setDepth(4)
    halo.fillStyle(cat.border, 0.18)
    halo.fillCircle(cx - btnW / 2 + 38, cy, 22)

    // Icon symbol
    const iconTxt = this.add
      .text(cx - btnW / 2 + 38, cy, cat.icon, {
        fontSize: '22px',
        fontFamily: 'Arial',
        color: cat.txt,
        fontStyle: 'bold',
      })
      .setOrigin(0.5)
      .setAlpha(0)
      .setDepth(5)

    // Label
    const labelTxt = this.add
      .text(cx - btnW / 2 + 74, cy, cat.label, {
        fontSize: '17px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#e2e8f0',
        fontStyle: 'bold',
      })
      .setOrigin(0, 0.5)
      .setAlpha(0)
      .setDepth(5)

    // Question count badge
    const badge = this.add
      .text(cx + btnW / 2 - 20, cy, `${cat.count} q`, {
        fontSize: '12px',
        fontFamily: 'Arial',
        color: cat.txt,
      })
      .setOrigin(1, 0.5)
      .setAlpha(0)
      .setDepth(5)

    // Transparent hit zone over full button
    const hit = this.add
      .rectangle(cx, cy, btnW, btnH, 0, 0)
      .setDepth(6)
      .setInteractive({ useHandCursor: true })

    hit.on('pointerover', () => draw(true))
    hit.on('pointerout',  () => draw(false))
    hit.on('pointerdown', () => {
      this.cameras.main.fadeOut(220, 0, 10, 40)
      this.time.delayedCall(220, () =>
        this.scene.start('GameScene', { category: cat.key })
      )
    })

    // Staggered fade-in
    const delay = 220 + index * 80
    ;[bg, halo, iconTxt, labelTxt, badge].forEach(obj =>
      this.tweens.add({ targets: obj, alpha: 1, duration: 280, delay })
    )
  }
}
