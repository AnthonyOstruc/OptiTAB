// Procedural audio — no files, no loading.
// A single AudioContext is shared across all scenes for the lifetime of the page.

let _ctx = null

function getCtx() {
  if (!_ctx) _ctx = new (window.AudioContext || window.webkitAudioContext)()
  if (_ctx.state === 'suspended') _ctx.resume()
  return _ctx
}

function tone(freq, dur, vol = 0.18, type = 'sine', delay = 0) {
  try {
    const c = getCtx()
    const osc  = c.createOscillator()
    const gain = c.createGain()
    osc.connect(gain)
    gain.connect(c.destination)
    osc.type = type
    osc.frequency.value = freq
    const t = c.currentTime + delay
    gain.gain.setValueAtTime(vol, t)
    gain.gain.exponentialRampToValueAtTime(0.0001, t + dur)
    osc.start(t)
    osc.stop(t + dur + 0.02)
  } catch (_) { /* AudioContext unavailable (e.g. server-side render) */ }
}

export const sfx = {
  // Rising three-note chime  C5 → E5 → G5
  correct() {
    [[523, 0], [659, 0.11], [784, 0.22]].forEach(([f, d]) =>
      tone(f, 0.18, 0.18, 'sine', d)
    )
  },

  // Descending sawtooth buzz
  wrong() {
    try {
      const c = getCtx()
      const osc = c.createOscillator()
      const gain = c.createGain()
      osc.connect(gain)
      gain.connect(c.destination)
      osc.type = 'sawtooth'
      osc.frequency.setValueAtTime(270, c.currentTime)
      osc.frequency.exponentialRampToValueAtTime(130, c.currentTime + 0.28)
      gain.gain.setValueAtTime(0.2, c.currentTime)
      gain.gain.exponentialRampToValueAtTime(0.0001, c.currentTime + 0.28)
      osc.start(c.currentTime)
      osc.stop(c.currentTime + 0.3)
    } catch (_) {}
  },

  // Quick ascending arpeggio  A4 C#5 E5 A5
  speedUp() {
    [440, 554, 659, 880].forEach((f, i) =>
      tone(f, 0.13, 0.14, 'sine', i * 0.07)
    )
  },

  // Slow descending melody  G4 E4 D4 C4
  gameOver() {
    [392, 330, 294, 262].forEach((f, i) =>
      tone(f, 0.22, 0.18, 'sine', i * 0.19)
    )
  },

  // Soft high tick
  laneSwitch() {
    tone(720, 0.06, 0.05, 'sine')
  },
}
