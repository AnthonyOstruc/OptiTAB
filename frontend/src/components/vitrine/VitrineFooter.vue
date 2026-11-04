<template>
  <footer class="vt-footer">
    <div class="vt-footer__inner">
      <div class="vt-footer__top">
        <div class="vt-footer__brand">
          <img src="@/assets/logos/Logo_bg.png" alt="OptiTAB" class="vt-footer__logo" width="140" height="46" loading="lazy" />
          <p class="vt-footer__pitch">{{ vitrineFooter.accroche }}</p>

          <div class="vt-footer__contacts">
            <a
              :href="whatsappUrl"
              target="_blank"
              rel="noopener noreferrer"
              class="vt-footer__contact"
              data-cta-name="whatsapp"
              data-cta-location="footer"
            >
              <img src="/icons/whatsapp.svg" alt="" width="18" height="18" />
              {{ vitrineContact.whatsappAffiche }}
            </a>
            <a :href="`mailto:${vitrineContact.email}`" class="vt-footer__contact">
              <EnvelopeIcon class="vt-footer__contact-icon" />
              {{ vitrineContact.email }}
            </a>
          </div>
          <p class="vt-footer__hours">Réponse sous 24&nbsp;h, 7&nbsp;jours sur&nbsp;7</p>
        </div>

        <nav v-for="colonne in vitrineFooter.colonnes" :key="colonne.titre" class="vt-footer__col" :aria-label="colonne.titre">
          <p class="vt-footer__title">{{ colonne.titre }}</p>
          <router-link v-for="lien in colonne.liens" :key="lien.lien" :to="lien.lien" class="vt-footer__link">
            {{ lien.texte }}
          </router-link>
        </nav>

        <div class="vt-footer__news">
          <p class="vt-footer__title">Conseils et nouveautés</p>
          <p class="vt-footer__news-text">Méthodes de révision, nouveaux chapitres et offres, directement dans ta boîte mail.</p>
          <form v-if="newsState !== 'ok'" class="vt-footer__form" novalidate @submit.prevent="subscribe">
            <label for="vt-news-email" class="vt-sr-only">Ton adresse e-mail</label>
            <input
              id="vt-news-email"
              v-model.trim="newsEmail"
              type="email"
              inputmode="email"
              autocomplete="email"
              placeholder="ton@email.fr"
              class="vt-footer__input"
              :aria-invalid="newsState === 'invalid' ? 'true' : 'false'"
            />
            <button type="submit" class="vt-footer__submit" :disabled="newsState === 'loading'">
              {{ newsState === 'loading' ? '…' : 'S’inscrire' }}
            </button>
          </form>
          <p v-if="newsMessage" :class="['vt-footer__news-msg', `is-${newsState}`]" role="status">{{ newsMessage }}</p>
          <a :href="GOOGLE_REVIEWS_URL" target="_blank" rel="noopener noreferrer" class="vt-footer__google">
            <span class="vt-footer__stars" aria-hidden="true">★★★★★</span>
            <span><strong>5/5</strong> sur Google</span>
          </a>
        </div>
      </div>

      <div class="vt-footer__bottom">
        <p class="vt-footer__copy">© {{ year }} OptiTAB. Tous droits réservés.</p>
        <nav class="vt-footer__legal" aria-label="Informations légales">
          <router-link v-for="lien in vitrineFooter.legal" :key="lien.lien" :to="lien.lien">{{ lien.texte }}</router-link>
          <button type="button" @click="openCookiePreferences">Gérer mes cookies</button>
        </nav>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref, computed } from 'vue'
import { EnvelopeIcon } from '@heroicons/vue/24/outline'
import { subscribeToNewsletter } from '@/api/newsletter'
import { vitrineFooter, vitrineContact, GOOGLE_REVIEWS_URL } from '@/config/vitrineContent'

const year = new Date().getFullYear()
const newsEmail = ref('')
const newsState = ref('idle')
const newsMessage = ref('')

const whatsappUrl = computed(
  () => `https://wa.me/${vitrineContact.whatsapp}?text=${encodeURIComponent(vitrineContact.messageWhatsapp)}`
)

const subscribe = async () => {
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(newsEmail.value)) {
    newsState.value = 'invalid'
    newsMessage.value = 'Vérifie ton adresse e-mail.'
    return
  }
  newsState.value = 'loading'
  newsMessage.value = ''
  try {
    await subscribeToNewsletter(newsEmail.value)
    newsState.value = 'ok'
    newsMessage.value = 'C’est noté, à très vite dans ta boîte mail !'
  } catch (error) {
    newsState.value = 'error'
    newsMessage.value = 'L’inscription n’a pas abouti. Réessaie dans un instant.'
  }
}

const openCookiePreferences = () => {
  window.dispatchEvent(new CustomEvent('open-cookie-preferences'))
}
</script>

<style scoped>
.vt-footer {
  background: var(--vt-navy-900);
  color: rgba(255, 255, 255, 0.78);
  font-size: 15px;
}

.vt-footer__inner {
  max-width: var(--vt-max);
  margin: 0 auto;
  padding: 64px var(--vt-gutter) 28px;
}

.vt-footer__top {
  display: grid;
  grid-template-columns: minmax(0, 1.5fr) minmax(0, 0.8fr) minmax(0, 0.8fr) minmax(0, 1.3fr);
  gap: 40px;
}

.vt-footer__logo {
  width: 140px;
  height: auto;
  padding: 8px 12px;
  border-radius: 12px;
  background: #fff;
}

.vt-footer__pitch {
  max-width: 340px;
  margin: 18px 0 20px;
  line-height: 1.6;
}

.vt-footer__contacts {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.vt-footer__contact {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  width: fit-content;
  color: #fff;
  font-weight: 600;
  text-decoration: none;
}

.vt-footer__contact:hover {
  color: var(--vt-green-300);
}

.vt-footer__contact img {
  filter: brightness(0) invert(1);
}

.vt-footer__contact-icon {
  width: 18px;
  height: 18px;
}

.vt-footer__hours {
  margin: 10px 0 0;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
}

.vt-footer__col {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.vt-footer__title {
  margin: 0 0 4px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #fff;
}

.vt-footer__link {
  width: fit-content;
  color: rgba(255, 255, 255, 0.78);
  text-decoration: none;
}

.vt-footer__link:hover {
  color: #fff;
  text-decoration: underline;
  text-underline-offset: 3px;
}

.vt-footer__news-text {
  margin: 8px 0 14px;
  line-height: 1.55;
}

.vt-footer__form {
  display: flex;
  gap: 8px;
}

.vt-footer__input {
  flex: 1;
  min-width: 0;
  height: 46px;
  padding: 0 14px;
  border: 1px solid rgba(255, 255, 255, 0.22);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
  font: inherit;
  font-size: 15px;
}

.vt-footer__input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.vt-footer__input:focus {
  outline: 2px solid var(--vt-green-300);
  outline-offset: 1px;
}

.vt-footer__submit {
  height: 46px;
  padding: 0 18px;
  border: 0;
  border-radius: 10px;
  background: var(--vt-green);
  color: var(--vt-navy-900);
  font: inherit;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
}

.vt-footer__submit:hover {
  background: var(--vt-green-300);
}

.vt-footer__news-msg {
  margin: 10px 0 0;
  font-size: 14px;
}

.vt-footer__news-msg.is-ok {
  color: var(--vt-green-300);
  font-weight: 600;
}

.vt-footer__news-msg.is-invalid,
.vt-footer__news-msg.is-error {
  color: #ffb4a8;
}

.vt-footer__google {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  margin-top: 22px;
  padding: 8px 14px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 999px;
  color: #fff;
  font-size: 14px;
  text-decoration: none;
}

.vt-footer__google:hover {
  background: rgba(255, 255, 255, 0.08);
}

.vt-footer__stars {
  color: #fbbc05;
  letter-spacing: 1px;
}

.vt-footer__bottom {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px 24px;
  margin-top: 48px;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.12);
  font-size: 13px;
}

.vt-footer__copy {
  margin: 0;
  color: rgba(255, 255, 255, 0.6);
}

.vt-footer__legal {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 20px;
}

.vt-footer__legal a,
.vt-footer__legal button {
  padding: 0;
  border: 0;
  background: none;
  color: rgba(255, 255, 255, 0.72);
  font: inherit;
  text-decoration: none;
  cursor: pointer;
}

.vt-footer__legal a:hover,
.vt-footer__legal button:hover {
  color: #fff;
}

@media (max-width: 1024px) {
  .vt-footer__top {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .vt-footer__inner {
    padding-top: 48px;
    padding-bottom: calc(24px + env(safe-area-inset-bottom, 0px));
  }

  .vt-footer__top {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 36px 20px;
  }

  .vt-footer__brand,
  .vt-footer__news {
    grid-column: 1 / -1;
  }

  .vt-footer__bottom {
    flex-direction: column;
    align-items: flex-start;
    margin-top: 36px;
  }
}
</style>
