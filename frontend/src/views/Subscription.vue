<template>
  <DashboardLayout>
    <div class="subscription-page">
      <!-- Page Header -->
      <div class="page-header">
        <div class="header-badge">
          <svg class="badge-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5z"/>
            <path d="M2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
          <span>Abonnement</span>
        </div>
        <h1>Mon abonnement</h1>
        <p>Gérez votre abonnement et accédez à toutes vos informations</p>
      </div>

      <!-- Subscription Manager -->
      <div class="subscription-wrapper">
        <SubscriptionManager />
      </div>

      <!-- Contact Section -->
      <div class="contact-section">
        <div class="contact-content">
          <div class="contact-header">
            <h3>Besoin d'aide ?</h3>
            <p>Notre équipe est disponible pour répondre à vos questions</p>
          </div>
          <div class="contact-actions">
            <a
              class="contact-btn whatsapp"
              data-cta-name="whatsapp"
              data-cta-location="subscription"
              href="https://wa.me/33764040251"
              target="_blank"
              rel="noopener noreferrer"
            >
              <svg class="btn-icon whatsapp-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
              </svg>
              <span>WhatsApp</span>
            </a>
            <a
              class="contact-btn email"
              href="mailto:contact@optitab.net"
            >
              <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="4" width="20" height="16" rx="2"/>
                <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
              </svg>
              <span>Email</span>
            </a>
          </div>
        </div>
        <div class="contact-badge">
          <svg class="badge-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          <span>Réponse sous 24h</span>
        </div>
      </div>

      <!-- Back to Plans -->
      <div class="back-section">
        <router-link to="/billing" class="back-button" data-cta-name="subscribe" data-cta-location="subscription">
          <svg class="back-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
          <span>Voir les offres</span>
        </router-link>
      </div>

      <Footer />
    </div>
  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import SubscriptionManager from '@/components/payments/SubscriptionManager.vue'
import Footer from '@/components/layout/Footer.vue'
</script>

<style scoped>
/* Base Layout */
.subscription-page {
  min-height: 100vh;
  padding: 2.5rem 1.5rem;
  font-size: 0.96rem;
  width: 100%;
  max-width: none;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  max-width: 960px;
  margin: 0 auto 3rem;
  text-align: center;
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%);
  border: 1px solid #bfdbfe;
  border-radius: 999px;
  color: #1e40af;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.badge-icon {
  width: 16px;
  height: 16px;
  color: #3b82f6;
}

.page-header h1 {
  font-size: 2.2rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 1rem;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.page-header p {
  font-size: 1rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.6;
}

/* Subscription Wrapper */
.subscription-wrapper {
  max-width: 1200px;
  margin: 0 auto 3rem;
}

:deep(.subscription-manager) {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

/* Contact Section */
.contact-section {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto 3.5rem;
  padding: 0;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  overflow: hidden;
}

.contact-content {
  padding: 2.75rem 3.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 3.25rem;
}

.contact-header {
  flex: 1;
}

.contact-header h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.5rem;
  line-height: 1.3;
}

.contact-header p {
  font-size: 0.95rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.5;
}

.contact-actions {
  display: flex;
  gap: 1rem;
  flex-shrink: 0;
}

.contact-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  transition: all 0.2s ease;
  border: 1px solid #d1d5db;
  background: white;
  color: #374151;
}

.contact-btn.whatsapp {
  background: #25d366;
  border-color: #25d366;
  color: white;
}

.contact-btn.whatsapp:hover {
  background: #20ba5a;
  border-color: #20ba5a;
  transform: translateY(-1px);
}

.contact-btn.email:hover {
  border-color: #9ca3af;
  background: #f9fafb;
}

.btn-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.contact-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  background: #f3f4f6;
  border-top: 1px solid #e5e7eb;
  font-size: 0.875rem;
  color: #4b5563;
  font-weight: 500;
}

.contact-badge .badge-icon {
  width: 16px;
  height: 16px;
  color: #6b7280;
}

/* Back Section */
.back-section {
  max-width: 1100px;
  margin: 0 auto 4.5rem;
  text-align: center;
}

.back-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.5rem 1rem;
  border-radius: 999px;
  background: #2563eb;
  color: #ffffff;
  font-weight: 600;
  font-size: 0.9rem;
  text-decoration: none;
  transition: all 0.18s ease;
  box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2);
}

.back-button:hover {
  background: #1e40af;
  transform: translateY(-1px);
  box-shadow: 0 7px 16px rgba(30, 64, 175, 0.22);
}

.back-icon {
  width: 0.95rem;
  height: 0.95rem;
}

/* Footer - Full width without horizontal scroll */
.subscription-page :deep(.footer) {
  width: 100%;
  margin: 0;
  border-radius: 0;
}

/* Responsive */
@media (max-width: 968px) {
  .subscription-page {
    padding: 2rem 1rem;
  }

  .page-header h1 {
    font-size: 1.875rem;
  }

  .page-header p {
    font-size: 0.95rem;
  }

  .contact-content {
    flex-direction: column;
    align-items: flex-start;
    padding: 2rem 1.5rem;
    gap: 1.5rem;
  }

  .contact-actions {
    flex-direction: row;
    flex-wrap: wrap;
    width: 100%;
  }

  .contact-btn {
    flex: 1 1 140px;
  }

  .back-button {
    padding: 0.625rem 1.25rem;
    font-size: 0.875rem;
  }
}

@media (max-width: 640px) {
  .subscription-page {
    padding: 1.25rem 0.75rem;
    font-size: 0.94rem;
  }

  .page-header {
    margin-bottom: 2rem;
  }

  .page-header h1 {
    font-size: 1.625rem;
  }

  .page-header p {
    font-size: 0.9rem;
  }

  .header-badge {
    padding: 0.4rem 0.875rem;
    font-size: 0.8125rem;
    margin-bottom: 1.25rem;
  }

  .badge-icon {
    width: 14px;
    height: 14px;
  }

  .subscription-wrapper {
    margin-bottom: 2rem;
  }

  .contact-section {
    margin-bottom: 2.5rem;
  }

  .contact-content {
    padding: 1.5rem 1.25rem;
    gap: 1.25rem;
  }

  .contact-header h3 {
    font-size: 1.25rem;
    line-height: 1.3;
  }

  .contact-header p {
    font-size: 0.875rem;
    line-height: 1.4;
  }

  .contact-actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.625rem;
    width: 100%;
  }

  .contact-btn {
    width: 100%;
    padding: 0.75rem 0.875rem;
    font-size: 0.8125rem;
    justify-content: center;
  }

  .btn-icon {
    width: 15px;
    height: 15px;
  }

  .contact-badge {
    padding: 0.625rem 1rem;
    font-size: 0.75rem;
  }

  .contact-badge .badge-icon {
    width: 14px;
    height: 14px;
  }

  .back-section {
    margin-bottom: 3rem;
  }

  .back-button {
    width: 100%;
    max-width: 100%;
    justify-content: center;
    padding: 0.75rem 1.25rem;
    font-size: 0.875rem;
  }

  .back-icon {
    width: 0.875rem;
    height: 0.875rem;
  }

}

@media (max-width: 380px) {
  .subscription-page {
    padding: 1rem 0.625rem;
  }

  .page-header h1 {
    font-size: 1.5rem;
  }

  .page-header p {
    font-size: 0.85rem;
  }

  .header-badge {
    padding: 0.375rem 0.75rem;
    font-size: 0.75rem;
  }

  .contact-content {
    padding: 1.25rem 1rem;
  }

  .contact-header h3 {
    font-size: 1.125rem;
  }

  .contact-header p {
    font-size: 0.8125rem;
  }

  .contact-btn {
    padding: 0.625rem 0.75rem;
    font-size: 0.75rem;
  }

  .btn-icon {
    width: 14px;
    height: 14px;
  }

  .back-button {
    padding: 0.625rem 1rem;
    font-size: 0.8125rem;
  }

}
</style>
