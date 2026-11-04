<template>
  <section v-if="visible" class="es-card qn" :aria-labelledby="idTitre">
    <div class="es-card__head">
      <h2 :id="idTitre" class="es-h2">{{ parent ? 'Notes aux quiz' : 'Mes quiz' }}</h2>
      <span v-if="notes.length" class="qn-moyenne" :title="`Moyenne des dernières notes sur ${notes.length} chapitre${notes.length > 1 ? 's' : ''}`">
        Moyenne <strong>{{ virgule(moyenne) }}</strong>/20
      </span>
    </div>
    <div class="es-card__body">
      <ul v-if="notes.length" class="qn-liste">
        <li v-for="c in notes.slice(0, 4)" :key="c.id">
          <component :is="parent ? 'div' : 'router-link'" :to="parent ? undefined : chapitreLink(c.id, 'quiz')" :class="['qn-ligne', { 'qn-ligne--lien': !parent }]">
            <span :class="['qn-note', `qn-note--${ton(c.quiz.derniere)}`]">
              <strong>{{ virgule(c.quiz.derniere) }}</strong><small>/20</small>
            </span>
            <span class="qn-ligne__texte">
              <strong>{{ c.titre }}</strong>
              <span>
                {{ depuis(c.quiz.quand) }}
                <template v-if="c.quiz.essais > 1"> · meilleure {{ virgule(c.quiz.meilleure) }}/20</template>
              </span>
              <span v-if="c.quiz.a_revoir?.length" class="qn-revoir" v-html="`À revoir : ${c.quiz.a_revoir.map(inline).join(', ')}`"></span>
            </span>
            <ChevronRightIcon v-if="!parent" class="qn-chev" aria-hidden="true" />
          </component>
        </li>
      </ul>

      <div v-else class="qn-vide">
        <span class="qn-vide__ico"><BoltIcon aria-hidden="true" /></span>
        <template v-if="parent">
          <strong>Pas encore de quiz</strong>
          <span>Les notes sur 20 des quiz de chapitre apparaîtront ici.</span>
        </template>
        <template v-else>
          <strong>Teste-toi en 15 minutes</strong>
          <span>Un quiz par chapitre, corrigé tout de suite, avec une note sur 20.</span>
          <router-link v-if="suggestion" :to="chapitreLink(suggestion.id, 'quiz')" class="es-btn es-btn--sm es-btn--green qn-vide__btn">
            Quiz : {{ suggestion.titre }}
          </router-link>
        </template>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, nextTick, onMounted, watch } from 'vue'
import { BoltIcon, ChevronRightIcon } from '@heroicons/vue/24/outline'
import { aUnQuiz } from '@/data/quiz'
import { chapitreLink } from '@/config/espace'
import { depuis } from '@/utils/espaceFormat'
import { renderInline } from '@/utils/optitabDoc'

// Notes des quiz de chapitre (tableau de bord élève et suivi parent) : dernière
// note de chaque chapitre, la meilleure si plusieurs passages, moyenne générale.
const props = defineProps({
  chapitres: { type: Array, default: () => [] },
  parent: { type: Boolean, default: false },
  // chapitre proposé en premier quand aucun quiz n'est encore fait
  prefere: { type: [Number, String], default: null }
})

const idTitre = `qn-${Math.random().toString(36).slice(2, 8)}`
const notes = computed(() => props.chapitres
  .filter((c) => c.quiz)
  .sort((a, b) => String(b.quiz.quand).localeCompare(String(a.quiz.quand))))
const moyenne = computed(() => notes.value.reduce((s, c) => s + c.quiz.derniere, 0) / (notes.value.length || 1))
const avecQuiz = computed(() => props.chapitres.filter((c) => aUnQuiz(c.id)))
const suggestion = computed(() => avecQuiz.value.find((c) => String(c.id) === String(props.prefere)) || avecQuiz.value[0] || null)
// Carte cachée tant qu'aucun chapitre de la classe n'a de quiz
const visible = computed(() => notes.value.length > 0 || (!props.parent && avecQuiz.value.length > 0))

const virgule = (n) => (Math.round(n * 10) / 10).toLocaleString('fr-FR', { maximumFractionDigits: 1 })
const ton = (n) => (n >= 14 ? 'ok' : n >= 10 ? 'moyen' : 'faible')
const inline = (t) => renderInline(t || '')

// Les noms de parties peuvent contenir une formule ($e^{u}$)
async function composer() {
  await nextTick()
  const mj = window.MathJax
  const el = document.getElementById(idTitre)?.closest('.qn')
  try {
    if (el && mj?.typesetPromise) await mj.typesetPromise([el])
  } catch {
    /* texte laissé tel quel */
  }
}
onMounted(composer)
watch(notes, composer)
</script>

<style scoped>
.qn-moyenne {
  font-size: 13px;
  font-weight: 600;
  color: var(--es-muted);
  white-space: nowrap;
}

.qn-moyenne strong {
  font-size: 16px;
  color: var(--es-ink);
}

.qn-liste {
  display: grid;
  gap: 6px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.qn-ligne {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 6px;
  border-radius: 12px;
  color: inherit;
  text-decoration: none;
}

.qn-ligne--lien:hover {
  background: var(--es-bg);
}

.qn-note {
  display: inline-flex;
  align-items: baseline;
  justify-content: center;
  flex-shrink: 0;
  min-width: 64px;
  padding: 8px 6px;
  border-radius: 12px;
  line-height: 1;
}

.qn-note strong {
  font-size: 18px;
  font-weight: 700;
}

.qn-note small {
  font-size: 11px;
  font-weight: 600;
  opacity: 0.8;
}

.qn-note--ok {
  background: var(--es-green-50);
  color: var(--es-green-700);
}

.qn-note--moyen {
  background: var(--es-navy-50);
  color: var(--es-navy);
}

.qn-note--faible {
  background: var(--es-orange-50);
  color: var(--es-orange-700);
}

.qn-ligne__texte {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
  font-size: 13px;
  color: var(--es-muted);
}

.qn-ligne__texte strong {
  overflow: hidden;
  font-size: 14px;
  color: var(--es-ink);
  white-space: nowrap;
  text-overflow: ellipsis;
}

.qn-revoir {
  color: var(--es-orange-700);
}

.qn-chev {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  color: var(--es-muted);
}

.qn-vide {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 6px 4px 4px;
  font-size: 13px;
  color: var(--es-muted);
  text-align: center;
}

.qn-vide strong {
  font-size: 15px;
  color: var(--es-ink);
}

.qn-vide__ico {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  margin-bottom: 6px;
  border-radius: 12px;
  background: var(--es-green-50);
  color: var(--es-green-700);
}

.qn-vide__ico svg {
  width: 22px;
  height: 22px;
}

.qn-vide__btn {
  max-width: 100%;
  margin-top: 10px;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
