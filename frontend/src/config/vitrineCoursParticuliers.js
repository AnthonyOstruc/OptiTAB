// Contenu de la page Cours particuliers (/cours-particuliers).
// Tarifs repris à l'identique de l'ancienne page (avant le 2 novembre 2026).

export const coursStats = [
  { valeur: '15+', libelle: 'ans d’enseignement' },
  { valeur: '300+', libelle: 'élèves accompagnés' },
  { valeur: '95 %', libelle: 'de réussite aux examens' },
  { valeur: '5/5', libelle: 'sur Google' }
]

export const coursPourQui = [
  {
    icone: 'notion',
    titre: 'Une notion qui bloque',
    texte: 'On reprend le chapitre à la base, avec des exemples simples, jusqu’à ce que tout soit clair avant le prochain contrôle.'
  },
  {
    icone: 'examen',
    titre: 'Un examen qui approche',
    texte: 'Brevet, bac, épreuves de spécialité : on révise les points clés et on s’entraîne sur des sujets types.'
  },
  {
    icone: 'prepa',
    titre: 'Prépa et études supérieures',
    texte: 'Un appui solide pour suivre le rythme, préparer les khôlles et les concours, en maths comme en physique.'
  },
  {
    icone: 'confiance',
    titre: 'Reprendre confiance',
    texte: 'Une méthode de travail claire, des objectifs atteignables et des progrès visibles pour retrouver la motivation.'
  }
]

// Le parcours, dans l'ordre où il se déroule.
export const coursEtapes = [
  {
    titre: 'Un premier échange',
    badge: 'Gratuit',
    texte: 'Vous me présentez la situation : niveau, difficultés, objectifs et échéances. Je vous explique comment je peux aider, sans aucun engagement.'
  },
  {
    titre: 'Un programme sur mesure',
    texte: 'Je prépare un plan de travail adapté au programme de la classe et aux prochaines échéances : contrôles, brevet, bac ou concours.'
  },
  {
    titre: 'Les séances en visio',
    texte: 'On reprend le cours là où ça bloque, puis on s’entraîne sur des exercices choisis pour l’élève. Chaque séance se termine par un travail précis à faire.'
  },
  {
    titre: 'Un suivi entre les séances',
    badge: '7 j/7',
    texte: 'Une question sur un exercice ? L’élève m’écrit sur WhatsApp et je réponds en général dans les 3 heures. Il peut aussi s’entraîner avec les ressources OptiTAB.'
  },
  {
    titre: 'Des progrès mesurés',
    texte: 'Nous faisons régulièrement le point sur les notes et les objectifs, pour ajuster le programme au fil de l’année.'
  }
]

export const coursMethode = [
  { icone: 'adapte', titre: 'Partir de l’élève', texte: 'Chaque séance s’adapte à son niveau, à son rythme et à sa façon de comprendre.' },
  { icone: 'clair', titre: 'Rendre simple le compliqué', texte: 'Les notions difficiles sont découpées en étapes claires, avec des exemples concrets.' },
  { icone: 'actif', titre: 'Faire participer', texte: 'L’élève cherche, propose et se trompe en sécurité : c’est ainsi qu’on retient.' },
  { icone: 'objectif', titre: 'Des objectifs clairs', texte: 'Un objectif par séance et un retour précis sur les points forts et ceux à travailler.' }
]

// Prix à l'heure et prix de l'heure dans un pack, par niveau.
export const coursTarifs = [
  { id: 'college', label: 'Collège', heure: 35, packs: { 5: 34, 10: 32, 20: 30 } },
  { id: 'lycee', label: 'Lycée', heure: 40, packs: { 5: 39, 10: 37, 20: 35 } },
  { id: 'prepa', label: 'Prépa et supérieur', heure: 45, packs: { 5: 44, 10: 42, 20: 40 } }
]

export const coursFaq = [
  {
    question: 'Quelles matières et quels niveaux ?',
    answer: 'Les mathématiques, la physique-chimie et l’informatique, du collège jusqu’à la prépa et l’université.'
  },
  {
    question: 'Comment se passe le premier échange ?',
    answer: 'Vous remplissez le formulaire en bas de page ou vous m’écrivez sur WhatsApp. Je vous recontacte sous 24 heures pour faire le point sur la situation et les objectifs. Cet échange est gratuit et sans engagement.'
  },
  {
    question: 'Comment se déroulent les cours ?',
    answer: 'En visio, en direct : on reprend le cours, on fait des exercices ensemble et l’élève repart avec un travail précis. Les horaires sont fixés ensemble, selon son emploi du temps.'
  },
  {
    question: 'Comment fonctionnent les packs d’heures ?',
    answer: 'Vous choisissez 5, 10 ou 20 heures. Plus le pack est grand, plus l’heure est avantageuse. Les heures sont à utiliser dans les 6 mois.'
  },
  {
    question: 'Comment se fait le paiement ?',
    answer: 'En ligne, par carte bancaire, avec un paiement sécurisé par Stripe. Une facture vous est fournie. Aucune carte n’est demandée pour le premier échange.'
  },
  {
    question: 'Y a-t-il un engagement ?',
    answer: 'Non. Les cours à l’heure se règlent séance par séance, et vous pouvez arrêter quand vous le souhaitez. Une remise est possible pour les frères et sœurs.'
  }
]
