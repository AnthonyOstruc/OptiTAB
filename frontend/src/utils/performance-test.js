/**
 * Utilitaire de test de performance pour mesurer l'impact des optimisations
 * Usage: Importer dans la console du navigateur et exécuter les fonctions
 */

/**
 * Mesure le temps de chargement d'une page
 * @param {string} url - URL à tester
 * @returns {Promise<Object>} - Statistiques de performance
 */
export async function measurePageLoad(url) {
  const start = performance.now()
  
  // Attendre que la page soit complètement chargée
  await new Promise((resolve) => {
    window.addEventListener('load', resolve, { once: true })
  })
  
  const end = performance.now()
  const loadTime = end - start
  
  return {
    url,
    loadTime: Math.round(loadTime),
    navigationTiming: performance.getEntriesByType('navigation')[0],
    resourceTiming: performance.getEntriesByType('resource')
  }
}

/**
 * Teste le temps de réponse de l'API avec et sans cache
 * @param {string} endpoint - Endpoint à tester
 * @param {Object} params - Paramètres de la requête
 * @returns {Promise<Object>} - Statistiques de temps de réponse
 */
export async function testApiCache(endpoint, params = {}) {
  const results = {
    endpoint,
    params,
    firstCall: null,
    cachedCall: null,
    improvement: null
  }
  
  // Nettoyer le cache avant le test
  if (window.__API_RESPONSE_CACHE__) {
    window.__API_RESPONSE_CACHE__.clear()
  }
  
  // Premier appel (sans cache)
  const start1 = performance.now()
  try {
    const response1 = await fetch(endpoint + '?' + new URLSearchParams(params))
    await response1.json()
    const end1 = performance.now()
    results.firstCall = Math.round(end1 - start1)
  } catch (error) {
    results.error = error.message
    return results
  }
  
  // Attendre un peu pour simuler une vraie navigation
  await new Promise(resolve => setTimeout(resolve, 100))
  
  // Deuxième appel (avec cache)
  const start2 = performance.now()
  try {
    const response2 = await fetch(endpoint + '?' + new URLSearchParams(params))
    await response2.json()
    const end2 = performance.now()
    results.cachedCall = Math.round(end2 - start2)
  } catch (error) {
    results.error = error.message
    return results
  }
  
  // Calculer l'amélioration
  results.improvement = Math.round(((results.firstCall - results.cachedCall) / results.firstCall) * 100)
  
  return results
}

/**
 * Teste la vitesse de prefetch au survol
 * @param {string} matiereId - ID de la matière à précharger
 * @returns {Promise<Object>} - Statistiques de prefetch
 */
export async function testPrefetch(matiereId) {
  const results = {
    matiereId,
    prefetchTime: null,
    navigationTime: null,
    totalTime: null
  }
  
  // Nettoyer le cache
  if (window.__API_RESPONSE_CACHE__) {
    window.__API_RESPONSE_CACHE__.clear()
  }
  
  // Simuler le prefetch (comme au survol)
  const prefetchStart = performance.now()
  try {
    const { useDataPrefetch } = await import('@/composables/useDataPrefetch')
    const { prefetchThemesNotions } = useDataPrefetch()
    await prefetchThemesNotions(matiereId)
    const prefetchEnd = performance.now()
    results.prefetchTime = Math.round(prefetchEnd - prefetchStart)
  } catch (error) {
    results.error = error.message
    return results
  }
  
  // Simuler la navigation (les données devraient être en cache)
  const navStart = performance.now()
  try {
    const { useDataPrefetch } = await import('@/composables/useDataPrefetch')
    const { prefetchThemesNotions } = useDataPrefetch()
    await prefetchThemesNotions(matiereId) // Devrait être instantané (cache)
    const navEnd = performance.now()
    results.navigationTime = Math.round(navEnd - navStart)
  } catch (error) {
    results.error = error.message
    return results
  }
  
  results.totalTime = results.prefetchTime + results.navigationTime
  
  return results
}

/**
 * Compare les performances avant/après optimisation
 * @param {string} matiereId - ID de la matière à tester
 * @returns {Promise<Object>} - Rapport comparatif
 */
export async function comparePerformance(matiereId) {
  console.log('🧪 Test de performance en cours...')
  
  const report = {
    matiereId,
    withoutPrefetch: null,
    withPrefetch: null,
    improvement: null
  }
  
  // Test SANS prefetch (simulation)
  console.log('📊 Test 1/2: Sans préchargement...')
  if (window.__API_RESPONSE_CACHE__) {
    window.__API_RESPONSE_CACHE__.clear()
  }
  
  const start1 = performance.now()
  try {
    const response = await fetch(`/api/themes/notions-pour-utilisateur/?matiere=${matiereId}`)
    await response.json()
    const end1 = performance.now()
    report.withoutPrefetch = Math.round(end1 - start1)
  } catch (error) {
    console.error('❌ Erreur test 1:', error)
    return report
  }
  
  // Attendre un peu
  await new Promise(resolve => setTimeout(resolve, 500))
  
  // Test AVEC prefetch
  console.log('📊 Test 2/2: Avec préchargement...')
  const prefetchResult = await testPrefetch(matiereId)
  report.withPrefetch = prefetchResult.navigationTime || prefetchResult.totalTime
  
  // Calculer l'amélioration
  if (report.withoutPrefetch && report.withPrefetch) {
    report.improvement = Math.round(((report.withoutPrefetch - report.withPrefetch) / report.withoutPrefetch) * 100)
  }
  
  // Afficher les résultats
  console.log('\n✅ Résultats du test de performance:')
  console.table({
    'Sans préchargement': { 'Temps (ms)': report.withoutPrefetch },
    'Avec préchargement': { 'Temps (ms)': report.withPrefetch },
    'Amélioration': { 'Temps (ms)': `${report.improvement}%` }
  })
  
  return report
}

/**
 * Affiche les statistiques du cache actuel
 */
export function getCacheStats() {
  const cache = window.__API_RESPONSE_CACHE__
  const inflight = window.__API_INFLIGHT__
  
  if (!cache) {
    console.warn('⚠️ Cache non initialisé')
    return null
  }
  
  const stats = {
    totalEntries: cache.size,
    inflightRequests: inflight ? inflight.size : 0,
    entries: []
  }
  
  const now = Date.now()
  for (const [key, value] of cache.entries()) {
    const age = Math.round((now - value.t) / 1000) // en secondes
    stats.entries.push({
      key: key.substring(0, 50) + '...',
      age: `${age}s`,
      expired: age > 300 // TTL = 5 minutes
    })
  }
  
  console.log('📦 Statistiques du cache:')
  console.log(`   Entrées totales: ${stats.totalEntries}`)
  console.log(`   Requêtes en cours: ${stats.inflightRequests}`)
  console.table(stats.entries)
  
  return stats
}

/**
 * Nettoie le cache manuellement
 */
export function clearCache() {
  if (window.__API_RESPONSE_CACHE__) {
    const size = window.__API_RESPONSE_CACHE__.size
    window.__API_RESPONSE_CACHE__.clear()
    console.log(`🗑️ Cache nettoyé (${size} entrées supprimées)`)
    return true
  }
  console.warn('⚠️ Cache non trouvé')
  return false
}

// Exposer les fonctions globalement pour faciliter les tests dans la console
if (typeof window !== 'undefined') {
  window.perfTest = {
    measurePageLoad,
    testApiCache,
    testPrefetch,
    comparePerformance,
    getCacheStats,
    clearCache
  }
  
  console.log(`
    🎯 Utilitaires de test de performance chargés!
    
    Fonctions disponibles:
    - window.perfTest.comparePerformance(matiereId) - Compare avant/après
    - window.perfTest.testPrefetch(matiereId)       - Teste le prefetch
    - window.perfTest.getCacheStats()                - Affiche le cache
    - window.perfTest.clearCache()                   - Nettoie le cache
    
    Exemple:
      await window.perfTest.comparePerformance(1)
  `)
}

export default {
  measurePageLoad,
  testApiCache,
  testPrefetch,
  comparePerformance,
  getCacheStats,
  clearCache
}

