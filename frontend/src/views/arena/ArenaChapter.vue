<template>
  <div class="arena-chapter">
    <ArenaCtaModal />
    <button class="back" @click="back">← Retour</button>

    <header v-if="chapter" class="chapter-head" :style="{ '--accent': chapter.color || '#2563eb' }">
      <div class="chapter-head__icon">{{ chapter.icon || '📘' }}</div>
      <div>
        <p class="chapter-head__eyebrow">Chapitre</p>
        <h1>{{ chapter.title }}</h1>
        <p>{{ chapter.description }}</p>
      </div>
    </header>

    <ul class="levels" v-if="chapter">
      <li v-for="level in chapter.levels" :key="level.id" class="level"
          :class="{ 'level--locked': level.locked }">
        <div class="level__order">{{ level.order }}</div>
        <div class="level__body">
          <h3>{{ level.title }}</h3>
          <p>
            <span :class="['pill', `pill--${level.difficulty}`]">{{ difficultyLabel(level.difficulty) }}</span>
            · {{ level.questions_count }} questions
            · ⏱ {{ level.time_limit_sec }}s
            · ⭐ {{ level.xp_reward }} XP
          </p>
        </div>
        <button class="level__cta" @click="play(level)">
          <template v-if="level.locked">🔒 Débloquer</template>
          <template v-else>Jouer</template>
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArenaStore } from '@/stores/arena'
import ArenaCtaModal from '@/components/arena/ArenaCtaModal.vue'

const route = useRoute()
const router = useRouter()
const arena = useArenaStore()

const chapter = computed(() => arena.currentChapter)

async function load() {
  if (route.params.slug) {
    await arena.loadChapter(route.params.slug)
  }
}

onMounted(load)
watch(() => route.params.slug, load)

function back() { router.push('/jeu') }

function play(level) {
  if (level.locked) {
    arena.showCta({
      id: 'unlock_level',
      title: 'Niveau réservé aux abonnés',
      body: "Continuez votre progression avec OptiTAB+ et débloquez tous les niveaux.",
      cta: "Découvrir l'offre",
      route: '/tarifs',
      trigger: 'level_locked',
    })
    arena.track('cta_displayed', { id: 'unlock_level', trigger: 'level_locked', level_id: level.id })
    return
  }
  router.push(`/jeu/jouer/${level.id}`)
}

function difficultyLabel(d) {
  return ({ easy: 'Facile', medium: 'Moyen', hard: 'Difficile', elite: 'Élite' })[d] || d
}
</script>

<style scoped>
.arena-chapter { max-width: 880px; margin: 0 auto; padding: 24px 20px 96px; }
.back {
  background: transparent; border: 0; color: #2563eb; font-weight: 700;
  cursor: pointer; padding: 0 0 16px; font-size: 14px;
}

.chapter-head {
  display: flex; gap: 18px; align-items: center;
  background: #fff;
  border-left: 6px solid var(--accent, #2563eb);
  border-radius: 18px;
  padding: 22px;
  box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
  margin-bottom: 22px;
}
.chapter-head__icon { font-size: 38px; }
.chapter-head__eyebrow { color: #2563eb; font-weight: 700; text-transform: uppercase; font-size: 12px; letter-spacing: 0.08em; margin: 0; }
.chapter-head h1 { margin: 4px 0; color: #0f172a; }
.chapter-head p { margin: 0; color: #64748b; }

.levels { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 12px; }

.level {
  display: flex; align-items: center; gap: 16px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 16px 18px;
  transition: border-color .15s ease, transform .15s ease;
}
.level:hover { border-color: #2563eb; transform: translateY(-1px); }
.level--locked { opacity: 0.7; }

.level__order {
  width: 38px; height: 38px; border-radius: 50%;
  background: #eff6ff; color: #2563eb;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800;
}
.level__body { flex: 1; }
.level__body h3 { margin: 0 0 4px; color: #0f172a; }
.level__body p { margin: 0; color: #64748b; font-size: 13px; }

.pill {
  display: inline-block; font-size: 11px; font-weight: 700; padding: 2px 8px;
  border-radius: 999px; margin-right: 6px;
}
.pill--easy   { background: #ecfdf5; color: #059669; }
.pill--medium { background: #eff6ff; color: #2563eb; }
.pill--hard   { background: #fef3c7; color: #b45309; }
.pill--elite  { background: linear-gradient(135deg, #fde68a, #f59e0b); color: #78350f; }

.level__cta {
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  color: #fff; border: 0; padding: 10px 16px; border-radius: 10px; font-weight: 700; cursor: pointer;
}
</style>
