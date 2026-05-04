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
              :disabled="!selectedProject"
              @generate="handleGenerateFromTemplate"
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

            <section v-if="selectedProject" class="speech-panel">
              <div class="speech-toolbar">
                <div>
                  <h3>Voix par slide</h3>
                  <p>{{ speechStatusLabel }}</p>
                </div>
                <label class="voice-select">
                  Voix FR - accent parisien
                  <select
                    v-model="selectedVoiceId"
                    :disabled="loadingVoiceOptions || generatingSpeech || generatingSpeechSlideId"
                  >
                    <option v-if="loadingVoiceOptions" value="">Chargement...</option>
                    <option v-else-if="!voiceOptions.length" value="">Aucune voix trouvee</option>
                    <option
                      v-for="voice in voiceOptions"
                      :key="voice.voice_id"
                      :value="voice.voice_id"
                      :disabled="!voice.api_usable"
                    >
                      {{ voice.name }}{{ voice.category ? ` - ${voice.category}` : '' }}{{ voice.api_usable ? '' : ' (abonnement requis)' }}
                    </option>
                  </select>
                  <span v-if="selectedVoiceMeta">{{ selectedVoiceMeta }}</span>
                  <span v-if="selectedVoiceWarning" class="voice-warning">{{ selectedVoiceWarning }}</span>
                  <span v-else-if="voiceOptionsError">{{ voiceOptionsError }}</span>
                </label>
                <button
                  class="btn-primary"
                  type="button"
                  :disabled="generatingSpeech || loadingVoiceOptions || !canGenerateSpeech || !selectedVoiceCanGenerate"
                  @click="handleGenerateSpeech"
                >
                  {{ generatingSpeech ? 'Generation des MP3...' : 'Generer les MP3 slides' }}
                </button>
              </div>
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
import { computed, onMounted, reactive, ref } from 'vue'
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
const generatingSpeech = ref(false)
const generatingSpeechSlideId = ref(null)
const exportingVideo = ref(false)
const savingSlide = ref(false)
const loadingVoiceOptions = ref(false)
const voiceOptions = ref([])
const selectedVoiceId = ref('')
const voiceOptionsError = ref('')
const showManualEditor = ref(false)
const projectFormOpen = ref(false)
const editingProject = ref(null)
const templateDraft = ref('')
const editorSectionRef = ref(null)

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
const selectedVoice = computed(() => {
  return voiceOptions.value.find((voice) => voice.voice_id === selectedVoiceId.value) || null
})
const selectedVoiceCanGenerate = computed(() => Boolean(selectedVoice.value?.api_usable))
const selectedVoiceMeta = computed(() => {
  if (!selectedVoice.value) return ''
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
  if (selectedVoice.value.requires_subscription) {
    return 'Voix professionnelle: abonnement ElevenLabs requis.'
  }
  if (selectedVoice.value.is_custom) {
    return 'ID personnalise: generation testee au moment de creer le MP3.'
  }
  if (!selectedVoice.value.matches_filter) {
    return 'Fallback compatible API: pas strictement accent parisien.'
  }
  return ''
})
const speechStatusLabel = computed(() => {
  if (!selectedProject.value?.id) return ''
  if (generatingSpeech.value) return 'Generation en cours'
  if (!projectSpeechText.value) return 'Texte voix indisponible'
  return `${generatedSlideSpeechCount.value}/${slidesSpeechCount.value} slides avec MP3`
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
  projectFormOpen.value = true
}

function splitFilledLines(value) {
  return String(value || '')
    .replace(/\r\n/g, '\n')
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean)
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

function updateSelectedProjectSlide(updatedSlide) {
  if (!updatedSlide?.id || !selectedProject.value?.slides) return
  const index = selectedProject.value.slides.findIndex((slide) => Number(slide.id) === Number(updatedSlide.id))
  if (index === -1) return

  selectedProject.value.slides.splice(index, 1, updatedSlide)
  selectedProject.value.updated_at = new Date().toISOString()
  upsertProjectSummary(selectedProject.value)
}

function appendTemplateField(lines, label, value) {
  splitFilledLines(value).forEach((line) => {
    lines.push(`${label}: ${line}`)
  })
}

function serializeProjectSlides(project) {
  const slides = Array.isArray(project?.slides) ? [...project.slides] : []
  slides.sort((a, b) => Number(a.order || 0) - Number(b.order || 0) || Number(a.id || 0) - Number(b.id || 0))

  return slides
    .map((slide, index) => {
      const lines = [`SLIDE ${slide.order || index + 1} | ${slide.slide_type || 'katex'}`]
      appendTemplateField(lines, 'TITLE', slide.title)
      appendTemplateField(lines, 'TEXT', slide.screen_text)
      appendTemplateField(lines, 'KATEX', slide.katex)
      appendTemplateField(lines, 'VOICE', slide.voice_script)
      return lines.join('\n')
    })
    .join('\n---\n')
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
  const apiMessage = error?.response?.data?.detail || error?.response?.data?.message
  return String(apiMessage || fallback)
}

async function loadVoiceOptions() {
  if (!canManage.value) return

  loadingVoiceOptions.value = true
  voiceOptionsError.value = ''
  try {
    const response = await listReelVoices({
      language: 'fr',
      accent: 'parisian',
    })
    const voices = Array.isArray(response?.data?.voices) ? response.data.voices : []
    voiceOptions.value = voices

    const currentSelectionExists = voices.some((voice) => voice.voice_id === selectedVoiceId.value && voice.api_usable)
    if (!currentSelectionExists) {
      const defaultVoiceId = response?.data?.default_voice_id || ''
      selectedVoiceId.value =
        voices.find((voice) => voice.voice_id === defaultVoiceId && voice.api_usable)?.voice_id ||
        voices.find((voice) => voice.matches_filter && voice.api_usable)?.voice_id ||
        voices.find((voice) => voice.api_usable)?.voice_id ||
        ''
    }

    if (!voices.length) {
      voiceOptionsError.value = 'Aucune voix disponible.'
    } else if (!voices.some((voice) => voice.matches_filter && voice.api_usable)) {
      voiceOptionsError.value = 'Aucune voix parisienne compatible API sur ce compte.'
    }
  } catch (error) {
    voiceOptions.value = []
    selectedVoiceId.value = ''
    voiceOptionsError.value = extractErrorMessage(error, 'Impossible de charger les voix.')
  } finally {
    loadingVoiceOptions.value = false
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

  savingProject.value = true
  try {
    const projectId = editingProject.value?.id
    const response = projectId
      ? await updateReelProject(projectId, payload)
      : await createReelProject({ ...payload, slide_count: 0 })
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
  try {
    const response = await generateSlidesFromTemplate(selectedProject.value.id, payload)
    const updatedProject = normalizeProject(response?.data)

    if (updatedProject?.id) {
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

async function handleGenerateSpeech() {
  if (!selectedProject.value?.id || !canGenerateSpeech.value || !selectedVoiceCanGenerate.value) return

  generatingSpeech.value = true
  try {
    const response = await generateReelSlideSpeeches(selectedProject.value.id, {
      voice_id: selectedVoiceId.value,
    })
    const updatedProject = normalizeProject(response?.data?.project || response?.data)

    if (updatedProject?.id) {
      selectedProject.value = updatedProject
      selectedSlideId.value = updatedProject.slides?.[0]?.id || selectedSlideId.value || null
      templateDraft.value = serializeProjectSlides(updatedProject)
      upsertProjectSummary(updatedProject)
      const count = response?.data?.speech?.generated_count ?? countGeneratedSlideSpeeches(updatedProject)
      setFeedback('success', `Voix par slide generees (${count} MP3).`)
    }
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de generer les voix par slide.'))
  } finally {
    generatingSpeech.value = false
  }
}

async function handleGenerateSlideSpeech(slideId) {
  if (!slideId || !selectedProject.value?.slides) return
  if (!selectedVoiceCanGenerate.value) {
    setFeedback('error', 'Selectionne une voix compatible API.')
    return
  }
  const slide = selectedProject.value.slides.find((item) => Number(item.id) === Number(slideId))
  const speechText = slideSpeechText(slide)
  if (!speechText) {
    setFeedback('error', 'Aucun texte vocal disponible pour cette slide.')
    return
  }

  generatingSpeechSlideId.value = Number(slideId)
  try {
    const response = await generateReelSlideSpeech(slideId, {
      text: speechText,
      voice_id: selectedVoiceId.value,
    })
    const updatedSlide = normalizeProject(response?.data)

    if (updatedSlide?.id) {
      updateSelectedProjectSlide(updatedSlide)
      setFeedback('success', `Voix de la slide ${updatedSlide.order || ''} generee.`.trim())
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
      katex_reset_cumulative: payload.katex_reset_cumulative,
    }

    if (diagnostic?.status) {
      patchData.layout_status = diagnostic.status
      patchData.layout_notes = diagnostic.notes || ''
    }

    const response = await updateReelSlide(payload.id, patchData)
    const updatedSlide = normalizeProject(response?.data)

    if (updatedSlide?.id) {
      const index = selectedProject.value.slides.findIndex((slide) => Number(slide.id) === Number(updatedSlide.id))
      if (index !== -1) {
        selectedProject.value.slides.splice(index, 1, updatedSlide)
      }
      selectedProject.value.updated_at = new Date().toISOString()
      templateDraft.value = serializeProjectSlides(selectedProject.value)
      upsertProjectSummary(selectedProject.value)
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
  selectedProject.value.slides.splice(index, 1, {
    ...selectedProject.value.slides[index],
    ...patchData,
  })

  try {
    const response = await updateReelSlide(payload.id, patchData)
    const updatedSlide = normalizeProject(response?.data)
    if (updatedSlide?.id) {
      selectedProject.value.slides.splice(index, 1, updatedSlide)
      selectedProject.value.updated_at = new Date().toISOString()
      templateDraft.value = serializeProjectSlides(selectedProject.value)
      upsertProjectSummary(selectedProject.value)
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
  min-height: auto;
  flex-shrink: 0;
  scroll-margin-top: 96px;
}

.left-column,
.right-column {
  display: flex;
  flex-direction: column;
  gap: 12px;
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

.speech-panel {
  border: 1px solid #dbe4ee;
  border-radius: 12px;
  background: #ffffff;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.speech-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.speech-toolbar h3 {
  margin: 0;
  color: #0f172a;
  font-size: 18px;
}

.speech-toolbar p {
  margin: 4px 0 0;
  color: #64748b;
  font-size: 13px;
  font-weight: 700;
}

.voice-select {
  min-width: min(100%, 340px);
  display: flex;
  flex-direction: column;
  gap: 5px;
  color: #334155;
  font-size: 12px;
  font-weight: 800;
}

.voice-select select {
  width: 100%;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  background: #ffffff;
  color: #0f172a;
  font: inherit;
  font-size: 13px;
  font-weight: 700;
  padding: 8px 10px;
}

.voice-select select:disabled {
  background: #e2e8f0;
  color: #64748b;
}

.voice-select span {
  color: #64748b;
  font-size: 11px;
  font-weight: 700;
}

.voice-select .voice-warning {
  color: #b45309;
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
}

@media (max-width: 768px) {
  .reel-studio-admin {
    padding: 12px 10px 84px;
  }

  .section-toolbar {
    align-items: stretch;
    flex-direction: column;
  }

  .speech-toolbar {
    align-items: stretch;
    flex-direction: column;
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
