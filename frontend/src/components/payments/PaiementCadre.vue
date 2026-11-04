<template>
  <div class="pc">
    <a href="/" class="pc-logo" aria-label="OptiTAB, accueil">
      <img src="/Logo_bg.png" alt="OptiTAB" width="132" height="43" />
    </a>
    <main class="pc-carte" aria-live="polite">
      <slot />
    </main>
    <p class="pc-aide">
      Une question ? <a href="https://wa.me/33764040251" target="_blank" rel="noopener noreferrer">WhatsApp</a>
      ou <a href="mailto:contact@optitab.net">contact@optitab.net</a>
    </p>
  </div>
</template>

<script setup>
// Cadre des pages de retour de paiement (réussi, annulé) : logo, carte centrée,
// contact. Pages autonomes : elles servent aussi aux visiteurs non connectés.
</script>

<style scoped>
.pc {
  --pc-navy: #1b3c8e;
  --pc-navy-dark: #122a66;
  --pc-ink: #172033;
  --pc-soft: #3a4357;
  --pc-muted: #667085;
  --pc-line: #e3e7ef;
  --pc-green: #3b8544;
  --pc-green-50: #eaf4ea;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  padding: 32px 16px 28px;
  background:
    radial-gradient(900px 420px at 50% -120px, rgba(27, 60, 142, 0.08), transparent 70%),
    #f5f7fb;
  font-family: 'Montserrat', 'Segoe UI', system-ui, sans-serif;
  color: var(--pc-ink);
}

.pc-logo {
  display: inline-flex;
  margin-bottom: 40px;
}

.pc-logo img {
  width: 132px;
  height: auto;
}

.pc-carte {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: min(520px, 100%);
  padding: 40px 36px 36px;
  border: 1px solid var(--pc-line);
  border-radius: 24px;
  background: #fff;
  box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04), 0 18px 48px rgba(18, 42, 102, 0.08);
  text-align: center;
}

.pc-aide {
  margin: 24px 0 0;
  text-align: center;
  font-size: 14px;
  color: var(--pc-muted);
}

.pc-aide a {
  font-weight: 700;
  color: var(--pc-navy);
}

@media (max-width: 520px) {
  .pc-logo {
    margin-bottom: 28px;
  }

  .pc-carte {
    padding: 32px 22px 26px;
    border-radius: 20px;
  }
}

</style>

<style>
/* Éléments communs aux pages de retour de paiement (contenu de la carte). */
@keyframes pc-apparition {
  from { transform: scale(0.6); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.pc-carte h1 {
  margin: 0 0 10px;
  font-size: 26px;
  font-weight: 700;
  line-height: 1.25;
  letter-spacing: -0.01em;
  color: var(--pc-ink);
}

.pc-carte .pc-texte {
  max-width: 400px;
  margin: 0 0 24px;
  font-size: 16px;
  line-height: 1.55;
  color: var(--pc-soft);
}

.pc-carte .pc-icone {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 72px;
  height: 72px;
  margin-bottom: 20px;
  border-radius: 50%;
  background: var(--pc-green-50);
  color: var(--pc-green);
  animation: pc-apparition 0.35s ease-out;
}

.pc-carte .pc-icone svg {
  width: 36px;
  height: 36px;
  stroke-width: 2.4;
}

.pc-carte .pc-icone--neutre {
  background: #eef1f8;
  color: var(--pc-navy);
}

.pc-carte .pc-icone--alerte {
  background: #fdf3e6;
  color: #a8620f;
}

.pc-carte .pc-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  min-height: 50px;
  padding: 0 22px;
  border-radius: 14px;
  background: var(--pc-navy);
  font: 600 16px 'Montserrat', sans-serif;
  color: #fff;
  text-decoration: none;
  transition: background-color 0.15s ease;
}

.pc-carte .pc-btn:hover {
  background: var(--pc-navy-dark);
}

.pc-carte .pc-btn svg {
  width: 18px;
  height: 18px;
}

.pc-carte .pc-lien {
  margin-top: 14px;
  font-size: 15px;
  font-weight: 600;
  color: var(--pc-navy);
  text-decoration: none;
}

.pc-carte .pc-lien:hover {
  text-decoration: underline;
}

@media (max-width: 520px) {
  .pc-carte h1 {
    font-size: 23px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .pc-carte .pc-icone {
    animation: none;
  }
}
</style>
