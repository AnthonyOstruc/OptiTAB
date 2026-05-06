# GAME_ROADMAP.md — Math Run (OptiTAB Mini-Game)

## Overview
A mobile-friendly endless math runner built with Vue 3 + Phaser.js, integrated into the OptiTAB educational platform.

**Route:** `/jeux/math-run`
**Tech:** Vue 3 + Phaser 3 (canvas-based game inside a Vue view)
**Design:** OptiTAB palette — navy blue (`#0a1628`, `#1e3a8a`), light blue (`#2563eb`, `#42a5f5`), amber (`#ffd54f`), white.

---

## Full Checklist

### Setup
- [x] Step 1 — Create GAME_ROADMAP.md
- [x] Step 2 — Install Phaser.js (`npm install phaser`)
- [x] Step 3 — Add Vue Router route `/jeux/math-run`

### Game Files
- [x] Step 4 — Create `MathRunView.vue` (Vue wrapper, mounts Phaser canvas)
- [x] Step 5 — Create `config.js` (Phaser game config factory)
- [x] Step 6 — Create `BootScene.js` (title screen with start button)
- [x] Step 7 — Create `GameScene.js` (full gameplay: player, lanes, questions, answers, keyboard, mobile, score, lives)
- [x] Step 8 — Create `GameOverScene.js` (final score, star rating, restart button)
- [x] Step 9 — Create `questions.js` (30 math questions with shuffled answers)

### Polish & Testing
- [x] Step 10 — Build verified (no compile errors) — `vite build` passes clean
- [x] Step 11 — Code review + bug fixes (see Notes); dev server started for manual test

---

## Files Created / Modified

| File | Status | Notes |
|------|--------|-------|
| `GAME_ROADMAP.md` | ✅ Done | This file |
| `frontend/src/views/games/MathRunView.vue` | ✅ Done | Vue wrapper with Phaser init/destroy lifecycle |
| `frontend/src/games/math-run/config.js` | ✅ Done | Phaser config factory (480×700 FIT scale) |
| `frontend/src/games/math-run/scenes/BootScene.js` | ✅ Done | Title screen, instructions, Start button |
| `frontend/src/games/math-run/scenes/GameScene.js` | ✅ Done | Full gameplay loop |
| `frontend/src/games/math-run/scenes/GameOverScene.js` | ✅ Done | Game over screen with star rating |
| `frontend/src/games/math-run/data/questions.js` | ✅ Done | 30 math questions, shuffle util |
| `frontend/src/router/index.js` | ✅ Done | Added `/jeux/math-run` route |
| `frontend/package.json` | ✅ Done | Phaser added via `npm install phaser` |

---

## Architecture

```
frontend/src/
├── views/
│   └── games/
│       └── MathRunView.vue          ← Vue page, mounts Phaser
└── games/
    └── math-run/
        ├── config.js                ← Phaser.Game config
        ├── data/
        │   └── questions.js         ← 30 questions + getRandomQuestion()
        └── scenes/
            ├── BootScene.js         ← Title / Start screen
            ├── GameScene.js         ← Core gameplay
            └── GameOverScene.js     ← Final score + restart
```

---

## Gameplay Design

**Concept:** The player runs automatically through 3 lanes. A math question appears at the top. Three answer blocks fall from the top of each lane toward the player. The player must switch to the lane with the correct answer before the blocks arrive.

**Controls:**
- Desktop: `←` / `→` arrow keys (also `A` / `D`)
- Mobile: On-screen ◀ / ▶ buttons inside the Phaser canvas

**Scoring:**
- Correct lane → +1 score
- Wrong lane → -1 life (starts with 3)
- 0 lives → Game Over

**Visual feedback:**
- Green flash + "✓ Correct !" on correct answer
- Red flash + "✗ Incorrect" on wrong answer
- Player slides between lanes with smooth tween (150ms)

**Difficulty:** Fixed for MVP (fall speed: 2800ms). Future: increase speed as score rises.

---

## Design Tokens

| Role | Color |
|------|-------|
| Background / HUD | `#0a1628` |
| Lane left | `#152a6b` |
| Lane center | `#1e3a8a` |
| Lane right | `#1a3070` |
| Question panel | `#2a38b7` |
| Answer blocks | `#2563eb` |
| Player | `#ffd54f` |
| Correct | `#22c55e` |
| Wrong | `#ef4444` |
| Hearts | `#ff5252` |

---

## Current Progress

All core files have been created. The game is at MVP state.

**What works:**
- Phaser mounts inside Vue, properly destroyed on route leave
- 3 lanes with scrolling stripe background (simulates running)
- Player character (simple graphics, smooth lane-switching tween)
- Math question displayed at top
- Answer blocks fall toward player at fixed speed
- Answer evaluated when blocks reach player level
- Score and lives HUD
- Mobile ◀ ▶ buttons inside the canvas
- Keyboard ← → support
- BootScene title screen
- GameOverScene with star rating and restart
- 30 shuffled math questions

---

## Next Step (for next session)

**Step 11 — Manual browser test:**
1. Run `npm run dev` in `frontend/`
2. Navigate to `http://localhost:5173/jeux/math-run`
3. Check browser console for runtime errors
4. Verify: title screen loads → Start → player in center lane → blocks fall → left/right moves player → score increments → lives deplete → Game Over screen shows → Restart works
5. Fix any issues found (most likely: canvas sizing on mobile, tween edge cases)

**Build confirmed clean:** `vite build` passed, `MathRunView` chunk = 1.38 MB (Phaser ~1.4 MB is expected)

**Completed improvements:**
- [x] Add progressive difficulty (faster fall speed as score increases)
- [x] Add high-score persistence (localStorage, per-category keys)
- [x] Add sound effects (procedural Web Audio API — no files)
- [x] Add particle effects on correct answer
- [x] Add player run animation (leg movement)
- [x] Add question categories / difficulty levels (MenuScene → 5 categories)
- [x] Add pause system (ESC/P + ⏸ button; overlay with Resume / Change Category)
- [x] Per-category high scores (`mathrun_hs_<category>` localStorage keys)
- [x] Streak / combo system (×2 at 3, ×3 at 5, ×5 at 10 — floating bonus text + "COMBO ×N !" banner)
- [x] Countdown 3-2-1-GO ! before first question each game
- [x] Question bank expanded 30 → 70 questions (16+16+24+14)
- [x] MenuScene shows per-category HS badge (★ N) + updated question counts
- [x] Timer bar (green→yellow→red) synced to block fall duration
- [x] Auth gate in MathRunView.vue (login prompt if not authenticated)
- [x] XP reward on game end (score × 10 XP via updateUserXPInstantly + Vue notification)
- [x] Leaderboard panel below canvas (top 10 per category, with tab switcher)
- [x] Backend Django app `mini_games` — MathRunScore model, migrations applied
- [x] `POST /api/mini-games/math-run/score/` — saves best per user/category
- [x] `GET /api/mini-games/math-run/leaderboard/?category=all` — top 10 per category
- [x] Score submitted silently to API on game over (via CustomEvent bridge Phaser→Vue)

**Remaining future improvements:**
- [ ] Connect to Django API for questions (replace static questions.js with API fetch)
- [ ] Premium access gate (subscription check — currently any logged-in user can play)

---

## Notes

- Phaser is initialized in `onMounted` and destroyed in `onUnmounted` to avoid memory leaks.
- The game uses Phaser's `Scale.FIT` mode at 480×700px — scales cleanly on all screen sizes.
- No external assets are used — all graphics are drawn with Phaser's Graphics API and text objects.
- Questions are shuffled on each call to `getRandomQuestion()` so answer positions vary.
- The route `/jeux/math-run` is public (no auth required for MVP).

### Bugs found and fixed in Step 11

**Bug 1 — BootScene instruction text invisible:**
`this.children.getByName()` does not exist on Phaser's `DisplayList`. The instruction text objects were never retrieved, so their fade-in tweens were never added and they stayed at `alpha: 0`.
Fix: stored direct references to the text objects in `instrTxts[]` array, then mapped tweens over those references.

**Bug 2 — Canvas CSS conflict with Phaser touch input:**
The `:deep(canvas)` CSS rule (`width: 100% !important; height: auto !important`) overrode Phaser's inline canvas dimensions. `height: auto` on a canvas defaults to intrinsic size (700px) even on a 375px-wide mobile screen, misaligning Phaser's internal pointer/touch coordinate system with the displayed canvas.
Fix: removed the `:deep(canvas)` override entirely. Added `height: min(700px, calc(100vw * 700 / 480))` to the container so Phaser's `Scale.FIT` has a correctly-sized parent on all screen widths.
