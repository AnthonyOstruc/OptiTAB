<template>
  <MainLayout>
    <div class="cgv-page">
      <!-- Header Section -->
      <div class="cgv-header">
        <div class="container">
          <div class="header-content">
            <h1 class="cgv-title">
              Politique de Cookies
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
            <!-- Section 1: Qu'est-ce qu'un cookie -->
            <section id="definition" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">1</span>
                Qu'est-ce qu'un cookie ?
              </h2>
              <div class="section-content">
                <p>Un cookie est un petit fichier texte déposé sur votre ordinateur, tablette ou smartphone lorsque vous visitez un site web. Il permet au site de mémoriser vos actions et préférences pendant une période donnée, afin que vous n'ayez pas à les ressaisir à chaque visite ou navigation sur le site.</p>
                <p>Les cookies ne peuvent pas endommager votre ordinateur et ne contiennent aucun virus. Ils sont utilisés par la plupart des sites web pour améliorer votre expérience de navigation.</p>
              </div>
            </section>

            <!-- Section 2: Types de cookies -->
            <section id="types" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">2</span>
                Types de cookies utilisés
              </h2>
              <div class="section-content">
                <h3 class="subsection-title">2.1 Cookies strictement nécessaires</h3>
                <p>Ces cookies sont indispensables au fonctionnement du site et ne peuvent pas être désactivés. Ils permettent :</p>
                <ul class="content-list">
                  <li>La navigation sur le site et l'utilisation de ses fonctionnalités</li>
                  <li>La mémorisation de votre session de connexion</li>
                  <li>La sécurité et la prévention des fraudes</li>
                  <li>L'équilibrage de la charge du serveur</li>
                </ul>

                <h3 class="subsection-title">2.2 Cookies de performance</h3>
                <p>Ces cookies nous aident à comprendre comment les visiteurs interagissent avec notre site :</p>
                <ul class="content-list">
                  <li>Nombre de visiteurs et pages visitées</li>
                  <li>Temps passé sur le site</li>
                  <li>Sources de trafic</li>
                  <li>Pages d'erreur rencontrées</li>
                </ul>

                <h3 class="subsection-title">2.3 Cookies de fonctionnalité</h3>
                <p>Ces cookies permettent d'améliorer votre expérience utilisateur :</p>
                <ul class="content-list">
                  <li>Mémorisation de vos préférences (langue, région)</li>
                  <li>Personnalisation de l'interface</li>
                  <li>Rappel de vos choix précédents</li>
                </ul>

                <h3 class="subsection-title">2.4 Cookies de ciblage</h3>
                <p>Ces cookies sont utilisés pour :</p>
                <ul class="content-list">
                  <li>Proposer des contenus adaptés à vos centres d'intérêt</li>
                  <li>Mesurer l'efficacité de nos campagnes publicitaires</li>
                  <li>Limiter le nombre d'affichages d'une publicité</li>
                </ul>
              </div>
            </section>

            <!-- Section 3: Cookies utilisés sur OptiTAB -->
            <section id="cookies-optitab" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">3</span>
                Cookies utilisés sur OptiTAB
              </h2>
              <div class="section-content">
                <div class="cookies-table">
                  <div class="cookie-item">
                    <div class="cookie-name">Session utilisateur</div>
                    <div class="cookie-details">
                      <strong>Finalité :</strong> Maintien de votre session de connexion<br>
                      <strong>Durée :</strong> Session (supprimé à la fermeture du navigateur)<br>
                      <strong>Type :</strong> Strictement nécessaire
                    </div>
                  </div>
                  
                  <div class="cookie-item">
                    <div class="cookie-name">Préférences utilisateur</div>
                    <div class="cookie-details">
                      <strong>Finalité :</strong> Mémorisation de vos paramètres et préférences<br>
                      <strong>Durée :</strong> 1 an<br>
                      <strong>Type :</strong> Fonctionnalité
                    </div>
                  </div>
                  
                  <div class="cookie-item">
                    <div class="cookie-name">Analytiques</div>
                    <div class="cookie-details">
                      <strong>Finalité :</strong> Analyse du trafic et amélioration du site<br>
                      <strong>Durée :</strong> 13 mois<br>
                      <strong>Type :</strong> Performance
                    </div>
                  </div>
                  
                  <div class="cookie-item">
                    <div class="cookie-name">Sécurité</div>
                    <div class="cookie-details">
                      <strong>Finalité :</strong> Protection contre les attaques et fraudes<br>
                      <strong>Durée :</strong> 24 heures<br>
                      <strong>Type :</strong> Strictement nécessaire
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <!-- Section 4: Gestion des cookies -->
            <section id="gestion" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">4</span>
                Gestion de vos cookies
              </h2>
              <div class="section-content">
                <h3 class="subsection-title">4.1 Paramètres du navigateur</h3>
                <p>Vous pouvez configurer votre navigateur pour :</p>
                <ul class="content-list">
                  <li>Accepter tous les cookies</li>
                  <li>Refuser tous les cookies</li>
                  <li>Être notifié avant l'installation d'un cookie</li>
                  <li>Supprimer les cookies existants</li>
                </ul>

                <h3 class="subsection-title">4.2 Instructions par navigateur</h3>
                <div class="browser-instructions">
                  <div class="browser-item">
                    <strong>Google Chrome :</strong> Paramètres > Confidentialité et sécurité > Cookies et autres données de site
                  </div>
                  <div class="browser-item">
                    <strong>Mozilla Firefox :</strong> Options > Vie privée et sécurité > Cookies et données de sites
                  </div>
                  <div class="browser-item">
                    <strong>Safari :</strong> Préférences > Confidentialité > Gérer les données de site web
                  </div>
                  <div class="browser-item">
                    <strong>Microsoft Edge :</strong> Paramètres > Cookies et autorisations de site
                  </div>
                </div>

                <h3 class="subsection-title">4.3 Conséquences du refus</h3>
                <p>Si vous refusez les cookies :</p>
                <ul class="content-list">
                  <li>Certaines fonctionnalités du site peuvent ne pas fonctionner correctement</li>
                  <li>Vous devrez vous reconnecter à chaque visite</li>
                  <li>Vos préférences ne seront pas mémorisées</li>
                  <li>L'expérience utilisateur peut être dégradée</li>
                </ul>
              </div>
            </section>

            <!-- Section 5: Cookies tiers -->
            <section id="tiers" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">5</span>
                Cookies de tiers
              </h2>
              <div class="section-content">
                <p>Notre site peut contenir des cookies provenant de services tiers :</p>
                
                <h3 class="subsection-title">5.1 Google Analytics</h3>
                <p>Nous utilisons Google Analytics pour analyser l'utilisation de notre site :</p>
                <ul class="content-list">
                  <li><strong>Finalité :</strong> Mesure d'audience et statistiques</li>
                  <li><strong>Données collectées :</strong> Pages visitées, durée de visite, source de trafic</li>
                  <li><strong>Durée :</strong> 13 mois</li>
                  <li><strong>Désactivation :</strong> <a href="https://tools.google.com/dlpage/gaoptout" class="link" target="_blank">Outil de désactivation Google Analytics</a></li>
                </ul>

                <h3 class="subsection-title">5.2 Réseaux sociaux</h3>
                <p>Des boutons de partage peuvent déposer des cookies :</p>
                <ul class="content-list">
                  <li>Facebook, Twitter, LinkedIn, etc.</li>
                  <li>Ces cookies sont gérés par les plateformes concernées</li>
                  <li>Consultez leurs politiques de confidentialité respectives</li>
                </ul>
              </div>
            </section>

            <!-- Section 6: Durée de conservation -->
            <section id="duree" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">6</span>
                Durée de conservation
              </h2>
              <div class="section-content">
                <p>Les cookies ont différentes durées de vie :</p>
                <ul class="content-list">
                  <li><strong>Cookies de session :</strong> Supprimés à la fermeture du navigateur</li>
                  <li><strong>Cookies persistants :</strong> Conservés selon la durée définie (de quelques jours à plusieurs années)</li>
                  <li><strong>Cookies de sécurité :</strong> Généralement 24 heures</li>
                  <li><strong>Cookies de préférences :</strong> 1 an maximum</li>
                  <li><strong>Cookies analytiques :</strong> 13 mois maximum</li>
                </ul>
                <p>Vous pouvez supprimer manuellement tous les cookies à tout moment via les paramètres de votre navigateur.</p>
              </div>
            </section>

            <!-- Section 7: Vos droits -->
            <section id="droits" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">7</span>
                Vos droits
              </h2>
              <div class="section-content">
                <p>Concernant les cookies, vous avez le droit de :</p>
                <ul class="content-list">
                  <li><strong>Être informé :</strong> Connaître les cookies utilisés et leur finalité</li>
                  <li><strong>Donner votre consentement :</strong> Accepter ou refuser les cookies non essentiels</li>
                  <li><strong>Retirer votre consentement :</strong> Modifier vos préférences à tout moment</li>
                  <li><strong>Accéder aux données :</strong> Demander quelles données sont collectées</li>
                  <li><strong>Supprimer :</strong> Effacer les cookies de votre navigateur</li>
                </ul>
                <p>Pour exercer ces droits, contactez-nous à <a href="mailto:support@optitab.net" class="link">support@optitab.net</a></p>
              </div>
            </section>

            <!-- Section 8: Contact -->
            <section id="contact" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">8</span>
                Contact
              </h2>
              <div class="section-content">
                <p>Pour toute question concernant notre politique de cookies :</p>
                <div class="contact-info">
                  <div class="contact-item">
                    <strong>Email :</strong> <a href="mailto:support@optitab.net" class="link">support@optitab.net</a>
                  </div>
                </div>
                <p>Nous nous engageons à répondre à vos demandes dans les meilleurs délais.</p>
              </div>
            </section>
          </div>
        </div>

        <!-- Footer Note -->
        <div class="cgv-footer">
          <div class="container">
            <div class="footer-note">
              <p><strong>Note importante :</strong> Cette politique de cookies peut être modifiée pour refléter les changements dans nos pratiques ou pour des raisons légales. Nous vous informerons de tout changement significatif.</p>
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
        message="Bonjour, j'ai une question sur la politique de cookies d'OptiTAB !"
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
  { id: 'definition', title: 'Qu\'est-ce qu\'un cookie ?' },
  { id: 'types', title: 'Types de cookies utilisés' },
  { id: 'cookies-optitab', title: 'Cookies utilisés sur OptiTAB' },
  { id: 'gestion', title: 'Gestion de vos cookies' },
  { id: 'tiers', title: 'Cookies de tiers' },
  { id: 'duree', title: 'Durée de conservation' },
  { id: 'droits', title: 'Vos droits' },
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
  activeSection.value = 'definition'
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

/* Cookies table */
.cookies-table {
  margin: 1.5rem 0;
}

.cookie-item {
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
}

.cookie-name {
  font-weight: 600;
  color: #1f2937;
  font-size: 1.1rem;
  margin-bottom: 0.75rem;
}

.cookie-details {
  color: #4b5563;
  line-height: 1.6;
}

/* Browser instructions */
.browser-instructions {
  margin: 1.5rem 0;
}

.browser-item {
  background: #f8fafc;
  border-left: 4px solid #6366f1;
  padding: 1rem;
  margin-bottom: 0.75rem;
  color: #4b5563;
  line-height: 1.6;
}

.browser-item strong {
  color: #1f2937;
  font-weight: 600;
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

  .cookie-item {
    padding: 1rem;
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
