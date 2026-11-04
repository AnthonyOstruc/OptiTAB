<template>
  <!-- Ancienne page « Conditions d'utilisation » : devenue la vue d'ensemble des
       documents légaux, pour éviter un second texte qui contredirait les CGU. -->
  <LegalPage
    title="Conditions et informations légales"
    intro="Tous les documents qui encadrent l’utilisation d’OptiTAB, résumés en quelques lignes."
    updated="2 novembre 2026"
  >
    <template #essentiel>
      <ul>
        <li>Les règles d’utilisation du site sont dans les CGU, les conditions d’achat dans les CGV.</li>
        <li>Vos données personnelles et les cookies ont chacun leur politique dédiée.</li>
        <li>Une question sur l’un de ces documents&nbsp;? Écrivez-nous, nous répondons sous 24&nbsp;h.</li>
      </ul>
    </template>

    <section v-for="doc in DOCUMENTS" :id="doc.id" :key="doc.id">
      <h2>{{ doc.titre }}</h2>
      <p>{{ doc.resume }}</p>
      <ul>
        <li v-for="point in doc.points" :key="point">{{ point }}</li>
      </ul>
      <div class="lg-button">
        <router-link :to="doc.lien" class="vt-btn vt-btn--ghost vt-btn--sm">
          Lire {{ doc.article }} {{ doc.court }}
          <ArrowRightIcon aria-hidden="true" />
        </router-link>
      </div>
    </section>
  </LegalPage>
</template>

<script setup>
import { ArrowRightIcon } from '@heroicons/vue/24/outline'
import LegalPage from '@/components/vitrine/LegalPage.vue'

const DOCUMENTS = [
  {
    id: 'cgu',
    titre: 'Conditions générales d’utilisation',
    article: 'les',
    court: 'CGU',
    lien: '/cgu',
    resume: 'Les règles d’utilisation de la plateforme, avec ou sans abonnement.',
    points: [
      'Un compte est personnel et ne se partage pas.',
      'Les contenus sont réservés à un usage personnel et scolaire.',
      'Avant 15 ans, l’inscription se fait avec l’accord d’un parent.'
    ]
  },
  {
    id: 'cgv',
    titre: 'Conditions générales de vente',
    article: 'les',
    court: 'CGV',
    lien: '/cgv',
    resume: 'Les conditions des abonnements, des pass et des cours particuliers.',
    points: [
      'Chaque abonnement ou pass donne accès à une classe.',
      'Les abonnements sont sans engagement et se résilient à tout moment.',
      'Le paiement est sécurisé par Stripe.'
    ]
  },
  {
    id: 'confidentialite',
    titre: 'Politique de confidentialité',
    article: 'la',
    court: 'politique de confidentialité',
    lien: '/confidentialite',
    resume: 'Les données que nous collectons, pourquoi, et comment exercer vos droits.',
    points: [
      'Vos données ne sont jamais vendues ni louées.',
      'Vous pouvez les consulter, les corriger ou les supprimer sur demande.'
    ]
  },
  {
    id: 'cookies',
    titre: 'Politique de cookies',
    article: 'la',
    court: 'politique de cookies',
    lien: '/cookies',
    resume: 'Les cookies utilisés sur le site et la façon de gérer vos choix.',
    points: [
      'Les statistiques et la publicité ne sont activées qu’avec votre accord.',
      'Vous pouvez changer d’avis à tout moment avec « Gérer mes cookies ».'
    ]
  },
  {
    id: 'mentions',
    titre: 'Mentions légales',
    article: 'les',
    court: 'mentions légales',
    lien: '/legal',
    resume: 'L’éditeur du site, le directeur de la publication et les hébergeurs.',
    points: ['Les coordonnées pour nous joindre et les règles de propriété intellectuelle.']
  }
]
</script>
