export const freeContentMeta = {
  course: {
    title: 'Cours de maths gratuits',
    highlight: 'Cours de maths offerts',
    description: 'Testez la méthode OptiTAB avec des cours de maths gratuits.',
    badge: 'Cours express',
    accent: '#2563eb',
    routeName: 'FreeCourses',
    hero: {
      title: 'Cours de maths gratuits en ligne',
      subtitle: 'Accédez à un chapitre de maths gratuit avec méthode pas à pas, exemples concrets et exercices corrigés.',
      stats: ['Cours de maths', 'Exercices corrigés', 'Fiches de révision']
    },
    subjectLine: 'Plateforme de maths OptiTAB • Collège, lycée, prépa',
    context: 'La vitrine gratuite est dédiée aux mathématiques pour vous faire tester la méthode OptiTAB avant abonnement.',
    searchPlaceholder: 'Rechercher un chapitre de maths (ex : produit scalaire, projection, orthogonalité...)',
    quickFilters: [],
    pedago: {
      badge: 'Méthode OptiTAB',
      title: 'Un mini parcours pour comprendre et pratiquer',
      subtitle: 'Même structure que dans l’espace abonné : rappel de cours, exemple guidé, exercice d’entraînement.',
      steps: [
        { title: '1. Comprendre', text: 'Lis la synthèse structurée : définitions, propriétés clés et astuces visuelles.' },
        { title: '2. Observer', text: 'Suis un exemple commenté pas-à-pas pour voir la méthode appliquée sur un vrai sujet.' },
        { title: '3. Tenter', text: 'Télécharge la fiche ou lance l’exercice corrigé et compare ton raisonnement.' }
      ],
      ctaText: 'Débloquer tous les chapitres'
    },
    checklist: {
      badge: 'Ce que tu révises',
      title: 'Produit scalaire & repères vectoriels',
      bullets: [
        'Définitions, propriétés et formules indispensables',
        'Méthodes pour prouver l’orthogonalité ou calculer un angle',
        'Exercices-type corrigés (coordonnées, projections, repérage spatial)'
      ],
      note: 'Ces extraits sont issus de nos parcours premium et restent ouverts pour que tu puisses tester l’approche.'
    }
  },
  exercise: {
    title: 'Exercices de maths gratuits',
    highlight: 'Exercices de maths corrigés',
    description: 'Passez de la théorie à la pratique avec des exercices de maths corrigés.',
    badge: 'Ateliers interactifs',
    accent: '#10b981',
    routeName: 'FreeExercises',
    hero: {
      title: 'Exercices de maths corrigés gratuits',
      subtitle: 'Entraînez-vous sur des exercices de maths avec correction détaillée et méthode étape par étape.',
      stats: ['Corrections détaillées', 'Méthodes bac', 'Progression guidée']
    },
    searchPlaceholder: 'Rechercher un exercice de maths (ex : fractions, dérivation, probabilités...)',
    quickFilters: ['Mathématiques', 'Brevet', 'Bac', 'Prépa']
  },
  summary: {
    title: 'Fiches de maths gratuites',
    highlight: 'Fiches de révision maths',
    description: 'L’essentiel des maths, prêt à être mémorisé.',
    badge: 'Focus révision',
    accent: '#f97316',
    routeName: 'FreeSummaries',
    hero: {
      title: 'Fiches de révision maths gratuites',
      subtitle: 'Révisez rapidement avec des fiches de maths claires, prêtes à imprimer et à mémoriser.',
      stats: ['Formules clés', 'Méthodes essentielles', 'Format rapide']
    },
    searchPlaceholder: 'Chercher une fiche de maths (ex : trigonométrie, fonctions, géométrie...)',
    quickFilters: ['Collège', 'Lycée', 'Terminale', 'Prépa']
  }
}

export const freeContentHomeBlocks = Object.entries(freeContentMeta).map(([type, meta]) => ({
  type,
  title: meta.title,
  highlight: meta.highlight,
  description: meta.description,
  badge: meta.badge,
  accent: meta.accent,
  to: { name: meta.routeName },
  bullets: type === 'course' 
    ? [
        'Cours structurés et faciles à suivre',
        'Explications claires avec exemples corrigés',
        'Accès 24h/24 sur mobile et ordinateur',
        'Sans carte bancaire, sans engagement'
      ]
    : type === 'exercise'
    ? [
        'Exercices corrigés pas-à-pas',
        'Astuces et méthodes directement applicables',
        'Interface fluide pensée pour les mobiles',
        'Accès immédiat, sans création de compte'
      ]
    : [
        'Notions clés synthétisées en une page',
        'Idéales avant contrôles et examens',
        'Consultation rapide sur mobile ou tablette',
        'Utilisables sans compte ni inscription'
      ]
}))

export const freeContentFallback = {
  course: [
    {
      slug: 'fractions-6eme',
      titre: 'Fractions - comprendre et comparer',
      accroche: 'Chapitre offert 6e - Mathématiques',
      excerpt: 'Une méthode visuelle pour passer des parts de pizza aux opérations sur les fractions.',
      badge: 'Nouveau',
      lecture_duree: '15 min',
      tag_secondaire: '6e',
      matiere_nom: 'Mathématiques',
      niveau_nom: '6e',
      pays_nom: 'France',
      cover_image: '',
      resource_type: 'course'
    },
    {
      slug: 'geographie-climats',
      titre: 'Comprendre les grands climats',
      accroche: 'Extrait offert 5e - Géographie',
      excerpt: 'Observe trois cartes interactives pour comparer les climats mondiaux.',
      badge: 'Parents rassurés',
      lecture_duree: '10 min',
      tag_secondaire: '5e',
      matiere_nom: 'Géographie',
      niveau_nom: '5e',
      pays_nom: 'France',
      cover_image: '',
      resource_type: 'course'
    }
  ],
  exercise: [
    {
      slug: 'fractions-entrainement',
      titre: 'Série d’exercices sur les fractions',
      accroche: 'Corrigés détaillés',
      excerpt: '4 exercices progressifs pour additionner et simplifier les fractions.',
      badge: 'Guidé',
      lecture_duree: '20 min',
      tag_secondaire: 'Maths',
      matiere_nom: 'Mathématiques',
      niveau_nom: '5e',
      pays_nom: 'France',
      cover_image: '',
      resource_type: 'exercise'
    },
    {
      slug: 'conjugaison-imparfait',
      titre: 'Imparfait de l’indicatif',
      accroche: 'Exercices interactifs',
      excerpt: 'Complète les phrases puis compare ta réponse avec la correction audio.',
      badge: 'Audio',
      lecture_duree: '12 min',
      tag_secondaire: 'Français',
      matiere_nom: 'Français',
      niveau_nom: 'CM2',
      pays_nom: 'France',
      cover_image: '',
      resource_type: 'exercise'
    }
  ],
  summary: [
    {
      slug: 'fiche-triangles',
      titre: 'Fiche mémo - Triangles remarquables',
      accroche: 'Format PDF offert',
      excerpt: 'Rappels + figures annotées pour reconnaitre rectangle, isocèle et équilatéral.',
      badge: 'À imprimer',
      lecture_duree: '5 min',
      tag_secondaire: 'Maths',
      matiere_nom: 'Mathématiques',
      niveau_nom: '5e',
      pays_nom: 'France',
      cover_image: '',
      resource_type: 'summary'
    },
    {
      slug: 'fiche-revolution',
      titre: 'Révolution française - dates clés',
      accroche: 'Ligne du temps offerte',
      excerpt: 'Un résumé chronologique pour préparer le contrôle.',
      badge: 'Chrono',
      lecture_duree: '7 min',
      tag_secondaire: 'Histoire',
      matiere_nom: 'Histoire',
      niveau_nom: '4e',
      pays_nom: 'France',
      cover_image: '',
      resource_type: 'summary'
    }
  ]
}
