<template>
  <DashboardLayout>
    <div class="admin-layout">
      <nav class="admin-nav">
        <router-link to="/admin/matieres" class="admin-link" :class="{ active: isActive('AdminMatieres') }">Matières</router-link>
        <router-link to="/admin/themes" class="admin-link" :class="{ active: isActive('AdminThemes') }">Thèmes</router-link>
        <router-link to="/admin/notions" class="admin-link" :class="{ active: isActive('AdminNotions') }">Notions</router-link>
        <router-link to="/admin/chapitres" class="admin-link" :class="{ active: isActive('AdminChapitres') }">Chapitres</router-link>
        <router-link to="/admin/exercices" class="admin-link" :class="{ active: isActive('AdminExercices') }">Exercices</router-link>
        <router-link to="/admin/exercices-plus" class="admin-link" :class="{ active: isActive('AdminExercicesPlus') }">Exercices+</router-link>
        <router-link to="/admin/cours" class="admin-link" :class="{ active: isActive('AdminCours') }">Cours</router-link>
        <router-link to="/admin/cours-plus" class="admin-link" :class="{ active: isActive('AdminCoursPlus') }">Cours+</router-link>
        <router-link to="/admin/sheets" class="admin-link" :class="{ active: isActive('AdminSheets') }">Fiches</router-link>
        <router-link to="/admin/quiz" class="admin-link" :class="{ active: isActive('AdminQuiz') }">Quiz</router-link>
        <router-link to="/admin/quiz-plus" class="admin-link" :class="{ active: isActive('AdminQuizPlus') }">Quiz+</router-link>
        <router-link to="/admin/niveaux" class="admin-link" :class="{ active: isActive('AdminNiveaux') }">Niveaux</router-link>
        <router-link to="/admin/pays" class="admin-link" :class="{ active: isActive('AdminPays') }">Pays</router-link>
      </nav>
      <div class="admin-content">
        <router-view />
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { useRoute } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
const route = useRoute()
function isActive(name) {
  return route.name === name
}
</script>

<style scoped>
.admin-nav {
  display: flex;
  gap: 1rem;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
}
.admin-link {
  text-decoration: none;
  color: #374151;
  font-weight: 600;
  padding: 6px 10px;
  border-radius: 4px;
}
.admin-link.active {
  background: #6366f1;
  color: #fff;
}
.admin-content {
  padding-top: 1rem;
}
</style> 