"""Contrôles de structure et de calcul des données utilisées dans le livre."""
from pathlib import Path
import json
import math
import re
import sympy as s

ROOT = Path(__file__).resolve().parent
(ROOT/'build').mkdir(exist_ok=True)
x, n, m, h = s.symbols('x n m h', real=True)
checks = []

def equal(name, left, right):
    assert s.simplify(left - right) == 0, name
    checks.append(name)

def check(name, condition):
    assert condition, name
    checks.append(name)

for chapter in sorted((ROOT / 'chapitres').glob('*.tex')):
    body = chapter.read_text(encoding='utf-8')
    answers = (ROOT / 'corriges' / chapter.name).read_text(encoding='utf-8')
    titles = re.findall(r'\\begin\{exercice\}\[(\d)\]\{([^\n]+)\}', body)
    corrections = re.findall(r'\\begin\{corrige\}\{(\d+)\}\{([^\n]+)\}', answers)
    check(f'{chapter.stem}: 15 exercices et 15 corrigés', len(titles) == len(corrections) == 15)
    check(f'{chapter.stem}: titres et numéros concordants',
          [title for _, title in titles] == [title for _, title in corrections]
          and [int(number) for number, _ in corrections] == list(range(1, 16)))
    check(f'{chapter.stem}: progression 5/6/4', [int(level) for level, _ in titles] == [1]*5 + [2]*6 + [3]*4)

equal('1.6 formes du trinôme', x*x-6*x+5, (x-3)**2-4)
equal('1.7 différence des paraboles', (x*x-4*x+3)-(-x*x+2*x+3), 2*x*(x-3))
equal('1.9 sommet', (x+2)*(x-4), (x-1)**2-9)
equal('1.12 aire du jardin', x*(40-2*x), -2*(x-10)**2+200)
equal('1.13 bénéfice', x*(50-s.Rational(1,5)*x)-(10*x+500), -s.Rational(1,5)*(x-100)**2+1500)
equal('1.14 hauteur canonique', -5*x*x+10*x+1, -5*(x-1)**2+6)
equal('1.15 discriminant', (-2*m)**2-4*(m+2), 4*(m-2)*(m+1))
equal('1.15 point commun', (x*x-2*m*x+m+2).subs(x,s.Rational(1,2)), s.Rational(9,4))
equal('2.1 différence', ((n+1)**2-3*(n+1)+2)-(n*n-3*n+2), 2*n-2)
equal('2.8 différence rationnelle', (n+2)/(n+3)-(n+1)/(n+2), 1/((n+2)*(n+3)))
check('2.7 sommes', sum(range(4,62,3)) == 650 and sum(3*2**k for k in range(8)) == 765 and sum(2*k+1 for k in range(3,11)) == 112)
check('2.9 seuil demi-raison', 16*.5**7 >= .1 > 16*.5**8)
check('2.11 seuil épargne', 1000*1.05**8 < 1500 <= 1000*1.05**9)
check('2.12 sièges et recette', sum(2*k+16 for k in range(1,21)) == 740 and 9*270+12*470 == 8070)
check('2.12 seuil capacité', 24*(24+17) < 1000 <= 25*(25+17))
equal('2.13 suite auxiliaire', s.Rational(4,5)*(x+30)+6-30, s.Rational(4,5)*x)
check('2.13 seuil traitement', 30-20*.8**10 < 28 <= 30-20*.8**11)
check('2.14 total contrats', math.isclose(sum(24000*1.04**k for k in range(10)),288146.5709510064))
check('2.14 premier dépassement', all(24000*1.04**k <= 24000+1000*k for k in range(1,4)) and 24000*1.04**4 > 28000)
check('2.15 allumettes', (3*25**2+5*25)//2 == 1000 and (3*26**2+5*26)//2 > 1000)
equal('3.6 taux du carré', ((x+h)**2-x*x)/h, 2*x+h)
equal('3.7 produit', s.diff((x*x+1)*(3*x-2),x), 9*x*x-4*x+3)
equal('3.7 produit développé', (x-1)**2*(x+2), x**3-3*x+2)
equal('3.8 quotient', s.diff(x/(x*x+1),x), (1-x*x)/(x*x+1)**2)
equal('3.14 écart tangente', s.Rational(3,2)*x*x-2*x+1-(4*x-5), s.Rational(3,2)*(x-2)**2)
C = s.Rational(2,100)*x**3-s.Rational(6,10)*x*x+10*x+100
equal('3.15 accroissement exact', C.subs(x,20+h)-C.subs(x,20), 10*h+s.Rational(6,10)*h*h+s.Rational(2,100)*h**3)
equal('4.6 dérivée factorisée', s.diff(x**3-3*x*x-9*x+5,x), 3*(x+1)*(x-3))
check('4.6 valeurs des extremums', [(k**3-3*k*k-9*k+5) for k in [-3,-1,3,5]] == [-22,10,-22,10])
equal('4.7 inégalité', x+4/x-4, (x-2)**2/x)
check('4.11 optimum entier', max(range(21),key=lambda k:-2*k*k+27*k-40) == 7)
equal('4.12 volume boîte', s.diff(x*(24-2*x)**2,x), 12*(x-4)*(x-12))
equal('4.13 aire rectangle', s.diff(2*x*(9-x*x),x), 18-6*x*x)
equal('4.14 volume cylindre', s.diff(s.pi*x*x*(20-x),x), s.pi*x*(40-3*x))
equal('4.15 distance carrée', x*x+(x*x-2)**2, x**4-3*x*x+4)
equal('4.15 minimum distance carrée', (x**4-3*x*x+4).subs(x,s.sqrt(s.Rational(3,2))), s.Rational(7,4))
equal('5.7 dérivée produit', s.diff((x+1)*s.exp(-x),x), -x*s.exp(-x))
equal('5.8 carré', s.exp(2*x)-2*s.exp(x), (s.exp(x)-1)**2-1)
equal('5.9 dérivée quotient', s.diff(s.exp(x)/(1+s.exp(x)),x), s.exp(x)/(1+s.exp(x))**2)
check('5.11 Euler', math.isclose((1+1/2)**2,2.25) and math.isclose((1+1/10)**10,2.5937424601))
check('5.12 seuil refroidissement', 20+70*math.exp(-1.2)>40>=20+70*math.exp(-1.3))
equal('5.13 dérivée concentration', s.diff(8*x*s.exp(-x/2),x), 4*(2-x)*s.exp(-x/2))
equal('5.15 dérivée du gain', s.diff(100*(x+1)*s.exp(-x/2),x), 50*(1-x)*s.exp(-x/2))
check('5.15 durées entières favorables', [k for k in range(1,7) if 100*(k+1)*math.exp(-k/2)>100] == [1,2])

report = {'checks_passed':len(checks), 'checks':checks}
(ROOT/'build/verification-mathematique.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(checks)} contrôles de structure et de calcul réussis.')
