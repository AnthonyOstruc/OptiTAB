<template>
  <div class="test-home">
    <h1>OptiTAB - Test</h1>
    <p>Application fonctionne correctement</p>
    <router-link to="/dashboard">Aller au Dashboard</router-link>
  </div>
</template>

<script setup>
console.log('Home component loaded successfully')
</script>

<style scoped>
.test-home {
  padding: 20px;
  text-align: center;
}

.test-home h1 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.test-home p {
  color: #7f8c8d;
  margin-bottom: 20px;
}

.test-home a {
  color: #3498db;
  text-decoration: none;
  padding: 10px 20px;
  border: 1px solid #3498db;
  border-radius: 5px;
  display: inline-block;
}

.test-home a:hover {
  background-color: #3498db;
  color: white;
}
</style>
