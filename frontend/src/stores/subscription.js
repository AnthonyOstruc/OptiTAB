import { defineStore } from 'pinia'

export const useSubscriptionStore = defineStore('subscription', {
  state: () => ({
    status: null,
    loading: false,
    loadedAt: 0,
    error: null
  }),
  getters: {
    hasAccess(state) {
      const status = state.status
      if (!status) return false
      if (status.has_access !== undefined) {
        return Boolean(status.has_access)
      }
      // Fallback: combine abonnement actif OU pass actif OU accès manuel
      return Boolean(
        (status.has_manual_access ?? false) ||
        (status.is_active ?? false) ||
        (status.has_active_pass ?? false)
      )
    },
    isTrial(state) {
      return Boolean(state.status?.is_trial)
    }
  },
  actions: {
    async fetchStatus({ force = false } = {}) {
      if (this.loading) return
      const now = Date.now()
      if (!force && this.status && now - this.loadedAt < 60_000) {
        return
      }
      this.loading = true
      this.error = null
      try {
        const { getSubscriptionStatus } = await import('@/api/subscriptions')
        const response = await getSubscriptionStatus()
        this.status = response.data
        this.loadedAt = Date.now()
      } catch (error) {
        this.error = error
        this.status = null
      } finally {
        this.loading = false
      }
    },
    clear() {
      this.status = null
      this.error = null
      this.loadedAt = 0
      this.loading = false
    }
  }
})
