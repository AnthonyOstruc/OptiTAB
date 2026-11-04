// Classes publiées dans les ressources gratuites : adresse, intitulés et textes
// propres à chaque classe (chaque page de classe a un texte unique).

export const CYCLES = [
  { cle: 'primaire', titre: 'École primaire', court: 'Primaire', resume: 'Compter, calculer, mesurer et se repérer : les bases solides, du CP au CM2.' },
  { cle: 'college', titre: 'Collège', court: 'Collège', resume: 'De la 6e au brevet : calcul, géométrie, fonctions et raisonnement.' },
  { cle: 'lycee', titre: 'Lycée', court: 'Lycée', resume: 'De la Seconde au bac : analyse, probabilités, géométrie et algorithmique.' }
]

export const CLASSES = [
  {
    nom: 'CP', slug: 'cp', court: 'CP', long: 'CP', cycle: 'primaire',
    accroche: 'Nombres jusqu’à 100, premières additions et soustractions, formes et mesures.',
    intro: 'Au CP, votre enfant apprend à lire, écrire et comparer les nombres jusqu’à 100, à additionner et soustraire, à reconnaître les formes et à mesurer. Chaque chapitre propose une leçon illustrée, une fiche à relire et des exercices corrigés à faire ensemble.'
  },
  {
    nom: 'CE1', slug: 'ce1', court: 'CE1', long: 'CE1', cycle: 'primaire',
    accroche: 'Nombres jusqu’à 1 000, calcul posé, tables et premiers problèmes.',
    intro: 'Au CE1, on découvre les nombres jusqu’à 1 000, le calcul posé, les premières tables de multiplication et la résolution de petits problèmes. Les leçons sont courtes et illustrées, avec des exercices corrigés pas à pas.'
  },
  {
    nom: 'CE2', slug: 'ce2', court: 'CE2', long: 'CE2', cycle: 'primaire',
    accroche: 'Nombres jusqu’à 10 000, multiplication, monnaie, durées et géométrie.',
    intro: 'Au CE2, les nombres vont jusqu’à 10 000 : multiplication posée, premières divisions, monnaie, durées, longueurs et figures. Chaque leçon s’accompagne d’une fiche de révision et d’exercices corrigés.'
  },
  {
    nom: 'CM1', slug: 'cm1', court: 'CM1', long: 'CM1', cycle: 'primaire',
    accroche: 'Grands nombres, fractions, nombres décimaux et périmètres.',
    intro: 'Au CM1, on travaille les grands nombres, les premières fractions et les nombres décimaux, la division et les périmètres. Des leçons claires et des exercices corrigés pour progresser à son rythme.'
  },
  {
    nom: 'CM2', slug: 'cm2', court: 'CM2', long: 'CM2', cycle: 'primaire',
    accroche: 'Décimaux, fractions, proportionnalité, aires et préparation à la 6e.',
    intro: 'Au CM2, on consolide les décimaux et les fractions, on découvre la proportionnalité et les aires, et on prépare l’entrée en 6e. Cours illustrés, fiches et exercices corrigés pour chaque notion.'
  },
  {
    nom: '6ème', slug: '6e', court: '6e', long: 'sixième', cycle: 'college',
    accroche: 'Nombres décimaux, fractions, angles, symétrie et proportionnalité.',
    intro: 'En 6e, on consolide les nombres décimaux et les fractions, on découvre les angles, la symétrie axiale et la proportionnalité. Chaque chapitre suit le programme officiel avec un cours complet, une fiche de révision et des exercices corrigés.'
  },
  {
    nom: '5ème', slug: '5e', court: '5e', long: 'cinquième', cycle: 'college',
    accroche: 'Nombres relatifs, priorités de calcul, triangles et premiers calculs littéraux.',
    intro: 'En 5e, on découvre les nombres relatifs, les priorités de calcul et le calcul littéral, les triangles et les parallélogrammes. Cours, fiches et exercices corrigés pour chaque chapitre du programme.'
  },
  {
    nom: '4ème', slug: '4e', court: '4e', long: 'quatrième', cycle: 'college',
    accroche: 'Relatifs, puissances, théorème de Pythagore, équations et proportionnalité.',
    intro: 'En 4e, on calcule avec les relatifs, les fractions et les puissances, on démontre avec le théorème de Pythagore et on résout ses premières équations. Tout le programme, chapitre par chapitre, avec des exercices corrigés.'
  },
  {
    nom: '3ème', slug: '3e', court: '3e', long: 'troisième', cycle: 'college',
    accroche: 'Thalès, trigonométrie, fonctions, statistiques : tout pour réussir le brevet.',
    intro: 'En 3e, on prépare le brevet : calcul littéral, équations, théorème de Thalès, trigonométrie, fonctions et statistiques. Chaque chapitre propose un cours complet, une fiche pour réviser et des exercices corrigés pas à pas.'
  },
  {
    nom: '2nde', slug: 'seconde', court: 'Seconde', long: 'Seconde', cycle: 'lycee',
    accroche: 'Fonctions de référence, vecteurs, équations de droites, probabilités.',
    intro: 'En Seconde, on étudie les fonctions de référence, les vecteurs et les équations de droites, les statistiques et les probabilités, avec une première approche de l’algorithmique. Cours complets, fiches et exercices corrigés.'
  },
  {
    nom: '1ère', slug: 'premiere', court: 'Première', long: 'Première', cycle: 'lycee',
    accroche: 'Second degré, dérivation, suites, produit scalaire et probabilités (spécialité).',
    intro: 'En Première (spécialité mathématiques), on aborde le second degré, la dérivation, les suites, l’exponentielle, le produit scalaire et les probabilités conditionnelles. Chaque chapitre : un cours rigoureux, une fiche et des exercices corrigés.'
  },
  {
    nom: 'Terminale', slug: 'terminale', court: 'Terminale', long: 'Terminale', cycle: 'lycee',
    accroche: 'Limites, logarithme, intégrales, géométrie dans l’espace : tout le bac.',
    intro: 'En Terminale (spécialité mathématiques), on prépare le bac : suites et limites, continuité, logarithme, intégrales, géométrie dans l’espace, probabilités et algorithmique. Un cours complet, une fiche et des exercices corrigés par chapitre.'
  }
]

export const CLASSE_PAR_NOM = new Map(CLASSES.map((c) => [c.nom, c]))
