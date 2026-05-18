<template>
  <Teleport to="body">
    <Transition name="gemini-dialog-fade">
      <div v-if="open" class="gemini-dialog-backdrop" @mousedown.self="close">
        <div class="gemini-dialog" role="dialog" aria-modal="true" :aria-label="title">
          <header class="gemini-dialog__header">
            <div>
              <h2>{{ title }}</h2>
              <p>{{ subtitle }}</p>
            </div>
            <button class="gemini-dialog__close" type="button" @click="close" aria-label="Fermer">✕</button>
          </header>

          <section class="gemini-dialog__section">
            <h3 class="gemini-dialog__section-title">1. Type de carrousel</h3>
            <p class="gemini-dialog__hint">
              Le style visuel des images sera adapté à ce type.
            </p>
            <div class="gemini-dialog__cards">
              <button
                v-for="opt in CAROUSEL_TYPES"
                :key="opt.id"
                type="button"
                class="gemini-dialog__card"
                :class="{ 'gemini-dialog__card--active': carouselType === opt.id }"
                @click="carouselType = opt.id"
              >
                <span class="gemini-dialog__card-icon">{{ opt.icon }}</span>
                <span class="gemini-dialog__card-info">
                  <span class="gemini-dialog__card-label">{{ opt.label }}</span>
                  <span class="gemini-dialog__card-desc">{{ opt.description }}</span>
                </span>
              </button>
            </div>
          </section>

          <section class="gemini-dialog__section">
            <h3 class="gemini-dialog__section-title">2. Quelles slides recevront une image ?</h3>
            <p class="gemini-dialog__hint">
              Pour un rendu pro, on recommande hook + CTA uniquement. Les slides du milieu restent en typographie pure pour la lisibilité.
            </p>
            <div class="gemini-dialog__options">
              <label
                v-for="opt in SLIDE_STRATEGIES"
                :key="opt.id"
                class="gemini-dialog__option"
                :class="{ 'gemini-dialog__option--active': strategy === opt.id }"
              >
                <input
                  type="radio"
                  name="gemini-strategy"
                  :value="opt.id"
                  v-model="strategy"
                />
                <span class="gemini-dialog__option-info">
                  <span class="gemini-dialog__option-label">
                    {{ opt.label }}
                    <span v-if="opt.badge" class="gemini-dialog__badge">{{ opt.badge }}</span>
                  </span>
                  <span class="gemini-dialog__option-desc">{{ opt.description }}</span>
                </span>
              </label>
            </div>
          </section>

          <section class="gemini-dialog__section">
            <h3 class="gemini-dialog__section-title">3. Utiliser les screenshots OptiTAB ?</h3>
            <p class="gemini-dialog__hint">
              Les captures dans <code>backend/reel_studio/site_references/</code> sont envoyées à Gemini comme référence visuelle pour reproduire fidèlement ton interface.
            </p>
            <label class="gemini-dialog__toggle" :class="{ 'gemini-dialog__toggle--active': useReferences }">
              <input type="checkbox" v-model="useReferences" />
              <span class="gemini-dialog__toggle-info">
                <span class="gemini-dialog__toggle-label">
                  {{ useReferences ? '✅ Utiliser les références' : '⛔ Ne pas utiliser les références' }}
                </span>
                <span class="gemini-dialog__toggle-desc">
                  {{ useReferences
                    ? "Gemini verra tes captures et reproduira l'UI OptiTAB dans les mockups d'écran."
                    : "Gemini ignore les captures, génère librement (utile pour des images génériques ou si le rendu de l'UI n'est pas adapté)." }}
                </span>
              </span>
            </label>
          </section>

          <footer class="gemini-dialog__footer">
            <div class="gemini-dialog__cost-hint">
              <span class="gemini-dialog__cost-icon">💸</span>
              <span>
                Environ <strong>{{ estimatedCount }}</strong> image(s) générée(s) –
                réduit le coût Gemini et améliore la cohérence visuelle.
              </span>
            </div>
            <div class="gemini-dialog__actions">
              <button class="gemini-dialog__btn gemini-dialog__btn--ghost" type="button" @click="close">
                Annuler
              </button>
              <button class="gemini-dialog__btn gemini-dialog__btn--primary" type="button" @click="confirm">
                {{ confirmLabel }}
              </button>
            </div>
          </footer>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  open: { type: Boolean, default: false },
  title: { type: String, default: 'Options de génération Gemini' },
  subtitle: { type: String, default: 'Choisis le style et la portée pour des images cohérentes et professionnelles.' },
  confirmLabel: { type: String, default: 'Lancer la génération' },
  totalSlides: { type: Number, default: 0 },
  initialCarouselType: { type: String, default: 'marketing' },
  initialStrategy: { type: String, default: 'hook_cta' },
  initialUseReferences: { type: Boolean, default: true },
})

const emit = defineEmits(['close', 'confirm'])

const CAROUSEL_TYPES = [
  { id: 'marketing', label: 'Marketing / Conversion', icon: '🚀', description: 'Premium éditorial, mockup produit' },
  { id: 'notion', label: 'Notion pédagogique', icon: '📐', description: 'Tableau noir, formules abstraites' },
  { id: 'tips', label: 'Conseils & Astuces', icon: '💡', description: 'Inspirant, lumineux' },
  { id: 'quiz', label: 'Quiz / QCM', icon: '🎯', description: 'Ludique, gamifié' },
  { id: 'avantapres', label: 'Avant / Après', icon: '🔄', description: 'Split-screen, transformation' },
  { id: 'story', label: 'Storytelling', icon: '📖', description: 'Narratif, cinématographique' },
]

const SLIDE_STRATEGIES = [
  {
    id: 'hook_cta',
    label: 'Hook + CTA',
    badge: 'Recommandé',
    description: 'Image sur la 1ère et la dernière slide uniquement. Rendu le plus pro.',
  },
  {
    id: 'hook',
    label: 'Hook seul',
    description: 'Image uniquement sur la slide d\'accroche.',
  },
  {
    id: 'cta',
    label: 'CTA seul',
    description: 'Image uniquement sur la slide finale.',
  },
  {
    id: 'all',
    label: 'Toutes les slides',
    description: 'Une image générée pour chaque slide. Plus coûteux et moins cohérent visuellement.',
  },
  {
    id: 'none',
    label: 'Aucune image',
    description: 'Garde le texte seulement (idéal si tu veux ajouter tes propres visuels).',
  },
]

const carouselType = ref(props.initialCarouselType || 'marketing')
const strategy = ref(props.initialStrategy || 'hook_cta')
const useReferences = ref(props.initialUseReferences !== false)

watch(() => props.open, (val) => {
  if (val) {
    carouselType.value = props.initialCarouselType || 'marketing'
    strategy.value = props.initialStrategy || 'hook_cta'
    useReferences.value = props.initialUseReferences !== false
  }
})

const estimatedCount = computed(() => {
  const total = Number(props.totalSlides) || 0
  switch (strategy.value) {
    case 'all':
      return total || '?'
    case 'hook':
    case 'cta':
      return 1
    case 'none':
      return 0
    case 'hook_cta':
    default:
      return total >= 2 ? 2 : total
  }
})

function close() {
  emit('close')
}

function confirm() {
  emit('confirm', {
    carouselType: carouselType.value,
    strategy: strategy.value,
    useReferences: useReferences.value,
  })
}
</script>

<style scoped>
.gemini-dialog-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 30000;
  padding: 24px;
  backdrop-filter: blur(2px);
}

.gemini-dialog {
  width: min(640px, 100%);
  max-height: 90vh;
  background: #ffffff;
  border-radius: 18px;
  box-shadow: 0 24px 64px rgba(15, 23, 42, 0.32);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.gemini-dialog__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 20px 24px 12px;
  border-bottom: 1px solid #f1f5f9;
}
.gemini-dialog__header h2 {
  margin: 0;
  font-size: 18px;
  color: #29428e;
}
.gemini-dialog__header p {
  margin: 4px 0 0;
  font-size: 13px;
  color: #64748b;
}
.gemini-dialog__close {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #94a3b8;
  padding: 4px 8px;
  border-radius: 6px;
}
.gemini-dialog__close:hover { background: #f1f5f9; color: #475569; }

.gemini-dialog__section {
  padding: 16px 24px;
  border-bottom: 1px solid #f1f5f9;
  overflow-y: auto;
}
.gemini-dialog__section:last-of-type { border-bottom: none; }

.gemini-dialog__section-title {
  margin: 0 0 4px;
  font-size: 13px;
  font-weight: 700;
  color: #1e293b;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.gemini-dialog__hint {
  margin: 0 0 12px;
  font-size: 12px;
  color: #64748b;
  line-height: 1.45;
}

.gemini-dialog__cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.gemini-dialog__card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  background: #ffffff;
  cursor: pointer;
  text-align: left;
  transition: all 0.12s;
}
.gemini-dialog__card:hover { border-color: #c7d2fe; background: #f8faff; }
.gemini-dialog__card--active {
  border-color: #29428e;
  background: #eef2ff;
  box-shadow: 0 0 0 3px rgba(41, 66, 142, 0.12);
}

.gemini-dialog__card-icon {
  font-size: 20px;
  flex: 0 0 auto;
}

.gemini-dialog__card-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.gemini-dialog__card-label {
  font-weight: 700;
  font-size: 13px;
  color: #1e293b;
}

.gemini-dialog__card-desc {
  font-size: 11px;
  color: #64748b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.gemini-dialog__options {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.gemini-dialog__option {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 12px;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.12s;
}
.gemini-dialog__option:hover { border-color: #c7d2fe; background: #f8faff; }
.gemini-dialog__option--active {
  border-color: #29428e;
  background: #eef2ff;
  box-shadow: 0 0 0 3px rgba(41, 66, 142, 0.12);
}

.gemini-dialog__option input {
  margin-top: 3px;
  accent-color: #29428e;
}

.gemini-dialog__option-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.gemini-dialog__option-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 13px;
  color: #1e293b;
}

.gemini-dialog__badge {
  background: #29428e;
  color: #ffffff;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 999px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.gemini-dialog__option-desc {
  font-size: 12px;
  color: #64748b;
  line-height: 1.4;
}

.gemini-dialog__toggle {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 14px;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  background: #fafbff;
  cursor: pointer;
  transition: all 0.12s;
}
.gemini-dialog__toggle:hover { border-color: #c7d2fe; background: #f4f6ff; }
.gemini-dialog__toggle--active {
  border-color: #29428e;
  background: #eef2ff;
  box-shadow: 0 0 0 3px rgba(41, 66, 142, 0.10);
}
.gemini-dialog__toggle input {
  margin-top: 3px;
  accent-color: #29428e;
  width: 16px;
  height: 16px;
}
.gemini-dialog__toggle-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}
.gemini-dialog__toggle-label {
  font-weight: 700;
  font-size: 13px;
  color: #1e293b;
}
.gemini-dialog__toggle-desc {
  font-size: 12px;
  color: #64748b;
  line-height: 1.4;
}

.gemini-dialog__footer {
  padding: 14px 24px 18px;
  border-top: 1px solid #f1f5f9;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: #fafbff;
}

.gemini-dialog__cost-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #475569;
}
.gemini-dialog__cost-icon { font-size: 16px; }
.gemini-dialog__cost-hint strong { color: #29428e; }

.gemini-dialog__actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.gemini-dialog__btn {
  padding: 9px 18px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  border: none;
  transition: all 0.12s;
}

.gemini-dialog__btn--ghost {
  background: transparent;
  color: #64748b;
  border: 1px solid #e2e8f0;
}
.gemini-dialog__btn--ghost:hover { background: #f1f5f9; color: #1e293b; }

.gemini-dialog__btn--primary {
  background: #29428e;
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(41, 66, 142, 0.28);
}
.gemini-dialog__btn--primary:hover {
  background: #1c3070;
  box-shadow: 0 4px 12px rgba(41, 66, 142, 0.36);
}

.gemini-dialog-fade-enter-active,
.gemini-dialog-fade-leave-active {
  transition: opacity 0.18s;
}
.gemini-dialog-fade-enter-from,
.gemini-dialog-fade-leave-to {
  opacity: 0;
}
.gemini-dialog-fade-enter-active .gemini-dialog,
.gemini-dialog-fade-leave-active .gemini-dialog {
  transition: transform 0.22s;
}
.gemini-dialog-fade-enter-from .gemini-dialog,
.gemini-dialog-fade-leave-to .gemini-dialog {
  transform: translateY(12px) scale(0.98);
}
</style>
