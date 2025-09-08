<template>
  <div class="test-filtrage">
    <h2>Test de Filtrage des Matières</h2>
    
    <!-- Informations utilisateur -->
    <div class="user-info">
      <h3>Informations Utilisateur</h3>
      <p><strong>Email:</strong> {{ userStore.email }}</p>
      <p><strong>Pays:</strong> {{ userStore.pays?.nom || 'Non configuré' }}</p>
      <p><strong>Niveau:</strong> {{ userStore.niveau_pays?.nom || 'Non configuré' }}</p>
      <p><strong>Admin:</strong> {{ userStore.isAdmin ? 'Oui' : 'Non' }}</p>
    </div>

    <!-- Test API standard -->
    <div class="test-section">
      <h3>Test API Standard (getMatieres)</h3>
      <button @click="testStandardAPI" :disabled="loading">Tester getMatieres()</button>
      <div v-if="standardResult">
        <p><strong>Résultat:</strong> {{ standardResult.length }} matières trouvées</p>
        <ul>
          <li v-for="m in standardResult" :key="m.id">
            {{ m.nom }} (ID: {{ m.id }})
          </li>
        </ul>
      </div>
    </div>

    <!-- Test API utilisateur -->
    <div class="test-section">
      <h3>Test API Utilisateur (getMatieresUtilisateur)</h3>
      <button @click="testUserAPI" :disabled="loading">Tester getMatieresUtilisateur()</button>
      <div v-if="userResult">
        <p><strong>Filtres appliqués:</strong></p>
        <ul>
          <li>Pays: {{ userResult.filtres_appliques.pays ? 'Oui' : 'Non' }}</li>
          <li>Niveau: {{ userResult.filtres_appliques.niveau ? 'Oui' : 'Non' }}</li>
        </ul>
        <p><strong>Matières disponibles:</strong> {{ userResult.matieres_disponibles.length }}</p>
        <ul>
          <li v-for="m in userResult.matieres_disponibles" :key="m.id">
            {{ m.nom }} (ID: {{ m.id }})
          </li>
        </ul>
      </div>
    </div>

    <!-- Test API admin -->
    <div class="test-section">
      <h3>Test API Admin (getMatieresAdmin)</h3>
      <button @click="testAdminAPI" :disabled="loading">Tester getMatieresAdmin()</button>
      <div v-if="adminResult">
        <p><strong>Résultat:</strong> {{ adminResult.length }} matières trouvées</p>
        <ul>
          <li v-for="m in adminResult" :key="m.id">
            {{ m.nom }} (ID: {{ m.id }})
          </li>
        </ul>
      </div>
    </div>

    <!-- Messages d'erreur -->
    <div v-if="error" class="error">
      <strong>Erreur:</strong> {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { getMatieres, getMatieresUtilisateur, getMatieresAdmin } from '@/api/matieres'

const userStore = useUserStore()
const loading = ref(false)
const error = ref('')
const standardResult = ref(null)
const userResult = ref(null)
const adminResult = ref(null)

async function testStandardAPI() {
  loading.value = true
  error.value = ''
  try {
    const response = await getMatieres()
    standardResult.value = response.data
    console.log('✅ Test getMatieres réussi:', response.data)
  } catch (err) {
    error.value = `Erreur getMatieres: ${err.message}`
    console.error('❌ Erreur getMatieres:', err)
  } finally {
    loading.value = false
  }
}

async function testUserAPI() {
  loading.value = true
  error.value = ''
  try {
    const response = await getMatieresUtilisateur()
    userResult.value = response.data
    console.log('✅ Test getMatieresUtilisateur réussi:', response.data)
  } catch (err) {
    error.value = `Erreur getMatieresUtilisateur: ${err.message}`
    console.error('❌ Erreur getMatieresUtilisateur:', err)
  } finally {
    loading.value = false
  }
}

async function testAdminAPI() {
  loading.value = true
  error.value = ''
  try {
    const response = await getMatieresAdmin()
    adminResult.value = response.data
    console.log('✅ Test getMatieresAdmin réussi:', response.data)
  } catch (err) {
    error.value = `Erreur getMatieresAdmin: ${err.message}`
    console.error('❌ Erreur getMatieresAdmin:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.test-filtrage {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.user-info {
  background: #f0f8ff;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.test-section {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.test-section button {
  background: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 10px;
}

.test-section button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.test-section ul {
  margin: 10px 0;
  padding-left: 20px;
}

.error {
  background: #ffebee;
  color: #c62828;
  padding: 10px;
  border-radius: 4px;
  margin-top: 10px;
}
</style>
