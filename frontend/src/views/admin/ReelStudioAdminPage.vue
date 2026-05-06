<template>
  <main class="reel-studio-admin">
    <FormatHelp :format-template="REEL_FORMAT_TEMPLATE" :show-notes="false" :initial-show="false" />

    <header class="page-header">
      <div>
        <h1>Reel Studio OptiTAB</h1>
      </div>
    </header>

    <p v-if="feedback.text" :class="['feedback', `feedback--${feedback.type}`]">{{ feedback.text }}</p>

    <p v-if="!canManage" class="feedback feedback--error">
      Accès refusé: cette section est réservée aux utilisateurs admin/staff.
    </p>

    <section v-else class="studio-stack">
      <section class="project-panel">
        <div class="section-toolbar">
          <div>
            <h2>Gestion des reels</h2>
            <p>{{ projects.length }} reel{{ projects.length > 1 ? 's' : '' }} enregistre{{ projects.length > 1 ? 's' : '' }}</p>
          </div>
          <button class="btn-primary" type="button" @click="openCreateProjectForm">
            Nouveau reel
          </button>
        </div>

        <ReelProjectForm
          v-if="projectFormOpen"
          :loading="savingProject"
          :initial-values="projectFormInitialValues"
          :submit-label="projectFormSubmitLabel"
          :form-title="projectFormTitle"
          @submit="handleSubmitProject"
          @cancel="closeProjectForm"
        />

      </section>

      <section ref="editorSectionRef" class="content-grid">
        <section class="right-column">
          <p v-if="loadingProjectDetail" class="loading-state">Chargement du projet...</p>

          <template v-else>
            <p v-if="!selectedProject" class="empty-editor-state">
              Selectionne un reel en base ou cree un nouveau reel.
            </p>

            <ReelTemplateBuilder
              v-model:template-text="templateDraft"
              :loading="generatingTemplate"
              :saving="savingTemplate"
              :disabled="!selectedProject"
              @generate="handleGenerateFromTemplate"
              @save="handleSaveTemplate"
            />

            <ReelPreview
              :slides="selectedProject?.slides || []"
              :selected-slide-id="selectedSlideId"
              :generating-speech-slide-id="generatingSpeechSlideId"
              :exporting-video="exportingVideo"
              @select-slide="selectedSlideId = $event"
              @diagnostic="handleSlideDiagnostic"
              @update-slide="handlePatchSlide"
              @generate-slide-speech="handleGenerateSlideSpeech"
              @export-video="handleExportVideo"
            />

            <section v-if="selectedProject" class="instagram-caption-panel">
              <div class="instagram-caption-header">
                <div>
                  <h3>Description Instagram</h3>
                  <p>Texte SEO pret a copier pour publier le reel.</p>
                </div>
                <button
                  class="btn-secondary"
                  type="button"
                  :disabled="!instagramCaptionText"
                  @click="copyInstagramCaption"
                >
                  Copier Instagram
                </button>
              </div>
              <textarea
                class="instagram-caption-text"
                :value="instagramCaptionText || 'Ajoute un bloc INSTAGRAM_DESCRIPTION dans le template genere.'"
                readonly
                rows="10"
                @focus="$event.target.select()"
              ></textarea>
            </section>

            <section v-if="selectedProject" class="speech-panel">
              <div class="speech-panel-header">
                <div>
                  <h3>Voix par slide</h3>
                  <p>{{ speechStatusLabel }}</p>
                </div>

                <div class="voice-charcount" :class="{ 'voice-charcount--warn': speechCharCountWarning }">
                  <strong>{{ speechCharCount.toLocaleString('fr-FR') }}</strong>
                  <span>caracteres a generer</span>
                  <small v-if="speechCharCountWarning">{{ speechCharCountWarning }}</small>
                </div>
              </div>

              <div class="speech-controls">
                <label class="voice-select voice-select--provider">
                  Fournisseur de voix
                  <select
                    v-model="selectedProviderId"
                    :disabled="loadingVoiceOptions || generatingSpeech || generatingSpeechSlideId || testingVoice"
                    @change="onProviderChange"
                  >
                    <option v-if="loadingVoiceOptions && !providers.length" value="">Chargement...</option>
                    <option
                      v-for="provider in providers"
                      :key="provider.id"
                      :value="provider.id"
                      :disabled="!provider.configured"
                    >
                      {{ provider.label }}{{ provider.configured ? '' : ' (non configure)' }}
                    </option>
                  </select>
                  <span v-if="selectedProviderMeta">{{ selectedProviderMeta }}</span>
                </label>

                <label class="voice-select voice-select--voice">
                  Voix
                  <select
                    v-model="selectedVoiceId"
                    :disabled="loadingVoiceOptions || generatingSpeech || generatingSpeechSlideId || testingVoice || !currentProviderVoices.length"
                  >
                    <option v-if="loadingVoiceOptions" value="">Chargement...</option>
                    <option v-else-if="!currentProviderVoices.length" value="">Aucune voix trouvee</option>
                    <option
                      v-for="voice in currentProviderVoices"
                      :key="voice.voice_id"
                      :value="voice.voice_id"
                      :disabled="voice.api_usable === false"
                    >
                      {{ voiceOptionLabel(voice) }}
                    </option>
                  </select>
                  <span v-if="selectedVoiceMeta">{{ selectedVoiceMeta }}</span>
                  <span v-if="selectedVoiceWarning" class="voice-warning">{{ selectedVoiceWarning }}</span>
                  <span v-else-if="voiceOptionsError">{{ voiceOptionsError }}</span>
                </label>

                <section v-if="selectedProviderId === 'elevenlabs'" class="voice-advanced">
                  <div class="voice-advanced-header">
                    <button
                      class="voice-advanced-toggle"
                      type="button"
                      :aria-expanded="String(showElevenLabsAdvanced)"
                      @click="showElevenLabsAdvanced = !showElevenLabsAdvanced"
                    >
                      <span class="voice-advanced-arrow" :class="{ 'is-open': showElevenLabsAdvanced }">></span>
                      <span>Options avancees</span>
                    </button>
                    <button
                      v-if="showElevenLabsAdvanced"
                      class="btn-secondary"
                      type="button"
                      @click="resetElevenLabsSettings"
                    >
                      Reset
                    </button>
                  </div>

                  <div v-if="showElevenLabsAdvanced" class="voice-advanced-grid">
                    <label class="voice-advanced-field voice-advanced-field--wide">
                      Model
                      <select v-model="elevenLabsSettings.model_id">
                        <option
                          v-for="model in ELEVENLABS_MODEL_OPTIONS"
                          :key="model.value"
                          :value="model.value"
                        >
                          {{ model.label }}
                        </option>
                      </select>
                    </label>

                    <label class="voice-advanced-field">
                      Stability
                      <input v-model.number="elevenLabsSettings.stability" type="number" min="0" max="1" step="0.01" />
                    </label>

                    <label class="voice-advanced-field">
                      Similarity boost
                      <input v-model.number="elevenLabsSettings.similarity_boost" type="number" min="0" max="1" step="0.01" />
                    </label>

                    <label class="voice-advanced-field">
                      Style
                      <input v-model.number="elevenLabsSettings.style" type="number" min="0" max="1" step="0.01" />
                    </label>

                    <label class="voice-advanced-field">
                      Speed
                      <input v-model.number="elevenLabsSettings.speed" type="number" min="0.5" max="2" step="0.01" />
                    </label>

                    <label class="voice-advanced-field">
                      Language code
                      <input v-model.trim="elevenLabsSettings.language_code" type="text" maxlength="16" />
                    </label>

                    <label class="voice-advanced-field">
                      Text normalization
                      <select v-model="elevenLabsSettings.apply_text_normalization">
                        <option value="on">on</option>
                        <option value="auto">auto</option>
                        <option value="off">off</option>
                      </select>
                    </label>

                    <label class="voice-toggle">
                      <input v-model="elevenLabsSettings.use_speaker_boost" type="checkbox" />
                      <span>Use speaker boost</span>
                    </label>
                  </div>
                </section>

                <div
                  v-if="selectedProviderId === 'elevenlabs'"
                  class="voice-usage"
                  :class="{ 'voice-usage--error': !elevenLabsUsageAvailable }"
                >
                  <div class="voice-usage-header">
                    <strong>Credits ElevenLabs</strong>
                    <span v-if="elevenLabsUsageAvailable">{{ elevenLabsUsagePercentLabel }} utilises</span>
                    <span v-else>Quota indisponible</span>
                  </div>

                  <template v-if="elevenLabsUsageAvailable">
                    <div class="voice-usage-bar" aria-hidden="true">
                      <span :style="elevenLabsUsageBarStyle"></span>
                    </div>
                    <dl class="voice-usage-grid">
                      <div>
                        <dt>Consomme</dt>
                        <dd>{{ elevenLabsUsageConsumedLabel }}</dd>
                      </div>
                      <div>
                        <dt>Total</dt>
                        <dd>{{ elevenLabsUsageTotalLabel }}</dd>
                      </div>
                      <div>
                        <dt>Restant</dt>
                        <dd>{{ elevenLabsUsageRemainingLabel }}</dd>
                      </div>
                      <div>
                        <dt>Pourcentage</dt>
                        <dd>{{ elevenLabsUsagePercentLabel }}</dd>
                      </div>
                    </dl>
                    <p v-if="elevenLabsUsageResetLabel">{{ elevenLabsUsageResetLabel }}</p>
                  </template>

                  <p v-else>{{ elevenLabsUsageErrorLabel }}</p>
                </div>

                <div class="speech-actions">
                  <button
                    class="btn-secondary"
                    type="button"
                    :disabled="testingVoice || loadingVoiceOptions || !selectedVoiceId || !selectedProviderConfigured || !selectedVoiceApiUsable"
                    @click="handleTestVoice"
                    title="Genere un court extrait audio pour preecouter la voix"
                  >
                    {{ testingVoice ? 'Lecture...' : 'Tester la voix' }}
                  </button>

                  <button
                    class="btn-primary"
                    type="button"
                    :disabled="generatingSpeech || loadingVoiceOptions || !canGenerateSpeech || !selectedVoiceCanGenerate || !selectedProviderConfigured"
                    @click="handleGenerateSpeech"
                  >
                    {{ generatingSpeech ? 'Generation des MP3...' : 'Generer les MP3 slides' }}
                  </button>
                </div>
              </div>
              <audio v-if="testAudioUrl" :src="testAudioUrl" controls class="voice-test-audio" />
            </section>

            <section class="manual-editor-wrap">
              <button class="btn-secondary" type="button" @click="showManualEditor = !showManualEditor">
              {{ showManualEditor ? 'Masquer édition manuelle' : 'Afficher édition manuelle' }}
              </button>

              <ReelSlideEditor
                v-if="showManualEditor"
                :slide="selectedSlide"
                :saving="savingSlide"
                @save="handleSaveSlide"
                @delete="handleDeleteSlide"
              />
            </section>
          </template>
        </section>
      </section>

      <section class="project-panel project-panel--list">
        <ReelProjectsList
          :projects="projects"
          :selected-project-id="selectedProjectId"
          :loading="loadingProjects"
          @select="selectProject"
          @edit="openEditProjectForm"
          @delete="handleDeleteProject"
        />
      </section>
    </section>
  </main>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import {
  createReelProject,
  deleteReelProject,
  deleteReelSlide,
  downloadReelVideo,
  exportReelVideo,
  generateReelSlideSpeech,
  generateReelSlideSpeeches,
  generateSlidesFromTemplate,
  getReelProject,
  listReelProjects,
  listReelVoices,
  saveReelTemplate,
  testReelTTSVoice,
  updateReelProject,
  updateReelSlide,
} from '@/api/reelStudio'
import ReelPreview from '@/components/admin/reel-studio/ReelPreview.vue'
import ReelProjectForm from '@/components/admin/reel-studio/ReelProjectForm.vue'
import ReelProjectsList from '@/components/admin/reel-studio/ReelProjectsList.vue'
import ReelSlideEditor from '@/components/admin/reel-studio/ReelSlideEditor.vue'
import ReelTemplateBuilder from '@/components/admin/reel-studio/ReelTemplateBuilder.vue'
import FormatHelp from '@/components/admin/FormatHelp.vue'

const userStore = useUserStore()
const canManage = computed(() => Boolean(userStore.isAdmin))

const projects = ref([])
const selectedProjectId = ref(null)
const selectedProject = ref(null)
const selectedSlideId = ref(null)

const loadingProjects = ref(false)
const loadingProjectDetail = ref(false)
const savingProject = ref(false)
const generatingTemplate = ref(false)
const savingTemplate = ref(false)
const generatingSpeech = ref(false)
const generatingSpeechSlideId = ref(null)
const exportingVideo = ref(false)
const savingSlide = ref(false)
const loadingVoiceOptions = ref(false)
const voiceOptions = ref([])
const selectedVoiceId = ref('')
const voiceOptionsError = ref('')
const providers = ref([])
const selectedProviderId = ref('')
const testingVoice = ref(false)
const testAudioUrl = ref('')
const SPEECH_CHAR_WARNING_THRESHOLD = 4000
const SPEECH_CHAR_HARD_LIMIT = 4500
const showManualEditor = ref(false)
const showElevenLabsAdvanced = ref(false)
const projectFormOpen = ref(false)
const editingProject = ref(null)
const templateDraft = ref('')
const editorSectionRef = ref(null)
const ELEVENLABS_SETTINGS_STORAGE_KEY = 'reelStudio.elevenLabsSettings.v1'
const ELEVENLABS_MODEL_OPTIONS = [
  { value: 'eleven_multilingual_v3', label: 'eleven_multilingual_v3' },
  { value: 'eleven_multilingual_v2', label: 'eleven_multilingual_v2' },
]
const DEFAULT_ELEVENLABS_SETTINGS = Object.freeze({
  model_id: 'eleven_multilingual_v3',
  stability: 0.64,
  similarity_boost: 0.84,
  style: 0.10,
  speed: 1,
  use_speaker_boost: true,
  language_code: 'fr',
  apply_text_normalization: 'on',
})
const elevenLabsSettings = reactive(loadStoredElevenLabsSettings())

const feedback = reactive({
  type: 'info',
  text: '',
})

const diagnosticsBySlideId = reactive({})
let detailRequestId = 0
const REEL_FORMAT_TEMPLATE = `FORMAT REEL STUDIO (PRO) - GÉNÉRATION COMPLÈTE

Objectif:
- Écrire toutes les slides d'un coup
- Chaque bloc = 1 slide claire et identifiable
- L'ordre SLIDE 1, 2, 3... détermine la timeline finale
- Tu n'es pas obligé d'avoir 6 slides
- Si une formule dépasse, ne fais pas une ligne horizontale
- Coupe-la en plusieurs lignes KATEX courtes

Structure:
SLIDE <numéro> | <type>
TITLE: ...
TEXT: ...
KATEX: ...
VOICE: ...
---

Voix ElevenLabs (eleven_v3):
- Chaque slide doit avoir son VOICE: pour generer son MP3 independant.
- Ajoute les indications de jeu directement dans VOICE avec des tags entre crochets.
- Les tags ne s'affichent pas dans le reel: ils servent seulement a guider la voix.
- Format recommande: VOICE: [thoughtful] On cherche d'abord la bonne identite.
- Mets le tag juste avant le passage concerne, ou juste apres une phrase s'il sert de reaction.
- N'en mets pas trop: 1 a 2 tags par slide suffisent souvent.
- Utilise aussi la ponctuation: ... pour une pause/hesitation, ? pour une intonation interrogative, MAJUSCULES pour insister.

Tags utiles selon ElevenLabs:
- Emotions/direction: [thoughtful], [curious], [excited], [happy], [sad], [angry], [surprised], [annoyed], [appalled], [sarcastic], [mischievously], [crying]
- Livraison: [whispers], [shouts], [dramatically], [warmly], [calm]
- Reactions: [laughs], [laughing], [chuckles], [sighs], [exhales], [clears throat], [inhales deeply], [exhales sharply]
- Pauses: [short pause], [long pause]
- A eviter pour OptiTAB: tags visuels ou non vocaux comme [standing], [grinning], [music].
- Si un tag ne marche pas, teste une variante ou change de voix: ElevenLabs precise que l'effet depend beaucoup de la voix choisie.
- Pour plus d'expressivite, garde ELEVENLABS_MODEL_ID=eleven_v3 et une stabilite proche Creative/Natural; Robust rend les tags moins reactifs.

Hook recommandé:
- La slide hook doit contenir une phrase courte + le défi mathématique + une question.
- Utilise TITLE pour la phrase d'accroche, KATEX pour le défi, TEXT pour la question.
- Exemple visuel attendu: "Défi express" + formule au centre + "Tu trouves combien ?"

Correction recommandée:
- La slide 2 doit commencer par TEXT: Correction :
- Ensuite, mets les lignes KATEX de résolution.
- Toutes les slides de calcul suivantes doivent continuer la même correction.
- Le mot "Correction :" n'est pas ajouté automatiquement: il faut l'écrire explicitement dans TEXT.
- Si la correction devient trop pleine, coche "Nouvelle page" sur une slide: le cumul repart de cette slide en gardant le texte de correction.

CTA recommandé:
- La slide cta doit contenir le résultat final et l'appel à l'action.
- Utilise TITLE pour "Résultat", KATEX pour la formule finale, TEXT pour l'appel à l'action.
- En CTA: titre et texte alignés à gauche, seule la formule est centrée.
- TEXT recommandé sur 3 lignes:
  Abonne-toi à OptiTAB
  Sauvegarde ce Reel
  Commente ton résultat

Description Instagram obligatoire:
- Apres les slides, ajoute un bloc INSTAGRAM_DESCRIPTION copiable.
- Objectif: description Instagram SEO avec style Semji/semantic SEO.
- Commence par une accroche courte avec emoji + mot-cle principal.
- Explique l'exercice en 2 a 4 phrases naturelles avec les mots-cles maths importants.
- Ajoute 3 a 5 benefices/lignes "Dans ce reel".
- Ajoute les appels a l'action: commentaire, sauvegarde, partage, abonnement.
- Termine par exactement 5 hashtags pertinents, pas plus.
- Format obligatoire:
INSTAGRAM_DESCRIPTION:
...
END_INSTAGRAM_DESCRIPTION

Types autorisés:
- hook
- katex
- cumulative_katex
- result
- cta

Mode Auto (IA décide le nombre de slides):
TITLE: Simplification de racines
HOOK: Défi express
KATEX: A=\\frac{\\sqrt{72}+\\sqrt{32}}{\\sqrt{2}}
TEXT: Tu trouves combien ?
KATEX: \\sqrt{72}=6\\sqrt{2}
KATEX: \\sqrt{32}=4\\sqrt{2}
KATEX: A=\\frac{6\\sqrt{2}+4\\sqrt{2}}{\\sqrt{2}}
KATEX: A=10
CTA: Abonne-toi à OptiTAB | Sauvegarde ce Reel | Commente ton résultat

Exemple prêt à copier:
SLIDE 1 | hook
TITLE: Défi express
KATEX: A=\\frac{\\sqrt{72}+\\sqrt{32}}{\\sqrt{2}}
TEXT: Tu trouves combien ?
VOICE: [curious] Défi express... simplifie cette expression.
---
SLIDE 2 | katex
TITLE: Dérivation produit
TEXT: Correction :
KATEX: f(x)=x\\ln(x)
VOICE: [thoughtful] On part de f de x égale x ln x.
---
SLIDE 3 | cumulative_katex
KATEX: u=x \\qquad v=\\ln(x)
VOICE: On reconnaît un produit.
---
SLIDE 4 | cumulative_katex
KATEX: u'=1 \\qquad v'=\\frac{1}{x}
VOICE: [calm] On dérive chaque facteur.
---
SLIDE 5 | result
TITLE: Résultat
KATEX: f'(x)=u'v+uv'
KATEX: f'(x)=\\ln(x)+1
VOICE: [excited] Résultat final: ln de x plus un.
---
SLIDE 6 | cta
TITLE: Résultat
KATEX: f'(x)=\\ln(x)+1
TEXT: Abonne-toi à OptiTAB
Sauvegarde ce Reel
Commente ton résultat
VOICE: [warmly] Abonne-toi pour la suite.
---
INSTAGRAM_DESCRIPTION:
🧠 Derivee piegeuse

Essaie de deriver cette fonction avant de regarder la correction :

f(x)=x\\ln(x)

Un exercice classique de terminale pour revoir la derivee d'un produit et les proprietes du logarithme.

Dans ce reel :
✅ derivee d'un produit
✅ derivee de ln(x)
✅ simplification du resultat final

✍️ Donne ta reponse en commentaire
💾 Sauvegarde ce reel pour reviser
📩 Partage-le a un ami
➕ Abonne-toi a OptiTAB pour progresser en maths

#maths #derivation #logarithme #terminale #bac
END_INSTAGRAM_DESCRIPTION
`

const selectedSlide = computed(() => {
  if (!selectedProject.value?.slides?.length) return null
  return selectedProject.value.slides.find((slide) => Number(slide.id) === Number(selectedSlideId.value)) || null
})

const projectFormInitialValues = computed(() => editingProject.value || {})
const projectFormTitle = computed(() => (editingProject.value?.id ? 'Modifier le reel' : 'Nouveau reel'))
const projectFormSubmitLabel = computed(() => (editingProject.value?.id ? 'Mettre a jour' : 'Creer le reel'))
const projectSpeechText = computed(() => buildProjectSpeechText(selectedProject.value))
const slidesSpeechCount = computed(() => countSlidesWithSpeechText(selectedProject.value))
const generatedSlideSpeechCount = computed(() => countGeneratedSlideSpeeches(selectedProject.value))
const canGenerateSpeech = computed(() => Boolean(selectedProject.value?.id && projectSpeechText.value))
const selectedProvider = computed(() => {
  return providers.value.find((p) => p.id === selectedProviderId.value) || null
})
const elevenLabsProvider = computed(() => {
  return providers.value.find((p) => p.id === 'elevenlabs') || null
})
const elevenLabsUsage = computed(() => elevenLabsProvider.value?.usage || null)
const elevenLabsUsageAvailable = computed(() => {
  const usage = elevenLabsUsage.value
  return Boolean(usage?.available && Number(usage.total) > 0)
})
const elevenLabsUsagePercent = computed(() => {
  const percent = Number(elevenLabsUsage.value?.used_percent)
  if (!Number.isFinite(percent)) return 0
  return Math.max(0, Math.min(100, percent))
})
const elevenLabsUsageBarStyle = computed(() => ({
  width: `${elevenLabsUsagePercent.value}%`,
}))
const elevenLabsUsageConsumedLabel = computed(() => formatCreditCount(elevenLabsUsage.value?.used))
const elevenLabsUsageTotalLabel = computed(() => formatCreditCount(elevenLabsUsage.value?.total))
const elevenLabsUsageRemainingLabel = computed(() => formatCreditCount(elevenLabsUsage.value?.remaining))
const elevenLabsUsagePercentLabel = computed(() => `${formatPercent(elevenLabsUsagePercent.value)}%`)
const elevenLabsUsageResetLabel = computed(() => {
  const resetUnix = Number(elevenLabsUsage.value?.reset_unix)
  if (!Number.isFinite(resetUnix) || resetUnix <= 0) return ''
  const resetDate = new Date(resetUnix * 1000)
  if (Number.isNaN(resetDate.getTime())) return ''
  return `Reset le ${resetDate.toLocaleDateString('fr-FR')}`
})
const elevenLabsUsageErrorLabel = computed(() => {
  const usage = elevenLabsUsage.value
  if (usage?.error_code === 'missing_permissions') {
    return 'Permission user_read manquante sur la cle ElevenLabs.'
  }
  return usage?.error || 'Impossible de lire les credits ElevenLabs.'
})
const selectedProviderConfigured = computed(() => Boolean(selectedProvider.value?.configured))
const currentProviderVoices = computed(() => selectedProvider.value?.voices || [])
const selectedProviderMeta = computed(() => {
  if (!selectedProvider.value) return ''
  if (!selectedProvider.value.configured) {
    return selectedProvider.value.error
      ? `Non configure: ${selectedProvider.value.error}`
      : 'Non configure (cle API ou credentials manquants)'
  }
  return ''
})
const selectedVoice = computed(() => {
  return currentProviderVoices.value.find((voice) => voice.voice_id === selectedVoiceId.value) || null
})
const selectedVoiceApiUsable = computed(() => {
  if (!selectedVoice.value) return false
  if (selectedVoice.value.api_usable === false) return false
  return true
})
const selectedVoiceCanGenerate = computed(() => {
  if (!selectedVoiceApiUsable.value) return false
  return selectedVoiceHasQuotaForCharacters(speechCharCount.value)
})
const speechCharCount = computed(() => projectSpeechText.value?.length || 0)
const speechCharCountWarning = computed(() => {
  if (!speechCharCount.value) return ''
  if (speechCharCount.value > SPEECH_CHAR_HARD_LIMIT) {
    return `au-dessus de la limite ${SPEECH_CHAR_HARD_LIMIT} caracteres (Google TTS): coupe le texte ou bascule sur ElevenLabs.`
  }
  if (speechCharCount.value > SPEECH_CHAR_WARNING_THRESHOLD) {
    return `proche de la limite ${SPEECH_CHAR_HARD_LIMIT} caracteres.`
  }
  return ''
})
const selectedVoiceMeta = computed(() => {
  if (!selectedVoice.value) return ''
  if (selectedProviderId.value === 'google') {
    return voiceQuotaUsageLabel(selectedVoice.value)
  }
  return ''
  const labels = selectedVoice.value.labels || {}
  return [
    selectedVoice.value.matches_filter ? 'FR accent parisien' : 'compatible API',
    selectedVoice.value.is_custom ? 'ID personnalise' : '',
    labels.language ? labels.language.toUpperCase() : '',
    labels.accent === 'parisian' ? 'accent parisien' : labels.accent,
    selectedVoice.value.category,
  ].filter(Boolean).join(' · ')
})
const selectedVoiceWarning = computed(() => {
  if (!selectedVoice.value) return ''
  if (selectedProviderId.value === 'google') {
    if (selectedVoice.value.api_usable === false) {
      return selectedVoice.value.api_usable_reason || 'Seuil de quota Google atteint pour cette famille de voix.'
    }
    if (!selectedVoiceHasQuotaForCharacters(speechCharCount.value)) {
      return 'Ce reel depasserait le seuil de 90% du quota gratuit pour cette famille de voix.'
    }
    if (selectedVoice.value.quota_status === 'near_limit') {
      return 'Quota Google proche du seuil de grisage.'
    }
    return ''
  }
  return ''
})

function voiceOptionLabel(voice) {
  if (!voice) return ''
  if (voice.tier) {
    return [compactGoogleVoiceName(voice), voiceQuotaPercentLabel(voice)].filter(Boolean).join(' ')
  }
  // ElevenLabs voices
  const label = String(voice.name || voice.voice_id || '').trim()
  const parts = []
  if (voice.category) parts.push(voice.category)
  if (voice.api_usable === false) parts.push('non disponible')
  return parts.length ? `${label} - ${parts.join(', ')}` : label
}

function compactGoogleVoiceName(voice) {
  const name = String(voice?.name || voice?.voice_id || '').trim()
  const match = name.match(/^(.+?)\s*\(([^-)]+)(?:\s*-\s*[^)]*)?\)$/)
  if (!match) return name
  const voiceName = match[1].trim()
  const model = match[2].trim()
  return model ? `${voiceName} (${model})` : voiceName
}

function voiceQuotaPercentLabel(voice) {
  const quota = voice?.quota || {}
  const percent = Number(quota.used_percent ?? voice?.quota_used_percent ?? 0)
  if (!Number.isFinite(percent)) return ''
  return `${Math.round(percent)}%`
}

function formatCreditCount(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return '0'
  return Math.max(0, Math.round(number)).toLocaleString('fr-FR')
}

function formatPercent(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return '0'
  if (number >= 10) return Math.round(number).toLocaleString('fr-FR')
  return Number(number.toFixed(1)).toLocaleString('fr-FR')
}

function voiceQuotaUsageLabel(voice) {
  const quota = voice?.quota || {}
  const used = Number(quota.used_characters ?? voice?.quota_used_characters)
  const limit = Number(quota.free_monthly_character_limit ?? voice?.free_monthly_character_limit)
  if (!Number.isFinite(used) || !Number.isFinite(limit) || limit <= 0) return ''
  return `${Math.max(0, Math.round(used))}/${Math.max(0, Math.round(limit))}`
}

function selectedVoiceRemainingUntilDisable() {
  const voice = selectedVoice.value
  if (!voice || selectedProviderId.value !== 'google') return Number.POSITIVE_INFINITY
  const quota = voice.quota || {}
  return Number(
    quota.remaining_until_disable_characters ??
      voice.quota_remaining_until_disable_characters ??
      Number.POSITIVE_INFINITY,
  )
}

function selectedVoiceHasQuotaForCharacters(characterCount) {
  if (selectedProviderId.value !== 'google') return true
  if (!selectedVoiceApiUsable.value) return false
  const count = Number(characterCount || 0)
  const remaining = selectedVoiceRemainingUntilDisable()
  return !Number.isFinite(remaining) || count <= remaining
}

function clampNumber(value, fallback, min, max) {
  const number = Number(value)
  if (!Number.isFinite(number)) return fallback
  return Math.max(min, Math.min(max, number))
}

function normalizeElevenLabsSettings(value = {}) {
  const modelIds = ELEVENLABS_MODEL_OPTIONS.map((item) => item.value)
  const modelId = modelIds.includes(value.model_id)
    ? value.model_id
    : DEFAULT_ELEVENLABS_SETTINGS.model_id
  const normalizationModes = ['auto', 'on', 'off']
  const textNormalization = normalizationModes.includes(value.apply_text_normalization)
    ? value.apply_text_normalization
    : DEFAULT_ELEVENLABS_SETTINGS.apply_text_normalization

  return {
    model_id: modelId,
    stability: clampNumber(value.stability, DEFAULT_ELEVENLABS_SETTINGS.stability, 0, 1),
    similarity_boost: clampNumber(value.similarity_boost, DEFAULT_ELEVENLABS_SETTINGS.similarity_boost, 0, 1),
    style: clampNumber(value.style, DEFAULT_ELEVENLABS_SETTINGS.style, 0, 1),
    speed: clampNumber(value.speed, DEFAULT_ELEVENLABS_SETTINGS.speed, 0.5, 2),
    use_speaker_boost: typeof value.use_speaker_boost === 'boolean'
      ? value.use_speaker_boost
      : DEFAULT_ELEVENLABS_SETTINGS.use_speaker_boost,
    language_code: String(value.language_code || DEFAULT_ELEVENLABS_SETTINGS.language_code).trim() || 'fr',
    apply_text_normalization: textNormalization,
  }
}

function loadStoredElevenLabsSettings() {
  if (typeof window === 'undefined') return { ...DEFAULT_ELEVENLABS_SETTINGS }
  try {
    const raw = window.localStorage.getItem(ELEVENLABS_SETTINGS_STORAGE_KEY)
    if (!raw) return { ...DEFAULT_ELEVENLABS_SETTINGS }
    return normalizeElevenLabsSettings(JSON.parse(raw))
  } catch (_) {
    return { ...DEFAULT_ELEVENLABS_SETTINGS }
  }
}

function persistElevenLabsSettings() {
  if (typeof window === 'undefined') return
  try {
    window.localStorage.setItem(
      ELEVENLABS_SETTINGS_STORAGE_KEY,
      JSON.stringify(normalizeElevenLabsSettings(elevenLabsSettings)),
    )
  } catch (_) {
    // Local storage can be unavailable in private contexts.
  }
}

function resetElevenLabsSettings() {
  Object.assign(elevenLabsSettings, DEFAULT_ELEVENLABS_SETTINGS)
}

function getElevenLabsSettingsPayload() {
  return normalizeElevenLabsSettings(elevenLabsSettings)
}

function buildSpeechGenerationPayload(extra = {}) {
  const payload = {
    ...extra,
    provider: selectedProviderId.value,
    voice_id: selectedVoiceId.value,
  }
  if (selectedProviderId.value === 'elevenlabs') {
    Object.assign(payload, getElevenLabsSettingsPayload())
  }
  return payload
}

watch(elevenLabsSettings, persistElevenLabsSettings, { deep: true })

const speechStatusLabel = computed(() => {
  if (!selectedProject.value?.id) return ''
  if (generatingSpeech.value) return 'Generation en cours'
  if (!projectSpeechText.value) return 'Texte voix indisponible'
  return `${generatedSlideSpeechCount.value}/${slidesSpeechCount.value} slides avec MP3`
})
const instagramCaptionText = computed(() => {
  const projectCaption = String(selectedProject.value?.instagram_caption || '').trim()
  if (projectCaption) return projectCaption
  return extractInstagramCaption(templateDraft.value)
})

function setFeedback(type, text) {
  feedback.type = type
  feedback.text = text
}

function clearDiagnostics() {
  Object.keys(diagnosticsBySlideId).forEach((key) => {
    delete diagnosticsBySlideId[key]
  })
}

function normalizePayload(payload) {
  if (payload && typeof payload === 'object' && payload.success && Object.prototype.hasOwnProperty.call(payload, 'data')) {
    return payload.data
  }
  return payload
}

function normalizeProjectsList(payload) {
  const normalized = normalizePayload(payload)
  if (Array.isArray(normalized)) return normalized
  if (Array.isArray(normalized?.results)) return normalized.results
  return []
}

function normalizeProject(payload) {
  const normalized = normalizePayload(payload)
  return normalized && typeof normalized === 'object' ? normalized : null
}

function upsertProjectSummary(project) {
  if (!project?.id) return

  const summary = {
    id: project.id,
    title: project.title,
    theme: project.theme,
    level: project.level,
    format_type: project.format_type,
    instagram_caption: project.instagram_caption,
    target_duration_seconds: project.target_duration_seconds,
    slide_count: Array.isArray(project.slides) ? project.slides.length : project.slide_count,
    status: project.status,
    speech_audio_url: project.speech_audio_url,
    speech_status: project.speech_status,
    speech_generated_at: project.speech_generated_at,
    video_file_url: project.video_file_url,
    video_status: project.video_status,
    video_generated_at: project.video_generated_at,
    created_at: project.created_at,
    updated_at: project.updated_at,
  }

  const idx = projects.value.findIndex((item) => Number(item.id) === Number(summary.id))
  if (idx === -1) {
    projects.value = [summary, ...projects.value]
  } else {
    projects.value.splice(idx, 1, summary)
  }

  projects.value = [...projects.value].sort((a, b) => new Date(b.updated_at || b.created_at || 0) - new Date(a.updated_at || a.created_at || 0))
}

function closeProjectForm() {
  projectFormOpen.value = false
  editingProject.value = null
}

function openCreateProjectForm() {
  editingProject.value = null
  selectedProject.value = null
  selectedProjectId.value = null
  selectedSlideId.value = null
  templateDraft.value = ''
  clearDiagnostics()
  projectFormOpen.value = true
}

function splitFilledLines(value) {
  return String(value || '')
    .replace(/\r\n/g, '\n')
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean)
}

function extractInstagramCaption(value) {
  const lines = String(value || '').replace(/\r\n/g, '\n').replace(/\r/g, '\n').split('\n')
  const captionLines = []
  let capturing = false

  for (const rawLine of lines) {
    const line = String(rawLine || '').trimEnd()
    const stripped = line.trim()
    const startMatch = stripped.match(/^(INSTAGRAM_DESCRIPTION|DESCRIPTION_INSTAGRAM|INSTAGRAM_CAPTION|CAPTION_INSTAGRAM|INSTAGRAM)\s*:\s*(.*)$/i)

    if (capturing) {
      if (/^END_(INSTAGRAM_DESCRIPTION|DESCRIPTION_INSTAGRAM|INSTAGRAM_CAPTION|CAPTION_INSTAGRAM|INSTAGRAM)$/i.test(stripped)) {
        break
      }
      captionLines.push(line)
      continue
    }

    if (startMatch) {
      capturing = true
      if (startMatch[2]) captionLines.push(startMatch[2].trim())
    }
  }

  return captionLines.join('\n').trim()
}

function appendInstagramCaptionBlock(value, caption) {
  const safeCaption = String(caption || '').trim()
  if (!safeCaption) return value

  const body = String(value || '').trim()
  const captionBlock = `INSTAGRAM_DESCRIPTION:\n${safeCaption}\nEND_INSTAGRAM_DESCRIPTION`
  return body ? `${body}\n---\n${captionBlock}` : captionBlock
}

async function copyTextToClipboard(value) {
  const text = String(value || '')
  if (!text) return

  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text)
    return
  }

  const textarea = document.createElement('textarea')
  textarea.value = text
  textarea.setAttribute('readonly', '')
  textarea.style.position = 'fixed'
  textarea.style.left = '-9999px'
  document.body.appendChild(textarea)
  textarea.select()
  document.execCommand('copy')
  textarea.remove()
}

async function copyInstagramCaption() {
  if (!instagramCaptionText.value) return

  try {
    await copyTextToClipboard(instagramCaptionText.value)
    setFeedback('success', 'Description Instagram copiee.')
  } catch (error) {
    setFeedback('error', 'Impossible de copier la description Instagram.')
  }
}

function normalizeSpeechLine(value) {
  return String(value || '')
    .replace(/\r\n/g, '\n')
    .replace(/\r/g, '\n')
    .split('\n')
    .map((line) => line.replace(/\s+/g, ' ').trim())
    .filter(Boolean)
    .join(' ')
}

function slideSpeechText(slide) {
  const voice = normalizeSpeechLine(slide?.voice_script)
  if (voice) return voice

  return [slide?.title, slide?.screen_text]
    .map((part) => normalizeSpeechLine(part))
    .filter(Boolean)
    .join('. ')
}

function buildProjectSpeechText(project) {
  const slides = Array.isArray(project?.slides) ? [...project.slides] : []
  slides.sort((a, b) => Number(a.order || 0) - Number(b.order || 0) || Number(a.id || 0) - Number(b.id || 0))
  return slides
    .map((slide) => slideSpeechText(slide))
    .filter(Boolean)
    .join('\n\n')
}

function countSlidesWithSpeechText(project) {
  const slides = Array.isArray(project?.slides) ? project.slides : []
  return slides.filter((slide) => Boolean(slideSpeechText(slide))).length
}

function countGeneratedSlideSpeeches(project) {
  const slides = Array.isArray(project?.slides) ? project.slides : []
  return slides.filter((slide) => slide?.speech_audio_url).length
}

function splitSlideProjectPayload(payload) {
  if (!payload || typeof payload !== 'object') {
    return { slide: null, project: null }
  }

  const { project, ...slide } = payload
  return {
    slide: slide?.id ? slide : null,
    project: project?.id ? project : null,
  }
}

function applyProjectSummary(project) {
  if (!project?.id || !selectedProject.value?.id) return
  if (Number(project.id) !== Number(selectedProject.value.id)) return

  const currentSlides = Array.isArray(selectedProject.value.slides) ? selectedProject.value.slides : []
  selectedProject.value = {
    ...selectedProject.value,
    ...project,
    slides: currentSlides,
  }
  upsertProjectSummary(selectedProject.value)
}

function updateSelectedProjectSlide(updatedSlide) {
  const { slide, project } = splitSlideProjectPayload(updatedSlide)
  if (!slide?.id || !selectedProject.value?.slides) return

  const index = selectedProject.value.slides.findIndex((item) => Number(item.id) === Number(slide.id))
  if (index === -1) return

  selectedProject.value.slides.splice(index, 1, slide)
  if (project?.id) {
    applyProjectSummary(project)
  } else {
    selectedProject.value.updated_at = new Date().toISOString()
    upsertProjectSummary(selectedProject.value)
  }
}

function appendTemplateField(lines, label, value) {
  splitFilledLines(value).forEach((line) => {
    lines.push(`${label}: ${line}`)
  })
}

function serializeProjectSlides(project) {
  const slides = Array.isArray(project?.slides) ? [...project.slides] : []
  slides.sort((a, b) => Number(a.order || 0) - Number(b.order || 0) || Number(a.id || 0) - Number(b.id || 0))

  const slidesText = slides
    .map((slide, index) => {
      const lines = [`SLIDE ${slide.order || index + 1} | ${slide.slide_type || 'katex'}`]
      appendTemplateField(lines, 'TITLE', slide.title)
      appendTemplateField(lines, 'TEXT', slide.screen_text)
      appendTemplateField(lines, 'KATEX', slide.katex)
      appendTemplateField(lines, 'VOICE', slide.voice_script)
      return lines.join('\n')
    })
    .join('\n---\n')

  return appendInstagramCaptionBlock(slidesText, project?.instagram_caption)
}

function scrollEditorIntoView() {
  requestAnimationFrame(() => {
    editorSectionRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  })
}

async function openEditProjectForm(project) {
  if (!project?.id) return
  closeProjectForm()

  const currentProjectAlreadyLoaded =
    Number(selectedProject.value?.id) === Number(project.id) &&
    Array.isArray(selectedProject.value?.slides)
  const projectToEdit = currentProjectAlreadyLoaded ? selectedProject.value : await selectProject(project.id)
  templateDraft.value = serializeProjectSlides(projectToEdit || selectedProject.value)

  if (!templateDraft.value) {
    setFeedback('info', 'Ce reel n a pas encore de slides a modifier.')
  }

  scrollEditorIntoView()
}

function extractErrorMessage(error, fallback) {
  const data = error?.response?.data || {}
  const fieldMessage = Object.values(data).find((value) => Array.isArray(value) && value.length)
  const apiMessage = data.detail || data.message || fieldMessage?.[0]
  return String(apiMessage || fallback)
}

async function loadVoiceOptions() {
  if (!canManage.value) return

  loadingVoiceOptions.value = true
  voiceOptionsError.value = ''
  try {
    const response = await listReelVoices()
    const data = response?.data || {}
    const providerList = Array.isArray(data.providers) ? data.providers : []
    providers.value = providerList

    // Pick the best initial provider: previous selection if still available + configured,
    // else the backend-recommended default if configured, else first configured provider.
    const currentProviderStillOk = providerList.some(
      (p) => p.id === selectedProviderId.value && p.configured,
    )
    if (!currentProviderStillOk) {
      const preferred = data.default_provider || ''
      selectedProviderId.value =
        providerList.find((p) => p.id === preferred && p.configured)?.id ||
        providerList.find((p) => p.configured)?.id ||
        providerList[0]?.id ||
        ''
    }

    // Sync legacy voiceOptions to current provider voices for any code that still reads it.
    voiceOptions.value = currentProviderVoices.value

    selectVoiceForCurrentProvider()

    if (!providerList.length) {
      voiceOptionsError.value = 'Aucun fournisseur de voix disponible.'
    } else if (!selectedProvider.value?.configured) {
      voiceOptionsError.value = selectedProvider.value?.error || 'Le fournisseur selectionne n est pas configure.'
    }
  } catch (error) {
    providers.value = []
    voiceOptions.value = []
    selectedVoiceId.value = ''
    voiceOptionsError.value = extractErrorMessage(error, 'Impossible de charger les voix.')
  } finally {
    loadingVoiceOptions.value = false
  }
}

function selectVoiceForCurrentProvider() {
  const provider = selectedProvider.value
  if (!provider) {
    selectedVoiceId.value = ''
    return
  }
  const voices = provider.voices || []
  const currentExists = voices.some(
    (v) => v.voice_id === selectedVoiceId.value && v.api_usable !== false,
  )
  if (currentExists) return

  const defaultId = provider.default_voice_id || ''
  selectedVoiceId.value =
    voices.find((v) => v.voice_id === defaultId && v.api_usable !== false)?.voice_id ||
    voices.find((v) => v.api_usable !== false)?.voice_id ||
    ''
}

function resetTestAudio() {
  if (testAudioUrl.value) {
    window.URL.revokeObjectURL(testAudioUrl.value)
    testAudioUrl.value = ''
  }
}

function onProviderChange() {
  resetTestAudio()
  selectVoiceForCurrentProvider()
  voiceOptions.value = currentProviderVoices.value
}

async function handleTestVoice() {
  if (!selectedProviderId.value || !selectedVoiceId.value) return
  if (!selectedVoiceApiUsable.value) return

  // Build a short preview: take the first sentence of the project speech text,
  // or fall back to a generic French sample.
  const fullText = projectSpeechText.value || ''
  const firstSentence = fullText.split(/[.!?\n]/).map((s) => s.trim()).find(Boolean) || ''
  const previewText = (firstSentence || 'Bonjour, ceci est un test de voix OptiTAB.').slice(0, 240)
  if (!selectedVoiceHasQuotaForCharacters(previewText.length)) {
    setFeedback('error', 'Cette voix est trop proche du seuil de quota Google pour generer un apercu.')
    return
  }

  testingVoice.value = true
  try {
    const response = await testReelTTSVoice(buildSpeechGenerationPayload({ text: previewText }))

    resetTestAudio()
    const blob = response?.data instanceof Blob ? response.data : new Blob([response?.data], { type: 'audio/mpeg' })
    testAudioUrl.value = window.URL.createObjectURL(blob)

    const cached = response?.headers?.['x-tts-cached'] === '1'
    const chars = response?.headers?.['x-tts-character-count'] || previewText.length
    setFeedback('success', `Apercu voix genere (${chars} caracteres${cached ? ', depuis le cache' : ''}).`)
    if (!cached) loadVoiceOptions()
  } catch (error) {
    const blobMessage = await readBlobErrorMessage(error)
    setFeedback('error', blobMessage || extractErrorMessage(error, 'Impossible de generer l apercu voix.'))
  } finally {
    testingVoice.value = false
  }
}

async function readBlobErrorMessage(error) {
  const data = error?.response?.data
  if (!(data instanceof Blob)) return ''
  try {
    const text = await data.text()
    if (!text) return ''
    try {
      const parsed = JSON.parse(text)
      return parsed?.detail || parsed?.message || ''
    } catch (_) {
      return text.slice(0, 200)
    }
  } catch (_) {
    return ''
  }
}

async function loadProjects() {
  if (!canManage.value) return

  loadingProjects.value = true
  try {
    const response = await listReelProjects()
    projects.value = normalizeProjectsList(response?.data)

    if (!projects.value.length) {
      selectedProject.value = null
      selectedProjectId.value = null
      selectedSlideId.value = null
      openCreateProjectForm()
      return
    }

    const selectedStillExists = projects.value.some((project) => Number(project.id) === Number(selectedProjectId.value))
    if (selectedStillExists) {
      await selectProject(selectedProjectId.value)
    } else {
      selectedProject.value = null
      selectedProjectId.value = null
      selectedSlideId.value = null
    }
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de charger les projets Reel Studio.'))
  } finally {
    loadingProjects.value = false
  }
}

async function handleSubmitProject(payload) {
  if (!canManage.value) return

  const safeTitle = String(payload?.title || '').trim()
  if (!safeTitle) {
    setFeedback('error', 'Ajoute un titre avant de creer le reel.')
    return
  }

  savingProject.value = true
  try {
    const projectId = editingProject.value?.id
    const projectPayload = {
      ...payload,
      title: safeTitle,
    }
    const response = projectId
      ? await updateReelProject(projectId, projectPayload)
      : await createReelProject({ ...projectPayload, slide_count: 0 })
    const project = normalizeProject(response?.data)

    if (project?.id) {
      upsertProjectSummary(project)
      selectedProject.value = project
      selectedProjectId.value = Number(project.id)
      selectedSlideId.value = project.slides?.[0]?.id || null
      templateDraft.value = serializeProjectSlides(project)
      clearDiagnostics()
      closeProjectForm()
      setFeedback('success', projectId ? 'Reel mis a jour.' : 'Reel cree en base.')
    }
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de sauvegarder le reel.'))
  } finally {
    savingProject.value = false
  }
}

async function handleDeleteProject(project) {
  if (!project?.id || !canManage.value) return
  if (!window.confirm(`Supprimer le reel "${project.title || project.id}" et toutes ses slides ?`)) return

  savingProject.value = true
  try {
    await deleteReelProject(project.id)
    projects.value = projects.value.filter((item) => Number(item.id) !== Number(project.id))

    if (Number(selectedProjectId.value) === Number(project.id)) {
      selectedProject.value = null
      selectedProjectId.value = null
      selectedSlideId.value = null
      templateDraft.value = ''
      clearDiagnostics()
    }

    if (editingProject.value?.id && Number(editingProject.value.id) === Number(project.id)) {
      closeProjectForm()
    }

    if (!projects.value.length) {
      openCreateProjectForm()
    }

    setFeedback('success', 'Reel supprime.')
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de supprimer le reel.'))
  } finally {
    savingProject.value = false
  }
}

async function selectProject(projectId) {
  if (!projectId || !canManage.value) return null

  selectedProjectId.value = Number(projectId)
  loadingProjectDetail.value = true
  const requestId = ++detailRequestId

  try {
    const response = await getReelProject(projectId)
    if (requestId !== detailRequestId) return null

    const project = normalizeProject(response?.data)
    selectedProject.value = project
    selectedSlideId.value = project?.slides?.[0]?.id || null
    clearDiagnostics()
    upsertProjectSummary(project)
    return project
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de charger le projet sélectionné.'))
    return null
  } finally {
    if (requestId === detailRequestId) {
      loadingProjectDetail.value = false
    }
  }
}

async function handleGenerateFromTemplate(payload) {
  if (!selectedProject.value?.id) return

  generatingTemplate.value = true
  const submittedInstagramCaption = extractInstagramCaption(payload?.template_text)
  try {
    const response = await generateSlidesFromTemplate(selectedProject.value.id, payload)
    const updatedProject = normalizeProject(response?.data)

    if (updatedProject?.id) {
      if (submittedInstagramCaption && !String(updatedProject.instagram_caption || '').trim()) {
        updatedProject.instagram_caption = submittedInstagramCaption
      }
      selectedProject.value = updatedProject
      selectedSlideId.value = updatedProject.slides?.[0]?.id || null
      templateDraft.value = serializeProjectSlides(updatedProject)
      clearDiagnostics()
      upsertProjectSummary(updatedProject)
      setFeedback('success', `Slides générées depuis template (${updatedProject.slides?.length || 0} slides).`)
    }
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de générer les slides depuis le template.'))
  } finally {
    generatingTemplate.value = false
  }
}

async function handleSaveTemplate(payload) {
  if (!selectedProject.value?.id) return

  savingTemplate.value = true
  const submittedInstagramCaption = extractInstagramCaption(payload?.template_text)
  try {
    const response = await saveReelTemplate(selectedProject.value.id, payload)
    const updatedProject = normalizeProject(response?.data)

    if (updatedProject?.id) {
      if (submittedInstagramCaption && !String(updatedProject.instagram_caption || '').trim()) {
        updatedProject.instagram_caption = submittedInstagramCaption
      }
      selectedProject.value = updatedProject
      selectedSlideId.value = updatedProject.slides?.[0]?.id || selectedSlideId.value || null
      templateDraft.value = serializeProjectSlides(updatedProject)
      clearDiagnostics()
      upsertProjectSummary(updatedProject)
      const readyCount = countGeneratedSlideSpeeches(updatedProject)
      const totalSlides = updatedProject.slides?.length || 0
      const voicePart = readyCount ? ` Voix conservee sur ${readyCount}/${totalSlides} slide${totalSlides > 1 ? 's' : ''}.` : ''
      setFeedback('success', `Reel sauvegarde (${totalSlides} slides).${voicePart}`)
    }
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de sauvegarder le template.'))
  } finally {
    savingTemplate.value = false
  }
}

async function handleGenerateSpeech() {
  if (!selectedProject.value?.id || !canGenerateSpeech.value || !selectedVoiceCanGenerate.value) return

  generatingSpeech.value = true
  try {
    const response = await generateReelSlideSpeeches(
      selectedProject.value.id,
      buildSpeechGenerationPayload(),
    )
    const updatedProject = normalizeProject(response?.data?.project || response?.data)

    if (updatedProject?.id) {
      selectedProject.value = updatedProject
      selectedSlideId.value = updatedProject.slides?.[0]?.id || selectedSlideId.value || null
      templateDraft.value = serializeProjectSlides(updatedProject)
      upsertProjectSummary(updatedProject)
      const speechMeta = response?.data?.speech || {}
      const count = speechMeta.generated_count ?? countGeneratedSlideSpeeches(updatedProject)
      const charCount = Number(speechMeta.character_count || 0)
      const cachedCount = Number(speechMeta.cached_count || 0)
      const provider = speechMeta.provider || selectedProviderId.value
      const parts = [`Voix par slide generees (${count} MP3, ${provider})`]
      if (charCount) parts.push(`${charCount.toLocaleString('fr-FR')} caracteres`)
      if (cachedCount) parts.push(`${cachedCount} reutilisees du cache`)
      setFeedback('success', parts.join(' · ') + '.')
      loadVoiceOptions()
    }
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de generer les voix par slide.'))
  } finally {
    generatingSpeech.value = false
  }
}

async function handleGenerateSlideSpeech(payload) {
  const slideId = payload && typeof payload === 'object' ? payload.id : payload
  const requestedText = payload && typeof payload === 'object' ? String(payload.text || '').trim() : ''
  const requestedVoiceScript = payload && typeof payload === 'object' ? String(payload.voice_script || '').trim() : ''
  const shouldSaveVoiceScript = Boolean(payload && typeof payload === 'object' && payload.save_voice_script)

  if (!slideId || !selectedProject.value?.slides) return
  if (!selectedVoiceApiUsable.value) {
    setFeedback('error', 'Selectionne une voix compatible API.')
    return
  }
  let slide = selectedProject.value.slides.find((item) => Number(item.id) === Number(slideId))
  const speechText = requestedText || slideSpeechText(slide)
  if (!speechText) {
    setFeedback('error', 'Aucun texte vocal disponible pour cette slide.')
    return
  }
  if (!selectedVoiceHasQuotaForCharacters(speechText.length)) {
    setFeedback('error', 'Cette slide depasserait le seuil de 90% du quota gratuit Google pour cette voix.')
    return
  }

  generatingSpeechSlideId.value = Number(slideId)
  try {
    if (shouldSaveVoiceScript && requestedVoiceScript !== String(slide?.voice_script || '').trim()) {
      const saveResponse = await updateReelSlide(slideId, { voice_script: requestedVoiceScript })
      const savedSlide = normalizeProject(saveResponse?.data)
      if (savedSlide?.id) {
        updateSelectedProjectSlide(savedSlide)
        templateDraft.value = serializeProjectSlides(selectedProject.value)
        slide = savedSlide
      }
    }

    const response = await generateReelSlideSpeech(
      slideId,
      buildSpeechGenerationPayload({ text: speechText }),
    )
    const updatedSlide = normalizeProject(response?.data)

    if (updatedSlide?.id) {
      updateSelectedProjectSlide(updatedSlide)
      setFeedback('success', `Voix de la slide ${updatedSlide.order || ''} generee.`.trim())
      loadVoiceOptions()
    }
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de generer la voix de cette slide.'))
  } finally {
    generatingSpeechSlideId.value = null
  }
}

function buildVideoFilename(project) {
  const safeTitle = String(project?.title || 'optitab-reel')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-zA-Z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .toLowerCase() || 'optitab-reel'
  return `${safeTitle}.mp4`
}

function filenameFromContentDisposition(value) {
  const disposition = String(value || '')
  const utf8Match = disposition.match(/filename\*=UTF-8''([^;]+)/i)
  if (utf8Match?.[1]) {
    try {
      return decodeURIComponent(utf8Match[1])
    } catch (_) {
      return utf8Match[1]
    }
  }

  const quotedMatch = disposition.match(/filename="?([^";]+)"?/i)
  return quotedMatch?.[1] || ''
}

function triggerBlobDownload(blob, filename) {
  if (!blob) return
  const objectUrl = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = objectUrl
  link.download = filename
  link.style.display = 'none'
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.setTimeout(() => window.URL.revokeObjectURL(objectUrl), 60000)
}

async function downloadExportedVideo(project, fallbackUrl) {
  const filename = buildVideoFilename(project)

  try {
    const response = await downloadReelVideo(project.id)
    const headerFilename = filenameFromContentDisposition(response?.headers?.['content-disposition'])
    triggerBlobDownload(response?.data, headerFilename || filename)
    return
  } catch (error) {
    if (!fallbackUrl) throw error
  }

  const fallbackOrigin = new URL(fallbackUrl, window.location.href).origin
  const response = await fetch(fallbackUrl, {
    credentials: fallbackOrigin === window.location.origin ? 'same-origin' : 'omit',
  })
  if (!response.ok) {
    throw new Error(`Telechargement MP4 impossible (${response.status}).`)
  }
  const blob = await response.blob()
  triggerBlobDownload(blob, filename)
}

async function handleExportVideo(payload) {
  if (!selectedProject.value?.id || !payload?.frames?.length) return

  exportingVideo.value = true
  try {
    const response = await exportReelVideo(selectedProject.value.id, payload)
    const updatedProject = normalizeProject(response?.data?.project || response?.data)
    const videoUrl = response?.data?.video?.url || updatedProject?.video_file_url

    if (updatedProject?.id) {
      selectedProject.value = updatedProject
      templateDraft.value = serializeProjectSlides(updatedProject)
      upsertProjectSummary(updatedProject)
    }

    if (videoUrl && (updatedProject?.id || selectedProject.value?.id)) {
      await downloadExportedVideo(updatedProject || selectedProject.value, videoUrl)
      setFeedback('success', 'Video MP4 exportee et telechargement lance.')
    } else {
      setFeedback('success', 'Video MP4 generee.')
    }
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible d exporter la video MP4.'))
  } finally {
    exportingVideo.value = false
  }
}

function handleSlideDiagnostic(diagnostic) {
  if (!diagnostic?.slideId) return
  diagnosticsBySlideId[diagnostic.slideId] = diagnostic
}

async function handleSaveSlide(payload) {
  if (!payload?.id || !selectedProject.value) return

  savingSlide.value = true
  try {
    const diagnostic = diagnosticsBySlideId[payload.id]
    const patchData = {
      title: payload.title,
      screen_text: payload.screen_text,
      katex: payload.katex,
      voice_script: payload.voice_script,
      title_scale: payload.title_scale,
      screen_text_scale: payload.screen_text_scale,
      katex_scale: payload.katex_scale,
      katex_inline_with_previous: payload.katex_inline_with_previous,
      katex_inline_separator: payload.katex_inline_separator,
      katex_inline_offset_percent: payload.katex_inline_offset_percent,
      katex_cumulative_gap_em: payload.katex_cumulative_gap_em,
      katex_reset_cumulative: payload.katex_reset_cumulative,
    }

    if (diagnostic?.status) {
      patchData.layout_status = diagnostic.status
      patchData.layout_notes = diagnostic.notes || ''
    }

    const response = await updateReelSlide(payload.id, patchData)
    const updatedSlide = normalizeProject(response?.data)

    if (updatedSlide?.id) {
      updateSelectedProjectSlide(updatedSlide)
      templateDraft.value = serializeProjectSlides(selectedProject.value)
      setFeedback('success', 'Slide mise à jour.')
    }
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de sauvegarder la slide.'))
  } finally {
    savingSlide.value = false
  }
}

async function handlePatchSlide(payload) {
  if (!payload?.id || !selectedProject.value) return

  const patchData = payload.patch && typeof payload.patch === 'object' ? payload.patch : {}
  const index = selectedProject.value.slides.findIndex((slide) => Number(slide.id) === Number(payload.id))
  if (index === -1 || !Object.keys(patchData).length) return

  const previousSlide = { ...selectedProject.value.slides[index] }
  const nextSlide = { ...previousSlide, ...patchData }
  const speechTextWillChange = slideSpeechText(nextSlide) !== slideSpeechText(previousSlide)
  const optimisticPatch = speechTextWillChange
    ? {
        ...patchData,
        speech_audio: null,
        speech_audio_url: null,
        speech_text: '',
        speech_voice_id: '',
        speech_model_id: '',
        speech_output_format: '',
        speech_status: 'empty',
        speech_error: '',
        speech_generated_at: null,
      }
    : patchData
  selectedProject.value.slides.splice(index, 1, {
    ...selectedProject.value.slides[index],
    ...optimisticPatch,
  })

  try {
    const response = await updateReelSlide(payload.id, patchData)
    const updatedSlide = normalizeProject(response?.data)
    if (updatedSlide?.id) {
      const { slide, project } = splitSlideProjectPayload(updatedSlide)
      selectedProject.value.slides.splice(index, 1, slide || updatedSlide)
      if (project?.id) {
        applyProjectSummary(project)
      } else {
        selectedProject.value.updated_at = new Date().toISOString()
        upsertProjectSummary(selectedProject.value)
      }
      templateDraft.value = serializeProjectSlides(selectedProject.value)
    }
  } catch (error) {
    selectedProject.value.slides.splice(index, 1, previousSlide)
    setFeedback('error', extractErrorMessage(error, 'Impossible de sauvegarder la slide.'))
  }
}

async function handleDeleteSlide(slideId) {
  if (!slideId || !selectedProject.value?.id) return
  if (!window.confirm('Supprimer cette slide ?')) return

  savingSlide.value = true
  try {
    await deleteReelSlide(slideId)
    selectedProject.value.slides = selectedProject.value.slides.filter((slide) => Number(slide.id) !== Number(slideId))
    selectedProject.value.slide_count = selectedProject.value.slides.length
    selectedProject.value.updated_at = new Date().toISOString()
    templateDraft.value = serializeProjectSlides(selectedProject.value)
    upsertProjectSummary(selectedProject.value)

    if (Number(selectedSlideId.value) === Number(slideId)) {
      selectedSlideId.value = selectedProject.value.slides[0]?.id || null
    }

    delete diagnosticsBySlideId[slideId]
    setFeedback('success', 'Slide supprimée.')
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de supprimer la slide.'))
  } finally {
    savingSlide.value = false
  }
}

onMounted(() => {
  loadVoiceOptions()
  loadProjects()
})
</script>

<style src="@/styles/admin-common.css"></style>
<style scoped>
.reel-studio-admin {
  width: 100%;
  min-height: 100%;
  padding: 16px 16px 96px;
  background: #f8fafc;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.page-header h1 {
  margin: 0;
  color: #0f172a;
  font-size: 28px;
  line-height: 1.2;
}

.feedback {
  margin: 0;
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 14px;
  font-weight: 700;
}

.feedback--info {
  background: #eff6ff;
  color: #1e40af;
}

.feedback--success {
  background: #dcfce7;
  color: #166534;
}

.feedback--error {
  background: #fee2e2;
  color: #991b1b;
}

.studio-stack {
  display: flex;
  flex-direction: column;
  gap: 14px;
  min-height: 0;
}

.project-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.project-panel--list {
  order: 9999;
  position: static;
  z-index: auto;
  clear: both;
  margin-top: 56px;
  padding-bottom: 96px;
  transform: none;
}

.section-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border: 1px solid #dbe4ee;
  border-radius: 12px;
  background: #ffffff;
  padding: 14px 16px;
}

.section-toolbar h2 {
  margin: 0;
  color: #0f172a;
  font-size: 18px;
}

.section-toolbar p {
  margin: 4px 0 0;
  color: #64748b;
  font-size: 13px;
  font-weight: 700;
}

.content-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 14px;
  min-width: 0;
  min-height: auto;
  flex-shrink: 0;
  scroll-margin-top: 96px;
}

.left-column,
.right-column {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-width: 0;
  min-height: auto;
}

.right-column > * {
  flex-shrink: 0;
}

.loading-state {
  margin: 0;
  color: #475569;
  font-size: 14px;
}

.empty-editor-state {
  margin: 0;
  border: 1px dashed #bfdbfe;
  border-radius: 12px;
  background: #eff6ff;
  color: #1e40af;
  padding: 16px;
  font-size: 14px;
  font-weight: 800;
}

.btn-primary {
  border: 0;
  border-radius: 8px;
  padding: 10px 14px;
  background: #1d4ed8;
  color: #ffffff;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.btn-primary:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

.btn-secondary {
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  padding: 10px 14px;
  background: #eff6ff;
  color: #1e40af;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.btn-secondary:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.instagram-caption-panel {
  border: 1px solid #dbe4ee;
  border-radius: 12px;
  background: #ffffff;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.instagram-caption-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.instagram-caption-header h3 {
  margin: 0;
  color: #0f172a;
  font-size: 18px;
}

.instagram-caption-header p {
  margin: 4px 0 0;
  color: #64748b;
  font-size: 13px;
  font-weight: 700;
}

.instagram-caption-text {
  width: 100%;
  min-height: 220px;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  background: #f8fbff;
  color: #0f172a;
  font-family: inherit;
  font-size: 14px;
  line-height: 1.5;
  padding: 12px;
  resize: vertical;
  box-sizing: border-box;
}

.speech-panel {
  box-sizing: border-box;
  border: 1px solid #dbe4ee;
  border-radius: 12px;
  background: #ffffff;
  padding: 18px;
  min-width: 0;
  max-width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.speech-panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.speech-panel-header h3 {
  margin: 0;
  color: #0f172a;
  font-size: 19px;
  line-height: 1.2;
}

.speech-panel-header p {
  margin: 6px 0 0;
  color: #64748b;
  font-size: 13px;
  font-weight: 700;
  line-height: 1.35;
}

.speech-controls {
  box-sizing: border-box;
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  align-items: start;
  gap: 12px;
  min-width: 0;
  max-width: 100%;
}

.voice-select {
  box-sizing: border-box;
  min-width: 0;
  max-width: 100%;
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: #334155;
  font-size: 12px;
  font-weight: 800;
  line-height: 1.25;
}

.voice-select select {
  box-sizing: border-box;
  width: 100%;
  min-width: 0;
  max-width: 100%;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  background: #ffffff;
  color: #0f172a;
  font-family: inherit;
  font-size: 13px;
  font-weight: 700;
  line-height: 1.35;
  padding: 9px 10px;
  min-height: 42px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.voice-select select:disabled {
  background: #e2e8f0;
  color: #64748b;
}

.voice-select span {
  color: #64748b;
  font-size: 11px;
  font-weight: 700;
  line-height: 1.35;
  overflow-wrap: anywhere;
}

.voice-select .voice-warning {
  color: #b45309;
}

.voice-advanced {
  box-sizing: border-box;
  display: grid;
  gap: 10px;
  min-width: 0;
  max-width: 100%;
  border: 1px solid #dbeafe;
  border-radius: 8px;
  background: #ffffff;
  padding: 12px;
}

.voice-advanced-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  min-width: 0;
}

.voice-advanced-toggle {
  border: 0;
  background: transparent;
  padding: 0;
  color: #1e3a8a;
  font-family: inherit;
  font-size: 13px;
  font-weight: 900;
  line-height: 1.25;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.voice-advanced-arrow {
  display: inline-grid;
  place-items: center;
  width: 18px;
  height: 18px;
  border-radius: 6px;
  background: #eff6ff;
  color: #1d4ed8;
  font-size: 13px;
  font-weight: 900;
  line-height: 1;
  transition: transform 0.15s ease;
}

.voice-advanced-arrow.is-open {
  transform: rotate(90deg);
}

.voice-advanced-header .btn-secondary {
  min-height: 30px;
  padding: 6px 10px;
  font-size: 12px;
}

.voice-advanced-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(120px, 1fr));
  gap: 10px;
  min-width: 0;
}

.voice-advanced-field,
.voice-toggle {
  box-sizing: border-box;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 5px;
  color: #334155;
  font-size: 12px;
  font-weight: 800;
  line-height: 1.25;
}

.voice-advanced-field--wide {
  grid-column: span 2;
}

.voice-advanced-field input,
.voice-advanced-field select {
  box-sizing: border-box;
  width: 100%;
  min-width: 0;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  background: #f8fafc;
  color: #0f172a;
  font-family: inherit;
  font-size: 13px;
  font-weight: 800;
  line-height: 1.35;
  min-height: 36px;
  padding: 7px 9px;
}

.voice-toggle {
  justify-content: end;
  flex-direction: row;
  align-items: center;
}

.voice-toggle input {
  width: 18px;
  height: 18px;
  margin: 0;
}

.voice-toggle span {
  color: #0f172a;
  font-size: 13px;
  font-weight: 800;
  line-height: 1.35;
}

.voice-usage {
  box-sizing: border-box;
  display: grid;
  gap: 10px;
  min-width: 0;
  max-width: 100%;
  border: 1px solid #bae6fd;
  border-radius: 8px;
  background: #f8fafc;
  padding: 12px;
}

.voice-usage-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  min-width: 0;
}

.voice-usage-header strong {
  color: #0f172a;
  font-size: 13px;
  font-weight: 900;
  line-height: 1.25;
}

.voice-usage-header span,
.voice-usage p {
  color: #475569;
  font-size: 12px;
  font-weight: 800;
  line-height: 1.35;
}

.voice-usage p {
  margin: 0;
}

.voice-usage-bar {
  height: 8px;
  overflow: hidden;
  border-radius: 999px;
  background: #e2e8f0;
}

.voice-usage-bar span {
  display: block;
  height: 100%;
  min-width: 2px;
  border-radius: inherit;
  background: #0284c7;
}

.voice-usage-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 8px;
  margin: 0;
}

.voice-usage-grid div {
  min-width: 0;
}

.voice-usage-grid dt {
  color: #64748b;
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0;
  line-height: 1.25;
  text-transform: uppercase;
}

.voice-usage-grid dd {
  margin: 2px 0 0;
  color: #0f172a;
  font-size: 13px;
  font-weight: 900;
  line-height: 1.25;
  overflow-wrap: anywhere;
}

.voice-usage--error {
  border-color: #fed7aa;
  background: #fff7ed;
}

.voice-usage--error .voice-usage-header span,
.voice-usage--error p {
  color: #9a3412;
}

.speech-actions {
  box-sizing: border-box;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  width: min(100%, 480px);
  max-width: 100%;
  min-width: 0;
  justify-self: end;
}

.speech-actions .btn-primary,
.speech-actions .btn-secondary {
  width: 100%;
  min-height: 42px;
  line-height: 1.2;
  white-space: normal;
}

.voice-charcount {
  font-size: 12px;
  color: #475569;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  padding: 9px 12px;
  border-radius: 8px;
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: flex-end;
  gap: 4px 6px;
  max-width: 360px;
  text-align: right;
}

.voice-charcount strong {
  color: #0f172a;
  font-size: 14px;
}

.voice-charcount small {
  flex-basis: 100%;
  color: inherit;
  font-size: 11px;
  font-weight: 700;
  line-height: 1.35;
}

.voice-charcount--warn {
  color: #b45309;
  background: #fef3c7;
  border-color: #fde68a;
}

.voice-charcount--warn strong {
  color: #92400e;
}

.voice-test-audio {
  margin-top: 12px;
  width: 100%;
  max-width: 360px;
}

.speech-audio {
  width: 100%;
}

.manual-editor-wrap {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-bottom: 36px;
}

@media (max-width: 1140px) {
  .content-grid {
    grid-template-columns: 1fr;
  }

  .speech-controls {
    grid-template-columns: minmax(0, 1fr);
  }

  .speech-actions {
    grid-column: auto;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    justify-self: stretch;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .reel-studio-admin {
    padding: 12px 10px 84px;
  }

  .section-toolbar {
    align-items: stretch;
    flex-direction: column;
  }

  .speech-panel-header {
    align-items: stretch;
    flex-direction: column;
  }

  .speech-controls {
    grid-template-columns: 1fr;
  }

  .voice-usage-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .voice-usage-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .voice-advanced-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .voice-advanced-field--wide {
    grid-column: span 2;
  }

  .speech-actions {
    grid-column: auto;
    grid-template-columns: 1fr;
    min-width: 0;
    justify-self: stretch;
    width: 100%;
  }

  .voice-charcount {
    justify-content: flex-start;
    max-width: none;
    text-align: left;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .page-header h1 {
    font-size: 22px;
  }
}
</style>
