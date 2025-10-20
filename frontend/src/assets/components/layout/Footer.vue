<template>
  <footer class="footer">
    <div class="footer-support">
      <h2>Conseillers disponibles 7j/7 – Contactez-nous facilement</h2>
      <p>
        Notre équipe pédagogique est à votre écoute tous les jours, par WhatsApp ou e-mail.<br>
        Posez vos questions, demandez conseil et trouvez la formule qui vous convient : nous sommes là pour vous accompagner à chaque étape
      </p>
      <div class="footer-contacts">
        <a href="mailto:contact@optitab.net" class="footer-contact">
          <img src="/icons/envelope.svg" alt="Email" /> contact@optitab.net
        </a>
        <a href="https://wa.me/33764040251" target="_blank" rel="noopener" class="footer-contact">
          <img src="/icons/whatsapp.svg" alt="WhatsApp" /> 07 64 04 02 51
        </a>
      </div>
    </div>
    <div class="footer-legal-separator"></div>
    <div class="footer-legal-copyright">
      <span class="footer-legal-copyright-text">© {{ new Date().getFullYear() }} <strong class="footer-copyright-bold">OptiTAB</strong>. Tous droits réservés.</span>
      <span v-if="footerLinks.length" class="footer-legal-sep">|</span>
      <template v-for="(link, idx) in footerLinks" :key="link.label">
        <router-link v-if="link.href.startsWith('/')" :to="link.href" class="footer-legal-link">{{ link.label }}</router-link>
        <a v-else :href="link.href" class="footer-legal-link" target="_blank" rel="noopener">{{ link.label }}</a>
        <span v-if="idx < footerLinks.length - 1" class="footer-legal-sep">|</span>
      </template>
    </div>
  </footer>
</template>

<script setup>
import { footerLinks } from '@/config/footerContent.js';
// Footer compact et personnalisé, plus de props dynamiques nécessaires
</script>

<style scoped lang="scss">
.footer {
  background: #4e63c2;
  padding: 24px 0 0 0;
  margin-top: 0;
}
.footer-support {
  max-width: 700px;
  margin: 0 auto 1.5rem auto;
  color: #fff;
  text-align: left;
  padding: 0 1rem;
}
.footer-support h2 {
  font-size: 1.08rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-align: center;
}
.footer-support p {
  font-size: 0.92rem;
  margin-bottom: 1.1rem;
  color: #e0e6f7;
  line-height: 1.5;
  text-align: center;
}
.footer-contacts {
  display: flex;
  flex-direction: row;
  gap: 2.5rem;
  align-items: center;
  flex-wrap: wrap;
  margin-top: 0.5rem;
  justify-content: center;
}
.footer-contact {
  color: #fff;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 1.05rem;
  transition: color 0.2s;
}
.footer-contact img {
  width: 22px;
  height: 22px;
  filter: brightness(0) invert(1);
}
.footer-contact:hover {
  color: #c7d2fe;
}
.footer-legal-links {
  margin: 1.2rem auto 0 auto;
  text-align: center;
  width: 100%;
  display: flex;
  justify-content: center;
}
.footer-legal-links nav {
  width: 100%;
}
.footer-legal-links ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.5rem;
  width: 100%;
}
@media (max-width: 600px) {
  .footer-legal-links {
    margin: 0.5rem auto 0 auto;
  }
  .footer-legal-links ul {
    gap: 0.7rem;
  }
}
.footer-legal-li {
  display: flex;
  align-items: center;
}
.footer-legal-sep {
  margin: 0 0.3em;
  color: #bfc8e6;
  font-size: 1em;
  user-select: none;
}
.footer-legal-link {
  color: #e0e6f7;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
  font-size: 0.85rem;
  white-space: nowrap;
}
.footer-legal-link:hover {
  color: #fff;
  text-decoration: underline;
}
.footer-legal-copyright {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin: 1.2rem auto 0.7rem auto;
  font-size: 0.85rem;
  color: #e0e6f7;
  row-gap: 0.2rem;
}
.footer-legal-copyright-text {
  color: #e0e6f7;
  font-size: 0.85rem;
  font-weight: 500;
  white-space: nowrap;
}
.footer-legal-separator {
  width: 100%;
  max-width: 900px;
  margin: 1.2rem auto 0.7rem auto;
  border-top: 1.5px solid #bfc8e6;
  opacity: 0.7;
}
.footer-copyright-bold {
  font-weight: 700;
}
@media (max-width: 700px) {
  .footer-legal-copyright {
    gap: 0.2rem;
    font-size: 0.8rem;
  }
  .footer-legal-link, .footer-legal-copyright-text {
    font-size: 0.8rem;
  }
  .footer-legal-sep {
    margin: 0 0.15em;
  }
}
</style> 