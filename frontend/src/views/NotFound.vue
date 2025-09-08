<template>
  <div class="not-found">
    <h1>404</h1>
    <p>Oups, la page que vous cherchez n'existe pas.</p>
    <router-link to="/">Retour à l'accueil</router-link>
  </div>
</template>

<script setup>
</script>

<style scoped>
.not-found {
  text-align: center;
  margin-top: 100px;
}
h1 {
  font-size: 6rem;
  margin-bottom: 1rem;
}
p {
  font-size: 1.5rem;
  margin-bottom: 2rem;
}
</style> 