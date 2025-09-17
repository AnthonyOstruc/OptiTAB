<template>
  <MainLayout>
    <div class="cgv-page">
      <!-- Header Section -->
      <div class="cgv-header">
        <div class="container">
          <div class="header-content">
            <h1 class="cgv-title">
              Contact
            </h1>
            <p class="cgv-subtitle">
              <span class="gradient-text">OptiTAB</span> - Plateforme d'apprentissage
            </p>
            <div class="cgv-meta">
              <span class="meta-text">Une question ? N'hésitez pas à nous contacter !</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Table of Contents -->
      <div class="toc-section">
        <div class="container">
          <h2 class="toc-title">Sommaire</h2>
          <div class="toc-list">
            <a 
              v-for="(section, index) in sections" 
              :key="index"
              :href="`#${section.id}`" 
              :class="['toc-link', { 'active': activeSection === section.id }]"
              @click="scrollToSection(section.id, $event)"
            >
              <span class="toc-number">{{ index + 1 }}</span>
              <span class="toc-text">{{ section.title }}</span>
              <span class="toc-arrow">→</span>
            </a>
          </div>
        </div>
      </div>

      <!-- Content Sections -->
      <div class="cgv-content">
        <div class="container">
          <div class="content-wrapper">
            <!-- Section 1: Informations de contact -->
            <section id="informations" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">1</span>
                Informations de contact
              </h2>
              <div class="section-content">
                <div class="contact-info">
                  <div class="contact-item">
                    <strong>
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="#25D366" style="display: inline-block; margin-right: 0.5rem; vertical-align: middle;">
                        <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.821 11.821 0 0020.885 3.488"/>
                      </svg>
                      WhatsApp :
                    </strong> <a href="https://wa.me/33764040251" target="_blank" class="link">07 64 04 02 51</a>
                  </div>
                  <div class="contact-item">
                    <strong>✉️ Email :</strong> <a href="mailto:contact@optitab.net" class="link">contact@optitab.net</a>
                  </div>
                  <div class="contact-item">
                    <strong>🌐 Site web :</strong> <a href="https://www.optitab.net" target="_blank" class="link">www.optitab.net</a>
                  </div>
                </div>
              </div>
            </section>

            <!-- Section 2: Formulaire de contact -->
            <section id="formulaire" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">2</span>
                Formulaire de contact
              </h2>
              <div class="section-content">
                <form @submit.prevent="handleSubmit" class="contact-form">
                  <div class="form-row">
                    <div class="form-group">
                      <label for="firstName" class="form-label">Prénom *</label>
                      <input 
                        type="text" 
                        id="firstName" 
                        v-model="form.firstName"
                        class="form-input"
                        placeholder="Votre prénom"
                        required
                      />
                    </div>
                    <div class="form-group">
                      <label for="lastName" class="form-label">Nom *</label>
                      <input 
                        type="text" 
                        id="lastName" 
                        v-model="form.lastName"
                        class="form-input"
                        placeholder="Votre nom"
                        required
                      />
                    </div>
                  </div>

                  <div class="form-group">
                    <label for="email" class="form-label">Email *</label>
                    <input 
                      type="email" 
                      id="email" 
                      v-model="form.email"
                      class="form-input"
                      placeholder="votre@email.com"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label for="subject" class="form-label">Sujet *</label>
                    <select 
                      id="subject" 
                      v-model="form.subject"
                      class="form-select"
                      required
                    >
                      <option value="">Je vous contacte à propos de...</option>
                      <option value="Demande d'information">Demande d'information</option>
                      <option value="Support technique">Support technique</option>
                      <option value="Partenariat">Partenariat</option>
                      <option value="Autre">Autre</option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label for="message" class="form-label">Message *</label>
                    <textarea 
                      id="message" 
                      v-model="form.message"
                      class="form-textarea"
                      placeholder="Votre message..."
                      rows="4"
                      required
                    ></textarea>
                  </div>

                  <button type="submit" class="submit-button" :disabled="isSubmitting">
                    <span v-if="!isSubmitting">Envoyer message</span>
                    <span v-else>Envoi en cours...</span>
                  </button>
                </form>
              </div>
            </section>

            <!-- Section 3: Réseaux sociaux -->
            <section id="reseaux" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">3</span>
                Réseaux sociaux
              </h2>
              <div class="section-content">
                <p>Suivez-nous sur nos réseaux sociaux pour rester informé de nos actualités :</p>
                <div class="social-media-section">
                  <div class="social-media-row">
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
            </section>

            <!-- Section 4: Support -->
            <section id="support" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">4</span>
                Support et assistance
              </h2>
              <div class="section-content">
                <p>Notre équipe est disponible pour vous accompagner :</p>
                <ul class="content-list">
                  <li><strong>Support technique :</strong> assistance pour l'utilisation de la plateforme</li>
                  <li><strong>Support pédagogique :</strong> conseils et accompagnement dans l'apprentissage</li>
                  <li><strong>Support commercial :</strong> informations sur nos offres et tarifs</li>
                  <li><strong>Délai de réponse :</strong> sous 24h en moyenne</li>
                </ul>
                <div class="highlight-text">
                  <p><strong>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="#25D366" style="display: inline-block; margin-right: 0.5rem; vertical-align: middle;">
                      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.821 11.821 0 0020.885 3.488"/>
                    </svg>
                    WhatsApp :
                  </strong> <a href="https://wa.me/33764040251" target="_blank" class="link">07 64 04 02 51</a> - Réponse immédiate</p>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>

      <!-- Footer Note -->
      <div class="cgv-footer">
        <div class="container">
          <div class="footer-note">
            <p><strong>Note importante :</strong> Nous nous engageons à répondre à toutes vos questions dans les plus brefs délais. N'hésitez pas à nous contacter pour toute information complémentaire.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Bouton retour en haut -->
    <button 
      v-show="showBackToTop" 
      @click="scrollToTop"
      class="back-to-top"
      title="Retour en haut"
    >
      ↑
    </button>
    
    <!-- Bouton WhatsApp flottant -->
    <WhatsappChatButton
      phone="33764040251"
      message="Bonjour, j'ai une question sur OptiTAB !"
      tooltip="Une question ? Discutons sur WhatsApp !"
    />
  </MainLayout>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import WhatsappChatButton from '@/components/home/WhatsappChatButton.vue'

const isSubmitting = ref(false)
const showBackToTop = ref(false)
const activeSection = ref('')

const form = ref({
  firstName: '',
  lastName: '',
  email: '',
  subject: '',
  message: ''
})

const sections = ref([
  { id: 'informations', title: 'Informations de contact' },
  { id: 'formulaire', title: 'Formulaire de contact' },
  { id: 'reseaux', title: 'Réseaux sociaux' },
  { id: 'support', title: 'Support et assistance' }
])

// Fonction pour retourner en haut
const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

// Fonction pour gérer l'affichage du bouton retour en haut
const handleScroll = () => {
  showBackToTop.value = window.scrollY > 300
  
  // Détecter la section active
  const sections = document.querySelectorAll('.cgv-section')
  let current = ''
  
  sections.forEach(section => {
    const rect = section.getBoundingClientRect()
    if (rect.top <= 100 && rect.bottom >= 100) {
      current = section.id
    }
  })
  
  if (current) {
    activeSection.value = current
  }
}

// Fonction pour scroll vers une section
const scrollToSection = (sectionId, event) => {
  event.preventDefault()
  const element = document.getElementById(sectionId)
  if (element) {
    const offset = 80 // Hauteur du header
    const elementPosition = element.offsetTop - offset
    window.scrollTo({
      top: elementPosition,
      behavior: 'smooth'
    })
  }
}

const handleSubmit = () => {
  isSubmitting.value = true
  
  // Construire le corps du message
  const body = `Bonjour,\n\nJe m'appelle ${form.value.firstName} ${form.value.lastName}.\n\n${form.value.message}\n\nCordialement,\n${form.value.firstName} ${form.value.lastName}`
  
  // Créer le lien mailto
  const mailtoUrl = `mailto:contact@optitab.net?subject=${encodeURIComponent(form.value.subject)}&body=${encodeURIComponent(body)}`
  
  // Ouvrir le client email
  window.open(mailtoUrl)
  
  // Réinitialiser le formulaire après un délai
  setTimeout(() => {
    form.value = {
      firstName: '',
      lastName: '',
      email: '',
      subject: '',
      message: ''
    }
    isSubmitting.value = false
  }, 1000)
}

// Lifecycle hooks
onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  // Définir la première section comme active au chargement
  activeSection.value = 'informations'
  
  // Vérifier si on doit scroll vers une section spécifique
  const hash = window.location.hash
  if (hash === '#informations') {
    // Attendre que le DOM soit rendu puis scroll vers les informations de contact
    setTimeout(() => {
      const element = document.getElementById('informations')
      if (element) {
        const offset = 80 // Hauteur du header
        const elementPosition = element.offsetTop - offset
        window.scrollTo({
          top: elementPosition,
          behavior: 'smooth'
        })
        activeSection.value = 'informations'
      }
    }, 100)
  } else if (hash === '#formulaire') {
    // Attendre que le DOM soit rendu puis scroll vers le formulaire
    setTimeout(() => {
      const element = document.getElementById('formulaire')
      if (element) {
        const offset = 80 // Hauteur du header
        const elementPosition = element.offsetTop - offset
        window.scrollTo({
          top: elementPosition,
          behavior: 'smooth'
        })
        activeSection.value = 'formulaire'
      }
    }, 100)
  }
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
/* Page Container */
.cgv-page {
  min-height: 100vh;
  background: #ffffff;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* Header Section - Style propre */
.cgv-header {
  background: #f8fafc;
  border-bottom: 1px solid #e5e7eb;
  padding: 4rem 0;
  margin-top: 40px;
  margin-bottom: 0;
}

.header-content {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.cgv-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #111827;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  letter-spacing: -0.03em;
}

.gradient-text {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.cgv-subtitle {
  font-size: 1.2rem;
  color: #6b7280;
  line-height: 1.4;
  margin-bottom: 2.5rem;
  font-weight: 500;
}

.cgv-meta {
  margin-top: 1.5rem;
}

.meta-text {
  font-size: 0.95rem;
  color: #6b7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Table of Contents - Style propre */
.toc-section {
  background: white;
  padding: 3rem 0;
  margin: 0;
}

.toc-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #111827;
  text-align: center;
  margin-bottom: 2rem;
  letter-spacing: -0.01em;
}

.toc-list {
  max-width: 800px;
  margin: 0 auto;
  background: transparent;
  border-radius: 0;
  padding: 0;
  border: none;
  box-shadow: none;
}

.toc-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 0.5rem 0;
  text-decoration: none;
  color: #374151;
  font-weight: 400;
  transition: all 0.15s ease;
  border-bottom: 1px solid #f3f4f6;
  position: relative;
  border-radius: 0;
  margin-bottom: 0;
}

.toc-link:last-child {
  border-bottom: none;
}

.toc-link:hover {
  background: transparent;
  color: #6366f1;
}

.toc-link:hover .toc-arrow {
  transform: translateX(4px);
  opacity: 1;
}

.toc-link.active {
  background: white;
  color: #374151;
}

.toc-link.active .toc-number {
  background: #6366f1;
  color: white;
}

.toc-number {
  background: #6366f1;
  color: white;
  width: 20px;
  height: 20px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.75rem;
  flex-shrink: 0;
}

.toc-text {
  font-size: 0.95rem;
  flex: 1;
  line-height: 1.5;
  font-weight: 500;
}

.toc-arrow {
  color: #9ca3af;
  font-size: 0.8rem;
  opacity: 0;
  transform: translateX(0);
  transition: all 0.15s ease;
}

.toc-link.active .toc-arrow {
  opacity: 0;
  color: #9ca3af;
}

/* Content - Style propre */
.cgv-content {
  background: white;
  padding: 4rem 0;
}

.content-wrapper {
  max-width: 800px;
  margin: 0 auto;
}

.cgv-section {
  margin-bottom: 2.5rem;
  padding: 0;
  background: transparent;
  border: none;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.4rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 3px solid #6366f1;
  letter-spacing: -0.01em;
}

.section-number {
  background: #6366f1;
  color: white;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.section-content {
  margin-left: 0;
  padding: 0 0.5rem;
}

.subsection-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #374151;
  margin: 1.5rem 0 0.75rem 0;
  padding-left: 1rem;
  border-left: 4px solid #6366f1;
  letter-spacing: -0.005em;
}

.content-list {
  list-style: none;
  padding: 0;
  margin: 1rem 0;
}

.content-list li {
  position: relative;
  padding-left: 1.5rem;
  margin-bottom: 0.75rem;
  color: #4b5563;
  line-height: 1.7;
  font-size: 1rem;
  font-weight: 400;
}

.content-list li::before {
  content: "•";
  color: #6366f1;
  font-weight: bold;
  position: absolute;
  left: 0;
  top: 0;
}

.contact-info {
  background: transparent;
  padding: 0;
  border: none;
  margin-top: 0.5rem;
}

.contact-item {
  margin-bottom: 0.5rem;
  color: #4b5563;
  font-size: 0.95rem;
}

.contact-item:last-child {
  margin-bottom: 0;
}

/* Contact Form */
.contact-form {
  background: #f8fafc;
  padding: 2rem;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  margin-top: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.form-input,
.form-select,
.form-textarea {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: white;
  font-family: inherit;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 120px;
}

.submit-button {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

/* Social Media */
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

/* Highlight Text */
.highlight-text {
  background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%);
  padding: 1.5rem;
  border-radius: 12px;
  border-left: 4px solid #6366f1;
  margin: 1.5rem 0;
}

.highlight-text p {
  margin: 0;
  font-weight: 500;
  color: #1f2937;
}

/* Links */
.link {
  color: #6366f1;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.link:hover {
  color: #4f46e5;
  text-decoration: underline;
}

/* Footer - Style propre */
.cgv-footer {
  background: white;
  border: none;
  padding: 3rem 0;
  margin-top: 0;
}

.footer-note {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  color: #6b7280;
  max-width: 800px;
  margin: 0 auto;
  font-size: 0.95rem;
  line-height: 1.6;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.footer-note strong {
  color: #374151;
  font-weight: 600;
}

/* Responsive */
@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }

  .cgv-title {
    font-size: 1.875rem;
  }

  .toc-list {
    margin: 0;
  }

  .section-title {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .section-content {
    padding: 0;
  }

  .cgv-header {
    padding: 2rem 0;
  }

  .cgv-content {
    padding: 1rem 0;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .social-media-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .social-media-icons-inline {
    margin-left: 0;
  }
}

/* Bouton retour en haut */
.back-to-top {
  position: fixed;
  bottom: 100px;
  right: 24px;
  width: 48px;
  height: 48px;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 50%;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.back-to-top:hover {
  background: #4f46e5;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
}

.back-to-top:active {
  transform: translateY(0);
}

@media (max-width: 768px) {
  .back-to-top {
    bottom: 80px;
    right: 16px;
    width: 44px;
    height: 44px;
    font-size: 1.1rem;
  }
}
</style>