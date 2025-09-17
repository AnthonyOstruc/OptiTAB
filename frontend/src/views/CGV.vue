<template>
  <MainLayout>
    <div class="cgv-page">
      <!-- Header Section -->
      <div class="cgv-header">
        <div class="container">
          <div class="header-content">
            <h1 class="cgv-title">
              Conditions Générales de Vente
            </h1>
            <p class="cgv-subtitle">
              <span class="gradient-text">OptiTAB</span> - Plateforme d'apprentissage
            </p>
            <div class="cgv-meta">
              <span class="meta-text">Dernière mise à jour : {{ currentDate }} • Version 1.0</span>
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
            <!-- Section 1: Objet -->
            <section id="objet" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">1</span>
                Objet et champ d'application
              </h2>
              <div class="section-content">
                <p>Les présentes Conditions Générales de Vente (CGV) régissent les relations contractuelles entre OptiTAB et ses utilisateurs concernant :</p>
                <ul class="content-list">
                  <li>Les abonnements aux services pédagogiques en ligne,</li>
                  <li>L'accès aux contenus et ressources éducatives,</li>
                  <li>Les services de soutien scolaire personnalisé,</li>
                  <li>Les outils d'apprentissage interactifs.</li>
                </ul>
                <p>La validation d'une commande ou d'un abonnement entraîne l'acceptation pleine et entière des présentes CGV.</p>
              </div>
            </section>

            <!-- Section 2: Définitions -->
            <section id="definitions" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">2</span>
                Définitions
              </h2>
              <div class="section-content">
                <ul class="content-list">
                  <li><strong>Service :</strong> ensemble des fonctionnalités proposées par OptiTAB (contenus pédagogiques, exercices, outils interactifs, suivi, support).</li>
                  <li><strong>Utilisateur :</strong> toute personne naviguant sur le site ou utilisant les services.</li>
                  <li><strong>Abonné :</strong> tout utilisateur disposant d'un abonnement payant.</li>
                  <li><strong>Espace client :</strong> espace personnel permettant à l'abonné de gérer son compte et ses abonnements.</li>
                </ul>
              </div>
            </section>

            <!-- Section 3: Services -->
            <section id="services" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">3</span>
                Description des services
              </h2>
              <div class="section-content">
                <h3 class="subsection-title">3.1 Services inclus</h3>
                <ul class="content-list">
                  <li>Accès illimité à la bibliothèque de contenus pédagogiques,</li>
                  <li>Exercices interactifs et corrigés automatiquement,</li>
                  <li>Suivi personnalisé des progrès,</li>
                  <li>Support technique et pédagogique,</li>
                  <li>Accès mobile et hors ligne (selon l'offre).</li>
                </ul>
                
                <h3 class="subsection-title">3.2 Disponibilité</h3>
                <p>Les services sont disponibles 24h/24, 7j/7, sous réserve d'interruptions liées à la maintenance, aux mises à jour ou à des cas de force majeure.</p>
                <p>OptiTAB met tout en œuvre pour assurer une disponibilité optimale mais ne garantit pas une disponibilité continue à 100 %.</p>
              </div>
            </section>

            <!-- Section 4: Abonnements -->
            <section id="abonnements" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">4</span>
                Abonnements et tarifs
              </h2>
              <div class="section-content">
                <h3 class="subsection-title">4.1 Formules d'abonnement</h3>
                <ul class="content-list">
                  <li><strong>Mensuel :</strong> 19,90 €/mois</li>
                  <li><strong>Annuel :</strong> 199 €/an (soit 16,58 €/mois)</li>
                  <li><strong>Famille :</strong> 29,90 €/mois (jusqu'à 3 enfants)</li>
                </ul>
                
                <h3 class="subsection-title">4.2 Modalités de paiement</h3>
                <p>Paiement par carte bancaire, PayPal ou virement.</p>
                <p>Les abonnements sont renouvelés automatiquement à chaque échéance, sauf résiliation par l'utilisateur.</p>
              </div>
            </section>

            <!-- Section 5: Engagement -->
            <section id="engagement" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">5</span>
                Durée et engagement
              </h2>
              <div class="section-content">
                <ul class="content-list">
                  <li>Les abonnements mensuels se renouvellent automatiquement.</li>
                  <li>Les abonnements annuels sont sans engagement.</li>
                  <li>La résiliation est possible à tout moment depuis l'espace client.</li>
                  <li>L'accès reste actif jusqu'à la fin de la période déjà réglée.</li>
                </ul>
              </div>
            </section>

            <!-- Section 6: Remboursement -->
            <section id="remboursement" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">6</span>
                Politique de remboursement
              </h2>
              <div class="section-content">
                <h3 class="subsection-title">6.1 Droit de rétractation</h3>
                <p>Conformément à l'article L.221-28 du Code de la consommation, le droit de rétractation ne s'applique pas aux services numériques fournis immédiatement après la commande et pleinement exécutés avant la fin du délai de rétractation.</p>
                
                <h3 class="subsection-title">6.2 Remboursement exceptionnel</h3>
                <p>En cas de problème technique majeur non résolu dans un délai de 48h après signalement, un remboursement au prorata pourra être accordé.</p>
              </div>
            </section>

            <!-- Section 7: Conditions d'accès et sécurité -->
            <section id="acces" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">7</span>
                Conditions d'accès et sécurité
              </h2>
              <div class="section-content">
                <ul class="content-list">
                  <li>L'accès aux services nécessite la création d'un compte utilisateur.</li>
                  <li>L'utilisateur s'engage à fournir des informations exactes et à jour.</li>
                  <li>Les identifiants (email et mot de passe) sont strictement personnels et confidentiels.</li>
                  <li>Le partage ou la revente d'un compte est strictement interdit.</li>
                  <li>OptiTAB se réserve le droit de suspendre ou de résilier un compte en cas d'utilisation frauduleuse ou de non-respect des présentes CGV.</li>
                </ul>
              </div>
            </section>

            <!-- Section 8: Propriété intellectuelle -->
            <section id="propriete" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">8</span>
                Propriété intellectuelle
              </h2>
              <div class="section-content">
                <ul class="content-list">
                  <li>L'ensemble des contenus pédagogiques, outils, cours, exercices, fiches, textes, graphismes, vidéos, logos et marques restent la propriété exclusive d'OptiTAB.</li>
                  <li>Toute reproduction, diffusion ou exploitation sans autorisation écrite préalable est interdite et pourra donner lieu à des poursuites.</li>
                  <li>L'utilisateur dispose d'un droit personnel, non exclusif et non transférable d'utiliser les services à titre strictement personnel et non commercial.</li>
                </ul>
              </div>
            </section>

            <!-- Section 9: Responsabilités -->
            <section id="responsabilites" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">9</span>
                Responsabilités
              </h2>
              <div class="section-content">
                <h3 class="subsection-title">9.1 Responsabilité d'OptiTAB</h3>
                <ul class="content-list">
                  <li>Fournir un service conforme à la description,</li>
                  <li>Maintenir une qualité de service dans la mesure du possible,</li>
                  <li>Protéger les données personnelles conformément au RGPD.</li>
                </ul>
                <p>OptiTAB ne pourra être tenu responsable :</p>
                <ul class="content-list">
                  <li>Des interruptions indépendantes de sa volonté (hébergeur, force majeure, panne Internet),</li>
                  <li>D'une mauvaise utilisation du service par l'utilisateur,</li>
                  <li>Des résultats scolaires de l'utilisateur : les contenus pédagogiques sont fournis à titre éducatif, sans garantie de réussite à un examen ou concours.</li>
                </ul>
                
                <h3 class="subsection-title">9.2 Responsabilité de l'utilisateur</h3>
                <ul class="content-list">
                  <li>Utiliser le service conformément aux CGV et CGU,</li>
                  <li>Ne pas nuire au bon fonctionnement du service,</li>
                  <li>Respecter les droits de propriété intellectuelle.</li>
                </ul>
              </div>
            </section>

            <!-- Section 10: Données personnelles -->
            <section id="donnees" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">10</span>
                Données personnelles et confidentialité
              </h2>
              <div class="section-content">
                <p>Le traitement des données personnelles est régi par la Politique de Confidentialité d'OptiTAB, conforme au RGPD.</p>
                <p>L'utilisateur dispose d'un droit d'accès, de rectification, de suppression et d'opposition à ses données, en contactant : <a href="mailto:contact@optitab.com" class="link">contact@optitab.com</a>.</p>
              </div>
            </section>

            <!-- Section 11: Évolution des services -->
            <section id="evolution" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">11</span>
                Évolution des services
              </h2>
              <div class="section-content">
                <p>OptiTAB se réserve le droit de faire évoluer ses services et ses offres. Toute modification substantielle sera communiquée aux abonnés dans un délai raisonnable.</p>
              </div>
            </section>

            <!-- Section 12: Archivage et preuve -->
            <section id="archivage" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">12</span>
                Archivage et preuve
              </h2>
              <div class="section-content">
                <p>Les registres informatisés conservés par OptiTAB seront considérés comme preuve des communications, abonnements, paiements et transactions intervenus entre OptiTAB et l'utilisateur.</p>
              </div>
            </section>

            <!-- Section 13: Droit applicable -->
            <section id="droit" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">13</span>
                Droit applicable et juridiction compétente
              </h2>
              <div class="section-content">
                <p>Les présentes CGV sont régies par le droit français.</p>
                <p>En cas de litige, les tribunaux français seront seuls compétents.</p>
                <p>OptiTAB privilégiera toujours une résolution amiable avant toute procédure judiciaire.</p>
              </div>
            </section>

            <!-- Section 14: Contact -->
            <section id="contact" class="cgv-section">
              <h2 class="section-title">
                <span class="section-number">14</span>
                Contact et support
              </h2>
              <div class="section-content">
                <div class="contact-info">
                  <div class="contact-item">
                    <strong>Email :</strong> <a href="mailto:contact@optitab.com" class="link">contact@optitab.com</a>
                  </div>
                  <div class="contact-item">
                    <strong>Support :</strong> <a href="mailto:support@optitab.com" class="link">support@optitab.com</a>
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
      message="Bonjour, j'ai une question sur les CGV d'OptiTAB !"
      tooltip="Une question ? Discutons sur WhatsApp !"
    />
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
  { id: 'objet', title: 'Objet et champ d\'application' },
  { id: 'definitions', title: 'Définitions' },
  { id: 'services', title: 'Description des services' },
  { id: 'abonnements', title: 'Abonnements et tarifs' },
  { id: 'engagement', title: 'Durée et engagement' },
  { id: 'remboursement', title: 'Politique de remboursement' },
  { id: 'acces', title: 'Conditions d\'accès et sécurité' },
  { id: 'propriete', title: 'Propriété intellectuelle' },
  { id: 'responsabilites', title: 'Responsabilités' },
  { id: 'donnees', title: 'Données personnelles et confidentialité' },
  { id: 'evolution', title: 'Évolution des services' },
  { id: 'archivage', title: 'Archivage et preuve' },
  { id: 'droit', title: 'Droit applicable et juridiction compétente' },
  { id: 'contact', title: 'Contact et support' }
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
  activeSection.value = 'objet'
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