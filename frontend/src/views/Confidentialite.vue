<template>
  <MainLayout>
    <div class="cgv-page">
      <!-- Header Section -->
      <div class="cgv-header">
        <div class="container">
          <div class="header-content">
            <h1 class="cgv-title">
              Politique de Confidentialité
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
            <!-- Section 1: Responsable du traitement -->
            <section id="responsable" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">1</span>
                Responsable du traitement
              </h2>
              <div class="section-content">
                <p>Le responsable du traitement des données est :</p>
                <div class="contact-info">
                  <div class="contact-item">
                    <strong>OptiTAB</strong>
                  </div>
                  <div class="contact-item">
                    <strong>Email :</strong> <a href="mailto:support@optitab.net" class="link">support@optitab.net</a>
                  </div>
                </div>
              </div>
            </section>

            <!-- Section 2: Données collectées -->
            <section id="donnees" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">2</span>
                Données collectées
              </h2>
              <div class="section-content">
                <p>Lors de l'utilisation de la plateforme, nous pouvons collecter :</p>
                <ul class="content-list">
                  <li><strong>Informations d'inscription :</strong> nom, prénom, email, mot de passe.</li>
                  <li><strong>Informations de paiement :</strong> carte bancaire ou autre méthode utilisée pour les abonnements.</li>
                  <li><strong>Données d'utilisation :</strong> historique de connexion, pages visitées, activités sur la plateforme.</li>
                  <li><strong>Contenu généré par l'utilisateur :</strong> exercices envoyés pour correction, commentaires.</li>
                </ul>
                <p>Toutes les données collectées sont utilisées exclusivement pour le fonctionnement et l'amélioration de nos services.</p>
              </div>
            </section>

            <!-- Section 3: Finalité du traitement -->
            <section id="finalite" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">3</span>
                Finalité du traitement
              </h2>
              <div class="section-content">
                <p>Les données sont utilisées pour :</p>
                <ul class="content-list">
                  <li>Gérer les comptes utilisateurs et l'accès aux services.</li>
                  <li>Traiter les abonnements et paiements.</li>
                  <li>Personnaliser l'expérience utilisateur.</li>
                  <li>Envoyer des notifications, mises à jour et communications importantes.</li>
                  <li>Améliorer et sécuriser la plateforme.</li>
                </ul>
              </div>
            </section>

            <!-- Section 4: Base légale -->
            <section id="base" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">4</span>
                Base légale
              </h2>
              <div class="section-content">
                <p>Le traitement des données repose sur :</p>
                <ul class="content-list">
                  <li>L'exécution du contrat (gestion de votre compte et abonnements).</li>
                  <li>Votre consentement pour certaines communications ou services.</li>
                  <li>L'intérêt légitime de la plateforme pour sécuriser et améliorer le service.</li>
                </ul>
              </div>
            </section>

            <!-- Section 5: Partage des données -->
            <section id="partage" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">5</span>
                Partage des données
              </h2>
              <div class="section-content">
                <p>OptiTAB ne vend ni ne loue vos données. Les informations peuvent être partagées uniquement avec :</p>
                <ul class="content-list">
                  <li>Prestataires techniques nécessaires au fonctionnement de la plateforme (hébergement, paiement sécurisé).</li>
                  <li>Autorités légales si la loi l'exige.</li>
                </ul>
              </div>
            </section>

            <!-- Section 6: Sécurité des données -->
            <section id="securite" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">6</span>
                Sécurité des données
              </h2>
              <div class="section-content">
                <p>Nous mettons en place des mesures techniques et organisationnelles pour protéger vos données :</p>
                <ul class="content-list">
                  <li>Chiffrement des informations sensibles (mot de passe, données financières).</li>
                  <li>Sauvegardes régulières.</li>
                  <li>Limitation d'accès aux données aux seules personnes autorisées.</li>
                </ul>
              </div>
            </section>

            <!-- Section 7: Conservation des données -->
            <section id="conservation" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">7</span>
                Conservation des données
              </h2>
              <div class="section-content">
                <ul class="content-list">
                  <li>Les données liées au compte sont conservées tant que le compte existe.</li>
                  <li>Les données financières sont conservées conformément aux obligations légales et fiscales.</li>
                  <li>Les données anonymisées peuvent être utilisées à des fins statistiques.</li>
                </ul>
              </div>
            </section>

            <!-- Section 8: Droits des utilisateurs -->
            <section id="droits" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">8</span>
                Droits des utilisateurs
              </h2>
              <div class="section-content">
                <p>Vous pouvez à tout moment :</p>
                <ul class="content-list">
                  <li>Accéder à vos données personnelles.</li>
                  <li>Rectifier des informations inexactes.</li>
                  <li>Supprimer votre compte et vos données (dans la limite des obligations légales).</li>
                  <li>Demander la limitation du traitement ou vous opposer à certaines utilisations.</li>
                  <li>Retirer votre consentement pour certaines communications.</li>
                </ul>
                <p>Pour exercer vos droits : <a href="mailto:support@optitab.net" class="link">support@optitab.net</a></p>
              </div>
            </section>

            <!-- Section 9: Cookies et traceurs -->
            <section id="cookies" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">9</span>
                Cookies et traceurs
              </h2>
              <div class="section-content">
                <p>OptiTAB utilise des cookies pour :</p>
                <ul class="content-list">
                  <li>Assurer le bon fonctionnement du site.</li>
                  <li>Analyser la fréquentation du site (statistiques anonymes).</li>
                  <li>Garder votre session active et personnaliser l'expérience utilisateur.</li>
                </ul>
                <p>Vous pouvez configurer votre navigateur pour refuser les cookies, mais certaines fonctionnalités pourraient être limitées.</p>
              </div>
            </section>

            <!-- Section 10: Mineurs -->
            <section id="mineurs" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">10</span>
                Mineurs
              </h2>
              <div class="section-content">
                <ul class="content-list">
                  <li>L'accès à OptiTAB est interdit aux enfants de moins de 13 ans sans consentement parental.</li>
                  <li>Les parents ou tuteurs peuvent demander la suppression des données de leurs enfants.</li>
                </ul>
              </div>
            </section>

            <!-- Section 11: Modifications de la Politique -->
            <section id="modifications" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">11</span>
                Modifications de la Politique
              </h2>
              <div class="section-content">
                <p>OptiTAB peut modifier cette politique pour se conformer à la législation ou améliorer la transparence.</p>
                <p>Les utilisateurs seront informés des changements. L'usage continu de la plateforme vaut acceptation de la nouvelle politique.</p>
              </div>
            </section>

            <!-- Section 12: Contact -->
            <section id="contact" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">12</span>
                Contact
              </h2>
              <div class="section-content">
                <p>Pour toute question relative à la confidentialité :</p>
                <div class="contact-info">
                  <div class="contact-item">
                    <strong>Email :</strong> <a href="mailto:support@optitab.net" class="link">support@optitab.net</a>
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
              <p><strong>Note importante :</strong> Cette politique de confidentialité est régie par le droit français et le RGPD. En cas de litige, les tribunaux français seront compétents.</p>
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
        message="Bonjour, j'ai une question sur la politique de confidentialité d'OptiTAB !"
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
  { id: 'responsable', title: 'Responsable du traitement' },
  { id: 'donnees', title: 'Données collectées' },
  { id: 'finalite', title: 'Finalité du traitement' },
  { id: 'base', title: 'Base légale' },
  { id: 'partage', title: 'Partage des données' },
  { id: 'securite', title: 'Sécurité des données' },
  { id: 'conservation', title: 'Conservation des données' },
  { id: 'droits', title: 'Droits des utilisateurs' },
  { id: 'cookies', title: 'Cookies et traceurs' },
  { id: 'mineurs', title: 'Mineurs' },
  { id: 'modifications', title: 'Modifications de la Politique' },
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
  activeSection.value = 'responsable'
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