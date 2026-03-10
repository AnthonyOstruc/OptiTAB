<template>
  <section class="unlock-benefits-section">
    <div class="unlock-container">
      <div class="unlock-content">
        <!-- Left: Benefits -->
        <div class="unlock-left">
          <div class="unlock-badge">
            <span class="badge-icon">🚀</span>
            <span class="badge-text">L'abonnement OptiTAB</span>
          </div>
          <h2 class="unlock-title">
            Avec l'abonnement, tu <span class="unlock-highlight">débloques</span> :
          </h2>
          <div class="benefits-grid">
            <div class="benefit-item">
              <div class="benefit-icon-wrapper">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                  <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                </svg>
              </div>
              <div>
                <strong class="benefit-name">Tous les chapitres</strong>
                <p class="benefit-desc">Cours complets pour chaque notion de ton programme</p>
              </div>
            </div>
            <div class="benefit-item">
              <div class="benefit-icon-wrapper">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                </svg>
              </div>
              <div>
                <strong class="benefit-name">Toutes les fiches de synthèse</strong>
                <p class="benefit-desc">L'essentiel de chaque chapitre condensé pour réviser efficacement</p>
              </div>
            </div>
            <div class="benefit-item">
              <div class="benefit-icon-wrapper">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="9 11 12 14 22 4"/>
                  <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
                </svg>
              </div>
              <div>
                <strong class="benefit-name">Tous les exercices guidés</strong>
                <p class="benefit-desc">Corrections détaillées pas à pas pour comprendre chaque étape</p>
              </div>
            </div>
            <div class="benefit-item">
              <div class="benefit-icon-wrapper">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="20" x2="18" y2="10"/>
                  <line x1="12" y1="20" x2="12" y2="4"/>
                  <line x1="6" y1="20" x2="6" y2="14"/>
                </svg>
              </div>
              <div>
                <strong class="benefit-name">Des révisions adaptées à ton niveau</strong>
                <p class="benefit-desc">Suivi de progression et contenus ciblés selon tes besoins</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Right: CTA Card -->
        <div class="unlock-right">
          <div class="unlock-cta-card">
            <div class="cta-card-header">
              <p class="cta-price-from">À partir de</p>
              <div class="cta-price">
                <span class="cta-price-amount">4,99€</span>
                <span class="cta-price-period">/semaine</span>
              </div>
              <p class="cta-price-or">ou <strong>7,99€/mois</strong> (le plus populaire)</p>
            </div>
            <ul class="cta-reassurance">
              <li>✅ Accès immédiat après paiement</li>
              <li>✅ Sans engagement, annulable à tout moment</li>
              <li>✅ Paiement 100% sécurisé</li>
            </ul>
            <button class="cta-subscribe-btn" @click="$emit('subscribe')">
              S'abonner et débloquer tout →
            </button>
            <button class="cta-pricing-btn" @click="$emit('see-pricing')">
              Voir tous les tarifs
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineEmits(['subscribe', 'see-pricing'])
</script>

<style scoped lang="scss">
.unlock-benefits-section {
  padding: 80px 0;
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
}

.unlock-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2vw;
}

.unlock-content {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 48px;
  align-items: center;
}

// Left: Benefits
.unlock-left {
  min-width: 0;
}

.unlock-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(37, 99, 235, 0.08));
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 50px;
  padding: 10px 24px;
  margin-bottom: 20px;
  font-size: 0.95rem;
  font-weight: 600;
  color: #6366f1;

  .badge-icon {
    font-size: 1.1rem;
  }
}

.unlock-title {
  font-size: 2.25rem;
  font-weight: 900;
  color: #0f172a;
  margin-bottom: 32px;
  line-height: 1.25;
}

.unlock-highlight {
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

// Benefits Grid
.benefits-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.benefit-item {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.benefit-icon-wrapper {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  background: #eef2ff;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4f46e5;
}

.benefit-name {
  font-size: 1.05rem;
  color: #0f172a;
  display: block;
  margin-bottom: 2px;
}

.benefit-desc {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0;
  line-height: 1.4;
}

// Right: CTA Card
.unlock-cta-card {
  background: #ffffff;
  border: 2px solid #e0e7ff;
  border-radius: 24px;
  padding: 36px 28px;
  text-align: center;
  box-shadow: 0 8px 32px rgba(37, 99, 235, 0.08);
}

.cta-card-header {
  margin-bottom: 24px;
}

.cta-price-from {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0 0 4px;
}

.cta-price {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 4px;
}

.cta-price-amount {
  font-size: 3rem;
  font-weight: 900;
  color: #0f172a;
}

.cta-price-period {
  font-size: 1.1rem;
  color: #64748b;
  font-weight: 500;
}

.cta-price-or {
  font-size: 0.95rem;
  color: #475569;
  margin: 8px 0 0;
}

// Reassurance
.cta-reassurance {
  list-style: none;
  padding: 0;
  margin: 0 0 24px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  text-align: left;

  li {
    font-size: 0.9rem;
    color: #334155;
    line-height: 1.4;
  }
}

// Buttons
.cta-subscribe-btn {
  width: 100%;
  padding: 16px 24px;
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  color: #ffffff;
  font-size: 1.05rem;
  font-weight: 700;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 14px rgba(42, 56, 183, 0.3);
  margin-bottom: 12px;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(42, 56, 183, 0.4);
  }
}

.cta-pricing-btn {
  width: 100%;
  padding: 12px 24px;
  background: transparent;
  color: #4f46e5;
  font-size: 0.95rem;
  font-weight: 600;
  border: 1px solid #c7d2fe;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: #eef2ff;
  }
}

// Responsive
@media (max-width: 1024px) {
  .unlock-content {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .unlock-cta-card {
    max-width: 500px;
    margin: 0 auto;
  }
}

@media (max-width: 768px) {
  .unlock-benefits-section {
    padding: 56px 0;
  }

  .unlock-container {
    padding: 0 16px;
  }

  .unlock-title {
    font-size: 1.6rem;
    margin-bottom: 24px;
  }

  .unlock-badge {
    padding: 8px 20px;
    font-size: 0.88rem;
    margin-bottom: 16px;
  }

  .benefits-grid {
    gap: 16px;
  }

  .benefit-item {
    gap: 12px;
  }

  .benefit-icon-wrapper {
    width: 40px;
    height: 40px;
    border-radius: 10px;

    svg {
      width: 20px;
      height: 20px;
    }
  }

  .benefit-name {
    font-size: 0.95rem;
  }

  .benefit-desc {
    font-size: 0.85rem;
  }

  .unlock-cta-card {
    max-width: 100%;
    padding: 28px 22px;
    border-radius: 18px;
  }

  .cta-price-amount {
    font-size: 2.5rem;
  }

  .cta-price-period {
    font-size: 1rem;
  }

  .cta-price-or {
    font-size: 0.88rem;
  }

  .cta-reassurance {
    gap: 8px;
    margin-bottom: 20px;

    li {
      font-size: 0.85rem;
    }
  }

  .cta-subscribe-btn {
    padding: 14px 20px;
    font-size: 1rem;
    border-radius: 12px;
  }

  .cta-pricing-btn {
    padding: 11px 20px;
    font-size: 0.9rem;
    border-radius: 10px;
  }
}

@media (max-width: 480px) {
  .unlock-benefits-section {
    padding: 40px 0;
  }

  .unlock-container {
    padding: 0 12px;
  }

  .unlock-title {
    font-size: 1.35rem;
    margin-bottom: 20px;
  }

  .unlock-badge {
    padding: 7px 16px;
    font-size: 0.8rem;
  }

  .benefits-grid {
    gap: 14px;
  }

  .benefit-icon-wrapper {
    width: 36px;
    height: 36px;
    border-radius: 8px;

    svg {
      width: 18px;
      height: 18px;
    }
  }

  .benefit-name {
    font-size: 0.9rem;
  }

  .benefit-desc {
    font-size: 0.82rem;
  }

  .unlock-cta-card {
    padding: 24px 18px;
    border-radius: 14px;
  }

  .cta-price-from {
    font-size: 0.82rem;
  }

  .cta-price-amount {
    font-size: 2.2rem;
  }

  .cta-reassurance li {
    font-size: 0.82rem;
  }

  .cta-subscribe-btn {
    padding: 13px 16px;
    font-size: 0.95rem;
  }

  .cta-pricing-btn {
    padding: 10px 16px;
    font-size: 0.85rem;
  }
}

@media (max-width: 360px) {
  .unlock-title {
    font-size: 1.2rem;
  }

  .benefit-item {
    gap: 10px;
  }

  .unlock-cta-card {
    padding: 20px 14px;
  }

  .cta-price-amount {
    font-size: 2rem;
  }
}
</style>
