import { API, getFullCurriculum, searchCurriculum } from './index'

/**
 * Tests API - Architecture DRY et professionnelle
 */

// ========================================
// TESTS PAR ENTITÉ
// ========================================

/**
 * Test complet d'une entité
 */
const testEntity = async (entityName, entityAPI, testData = {}) => {
  console.log(`\n🧪 TEST ${entityName.toUpperCase()}`)
  console.log('-'.repeat(30))
  
  try {
    // Test getAll
    const allItems = await entityAPI.getAll()
    console.log(`✅ getAll: ${allItems.length} éléments`)
    
    if (allItems.length > 0) {
      const firstItem = allItems[0]
      
      // Test getById
      const itemDetail = await entityAPI.getById(firstItem.id)
      console.log(`✅ getById: élément ${firstItem.id} récupéré`)
      
      // Test des méthodes spécialisées si elles existent
      if (entityAPI.getByFilter) {
        const filtered = await entityAPI.getByFilter({ est_actif: true })
        console.log(`✅ getByFilter: ${filtered.length} éléments actifs`)
      }
      
      // Test hiérarchique si applicable
      if (entityAPI.getHierarchical) {
        const hierarchical = await entityAPI.getHierarchical(firstItem.id, 'children')
        console.log(`✅ getHierarchical: ${hierarchical.length} enfants`)
      }
    }
    
    return true
  } catch (error) {
    console.error(`❌ Erreur test ${entityName}:`, error.message)
    return false
  }
}

// ========================================
// TESTS HIÉRARCHIQUES
// ========================================

/**
 * Test de la hiérarchie complète
 */
const testHierarchy = async () => {
  console.log('\n🏗️ TEST HIÉRARCHIE COMPLÈTE')
  console.log('='.repeat(40))
  
  try {
    // Test pays → niveaux → matières
    const pays = await API.pays.getAll()
    if (pays.length > 0) {
      const paysId = pays[0].id
      
      // Test hiérarchie pays
      const paysHierarchy = await API.pays.getHierarchy(paysId)
      console.log(`✅ Pays ${pays[0].nom}: ${paysHierarchy.children.length} niveaux`)
      
      if (paysHierarchy.children.length > 0) {
        const niveauId = paysHierarchy.children[0].id
        
        // Test hiérarchie niveau
        const niveauHierarchy = await API.niveaux.getHierarchy(niveauId)
        console.log(`✅ Niveau ${paysHierarchy.children[0].nom}: ${niveauHierarchy.children.length} matières`)
      }
    }
    
    return true
  } catch (error) {
    console.error('❌ Erreur test hiérarchie:', error.message)
    return false
  }
}

// ========================================
// TESTS FONCTIONNELS
// ========================================

/**
 * Test du curriculum complet
 */
const testFullCurriculum = async () => {
  console.log('\n📚 TEST CURRICULUM COMPLET')
  console.log('='.repeat(35))
  
  try {
    const pays = await API.pays.getAll()
    if (pays.length > 0) {
      const curriculum = await getFullCurriculum(pays[0].id)
      console.log(`✅ Curriculum ${curriculum.pays.nom}: ${curriculum.niveaux.length} niveaux`)
      
      const totalMatieres = curriculum.niveaux.reduce((total, niveau) => 
        total + niveau.matieres.length, 0)
      console.log(`✅ Total matières: ${totalMatieres}`)
    }
    
    return true
  } catch (error) {
    console.error('❌ Erreur test curriculum:', error.message)
    return false
  }
}

/**
 * Test de recherche globale
 */
const testGlobalSearch = async () => {
  console.log('\n🔍 TEST RECHERCHE GLOBALE')
  console.log('='.repeat(30))
  
  try {
    const results = await searchCurriculum('math')
    console.log(`✅ Recherche "math":`)
    console.log(`  - Pays: ${results.pays.length}`)
    console.log(`  - Matières: ${results.matieres.length}`)
    console.log(`  - Thèmes: ${results.themes.length}`)
    console.log(`  - Notions: ${results.notions.length}`)
    console.log(`  - Chapitres: ${results.chapitres.length}`)
    console.log(`  - Exercices: ${results.exercices.length}`)
    
    return true
  } catch (error) {
    console.error('❌ Erreur test recherche:', error.message)
    return false
  }
}

// ========================================
// TESTS PRINCIPAUX
// ========================================

/**
 * Test complet de tous les endpoints
 */
export const testAllEndpoints = async () => {
  console.log('🚀 TEST COMPLET DE TOUS LES ENDPOINTS')
  console.log('='.repeat(50))
  
  const results = {
    pays: false,
    niveaux: false,
    matieres: false,
    themes: false,
    notions: false,
    chapitres: false,
    exercices: false,
    hierarchy: false,
    curriculum: false,
    search: false
  }
  
  // Tests par entité
  results.pays = await testEntity('Pays', API.pays)
  results.niveaux = await testEntity('Niveaux', API.niveaux)
  results.matieres = await testEntity('Matières', API.matieres)
  results.themes = await testEntity('Thèmes', API.themes)
  results.notions = await testEntity('Notions', API.notions)
  results.chapitres = await testEntity('Chapitres', API.chapitres)
  results.exercices = await testEntity('Exercices', API.exercices)
  
  // Tests fonctionnels
  results.hierarchy = await testHierarchy()
  results.curriculum = await testFullCurriculum()
  results.search = await testGlobalSearch()
  
  // Résumé
  console.log('\n📊 RÉSUMÉ DES TESTS')
  console.log('='.repeat(25))
  
  Object.entries(results).forEach(([test, success]) => {
    const status = success ? '✅' : '❌'
    console.log(`${status} ${test}`)
  })
  
  const successCount = Object.values(results).filter(Boolean).length
  const totalCount = Object.keys(results).length
  
  console.log(`\n🎯 ${successCount}/${totalCount} tests réussis`)
  
  return results
}

/**
 * Test rapide des endpoints principaux
 */
export const testQuickEndpoints = async () => {
  console.log('⚡ TEST RAPIDE')
  console.log('='.repeat(20))
  
  try {
    // Test pays
    const pays = await API.pays.getAll()
    console.log(`✅ Pays: ${pays.length} trouvés`)
    
    if (pays.length > 0) {
      // Test niveaux
      const niveaux = await API.pays.getNiveaux(pays[0].id)
      console.log(`✅ Niveaux: ${niveaux.length} trouvés`)
      
      if (niveaux.length > 0) {
        // Test matières
        const matieres = await API.niveaux.getMatieres(niveaux[0].id)
        console.log(`✅ Matières: ${matieres.length} trouvées`)
      }
    }
    
    console.log('✅ Test rapide réussi!')
    return true
    
  } catch (error) {
    console.error('❌ Erreur test rapide:', error.message)
    return false
  }
}

// ========================================
// TESTS SPÉCIALISÉS
// ========================================

/**
 * Test des opérations CRUD
 */
export const testCRUD = async (entityName, entityAPI, sampleData) => {
  console.log(`\n🔄 TEST CRUD ${entityName.toUpperCase()}`)
  console.log('-'.repeat(30))
  
  try {
    // Create
    const created = await entityAPI.create(sampleData)
    console.log(`✅ Create: ${created.id} créé`)
    
    // Read
    const read = await entityAPI.getById(created.id)
    console.log(`✅ Read: ${read.id} lu`)
    
    // Update
    const updated = await entityAPI.update(created.id, { ...sampleData, updated: true })
    console.log(`✅ Update: ${updated.id} mis à jour`)
    
    // Delete
    await entityAPI.delete(created.id)
    console.log(`✅ Delete: ${created.id} supprimé`)
    
    return true
  } catch (error) {
    console.error(`❌ Erreur CRUD ${entityName}:`, error.message)
    return false
  }
}

// Export par défaut
export default {
  testAllEndpoints,
  testQuickEndpoints,
  testCRUD
}
