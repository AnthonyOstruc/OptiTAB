<template>
  <MainLayout>
    <div class="confidentialite-page">
      <div class="container">
        <h1>Politique de confidentialité</h1>
        
        <section class="content-section">
          <h2>1. Collecte des informations</h2>
          <p>Nous collectons les informations que vous nous fournissez directement, notamment :</p>
          <ul>
            <li>Informations d'identification (nom, prénom, email)</li>
            <li>Informations de compte (nom d'utilisateur, mot de passe)</li>
            <li>Données de progression et d'utilisation de la plateforme</li>
            <li>Communications avec notre équipe de support</li>
          </ul>
        </section>

        <section class="content-section">
          <h2>2. Utilisation des informations</h2>
          <p>Nous utilisons vos informations pour :</p>
          <ul>
            <li>Fournir et améliorer nos services éducatifs</li>
            <li>Personnaliser votre expérience d'apprentissage</li>
            <li>Communiquer avec vous concernant votre compte</li>
            <li>Assurer la sécurité de notre plateforme</li>
            <li>Respecter nos obligations légales</li>
          </ul>
        </section>

        <section class="content-section">
          <h2>3. Partage des informations</h2>
          <p>Nous ne vendons, n'échangeons ni ne louons vos informations personnelles à des tiers. Nous pouvons partager vos informations uniquement dans les cas suivants :</p>
          <ul>
            <li>Avec votre consentement explicite</li>
            <li>Pour respecter une obligation légale</li>
            <li>Pour protéger nos droits et notre sécurité</li>
            <li>Avec nos prestataires de services de confiance (hébergement, support)</li>
          </ul>
        </section>

        <section class="content-section">
          <h2>4. Sécurité des données</h2>
          <p>Nous mettons en œuvre des mesures de sécurité appropriées pour protéger vos informations personnelles contre l'accès non autorisé, la modification, la divulgation ou la destruction.</p>
        </section>

        <section class="content-section">
          <h2>5. Vos droits</h2>
          <p>Vous avez le droit de :</p>
          <ul>
            <li>Accéder à vos informations personnelles</li>
            <li>Corriger vos informations inexactes</li>
            <li>Demander la suppression de vos données</li>
            <li>Vous opposer au traitement de vos données</li>
            <li>Demander la portabilité de vos données</li>
          </ul>
        </section>

        <section class="content-section">
          <h2>6. Cookies et technologies similaires</h2>
          <p>Nous utilisons des cookies et des technologies similaires pour améliorer votre expérience, analyser l'utilisation de notre site et personnaliser le contenu.</p>
        </section>

        <section class="content-section">
          <h2>7. Modifications de cette politique</h2>
          <p>Nous pouvons mettre à jour cette politique de confidentialité de temps à autre. Nous vous informerons de tout changement important en publiant la nouvelle politique sur cette page.</p>
        </section>

        <section class="content-section">
          <h2>8. Contact</h2>
          <p>Si vous avez des questions concernant cette politique de confidentialité, contactez-nous à :</p>
          <p><strong>Email :</strong> support@optitab.com</p>
          <p><strong>Téléphone :</strong> 07 64 04 02 51</p>
        </section>

        <div class="last-updated">
          <p><em>Dernière mise à jour : {{ new Date().toLocaleDateString('fr-FR') }}</em></p>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import MainLayout from '@/components/layout/MainLayout.vue'
</script>

<style scoped>
.confidentialite-page {
  padding: 2rem 0;
  min-height: 100vh;
  background: #f8fafc;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

h1 {
  color: #1f2937;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 2rem;
  text-align: center;
  border-bottom: 3px solid #2563eb;
  padding-bottom: 1rem;
}

.content-section {
  margin-bottom: 2rem;
}

h2 {
  color: #2563eb;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  border-left: 4px solid #2563eb;
  padding-left: 1rem;
}

p {
  color: #374151;
  line-height: 1.6;
  margin-bottom: 1rem;
  font-size: 1rem;
}

ul {
  margin-left: 1.5rem;
  margin-bottom: 1rem;
}

li {
  color: #374151;
  line-height: 1.6;
  margin-bottom: 0.5rem;
}

.last-updated {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
  text-align: center;
}

.last-updated p {
  color: #6b7280;
  font-style: italic;
  margin: 0;
}

@media (max-width: 768px) {
  .container {
    padding: 1.5rem;
    margin: 0 0.5rem;
  }
  
  h1 {
    font-size: 2rem;
  }
  
  h2 {
    font-size: 1.3rem;
  }
}
</style> 