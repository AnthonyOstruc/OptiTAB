import heroImage from '@/assets/Images/HeroSection3.jpg';
// import icons from '@/assets/icons'; // supprimé car on utilise maintenant des noms de fichiers

export const sectionHero = {
  titre: "OptiTAB — Votre Succès, Notre Mission",
  sousTitre: "Votre plateforme de référence pour apprendre, pratiquer et progresser.",
  image: heroImage,
  bg: "linear-gradient(135deg, #fefefe 0%, #f8fafc 30%, #f1f5f9 60%, #e2e8f0 100%)"
};

export const introFeatures = {
  titre: "Tout ce qu’il vous faut pour",
  highlight: "Réussir dans toutes les matières",
  description: "OptiTAB est une plateforme complète de soutien scolaire en ligne qui réunit des cours clairs, des exercices guidés, et des outils intelligents pour progresser efficacement, du collège au lycée.",
  features: [
    {
      icon: 'fichesSynthese',
      titre: "Cours Structurés et Accessibles",
      description: "Des leçons rédigées par des enseignants certifiés, conçues pour être claires, progressives et adaptées à chaque niveau."
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

export const titreSujets = "Cours et accompagnement, du collège aux grandes écoles.";

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
      titre: "Inscrivez-vous Gratuitement",
      description: "Créez votre compte en quelques secondes et obtenez un accès immédiat à notre contenu de démarrage."
    },
    {
      numero: '02',
      icon: '📘',
      titre: "Choisissez Votre Niveau",
      description: "Sélectionnez parmi les cours débutant à avancé adaptés à vos besoins."
    },
    {
      numero: '03',
      icon: '📈',
      titre: "Commencez à Apprendre",
      description: "Regardez les leçons, pratiquez les exercices et suivez vos progrès en maîtrisant de nouveaux concepts."
    }
  ],
  ctaText: "Commencez Votre Essai Gratuit",
  ctaSecondary: "Découvrir les Fonctionnalités",
  ctaTop: "Prêt à commencer ?",
  titreBas: "Donnez à votre enfant les clés de la réussite avec un apprentissage adapté à ses besoins !"
};

export const introPiedDePage = {
  message: "Contactez-nous pour toute question ou demande d'information. Nous sommes là pour vous accompagner dans votre réussite."
};

export const contactsPiedDePage = [
  {
    icone: 'mail',
    texte: 'contact@optitab.com',
    lien: 'mailto:contact@optitab.com',
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

export const faq = [
  {
    question: "Quels sujets de mathématiques Optitab couvre-t-il ?",
    answer: "Optitab couvre une gamme complète de mathématiques de l'arithmétique de base au calcul avancé. Cela inclut l'algèbre, la géométrie, la trigonométrie, les statistiques, le pré-calcul, le calcul, et plus encore. Notre contenu convient du collège au niveau universitaire."
  },
  {
    question: "Puis-je utiliser Optitab sur mon appareil mobile ?",
    answer: "Oui, Optitab est accessible sur tous les appareils : ordinateurs, tablettes et smartphones. Vous pouvez apprendre où que vous soyez, à tout moment."
  },
  {
    question: "Comment fonctionnent les outils de calcul intégrés ?",
    answer: "Nos outils de calcul (calculatrices, solveurs, graphiques) sont intégrés à la plateforme et utilisables directement dans les cours et exercices, sans installation supplémentaire."
  },
  {
    question: "Les enseignants sont-ils vraiment qualifiés ?",
    answer: "Tous nos contenus sont conçus et validés par des professeurs certifiés et des experts pédagogiques, pour garantir la qualité et la fiabilité de chaque ressource."
  },
  {
    question: "Que faire si je ne suis pas satisfait de mon abonnement ?",
    answer: "Vous pouvez résilier votre abonnement à tout moment. Si vous n'êtes pas satisfait, contactez notre support pour trouver une solution adaptée ou obtenir un remboursement selon nos conditions."
  },
  {
    question: "Comment fonctionne le suivi de progression ?",
    answer: "Votre progression est suivie automatiquement : vous visualisez vos résultats, vos badges, et vos objectifs atteints sur votre tableau de bord personnel."
  },
  {
    question: "Puis-je accéder aux contenus hors ligne ?",
    answer: "Certaines ressources sont téléchargeables pour un accès hors ligne. Nous travaillons à élargir cette fonctionnalité pour plus de flexibilité."
  }
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
  legal: "Pas satisfait ? Obtenez un remboursement intégral sous 30 jours, sans questions posées.",
  garantie: "Garantie satisfait ou remboursé 30 jours",
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
      bouton: 'Essai 7 jours gratuit',
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
      bouton: 'Essai 7 jours gratuit',
      boutonType: 'premium',
      populaire: false
    }
  ]
}; 