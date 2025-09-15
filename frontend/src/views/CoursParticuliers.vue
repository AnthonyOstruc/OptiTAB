<template>
  <MainLayout>
    <div class="cours-particuliers-page">
      <!-- Hero Section -->
      <div class="hero-section">
        <div class="hero-content">
          <div class="hero-badge">
            <img src="/icons/AuteursExperts.svg" alt="Cours Particuliers" class="badge-icon" />
            <span class="badge-text">Cours Personnalisés</span>
          </div>
          <h1 class="hero-title">
            Cours particuliers
            <span class="gradient-text">sur mesure</span>
          </h1>
          <p class="hero-subtitle">
            Bénéficiez d'un accompagnement personnalisé avec nos professeurs expérimentés.
            Un suivi adapté à votre rythme et à vos besoins spécifiques pour maximiser vos résultats.
          </p>
          <div class="hero-features">
            <div class="feature-item">
              <span class="feature-icon">👨‍🏫</span>
              <span class="feature-text">Professeurs experts</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">📅</span>
              <span class="feature-text">Horaires flexibles</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">🎯</span>
              <span class="feature-text">Objectifs personnalisés</span>
            </div>
          </div>
        </div>
        <div class="hero-visual">
          <div class="floating-card card-1">
            <div class="card-icon-bg">
              <img src="/icons/AuteursExperts.svg" alt="Professeur" class="card-icon" />
            </div>
            <div class="card-content">
              <span class="card-title">Professeur dédié</span>
              <span class="card-desc">Suivi personnalisé</span>
            </div>
          </div>
          <div class="floating-card card-2">
            <div class="card-icon-bg">
              <img src="/icons/ApprentissageFlexible.svg" alt="Planning" class="card-icon" />
            </div>
            <div class="card-content">
              <span class="card-title">Planning adapté</span>
              <span class="card-desc">À votre rythme</span>
            </div>
          </div>
          <div class="floating-card card-3">
            <div class="card-icon-bg">
              <img src="/icons/SuiviProgression.svg" alt="Objectifs" class="card-icon" />
            </div>
            <div class="card-content">
              <span class="card-title">Objectifs clairs</span>
              <span class="card-desc">Progrès mesurés</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Avantages Section -->
      <div class="avantages-section">
        <div class="container">
          <div class="section-intro">
            <h2 class="section-title">Pourquoi choisir nos cours particuliers ?</h2>
            <p class="section-subtitle">
              Une méthode pédagogique éprouvée qui s'adapte à chaque élève
            </p>
          </div>
          <div class="avantages-grid">
            <div class="avantage-card">
              <div class="avantage-icon">
                <img src="/icons/AuteursExperts.svg" alt="Personnalisé" class="icon" />
              </div>
              <h3>Cours sur mesure</h3>
              <p>Programme adapté à votre niveau et à vos objectifs spécifiques</p>
            </div>
            <div class="avantage-card">
              <div class="avantage-icon">
                <img src="/icons/ApprentissageFlexible.svg" alt="Flexible" class="icon" />
              </div>
              <h3>Horaires flexibles</h3>
              <p>Choisissez les jours et horaires qui vous conviennent le mieux</p>
            </div>
            <div class="avantage-card">
              <div class="avantage-icon">
                <img src="/icons/SuiviProgression.svg" alt="Progression" class="icon" />
              </div>
              <h3>Suivi régulier</h3>
              <p>Bilans réguliers pour mesurer vos progrès et ajuster le programme</p>
            </div>
            <div class="avantage-card">
              <div class="avantage-icon">
                <img src="/icons/mail.svg" alt="Communication" class="icon" />
              </div>
              <h3>Communication directe</h3>
              <p>Contact direct avec votre professeur pour un suivi optimal</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Tarifs Section -->
      <div class="tarifs-section">
        <div class="container">
          <h2 class="section-title">Nos formules de cours particuliers</h2>
          <div class="tarifs-grid">
            <div class="tarif-card">
              <div class="tarif-header">
                <h3>Formule Essentiel</h3>
                <div class="tarif-price">
                  <span class="price">25€</span>
                  <span class="period">/heure</span>
                </div>
              </div>
              <div class="tarif-features">
                <div class="feature">✓ 1 heure de cours par semaine</div>
                <div class="feature">✓ Suivi des progrès</div>
                <div class="feature">✓ Exercices personnalisés</div>
                <div class="feature">✓ Support par email</div>
              </div>
              <button class="tarif-button">Choisir cette formule</button>
            </div>
            <div class="tarif-card featured">
              <div class="tarif-header">
                <h3>Formule Intensif</h3>
                <div class="tarif-price">
                  <span class="price">40€</span>
                  <span class="period">/heure</span>
                </div>
                <div class="popular-badge">Le plus populaire</div>
              </div>
              <div class="tarif-features">
                <div class="feature">✓ 2 heures de cours par semaine</div>
                <div class="feature">✓ Suivi intensif</div>
                <div class="feature">✓ Exercices avancés</div>
                <div class="feature">✓ Support téléphonique</div>
                <div class="feature">✓ Bilans mensuels</div>
              </div>
              <button class="tarif-button primary">Choisir cette formule</button>
            </div>
            <div class="tarif-card">
              <div class="tarif-header">
                <h3>Formule Premium</h3>
                <div class="tarif-price">
                  <span class="price">60€</span>
                  <span class="period">/heure</span>
                </div>
              </div>
              <div class="tarif-features">
                <div class="feature">✓ Cours à la demande</div>
                <div class="feature">✓ Suivi personnalisé complet</div>
                <div class="feature">✓ Préparation aux examens</div>
                <div class="feature">✓ Support prioritaire</div>
                <div class="feature">✓ Bilans hebdomadaires</div>
              </div>
              <button class="tarif-button">Choisir cette formule</button>
            </div>
          </div>
        </div>
      </div>

      <!-- CTA Section -->
      <div class="cta-section">
        <div class="cta-card">
          <div class="cta-content">
            <h3 class="cta-title">Prêt à booster vos résultats ?</h3>
            <p class="cta-text">
              Réservez votre premier cours gratuit et découvrez notre méthode d'enseignement personnalisé.
              Ensemble, nous atteindrons vos objectifs !
            </p>
            <div class="cta-buttons">
              <router-link to="/contact" class="cta-button primary">
                <img src="/icons/ApprentissageFlexible.svg" alt="Calendrier" class="button-icon" />
                Réserver un cours gratuit
              </router-link>
              <a href="mailto:contact@optitab.com" class="cta-button secondary">
                <img src="/icons/mail.svg" alt="Contact" class="button-icon" />
                Nous contacter
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import MainLayout from '@/components/layout/MainLayout.vue'
</script>

<style scoped>
/* Page Container */
.cours-particuliers-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

/* Hero Section */
.hero-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 4rem 2rem;
  position: relative;
  overflow: hidden;
}

.hero-content {
  flex: 1;
  max-width: 600px;
  z-index: 2;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #4e63c2 0%, #6b46c1 100%);
  color: #fff;
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 2rem;
  box-shadow: 0 4px 15px rgba(78, 99, 194, 0.3);
}

.badge-icon {
  width: 1.5rem;
  height: 1.5rem;
  filter: brightness(0) invert(1);
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  color: #1f2937;
  line-height: 1.1;
  margin-bottom: 1.5rem;
}

.gradient-text {
  background: linear-gradient(135deg, #4e63c2 0%, #6b46c1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 2.5rem;
}

/* Hero Features */
.hero-features {
  display: flex;
  gap: 2rem;
  margin-top: 2rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.feature-icon {
  font-size: 1.5rem;
}

.feature-text {
  font-size: 0.9rem;
  color: #6b7280;
  font-weight: 500;
}

/* Hero Visual */
.hero-visual {
  flex: 1;
  position: relative;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.floating-card {
  position: absolute;
  background: #fff;
  padding: 1.5rem;
  border-radius: 20px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  animation: float 6s ease-in-out infinite;
  min-width: 200px;
}

.floating-card:nth-child(1) {
  top: 15%;
  left: 5%;
  animation-delay: 0s;
}

.floating-card:nth-child(2) {
  top: 45%;
  right: 10%;
  animation-delay: 2s;
}

.floating-card:nth-child(3) {
  bottom: 15%;
  left: 15%;
  animation-delay: 4s;
}

.card-icon-bg {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #4e63c2 0%, #6b46c1 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-icon {
  width: 1.5rem;
  height: 1.5rem;
  filter: brightness(0) invert(1);
}

.card-content {
  display: flex;
  flex-direction: column;
}

.card-title {
  font-weight: 700;
  color: #1f2937;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.card-desc {
  font-size: 0.85rem;
  color: #6b7280;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

/* Avantages Section */
.avantages-section {
  background: #fff;
  padding: 4rem 0;
  margin: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section-intro {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1rem;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #6b7280;
  max-width: 600px;
  margin: 0 auto;
}

.avantages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.avantage-card {
  background: #f8fafc;
  padding: 2rem;
  border-radius: 16px;
  text-align: center;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.avantage-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  background: #fff;
}

.avantage-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #4e63c2 0%, #6b46c1 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  box-shadow: 0 8px 25px rgba(78, 99, 194, 0.3);
}

.avantage-icon .icon {
  width: 2rem;
  height: 2rem;
  filter: brightness(0) invert(1);
}

.avantage-card h3 {
  font-size: 1.3rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1rem;
}

.avantage-card p {
  color: #6b7280;
  line-height: 1.6;
}

/* Tarifs Section */
.tarifs-section {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  padding: 4rem 0;
}

.tarifs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.tarif-card {
  background: #fff;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  position: relative;
  transition: all 0.3s ease;
}

.tarif-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.tarif-card.featured {
  border: 2px solid #4e63c2;
  transform: scale(1.05);
}

.tarif-header {
  text-align: center;
  margin-bottom: 2rem;
}

.tarif-header h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1rem;
}

.tarif-price {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 0.25rem;
  margin-bottom: 1rem;
}

.price {
  font-size: 2.5rem;
  font-weight: 800;
  color: #4e63c2;
}

.period {
  font-size: 1rem;
  color: #6b7280;
  font-weight: 500;
}

.popular-badge {
  background: #4e63c2;
  color: #fff;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
}

.tarif-features {
  margin-bottom: 2rem;
}

.feature {
  display: block;
  margin-bottom: 0.75rem;
  color: #6b7280;
  font-weight: 500;
}

.tarif-button {
  width: 100%;
  padding: 1rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  border: 2px solid #4e63c2;
  background: transparent;
  color: #4e63c2;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tarif-button.primary {
  background: #4e63c2;
  color: #fff;
}

.tarif-button.primary:hover {
  background: #3b4ac2;
  transform: translateY(-2px);
}

.tarif-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(78, 99, 194, 0.3);
}

/* CTA Section */
.cta-section {
  background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
  padding: 4rem 2rem;
  margin-top: 2rem;
}

.cta-card {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 1rem;
}

.cta-text {
  font-size: 1.2rem;
  color: #d1d5db;
  line-height: 1.6;
  margin-bottom: 2.5rem;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.cta-button.primary {
  background: linear-gradient(135deg, #4e63c2 0%, #6b46c1 100%);
  color: #fff;
  box-shadow: 0 4px 15px rgba(78, 99, 194, 0.4);
}

.cta-button.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(78, 99, 194, 0.6);
}

.cta-button.secondary {
  background: transparent;
  color: #fff;
  border-color: #fff;
}

.cta-button.secondary:hover {
  background: #fff;
  color: #1f2937;
  transform: translateY(-2px);
}

.button-icon {
  width: 1.2rem;
  height: 1.2rem;
  filter: brightness(0) invert(1);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .hero-section {
    flex-direction: column;
    text-align: center;
    padding: 3rem 1.5rem;
  }

  .hero-title {
    font-size: 2.8rem;
  }

  .hero-visual {
    height: 300px;
    margin-top: 2rem;
  }

  .hero-features {
    justify-content: center;
  }

  .avantages-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.2rem;
  }

  .hero-subtitle {
    font-size: 1.1rem;
  }

  .hero-features {
    flex-direction: column;
    gap: 1rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .cta-title {
    font-size: 2rem;
  }

  .cta-buttons {
    flex-direction: column;
    align-items: center;
  }

  .cta-button {
    width: 100%;
    max-width: 300px;
    justify-content: center;
  }

  .tarifs-grid {
    grid-template-columns: 1fr;
  }

  .tarif-card.featured {
    transform: none;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 1.8rem;
  }

  .hero-badge {
    font-size: 0.8rem;
    padding: 0.4rem 0.8rem;
  }

  .avantage-card,
  .tarif-card {
    padding: 1.5rem;
  }

  .section-title {
    font-size: 1.6rem;
  }

  .cta-title {
    font-size: 1.8rem;
  }

  .floating-card {
    min-width: 150px;
    padding: 0.75rem;
  }

  .card-title {
    font-size: 0.9rem;
  }

  .card-desc {
    font-size: 0.8rem;
  }
}
</style>
