"""Sources éditoriales de la 6e : format du site et calcul exact."""
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT.parents[2]
REPO = FRONT.parent
CATS = [('Découverte', 'easy'), ('Entraînement', 'medium'), ('Problème', 'hard')]


def n(value):
    """Nombre exact en écriture française, sans arrondi silencieux."""
    v = Fraction(value)
    if v.denominator == 1:
        return str(v.numerator)
    d = v.denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    if d == 1:
        from decimal import Decimal, localcontext
        with localcontext() as ctx:
            ctx.prec = 40
            return format(Decimal(v.numerator) / Decimal(v.denominator), 'f').rstrip('0').rstrip('.').replace('.', '{,}')
    return rf'\frac{{{v.numerator}}}{{{v.denominator}}}'


def m(tex):
    return '$' + tex + '$'


def dm(text):
    return re.sub(r'\$([^$\n]+)\$', lambda x: '$\\displaystyle ' + x[1] + '$' if not x[1].startswith('\\displaystyle') else x[0], text)


@dataclass
class Question:
    texte: str
    methode: str
    resultat: str
    calcul: str = ''
    controle: str = ''


def q(texte, methode, resultat, calcul='', controle=''):
    return Question(texte, methode, resultat, calcul, controle)


@dataclass
class Exercice:
    titre: str
    intro: str
    questions: list
    conseil: str
    figure: dict = field(default_factory=dict)
    correction_figure: bool = False


def ex(titre, intro, questions, conseil, figure=None, correction_figure=False):
    assert len(questions) >= 6, titre
    assert all(x.methode and x.resultat for x in questions), titre
    return Exercice(titre, intro, questions, conseil, figure or {}, correction_figure)


def render_exercice(c, e, cat, diff, indice, image_names):
    br = '$\\\\$'
    lines = [f'=== {cat} - {c.titre} - {indice}. {e.titre}', f'Difficulté: {diff}']
    if image_names:
        lines.append('Images: ' + ', '.join(image_names))
    lines += ['', 'Énoncé: ' + dm(e.intro)]
    if image_names:
        lines += ['[IMAGE_1]']
    for j, question in enumerate(e.questions, 1):
        lines += [br, f'**Question {j} : {dm(question.texte)}**']
    lines += ['', 'Étapes:', '']
    for j, question in enumerate(e.questions, 1):
        lines += [f'**Question {j} : {dm(question.texte)}**', '', '    ● **Méthode :** ' + dm(question.methode), '    ' + br]
        if question.calcul:
            lines += ['    ● **Étape 1 :** ' + dm(question.calcul), '    ' + br]
        lines += ['    ● **Résultat :** ' + dm(question.resultat), '    ' + br, '']
    if len(image_names) > 1:
        lines += ['[IMAGE_2]', '']
    lines += ['    ● 💡 **À retenir :** ' + dm(e.conseil), '', 'Solution:']
    for j, question in enumerate(e.questions, 1):
        lines += [f'{j}. {dm(question.resultat)}', br]
    return '\n'.join(lines).rstrip() + '\n'
