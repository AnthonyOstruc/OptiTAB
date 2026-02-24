import heroImage from '@/assets/Images/HeroSection3.jpg';
// import icons from '@/assets/icons'; // supprimé car on utilise maintenant des noms de fichiers

export { faq } from './homeFaq.js'

export const sectionHero = {
  titre: 'Cours particuliers en ligne + plateforme de maths',
  sousTitre: 'Cours particuliers en ligne (maths, physique, chimie, info)',
  sousTitre2: 'Plateforme de maths (abonnement) : cours, fiches, exercices corrigés.',
  miniLine: "Collège • Lycée • Prépa • Université",
  reassurance: "Contenu structuré • Corrections pas à pas • Suivi de progression",
  ctaText: "Découvrir la plateforme Maths",
  ctaSecondary: "Découvrir les cours particuliers",
  image: heroImage,
  showImage: false,
  bg: "linear-gradient(135deg, #fefefe 0%, #f8fafc 30%, #f1f5f9 60%, #e2e8f0 100%)"
};

export const introFeatures = {
  titre: "Tout ce qu'il vous faut pour",
  highlight: "Réussir dans toutes les matières scientifiques",
  description: "OptiTAB est une plateforme de soutien scolaire en ligne conçue par des professeurs experts : cours clairs, exercices guidés et outils intelligents pour progresser efficacement, du collège au lycée et jusqu’aux grandes écoles.",
  features: [
    {
      icon: 'fichesSynthese',
      titre: "Cours Structurés et Accessibles",
      description: "Des leçons rédigées par des enseignants expérimentés, conçues pour être claires, progressives et adaptées à chaque niveau."
    },
    {
      icon: 'outilsIntelligents',
      titre: "Outils Intelligents",
      description: "Utilisez nos outils intégrés : calculatrices, solveurs, convertisseurs et graphiques interactifs pour travailler plus vite et mieux."
    },
    {
      icon: 'exercicesGuides',
      titre: "Exercices Guidés et Corrigés",
      description: "Pratiquez avec des exercices interactifs, avec des corrigés détaillés pour comprendre vos erreurs et progresser en autonomie."
    },
    {
      icon: 'AuteursExperts',
      titre: "Auteurs Experts",
      description: "Tous nos contenus sont conçus et validés par des professeurs qualifiés, pour vous garantir qualité et fiabilité."
    },
    {
      icon: 'ApprentissageFlexible',
      titre: "Apprentissage Flexible",
      description: "Travaillez à votre rythme, quand vous le voulez. La plateforme est accessible 24h/24, 7j/7 depuis tous vos appareils."
    },
    {
      icon: 'SuiviProgression',
      titre: "Suivi de votre Progression",
      description: "Visualisez vos progrès grâce à des tableaux de bord clairs, des objectifs à atteindre et des badges de réussite."
    }
  ]
};

export const titreSujets = "Cours particuliers et accompagnement, du collège aux grandes écoles.";

// export const sujets = subjects; // supprimé, tout est dynamique

export const titreFonctionnalites = "Nos fonctionnalités clés";
export const fonctionnalites = [
  {
    titre: 'Cours interactifs',
    description: 'Des cours adaptés à chaque niveau, du collège à la prépa.',
    icon: 'code'
  },
  {
    titre: 'Exercices guidés',
    description: 'Pratiquez avec des corrigés détaillés pour progresser efficacement.',
    icon: 'math'
  },
  {
    titre: 'Suivi personnalisé',
    description: 'Un accompagnement sur-mesure pour chaque élève.',
    icon: 'chemistry'
  }
];

export const etapesParcours = {
  titre: "Comment",
  highlight: "OptiTAB",
  titreFin: "Fonctionne",
  description: "Commencez en seulement trois étapes simples et entamez votre parcours vers la maîtrise des matières.",
  etapes: [
    {
      numero: '01',
      icon: '👤',
      titre: "Inscription",
      description: "Créez votre compte en quelques secondes."
    },
    {
      numero: '02',
      icon: '📘',
      titre: "Niveau",
      description: "Sélectionnez le niveau adapté."
    },
    {
      numero: '03',
      icon: '📈',
      titre: "Progression",
      description: "Cours, exercices et suivi de progression."
    }
  ],
  ctaText: "Commencer gratuitement",
  ctaSecondary: "Voir les tarifs",
  ctaTop: "Prêt à commencer ?",
  titreBas: "Donnez à votre enfant les clés de la réussite avec un apprentissage adapté à ses besoins !"
};

export const introPiedDePage = {
  message: "Contactez-nous pour toute question ou demande d'information. Nous sommes là pour vous accompagner dans votre réussite."
};

export const contactsPiedDePage = [
  {
    icone: 'mail',
    texte: 'contact@optitab.net',
    lien: 'mailto:contact@optitab.net',
    etiquette: 'Envoyer un email',
    externe: false
  },
  {
    icone: 'linkedin',
    texte: 'LinkedIn',
    lien: 'https://linkedin.com/company/optitab',
    etiquette: 'LinkedIn OptiTAB',
    externe: true
  }
];

export const liensPiedDePage = [
  { etiquette: "Politique de confidentialité", lien: "#" },
  { etiquette: "Conditions d'utilisation", lien: "#" },
  { etiquette: "Contact", lien: "#" }
];

export const newsletterSection = {
  titre: "Restez informé avec OptiTAB",
  description: "Recevez les dernières actualités, mises à jour et conseils pour progresser en maths directement dans votre boîte mail.",
  placeholder: "Votre email",
  bouton: "S’abonner"
};

export const pricingPlans = {
  titre: "Choisissez Votre Formule d'Apprentissage",
  description: "Commencez avec notre formule gratuite ou débloquez les fonctionnalités premium avec nos abonnements abordables. Annulation possible à tout moment.",
  legal: "Paiement sécurisé • Résiliation à tout moment • Pas de remboursement au prorata (sauf dispositions légales)",
  garantie: "Accès immédiat",
  plans: [
    {
      key: 'free',
      titre: 'Gratuit',
      sousTitre: 'Parfait pour commencer',
      prix: '0€',
      prixDetail: 'pour toujours',
      avantages: [
        'Accès à 20 leçons de base',
        'Outils de calcul basiques',
        'Support communautaire',
        'Suivi des progrès',
        'Accès mobile'
      ],
      bouton: 'Commencer Gratuitement',
      boutonType: 'secondary',
      populaire: false
    },
    {
      key: 'standard',
      titre: 'Standard',
      sousTitre: 'Pour les apprenants sérieux',
      prix: '19€',
      prixDetail: 'par mois',
      avantages: [
        'Accès à plus de 200 leçons',
        'Outils de calcul avancés',
        'Support professeur 1-à-1',
        'Analyses détaillées des progrès',
        'Accès au contenu hors ligne',
        'Support prioritaire'
      ],
      bouton: "S'abonner maintenant",
      boutonType: 'primary',
      badge: 'Le Plus Populaire',
      populaire: true
    },
    {
      key: 'premium',
      titre: 'Premium',
      sousTitre: 'Pour une réussite maximale',
      prix: '39€',
      prixDetail: 'par mois',
      avantages: [
        'Accès à plus de 500 leçons',
        'Tous les outils de calcul',
        'Support professeur illimité',
        'Analyses avancées',
        'Parcours d\'apprentissage personnalisés',
        'Programmes de certification',
        'Partage familial (4 comptes)'
      ],
      bouton: "S'abonner maintenant",
      boutonType: 'premium',
      populaire: false
    }
  ]
};

export { freeContentHomeBlocks } from './freeContent';
