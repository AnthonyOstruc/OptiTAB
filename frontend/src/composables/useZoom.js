import { ref, computed, nextTick } from 'vue'

/**
 * Composable pour gérer le zoom responsive avec fallback mobile
 * Détecte le support du zoom natif et utilise transform comme fallback sur mobile
 */
export function useZoom(options = {}) {
  const { computeAutoZoom: computeAutoZoomOverride } = options
  const viewportWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1920)
  const contentHeight = ref(0)
  const isMobileDevice = ref(false)
  const supportsNativeZoom = ref(false)

  function detectMobileAndZoomSupport() {
    if (typeof window === 'undefined') return
    
    // Détection mobile plus précise
    const userAgent = navigator.userAgent.toLowerCase()
    const isMobile = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini|mobile/i.test(userAgent)
    const isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0)
    const hasSmallScreen = window.innerWidth <= 768
    
    isMobileDevice.value = isMobile || (isTouchDevice && hasSmallScreen)
    
    // Test plus robuste du support du zoom natif
    let zoomSupported = false
    try {
      // Créer un élément de test
      const testEl = document.createElement('div')
      testEl.style.cssText = 'position:absolute;left:-9999px;top:-9999px;zoom:1.5;'
      document.body.appendChild(testEl)
      
      // Vérifier si le zoom fonctionne réellement
      const rect = testEl.getBoundingClientRect()
      testEl.style.zoom = '2'
      const newRect = testEl.getBoundingClientRect()
      
      // Le zoom fonctionne si les dimensions changent proportionnellement
      zoomSupported = Math.abs(newRect.width - rect.width * (2/1.5)) < 1
      
      document.body.removeChild(testEl)
    } catch (e) {
      zoomSupported = false
    }
    
    // Sur mobile, toujours utiliser transform même si zoom est "supporté"
    supportsNativeZoom.value = zoomSupported && !isMobileDevice.value
    
    console.log('[Zoom Detection]', {
      isMobile: isMobileDevice.value,
      zoomSupported,
      willUseNativeZoom: supportsNativeZoom.value
    })
  }

  function defaultComputeAutoZoom(width) {
    if (width >= 1400) return 1
    if (width >= 1200) return 0.95
    if (width >= 1024) return 0.9
    if (width >= 900) return 0.85
    if (width >= 768) return 0.8
    if (width >= 640) return 0.78
    if (width >= 520) return 0.76
    if (width >= 420) return 0.74
    return 0.72
  }

  const computeZoom = typeof computeAutoZoomOverride === 'function' ? computeAutoZoomOverride : defaultComputeAutoZoom
  const zoomLevel = computed(() => computeZoom(viewportWidth.value))

  function createZoomStyle(options = {}) {
    const {
      cssVar = '--content-zoom',
      heightVar = '--content-height',
      mobileZoomAdjustment = null,
      minMobileZoom = 0.45
    } = options

    return computed(() => {
      const baseHeight = `${contentHeight.value}px`
      let z = zoomLevel.value || 1
      
      // Ajustement mobile personnalisable
      if (viewportWidth.value <= 768) {
        if (mobileZoomAdjustment) {
          z = mobileZoomAdjustment(z)
        } else {
          z = Math.max(minMobileZoom, z * 0.75)
        }
      }
      
      const widthPercent = (100 / z).toFixed(3)
      
      const baseStyle = {
        [cssVar]: z,
        [heightVar]: baseHeight,
        '--use-native-zoom': supportsNativeZoom.value ? '1' : '0'
      }
      
      if (supportsNativeZoom.value) {
        // Utiliser le zoom natif uniquement si vraiment supporté
        return {
          ...baseStyle,
          zoom: z,
          transform: 'none',
          width: '100%',
          height: 'auto'
        }
      } else {
        // Fallback transform pour mobile et navigateurs sans support zoom
        const style = {
          ...baseStyle,
          transform: `scale(${z})`,
          transformOrigin: 'top left',
          width: `${widthPercent}%`,
          height: 'auto',
          minHeight: 'auto'
        }
        
        // Seulement appliquer la hauteur si elle est mesurée et valide
        if (contentHeight.value > 0 && Number.isFinite(z) && z < 1) {
          const marginBottom = -Math.round(contentHeight.value * (1 - z))
          style.marginBottom = `${marginBottom}px`
        }
        
        return style
      }
    })
  }

  function updateViewportWidth() {
    if (typeof window === 'undefined') return
    viewportWidth.value = window.innerWidth
  }

  function measureContentHeight(elementRef) {
    if (!elementRef?.value) {
      contentHeight.value = 0
      return
    }
    contentHeight.value = elementRef.value.scrollHeight || elementRef.value.offsetHeight || 0
  }

  // Setup des event listeners
  function setupViewportListener() {
    if (typeof window !== 'undefined') {
      window.addEventListener('resize', updateViewportWidth, { passive: true })
    }
  }

  function cleanupViewportListener() {
    if (typeof window !== 'undefined') {
      window.removeEventListener('resize', updateViewportWidth)
    }
  }

  return {
    viewportWidth,
    contentHeight,
    isMobileDevice,
    supportsNativeZoom,
    zoomLevel,
    detectMobileAndZoomSupport,
    createZoomStyle,
    updateViewportWidth,
    measureContentHeight,
    setupViewportListener,
    cleanupViewportListener
  }
}
