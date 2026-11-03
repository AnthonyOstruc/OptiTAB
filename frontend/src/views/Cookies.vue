<template>
  <LegalPage
    title="Politique de cookies"
    intro="Les cookies et traceurs utilisés sur OptiTAB, à quoi ils servent et comment gérer vos choix."
    updated="2 novembre 2026"
  >
    <template #essentiel>
      <ul>
        <li>Sans votre accord, seuls les éléments indispensables au fonctionnement du site sont utilisés.</li>
        <li>Les statistiques (Google Analytics, Microsoft Clarity) et la publicité (Meta Pixel) restent désactivées tant que vous ne les acceptez pas.</li>
        <li>Refuser est aussi simple qu’accepter, et vous pouvez changer d’avis à tout moment.</li>
      </ul>
    </template>

    <section id="definition">
      <h2>Qu’est-ce qu’un cookie&nbsp;?</h2>
      <p>
        Un cookie est un petit fichier enregistré sur votre ordinateur, tablette ou téléphone lorsque vous visitez un
        site. Il permet de mémoriser certaines informations, comme vos préférences, d’une page à l’autre ou d’une visite
        à l’autre. Les mêmes règles s’appliquent aux technologies voisines, comme le stockage local du navigateur.
      </p>
    </section>

    <section id="choix">
      <h2>Gérer vos choix</h2>
      <p>À votre première visite, un bandeau vous propose trois options :</p>
      <ul>
        <li><strong>Tout accepter :</strong> active les statistiques et la publicité.</li>
        <li><strong>Tout refuser :</strong> conserve uniquement les éléments indispensables.</li>
        <li><strong>Personnaliser :</strong> vous choisissez catégorie par catégorie.</li>
      </ul>
      <p>
        Les catégories facultatives sont désactivées par défaut. Vous pouvez modifier votre choix à tout moment avec le
        lien « Gérer mes cookies » en bas de chaque page, ou directement ici :
      </p>
      <div class="lg-button">
        <button type="button" class="vt-btn vt-btn--primary vt-btn--sm" @click="openPreferences">
          <AdjustmentsHorizontalIcon aria-hidden="true" />
          Gérer mes cookies
        </button>
      </div>
    </section>

    <section id="liste">
      <h2>Cookies et traceurs utilisés</h2>
      <div class="lg-table-wrap">
        <table class="lg-table lg-table--cards">
          <thead>
            <tr>
              <th scope="col">Nom</th>
              <th scope="col">Rôle</th>
              <th scope="col">Catégorie</th>
              <th scope="col">Durée</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">optitab_cookie_consent_v1</th>
              <td data-label="Rôle">Mémoriser votre choix de cookies</td>
              <td data-label="Catégorie"><span class="lg-tag">Indispensable</span></td>
              <td data-label="Durée">6 mois</td>
            </tr>
            <tr>
              <th scope="row">Jetons de connexion</th>
              <td data-label="Rôle">Vous garder connecté (stockage local du navigateur)</td>
              <td data-label="Catégorie"><span class="lg-tag">Indispensable</span></td>
              <td data-label="Durée">Jusqu’à la déconnexion</td>
            </tr>
            <tr>
              <th scope="row">Google Analytics 4 (_ga, _ga_*)</th>
              <td data-label="Rôle">Mesurer l’audience : pages vues, durée des visites, provenance</td>
              <td data-label="Catégorie"><span class="lg-tag lg-tag--vert">Statistiques</span></td>
              <td data-label="Durée">13 mois max.</td>
            </tr>
            <tr>
              <th scope="row">Microsoft Clarity (_clck, _clsk)</th>
              <td data-label="Rôle">Comprendre la navigation (parcours, zones cliquées)</td>
              <td data-label="Catégorie"><span class="lg-tag lg-tag--vert">Statistiques</span></td>
              <td data-label="Durée">De la session à 12 mois</td>
            </tr>
            <tr>
              <th scope="row">Meta Pixel (_fbp, _fbc)</th>
              <td data-label="Rôle">Mesurer et optimiser nos campagnes publicitaires</td>
              <td data-label="Catégorie"><span class="lg-tag lg-tag--orange">Publicité</span></td>
              <td data-label="Durée">Jusqu’à 90 jours</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p class="lg-note">
        Google Tag Manager sert uniquement à charger ces outils : il ne dépose pas de cookie lui-même et applique vos
        choix (mode « consentement » de Google, refusé par défaut).
      </p>
    </section>

    <section id="tiers">
      <h2>Services tiers</h2>
      <p>Les outils de mesure sont fournis par des sociétés tierces, qui appliquent leur propre politique :</p>
      <ul>
        <li><strong>Google Analytics :</strong> <a href="https://policies.google.com/privacy?hl=fr" target="_blank" rel="noopener noreferrer">politique de Google</a> · <a href="https://tools.google.com/dlpage/gaoptout?hl=fr" target="_blank" rel="noopener noreferrer">module de désactivation</a></li>
        <li><strong>Microsoft Clarity :</strong> <a href="https://privacy.microsoft.com/fr-fr/privacystatement" target="_blank" rel="noopener noreferrer">déclaration de confidentialité de Microsoft</a></li>
        <li><strong>Meta Pixel :</strong> <a href="https://www.facebook.com/privacy/policy/" target="_blank" rel="noopener noreferrer">politique de confidentialité de Meta</a></li>
      </ul>
      <p>
        Les liens vers nos réseaux sociaux (Instagram, TikTok, Facebook) sont de simples liens : aucun cookie de ces
        réseaux n’est déposé tant que vous ne cliquez pas dessus.
      </p>
    </section>

    <section id="navigateur">
      <h2>Réglages du navigateur</h2>
      <p>Vous pouvez aussi bloquer ou supprimer les cookies depuis votre navigateur :</p>
      <ul>
        <li><strong>Chrome :</strong> Paramètres › Confidentialité et sécurité › Cookies tiers</li>
        <li><strong>Firefox :</strong> Paramètres › Vie privée et sécurité › Cookies et données de sites</li>
        <li><strong>Safari :</strong> Réglages › Confidentialité › Gérer les données de sites web</li>
        <li><strong>Edge :</strong> Paramètres › Cookies et autorisations de site</li>
      </ul>
      <p>
        Refuser les cookies facultatifs n’empêche pas d’utiliser le site. Bloquer tous les cookies et le stockage local
        peut en revanche empêcher la connexion à votre compte.
      </p>
    </section>

    <section id="droits">
      <h2>Vos droits</h2>
      <p>
        Les données recueillies grâce aux cookies sont des données personnelles : vous disposez des droits décrits dans la
        <router-link to="/confidentialite">politique de confidentialité</router-link> (accès, effacement, opposition…),
        que vous pouvez exercer en écrivant à <a :href="`mailto:${legalInfo.email}`">{{ legalInfo.email }}</a>.
      </p>
    </section>
  </LegalPage>
</template>

<script setup>
import { AdjustmentsHorizontalIcon } from '@heroicons/vue/24/outline'
import LegalPage from '@/components/vitrine/LegalPage.vue'
import { legalInfo } from '@/config/legalInfo'

// Le bandeau (CookieConsent.vue) écoute cet événement pour rouvrir ses réglages.
const openPreferences = () => {
  window.dispatchEvent(new CustomEvent('open-cookie-preferences'))
}
</script>
