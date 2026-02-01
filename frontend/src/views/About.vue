<template>
  <MainLayout>
    <div class="about-zoom" :style="aboutZoomStyle">
      <div ref="aboutContentRef" class="about-page">
      <!-- Hero Section Pédagogique -->
      <div class="hero-section">
        <div class="hero-content">
          <h1 class="hero-title">
            Votre enfant mérite le 
            <span class="gradient-text">meilleur accompagnement</span>
          </h1>
          <p class="hero-subtitle">
            OptiTAB révolutionne l'apprentissage des mathématiques avec une approche 
            pédagogique éprouvée, des outils interactifs et un suivi personnalisé 
            pour garantir la réussite de votre enfant.
          </p>
          <div class="hero-stats">
            <div class="stat-item">
              <span class="stat-number">95%</span>
              <span class="stat-label">Amélioration des notes</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">+1000</span>
              <span class="stat-label">Cours, exercices et synthèses</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">7/7</span>
              <span class="stat-label">Support disponible</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Section Pourquoi OptiTAB -->
      <div class="why-section">
        <div class="container">
          <div class="section-intro">
            <h2 class="section-title">Pourquoi les parents choisissent OptiTAB ?</h2>
            <p class="section-subtitle">
              Une approche pédagogique éprouvée qui transforme l'apprentissage des mathématiques
            </p>
          </div>
          <div class="benefits-grid">
            <div class="benefit-card">
              <div class="benefit-icon">
                <img src="/icons/ResultatsGarantis.svg?v=2" alt="Résultats" class="icon" />
              </div>
              <h3>Résultats Garantis</h3>
              <p>Votre enfant pratique avec des exercices progressifs et reçoit des corrections détaillées pour progresser efficacement</p>
            </div>
            <div class="benefit-card">
              <div class="benefit-icon">
                <img src="/icons/AuteursExperts.svg" alt="Experts" class="icon" />
              </div>
              <h3>Experts Pédagogues</h3>
              <p>Contenu créé par des enseignants expérimentés et des experts en mathématiques</p>
            </div>
            <div class="benefit-card">
              <div class="benefit-icon">
                <img src="/icons/SuiviProgression.svg" alt="Suivi" class="icon" />
              </div>
              <h3>Suivi Détaillé</h3>
              <p>Tableau de bord personnalisé pour suivre les progrès en temps réel</p>
            </div>
            <div class="benefit-card">
              <div class="benefit-icon">
                <img src="/icons/ApprentissageFlexible.svg" alt="Flexibilité" class="icon" />
              </div>
              <h3>Apprentissage Flexible</h3>
              <p>Adapté au rythme et au niveau d'apprentissage de votre enfant</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Content Sections -->
      <div class="content-container">
        <div v-for="(section, i) in about" :key="i" class="about-section" :class="{ 'parents-section': section.title === 'Un mot pour les parents' }">
          <!-- Section Header -->
          <div class="section-header">
            <div class="section-icon">
              <img :src="getSectionIcon(section.emoji)" :alt="section.title" class="icon-emoji" />
            </div>
            <h2 class="section-title">{{ section.title }}</h2>
          </div>

          <!-- Section Content -->
          <div class="section-content">
            <!-- Text Content -->
            <div v-if="section.content" class="text-content">
              <p 
                v-for="(p, j) in section.content" 
                :key="j" 
                class="content-paragraph"
                :class="{ 'highlight-text': p.includes('@') || p.includes('www') || p.includes('WhatsApp') }"
                v-html="p"
              >
              </p>
            </div>

            <!-- List Content -->
            <div v-if="section.list" class="list-content">
              <ul class="feature-list">
                <li 
                  v-for="(item, k) in section.list" 
                  :key="k" 
                  class="feature-item"
                >
                  <div class="feature-bullet"></div>
                  <span class="feature-text">{{ item }}</span>
                </li>
              </ul>
            </div>

            <!-- Additional Content -->
            <div v-if="section.additionalContent" class="text-content">
              <p 
                v-for="(p, j) in section.additionalContent" 
                :key="'additional-' + j" 
                class="content-paragraph"
                v-html="p"
              >
              </p>
            </div>

            <!-- Social Media Icons -->
            <div v-if="section.socialMedia" class="social-media-section">
              <div class="social-media-row highlight-text">
                <span class="social-media-label">📱 Réseaux sociaux : @Opti.TAB</span>
                <div class="social-media-icons-inline">
                  <a href="https://instagram.com/optitabedu" target="_blank" class="social-icon-inline instagram-icon">
                    <svg class="social-icon-svg-inline" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.919-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z" fill="currentColor"/>
                    </svg>
                  </a>
                  <a href="https://facebook.com/optitabedu" target="_blank" class="social-icon-inline facebook-icon">
                    <svg class="social-icon-svg-inline" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" fill="currentColor"/>
                    </svg>
                  </a>
                  <a href="https://linkedin.com/company/optitabedu" target="_blank" class="social-icon-inline linkedin-icon">
                    <svg class="social-icon-svg-inline" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" fill="currentColor"/>
                    </svg>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>


      <!-- Call to Action -->
      <div class="cta-section">
        <div class="cta-card">
          <div class="cta-content">
            <h3 class="cta-title">Donnez à votre enfant les clés de la réussite</h3>
            <p class="cta-text">
              Des familles nous font déjà confiance pour soutenir l'apprentissage de leurs enfants, rejoignez-les !
            </p>
             <div class="cta-buttons">
               <button @click="openSignupModal" class="cta-button primary" data-cta-name="signup" data-cta-location="about_page">
                 Commencer maintenant
               </button>
              <button @click="openContactModal('Parler à un expert')" class="cta-button secondary">
                Parler à un expert
              </button>
            </div>
            <div class="cta-guarantee">
              <span class="guarantee-text">Sans engagement • Résultats garantis • Support 7/7</span>
            </div>
            <div class="cta-reviews">
              <GoogleReviewsCompact />
            </div>
          </div>
        </div>
      </div>
      </div>
    </div>

    <!-- Bouton WhatsApp flottant -->
    <WhatsappChatButton
      phone="33764040251"
      message="Bonjour, j'ai une question sur OptiTAB !"
      tooltip="Une question ? Discutons sur WhatsApp !"
    />
    <!-- Modal de contact -->
    <ContactModal 
      :isOpen="isContactModalOpen" 
      :initialSubject="contactModalSubject"
      @close="closeContactModal"
      @success="handleContactSuccess"
    />
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import WhatsappChatButton from '@/components/home/WhatsappChatButton.vue'
import GoogleReviewsCompact from '@/components/home/GoogleReviewsCompact.vue'
import ContactModal from '@/components/common/ContactModal.vue'
import about from '@/config/aboutContent.js'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { useZoom } from '@/composables/useZoom'

const { openModal } = useModalManager()

// --- Mobile zoom (same logic as Home) ---
const aboutContentRef = ref(null)

function computeAboutZoom(width) {
  if (width >= 1400) return 1
  if (width >= 1200) return 0.95
  if (width >= 1024) return 0.9
  if (width >= 900) return 0.85
  if (width >= 768) return 0.8
  if (width >= 640) return 0.72
  if (width >= 520) return 0.68
  if (width >= 420) return 0.64
  if (width >= 360) return 0.6
  return 0.55
}

const {
  contentHeight,
  zoomLevel,
  supportsNativeZoom,
  detectMobileAndZoomSupport,
  createZoomStyle,
  updateViewportWidth,
  measureContentHeight,
  setupViewportListener,
  cleanupViewportListener
} = useZoom({ computeAutoZoom: computeAboutZoom })

const baseAboutZoomStyle = createZoomStyle({
  cssVar: '--about-zoom',
  heightVar: '--about-content-height',
  mobileZoomAdjustment: (z) => z
})

// On mobile (transform: scale), keep height auto to avoid scroll blocking on some browsers,
// then compensate the extra space with a negative margin.
const aboutZoomStyle = computed(() => {
  const style = baseAboutZoomStyle.value
  if (supportsNativeZoom.value) return style

  const z = Number(zoomLevel.value || 1)
  if (!contentHeight.value || !Number.isFinite(z) || z >= 1) {
    return { ...style, height: 'auto', minHeight: 'auto', marginBottom: '' }
  }

  const marginBottom = -Math.round(contentHeight.value * (1 - z))
  return { ...style, height: 'auto', minHeight: 'auto', marginBottom: `${marginBottom}px` }
})

let aboutResizeObserver = null
const measureAboutHeight = () => {
  measureContentHeight(aboutContentRef)
}

const handleViewportChange = async () => {
  updateViewportWidth()
  await nextTick()
  measureAboutHeight()
}

const handleResize = () => {
  void handleViewportChange()
}

const handleOrientationChange = () => {
  setTimeout(() => {
    void handleViewportChange()
  }, 200)
}

onMounted(async () => {
  detectMobileAndZoomSupport()
  setupViewportListener()

  await nextTick()
  measureAboutHeight()

  if (typeof window !== 'undefined') {
    window.addEventListener('resize', handleResize, { passive: true })
    window.addEventListener('orientationchange', handleOrientationChange, { passive: true })

    setTimeout(measureAboutHeight, 250)

    if (window.ResizeObserver && aboutContentRef.value) {
      aboutResizeObserver = new ResizeObserver(() => {
        measureAboutHeight()
      })
      aboutResizeObserver.observe(aboutContentRef.value)
    }
  }
})

onUnmounted(() => {
  cleanupViewportListener()
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', handleResize)
    window.removeEventListener('orientationchange', handleOrientationChange)
  }
  aboutResizeObserver?.disconnect?.()
  aboutResizeObserver = null
})

// Gestion du modal de contact
const isContactModalOpen = ref(false)
const contactModalSubject = ref('')

const openContactModal = (subject = '') => {
  contactModalSubject.value = subject
  isContactModalOpen.value = true
}

const closeContactModal = () => {
  isContactModalOpen.value = false
  contactModalSubject.value = ''
}

const handleContactSuccess = (message) => {
  alert(message)
}

// Fonction pour ouvrir le modal de création de compte
const openSignupModal = () => {
  openModal(MODAL_IDS.REGISTER)
}

// Fonction pour mapper les emojis vers les icônes SVG
const getSectionIcon = (emoji) => {
  const iconMap = {
    '🚀': '/icons/ResultatsGarantis.svg',
    '📚': '/icons/proposeoptitab.svg',
    '🎯': '/icons/notremission.svg',
    '💡': '/icons/uniqueOpitab.svg',
    '👤': '/icons/quisommenous.svg',
    '👥': '/icons/AuteursExperts.svg',
    '📈': '/icons/visionavenir.svg',
    '📊': '/icons/SuiviProgression.svg',
    '🔄': '/icons/ApprentissageFlexible.svg',
    '🎓': '/icons/ResultatsGarantis.svg',
    '📬': '/icons/contactEchanges.svg',
    '👪': '/icons/motParent.svg',
    '📧': '/icons/mail.svg',
    '✅': '/icons/ApprentissageFlexible.svg'
  }
  return iconMap[emoji] || '/icons/ResultatsGarantis.svg'
}
</script>

<style scoped>
:root {
  --primary: #2a38b7;
  --primary-light: #667eea;
  --dark: #0f172a;
  --gray-dark: #475569;
  --gray: #64748b;
  --gray-light: #cbd5e1;
  --gray-lighter: #f1f5f9;
  --white: #ffffff;
}

/* Page Container */
.about-zoom {
  width: 100%;
  overflow-x: hidden;
  overflow-y: visible;
}

.about-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 50%, #f1f5f9 100%);
}

/* Hero Section Pédagogique */
.hero-section {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
  padding: 4rem 2rem;
  padding-top: calc(4rem + 60px); /* 60px pour compenser le header fixe */
  margin-top: 0;
}

.hero-content {
  width: 100%;
}


.hero-title {
  font-size: 2.5rem;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.3;
  margin-bottom: 1.5rem;
}

.gradient-text {
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 3rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  text-align: justify;
}

/* Hero Stats */
.hero-stats {
  display: flex;
  gap: 3rem;
  justify-content: center;
  margin-top: 2rem;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 2.2rem;
  font-weight: 700;
  color: #2a38b7;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.95rem;
  color: #6b7280;
  font-weight: 500;
}


/* Why Section */
.why-section {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 50%, #f0f4ff 100%);
  padding: 3rem 0;
  margin: 1.5rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section-intro {
  text-align: center;
  margin-bottom: 2rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2a38b7;
  margin-bottom: 1rem;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #6b7280;
  max-width: 600px;
  margin: 0 auto;
  text-align: justify;
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
  max-width: 700px;
  margin: 0 auto;
}

.benefit-card {
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.benefit-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: #d1d5db;
}

.benefit-icon {
  width: 80px;
  height: 80px;
  background: transparent;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
}

.benefit-icon .icon {
  width: 4rem;
  height: 4rem;
  filter: none;
  color: #2563eb;
}

.benefit-card h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.75rem;
}

.benefit-card p {
  color: #6b7280;
  line-height: 1.5;
  text-align: left;
  font-size: 0.9rem;
}

/* Content Container */
.content-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2rem 0 2rem;
}

/* Section Styles */
.about-section {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 2px solid rgba(42, 56, 183, 0.1);
}


.section-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.section-icon {
  width: 120px;
  height: 120px;
  background: transparent;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-emoji {
  width: 5.4rem;
  height: 5.4rem;
  filter: none;
  color: #2a38b7;
}

/* Style spécifique pour la section "Un mot pour les parents" - icône plus grande */
.parents-section .icon-emoji {
  width: 8rem;
  height: 8rem;
}

.section-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #2a38b7;
  margin: 0;
}

.section-content {
  color: #374151;
}

.content-paragraph {
  font-size: 1.1rem;
  font-weight: 500;
  color: #374151;
  line-height: 1.7;
  margin-bottom: 1rem;
  text-align: justify;
}

.highlight-text {
  background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border-left: 4px solid #2a38b7;
  font-weight: 500;
}

.contact-link {
  color: #2a38b7;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.contact-link:hover {
  color: #667eea;
  text-decoration: underline;
}

/* Feature List */
.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding: 1rem 1.25rem;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
}

.feature-bullet {
  width: 8px;
  height: 8px;
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  border-radius: 50%;
  margin-top: 0.5rem;
  flex-shrink: 0;
}

.feature-text {
  font-size: 1rem;
  font-weight: 500;
  color: #374151;
  line-height: 1.5;
  text-align: justify;
}

/* Social Media Section */
.social-media-section {
  margin-top: 1.5rem;
}

.social-media-row {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  flex-wrap: wrap;
  gap: 1rem;
}

.social-media-label {
  font-size: 1.05rem;
  color: #374151;
  font-weight: 500;
  margin: 0;
}

.social-media-icons-inline {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-left: 0.5rem;
}

.social-media-icons {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.social-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  background: #fff;
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  transition: all 0.3s ease;
  text-decoration: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.social-icon:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.social-icon:nth-child(1):hover {
  border-color: #E4405F;
  background: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 100%);
}

.social-icon:nth-child(2):hover {
  border-color: #1877F2;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
}

.social-icon:nth-child(3):hover {
  border-color: #0A66C2;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
}

.social-icon-svg {
  width: 32px;
  height: 32px;
}

/* Couleurs spécifiques pour chaque réseau social */
.instagram-icon .social-icon-svg {
  color: #E4405F;
}

.facebook-icon .social-icon-svg {
  color: #1877F2;
}

.linkedin-icon .social-icon-svg {
  color: #0A66C2;
}

/* Effets de survol avec couleurs */
.instagram-icon:hover .social-icon-svg {
  color: #C13584;
}

.facebook-icon:hover .social-icon-svg {
  color: #166FE5;
}

.linkedin-icon:hover .social-icon-svg {
  color: #004182;
}

/* Icônes en ligne */
.social-icon-inline {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: transparent;
  border-radius: 6px;
  border: none;
  transition: all 0.3s ease;
  text-decoration: none;
  box-shadow: none;
}

.social-icon-inline:hover {
  transform: none;
  box-shadow: none;
}

.instagram-icon:hover {
  border: none;
  background: transparent;
}

.facebook-icon:hover {
  border: none;
  background: transparent;
}

.linkedin-icon:hover {
  border: none;
  background: transparent;
}

.social-icon-svg-inline {
  width: 20px;
  height: 20px;
}

/* Couleurs spécifiques pour les icônes en ligne */
.instagram-icon .social-icon-svg-inline {
  color: #E4405F;
}

.facebook-icon .social-icon-svg-inline {
  color: #1877F2;
}

.linkedin-icon .social-icon-svg-inline {
  color: #0A66C2;
}

/* Effets de survol avec couleurs pour les icônes en ligne */
.instagram-icon:hover .social-icon-svg-inline {
  color: #C13584;
}

.facebook-icon:hover .social-icon-svg-inline {
  color: #166FE5;
}

.linkedin-icon:hover .social-icon-svg-inline {
  color: #004182;
}


/* CTA Section */
.cta-section {
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 50%, #f1f5f9 100%);
  padding: 5rem 2rem;
  margin-top: 0;
  position: relative;
}

.cta-card {
  max-width: 900px;
  margin: 0 auto;
  text-align: center;
  background: #ffffff;
  border-radius: 24px;
  padding: 3.5rem 3rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08), 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(37, 99, 235, 0.08);
}

.cta-title {
  font-size: 2.75rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 1.25rem;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.cta-text {
  font-size: 1.15rem;
  color: #64748b;
  line-height: 1.7;
  margin-bottom: 2.75rem;
  text-align: center;
  max-width: 650px;
  margin-left: auto;
  margin-right: auto;
  font-weight: 400;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 2.5rem;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1.1rem 2.5rem;
  border-radius: 14px;
  font-size: 1.05rem;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid transparent;
  cursor: pointer;
  min-width: 200px;
  letter-spacing: 0.01em;
}

.cta-button.primary {
  background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
  color: #fff;
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.35), 0 2px 4px rgba(37, 99, 235, 0.2);
}

.cta-button.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.45), 0 4px 8px rgba(37, 99, 235, 0.25);
  background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
}

.cta-button.primary:active {
  transform: translateY(0);
}

.cta-button.secondary {
  background: #ffffff;
  color: #2563eb;
  border-color: #2563eb;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.cta-button.secondary:hover {
  background: linear-gradient(135deg, #eff6ff 0%, #f0f4ff 100%);
  border-color: #2563eb;
  color: #1d4ed8;
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.2), 0 2px 4px rgba(0, 0, 0, 0.08);
}

.cta-button.secondary:active {
  transform: translateY(0);
}

.button-icon {
  width: 1.2rem;
  height: 1.2rem;
  filter: none;
}

.cta-guarantee {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(226, 232, 240, 0.8);
}

.guarantee-text {
  color: #64748b;
  font-size: 0.9rem;
  font-weight: 500;
  letter-spacing: 0.01em;
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  justify-content: center;
  position: relative;
  padding-left: 1.5rem;
}

.guarantee-text::before {
  content: '✓';
  color: #10b981;
  font-weight: 700;
  font-size: 1rem;
  position: absolute;
  left: 0;
}

.cta-reviews {
  margin-top: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top: 1.5rem;
}

.guarantee-icon {
  width: 1.1rem;
  height: 1.1rem;
  filter: none;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .hero-section {
    padding: 3rem 1.5rem;
    padding-top: calc(3rem + 60px); /* 60px pour compenser le header fixe */
  }
  
  .hero-title {
    font-size: 2.2rem;
  }
  
  .hero-stats {
    gap: 2rem;
  }
  
  .benefits-grid {
    grid-template-columns: repeat(2, 1fr);
    max-width: 600px;
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 2rem 1.25rem;
    padding-top: calc(2rem + 60px); /* 60px pour compenser le header fixe */
    margin-top: 0;
  }
  
  .hero-title {
    font-size: 1.75rem;
    line-height: 1.3;
    margin-bottom: 1rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 2rem;
    padding: 0 0.5rem;
  }
  
  .hero-stats {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 1.5rem;
    justify-content: center;
    margin-top: 1.5rem;
  }
  
  .stat-item {
    flex: 0 1 calc(33.333% - 1rem);
    min-width: 80px;
  }
  
  .stat-number {
    font-size: 1.8rem;
    margin-bottom: 0.25rem;
  }
  
  .stat-label {
    font-size: 0.85rem;
    line-height: 1.3;
  }
  
  .why-section {
    padding: 2.5rem 0;
    margin: 1.5rem 0;
  }
  
  .container {
    padding: 0 1.25rem;
  }
  
  .section-intro {
    margin-bottom: 2rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .section-subtitle {
    font-size: 1.05rem;
    padding: 0 0.5rem;
  }
  
  .benefits-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
    max-width: 100%;
  }
  
  .benefit-card {
    padding: 0.75rem;
    border-radius: 8px;
  }
  
  .benefit-icon {
    width: 50px;
    height: 50px;
    margin-bottom: 0.5rem;
  }
  
  .benefit-icon .icon {
    width: 2.5rem;
    height: 2.5rem;
  }
  
  .benefit-card h3 {
    font-size: 0.9rem;
    margin-bottom: 0.4rem;
  }
  
  .benefit-card p {
    font-size: 0.75rem;
    line-height: 1.4;
  }
  
  .content-container {
    padding: 0 1.25rem;
  }
  
  .about-section {
    padding: 1.5rem;
    margin-bottom: 1.25rem;
    border-radius: 12px;
  }
  
  .section-header {
    flex-direction: row;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  
  .section-icon {
    width: 70px;
    height: 70px;
    flex-shrink: 0;
  }
  
  .icon-emoji {
    width: 3.5rem;
    height: 3.5rem;
  }
  
  .parents-section .icon-emoji {
    width: 5rem;
    height: 5rem;
  }
  
  .section-title {
    font-size: 1.4rem;
    line-height: 1.3;
    margin: 0;
  }
  
  .content-paragraph {
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 0.875rem;
  }
  
  .feature-item {
    padding: 0.875rem 1rem;
    margin-bottom: 0.75rem;
  }
  
  .feature-text {
    font-size: 0.95rem;
    line-height: 1.5;
  }
  
  .social-media-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .social-media-label {
    font-size: 0.95rem;
  }
  
  .social-media-icons-inline {
    margin-left: 0;
  }
  
  .cta-section {
    padding: 3rem 1.25rem;
  }
  
  .cta-card {
    padding: 2.5rem 1.75rem;
    border-radius: 20px;
  }
  
  .cta-title {
    font-size: 2rem;
    line-height: 1.25;
    margin-bottom: 1rem;
    letter-spacing: -0.01em;
  }
  
  .cta-text {
    font-size: 1rem;
    line-height: 1.65;
    margin-bottom: 2.25rem;
    padding: 0;
  }
  
  .cta-buttons {
    flex-direction: column;
    align-items: stretch;
    gap: 0.875rem;
    margin-bottom: 2rem;
  }
  
  .cta-button {
    width: 100%;
    max-width: 100%;
    padding: 1rem 1.75rem;
    font-size: 1rem;
    justify-content: center;
    min-width: auto;
  }
  
  .cta-guarantee {
    padding-top: 1.75rem;
    margin-bottom: 1.75rem;
  }
  
  .guarantee-text {
    font-size: 0.85rem;
    gap: 0.5rem;
  }
  
  .cta-reviews {
    padding-top: 1.25rem;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 1.5rem 1rem;
    padding-top: calc(1.5rem + 60px); /* 60px pour compenser le header fixe */
    margin-top: 0;
  }
  
  .hero-title {
    font-size: 1.5rem;
    line-height: 1.3;
    margin-bottom: 0.875rem;
  }
  
  .hero-subtitle {
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
    padding: 0;
  }
  
  .hero-stats {
    flex-direction: row;
    gap: 1rem;
    margin-top: 1.25rem;
  }
  
  .stat-item {
    flex: 1;
    min-width: 70px;
  }
  
  .stat-number {
    font-size: 1.5rem;
    margin-bottom: 0.25rem;
  }
  
  .stat-label {
    font-size: 0.8rem;
  }
  
  .why-section {
    padding: 2rem 0;
    margin: 1rem 0;
  }
  
  .container {
    padding: 0 1rem;
  }
  
  .section-intro {
    margin-bottom: 1.5rem;
  }
  
  .section-title {
    font-size: 1.75rem;
  }
  
  .section-subtitle {
    font-size: 1rem;
    padding: 0;
  }
  
  .benefits-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
  }
  
  .benefit-card {
    padding: 0.65rem;
    border-radius: 8px;
  }
  
  .benefit-icon {
    width: 45px;
    height: 45px;
    margin-bottom: 0.4rem;
  }
  
  .benefit-icon .icon {
    width: 2.25rem;
    height: 2.25rem;
  }
  
  .benefit-card h3 {
    font-size: 0.85rem;
    margin-bottom: 0.35rem;
  }
  
  .benefit-card p {
    font-size: 0.7rem;
    line-height: 1.35;
  }
  
  .content-container {
    padding: 0 1rem;
  }
  
  .about-section {
    padding: 1.25rem;
    margin-bottom: 1rem;
    border-radius: 10px;
  }
  
  .section-header {
    gap: 0.75rem;
    margin-bottom: 1.25rem;
  }
  
  .section-icon {
    width: 60px;
    height: 60px;
  }
  
  .icon-emoji {
    width: 3rem;
    height: 3rem;
  }
  
  .parents-section .icon-emoji {
    width: 4rem;
    height: 4rem;
  }
  
  .section-title {
    font-size: 1.25rem;
  }
  
  .content-paragraph {
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 0.75rem;
  }
  
  .feature-item {
    padding: 0.75rem;
    margin-bottom: 0.625rem;
  }
  
  .feature-text {
    font-size: 0.9rem;
  }
  
  .cta-section {
    padding: 2.5rem 1rem;
  }
  
  .cta-card {
    padding: 2rem 1.5rem;
    border-radius: 18px;
  }
  
  .cta-title {
    font-size: 1.75rem;
    line-height: 1.25;
    margin-bottom: 0.875rem;
    letter-spacing: -0.01em;
  }
  
  .cta-text {
    font-size: 0.95rem;
    line-height: 1.65;
    margin-bottom: 2rem;
    padding: 0;
  }
  
  .cta-buttons {
    margin-bottom: 1.75rem;
  }
  
  .cta-button {
    padding: 0.95rem 1.5rem;
    font-size: 0.95rem;
  }
  
  .cta-guarantee {
    padding-top: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  .guarantee-text {
    font-size: 0.8rem;
  }
  
  .cta-reviews {
    padding-top: 1rem;
  }
}
</style> 
