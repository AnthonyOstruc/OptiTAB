<template>
  <section class="batch-panel" aria-label="Reel +, création en série">
    <header class="batch-header">
      <div>
        <span class="batch-eyebrow">REEL + · CRÉATION EN SÉRIE</span>
        <h2>Préparez jusqu’à 30 reels à la fois</h2>
        <p>Un onglet par reel. Les mêmes outils d’édition, avec une génération à la suite.</p>
      </div>
      <button class="batch-secondary" type="button" :disabled="busy" @click="importOpen = !importOpen">
        {{ importOpen ? 'Fermer l’import' : '+ Nouvelle série' }}
      </button>
    </header>

    <form v-if="importOpen || !batches.length" class="batch-import" @submit.prevent="submit">
      <label class="batch-label">
        Nom de la série
        <input v-model="title" maxlength="255" placeholder="Ex. Octobre — Terminale" :disabled="busy" required />
      </label>
      <label class="batch-label">
        Tous vos scripts
        <span class="batch-help">Gardez le format habituel et ajoutez simplement REEL: suivi du nom avant chaque script.</span>
        <textarea v-model="source" rows="12" spellcheck="false" :placeholder="example" :disabled="busy" required />
      </label>
      <div class="batch-import-footer">
        <button class="batch-link" type="button" :disabled="busy" @click="copyExample">{{ exampleCopied ? 'Exemple copié' : 'Copier un exemple' }}</button>
        <span :class="{ 'batch-error-text': parsed.projects.length > 30 }">{{ parsed.projects.length }} / 30 reels détectés</span>
      </div>
      <ul v-if="source.trim() && parsed.errors.length" class="batch-errors" role="alert">
        <li v-for="error in parsed.errors" :key="error">{{ error }}</li>
      </ul>
      <div v-else-if="parsed.projects.length" class="batch-import-preview" aria-label="Reels à importer">
        <span v-for="(project, index) in parsed.projects" :key="index">{{ index + 1 }}. {{ project.title }}</span>
      </div>
      <button class="batch-primary" type="submit" :disabled="busy || !title.trim() || !!parsed.errors.length">
        {{ importing ? 'Création de la série…' : `Créer les ${parsed.projects.length || ''} reels` }}
      </button>
      <p v-if="importError" class="batch-error-text" role="alert">{{ importError }}</p>
    </form>

    <template v-if="batches.length">
      <div class="batch-series-row">
        <label class="batch-label">
          Série enregistrée
          <select :value="activeBatchId" :disabled="busy" @change="$emit('select-batch', $event.target.value)">
            <option v-for="batch in batches" :key="batch.id" :value="batch.id">{{ batch.title }} · {{ batch.projects.length }} reels</option>
          </select>
        </label>
        <div class="batch-stats"><strong>{{ projects.length }}</strong> reels <span>·</span> {{ voicesReady }} voix prêtes <span>·</span> {{ videosReady }} vidéos prêtes</div>
      </div>

      <div class="batch-actions">
        <button class="batch-primary" type="button" :disabled="busy || !projects.length || !voiceReady" @click="$emit('run', 'speech')">
          Créer toutes les voix
        </button>
        <button class="batch-video" type="button" :disabled="busy || !projects.length" @click="$emit('run', 'video')">
          Créer et télécharger les vidéos
        </button>
        <label class="batch-check"><input v-model="skipReady" type="checkbox" :disabled="busy" /> Reprendre uniquement les reels restants</label>
      </div>
      <p class="batch-help">Voix : {{ voiceLabel || 'sélectionnez une voix dans l’éditeur ci-dessous' }}. Les réglages choisis s’appliquent à toute la série.</p>
      <p class="batch-help">Gardez cette page ouverte pendant la génération. Chaque MP4 est téléchargé dès qu’il est prêt ; autorisez les téléchargements multiples si le navigateur le demande.</p>

      <div v-if="queue.phase" class="batch-progress" aria-live="polite">
        <div class="batch-progress-heading">
          <strong>{{ queue.running ? (queue.phase === 'speech' ? 'Génération des voix' : 'Création des vidéos') : queue.message }}</strong>
          <span>{{ queue.completed }} / {{ queue.total }}</span>
        </div>
        <progress :value="queue.completed" :max="queue.total || 1" aria-label="Progression de la série"></progress>
        <div class="batch-progress-heading">
          <span>{{ queue.running ? queue.currentTitle : 'Les reels terminés sont conservés.' }}</span>
          <button v-if="queue.running" class="batch-secondary" type="button" :disabled="queue.stopRequested" @click="$emit('stop')">
            {{ queue.stopRequested ? 'Arrêt après ce reel…' : 'Arrêter après ce reel' }}
          </button>
        </div>
      </div>

      <div class="batch-tabs" role="tablist" aria-label="Reels de la série">
        <button v-for="(project, index) in projects" :id="`batch-tab-${project.id}`" :key="project.id" type="button" role="tab"
          :aria-selected="Number(selectedProjectId) === Number(project.id)" aria-controls="batch-reel-editor"
          :tabindex="Number(selectedProjectId) === Number(project.id) || (!selectedProjectId && index === 0) ? 0 : -1"
          :class="['batch-tab', { 'batch-tab--active': Number(selectedProjectId) === Number(project.id) }]"
          :disabled="busy" @click="$emit('select-project', project.id)" @keydown="onTabKeydown($event, index)">
          <span class="batch-tab-number">{{ index + 1 }}</span>
          <span>{{ project.title }}</span>
          <span v-if="statusFor(project)" :class="['batch-dot', `batch-dot--${statusFor(project)}`]" :title="statusLabel(project)"></span>
        </button>
      </div>

      <details class="batch-tracking">
        <summary>Suivi des reels <span>{{ voicesReady }} voix prêtes · {{ videosReady }} vidéos prêtes</span></summary>
        <div class="batch-tracking-table">
        <table>
          <caption class="batch-sr-only">Suivi de la série</caption>
          <thead><tr><th scope="col">Reel</th><th scope="col">Voix</th><th scope="col">Vidéo</th><th scope="col">Suivi</th><th scope="col"><span class="batch-sr-only">Actions</span></th></tr></thead>
          <tbody>
            <tr v-for="project in projects" :key="project.id">
              <th scope="row"><button type="button" class="batch-link" :disabled="busy" @click="$emit('select-project', project.id)">{{ project.title }}</button></th>
              <td><span :class="['batch-badge', { 'batch-badge--ready': project.speech_status === 'ready' }]">{{ project.speech_status === 'ready' ? 'Prête' : 'À générer' }}</span></td>
              <td><span :class="['batch-badge', { 'batch-badge--ready': project.video_status === 'ready' }]">{{ project.video_status === 'ready' ? 'Prête' : 'À générer' }}</span></td>
              <td :class="{ 'batch-error-text': statusFor(project) === 'error' }">{{ statusLabel(project) }}</td>
              <td><button v-if="project.video_status === 'ready'" type="button" class="batch-link" :disabled="busy" @click="$emit('download', project)">Télécharger MP4</button></td>
            </tr>
          </tbody>
        </table>
        </div>
      </details>
    </template>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'
import { parseReelBatch } from './reelBatch'

const props = defineProps({
  batches: { type: Array, default: () => [] },
  projects: { type: Array, default: () => [] },
  activeBatchId: { type: String, default: '' },
  selectedProjectId: { type: Number, default: null },
  busy: Boolean,
  importing: Boolean,
  voiceReady: Boolean,
  voiceLabel: { type: String, default: '' },
  queue: { type: Object, required: true },
})
const emit = defineEmits(['import', 'select-batch', 'select-project', 'run', 'stop', 'download'])
const title = ref('')
const source = ref('')
const importOpen = ref(false)
const importError = ref('')
const exampleCopied = ref(false)
const skipReady = defineModel('skipReady', { type: Boolean, default: true })
const parsed = computed(() => parseReelBatch(source.value))
const voicesReady = computed(() => props.projects.filter(p => p.speech_status === 'ready').length)
const videosReady = computed(() => props.projects.filter(p => p.video_status === 'ready').length)
const example = `REEL: 1 oct
SLIDE 1 | hook
TITLE: Le défi du jour
TEXT: Combien vaut ce carré ?
VOICE: Combien vaut le carré de trois ?
---
SLIDE 2 | result
KATEX: 3^2 = 9
VOICE: Trois au carré égale neuf.

REEL: 2 oct
SLIDE 1 | hook
TITLE: À vous de jouer
TEXT: Un nouveau défi !
VOICE: Combien vaut le carré de quatre ?
---
SLIDE 2 | result
KATEX: 4^2 = 16
VOICE: Quatre au carré égale seize.`

let importId = ''
let importSignature = ''
function submit() {
  if (props.busy || parsed.value.errors.length || !title.value.trim()) return
  importError.value = ''
  const signature = JSON.stringify([title.value.trim(), parsed.value.projects])
  if (signature !== importSignature) {
    importId = crypto.randomUUID()
    importSignature = signature
  }
  emit('import', { batch_id: importId, title: title.value.trim(), projects: parsed.value.projects }, (error) => {
    if (error) { importError.value = error; return }
    title.value = ''
    source.value = ''
    importSignature = ''
    importOpen.value = false
  })
}
async function copyExample() {
  try { await navigator.clipboard.writeText(example); exampleCopied.value = true }
  catch { importError.value = 'Copie indisponible. Utilisez le modèle affiché dans le champ.' }
}
function statusFor(project) { return props.queue.results[project.id]?.status || '' }
function statusLabel(project) { return props.queue.results[project.id]?.message || '—' }
function onTabKeydown(event, index) {
  if (props.busy) return
  const count = props.projects.length
  const targets = { ArrowRight: (index + 1) % count, ArrowLeft: (index + count - 1) % count, Home: 0, End: count - 1 }
  if (!(event.key in targets)) return
  event.preventDefault()
  const project = props.projects[targets[event.key]]
  document.getElementById(`batch-tab-${project.id}`)?.focus()
  emit('select-project', project.id)
}
</script>

<style scoped>
.batch-panel { padding: 24px; border: 1px solid #dbe4f0; border-radius: 16px; background: #fff; display: grid; gap: 20px; min-width: 0; }
.batch-header, .batch-series-row, .batch-import-footer, .batch-progress-heading { display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
.batch-eyebrow { color: #3155ca; font-size: 11px; font-weight: 800; letter-spacing: .09em; }
h2 { margin: 8px 0; color: #172b50; font-size: 23px; }
p { margin: 0; color: #64748b; font-size: 14px; line-height: 1.6; }
.batch-import { display: grid; gap: 16px; padding: 20px; border-radius: 12px; border: 1px solid #dce6f5; background: #f8faff; }
.batch-label { display: grid; gap: 8px; color: #334155; font-size: 13px; font-weight: 700; }
.batch-label input, .batch-label select, textarea { width: 100%; box-sizing: border-box; border: 1px solid #cbd5e1; border-radius: 8px; background: #fff; padding: 11px 12px; color: #0f172a; font: inherit; }
.batch-series-row .batch-label { flex: 1; max-width: 480px; min-width: 200px; }
textarea { resize: vertical; font: 13px/1.65 ui-monospace, monospace; min-height: 160px; }
.batch-help { font-size: 12px; font-weight: 400; color: #64748b; line-height: 1.6; }
button { cursor: pointer; font: inherit; }
button:disabled { cursor: not-allowed; opacity: .5; }
button:focus-visible, input:focus-visible, select:focus-visible, textarea:focus-visible { outline: 3px solid #93b4ff; outline-offset: 2px; }
.batch-primary, .batch-secondary, .batch-video { border: 1px solid transparent; border-radius: 8px; padding: 11px 16px; font-size: 13px; font-weight: 700; }
.batch-primary { background: #3155ca; color: #fff; }
.batch-video { background: #7053c7; color: #fff; }
.batch-secondary { background: #fff; border-color: #d4deed; color: #334155; }
.batch-import > .batch-primary { justify-self: start; }
.batch-link { background: none; border: 0; padding: 0; color: #3155ca; font-size: 13px; text-align: left; font-weight: 600; }
.batch-import-footer { color: #64748b; font-size: 12px; }
.batch-import-preview { display: flex; flex-wrap: wrap; gap: 6px; }
.batch-import-preview span { background: #eaf0ff; color: #3155ca; padding: 5px 9px; border-radius: 6px; font-size: 12px; }
.batch-errors, .batch-error-text { color: #b42335 !important; font-size: 13px; }
.batch-errors { margin: 0; padding-left: 20px; }
.batch-stats { font-size: 13px; color: #64748b; }
.batch-stats strong { color: #172b50; font-size: 22px; }
.batch-stats span { padding: 0 8px; color: #cbd5e1; }
.batch-actions { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.batch-check { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #64748b; }
.batch-progress { background: #f1f6ff; border: 1px solid #d8e5ff; border-radius: 10px; padding: 16px; display: grid; gap: 12px; font-size: 13px; color: #25458d; }
progress { width: 100%; height: 8px; accent-color: #3155ca; }
.batch-tabs { display: flex; gap: 8px; overflow-x: auto; padding: 3px 3px 12px; }
.batch-tab { flex-shrink: 0; display: flex; align-items: center; gap: 9px; border: 1px solid #dbe4ef; border-radius: 9px; background: #fff; color: #475569; padding: 10px 14px; font-size: 13px; font-weight: 600; }
.batch-tab--active { border-color: #3155ca; background: #edf2ff; color: #2549bc; box-shadow: 0 0 0 1px #3155ca; }
.batch-tab-number { background: #e8edf4; color: #526581; border-radius: 5px; padding: 2px 5px; font-size: 11px; }
.batch-dot { width: 7px; height: 7px; border-radius: 50%; background: #94a3b8; }
.batch-dot--success { background: #16a078; }.batch-dot--error { background: #dc3545; }.batch-dot--running { background: #3155ca; }
.batch-tracking summary { cursor: pointer; color: #334155; font-size: 13px; font-weight: 700; padding: 10px 0; }
.batch-tracking summary span { font-size: 12px; color: #64748b; font-weight: 400; margin-left: 12px; }
.batch-tracking-table { overflow: auto; max-height: 340px; margin-top: 10px; }
table { width: 100%; border-collapse: collapse; text-align: left; font-size: 12px; }
caption { text-align: left; color: #334155; font-weight: 700; padding-bottom: 12px; }
th, td { border-bottom: 1px solid #edf1f6; padding: 10px 12px; color: #64748b; }
thead th { background: #f8fafc; font-weight: 600; }
td:nth-child(4) { max-width: 340px; overflow-wrap: anywhere; }
.batch-badge { white-space: nowrap; display: inline-block; padding: 4px 8px; background: #f1f5f9; color: #64748b; border-radius: 5px; }
.batch-badge--ready { background: #e8f7f0; color: #167553; }
.batch-sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); }
@media (max-width: 640px) { .batch-panel { padding: 16px; } .batch-import { padding: 12px; } h2 { font-size: 20px; } .batch-actions > button { width: 100%; } }
</style>
