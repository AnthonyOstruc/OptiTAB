<template>
  <a 
    :href="googleReviewsUrl" 
    target="_blank" 
    rel="noopener noreferrer" 
    class="google-reviews-compact"
    :class="{ 'inline': inline }"
  >
    <svg class="google-logo-svg" viewBox="0 0 256 262" aria-hidden="true">
      <path fill="#4285F4" d="M255.9 133.5c0-10.7-.9-18.5-2.9-26.6H130.6v48.2h71.9c-1.5 12-9.8 30-28.2 42.1l-.3 2.2 41 31.7 2.8.3c25.9-23.9 38.1-59.1 38.1-97.9z"/>
      <path fill="#34A853" d="M130.6 261.1c34.5 0 63.4-11.3 84.5-30.8l-40.2-31.1c-10.7 7.2-25.1 12.3-44.3 12.3-33.9 0-62.7-22.9-72.9-54.5l-2.1.2-41.7 32.2-.5 2c20.9 41.6 64 69.7 117.2 69.7z"/>
      <path fill="#FBBC05" d="M57.7 156.9c-2.7-8.1-4.3-16.8-4.3-25.9s1.6-17.8 4.2-25.9l-.1-2.3L15.2 70.1l-1.4.7C5.1 88.1 0 108.1 0 130.9c0 22.8 5.1 42.8 13.8 60.2l43.9-34.2z"/>
      <path fill="#EA4335" d="M130.6 50.4c24 0 40.1 10.4 49.3 19.2l36-35.1C193.8 12.6 165 0 130.6 0 77.4 0 34.3 28.1 13.4 69.7l43.9 34.2c10.3-31.6 39-53.5 73.3-53.5z"/>
    </svg>
    <span class="rating-text">
      <span class="star-icon">⭐</span>
      <span class="rating-badge">5/5</span>
    </span>
    <span class="link-text">— Voir sur Google</span>
  </a>
</template>

<script setup>
const props = defineProps({
  inline: {
    type: Boolean,
    default: false
  },
  googleReviewsUrl: {
    type: String,
    default: 'https://www.google.com/search?sa=X&sca_esv=87839103094c6a77&rlz=1C1ONGR_frFR997FR997&tbm=lcl&sxsrf=AE3TifM8SPH5m33A0ZODqZcHY3n5nxpSQA:1762342450222&q=OptiTAB+Avis&rflfq=1&num=20&stick=H4sIAAAAAAAAAONgkxI2MzU1tzA3MTY3tDQxMDS3MDEw2MDI-IqRx7-gJDPE0UnBsSyzeBErChcASF6_gzgAAAA&rldimm=6557874371940178400&hl=fr-FR&ved=2ahUKEwiviN-d9dqQAxWDNPsDHWjSMyYQ9fQKegQIRxAF&biw=733&bih=696&dpr=1.56#lkt=LocalPoiReviews'
  }
})
</script>

<style scoped lang="scss">
.google-reviews-compact {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  text-decoration: none;
  color: #6b7280;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  white-space: nowrap;
  
  &:hover {
    color: #1f2937;
    text-decoration: none;
    
    .link-text {
      text-decoration: underline;
    }
  }
  
  &.inline {
    display: inline-flex;
  }
  
  .google-logo-svg {
    height: 0.875rem; /* 14px */
    width: 0.875rem; /* 14px */
    flex-shrink: 0;
  }
  
  .rating-text {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    font-weight: 600;
    
    .star-icon {
      font-size: 0.875rem;
      line-height: 1;
      filter: brightness(1.2);
    }
    
    .rating-badge {
      font-size: 0.875rem;
      background: #fcd34d;
      color: #1f2937;
      padding: 0.125rem 0.375rem;
      border-radius: 0.25rem;
      font-weight: 700;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
  }
  
  .link-text {
    font-size: 0.875rem;
    color: #6b7280;
    transition: text-decoration 0.2s ease;
  }
}

/* Version footer (plus petit) */
.google-reviews-compact.footer-size {
  font-size: 0.8rem;
  gap: 0.3rem;
  
  .google-logo-svg {
    height: 0.75rem; /* 12px */
    width: 0.75rem; /* 12px */
    filter: brightness(1.2) saturate(1.3);
  }
  
  .rating-text {
    gap: 0.2rem;
    
    .star-icon {
      font-size: 0.75rem;
      filter: brightness(1.3) saturate(1.2);
    }
    
    .rating-badge {
      font-size: 0.75rem;
      background: #fcd34d;
      color: #1f2937;
      padding: 0.1rem 0.3rem;
      border-radius: 0.25rem;
      font-weight: 700;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }
  }
  
  .link-text {
    font-size: 0.8rem;
    color: #fff !important;
  }
}
</style>

