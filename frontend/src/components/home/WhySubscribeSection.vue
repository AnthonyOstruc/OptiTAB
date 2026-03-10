<template>
  <section class="why-section">
    <div class="why-container">

      <!-- Header -->
      <div class="why-header">
        <span class="why-eyebrow">Pourquoi s'abonner ?</span>
        <h2 class="why-title">
          Découvre gratuitement, puis <span class="why-highlight">débloque tout</span>
        </h2>
        <p class="why-desc">
          Explore OptiTAB sans engagement. Quand tu es prêt, l'abonnement te donne accès à tout.
        </p>
      </div>

      <!-- Desktop comparison table -->
      <div class="cmp-wrap">
        <!-- sticky column headers -->
        <div class="cmp-grid cmp-head">
          <div class="cmp-label-col"></div>

          <!-- Free -->
          <div class="cmp-col-head tier-free">
            <div class="tier-icon tier-icon-free">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
            </div>
            <p class="tier-name">Gratuit</p>
            <p class="tier-sub">Sans inscription</p>
          </div>

          <!-- Discovery -->
          <div class="cmp-col-head tier-discovery">
            <div class="tier-icon tier-icon-discovery">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
            </div>
            <p class="tier-name">Découverte</p>
            <p class="tier-sub">Compte gratuit</p>
          </div>

          <!-- Premium -->
          <div class="cmp-col-head tier-premium">
            <div class="tier-icon tier-icon-premium">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            </div>
            <p class="tier-name">Abonnement</p>
            <p class="tier-sub">Dès 3,99€</p>
            <span class="recommended-badge">Recommandé</span>
          </div>
        </div>

        <!-- Feature rows -->
        <div class="cmp-body">
          <div class="cmp-grid cmp-row" v-for="(row, i) in features" :key="i" :class="{ 'row-alt': i % 2 === 1 }">
            <div class="cmp-label-col row-label">{{ row.label }}</div>
            <div class="cmp-row-cell">
              <template v-if="row.free">
                <CheckIcon class-name="check-basic" />
                <span class="cell-text">{{ row.free }}</span>
              </template>
              <CrossIcon v-else />
            </div>
            <div class="cmp-row-cell">
              <template v-if="row.discovery">
                <CheckIcon class-name="check-basic" />
                <span class="cell-text">{{ row.discovery }}</span>
              </template>
              <CrossIcon v-else />
            </div>
            <div class="cmp-row-cell cmp-row-cell--premium">
              <CheckIcon class-name="check-premium" />
              <span class="cell-text cell-text--premium">{{ row.premium }}</span>
            </div>
          </div>
        </div>

        <!-- CTA row -->
        <div class="cmp-grid cmp-cta">
          <div class="cmp-label-col"></div>
          <div class="cmp-cta-cell">
            <button class="cta-btn cta-btn--free" @click="$emit('explore-free')">Explorer</button>
          </div>
          <div class="cmp-cta-cell">
            <button class="cta-btn cta-btn--discovery" @click="$emit('create-account')">Créer un compte</button>
          </div>
          <div class="cmp-cta-cell cmp-cta-cell--premium">
            <button class="cta-btn cta-btn--premium" @click="$emit('subscribe')">S'abonner →</button>
            <span class="cta-note">Sans engagement</span>
          </div>
        </div>
      </div>

      <!-- Mobile cards -->
      <div class="mob-cards">

        <!-- Premium card -->
        <div class="mob-premium">
          <div class="mob-premium-top">
            <span class="mob-recommended">Recommandé</span>
            <div class="mob-premium-title-row">
              <div class="tier-icon tier-icon-premium">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
              </div>
              <div>
                <p class="mob-plan-name">Abonnement</p>
                <p class="mob-plan-price">Dès <strong>3,99€</strong></p>
              </div>
            </div>
          </div>
          <div class="mob-premium-body">
            <ul class="mob-features">
              <li v-for="f in features" :key="f.label">
                <span class="mob-chk">
                  <svg width="10" height="10" viewBox="0 0 12 12" fill="none"><path d="M2 6l3 3 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </span>
                <span><strong>{{ f.premium }}</strong><span class="mob-feat-cat"> · {{ f.label }}</span></span>
              </li>
            </ul>
            <button class="mob-subscribe-btn" @click="$emit('subscribe')">S'abonner maintenant →</button>
            <p class="mob-security">🔒 Paiement sécurisé · Sans engagement</p>
          </div>
        </div>

        <!-- Divider -->
        <div class="mob-sep"><span>ou commencer gratuitement</span></div>

        <!-- Free tiers 2-col -->
        <div class="mob-free-grid">

          <!-- Gratuit -->
          <div class="mob-free-card">
            <div class="mob-free-card-head">
              <div class="tier-icon tier-icon-free">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
              </div>
              <div>
                <p class="mob-free-name">Gratuit</p>
                <p class="mob-free-badge mob-free-badge--free">Sans inscription</p>
              </div>
            </div>
            <p class="mob-free-hook">Explore dès maintenant</p>
            <ul class="mob-free-list">
              <li>✓ Cours en accès partiel</li>
              <li>✓ Fiches de révision</li>
              <li>✓ Outils de calcul</li>
            </ul>
            <button class="mob-free-btn mob-free-btn--free" @click="$emit('explore-free')">Explorer →</button>
          </div>

          <!-- Découverte -->
          <div class="mob-free-card mob-free-card--discovery">
            <div class="mob-free-card-head">
              <div class="tier-icon tier-icon-discovery">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
              </div>
              <div>
                <p class="mob-free-name">Découverte</p>
                <p class="mob-free-badge mob-free-badge--discovery">Compte gratuit</p>
              </div>
            </div>
            <p class="mob-free-hook">1 chapitre complet offert</p>
            <ul class="mob-free-list">
              <li>✓ Cours complet</li>
              <li>✓ Exercices corrigés</li>
              <li>✓ Fiche de synthèse</li>
            </ul>
            <button class="mob-free-btn mob-free-btn--discovery" @click="$emit('create-account')">Créer un compte →</button>
          </div>

        </div>

      </div>

      <!-- Footer note -->
      <p class="why-footnote">
        💡 <strong>Commence gratuitement</strong> — aucune carte bancaire requise. Tu ne paies que si tu veux aller plus loin.
      </p>

    </div>
  </section>
</template>

<script setup>
import { h } from 'vue'

defineEmits(['explore-free', 'create-account', 'subscribe'])

const features = [
  { label: 'Cours en ligne',       free: 'Accès partiel',    discovery: '1 chapitre complet', premium: 'Tous les chapitres' },
  { label: 'Fiches de synthèse',   free: 'Accès partiel',    discovery: '1 chapitre complet', premium: 'Toutes les fiches' },
  { label: 'Exercices corrigés',   free: 'Accès partiel',    discovery: '1 chapitre complet', premium: 'Tous les exercices' },
  { label: 'Suivi de progression', free: null,               discovery: null,                 premium: 'Complet' },
  { label: 'Révisions adaptées',   free: null,               discovery: null,                 premium: 'Oui' },
  { label: 'Outils de calcul',     free: 'Basiques',         discovery: 'Basiques',           premium: 'Avancés' },
]

const CheckIcon = (props) => h('span', { class: ['cell-check', props.className] },
  [h('svg', { width: 11, height: 11, viewBox: '0 0 12 12', fill: 'none' },
    [h('path', { d: 'M2 6l3 3 5-5', stroke: 'currentColor', 'stroke-width': 2, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' })]
  )]
)

const CrossIcon = () => h('span', { class: 'cell-cross' },
  [h('svg', { width: 11, height: 11, viewBox: '0 0 12 12', fill: 'none' },
    [h('path', { d: 'M3 3l6 6M9 3l-6 6', stroke: 'currentColor', 'stroke-width': 1.8, 'stroke-linecap': 'round' })]
  )]
)
</script>

<style scoped lang="scss">
// ─────────────────────────────────────────
// Tokens
// ─────────────────────────────────────────
$blue-dark:  #2563eb;
$blue-mid:   #3b82f6;
$blue-light: #f0f7ff;
$blue-border:#c7dcfe;
$text-dark:  #0f172a;
$text-mid:   #334155;
$text-soft:  #64748b;
$border:     #e2e8f0;
$row-alt:    #f8fafc;
$radius-lg:  20px;
$radius-md:  12px;
$radius-sm:  8px;

// ─────────────────────────────────────────
// Section wrapper
// ─────────────────────────────────────────
.why-section {
  padding: 96px 0 80px;
  background: #ffffff;
}

.why-container {
  max-width: 1080px;
  margin: 0 auto;
  padding: 0 24px;
}

// ─────────────────────────────────────────
// Header
// ─────────────────────────────────────────
.why-header {
  text-align: center;
  margin-bottom: 56px;
}

.why-eyebrow {
  display: inline-block;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: $blue-mid;
  background: $blue-light;
  border: 1px solid $blue-border;
  border-radius: 50px;
  padding: 5px 18px;
  margin-bottom: 20px;
}

.why-title {
  font-size: 2.4rem;
  font-weight: 900;
  color: $text-dark;
  line-height: 1.2;
  margin: 0 0 16px;
}

.why-highlight {
  background: linear-gradient(135deg, $blue-dark 0%, #3b82f6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.why-desc {
  font-size: 1.05rem;
  color: $text-soft;
  line-height: 1.65;
  max-width: 520px;
  margin: 0 auto;
}

// ─────────────────────────────────────────
// Comparison grid
// ─────────────────────────────────────────
.cmp-wrap {
  border-radius: $radius-lg;
  overflow: hidden;
  border: 1px solid $border;
  box-shadow: 0 2px 32px rgba(0,0,0,0.06);
  margin-bottom: 40px;
}

.cmp-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr 1.15fr;
}

// ─────────────────────────────────────────
// Column headers
// ─────────────────────────────────────────
.cmp-head {
  border-bottom: 1px solid $border;
  background: #fff;
}

.cmp-label-col {
  padding: 0 24px;
  display: flex;
  align-items: center;
  border-right: 1px solid $border;
  background: #fafafa;
}

.cmp-col-head {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  gap: 6px;
  padding: 28px 16px 22px;
  text-align: center;
  position: relative;
  border-right: 1px solid $border;

  &:last-child {
    border-right: none;
  }
}

.tier-free {
  background: #fff;
}

.tier-discovery {
  background: #fff;
}

.tier-premium {
  background: linear-gradient(180deg, $blue-light 0%, #fff 100%);
  border-left: 2px solid $blue-border !important;
  border-right: none !important;
}

.tier-icon {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2px;
}

.tier-icon-free      { background: #f0fdf4; color: #16a34a; }
.tier-icon-discovery { background: #fffbeb; color: #d97706; }
.tier-icon-premium   { background: $blue-light; color: $blue-mid; }

.tier-name {
  font-size: 0.92rem;
  font-weight: 800;
  color: $text-dark;
  margin: 0;
}

.tier-sub {
  font-size: 0.72rem;
  color: $text-soft;
  margin: 0;
}

.recommended-badge {
  display: inline-block;
  background: $blue-mid;
  color: #fff;
  font-size: 0.62rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 4px 14px;
  border-radius: 50px;
  white-space: nowrap;
  margin-top: 6px;
}

// ─────────────────────────────────────────
// Feature rows
// ─────────────────────────────────────────
.cmp-body {
  background: #fff;
}

.cmp-row {
  border-bottom: 1px solid #f1f5f9;
  min-height: 52px;

  &:last-child { border-bottom: none; }
}

.row-alt {
  .cmp-label-col,
  .cmp-row-cell { background: $row-alt; }
  .cmp-row-cell--premium { background: mix(#eff6ff, #f8fafc, 60%); }
}

.row-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: $text-dark;
  padding: 0 24px;
  min-height: 52px;
}

.cmp-row-cell {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 0 16px;
  font-size: 0.875rem;
  color: $text-mid;
  border-right: 1px solid #f1f5f9;
  background: #fff;

  &:last-child { border-right: none; }
}

.cmp-row-cell--premium {
  background: rgba(239, 246, 255, 0.55);
  border-left: 2px solid $blue-border;
  border-right: none;
}

// Cell icons
.cell-check {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  flex-shrink: 0;
}

.check-basic {
  background: #dcfce7;
  color: #15803d;
}

.check-premium {
  background: $blue-light;
  color: $blue-mid;
}

.cell-cross {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #f1f5f9;
  color: #cbd5e1;
  flex-shrink: 0;
}

.cell-text {
  font-size: 0.84rem;
  color: $text-mid;
}

.cell-text--premium {
  font-weight: 700;
  color: $text-dark;
}

// ─────────────────────────────────────────
// CTA row
// ─────────────────────────────────────────
.cmp-cta {
  border-top: 1px solid $border;
  background: #fafafa;
}

.cmp-cta-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 20px 16px;
  border-right: 1px solid $border;

  &:last-child { border-right: none; }
}

.cmp-cta-cell--premium {
  background: $blue-light;
  border-left: 2px solid $blue-border;
  border-right: none;
}

// ─────────────────────────────────────────
// Shared CTA buttons
// ─────────────────────────────────────────
.cta-btn {
  padding: 10px 18px;
  border-radius: $radius-sm;
  font-size: 0.875rem;
  font-weight: 700;
  cursor: pointer;
  border: none;
  transition: all 0.18s ease;
  white-space: nowrap;
  line-height: 1;
}

.cta-btn--full { width: 100%; text-align: center; }

.cta-btn--free {
  background: #f0fdf4;
  color: #15803d;
  border: 1.5px solid #bbf7d0;
  &:hover { background: #dcfce7; }
}

.cta-btn--discovery {
  background: #fffbeb;
  color: #b45309;
  border: 1.5px solid #fde68a;
  &:hover { background: #fef3c7; }
}

.cta-btn--premium {
  background: $blue-mid;
  color: #fff;
  box-shadow: 0 2px 14px rgba(37,99,235,0.22);
  &:hover {
    background: darken($blue-mid, 5%);
    transform: translateY(-1px);
    box-shadow: 0 4px 18px rgba(37,99,235,0.32);
  }
}

.cta-btn--outline {
  background: #fff;
  color: $text-mid;
  border: 1.5px solid $border;
  &:hover { background: #f8fafc; }
}

.cta-note {
  font-size: 0.7rem;
  color: $text-soft;
}

// ─────────────────────────────────────────
// Footer note
// ─────────────────────────────────────────
.why-footnote {
  text-align: center;
  font-size: 0.9rem;
  color: $text-soft;
  line-height: 1.6;
  margin: 0;
  padding: 20px 20px;
  background: #f8fafc;
  border-radius: $radius-md;
  border: 1px solid $border;
}

// ─────────────────────────────────────────
// Mobile cards
// ─────────────────────────────────────────
.mob-cards {
  display: none;
  margin-bottom: 32px;
}

// ── Premium card ──
.mob-premium {
  border-radius: $radius-md;
  overflow: hidden;
  border: 1.5px solid $blue-border;
  box-shadow: 0 4px 24px rgba(37, 99, 235, 0.1);
  margin-bottom: 16px;
}

.mob-premium-top {
  background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
  padding: 20px 22px 18px;
}

.mob-recommended {
  display: inline-block;
  background: rgba(255,255,255,0.2);
  color: #fff;
  font-size: 0.62rem;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 3px 12px;
  border-radius: 50px;
  border: 1px solid rgba(255,255,255,0.35);
  margin-bottom: 14px;
}

.mob-premium-title-row {
  display: flex;
  align-items: center;
  gap: 12px;

  .tier-icon-premium {
    background: rgba(255,255,255,0.15);
    color: #fff;
    border: 1px solid rgba(255,255,255,0.25);
  }
}

.mob-plan-name {
  font-size: 1.15rem;
  font-weight: 800;
  color: #fff;
  margin: 0;
}

.mob-plan-price {
  font-size: 0.82rem;
  color: rgba(255,255,255,0.8);
  margin: 2px 0 0;

  strong { color: #fff; }
}

.mob-premium-body {
  background: #fff;
  padding: 20px 22px 22px;
}

.mob-features {
  list-style: none;
  padding: 0;
  margin: 0 0 20px;
  display: flex;
  flex-direction: column;
  gap: 11px;

  li {
    display: flex;
    align-items: flex-start;
    gap: 9px;
    font-size: 0.875rem;
    color: $text-mid;
    line-height: 1.4;
  }
}

.mob-chk {
  flex-shrink: 0;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: $blue-light;
  color: $blue-mid;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-top: 1px;
}

.mob-feat-cat {
  color: $text-soft;
  font-weight: 400;
}

.mob-subscribe-btn {
  width: 100%;
  padding: 13px 16px;
  background: $blue-mid;
  color: #fff;
  border: none;
  border-radius: $radius-sm;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.18s ease;
  text-align: center;

  &:hover {
    background: darken($blue-mid, 6%);
    transform: translateY(-1px);
  }
}

.mob-security {
  text-align: center;
  font-size: 0.72rem;
  color: $text-soft;
  margin: 10px 0 0;
}

// ── Separator ──
.mob-sep {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0 0 14px;
  color: $text-soft;
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.04em;
  text-transform: uppercase;

  &::before, &::after {
    content: '';
    flex: 1;
    height: 1px;
    background: $border;
  }
}

// ── Free tiers 2-col grid ──
.mob-free-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.mob-free-card {
  background: #fff;
  border: 1px solid $border;
  border-radius: $radius-md;
  padding: 16px 14px 18px;
  display: flex;
  flex-direction: column;
  gap: 0;

  &--discovery {
    background: #fffdf5;
    border-color: #fde68a;
  }
}

.mob-free-card-head {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.mob-free-name {
  font-size: 0.88rem;
  font-weight: 800;
  color: $text-dark;
  margin: 0;
  line-height: 1.2;
}

.mob-free-badge {
  display: inline-block;
  font-size: 0.62rem;
  font-weight: 700;
  border-radius: 50px;
  padding: 2px 8px;
  margin-top: 3px;

  &--free {
    background: #f0fdf4;
    color: #15803d;
    border: 1px solid #bbf7d0;
  }

  &--discovery {
    background: #fffbeb;
    color: #b45309;
    border: 1px solid #fde68a;
  }
}

.mob-free-hook {
  font-size: 0.78rem;
  font-weight: 700;
  color: $text-dark;
  margin: 0 0 8px;
  line-height: 1.3;
}

.mob-free-list {
  list-style: none;
  padding: 0;
  margin: 0 0 14px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;

  li {
    font-size: 0.72rem;
    color: $text-soft;
    line-height: 1.3;
  }
}

.mob-free-btn {
  width: 100%;
  padding: 9px 10px;
  border-radius: $radius-sm;
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
  border: none;
  transition: all 0.15s ease;
  text-align: center;
  margin-top: auto;

  &--free {
    background: #f0fdf4;
    color: #15803d;
    border: 1px solid #bbf7d0;
    &:hover { background: #dcfce7; }
  }

  &--discovery {
    background: #fffbeb;
    color: #b45309;
    border: 1px solid #fde68a;
    &:hover { background: #fef3c7; }
  }
}

// ─────────────────────────────────────────
// Responsive
// ─────────────────────────────────────────
@media (max-width: 700px) {
  .cmp-wrap { display: none; }
  .mob-cards { display: block; }

  .why-section { padding: 64px 0 48px; }
  .why-title { font-size: 1.75rem; }
  .why-header { margin-bottom: 36px; }
}

@media (max-width: 600px) {
  .why-container { padding: 0 16px; }
  .why-title { font-size: 1.55rem; }
  .mob-tier-sub { display: none; }
}

@media (max-width: 420px) {
  .why-section { padding: 44px 0 36px; }
  .why-container { padding: 0 12px; }
  .why-title { font-size: 1.35rem; line-height: 1.25; }
  .why-desc { font-size: 0.88rem; }
  .mob-premium-top { padding: 18px 18px 16px; }
  .mob-premium-body { padding: 18px 18px 20px; }
  .mob-free-card { padding: 14px 10px 14px; }
  .mob-free-hook { font-size: 0.72rem; }
}
</style>
