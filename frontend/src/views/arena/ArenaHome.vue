<template>
  <div class="arena-home">
    <ArenaCtaModal />

    <header class="arena-hero">
      <div class="arena-hero__left">
        <p class="arena-hero__eyebrow">OptiTAB Arena</p>
        <h1>Entraînez-vous. Progressez. Brillez.</h1>
        <p class="arena-hero__lead">
          Un défi de mathématiques chaque jour, des niveaux à débloquer,
          une Forge personnelle pour transformer vos erreurs en force.
        </p>
        <div class="arena-hero__stats">
          <div class="stat"><span class="stat__value">{{ arena.streak }}</span><span class="stat__label">Série</span></div>
          <div class="stat"><span class="stat__value">{{ arena.bestStreak }}</span><span class="stat__label">Record</span></div>
          <div class="stat"><span class="stat__value">{{ arena.xp }}</span><span class="stat__label">XP total</span></div>
        </div>
      </div>
      <div class="arena-hero__right">
        <div v-if="dailyAvailable" class="daily-card" @click="goDaily">
          <span class="daily-card__badge">⚡ Défi du jour</span>
          <h3>{{ daily?.daily?.level?.title }}</h3>
          <p v-if="daily?.daily?.bonus_xp">+{{ daily.daily.bonus_xp }} XP bonus</p>
          <button class="btn-primary">{{ daily?.playable ? 'Jouer maintenant' : 'Voir' }}</button>
          <p v-if="!daily?.playable && daily?.cta" class="daily-card__hint">{{ daily.cta.body }}</p>
        </div>
        <div v-else class="daily-card daily-card--empty">
          <span class="daily-card__badge">⚡ Défi du jour</span>
          <p>Aucun défi quotidien aujourd'hui.</p>
        </div>
      </div>
    </header>

    <div v-if="arena.isAdminPreview && !arena.isPublic" class="admin-banner">
      🔧 Mode aperçu administrateur — le jeu n'est pas encore public.
    </div>

    <section class="arena-section">
      <header class="arena-section__head">
        <h2>Chapitres</h2>
        <RouterLink to="/jeu/forge" class="link-forge">🔥 Forge des erreurs</RouterLink>
      </header>
      <div class="arena-grid">
        <article v-for="chapter in arena.chapters" :key="chapter.id" class="chapter-card"
                 :style="{ '--accent': chapter.color || '#2563eb' }"
                 @click="goChapter(chapter)">
          <div class="chapter-card__icon">{{ chapter.icon || '📘' }}</div>
          <h3>{{ chapter.title }}</h3>
          <p>{{ chapter.description }}</p>
          <div class="chapter-card__footer">
            <span class="badge" v-if="chapter.is_premium">OptiTAB+</span>
            <span class="badge badge--free" v-else>Accès libre</span>
            <span class="chapter-card__count">{{ chapter.levels?.length || 0 }} niveaux</span>
          </div>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useArenaStore } from '@/stores/arena'
import ArenaCtaModal from '@/components/arena/ArenaCtaModal.vue'

const arena = useArenaStore()
const router = useRouter()

const daily = computed(() => arena.daily)
const dailyAvailable = computed(() => Boolean(daily.value && daily.value.available))

onMounted(async () => {
  await Promise.all([
    arena.loadConfig(),
    arena.loadChapters(),
    arena.loadDaily(),
    arena.loadMe(),
  ])
  arena.track('game_started', {})
})

function goChapter(chapter) {
  router.push(`/jeu/chapitre/${chapter.slug}`)
}

function goDaily() {
  if (!daily.value?.playable && daily.value?.cta) {
    arena.showCta(daily.value.cta)
    arena.track('cta_displayed', { id: daily.value.cta.id, trigger: daily.value.cta.trigger })
    return
  }
  if (daily.value?.daily?.level?.id) {
    router.push(`/jeu/jouer/${daily.value.daily.level.id}?daily=1`)
  }
}
</script>

<style scoped>
.arena-home {
  max-width: 1080px;
  margin: 0 auto;
  padding: 24px 20px 96px;
}

.arena-hero {
  display: grid;
  gap: 24px;
  grid-template-columns: 1fr;
  background: radial-gradient(120% 120% at 0% 0%, #1e3a8a 0%, #0f172a 60%);
  border-radius: 24px;
  color: #fff;
  padding: 32px 28px;
}

@media (min-width: 900px) {
  .arena-hero { grid-template-columns: 1.5fr 1fr; align-items: stretch; }
}

.arena-hero__eyebrow {
  margin: 0 0 8px;
  letter-spacing: 0.16em;
  font-size: 12px;
  text-transform: uppercase;
  color: #93c5fd;
  font-weight: 700;
}

.arena-hero h1 {
  margin: 0 0 12px;
  font-size: 32px;
  line-height: 1.2;
}

.arena-hero__lead {
  margin: 0 0 20px;
  color: #cbd5e1;
  max-width: 540px;
}

.arena-hero__stats {
  display: flex;
  gap: 18px;
}

.stat { display: flex; flex-direction: column; }
.stat__value { font-size: 26px; font-weight: 800; }
.stat__label { font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; }

.daily-card {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 18px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  cursor: pointer;
  transition: transform .15s ease, border-color .15s ease;
}
.daily-card:hover { transform: translateY(-2px); border-color: rgba(255, 255, 255, 0.25); }
.daily-card--empty { cursor: default; opacity: 0.7; }

.daily-card__badge { font-size: 12px; color: #fde68a; letter-spacing: 0.06em; }
.daily-card h3 { margin: 0; font-size: 22px; }
.daily-card p { margin: 0; color: #cbd5e1; }
.daily-card__hint { font-size: 12px; color: #fbbf24; }

.btn-primary {
  align-self: flex-start;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  border: 0;
  color: #fff;
  font-weight: 700;
  padding: 10px 18px;
  border-radius: 10px;
  cursor: pointer;
  margin-top: 4px;
}

.admin-banner {
  margin-top: 16px;
  background: #fef3c7;
  color: #92400e;
  border-radius: 12px;
  padding: 10px 14px;
  font-weight: 600;
  font-size: 14px;
}

.arena-section { margin-top: 36px; }
.arena-section__head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 14px;
}
.arena-section h2 { margin: 0; color: #0f172a; }
.link-forge { color: #2563eb; font-weight: 700; text-decoration: none; }

.arena-grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
}

.chapter-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 18px;
  padding: 20px;
  cursor: pointer;
  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
  border-top: 4px solid var(--accent, #2563eb);
}
.chapter-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  border-color: var(--accent, #2563eb);
}
.chapter-card__icon { font-size: 28px; }
.chapter-card h3 { margin: 8px 0 4px; color: #0f172a; }
.chapter-card p { margin: 0 0 14px; color: #64748b; min-height: 36px; }
.chapter-card__footer { display: flex; justify-content: space-between; align-items: center; }
.chapter-card__count { font-size: 12px; color: #94a3b8; }
.badge {
  font-size: 11px;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 999px;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  color: #fff;
}
.badge--free { background: #ecfdf5; color: #059669; }
</style>
