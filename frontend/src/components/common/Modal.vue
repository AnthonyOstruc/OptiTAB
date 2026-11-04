<template>
  <Teleport to="body">
    <Transition name="om">
      <div v-if="isOpen" class="om" :class="`om--${size}`">
        <div class="om-overlay" role="presentation" @click="handleOverlayClick" />
        <div
          ref="panneau"
          class="om-panel"
          :class="contentClass"
          role="dialog"
          aria-modal="true"
          :aria-labelledby="title ? titleId : undefined"
          :aria-label="title ? undefined : ariaLabel"
          tabindex="-1"
          @click.stop
          @keydown="surTouche"
        >
          <span class="om-handle" aria-hidden="true" />
          <header v-if="showHeader && (title || icon)" :class="['om-head', { 'om-head--center': centered }]">
            <span v-if="icon" class="om-head__icon"><component :is="icon" aria-hidden="true" /></span>
            <div class="om-head__text">
              <p v-if="eyebrow" class="om-head__eyebrow">{{ eyebrow }}</p>
              <h2 v-if="title" :id="titleId" class="om-head__title">{{ title }}</h2>
              <p v-if="subtitle" class="om-head__subtitle">{{ subtitle }}</p>
            </div>
          </header>
          <button
            v-if="showHeader && showCloseButton && canClose"
            type="button"
            class="om-close"
            :aria-label="closeButtonLabel"
            @click="handleClose"
          >
            <XMarkIcon aria-hidden="true" />
          </button>
          <div class="om-body">
            <slot />
          </div>
          <footer v-if="$slots.footer" class="om-foot">
            <slot name="footer" />
          </footer>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'
import { lockBodyScroll, unlockBodyScroll } from '@/utils/bodyScrollLock'

// Cadre commun de toutes les fenêtres du site (connexion, inscription, choix de
// la classe, abonnement, contact…). Même design que la vitrine et l'espace :
// carte centrée sur ordinateur, panneau qui monte du bas sur téléphone.
// Accessibilité : focus gardé dans la fenêtre, Échap pour fermer, page
// derrière bloquée, focus rendu à l'élément d'origine à la fermeture.
// Les styles communs (.om-btn, .om-field, .om-divider…) sont plus bas, non limités.
const props = defineProps({
  isOpen: { type: Boolean, default: false },
  title: { type: String, default: '' },
  // Petite ligne au-dessus du titre, et phrase sous le titre.
  eyebrow: { type: String, default: '' },
  subtitle: { type: String, default: '' },
  // Pictogramme (composant heroicons) affiché à gauche du titre.
  icon: { type: [Object, Function], default: null },
  centered: { type: Boolean, default: false },
  ariaLabel: { type: String, default: 'Fenêtre' },
  showHeader: { type: Boolean, default: true },
  showCloseButton: { type: Boolean, default: true },
  closeButtonLabel: { type: String, default: 'Fermer' },
  closeOnOverlay: { type: Boolean, default: true },
  canClose: { type: Boolean, default: true },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large', 'full'].includes(value)
  },
  contentClass: { type: String, default: '' }
})

const emit = defineEmits(['close', 'overlay-click'])

const panneau = ref(null)
const titleId = `om-titre-${Math.random().toString(36).slice(2, 9)}`
let focusAvant = null

const handleClose = () => emit('close')

const handleOverlayClick = () => {
  if (props.closeOnOverlay && props.canClose) {
    emit('overlay-click')
    emit('close')
  }
}

// ---------- Page bloquée derrière (même outil que le reste du site, fiable sur iPhone) ----------
const cleBlocage = `fenetre-${titleId}`
function bloquerPage(oui) {
  if (oui) lockBodyScroll(cleBlocage, { mode: 'fixed' })
  else unlockBodyScroll(cleBlocage)
}

const FOCUSABLES = 'a[href], button:not([disabled]), input:not([disabled]):not([type="hidden"]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
const focusables = () => [...(panneau.value?.querySelectorAll(FOCUSABLES) || [])].filter((el) => el.offsetParent !== null)

function surTouche(event) {
  if (event.key === 'Escape' && props.canClose) {
    event.stopPropagation()
    handleClose()
    return
  }
  if (event.key !== 'Tab') return
  const liste = focusables()
  if (!liste.length) return
  const premier = liste[0]
  const dernier = liste[liste.length - 1]
  if (event.shiftKey && document.activeElement === premier) {
    event.preventDefault()
    dernier.focus()
  } else if (!event.shiftKey && document.activeElement === dernier) {
    event.preventDefault()
    premier.focus()
  }
}

async function ouvrir() {
  focusAvant = document.activeElement
  bloquerPage(true)
  await nextTick()
  // Premier champ à remplir, sinon la fenêtre elle-même (sans faire défiler).
  const champ = panneau.value?.querySelector('input:not([type="hidden"]):not([type="checkbox"]):not([disabled]), textarea, select')
  const cible = champ && window.matchMedia('(min-width: 641px)').matches ? champ : panneau.value
  cible?.focus({ preventScroll: true })
}

function fermer() {
  bloquerPage(false)
  if (focusAvant && typeof focusAvant.focus === 'function' && document.contains(focusAvant)) {
    focusAvant.focus({ preventScroll: true })
  }
  focusAvant = null
}

watch(() => props.isOpen, (ouverte, avant) => {
  if (ouverte && !avant) ouvrir()
  else if (!ouverte && avant) fermer()
})

// Échap aussi quand le focus est resté hors de la fenêtre.
function surToucheDocument(event) {
  if (props.isOpen && event.key === 'Escape' && props.canClose && !panneau.value?.contains(event.target)) handleClose()
}

onMounted(() => {
  document.addEventListener('keydown', surToucheDocument)
  if (props.isOpen) ouvrir()
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', surToucheDocument)
  if (props.isOpen) fermer()
})
</script>

<style>
/* ---------- Cadre ---------- */

.om {
  --om-navy: #1b3c8e;
  --om-navy-700: #163274;
  --om-navy-900: #0d1f4f;
  --om-navy-100: #dfe6f5;
  --om-navy-50: #f1f4fb;
  --om-green: #5fac60;
  --om-green-700: #2f7a3a;
  --om-green-50: #ecf7ec;
  --om-orange-50: #fef4e6;
  --om-orange-700: #9a5c0f;
  --om-red: #c0392b;
  --om-red-50: #fdeeec;
  --om-ink: #121a33;
  --om-ink-soft: #2c3550;
  --om-muted: #5d667d;
  --om-line: #e4e8f0;
  --om-line-strong: #cfd6e4;
  --om-bg-soft: #f6f8fc;
  --om-font: 'Montserrat', 'Segoe UI', system-ui, -apple-system, sans-serif;

  position: fixed;
  inset: 0;
  z-index: 13000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  font-family: var(--om-font);
  color: var(--om-ink);
}

.om-overlay {
  position: absolute;
  inset: 0;
  background: rgba(13, 31, 79, 0.48);
  backdrop-filter: blur(6px);
}

.om-panel {
  position: relative;
  width: 100%;
  max-width: 600px;
  max-height: calc(100dvh - 48px);
  overflow-y: auto;
  overscroll-behavior: contain;
  padding: 32px;
  border-radius: 24px;
  background: #fff;
  box-shadow: 0 2px 6px rgba(16, 32, 79, 0.08), 0 32px 80px rgba(16, 32, 79, 0.28);
  outline: none;
}

.om--small .om-panel { max-width: 460px; }
.om--medium .om-panel { max-width: 600px; }
.om--large .om-panel { max-width: 780px; }
.om--full .om-panel { max-width: 1100px; }

.om-handle {
  display: none;
}

.om-head {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  margin: 0 40px 22px 0;
}

.om-head--center {
  flex-direction: column;
  align-items: center;
  margin: 0 0 22px;
  text-align: center;
}

.om-head__icon {
  display: inline-grid;
  flex-shrink: 0;
  place-items: center;
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: var(--om-navy-50);
  color: var(--om-navy);
}

.om-head__icon svg {
  width: 26px;
  height: 26px;
}

.om-head__eyebrow {
  margin: 0 0 4px;
  color: var(--om-green-700);
  font-size: 12.5px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.om-head__title {
  margin: 0;
  color: var(--om-navy-900);
  font-size: 24px;
  font-weight: 700;
  line-height: 1.25;
  letter-spacing: -0.01em;
}

.om-head__subtitle {
  margin: 6px 0 0;
  color: var(--om-muted);
  font-size: 15px;
  line-height: 1.5;
}

.om-close {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 2;
  display: inline-grid;
  place-items: center;
  width: 40px;
  height: 40px;
  border: 0;
  border-radius: 50%;
  background: var(--om-bg-soft);
  color: var(--om-ink-soft);
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.om-close:hover {
  background: var(--om-navy-50);
  color: var(--om-navy);
}

.om-close:focus-visible {
  outline: 2px solid var(--om-navy);
  outline-offset: 2px;
}

.om-close svg {
  width: 22px;
  height: 22px;
}

.om-foot {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid var(--om-line);
}

/* Téléphone : panneau qui monte du bas de l'écran */
@media (max-width: 640px) {
  .om {
    align-items: flex-end;
    padding: 0;
  }

  .om-panel,
  .om--small .om-panel,
  .om--medium .om-panel,
  .om--large .om-panel,
  .om--full .om-panel {
    max-width: none;
    max-height: 92dvh;
    padding: 28px 20px calc(24px + env(safe-area-inset-bottom, 0px));
    border-radius: 24px 24px 0 0;
  }

  .om-handle {
    position: absolute;
    top: 10px;
    left: 50%;
    display: block;
    width: 40px;
    height: 4px;
    margin-left: -20px;
    border-radius: 999px;
    background: var(--om-line-strong);
  }

  .om-head {
    gap: 12px;
    margin-bottom: 18px;
  }

  .om-head__icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
  }

  .om-head__icon svg {
    width: 22px;
    height: 22px;
  }

  .om-head__title {
    font-size: 21px;
  }

  .om-head__subtitle {
    margin-top: 4px;
    font-size: 14px;
  }

  .om-close {
    top: 16px;
    right: 14px;
  }

  /* Formulaires plus serrés (connexion, inscription, mot de passe oublié…) */
  .om .om-panel .dynamic-form {
    gap: 12px;
  }

  .om .om-panel .form-fields {
    gap: 14px;
  }

  .om .om-panel .form-group,
  .om .om-panel .om-field {
    gap: 6px;
  }

  .om .om-panel .form-label,
  .om .om-panel .om-label {
    font-size: 13.5px;
  }

  /* 16 px minimum : en dessous, l'iPhone zoome dans la page au toucher d'un champ. */
  .om .om-panel .form-input,
  .om .om-panel .om-input {
    min-height: 46px;
    padding: 10px 14px;
    font-size: 16px;
  }

  .om .om-panel .input-wrapper:has(.password-toggle) .form-input {
    padding-right: 46px;
  }

  .om .om-panel .form-submit-btn {
    min-height: 48px;
  }

  .om .om-panel .om-divider {
    margin: 16px 0;
  }

  .om .om-panel .om-btn {
    min-height: 48px;
  }
}

/* Apparition */
.om-enter-active,
.om-leave-active {
  transition: opacity 0.22s ease;
}

.om-enter-active .om-panel,
.om-leave-active .om-panel {
  transition: transform 0.26s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.om-enter-from,
.om-leave-to {
  opacity: 0;
}

.om-enter-from .om-panel,
.om-leave-to .om-panel {
  transform: translateY(14px) scale(0.98);
}

@media (max-width: 640px) {
  .om-enter-from .om-panel,
  .om-leave-to .om-panel {
    transform: translateY(100%);
  }
}

@media (prefers-reduced-motion: reduce) {
  .om-enter-active,
  .om-leave-active,
  .om-enter-active .om-panel,
  .om-leave-active .om-panel {
    transition: none;
  }
}

/* ---------- Éléments communs à toutes les fenêtres ---------- */

.om-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 50px;
  padding: 0 24px;
  border: 1.5px solid transparent;
  border-radius: 999px;
  font: 600 15.5px/1.2 var(--om-font, 'Montserrat', sans-serif);
  text-decoration: none;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s, color 0.2s, box-shadow 0.2s;
}

.om-btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.om-btn--block {
  width: 100%;
}

.om-btn--primary {
  background: var(--om-navy, #1b3c8e);
  color: #fff;
}

.om-btn--primary:hover:not(:disabled) {
  background: var(--om-navy-700, #163274);
  box-shadow: 0 8px 22px rgba(27, 60, 142, 0.25);
}

.om-btn--green {
  background: var(--om-green-700, #2f7a3a);
  color: #fff;
}

.om-btn--green:hover:not(:disabled) {
  background: #276832;
}

.om-btn--danger {
  background: var(--om-red, #c0392b);
  color: #fff;
}

.om-btn--danger:hover:not(:disabled) {
  background: #a33024;
}

.om-btn--ghost {
  border-color: var(--om-line-strong, #cfd6e4);
  background: #fff;
  color: var(--om-ink, #121a33);
}

.om-btn--ghost:hover:not(:disabled) {
  border-color: var(--om-navy, #1b3c8e);
  color: var(--om-navy, #1b3c8e);
}

.om-btn svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.om-link {
  padding: 0;
  border: 0;
  background: none;
  color: var(--om-navy, #1b3c8e);
  font: inherit;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
}

.om-link:hover {
  text-decoration: underline;
}

.om-divider {
  display: flex;
  align-items: center;
  gap: 14px;
  margin: 22px 0;
  color: var(--om-muted, #5d667d);
  font-size: 13.5px;
}

.om-divider::before,
.om-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--om-line, #e4e8f0);
}

.om-alert {
  margin: 0;
  padding: 12px 14px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.5;
}

.om-alert--error {
  border: 1px solid #f3c4bd;
  background: var(--om-red-50, #fdeeec);
  color: #8e2a1f;
}

.om-alert--success {
  border: 1px solid #cfe7cf;
  background: var(--om-green-50, #ecf7ec);
  color: var(--om-green-700, #2f7a3a);
}

.om-alert--info {
  border: 1px solid var(--om-navy-100, #dfe6f5);
  background: var(--om-navy-50, #f1f4fb);
  color: var(--om-navy-900, #0d1f4f);
}

.om-field {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.om-label {
  color: var(--om-ink-soft, #2c3550);
  font-size: 14px;
  font-weight: 600;
}

.om-input,
.om .om-input {
  width: 100%;
  min-height: 48px;
  padding: 12px 16px;
  border: 1.5px solid var(--om-line-strong, #cfd6e4);
  border-radius: 12px;
  background: #fff;
  color: var(--om-ink, #121a33);
  font: 500 15.5px/1.4 var(--om-font, 'Montserrat', sans-serif);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.om-input::placeholder {
  color: #8a93a8;
  font-weight: 500;
}

.om-input:focus {
  border-color: var(--om-navy, #1b3c8e);
  outline: none;
  box-shadow: 0 0 0 4px rgba(27, 60, 142, 0.12);
}

textarea.om-input {
  min-height: 120px;
  resize: vertical;
}

.om-check {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  color: var(--om-ink-soft, #2c3550);
  font-size: 14px;
  line-height: 1.5;
  cursor: pointer;
}

.om-check input {
  width: 18px;
  height: 18px;
  margin: 1px 0 0;
  flex-shrink: 0;
  accent-color: var(--om-navy, #1b3c8e);
}
</style>
