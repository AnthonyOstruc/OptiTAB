import { defineStore } from 'pinia'

const parseDateToTimestamp = (value) => {
  if (!value) return 0
  const ts = new Date(value).getTime()
  return Number.isFinite(ts) ? ts : 0
}

const normalizeStatusValue = (status) => String(
  status?.status ||
  status?.subscription_status ||
  status?.plan_status ||
  status?.stripe_status ||
  ''
).toLowerCase()

const hasActiveSubscription = (status) => {
  if (!status) return false
  const normalizedStatus = normalizeStatusValue(status)
  const now = Date.now()
  const periodEndTs = parseDateToTimestamp(status.current_period_end)
  const hasFuturePeriod = periodEndTs > now

  if (status.is_active || status.subscription_active) return true
  if (['active', 'trialing', 'past_due'].includes(normalizedStatus)) return true
  if (status.cancel_at_period_end && hasFuturePeriod) return true
  if (
    hasFuturePeriod &&
    (
      status.has_subscription ||
      status.subscription_id ||
      status.plan_name ||
      status.plan_stripe_price_id
    )
  ) {
    return true
  }
  if (Array.isArray(status.subscriptions) && status.subscriptions.some(sub => sub?.is_active)) {
    return true
  }
  return false
}

const hasAnyAccess = (status) => {
  if (!status) return false
  if (typeof status.has_access !== 'undefined') {
    return Boolean(status.has_access)
  }

  const passEndTs = parseDateToTimestamp(status.active_pass_ends_at || status.has_active_pass_until)
  const hasFuturePass = passEndTs > Date.now()

  return Boolean(status.has_manual_access) ||
    hasActiveSubscription(status) ||
    Boolean(status.has_active_pass) ||
    hasFuturePass
}

const collectUnlockedLevels = (status) => {
  if (!status) return []
  const seen = new Set()
  const result = []
  const addLevel = (level) => {
    if (!level || level.id == null) return
    const key = Number(level.id)
    if (Number.isNaN(key) || seen.has(key)) return
    seen.add(key)
    result.push(level)
  }
  const list = Array.isArray(status.unlocked_levels) ? status.unlocked_levels : []
  list.forEach(addLevel)
  if (status.subscription_niveau && hasActiveSubscription(status)) {
    addLevel(status.subscription_niveau)
  }
  if (status.has_active_pass && status.pass_niveau) {
    addLevel(status.pass_niveau)
  }
  return result
}

export const useSubscriptionStore = defineStore('subscription', {
  state: () => ({
    status: null,
    loading: false,
    loadedAt: 0,
    error: null
  }),
  getters: {
    hasAccess(state) {
      return hasAnyAccess(state.status)
    },
    isTrial(state) {
      return Boolean(state.status?.is_trial)
    },
    unlockedLevels(state) {
      return collectUnlockedLevels(state.status)
    },
    levelUnlocked(state) {
      return (niveauId) => {
        if (!niveauId) return false
        if (state.status?.has_manual_access) return true
        const targetId = Number(niveauId)
        if (Number.isNaN(targetId)) return false
        return collectUnlockedLevels(state.status).some(level => Number(level.id) === targetId)
      }
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
    },
    async refreshUntilAccess({ attempts = 5, interval = 2000 } = {}) {
      for (let i = 0; i < attempts; i++) {
        await this.fetchStatus({ force: true })
        if (this.hasAccess) {
          return true
        }
        await new Promise(resolve => setTimeout(resolve, interval))
      }
      return this.hasAccess
    }
  }
})
