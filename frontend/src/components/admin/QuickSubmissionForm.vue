<template>
  <div class="quick-submission-form">
    <div class="form-header">
      <h3>➕ Enregistrer une réception WhatsApp</h3>
      <p>Enregistrez rapidement qu'un élève a envoyé un quiz</p>
    </div>

    <form @submit.prevent="handleSubmit" class="form-body">
      <div class="form-group">
        <label for="user">Élève *</label>
        <select v-model="form.userId" id="user" required>
          <option value="">-- Sélectionner un élève --</option>
          <option v-for="user in users" :key="user.id" :value="user.id">
            {{ user.full_name && user.full_name.trim() ? `${user.full_name} (${user.email})` : user.email }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="quiz">Quiz *</label>
        <input 
          v-model="quizSearch" 
          type="text" 
          placeholder="Rechercher un quiz..."
          class="search-input"
          @input="filterQuiz"
        />
        <select v-model="form.quizId" id="quiz" required>
          <option value="">-- Sélectionner un quiz --</option>
          <option v-for="quiz in filteredQuiz" :key="quiz.id" :value="quiz.id">
            {{ quiz.titre }} - {{ quiz.notion?.titre || 'Sans notion' }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="notes">Notes administratives</label>
        <textarea 
          v-model="form.notes_admin" 
          id="notes"
          rows="3"
          placeholder="Ex: Reçu par WhatsApp le 11/12/2025 à 14h30"
        ></textarea>
      </div>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <div v-if="success" class="success-message">
        ✅ Soumission enregistrée avec succès !
      </div>

      <div class="form-actions">
        <button type="button" @click="resetForm" class="btn-reset">
          Réinitialiser
        </button>
        <button type="submit" class="btn-submit" :disabled="submitting">
          {{ submitting ? 'Enregistrement...' : '✓ Enregistrer' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { createQuizSubmission } from '@/api/quizSubmissions'
import { getQuizAdmin } from '@/api/quiz'
import apiClient from '@/api/client'

const emit = defineEmits(['submitted'])

const form = ref({
  userId: '',
  quizId: '',
  notes_admin: ''
})

const users = ref([])
const allQuiz = ref([])
const filteredQuiz = ref([])
const quizSearch = ref('')

const submitting = ref(false)
const error = ref('')
const success = ref(false)

onMounted(async () => {
  await loadUsers()
  await loadQuiz()
})

async function loadUsers() {
  try {
    // Charger la liste des utilisateurs (élèves)
    const response = await apiClient.get('/api/users/users/?role=student&limit=1000')
    // ResponseService enveloppe dans { data: { results: [...] } }
    users.value = response.data?.data?.results || response.data?.results || response.data || []
    console.log('Utilisateurs chargés:', users.value.length)
  } catch (err) {
    console.error('Erreur chargement utilisateurs:', err)
  }
}

async function loadQuiz() {
  try {
    const response = await getQuizAdmin({ limit: 1000 })
    allQuiz.value = response.data?.results || response.data || []
    filteredQuiz.value = allQuiz.value
  } catch (err) {
    console.error('Erreur chargement quiz:', err)
  }
}

function filterQuiz() {
  const search = quizSearch.value.toLowerCase()
  if (!search) {
    filteredQuiz.value = allQuiz.value
    return
  }
  
  filteredQuiz.value = allQuiz.value.filter(quiz => {
    const titre = quiz.titre?.toLowerCase() || ''
    const notion = quiz.notion?.titre?.toLowerCase() || ''
    return titre.includes(search) || notion.includes(search)
  })
}

async function handleSubmit() {
  error.value = ''
  success.value = false

  if (!form.value.userId || !form.value.quizId) {
    error.value = 'Veuillez sélectionner un élève et un quiz'
    return
  }

  submitting.value = true
  try {
    await apiClient.post('/api/suivis/quiz-submissions/', {
      user_id: form.value.userId,
      quiz: form.value.quizId,
      notes_admin: form.value.notes_admin
    })

    success.value = true
    emit('submitted')
    
    // Réinitialiser le formulaire après 2 secondes
    setTimeout(() => {
      resetForm()
      success.value = false
    }, 2000)
  } catch (err) {
    console.error('Erreur création soumission:', err)
    error.value = err.response?.data?.detail || 'Erreur lors de l\'enregistrement'
  } finally {
    submitting.value = false
  }
}

function resetForm() {
  form.value = {
    userId: '',
    quizId: '',
    notes_admin: ''
  }
  quizSearch.value = ''
  filteredQuiz.value = allQuiz.value
  error.value = ''
  success.value = false
}
</script>

<style scoped>
.quick-submission-form {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.form-header h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.form-header p {
  color: #64748b;
  font-size: 0.875rem;
  margin: 0 0 1.5rem 0;
}

.form-body {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.875rem;
}

.form-group select,
.form-group textarea,
.search-input {
  padding: 0.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
}

.form-group select:focus,
.form-group textarea:focus,
.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-input {
  margin-bottom: 0.5rem;
}

.form-group textarea {
  resize: vertical;
  font-family: inherit;
}

.error-message,
.success-message {
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.875rem;
}

.error-message {
  background: #fee2e2;
  color: #991b1b;
  border-left: 4px solid #dc2626;
}

.success-message {
  background: #d1fae5;
  color: #065f46;
  border-left: 4px solid #10b981;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}

.btn-reset,
.btn-submit {
  flex: 1;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-reset {
  background: #f1f5f9;
  color: #64748b;
}

.btn-reset:hover {
  background: #e2e8f0;
}

.btn-submit {
  background: #3b82f6;
  color: white;
}

.btn-submit:hover:not(:disabled) {
  background: #2563eb;
  transform: translateY(-2px);
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .form-actions {
    flex-direction: column;
  }
}
</style>

