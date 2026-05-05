<template>
  <div class="arena-play">
    <ArenaCtaModal />

    <header class="play-head" v-if="level">
      <button class="back" @click="quit">← Quitter</button>
      <div class="play-head__title">
        <p class="eyebrow">Niveau {{ level.order }}</p>
        <h2>{{ level.title }}</h2>
      </div>
      <div class="play-head__timer" :class="{ 'play-head__timer--low': remaining <= 15 }">
        ⏱ {{ remainingDisplay }}
      </div>
    </header>

    <div v-if="!finished && currentQuestion" class="play-card">
      <p class="play-card__progress">
        Question {{ index + 1 }} / {{ questions.length }}
      </p>
      <ArenaPrompt :text="currentQuestion.prompt" />

      <div class="choices" v-if="currentQuestion.type === 'mcq'">
        <button v-for="(choice, i) in currentQuestion.choices" :key="i"
                class="choice"
                :class="{ 'choice--selected': selected[currentQuestion.id] === i }"
                @click="select(i)">
          <span class="choice__letter">{{ String.fromCharCode(65 + i) }}</span>
          <ArenaPrompt :text="String(choice)" />
        </button>
      </div>

      <input v-else
             v-model="numericAnswers[currentQuestion.id]"
             class="numeric-input"
             type="text"
             placeholder="Votre réponse" />

      <div class="play-actions">
        <button class="ghost" v-if="canHint" @click="useHint">💡 Indice</button>
        <button class="primary" @click="next">{{ index + 1 === questions.length ? 'Terminer' : 'Question suivante' }}</button>
      </div>
      <p v-if="hintShown" class="hint">{{ currentQuestion.hint || 'Aucun indice disponible.' }}</p>
    </div>

    <section v-if="finished && result" class="result">
      <div class="result__icon" :class="{ pass: result.passed, fail: !result.passed }">
        {{ result.passed ? '🎉' : '💪' }}
      </div>
      <h2>{{ result.passed ? 'Niveau réussi !' : 'Essayez à nouveau' }}</h2>
      <p class="result__score">{{ result.score }} / {{ result.max_score }} · précision {{ Math.round(result.accuracy * 100) }}%</p>
      <p class="result__xp">+ {{ result.xp_awarded }} XP · série {{ result.streak }} 🔥</p>

      <ol class="recap" v-if="result.answer_results?.length">
        <li v-for="(q, i) in questions" :key="q.id" class="recap__item"
            :class="{ 'recap__item--ok': resultMap[q.id]?.is_correct, 'recap__item--ko': resultMap[q.id] && !resultMap[q.id].is_correct }">
          <div class="recap__head">
            <span class="recap__index">Q{{ i + 1 }}</span>
            <span class="recap__verdict">{{ resultMap[q.id]?.is_correct ? '✓ Correct' : '✗ À revoir' }}</span>
          </div>
          <ArenaPrompt :text="q.prompt" />
          <p class="recap__answers">
            <span class="recap__label">Votre réponse :</span>
            <ArenaPrompt :text="userAnswerLabel(q)" />
          </p>
          <p v-if="!resultMap[q.id]?.is_correct" class="recap__answers recap__answers--correct">
            <span class="recap__label">Bonne réponse :</span>
            <ArenaPrompt :text="correctAnswerLabel(q, resultMap[q.id])" />
          </p>
          <div v-if="q.explanation" class="recap__explanation">
            <ArenaPrompt :text="q.explanation" />
          </div>
        </li>
      </ol>

      <div class="result__actions">
        <button class="ghost" @click="quit">Retour</button>
        <button class="primary" @click="replay">Rejouer</button>
      </div>

      <div v-if="result.ctas?.length" class="result__cta">
        <h3>{{ result.ctas[0].title }}</h3>
        <p>{{ result.ctas[0].body }}</p>
        <button class="primary" @click="openCta(result.ctas[0])">{{ result.ctas[0].cta }}</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, onBeforeUnmount, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArenaStore } from '@/stores/arena'
import ArenaCtaModal from '@/components/arena/ArenaCtaModal.vue'
import ArenaPrompt from '@/components/arena/ArenaPrompt.vue'

const route = useRoute()
const router = useRouter()
const arena = useArenaStore()

const level = computed(() => arena.currentLevel)
const questions = computed(() => arena.currentQuestions)

const index = ref(0)
const selected = ref({})
const numericAnswers = ref({})
const startedAt = ref(Date.now())
const remaining = ref(0)
const timer = ref(null)
const hintShown = ref(false)
const finished = ref(false)
const result = ref(null)

const currentQuestion = computed(() => questions.value[index.value])
const canHint = computed(() => arena.isPremium && !hintShown.value && currentQuestion.value?.hint)
const isDaily = computed(() => route.query.daily === '1')

const remainingDisplay = computed(() => {
  const m = Math.floor(Math.max(0, remaining.value) / 60).toString().padStart(2, '0')
  const s = (Math.max(0, remaining.value) % 60).toString().padStart(2, '0')
  return `${m}:${s}`
})

const resultMap = computed(() => {
  const out = {}
  for (const r of (result.value?.answer_results || [])) {
    out[r.question_id] = r
  }
  return out
})

function userAnswerLabel(q) {
  if (q.type === 'mcq') {
    const i = selected.value[q.id]
    if (i === undefined || i === null) return '—'
    const letter = String.fromCharCode(65 + i)
    return `${letter}. ${q.choices?.[i] ?? ''}`
  }
  const v = numericAnswers.value[q.id]
  return (v === undefined || v === null || v === '') ? '—' : String(v)
}

function correctAnswerLabel(q, r) {
  const c = r?.correct_answer
  if (c === undefined || c === null) return ''
  if (q.type === 'mcq' && Array.isArray(c)) {
    return c.map((i) => `${String.fromCharCode(65 + i)}. ${q.choices?.[i] ?? ''}`).join(', ')
  }
  if (q.type === 'numeric' && typeof c === 'object') {
    return String(c.value ?? '')
  }
  return String(c)
}

async function load() {
  hintShown.value = false
  finished.value = false
  result.value = null
  selected.value = {}
  numericAnswers.value = {}
  index.value = 0
  try {
    await arena.loadLevel(Number(route.params.levelId))
  } catch (_) {
    // The store has already pushed the appropriate CTA modal (e.g. paywall).
    // Send the user back to the home so they aren't stranded on a blank page.
    router.replace('/jeu')
    return
  }
  startedAt.value = Date.now()
  remaining.value = level.value?.time_limit_sec || 90
  timer.value = setInterval(tick, 1000)
}

onMounted(load)
onBeforeUnmount(() => { if (timer.value) clearInterval(timer.value) })

function tick() {
  remaining.value -= 1
  if (remaining.value <= 0) {
    clearInterval(timer.value)
    submit()
  }
}

function select(i) {
  if (!currentQuestion.value) return
  selected.value[currentQuestion.value.id] = i
}

function next() {
  if (index.value < questions.value.length - 1) {
    index.value += 1
    hintShown.value = false
  } else {
    submit()
  }
}

function useHint() {
  hintShown.value = true
  arena.track('hint_used', { question_id: currentQuestion.value?.id })
}

async function submit() {
  if (timer.value) clearInterval(timer.value)
  const answers = questions.value.map((q) => {
    if (q.type === 'mcq') {
      const value = selected.value[q.id]
      return {
        question_id: q.id,
        answer: value === undefined ? { value: [] } : { value: [value] },
        time_ms: 0,
      }
    }
    return {
      question_id: q.id,
      answer: { value: numericAnswers.value[q.id] },
      time_ms: 0,
    }
  })
  const duration = Math.round((Date.now() - startedAt.value) / 1000)
  const data = await arena.submitAttempt(Number(route.params.levelId), {
    answers, duration_sec: duration,
    used_hint: hintShown.value, is_daily: isDaily.value,
  })
  result.value = data
  finished.value = true
}

function quit() { router.push('/jeu') }
function replay() { load() }

function openCta(cta) {
  arena.track('cta_clicked', { id: cta.id, trigger: cta.trigger })
  router.push(cta.route || '/tarifs')
}
</script>

<style scoped>
.arena-play { max-width: 720px; margin: 0 auto; padding: 24px 20px 96px; }

.play-head { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 20px; }
.back { background: transparent; border: 0; color: #2563eb; font-weight: 700; cursor: pointer; }
.play-head__title { flex: 1; }
.play-head__title .eyebrow { color: #94a3b8; font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin: 0; }
.play-head__title h2 { margin: 2px 0 0; color: #0f172a; }
.play-head__timer {
  background: #f1f5f9; padding: 6px 12px; border-radius: 999px;
  font-weight: 800; color: #0f172a;
}
.play-head__timer--low { background: #fee2e2; color: #b91c1c; }

.play-card {
  background: #fff;
  border-radius: 18px;
  padding: 24px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
}
.play-card__progress { margin: 0 0 8px; color: #94a3b8; font-size: 12px; letter-spacing: 0.1em; text-transform: uppercase; }

.choices { display: grid; gap: 10px; margin-top: 20px; }
.choice {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 16px;
  background: #fff;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  cursor: pointer;
  text-align: left;
  font-size: 16px;
  transition: border-color .15s ease, background .15s ease;
}
.choice:hover { border-color: #2563eb; }
.choice--selected { border-color: #2563eb; background: #eff6ff; }
.choice__letter {
  width: 28px; height: 28px; border-radius: 50%; background: #eff6ff;
  color: #2563eb; font-weight: 800; display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

.numeric-input {
  width: 100%;
  margin-top: 16px;
  padding: 12px 14px;
  border-radius: 12px;
  border: 1.5px solid #e2e8f0;
  font-size: 16px;
}
.numeric-input:focus { border-color: #2563eb; outline: none; }

.play-actions { display: flex; gap: 12px; justify-content: flex-end; margin-top: 22px; }
.ghost { background: transparent; border: 1px solid #e2e8f0; padding: 10px 14px; border-radius: 10px; cursor: pointer; font-weight: 600; color: #475569; }
.primary {
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  color: #fff; border: 0; padding: 10px 18px; border-radius: 10px; font-weight: 700; cursor: pointer;
}
.hint { margin-top: 14px; padding: 10px 12px; background: #fef9c3; border-radius: 10px; color: #854d0e; }

.result {
  background: #fff;
  border-radius: 18px;
  padding: 32px 24px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
}
.result__icon { font-size: 56px; }
.result h2 { margin: 8px 0; color: #0f172a; }
.result__score { color: #64748b; }
.result__xp { color: #2563eb; font-weight: 700; }
.result__actions { display: flex; gap: 12px; justify-content: center; margin-top: 20px; }

.result__cta {
  margin-top: 28px;
  padding: 22px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(124, 58, 237, 0.12));
  text-align: left;
}
.result__cta h3 { margin: 0 0 6px; color: #0f172a; }
.result__cta p { margin: 0 0 12px; color: #475569; }

.recap {
  list-style: none;
  padding: 0;
  margin: 28px 0 8px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  text-align: left;
}
.recap__item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-left: 4px solid #cbd5e1;
  border-radius: 12px;
  padding: 14px 16px;
}
.recap__item--ok { border-left-color: #10b981; background: #ecfdf5; }
.recap__item--ko { border-left-color: #ef4444; background: #fef2f2; }
.recap__head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.04em;
}
.recap__index { color: #64748b; text-transform: uppercase; }
.recap__verdict { color: #0f172a; }
.recap__item--ok .recap__verdict { color: #047857; }
.recap__item--ko .recap__verdict { color: #b91c1c; }
.recap__answers {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  align-items: baseline;
  margin: 8px 0 0;
  font-size: 14px;
  color: #475569;
}
.recap__answers--correct { color: #047857; font-weight: 600; }
.recap__label { font-weight: 700; color: #334155; }
.recap__explanation {
  margin-top: 10px;
  padding: 10px 12px;
  background: #fff;
  border-radius: 8px;
  border: 1px dashed #cbd5e1;
  font-size: 14px;
  color: #334155;
}
</style>
