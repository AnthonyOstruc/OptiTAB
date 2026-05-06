import Phaser from 'phaser'

const MATH_SYMBOLS = ['∫', 'π', '∞', '∑', '√', '∂', 'θ', 'λ', 'Δ', 'φ', 'α', '≤', '≥', 'σ', 'ε']

export default class BootScene extends Phaser.Scene {
  constructor() { super({ key: 'BootScene' }) }

  create() {
    const W = this.scale.width
    const H = this.scale.height

    // ── Background ──────────────────────────────────────────────────────────
    this.add.rectangle(W / 2, H / 2, W, H, 0x040d1a)

    // Subtle dot grid
    const dots = this.add.graphics()
    dots.fillStyle(0x1e3a8a, 0.45)
    for (let x = 24; x < W; x += 32) {
      for (let y = 24; y < H; y += 32) {
        dots.fillCircle(x, y, 1)
      }
    }

    // Lane strips
    const laneW = W / 3
    const laneColors = [0x152a6b, 0x1e3a8a, 0x152a6b]
    for (let i = 0; i < 3; i++) {
      this.add.rectangle((i + 0.5) * laneW, H / 2, laneW - 2, H, laneColors[i]).setAlpha(0.38)
    }
    this.add.rectangle(laneW, H / 2, 1, H, 0x3b82f6, 0.22)
    this.add.rectangle(laneW * 2, H / 2, 1, H, 0x3b82f6, 0.22)

    // ── Floating math symbols ────────────────────────────────────────────────
    this.floatSymbols = []
    for (let i = 0; i < 16; i++) {
      const sym = MATH_SYMBOLS[i % MATH_SYMBOLS.length]
      const x = 12 + Math.random() * (W - 24)
      const y = Math.random() * H
      const size = 10 + Math.floor(Math.random() * 20)
      const alpha = 0.035 + Math.random() * 0.075
      const speed = 7 + Math.random() * 18
      const txt = this.add.text(x, y, sym, {
        fontSize: `${size}px`, fontFamily: 'Arial', color: '#3b82f6',
      }).setAlpha(alpha)
      this.floatSymbols.push({ txt, speed })
    }

    // ── Scrolling lane stripes ───────────────────────────────────────────────
    this.stripes = []
    for (let lane = 0; lane < 3; lane++) {
      for (let row = 0; row < 7; row++) {
        const stripe = this.add.rectangle(
          (lane + 0.5) * laneW, row * 110 + 55, laneW - 14, 38, 0xffffff, 0.025,
        )
        this.stripes.push(stripe)
      }
    }

    // ── Title block ──────────────────────────────────────────────────────────
    // Glow behind title
    const titleGlow = this.add.graphics()
    titleGlow.fillStyle(0x1d4ed8, 0.12)
    titleGlow.fillRoundedRect(W / 2 - 140, H * 0.168, 280, 66, 12)

    const titleTxt = this.add
      .text(W / 2, H * 0.215, 'MATH RUN', {
        fontSize: '50px',
        fontFamily: "'Segoe UI', system-ui, sans-serif",
        color: '#ffd54f',
        fontStyle: 'bold',
        stroke: '#1e3a8a',
        strokeThickness: 7,
      })
      .setOrigin(0.5).setAlpha(0)

    // Golden accent bar
    const accentBar = this.add.graphics().setAlpha(0)
    accentBar.fillStyle(0xfbbf24, 1)
    accentBar.fillRoundedRect(W / 2 - 56, H * 0.268, 112, 3, 2)

    const subtitleTxt = this.add
      .text(W / 2, H * 0.308, 'Entraîne-toi aux mathématiques', {
        fontSize: '14px',
        fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#475569',
        letterSpacing: 0.3,
      })
      .setOrigin(0.5).setAlpha(0)

    // ── Feature cards ────────────────────────────────────────────────────────
    const features = [
      { icon: '←→',  lines: ['Changer', 'de voie'],  color: 0x60a5fa,  hex: '#60a5fa' },
      { icon: '♥',   lines: ['3 vies',  'par partie'], color: 0xf87171, hex: '#f87171' },
      { icon: '∞',   lines: ['Score',   'illimité'],   color: 0xfbbf24, hex: '#fbbf24' },
    ]
    const cW = 136; const cH = 74; const cGap = 7
    const totalCW = cW * 3 + cGap * 2
    const startCX = W / 2 - totalCW / 2 + cW / 2
    const cardY = H * 0.435

    features.forEach((feat, i) => {
      const cx = startCX + i * (cW + cGap)
      const bg = this.add.graphics().setAlpha(0)
      bg.fillStyle(0x0b1a38, 1)
      bg.fillRoundedRect(cx - cW / 2, cardY - cH / 2, cW, cH, 10)
      bg.lineStyle(1, 0x1e3a8a, 0.85)
      bg.strokeRoundedRect(cx - cW / 2, cardY - cH / 2, cW, cH, 10)
      // Top accent bar
      bg.lineStyle(2.5, feat.color, 1)
      bg.lineBetween(cx - cW / 2 + 14, cardY - cH / 2 + 1.5, cx + cW / 2 - 14, cardY - cH / 2 + 1.5)

      const iconT = this.add.text(cx, cardY - 16, feat.icon, {
        fontSize: '19px', fontFamily: 'Arial', color: feat.hex, fontStyle: 'bold',
      }).setOrigin(0.5).setAlpha(0)

      const line1 = this.add.text(cx, cardY + 6, feat.lines[0], {
        fontSize: '11px', fontFamily: "'Segoe UI', Arial, sans-serif", color: '#64748b',
      }).setOrigin(0.5).setAlpha(0)

      const line2 = this.add.text(cx, cardY + 21, feat.lines[1], {
        fontSize: '11px', fontFamily: "'Segoe UI', Arial, sans-serif", color: '#475569',
      }).setOrigin(0.5).setAlpha(0)

      const delay = 460 + i * 70
      this.tweens.add({ targets: bg,    alpha: 1, duration: 300, delay })
      this.tweens.add({ targets: iconT, alpha: 1, duration: 300, delay: delay + 55 })
      this.tweens.add({ targets: line1, alpha: 1, duration: 300, delay: delay + 90 })
      this.tweens.add({ targets: line2, alpha: 1, duration: 300, delay: delay + 110 })
    })

    // ── High score badge ──────────────────────────────────────────────────────
    const cats = ['all','addition','subtraction','multiplication','division','limits','derivatives','integrals','sequences']
    const hiScore = Math.max(...cats.map(c => parseInt(localStorage.getItem(`mathrun_hs_${c}`) || '0', 10)))

    if (hiScore > 0) {
      const hsY = H * 0.60
      const hsBg = this.add.graphics().setAlpha(0)
      hsBg.fillStyle(0x78350f, 0.7)
      hsBg.fillRoundedRect(W / 2 - 100, hsY - 20, 200, 40, 10)
      hsBg.lineStyle(1.5, 0xfbbf24, 0.65)
      hsBg.strokeRoundedRect(W / 2 - 100, hsY - 20, 200, 40, 10)
      const hsTxt = this.add
        .text(W / 2, hsY, `★  Meilleur score : ${hiScore} pts`, {
          fontSize: '14px', fontFamily: "'Segoe UI', Arial, sans-serif",
          color: '#fbbf24', fontStyle: 'bold',
        }).setOrigin(0.5).setAlpha(0)
      this.tweens.add({ targets: [hsBg, hsTxt], alpha: 1, duration: 400, delay: 820 })
    }

    // ── Start button ──────────────────────────────────────────────────────────
    const btnY  = H * 0.795
    const btnW2 = 236
    const btnH2 = 58

    this.btnGlow = this.add.graphics().setAlpha(0).setDepth(4)
    this._drawGlow(this.btnGlow, W / 2, btnY, btnW2 + 12, btnH2 + 12)

    this.btnBg = this.add.graphics().setAlpha(0).setDepth(5)
    this._drawBtn(this.btnBg, W / 2, btnY, btnW2, btnH2, false)

    this.startBtn = this.add
      .text(W / 2, btnY, '▶  Commencer', {
        fontSize: '22px', fontFamily: "'Segoe UI', Arial, sans-serif",
        color: '#ffffff', fontStyle: 'bold',
      })
      .setOrigin(0.5).setDepth(6).setAlpha(0).setInteractive({ useHandCursor: true })

    this.startBtn.on('pointerover', () => this._drawBtn(this.btnBg, W / 2, btnY, btnW2, btnH2, true))
    this.startBtn.on('pointerout',  () => this._drawBtn(this.btnBg, W / 2, btnY, btnW2, btnH2, false))
    this.startBtn.on('pointerdown', () => this.startGame())

    this.input.keyboard.on('keydown-ENTER', () => this.startGame())
    this.input.keyboard.on('keydown-SPACE', () => this.startGame())

    // Keyboard hint
    const kbHint = this.add.text(W / 2, H * 0.915, 'ENTRÉE  ou  ESPACE  pour démarrer', {
      fontSize: '11px', fontFamily: "'Segoe UI', Arial, sans-serif", color: '#1e3a8a',
    }).setOrigin(0.5).setAlpha(0)

    // ── Staggered reveal ─────────────────────────────────────────────────────
    this.tweens.add({ targets: titleTxt,    alpha: 1, duration: 520, delay: 80 })
    this.tweens.add({ targets: accentBar,   alpha: 1, duration: 400, delay: 380 })
    this.tweens.add({ targets: subtitleTxt, alpha: 1, duration: 500, delay: 420 })
    this.tweens.add({ targets: [this.btnBg, this.startBtn], alpha: 1, duration: 420, delay: 760 })
    this.tweens.add({ targets: this.btnGlow, alpha: 0.85, duration: 420, delay: 920 })
    this.tweens.add({ targets: kbHint,      alpha: 1, duration: 400, delay: 1100 })

    // Glow pulse
    this.tweens.add({
      targets: this.btnGlow, alpha: 0.2, duration: 1500, yoyo: true,
      repeat: -1, ease: 'Sine.easeInOut', delay: 1300,
    })
    // Title subtle breathe
    this.tweens.add({
      targets: titleTxt, scaleX: 1.012, scaleY: 1.012,
      duration: 2400, yoyo: true, repeat: -1,
      ease: 'Sine.easeInOut', delay: 900,
    })

    this.stripeSpeed = 42
  }

  _drawBtn(g, x, y, w, h, hover) {
    g.clear()
    g.fillStyle(hover ? 0x1d4ed8 : 0x2563eb, 1)
    g.fillRoundedRect(x - w / 2, y - h / 2, w, h, 16)
    // Top shine
    g.fillStyle(0xffffff, 0.1)
    g.fillRoundedRect(x - w / 2 + 4, y - h / 2 + 4, w - 8, h * 0.42, 12)
    if (hover) {
      g.lineStyle(2, 0x93c5fd, 0.85)
      g.strokeRoundedRect(x - w / 2, y - h / 2, w, h, 16)
    }
  }

  _drawGlow(g, x, y, w, h) {
    g.clear()
    g.lineStyle(2.5, 0x3b82f6, 0.75)
    g.strokeRoundedRect(x - w / 2, y - h / 2, w, h, 20)
  }

  startGame() {
    this.cameras.main.fadeOut(250, 4, 13, 26)
    this.time.delayedCall(250, () => this.scene.start('MenuScene'))
  }

  update(time, delta) {
    const H = this.scale.height
    const dt = delta / 1000
    const sp = this.stripeSpeed * dt
    this.stripes.forEach(s => {
      s.y += sp
      if (s.y > H + 20) s.y = -20
    })
    this.floatSymbols.forEach(({ txt, speed }) => {
      txt.y -= speed * dt
      if (txt.y < -24) txt.y = H + 24
    })
  }
}
