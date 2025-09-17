<template>
  <MainLayout>
    <div class="cgv-page">
      <!-- Header Section -->
      <div class="cgv-header">
        <div class="container">
          <div class="header-content">
            <h1 class="cgv-title">
              Mentions Légales
            </h1>
            <p class="cgv-subtitle">
              <span class="gradient-text">OptiTAB</span> - Plateforme d'apprentissage
            </p>
            <div class="cgv-meta">
              <span class="meta-text">Dernière mise à jour : 16 septembre 2025 • Site web : www.optitab.net</span>
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
            <!-- Section 1: Éditeur -->
            <section id="editeur" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">1</span>
                Éditeur du site
              </h2>
              <div class="section-content">
                <p><strong>Éditeur du site :</strong> OptiTAB</p>
                
                <h3 class="subsection-title">Responsable éditorial :</h3>
                <div class="contact-info">
                  <div class="contact-item">
                    <strong>Nom :</strong> Anthony Tabet
                    <a href="https://www.linkedin.com/in/anthony-tabet-a34aa6192/" target="_blank" class="linkedin-link" title="Profil LinkedIn">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                      </svg>
                    </a>
                  </div>
                  <div class="contact-item">
                    <strong>Email :</strong> <a href="mailto:anthony@optitab.net" class="link">anthony@optitab.net</a>
                  </div>
                </div>
                
                <h3 class="subsection-title">Responsable du traitement des données :</h3>
                <div class="contact-info">
                  <div class="contact-item">
                    <strong>Nom :</strong> OptiTAB
                  </div>
                  <div class="contact-item">
                    <strong>Email :</strong> <a href="mailto:support@optitab.net" class="link">support@optitab.net</a>
                  </div>
                </div>
              </div>
            </section>

            <!-- Section 2: Directeur de publication -->
            <section id="directeur" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">2</span>
                Directeur de publication
              </h2>
              <div class="section-content">
                <p>Le directeur de la publication est :</p>
                <div class="contact-info">
                  <div class="contact-item">
                    <strong>Nom :</strong> TABET Anthony
                  </div>
                  <div class="contact-item">
                    <strong>Fonction :</strong> Fondateur / Responsable éditorial
                  </div>
                </div>
              </div>
            </section>

            <!-- Section 3: Hébergement -->
            <section id="hebergement" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">3</span>
                Hébergement
              </h2>
              <div class="section-content">
                <p>Le site est hébergé par :</p>
                <div class="contact-info">
                  <div class="contact-item">
                    <strong>Nom de l'hébergeur :</strong> Render
                  </div>
                  <div class="contact-item">
                    <strong>Adresse :</strong> 995 Market St, San Francisco, CA 94103, USA
                  </div>
                  <div class="contact-item">
                    <strong>Site web :</strong> <a href="https://render.com" class="link" target="_blank">https://render.com</a>
                  </div>
                </div>
              </div>
            </section>

            <!-- Section 4: Propriété intellectuelle -->
            <section id="propriete" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">4</span>
                Propriété intellectuelle
              </h2>
              <div class="section-content">
                <p>L'ensemble de ce site relève de la législation française et internationale sur le droit d'auteur et la propriété intellectuelle. Tous les droits de reproduction sont réservés, y compris pour les documents téléchargeables et les représentations iconographiques et photographiques.</p>
                <p>La reproduction de tout ou partie de ce site sur un support électronique quel qu'il soit est formellement interdite sauf autorisation expresse du directeur de la publication.</p>
                <p>Le logo et le nom OptiTAB sont la propriété d'OptiTAB. Toute reproduction ou utilisation non autorisée est interdite.</p>
              </div>
            </section>

            <!-- Section 5: Responsabilité -->
            <section id="responsabilite" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">5</span>
                Responsabilité
              </h2>
              <div class="section-content">
                <p>Les informations contenues sur ce site sont aussi précises que possible et le site remis à jour à différentes périodes de l'année, mais peut toutefois contenir des inexactitudes ou des omissions.</p>
                <p>Si vous constatez une lacune, erreur ou ce qui parait être un dysfonctionnement, merci de bien vouloir le signaler par email, à l'adresse contact@optitab.net, en décrivant le problème de la manière la plus précise possible.</p>
                <p>Tout contenu téléchargé se fait aux risques et périls de l'utilisateur et sous sa seule responsabilité. En conséquence, ne saurait être tenu responsable d'un quelconque dommage subi par l'ordinateur de l'utilisateur ou d'une quelconque perte de données consécutives au téléchargement.</p>
              </div>
            </section>

            <!-- Section 6: Liens hypertextes -->
            <section id="liens" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">6</span>
                Liens hypertextes
              </h2>
              <div class="section-content">
                <p>Des liens hypertextes peuvent être présents sur le site. L'utilisateur est informé qu'en cliquant sur ces liens, il sortira du site optitab.net. Ce dernier n'a pas de contrôle sur les pages web sur lesquelles aboutissent ces liens et ne saurait en aucun cas être responsable de leur contenu.</p>
              </div>
            </section>

            <!-- Section 7: Cookies -->
            <section id="cookies" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">7</span>
                Cookies
              </h2>
              <div class="section-content">
                <p>Le site optitab.net peut être amené à vous demander l'acceptation des cookies pour des besoins de statistiques et d'affichage. Un cookie est une information déposée sur votre disque dur par le serveur du site que vous visitez.</p>
                <p>Il contient plusieurs données qui sont stockées sur votre ordinateur dans un simple fichier texte auquel un serveur accède pour lire et enregistrer des informations. Certaines parties de ce site ne peuvent être fonctionnelles sans l'acceptation de cookies.</p>
              </div>
            </section>

            <!-- Section 8: Droit applicable -->
            <section id="droit" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">8</span>
                Droit applicable et juridiction compétente
              </h2>
              <div class="section-content">
                <p>Tout litige en relation avec l'utilisation du site optitab.net est soumis au droit français. Il est fait attribution exclusive de juridiction aux tribunaux compétents d'Angers, France.</p>
              </div>
            </section>

            <!-- Section 9: Contact -->
            <section id="contact" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">9</span>
                Contact
              </h2>
              <div class="section-content">
                <p>Pour toute question concernant ces mentions légales :</p>
                <div class="contact-info">
                  <div class="contact-item">
                    <strong>Email :</strong> <a href="mailto:contact@optitab.net" class="link">contact@optitab.net</a>
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>

        <!-- Footer Note -->
        <div class="cgv-footer">
          <div class="container">
            <div class="footer-note">
              <p><strong>Note importante :</strong> Ces mentions légales sont régies par le droit français. En cas de litige, les tribunaux français seront compétents.</p>
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
        message="Bonjour, j'ai une question sur les mentions légales d'OptiTAB !"
        tooltip="Une question ? Discutons sur WhatsApp !"
      />
    </div>
  </MainLayout>
</template>

<script setup>
import MainLayout from '@/components/layout/MainLayout.vue'
import WhatsappChatButton from '@/components/home/WhatsappChatButton.vue'
import { ref, onMounted, onUnmounted } from 'vue'

// Date actuelle
const currentDate = ref(new Date().toLocaleDateString('fr-FR', {
  year: 'numeric',
  month: 'long',
  day: 'numeric'
}))

// Bouton retour en haut
const showBackToTop = ref(false)

// Section active pour la navigation
const activeSection = ref('')

// Sections pour le sommaire
const sections = ref([
  { id: 'editeur', title: 'Éditeur du site' },
  { id: 'directeur', title: 'Directeur de publication' },
  { id: 'hebergement', title: 'Hébergement' },
  { id: 'propriete', title: 'Propriété intellectuelle' },
  { id: 'responsabilite', title: 'Responsabilité' },
  { id: 'liens', title: 'Liens hypertextes' },
  { id: 'cookies', title: 'Cookies' },
  { id: 'droit', title: 'Droit applicable et juridiction compétente' },
  { id: 'contact', title: 'Contact' }
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

// Lifecycle hooks
onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  // Définir la première section comme active au chargement
  activeSection.value = 'editeur'
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
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: #1f2937;
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
  margin-bottom: 2rem;
  text-align: center;
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
  padding: 0;
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
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.linkedin-link {
  color: #0077b5;
  text-decoration: none;
  transition: color 0.2s ease;
  display: inline-flex;
  align-items: center;
}

.linkedin-link:hover {
  color: #005885;
  transform: scale(1.1);
}

.contact-item:last-child {
  margin-bottom: 0;
}

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
