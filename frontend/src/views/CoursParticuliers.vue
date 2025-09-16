<template>
  <MainLayout>
    <div class="cours-particuliers-page">
      <!-- Hero Section -->
      <div class="hero-section">
        <div class="hero-content">
          <h1 class="hero-title">
            Cours particuliers
            <span class="gradient-text">professionnels</span>
          </h1>
          <p class="hero-subtitle">
            Enseignement individuel dispensé par des professeurs qualifiés.
            Méthodes pédagogiques structurées et évaluation continue des acquis.
          </p>
          <div class="hero-stats">
            <div class="stat-item">
              <span class="stat-number">95%</span>
              <span class="stat-label">Taux de réussite</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">15+</span>
              <span class="stat-label">Années d'expérience</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">1:1</span>
              <span class="stat-label">Ratio professeur/élève</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Avantages Section -->
      <div class="avantages-section">
        <div class="container">
          <div class="section-intro">
            <h2 class="section-title">Méthodologie d'enseignement</h2>
            <p class="section-subtitle">
              Approche structurée basée sur l'évaluation des compétences et l'adaptation des contenus
            </p>
          </div>
          <div class="avantages-grid">
            <div class="avantage-card">
              <div class="avantage-icon">
                <img src="/icons/exercicesGuides.svg" alt="Adaptation" class="icon" />
              </div>
              <h3>Adaptation Pédagogique</h3>
              <p>Identification du profil d'apprentissage et ajustement des méthodes d'enseignement en fonction des besoins spécifiques de l'élève.</p>
            </div>
            <div class="avantage-card">
              <div class="avantage-icon">
                <img src="/icons/AuteursExperts.svg" alt="Experts" class="icon" />
              </div>
              <h3>Qualification Professionnelle</h3>
              <p>Enseignants diplômés et spécialisés dans leur discipline. Formation continue en pédagogie et expérience en enseignement individuel.</p>
            </div>
            <div class="avantage-card">
              <div class="avantage-icon">
                <img src="/icons/SuiviProgression.svg" alt="Suivi" class="icon" />
              </div>
              <h3>Suivi des Acquis</h3>
              <p>Évaluations régulières et tests de positionnement pour identifier les compétences acquises et les axes d'amélioration.</p>
            </div>
            <div class="avantage-card">
              <div class="avantage-icon">
                <img src="/icons/ApprentissageFlexible.svg" alt="Flexibilité" class="icon" />
              </div>
              <h3>Organisation Flexible</h3>
              <p>Horaires adaptables et durée des séances modulable selon les contraintes et objectifs pédagogiques définis.</p>
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
                <div class="feature">✓ 1 heure de cours individuel par semaine</div>
                <div class="feature">✓ Évaluation initiale des compétences</div>
                <div class="feature">✓ Exercices adaptés au niveau</div>
                <div class="feature">✓ Rapport de progression mensuel</div>
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
                <div class="feature">✓ 2 heures de cours individuel par semaine</div>
                <div class="feature">✓ Méthodologie adaptée au profil</div>
                <div class="feature">✓ Travail ciblé sur les difficultés</div>
                <div class="feature">✓ Communication régulière avec les parents</div>
                <div class="feature">✓ Évaluations intermédiaires</div>
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
                <div class="feature">✓ Cours individuels à la demande</div>
                <div class="feature">✓ Plan de formation personnalisé</div>
                <div class="feature">✓ Préparation aux examens</div>
                <div class="feature">✓ Suivi pédagogique renforcé</div>
                <div class="feature">✓ Rapports de progression hebdomadaires</div>
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
            <h3 class="cta-title">Consultation pédagogique</h3>
            <p class="cta-text">
              Entretien d'évaluation gratuit pour définir les objectifs d'apprentissage.
              Élaboration d'un plan de formation adapté aux besoins identifiés.
            </p>
            <div class="cta-buttons">
              <router-link to="/contact" class="cta-button primary">
                Demander un entretien
              </router-link>
              <a href="mailto:contact@optitab.com" class="cta-button secondary">
                Contacter nos services
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Bouton WhatsApp flottant -->
    <WhatsappChatButton
      phone="33764040251"
      message="Bonjour, j'ai une question sur les cours particuliers OptiTAB !"
      tooltip="Une question ? Discutons sur WhatsApp !"
    />
  </MainLayout>
</template>

<script setup>
import MainLayout from '@/components/layout/MainLayout.vue'
import WhatsappChatButton from '@/components/home/WhatsappChatButton.vue'
</script>

<style scoped>
/* Page Container */
.cours-particuliers-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

/* Hero Section */
.hero-section {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
  padding: 4rem 2rem;
  margin-top: 20px;
}

.hero-content {
  width: 100%;
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
  font-size: 2.5rem;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.3;
  margin-bottom: 1.5rem;
}

.gradient-text {
  background: linear-gradient(135deg, #4e63c2 0%, #6b46c1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 3rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

/* Hero Stats */
.hero-stats {
  display: flex;
  gap: 3rem;
  justify-content: center;
  margin-top: 2rem;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 2.2rem;
  font-weight: 700;
  color: #6366f1;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.95rem;
  color: #6b7280;
  font-weight: 500;
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
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.avantage-card {
  background: #ffffff;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.avantage-icon {
  width: 80px;
  height: 80px;
  background: transparent;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
}

.avantage-icon .icon {
  width: 7.5rem;
  height: 7.5rem;
  filter: none;
  color: #6366f1;
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
  background: #ffffff;
  padding: 3rem 2rem;
  margin-top: 0;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.cta-card {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.cta-title {
  font-size: 2rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.cta-text {
  font-size: 1.1rem;
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 2rem;
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
  color: #6366f1;
  border-color: #6366f1;
}

.cta-button.secondary:hover {
  background: #6366f1;
  color: #fff;
  transform: none;
}

.button-icon {
  width: 1.2rem;
  height: 1.2rem;
  filter: none;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .hero-section {
    padding: 3rem 1.5rem;
  }

  .hero-title {
    font-size: 2.2rem;
  }

  .hero-stats {
    gap: 2rem;
  }

  .avantages-grid {
    grid-template-columns: repeat(2, 1fr);
    max-width: 600px;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1.1rem;
  }

  .hero-stats {
    flex-direction: column;
    gap: 1.5rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .avantages-grid {
    grid-template-columns: 1fr;
    max-width: 400px;
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
}
</style>
