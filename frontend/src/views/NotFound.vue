<template>
  <component :is="connecte ? EspaceLayout : VitrineLayout" v-bind="connecte ? { title: 'Page introuvable' } : {}">
    <section class="nf">
      <div class="nf__code" aria-hidden="true">
        <span>4</span><span class="nf__zero">0</span><span>4</span>
      </div>
      <p class="nf__kicker">Aucune solution… sur cette adresse</p>
      <h1 class="nf__title">Cette page n’existe pas, ou plus.</h1>
      <p class="nf__text">Le lien est peut-être ancien ou mal recopié. Voici où continuer :</p>

      <ul class="nf__links">
        <li v-for="lien in liens" :key="lien.to">
          <router-link :to="lien.to" class="nf__link">
            <span class="nf__icon"><component :is="lien.icone" aria-hidden="true" /></span>
            <span class="nf__link-text">
              <strong>{{ lien.titre }}</strong>
              <span>{{ lien.texte }}</span>
            </span>
            <ChevronRightIcon class="nf__chev" aria-hidden="true" />
          </router-link>
        </li>
      </ul>

      <p class="nf__help">
        Vous cherchiez quelque chose de précis&nbsp;?
        <router-link to="/contact">Écrivez-nous</router-link>, nous répondons sous 24&nbsp;h.
      </p>
    </section>
  </component>
</template>

<script setup>
import { computed } from 'vue'
import {
  BookOpenIcon,
  ChatBubbleLeftRightIcon,
  ChevronRightIcon,
  CreditCardIcon,
  HomeIcon,
  SparklesIcon
} from '@heroicons/vue/24/outline'
import EspaceLayout from '@/components/espace/EspaceLayout.vue'
import VitrineLayout from '@/components/vitrine/VitrineLayout.vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const connecte = computed(() => userStore.isAuthenticated)

const liens = computed(() => (connecte.value
  ? [
      { to: '/dashboard', icone: HomeIcon, titre: 'Mon espace', texte: 'Reprendre où vous vous êtes arrêté' },
      { to: '/chapitres', icone: BookOpenIcon, titre: 'Mes chapitres', texte: 'Cours, fiches et exercices de la classe' },
      { to: '/contact', icone: ChatBubbleLeftRightIcon, titre: 'Contact', texte: 'Une question ? Réponse sous 24 h' }
    ]
  : [
      { to: '/', icone: HomeIcon, titre: 'Accueil', texte: 'Découvrir OptiTAB' },
      { to: '/ressources-gratuites', icone: SparklesIcon, titre: 'Ressources gratuites', texte: 'Cours, fiches et exercices en accès libre' },
      { to: '/tarifs', icone: CreditCardIcon, titre: 'Tarifs', texte: 'Des formules simples, sans engagement' }
    ]))
</script>

<style scoped>
.nf {
  --nf-navy: #1b3c8e;
  --nf-green: #5fac60;
  --nf-ink: #172033;
  --nf-muted: #667085;
  --nf-line: #e3e7ef;

  max-width: 640px;
  margin: 0 auto;
  padding: 48px 16px 72px;
  font-family: 'Montserrat', 'Segoe UI', system-ui, sans-serif;
  text-align: center;
}

.nf__code {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: clamp(88px, 16vw, 132px);
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.04em;
  color: var(--nf-navy);
}

.nf__zero {
  position: relative;
  color: var(--nf-green);
}

.nf__zero::after {
  content: '';
  position: absolute;
  top: 50%;
  left: -6%;
  width: 112%;
  height: 0.08em;
  border-radius: 0.04em;
  background: var(--nf-navy);
  transform: rotate(-35deg);
}

.nf__kicker {
  margin: 18px 0 0;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #3b8544;
}

.nf__title {
  margin: 10px 0 0;
  font-size: clamp(24px, 3.4vw, 32px);
  font-weight: 700;
  line-height: 1.2;
  color: var(--nf-ink);
}

.nf__text {
  margin: 12px 0 0;
  font-size: 16px;
  color: var(--nf-muted);
}

.nf__links {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 28px 0 0;
  padding: 0;
  text-align: left;
  list-style: none;
}

.nf__link {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  border: 1px solid var(--nf-line);
  border-radius: 14px;
  background: #fff;
  text-decoration: none;
  transition: border-color 0.15s ease, box-shadow 0.2s ease, transform 0.2s ease;
}

.nf__link:hover {
  border-color: var(--nf-navy);
  box-shadow: 0 10px 24px rgba(16, 24, 40, 0.08);
  transform: translateY(-1px);
}

.nf__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  flex-shrink: 0;
  border-radius: 12px;
  background: #eef1f8;
  color: var(--nf-navy);
}

.nf__icon svg {
  width: 22px;
  height: 22px;
}

.nf__link-text {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
  font-size: 14px;
  color: var(--nf-muted);
}

.nf__link-text strong {
  font-size: 16px;
  color: var(--nf-ink);
}

.nf__chev {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  color: #98a2b3;
}

.nf__help {
  margin: 28px 0 0;
  font-size: 15px;
  color: var(--nf-muted);
}

.nf__help a {
  font-weight: 700;
  color: var(--nf-navy);
}

@media (prefers-reduced-motion: reduce) {
  .nf__link {
    transition: none;
  }
}
</style>
