import { defineStore } from 'pinia'
import {
  getArenaConfig,
  getArenaMe,
  getArenaChapters,
  getArenaChapter,
  getArenaLevelPlay,
  submitArenaAttempt,
  getArenaDaily,
  getArenaForge,
  trackArenaEvent,
} from '@/api/arena'

const initialState = () => ({
  config: null,
  configLoaded: false,
  me: null,
  chapters: [],
  currentChapter: null,
  currentLevel: null,
  currentQuestions: [],
  daily: null,
  forge: null,
  loading: false,
  error: null,
  lastResult: null,
  cta: null,
})

export const useArenaStore = defineStore('arena', {
  state: initialState,

  getters: {
    isPublic: (s) => !!(s.config && s.config.is_public),
    isAdminPreview: (s) => !!(s.config && s.config.admin_preview),
    isAccessible: (s) => !!(s.config && (s.config.is_public || s.config.admin_preview)),
    isPremium: (s) => !!(s.me && s.me.is_premium),
    streak: (s) => s.me?.state?.current_streak ?? 0,
    bestStreak: (s) => s.me?.state?.best_streak ?? 0,
    xp: (s) => s.me?.user_xp ?? 0,
  },

  actions: {
    async loadConfig() {
      try {
        const { data } = await getArenaConfig()
        this.config = data
        this.configLoaded = true
      } catch (e) {
        this.config = null
        this.configLoaded = true
      }
    },
    async loadMe() {
      try {
        const { data } = await getArenaMe()
        this.me = data
      } catch (e) {
        this.me = null
      }
    },
    async loadChapters() {
      this.loading = true
      try {
        const { data } = await getArenaChapters()
        this.chapters = Array.isArray(data) ? data : (data?.results || [])
      } finally {
        this.loading = false
      }
    },
    async loadChapter(slug) {
      this.loading = true
      try {
        const { data } = await getArenaChapter(slug)
        this.currentChapter = data
      } finally {
        this.loading = false
      }
    },
    async loadLevel(levelId) {
      this.loading = true
      this.cta = null
      try {
        const { data } = await getArenaLevelPlay(levelId)
        this.currentLevel = data?.level || null
        this.currentQuestions = data?.questions || []
        return data
      } catch (e) {
        if (e?.response?.status === 402 && e.response.data?.cta) {
          this.cta = e.response.data.cta
        }
        throw e
      } finally {
        this.loading = false
      }
    },
    async submitAttempt(levelId, payload) {
      this.loading = true
      try {
        const { data } = await submitArenaAttempt(levelId, payload)
        this.lastResult = data
        // Don't auto-open the modal: the result screen renders the CTA inline
        // contextually. The modal is reserved for hard gates (locked level,
        // daily limit reached) that interrupt navigation, not for post-attempt
        // moments where the user has earned feedback first.
        // Refresh user state so XP/streak update everywhere.
        this.loadMe().catch(() => {})
        return data
      } finally {
        this.loading = false
      }
    },
    async loadDaily() {
      try {
        const { data } = await getArenaDaily()
        this.daily = data
      } catch (e) {
        this.daily = null
      }
    },
    async loadForge() {
      try {
        const { data } = await getArenaForge()
        this.forge = data
      } catch (e) {
        this.forge = null
      }
    },
    async track(name, payload = {}) {
      try {
        await trackArenaEvent(name, payload)
      } catch (_) {
        // Analytics is best-effort.
      }
    },
    showCta(cta) {
      this.cta = cta
    },
    dismissCta() {
      this.cta = null
    },
    reset() {
      Object.assign(this, initialState())
    },
  },
})
