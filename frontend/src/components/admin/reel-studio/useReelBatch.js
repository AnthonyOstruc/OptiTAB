import { computed, nextTick, reactive, ref, watch } from 'vue'
import { createReelBatch, exportReelVideo, generateReelSlideSpeeches, getReelProject, saveReelTemplate } from '@/api/reelStudio'
import { runReelQueue } from './reelBatch'

// A timeout does not mean the server stopped generating. Do not automatically
// resend expensive batch operations through the API client's network retries.
const GENERATION_CONFIG = { __networkRetryChainActive: true }

export function useReelBatch({ projects, selectedProject, templateDraft, previewRef, selectProject, serializeProject,
  upsertProject, normalizeProject, normalizeList, speechPayload, downloadVideo, setFeedback, errorMessage, isBlocked, refreshVoices }) {
  const activeBatchId = ref('')
  const importing = ref(false)
  const downloading = ref(false)
  const selecting = ref(false)
  const failedDownloads = new Set()
  const skipReady = ref(true)
  const queue = reactive({ running: false, stopRequested: false, phase: '', currentTitle: '', completed: 0, total: 0, message: '', results: {} })
  const batches = computed(() => {
    const groups = new Map()
    for (const project of projects.value) {
      if (!project.batch_id) continue
      if (!groups.has(project.batch_id)) groups.set(project.batch_id, { id: project.batch_id, title: project.batch_title, projects: [] })
      groups.get(project.batch_id).projects.push(project)
    }
    for (const group of groups.values()) group.projects.sort((a, b) => a.batch_order - b.batch_order || a.id - b.id)
    return [...groups.values()]
  })
  const currentProjects = computed(() => batches.value.find(batch => batch.id === activeBatchId.value)?.projects || [])
  const dirty = computed(() => Boolean(selectedProject.value?.batch_id && templateDraft.value !== serializeProject(selectedProject.value)))
  watch(batches, (value) => {
    if (!value.some(batch => batch.id === activeBatchId.value)) activeBatchId.value = value[0]?.id || ''
  }, { immediate: true })

  async function saveDraft() {
    if (!dirty.value) return
    if (!templateDraft.value.trim()) throw new Error('Le script est vide. Ajoutez un script avant de changer de reel.')
    const response = await saveReelTemplate(selectedProject.value.id, { template_text: templateDraft.value })
    const project = normalizeProject(response.data)
    if (!project?.id) throw new Error('La sauvegarde du reel n’a pas été confirmée.')
    selectedProject.value = project
    templateDraft.value = serializeProject(project)
    upsertProject(project)
  }

  async function loadProject(id) {
    const project = await selectProject(id)
    if (!project?.id) throw new Error('Impossible de charger ce reel. Réessayez avant de continuer.')
    templateDraft.value = serializeProject(project)
    await nextTick()
    return project
  }

  async function selectReel(id) {
    if (isBlocked()) return
    selecting.value = true
    try { await saveDraft(); await loadProject(id) }
    catch (error) { setFeedback('error', errorMessage(error, error.message || 'Impossible de changer de reel.')) }
    finally { selecting.value = false }
  }

  async function selectBatch(id) {
    if (isBlocked()) return
    selecting.value = true
    try {
      await saveDraft()
      const first = batches.value.find(batch => batch.id === id)?.projects[0]
      if (first) await loadProject(first.id)
      if (id !== activeBatchId.value) Object.assign(queue, { phase: '', results: {}, completed: 0, total: 0 })
      activeBatchId.value = id
    } catch (error) { setFeedback('error', errorMessage(error, error.message || 'Impossible de changer de série.')) }
    finally { selecting.value = false }
  }

  async function importBatch(payload, done) {
    if (isBlocked()) return
    importing.value = true
    try {
      await saveDraft()
      const response = await createReelBatch(payload)
      const created = normalizeList(response.data)
      if (!created.length) throw new Error('La création de la série n’a pas été confirmée.')
      created.forEach(upsertProject)
      activeBatchId.value = created[0].batch_id
      Object.assign(queue, { phase: '', results: {}, completed: 0, total: 0 })
      await loadProject(created[0].id)
      setFeedback('success', `${created.length} reels créés. Vous pouvez modifier chaque reel dans son onglet.`)
      done?.()
    } catch (error) {
      const message = errorMessage(error, error.message || 'Impossible de créer la série.')
      setFeedback('error', message)
      done?.(message)
    } finally { importing.value = false }
  }

  async function run(phase) {
    if (isBlocked() || !currentProjects.value.length || !['speech', 'video'].includes(phase)) return
    const items = [...currentProjects.value]
    const settings = speechPayload()
    const resume = skipReady.value
    const initialProjectId = selectedProject.value?.id
    let draftSaved = false
    Object.assign(queue, { running: true, stopRequested: false, phase, currentTitle: 'Sauvegarde…', completed: 0, total: items.length, message: '', results: {} })
    try {
      await saveDraft()
      draftSaved = true
      await runReelQueue(items, {
        shouldStop: () => queue.stopRequested,
        onStart: (item) => {
          queue.currentTitle = item.title
          queue.results[item.id] = { status: 'running', message: phase === 'speech' ? 'Voix en cours…' : 'Vidéo en cours…' }
        },
        process: async (item) => {
          const detail = normalizeProject((await getReelProject(item.id)).data)
          if (!detail?.slides?.length) throw new Error('Ce reel ne contient aucune slide.')
          upsertProject(detail)
          if (phase === 'speech') {
            const allSlideVoicesReady = detail.slides.every(slide => {
              const hasSpeech = [slide.voice_script, slide.title, slide.screen_text].some(value => String(value || '').trim())
              return !hasSpeech || (slide.speech_status === 'ready' && Boolean(slide.speech_audio_url))
            })
            if (resume && allSlideVoicesReady && detail.speech_status === 'ready' && detail.speech_voice_id === settings.voice_id) return
            const response = await generateReelSlideSpeeches(item.id, settings, GENERATION_CONFIG)
            const body = normalizeProject(response.data)
            const project = body?.project || body
            if (!project?.id || project.speech_status !== 'ready') throw new Error('Les voix de ce reel ne sont pas toutes prêtes.')
            upsertProject(project)
          } else {
            if (resume && detail.video_status === 'ready' && detail.video_file_url) {
              if (failedDownloads.has(item.id)) {
                await downloadVideo(detail, detail.video_file_url)
                failedDownloads.delete(item.id)
                queue.results[item.id].message = 'Téléchargement…'
                return
              }
              queue.results[item.id].message = 'Vidéo déjà prête'
              return
            }
            await loadProject(item.id)
            if (!previewRef.value) throw new Error('L’aperçu du reel n’est pas disponible.')
            const payload = await previewRef.value.prepareVideoExport()
            if (!payload?.frames?.length) throw new Error('Les images du reel n’ont pas pu être préparées.')
            const body = normalizeProject((await exportReelVideo(item.id, payload, GENERATION_CONFIG)).data)
            const project = body?.project || body
            if (!project?.id || project.video_status !== 'ready') throw new Error('La création de la vidéo n’a pas été confirmée.')
            upsertProject(project)
            queue.results[item.id].message = 'Téléchargement…'
            failedDownloads.add(item.id)
            await downloadVideo(project, body?.video?.url || project.video_file_url)
            failedDownloads.delete(item.id)
          }
        },
        onSuccess: (item) => {
          queue.completed += 1
          const previousMessage = queue.results[item.id].message
          queue.results[item.id] = { status: 'success', message: phase === 'speech' ? 'Voix prêtes' : (previousMessage === 'Vidéo déjà prête' ? previousMessage : 'MP4 prêt · téléchargement lancé') }
        },
        onError: (item, error) => {
          const message = !error.response && ['ECONNABORTED', 'ERR_NETWORK'].includes(error.code)
            ? 'Connexion interrompue. Le serveur peut encore travailler : attendez puis vérifiez le reel avant de reprendre.'
            : errorMessage(error, error.message || 'La génération a échoué.')
          queue.results[item.id] = { status: 'error', message }
          queue.message = 'Série en pause · une erreur à corriger'
          setFeedback('error', `${item.title} : ${message}`)
        },
      })
      if (!queue.message) queue.message = queue.completed === queue.total ? 'Série terminée' : 'Série arrêtée · prête à reprendre'
    } catch (error) {
      queue.message = 'Série en pause'
      setFeedback('error', errorMessage(error, error.message || 'Impossible de lancer la série.'))
    } finally {
      // Restore the reel being edited, with fresh audio/video state from the server.
      if (initialProjectId && draftSaved) {
        try { await loadProject(initialProjectId) }
        catch { /* The original queue result remains visible. */ }
      }
      if (phase === 'speech') await refreshVoices()
      queue.running = false
      queue.currentTitle = ''
    }
  }

  async function download(project) {
    if (isBlocked()) return
    downloading.value = true
    try { await downloadVideo(project, project.video_file_url) }
    catch (error) { setFeedback('error', errorMessage(error, 'Impossible de télécharger le MP4.')) }
    finally { downloading.value = false }
  }

  return reactive({ batches, currentProjects, activeBatchId, importing, downloading, selecting, skipReady, queue, dirty,
    saveDraft, selectReel, selectBatch, importBatch, run, download, stop: () => { queue.stopRequested = true } })
}
