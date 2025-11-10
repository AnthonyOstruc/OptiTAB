import { defineStore } from 'pinia'
import { createCheckoutSession } from '@/api/subscriptions'
import { useUserStore } from '@/stores/user'

const STORAGE_KEY = 'optitab_checkout_intent'

export const useCheckoutIntentStore = defineStore('checkoutIntent', {
  state: () => ({
    priceId: '',
    niveauId: null,
    planName: '',
    niveauLabel: '',
    source: '',
    createdAt: null,
    processing: false
  }),
  getters: {
    hasIntent(state) {
      return Boolean(state.priceId && state.niveauId)
    }
  },
  actions: {
    initFromStorage() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY)
        if (!raw) return
        const payload = JSON.parse(raw)
        this.priceId = payload.priceId || ''
        this.niveauId = payload.niveauId || null
        this.planName = payload.planName || ''
        this.niveauLabel = payload.niveauLabel || ''
        this.source = payload.source || ''
        this.createdAt = payload.createdAt || null
      } catch (error) {
        console.warn('Impossible de lire le checkout intent stocké:', error)
        this.clearIntent()
      }
    },
    setIntent(payload = {}) {
      this.priceId = payload.priceId || ''
      this.niveauId = payload.niveauId || null
      this.planName = payload.planName || ''
      this.niveauLabel = payload.niveauLabel || ''
      this.source = payload.source || ''
      this.createdAt = new Date().toISOString()
      const data = {
        priceId: this.priceId,
        niveauId: this.niveauId,
        planName: this.planName,
        niveauLabel: this.niveauLabel,
        source: this.source,
        createdAt: this.createdAt
      }
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
    },
    clearIntent() {
      this.priceId = ''
      this.niveauId = null
      this.planName = ''
      this.niveauLabel = ''
      this.source = ''
      this.createdAt = null
      localStorage.removeItem(STORAGE_KEY)
    },
    async processIntent() {
      if (!this.hasIntent || this.processing) {
        return { processed: false }
      }
      const userStore = useUserStore()
      if (!userStore.isAuthenticated) {
        return { processed: false }
      }
      try {
        this.processing = true
        const { data } = await createCheckoutSession(this.priceId, {
          niveau_pays_id: this.niveauId
        })
        const redirectUrl = data?.checkout_url || data?.url
        if (redirectUrl) {
          window.location.href = redirectUrl
          this.clearIntent()
          return { processed: true, redirected: true }
        }
        this.clearIntent()
        return { processed: false, error: 'missing_url' }
      } catch (error) {
        this.clearIntent()
        throw error
      } finally {
        this.processing = false
      }
    }
  }
})
