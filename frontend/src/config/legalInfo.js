// Identité légale d'OptiTAB, reprise par les pages Mentions légales, CGV, CGU,
// Confidentialité et Cookies.
//
// À COMPLÉTER : les champs vides ne sont pas affichés. La loi (LCEN, art. 6 III)
// impose pourtant d'afficher la raison sociale, la forme juridique, l'adresse du
// siège, le numéro SIREN/RCS et un numéro de téléphone de l'éditeur, ainsi que
// le médiateur de la consommation choisi (Code de la consommation, L.616-1).

export const legalInfo = {
  marque: 'OptiTAB',
  site: 'www.optitab.net',

  editeur: {
    raisonSociale: '', // nom de la société éditrice
    formeJuridique: '', // ex. « SAS au capital de 1 000 € » ou « Entreprise individuelle »
    adresse: '', // adresse du siège
    siren: '', // ex. « 123 456 789 RCS Angers »
    tva: '', // numéro de TVA intracommunautaire, s'il existe
    telephone: '' // numéro affiché au public
  },

  directeurPublication: 'Anthony Tabet',
  linkedin: 'https://www.linkedin.com/in/anthony-tabet-a34aa6192/',
  email: 'contact@optitab.net',
  whatsapp: '33764040251',
  whatsappAffiche: '07 64 04 02 51',

  hebergeurs: [
    {
      role: 'Site, serveur et base de données',
      nom: 'Render Services, Inc.',
      adresse: '995 Market St, San Francisco, CA 94103, États-Unis',
      site: 'https://render.com'
    },
    {
      role: 'Images et documents des cours (serveurs à Paris)',
      nom: 'Amazon Web Services EMEA SARL',
      adresse: '38 avenue John F. Kennedy, L-1855 Luxembourg',
      site: 'https://aws.amazon.com'
    }
  ],

  // Médiateur de la consommation : nom + site, à renseigner dès l'adhésion.
  mediateur: { nom: '', site: '' },

  juridiction: 'Angers'
}

// Les cinq documents, dans l'ordre du pied de page.
export const legalDocs = [
  { lien: '/legal', court: 'Mentions légales' },
  { lien: '/confidentialite', court: 'Confidentialité' },
  { lien: '/cookies', court: 'Cookies' },
  { lien: '/cgu', court: 'CGU' },
  { lien: '/cgv', court: 'CGV' }
]
