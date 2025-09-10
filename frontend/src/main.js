import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { useSubjectsStore } from '@/stores/subjects/index'

import 'katex/dist/katex.min.css'
import 'mathlive'
import '@/styles/global.css'

// Supprimer les icônes MathLive globalement
if (typeof document !== 'undefined') {
  const style = document.createElement('style');
  style.textContent = `
    /* Cache le bouton menu (≡) et le toggle clavier virtuel */
    math-field::part(menu-toggle),
    math-field::part(virtual-keyboard-toggle) {
      display: none !important;
    }
  `;
  document.head.appendChild(style);
}


const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.use(router)

// Récupère l'utilisateur via l'API si un token est présent
const userStore = useUserStore()

// Nettoyer automatiquement les tokens expirés avant de tenter la récupération
import apiClient, { apiUtils } from '@/api/client'
const tokensCleaned = apiUtils.cleanExpiredTokens()
const hasValidToken = localStorage.getItem('access_token')

// Désactiver les logs en production (laissé actif en local)
if (import.meta && import.meta.env && import.meta.env.PROD) {
  const noop = () => {}
  console.log = noop
  console.debug = noop
  console.info = noop
  console.warn = noop
}

// Ces logs sont utiles en dev mais désactivés en prod par le bloc ci-dessus
if (tokensCleaned) {
  console.log('Tokens expirés nettoyés au démarrage de l\'application')
}

if (hasValidToken) {
  console.log('Tentative de récupération du profil utilisateur...')
  userStore.fetchUser()

  // Démarrer la surveillance automatique des tokens après la récupération de l'utilisateur
  setTimeout(() => {
    console.log('Démarrage de la surveillance automatique des tokens...')
    apiUtils.startTokenMonitoring()
  }, 1000) // Petit délai pour laisser le temps à fetchUser de s'exécuter
} else if (tokensCleaned) {
  console.log('Aucun token valide trouvé après nettoyage')
}

// NOTE: L'initialisation du store des matières est maintenant gérée dans App.vue
// après que l'utilisateur ait configuré son pays/niveau pour éviter les erreurs API

// Rien à ajouter ici pour MathJax : vue-mathjax-next gère tout automatiquement via import dans les composants.
// Si besoin d'un usage global, on pourrait faire :
// import MathJax from 'vue-mathjax-next'
// app.use(MathJax)
// Mais pour l'instant, l'import local dans ExerciceQCM.vue suffit.

app.mount('#app')
