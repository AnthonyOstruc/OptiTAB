<template>
  <section class="pricing-section">
    <h2 class="pricing-title">
      <span>{{ titre.split(' ')[0] }}</span> <span class="pricing-highlight">{{ titre.split(' ').slice(1).join(' ') }}</span>
    </h2>
    <p class="pricing-desc">{{ description }}</p>
    <div class="pricing-cards">
      <div v-for="plan in plans" :key="plan.key" :class="['pricing-card', { populaire: plan.populaire }]">
        <div v-if="plan.badge" class="pricing-badge">{{ plan.badge }}</div>
        <div class="pricing-card-header">
          <div class="pricing-card-icon" :class="plan.key">
            <svg v-if="plan.key==='free'" width="36" height="36" fill="none" stroke="#a78bfa" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 2"/></svg>
            <svg v-else-if="plan.key==='standard'" width="36" height="36" fill="none" stroke="#6366f1" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
            <svg v-else width="36" height="36" fill="none" stroke="#a78bfa" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 2"/><circle cx="12" cy="12" r="6"/></svg>
          </div>
          <h3 class="pricing-card-title">{{ plan.titre }}</h3>
          <p class="pricing-card-subtitle">{{ plan.sousTitre }}</p>
        </div>
        <div class="pricing-card-price">
          <span class="pricing-card-amount">{{ plan.prix }}</span>
          <span class="pricing-card-detail">{{ plan.prixDetail }}</span>
        </div>
        <ul class="pricing-card-features">
          <li v-for="(avantage, i) in plan.avantages" :key="i">
            <svg width="18" height="18" fill="none" stroke="#3ec28f" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg>
            <span>{{ avantage }}</span>
          </li>
        </ul>
        <button :class="['pricing-btn', plan.boutonType]">{{ plan.bouton }}</button>
      </div>
    </div>
    <div class="pricing-garantie">
      <svg width="20" height="20" fill="none" stroke="#3ec28f" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M9 12l2 2l4-4"/></svg>
      <span>{{ garantie }}</span>
    </div>
    <div class="pricing-legal">{{ legal }}</div>
  </section>
</template>

<script setup>
const props = defineProps({
  titre: { type: String, required: true },
  description: { type: String, required: true },
  plans: { type: Array, required: true },
  garantie: { type: String, default: '' },
  legal: { type: String, default: '' }
})
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;
.pricing-section {
  max-width: 1200px;
  margin: 0 auto 48px auto;
  padding: 32px 0 0 0;
  text-align: center;
}
.pricing-title {
  font-size: 2.3rem;
  font-weight: 900;
  color: $bleu-principal;
  margin-bottom: 10px;
  /* Descendre le titre H2 */
  margin-top: 1.5rem;
  padding-top: 0.75rem;
}
.pricing-highlight {
  color: #a78bfa;
}
.pricing-desc {
  color: #52525b;
  font-size: 1.15rem;
  margin-bottom: 32px;
}
.pricing-cards {
  display: flex;
  gap: 32px;
  justify-content: center;
  align-items: stretch;
  flex-wrap: wrap;
  margin-bottom: 32px;
}
.pricing-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 16px rgba(30,41,59,0.06);
  border: 1.5px solid #f3f4f6;
  padding: 38px 32px 32px 32px;
  min-width: 270px;
  max-width: 340px;
  flex: 1 1 300px;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: box-shadow 0.2s, border 0.2s;
}
.pricing-card.populaire {
  border: 2.5px solid #6366f1;
  box-shadow: 0 4px 24px rgba(99,102,241,0.10);
  z-index: 2;
}
.pricing-badge {
  position: absolute;
  top: -22px;
  left: 50%;
  transform: translateX(-50%);
  background: #6366f1;
  color: #fff;
  font-weight: 700;
  font-size: 1rem;
  border-radius: 16px;
  padding: 6px 22px;
  box-shadow: 0 2px 8px rgba(99,102,241,0.10);
  letter-spacing: 0.01em;
}
.pricing-card-header {
  margin-bottom: 18px;
}
.pricing-card-icon {
  margin-bottom: 10px;
}
.pricing-card-title {
  font-size: 1.18rem;
  font-weight: 800;
  color: $bleu-principal;
  margin-bottom: 2px;
}
.pricing-card-subtitle {
  color: #6366f1;
  font-size: 1.01rem;
  margin-bottom: 0;
}
.pricing-card-price {
  font-size: 2.1rem;
  font-weight: 900;
  color: #18181b;
  margin-bottom: 18px;
  display: flex;
  align-items: flex-end;
  gap: 8px;
  justify-content: center;
}
.pricing-card-amount {
  font-size: 2.1rem;
  font-weight: 900;
}
.pricing-card-detail {
  font-size: 1.1rem;
  color: #52525b;
  font-weight: 500;
}
.pricing-card-features {
  list-style: none;
  padding: 0;
  margin: 0 0 22px 0;
  text-align: left;
}
.pricing-card-features li {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #18181b;
  font-size: 1.01rem;
  margin-bottom: 8px;
}
.pricing-btn {
  width: 100%;
  padding: 14px 0;
  border-radius: 10px;
  font-weight: 700;
  font-size: 1.08rem;
  cursor: pointer;
  border: none;
  transition: background 0.2s, color 0.2s;
  margin-top: 8px;
}
.pricing-btn.primary {
  background: #6366f1;
  color: #fff;
}
.pricing-btn.primary:hover {
  background: #4f46e5;
}
.pricing-btn.secondary {
  background: #fff;
  color: #6366f1;
  border: 2px solid #e0e7ff;
}
.pricing-btn.secondary:hover {
  background: #f3f4f6;
  color: #6366f1;
}
.pricing-btn.premium {
  background: #a78bfa;
  color: #fff;
}
.pricing-btn.premium:hover {
  background: #7c3aed;
}
.pricing-garantie {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: #f0fdf4;
  color: #15803d;
  font-weight: 600;
  font-size: 1.05rem;
  border-radius: 10px;
  padding: 10px 22px;
  margin: 0 auto 18px auto;
  max-width: 350px;
}
.pricing-legal {
  color: #52525b;
  font-size: 0.98rem;
  margin-top: 8px;
}
@media (max-width: 900px) {
  .pricing-cards {
    flex-direction: column;
    gap: 18px;
    align-items: center;
    width: 100%;
  }
  .pricing-section {
    padding: 18px 0 0 0;
  }
}
@media (max-width: 600px) {
  .pricing-section {
    padding: 8px 0 0 0;
    width: 100vw;
    box-sizing: border-box;
  }
  .pricing-cards {
    width: 100vw;
    padding: 0 8px;
    box-sizing: border-box;
    gap: 12px;
  }
  .pricing-card {
    padding: 18px 4vw 14px 4vw;
    min-width: 0;
    max-width: 420px;
    margin: 0 auto;
    width: 100%;
  }
  .pricing-garantie {
    font-size: 0.98rem;
    padding: 8px 8px;
  }
}
</style> 