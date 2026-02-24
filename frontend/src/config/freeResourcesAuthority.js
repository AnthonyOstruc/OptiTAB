const STABLE_PATHS = Object.freeze({
  hub: '/ressources-gratuites',
  courses: '/ressources-gratuites/cours',
  exercises: '/ressources-gratuites/exercices',
  summaries: '/ressources-gratuites/syntheses'
})

const SITE_BASE_URL = 'https://optitab.net'

function normalizePathname(pathname) {
  const raw = String(pathname || '').trim()
  if (!raw || raw === '/') return '/'
  const normalized = raw.startsWith('/') ? raw : `/${raw}`
  return normalized.replace(/\/+$/, '') || '/'
}

function toPathname(href) {
  try {
    return normalizePathname(new URL(String(href || ''), SITE_BASE_URL).pathname)
  } catch {
    return normalizePathname(href)
  }
}

export const KNOWN_404_POPULAR_LINK_PATHS = Object.freeze([
  '/ressources-gratuites/exercices/exercice-gratuit-1058-france-1ere-mathematiques-boucles-for-avec-range-exercices-de-base'
])

const KNOWN_404_POPULAR_LINK_PATH_SET = new Set(
  KNOWN_404_POPULAR_LINK_PATHS.map((path) => toPathname(path))
)

export function isKnownBrokenPopularLink(href) {
  return KNOWN_404_POPULAR_LINK_PATH_SET.has(toPathname(href))
}

const SHARED_FAQ = Object.freeze([
  {
    question: "Comment combiner cours, exercices corrigés et fiches de révision ?",
    answer: "Commencez par un cours pour comprendre la notion, entraînez-vous avec des exercices corrigés, puis terminez avec une fiche de révision pour fixer l'essentiel."
  },
  {
    question: "Ces ressources couvrent-elles le collège, le lycée et les objectifs Bac/Brevet ?",
    answer: "Oui, les contenus sont organisés pour accompagner la progression du collège au lycée, avec des chapitres utiles pour préparer Bac/Brevet."
  },
  {
    question: "Comment organiser une séance efficace en moins d'une heure ?",
    answer: "Faites 15 minutes de cours, 30 minutes d'exercices corrigés ciblés, puis 10 minutes de fiche de révision pour consolider."
  }
])

function withSharedFaq(uniqueItems) {
  return [...SHARED_FAQ, ...(Array.isArray(uniqueItems) ? uniqueItems : [])]
}

export const FREE_RESOURCES_AUTHORITY_CONTENT = Object.freeze({
  hub: {
    introParagraphs: [
      "Cette page rassemble une base claire pour travailler les maths du collège au lycée, puis vers la prépa. Que vous prépariez un contrôle continu, un devoir surveillé ou un examen Bac/Brevet, vous trouvez ici des parcours simples à suivre: des cours pour comprendre, des exercices corrigés pour s'entraîner et des fiches de révision pour mémoriser. L'objectif est de gagner du temps dans l'organisation, d'aller directement aux notions utiles et de progresser avec une méthode régulière. Chaque bloc vise une utilisation concrète, sans détour, pour maintenir un rythme de travail réaliste.",
      "Sur OptiTAB, la logique est progressive: commencer par la notion, vérifier les acquis avec des exemples guidés, puis consolider avec des entraînements ciblés. Les élèves de collège peuvent revoir les fondamentaux, les élèves de lycée peuvent renforcer l'algèbre, l'analyse et la géométrie, et les profils orientés Bac/Brevet peuvent travailler les points les plus évalués. Chaque ressource est pensée pour rester lisible, actionnable et adaptée à un rythme de travail réaliste sur la semaine.",
      "Cette page hub sert aussi de point d'entrée éditorial: elle vous oriente vers les chapitres les plus demandés, les listes par niveau et les contenus les plus utiles pour réviser efficacement. Vous pouvez alterner entre cours, exercices corrigés et fiches de révision selon votre besoin du moment: comprendre une notion, corriger une erreur récurrente, ou réactiver rapidement les méthodes avant une évaluation. Le maillage interne ci-dessous vous guide vers les URL canoniques des ressources les plus consultées. En pratique, cela permet de bâtir une routine hebdomadaire stable, adaptée à votre niveau, avec des objectifs simples et mesurables."
    ],
    popularLinks: [
      { label: 'Liste des cours gratuits', href: STABLE_PATHS.courses },
      { label: 'Liste des exercices corrigés', href: STABLE_PATHS.exercises },
      { label: 'Liste des fiches de révision', href: STABLE_PATHS.summaries },
      { label: 'Ressources gratuites par niveau', href: STABLE_PATHS.hub },
      { label: 'Cours de maths collège et Brevet', href: STABLE_PATHS.courses },
      { label: 'Cours de maths lycée et Bac', href: STABLE_PATHS.courses },
      { label: 'Exercices corrigés collège', href: STABLE_PATHS.exercises },
      { label: 'Exercices corrigés lycée', href: STABLE_PATHS.exercises },
      { label: 'Cours Terminale: factorisation', href: '/ressources-gratuites/cours/france/lycee/maths/terminal-bac-factorisation-mise-en-forme-factorisee-methodes-et-techniques-115' },
      { label: 'Fiche de révision MPSI: sommes et produits', href: '/ressources-gratuites/syntheses/france/prepa/maths/mpsi-mp2i-resume-sommes-et-produits-58' }
    ],
    faq: withSharedFaq([
      {
        question: "Par où commencer sur le hub des ressources gratuites ?",
        answer: "Commencez par choisir le format le plus adapté à votre besoin immédiat: cours pour comprendre, exercices corrigés pour appliquer, fiches de révision pour mémoriser."
      },
      {
        question: "Puis-je utiliser ce hub pour planifier ma semaine de révision ?",
        answer: "Oui, le hub sert de point de départ pour répartir vos séances entre compréhension, entraînement et synthèse sur la semaine."
      }
    ])
  },
  course: {
    introParagraphs: [
      "La liste des cours gratuits est pensée pour structurer la progression sur des notions clés, du collège au lycée puis jusqu'aux niveaux prépa. Chaque contenu vise un objectif précis: poser les bases, clarifier la méthode et préparer des applications concrètes avant entraînement. Si vous visez une validation de chapitre ou un palier Bac/Brevet, vous pouvez suivre un parcours simple: lire le cours, vérifier la compréhension sur quelques exemples, puis compléter avec des exercices corrigés et des fiches de révision pour ancrer durablement les automatismes. Cette organisation facilite un travail autonome et limite les révisions de dernière minute.",
      "Le format des cours est conçu pour réduire les blocages fréquents: vocabulaire explicite, enchaînement logique, et repères méthodologiques directement exploitables en devoir. Les élèves de collège consolident les fondamentaux, ceux de lycée approfondissent les techniques attendues en contrôle, et les profils orientés filières sélectives avancent vers des chapitres plus denses. OptiTAB met l'accent sur la lisibilité des explications afin que le temps passé en révision produise un gain réel, notamment avant les échéances Bac/Brevet.",
      "Pour un travail complet, utilisez cette page en complément des autres formats: les cours installent la compréhension, les exercices corrigés testent la maîtrise opérationnelle, et les fiches de révision servent de support de rappel rapide. Le bloc de liens populaires ci-dessous vous envoie vers des URL canoniques pertinentes pour gagner du temps de navigation et accéder directement aux chapitres les plus consultés par niveau. Vous pouvez ainsi construire une progression continue sans multiplier les sources ni perdre du temps entre plusieurs outils."
    ],
    popularLinks: [
      { label: 'Tous les cours gratuits', href: STABLE_PATHS.courses },
      { label: 'Cours de maths collège', href: STABLE_PATHS.courses },
      { label: 'Cours de maths lycée', href: STABLE_PATHS.courses },
      { label: 'Réviser avec des exercices corrigés', href: STABLE_PATHS.exercises },
      { label: 'Réviser avec des fiches de révision', href: STABLE_PATHS.summaries },
      { label: 'Hub ressources gratuites', href: STABLE_PATHS.hub },
      { label: 'Parcours Bac/Brevet en cours', href: STABLE_PATHS.courses },
      { label: 'Cours de maths Terminale: factorisation', href: '/ressources-gratuites/cours/france/lycee/maths/terminal-bac-factorisation-mise-en-forme-factorisee-methodes-et-techniques-115' },
      { label: 'Cours de maths Terminale: matrices', href: '/ressources-gratuites/cours/france/lycee/maths/terminal-bac-matrices-112' },
      { label: 'Cours de maths MPSI: nombres complexes', href: '/ressources-gratuites/cours/france/prepa/maths/mpsi-mp2i-nombres-complexes-123' }
    ],
    faq: withSharedFaq([
      {
        question: "Comment exploiter la liste de cours avant un DS ?",
        answer: "Ciblez les chapitres du DS, lisez chaque cours de façon active, puis validez immédiatement avec quelques exercices corrigés du même thème."
      },
      {
        question: "Quelle progression suivre entre collège et lycée sur les cours ?",
        answer: "Consolidez d'abord les fondamentaux du collège, puis montez progressivement vers les chapitres de lycée liés à vos prochaines évaluations."
      }
    ])
  },
  exercise: {
    introParagraphs: [
      "Cette liste d'exercices corrigés gratuits vous aide à transformer la théorie en réflexes solides, du collège au lycée et jusqu'aux niveaux prépa. Chaque chapitre regroupe des entraînements guidés pour travailler les méthodes attendues en évaluation et vérifier la qualité du raisonnement. Si vous préparez un devoir Bac/Brevet, vous pouvez organiser une séance efficace: lecture rapide d'un cours, résolution d'exercices corrigés représentatifs, puis consolidation avec des fiches de révision pour stabiliser les points techniques à retenir. Ce cadre vous permet de mesurer rapidement vos progrès sur des objectifs concrets et d'ajuster votre plan de travail.",
      "Les exercices sont pensés pour progresser par étapes: compréhension de l'énoncé, choix de la stratégie, calcul propre, puis vérification du résultat. Ce format réduit les erreurs récurrentes (mauvaise interprétation, oubli de conditions, manque de justification) et améliore la régularité des performances. Les élèves de collège et de lycée peuvent cibler les chapitres prioritaires, tandis que les profils orientés filières exigeantes renforcent les automatismes sur des thèmes plus avancés. OptiTAB privilégie une logique de progression réaliste et directement exploitable.",
      "Pour maximiser l'impact, combinez systématiquement les formats: les cours clarifient les notions avant l'entraînement, les exercices corrigés installent la maîtrise opérationnelle, et les fiches de révision servent de support de rappel avant contrôle. Les liens populaires ci-dessous pointent vers des URL canoniques utiles pour accéder vite aux chapitres les plus demandés et construire un plan de travail cohérent selon votre niveau et votre objectif Bac/Brevet. Cette logique réduit les révisions dispersées et aide à garder une préparation régulière jusqu'à l'examen."
    ],
    popularLinks: [
      { label: 'Tous les exercices corrigés', href: STABLE_PATHS.exercises },
      { label: 'Exercices corrigés collège', href: STABLE_PATHS.exercises },
      { label: 'Exercices corrigés lycée', href: STABLE_PATHS.exercises },
      { label: 'Cours associés aux exercices', href: STABLE_PATHS.courses },
      { label: 'Fiches de révision pour consolider', href: STABLE_PATHS.summaries },
      { label: 'Hub ressources gratuites', href: STABLE_PATHS.hub },
      { label: 'Exercices corrigés Bac/Brevet', href: STABLE_PATHS.exercises },
      { label: 'Exercices corrigés Première: boucles', href: '/ressources-gratuites/exercices/france/lycee/maths/premiere-1er-boucles-iterations-163' },
      { label: 'Exercices corrigés Seconde: fonctions', href: '/ressources-gratuites/exercices/france/lycee/maths/seconde-notion-de-fonction-178' },
      { label: 'Exercices corrigés Terminale: arithmétique', href: '/ressources-gratuites/exercices/france/lycee/maths/terminal-bac-arithmetique-103' }
    ],
    faq: withSharedFaq([
      {
        question: "Comment choisir un chapitre d'exercices corrigés pertinent ?",
        answer: "Choisissez d'abord les chapitres directement liés à votre prochain contrôle, puis élargissez aux thèmes voisins une fois les bases maîtrisées."
      },
      {
        question: "Pourquoi refaire un exercice corrigé sans regarder la solution ?",
        answer: "Cela permet de vérifier vos automatismes réels et d'identifier précisément les étapes où le raisonnement se fragilise."
      }
    ])
  },
  summary: {
    introParagraphs: [
      "Cette page regroupe des fiches de révision conçues pour aller à l'essentiel sans perdre la rigueur, du collège au lycée puis vers la prépa. Chaque fiche condense les notions importantes, les formules utiles et les repères de méthode à maîtriser avant évaluation. Pour une préparation Bac/Brevet efficace, utilisez-les comme support de cadrage: repérer les points clés, vérifier les liens entre notions, puis compléter avec des cours détaillés et des exercices corrigés afin de transformer la révision en résultat concret. Vous disposez ainsi d'un support fiable pour planifier des séances courtes mais efficaces sur toute la semaine.",
      "Le format synthétique est particulièrement utile quand le temps est limité: en quelques minutes, vous visualisez la structure d'un chapitre, les erreurs à éviter et les démarches attendues. Les élèves de collège peuvent consolider les bases, les élèves de lycée peuvent sécuriser les acquis avant devoir, et les profils plus avancés peuvent garder une vue d'ensemble avant entraînement intensif. OptiTAB privilégie des fiches lisibles, hiérarchisées et faciles à relire pour maintenir une progression régulière sans surcharge.",
      "Pour obtenir un vrai gain de performance, combinez systématiquement les trois formats complémentaires: cours pour comprendre le fond, exercices corrigés pour vérifier l'exécution, fiches de révision pour ancrer les automatismes. Le bloc de liens populaires ci-dessous facilite l'accès aux URL canoniques les plus utiles selon votre objectif. Vous gagnez du temps, vous évitez les parcours dispersés et vous construisez une révision cohérente orientée Bac/Brevet. Ce fonctionnement rend les révisions plus prévisibles et améliore la confiance avant les contrôles."
    ],
    popularLinks: [
      { label: 'Toutes les fiches de révision', href: STABLE_PATHS.summaries },
      { label: 'Fiches de révision collège', href: STABLE_PATHS.summaries },
      { label: 'Fiches de révision lycée', href: STABLE_PATHS.summaries },
      { label: 'Cours pour compléter les fiches', href: STABLE_PATHS.courses },
      { label: "Exercices corrigés pour s'entraîner", href: STABLE_PATHS.exercises },
      { label: 'Hub ressources gratuites', href: STABLE_PATHS.hub },
      { label: 'Fiches de révision Bac/Brevet', href: STABLE_PATHS.summaries },
      { label: 'Fiche de révision MPSI: sommes et produits', href: '/ressources-gratuites/syntheses/france/prepa/maths/mpsi-mp2i-resume-sommes-et-produits-58' },
      { label: 'Cours Terminale: factorisation', href: '/ressources-gratuites/cours/france/lycee/maths/terminal-bac-factorisation-mise-en-forme-factorisee-methodes-et-techniques-115' },
      { label: 'Cours MPSI: nombres complexes', href: '/ressources-gratuites/cours/france/prepa/maths/mpsi-mp2i-nombres-complexes-123' }
    ],
    faq: withSharedFaq([
      {
        question: "Quand utiliser une fiche de révision plutôt qu'un cours complet ?",
        answer: "Utilisez la fiche pour une vue rapide des points clés, puis revenez au cours complet si une méthode ou une démonstration demande plus de détail."
      },
      {
        question: "Comment exploiter les fiches la veille d'un Bac/Brevet ?",
        answer: "Faites une lecture active des formules essentielles, puis vérifiez immédiatement leur application sur quelques exercices corrigés ciblés."
      }
    ])
  }
})

export const FREE_RESOURCES_FAQ_BY_ROUTE = Object.freeze({
  FreeResourcesHome: FREE_RESOURCES_AUTHORITY_CONTENT.hub.faq,
  FreeCourses: FREE_RESOURCES_AUTHORITY_CONTENT.course.faq,
  FreeExercises: FREE_RESOURCES_AUTHORITY_CONTENT.exercise.faq,
  FreeSummaries: FREE_RESOURCES_AUTHORITY_CONTENT.summary.faq
})
