<template>
  <VitrineLayout>
    <section class="vt-section rg-secours">
      <div class="vt-container">
        <p class="vt-kicker">{{ texte.kicker }}</p>
        <h1 class="vt-title">{{ texte.titre }}</h1>
        <p class="vt-lead">{{ texte.lead }}</p>
        <a class="vt-btn vt-btn--primary" :href="texte.lien">{{ texte.bouton }}</a>
      </div>
    </section>
  </VitrineLayout>
</template>

<script setup>
// Page de secours des ressources gratuites et du blog : affichée seulement
// quand la page statique demandée n'existe pas (voir router/ressources.js).
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import VitrineLayout from '@/components/vitrine/VitrineLayout.vue'
import { RACINE_BLOG, RACINE_RESSOURCES } from '@/router/ressources'

const route = useRoute()
const texte = computed(() => (route.path.startsWith('/blog')
  ? {
      kicker: 'Le blog OptiTAB',
      titre: 'Conseils et méthodes pour progresser en maths',
      lead: 'Cette page n’est pas disponible pour le moment. Retrouve tous les articles depuis l’accueil du blog.',
      lien: RACINE_BLOG,
      bouton: 'Voir le blog'
    }
  : {
      kicker: 'Ressources gratuites',
      titre: 'Cours de maths gratuits, du CP à la Terminale',
      lead: 'Cette page n’est pas disponible pour le moment. Retrouve tous les cours, fiches de révision et exercices corrigés gratuits depuis l’accueil des ressources.',
      lien: RACINE_RESSOURCES,
      bouton: 'Voir les ressources gratuites'
    }))
</script>

<style scoped>
.rg-secours {
  padding: 96px 0;
  text-align: center;
}

.rg-secours .vt-lead {
  max-width: 56ch;
  margin: 16px auto 28px;
}
</style>
