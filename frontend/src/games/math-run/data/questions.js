const rawQuestions = [
  // ─── Addition (6) ──────────────────────────────────────────────────────────
  { category: 'addition', question: '7 + 8 = ?',    correctAnswer: '15', distractors: ['13', '16'] },
  { category: 'addition', question: '14 + 9 = ?',   correctAnswer: '23', distractors: ['21', '25'] },
  { category: 'addition', question: '26 + 7 = ?',   correctAnswer: '33', distractors: ['31', '35'] },
  { category: 'addition', question: '45 + 18 = ?',  correctAnswer: '63', distractors: ['61', '65'] },
  { category: 'addition', question: '37 + 25 = ?',  correctAnswer: '62', distractors: ['60', '64'] },
  { category: 'addition', question: '53 + 29 = ?',  correctAnswer: '82', distractors: ['80', '84'] },

  // ─── Subtraction (6) ────────────────────────────────────────────────────────
  { category: 'subtraction', question: '15 − 7 = ?',   correctAnswer: '8',  distractors: ['6',  '9'  ] },
  { category: 'subtraction', question: '24 − 9 = ?',   correctAnswer: '15', distractors: ['13', '17' ] },
  { category: 'subtraction', question: '40 − 13 = ?',  correctAnswer: '27', distractors: ['25', '29' ] },
  { category: 'subtraction', question: '71 − 28 = ?',  correctAnswer: '43', distractors: ['41', '45' ] },
  { category: 'subtraction', question: '82 − 35 = ?',  correctAnswer: '47', distractors: ['45', '49' ] },
  { category: 'subtraction', question: '100 − 37 = ?', correctAnswer: '63', distractors: ['57', '67' ] },

  // ─── Multiplication (12) ────────────────────────────────────────────────────
  { category: 'multiplication', question: '3 × 4 = ?',  correctAnswer: '12', distractors: ['8',  '24'] },
  { category: 'multiplication', question: '6 × 7 = ?',  correctAnswer: '42', distractors: ['36', '48'] },
  { category: 'multiplication', question: '8 × 9 = ?',  correctAnswer: '72', distractors: ['63', '81'] },
  { category: 'multiplication', question: '5 × 6 = ?',  correctAnswer: '30', distractors: ['25', '36'] },
  { category: 'multiplication', question: '4 × 7 = ?',  correctAnswer: '28', distractors: ['24', '32'] },
  { category: 'multiplication', question: '9 × 6 = ?',  correctAnswer: '54', distractors: ['48', '63'] },
  { category: 'multiplication', question: '7 × 8 = ?',  correctAnswer: '56', distractors: ['48', '63'] },
  { category: 'multiplication', question: '3 × 9 = ?',  correctAnswer: '27', distractors: ['24', '30'] },
  { category: 'multiplication', question: '6 × 4 = ?',  correctAnswer: '24', distractors: ['18', '28'] },
  { category: 'multiplication', question: '12 × 3 = ?', correctAnswer: '36', distractors: ['30', '42'] },
  { category: 'multiplication', question: '15 × 4 = ?', correctAnswer: '60', distractors: ['54', '64'] },
  { category: 'multiplication', question: '8² = ?',     correctAnswer: '64', distractors: ['56', '72'] },

  // ─── Division (6) ────────────────────────────────────────────────────────────
  { category: 'division', question: '36 ÷ 4 = ?', correctAnswer: '9', distractors: ['7', '12'] },
  { category: 'division', question: '48 ÷ 6 = ?', correctAnswer: '8', distractors: ['6', '9'  ] },
  { category: 'division', question: '63 ÷ 7 = ?', correctAnswer: '9', distractors: ['7', '8'  ] },
  { category: 'division', question: '56 ÷ 8 = ?', correctAnswer: '7', distractors: ['6', '9'  ] },
  { category: 'division', question: '72 ÷ 9 = ?', correctAnswer: '8', distractors: ['7', '9'  ] },
  { category: 'division', question: '45 ÷ 5 = ?', correctAnswer: '9', distractors: ['7', '8'  ] },
]

function shuffle(arr) {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

let lastQuestion = ''

export function getRandomQuestion(category = 'all') {
  const pool = category === 'all'
    ? rawQuestions
    : rawQuestions.filter(q => q.category === category)

  const source = pool.length > 0 ? pool : rawQuestions

  let q, attempts = 0
  do {
    q = source[Math.floor(Math.random() * source.length)]
    attempts++
  } while (q.question === lastQuestion && source.length > 1 && attempts < 10)

  lastQuestion = q.question
  const answers = shuffle([q.correctAnswer, ...q.distractors])
  return { question: q.question, answers, correctAnswer: q.correctAnswer }
}
