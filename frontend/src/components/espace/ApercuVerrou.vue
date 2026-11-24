<template>
  <div :class="['av', { 'av--suite': suite }]">
    <span class="av__icone" aria-hidden="true"><LockClosedIcon /></span>
    <strong class="av__titre">{{ titre }}</strong>
    <p class="av__texte">{{ texte }}</p>
    <router-link
      :to="{ name: 'Billing', hash: '#plans' }"
      class="es-btn es-btn--green"
      data-cta-name="pricing"
      :data-cta-location="`apercu_${emplacement}`"
    >
      Débloquer ma classe
      <ArrowRightIcon aria-hidden="true" />
    </router-link>
    <p class="av__note">Pass ponctuel ou abonnement sans engagement.</p>
  </div>
</template>

<script setup>
// Contenu réservé aux abonnés, dans un chapitre ouvert en aperçu (élève connecté
// sans abonnement). Le serveur n'envoie pas ce contenu : il n'y a rien à « cacher ».
import { ArrowRightIcon, LockClosedIcon } from '@heroicons/vue/24/outline'

defineProps({
  titre: { type: String, required: true },
  texte: { type: String, required: true },
  // Nom de l'endroit, pour le suivi des clics (cours, fiche, quiz, exercice).
  emplacement: { type: String, default: 'chapitre' },
  // Placé à la suite d'un contenu (fin de l'aperçu du cours) : filet de séparation.
  suite: { type: Boolean, default: false }
})
</script>

<style scoped>
.av {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 560px;
  margin: 0 auto;
  padding: 36px 20px;
  text-align: center;
}

.av--suite {
  max-width: none;
  margin-top: 28px;
  padding: 32px 20px 8px;
  border-top: 1px dashed var(--es-line);
}

.av__icone {
  display: grid;
  place-items: center;
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: var(--es-bg);
  color: var(--es-muted);
}

.av__icone svg {
  width: 26px;
  height: 26px;
}

.av__titre {
  margin-top: 14px;
  font-size: 19px;
  line-height: 1.3;
  color: var(--es-ink, #121a33);
}

.av__texte {
  max-width: 460px;
  margin: 8px 0 20px;
  font-size: 15px;
  line-height: 1.6;
  color: var(--es-muted);
}

.av__note {
  margin: 12px 0 0;
  font-size: 13px;
  color: var(--es-muted);
}
</style>
