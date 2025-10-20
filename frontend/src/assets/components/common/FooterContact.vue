<template>
  <div class="footer-contact-line">
    <component
      v-for="contact in contacts"
      :key="contact.text"
      :is="contact.external ? 'a' : (contact.href && contact.href.startsWith('/') ? 'router-link' : 'a')"
      :href="contact.external || !contact.href?.startsWith('/') ? contact.href : undefined"
      :to="!contact.external && contact.href?.startsWith('/') ? contact.href : undefined"
      :aria-label="contact.label || contact.text"
      class="contact-link"
      :target="contact.external ? '_blank' : undefined"
      :rel="contact.external ? 'noopener noreferrer' : undefined"
    >
      <!-- Affichage dynamique de l'icône -->
      <img v-if="typeof contact.icon === 'string'" :src="`/icons/${contact.icon}.svg`" :alt="contact.label || contact.text" class="contact-icon-img" />
      <component v-else-if="typeof contact.icon === 'object' || typeof contact.icon === 'function'" :is="contact.icon" class="contact-icon-svg" />
      <span v-else>{{ contact.icon }}</span>
      <span>{{ contact.text }}</span>
    </component>
  </div>
</template>

<script setup>
defineProps({
  contacts: {
    type: Array,
    required: true,
  },
});
</script>

<style scoped>
.footer-contact-line {
  text-align: center;
  margin-top: 1rem;
  font-size: 1rem;
  display: flex;
  justify-content: center;
  gap: 2.5rem;
  flex-wrap: wrap;
}

.contact-link {
  color: var(--footer-link-color, #fff);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  font-weight: 600;
  transition: color 0.2s, text-decoration 0.2s;
}

.contact-icon-img, .contact-icon-svg {
  width: 28px;
  height: 28px;
  filter: brightness(0) invert(1);
  vertical-align: middle;
  display: block;
}

.contact-link:hover {
  text-decoration: underline;
  color: var(--footer-link-hover, #e0e0e0);
}
</style> 