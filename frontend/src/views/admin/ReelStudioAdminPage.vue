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

    <section v-else class="content-grid">
      <section class="right-column">
        <p v-if="loadingProjectDetail" class="loading-state">Chargement du projet...</p>

        <template v-else>
          <ReelTemplateBuilder
            :loading="generatingTemplate"
            :disabled="!selectedProject"
            @generate="handleGenerateFromTemplate"
          />

          <ReelPreview
            :slides="selectedProject?.slides || []"
            :selected-slide-id="selectedSlideId"
            @select-slide="selectedSlideId = $event"
            @diagnostic="handleSlideDiagnostic"
            @update-slide="handlePatchSlide"
          />

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
  </main>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useUserStore } from '@/stores/user'
import {
  createReelProject,
  deleteReelSlide,
  generateSlidesFromTemplate,
  getReelProject,
  listReelProjects,
  updateReelSlide,
} from '@/api/reelStudio'
import ReelPreview from '@/components/admin/reel-studio/ReelPreview.vue'
import ReelSlideEditor from '@/components/admin/reel-studio/ReelSlideEditor.vue'
import ReelTemplateBuilder from '@/components/admin/reel-studio/ReelTemplateBuilder.vue'
import FormatHelp from '@/components/admin/FormatHelp.vue'

const userStore = useUserStore()
const canManage = computed(() => Boolean(userStore.isAdmin))

const projects = ref([])
const selectedProjectId = ref(null)
const selectedProject = ref(null)
const selectedSlideId = ref(null)

const loadingProjectDetail = ref(false)
const generatingTemplate = ref(false)
const savingSlide = ref(false)
const showManualEditor = ref(false)

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
VOICE: Défi express: simplifie cette expression.
---
SLIDE 2 | katex
TITLE: Dérivation produit
TEXT: Correction :
KATEX: f(x)=x\\ln(x)
VOICE: On part de f de x égale x ln x.
---
SLIDE 3 | cumulative_katex
KATEX: u=x \\qquad v=\\ln(x)
VOICE: On reconnaît un produit.
---
SLIDE 4 | cumulative_katex
KATEX: u'=1 \\qquad v'=\\frac{1}{x}
VOICE: On dérive chaque facteur.
---
SLIDE 5 | result
TITLE: Résultat
KATEX: f'(x)=u'v+uv'
KATEX: f'(x)=\\ln(x)+1
VOICE: Résultat final: ln de x plus un.
---
SLIDE 6 | cta
TITLE: Résultat
KATEX: f'(x)=\\ln(x)+1
TEXT: Abonne-toi à OptiTAB
Sauvegarde ce Reel
Commente ton résultat
VOICE: Abonne-toi pour la suite.
`

const selectedSlide = computed(() => {
  if (!selectedProject.value?.slides?.length) return null
  return selectedProject.value.slides.find((slide) => Number(slide.id) === Number(selectedSlideId.value)) || null
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
    slide_count: project.slide_count,
    status: project.status,
    created_at: project.created_at,
    updated_at: project.updated_at,
  }

  const idx = projects.value.findIndex((item) => Number(item.id) === Number(summary.id))
  if (idx === -1) {
    projects.value = [summary, ...projects.value]
    return
  }

  projects.value.splice(idx, 1, summary)
}

function extractErrorMessage(error, fallback) {
  const apiMessage = error?.response?.data?.detail || error?.response?.data?.message
  return String(apiMessage || fallback)
}

async function loadProjects() {
  if (!canManage.value) return

  try {
    const response = await listReelProjects()
    projects.value = normalizeProjectsList(response?.data)

    if (!projects.value.length) {
      const autoProjectResponse = await createReelProject({
        title: `Reel Studio - ${new Date().toISOString().slice(0, 10)}`,
        theme: 'OptiTAB',
        level: 'Terminale',
        format_type: 'Correction pas à pas',
        target_duration_seconds: 30,
        slide_count: 6,
      })
      const autoProject = normalizeProject(autoProjectResponse?.data)
      if (autoProject?.id) {
        upsertProjectSummary(autoProject)
        selectedProject.value = autoProject
        selectedProjectId.value = Number(autoProject.id)
        selectedSlideId.value = autoProject?.slides?.[0]?.id || null
      }
      return
    }

    const selectedStillExists = projects.value.some((project) => Number(project.id) === Number(selectedProjectId.value))
    const nextId = selectedStillExists ? selectedProjectId.value : projects.value[0].id
    await selectProject(nextId)
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de charger les projets Reel Studio.'))
  }
}

async function selectProject(projectId) {
  if (!projectId || !canManage.value) return

  selectedProjectId.value = Number(projectId)
  loadingProjectDetail.value = true
  const requestId = ++detailRequestId

  try {
    const response = await getReelProject(projectId)
    if (requestId !== detailRequestId) return

    const project = normalizeProject(response?.data)
    selectedProject.value = project
    selectedSlideId.value = project?.slides?.[0]?.id || null
    clearDiagnostics()
    upsertProjectSummary(project)
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de charger le projet sélectionné.'))
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
    }
  } catch (error) {
    selectedProject.value.slides.splice(index, 1, previousSlide)
    setFeedback('error', extractErrorMessage(error, 'Impossible de sauvegarder la disposition KaTeX.'))
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
  loadProjects()
})
</script>

<style src="@/styles/admin-common.css"></style>
<style scoped>
.reel-studio-admin {
  width: 100%;
  min-height: 100%;
  padding: 16px;
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

.content-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 14px;
  min-height: 0;
}

.left-column,
.right-column {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 0;
}

.loading-state {
  margin: 0;
  color: #475569;
  font-size: 14px;
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

  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .page-header h1 {
    font-size: 22px;
  }
}
</style>
