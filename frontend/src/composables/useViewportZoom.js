import { watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'

/**
 * Composable pour gérer le zoom du viewport sur mobile
 * Désactive le zoom sur les pages protégées (requiresAuth) quand l'utilisateur est connecté
 * Pour préserver l'intégrité du header et footer sur mobile
 */
export function useViewportZoom() {
  const route = useRoute()
  const userStore = useUserStore()
  
  // Viewport par défaut (avec zoom activé)
  const defaultViewport = 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes, viewport-fit=cover'
  
  // Viewport sans zoom (pour pages protégées sur mobile)
  const noZoomViewport = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover'
  
  /**
   * Détecte si on est sur un appareil mobile
   */
  const isMobile = () => {
    if (typeof window === 'undefined') return false
    const userAgent = navigator.userAgent.toLowerCase()
    const isMobileUA = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini|mobile/i.test(userAgent)
    const isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0)
    const hasSmallScreen = window.innerWidth <= 768
    return isMobileUA || (isTouchDevice && hasSmallScreen)
  }
  
  /**
   * Met à jour le viewport meta tag
   */
  const updateViewport = () => {
    if (typeof document === 'undefined') return
    
    const viewportMeta = document.querySelector('meta[name="viewport"]')
    if (!viewportMeta) return
    
    // Désactiver le zoom uniquement si:
    // 1. On est sur mobile
    // 2. L'utilisateur est connecté
    // 3. La route requiert l'authentification
    const shouldDisableZoom = isMobile() && 
                              userStore.isAuthenticated && 
                              route.meta?.requiresAuth === true
    
    const newViewport = shouldDisableZoom ? noZoomViewport : defaultViewport
    
    if (viewportMeta.getAttribute('content') !== newViewport) {
      viewportMeta.setAttribute('content', newViewport)
    }
  }
  
  // Watcher pour les changements de route et d'authentification
  watch(
    [() => route.path, () => route.meta, () => userStore.isAuthenticated],
    () => {
      updateViewport()
    },
    { immediate: true }
  )
  
  // Mettre à jour au montage
  onMounted(() => {
    updateViewport()
    
    // Écouter les changements de taille de fenêtre (rotation d'écran)
    if (typeof window !== 'undefined') {
      window.addEventListener('resize', updateViewport)
      window.addEventListener('orientationchange', updateViewport)
    }
  })
  
  onUnmounted(() => {
    if (typeof window !== 'undefined') {
      window.removeEventListener('resize', updateViewport)
      window.removeEventListener('orientationchange', updateViewport)
    }
  })
  
  return {
    updateViewport,
    isMobile
  }
}
