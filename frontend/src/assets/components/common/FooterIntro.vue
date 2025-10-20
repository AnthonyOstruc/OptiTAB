<template>
  <div class="footer-intro">
    <p>
      <strong>Une équipe dédiée à votre service, disponible 7j/7.</strong><br />
      {{ message }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    required: true,
  },
});
</script>

<style scoped>
.footer-intro {
  max-width: 800px;
  margin: 0 auto 2rem auto;
  font-size: 1rem;
  color: var(--footer-text-color, #fff);
  font-family: 'Poppins', sans-serif;
  text-align: center;
}

.footer-intro strong {
  font-weight: 700;
  font-size: 1.1rem;
  display: block;
  margin-bottom: 0.25rem;
}
</style> 