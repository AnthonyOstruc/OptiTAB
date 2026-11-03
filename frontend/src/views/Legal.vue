<template>
  <LegalPage
    title="Mentions légales"
    intro="Qui édite le site OptiTAB, qui l’héberge et comment nous joindre."
    updated="2 novembre 2026"
  >
    <section id="editeur">
      <h2>Éditeur du site</h2>
      <p>Le site <strong>{{ legalInfo.site }}</strong> est édité sous la marque <strong>{{ legalInfo.marque }}</strong>.</p>
      <div class="lg-card">
        <dl class="lg-facts">
          <template v-for="fact in editeurFacts" :key="fact.label">
            <dt>{{ fact.label }}</dt>
            <dd>
              <a v-if="fact.href" :href="fact.href">{{ fact.value }}</a>
              <template v-else>{{ fact.value }}</template>
            </dd>
          </template>
        </dl>
      </div>
    </section>

    <section id="directeur">
      <h2>Directeur de la publication</h2>
      <div class="lg-card">
        <dl class="lg-facts">
          <dt>Nom</dt>
          <dd>
            {{ legalInfo.directeurPublication }} ·
            <a :href="legalInfo.linkedin" target="_blank" rel="noopener noreferrer">profil LinkedIn</a>
          </dd>
          <dt>Fonction</dt>
          <dd>Fondateur et responsable éditorial</dd>
          <dt>E-mail</dt>
          <dd><a :href="`mailto:${legalInfo.email}`">{{ legalInfo.email }}</a></dd>
        </dl>
      </div>
    </section>

    <section id="hebergement">
      <h2>Hébergement</h2>
      <p>Le site et ses contenus sont hébergés par les prestataires suivants.</p>
      <div v-for="hebergeur in legalInfo.hebergeurs" :key="hebergeur.nom" class="lg-card">
        <p class="lg-card__title">{{ hebergeur.role }}</p>
        <dl class="lg-facts">
          <dt>Hébergeur</dt>
          <dd>{{ hebergeur.nom }}</dd>
          <dt>Adresse</dt>
          <dd>{{ hebergeur.adresse }}</dd>
          <dt>Site web</dt>
          <dd><a :href="hebergeur.site" target="_blank" rel="noopener noreferrer">{{ hebergeur.site.replace('https://', '') }}</a></dd>
        </dl>
      </div>
    </section>

    <section id="propriete">
      <h2>Propriété intellectuelle</h2>
      <p>
        L’ensemble du site relève de la législation française et internationale sur le droit d’auteur et la propriété
        intellectuelle : cours, fiches de synthèse, exercices et leurs corrigés, figures, vidéos, textes, logos et marque
        {{ legalInfo.marque }}.
      </p>
      <p>
        Toute reproduction, représentation ou diffusion, totale ou partielle, sur quelque support que ce soit, est
        interdite sans l’autorisation écrite préalable du directeur de la publication.
      </p>
    </section>

    <section id="responsabilite">
      <h2>Responsabilité</h2>
      <p>
        Nous apportons le plus grand soin à l’exactitude des contenus et les mettons à jour régulièrement. Le site peut
        toutefois contenir des inexactitudes ou des omissions.
      </p>
      <p>
        Si vous constatez une erreur ou un dysfonctionnement, merci de nous l’indiquer à
        <a :href="`mailto:${legalInfo.email}`">{{ legalInfo.email }}</a> en décrivant le problème le plus précisément
        possible.
      </p>
      <p>
        {{ legalInfo.marque }} ne saurait être tenu responsable d’un dommage subi par l’équipement de l’utilisateur ou d’une
        perte de données consécutifs au téléchargement d’un document depuis le site.
      </p>
    </section>

    <section id="liens">
      <h2>Liens hypertextes</h2>
      <p>
        Le site peut contenir des liens vers d’autres sites. {{ legalInfo.marque }} n’exerce aucun contrôle sur ces sites
        et n’est pas responsable de leur contenu.
      </p>
    </section>

    <section id="donnees">
      <h2>Données personnelles et cookies</h2>
      <p>
        La manière dont nous traitons vos données est détaillée dans la
        <router-link to="/confidentialite">politique de confidentialité</router-link>, et l’usage des cookies dans la
        <router-link to="/cookies">politique de cookies</router-link>. Vous pouvez modifier vos choix de cookies à tout
        moment avec le lien « Gérer mes cookies » en bas de chaque page.
      </p>
    </section>

    <section id="droit">
      <h2>Droit applicable</h2>
      <p>
        Les présentes mentions légales sont régies par le droit français. Tout litige relatif à l’utilisation du site
        relève des tribunaux compétents d’{{ legalInfo.juridiction }}, sous réserve des règles protectrices des
        consommateurs.
      </p>
    </section>
  </LegalPage>
</template>

<script setup>
import { computed } from 'vue'
import LegalPage from '@/components/vitrine/LegalPage.vue'
import { legalInfo } from '@/config/legalInfo'

// Seules les informations renseignées dans config/legalInfo.js sont affichées.
const editeurFacts = computed(() => {
  const e = legalInfo.editeur
  return [
    { label: 'Raison sociale', value: e.raisonSociale },
    { label: 'Forme juridique', value: e.formeJuridique },
    { label: 'Siège social', value: e.adresse },
    { label: 'SIREN / RCS', value: e.siren },
    { label: 'N° de TVA', value: e.tva },
    { label: 'Téléphone', value: e.telephone },
    { label: 'E-mail', value: legalInfo.email, href: `mailto:${legalInfo.email}` },
    { label: 'WhatsApp', value: legalInfo.whatsappAffiche, href: `https://wa.me/${legalInfo.whatsapp}` }
  ].filter((fact) => fact.value)
})
</script>
