<template>
  <MainLayout>
    <div class="conditions-page">
      <div class="container">
        <h1>Conditions d'utilisation</h1>
        
        <section class="content-section">
          <h2>1. Acceptation des conditions</h2>
          <p>En utilisant la plateforme OptiTAB, vous acceptez d'être lié par ces conditions d'utilisation. Si vous n'acceptez pas ces conditions, veuillez ne pas utiliser nos services.</p>
        </section>

        <section class="content-section">
          <h2>2. Description du service</h2>
          <p>OptiTAB est une plateforme éducative en ligne qui propose :</p>
          <ul>
            <li>Des cours et exercices interactifs</li>
            <li>Des fiches de révision</li>
            <li>Des quiz d'évaluation</li>
            <li>Un suivi de progression personnalisé</li>
            <li>Un support pédagogique</li>
          </ul>
        </section>

        <section class="content-section">
          <h2>3. Inscription et compte utilisateur</h2>
          <p>Pour utiliser nos services, vous devez :</p>
          <ul>
            <li>Créer un compte avec des informations exactes et à jour</li>
            <li>Protéger vos identifiants de connexion</li>
            <li>Notifier immédiatement toute utilisation non autorisée</li>
            <li>Être âgé d'au moins 13 ans ou avoir l'autorisation parentale</li>
          </ul>
        </section>

        <section class="content-section">
          <h2>4. Utilisation acceptable</h2>
          <p>Vous vous engagez à :</p>
          <ul>
            <li>Utiliser la plateforme uniquement à des fins éducatives</li>
            <li>Respecter les droits de propriété intellectuelle</li>
            <li>Ne pas tenter de contourner les mesures de sécurité</li>
            <li>Ne pas perturber le fonctionnement de la plateforme</li>
            <li>Respecter les autres utilisateurs</li>
          </ul>
        </section>

        <section class="content-section">
          <h2>5. Contenu et propriété intellectuelle</h2>
          <p>Tout le contenu de la plateforme OptiTAB (cours, exercices, fiches, etc.) est protégé par les droits d'auteur et autres droits de propriété intellectuelle. Vous pouvez utiliser ce contenu uniquement pour votre apprentissage personnel.</p>
        </section>

        <section class="content-section">
          <h2>6. Paiement et abonnement</h2>
          <p>Certains services peuvent nécessiter un abonnement payant. Les conditions de paiement et d'abonnement sont définies dans nos CGV (Conditions Générales de Vente).</p>
        </section>

        <section class="content-section">
          <h2>7. Limitation de responsabilité</h2>
          <p>OptiTAB s'efforce de fournir des services de qualité, mais ne peut garantir :</p>
          <ul>
            <li>La disponibilité permanente de la plateforme</li>
            <li>L'exactitude absolue du contenu éducatif</li>
            <li>Les résultats scolaires des utilisateurs</li>
            <li>L'absence d'erreurs techniques</li>
          </ul>
        </section>

        <section class="content-section">
          <h2>8. Résiliation</h2>
          <p>Nous pouvons suspendre ou résilier votre compte en cas de :</p>
          <ul>
            <li>Violation de ces conditions d'utilisation</li>
            <li>Utilisation frauduleuse du service</li>
            <li>Comportement préjudiciable aux autres utilisateurs</li>
            <li>Non-paiement des frais d'abonnement</li>
          </ul>
        </section>

        <section class="content-section">
          <h2>9. Modifications des conditions</h2>
          <p>Nous nous réservons le droit de modifier ces conditions d'utilisation. Les modifications seront notifiées via la plateforme ou par email. Votre utilisation continue du service après modification constitue votre acceptation des nouvelles conditions.</p>
        </section>

        <section class="content-section">
          <h2>10. Droit applicable</h2>
          <p>Ces conditions d'utilisation sont régies par le droit français. Tout litige sera soumis à la compétence des tribunaux français.</p>
        </section>

        <section class="content-section">
          <h2>11. Contact</h2>
          <p>Pour toute question concernant ces conditions d'utilisation, contactez-nous :</p>
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
.conditions-page {
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