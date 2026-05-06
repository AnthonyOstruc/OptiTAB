import Phaser from 'phaser'

const CAT_ALL = {
  key: 'all', label: 'Tout  (mixte)', icon: '∞',
  bgColor: 0x1e3a8a, border: 0x3b82f6, txt: '#93c5fd', count: 130,
}

const CATS_BASIC = [
  { key: 'addition',       label: 'Addition',       icon: '+',    bgColor: 0x14532d, border: 0x22c55e, txt: '#4ade80', count: 16 },
  { key: 'subtraction',    label: 'Soustraction',   icon: '−',    bgColor: 0x78350f, border: 0xf59e0b, txt: '#fbbf24', count: 16 },
  { key: 'multiplication', label: 'Multiplication', icon: '×',    bgColor: 0x4c1d95, border: 0xa78bfa, txt: '#c4b5fd', count: 24 },
  { key: 'division',       label: 'Division',       icon: '÷',    bgColor: 0x164e63, border: 0x22d3ee, txt: '#67e8f9', count: 14 },
]

const CATS_ADVANCED = [
  { key: 'limits',      label: 'Limites',    icon: 'lim', bgColor: 0x3b0764, border: 0xa855f7, txt: '#d8b4fe', count: 15 },
  { key: 'derivatives', label: 'Dérivées',   icon: "d/dx",bgColor: 0x1e1b4b, border: 0x818cf8, txt: '#a5b4fc', count: 15 },
  { key: 'integrals',   label: 'Intégrales', icon: '∫',   bgColor: 0x0f3d2e, border: 0x34d399, txt: '#6ee7b7', count: 15 },
  { key: 'sequences',   label: 'Suites',     icon: 'u_n', bgColor: 0x431407, border: 0xfb923c, txt: '#fdba74', count: 15 },
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
      this.add.rectangle((i + 0.5) * W / 3, H / 2, W / 3 - 2, H, laneColors[i]).setAlpha(0.3)
    }

    // Title
    const title = this.add
      .text(W / 2, H * 0.085, 'Choisir une catégorie', {
        fontSize: '22px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#e2e8f0',
        fontStyle: 'bold',
      })
      .setOrigin(0.5)
      .setAlpha(0)

    const sub = this.add
      .text(W / 2, H * 0.148, 'Quel thème veux-tu pratiquer ?', {
        fontSize: '13px',
        fontFamily: 'Arial',
        color: '#475569',
      })
      .setOrigin(0.5)
      .setAlpha(0)

    this.tweens.add({ targets: title, alpha: 1, duration: 320, delay: 60  })
    this.tweens.add({ targets: sub,   alpha: 1, duration: 320, delay: 160 })

    // ── "All" full-width button ─────────────────────────────────────────────
    this._makeFullBtn(W / 2, H * 0.225, 418, 50, CAT_ALL, 0)

    // ── Section label "Opérations" ──────────────────────────────────────────
    this._makeSectionLabel(W / 2, H * 0.322, 'Opérations de base', 180)

    // Two-column layout: each col cx, button width
    const btnW = 210
    const cx1  = W / 2 - btnW / 2 - 6
    const cx2  = W / 2 + btnW / 2 + 6
    const btnH = 50

    // Basic row 1: addition | subtraction
    this._makeSmallBtn(cx1, H * 0.39,  btnW, btnH, CATS_BASIC[0], 2)
    this._makeSmallBtn(cx2, H * 0.39,  btnW, btnH, CATS_BASIC[1], 3)
    // Basic row 2: multiplication | division
    this._makeSmallBtn(cx1, H * 0.466, btnW, btnH, CATS_BASIC[2], 4)
    this._makeSmallBtn(cx2, H * 0.466, btnW, btnH, CATS_BASIC[3], 5)

    // ── Section label "Lycée" ───────────────────────────────────────────────
    this._makeSectionLabel(W / 2, H * 0.545, 'Lycée / Terminale', 340)

    // Advanced row 1: limits | derivatives
    this._makeSmallBtn(cx1, H * 0.613, btnW, btnH, CATS_ADVANCED[0], 6)
    this._makeSmallBtn(cx2, H * 0.613, btnW, btnH, CATS_ADVANCED[1], 7)
    // Advanced row 2: integrals | sequences
    this._makeSmallBtn(cx1, H * 0.689, btnW, btnH, CATS_ADVANCED[2], 8)
    this._makeSmallBtn(cx2, H * 0.689, btnW, btnH, CATS_ADVANCED[3], 9)

    // ── Back link ───────────────────────────────────────────────────────────
    const back = this.add
      .text(W / 2, H * 0.938, '← Retour au menu', {
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
    this.tweens.add({ targets: back, alpha: 1, duration: 300, delay: 850 })
    this.input.keyboard.on('keydown-ESC', () => this.scene.start('BootScene'))
  }

  _makeSectionLabel(cx, cy, text, delay) {
    const W = this.scale.width
    const lbl = this.add
      .text(cx, cy, text, {
        fontSize: '11px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#374151',
        fontStyle: 'bold',
        letterSpacing: 1,
      })
      .setOrigin(0.5)
      .setAlpha(0)
    this.tweens.add({ targets: lbl, alpha: 1, duration: 280, delay })

    // Decorative lines left and right
    const lineY = cy
    const txtW  = text.length * 6.5
    const lineX1 = cx - txtW / 2 - 12
    const lineX2 = cx + txtW / 2 + 12
    const lineL  = this.add.rectangle(lineX1 - 20, lineY, 40, 1, 0x1e3a8a, 0.6).setAlpha(0)
    const lineR  = this.add.rectangle(lineX2 + 20, lineY, 40, 1, 0x1e3a8a, 0.6).setAlpha(0)
    this.tweens.add({ targets: [lineL, lineR], alpha: 1, duration: 280, delay })
  }

  _makeFullBtn(cx, cy, btnW, btnH, cat, index) {
    const bg = this.add.graphics().setAlpha(0).setDepth(3)
    const draw = (hovered) => {
      bg.clear()
      bg.fillStyle(cat.bgColor, hovered ? 0.85 : 0.65)
      bg.fillRoundedRect(cx - btnW / 2, cy - btnH / 2, btnW, btnH, 12)
      bg.lineStyle(2, cat.border, hovered ? 1 : 0.5)
      bg.strokeRoundedRect(cx - btnW / 2, cy - btnH / 2, btnW, btnH, 12)
    }
    draw(false)

    const halo = this.add.graphics().setAlpha(0).setDepth(4)
    halo.fillStyle(cat.border, 0.18)
    halo.fillCircle(cx - btnW / 2 + 38, cy, 22)

    const iconTxt = this.add
      .text(cx - btnW / 2 + 38, cy, cat.icon, {
        fontSize: '22px', fontFamily: 'Arial', color: cat.txt, fontStyle: 'bold',
      })
      .setOrigin(0.5).setAlpha(0).setDepth(5)

    const labelTxt = this.add
      .text(cx - btnW / 2 + 74, cy, cat.label, {
        fontSize: '17px', fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#e2e8f0', fontStyle: 'bold',
      })
      .setOrigin(0, 0.5).setAlpha(0).setDepth(5)

    const hs    = parseInt(localStorage.getItem(`mathrun_hs_${cat.key}`) || '0', 10)
    const badge = this.add
      .text(cx + btnW / 2 - 18, hs > 0 ? cy - 10 : cy, `${cat.count} q`, {
        fontSize: '12px', fontFamily: 'Arial', color: cat.txt,
      })
      .setOrigin(1, 0.5).setAlpha(0).setDepth(5)

    const hsBadge = hs > 0
      ? this.add.text(cx + btnW / 2 - 18, cy + 10, `★ ${hs}`, {
          fontSize: '12px', fontFamily: "'Segoe UI', Arial, sans-serif",
          color: '#fbbf24', fontStyle: 'bold',
        }).setOrigin(1, 0.5).setAlpha(0).setDepth(5)
      : null

    const hit = this.add.rectangle(cx, cy, btnW, btnH, 0, 0).setDepth(6).setInteractive({ useHandCursor: true })
    hit.on('pointerover', () => draw(true))
    hit.on('pointerout',  () => draw(false))
    hit.on('pointerdown', () => {
      this.cameras.main.fadeOut(220, 0, 10, 40)
      this.time.delayedCall(220, () => this.scene.start('GameScene', { category: cat.key }))
    })

    const delay = 220 + index * 70
    const targets = [bg, halo, iconTxt, labelTxt, badge]
    if (hsBadge) targets.push(hsBadge)
    targets.forEach(o => this.tweens.add({ targets: o, alpha: 1, duration: 260, delay }))
  }

  _makeSmallBtn(cx, cy, btnW, btnH, cat, index) {
    const bg = this.add.graphics().setAlpha(0).setDepth(3)
    const draw = (hovered) => {
      bg.clear()
      bg.fillStyle(cat.bgColor, hovered ? 0.9 : 0.7)
      bg.fillRoundedRect(cx - btnW / 2, cy - btnH / 2, btnW, btnH, 10)
      bg.lineStyle(1.5, cat.border, hovered ? 1 : 0.55)
      bg.strokeRoundedRect(cx - btnW / 2, cy - btnH / 2, btnW, btnH, 10)
    }
    draw(false)

    // Icon halo
    const halo = this.add.graphics().setAlpha(0).setDepth(4)
    halo.fillStyle(cat.border, 0.2)
    halo.fillCircle(cx - btnW / 2 + 24, cy, 17)

    const iconTxt = this.add
      .text(cx - btnW / 2 + 24, cy, cat.icon, {
        fontSize: '14px', fontFamily: 'Arial', color: cat.txt, fontStyle: 'bold',
      })
      .setOrigin(0.5).setAlpha(0).setDepth(5)

    const labelTxt = this.add
      .text(cx - btnW / 2 + 46, cy, cat.label, {
        fontSize: '13px', fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#e2e8f0', fontStyle: 'bold',
      })
      .setOrigin(0, 0.5).setAlpha(0).setDepth(5)

    const hs    = parseInt(localStorage.getItem(`mathrun_hs_${cat.key}`) || '0', 10)
    const badge = this.add
      .text(cx + btnW / 2 - 10, hs > 0 ? cy - 9 : cy, `${cat.count}q`, {
        fontSize: '10px', fontFamily: 'Arial', color: cat.txt,
      })
      .setOrigin(1, 0.5).setAlpha(0).setDepth(5)

    const hsBadge = hs > 0
      ? this.add.text(cx + btnW / 2 - 10, cy + 9, `★${hs}`, {
          fontSize: '10px', fontFamily: "'Segoe UI', Arial, sans-serif",
          color: '#fbbf24', fontStyle: 'bold',
        }).setOrigin(1, 0.5).setAlpha(0).setDepth(5)
      : null

    const hit = this.add.rectangle(cx, cy, btnW, btnH, 0, 0).setDepth(6).setInteractive({ useHandCursor: true })
    hit.on('pointerover', () => draw(true))
    hit.on('pointerout',  () => draw(false))
    hit.on('pointerdown', () => {
      this.cameras.main.fadeOut(220, 0, 10, 40)
      this.time.delayedCall(220, () => this.scene.start('GameScene', { category: cat.key }))
    })

    const delay = 220 + index * 55
    const targets = [bg, halo, iconTxt, labelTxt, badge]
    if (hsBadge) targets.push(hsBadge)
    targets.forEach(o => this.tweens.add({ targets: o, alpha: 1, duration: 240, delay }))
  }
}
