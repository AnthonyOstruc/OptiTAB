<template>
  <div class="ah">
    <header class="es-page-head">
      <div>
        <p class="ah__eyebrow">Administration</p>
        <h1 class="es-h1">Tableau de bord</h1>
        <p class="es-sub">Tous les outils pour gérer les contenus, le programme et les abonnements.</p>
      </div>
      <div class="ah__liens">
        <a href="/ressources-gratuites/" target="_blank" rel="noopener" class="es-btn es-btn--ghost es-btn--sm">
          <BookOpenIcon aria-hidden="true" />
          Ressources gratuites
        </a>
        <a href="/blog/" target="_blank" rel="noopener" class="es-btn es-btn--ghost es-btn--sm">
          <NewspaperIcon aria-hidden="true" />
          Blog
        </a>
      </div>
    </header>

    <section v-for="section in ADMIN_SECTIONS" :key="section.titre" class="ah__section" :aria-labelledby="idSection(section)">
      <h2 :id="idSection(section)" class="ah__titre">{{ section.titre }}</h2>
      <div class="ah__grille">
        <RouterLink v-for="item in section.items" :key="item.to" :to="item.to" class="ah__tuile">
          <span class="ah__icone" aria-hidden="true"><component :is="item.icon" /></span>
          <span class="ah__texte">
            <strong>{{ item.label }}</strong>
            <span>{{ item.description }}</span>
          </span>
          <ChevronRightIcon class="ah__fleche" aria-hidden="true" />
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
// Accueil de l'administration, dans le style du nouvel espace. La liste des
// outils vient de config/adminMenu.js (la même que le menu latéral).
import { BookOpenIcon, ChevronRightIcon, NewspaperIcon } from '@heroicons/vue/24/outline'
import { ADMIN_SECTIONS } from '@/config/adminMenu'

const idSection = (section) => `ah-${section.titre.toLowerCase().normalize('NFD').replace(/[^a-z]+/g, '-')}`
</script>

<style scoped>
.ah__eyebrow {
  margin: 0 0 6px !important;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--es-green-700);
}

.ah__liens {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.ah__liens svg {
  width: 17px;
  height: 17px;
}

.ah__section + .ah__section {
  margin-top: 32px;
}

.ah__titre {
  margin: 0 0 12px !important;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--es-muted);
}

.ah__grille {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 12px;
}

.ah__tuile {
  display: flex;
  align-items: center;
  gap: 14px;
  min-height: 84px;
  padding: 16px;
  border: 1px solid var(--es-line);
  border-radius: var(--es-radius);
  background: var(--es-card);
  box-shadow: var(--es-shadow);
  text-decoration: none;
  transition: border-color 0.15s ease, box-shadow 0.15s ease, transform 0.15s ease;
}

.ah__tuile:hover {
  border-color: var(--es-navy-100);
  box-shadow: var(--es-shadow-lg);
  transform: translateY(-1px);
}

.ah__tuile:focus-visible {
  outline: 3px solid rgba(27, 60, 142, 0.35);
  outline-offset: 2px;
}

.ah__icone {
  display: inline-flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: var(--es-navy-50);
  color: var(--es-navy);
}

.ah__icone svg {
  width: 22px;
  height: 22px;
}

.ah__texte {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}

.ah__texte strong {
  font-size: 15px;
  font-weight: 700;
  color: var(--es-ink);
}

.ah__texte span {
  font-size: 13px;
  line-height: 1.4;
  color: var(--es-muted);
}

.ah__fleche {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  color: #a3abbd;
  transition: transform 0.15s ease, color 0.15s ease;
}

.ah__tuile:hover .ah__fleche {
  color: var(--es-navy);
  transform: translateX(2px);
}

@media (max-width: 640px) {
  .ah__grille {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .ah__tuile {
    min-height: 0;
    padding: 14px;
  }
}
</style>
