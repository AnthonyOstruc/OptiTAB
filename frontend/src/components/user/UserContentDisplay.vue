<template>
  <div class="user-content-display">
    <!-- En-tête avec informations utilisateur -->
    <div class="user-header">
      <div class="user-info">
        <div class="user-pays">
          {{ userStore.pays?.drapeau_emoji }} {{ userStore.pays?.nom }}
        </div>
        <div class="user-niveau" :style="{ backgroundColor: userStore.niveau_pays?.couleur }">
          {{ userStore.niveau_pays?.nom }}
        </div>
      </div>
      <div class="content-summary">
        <div class="summary-item">
          <span class="summary-icon">📚</span>
          <span class="summary-count">{{ matieres.length }}</span>
          <span class="summary-label">Matières</span>
        </div>
        <div class="summary-item">
          <span class="summary-icon">🎯</span>
          <span class="summary-count">{{ themes.length }}</span>
          <span class="summary-label">Thèmes</span>
        </div>
        <div class="summary-item">
          <span class="summary-icon">📝</span>
          <span class="summary-count">{{ exercices.length }}</span>
          <span class="summary-label">Exercices</span>
        </div>
        <div class="summary-item">
          <span class="summary-icon">🎓</span>
          <span class="summary-count">{{ cours.length }}</span>
          <span class="summary-label">Cours</span>
        </div>
        <div class="summary-item">
          <span class="summary-icon">❓</span>
          <span class="summary-count">{{ quiz.length }}</span>
          <span class="summary-label">Quiz</span>
        </div>
      </div>
    </div>

    <!-- Contenu principal -->
    <div class="content-sections">
      <!-- Matières -->
      <div class="content-section">
        <h3 class="section-title">
          <span class="section-icon">📚</span>
          Matières disponibles
        </h3>
        <div v-if="loadingMatieres" class="loading-section">
          <div class="spinner"></div>
          <p>Chargement des matières...</p>
        </div>
        <div v-else-if="matieres.length === 0" class="empty-section">
          <p>Aucune matière disponible pour votre niveau</p>
        </div>
        <div v-else class="matieres-grid">
          <div 
            v-for="matiere in matieres" 
            :key="matiere.id"
            class="matiere-card"
            @click="selectMatiere(matiere)"
          >
            <div class="matiere-icon" v-html="matiere.svg_icon"></div>
            <div class="matiere-info">
              <h4 class="matiere-nom">{{ matiere.nom }}</h4>
              <p class="matiere-description">{{ matiere.description }}</p>
              <div class="matiere-badge" v-if="matiere.est_obligatoire">
                Obligatoire
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Thèmes -->
      <div class="content-section">
        <h3 class="section-title">
          <span class="section-icon">🎯</span>
          Thèmes disponibles
        </h3>
        <div v-if="loadingThemes" class="loading-section">
          <div class="spinner"></div>
          <p>Chargement des thèmes...</p>
        </div>
        <div v-else-if="themes.length === 0" class="empty-section">
          <p>Aucun thème disponible pour votre niveau</p>
        </div>
        <div v-else class="themes-grid">
          <div 
            v-for="theme in themes" 
            :key="theme.id"
            class="theme-card"
          >
            <div class="theme-info">
              <h4 class="theme-nom">{{ theme.nom }}</h4>
              <p class="theme-description">{{ theme.description }}</p>
              <div class="theme-matiere">{{ theme.matiere.nom }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Exercices -->
      <div class="content-section">
        <h3 class="section-title">
          <span class="section-icon">📝</span>
          Exercices disponibles
        </h3>
        <div v-if="loadingExercices" class="loading-section">
          <div class="spinner"></div>
          <p>Chargement des exercices...</p>
        </div>
        <div v-else-if="exercices.length === 0" class="empty-section">
          <p>Aucun exercice disponible pour votre niveau</p>
        </div>
        <div v-else class="exercices-grid">
          <div 
            v-for="exercice in exercices.slice(0, 6)" 
            :key="exercice.id"
            class="exercice-card"
          >
            <div class="exercice-info">
              <h4 class="exercice-titre">{{ exercice.titre }}</h4>
              <div class="exercice-difficulte">
                Difficulté: {{ exercice.difficulte }}
              </div>
              <div class="exercice-chapitre">{{ exercice.chapitre.nom }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Cours -->
      <div class="content-section">
        <h3 class="section-title">
          <span class="section-icon">🎓</span>
          Cours disponibles
        </h3>
        <div v-if="loadingCours" class="loading-section">
          <div class="spinner"></div>
          <p>Chargement des cours...</p>
        </div>
        <div v-else-if="cours.length === 0" class="empty-section">
          <p>Aucun cours disponible pour votre niveau</p>
        </div>
        <div v-else class="cours-grid">
          <div 
            v-for="cours_item in cours.slice(0, 6)" 
            :key="cours_item.id"
            class="cours-card"
          >
            <div class="cours-info">
              <h4 class="cours-titre">{{ cours_item.titre }}</h4>
              <p class="cours-description">{{ cours_item.description }}</p>
              <div class="cours-chapitre">{{ cours_item.chapitre.nom }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quiz -->
      <div class="content-section">
        <h3 class="section-title">
          <span class="section-icon">❓</span>
          Quiz disponibles
        </h3>
        <div v-if="loadingQuiz" class="loading-section">
          <div class="spinner"></div>
          <p>Chargement des quiz...</p>
        </div>
        <div v-else-if="quiz.length === 0" class="empty-section">
          <p>Aucun quiz disponible pour votre niveau</p>
        </div>
        <div v-else class="quiz-grid">
          <div 
            v-for="quiz_item in quiz.slice(0, 6)" 
            :key="quiz_item.id"
            class="quiz-card"
          >
            <div class="quiz-info">
              <h4 class="quiz-titre">{{ quiz_item.titre }}</h4>
              <p class="quiz-description">{{ quiz_item.description }}</p>
              <div class="quiz-difficulte">
                Difficulté: {{ quiz_item.difficulty }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { getMatieresUtilisateur } from '@/api/matieres.js'
import { getThemesPourUtilisateur } from '@/api/themes.js'
import { getExercicesPourUtilisateur } from '@/api/exercices.js'
import { getCoursPourUtilisateur } from '@/api/cours.js'
import { getQuizPourUtilisateur } from '@/api/quiz.js'

export default {
  name: 'UserContentDisplay',
  emits: ['matiere-selected'],
  setup(props, { emit }) {
    const userStore = useUserStore()
    
    // États réactifs
    const matieres = ref([])
    const themes = ref([])
    const exercices = ref([])
    const cours = ref([])
    const quiz = ref([])
    
    const loadingMatieres = ref(false)
    const loadingThemes = ref(false)
    const loadingExercices = ref(false)
    const loadingCours = ref(false)
    const loadingQuiz = ref(false)

    // Computed
    const hasUserConfiguration = computed(() => {
      return userStore.pays && userStore.niveau_pays
    })

    // Méthodes
    const loadMatieres = async () => {
      if (!hasUserConfiguration.value) return
      
      try {
        loadingMatieres.value = true
        const data = await getMatieresUtilisateur()
        matieres.value = data.data.matieres_disponibles
      } catch (error) {
        console.error('Erreur lors du chargement des matières:', error)
      } finally {
        loadingMatieres.value = false
      }
    }

    const loadThemes = async () => {
      if (!hasUserConfiguration.value) return
      
      try {
        loadingThemes.value = true
        const data = await getThemesPourUtilisateur()
        themes.value = data
      } catch (error) {
        console.error('Erreur lors du chargement des thèmes:', error)
      } finally {
        loadingThemes.value = false
      }
    }

    const loadExercices = async () => {
      if (!hasUserConfiguration.value) return
      
      try {
        loadingExercices.value = true
        const data = await getExercicesPourUtilisateur()
        exercices.value = data
      } catch (error) {
        console.error('Erreur lors du chargement des exercices:', error)
      } finally {
        loadingExercices.value = false
      }
    }

    const loadCours = async () => {
      if (!hasUserConfiguration.value) return
      
      try {
        loadingCours.value = true
        const data = await getCoursPourUtilisateur()
        cours.value = data
      } catch (error) {
        console.error('Erreur lors du chargement des cours:', error)
      } finally {
        loadingCours.value = false
      }
    }

    const loadQuiz = async () => {
      if (!hasUserConfiguration.value) return
      
      try {
        loadingQuiz.value = true
        const data = await getQuizPourUtilisateur()
        quiz.value = data
      } catch (error) {
        console.error('Erreur lors du chargement des quiz:', error)
      } finally {
        loadingQuiz.value = false
      }
    }

    const loadAllContent = async () => {
      if (!hasUserConfiguration.value) return
      
      await Promise.all([
        loadMatieres(),
        loadThemes(),
        loadExercices(),
        loadCours(),
        loadQuiz()
      ])
    }

    const selectMatiere = (matiere) => {
      emit('matiere-selected', matiere)
    }

    // Initialisation
    onMounted(() => {
      if (hasUserConfiguration.value) {
        loadAllContent()
      }
    })

    return {
      userStore,
      matieres,
      themes,
      exercices,
      cours,
      quiz,
      loadingMatieres,
      loadingThemes,
      loadingExercices,
      loadingCours,
      loadingQuiz,
      hasUserConfiguration,
      selectMatiere
    }
  }
}
</script>

<style scoped>
.user-content-display {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.user-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 1rem;
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-pays {
  font-size: 1.25rem;
  font-weight: 600;
}

.user-niveau {
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-weight: 600;
  color: white;
}

.content-summary {
  display: flex;
  gap: 2rem;
}

.summary-item {
  text-align: center;
}

.summary-icon {
  font-size: 1.5rem;
  display: block;
  margin-bottom: 0.5rem;
}

.summary-count {
  font-size: 1.5rem;
  font-weight: bold;
  display: block;
}

.summary-label {
  font-size: 0.875rem;
  opacity: 0.9;
}

.content-sections {
  display: grid;
  gap: 2rem;
}

.content-section {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 0 0 1.5rem 0;
  color: #1f2937;
  font-size: 1.25rem;
}

.section-icon {
  font-size: 1.5rem;
}

.loading-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 3rem;
  color: #6b7280;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e5e7eb;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-section {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
  font-style: italic;
}

.matieres-grid,
.themes-grid,
.exercices-grid,
.cours-grid,
.quiz-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.matiere-card,
.theme-card,
.exercice-card,
.cours-card,
.quiz-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.2s;
  background: white;
}

.matiere-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.matiere-card {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.matiere-icon {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
}

.matiere-info {
  flex: 1;
}

.matiere-nom {
  margin: 0 0 0.5rem 0;
  color: #1f2937;
  font-size: 1.125rem;
  font-weight: 600;
}

.matiere-description {
  margin: 0 0 0.75rem 0;
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.4;
}

.matiere-badge {
  display: inline-block;
  background-color: #10b981;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.theme-nom,
.exercice-titre,
.cours-titre,
.quiz-titre {
  margin: 0 0 0.5rem 0;
  color: #1f2937;
  font-size: 1rem;
  font-weight: 600;
}

.theme-description,
.cours-description,
.quiz-description {
  margin: 0 0 0.75rem 0;
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.4;
}

.theme-matiere,
.exercice-chapitre,
.cours-chapitre {
  color: #3b82f6;
  font-size: 0.875rem;
  font-weight: 500;
}

.exercice-difficulte,
.quiz-difficulte {
  color: #f59e0b;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  .user-header {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }
  
  .content-summary {
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
  }
  
  .matieres-grid,
  .themes-grid,
  .exercices-grid,
  .cours-grid,
  .quiz-grid {
    grid-template-columns: 1fr;
  }
}
</style> 