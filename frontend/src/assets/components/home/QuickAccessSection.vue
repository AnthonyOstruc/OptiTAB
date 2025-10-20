<template>
  <section class="quick-access-section">
    <h2 class="quick-access-title">Accès rapide</h2>
    <div class="quick-access-grid">
      <div v-for="card in cards" :key="card.title" class="quick-access-card">
        <div class="quick-access-icon">{{ card.icon }}</div>
        <div class="quick-access-content">
          <h3 class="quick-access-card-title">{{ card.title }}</h3>
          <p class="quick-access-card-desc">{{ card.desc }}</p>
          <component
            :is="card.link && card.link.startsWith('/') ? 'router-link' : 'a'"
            :to="card.link && card.link.startsWith('/') ? card.link : undefined"
            :href="card.link && !card.link.startsWith('/') ? card.link : undefined"
            class="quick-access-btn"
            :target="card.link && !card.link.startsWith('/') ? '_blank' : undefined"
            :rel="card.link && !card.link.startsWith('/') ? 'noopener noreferrer' : undefined"
          >
            {{ card.cta }}
          </component>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  cards: { type: Array, required: true }
})
</script>

<style scoped>
.quick-access-section {
  padding: 3.5rem 0 2.5rem 0;
  background: #f8fafc;
}
.quick-access-title {
  text-align: center;
  font-size: 2rem;
  font-weight: 800;
  color: #2563eb;
  margin-bottom: 2.2rem;
}
.quick-access-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 2rem;
  max-width: 950px;
  margin: 0 auto;
}
.quick-access-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 12px rgba(30,41,59,0.07);
  padding: 2rem 1.2rem 1.5rem 1.2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: box-shadow 0.18s, transform 0.18s;
}
.quick-access-card:hover {
  box-shadow: 0 6px 24px rgba(37,99,235,0.13);
  transform: translateY(-4px) scale(1.03);
}
.quick-access-icon {
  font-size: 2.3rem;
  margin-bottom: 1.1rem;
}
.quick-access-card-title {
  font-size: 1.18rem;
  font-weight: 700;
  color: #18181b;
  margin-bottom: 0.5rem;
  text-align: center;
}
.quick-access-card-desc {
  font-size: 1.02rem;
  color: #475569;
  margin-bottom: 1.1rem;
  text-align: center;
}
.quick-access-btn {
  display: inline-block;
  background: #2563eb;
  color: #fff;
  font-weight: 600;
  border-radius: 8px;
  padding: 0.7rem 1.5rem;
  text-decoration: none;
  font-size: 1.05rem;
  transition: background 0.18s;
}
.quick-access-btn:hover {
  background: #1e40af;
}
</style> 