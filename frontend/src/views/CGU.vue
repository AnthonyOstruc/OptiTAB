<template>
  <MainLayout>
    <div class="cgv-page">
      <!-- Header Section -->
      <div class="cgv-header">
        <div class="container">
          <div class="header-content">
            <h1 class="cgv-title">
              Conditions Générales d'Utilisation
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
            <!-- Section 1: Définitions -->
            <section id="definitions" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">1</span>
                Définitions
              </h2>
              <div class="section-content">
                <ul class="content-list">
                  <li><strong>OptiTAB / la plateforme / le service :</strong> site Internet et applications associées fournissant des cours particuliers, exercices guidés, fiches pédagogiques et outils éducatifs.</li>
                  <li><strong>Utilisateur :</strong> toute personne s'inscrivant ou utilisant OptiTAB.</li>
                  <li><strong>Compte utilisateur :</strong> espace personnel créé lors de l'inscription permettant l'accès aux services.</li>
                  <li><strong>Abonnement :</strong> contrat d'accès payant aux services proposés par OptiTAB.</li>
                  <li><strong>Contenu :</strong> textes, images, vidéos, logiciels, exercices, fiches pédagogiques, outils et tout matériel mis à disposition sur la plateforme.</li>
                  <li><strong>Prestataire :</strong> tiers participant à l'hébergement, paiement ou services techniques.</li>
                </ul>
              </div>
            </section>

            <!-- Section 2: Accès au service -->
            <section id="acces" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">2</span>
                Accès au service
              </h2>
              <div class="section-content">
                <ul class="content-list">
                  <li>L'accès à OptiTAB nécessite la création d'un compte valide.</li>
                  <li>L'utilisateur doit fournir des informations exactes et à jour.</li>
                  <li>La confidentialité des identifiants est de la responsabilité de l'utilisateur. Toute activité sur le compte est imputable à l'utilisateur.</li>
                  <li>OptiTAB peut suspendre ou supprimer un compte en cas de non-respect des CGU, pour maintenance, problème technique ou force majeure, sans responsabilité.</li>
                </ul>
              </div>
            </section>

            <!-- Section 3: Services proposés -->
            <section id="services" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">3</span>
                Services proposés
              </h2>
              <div class="section-content">
                <p>OptiTAB propose :</p>
                <ul class="content-list">
                  <li>Des cours particuliers en ligne avec réservation.</li>
                  <li>Des exercices guidés et fiches pédagogiques.</li>
                  <li>Des outils de calcul et d'aide aux devoirs.</li>
                </ul>
                <p>La plateforme peut modifier, suspendre ou interrompre tout service à tout moment, temporairement ou définitivement, avec ou sans préavis.</p>
              </div>
            </section>

            <!-- Section 4: Abonnements et paiements -->
            <section id="abonnements" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">4</span>
                Abonnements et paiements
              </h2>
              <div class="section-content">
                <ul class="content-list">
                  <li>Les services peuvent être proposés via des abonnements payants.</li>
                  <li>Paiement en ligne par carte bancaire, PayPal ou virement sécurisé.</li>
                  <li>Les abonnements se renouvellent automatiquement sauf résiliation par l'utilisateur.</li>
                  <li>Aucun remboursement n'est possible pour les périodes déjà entamées, sauf dispositions légales.</li>
                  <li>En cas de défaut de paiement, OptiTAB peut suspendre l'accès au compte.</li>
                </ul>
                <p>Conformément à l'article L221-28 du Code de la consommation, le droit de rétractation ne s'applique pas aux services numériques fournis immédiatement après la commande.</p>
                <p>En cas de problème technique majeur non résolu sous 48h, un remboursement au prorata peut être accordé.</p>
              </div>
            </section>

            <!-- Section 5: Propriété intellectuelle -->
            <section id="propriete" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">5</span>
                Propriété intellectuelle
              </h2>
              <div class="section-content">
                <ul class="content-list">
                  <li>Tous les contenus (textes, images, vidéos, logiciels, exercices, fiches) sont protégés par le droit d'auteur.</li>
                  <li>Toute reproduction, diffusion, extraction ou exploitation commerciale sans autorisation écrite est interdite et passible de sanctions civiles et pénales.</li>
                  <li>L'arborescence et la structure du site sont protégées.</li>
                  <li>L'utilisateur peut utiliser le contenu uniquement pour un usage personnel et non commercial.</li>
                </ul>
              </div>
            </section>

            <!-- Section 6: Contenu utilisateur -->
            <section id="contenu" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">6</span>
                Contenu utilisateur
              </h2>
              <div class="section-content">
                <ul class="content-list">
                  <li>Les utilisateurs conservent la propriété des contenus qu'ils postent (exercices, commentaires).</li>
                  <li>En publiant sur OptiTAB, l'utilisateur accorde une licence non exclusive, gratuite et mondiale à OptiTAB pour utiliser ce contenu afin d'améliorer les services.</li>
                  <li>Tout contenu illégal, injurieux ou portant atteinte aux droits d'autrui est interdit.</li>
                  <li>L'utilisateur garantit être titulaire des droits sur le contenu publié. OptiTAB peut supprimer tout contenu non conforme.</li>
                </ul>
              </div>
            </section>

            <!-- Section 7: Obligations de l'utilisateur -->
            <section id="obligations" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">7</span>
                Obligations de l'utilisateur
              </h2>
              <div class="section-content">
                <ul class="content-list">
                  <li>Ne pas utiliser la plateforme à des fins illégales ou frauduleuses.</li>
                  <li>Ne pas perturber le fonctionnement du site ou tenter d'accéder à des données non autorisées.</li>
                  <li>Respecter les autres utilisateurs et le personnel d'OptiTAB.</li>
                  <li>Respecter les règles relatives aux mineurs : tout utilisateur de moins de 15 ans doit fournir un consentement parental explicite pour créer un compte et utiliser la plateforme. Les utilisateurs de 15 ans et plus peuvent consentir eux-mêmes au traitement de leurs données personnelles.</li>
                </ul>
              </div>
            </section>

            <!-- Section 8: Données personnelles et sécurité -->
            <section id="donnees" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">8</span>
                Données personnelles et sécurité
              </h2>
              <div class="section-content">
                <ul class="content-list">
                  <li>Les données collectées sont traitées conformément à la Politique de confidentialité complète.</li>
                  <li>L'utilisateur peut accéder, rectifier, supprimer ou demander la portabilité de ses données personnelles.</li>
                  <li>OptiTAB met en place des mesures de sécurité pour protéger les comptes et données, mais l'utilisateur reste responsable de la confidentialité de son mot de passe.</li>
                  <li>Les données peuvent être partagées avec des prestataires (hébergement, paiement, emailing) sous garanties RGPD.</li>
                </ul>
              </div>
            </section>

            <!-- Section 9: Cookies et tracking -->
            <section id="cookies" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">9</span>
                Cookies et tracking
              </h2>
              <div class="section-content">
                <ul class="content-list">
                  <li>OptiTAB utilise des cookies pour le fonctionnement du site, l'authentification et les statistiques (ex. Google Analytics, pixel Facebook).</li>
                  <li>L'utilisateur peut refuser les cookies via les paramètres de son navigateur.</li>
                  <li>Le refus des cookies peut limiter certaines fonctionnalités de la plateforme.</li>
                </ul>
              </div>
            </section>

            <!-- Section 10: Responsabilité -->
            <section id="responsabilite" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">10</span>
                Responsabilité
              </h2>
              <div class="section-content">
                <ul class="content-list">
                  <li>OptiTAB s'efforce de fournir des contenus exacts et des services disponibles.</li>
                  <li>La plateforme n'est pas responsable des erreurs, omissions ou résultats scolaires obtenus par l'utilisateur.</li>
                  <li>OptiTAB ne peut être tenu responsable des dommages indirects liés à l'utilisation du service (perte de données, interruption de service, etc.).</li>
                  <li>OptiTAB n'est pas responsable des contenus publiés par les utilisateurs.</li>
                </ul>
              </div>
            </section>

            <!-- Section 11: Suspension et résiliation -->
            <section id="suspension" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">11</span>
                Suspension et résiliation
              </h2>
              <div class="section-content">
                <ul class="content-list">
                  <li>OptiTAB peut suspendre ou résilier un compte en cas de violation des CGU.</li>
                  <li>L'utilisateur peut supprimer son compte à tout moment depuis son espace personnel.</li>
                  <li>La résiliation ou suspension peut entraîner la perte des contenus et données, sauf obligations légales.</li>
                </ul>
              </div>
            </section>

            <!-- Section 12: Modifications des CGU -->
            <section id="modifications" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">12</span>
                Modifications des CGU
              </h2>
              <div class="section-content">
                <ul class="content-list">
                  <li>OptiTAB se réserve le droit de modifier les CGU à tout moment.</li>
                  <li>Les utilisateurs seront informés par email ou notification.</li>
                  <li>La continuité d'utilisation vaut acceptation des nouvelles CGU.</li>
                </ul>
              </div>
            </section>

            <!-- Section 13: Mineurs -->
            <section id="mineurs" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">13</span>
                Mineurs
              </h2>
              <div class="section-content">
                <ul class="content-list">
                  <li>Pour les utilisateurs de moins de 15 ans, l'inscription nécessite un consentement parental explicite.</li>
                  <li>Les utilisateurs de 15 ans et plus peuvent consentir eux-mêmes au traitement de leurs données personnelles.</li>
                  <li>OptiTAB peut demander une preuve de consentement parental si nécessaire.</li>
                </ul>
              </div>
            </section>

            <!-- Section 14: Résolution des litiges -->
            <section id="litiges" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">14</span>
                Résolution des litiges
              </h2>
              <div class="section-content">
                <ul class="content-list">
                  <li>Les présentes CGU sont régies par le droit français.</li>
                  <li>En cas de litige, les parties s'engagent à rechercher une solution amiable avant toute action judiciaire.</li>
                  <li>À défaut d'accord, le litige sera porté devant les tribunaux compétents en France.</li>
                  <li>L'utilisateur peut également saisir un médiateur de la consommation.</li>
                </ul>
              </div>
            </section>

            <!-- Section 15: Contact -->
            <section id="contact" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">15</span>
                Contact
              </h2>
              <div class="section-content">
                <p>Pour toute question relative aux CGU ou à la plateforme :</p>
                <div class="contact-info">
                  <div class="contact-item">
                    <strong>Email :</strong> <a href="mailto:contact@optitab.net" class="link">contact@optitab.net</a>
                  </div>
                  <div class="contact-item">
                    <strong>WhatsApp :</strong> <a href="https://wa.me/33764040251" class="link">07 64 04 02 51</a>
                  </div>
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
            <p><strong>Note importante :</strong> Ces conditions peuvent être modifiées. Les utilisateurs seront informés de tout changement par email ou notification sur la plateforme.</p>
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
        message="Bonjour, j'ai une question sur les CGU d'OptiTAB !"
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
  { id: 'definitions', title: 'Définitions' },
  { id: 'acces', title: 'Accès au service' },
  { id: 'services', title: 'Services proposés' },
  { id: 'abonnements', title: 'Abonnements et paiements' },
  { id: 'propriete', title: 'Propriété intellectuelle' },
  { id: 'contenu', title: 'Contenu utilisateur' },
  { id: 'obligations', title: 'Obligations de l\'utilisateur' },
  { id: 'donnees', title: 'Données personnelles et sécurité' },
  { id: 'cookies', title: 'Cookies et tracking' },
  { id: 'responsabilite', title: 'Responsabilité' },
  { id: 'suspension', title: 'Suspension et résiliation' },
  { id: 'modifications', title: 'Modifications des CGU' },
  { id: 'mineurs', title: 'Mineurs' },
  { id: 'litiges', title: 'Résolution des litiges' },
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
  activeSection.value = 'definitions'
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