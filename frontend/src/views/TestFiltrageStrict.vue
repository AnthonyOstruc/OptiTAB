<template>
  <div class="test-filtrage-strict">
    <h1>Test du Filtrage Strict des Matières</h1>
    
    <!-- Informations utilisateur -->
    <div class="user-info">
      <h2>Configuration Utilisateur</h2>
      <p><strong>Email:</strong> {{ userStore.email }}</p>
      <p><strong>Pays:</strong> {{ userStore.pays?.nom || 'Non configuré' }} (ID: {{ userStore.pays?.id }})</p>
      <p><strong>Niveau:</strong> {{ userStore.niveau_pays?.nom || 'Non configuré' }} (ID: {{ userStore.niveau_pays?.id }})</p>
      <p><strong>Admin:</strong> {{ userStore.isAdmin ? 'Oui' : 'Non' }}</p>
    </div>

    <!-- Test du filtrage strict -->
    <div class="test-section">
      <h2>Test du Filtrage Strict</h2>
      <p class="info">
        <strong>Nouveau comportement :</strong> Seules les matières qui correspondent AU PAYS ET AU NIVEAU de l'utilisateur seront affichées.
      </p>
      
      <button @click="testFiltrageStrict" :disabled="loading" class="test-button">
        {{ loading ? 'Test en cours...' : 'Tester le Filtrage Strict' }}
      </button>
      
      <div v-if="result" class="result">
        <h3>Résultats du Test</h3>
        <p><strong>Status:</strong> {{ result.status }}</p>
        <p><strong>Message:</strong> {{ result.message }}</p>
        <p><strong>Filtres appliqués:</strong></p>
        <ul>
          <li>Pays: {{ result.filtres_appliques?.pays ? 'Oui' : 'Non' }}</li>
          <li>Niveau: {{ result.filtres_appliques?.niveau ? 'Oui' : 'Non' }}</li>
        </ul>
        <p><strong>Matières disponibles:</strong> {{ result.matieres_disponibles?.length || 0 }}</p>
        
        <div v-if="result.matieres_disponibles && result.matieres_disponibles.length > 0" class="matieres-list">
          <h4>Matières filtrées (Pays ET Niveau):</h4>
          <div v-for="matiere in result.matieres_disponibles" :key="matiere.id" class="matiere-item">
            <div class="matiere-header">
              <span class="matiere-icon" v-html="matiere.svg_icon || '📚'"></span>
              <span class="matiere-nom">{{ matiere.nom }}</span>
            </div>
            <div class="matiere-details">
              <p><strong>Pays associés:</strong> {{ matiere.pays_associes?.map(p => p.nom).join(', ') || 'Aucun' }}</p>
              <p><strong>Niveaux associés:</strong> {{ matiere.niveaux_associes?.map(n => n.nom).join(', ') || 'Aucun' }}</p>
            </div>
          </div>
        </div>
        
        <div v-else class="no-matieres">
          <p>⚠️ Aucune matière ne correspond exactement à votre pays ET niveau.</p>
          <p>Vérifiez que :</p>
          <ul>
            <li>Votre pays et niveau sont correctement configurés</li>
            <li>Il existe des matières associées à votre pays ET niveau</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Comparaison avec l'ancien filtrage -->
    <div class="test-section">
      <h2>Comparaison avec l'Ancien Filtrage</h2>
      <p class="info">
        <strong>Ancien comportement :</strong> Matières du pays OU du niveau (plus permissif)
      </p>
      
      <button @click="testAncienFiltrage" :disabled="loading" class="test-button">
        {{ loading ? 'Test en cours...' : 'Simuler l\'Ancien Filtrage' }}
      </button>
      
      <div v-if="ancienResult" class="result">
        <h3>Résultats de l'Ancien Filtrage (Simulation)</h3>
        <p><strong>Matières (Pays OU Niveau):</strong> {{ ancienResult.length }}</p>
        
        <div v-if="ancienResult.length > 0" class="matieres-list">
          <div v-for="matiere in ancienResult" :key="matiere.id" class="matiere-item old">
            <div class="matiere-header">
              <span class="matiere-icon" v-html="matiere.svg_icon || '📚'"></span>
              <span class="matiere-nom">{{ matiere.nom }}</span>
              <span class="matiere-type">
                {{ getMatiereType(matiere) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Instructions -->
    <div class="instructions">
      <h2>Instructions</h2>
      <ol>
        <li>Assurez-vous d'être connecté avec un utilisateur qui a un pays et un niveau configurés</li>
        <li>Cliquez sur "Tester le Filtrage Strict" pour voir les matières qui correspondent exactement à votre configuration</li>
        <li>Comparez avec l'ancien filtrage pour voir la différence</li>
        <li>Vérifiez que le composant <code>SelectedMatiereHeader</code> utilise maintenant ce filtrage strict</li>
      </ol>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { getMatieresUtilisateur, filtrerMatieres } from '@/api/matieres.js'

const userStore = useUserStore()
const loading = ref(false)
const result = ref(null)
const ancienResult = ref(null)

const testFiltrageStrict = async () => {
  loading.value = true
  try {
    const response = await getMatieresUtilisateur()
    result.value = response.data
    console.log('Filtrage strict:', result.value)
  } catch (error) {
    console.error('Erreur lors du test du filtrage strict:', error)
    result.value = { error: error.message }
  } finally {
    loading.value = false
  }
}

const testAncienFiltrage = async () => {
  loading.value = true
  try {
    // Simuler l'ancien filtrage en utilisant filtrerMatieres avec pays OU niveau
    const userPays = userStore.pays?.id
    const userNiveau = userStore.niveau_pays?.id
    
    // Test avec pays seulement
    const paysResponse = userPays ? await filtrerMatieres(userPays, null) : { data: { matieres: [] } }
    const paysMatieres = paysResponse.data.matieres || []
    
    // Test avec niveau seulement
    const niveauResponse = userNiveau ? await filtrerMatieres(null, userNiveau) : { data: { matieres: [] } }
    const niveauMatieres = niveauResponse.data.matieres || []
    
    // Combiner et dédupliquer (simulation de l'ancien comportement OR)
    const allMatieres = [...paysMatieres, ...niveauMatieres]
    const uniqueMatieres = allMatieres.filter((matiere, index, self) => 
      index === self.findIndex(m => m.id === matiere.id)
    )
    
    ancienResult.value = uniqueMatieres
    console.log('Ancien filtrage (simulation):', ancienResult.value)
  } catch (error) {
    console.error('Erreur lors du test de l\'ancien filtrage:', error)
    ancienResult.value = []
  } finally {
    loading.value = false
  }
}

const getMatiereType = (matiere) => {
  const userPays = userStore.pays?.id
  const userNiveau = userStore.niveau_pays?.id
  
  const hasPays = matiere.pays_associes?.some(p => p.id === userPays)
  const hasNiveau = matiere.niveaux_associes?.some(n => n.id === userNiveau)
  
  if (hasPays && hasNiveau) return 'Pays ET Niveau'
  if (hasPays) return 'Pays seulement'
  if (hasNiveau) return 'Niveau seulement'
  return 'Aucun'
}
</script>

<style scoped>
.test-filtrage-strict {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.user-info {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  border: 1px solid #e9ecef;
}

.test-section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  background: #fff;
}

.info {
  background: #e7f3ff;
  padding: 10px;
  border-radius: 4px;
  border-left: 4px solid #007bff;
  margin-bottom: 15px;
}

.test-button {
  background: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 15px;
}

.test-button:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.result {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  border: 1px solid #dee2e6;
}

.matieres-list {
  margin-top: 15px;
}

.matiere-item {
  background: #fff;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 10px;
}

.matiere-item.old {
  border-left: 4px solid #ffc107;
  background: #fffbf0;
}

.matiere-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 5px;
}

.matiere-icon {
  font-size: 20px;
}

.matiere-nom {
  font-weight: bold;
  color: #495057;
}

.matiere-type {
  background: #6c757d;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  margin-left: auto;
}

.matiere-details {
  font-size: 14px;
  color: #6c757d;
}

.matiere-details p {
  margin: 2px 0;
}

.no-matieres {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 4px;
  padding: 15px;
  color: #856404;
}

.instructions {
  background: #d1ecf1;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #bee5eb;
}

.instructions ol {
  margin: 10px 0;
  padding-left: 20px;
}

.instructions li {
  margin-bottom: 5px;
}

.instructions code {
  background: #f8f9fa;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: monospace;
}
</style>
