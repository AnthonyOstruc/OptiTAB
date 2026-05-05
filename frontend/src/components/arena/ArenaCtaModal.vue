<template>
  <transition name="fade">
    <div v-if="open && cta" class="cta-overlay" @click.self="dismiss">
      <div class="cta-modal" role="dialog" aria-modal="true">
        <div class="cta-modal__badge">OptiTAB+</div>
        <h2 class="cta-modal__title">{{ cta.title }}</h2>
        <p class="cta-modal__body">{{ cta.body }}</p>
        <div class="cta-modal__actions">
          <button class="btn-ghost" @click="dismiss">Plus tard</button>
          <button class="btn-primary" @click="goToOffer">{{ cta.cta || "Découvrir l'offre" }}</button>
        </div>
        <p class="cta-modal__legal">Sans engagement · paiement sécurisé · résiliable à tout moment.</p>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useArenaStore } from '@/stores/arena'

const arena = useArenaStore()
const router = useRouter()

const cta = computed(() => arena.cta)
const open = computed(() => Boolean(arena.cta))

function dismiss() {
  arena.track('cta_dismissed', { id: arena.cta?.id, trigger: arena.cta?.trigger })
  arena.dismissCta()
}

function goToOffer() {
  const target = arena.cta?.route || '/tarifs'
  arena.track('cta_clicked', { id: arena.cta?.id, trigger: arena.cta?.trigger })
  arena.dismissCta()
  router.push(target)
}
</script>

<style scoped>
.cta-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.55);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.cta-modal {
  width: 100%;
  max-width: 420px;
  background: #fff;
  border-radius: 18px;
  padding: 28px 24px 24px;
  box-shadow: 0 20px 60px rgba(15, 23, 42, 0.25);
  text-align: left;
}

.cta-modal__badge {
  display: inline-block;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  color: #fff;
  font-weight: 700;
  font-size: 12px;
  letter-spacing: 0.04em;
  padding: 4px 10px;
  border-radius: 999px;
  margin-bottom: 12px;
}

.cta-modal__title {
  margin: 0 0 8px;
  color: #0f172a;
  font-size: 20px;
  line-height: 1.3;
}

.cta-modal__body {
  margin: 0 0 20px;
  color: #475569;
  font-size: 15px;
  line-height: 1.5;
}

.cta-modal__actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-ghost {
  background: transparent;
  border: 1px solid #e2e8f0;
  color: #475569;
  padding: 10px 16px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
}

.btn-primary {
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  color: #fff;
  border: 0;
  padding: 10px 20px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 700;
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.25);
}

.cta-modal__legal {
  margin: 16px 0 0;
  color: #94a3b8;
  font-size: 11px;
  text-align: center;
}

.fade-enter-active, .fade-leave-active { transition: opacity .15s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
