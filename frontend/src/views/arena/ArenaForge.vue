<template>
  <div class="forge">
    <ArenaCtaModal />
    <button class="back" @click="$router.push('/jeu')">← Retour</button>

    <header class="forge-head">
      <p class="eyebrow">🔥 Forge des erreurs</p>
      <h1>Transformez vos erreurs en force</h1>
      <p>La Forge garde une trace des questions ratées pour vous les redonner au bon moment.</p>
    </header>

    <div v-if="!arena.forge" class="empty">Chargement...</div>

    <ul v-else-if="arena.forge.mistakes?.length" class="forge-list">
      <li v-for="m in arena.forge.mistakes" :key="m.id" class="forge-item">
        <div class="forge-item__head">
          <span class="forge-item__pill">{{ m.chapter_title }} · {{ m.level_title }}</span>
          <span class="forge-item__mastery">Maîtrise {{ m.mastery }}/3</span>
        </div>
        <ArenaPrompt :text="m.question_prompt" />
        <p class="forge-item__meta">Vu {{ m.times_wrong }}× · dernier essai {{ formatDate(m.last_seen) }}</p>
      </li>
    </ul>

    <div v-else class="empty">Aucune erreur enregistrée — bravo !</div>

    <section v-if="arena.forge?.truncated" class="forge-cta">
      <h3>{{ arena.forge.cta?.title || 'Voir toutes vos erreurs' }}</h3>
      <p>{{ arena.forge.cta?.body }}</p>
      <button class="primary" @click="goPremium">Activer OptiTAB+</button>
    </section>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useArenaStore } from '@/stores/arena'
import ArenaCtaModal from '@/components/arena/ArenaCtaModal.vue'
import ArenaPrompt from '@/components/arena/ArenaPrompt.vue'

const arena = useArenaStore()
const router = useRouter()

onMounted(() => {
  arena.loadForge()
  arena.track('forge_opened')
})

function goPremium() {
  arena.track('cta_clicked', { id: 'forge_unlimited', trigger: 'forge_truncated' })
  router.push(arena.forge?.cta?.route || '/tarifs')
}

function formatDate(iso) {
  if (!iso) return ''
  try { return new Date(iso).toLocaleDateString('fr-FR') } catch { return iso }
}
</script>

<style scoped>
.forge { max-width: 760px; margin: 0 auto; padding: 24px 20px 96px; }
.back { background: transparent; border: 0; color: #2563eb; font-weight: 700; cursor: pointer; padding-bottom: 12px; }
.forge-head { margin-bottom: 22px; }
.eyebrow { color: #d97706; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; margin: 0; font-size: 12px; }
.forge-head h1 { margin: 4px 0; color: #0f172a; }
.forge-head p { margin: 0; color: #64748b; }

.forge-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 12px; }
.forge-item {
  background: #fff; border: 1px solid #e2e8f0; border-radius: 14px;
  padding: 16px 18px;
}
.forge-item__head { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 12px; }
.forge-item__pill { background: #eff6ff; color: #2563eb; padding: 2px 8px; border-radius: 999px; font-weight: 700; }
.forge-item__mastery { color: #94a3b8; }
.forge-item__meta { color: #94a3b8; font-size: 12px; margin: 8px 0 0; }

.empty { padding: 24px; text-align: center; color: #94a3b8; }

.forge-cta {
  margin-top: 28px;
  padding: 22px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(124, 58, 237, 0.12));
}
.forge-cta h3 { margin: 0 0 6px; color: #0f172a; }
.forge-cta p { margin: 0 0 12px; color: #475569; }
.primary {
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  color: #fff; border: 0; padding: 10px 18px; border-radius: 10px; font-weight: 700; cursor: pointer;
}
</style>
