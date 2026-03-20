<template>
  <MainLayout>
    <section class="blog-coming-soon">
      <div class="coming-soon-container">
        <div class="coming-soon-icon">📝</div>
        <h1>Blog — Bientôt disponible</h1>
        <p class="coming-soon-text">
          Nous préparons des articles de qualité pour vous aider à réussir en mathématiques.
          <br />Revenez bientôt !
        </p>
        <RouterLink to="/" class="coming-soon-btn">← Retour à l'accueil</RouterLink>
      </div>
    </section>
  </MainLayout>
</template>

<script setup>
import MainLayout from '@/components/layout/MainLayout.vue'
import { setPageSeo } from '@/services/seo'

setPageSeo({
  title: 'Blog — Bientôt disponible',
  description: 'Le blog OptiTAB arrive bientôt. Articles, conseils et astuces en mathématiques.',
  robots: 'noindex,follow',
})
</script>

<style scoped>
.blog-coming-soon {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.coming-soon-container {
  text-align: center;
  max-width: 520px;
}

.coming-soon-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

h1 {
  font-size: 1.8rem;
  color: #1e293b;
  margin-bottom: 1rem;
}

.coming-soon-text {
  font-size: 1.05rem;
  color: #64748b;
  line-height: 1.7;
  margin-bottom: 2rem;
}

.coming-soon-btn {
  display: inline-block;
  padding: 0.7rem 1.5rem;
  background: #4e63c2;
  color: #fff;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: background 0.2s;
}

.coming-soon-btn:hover {
  background: #3b4fa3;
}
</style>
