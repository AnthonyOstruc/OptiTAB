import Phaser from 'phaser'

const MATH_SYMBOLS = ['∫', 'π', '∞', '∑', '√', 'θ', 'Δ', 'φ', 'α', 'λ']

const CAT_ALL = {
  key: 'all', label: 'Mode mixte', sub: 'Toutes les catégories',
  icon: '∞', icons: ['+', '−', '×', '÷', '∫', "d/dx"],
  bgColor: 0x0f1e40, border: 0x3b82f6, txt: '#93c5fd', count: 130,
}

const CATS_BASIC = [
  { key: 'addition',       label: 'Addition',       sub: 'a + b',     icon: '+',    bgColor: 0x052e16, border: 0x22c55e, txt: '#4ade80',  count: 16 },
  { key: 'subtraction',    label: 'Soustraction',   sub: 'a − b',     icon: '−',    bgColor: 0x2d1a04, border: 0xf59e0b, txt: '#fbbf24',  count: 16 },
  { key: 'multiplication', label: 'Multiplication', sub: 'a × b',     icon: '×',    bgColor: 0x1e0a38, border: 0xa78bfa, txt: '#c4b5fd', count: 24 },
  { key: 'division',       label: 'Division',       sub: 'a ÷ b',     icon: '÷',    bgColor: 0x062028, border: 0x22d3ee, txt: '#67e8f9',  count: 14 },
]

const CATS_ADVANCED = [
  { key: 'limits',      label: 'Limites',    sub: 'lim f(x)',  icon: 'lim',  bgColor: 0x180631, border: 0xa855f7, txt: '#d8b4fe', count: 15 },
  { key: 'derivatives', label: 'Dérivées',   sub: "f'(x)",     icon: "d/dx", bgColor: 0x0c0c2e, border: 0x818cf8, txt: '#a5b4fc', count: 15 },
  { key: 'integrals',   label: 'Intégrales', sub: '∫ f(x)dx',  icon: '∫',    bgColor: 0x042218, border: 0x34d399, txt: '#6ee7b7', count: 15 },
  { key: 'sequences',   label: 'Suites',     sub: 'uₙ, vₙ',   icon: 'uₙ',   bgColor: 0x1f0a03, border: 0xfb923c, txt: '#fdba74', count: 15 },
]

export default class MenuScene extends Phaser.Scene {
  constructor() { super({ key: 'MenuScene' }) }

  create() {
    const W = this.scale.width
    const H = this.scale.height

    // ── Background ────────────────────────────────────────────────────────────
    this.add.rectangle(W / 2, H / 2, W, H, 0x040d1a)

    // Dot grid
    const dots = this.add.graphics()
    dots.fillStyle(0x1e3a8a, 0.3)
    for (let x = 24; x < W; x += 36) {
      for (let y = 24; y < H; y += 36) dots.fillCircle(x, y, 1)
    }

    // Lane strips
    const laneW = W / 3
    for (let i = 0; i < 3; i++) {
      this.add.rectangle((i + 0.5) * laneW, H / 2, laneW - 2, H, [0x101e42, 0x172040, 0x101e42][i]).setAlpha(0.3)
    }
    this.add.rectangle(laneW, H / 2, 1, H, 0x3b82f6, 0.18)
    this.add.rectangle(laneW * 2, H / 2, 1, H, 0x3b82f6, 0.18)

    // Floating symbols
    this._spawnFloatSymbols(W, H)

    // ── Header ───────────────────────────────────────────────────────────────
    const headerGlow = this.add.graphics()
    headerGlow.fillStyle(0x1d4ed8, 0.08)
    headerGlow.fillRect(0, 0, W, 68)

    const titleH = this.add
      .text(W / 2, 26, 'MATH RUN', {
        fontSize: '24px', fontFamily: "'Segoe UI', system-ui, sans-serif",
        color: '#ffd54f', fontStyle: 'bold',
        stroke: '#1e3a8a', strokeThickness: 4,
      })
      .setOrigin(0.5).setAlpha(0)

    const subH = this.add
      .text(W / 2, 50, 'Choisir un mode', {
        fontSize: '12px', fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#334155',
      })
      .setOrigin(0.5).setAlpha(0)

    // Header separator
    const sep = this.add.graphics()
    sep.lineStyle(1, 0x1e3a8a, 0.5)
    sep.lineBetween(0, 66, W, 66)

    // ── "All" full-width button ───────────────────────────────────────────────
    this._makeFullBtn(W / 2, H * 0.155, W - 32, 58, CAT_ALL, 0)

    // ── Section: Opérations de base ──────────────────────────────────────────
    this._makeSectionLabel(W / 2, H * 0.265, 'OPÉRATIONS DE BASE', 0x22c55e, 180)

    const btnW = (W - 40) / 2
    const cx1 = 16 + btnW / 2
    const cx2 = W - 16 - btnW / 2

    this._makeSmallBtn(cx1, H * 0.345, btnW, 58, CATS_BASIC[0], 2)
    this._makeSmallBtn(cx2, H * 0.345, btnW, 58, CATS_BASIC[1], 3)
    this._makeSmallBtn(cx1, H * 0.435, btnW, 58, CATS_BASIC[2], 4)
    this._makeSmallBtn(cx2, H * 0.435, btnW, 58, CATS_BASIC[3], 5)

    // ── Section: Lycée / Terminale ───────────────────────────────────────────
    this._makeSectionLabel(W / 2, H * 0.527, 'LYCÉE  /  TERMINALE', 0xa855f7, 340)

    this._makeSmallBtn(cx1, H * 0.605, btnW, 58, CATS_ADVANCED[0], 6)
    this._makeSmallBtn(cx2, H * 0.605, btnW, 58, CATS_ADVANCED[1], 7)
    this._makeSmallBtn(cx1, H * 0.695, btnW, 58, CATS_ADVANCED[2], 8)
    this._makeSmallBtn(cx2, H * 0.695, btnW, 58, CATS_ADVANCED[3], 9)

    // ── Back link ─────────────────────────────────────────────────────────────
    const back = this.add
      .text(W / 2, H * 0.935, '← Retour à l\'accueil', {
        fontSize: '13px', fontFamily: "'Segoe UI', Arial, sans-serif", color: '#243044',
      })
      .setOrigin(0.5).setAlpha(0).setInteractive({ useHandCursor: true })
    back.on('pointerover', () => back.setStyle({ color: '#475569' }))
    back.on('pointerout',  () => back.setStyle({ color: '#243044' }))
    back.on('pointerdown', () => {
      this.cameras.main.fadeOut(200, 4, 13, 26)
      this.time.delayedCall(200, () => this.scene.start('BootScene'))
    })
    this.input.keyboard.on('keydown-ESC', () => this.scene.start('BootScene'))

    // ── Staggered reveal ─────────────────────────────────────────────────────
    this.tweens.add({ targets: titleH, alpha: 1, duration: 320, delay: 60 })
    this.tweens.add({ targets: subH,   alpha: 1, duration: 320, delay: 160 })
    this.tweens.add({ targets: back,   alpha: 1, duration: 300, delay: 1000 })
  }

  _spawnFloatSymbols(W, H) {
    this.floatSymbols = []
    for (let i = 0; i < 10; i++) {
      const sym = MATH_SYMBOLS[i % MATH_SYMBOLS.length]
      const x = 12 + Math.random() * (W - 24)
      const y = Math.random() * H
      const size = 9 + Math.floor(Math.random() * 16)
      const alpha = 0.025 + Math.random() * 0.055
      const speed = 5 + Math.random() * 14
      const txt = this.add.text(x, y, sym, {
        fontSize: `${size}px`, fontFamily: 'Arial', color: '#3b82f6',
      }).setAlpha(alpha)
      this.floatSymbols.push({ txt, speed })
    }
  }

  _makeSectionLabel(cx, cy, text, accentColor, delay) {
    const W = this.scale.width
    const lbl = this.add
      .text(cx, cy, text, {
        fontSize: '10px', fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#374151', fontStyle: 'bold', letterSpacing: 1.5,
      })
      .setOrigin(0.5).setAlpha(0)

    const lineLen = 52
    const gapFromText = 10
    const txtHalfW = text.length * 5.5
    const lineY = cy
    const lx1 = cx - txtHalfW - gapFromText
    const lx2 = cx + txtHalfW + gapFromText

    const lines = this.add.graphics().setAlpha(0)
    lines.lineStyle(1, accentColor, 0.45)
    lines.lineBetween(lx1 - lineLen, lineY, lx1, lineY)
    lines.lineBetween(lx2, lineY, lx2 + lineLen, lineY)

    this.tweens.add({ targets: lbl,   alpha: 1, duration: 280, delay })
    this.tweens.add({ targets: lines, alpha: 1, duration: 280, delay })
  }

  _makeFullBtn(cx, cy, btnW, btnH, cat, index) {
    const bg = this.add.graphics().setAlpha(0).setDepth(3)
    const draw = (hovered) => {
      bg.clear()
      bg.fillStyle(cat.bgColor, hovered ? 0.95 : 0.8)
      bg.fillRoundedRect(cx - btnW / 2, cy - btnH / 2, btnW, btnH, 12)
      bg.lineStyle(hovered ? 2 : 1.5, cat.border, hovered ? 1 : 0.6)
      bg.strokeRoundedRect(cx - btnW / 2, cy - btnH / 2, btnW, btnH, 12)
      // Top accent
      bg.fillStyle(cat.border, 0.6)
      bg.fillRoundedRect(cx - btnW / 2 + 2, cy - btnH / 2 + 1, btnW - 4, 2, 2)
      if (hovered) {
        bg.fillStyle(0xffffff, 0.04)
        bg.fillRoundedRect(cx - btnW / 2 + 2, cy - btnH / 2 + 3, btnW - 4, btnH / 2 - 4, 10)
      }
    }
    draw(false)

    // Icon halo
    const halo = this.add.graphics().setAlpha(0).setDepth(4)
    halo.fillStyle(cat.border, 0.15)
    halo.fillCircle(cx - btnW / 2 + 34, cy, 22)

    const iconTxt = this.add
      .text(cx - btnW / 2 + 34, cy, cat.icon, {
        fontSize: '24px', fontFamily: 'Arial', color: cat.txt, fontStyle: 'bold',
      })
      .setOrigin(0.5).setAlpha(0).setDepth(5)

    const labelTxt = this.add
      .text(cx - btnW / 2 + 68, cy - 8, cat.label, {
        fontSize: '17px', fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#e2e8f0', fontStyle: 'bold',
      })
      .setOrigin(0, 0.5).setAlpha(0).setDepth(5)

    const subTxt = this.add
      .text(cx - btnW / 2 + 68, cy + 10, cat.sub, {
        fontSize: '11px', fontFamily: "'Segoe UI', Arial, sans-serif", color: '#475569',
      })
      .setOrigin(0, 0.5).setAlpha(0).setDepth(5)

    const hs = parseInt(localStorage.getItem(`mathrun_hs_${cat.key}`) || '0', 10)
    const badgeTxt = this.add
      .text(cx + btnW / 2 - 14, hs > 0 ? cy - 10 : cy, `${cat.count} q`, {
        fontSize: '11px', fontFamily: 'Arial', color: cat.txt,
      })
      .setOrigin(1, 0.5).setAlpha(0).setDepth(5)

    const hsBadge = hs > 0
      ? this.add.text(cx + btnW / 2 - 14, cy + 10, `★ ${hs}`, {
          fontSize: '12px', fontFamily: "'Segoe UI', Arial, sans-serif",
          color: '#fbbf24', fontStyle: 'bold',
        }).setOrigin(1, 0.5).setAlpha(0).setDepth(5)
      : null

    const hit = this.add.rectangle(cx, cy, btnW, btnH, 0, 0).setDepth(6).setInteractive({ useHandCursor: true })
    hit.on('pointerover', () => draw(true))
    hit.on('pointerout',  () => draw(false))
    hit.on('pointerdown', () => {
      this.cameras.main.fadeOut(220, 4, 13, 26)
      this.time.delayedCall(220, () => this.scene.start('GameScene', { category: cat.key }))
    })

    const delay = 240 + index * 70
    const targets = [bg, halo, iconTxt, labelTxt, subTxt, badgeTxt]
    if (hsBadge) targets.push(hsBadge)
    targets.forEach(o => this.tweens.add({ targets: o, alpha: 1, duration: 260, delay }))
  }

  _makeSmallBtn(cx, cy, btnW, btnH, cat, index) {
    const bg = this.add.graphics().setAlpha(0).setDepth(3)
    const draw = (hovered) => {
      bg.clear()
      bg.fillStyle(cat.bgColor, hovered ? 0.95 : 0.78)
      bg.fillRoundedRect(cx - btnW / 2, cy - btnH / 2, btnW, btnH, 10)
      bg.lineStyle(hovered ? 2 : 1.5, cat.border, hovered ? 1 : 0.55)
      bg.strokeRoundedRect(cx - btnW / 2, cy - btnH / 2, btnW, btnH, 10)
      // Top accent
      bg.fillStyle(cat.border, 0.55)
      bg.fillRoundedRect(cx - btnW / 2 + 2, cy - btnH / 2 + 1, btnW - 4, 2, 2)
      if (hovered) {
        bg.fillStyle(0xffffff, 0.04)
        bg.fillRoundedRect(cx - btnW / 2 + 2, cy - btnH / 2 + 3, btnW - 4, btnH / 2 - 4, 8)
      }
    }
    draw(false)

    // Icon circle
    const halo = this.add.graphics().setAlpha(0).setDepth(4)
    halo.fillStyle(cat.border, 0.18)
    halo.fillCircle(cx - btnW / 2 + 24, cy, 17)

    const iconTxt = this.add
      .text(cx - btnW / 2 + 24, cy, cat.icon, {
        fontSize: cat.icon.length > 2 ? '9px' : '15px',
        fontFamily: 'Arial', color: cat.txt, fontStyle: 'bold',
      })
      .setOrigin(0.5).setAlpha(0).setDepth(5)

    const labelTxt = this.add
      .text(cx - btnW / 2 + 48, cy - 9, cat.label, {
        fontSize: '13px', fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#e2e8f0', fontStyle: 'bold',
      })
      .setOrigin(0, 0.5).setAlpha(0).setDepth(5)

    const subTxt = this.add
      .text(cx - btnW / 2 + 48, cy + 8, cat.sub, {
        fontSize: '11px', fontFamily: "'Segoe UI', Arial, sans-serif", color: '#475569',
      })
      .setOrigin(0, 0.5).setAlpha(0).setDepth(5)

    const hs = parseInt(localStorage.getItem(`mathrun_hs_${cat.key}`) || '0', 10)
    const hsBadge = hs > 0
      ? this.add.text(cx + btnW / 2 - 10, cy, `★${hs}`, {
          fontSize: '10px', fontFamily: "'Segoe UI', Arial, sans-serif",
          color: '#fbbf24', fontStyle: 'bold',
        }).setOrigin(1, 0.5).setAlpha(0).setDepth(5)
      : null

    const hit = this.add.rectangle(cx, cy, btnW, btnH, 0, 0).setDepth(6).setInteractive({ useHandCursor: true })
    hit.on('pointerover', () => draw(true))
    hit.on('pointerout',  () => draw(false))
    hit.on('pointerdown', () => {
      this.cameras.main.fadeOut(220, 4, 13, 26)
      this.time.delayedCall(220, () => this.scene.start('GameScene', { category: cat.key }))
    })

    const delay = 240 + index * 55
    const targets = [bg, halo, iconTxt, labelTxt, subTxt]
    if (hsBadge) targets.push(hsBadge)
    targets.forEach(o => this.tweens.add({ targets: o, alpha: 1, duration: 240, delay }))
  }

  update(time, delta) {
    if (!this.floatSymbols) return
    const H = this.scale.height
    const dt = delta / 1000
    this.floatSymbols.forEach(({ txt, speed }) => {
      txt.y -= speed * dt
      if (txt.y < -24) txt.y = H + 24
    })
  }
}
