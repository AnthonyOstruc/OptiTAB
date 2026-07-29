/**
 * Adresse publique de la page "lien en bio".
 * Centralisée ici pour que le studio d'administration et la page elle-même
 * ne puissent pas diverger si l'URL change un jour.
 */
export const BIO_LANDING_PATH = '/avis'

/**
 * OptiTAB — Contenu de la page "lien en bio"
 *
 * C'est LE seul fichier à modifier pour faire vivre la page.
 * La vue (`@/views/BioLanding.vue`) ne fait qu'afficher ce qui est ici.
 *
 * RÈGLE DE TON : la page s'adresse aussi bien à un élève qu'à un parent.
 * On évite donc « votre enfant » comme « ta classe ». On parle de la
 * situation, pas de la personne. En cas de doute, l'infinitif règle tout :
 * « Comprendre la méthode » plutôt que « Tu comprends la méthode ».
 *
 * TÉMOIGNAGES : voir la section dédiée plus bas. On n'affiche que de
 * vraies captures d'écran, jamais de conversation reconstituée.
 */

// ============================================================
// Contact
// ============================================================

export const CONTACT = {
  whatsappPhone: '33764040251',
  whatsappDisplay: '07 64 04 02 51',
  whatsappMessage: "Bonjour, j'aimerais des informations sur OptiTAB."
}

/**
 * Construit un lien wa.me avec un message pré-rempli.
 * @param {string} message
 */
export function buildWhatsappUrl(message = CONTACT.whatsappMessage) {
  const phone = String(CONTACT.whatsappPhone).replace(/[^0-9]/g, '')
  const text = String(message || '').trim()
  return text
    ? `https://wa.me/${phone}?text=${encodeURIComponent(text)}`
    : `https://wa.me/${phone}`
}

// ============================================================
// Provenance (utm_source) — personnalise le petit badge du hero
// ============================================================

export const SOURCE_LABELS = {
  instagram: 'Instagram',
  facebook: 'Facebook',
  tiktok: 'TikTok',
  youtube: 'YouTube',
  snapchat: 'Snapchat',
  linkedin: 'LinkedIn'
}

export const SOCIAL_LINKS = [
  { name: 'Instagram', handle: '@opti.tab', href: 'https://instagram.com/opti.tab' },
  { name: 'TikTok', handle: '@optitab', href: 'https://tiktok.com/@optitab' },
  { name: 'Facebook', handle: 'OptiTAB', href: 'https://facebook.com/optitab' }
]

// ============================================================
// Hero
// ============================================================

export const HERO = {
  kicker: 'OptiTAB — Maths, du collège à la prépa',
  title: 'Progresser en maths, avec méthode',
  subtitle:
    'Cours clairs, fiches de synthèse et exercices corrigés pas à pas. Élève ou parent, une question suffit pour commencer.',
  primaryCta: 'Écrire sur WhatsApp',
  secondaryCta: 'Voir les témoignages',
  // Ligne de réassurance sous le bouton. Affichée en texte léger, séparée
  // par des points médians. Garder 3 items courts : au-delà, ça se casse
  // sur deux lignes en mobile et l'effet « épuré » disparaît.
  trustLine: ['Dès 4,99 €/mois', 'Sans engagement', 'Réponse 7j/7']
}

/**
 * Bande de chiffres sous le hero.
 *
 * ⚠️ Ces chiffres sont des allégations commerciales : ils doivent être
 * exacts et justifiables (art. L.121-2 du Code de la consommation).
 * Au 29/07/2026, la base compte 74 élèves inscrits sur la plateforme.
 * Si tu as accompagné d'autres élèves en cours particuliers sans compte,
 * ajuste `ELEVES_ACCOMPAGNES` en conséquence — mais garde de quoi le prouver.
 */
const ELEVES_ACCOMPAGNES = '+70'

export const STATS = [
  { value: ELEVES_ACCOMPAGNES, label: 'élèves accompagnés' },
  { value: '+150', label: 'chapitres' },
  { value: '+1000', label: 'exercices corrigés' },
  // Libellé vide : « Collège → prépa » se suffit et tient sur une ligne,
  // là où « 6e → prépa tous les niveaux » débordait sur deux.
  { value: 'Collège → prépa', label: '' }
]

// ============================================================
// Témoignages : tes vraies captures WhatsApp & SMS
// ============================================================

/**
 * On n'affiche QUE de vraies captures d'écran. Pas de conversation
 * reconstituée : un faux chat se repère immédiatement et détruit
 * la confiance qu'on cherche justement à construire.
 *
 * ------------------------------------------------------------
 * AJOUTER UNE CAPTURE — 3 étapes
 * ------------------------------------------------------------
 * 1. Demande l'accord de la personne (et garde une trace du message).
 * 2. Anonymise la capture : numéro de téléphone, photo de profil,
 *    nom complet, nom de l'établissement. Puis dépose le fichier dans
 *    `frontend/public/images/temoignages/`.
 * 3. Ajoute une entrée ci-dessous.
 *
 * Format :
 * {
 *   id:      identifiant unique
 *   channel: 'whatsapp' | 'sms'
 *   author:  profil, sans aucun nom ni prénom — ex. "Maman d'élève"
 *   role:    niveau, ex. 'Terminale', 'Prépa MPSI'
 *   src:     chemin de la capture, ex. '/images/temoignages/sandra.png'
 *   alt:     description pour l'accessibilité et le référencement
 *   featured: (optionnel) true => cette capture s'affiche aussi dans le hero.
 *             Mets-le sur une seule entrée, la plus parlante.
 * }
 *
 * Tant que ce tableau est vide, la section est masquée en production
 * et un guide s'affiche en développement.
 */
export const TESTIMONIALS = [
  // Exemple — décommente et adapte une fois ta première capture déposée :
  //
  // {
  //   id: 'terminale-1',
  //   channel: 'whatsapp',
  //   author: "Maman d'élève",
  //   role: 'Terminale',
  //   src: '/images/temoignages/whatsapp-terminale-1.png',
  //   alt: "Message WhatsApp d'une maman : sa fille est passée de 8 à 14 de moyenne",
  //   featured: true
  // },
]

export const TESTIMONIALS_SECTION = {
  title: 'Ce qu\'ils nous écrivent',
  // Volontairement sans sous-titre : le titre et les badges WhatsApp / SMS
  // des cartes suffisent. L'ancienne phrase affirmait « publiées avec accord »,
  // ce qui n'est plus garanti depuis que la case d'accord ne bloque plus la
  // publication — mieux vaut ne rien dire que d'affirmer l'inexact.
  subtitle: ''
}

// ============================================================
// Ce que comprend l'accompagnement
// ============================================================

export const VALUE_SECTION = {
  title: 'Ce que vous trouverez sur OptiTAB',
  subtitle: 'Une plateforme complète, et quelqu\'un pour répondre quand ça bloque.'
}

export const VALUE_PROPS = [
  {
    icon: 'book',
    title: 'Des cours clairs',
    text: 'Chaque notion expliquée simplement, avec des exemples concrets.'
  },
  {
    icon: 'sheet',
    title: 'Des fiches de synthèse',
    text: "L'essentiel d'un chapitre sur une page : formules, méthodes, pièges à éviter."
  },
  {
    icon: 'steps',
    title: 'Des exercices pas à pas',
    text: 'Chaque étape détaillée pour comprendre la méthode, puis refaire seul.'
  },
  {
    icon: 'chat',
    title: 'Une réponse quand ça bloque',
    text: 'Une question, un doute ? On répond par message, 7j/7.'
  }
]

// ============================================================
// Comment ça se passe
// ============================================================

export const STEPS_SECTION = {
  title: 'Comment ça se passe',
  subtitle: 'Trois étapes, et la première prend 30 secondes.'
}

export const STEPS = [
  {
    number: '1',
    title: 'Vous écrivez',
    text: 'Un message WhatsApp. Élève ou parent, vous décrivez la situation en quelques mots.'
  },
  {
    number: '2',
    title: 'On identifie le blocage',
    text: 'Lacunes de base, méthode ou organisation : on cible ce qui coince vraiment.'
  },
  {
    number: '3',
    title: 'On avance à votre rythme',
    text: 'Accès à la plateforme, un plan clair, et un suivi pour ne pas décrocher en route.'
  }
]

// ============================================================
// Réassurance
// ============================================================

export const GUARANTEES = [
  'Sans engagement, annulable à tout moment',
  'Programme aligné sur l\'Éducation nationale',
  'Du collège à la prépa (Brevet, Bac, MPSI, PCSI, BTS)',
  'Ressources gratuites accessibles sans carte bancaire'
]

export const PRICING_TEASER = {
  title: 'Un accompagnement accessible',
  price: '4,99 €',
  priceSuffix: '/ mois',
  note: 'Sans engagement · Annulable à tout moment · Accès immédiat',
  cta: 'Voir les tarifs en détail'
}

// ============================================================
// FAQ — les objections réelles, côté élève comme côté parent
// ============================================================

export const FAQ_SECTION = {
  titlePrefix: 'Les questions',
  titleHighlight: 'fréquentes',
  description: 'Ce qu\'on nous demande le plus souvent avant de commencer.'
}

export const FAQ = [
  {
    question: 'En cas de grosses lacunes, est-ce que ça peut vraiment marcher ?',
    answer:
      "Oui, et c'est le cas le plus fréquent. Le parcours Bases & Méthode reprend les fondamentaux à un rythme progressif, sans sauter d'étapes. On commence toujours par identifier d'où vient le blocage avant de proposer quoi que ce soit."
  },
  {
    question: 'Faut-il être aidé par un adulte pour suivre ?',
    answer:
      "Non. Les cours et les corrigés sont pensés pour être suivis en autonomie. Un parent peut suivre la progression sans avoir à expliquer lui-même, même s'il n'a pas fait de maths depuis longtemps."
  },
  {
    question: 'Combien ça coûte, et y a-t-il un engagement ?',
    answer:
      "L'abonnement démarre à 4,99 € par mois, sans engagement et annulable à tout moment depuis l'espace personnel. Une partie des cours et exercices est aussi accessible gratuitement, sans carte bancaire."
  },
  {
    question: 'Quels niveaux sont couverts ?',
    answer:
      'Du collège (6e à 3e, Brevet) au lycée (Seconde, Première, Terminale, Bac), jusqu\'au supérieur (BTS, prépa MPSI, MP2I, PCSI). Le parcours Bases & Méthode est disponible à tous les niveaux.'
  },
  {
    question: 'Comment vous contacter avant de se décider ?',
    answer:
      "Par WhatsApp, c'est le plus rapide : vous décrivez la situation, on répond avec un premier avis honnête. Si OptiTAB n'est pas adapté, on le dira."
  }
]

// ============================================================
// CTA final
// ============================================================

export const FINAL_CTA = {
  title: 'Une question ? Écrivez-nous',
  text: 'Décrivez la situation en quelques mots, que vous soyez élève ou parent. On répond avec un premier avis clair, sans engagement.',
  cta: 'Écrire sur WhatsApp',
  hint: CONTACT.whatsappDisplay
}
