<template>
  <LegalPage
    title="Conditions générales de vente"
    intro="Les conditions applicables aux abonnements, aux pass et aux cours particuliers vendus sur OptiTAB."
    updated="2 novembre 2026"
  >
    <template #essentiel>
      <ul>
        <li>Chaque abonnement ou pass donne accès aux contenus d’un niveau, choisi lors de la commande.</li>
        <li>Les abonnements sont sans engagement et se résilient à tout moment depuis votre espace.</li>
        <li>Les pass sont des paiements uniques, sans renouvellement.</li>
        <li>Le paiement est sécurisé par Stripe, et une facture vous est envoyée par e-mail.</li>
      </ul>
    </template>

    <section id="objet">
      <h2>Objet</h2>
      <p>
        Les présentes conditions générales de vente (CGV) régissent les ventes conclues sur le site
        {{ legalInfo.site }} entre l’éditeur d’{{ legalInfo.marque }}, présenté dans les
        <router-link to="/legal">mentions légales</router-link>, et ses clients :
      </p>
      <ul>
        <li>les abonnements et pass d’accès à la plateforme ;</li>
        <li>les formules avec accompagnement par un professeur ;</li>
        <li>les cours particuliers en ligne.</li>
      </ul>
      <p>Toute commande vaut acceptation pleine et entière des présentes CGV.</p>
    </section>

    <section id="services">
      <h2>Ce que comprend l’accès</h2>
      <ul>
        <li>Les cours, fiches de synthèse, exercices corrigés pas à pas et quiz du niveau choisi.</li>
        <li>Le suivi de progression et les outils de calcul.</li>
        <li>Pour les formules avec accompagnement, les services décrits sur la <router-link to="/tarifs">page Tarifs</router-link> (questions à un professeur, séances particulières…).</li>
      </ul>
      <p class="lg-note">
        Chaque abonnement ou pass débloque <strong>un seul niveau</strong>, choisi au moment de la commande. Pour
        accéder à un autre niveau, une souscription distincte est nécessaire.
      </p>
      <p>
        Le service est accessible 24&nbsp;h/24, sous réserve des opérations de maintenance et des cas de force majeure,
        sans garantie de disponibilité continue.
      </p>
    </section>

    <section id="tarifs">
      <h2>Offres et tarifs</h2>
      <p>
        Les offres en vigueur sont présentées sur la <router-link to="/tarifs">page Tarifs</router-link>. Le prix
        applicable est celui affiché au moment de la commande ; il est indiqué en euros, toutes taxes comprises.
      </p>

      <div aria-live="polite">
        <p v-if="plansLoading" class="lg-note">Chargement des tarifs…</p>
        <p v-else-if="plansError || !displayPlans.length" class="lg-note">
          Les tarifs ne peuvent pas être affichés pour le moment. Ils restent consultables sur la
          <router-link to="/tarifs">page Tarifs</router-link>.
        </p>
        <div v-else class="lg-table-wrap">
          <table class="lg-table lg-table--cards">
            <thead>
              <tr>
                <th scope="col">Offre</th>
                <th scope="col">Type</th>
                <th scope="col">Durée</th>
                <th scope="col">Prix</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(plan, idx) in displayPlans" :key="planKey(plan, idx)">
                <th scope="row">{{ plan.name || 'Offre' }}</th>
                <td data-label="Type">
                  <span :class="['lg-tag', { 'lg-tag--vert': plan.mode !== 'subscription' }]">
                    {{ plan.mode === 'subscription' ? 'Abonnement' : 'Pass' }}
                  </span>
                </td>
                <td data-label="Durée">{{ humanPlanPeriod(plan) }}</td>
                <td data-label="Prix"><strong>{{ formatEur(plan.price) }}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section id="commande">
      <h2>Commande et paiement</h2>
      <ul>
        <li>Le paiement s’effectue en ligne par carte bancaire, de manière sécurisée, via notre prestataire Stripe. Nous n’avons jamais accès à vos données de carte.</li>
        <li>Si vous commandez sans être connecté, votre compte est créé automatiquement avec l’adresse e-mail saisie lors du paiement.</li>
        <li>L’accès est ouvert dès la confirmation du paiement, et une facture vous est envoyée par e-mail.</li>
        <li>Pour un abonnement, le montant est prélevé à chaque échéance jusqu’à la résiliation.</li>
      </ul>
    </section>

    <section id="duree">
      <h2>Durée, renouvellement et résiliation</h2>
      <h3>Abonnements</h3>
      <ul>
        <li>L’abonnement est souscrit pour la période choisie (par exemple la semaine ou le mois) et se renouvelle automatiquement à chaque échéance.</li>
        <li>Il est sans engagement : vous pouvez le résilier à tout moment depuis votre espace, rubrique Abonnement.</li>
        <li>La résiliation arrête le renouvellement ; l’accès reste ouvert jusqu’à la fin de la période déjà payée.</li>
        <li>Pour ne pas être facturé de la période suivante, la résiliation doit intervenir avant la date de renouvellement indiquée dans votre espace.</li>
      </ul>
      <h3>Pass</h3>
      <ul>
        <li>Le pass est un paiement unique qui ouvre l’accès pour la durée indiquée lors de l’achat (24&nbsp;heures, un an…).</li>
        <li>Il prend fin automatiquement, sans renouvellement ni prélèvement ultérieur.</li>
      </ul>
    </section>

    <section id="retractation">
      <h2>Droit de rétractation et remboursement</h2>
      <p>
        Conformément à l’article L.221-28 du Code de la consommation, le droit de rétractation ne s’applique pas à la
        fourniture d’un contenu numérique dont l’exécution a commencé, avec votre accord préalable exprès, avant la fin
        du délai de rétractation, et pour lequel vous avez renoncé expressément à ce droit.
      </p>
      <p>
        À défaut, vous disposez d’un délai de 14&nbsp;jours à compter de la souscription pour vous rétracter, en nous
        écrivant à <a :href="`mailto:${legalInfo.email}`">{{ legalInfo.email }}</a>.
      </p>
      <p>
        En dehors de ce cas et sauf disposition légale contraire, une période commencée n’est pas remboursée, ni en
        totalité ni au prorata. Les sommes restées impayées (échéance rejetée, contestation bancaire) restent dues.
      </p>
    </section>

    <section id="cours-particuliers">
      <h2>Cours particuliers</h2>
      <ul>
        <li>Le tarif et les modalités d’une séance (date, durée, niveau) sont convenus avec le professeur avant la séance.</li>
        <li>Le règlement s’effectue en ligne par carte bancaire, via un lien de paiement sécurisé Stripe ; un reçu est envoyé par e-mail.</li>
        <li>Les conditions de report ou d’annulation d’une séance sont précisées lors de sa réservation.</li>
      </ul>
    </section>

    <section id="compte">
      <h2>Compte et usage personnel</h2>
      <p>
        L’accès est strictement personnel. Le partage ou la revente d’un compte est interdit et peut entraîner sa
        suspension, sans remboursement de la période en cours. Les règles complètes figurent dans les
        <router-link to="/cgu">conditions générales d’utilisation</router-link>.
      </p>
    </section>

    <section id="propriete">
      <h2>Propriété intellectuelle</h2>
      <p>
        Les contenus restent la propriété exclusive d’{{ legalInfo.marque }}. L’achat d’un accès confère un droit
        d’utilisation personnel, non exclusif et non transférable, pour un usage scolaire et non commercial. Toute
        reproduction ou diffusion sans autorisation écrite est interdite.
      </p>
    </section>

    <section id="responsabilite">
      <h2>Responsabilité</h2>
      <ul>
        <li>{{ legalInfo.marque }} s’engage à fournir un service conforme à sa description et à protéger vos données personnelles.</li>
        <li>Les contenus sont un support d’apprentissage : ils ne garantissent pas la réussite à un contrôle, un examen ou un concours.</li>
        <li>{{ legalInfo.marque }} n’est pas responsable des interruptions dues à un cas de force majeure ou à une panne extérieure.</li>
      </ul>
    </section>

    <section id="donnees">
      <h2>Données personnelles</h2>
      <p>
        Les données nécessaires à la commande sont traitées conformément à la
        <router-link to="/confidentialite">politique de confidentialité</router-link>. Vous pouvez exercer vos droits
        (accès, rectification, suppression…) à <a :href="`mailto:${legalInfo.email}`">{{ legalInfo.email }}</a>.
      </p>
    </section>

    <section id="evolution">
      <h2>Évolution des offres et des CGV</h2>
      <p>
        {{ legalInfo.marque }} peut faire évoluer ses offres, ses tarifs et les présentes CGV. Les conditions applicables
        sont celles en vigueur à la date de la commande. Toute modification substantielle est communiquée aux abonnés
        dans un délai raisonnable, et chacun reste libre de résilier.
      </p>
      <p>
        Les enregistrements conservés dans nos systèmes et ceux de Stripe font foi des commandes, paiements et échanges
        intervenus.
      </p>
    </section>

    <section id="litiges">
      <h2>Droit applicable et médiation</h2>
      <p>
        Les présentes CGV sont régies par le droit français. En cas de difficulté, contactez-nous d’abord : nous
        recherchons toujours une solution amiable.
      </p>
      <p v-if="legalInfo.mediateur.nom">
        Conformément à l’article L.612-1 du Code de la consommation, vous pouvez recourir gratuitement au médiateur de
        la consommation <strong>{{ legalInfo.mediateur.nom }}</strong>
        <template v-if="legalInfo.mediateur.site">
          (<a :href="legalInfo.mediateur.site" target="_blank" rel="noopener noreferrer">{{ legalInfo.mediateur.site.replace('https://', '') }}</a>)
        </template>.
      </p>
      <p v-else>
        Conformément à l’article L.612-1 du Code de la consommation, vous pouvez recourir gratuitement à un médiateur de
        la consommation en vue d’une résolution amiable ; ses coordonnées vous sont communiquées sur simple demande.
      </p>
      <p>À défaut d’accord, le litige est porté devant les juridictions compétentes.</p>
    </section>
  </LegalPage>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import LegalPage from '@/components/vitrine/LegalPage.vue'
import { legalInfo } from '@/config/legalInfo'
import { getPlans } from '@/api/subscriptions'

// Tarifs lus en direct : le tableau suit les offres configurées dans l'admin.
const plans = ref([])
const plansLoading = ref(true)
const plansError = ref(false)

const displayPlans = computed(() =>
  (Array.isArray(plans.value) ? plans.value : [])
    .filter((plan) => plan && typeof plan === 'object')
    .slice()
    .sort((a, b) => Number(a?.price || 0) - Number(b?.price || 0))
)

const planKey = (plan, idx) => String(plan?.stripe_price_id || plan?.id || plan?.name || idx)

const humanPlanPeriod = (plan) => {
  const mode = String(plan?.mode || '').toLowerCase()
  const billingPeriod = String(plan?.billing_period || '').toLowerCase()
  const accessDays = Number(plan?.access_days || 0)

  if (mode === 'one_time') {
    if (accessDays === 1) return '24 heures, paiement unique'
    if (accessDays >= 365) return '1 an, paiement unique'
    if (accessDays > 0) return `${accessDays} jours, paiement unique`
    return 'Paiement unique'
  }

  if (billingPeriod === 'weekly') return 'Renouvelé chaque semaine'
  if (billingPeriod === 'monthly') return 'Renouvelé chaque mois'
  if (billingPeriod === 'yearly' || billingPeriod === 'annual') return 'Renouvelé chaque année'
  return 'Renouvellement périodique'
}

const formatEur = (value) => {
  const amount = Number(value)
  if (!Number.isFinite(amount)) return ''
  return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(amount)
}

onMounted(async () => {
  try {
    const { data } = await getPlans()
    plans.value = Array.isArray(data?.plans) ? data.plans : []
  } catch (error) {
    console.error('Erreur chargement plans (CGV):', error)
    plansError.value = true
  } finally {
    plansLoading.value = false
  }
})
</script>
