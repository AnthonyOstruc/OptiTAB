<template>
  <section class="free-showcase">
    <div class="showcase-header">
      <p class="eyebrow">
        <SparklesIcon class="eyebrow-icon" />
        Aperçus gratuits
      </p>
      <h2>Offrez un avant-goût d'OptiTAB</h2>
      <p class="header-subtitle">
        Sélectionnez quelques chapitres ouverts pour convaincre les élèves et rassurer les parents avant l'abonnement.
      </p>
    </div>

    <div class="cards-grid">
      <article
        v-for="item in items"
        :key="item.type"
        class="card"
        role="button"
        tabindex="0"
        @click="goTo(item)"
        @keyup.enter.prevent="goTo(item)"
      >
        <div class="card-badge" :style="{ background: item.accent || '#0f172a' }">
          {{ item.badge }}
        </div>
        <h3>{{ item.title }}</h3>
        <p class="card-highlight">
          {{ item.highlight }}
        </p>
        <p class="card-description">{{ item.description }}</p>
        <ul class="card-bullets">
          <li v-for="bullet in item.bullets" :key="bullet">
            <CheckCircleIcon class="bullet-icon" />
            <span>{{ bullet }}</span>
          </li>
        </ul>
        <RouterLink :to="item.to" class="card-link">
          Explorer gratuitement
          <ArrowUpRightIcon class="link-icon" />
        </RouterLink>
      </article>
    </div>
  </section>
</template>

<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { SparklesIcon, CheckCircleIcon, ArrowUpRightIcon } from '@heroicons/vue/24/outline'

defineProps({
  items: {
    type: Array,
    default: () => []
  }
})

const router = useRouter()

const goTo = (item) => {
  if (!item?.to) return
  router.push(item.to)
}
</script>

<style scoped lang="scss">
.free-showcase {
  padding: 80px 0;
  display: flex;
  flex-direction: column;
  gap: 36px;
}

.showcase-header {
  text-align: center;
  max-width: 820px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin: 0 auto;
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 600;
  color: #0f172a;
  background: #f1f5f9;
}

.eyebrow-icon {
  width: 18px;
  height: 18px;
  color: #f97316;
}

h2 {
  font-size: clamp(28px, 4vw, 36px);
  color: #0f172a;
  margin: 0;
}

.header-subtitle {
  margin: 0 auto;
  color: #475569;
  font-size: 16px;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
}

.card {
  border-radius: 28px;
  padding: 32px;
  background: #ffffff;
  box-shadow: 0 20px 45px rgba(15, 23, 42, 0.08);
  display: flex;
  flex-direction: column;
  gap: 14px;
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(226, 232, 240, 0.8);
  cursor: pointer;
}

.card::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1px;
  background: linear-gradient(120deg, rgba(248, 250, 252, .8), rgba(59, 130, 246, .3));
  -webkit-mask:
    linear-gradient(#fff 0 0) content-box,
    linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
}

.card-badge {
  display: inline-flex;
  align-self: flex-start;
  padding: 6px 14px;
  border-radius: 999px;
  color: #fff;
  font-weight: 600;
  font-size: 13px;
}

.card-highlight {
  text-transform: uppercase;
  font-size: 13px;
  letter-spacing: 0.08em;
  color: #64748b;
  margin: 0;
}

.card-description {
  color: #1f2937;
  margin: 0;
  font-size: 15px;
  line-height: 1.5;
}

.card-bullets {
  display: flex;
  flex-direction: column;
  gap: 8px;
  list-style: none;
  padding: 0;
  margin: 4px 0 18px;
}

.card-bullets li {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #475569;
  font-size: 14px;
}

.bullet-icon {
  width: 18px;
  height: 18px;
  color: #22c55e;
}

.card-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
  color: #0f172a;
  text-decoration: none;
  margin-top: auto;
  transition: transform 0.2s ease, color 0.2s ease;
}

.card-link:hover {
  color: #2563eb;
  transform: translateY(-2px);
}

.link-icon {
  width: 18px;
  height: 18px;
}

@media (max-width: 768px) {
  .free-showcase {
    padding: 60px 0 30px;
  }

  .card {
    padding: 24px;
  }
}
</style>
