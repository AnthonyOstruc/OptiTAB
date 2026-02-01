<template>
  <DashboardLayout>
    <section class="coming-soon">
      <div class="card">
        <div class="icon">🧩</div>
        <h1>Quiz — bientôt disponible</h1>
        <p>Cette section sera bientôt ouverte à tous les élèves.</p>
        <p>Revenez prochainement pour découvrir les quiz interactifs.</p>
        <div class="actions">
          <router-link class="btn" :to="{ name: 'Dashboard' }">Retour au tableau de bord</router-link>
        </div>
      </div>
    </section>
  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
</script>

<style scoped>
.coming-soon {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 120px);
  padding: 2rem 1rem;
}
.card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 2rem 2.25rem;
  text-align: center;
  max-width: 680px;
  width: 100%;
  box-shadow: 0 8px 24px rgba(2, 6, 23, 0.06);
}
.icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
h1 { font-size: 1.5rem; margin: 0.25rem 0 0.5rem; color: #0f172a; }
p { color: #475569; margin: 0.1rem 0; }
.actions { margin-top: 1rem; }
.btn {
  display: inline-block;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  color: #fff;
  padding: 0.6rem 1rem;
  border-radius: 10px;
  font-weight: 700;
}
.btn:hover { filter: brightness(1.05); }
</style>

