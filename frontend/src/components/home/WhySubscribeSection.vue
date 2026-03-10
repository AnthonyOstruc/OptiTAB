<template>
  <section class="why-subscribe-section">
    <div class="why-subscribe-container">
      <!-- Header -->
      <div class="why-subscribe-header">
        <div class="why-badge">
          <span class="badge-icon">🎯</span>
          <span class="badge-text">Pourquoi s'abonner ?</span>
        </div>
        <h2 class="why-title">
          Découvre gratuitement, puis <span class="why-highlight">débloque tout</span>
        </h2>
        <p class="why-desc">
          Explore OptiTAB sans engagement. Quand tu es prêt, l'abonnement te donne accès à tout.
        </p>
      </div>

      <!-- Comparison Table -->
      <div class="comparison-table">
        <!-- Table Header -->
        <div class="table-row table-header-row">
          <div class="table-cell table-feature-label">&nbsp;</div>
          <div class="table-cell table-col-header">
            <div class="col-icon col-icon-free">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
            </div>
            <span class="col-title">Gratuit</span>
            <span class="col-sub">Sans inscription</span>
          </div>
          <div class="table-cell table-col-header">
            <div class="col-icon col-icon-discovery">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
            </div>
            <span class="col-title">Découverte</span>
            <span class="col-sub">Compte gratuit</span>
          </div>
          <div class="table-cell table-col-header col-premium-header">
            <div class="col-premium-badge">Recommandé</div>
            <div class="col-icon col-icon-premium">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            </div>
            <span class="col-title">Abonnement</span>
            <span class="col-sub">Dès 4,99€/sem</span>
          </div>
        </div>

        <!-- Feature Rows -->
        <div class="table-row">
          <div class="table-cell table-feature-label">Cours en ligne</div>
          <div class="table-cell"><span class="cell-yes-basic">✓</span> Accès partiel</div>
          <div class="table-cell"><span class="cell-yes-basic">✓</span> 1 chapitre complet</div>
          <div class="table-cell cell-premium"><span class="cell-yes">✓</span> <strong>Tous les chapitres</strong></div>
        </div>
        <div class="table-row">
          <div class="table-cell table-feature-label">Fiches de synthèse</div>
          <div class="table-cell"><span class="cell-yes-basic">✓</span> Accès partiel</div>
          <div class="table-cell"><span class="cell-yes-basic">✓</span> 1 chapitre complet</div>
          <div class="table-cell cell-premium"><span class="cell-yes">✓</span> <strong>Toutes les fiches</strong></div>
        </div>
        <div class="table-row">
          <div class="table-cell table-feature-label">Exercices corrigés</div>
          <div class="table-cell"><span class="cell-yes-basic">✓</span> Accès partiel</div>
          <div class="table-cell"><span class="cell-yes-basic">✓</span> 1 chapitre complet</div>
          <div class="table-cell cell-premium"><span class="cell-yes">✓</span> <strong>Tous les exercices</strong></div>
        </div>
        <div class="table-row">
          <div class="table-cell table-feature-label">Suivi de progression</div>
          <div class="table-cell"><span class="cell-no">✕</span></div>
          <div class="table-cell"><span class="cell-no">✕</span></div>
          <div class="table-cell cell-premium"><span class="cell-yes">✓</span> <strong>Complet</strong></div>
        </div>
        <div class="table-row">
          <div class="table-cell table-feature-label">Révisions adaptées</div>
          <div class="table-cell"><span class="cell-no">✕</span></div>
          <div class="table-cell"><span class="cell-no">✕</span></div>
          <div class="table-cell cell-premium"><span class="cell-yes">✓</span> <strong>Oui</strong></div>
        </div>
        <div class="table-row">
          <div class="table-cell table-feature-label">Outils de calcul</div>
          <div class="table-cell"><span class="cell-yes-basic">✓</span> Basiques</div>
          <div class="table-cell"><span class="cell-yes-basic">✓</span> Basiques</div>
          <div class="table-cell cell-premium"><span class="cell-yes">✓</span> <strong>Avancés</strong></div>
        </div>

        <!-- CTA Row -->
        <div class="table-row table-cta-row">
          <div class="table-cell table-feature-label">&nbsp;</div>
          <div class="table-cell">
            <button class="table-btn btn-free" @click="$emit('explore-free')">Explorer</button>
          </div>
          <div class="table-cell">
            <button class="table-btn btn-discovery" @click="$emit('create-account')">Créer un compte</button>
          </div>
          <div class="table-cell cell-premium">
            <button class="table-btn btn-premium" @click="$emit('subscribe')">S'abonner →</button>
            <span class="btn-note">Sans engagement</span>
          </div>
        </div>
      </div>

      <!-- Mobile Cards (hidden on desktop, shown on mobile) -->
      <div class="mobile-cards">
        <!-- Premium first on mobile -->
        <div class="m-card m-card-premium">
          <div class="m-card-badge">Recommandé</div>
          <div class="m-card-header">
            <div class="m-card-icon m-icon-premium">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            </div>
            <div>
              <h3 class="m-card-title">Abonnement</h3>
              <p class="m-card-price">Dès <strong>4,99€</strong>/semaine</p>
            </div>
          </div>
          <ul class="m-card-list">
            <li><span class="m-check m-check-p">✓</span> <strong>Tous les chapitres</strong> de ton niveau</li>
            <li><span class="m-check m-check-p">✓</span> <strong>Toutes les fiches</strong> de synthèse</li>
            <li><span class="m-check m-check-p">✓</span> <strong>Tous les exercices</strong> guidés et corrigés</li>
            <li><span class="m-check m-check-p">✓</span> <strong>Suivi de progression</strong> complet</li>
            <li><span class="m-check m-check-p">✓</span> <strong>Révisions adaptées</strong> à ton niveau</li>
            <li><span class="m-check m-check-p">✓</span> <strong>Outils avancés</strong> de calcul</li>
          </ul>
          <button class="m-card-btn m-btn-premium" @click="$emit('subscribe')">S'abonner maintenant →</button>
          <p class="m-card-note">🔒 Paiement sécurisé • Sans engagement</p>
        </div>

        <div class="m-cards-secondary">
          <!-- Gratuit -->
          <div class="m-card m-card-light">
            <div class="m-card-header">
              <div class="m-card-icon m-icon-free">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
              </div>
              <div>
                <h3 class="m-card-title">Gratuit</h3>
                <p class="m-card-sub">Sans inscription</p>
              </div>
            </div>
            <ul class="m-card-list m-list-compact">
              <li><span class="m-check m-check-g">✓</span> Cours, fiches et exercices en accès partiel</li>
              <li><span class="m-check m-check-g">✓</span> Outils de calcul basiques</li>
            </ul>
            <button class="m-card-btn m-btn-light" @click="$emit('explore-free')">Explorer</button>
          </div>
          <!-- Découverte -->
          <div class="m-card m-card-light">
            <div class="m-card-header">
              <div class="m-card-icon m-icon-discovery">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
              </div>
              <div>
                <h3 class="m-card-title">Découverte</h3>
                <p class="m-card-sub">Compte gratuit</p>
              </div>
            </div>
            <ul class="m-card-list m-list-compact">
              <li><span class="m-check m-check-d">✓</span> 1 chapitre débloqué : cours, fiches et exercices</li>
              <li><span class="m-check m-check-d">✓</span> Outils de calcul basiques</li>
            </ul>
            <button class="m-card-btn m-btn-light" @click="$emit('create-account')">Créer un compte</button>
          </div>
        </div>
      </div>

      <!-- Transition CTA -->
      <div class="transition-cta">
        <p class="transition-text">
          💡 <strong>Découvre gratuitement</strong>, puis débloque tout avec l'abonnement.
          <br class="hide-mobile" />
          Pas de surprise : tu ne paies que si tu veux aller plus loin.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
defineEmits(['explore-free', 'create-account', 'subscribe'])
</script>

<style scoped lang="scss">
.why-subscribe-section {
  padding: 80px 0;
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 50%, #f8fafc 100%);
}

.why-subscribe-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 24px;
}

/* ── Header ── */
.why-subscribe-header {
  text-align: center;
  margin-bottom: 48px;
}

.why-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.08), rgba(37, 99, 235, 0.06));
  border: 1px solid rgba(99, 102, 241, 0.18);
  border-radius: 50px;
  padding: 8px 22px;
  margin-bottom: 18px;
  font-size: 0.9rem;
  font-weight: 600;
  color: #6366f1;

  .badge-icon {
    font-size: 1rem;
  }
}

.why-title {
  font-size: 2.25rem;
  font-weight: 900;
  color: #0f172a;
  margin-bottom: 14px;
  line-height: 1.25;
}

.why-highlight {
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.why-desc {
  font-size: 1.08rem;
  color: #475569;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
}

/* ── Comparison Table (Desktop) ── */
.comparison-table {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  overflow: hidden;
  margin-bottom: 40px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
}

.table-row {
  display: grid;
  grid-template-columns: 1.4fr 1fr 1fr 1.2fr;
  border-bottom: 1px solid #f1f5f9;

  &:last-child {
    border-bottom: none;
  }
}

.table-header-row {
  background: #f8fafc;
  border-bottom: 2px solid #e2e8f0;
}

.table-cta-row {
  background: #fafbff;
  border-top: 2px solid #e2e8f0;
  border-bottom: none;
}

.table-cell {
  padding: 14px 20px;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.9rem;
  color: #334155;
  border-right: 1px solid #f1f5f9;

  &:last-child {
    border-right: none;
  }
}

.table-feature-label {
  font-weight: 600;
  color: #0f172a;
  font-size: 0.88rem;
}

/* Column Headers */
.table-col-header {
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 4px;
  padding: 20px 12px;
  position: relative;
}

.col-premium-header {
  background: linear-gradient(180deg, #eef2ff 0%, #f8fafc 100%);
}

.col-premium-badge {
  position: absolute;
  top: -1px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  color: #fff;
  font-size: 0.68rem;
  font-weight: 700;
  padding: 3px 14px;
  border-radius: 0 0 10px 10px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.col-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 4px;
}

.col-icon-free {
  background: #f0fdf4;
  color: #16a34a;
}

.col-icon-discovery {
  background: #fef3c7;
  color: #d97706;
}

.col-icon-premium {
  background: #eef2ff;
  color: #4f46e5;
}

.col-title {
  font-size: 0.95rem;
  font-weight: 800;
  color: #0f172a;
}

.col-sub {
  font-size: 0.75rem;
  color: #64748b;
}

/* Cell Indicators */
.cell-yes {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #eef2ff;
  color: #4f46e5;
  font-size: 0.7rem;
  font-weight: 800;
  flex-shrink: 0;
}

.cell-yes-basic {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #f0fdf4;
  color: #16a34a;
  font-size: 0.7rem;
  font-weight: 800;
  flex-shrink: 0;
}

.cell-no {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #f1f5f9;
  color: #94a3b8;
  font-size: 0.7rem;
  font-weight: 700;
  flex-shrink: 0;
}

.cell-partial {
  font-size: 0.82rem;
  color: #64748b;
  font-style: italic;
}

.cell-premium {
  background: rgba(238, 242, 255, 0.4);
  font-weight: 500;
}

/* Table Buttons */
.table-btn {
  padding: 10px 20px;
  border-radius: 10px;
  font-size: 0.88rem;
  font-weight: 700;
  cursor: pointer;
  border: none;
  transition: all 0.2s ease;
  width: 100%;
  text-align: center;
}

.table-cta-row .table-cell {
  flex-direction: column;
  align-items: center;
  padding: 20px;
  gap: 6px;
}

.btn-free {
  background: #f0fdf4;
  color: #16a34a;
  border: 1px solid #bbf7d0;

  &:hover {
    background: #dcfce7;
  }
}

.btn-discovery {
  background: #fffbeb;
  color: #d97706;
  border: 1px solid #fde68a;

  &:hover {
    background: #fef3c7;
  }
}

.btn-premium {
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  color: #fff;
  box-shadow: 0 3px 12px rgba(42, 56, 183, 0.25);

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 5px 16px rgba(42, 56, 183, 0.35);
  }
}

.btn-note {
  font-size: 0.72rem;
  color: #64748b;
}

/* ── Mobile Cards ── */
.mobile-cards {
  display: none;
  margin-bottom: 32px;
}

.m-card {
  border-radius: 16px;
  padding: 24px 20px;
  position: relative;
}

.m-card-premium {
  background: linear-gradient(180deg, #fafaff 0%, #fff 100%);
  border: 2px solid #2563eb;
  box-shadow: 0 6px 24px rgba(37, 99, 235, 0.1);
  margin-bottom: 14px;
}

.m-card-badge {
  position: absolute;
  top: -11px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  color: #fff;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 4px 16px;
  border-radius: 50px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  white-space: nowrap;
}

.m-card-light {
  background: #ffffff;
  border: 1px solid #e2e8f0;
}

.m-cards-secondary {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.m-card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.m-card-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.m-icon-premium {
  background: #eef2ff;
  color: #4f46e5;
}

.m-icon-free {
  background: #f0fdf4;
  color: #16a34a;
}

.m-icon-discovery {
  background: #fef3c7;
  color: #d97706;
}

.m-card-title {
  font-size: 1.1rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
}

.m-card-price {
  font-size: 0.85rem;
  color: #475569;
  margin: 2px 0 0;
}

.m-card-sub {
  font-size: 0.78rem;
  color: #64748b;
  margin: 1px 0 0;
}

.m-card-list {
  list-style: none;
  padding: 0;
  margin: 0 0 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;

  li {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    font-size: 0.88rem;
    color: #334155;
    line-height: 1.35;
  }
}

.m-list-compact {
  gap: 7px;

  li {
    font-size: 0.82rem;
  }
}

.m-check {
  flex-shrink: 0;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.65rem;
  font-weight: 800;
  margin-top: 1px;
}

.m-check-p {
  background: #eef2ff;
  color: #4f46e5;
}

.m-check-g {
  background: #dcfce7;
  color: #16a34a;
}

.m-check-d {
  background: #fef3c7;
  color: #d97706;
}

.m-card-btn {
  width: 100%;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  border: none;
  transition: all 0.2s ease;
  text-align: center;
}

.m-btn-premium {
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  color: #fff;
  box-shadow: 0 3px 12px rgba(42, 56, 183, 0.25);
  padding: 14px 16px;
  font-size: 0.95rem;
}

.m-btn-light {
  background: #f8fafc;
  color: #334155;
  border: 1px solid #e2e8f0;
  font-size: 0.82rem;
  padding: 10px 12px;

  &:hover {
    background: #f1f5f9;
  }
}

.m-card-note {
  text-align: center;
  font-size: 0.75rem;
  color: #64748b;
  margin: 10px 0 0;
}

/* ── Transition CTA ── */
.transition-cta {
  max-width: 650px;
  margin: 0 auto;
  text-align: center;
  background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
  border: 1px solid #e0e7ff;
  border-radius: 14px;
  padding: 20px 28px;
}

.transition-text {
  font-size: 1rem;
  color: #334155;
  line-height: 1.6;
  margin: 0;
}

/* ── Responsive ── */
@media (max-width: 900px) {
  .comparison-table {
    display: none;
  }

  .mobile-cards {
    display: block;
  }
}

@media (max-width: 768px) {
  .why-subscribe-section {
    padding: 56px 0;
  }

  .why-subscribe-container {
    padding: 0 16px;
  }

  .why-title {
    font-size: 1.6rem;
  }

  .why-desc {
    font-size: 0.95rem;
  }

  .why-subscribe-header {
    margin-bottom: 32px;
  }

  .transition-cta {
    padding: 18px 20px;
    border-radius: 12px;
  }

  .transition-text {
    font-size: 0.9rem;
  }

  .hide-mobile {
    display: none;
  }
}

@media (max-width: 480px) {
  .why-subscribe-section {
    padding: 40px 0;
  }

  .why-subscribe-container {
    padding: 0 12px;
  }

  .why-title {
    font-size: 1.35rem;
    line-height: 1.3;
  }

  .why-badge {
    padding: 6px 14px;
    font-size: 0.8rem;
    margin-bottom: 12px;
  }

  .why-desc {
    font-size: 0.88rem;
  }

  .why-subscribe-header {
    margin-bottom: 24px;
  }

  .m-cards-secondary {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .m-card-premium {
    padding: 22px 18px;
  }

  .m-card-light {
    padding: 18px 16px;
  }

  .m-card-title {
    font-size: 1rem;
  }

  .m-card-list li {
    font-size: 0.84rem;
  }

  .m-list-compact li {
    font-size: 0.8rem;
  }

  .transition-cta {
    padding: 16px 14px;
  }

  .transition-text {
    font-size: 0.85rem;
    line-height: 1.5;
  }
}

@media (max-width: 360px) {
  .why-title {
    font-size: 1.2rem;
  }

  .m-card-premium {
    padding: 18px 14px;
  }

  .m-card-light {
    padding: 14px 12px;
  }
}
</style>
