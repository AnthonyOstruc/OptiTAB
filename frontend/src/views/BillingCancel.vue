<template>
  <div class="billing-cancel-page">
    <div class="cancel-card">
      <div class="cancel-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.25">
          <circle cx="12" cy="12" r="10" />
          <path d="M9 9l6 6M15 9l-6 6" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </div>

      <p class="eyebrow">PAIEMENT INTERROMPU</p>
      <h1 class="title">Paiement annulé</h1>
      <p class="description">
        Aucun débit n’a été confirmé. Vous pouvez reprendre un pass ou un abonnement quand vous voulez.
      </p>

      <div class="actions">
        <router-link
          class="btn btn-primary"
          to="/billing"
          data-cta-name="subscribe"
          data-cta-location="billing_cancel"
        >
          Voir les offres
        </router-link>
        <router-link class="btn btn-secondary" to="/dashboard">
          Retour au tableau de bord
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.billing-cancel-page {
  min-height: 72vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  background:
    radial-gradient(circle at 20% 15%, rgba(59, 130, 246, 0.1), transparent 46%),
    radial-gradient(circle at 85% 80%, rgba(99, 102, 241, 0.09), transparent 45%),
    #f8fafc;
}

.cancel-card {
  width: min(560px, 100%);
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  box-shadow: 0 22px 48px -30px rgba(15, 23, 42, 0.42);
  padding: 2rem;
  text-align: center;
}

.cancel-icon {
  width: 74px;
  height: 74px;
  margin: 0 auto 1rem;
  display: grid;
  place-items: center;
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.25);
  border-radius: 999px;
}

.cancel-icon svg {
  width: 40px;
  height: 40px;
}

.eyebrow {
  margin: 0;
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #2563eb;
}

.title {
  margin: 0.5rem 0 0.75rem;
  font-size: clamp(1.7rem, 4vw, 2.2rem);
  font-weight: 800;
  color: #111827;
}

.description {
  margin: 0;
  color: #4b5563;
  font-size: 1rem;
  line-height: 1.55;
}

.actions {
  margin-top: 1.5rem;
  display: grid;
  gap: 0.75rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 44px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 0.98rem;
  text-decoration: none;
  transition: transform 0.15s ease, box-shadow 0.2s ease, background-color 0.2s ease;
}

.btn:hover {
  transform: translateY(-1px);
}

.btn-primary {
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
  color: #ffffff;
  box-shadow: 0 14px 24px -18px rgba(37, 99, 235, 0.8);
}

.btn-primary:hover {
  box-shadow: 0 16px 28px -18px rgba(37, 99, 235, 0.95);
}

.btn-secondary {
  background: #f3f4f6;
  color: #1f2937;
  border: 1px solid #e5e7eb;
}

.btn-secondary:hover {
  background: #eef2ff;
}

@media (max-width: 640px) {
  .billing-cancel-page {
    padding: 1rem;
    min-height: 66vh;
  }

  .cancel-card {
    padding: 1.4rem 1rem 1.2rem;
    border-radius: 16px;
  }
}
</style>

