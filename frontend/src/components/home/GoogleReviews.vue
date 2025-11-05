<template>
  <section class="google-reviews-section">
    <div class="reviews-header">
      <a href="https://maps.google.com/?q=OptiTAB" target="_blank" rel="noopener noreferrer" class="google-badge">
        <div class="google-badge-top">
          <!-- Logo Google (SVG propre) -->
          <svg class="google-logo-svg" viewBox="0 0 256 262" aria-hidden="true">
            <path fill="#4285F4" d="M255.9 133.5c0-10.7-.9-18.5-2.9-26.6H130.6v48.2h71.9c-1.5 12-9.8 30-28.2 42.1l-.3 2.2 41 31.7 2.8.3c25.9-23.9 38.1-59.1 38.1-97.9z"/>
            <path fill="#34A853" d="M130.6 261.1c34.5 0 63.4-11.3 84.5-30.8l-40.2-31.1c-10.7 7.2-25.1 12.3-44.3 12.3-33.9 0-62.7-22.9-72.9-54.5l-2.1.2-41.7 32.2-.5 2c20.9 41.6 64 69.7 117.2 69.7z"/>
            <path fill="#FBBC05" d="M57.7 156.9c-2.7-8.1-4.3-16.8-4.3-25.9s1.6-17.8 4.2-25.9l-.1-2.3L15.2 70.1l-1.4.7C5.1 88.1 0 108.1 0 130.9c0 22.8 5.1 42.8 13.8 60.2l43.9-34.2z"/>
            <path fill="#EA4335" d="M130.6 50.4c24 0 40.1 10.4 49.3 19.2l36-35.1C193.8 12.6 165 0 130.6 0 77.4 0 34.3 28.1 13.4 69.7l43.9 34.2c10.3-31.6 39-53.5 73.3-53.5z"/>
          </svg>
          <!-- Note en pastille -->
          <span class="rating-badge">
            5
          </span>
          <!-- Etoiles (SVG, accessible) -->
          <span class="stars" aria-label="Note moyenne 5 sur 5">
            <svg v-for="i in 5" :key="i" class="star" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path d="M10 1.7l2.36 4.78 5.28.77-3.82 3.72.9 5.26L10 13.9 5.28 16.2l.9-5.26L2.36 7.25l5.28-.77L10 1.7z"/>
            </svg>
          </span>
          <!-- Message -->
          <span class="reviews-text">Les élèves adorent OptiTAB</span>
        </div>
        <!-- Ligne source (petit) -->
        <div class="google-badge-footer">
          <span>Données&nbsp;: Google</span>
          <span>•</span>
          <span>MAJ&nbsp;05/11/2025</span>
          <span class="footer-separator">•</span>
          <span class="footer-link">Voir sur Google</span>
        </div>
      </a>
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped lang="scss">
.google-reviews-section {
  background: #ffffff;
  padding: 4rem 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.reviews-header {
  text-align: center;
}

.google-badge {
  display: inline-flex;
  flex-direction: column;
  align-items: flex-start;
  width: fit-content;
  margin: 0 auto;
  padding: 0.625rem; /* p-2.5 */
  border-radius: 0.5rem; /* rounded-lg */
  border: 1px solid #e5e7eb; /* border-gray-200 */
  background: rgba(255, 255, 255, 0.7); /* bg-white/70 */
  backdrop-filter: blur(8px);
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); /* shadow-sm */
  text-decoration: none;
  color: inherit;
  cursor: pointer;
  transition: all 0.2s ease;
}

.google-badge:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); /* shadow-md */
  text-decoration: none;
  color: inherit;
}

.google-badge-top {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem; /* gap-2 */
  flex-wrap: wrap;
}

.google-badge > .google-badge-footer {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  flex-wrap: wrap;
}

.google-logo-svg {
  height: 0.9375rem; /* 15px */
  width: 0.9375rem; /* 15px */
  flex-shrink: 0;
}

.rating-badge {
  background: #f59e0b; /* bg-amber-500 */
  color: white;
  font-weight: 600; /* font-semibold */
  font-size: 0.75rem; /* text-xs */
  padding: 0.125rem 0.5rem; /* px-2 py-0.5 */
  border-radius: 0.5rem; /* rounded-lg */
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); /* shadow-sm */
}

.stars {
  display: inline-flex;
  align-items: center;
  gap: 0;
}

.star {
  width: 0.9375rem; /* 15px */
  height: 0.9375rem; /* 15px */
  color: #fbbf24; /* text-amber-400 */
}

.reviews-text {
  color: #1f2937; /* text-gray-800 */
  font-size: 0.875rem; /* text-sm */
}

.google-badge-footer {
  margin-top: 0.5rem; /* mt-2 */
  display: flex;
  align-items: center;
  gap: 0.5rem; /* gap-2 */
  font-size: 0.75rem; /* text-xs */
  color: #6b7280; /* text-gray-500 */
}

.footer-separator {
  opacity: 0.6;
}

.footer-link {
  transition: text-decoration 0.2s ease;
}

.google-badge:hover .footer-link {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .google-reviews-section {
    padding: 3rem 1rem;
  }

  .google-badge {
    max-width: 100%;
  }

  .google-badge-top {
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem;
  }

  .google-badge-footer {
    flex-wrap: wrap;
    justify-content: center;
    font-size: 0.7rem;
  }
}
</style>

