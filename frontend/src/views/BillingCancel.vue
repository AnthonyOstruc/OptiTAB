<template>
  <PaiementCadre>
    <span class="pc-icone pc-icone--neutre" aria-hidden="true"><ArrowUturnLeftIcon /></span>
    <h1>Paiement annulé</h1>
    <p class="pc-texte">
      Aucun montant n’a été débité. Tu peux reprendre un pass ou un abonnement quand tu veux.
    </p>
    <router-link class="pc-btn" to="/billing" data-cta-name="subscribe" data-cta-location="billing_cancel">
      Revoir les formules
    </router-link>
    <router-link class="pc-lien" to="/dashboard">Aller à l’accueil</router-link>
  </PaiementCadre>
</template>

<script setup>
// Retour depuis le paiement Stripe quand l'élève a abandonné.
import PaiementCadre from '@/components/payments/PaiementCadre.vue'
import { ArrowUturnLeftIcon } from '@heroicons/vue/24/outline'
</script>
