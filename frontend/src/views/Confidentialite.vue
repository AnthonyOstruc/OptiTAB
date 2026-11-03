<template>
  <LegalPage
    title="Politique de confidentialité"
    intro="Quelles données nous collectons, pourquoi, avec qui elles sont partagées et comment exercer vos droits."
    updated="2 novembre 2026"
  >
    <template #essentiel>
      <ul>
        <li>Nous collectons uniquement ce qui est utile au service : votre compte, votre classe et votre progression.</li>
        <li>Vos données ne sont jamais vendues ni louées.</li>
        <li>Vos données bancaires sont traitées par Stripe et ne passent jamais par nos serveurs.</li>
        <li>Les statistiques et la publicité ne sont activées qu’avec votre accord.</li>
        <li>Vous pouvez consulter, corriger ou supprimer vos données sur simple demande.</li>
      </ul>
    </template>

    <section id="responsable">
      <h2>Responsable du traitement</h2>
      <p>
        Le responsable du traitement est l’éditeur du site {{ legalInfo.marque }}, présenté dans les
        <router-link to="/legal">mentions légales</router-link>.
      </p>
      <div class="lg-card">
        <dl class="lg-facts">
          <dt>Contact</dt>
          <dd><a :href="`mailto:${legalInfo.email}`">{{ legalInfo.email }}</a></dd>
          <dt>Responsable éditorial</dt>
          <dd>{{ legalInfo.directeurPublication }}</dd>
        </dl>
      </div>
    </section>

    <section id="donnees">
      <h2>Données collectées</h2>
      <ul>
        <li><strong>Votre compte :</strong> prénom, nom, adresse e-mail et mot de passe (enregistré sous forme chiffrée, jamais en clair). Si vous utilisez « Continuer avec Google », nous recevons votre nom, votre e-mail et votre identifiant Google.</li>
        <li><strong>Votre profil scolaire :</strong> pays, classe, profil élève ou parent, et le lien entre un compte parent et un compte élève lorsque vous le créez.</li>
        <li><strong>Votre activité :</strong> exercices réalisés, réponses, quiz rendus, points d’expérience et progression.</li>
        <li><strong>Vos paiements :</strong> formule choisie, montant, date, statut et factures. Les données de carte bancaire sont saisies directement chez Stripe : nous n’y avons jamais accès.</li>
        <li><strong>Vos échanges avec nous :</strong> messages envoyés par le formulaire de contact, par e-mail ou par WhatsApp, et adresse e-mail si vous vous inscrivez à la newsletter.</li>
        <li><strong>Données techniques :</strong> journaux de connexion et, avec votre accord uniquement, mesures d’audience (voir la <router-link to="/cookies">politique de cookies</router-link>).</li>
      </ul>
    </section>

    <section id="finalites">
      <h2>Pourquoi nous les utilisons</h2>
      <div class="lg-table-wrap">
        <table class="lg-table">
          <thead>
            <tr><th scope="col">Utilisation</th><th scope="col">Base légale</th></tr>
          </thead>
          <tbody>
            <tr><td>Créer et gérer votre compte, donner accès aux contenus de votre classe</td><td><span class="lg-tag">Contrat</span></td></tr>
            <tr><td>Suivre votre progression et vos résultats</td><td><span class="lg-tag">Contrat</span></td></tr>
            <tr><td>Encaisser les abonnements et pass, émettre les factures</td><td><span class="lg-tag">Contrat</span> <span class="lg-tag">Obligation légale</span></td></tr>
            <tr><td>Répondre à vos questions et assurer le support</td><td><span class="lg-tag">Contrat</span></td></tr>
            <tr><td>Envoyer la newsletter</td><td><span class="lg-tag lg-tag--vert">Consentement</span></td></tr>
            <tr><td>Mesurer l’audience et nos campagnes publicitaires</td><td><span class="lg-tag lg-tag--vert">Consentement</span></td></tr>
            <tr><td>Sécuriser le site et prévenir la fraude</td><td><span class="lg-tag lg-tag--orange">Intérêt légitime</span></td></tr>
          </tbody>
        </table>
      </div>
    </section>

    <section id="destinataires">
      <h2>Qui peut y avoir accès</h2>
      <p>
        Vos données sont réservées à l’équipe {{ legalInfo.marque }}. Nous ne les vendons ni ne les louons. Elles sont
        confiées, pour le strict nécessaire, aux prestataires suivants :
      </p>
      <div class="lg-table-wrap">
        <table class="lg-table">
          <thead>
            <tr><th scope="col">Prestataire</th><th scope="col">Rôle</th></tr>
          </thead>
          <tbody>
            <tr><th scope="row">Render</th><td>Hébergement du site, du serveur et de la base de données</td></tr>
            <tr><th scope="row">Amazon Web Services</th><td>Stockage des images et documents des cours (serveurs à Paris)</td></tr>
            <tr><th scope="row">Stripe</th><td>Paiement sécurisé des abonnements, pass et cours particuliers</td></tr>
            <tr><th scope="row">Google</th><td>Connexion avec Google, envoi des e-mails et, avec votre accord, mesure d’audience (Google Analytics)</td></tr>
            <tr><th scope="row">Microsoft</th><td>Avec votre accord, analyse de l’expérience de navigation (Clarity)</td></tr>
            <tr><th scope="row">Meta</th><td>Avec votre accord, mesure des campagnes publicitaires (Pixel) ; WhatsApp si vous nous écrivez par ce moyen</td></tr>
          </tbody>
        </table>
      </div>
      <p>Vos données peuvent aussi être communiquées aux autorités lorsque la loi l’exige.</p>
    </section>

    <section id="transferts">
      <h2>Transferts hors de l’Union européenne</h2>
      <p>
        Certains de ces prestataires sont établis aux États-Unis. Ces transferts sont encadrés par les garanties prévues
        par le RGPD : décision d’adéquation de la Commission européenne (« Data Privacy Framework ») ou clauses
        contractuelles types.
      </p>
    </section>

    <section id="conservation">
      <h2>Durée de conservation</h2>
      <ul>
        <li><strong>Compte et progression :</strong> tant que votre compte existe, puis archivage d’un an au maximum.</li>
        <li><strong>Factures et pièces comptables :</strong> 10 ans, comme l’impose le Code de commerce.</li>
        <li><strong>Newsletter :</strong> jusqu’à votre désinscription, possible en un clic dans chaque e-mail.</li>
        <li><strong>Cookies de mesure :</strong> 13 mois au maximum ; votre choix de cookies est mémorisé 6 mois.</li>
      </ul>
      <p>Au-delà, les données sont supprimées ou rendues anonymes, pour n’être utilisées qu’à des fins statistiques.</p>
    </section>

    <section id="securite">
      <h2>Sécurité</h2>
      <ul>
        <li>Mots de passe chiffrés et connexions protégées (HTTPS).</li>
        <li>Paiements entièrement gérés par Stripe, certifié PCI-DSS.</li>
        <li>Accès aux données limité aux seules personnes qui en ont besoin.</li>
        <li>Sauvegardes régulières et mises à jour de sécurité.</li>
      </ul>
    </section>

    <section id="droits">
      <h2>Vos droits</h2>
      <p>Conformément au RGPD et à la loi Informatique et Libertés, vous pouvez à tout moment :</p>
      <ul>
        <li>accéder à vos données et en obtenir une copie ;</li>
        <li>les faire rectifier ou compléter ;</li>
        <li>demander leur effacement, y compris la suppression de votre compte ;</li>
        <li>vous opposer à leur utilisation ou en demander la limitation ;</li>
        <li>récupérer vos données dans un format lisible (portabilité) ;</li>
        <li>retirer votre consentement (newsletter, cookies) ;</li>
        <li>définir des directives sur le sort de vos données après votre décès.</li>
      </ul>
      <p>
        Écrivez-nous à <a :href="`mailto:${legalInfo.email}`">{{ legalInfo.email }}</a> : nous répondons dans un délai
        d’un mois au maximum. Si vous estimez que vos droits ne sont pas respectés, vous pouvez adresser une réclamation à
        la CNIL sur <a href="https://www.cnil.fr" target="_blank" rel="noopener noreferrer">cnil.fr</a>.
      </p>
    </section>

    <section id="mineurs">
      <h2>Élèves mineurs</h2>
      <ul>
        <li>Avant 15 ans, l’inscription nécessite l’accord d’un parent ou du représentant légal.</li>
        <li>À partir de 15 ans, l’élève peut consentir lui-même au traitement de ses données.</li>
        <li>Les parents peuvent demander à tout moment l’accès aux données de leur enfant ou leur suppression.</li>
      </ul>
    </section>

    <section id="modifications">
      <h2>Modifications</h2>
      <p>
        Cette politique peut évoluer pour suivre la réglementation ou nos services. En cas de changement important, nous
        vous prévenons par e-mail ou par une notification sur la plateforme.
      </p>
    </section>
  </LegalPage>
</template>

<script setup>
import LegalPage from '@/components/vitrine/LegalPage.vue'
import { legalInfo } from '@/config/legalInfo'
</script>
