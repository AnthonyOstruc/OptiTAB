<template>
  <div class="review-card">
    <div class="review-header">
      <div class="review-title">À réviser aujourd'hui</div>
      <div class="review-meta">{{ dueItems.length }} à faire</div>
    </div>
    <div v-if="dueItems.length === 0" class="empty">Rien à réviser pour l'instant 🎉</div>
    <ul v-else class="review-list">
      <li v-for="it in dueItems" :key="it.exerciceId" class="review-item">
        <div class="review-left">
          <div class="review-ex-title">{{ it.exTitle }}</div>
          <div class="review-ex-meta">{{ it.chapitreTitle }}</div>
        </div>
        <button class="review-btn" @click="openChapter(it.chapitreId)">Réviser</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  statuses: { type: Array, default: () => [] },
  exercices: { type: Array, default: () => [] },
  chapitres: { type: Array, default: () => [] }
})

const router = useRouter()

function toDateKey(iso) {
  if (!iso) return null
  const d = new Date(iso)
  const yyyy = d.getFullYear()
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  return `${yyyy}-${mm}-${dd}`
}

function intervalForAttempts(n) {
  if (n <= 1) return 1
  if (n === 2) return 3
  if (n === 3) return 7
  return 14
}

const exercicesIndex = computed(() => Object.fromEntries((props.exercices || []).map(e => [e.id, e])))
const chapitresIndex = computed(() => Object.fromEntries((props.chapitres || []).map(c => [c.id, c])))

const byExercise = computed(() => {
  const map = {}
  for (const s of props.statuses || []) {
    const exId = s.exercice
    if (!exId) continue
    if (!map[exId]) map[exId] = { attempts: 0, lastDate: null, lastCorrect: null, incorrectDates: [] }
    map[exId].attempts += 1
    const d = new Date(s.date_creation || s.created_at || Date.now())
    if (!map[exId].lastDate || d > map[exId].lastDate) {
      map[exId].lastDate = d
      map[exId].lastCorrect = !!s.est_correct
    }
    if (s.est_correct === false) map[exId].incorrectDates.push(d)
  }
  return map
})

const dueItems = computed(() => {
  const today = new Date()
  const results = []
  for (const [exIdStr, meta] of Object.entries(byExercise.value)) {
    const exId = Number(exIdStr)
    const ex = exercicesIndex.value[exId]
    if (!ex) continue
    const chapterId = ex.chapitre
    const chapter = chapitresIndex.value[chapterId]
    const exTitle = ex.titre || ex.nom || `Exercice ${ex.id}`
    const chapitreTitle = chapter ? (chapter.nom || chapter.titre || `Chapitre ${chapter.id}`) : 'Chapitre'

    // si dernier statut correct, pas prioritaire de révision
    if (meta.lastCorrect === true) continue

    // si jamais tenté -> pas dans statuses (byExercise le filtrera)
    const attempts = meta.attempts
    const intervalDays = intervalForAttempts(attempts)
    const lastIncorrect = meta.incorrectDates.sort((a,b) => b - a)[0] || meta.lastDate
    const nextDate = new Date(lastIncorrect)
    nextDate.setDate(nextDate.getDate() + intervalDays)
    if (toDateKey(nextDate.toISOString()) <= toDateKey(today.toISOString())) {
      results.push({
        exerciceId: exId,
        exTitle,
        chapitreId: chapterId,
        chapitreTitle,
        priority: intervalDays
      })
    }
  }
  // tri par priorité (plus petit intervalle = plus urgent), puis par id
  return results.sort((a, b) => (a.priority - b.priority) || (a.exerciceId - b.exerciceId)).slice(0, 8)
})

function openChapter(chapitreId) {
  if (!chapitreId) return
  router.push({ name: 'Exercices', params: { chapitreId: String(chapitreId) } })
}
</script>

<style scoped>
.review-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  box-shadow: 0 2px 6px rgba(30,41,59,0.06);
}
.review-header { display:flex; align-items:center; justify-content:space-between; }
.review-title { font-weight:800; color:#1f2937; }
.review-meta { font-weight:700; color:#2563eb; }
.empty { color:#64748b; font-size:.95rem; margin-top:.5rem; }
.review-list { list-style:none; margin: .5rem 0 0 0; padding:0; display:flex; flex-direction:column; gap:.5rem; }
.review-item { display:flex; align-items:center; gap:.75rem; border:1px solid #e5e7eb; border-radius:10px; padding:.5rem .75rem; }
.review-left { flex:1; }
.review-ex-title { font-weight:700; color:#111827; }
.review-ex-meta { color:#64748b; font-size:.9rem; }
.review-btn { background:#16a34a; color:#fff; border:none; border-radius:8px; padding:.4rem .75rem; font-weight:700; cursor:pointer; }
.review-btn:hover { background:#15803d; }
</style>


