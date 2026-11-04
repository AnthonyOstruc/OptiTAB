<template>
  <LegalPage
    title="Conditions générales d’utilisation"
    intro="Les règles d’utilisation de la plateforme OptiTAB, que vous ayez un compte gratuit ou un abonnement."
    updated="2 novembre 2026"
  >
    <template #essentiel>
      <ul>
        <li>Un compte est personnel : il ne se partage pas.</li>
        <li>Les contenus sont réservés à votre usage personnel et ne doivent pas être diffusés.</li>
        <li>Avant 15 ans, l’inscription se fait avec l’accord d’un parent.</li>
        <li>Les conditions de paiement sont détaillées dans les <router-link to="/cgv">CGV</router-link>.</li>
      </ul>
    </template>

    <section id="definitions">
      <h2>Définitions</h2>
      <ul>
        <li><strong>{{ legalInfo.marque }}, la plateforme ou le service :</strong> le site {{ legalInfo.site }} et l’ensemble de ses fonctionnalités.</li>
        <li><strong>Utilisateur :</strong> toute personne qui navigue sur le site ou utilise le service.</li>
        <li><strong>Compte :</strong> espace personnel créé à l’inscription, qui donne accès au service.</li>
        <li><strong>Abonnement ou pass :</strong> accès payant aux contenus d’un niveau, dans les conditions des <router-link to="/cgv">CGV</router-link>.</li>
        <li><strong>Contenus :</strong> cours, fiches de synthèse, exercices et corrigés, quiz, figures, vidéos, textes et outils mis à disposition.</li>
      </ul>
    </section>

    <section id="acces">
      <h2>Accès au service</h2>
      <ul>
        <li>Une partie des contenus est accessible librement, sans inscription. Le reste nécessite un compte, et pour l’accès complet un abonnement ou un pass.</li>
        <li>Vous vous engagez à fournir des informations exactes et à les tenir à jour.</li>
        <li>Vos identifiants sont personnels et confidentiels : toute activité réalisée depuis votre compte vous est imputable.</li>
        <li>Le service est accessible 24&nbsp;h/24, sous réserve des opérations de maintenance et des cas de force majeure.</li>
      </ul>
    </section>

    <section id="services">
      <h2>Services proposés</h2>
      <ul>
        <li>Des cours, fiches de synthèse, exercices corrigés pas à pas et quiz, classés par niveau et par chapitre.</li>
        <li>Un tableau de bord pour suivre sa progression.</li>
        <li>Des outils de calcul et un grapheur.</li>
        <li>Des cours particuliers en ligne, organisés sur demande avec un professeur.</li>
      </ul>
      <p>
        {{ legalInfo.marque }} fait évoluer ses contenus et fonctionnalités en permanence et peut modifier, suspendre ou
        arrêter un service. Les abonnés sont prévenus de toute modification importante.
      </p>
    </section>

    <section id="usage">
      <h2>Règles d’utilisation</h2>
      <p>En utilisant {{ legalInfo.marque }}, vous vous engagez à :</p>
      <ul>
        <li>ne pas partager, prêter ou revendre votre compte ;</li>
        <li>ne pas copier, extraire ou rediffuser les contenus, notamment sur d’autres sites ou réseaux ;</li>
        <li>ne pas perturber le fonctionnement du site ni tenter d’accéder à des données qui ne vous sont pas destinées ;</li>
        <li>rester respectueux envers l’équipe et les autres utilisateurs.</li>
      </ul>
      <p>
        En cas de manquement, {{ legalInfo.marque }} peut suspendre ou fermer le compte concerné, après vous en avoir
        informé sauf urgence.
      </p>
    </section>

    <section id="propriete">
      <h2>Propriété intellectuelle</h2>
      <p>
        Tous les contenus, ainsi que la structure du site, sont protégés par le droit d’auteur. Vous disposez d’un droit
        d’utilisation personnel, non exclusif et non transférable, pour votre usage scolaire et non commercial. Toute
        autre utilisation nécessite notre accord écrit préalable.
      </p>
    </section>

    <section id="contenu">
      <h2>Contenus que vous déposez</h2>
      <p>
        Les contenus que vous déposez sur la plateforme, par exemple vos réponses ou vos copies de quiz, restent les
        vôtres. Vous nous autorisez à les utiliser dans la seule mesure nécessaire au fonctionnement du service (correction,
        suivi de progression). Tout contenu illicite ou injurieux est interdit et peut être supprimé.
      </p>
    </section>

    <section id="donnees">
      <h2>Données personnelles et cookies</h2>
      <p>
        Vos données sont traitées conformément à la <router-link to="/confidentialite">politique de confidentialité</router-link>.
        Les cookies facultatifs (statistiques, publicité) ne sont utilisés qu’avec votre accord, que vous pouvez modifier
        à tout moment : voir la <router-link to="/cookies">politique de cookies</router-link>.
      </p>
    </section>

    <section id="responsabilite">
      <h2>Responsabilité</h2>
      <ul>
        <li>Nous apportons le plus grand soin à l’exactitude des contenus, sans pouvoir garantir l’absence totale d’erreur.</li>
        <li>Les contenus sont un support d’apprentissage : ils ne garantissent pas un résultat à un contrôle, un examen ou un concours.</li>
        <li>{{ legalInfo.marque }} n’est pas responsable des interruptions dues à un cas de force majeure ou à une panne extérieure (réseau, fournisseur d’accès).</li>
      </ul>
    </section>

    <section id="compte">
      <h2>Fermeture du compte</h2>
      <ul>
        <li>Vous pouvez demander la suppression de votre compte à tout moment, par e-mail à <a :href="`mailto:${legalInfo.email}`">{{ legalInfo.email }}</a>.</li>
        <li>Un abonnement en cours se résilie séparément, depuis votre espace (rubrique Abonnement), dans les conditions des <router-link to="/cgv">CGV</router-link>.</li>
        <li>La suppression du compte entraîne celle de votre progression, sous réserve des données que la loi nous oblige à conserver (factures).</li>
      </ul>
    </section>

    <section id="mineurs">
      <h2>Élèves mineurs</h2>
      <ul>
        <li>Avant 15 ans, l’inscription nécessite l’accord explicite d’un parent ou du représentant légal, qui peut lui être demandé.</li>
        <li>À partir de 15 ans, l’élève peut consentir lui-même au traitement de ses données.</li>
        <li>Les achats sont effectués par un parent ou avec son accord.</li>
      </ul>
    </section>

    <section id="modifications">
      <h2>Modification des CGU</h2>
      <p>
        Les présentes conditions peuvent évoluer. En cas de changement important, vous êtes prévenu par e-mail ou par une
        notification. La poursuite de l’utilisation du service vaut acceptation des nouvelles conditions.
      </p>
    </section>

    <section id="litiges">
      <h2>Droit applicable et litiges</h2>
      <p>
        Les présentes CGU sont régies par le droit français. En cas de difficulté, contactez-nous d’abord : nous
        recherchons toujours une solution amiable. Vous pouvez également recourir gratuitement à un médiateur de la
        consommation (voir les <router-link to="/cgv">CGV</router-link>). À défaut d’accord, le litige est porté devant les
        tribunaux compétents.
      </p>
    </section>
  </LegalPage>
</template>

<script setup>
import LegalPage from '@/components/vitrine/LegalPage.vue'
import { legalInfo } from '@/config/legalInfo'
</script>
