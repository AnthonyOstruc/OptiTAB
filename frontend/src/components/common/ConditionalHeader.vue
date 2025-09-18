<template>
  <div class="header-center">
    <!-- Contenu conditionnel basé sur le type -->
    <component 
      :is="currentComponent" 
      v-bind="componentProps"
      @subject-changed="handleSubjectChange"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import SubjectFilters from './SubjectFilters.vue'
import ChapterNavigation from './ChapterNavigation.vue'
import SelectedMatiereHeader from './SelectedMatiereHeader.vue'

// Props
const props = defineProps({
  subjectPages: {
    type: Array,
    default: () => ['Calculator', 'Exercises', 'Sheets']
  },
  searchPages: {
    type: Array,
    default: () => ['Dashboard', 'Chapitres', 'Notions']
  },
  chapterPages: {
    type: Array,
    default: () => ['Exercices', 'ChapterQuiz', 'CourseChapitre', 'QuizChapitres', 'CourseChapitres', 'Chapitres']
  },
  matierePages: {
    type: Array,
    default: () => ['Dashboard', 'Themes', 'Notions', 'Exercises', 'OnlineCourses', 'CourseNotions', 'Quiz', 'QuizNotions', 'Sheets']
  },
  subjectProps: {
    type: Object,
    default: () => ({})
  },
  searchProps: {
    type: Object,
    default: () => ({})
  },
  chapterProps: {
    type: Object,
    default: () => ({})
  },
  matiereProps: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['subject-changed', 'search'])
const route = useRoute()

const currentComponent = computed(() => {
  const currentPage = route.name
  // Affichage OBLIGATOIRE des tabs pour Quiz, QuizNotions et Dashboard (sauf Calculator)
  if ((currentPage === 'Quiz' || currentPage === 'QuizNotions' || currentPage === 'Dashboard' || props.matierePages.includes(currentPage)) && currentPage !== 'Calculator') {
    return SelectedMatiereHeader
  }
  if (props.chapterPages.includes(currentPage)) {
    return ChapterNavigation
  }
  if (props.subjectPages.includes(currentPage)) {
    return SubjectFilters
  }
  return null
})

const componentProps = computed(() => {
  const currentPage = route.name
  // Props OBLIGATOIRES pour Quiz, QuizNotions et Dashboard (sauf Calculator)
  if ((currentPage === 'Quiz' || currentPage === 'QuizNotions' || currentPage === 'Dashboard' || props.matierePages.includes(currentPage)) && currentPage !== 'Calculator') {
    return {
      matiereId: props.matiereProps.matiereId,
      ...props.matiereProps
    }
  }
  if (props.chapterPages.includes(currentPage)) {
    return {
      chapitreId: route.params.chapitreId,
      ...props.chapterProps
    }
  }
  if (props.subjectPages.includes(currentPage)) {
    return {
      ...props.subjectProps
    }
  }
  return {
    ...props.searchProps
  }
})

const handleSubjectChange = (subjectId) => {
  emit('subject-changed', subjectId)
}
</script>

<style scoped>
.header-center {
  /* Centré exactement au milieu du header */
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  justify-content: center;
  /* Réserve de place pour les éléments gauche/droite pour éviter le chevauchement */
  max-width: min(600px, calc(100vw - 420px));
  width: fit-content;
  min-width: 0;
  overflow: visible;
  z-index: 200; /* s'assurer que les tabs restent cliquables au-dessus */
}

/* Responsive - Optimisé pour que les onglets restent toujours visibles */
@media (max-width: 1200px) {
  .header-center {
    max-width: 500px;
  }
}

/* Fallback UX: en dessous d'une certaine largeur, on centre dans le flux 
   pour éviter tout chevauchement avec la zone droite (avatar/xp). */
@media (max-width: 1100px) {
  .header-center {
    position: static;
    left: auto;
    top: auto;
    transform: none;
    margin: 0 auto;
  }
}


@media (max-width: 1024px) {
  .header-center {
    max-width: 400px;
    /* Assurer que les onglets restent visibles */
    min-width: 200px;
  }
}

@media (max-width: 768px) {
  .header-center {
    max-width: none;
    /* Assurer que les onglets restent toujours visibles sur mobile */
    min-width: 150px;
  }
}

@media (max-width: 480px) {
  .header-center {
    /* Assurer que les onglets restent toujours visibles même sur très petit écran */
    min-width: 120px;
  }
}

@media (max-width: 360px) {
  .header-center {
    /* Assurer que les onglets restent toujours visibles */
    min-width: 100px;
  }
}

/* Assurer que les onglets restent visibles en mode paysage sur mobile */
@media (max-height: 500px) and (orientation: landscape) {
  .header-center {
    /* Assurer que les onglets restent visibles en mode paysage */
    min-width: 120px;
  }
}
</style> 