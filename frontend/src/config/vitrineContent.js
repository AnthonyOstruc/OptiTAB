// Contenu de la nouvelle vitrine (pages hors connexion).
// Tous les textes sont ici : les composants ne font que les mettre en page.
// Les chiffres sont ceux de la base au 2026-11-02 (211 chapitres, 3 358 exercices).

export const vitrineStats = [
  { valeur: '211', libelle: 'chapitres complets', detail: 'cours + fiche de synthèse' },
  { valeur: '3 300+', libelle: 'exercices corrigés', detail: 'expliqués étape par étape' },
  { valeur: '10', libelle: 'classes couvertes', detail: 'du CE2 à la Terminale' },
  { valeur: '5/5', libelle: 'sur Google', detail: 'avis d’élèves et de parents' }
]

export const vitrineHero = {
  eyebrow: 'Cours de maths en ligne · du CE2 à la Terminale',
  titre: 'Les maths, enfin',
  titreAccent: 'claires.',
  sousTitre:
    'Pour chaque chapitre du programme : un cours limpide, une fiche de synthèse et des exercices corrigés pas à pas. Tu avances à ton rythme, et tu sais toujours quoi faire ensuite.',
  ctaPrincipal: 'Créer mon compte gratuit',
  ctaSecondaire: 'Essayer sans inscription',
  rassurance: ['Sans carte bancaire', 'Sans engagement', 'Ordinateur, tablette et mobile']
}

// Les trois portes d'entrée : chacun sait tout de suite où cliquer.
export const vitrineParcours = [
  {
    cle: 'gratuit',
    etiquette: 'Je découvre',
    titre: 'Essayer gratuitement',
    texte:
      'Une partie des cours, fiches et exercices corrigés en accès libre. Aucune inscription, aucune carte bancaire.',
    points: ['Tous les niveaux, du CE2 à la Terminale', 'Accès immédiat'],
    cta: 'Voir les ressources gratuites',
    lien: '/ressources-gratuites',
    ton: 'green'
  },
  {
    cle: 'plateforme',
    etiquette: 'Je révise sérieusement',
    titre: 'Débloquer toute la plateforme',
    texte:
      'Tous les chapitres de ta classe, tous les exercices corrigés pas à pas et le suivi de ta progression.',
    points: ['Dès 3,99 €, sans engagement', 'Un chapitre complet offert à l’inscription'],
    cta: 'Voir les formules',
    ancre: 'tarifs',
    ton: 'navy',
    miseEnAvant: true
  },
  {
    cle: 'prof',
    etiquette: 'J’ai besoin d’un prof',
    titre: 'Prendre des cours particuliers',
    texte:
      'Des séances en ligne en maths, physique-chimie et informatique, du collège à la prépa, avec un professeur expérimenté.',
    points: ['Préparation brevet, bac et concours', 'Réponse sous 24 h'],
    cta: 'Découvrir les cours particuliers',
    lien: '/cours-particuliers',
    ton: 'orange'
  }
]

// `niveau` doit correspondre exactement au niveau_nom des ressources gratuites.
export const vitrineClasses = [
  {
    cycle: 'Primaire',
    classes: [
      { niveau: 'CE2', libelle: 'CE2', chapitres: 36 },
      { niveau: 'CM1', libelle: 'CM1', chapitres: 21 },
      { niveau: 'CM2', libelle: 'CM2', chapitres: 21 }
    ]
  },
  {
    cycle: 'Collège',
    classes: [
      { niveau: '6ème', libelle: '6e', chapitres: 26 },
      { niveau: '5ème', libelle: '5e', chapitres: 20 },
      { niveau: '4ème', libelle: '4e', chapitres: 18 },
      { niveau: '3ème', libelle: '3e', chapitres: 19, note: 'Brevet' }
    ]
  },
  {
    cycle: 'Lycée',
    classes: [
      { niveau: '2nde', libelle: 'Seconde', chapitres: 14 },
      { niveau: '1ère', libelle: 'Première', chapitres: 12, note: 'Spécialité' },
      { niveau: 'Terminale', libelle: 'Terminale', chapitres: 24, note: 'Bac' }
    ]
  }
]

// « Un chapitre OptiTAB, c'est… » : la méthode en quatre temps.
export const vitrineMethode = [
  {
    numero: '1',
    titre: 'Le cours',
    texte: 'L’essentiel du chapitre, expliqué simplement, avec des exemples et des figures soignées.',
    icone: 'cours'
  },
  {
    numero: '2',
    titre: 'La fiche de synthèse',
    texte: 'Les définitions, propriétés et méthodes à retenir, réunies sur une seule page.',
    icone: 'fiche'
  },
  {
    numero: '3',
    titre: 'Les exercices corrigés',
    texte: 'Du premier exercice d’application au sujet type contrôle, chaque correction est détaillée étape par étape.',
    icone: 'exercices'
  },
  {
    numero: '4',
    titre: 'La progression',
    texte: 'Tu vois ce qui est acquis, ce qui reste à revoir, et tu gagnes de l’XP à chaque exercice réussi.',
    icone: 'progression'
  }
]

export const vitrineFormules = [
  {
    titre: 'Sans inscription',
    prix: 'Gratuit',
    texte: 'Une partie des cours, fiches et exercices en libre accès.'
  },
  {
    titre: 'Compte gratuit',
    prix: 'Gratuit',
    texte: 'Un chapitre complet débloqué pour tester la méthode.'
  },
  {
    titre: 'Abonnement',
    prix: 'Dès 3,99 €',
    texte: 'Toute ta classe, tous les corrigés et le suivi de progression.',
    miseEnAvant: true
  }
]

export const vitrineProf = {
  etiquette: 'Cours particuliers en ligne',
  titre: 'Un vrai prof, quand tu en as besoin',
  texte:
    'OptiTAB a été créé par Anthony, ingénieur diplômé de l’ISAE-SUPAERO et professeur depuis plus de 15 ans. Il accompagne lui‑même les élèves en cours particuliers, du collège à la prépa.',
  points: [
    'Maths, physique-chimie et informatique',
    'Préparation au brevet, au bac et aux concours',
    'Séances en ligne, horaires adaptés à ton emploi du temps'
  ],
  cta: 'Découvrir les cours particuliers',
  ctaSecondaire: 'Poser une question',
  photo: '/images/professeurs/anthony.jpg',
  photoAlt: 'Anthony, fondateur d’OptiTAB et professeur de mathématiques'
}

export const vitrineFaq = [
  {
    question: 'Qu’est-ce que je trouve sur OptiTAB ?',
    answer:
      'Pour chaque chapitre du programme de maths, du CE2 à la Terminale : un cours, une fiche de synthèse et des exercices corrigés pas à pas. Tu as aussi un tableau de bord pour suivre ta progression et des outils de calcul.'
  },
  {
    question: 'Est-ce que je peux essayer gratuitement ?',
    answer:
      'Oui, de deux façons. Sans inscription, une partie des cours, fiches et exercices est en libre accès dans les ressources gratuites. Avec un compte gratuit, tu débloques en plus un chapitre complet pour tester la méthode. Aucune carte bancaire n’est demandée.'
  },
  {
    question: 'Quelle formule choisir ?',
    answer:
      'Le pass 24 h dépanne avant un contrôle. L’abonnement hebdomadaire convient pour réviser quelques jours. Le mensuel est le plus avantageux dès que tu travailles plus de deux semaines. La formule Accompagné ajoute des questions illimitées à un professeur par WhatsApp ou e‑mail.'
  },
  {
    question: 'Puis-je annuler à tout moment ?',
    answer:
      'Oui, directement depuis Mon compte, rubrique Abonnement. Tu gardes l’accès jusqu’à la fin de la période déjà payée. Les pass sont des paiements uniques, sans renouvellement.'
  },
  {
    question: 'Le paiement est-il sécurisé ?',
    answer:
      'Oui. Le paiement passe par Stripe, leader du paiement en ligne. Aucune donnée de carte n’est stockée chez nous, et une facture t’est envoyée par e‑mail après chaque règlement.'
  },
  {
    question: 'OptiTAB fonctionne-t-il sur téléphone ?',
    answer:
      'Oui, sur ordinateur, tablette et smartphone, directement dans le navigateur. Il n’y a aucune application à installer.'
  },
  {
    question: 'Qui écrit les contenus ?',
    answer:
      'Des enseignants expérimentés, en suivant le programme officiel de l’Éducation nationale. Les contenus sont relus et enrichis chaque semaine.'
  },
  {
    question: 'Proposez-vous des cours particuliers ?',
    answer:
      'Oui : des cours particuliers en ligne en maths, physique-chimie et informatique, du collège aux classes préparatoires. Tous les détails et les tarifs sont sur la page Cours particuliers.'
  },
  {
    question: 'Comment vous contacter ?',
    answer:
      'Par WhatsApp au 07 64 04 02 51 ou par e‑mail à contact@optitab.net, 7 jours sur 7. Nous répondons sous 24 heures.'
  }
]

export const vitrineContact = {
  email: 'contact@optitab.net',
  whatsapp: '33764040251',
  whatsappAffiche: '07 64 04 02 51',
  messageWhatsapp: 'Bonjour, j’ai une question sur OptiTAB !'
}

// En-tête allégé : uniquement des ancres vers les sections de l'accueil, pour que
// le visiteur reste sur la page jusqu'aux formules. Les autres pages sont listées
// dans le pied de page (utile aussi pour le référencement).
// Hors de l'accueil, un lien qui a une page dédiée (`page`) y mène directement.
export const vitrineAncres = [
  { ancre: 'methode', texte: 'La méthode', navName: 'method' },
  { ancre: 'tarifs', texte: 'Tarifs', navName: 'pricing', page: '/tarifs' },
  { ancre: 'cours-particuliers', texte: 'Cours particuliers', navName: 'tutoring', page: '/cours-particuliers' },
  { ancre: 'faq', texte: 'Questions', navName: 'faq' }
]

export const vitrineFooter = {
  accroche:
    'La plateforme de maths en ligne qui accompagne chaque élève, du CE2 à la Terminale : cours, fiches de synthèse et exercices corrigés pas à pas.',
  colonnes: [
    {
      titre: 'Apprendre',
      liens: [
        { texte: 'Ressources gratuites', lien: '/ressources-gratuites' },
        { texte: 'Cours gratuits', lien: '/ressources-gratuites/cours' },
        { texte: 'Exercices corrigés', lien: '/ressources-gratuites/exercices' },
        { texte: 'Fiches de synthèse', lien: '/ressources-gratuites/syntheses' }
      ]
    },
    {
      titre: 'OptiTAB',
      liens: [
        { texte: 'Tarifs', lien: '/tarifs' },
        { texte: 'Cours particuliers', lien: '/cours-particuliers' },
        { texte: 'Blog', lien: '/blog' },
        { texte: 'À propos', lien: '/about' },
        { texte: 'Contact', lien: '/contact' }
      ]
    }
  ],
  legal: [
    { texte: 'Mentions légales', lien: '/legal' },
    { texte: 'Confidentialité', lien: '/confidentialite' },
    { texte: 'Cookies', lien: '/cookies' },
    { texte: 'CGU', lien: '/cgu' },
    { texte: 'CGV', lien: '/cgv' }
  ]
}

export const GOOGLE_REVIEWS_URL =
  'https://www.google.com/search?sa=X&sca_esv=87839103094c6a77&rlz=1C1ONGR_frFR997FR997&tbm=lcl&sxsrf=AE3TifM8SPH5m33A0ZODqZcHY3n5nxpSQA:1762342450222&q=OptiTAB+Avis&rflfq=1&num=20&stick=H4sIAAAAAAAAAONgkxI2MzU1tzA3MTY3tDQxMDS3MDEw2MDI-IqRx7-gJDPE0UnBsSyzeBErChcASF6_gzgAAAA&rldimm=6557874371940178400&hl=fr-FR&ved=2ahUKEwiviN-d9dqQAxWDNPsDHWjSMyYQ9fQKegQIRxAF&biw=733&bih=696&dpr=1.56#lkt=LocalPoiReviews'
