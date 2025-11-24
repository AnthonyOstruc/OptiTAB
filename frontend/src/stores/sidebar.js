import { defineStore } from 'pinia'

const readBoolean = (key, defaultValue) => {
  if (typeof window === 'undefined') return defaultValue
  const stored = localStorage.getItem(key)
  if (stored === null) return defaultValue
  return stored === 'true'
}

export const useSidebarStore = defineStore('sidebar', {
  state: () => ({
    isOpen: true,
    isCollapsed: false,
    initialized: false,
    channel: null,
  }),

  actions: {
    init() {
      if (this.initialized) return
      this.isOpen = readBoolean('sidebar-open', true)
      this.isCollapsed = readBoolean('sidebar-collapsed', false)

      if (typeof window !== 'undefined') {
        window.addEventListener('storage', this.handleStorage)
        window.addEventListener('focus', this.syncFromStorage)
        document.addEventListener('visibilitychange', this.handleVisibilityChange)
      }

      if (typeof BroadcastChannel !== 'undefined') {
        this.channel = new BroadcastChannel('sidebar-state')
        this.channel.onmessage = (event) => {
          const data = event.data || {}
          if (typeof data.isOpen === 'boolean' && data.isOpen !== this.isOpen) {
            this.isOpen = data.isOpen
          }
          if (typeof data.isCollapsed === 'boolean' && data.isCollapsed !== this.isCollapsed) {
            this.isCollapsed = data.isCollapsed
          }
        }
      }

      this.initialized = true
    },

    syncFromStorage() {
      const nextOpen = readBoolean('sidebar-open', this.isOpen)
      const nextCollapsed = readBoolean('sidebar-collapsed', this.isCollapsed)
      if (nextOpen !== this.isOpen) this.isOpen = nextOpen
      if (nextCollapsed !== this.isCollapsed) this.isCollapsed = nextCollapsed
    },

    handleStorage(event) {
      if (!event || event.storageArea !== localStorage) return
      if (event.key === 'sidebar-open' || event.key === 'sidebar-collapsed') {
        this.syncFromStorage()
      }
    },

    handleVisibilityChange() {
      if (document.visibilityState === 'visible') {
        this.syncFromStorage()
      }
    },

    setOpen(value) {
      if (this.isOpen === value) return
      this.isOpen = value
      if (typeof window !== 'undefined') {
        localStorage.setItem('sidebar-open', value.toString())
      }
      this.broadcastState()
    },

    toggleOpen() {
      this.setOpen(!this.isOpen)
    },

    setCollapsed(value) {
      if (this.isCollapsed === value) return
      this.isCollapsed = value
      if (typeof window !== 'undefined') {
        localStorage.setItem('sidebar-collapsed', value.toString())
      }
      this.broadcastState()
    },

    toggleCollapsed() {
      this.setCollapsed(!this.isCollapsed)
    },

    broadcastState() {
      if (this.channel) {
        this.channel.postMessage({
          isOpen: this.isOpen,
          isCollapsed: this.isCollapsed,
        })
      }
    },
  },
})
