<template>
  <DashboardLayout>
    <!-- Les exercices guidés ne donnent pas d'XP, donc pas de notification -->
    <!-- Seuls les quiz donnent des XP avec leurs propres notifications -->
    
    <!-- Contenu de la page -->
    <slot />
  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
</script>

<style scoped>
/* Ce composant n'a pas de styles spécifiques */
</style>
