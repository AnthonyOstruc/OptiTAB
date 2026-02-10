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
    default: () => ['Dashboard', 'Notions']
  },
  chapterPages: {
    type: Array,
    default: () => ['ExercicesByNotion', 'QuizByNotion', 'CourseByNotion', 'SynthesisByNotion']
  },
  matierePages: {
    type: Array,
    default: () => ['Dashboard', 'Themes', 'Notions', 'Exercises', 'OnlineCourses', 'CourseNotions', 'Quiz', 'QuizNotions', 'Sheets', 'TablesFormules']
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
      // chapitres supprimés; aucun id nécessaire
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
  /* Prendre tout l'espace disponible */
  flex: 1;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  min-width: 0;
  overflow: visible;
  z-index: 200; /* s'assurer que les tabs restent cliquables au-dessus */
  padding: 0;
}

/* Responsive - Maintenir le layout fixe sur tous les écrans */
@media (max-width: 768px) {
  .header-center {
    padding: 0;
  }
}
</style> 
