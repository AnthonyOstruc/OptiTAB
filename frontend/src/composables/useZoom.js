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
  let observedElement = null
  let resizeObserver = null
  let measureRaf = null

  function readElementHeight(el) {
    if (!el) return 0
    const scrollHeight = el.scrollHeight || 0
    const offsetHeight = el.offsetHeight || 0
    const rectHeight = typeof el.getBoundingClientRect === 'function'
      ? Math.ceil(el.getBoundingClientRect().height || 0)
      : 0
    return Math.max(scrollHeight, offsetHeight, rectHeight)
  }

  function cancelScheduledMeasure() {
    if (!measureRaf) return
    if (typeof cancelAnimationFrame === 'function') {
      cancelAnimationFrame(measureRaf)
    } else {
      clearTimeout(measureRaf)
    }
    measureRaf = null
  }

  function scheduleObservedHeightUpdate() {
    if (!observedElement) return
    cancelScheduledMeasure()
    if (typeof requestAnimationFrame === 'function') {
      measureRaf = requestAnimationFrame(() => {
        measureRaf = null
        contentHeight.value = readElementHeight(observedElement)
      })
      return
    }
    measureRaf = setTimeout(() => {
      measureRaf = null
      contentHeight.value = readElementHeight(observedElement)
    }, 0)
  }

  function stopContentObserver() {
    cancelScheduledMeasure()
    if (resizeObserver) {
      try {
        resizeObserver.disconnect()
      } catch (_) {}
      resizeObserver = null
    }
    observedElement = null
  }

  function detectMobileAndZoomSupport() {
    if (typeof window === 'undefined') return
    
    // Détection mobile plus précise
    const userAgent = navigator.userAgent.toLowerCase()
    const isMobile = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini|mobile/i.test(userAgent)
    const isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0)
    const hasSmallScreen = window.innerWidth <= 768
    
    isMobileDevice.value = isMobile || (isTouchDevice && hasSmallScreen)
    
    // Détection du support natif zoom:
    // 1) CSS.supports pour les moteurs modernes
    // 2) fallback via mesure réelle en cas de doute
    let zoomSupported = false
    try {
      if (typeof CSS !== 'undefined' && typeof CSS.supports === 'function') {
        zoomSupported = CSS.supports('zoom: 1') || CSS.supports('zoom', '1')
      }
    } catch (_) {
      zoomSupported = false
    }

    if (!zoomSupported) {
      try {
        const testEl = document.createElement('div')
        testEl.style.cssText = 'position:absolute;left:-9999px;top:-9999px;width:100px;height:100px;zoom:2;'
        document.body.appendChild(testEl)

        const rect = testEl.getBoundingClientRect()
        zoomSupported = rect.width >= 190 // ~200px si zoom fonctionne, ~100px sinon

        document.body.removeChild(testEl)
      } catch (_) {
        zoomSupported = false
      }
    }
    
    // En 2025+, le CSS zoom est supporté nativement par tous les navigateurs
    // (Safari, Chrome, Firefox 126+). On l'utilise aussi sur mobile pour éviter
    // les problèmes de hauteur causés par transform: scale().
    supportsNativeZoom.value = zoomSupported
    
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
    const element = elementRef?.value || elementRef
    if (!element) {
      stopContentObserver()
      contentHeight.value = 0
      return
    }
    contentHeight.value = readElementHeight(element)

    if (typeof ResizeObserver === 'undefined') return
    if (observedElement === element && resizeObserver) return

    stopContentObserver()
    observedElement = element
    resizeObserver = new ResizeObserver(() => {
      scheduleObservedHeightUpdate()
    })
    resizeObserver.observe(element)
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
    stopContentObserver()
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
