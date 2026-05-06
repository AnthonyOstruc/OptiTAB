const rawQuestions = [
  // ─── Addition (16) ────────────────────────────────────────────────────────
  { category: 'addition', question: '7 + 8 = ?',    correctAnswer: '15', distractors: ['13', '16'] },
  { category: 'addition', question: '14 + 9 = ?',   correctAnswer: '23', distractors: ['21', '25'] },
  { category: 'addition', question: '26 + 7 = ?',   correctAnswer: '33', distractors: ['31', '35'] },
  { category: 'addition', question: '45 + 18 = ?',  correctAnswer: '63', distractors: ['61', '65'] },
  { category: 'addition', question: '37 + 25 = ?',  correctAnswer: '62', distractors: ['60', '64'] },
  { category: 'addition', question: '53 + 29 = ?',  correctAnswer: '82', distractors: ['80', '84'] },
  { category: 'addition', question: '8 + 6 = ?',    correctAnswer: '14', distractors: ['12', '16'] },
  { category: 'addition', question: '17 + 8 = ?',   correctAnswer: '25', distractors: ['23', '27'] },
  { category: 'addition', question: '34 + 16 = ?',  correctAnswer: '50', distractors: ['48', '52'] },
  { category: 'addition', question: '48 + 23 = ?',  correctAnswer: '71', distractors: ['69', '73'] },
  { category: 'addition', question: '56 + 38 = ?',  correctAnswer: '94', distractors: ['92', '96'] },
  { category: 'addition', question: '19 + 13 = ?',  correctAnswer: '32', distractors: ['30', '34'] },
  { category: 'addition', question: '28 + 35 = ?',  correctAnswer: '63', distractors: ['61', '65'] },
  { category: 'addition', question: '41 + 27 = ?',  correctAnswer: '68', distractors: ['66', '70'] },
  { category: 'addition', question: '65 + 27 = ?',  correctAnswer: '92', distractors: ['89', '95'] },
  { category: 'addition', question: '73 + 19 = ?',  correctAnswer: '92', distractors: ['88', '96'] },

  // ─── Subtraction (16) ─────────────────────────────────────────────────────
  { category: 'subtraction', question: '15 − 7 = ?',   correctAnswer: '8',  distractors: ['6',  '9'  ] },
  { category: 'subtraction', question: '24 − 9 = ?',   correctAnswer: '15', distractors: ['13', '17' ] },
  { category: 'subtraction', question: '40 − 13 = ?',  correctAnswer: '27', distractors: ['25', '29' ] },
  { category: 'subtraction', question: '71 − 28 = ?',  correctAnswer: '43', distractors: ['41', '45' ] },
  { category: 'subtraction', question: '82 − 35 = ?',  correctAnswer: '47', distractors: ['45', '49' ] },
  { category: 'subtraction', question: '100 − 37 = ?', correctAnswer: '63', distractors: ['57', '67' ] },
  { category: 'subtraction', question: '20 − 8 = ?',   correctAnswer: '12', distractors: ['10', '14' ] },
  { category: 'subtraction', question: '30 − 14 = ?',  correctAnswer: '16', distractors: ['14', '18' ] },
  { category: 'subtraction', question: '45 − 17 = ?',  correctAnswer: '28', distractors: ['26', '30' ] },
  { category: 'subtraction', question: '60 − 23 = ?',  correctAnswer: '37', distractors: ['35', '39' ] },
  { category: 'subtraction', question: '90 − 46 = ?',  correctAnswer: '44', distractors: ['42', '46' ] },
  { category: 'subtraction', question: '64 − 29 = ?',  correctAnswer: '35', distractors: ['33', '37' ] },
  { category: 'subtraction', question: '88 − 45 = ?',  correctAnswer: '43', distractors: ['41', '45' ] },
  { category: 'subtraction', question: '97 − 52 = ?',  correctAnswer: '45', distractors: ['43', '47' ] },
  { category: 'subtraction', question: '75 − 38 = ?',  correctAnswer: '37', distractors: ['33', '41' ] },
  { category: 'subtraction', question: '53 − 18 = ?',  correctAnswer: '35', distractors: ['31', '39' ] },

  // ─── Multiplication (24) ──────────────────────────────────────────────────
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
  { category: 'multiplication', question: '2 × 7 = ?',  correctAnswer: '14', distractors: ['12', '16'] },
  { category: 'multiplication', question: '4 × 8 = ?',  correctAnswer: '32', distractors: ['28', '36'] },
  { category: 'multiplication', question: '5 × 9 = ?',  correctAnswer: '45', distractors: ['40', '50'] },
  { category: 'multiplication', question: '9 × 4 = ?',  correctAnswer: '36', distractors: ['32', '40'] },
  { category: 'multiplication', question: '11 × 5 = ?', correctAnswer: '55', distractors: ['50', '60'] },
  { category: 'multiplication', question: '6 × 8 = ?',  correctAnswer: '48', distractors: ['42', '54'] },
  { category: 'multiplication', question: '7 × 7 = ?',  correctAnswer: '49', distractors: ['42', '56'] },
  { category: 'multiplication', question: '9 × 9 = ?',  correctAnswer: '81', distractors: ['72', '90'] },
  { category: 'multiplication', question: '13 × 4 = ?', correctAnswer: '52', distractors: ['48', '56'] },
  { category: 'multiplication', question: '11 × 6 = ?', correctAnswer: '66', distractors: ['60', '72'] },
  { category: 'multiplication', question: '7 × 11 = ?', correctAnswer: '77', distractors: ['70', '84'] },
  { category: 'multiplication', question: '6² = ?',     correctAnswer: '36', distractors: ['30', '42'] },

  // ─── Division (14) ────────────────────────────────────────────────────────
  { category: 'division', question: '36 ÷ 4 = ?', correctAnswer: '9',  distractors: ['7',  '12'] },
  { category: 'division', question: '48 ÷ 6 = ?', correctAnswer: '8',  distractors: ['6',  '9' ] },
  { category: 'division', question: '63 ÷ 7 = ?', correctAnswer: '9',  distractors: ['7',  '8' ] },
  { category: 'division', question: '56 ÷ 8 = ?', correctAnswer: '7',  distractors: ['6',  '9' ] },
  { category: 'division', question: '72 ÷ 9 = ?', correctAnswer: '8',  distractors: ['7',  '9' ] },
  { category: 'division', question: '45 ÷ 5 = ?', correctAnswer: '9',  distractors: ['7',  '8' ] },
  { category: 'division', question: '24 ÷ 4 = ?', correctAnswer: '6',  distractors: ['4',  '8' ] },
  { category: 'division', question: '32 ÷ 8 = ?', correctAnswer: '4',  distractors: ['3',  '6' ] },
  { category: 'division', question: '54 ÷ 9 = ?', correctAnswer: '6',  distractors: ['5',  '7' ] },
  { category: 'division', question: '42 ÷ 7 = ?', correctAnswer: '6',  distractors: ['5',  '8' ] },
  { category: 'division', question: '64 ÷ 8 = ?', correctAnswer: '8',  distractors: ['6',  '10'] },
  { category: 'division', question: '81 ÷ 9 = ?', correctAnswer: '9',  distractors: ['7',  '12'] },
  { category: 'division', question: '35 ÷ 5 = ?', correctAnswer: '7',  distractors: ['5',  '9' ] },
  { category: 'division', question: '28 ÷ 4 = ?', correctAnswer: '7',  distractors: ['5',  '9' ] },

  // ─── Limites (15) ─────────────────────────────────────────────────────────
  { category: 'limits', question: 'lim(x→∞) 1/x = ?',          correctAnswer: '0',   distractors: ['1',   '+∞'] },
  { category: 'limits', question: 'lim(x→0) sin(x)/x = ?',     correctAnswer: '1',   distractors: ['0',   '+∞'] },
  { category: 'limits', question: 'lim(x→0) (eˣ−1)/x = ?',    correctAnswer: '1',   distractors: ['0',   'e'  ] },
  { category: 'limits', question: 'lim(x→+∞) eˣ = ?',          correctAnswer: '+∞',  distractors: ['0',   '1'  ] },
  { category: 'limits', question: 'lim(x→−∞) eˣ = ?',          correctAnswer: '0',   distractors: ['-∞',  '1'  ] },
  { category: 'limits', question: 'lim(x→+∞) ln(x) = ?',       correctAnswer: '+∞',  distractors: ['0',   '1'  ] },
  { category: 'limits', question: 'lim(x→0⁺) ln(x) = ?',       correctAnswer: '-∞',  distractors: ['0',   '1'  ] },
  { category: 'limits', question: 'lim(x→∞) x/eˣ = ?',         correctAnswer: '0',   distractors: ['1',   '+∞'] },
  { category: 'limits', question: 'lim(x→∞) ln(x)/x = ?',      correctAnswer: '0',   distractors: ['1',   '+∞'] },
  { category: 'limits', question: 'lim(x→0) tan(x)/x = ?',     correctAnswer: '1',   distractors: ['0',   '∞'  ] },
  { category: 'limits', question: 'lim(x→2) (x²−4)/(x−2)=?',  correctAnswer: '4',   distractors: ['0',   '2'  ] },
  { category: 'limits', question: 'lim(x→∞) (2x+1)/(x+3)=?',  correctAnswer: '2',   distractors: ['0',   '1'  ] },
  { category: 'limits', question: 'lim(x→∞) (3x²+1)/(x²)=?',  correctAnswer: '3',   distractors: ['0',   '+∞'] },
  { category: 'limits', question: 'lim(x→0⁺) x·ln(x) = ?',    correctAnswer: '0',   distractors: ['1',   '-∞'] },
  { category: 'limits', question: 'lim(x→1) (x²−1)/(x−1)=?',  correctAnswer: '2',   distractors: ['0',   '1'  ] },

  // ─── Dérivées (15) ────────────────────────────────────────────────────────
  { category: 'derivatives', question: "(x²)' = ?",           correctAnswer: '2x',      distractors: ['x',     '2'      ] },
  { category: 'derivatives', question: "(x³)' = ?",           correctAnswer: '3x²',     distractors: ['x²',    '3x'     ] },
  { category: 'derivatives', question: "(sin x)' = ?",        correctAnswer: 'cos x',   distractors: ['-cos x','sin x'  ] },
  { category: 'derivatives', question: "(cos x)' = ?",        correctAnswer: '-sin x',  distractors: ['sin x', '-cos x' ] },
  { category: 'derivatives', question: "(eˣ)' = ?",           correctAnswer: 'eˣ',      distractors: ['xeˣ',   'eˣ⁻¹'  ] },
  { category: 'derivatives', question: "(ln x)' = ?",         correctAnswer: '1/x',     distractors: ['ln x',  '1/x²'  ] },
  { category: 'derivatives', question: "(√x)' = ?",           correctAnswer: '1/(2√x)', distractors: ['1/√x',  '2√x'   ] },
  { category: 'derivatives', question: "(1/x)' = ?",          correctAnswer: '-1/x²',   distractors: ['1/x²',  '-1/x'  ] },
  { category: 'derivatives', question: "(tan x)' = ?",        correctAnswer: '1/cos²x', distractors: ['cos²x', 'tan²x' ] },
  { category: 'derivatives', question: "(3x+1)' = ?",         correctAnswer: '3',       distractors: ['1',     '3x'    ] },
  { category: 'derivatives', question: "(x²+1)' en x=2 = ?",  correctAnswer: '4',       distractors: ['5',     '2'     ] },
  { category: 'derivatives', question: "(2eˣ)' = ?",          correctAnswer: '2eˣ',     distractors: ['2xeˣ',  'eˣ'    ] },
  { category: 'derivatives', question: "(x·ln x)' = ?",       correctAnswer: '1+ln x',  distractors: ['ln x',  '1/x'   ] },
  { category: 'derivatives', question: "(x⁴)' = ?",           correctAnswer: '4x³',     distractors: ['4x',    '3x³'   ] },
  { category: 'derivatives', question: "(5x²−3x)' = ?",       correctAnswer: '10x−3',   distractors: ['5x−3',  '10x+3' ] },

  // ─── Intégrales (15) ──────────────────────────────────────────────────────
  { category: 'integrals', question: '∫ 1 dx = ?',         correctAnswer: 'x',      distractors: ['0',     '1'    ] },
  { category: 'integrals', question: '∫ x dx = ?',         correctAnswer: 'x²/2',   distractors: ['x²',    '2x'   ] },
  { category: 'integrals', question: '∫ x² dx = ?',        correctAnswer: 'x³/3',   distractors: ['x³',    'x²/2' ] },
  { category: 'integrals', question: '∫ cos x dx = ?',     correctAnswer: 'sin x',  distractors: ['-sin x','cos x' ] },
  { category: 'integrals', question: '∫ sin x dx = ?',     correctAnswer: '-cos x', distractors: ['cos x', 'sin x' ] },
  { category: 'integrals', question: '∫ eˣ dx = ?',        correctAnswer: 'eˣ',     distractors: ['xeˣ',   'eˣ/x' ] },
  { category: 'integrals', question: '∫ 1/x dx = ?',       correctAnswer: 'ln|x|',  distractors: ['1/x²',  'ln x²'] },
  { category: 'integrals', question: '∫₀¹ x dx = ?',       correctAnswer: '1/2',    distractors: ['1',     '0'    ] },
  { category: 'integrals', question: '∫₀¹ x² dx = ?',      correctAnswer: '1/3',    distractors: ['1/2',   '1'    ] },
  { category: 'integrals', question: '∫₀^π sin x dx = ?',  correctAnswer: '2',      distractors: ['0',     '1'    ] },
  { category: 'integrals', question: '∫₀² 2x dx = ?',      correctAnswer: '4',      distractors: ['2',     '8'    ] },
  { category: 'integrals', question: '∫₁^e 1/x dx = ?',    correctAnswer: '1',      distractors: ['e',     '0'    ] },
  { category: 'integrals', question: '∫ 2x dx = ?',        correctAnswer: 'x²',     distractors: ['2x²',   'x²/2' ] },
  { category: 'integrals', question: '∫₀² x² dx = ?',      correctAnswer: '8/3',    distractors: ['4/3',   '2'    ] },
  { category: 'integrals', question: '∫₀¹ eˣ dx = ?',      correctAnswer: 'e−1',    distractors: ['e',     '1'    ] },

  // ─── Suites (15) ──────────────────────────────────────────────────────────
  { category: 'sequences', question: 'uₙ=2n+1 : u₄ = ?',              correctAnswer: '9',  distractors: ['7',  '11'] },
  { category: 'sequences', question: 'uₙ=3n−1 : u₃ = ?',              correctAnswer: '8',  distractors: ['6',  '10'] },
  { category: 'sequences', question: 'uₙ=n² : u₅ = ?',                correctAnswer: '25', distractors: ['10', '20'] },
  { category: 'sequences', question: '1,1,2,3,5,? (Fibonacci)',        correctAnswer: '8',  distractors: ['7',  '9' ] },
  { category: 'sequences', question: 'u₀=1, q=3 (géo) : u₃ = ?',     correctAnswer: '27', distractors: ['9',  '81'] },
  { category: 'sequences', question: 'u₀=2, q=2 (géo) : u₄ = ?',     correctAnswer: '32', distractors: ['16', '64'] },
  { category: 'sequences', question: '1, 4, 7, 10, … : raison = ?',   correctAnswer: '3',  distractors: ['2',  '4' ] },
  { category: 'sequences', question: '1, 2, 4, 8, … : raison = ?',    correctAnswer: '2',  distractors: ['3',  '4' ] },
  { category: 'sequences', question: 'Somme 1+2+…+10 = ?',            correctAnswer: '55', distractors: ['45', '50'] },
  { category: 'sequences', question: 'uₙ=2ⁿ : u₅ = ?',               correctAnswer: '32', distractors: ['16', '64'] },
  { category: 'sequences', question: 'u₀=3, r=5 (arith) : u₃ = ?',   correctAnswer: '18', distractors: ['15', '21'] },
  { category: 'sequences', question: 'uₙ=n²+n : u₄ = ?',             correctAnswer: '20', distractors: ['16', '24'] },
  { category: 'sequences', question: 'lim uₙ=n/(n+1) = ?',            correctAnswer: '1',  distractors: ['0',  '+∞'] },
  { category: 'sequences', question: 'u₀=100, r=0.9 : u₁ = ?',       correctAnswer: '90', distractors: ['91', '99'] },
  { category: 'sequences', question: 'Somme 1+2+…+n = ?',             correctAnswer: 'n(n+1)/2', distractors: ['n²/2', 'n(n-1)/2'] },
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
